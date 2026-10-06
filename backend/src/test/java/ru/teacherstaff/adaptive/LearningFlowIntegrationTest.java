package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.*;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.*;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import java.nio.file.Path;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class LearningFlowIntegrationTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json; @Autowired TaskAudit taskAudit;
  @MockBean PistonCodeRunner runner;
  @MockBean LlmTutor tutor;
  @MockBean LearningContentGenerator generator;
  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:flow-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
    p.add("app.task-audit.enabled", () -> "false"); // background re-verification would race the tests; it is called directly where tested
  }
  @BeforeEach void prepare() { db.update("update users set password_hash=? where login='admin'",new BCryptPasswordEncoder().encode("admin-pass")); when(runner.configured()).thenReturn(true); when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true,"READY","17.0.1")); when(runner.run(any(Language.class),anyString(),anyString())).thenAnswer(call->((String)call.getArgument(1)).contains("WRONG")?new PistonCodeRunner.Run(false,"Неверный вывод программы."):new PistonCodeRunner.Run(true,"Решение прошло скрытые проверки")); when(tutor.status(anyLong())).thenReturn(new LlmStatus(false,false,false,"DISABLED", "gpt-6-luna")); }

  @Test void diagnosticConfirmsTopicsSoPracticeSkipsThemWithoutFakeProgress() throws Exception {
    String cookie=createStudentAndLogin("block-student"); long student=studentId("block-student");
    submitDiagnostic(cookie, student, true);
    // Block 0 answered correctly: its topics are confirmed, except VARIABLE_BASIC whose block-1 question was not answered.
    assertEquals(1,db.queryForObject("select confirmed from diagnostic_skill_results where user_id=? and skill_code='BASIC_CODE_READING'",Integer.class,student));
    assertEquals(0,db.queryForObject("select confirmed from diagnostic_skill_results where user_id=? and skill_code='VARIABLE_BASIC'",Integer.class,student));
    assertEquals(0,db.queryForObject("select count(*) from student_skills where user_id=?",Integer.class,student),"confirmation is not practice credit");
    addTask("PRIMITIVE_TYPES", "block 1 task");
    start(cookie);
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(cookie))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertNotEquals("BASIC_CODE_READING",next.path("skill").path("code").asText(),"a confirmed topic is never practiced, even though it has seed tasks");
    long assigned=next.path("task").path("id").asLong();
    var restored=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(cookie))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(assigned,restored.path("task").path("id").asLong());
    assertEquals(1,countLessonTasks(student));
    verifyNoInteractions(generator);
    var progress=json.readTree(mvc.perform(get("/api/progress").cookie(cookie(cookie))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    var basic=findSkill(progress,"BASIC_CODE_READING");
    assertEquals(1,basic.path("confirmedByDiagnostic").asInt()); assertEquals(0,basic.path("completedIterations").asInt()); assertEquals(0,basic.path("mastered").asInt());
    assertEquals(1,basic.path("diagnosticCorrect").asInt()); assertEquals(1,basic.path("diagnosticTotal").asInt());
  }

  @Test void weakTopicInsideAStrongBlockIsPracticedAndAPerfectDiagnosticStartsNothing() throws Exception {
    String token=createStudentAndLogin("umar-student"); long student=studentId("umar-student");
    // Everything right except one question on INTEGER_DIVISION: block 1 stays above 80%, the topic still needs practice.
    var rows=db.queryForList("select id,correct_option,skill_code from diagnostic_questions where language='JAVA' order by id"); var answers=new ArrayList<Map<String,Object>>(); boolean missed=false;
    for(var q:rows){var a=new LinkedHashMap<String,Object>();a.put("questionId",q.get("id"));if(!missed&&"INTEGER_DIVISION".equals(q.get("skill_code"))){a.put("selectedOption",(((Number)q.get("correct_option")).intValue()+1)%4);missed=true;}else a.put("selectedOption",q.get("correct_option"));answers.add(a);}
    mvc.perform(post("/api/diagnostic").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("answers",answers)))).andExpect(status().isOk());
    addTask("INTEGER_DIVISION","division practice");
    start(token);
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("INTEGER_DIVISION",next.path("skill").path("code").asText());

    String perfect=createStudentAndLogin("perfect-student"); long perfectId=studentId("perfect-student");
    var all=new ArrayList<Map<String,Object>>(); for(var q:rows) all.add(Map.of("questionId",q.get("id"),"selectedOption",q.get("correct_option")));
    mvc.perform(post("/api/diagnostic").cookie(cookie(perfect)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("answers",all)))).andExpect(status().isOk());
    assertEquals(0,db.queryForObject("select count(*) from diagnostic_skill_results where user_id=? and confirmed=0",Integer.class,perfectId));
    start(perfect);
    var done=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(perfect))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("COURSE_COMPLETE",done.path("reason").asText(),"no forced start of the last block");
    assertTrue(done.path("task").isNull());
  }

  @Test void retiredPredictionTaskKeepsHistoryButIsSkippedAndCannotBeAttempted() throws Exception {
    String token=createStudentAndLogin("retired-student"); long student=studentId("retired-student"); submitDiagnostic(token,student,false);
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name) values(?,?,?,?,?,?)", "BASIC_CODE_READING", "Вывод строки", "Что выведет этот код?", "public class Solution { public static String answer(){ return \"\"; } }", "class TestHarness { public static void main(String[] args) { Solution.answer(); } }", "TestHarness.java");
    long oldTask=db.queryForObject("select last_insert_rowid()",Long.class);
    db.update("insert into task_target_skills(task_id,skill_code) values(?,?)",oldTask,"BASIC_CODE_READING");
    int lesson=start(token); long lessonId=db.queryForObject("select id from lessons where user_id=? and lesson_number=?",Long.class,student,lesson);
    db.update("insert into lesson_tasks(lesson_id,task_id) values(?,?)",lessonId,oldTask);
    db.update("insert into submissions(lesson_id,task_id,source_code,passed,runner_output) values(?,?,?,?,?)",lessonId,oldTask,"old code",0,"old output");
    var importer=new DiagnosticImporter(db,json,Path.of("missing-diagnostic.md").toString());
    importer.run(null);
    importer.run(null);
    assertEquals(0,db.queryForObject("select active from tasks where id=?",Integer.class,oldTask));
    assertEquals(1,db.queryForObject("select count(*) from submissions where task_id=?",Integer.class,oldTask));
    var response=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertNotEquals(oldTask,response.path("task").path("id").asLong());
    var attempt=json.readTree(mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",oldTask,"sourceCode","public class Solution {}")))).andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
    assertEquals("TASK_UPDATED",attempt.path("error").asText());
    assertEquals(9,db.queryForObject("select count(*) from tasks where skill_code='BASIC_CODE_READING' and active=1 and title like 'Консоль:%'",Integer.class));
  }

  @Test void chatReceivesFreshEditorDraftForCurrentTask() throws Exception {
    String token=createStudentAndLogin("chat-draft-student"); long student=studentId("chat-draft-student"); submitDiagnostic(token,student,false); start(token);
    long task=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()).path("task").path("id").asLong();
    when(tutor.reply(anyLong(),any(TutorContext.class),anyString())).thenReturn("Подумай о первой строке.");
    String draft="public class Solution { public static void main(String[] args) { System.out.print(\"черновик\"); } }";
    mvc.perform(post("/api/chat").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("content","Что проверить?","taskId",String.valueOf(task),"sourceCode",draft)))).andExpect(status().isOk());
    var context=org.mockito.ArgumentCaptor.forClass(TutorContext.class); verify(tutor).reply(eq(student),context.capture(),eq("Что проверить?"));
    assertEquals(draft,context.getValue().currentEditorSource());
    assertNull(context.getValue().latestSubmissionSource());
  }

  @Test void successfulTasksCompleteOnlyScheduledIterations() throws Exception {
    String token=createStudentAndLogin("progress-student"); long student=studentId("progress-student"); submitDiagnostic(token,student,false);
    db.update("update student_languages set starting_block=0 where user_id=?",student);
    db.update("insert into student_skills(user_id,skill_code,completed_iterations,iteration_successes,mastered) select ?,code,3,0,1 from skills where code<>'BASIC_CODE_READING'",student);
    for(int i=4;i<=9;i++) addTask("extra "+i);
    int lesson1=start(token); solveThree(token); assertProgress(student,1,0,0); finish(token,lesson1);
    int lesson2=start(token); solveThree(token); assertProgress(student,2,0,0); finish(token,lesson2);
    int lesson3=start(token); var skipped=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()); assertEquals("NO_DUE_SKILL",skipped.path("reason").asText()); finish(token,lesson3);
    int lesson4=start(token); solveThree(token); assertProgress(student,3,1,0);
  }

  @Test void generatedTaskIsValidatedStoredOnceAndThenRestored() throws Exception {
    String token=createStudentAndLogin("generated-student"); long student=studentId("generated-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"LOGICAL_AND");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("LOGICAL_AND"))).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("LOGICAL_AND"))).thenReturn(generated("LOGICAL_AND", true));
    start(token);
    var first=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(first.path("task").path("id").asLong()>0);
    assertEquals(1,db.queryForObject("select count(*) from tasks where title='generated LOGICAL_AND'",Integer.class));
    var reloaded=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(first.path("task").path("id").asLong(),reloaded.path("task").path("id").asLong());
    verify(generator,times(1)).generateTask(eq(student),brief("LOGICAL_AND"));
    assertEquals(1,db.queryForObject("select difficulty from tasks where title='generated LOGICAL_AND'",Integer.class));
    var requested=org.mockito.ArgumentCaptor.forClass(ContentBrief.class); verify(generator).generateTask(eq(student),requested.capture());
    assertEquals(1,requested.getValue().difficulty()); assertEquals("Логическое И (&&)",requested.getValue().skillTitle()); assertFalse(requested.getValue().earlierSkills().isEmpty());
  }

  @Test void invalidGeneratedHarnessIsNeverStored() throws Exception {
    String token=createStudentAndLogin("invalid-generator-student"); long student=studentId("invalid-generator-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"FOR_LOOP_BASIC");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("FOR_LOOP_BASIC"))).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("FOR_LOOP_BASIC"))).thenReturn(generated("FOR_LOOP_BASIC", false));
    start(token);
    var response=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("LLM_GENERATION_FAILED_VALIDATION",response.path("reason").asText());
    assertEquals(0,db.queryForObject("select count(*) from tasks where title='generated FOR_LOOP_BASIC'",Integer.class));
    verify(generator,times(ApiController.GENERATION_ATTEMPTS)).generateTask(eq(student),brief("FOR_LOOP_BASIC"));
  }

  @Test void invalidGeneratedCandidateIsRetriedAndOnlyValidCandidateIsStored() throws Exception {
    String token=createStudentAndLogin("retry-generator-student"); long student=studentId("retry-generator-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"WHILE_LOOP_BASIC");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("WHILE_LOOP_BASIC"))).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("WHILE_LOOP_BASIC"))).thenReturn(generated("WHILE_LOOP_BASIC", false),generated("WHILE_LOOP_BASIC", true));
    start(token);
    var response=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(response.path("task").path("id").asLong()>0);
    assertEquals(1,db.queryForObject("select count(*) from tasks where title='generated WHILE_LOOP_BASIC'",Integer.class));
    verify(generator,times(2)).generateTask(eq(student),brief("WHILE_LOOP_BASIC"));
  }

  @Test void unavailableRunnerDoesNotCallGenerator() throws Exception {
    String token=createStudentAndLogin("runner-unavailable-student"); long student=studentId("runner-unavailable-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"SWITCH_BASIC");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("SWITCH_BASIC"))).thenReturn(Optional.empty());
    when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(false,"PISTON_UNREACHABLE",""));
    start(token);
    var response=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("RUNNER_UNAVAILABLE",response.path("reason").asText());
    verify(generator,never()).generateTask(eq(student),brief("SWITCH_BASIC"));
  }

  @Test void iterationStaysOnOneSkillAndGoesFromEasyToHard() throws Exception {
    String token=createStudentAndLogin("focus-student"); long student=studentId("focus-student"); submitDiagnostic(token,student,false);
    db.update("update student_languages set starting_block=0 where user_id=?",student);
    db.update("insert into student_skills(user_id,skill_code,completed_iterations,iteration_successes,mastered) select ?,code,3,0,1 from skills where code not in ('BASIC_CODE_READING','VARIABLE_BASIC','ASSIGNMENT')",student);
    for(String skill:List.of("VARIABLE_BASIC","ASSIGNMENT")) for(int i=1;i<=3;i++) addTask(skill,skill+" "+i);
    start(token);
    var difficulties=new ArrayList<Integer>();
    for(int i=0;i<3;i++) {
      var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
      assertEquals("BASIC_CODE_READING",next.path("skill").path("code").asText());
      long task=next.path("task").path("id").asLong(); difficulties.add(db.queryForObject("select difficulty from tasks where id=?",Integer.class,task));
      mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",task,"sourceCode","public class Solution {}")))).andExpect(status().isOk());
    }
    assertEquals(List.of(1,2,3),difficulties);
    assertProgress(student,1,0,0);
    var after=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("VARIABLE_BASIC",after.path("skill").path("code").asText());
  }

  @Test void outdatedLlmExplanationIsRegeneratedAndKeptWhenGenerationFails() throws Exception {
    String token=createStudentAndLogin("explanation-student"); long student=studentId("explanation-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"LOGICAL_OR");
    addTask("LOGICAL_OR","or task");
    db.update("insert into explanations(skill_code,content,source,prompt_version) values('LOGICAL_OR','old dry text','LLM',1)");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("LOGICAL_OR"))).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("LOGICAL_OR"))).thenReturn(generated("LOGICAL_OR", true));
    start(token);
    var kept=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("old dry text",kept.path("explanation").path("content").asText());
    when(generator.generateExplanation(eq(student),brief("LOGICAL_OR"))).thenReturn(Optional.of(new GeneratedExplanation("LOGICAL_OR","### Зачем это нужно\nподробно")));
    var fresh=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("### Зачем это нужно\nподробно",fresh.path("explanation").path("content").asText());
    assertEquals(LearningContentGenerator.EXPLANATION_PROMPT_VERSION,db.queryForObject("select prompt_version from explanations where skill_code='LOGICAL_OR'",Integer.class));
  }

  @Test void pythonTrackHasItsOwnDiagnosticLessonsAndProgress() throws Exception {
    String token=createStudentAndLogin("python-student"); long student=studentId("python-student");
    submitDiagnostic(token,student,false);
    int javaLesson=start(token);
    var pyDiagnostic=json.readTree(mvc.perform(get("/api/diagnostic").param("language","PYTHON").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertFalse(pyDiagnostic.path("completed").asBoolean());
    assertEquals(db.queryForObject("select count(*) from diagnostic_questions where language='PYTHON'",Integer.class),pyDiagnostic.path("questions").size());
    assertTrue(pyDiagnostic.path("questions").path(0).path("skillCode").asText().startsWith("PY_"));
    var answers=new ArrayList<Map<String,Object>>();
    for(var q:pyDiagnostic.path("questions")){var a=new LinkedHashMap<String,Object>();a.put("questionId",q.path("id").asLong());answers.add(a);}
    mvc.perform(post("/api/diagnostic").param("language","PYTHON").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("answers",answers)))).andExpect(status().isOk());
    var pyStart=json.readTree(mvc.perform(post("/api/lessons/start").param("language","PYTHON").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(1,pyStart.path("lesson").path("number").asInt(),"Python lessons are numbered separately from Java");
    assertEquals("PYTHON",pyStart.path("lesson").path("language").asText());
    var next=json.readTree(mvc.perform(get("/api/learning/next").param("language","PYTHON").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("PY_BASIC_CODE_READING",next.path("skill").path("code").asText());
    long task=next.path("task").path("id").asLong();
    assertEquals(1,db.queryForObject("select difficulty from tasks where id=?",Integer.class,task));
    assertTrue(next.path("explanation").path("content").asText().contains("print"));
    mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",task,"sourceCode","print('Привет', end='')")))).andExpect(status().isOk());
    verify(runner).run(eq(Language.PYTHON),eq("print('Привет', end='')"),contains("def run_checks"));
    var py=json.readTree(mvc.perform(get("/api/progress").param("language","PYTHON").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(1,py.path("solvedTasks").asInt()); assertEquals(1,py.path("activity").size());
    assertTrue(py.path("skills").path(0).path("skillCode").asText().startsWith("PY_"));
    var java=json.readTree(mvc.perform(get("/api/progress").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(0,java.path("solvedTasks").asInt()); assertEquals("JAVA",java.path("language").asText());
    var javaCurrent=json.readTree(mvc.perform(get("/api/lessons/current").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(javaLesson,javaCurrent.path("lesson").path("number").asInt(),"the Java lesson stays open while Python is studied");
  }

  @Test void unknownLanguageIsRejected() throws Exception {
    String token=createStudentAndLogin("lang-student");
    var body=json.readTree(mvc.perform(get("/api/diagnostic").param("language","COBOL").cookie(cookie(token))).andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
    assertEquals("UNKNOWN_LANGUAGE",body.path("error").asText());
  }

  @Test void adminChangesPasswordAndClosesStudentSessions() throws Exception {
    String token=createStudentAndLogin("pwd-student"); long student=studentId("pwd-student"); String admin=login("admin","admin-pass");
    var weak=json.readTree(mvc.perform(patch("/api/admin/students/{id}/password",student).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"password\":\"123\"}")).andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
    assertEquals("WEAK_PASSWORD",weak.path("error").asText());
    var changed=json.readTree(mvc.perform(patch("/api/admin/students/{id}/password",student).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"password\":\"new-secret-1\"}")).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(1,changed.path("sessionsClosed").asInt());
    mvc.perform(get("/api/auth/me").cookie(cookie(token))).andExpect(status().isUnauthorized());
    mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content("{\"login\":\"pwd-student\",\"password\":\"student-pass\"}")).andExpect(status().isBadRequest());
    login("pwd-student","new-secret-1");
    mvc.perform(patch("/api/admin/students/{id}/password",student).cookie(cookie(login("pwd-student","new-secret-1"))).contentType(MediaType.APPLICATION_JSON).content("{\"password\":\"hacker-pass\"}")).andExpect(status().isBadRequest());
  }

  @Test void duplicateLoginIsAClearError() throws Exception {
    createStudentAndLogin("dup-student"); String admin=login("admin","admin-pass");
    var body=json.readTree(mvc.perform(post("/api/admin/students").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login","dup-student","password","other-pass","displayName","Dup")))).andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
    assertEquals("LOGIN_TAKEN",body.path("error").asText());
  }

  @Test void llmUsageAnalyticsAggregatesCalls() throws Exception {
    createStudentAndLogin("usage-student"); long student=studentId("usage-student"); String admin=login("admin","admin-pass");
    db.update("delete from llm_calls");
    db.update("insert into llm_calls(user_id,purpose,language,status,duration_ms,input_tokens,cached_input_tokens,output_tokens,reasoning_tokens,total_tokens) values(?, 'CHAT','JAVA','OK',1000,100,20,50,10,150)",student);
    db.update("insert into llm_calls(user_id,purpose,language,status,duration_ms,total_tokens,outcome) values(?, 'TASK','PYTHON','OK',3000,400,'ACCEPTED')",student);
    db.update("insert into llm_calls(user_id,purpose,language,status,error,duration_ms) values(?, 'TASK','PYTHON','TIMEOUT','LlmUnavailableException: timeout',240000)",student);
    db.update("insert into llm_calls(user_id,purpose,language,status,duration_ms,created_at) values(?, 'CHAT','JAVA','OK',500,datetime('now','-40 days'))",student);
    var usage=json.readTree(mvc.perform(get("/api/admin/llm/usage").param("days","30").cookie(cookie(admin))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    var totals=usage.path("totals");
    assertEquals(3,totals.path("calls").asInt(),"calls older than the period are excluded");
    assertEquals(1,totals.path("errors").asInt()); assertEquals(1,totals.path("timeouts").asInt());
    assertEquals(550,totals.path("totalTokens").asInt()); assertEquals(1,totals.path("tasksAccepted").asInt());
    assertEquals(2000,totals.path("avgMs").asInt(),"average duration counts successful calls only");
    assertEquals(2,usage.path("byPurpose").size()); assertEquals(1,usage.path("byStudent").size());
    assertEquals(3,usage.path("byStudent").path(0).path("calls").asInt());
    assertEquals("TIMEOUT",usage.path("recentErrors").path(0).path("status").asText());
    mvc.perform(get("/api/admin/llm/usage").cookie(cookie(createStudentAndLogin("nosy-student")))).andExpect(status().isBadRequest());
  }

  @Test void statementsWithPlatformInternalsAreDetected() {
    assertEquals("solution.py",ApiController.internalTerm("Напиши код в файле `solution.py`."));
    assertEquals("run_checks",ApiController.internalTerm("Функция run_checks проверит"));
    assertNull(ApiController.internalTerm("Напиши функцию `area(width, height)` в редакторе."));
  }

  @Test void generatedTaskLeakingInternalsIsRejected() throws Exception {
    String token=createStudentAndLogin("leak-student"); long student=studentId("leak-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"SWITCH_BASIC");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("SWITCH_BASIC"))).thenReturn(Optional.empty());
    String test="public class TestHarness { public static void main(String[] a) { System.out.print(\""+PistonCodeRunner.PASS_MARKER_PLACEHOLDER+"\"); } }";
    when(generator.generateTask(eq(student),brief("SWITCH_BASIC"))).thenReturn(new GeneratedTask("SWITCH_BASIC","leaky","Код проверит TestHarness","",test,"TestHarness.java","public class Solution {}",List.of("SWITCH_BASIC"),List.of(),functionGoal(),wrongSolutions()));
    start(token);
    var response=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("LLM_GENERATION_FAILED_VALIDATION",response.path("reason").asText());
    assertEquals(0,db.queryForObject("select count(*) from tasks where title='leaky'",Integer.class));
  }

  @Test void legacyWeakTaskGetsVerifiedChecksWithoutRecalculatingCredit() throws Exception {
    String token=createStudentAndLogin("legacy-student"); long student=studentId("legacy-student");
    db.update("update tasks set quality_version=? where coalesce(quality_version,0)<?",LearningContentGenerator.TASK_QUALITY_VERSION,LearningContentGenerator.TASK_QUALITY_VERSION); // only this test's tasks are pending
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,source) values('PY_ARITHMETIC_BASIC','Считаем стоимость билетов','Посчитай стоимость 4 билетов по 6 рублей умножением.','','def run_checks():\n    assert True\n','test_solution.py','PYTHON','LLM')");
    long weak=db.queryForObject("select last_insert_rowid()",Long.class); db.update("insert into task_target_skills(task_id,skill_code) values(?, 'PY_ARITHMETIC_BASIC')",weak);
    db.update("insert into successful_task_credit(user_id,task_id) values(?,?)",student,weak);
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,source) values('PY_ARITHMETIC_BASIC','Безнадёжная задача','Условие','','def run_checks():\n    assert True\n','test_solution.py','PYTHON','LLM')");
    long hopeless=db.queryForObject("select last_insert_rowid()",Long.class); db.update("insert into task_target_skills(task_id,skill_code) values(?, 'PY_ARITHMETIC_BASIC')",hopeless);
    var goal=json.readTree("{\"kind\":\"FIXED_ARITHMETIC\",\"operation\":\"*\",\"operands\":[4,6],\"expectedOutput\":\"24\\n\",\"functionName\":null,\"requiredConstructs\":[]}");
    String strongChecks="import contextlib, io\n\ndef run_checks():\n    buffer = io.StringIO()\n    with contextlib.redirect_stdout(buffer):\n        import solution\n    assert buffer.getvalue() == '24\\n'\n";
    when(generator.available()).thenReturn(true);
    when(generator.repairTask(any(ContentBrief.class),argThat(t->t!=null&&t.id()==weak))).thenReturn(new GeneratedTask("PY_ARITHMETIC_BASIC","x","x","",strongChecks,"test_solution.py","print(4 * 6)\n",List.of("PY_ARITHMETIC_BASIC"),List.of(),goal,List.of()));
    when(generator.repairTask(any(ContentBrief.class),argThat(t->t!=null&&t.id()==hopeless))).thenReturn(new GeneratedTask("PY_ARITHMETIC_BASIC","x","x","",strongChecks,"test_solution.py","print(4 * 6)\n",List.of("PY_ARITHMETIC_BASIC"),List.of(),goal,List.of()));
    // Piston stand-in: only the exact calculation passes, and only for the repaired task; the hopeless task's checks accept anything.
    when(runner.run(eq(Language.PYTHON),anyString(),anyString())).thenAnswer(call->{String source=((String)call.getArgument(1)).strip();String test=call.getArgument(2);
      boolean hopelessCall=test.contains("hopeless-marker");
      return hopelessCall||source.equals("print(4 * 6)")?new PistonCodeRunner.Run(true,"ok"):new PistonCodeRunner.Run(false,"Неверный результат.");});
    when(generator.repairTask(any(ContentBrief.class),argThat(t->t!=null&&t.id()==hopeless))).thenReturn(new GeneratedTask("PY_ARITHMETIC_BASIC","x","x","",strongChecks+"# hopeless-marker\n","test_solution.py","print(4 * 6)\n",List.of("PY_ARITHMETIC_BASIC"),List.of(),goal,List.of()));
    assertEquals(1,taskAudit.auditPending());
    var repaired=db.queryForMap("select test_source,goal_json,quality_version,statement,active from tasks where id=?",weak);
    assertEquals(strongChecks,repaired.get("test_source")); assertEquals(LearningContentGenerator.TASK_QUALITY_VERSION,((Number)repaired.get("quality_version")).intValue());
    assertEquals("Посчитай стоимость 4 билетов по 6 рублей умножением.",repaired.get("statement"),"students keep the statement they saw");
    assertEquals(1,db.queryForObject("select count(*) from successful_task_credit where user_id=? and task_id=?",Integer.class,student,weak),"earlier credit is not recalculated");
    assertEquals(0,db.queryForObject("select active from tasks where id=?",Integer.class,hopeless),"a task whose checks cannot be made reliable is retired");
    verify(generator,times(TaskAudit.REPAIR_ATTEMPTS)).repairTask(any(ContentBrief.class),argThat(t->t!=null&&t.id()==hopeless));
    assertEquals(0,taskAudit.auditPending(),"nothing left to re-verify");
  }

  @Test void adminDeletesStudentWithAllPersonalData() throws Exception {
    String token=createStudentAndLogin("gone-student"); long student=studentId("gone-student"); submitDiagnostic(token,student,false); start(token);
    long task=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()).path("task").path("id").asLong();
    mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",task,"sourceCode","public class Solution {}")))).andExpect(status().isOk());
    db.update("insert into llm_calls(user_id,purpose,language,status,duration_ms) values(?, 'CHAT','JAVA','OK',100)",student);
    String admin=login("admin","admin-pass");
    var refused=json.readTree(mvc.perform(delete("/api/admin/students/{id}",student).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"confirmLogin\":\"someone-else\"}")).andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
    assertEquals("CONFIRMATION_REQUIRED",refused.path("error").asText());
    mvc.perform(delete("/api/admin/students/{id}",student).cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"confirmLogin\":\"gone-student\"}")).andExpect(status().isBadRequest());
    var deleted=json.readTree(mvc.perform(delete("/api/admin/students/{id}",student).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"confirmLogin\":\"gone-student\"}")).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(1,deleted.path("lessons").asInt()); assertEquals(1,deleted.path("submissions").asInt());
    for(String table:List.of("sessions","student_languages","diagnostic_answers","diagnostic_skill_results","student_skills","successful_task_credit","lessons"))
      assertEquals(0,db.queryForObject("select count(*) from "+table+" where user_id=?",Integer.class,student),table);
    assertEquals(0,db.queryForObject("select count(*) from users where id=?",Integer.class,student));
    assertEquals(1,db.queryForObject("select count(*) from llm_calls where user_id is null and purpose='CHAT' and duration_ms=100",Integer.class),"usage stays in analytics without the person");
    assertEquals(1,db.queryForObject("select count(*) from tasks where id=?",Integer.class,task),"shared tasks stay");
    mvc.perform(get("/api/auth/me").cookie(cookie(token))).andExpect(status().isUnauthorized());
    mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content("{\"login\":\"gone-student\",\"password\":\"student-pass\"}")).andExpect(status().isBadRequest());
    createStudentAndLogin("gone-student");
  }

  @Test void revokedCreditRecalculatesProgressAndTheTaskComesBackFirst() throws Exception {
    String token=createStudentAndLogin("revoke-student"); long student=studentId("revoke-student"); submitDiagnostic(token,student,false);
    db.update("insert into student_skills(user_id,skill_code,completed_iterations,iteration_successes,mastered) select ?,code,3,0,1 from skills where code<>'BASIC_CODE_READING' and language='JAVA'",student);
    int lesson1=start(token); solveThree(token); assertProgress(student,1,0,0);
    long lessonId=db.queryForObject("select id from lessons where user_id=? and lesson_number=?",Long.class,student,lesson1);
    long task=db.queryForObject("select task_id from lesson_tasks where lesson_id=? order by rowid limit 1",Long.class,lessonId);
    finish(token,lesson1);
    String admin=login("admin","admin-pass");
    mvc.perform(post("/api/admin/students/{id}/lessons/{l}/tasks/{t}/revoke",student,lessonId,task).cookie(cookie(token))).andExpect(status().isBadRequest());
    var revoked=json.readTree(mvc.perform(post("/api/admin/students/{id}/lessons/{l}/tasks/{t}/revoke",student,lessonId,task).cookie(cookie(admin))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(1,revoked.path("revokedSubmissions").asInt()); assertFalse(revoked.path("redoInOpenLesson").asBoolean());
    // The completed iteration loses one of its three tasks: progress is recomputed with the normal rules.
    assertProgress(student,0,0,2);
    assertEquals(0,db.queryForObject("select count(*) from skill_iterations where user_id=?",Integer.class,student));
    assertEquals(0,db.queryForObject("select count(*) from successful_task_credit where user_id=? and task_id=?",Integer.class,student,task));
    var detail=json.readTree(mvc.perform(get("/api/admin/students/{id}/lessons/{l}",student,lessonId).cookie(cookie(admin))).andReturn().getResponse().getContentAsString());
    var submission=findTask(detail,task).path("submissions").path(0);
    assertEquals(0,submission.path("passed").asInt()); assertFalse(submission.path("revokedAt").isNull(),"history keeps the solution, marked revoked");
    mvc.perform(post("/api/admin/students/{id}/lessons/{l}/tasks/{t}/revoke",student,lessonId,task).cookie(cookie(admin))).andExpect(status().isBadRequest());
    start(token);
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(task,next.path("task").path("id").asLong(),"the revoked task is assigned before new work");
    assertTrue(next.path("task").path("redo").asBoolean());
    assertEquals(0,db.queryForObject("select count(*) from pending_redos where user_id=?",Integer.class,student));
    mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",task,"sourceCode","public class Solution {}")))).andExpect(status().isOk());
    assertEquals(1,db.queryForObject("select count(*) from successful_task_credit where user_id=? and task_id=?",Integer.class,student,task),"solving it again earns the credit back");
  }

  @Test void revokingInsideTheOpenLessonMakesTheTaskUnsolvedAgain() throws Exception {
    String token=createStudentAndLogin("revoke-open"); long student=studentId("revoke-open"); submitDiagnostic(token,student,false); start(token);
    long task=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andReturn().getResponse().getContentAsString()).path("task").path("id").asLong();
    mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",task,"sourceCode","public class Solution {}")))).andExpect(status().isOk());
    long lessonId=db.queryForObject("select id from lessons where user_id=? and finished_at is null",Long.class,student);
    var revoked=json.readTree(mvc.perform(post("/api/admin/students/{id}/lessons/{l}/tasks/{t}/revoke",student,lessonId,task).cookie(cookie(login("admin","admin-pass")))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(revoked.path("redoInOpenLesson").asBoolean());
    assertEquals(0,db.queryForObject("select count(*) from pending_redos where user_id=?",Integer.class,student));
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andReturn().getResponse().getContentAsString());
    assertEquals(task,next.path("task").path("id").asLong()); assertTrue(next.path("task").path("redo").asBoolean());
    // The lesson ends before the student redoes it: the task must still come back first.
    mvc.perform(post("/api/admin/students/{id}/lessons/{l}/finish",student,lessonId).cookie(cookie(login("admin","admin-pass")))).andExpect(status().isOk());
    assertEquals(1,db.queryForObject("select count(*) from pending_redos where user_id=? and task_id=?",Integer.class,student,task));
    start(token);
    assertEquals(task,json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andReturn().getResponse().getContentAsString()).path("task").path("id").asLong());
  }

  @Test void adminFinishesAnyStudentsOpenLesson() throws Exception {
    String token=createStudentAndLogin("finish-by-admin"); long student=studentId("finish-by-admin"); submitDiagnostic(token,student,false); start(token);
    long lessonId=db.queryForObject("select id from lessons where user_id=? and finished_at is null",Long.class,student);
    mvc.perform(post("/api/admin/students/{id}/lessons/{l}/finish",student,lessonId).cookie(cookie(token))).andExpect(status().isBadRequest());
    String admin=login("admin","admin-pass");
    var finished=json.readTree(mvc.perform(post("/api/admin/students/{id}/lessons/{l}/finish",student,lessonId).cookie(cookie(admin))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertFalse(finished.path("lesson").path("finishedAt").isNull());
    mvc.perform(post("/api/admin/students/{id}/lessons/{l}/finish",student,lessonId).cookie(cookie(admin))).andExpect(status().isBadRequest());
    mvc.perform(post("/api/admin/students/{id}/lessons/{l}/finish",student+1000,lessonId).cookie(cookie(admin))).andExpect(status().isBadRequest());
    assertTrue(json.readTree(mvc.perform(get("/api/lessons/current").cookie(cookie(token))).andReturn().getResponse().getContentAsString()).path("lesson").isNull());
  }
  private static com.fasterxml.jackson.databind.JsonNode findTask(com.fasterxml.jackson.databind.JsonNode detail,long id){for(var t:detail.path("tasks"))if(t.path("id").asLong()==id)return t;throw new AssertionError(id);}

  private static ContentBrief brief(String skill){return argThat(b->b!=null&&skill.equals(b.skillCode()));}

  private String createStudentAndLogin(String login) throws Exception { String admin=login("admin","admin-pass"); mvc.perform(post("/api/admin/students").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login",login,"password","student-pass","displayName",login)))).andExpect(status().isOk()); return login(login,"student-pass"); }
  private String login(String login,String password) throws Exception { var r=mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login",login,"password",password)))).andExpect(status().isOk()).andReturn().getResponse(); return r.getCookie("adaptive_session").getValue(); }
  private long studentId(String login){return db.queryForObject("select id from users where login=?",Long.class,login);}
  private void submitDiagnostic(String token,long user,boolean correctBlockZero) throws Exception { var rows=db.queryForList("select id,correct_option,block_no from diagnostic_questions where language='JAVA' order by id"); var answers=new ArrayList<Map<String,Object>>();for(var q:rows){boolean correct=correctBlockZero&&((Number)q.get("block_no")).intValue()==0;var answer=new LinkedHashMap<String,Object>();answer.put("questionId",q.get("id"));if(correct)answer.put("selectedOption",q.get("correct_option"));answers.add(answer);}mvc.perform(post("/api/diagnostic").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("answers",answers)))).andExpect(status().isOk());}
  private int start(String token) throws Exception { return json.readTree(mvc.perform(post("/api/lessons/start").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()).path("lesson").path("number").asInt(); }
  private void finish(String token,int lesson) throws Exception { long id=db.queryForObject("select id from lessons where user_id=(select user_id from sessions where token_hash=?) and lesson_number=?",Long.class,Hashing.sha256(token),lesson);mvc.perform(post("/api/lessons/{id}/finish",id).cookie(cookie(token))).andExpect(status().isOk()); }
  private void solveThree(String token) throws Exception { for(int i=0;i<3;i++){var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());long task=next.path("task").path("id").asLong();assertTrue(task>0);mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",task,"sourceCode","public class Solution {}")))).andExpect(status().isOk());} }
  private void assertProgress(long user,int iterations,int mastered,int current){var row=db.queryForMap("select completed_iterations,mastered,iteration_successes from student_skills where user_id=? and skill_code='BASIC_CODE_READING'",user);assertEquals(iterations,((Number)row.get("completed_iterations")).intValue());assertEquals(mastered,((Number)row.get("mastered")).intValue());assertEquals(current,((Number)row.get("iteration_successes")).intValue());}
  private void addTask(String title){addTask("BASIC_CODE_READING", title);}
  private void addTask(String skillCode,String title){db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name) values(?,?,?, '', 'class TestHarness {}','TestHarness.java')",skillCode,title,title);long id=db.queryForObject("select last_insert_rowid()",Long.class);db.update("insert into task_target_skills(task_id,skill_code) values(?, ?)",id,skillCode);}
  private jakarta.servlet.http.Cookie cookie(String value){return new jakarta.servlet.http.Cookie("adaptive_session",value);}
  private int countLessonTasks(long student){return db.queryForObject("select count(*) from lesson_tasks where lesson_id=(select id from lessons where user_id=? and finished_at is null)",Integer.class,student);}
  private void prepareOnlySkill(long student,String skill){db.update("insert into student_skills(user_id,skill_code,completed_iterations,mastered) select ?,code,3,1 from skills where code<>?",student,skill);}
  private GeneratedTask generated(String skill,boolean valid){String test="public class TestHarness { public static void main(String[] a) { Solution.answer(1); Solution.answer(2); Solution.answer(3); System.out.print(\""+(valid?PistonCodeRunner.PASS_MARKER_PLACEHOLDER:"missing")+"\"); } }";return new GeneratedTask(skill,"generated "+skill,"statement","",test,"TestHarness.java","public class Solution { static int answer(int x) { return x; } }",List.of(skill),List.of(),functionGoal(),wrongSolutions());}
  private com.fasterxml.jackson.databind.JsonNode functionGoal(){try{return json.readTree("{\"kind\":\"FUNCTION_BEHAVIOR\",\"operation\":null,\"operands\":[],\"expectedOutput\":null,\"functionName\":\"answer\",\"requiredConstructs\":[]}");}catch(Exception e){throw new IllegalStateException(e);}}
  private static List<TaskGoal.Mutant> wrongSolutions(){return List.of(new TaskGoal.Mutant("hard-codes the first example","public class Solution { static int answer(int x) { return 1; } } // WRONG"),new TaskGoal.Mutant("off by one","public class Solution { static int answer(int x) { return x + 1; } } // WRONG"));}
  private static com.fasterxml.jackson.databind.JsonNode findSkill(com.fasterxml.jackson.databind.JsonNode progress,String code){for(var skill:progress.path("skills"))if(code.equals(skill.path("skillCode").asText()))return skill;throw new AssertionError(code);}
}
