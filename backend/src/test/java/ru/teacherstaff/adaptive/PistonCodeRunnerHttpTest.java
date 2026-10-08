package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpServer;
import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;

import java.net.InetSocketAddress;
import java.net.SocketException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.BiFunction;
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

  @Test void consoleSourceKeepsTheStudentsLineNumbersAndStartsWithTheLauncher() {
    String student="public class Solution {\n    public static void main(String[] args) {\n        System.out.println(\"Итого\");\n    }\n}\n";
    String source=PistonCodeRunner.consoleSource(student);
    assertTrue(source.startsWith("public class ConsoleRunner"), "single-file Java runs the first class: the launcher, not Solution");
    assertTrue(source.contains("Solution.main(new String[0])"));
    var lines=source.lines().toList(); var original=student.lines().toList();
    assertEquals(original.size(),lines.size(),"no lines are added");
    for(int i=1;i<original.size();i++) assertEquals(PistonCodeRunner.javaUnicodeEscapes(original.get(i)),lines.get(i),"line "+(i+1)+" is unchanged");
    String withImport=PistonCodeRunner.consoleSource("import java.util.Scanner;\npublic class Solution {\n}\n");
    assertTrue(withImport.startsWith("import java.util.Scanner; public class ConsoleRunner"), "imports stay first, the launcher follows on the same line: "+withImport);
    assertEquals(3,withImport.lines().count());
  }

  @Test void aFailedJavaCheckExplainsItself() {
    assertEquals("Тест 3: неверный ответ",PistonCodeRunner.assertionMessage("Exception in thread \"main\" java.lang.AssertionError: Тест 3: неверный ответ\n\tat TestHarness.main(TestHarness.java:9)"));
    assertNull(PistonCodeRunner.assertionMessage("Exception in thread \"main\" java.lang.AssertionError\n\tat TestHarness.main(TestHarness.java:9)"),"no message — the generic text is used");
  }

  @Test void consoleDiagnosticsUseTheStudentsFileNameAndReadableText() {
    String jvm="Exception in thread \"main\" java.lang.ArithmeticException: / by zero\n\tat Solution.main(ConsoleRunner.java:4)\n\tat ConsoleRunner.main(ConsoleRunner.java:6)";
    assertEquals("Exception in thread \"main\" java.lang.ArithmeticException: / by zero\n\tat Solution.main(Solution.java:4)",PistonCodeRunner.javaConsoleDiagnostic(jvm));
    assertEquals("Solution.java:3: error: ';' expected\n    System.out.println(\"Привет\")",
        PistonCodeRunner.javaConsoleDiagnostic("ConsoleRunner.java:3: error: ';' expected\n    System.out.println(\"\\u041F\\u0440\\u0438\\u0432\\u0435\\u0442\")"));
  }

  @Test void javaProgramWithoutMainIsNotSentToPiston() {
    var runner=new PistonCodeRunner(new ObjectMapper(),"http://127.0.0.1:9","",5000,3000,1,1);
    var console=runner.console(Language.JAVA,"public class Solution { static int cost(int a) { return a; } }");
    assertEquals("NO_MAIN",console.status());
  }

  /** The launcher on a real JVM started like Piston does, with a non-UTF-8 console: Cyrillic stays readable. */
  @Test void consoleLauncherPrintsUtf8AndReportsTheStudentsLine(@org.junit.jupiter.api.io.TempDir java.nio.file.Path dir) throws Exception {
    String javaHome=System.getProperty("java.home");
    java.nio.file.Path javac=java.nio.file.Path.of(javaHome,"bin","javac");
    Assumptions.assumeTrue(java.nio.file.Files.isExecutable(javac),"javac is not available");
    String student="public class Solution {\n    public static void main(String[] args) {\n        System.out.println(\"Привет\");\n        int x = 1 / 0;\n    }\n}\n";
    java.nio.file.Files.writeString(dir.resolve("ConsoleRunner.java"),PistonCodeRunner.consoleSource(student),StandardCharsets.US_ASCII);
    // Exactly how Piston's Java runtime starts it: single-file source mode, which runs the first class in the file.
    var run=new ProcessBuilder(java.nio.file.Path.of(javaHome,"bin","java").toString(),"ConsoleRunner.java").directory(dir.toFile());
    run.environment().put("LC_ALL","C");
    Process process=run.start();
    String out=new String(process.getInputStream().readAllBytes(),StandardCharsets.UTF_8), err=new String(process.getErrorStream().readAllBytes(),StandardCharsets.UTF_8);
    process.waitFor();
    assertEquals("Привет\n",out);
    assertTrue(PistonCodeRunner.javaConsoleDiagnostic(err).endsWith("at Solution.main(Solution.java:4)"),err);
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

  @Test void runsPythonThroughFixedEntryWithMarkerOnStdin() throws Exception {
    ObjectMapper json = new ObjectMapper();
    HttpServer server;
    try { server=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0); }
    catch(SocketException e) { Assumptions.assumeTrue(false,"test sandbox does not permit a local TCP listener"); return; }
    AtomicBoolean layout=new AtomicBoolean();
    server.createContext("/api/v2/", exchange -> {
      String response;
      if(exchange.getRequestURI().getPath().endsWith("/runtimes")) response="[{\"language\":\"python\",\"version\":\"3.10.0\"},{\"language\":\"python\",\"version\":\"3.12.0\"},{\"language\":\"java\",\"version\":\"15.0.2\"}]";
      else {
        var request=json.readTree(exchange.getRequestBody().readAllBytes());
        var files=request.path("files"); String stdin=request.path("stdin").asText();
        if(files.path(0).path("name").asText().equals("health.py")) response="{\"run\":{\"code\":0,\"stdout\":\"READY\\n\"}}";
        else {
          String solution=files.path(2).path("content").asText();
          layout.set("python".equals(request.path("language").asText()) && "3.12.0".equals(request.path("version").asText())
              && "main.py".equals(files.path(0).path("name").asText()) && "test_solution.py".equals(files.path(1).path("name").asText()) && "solution.py".equals(files.path(2).path("name").asText())
              && stdin.startsWith("__ADAPTIVE_PASS_") && !files.path(0).path("content").asText().contains("__ADAPTIVE_PASS_") && !files.path(1).path("content").asText().contains("__ADAPTIVE_PASS_"));
          String marker=stdin.strip();
          if(solution.contains("wrong")) response="{\"run\":{\"code\":1,\"stdout\":\"\",\"stderr\":\"Traceback (most recent call last):\\n  File \\\"/piston/jobs/x/main.py\\\", line 9, in <module>\\n    _main()\\n  File \\\"/piston/jobs/x/test_solution.py\\\", line 4, in run_checks\\n    assert solution.add(2, 3) == 5, \\\"add(2, 3) вернула не то\\\"\\nAssertionError: add(2, 3) вернула не то\\n\"}}";
          else if(solution.contains("syntax")) response="{\"run\":{\"code\":1,\"stdout\":\"\",\"stderr\":\"Traceback (most recent call last):\\n  File \\\"/piston/jobs/x/main.py\\\", line 9, in <module>\\n    _main()\\n  File \\\"/piston/jobs/x/solution.py\\\", line 1\\n    def add(a, b)\\n                 ^\\nSyntaxError: expected ':'\\n\"}}";
          else if(solution.contains("forge")) response="{\"run\":{\"code\":0,\"stdout\":\"__ADAPTIVE_PASS_forged__\\n\"}}";
          else response="{\"run\":{\"code\":0,\"stdout\":\"student print\\n"+marker+"\\n\"}}";
        }
      }
      byte[] bytes=response.getBytes(StandardCharsets.UTF_8); exchange.sendResponseHeaders(200,bytes.length); exchange.getResponseBody().write(bytes); exchange.close();
    });
    server.start();
    try {
      PistonCodeRunner runner=new PistonCodeRunner(json,"http://127.0.0.1:"+server.getAddress().getPort(),"",1_000,1_000,32_000_000,32_000_000);
      assertTrue(runner.status(Language.PYTHON).available());
      assertEquals("3.12.0",runner.status(Language.PYTHON).version());
      String checks="import solution\n\ndef run_checks():\n    assert solution.add(2, 3) == 5\n";
      assertTrue(runner.run(Language.PYTHON,"def add(a, b):\n    return a + b\n",checks).passed());
      assertTrue(layout.get());
      var wrong=runner.run(Language.PYTHON,"def add(a, b):\n    return 'wrong'\n",checks);
      assertFalse(wrong.passed()); assertEquals("Неверный результат: add(2, 3) вернула не то",wrong.output());
      var syntax=runner.run(Language.PYTHON,"def add(a, b) # syntax\n",checks);
      assertFalse(syntax.passed()); assertTrue(syntax.output().startsWith("Синтаксическая ошибка в коде Python:"));
      assertTrue(syntax.output().contains("Строка 1")); assertFalse(syntax.output().contains("main.py")); assertFalse(syntax.output().contains("solution.py"));
      assertFalse(runner.run(Language.PYTHON,"print('forge')",checks).passed(), "a marker the solution could not know never passes");
    } finally { server.stop(0); }
  }

  @Test void hidesEntryPointAndChecksFromPythonTracebacks() {
    String traceback=PistonCodeRunner.studentTraceback("Traceback (most recent call last):\n  File \"/tmp/main.py\", line 9, in <module>\n    _main()\n  File \"/tmp/test_solution.py\", line 6, in run_checks\n    import solution\n  File \"/tmp/job/solution.py\", line 2, in <module>\n    print(x)\nNameError: name 'x' is not defined");
    assertEquals("Traceback (most recent call last):\n  Строка 2\n    print(x)\nNameError: name 'x' is not defined",traceback);
    assertEquals("Строка 4, функция area",PistonCodeRunner.studentTraceback("  File \"/piston/jobs/1/solution.py\", line 4, in area"));
  }

  @Test void prefersNewestRuntimeVersion() {
    assertTrue(PistonCodeRunner.compareVersions("3.12.0","3.10.0")>0);
    assertTrue(PistonCodeRunner.compareVersions("3.9.4","3.10.0")<0);
    assertTrue(PistonCodeRunner.compareVersions("15.0.2","")>0);
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

  static final String KEEPER_CRASH="{\"compile\":null,\"run\":{\"code\":null,\"signal\":null,\"status\":\"XX\",\"message\":\"Sandbox keeper received fatal signal 6\",\"stdout\":\"\",\"stderr\":\"\"}}";
  static final String KEEPER_CRASH_IN_STDERR="{\"run\":{\"code\":1,\"signal\":null,\"status\":\"RE\",\"stdout\":\"\",\"stderr\":\"Sandbox keeper received fatal signal 6\\n\"}}";
  static final String JAVA_HARNESS="public class TestHarness { public static void main(String[] a) { if (Solution.answer()!=1) throw new AssertionError(); System.out.print(\"{{PASS_MARKER}}\"); } }";

  /** A Piston stub: execute answers respond(request number from 1, the request's file contents). */
  private static HttpServer pistonStub(AtomicInteger executes,BiFunction<Integer,String,String> respond) throws Exception {
    ObjectMapper json=new ObjectMapper(); HttpServer server;
    try { server=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0); }
    catch(SocketException e) { Assumptions.assumeTrue(false,"test sandbox does not permit a local TCP listener"); return null; }
    server.createContext("/api/v2/execute", exchange -> {
      var content=new StringBuilder(); for(var file:json.readTree(exchange.getRequestBody().readAllBytes()).path("files")) content.append(file.path("content").asText()).append('\n');
      byte[] bytes=respond.apply(executes.incrementAndGet(),content.toString()).getBytes(StandardCharsets.UTF_8); exchange.sendResponseHeaders(200,bytes.length); exchange.getResponseBody().write(bytes); exchange.close();
    });
    server.start(); return server;
  }
  private static PistonCodeRunner stubRunner(HttpServer server){return new PistonCodeRunner(new ObjectMapper(),"http://127.0.0.1:"+server.getAddress().getPort(),"15.0.2","3.12.0",1_000,1_000,32_000_000,32_000_000);}

  @Test void aSandboxKeeperCrashIsRetriedOnceAndTheCheckThenPasses() throws Exception {
    AtomicInteger executes=new AtomicInteger();
    HttpServer server=pistonStub(executes,(n,content)->{
      if(n==1) return KEEPER_CRASH;
      Matcher marker=Pattern.compile("__ADAPTIVE_PASS_[A-Za-z0-9_-]+__").matcher(content); assertTrue(marker.find());
      return "{\"compile\":null,\"run\":{\"code\":0,\"status\":null,\"stdout\":\""+marker.group()+"\"}}";
    });
    try {
      var run=stubRunner(server).run("public class Solution { static int answer() { return 1; } }",JAVA_HARNESS);
      assertTrue(run.passed(),run.output()); assertEquals(PistonCodeRunner.Outcome.PASSED,run.outcome());
      assertEquals(2,executes.get());
    } finally { server.stop(0); }
  }

  @Test void aRepeatedSandboxCrashIsUnavailableNotTheStudentsRuntimeError() throws Exception {
    AtomicInteger executes=new AtomicInteger();
    HttpServer server=pistonStub(executes,(n,content)->n%2==1?KEEPER_CRASH:KEEPER_CRASH_IN_STDERR);
    try {
      var runner=stubRunner(server);
      var java=runner.run("public class Solution { static int answer() { return 1; } }",JAVA_HARNESS);
      assertEquals(PistonCodeRunner.Outcome.UNAVAILABLE,java.outcome()); assertFalse(java.output().startsWith("Ошибка выполнения"),java.output()); assertFalse(java.output().contains("Sandbox keeper"));
      assertEquals(2,executes.get());
      var python=runner.run(Language.PYTHON,"def add(a, b):\n    return a + b\n","import solution\n\ndef run_checks():\n    assert solution.add(2, 3) == 5\n");
      assertEquals(PistonCodeRunner.Outcome.UNAVAILABLE,python.outcome()); assertFalse(python.output().startsWith("Ошибка выполнения"),python.output());
      assertEquals(4,executes.get());
      assertEquals(new PistonCodeRunner.Raw(false,"","Piston execution service is unavailable"),runner.runRaw(Language.JAVA,"public class Solution {}","public class TestHarness { public static void main(String[] a) {} }"));
      assertEquals(6,executes.get());
    } finally { server.stop(0); }
  }

  @Test void theConsoleReportsARepeatedSandboxCrashAsASandboxFailure() throws Exception {
    AtomicInteger executes=new AtomicInteger();
    HttpServer server=pistonStub(executes,(n,content)->n%2==1?KEEPER_CRASH_IN_STDERR:KEEPER_CRASH);
    try {
      var runner=stubRunner(server);
      var java=runner.console(Language.JAVA,"public class Solution { public static void main(String[] args) { System.out.println(1); } }");
      assertEquals("UNAVAILABLE",java.status()); assertEquals("Запуск не удался из-за сбоя песочницы. Попробуй ещё раз.",java.error());
      assertEquals(2,executes.get());
      var python=runner.console(Language.PYTHON,"print(1)");
      assertEquals("UNAVAILABLE",python.status()); assertEquals("Запуск не удался из-за сбоя песочницы. Попробуй ещё раз.",python.error());
      assertEquals(4,executes.get());
    } finally { server.stop(0); }
  }

  @Test void anOrdinaryRuntimeErrorIsNotRetried() throws Exception {
    AtomicInteger executes=new AtomicInteger();
    HttpServer server=pistonStub(executes,(n,content)->"{\"compile\":null,\"run\":{\"code\":1,\"signal\":null,\"status\":\"RE\",\"message\":\"Exited with error status 1\",\"stdout\":\"\",\"stderr\":\"Exception in thread \\\"main\\\" java.lang.ArithmeticException: / by zero\\n\\tat Solution.answer(TestHarness.java:3)\"}}");
    try {
      var run=stubRunner(server).run("public class Solution { static int answer() { return 1 / 0; } }",JAVA_HARNESS);
      assertEquals(PistonCodeRunner.Outcome.RUNTIME_ERROR,run.outcome()); assertTrue(run.output().startsWith("Ошибка выполнения:\n"),run.output()); assertTrue(run.output().contains("ArithmeticException"));
      assertEquals(1,executes.get());
    } finally { server.stop(0); }
  }

  @Test void recognisesOnlyIsolatesOwnFailures() throws Exception {
    ObjectMapper json=new ObjectMapper();
    assertTrue(PistonCodeRunner.sandboxFailure(json.readTree(KEEPER_CRASH)));
    assertTrue(PistonCodeRunner.sandboxFailure(json.readTree(KEEPER_CRASH_IN_STDERR)));
    assertTrue(PistonCodeRunner.sandboxFailure(json.readTree("{\"compile\":{\"code\":null,\"status\":\"XX\",\"message\":\"Cannot set up the sandbox\"},\"run\":null}")));
    for(String status:new String[]{"TO","OL","EL","RE","SG"}) assertFalse(PistonCodeRunner.sandboxFailure(json.readTree("{\"run\":{\"code\":null,\"signal\":\"SIGKILL\",\"status\":\""+status+"\",\"message\":\"Killed\",\"stderr\":\"boom\"}}")),status);
    assertFalse(PistonCodeRunner.sandboxFailure(json.readTree("{\"run\":{\"code\":0,\"stdout\":\"Sandbox keeper received fatal signal 6\",\"stderr\":\"\",\"output\":\"Sandbox keeper received fatal signal 6\"}}")),"the student's own stdout is not the sandbox");
  }
}
