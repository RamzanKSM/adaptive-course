package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.databind.node.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import java.net.URI;
import java.net.http.*;
import java.time.Duration;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.LinkedHashSet;
import java.util.regex.Pattern;

@Component
class PistonCodeRunner {
  static final String PASS_MARKER_PLACEHOLDER="{{PASS_MARKER}}";
  private final ObjectMapper json; private final String baseUrl, configuredJavaVersion; private volatile String discoveredJavaVersion; private volatile RuntimeStatus cachedStatus; private volatile long statusCheckedAt; private final long compileTimeout,runTimeout,compileMemory,runMemory; private final HttpClient http=HttpClient.newBuilder().version(HttpClient.Version.HTTP_1_1).connectTimeout(Duration.ofSeconds(5)).build();
  PistonCodeRunner(ObjectMapper json,@Value("${app.piston.base-url}") String baseUrl,@Value("${app.piston.java-version}") String javaVersion,@Value("${app.piston.compile-timeout-ms}") long compileTimeout,@Value("${app.piston.run-timeout-ms}") long runTimeout,@Value("${app.piston.compile-memory-bytes}") long compileMemory,@Value("${app.piston.run-memory-bytes}") long runMemory){this.json=json;this.baseUrl=baseUrl.replaceAll("/$","");this.configuredJavaVersion=javaVersion;this.compileTimeout=compileTimeout;this.runTimeout=runTimeout;this.compileMemory=compileMemory;this.runMemory=runMemory;}
  boolean configured(){return !baseUrl.isBlank();}
  RuntimeStatus status() {
    if(!configured()) return new RuntimeStatus(false,"PISTON_NOT_CONFIGURED","");
    long now=System.currentTimeMillis(); RuntimeStatus cached=cachedStatus;
    if(cached!=null&&now-statusCheckedAt<30_000)return cached;
    synchronized(this) { if(cachedStatus!=null&&now-statusCheckedAt<30_000)return cachedStatus; try { String version=javaVersion(); cachedStatus=version.isBlank()?new RuntimeStatus(false,"PISTON_JAVA_NOT_INSTALLED",""):runtimeProbe(version)?new RuntimeStatus(true,"READY",version):new RuntimeStatus(false,"PISTON_JAVA_EXECUTION_FAILED",version); } catch(Exception e) { cachedStatus=new RuntimeStatus(false,"PISTON_UNREACHABLE",""); } statusCheckedAt=now;return cachedStatus; }
  }
  Run run(String studentSource,String testSource) {
    try { if(!testSource.contains(PASS_MARKER_PLACEHOLDER)) return new Run(false,"Hidden test harness has no pass marker"); String javaVersion=javaVersion(); if(javaVersion.isBlank()) return new Run(false,"Piston does not expose a Java runtime"); String passMarker=randomPassMarker(); ObjectNode request=json.createObjectNode();request.put("language","java");request.put("version",javaVersion);request.put("compile_timeout",compileTimeout);request.put("run_timeout",runTimeout);request.put("compile_memory_limit",compileMemory);request.put("run_memory_limit",runMemory);ArrayNode files=request.putArray("files");files.addObject().put("name","TestHarness").put("content",combinedSource(studentSource,testSource.replace(PASS_MARKER_PLACEHOLDER,passMarker)));
      var response=http.send(HttpRequest.newBuilder(URI.create(baseUrl+"/api/v2/execute")).timeout(Duration.ofSeconds(20)).header("Content-Type","application/json").POST(HttpRequest.BodyPublishers.ofString(json.writeValueAsString(request))).build(),HttpResponse.BodyHandlers.ofString());
      if(response.statusCode()/100!=2)return new Run(false,"Piston execution service is unavailable");
      JsonNode root=json.readTree(response.body()),compile=root.path("compile"),run=root.path("run");
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
  private String limitFeedback(JsonNode execution) { String details=(execution.path("message").asText("")+"\n"+execution.path("status").asText("")+"\n"+execution.path("signal").asText("")+"\n"+execution.path("stderr").asText("")+"\n"+execution.path("output").asText("")).toLowerCase(); if("to".equals(execution.path("status").asText("" ).toLowerCase())||details.contains("timeout")||details.contains("time limit")||details.contains("timed out"))return "Превышен лимит времени выполнения."; if(details.contains("memory")||details.contains("out of memory")||details.contains("oom")||Integer.valueOf(137).equals(exitCode(execution)))return "Превышен лимит памяти."; return null; }
  private boolean isCompilerFailure(JsonNode run) { String text=(run.path("stderr").asText("")+"\n"+run.path("output").asText("")).toLowerCase(); return text.contains("compilation failed")||text.contains(": error:"); }
  private Integer exitCode(JsonNode node) { return node.hasNonNull("code")?node.path("code").asInt():null; }
  private String output(JsonNode node) { String out=node.path("stdout").asText(""); if(!out.isBlank())return out; out=node.path("output").asText(""); if(!out.isBlank())return out; String stderr=node.path("stderr").asText(""); if(!stderr.isBlank())return stderr; return node.path("message").asText(""); }
  private String safeDiagnostic(String output) { if(output==null)return "";String sanitized=output.replaceAll("(?m).*__ADAPTIVE_PASS_[A-Za-z0-9_-]+__.*(?:\\R|$)","").replace("TestHarness","Solution").trim();return sanitized.length()>3000?sanitized.substring(0,3000)+"\n…":sanitized; }
  private String javaVersion() throws Exception { if(!configuredJavaVersion.isBlank()) return configuredJavaVersion; String found=discoveredJavaVersion; if(found!=null)return found; synchronized(this){if(discoveredJavaVersion!=null)return discoveredJavaVersion; var r=http.send(HttpRequest.newBuilder(URI.create(baseUrl+"/api/v2/runtimes")).timeout(Duration.ofSeconds(5)).GET().build(),HttpResponse.BodyHandlers.ofString());if(r.statusCode()/100!=2)return "";for(JsonNode runtime:json.readTree(r.body()))if("java".equals(runtime.path("language").asText()))return discoveredJavaVersion=runtime.path("version").asText("");return "";} }
  private boolean runtimeProbe(String version) throws Exception { ObjectNode request=json.createObjectNode();request.put("language","java");request.put("version",version);request.put("compile_timeout",compileTimeout);request.put("run_timeout",runTimeout);request.put("compile_memory_limit",compileMemory);request.put("run_memory_limit",runMemory);request.putArray("files").addObject().put("name","HealthCheck.java").put("content","public class HealthCheck { public static void main(String[] a) { System.out.print(\"READY\"); } }");var response=http.send(HttpRequest.newBuilder(URI.create(baseUrl+"/api/v2/execute")).timeout(Duration.ofSeconds(10)).header("Content-Type","application/json").POST(HttpRequest.BodyPublishers.ofString(json.writeValueAsString(request))).build(),HttpResponse.BodyHandlers.ofString());if(response.statusCode()/100!=2)return false;JsonNode root=json.readTree(response.body()),compile=root.path("compile"),run=root.path("run");return (compile.isMissingNode()||compile.isNull()||compile.path("code").asInt(0)==0)&&Integer.valueOf(0).equals(exitCode(run))&&"READY".equals(output(run).strip()); }
  record Run(boolean passed,String output) {}
  record RuntimeStatus(boolean available,String reason,String javaVersion) {}
}
