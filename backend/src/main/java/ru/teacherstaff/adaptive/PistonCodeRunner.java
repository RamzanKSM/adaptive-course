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
    try { if(!testSource.contains(PASS_MARKER_PLACEHOLDER)) return new Run(false,"Hidden test harness has no pass marker"); String javaVersion=javaVersion(); if(javaVersion.isBlank()) return new Run(false,"Piston does not expose a Java runtime"); String passMarker=randomPassMarker(); ObjectNode request=json.createObjectNode();request.put("language","java");request.put("version",javaVersion);request.put("compile_timeout",compileTimeout);request.put("run_timeout",runTimeout);request.put("compile_memory_limit",compileMemory);request.put("run_memory_limit",runMemory);ArrayNode files=request.putArray("files");files.addObject().put("name","TestHarness.java").put("content",testSource.replace(PASS_MARKER_PLACEHOLDER,passMarker));files.addObject().put("name","Solution.java").put("content",studentSource);
      var response=http.send(HttpRequest.newBuilder(URI.create(baseUrl+"/api/v2/execute")).timeout(Duration.ofSeconds(20)).header("Content-Type","application/json").POST(HttpRequest.BodyPublishers.ofString(json.writeValueAsString(request))).build(),HttpResponse.BodyHandlers.ofString());
      if(response.statusCode()/100!=2)return new Run(false,"Piston execution service is unavailable"); JsonNode root=json.readTree(response.body()),compile=root.path("compile"),run=root.path("run");int compileCode=compile.path("code").asInt(0);String compileOutput=output(compile); if(compileCode!=0)return new Run(false,studentCompilerFeedback(compileOutput));int code=run.path("code").asInt(-1);String output=output(run);return new Run(code==0&&passMarker.equals(output.strip()),code==0&&passMarker.equals(output.strip())?"Решение прошло скрытые проверки":studentRunFeedback(output));
    } catch(Exception e){return new Run(false,"Piston execution service is unavailable");}
  }
  private String randomPassMarker(){byte[] bytes=new byte[24];new SecureRandom().nextBytes(bytes);return "__ADAPTIVE_PASS_"+Base64.getUrlEncoder().withoutPadding().encodeToString(bytes)+"__";}
  private String studentCompilerFeedback(String output){if(output==null||output.isBlank()||output.contains("TestHarness"))return "Java compilation failed";return output;}
  private String studentRunFeedback(String output){return "Решение не прошло скрытые проверки";}
  private String output(JsonNode node) { String out=node.path("output").asText(""); if(!out.isBlank())return out; String stderr=node.path("stderr").asText(""); if(!stderr.isBlank())return stderr; return node.path("message").asText(""); }
  private String javaVersion() throws Exception { if(!configuredJavaVersion.isBlank()) return configuredJavaVersion; String found=discoveredJavaVersion; if(found!=null)return found; synchronized(this){if(discoveredJavaVersion!=null)return discoveredJavaVersion; var r=http.send(HttpRequest.newBuilder(URI.create(baseUrl+"/api/v2/runtimes")).timeout(Duration.ofSeconds(5)).GET().build(),HttpResponse.BodyHandlers.ofString());if(r.statusCode()/100!=2)return "";for(JsonNode runtime:json.readTree(r.body()))if("java".equals(runtime.path("language").asText()))return discoveredJavaVersion=runtime.path("version").asText("");return "";} }
  private boolean runtimeProbe(String version) throws Exception { ObjectNode request=json.createObjectNode();request.put("language","java");request.put("version",version);request.put("compile_timeout",compileTimeout);request.put("run_timeout",runTimeout);request.put("compile_memory_limit",compileMemory);request.put("run_memory_limit",runMemory);request.putArray("files").addObject().put("name","HealthCheck.java").put("content","public class HealthCheck { public static void main(String[] a) { System.out.print(\"READY\"); } }");var response=http.send(HttpRequest.newBuilder(URI.create(baseUrl+"/api/v2/execute")).timeout(Duration.ofSeconds(10)).header("Content-Type","application/json").POST(HttpRequest.BodyPublishers.ofString(json.writeValueAsString(request))).build(),HttpResponse.BodyHandlers.ofString());if(response.statusCode()/100!=2)return false;JsonNode root=json.readTree(response.body()),compile=root.path("compile"),run=root.path("run");return compile.path("code").asInt(0)==0&&run.path("code").asInt(-1)==0&&"READY".equals(output(run).strip()); }
  record Run(boolean passed,String output) {}
  record RuntimeStatus(boolean available,String reason,String javaVersion) {}
}
