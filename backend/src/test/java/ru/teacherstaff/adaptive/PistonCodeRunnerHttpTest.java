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
          body="{\"compile\":{\"code\":0,\"output\":\"\"},\"run\":{\"code\":0,\"output\":\""+marker.group()+"\"}}";
        } else {
          body="{\"compile\":{\"code\":0,\"output\":\"\"},\"run\":{\"code\":0,\"output\":\"READY\"}}";
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
}
