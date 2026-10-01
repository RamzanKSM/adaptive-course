package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpServer;
import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;

import java.net.InetSocketAddress;
import java.net.SocketException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static org.junit.jupiter.api.Assertions.*;

class PistonCodeRunnerHttpTest {
  @Test void combinesHarnessAndSolutionIntoSingleSourceFile() {
    String combined=PistonCodeRunner.combinedSource(
        "import java.util.List;\npublic class Solution { static int answer() { return 42; } }",
        "import static java.lang.System.out;\npublic class TestHarness { public static void main(String[] a) { out.print(Solution.answer()); } }");
    assertTrue(combined.startsWith("import static java.lang.System.out;\nimport java.util.List;"));
    assertTrue(combined.indexOf("class TestHarness") < combined.indexOf("class Solution"));
    assertFalse(combined.contains("public class Solution"));
  }

  @Test void encodesNonAsciiJavaSourceAsUnicodeEscapes() {
    assertEquals("System.out.print(\\u0421\\u0443\\u043F\\u044C\\u044F\\u043D);",
        PistonCodeRunner.javaUnicodeEscapes("System.out.print(\"Супьян\");").replace("\"", ""));
    String combined=PistonCodeRunner.combinedSource("public class Solution { static String value() { return \"Супьян\"; } }",
        "public class TestHarness { static String expected() { return \"Привет\"; } }");
    assertTrue(combined.contains("\\u0421\\u0443\\u043F\\u044C\\u044F\\u043D"));
    assertTrue(combined.contains("\\u041F\\u0440\\u0438\\u0432\\u0435\\u0442"));
  }

  @Test void statusUsesPlainHttp11WithoutH2cUpgrade() throws Exception {
    AtomicBoolean h2cUpgrade = new AtomicBoolean();
    AtomicBoolean http11 = new AtomicBoolean(true);
    AtomicBoolean singleHarnessFile = new AtomicBoolean();
    ObjectMapper json = new ObjectMapper();
    HttpServer server;
    try {
      server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
    } catch (SocketException e) {
      Assumptions.assumeTrue(false, "test sandbox does not permit a local TCP listener");
      return;
    }
    server.createContext("/api/v2/", exchange -> {
      if(!"HTTP/1.1".equals(exchange.getProtocol())) http11.set(false);
      if(exchange.getRequestHeaders().containsKey("Upgrade") || exchange.getRequestHeaders().containsKey("HTTP2-Settings")) h2cUpgrade.set(true);
      String body;
      if(exchange.getRequestURI().getPath().endsWith("/runtimes")) {
        body="[{\"language\":\"java\",\"version\":\"15.0.2\"}]";
      } else {
        var request=json.readTree(exchange.getRequestBody().readAllBytes());
        var file=request.path("files").path(0);
        String content=file.path("content").asText();
        if("TestHarness".equals(file.path("name").asText())) {
          singleHarnessFile.set(request.path("files").size()==1 && content.indexOf("class TestHarness") < content.indexOf("class Solution") && !content.contains("public class Solution"));
          Matcher marker=Pattern.compile("__ADAPTIVE_PASS_[A-Za-z0-9_-]+__").matcher(content);
          assertTrue(marker.find(), "combined harness must contain the generated pass marker");
          body="{\"compile\":null,\"run\":{\"code\":0,\"stdout\":\""+marker.group()+"\"}}";
        } else {
          body="{\"compile\":null,\"run\":{\"code\":0,\"stdout\":\"READY\"}}";
        }
      }
      byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
      exchange.sendResponseHeaders(200, bytes.length);
      exchange.getResponseBody().write(bytes);
      exchange.close();
    });
    server.start();
    try {
      PistonCodeRunner runner = new PistonCodeRunner(new ObjectMapper(), "http://127.0.0.1:" + server.getAddress().getPort(), "", 1_000, 1_000, 64_000_000, 64_000_000);
      assertTrue(runner.status().available());
      assertTrue(runner.run("public class Solution { static int answer() { return 1; } }", "public class TestHarness { public static void main(String[] a) { if (Solution.answer()!=1) throw new AssertionError(); System.out.print(\"{{PASS_MARKER}}\"); } }").passed());
      assertTrue(http11.get());
      assertFalse(h2cUpgrade.get());
      assertTrue(singleHarnessFile.get());
    } finally {
      server.stop(0);
    }
  }

  @Test void reportsCompilerAndResourceFailuresAndEscapesCyrillicSource() throws Exception {
    ObjectMapper json = new ObjectMapper();
    HttpServer server;
    try { server=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0); }
    catch(SocketException e) { Assumptions.assumeTrue(false,"test sandbox does not permit a local TCP listener"); return; }
    AtomicBoolean cyrillicEscaped=new AtomicBoolean();
    server.createContext("/api/v2/execute", exchange -> {
      var request=json.readTree(exchange.getRequestBody().readAllBytes());
      String source=request.path("files").path(0).path("content").asText();
      String response;
      if(source.contains("HealthCheck")) response="{\"compile\":null,\"run\":{\"code\":0,\"stdout\":\"READY\"}}";
      else if(source.contains("doesNotExist")) response="{\"compile\":null,\"run\":{\"code\":1,\"stderr\":\"Main.java:1: error: cannot find symbol\\n  doesNotExist();\\n  ^\\ncompilation failed\"}}";
      else if(source.contains("compileStageTimeout")) response="{\"compile\":{\"code\":null,\"status\":\"TO\",\"message\":\"Time limit exceeded (wall clock)\"}}";
      else if(source.contains("compileStageMemory")) response="{\"compile\":{\"code\":null,\"status\":\"RE\",\"message\":\"Memory limit exceeded\"}}";
      else if(source.contains("loopForever")) response="{\"compile\":null,\"run\":{\"code\":null,\"signal\":\"SIGKILL\",\"status\":\"TO\",\"message\":\"Time limit exceeded (wall clock)\"}}";
      else if(source.contains("useLotsMemory")) response="{\"compile\":null,\"run\":{\"code\":137,\"status\":\"RE\",\"stderr\":\"Killed\",\"message\":\"Exited with error status 137\"}}";
      else { cyrillicEscaped.set(source.contains("\\u0421\\u0443\\u043F\\u044C\\u044F\\u043D")&&source.contains("\\u041F\\u0440\\u0438\\u0432\\u0435\\u0442")); response="{\"compile\":null,\"run\":{\"code\":1,\"stderr\":\"java.lang.AssertionError\"}}"; }
      byte[] bytes=response.getBytes(StandardCharsets.UTF_8); exchange.sendResponseHeaders(200,bytes.length); exchange.getResponseBody().write(bytes); exchange.close();
    });
    server.start();
    try {
      PistonCodeRunner runner=new PistonCodeRunner(json,"http://127.0.0.1:"+server.getAddress().getPort(),"15.0.2",1_000,1_000,32_000_000,32_000_000);
      String harness="public class TestHarness { public static void main(String[] a) { if (!Solution.answer().equals(\"Привет\")) throw new AssertionError(); System.out.print(\"{{PASS_MARKER}}\"); } }";
      var wrongCyrillic=runner.run("public class Solution { static String answer() { return \"Супьян\"; } }",harness);
      assertFalse(wrongCyrillic.passed()); assertEquals("Неверный вывод программы.",wrongCyrillic.output()); assertTrue(cyrillicEscaped.get());
      var compiler=runner.run("public class Solution { static void doesNotExist() {} }",harness);
      assertFalse(compiler.passed()); assertTrue(compiler.output().startsWith("Ошибка компиляции Java:")); assertTrue(compiler.output().contains("cannot find symbol"));
      assertEquals("Превышен лимит времени выполнения.",runner.run("public class Solution { static void compileStageTimeout() {} }",harness).output());
      assertEquals("Превышен лимит памяти.",runner.run("public class Solution { static void compileStageMemory() {} }",harness).output());
      assertEquals("Превышен лимит времени выполнения.",runner.run("public class Solution { static void loopForever() {} }",harness).output());
      assertEquals("Превышен лимит памяти.",runner.run("public class Solution { static void useLotsMemory() {} }",harness).output());
    } finally { server.stop(0); }
  }
}
