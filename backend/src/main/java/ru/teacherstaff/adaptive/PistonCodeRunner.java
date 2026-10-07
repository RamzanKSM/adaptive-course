package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.databind.node.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import java.net.URI;
import java.net.http.*;
import java.time.Duration;
import java.security.SecureRandom;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.regex.Pattern;

@Component
class PistonCodeRunner {
  static final String PASS_MARKER_PLACEHOLDER="{{PASS_MARKER}}";
  /**
   * Fixed Python entry point. The pass marker arrives on stdin and is read before the student's module is imported,
   * so it never sits in a file the solution could open. Hidden checks live in test_solution.run_checks().
   */
  static final String PYTHON_ENTRY="""
      import os, sys
      def _main():
          marker = sys.stdin.readline().strip()
          sys.stdin = open(os.devnull)
          import test_solution
          test_solution.run_checks()
          sys.stdout.write("\\n" + marker + "\\n")
          sys.stdout.flush()
      _main()
      """;
  private final ObjectMapper json; private final String baseUrl; private final Map<Language,String> configuredVersions=new EnumMap<>(Language.class);
  private final Map<Language,String> discoveredVersions=new ConcurrentHashMap<>(); private final Map<Language,CachedStatus> statuses=new ConcurrentHashMap<>();
  private final long compileTimeout,runTimeout,compileMemory,runMemory; private final HttpClient http=HttpClient.newBuilder().version(HttpClient.Version.HTTP_1_1).connectTimeout(Duration.ofSeconds(5)).build();
  @Autowired PistonCodeRunner(ObjectMapper json,@Value("${app.piston.base-url}") String baseUrl,@Value("${app.piston.java-version}") String javaVersion,@Value("${app.piston.python-version:}") String pythonVersion,@Value("${app.piston.compile-timeout-ms}") long compileTimeout,@Value("${app.piston.run-timeout-ms}") long runTimeout,@Value("${app.piston.compile-memory-bytes}") long compileMemory,@Value("${app.piston.run-memory-bytes}") long runMemory){this.json=json;this.baseUrl=baseUrl.replaceAll("/$","");configuredVersions.put(Language.JAVA,javaVersion==null?"":javaVersion);configuredVersions.put(Language.PYTHON,pythonVersion==null?"":pythonVersion);this.compileTimeout=compileTimeout;this.runTimeout=runTimeout;this.compileMemory=compileMemory;this.runMemory=runMemory;}
  PistonCodeRunner(ObjectMapper json,String baseUrl,String javaVersion,long compileTimeout,long runTimeout,long compileMemory,long runMemory){this(json,baseUrl,javaVersion,"",compileTimeout,runTimeout,compileMemory,runMemory);}
  boolean configured(){return !baseUrl.isBlank();}
  RuntimeStatus status(){return status(Language.JAVA);}
  RuntimeStatus status(Language language) {
    if(!configured()) return new RuntimeStatus(false,"PISTON_NOT_CONFIGURED","");
    long now=System.currentTimeMillis(); CachedStatus cached=statuses.get(language);
    if(cached!=null&&now-cached.checkedAt()<30_000)return cached.status();
    synchronized(this) {
      cached=statuses.get(language); if(cached!=null&&now-cached.checkedAt()<30_000)return cached.status();
      String prefix="PISTON_"+language.name()+"_"; RuntimeStatus status;
      try { String version=version(language); status=version.isBlank()?new RuntimeStatus(false,prefix+"NOT_INSTALLED",""):runtimeProbe(language,version)?new RuntimeStatus(true,"READY",version):new RuntimeStatus(false,prefix+"EXECUTION_FAILED",version); }
      catch(Exception e) { status=new RuntimeStatus(false,"PISTON_UNREACHABLE",""); }
      statuses.put(language,new CachedStatus(status,now)); return status;
    }
  }
  Run run(String studentSource,String testSource){return run(Language.JAVA,studentSource,testSource);}
  Run run(Language language,String studentSource,String testSource){return language==Language.PYTHON?runPython(studentSource,testSource):runJava(studentSource,testSource);}

  private Run runJava(String studentSource,String testSource) {
    try { if(!testSource.contains(PASS_MARKER_PLACEHOLDER)) return new Run(false,"Hidden test harness has no pass marker"); String javaVersion=version(Language.JAVA); if(javaVersion.isBlank()) return new Run(false,"Piston does not expose a Java runtime"); String passMarker=randomPassMarker(); ObjectNode request=execution(Language.JAVA,javaVersion);ArrayNode files=request.putArray("files");files.addObject().put("name","TestHarness").put("content",combinedSource(studentSource,testSource.replace(PASS_MARKER_PLACEHOLDER,passMarker)));
      JsonNode root=execute(request); if(root==null)return new Run(false,"Piston execution service is unavailable");
      JsonNode compile=root.path("compile"),run=root.path("run");
      // Piston returns compile: null for a successful Java compilation.
      if(!compile.isMissingNode()&&!compile.isNull()) {
        String compileLimit=limitFeedback(compile);
        if(compileLimit!=null)return new Run(false,compileLimit);
        Integer compileCode=exitCode(compile);
        if(compileCode!=null&&compileCode!=0)return new Run(false,studentCompilerFeedback(output(compile)));
      }
      if(run.isMissingNode()||run.isNull()||!run.isObject())return new Run(false,"Piston execution service is unavailable");
      Integer code=exitCode(run); String stdout=run.path("stdout").asText("");
      boolean passed=code!=null&&code==0&&passMarker.equals(stdout.strip());
      if(!passed&&isCompilerFailure(run))return new Run(false,studentCompilerFeedback(output(run)));
      return new Run(passed,passed?"Решение прошло скрытые проверки":studentRunFeedback(run));
    } catch(Exception e){return new Run(false,"Piston execution service is unavailable");}
  }

  private Run runPython(String studentSource,String testSource) {
    try {
      String version=version(Language.PYTHON); if(version.isBlank()) return new Run(false,"Piston does not expose a Python runtime");
      String passMarker=randomPassMarker(); ObjectNode request=execution(Language.PYTHON,version); request.put("stdin",passMarker+"\n");
      ArrayNode files=request.putArray("files");
      files.addObject().put("name","main.py").put("content",PYTHON_ENTRY.strip()+"\n");
      files.addObject().put("name","test_solution.py").put("content",testSource);
      files.addObject().put("name","solution.py").put("content",studentSource==null?"":studentSource);
      JsonNode root=execute(request); if(root==null)return new Run(false,"Piston execution service is unavailable");
      JsonNode run=root.path("run"); if(run.isMissingNode()||run.isNull()||!run.isObject())return new Run(false,"Piston execution service is unavailable");
      Integer code=exitCode(run); String stdout=run.path("stdout").asText("");
      List<String> lines=stdout.lines().map(String::strip).filter(l->!l.isEmpty()).toList();
      boolean passed=code!=null&&code==0&&!lines.isEmpty()&&passMarker.equals(lines.getLast());
      return new Run(passed,passed?"Решение прошло скрытые проверки":pythonFeedback(run));
    } catch(Exception e){return new Run(false,"Piston execution service is unavailable");}
  }

  static final int CONSOLE_MAX_CHARS=10_000, CONSOLE_MAX_LINES=200;
  /** Runs Solution.main with UTF-8 console streams; appended after the student's code so its line numbers stay unchanged. */
  static final String CONSOLE_LAUNCHER="public class ConsoleRunner { public static void main(String[] args) throws Throwable { "
      +"System.setOut(new java.io.PrintStream(new java.io.FileOutputStream(java.io.FileDescriptor.out), true, \"UTF-8\")); "
      +"System.setErr(new java.io.PrintStream(new java.io.FileOutputStream(java.io.FileDescriptor.err), true, \"UTF-8\")); "
      +"Solution.main(new String[0]); } }";
  /** Runs solution.py as a script (so `if __name__ == "__main__"` blocks run) with UTF-8 console streams. */
  static final String PYTHON_CONSOLE_ENTRY="""
      import runpy, sys
      sys.stdout.reconfigure(encoding="utf-8")
      sys.stderr.reconfigure(encoding="utf-8")
      runpy.run_path("solution.py", run_name="__main__")
      """;
  private static final Pattern JAVA_MAIN=Pattern.compile("\\bstatic\\s+(?:final\\s+)?void\\s+main\\s*\\(");

  /**
   * The program run as is, without hidden checks — what the student would see in a console. Nothing here is secret:
   * no checks, no pass marker. Keyboard input is empty.
   */
  Console console(Language language,String source) {
    try { return language==Language.PYTHON?consolePython(source):consoleJava(source); }
    catch(Exception e) { return Console.of("UNAVAILABLE","Запуск сейчас недоступен."); }
  }
  private Console consoleJava(String source) throws Exception {
    if(source==null||!JAVA_MAIN.matcher(source).find()) return Console.of("NO_MAIN",null);
    String version=version(Language.JAVA); if(version.isBlank()) return Console.of("UNAVAILABLE","Запуск Java сейчас недоступен.");
    ObjectNode request=execution(Language.JAVA,version);
    request.putArray("files").addObject().put("name","ConsoleRunner").put("content",consoleSource(source));
    JsonNode root=execute(request); if(root==null) return Console.of("UNAVAILABLE","Запуск Java сейчас недоступен.");
    JsonNode compile=root.path("compile"),run=root.path("run");
    if(!compile.isMissingNode()&&!compile.isNull()) {
      if(limitFeedback(compile)!=null) return Console.of("LIMIT",limitFeedback(compile));
      Integer code=exitCode(compile); if(code!=null&&code!=0) return Console.of("COMPILE_ERROR",javaConsoleDiagnostic(output(compile)));
    }
    if(run.isMissingNode()||run.isNull()||!run.isObject()) return Console.of("UNAVAILABLE","Запуск Java сейчас недоступен.");
    if(isCompilerFailure(run)&&run.path("stdout").asText("").isEmpty()) return Console.of("COMPILE_ERROR",javaConsoleDiagnostic(output(run)));
    return consoleResult(run,javaConsoleDiagnostic(run.path("stderr").asText("")));
  }
  private Console consolePython(String source) throws Exception {
    String version=version(Language.PYTHON); if(version.isBlank()) return Console.of("UNAVAILABLE","Запуск Python сейчас недоступен.");
    ObjectNode request=execution(Language.PYTHON,version); request.put("stdin","");
    ArrayNode files=request.putArray("files");
    files.addObject().put("name","main.py").put("content",PYTHON_CONSOLE_ENTRY.strip()+"\n");
    files.addObject().put("name","solution.py").put("content",source==null?"":source);
    JsonNode root=execute(request); if(root==null) return Console.of("UNAVAILABLE","Запуск Python сейчас недоступен.");
    JsonNode run=root.path("run"); if(run.isMissingNode()||run.isNull()||!run.isObject()) return Console.of("UNAVAILABLE","Запуск Python сейчас недоступен.");
    String traceback=studentTraceback(run.path("stderr").asText(""));
    String last=traceback.lines().filter(l->!l.isBlank()).reduce((a,b)->b).orElse("").strip();
    if(last.startsWith("SyntaxError")||last.startsWith("IndentationError")||last.startsWith("TabError")) return new Console("COMPILE_ERROR",clip(run.path("stdout").asText("")),clip(traceback),false);
    return consoleResult(run,traceback);
  }
  /** Common tail: output limits, a crash with its message, or a normal exit. stdout printed before a crash is kept. */
  private Console consoleResult(JsonNode run,String error) {
    String stdout=run.path("stdout").asText("");
    String status=run.path("status").asText("");
    boolean tooLong="OL".equals(status)||"EL".equals(status)||stdout.length()>CONSOLE_MAX_CHARS||stdout.lines().count()>CONSOLE_MAX_LINES;
    String limit="OL".equals(status)||"EL".equals(status)?null:limitFeedback(run);
    if(limit!=null) return new Console("LIMIT",clip(stdout),limit,tooLong);
    Integer code=exitCode(run);
    if(code!=null&&code!=0&&!tooLong) {
      String message=error.isBlank()?"Программа завершилась с кодом "+code+".":error;
      if(message.contains("EOFError")||message.contains("NoSuchElementException")) message+="\n\nВвод с клавиатуры в консоли пока не поддерживается: программа получает пустой ввод.";
      return new Console("RUNTIME_ERROR",clip(stdout),clip(message),false);
    }
    return new Console("OK",clip(stdout),null,tooLong);
  }
  static String consoleSource(String student) {
    String solution=student.replaceFirst("(?m)\\bpublic\\s+(?=(?:(?:final|abstract)\\s+)*class\\s+Solution\\b)","");
    return javaUnicodeEscapes(solution+"\n"+CONSOLE_LAUNCHER);
  }
  /** Compiler and JVM messages in the student's terms: Solution.java, their own line numbers, readable Cyrillic. */
  static String javaConsoleDiagnostic(String output) {
    if(output==null) return "";
    String text=output.lines().filter(l->!l.contains("at ConsoleRunner.")).reduce((a,b)->a+"\n"+b).orElse("").replace("ConsoleRunner.java","Solution.java");
    var escape=Pattern.compile("\\\\u([0-9A-Fa-f]{4})").matcher(text); var unescaped=new StringBuilder();
    while(escape.find()) escape.appendReplacement(unescaped,java.util.regex.Matcher.quoteReplacement(String.valueOf((char)Integer.parseInt(escape.group(1),16))));
    escape.appendTail(unescaped);
    return clip(unescaped.toString().strip());
  }
  private static String clip(String text) {
    if(text==null) return "";
    var lines=text.lines().limit(CONSOLE_MAX_LINES).toList();
    String kept=String.join("\n",lines)+(text.endsWith("\n")&&lines.size()==text.lines().count()?"\n":"");
    return kept.length()>CONSOLE_MAX_CHARS?kept.substring(0,CONSOLE_MAX_CHARS):kept;
  }
  /**
   * The console of one run. status: OK, COMPILE_ERROR, RUNTIME_ERROR, LIMIT, NO_MAIN (a Java task without main —
   * nothing to run), UNAVAILABLE. truncated: the output was cut to the first lines.
   */
  record Console(String status,String stdout,String error,boolean truncated) {
    static Console of(String status,String error){return new Console(status,"",error,false);}
    Map<String,Object> view(){var m=new LinkedHashMap<String,Object>();m.put("status",status);m.put("stdout",stdout);m.put("error",error);m.put("truncated",truncated);return m;}
    /** Plain text for the assistant's context. */
    String text(){return "статус="+status+(truncated?" (вывод обрезан)":"")+"\nвывод:\n"+(stdout==null||stdout.isEmpty()?"(пусто)":stdout)+(error==null||error.isBlank()?"":"\nошибка:\n"+error);}
  }

  private String pythonFeedback(JsonNode run) {
    String limit=limitFeedback(run); if(limit!=null)return limit;
    String stderr=run.path("stderr").asText("");
    String traceback=studentTraceback(stderr);
    String last=traceback.lines().filter(l->!l.isBlank()).reduce((a,b)->b).orElse("").strip();
    if(last.startsWith("AssertionError")) { String message=last.substring("AssertionError".length()).replaceFirst("^:\\s*","").strip(); return message.isBlank()?"Неверный результат.":"Неверный результат: "+safeDiagnostic(message); }
    if(last.startsWith("SyntaxError")||last.startsWith("IndentationError")||last.startsWith("TabError")) return "Синтаксическая ошибка в коде Python:\n"+safeDiagnostic(traceback);
    if(!traceback.isBlank()) return "Ошибка выполнения:\n"+safeDiagnostic(traceback);
    return "Неверный результат.";
  }
  /** Drops traceback frames of the hidden entry point and checks so students only see their own lines. */
  static String studentTraceback(String stderr) {
    if(stderr==null)return "";
    var kept=new ArrayList<String>(); boolean skipCode=false;
    for(String line:stderr.split("\\R")) {
      if(line.matches("\\s*File \"(.*(main|test_solution)\\.py|<frozen [^>]+>)\".*")) { skipCode=true; continue; }
      if(skipCode&&line.startsWith("    ")&&!line.stripLeading().startsWith("File ")) continue;
      skipCode=false;
      kept.add(studentFrame(line));
    }
    return String.join("\n",kept).strip();
  }

  /** Students never see platform file names: «File ".../solution.py", line 4, in area» becomes «Строка 4, функция area». */
  private static String studentFrame(String line) {
    var frame=Pattern.compile("^(\\s*)File \"[^\"]*solution\\.py\", line (\\d+)(?:, in (.+))?$").matcher(line);
    if(!frame.matches()) return line;
    String where=frame.group(3)==null||frame.group(3).equals("<module>")?"":", функция "+frame.group(3);
    return frame.group(1)+"Строка "+frame.group(2)+where;
  }
  private ObjectNode execution(Language language,String version) { ObjectNode request=json.createObjectNode();request.put("language",language.pistonLanguage);request.put("version",version);request.put("compile_timeout",compileTimeout);request.put("run_timeout",runTimeout);request.put("compile_memory_limit",compileMemory);request.put("run_memory_limit",runMemory);return request; }
  private JsonNode execute(ObjectNode request) throws Exception {
    var response=http.send(HttpRequest.newBuilder(URI.create(baseUrl+"/api/v2/execute")).timeout(Duration.ofSeconds(20)).header("Content-Type","application/json").POST(HttpRequest.BodyPublishers.ofString(json.writeValueAsString(request))).build(),HttpResponse.BodyHandlers.ofString());
    return response.statusCode()/100!=2?null:json.readTree(response.body());
  }
  private String randomPassMarker(){byte[] bytes=new byte[24];new SecureRandom().nextBytes(bytes);return "__ADAPTIVE_PASS_"+Base64.getUrlEncoder().withoutPadding().encodeToString(bytes)+"__";}
  static String combinedSource(String studentSource,String testSource) {
    SourceWithoutImports harness=withoutImports(testSource), solution=withoutImports(studentSource);
    String solutionBody=solution.body().replaceFirst("(?m)\\bpublic\\s+(?=(?:(?:final|abstract)\\s+)*class\\s+Solution\\b)","");
    var imports=new LinkedHashSet<String>(); imports.addAll(harness.imports()); imports.addAll(solution.imports());
    return javaUnicodeEscapes(String.join("\n",imports)+"\n"+harness.body()+"\n"+solutionBody);
  }
  /** Piston Java 15 compiles source as a non-UTF-8 locale; keep literals intact independently of that locale. */
  static String javaUnicodeEscapes(String source) {
    StringBuilder escaped=new StringBuilder(source.length());
    for(int i=0;i<source.length();i++) { char c=source.charAt(i); if(c>0x7f) escaped.append(String.format("\\u%04X",(int)c)); else escaped.append(c); }
    return escaped.toString();
  }
  private static SourceWithoutImports withoutImports(String source) {
    var imports=new LinkedHashSet<String>(); var matcher=Pattern.compile("(?m)^\\s*import\\s+(?:static\\s+)?[\\w.*]+\\s*;\\s*$").matcher(source);
    var body=new StringBuffer(); while(matcher.find()){imports.add(matcher.group().trim());matcher.appendReplacement(body,"");}matcher.appendTail(body);return new SourceWithoutImports(imports,body.toString());
  }
  private record SourceWithoutImports(LinkedHashSet<String> imports,String body) {}
  private String studentCompilerFeedback(String output){String diagnostic=safeDiagnostic(output);return diagnostic.isBlank()?"Ошибка компиляции Java.":"Ошибка компиляции Java:\n"+diagnostic;}
  private String studentRunFeedback(JsonNode run){
    String limit=limitFeedback(run); if(limit!=null)return limit;
    String diagnostic=safeDiagnostic(run.path("stderr").asText(""));
    if(!diagnostic.isBlank()&&!diagnostic.toLowerCase().contains("assertionerror"))return "Ошибка выполнения:\n"+diagnostic;
    return "Неверный вывод программы.";
  }
  private String limitFeedback(JsonNode execution) { String details=(execution.path("message").asText("")+"\n"+execution.path("status").asText("")+"\n"+execution.path("signal").asText("")+"\n"+execution.path("stderr").asText("")+"\n"+execution.path("output").asText("")).toLowerCase(); if("to".equals(execution.path("status").asText("" ).toLowerCase())||details.contains("timeout")||details.contains("time limit")||details.contains("timed out"))return "Превышен лимит времени выполнения."; if(details.contains("memory limit")||details.contains("out of memory")||details.contains("memoryerror")||details.contains("oom")||Integer.valueOf(137).equals(exitCode(execution)))return "Превышен лимит памяти."; return null; }
  private boolean isCompilerFailure(JsonNode run) { String text=(run.path("stderr").asText("")+"\n"+run.path("output").asText("")).toLowerCase(); return text.contains("compilation failed")||text.contains(": error:"); }
  private Integer exitCode(JsonNode node) { return node.hasNonNull("code")?node.path("code").asInt():null; }
  private String output(JsonNode node) { String out=node.path("stdout").asText(""); if(!out.isBlank())return out; out=node.path("output").asText(""); if(!out.isBlank())return out; String stderr=node.path("stderr").asText(""); if(!stderr.isBlank())return stderr; return node.path("message").asText(""); }
  private String safeDiagnostic(String output) { if(output==null)return "";String sanitized=output.replaceAll("(?m).*__ADAPTIVE_PASS_[A-Za-z0-9_-]+__.*(?:\\R|$)","").replace("TestHarness","Solution").trim();return sanitized.length()>3000?sanitized.substring(0,3000)+"\n…":sanitized; }
  private String version(Language language) throws Exception {
    String configured=configuredVersions.getOrDefault(language,""); if(!configured.isBlank()) return configured;
    String found=discoveredVersions.get(language); if(found!=null)return found;
    synchronized(this){
      found=discoveredVersions.get(language); if(found!=null)return found;
      var r=http.send(HttpRequest.newBuilder(URI.create(baseUrl+"/api/v2/runtimes")).timeout(Duration.ofSeconds(5)).GET().build(),HttpResponse.BodyHandlers.ofString());
      if(r.statusCode()/100!=2)return "";
      // Prefer the newest installed version when several are present (e.g. python 3.10 and 3.12).
      String best="";
      for(JsonNode runtime:json.readTree(r.body())) if(language.pistonLanguage.equals(runtime.path("language").asText())) { String v=runtime.path("version").asText(""); if(compareVersions(v,best)>0) best=v; }
      if(!best.isBlank()) discoveredVersions.put(language,best);
      return best;
    }
  }
  static int compareVersions(String a,String b) {
    if(b==null||b.isBlank())return a==null||a.isBlank()?0:1;
    String[] x=a.split("\\."),y=b.split("\\.");
    for(int i=0;i<Math.max(x.length,y.length);i++){ int p=i<x.length?parse(x[i]):0,q=i<y.length?parse(y[i]):0; if(p!=q)return Integer.compare(p,q); }
    return 0;
  }
  private static int parse(String part){ try { return Integer.parseInt(part.replaceAll("\\D.*","")); } catch(NumberFormatException e){ return 0; } }
  private boolean runtimeProbe(Language language,String version) throws Exception {
    ObjectNode request=execution(language,version);
    if(language==Language.PYTHON) request.putArray("files").addObject().put("name","health.py").put("content","print('READY')");
    else request.putArray("files").addObject().put("name","HealthCheck.java").put("content","public class HealthCheck { public static void main(String[] a) { System.out.print(\"READY\"); } }");
    JsonNode root=execute(request); if(root==null)return false;
    JsonNode compile=root.path("compile"),run=root.path("run");
    return (compile.isMissingNode()||compile.isNull()||compile.path("code").asInt(0)==0)&&Integer.valueOf(0).equals(exitCode(run))&&"READY".equals(output(run).strip());
  }
  private record CachedStatus(RuntimeStatus status,long checkedAt) {}
  /** Why a run ended. Task verification needs it: a wrong example must fail a check, not crash or time out. */
  enum Outcome { PASSED, CHECK_FAILED, COMPILE_ERROR, RUNTIME_ERROR, LIMIT, UNAVAILABLE }
  record Run(boolean passed,String output,Outcome outcome) {
    Run(boolean passed,String output){this(passed,output,classify(passed,output));}
    /** Every failure message is produced in this class, so its prefix identifies the cause. */
    static Outcome classify(boolean passed,String output) {
      if(passed) return Outcome.PASSED;
      String text=output==null?"":output;
      if(text.startsWith("Неверн")) return Outcome.CHECK_FAILED;
      if(text.startsWith("Ошибка компиляции")||text.startsWith("Синтаксическая ошибка")) return Outcome.COMPILE_ERROR;
      if(text.startsWith("Ошибка выполнения")) return Outcome.RUNTIME_ERROR;
      if(text.startsWith("Превышен лимит")) return Outcome.LIMIT;
      return Outcome.UNAVAILABLE;
    }
  }
  record RuntimeStatus(boolean available,String reason,String version) {}
}
