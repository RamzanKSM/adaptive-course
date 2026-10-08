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
import java.util.concurrent.atomic.AtomicReference;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.contains;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class LearningFlowIntegrationTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json; @Autowired TaskAudit taskAudit; @Autowired LlmSettings llmSettings; @Autowired HardTaskBank hardTaskBank;
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
  @BeforeEach void prepare() { db.update("update users set password_hash=? where login='admin'",new BCryptPasswordEncoder().encode("admin-pass")); when(runner.configured()).thenReturn(true); when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true,"READY","17.0.1")); when(runner.run(any(Language.class),anyString(),anyString())).thenAnswer(call->((String)call.getArgument(1)).contains("WRONG")?new PistonCodeRunner.Run(false,"Неверный вывод программы."):new PistonCodeRunner.Run(true,"Решение прошло скрытые проверки")); when(tutor.status(anyLong())).thenReturn(new LlmStatus(false,false,false,"DISABLED", "gpt-6-luna"));  when(runner.runRaw(any(Language.class),anyString(),anyString())).thenReturn(recordedAnswers(6)); }

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
    // Iterations shrink: three tasks to learn the topic, two to repeat it, one to confirm it.
    int lesson1=start(token); solve(token,3); assertProgress(student,1,0,0); finish(token,lesson1);
    int lesson2=start(token); solve(token,2); assertProgress(student,2,0,0); finish(token,lesson2);
    int lesson3=start(token); var skipped=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()); assertEquals("NO_DUE_SKILL",skipped.path("reason").asText()); finish(token,lesson3);
    int lesson4=start(token); solve(token,1); assertProgress(student,3,1,0);
  }

  @Test void generatedTaskIsValidatedStoredOnceAndThenRestored() throws Exception {
    String token=createStudentAndLogin("generated-student"); long student=studentId("generated-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"METHOD_PARAMETERS");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("METHOD_PARAMETERS"))).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("METHOD_PARAMETERS"))).thenReturn(generated("METHOD_PARAMETERS", true));
    start(token);
    var first=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(first.path("task").path("id").asLong()>0);
    assertEquals(1,db.queryForObject("select count(*) from tasks where title='generated METHOD_PARAMETERS'",Integer.class));
    var reloaded=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(first.path("task").path("id").asLong(),reloaded.path("task").path("id").asLong());
    verify(generator,times(1)).generateTask(eq(student),brief("METHOD_PARAMETERS"));
    assertEquals(1,db.queryForObject("select difficulty from tasks where title='generated METHOD_PARAMETERS'",Integer.class));
    var requested=org.mockito.ArgumentCaptor.forClass(ContentBrief.class); verify(generator).generateTask(eq(student),requested.capture());
    assertEquals(1,requested.getValue().difficulty()); assertEquals("Параметры и возвращаемое значение",requested.getValue().skillTitle()); assertFalse(requested.getValue().earlierSkills().isEmpty());
  }

  @Test void invalidGeneratedHarnessIsNeverStored() throws Exception {
    String token=createStudentAndLogin("invalid-generator-student"); long student=studentId("invalid-generator-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"STATIC_BASIC");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("STATIC_BASIC"))).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("STATIC_BASIC"))).thenReturn(generated("STATIC_BASIC", false));
    start(token);
    var response=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("LLM_GENERATION_FAILED_VALIDATION",response.path("reason").asText());
    assertEquals(0,db.queryForObject("select count(*) from tasks where title='generated STATIC_BASIC'",Integer.class));
    verify(generator,times(ApiController.GENERATION_ATTEMPTS)).generateTask(eq(student),brief("STATIC_BASIC"));
  }

  @Test void invalidGeneratedCandidateIsRetriedAndOnlyValidCandidateIsStored() throws Exception {
    String token=createStudentAndLogin("retry-generator-student"); long student=studentId("retry-generator-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"THIS_BASIC");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("THIS_BASIC"))).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("THIS_BASIC"))).thenReturn(generated("THIS_BASIC", false),generated("THIS_BASIC", true));
    start(token);
    var response=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(response.path("task").path("id").asLong()>0);
    assertEquals(1,db.queryForObject("select count(*) from tasks where title='generated THIS_BASIC'",Integer.class));
    verify(generator,times(2)).generateTask(eq(student),brief("THIS_BASIC"));
  }

  @Test void finishingALessonWhileATaskIsGeneratedKeepsTheTaskForTheNextLesson() throws Exception {
    String token=createStudentAndLogin("finish-while-generating"); long student=studentId("finish-while-generating"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"ENCAPSULATION_BASIC");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("ENCAPSULATION_BASIC"))).thenReturn(Optional.empty());
    start(token); long first=db.queryForObject("select id from lessons where user_id=? and finished_at is null",Long.class,student);
    // The student presses «Завершить урок» while the model is still writing the task.
    when(generator.generateTask(eq(student),brief("ENCAPSULATION_BASIC"))).thenAnswer(call->{
      mvc.perform(post("/api/lessons/{id}/finish",first).cookie(cookie(token))).andExpect(status().isOk());
      return generated("ENCAPSULATION_BASIC",true);
    });
    var response=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("LESSON_FINISHED",response.path("reason").asText()); assertTrue(response.path("task").isNull());
    long kept=db.queryForObject("select id from tasks where title='generated ENCAPSULATION_BASIC'",Long.class);
    assertEquals(0,db.queryForObject("select count(*) from lesson_tasks where lesson_id=?",Integer.class,first),"a finished lesson gets no new task");
    assertEquals("GENERATED",db.queryForObject("select reason from pending_redos where user_id=? and task_id=?",String.class,student,kept));
    // The next lesson starts with the kept task; it is not generated again.
    start(token);
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(kept,next.path("task").path("id").asLong()); assertFalse(next.path("task").path("redo").asBoolean(),"a kept task is new work, not a redo");
    verify(generator,times(1)).generateTask(eq(student),brief("ENCAPSULATION_BASIC"));
    assertEquals(0,db.queryForObject("select count(*) from pending_redos where user_id=?",Integer.class,student));
  }

  @Test void finishingALessonWhileTheExplanationIsGeneratedKeepsTheExplanationAndStartsNoTask() throws Exception {
    String token=createStudentAndLogin("finish-while-explaining"); long student=studentId("finish-while-explaining"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"FOR_LOOP_BASIC");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    db.update("delete from explanations where skill_code='FOR_LOOP_BASIC'");
    start(token); long first=db.queryForObject("select id from lessons where user_id=? and finished_at is null",Long.class,student);
    when(generator.generateExplanation(eq(student),brief("FOR_LOOP_BASIC"))).thenAnswer(call->{
      mvc.perform(post("/api/admin/students/{id}/lessons/{lesson}/finish",student,first).cookie(cookie(login("admin","admin-pass")))).andExpect(status().isOk());
      return Optional.of(new GeneratedExplanation("FOR_LOOP_BASIC","Цикл for повторяет тело, пока условие истинно."));
    });
    var response=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("LESSON_FINISHED",response.path("reason").asText());
    assertEquals("LLM",db.queryForObject("select source from explanations where skill_code='FOR_LOOP_BASIC'",String.class),"the explanation is saved for the topic");
    verify(generator,never()).generateTask(eq(student),brief("FOR_LOOP_BASIC"));
    assertEquals(0,db.queryForObject("select count(*) from lesson_tasks where lesson_id=?",Integer.class,first));
  }

  @Test void logoutFinishesTheStudentsOpenLessonsInEveryCourse() throws Exception {
    String token=createStudentAndLogin("logout-student"); long student=studentId("logout-student");
    for(String lang:List.of("JAVA","PYTHON")) db.update("insert into lessons(user_id,lesson_number,language,language_lesson_number) values(?,(select coalesce(max(lesson_number),0)+1 from lessons where user_id=?),?,1)",student,student,lang);
    String other=createStudentAndLogin("logout-bystander"); long bystander=studentId("logout-bystander");
    db.update("insert into lessons(user_id,lesson_number,language,language_lesson_number) values(?,1,'JAVA',1)",bystander);
    mvc.perform(post("/api/auth/logout").cookie(cookie(token))).andExpect(status().isNoContent());
    assertEquals(0,db.queryForObject("select count(*) from lessons where user_id=? and finished_at is null",Integer.class,student));
    assertEquals(1,db.queryForObject("select count(*) from lessons where user_id=? and finished_at is null",Integer.class,bystander),"only the student who logged out");
    String admin=login("admin","admin-pass");
    mvc.perform(post("/api/auth/logout").cookie(cookie(admin))).andExpect(status().isNoContent());
    assertEquals(1,db.queryForObject("select count(*) from lessons where user_id=? and finished_at is null",Integer.class,bystander),"an admin logout ends no lessons");
    assertNotNull(other);
  }

  @Test void runShowsTheConsoleWithoutCountingAnAttempt() throws Exception {
    String token=createStudentAndLogin("console-runner"); long student=studentId("console-runner");
    when(runner.console(any(Language.class),anyString(),anyString())).thenReturn(new PistonCodeRunner.Console("OK","30\n",null,false));
    var run=json.readTree(mvc.perform(post("/api/run").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"sourceCode\":\"print(int(input()) * 6)\",\"stdin\":\"5\\n\"}").param("language","PYTHON"))
        .andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    verify(runner).console(Language.PYTHON,"print(int(input()) * 6)","5\n"); // what the student typed into «Входные данные»
    assertEquals("OK",run.path("console").path("status").asText()); assertEquals("30\n",run.path("console").path("stdout").asText());
    assertEquals(0,db.queryForObject("select count(*) from submissions s join lessons l on l.id=s.lesson_id where l.user_id=?",Integer.class,student),"a run is not a submission");
    mvc.perform(post("/api/run").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"sourceCode\":\" \"}")).andExpect(status().isBadRequest());
    // Free practice, but limited per student so the shared runner cannot be flooded.
    for(int i=1;i<30;i++) mvc.perform(post("/api/run").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"sourceCode\":\"print(1)\"}")).andExpect(status().isOk());
    mvc.perform(post("/api/run").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"sourceCode\":\"print(1)\"}"))
        .andExpect(status().isTooManyRequests()).andExpect(org.springframework.test.web.servlet.result.MockMvcResultMatchers.header().exists("Retry-After"));
    String other=createStudentAndLogin("console-neighbour");
    mvc.perform(post("/api/run").cookie(cookie(other)).contentType(MediaType.APPLICATION_JSON).content("{\"sourceCode\":\"print(1)\"}")).andExpect(status().isOk());
  }

  @Test void submissionShowsAndKeepsWhatTheProgramPrinted() throws Exception {
    String token=createStudentAndLogin("console-attempt"); long student=studentId("console-attempt"); submitDiagnostic(token,student,false);
    addTask("console task"); prepareOnlySkill(student,"BASIC_CODE_READING"); start(token);
    when(runner.console(any(Language.class),anyString())).thenReturn(new PistonCodeRunner.Console("OK","Итого: 24\n",null,false));
    long task=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andReturn().getResponse().getContentAsString()).path("task").path("id").asLong();
    var appender=new ch.qos.logback.core.read.ListAppender<ch.qos.logback.classic.spi.ILoggingEvent>(); appender.start();
    var controllerLog=(ch.qos.logback.classic.Logger)org.slf4j.LoggerFactory.getLogger(ApiController.class); controllerLog.addAppender(appender);
    com.fasterxml.jackson.databind.JsonNode attempt; String requestId;
    try {
      var result=mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",task,"sourceCode","WRONG"))))
          .andExpect(status().isOk()).andReturn();
      attempt=json.readTree(result.getResponse().getContentAsString()); requestId=result.getResponse().getHeader("X-Request-Id");
    } finally { controllerLog.detachAppender(appender); }
    assertFalse(attempt.path("passed").asBoolean()); assertEquals("Итого: 24\n",attempt.path("console").path("stdout").asText());
    // One timing line per check, with the request id of the request's other log lines.
    var timing=appender.list.stream().map(e->e.getFormattedMessage()).filter(m->m.startsWith("CHECK_TIMING")).toList();
    assertEquals(1,timing.size(),timing.toString());
    assertTrue(timing.getFirst().matches("CHECK_TIMING request="+requestId+" student="+student+" task="+task+" language=JAVA tests_ms=\\d+ console_queue_ms=\\d+ console_piston_ms=\\d+ console_wait_ms=\\d+ total_ms=\\d+"),timing.getFirst());
    long lesson=db.queryForObject("select id from lessons where user_id=? and finished_at is null",Long.class,student);
    var detail=json.readTree(mvc.perform(get("/api/admin/students/{id}/lessons/{lesson}",student,lesson).cookie(cookie(login("admin","admin-pass")))).andReturn().getResponse().getContentAsString());
    assertEquals("Итого: 24\n",detail.path("tasks").path(0).path("submissions").path(0).path("console").path("stdout").asText(),"the teacher sees it in the lesson history");
  }

  @Test void studentsHaveOptionalGroupsAndEditableLoginNameAndGroup() throws Exception {
    String admin=login("admin","admin-pass");
    java.util.function.Function<Map<String,Object>,com.fasterxml.jackson.databind.JsonNode> create=body->{ try { return json.readTree(mvc.perform(post("/api/admin/students").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(body))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()); } catch(Exception e){ throw new RuntimeException(e); } };
    var first=create.apply(Map.of("login","group-a1","password","student-pass","displayName","Аня","group","  ИВТ-1  "));
    assertEquals("ИВТ-1",first.path("group").asText(),"trimmed");
    var second=create.apply(Map.of("login","group-a2","password","student-pass","displayName","Боря","group","ивт-1"));
    assertEquals("ИВТ-1",second.path("group").asText(),"letter case does not split a group");
    var third=create.apply(Map.of("login","group-none","password","student-pass","displayName","Вера"));
    assertTrue(third.path("group").isNull(),"the group is optional");
    var list=json.readTree(mvc.perform(get("/api/admin/students").cookie(cookie(admin))).andReturn().getResponse().getContentAsString());
    assertEquals("ИВТ-1",findStudent(list,"group-a1").path("group").asText());

    // Login, name and group change; only the fields sent.
    String studentToken=login("group-none","student-pass");
    long vera=third.path("id").asLong();
    var updated=json.readTree(mvc.perform(patch("/api/admin/students/{id}",vera).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON)
        .content("{\"login\":\"vera.k\",\"displayName\":\"Вера К.\",\"group\":\"ИВТ-2\"}")).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("vera.k",updated.path("login").asText()); assertEquals("Вера К.",updated.path("displayName").asText()); assertEquals("ИВТ-2",updated.path("group").asText());
    mvc.perform(get("/api/progress").cookie(cookie(studentToken))).andExpect(status().isOk()); // the open session survives a login change
    login("vera.k","student-pass");
    mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content("{\"login\":\"group-none\",\"password\":\"student-pass\"}")).andExpect(status().isBadRequest());
    mvc.perform(patch("/api/admin/students/{id}",vera).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"login\":\"group-a1\"}")).andExpect(status().isBadRequest());
    mvc.perform(patch("/api/admin/students/{id}",vera).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"login\":\"  \"}")).andExpect(status().isBadRequest());
    var ungrouped=json.readTree(mvc.perform(patch("/api/admin/students/{id}",vera).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"group\":\"\"}")).andReturn().getResponse().getContentAsString());
    assertTrue(ungrouped.path("group").isNull()); assertEquals("vera.k",ungrouped.path("login").asText(),"fields not sent stay as they were");
    mvc.perform(patch("/api/admin/students/{id}",vera).cookie(cookie(studentToken)).contentType(MediaType.APPLICATION_JSON).content("{\"group\":\"X\"}")).andExpect(status().isBadRequest());

    // Renaming a group moves all its students; renaming into an existing group merges; an empty name removes it.
    mvc.perform(patch("/api/admin/students/{id}",vera).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"group\":\"Вечерняя\"}")).andExpect(status().isOk());
    var renamed=json.readTree(mvc.perform(post("/api/admin/groups/rename").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"from\":\"ИВТ-1\",\"to\":\"ИВТ-1 (2026)\"}")).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(2,renamed.path("students").asInt());
    assertEquals(2,db.queryForObject("select count(*) from users where group_name='ИВТ-1 (2026)'",Integer.class));
    mvc.perform(post("/api/admin/groups/rename").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"from\":\"Вечерняя\",\"to\":\"ивт-1 (2026)\"}")).andExpect(status().isOk());
    assertEquals(3,db.queryForObject("select count(*) from users where group_name='ИВТ-1 (2026)'",Integer.class),"merged into the existing spelling");
    mvc.perform(post("/api/admin/groups/rename").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"from\":\"ИВТ-1 (2026)\",\"to\":\"\"}")).andExpect(status().isOk());
    assertEquals(0,db.queryForObject("select count(*) from users where group_name is not null and login in ('group-a1','group-a2','vera.k')",Integer.class));
    mvc.perform(post("/api/admin/groups/rename").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"from\":\"нет такой\",\"to\":\"x\"}")).andExpect(status().isBadRequest());
  }
  private static com.fasterxml.jackson.databind.JsonNode findStudent(com.fasterxml.jackson.databind.JsonNode list,String login){for(var s:list.path("students"))if(login.equals(s.path("login").asText()))return s;throw new AssertionError("no student "+login);}

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
    String token=createStudentAndLogin("explanation-student"); long student=studentId("explanation-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"INTERFACE_BASIC");
    addTask("INTERFACE_BASIC","or task");
    db.update("insert into explanations(skill_code,content,source,prompt_version) values('INTERFACE_BASIC','old dry text','LLM',1)");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("INTERFACE_BASIC"))).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("INTERFACE_BASIC"))).thenReturn(generated("INTERFACE_BASIC", true));
    start(token);
    var kept=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("old dry text",kept.path("explanation").path("content").asText());
    when(generator.generateExplanation(eq(student),brief("INTERFACE_BASIC"))).thenReturn(Optional.of(new GeneratedExplanation("INTERFACE_BASIC","### Зачем это нужно\nподробно")));
    var fresh=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("### Зачем это нужно\nподробно",fresh.path("explanation").path("content").asText());
    assertEquals(LearningContentGenerator.EXPLANATION_PROMPT_VERSION,db.queryForObject("select prompt_version from explanations where skill_code='INTERFACE_BASIC'",Integer.class));
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
  private static com.fasterxml.jackson.databind.JsonNode findModel(com.fasterxml.jackson.databind.JsonNode settings,String id){for(var m:settings.path("models"))if(id.equals(m.path("id").asText()))return m;return null;}
  private static com.fasterxml.jackson.databind.JsonNode findTask(com.fasterxml.jackson.databind.JsonNode detail,long id){for(var t:detail.path("tasks"))if(t.path("id").asLong()==id)return t;throw new AssertionError(id);}

  @Test void adminSeesWhoHasAnOpenLesson() throws Exception {
    String token=createStudentAndLogin("active-list"); long student=studentId("active-list"); submitDiagnostic(token,student,false); start(token);
    createStudentAndLogin("idle-list");
    var list=json.readTree(mvc.perform(get("/api/admin/students").cookie(cookie(login("admin","admin-pass")))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    for(var s:list.path("students")){
      if("active-list".equals(s.path("login").asText())){ assertEquals(1,s.path("activeLessons").size()); assertEquals("JAVA",s.path("activeLessons").path(0).path("language").asText()); assertEquals(1,s.path("activeLessons").path(0).path("number").asInt()); }
      if("idle-list".equals(s.path("login").asText())) assertEquals(0,s.path("activeLessons").size());
    }
  }

  @Test void adminChangesReasoningAndLimitsWithValidation() throws Exception {
    String admin=login("admin","admin-pass");
    var settings=json.readTree(mvc.perform(get("/api/admin/llm/settings").cookie(cookie(admin))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("low",settings.path("reasoning").path("CHAT").asText()); assertEquals("high",settings.path("reasoning").path("TASK").asText());
    assertFalse(settings.path("reasoningOptionsFromModel").asBoolean()); assertEquals(3,settings.path("reasoningOptions").size(),"fallback when the model list is unavailable");
    var saved=json.readTree(mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON)
        .content("{\"reasoning\":{\"CHAT\":\"medium\",\"TASK\":\"medium\"},\"limits\":{\"chatPerHour\":5,\"tasksPerHour\":0}}")).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("medium",saved.path("reasoning").path("CHAT").asText()); assertEquals(5,saved.path("limits").path("chatPerHour").asInt()); assertEquals(0,saved.path("limits").path("tasksPerHour").asInt());
    assertEquals("medium",llmSettings.effort("TASK_REPAIR"),"repairs follow the task generation level");
    mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"reasoning\":{\"CHAT\":\"ultra\"},\"limits\":{\"chatPerHour\":7}}")).andExpect(status().isBadRequest());
    mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"limits\":{\"chatPerDay\":-1}}")).andExpect(status().isBadRequest());
    assertEquals(5,llmSettings.limit("chatPerHour"),"an invalid request changes nothing");
    when(tutor.availableModels()).thenReturn(List.of(new ModelOption("gpt-6-luna","Luna","",List.of("minimal","low","medium","high","xhigh"),"medium")));
    mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"reasoning\":{\"TASK\":\"xhigh\"}}")).andExpect(status().isOk());
    assertEquals("xhigh",llmSettings.effort("TASK"),"levels advertised by the model are accepted");
    mvc.perform(get("/api/admin/llm/settings").cookie(cookie(createStudentAndLogin("settings-nosy")))).andExpect(status().isBadRequest());
    db.update("delete from app_settings where key like 'llm_effort_%' or key like 'llm_limit_%'");
  }

  @Test void chatIsRateLimitedPerStudent() throws Exception {
    String token=createStudentAndLogin("chatty"); long student=studentId("chatty"); submitDiagnostic(token,student,false); start(token);
    when(tutor.reply(anyLong(),any(TutorContext.class),anyString())).thenReturn("Подумай о первой строке.");
    db.update("insert into app_settings(key,value) values('llm_limit_chatPerHour','2') on conflict(key) do update set value=excluded.value");
    try {
      var ok=json.readTree(mvc.perform(post("/api/chat").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"content\":\"Вопрос\"}")).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
      assertEquals(2,ok.path("quota").path("hourLimit").asInt());
      db.update("insert into llm_calls(user_id,purpose,language,status,duration_ms,created_at) values(?, 'CHAT','JAVA','OK',100,datetime('now','-50 minutes')),(?, 'CHAT','JAVA','OK',100,datetime('now','-10 minutes'))",student,student);
      int messagesBefore=db.queryForObject("select count(*) from chat_messages",Integer.class);
      var limited=mvc.perform(post("/api/chat").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"content\":\"Ещё вопрос\"}")).andExpect(status().isTooManyRequests()).andReturn().getResponse();
      var body=json.readTree(limited.getContentAsString());
      assertEquals("LLM_RATE_LIMITED",body.path("error").asText()); assertTrue(body.path("message").asText().contains("2 в час"));
      long retry=Long.parseLong(limited.getHeader("Retry-After"));
      assertTrue(retry>=9*60&&retry<=11*60,"the second-newest call leaves the hour window in ~10 minutes: "+retry);
      assertEquals(messagesBefore,db.queryForObject("select count(*) from chat_messages",Integer.class),"a rejected question is not stored");
      verify(tutor,times(1)).reply(anyLong(),any(TutorContext.class),anyString());
      var quota=json.readTree(mvc.perform(get("/api/chat").cookie(cookie(token))).andReturn().getResponse().getContentAsString()).path("quota");
      assertEquals(2,quota.path("hourUsed").asInt()); assertTrue(quota.path("retryAfterSeconds").asLong()>0);
      db.update("update app_settings set value='0' where key='llm_limit_chatPerHour'");
      mvc.perform(post("/api/chat").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"content\":\"Без лимита\"}")).andExpect(status().isOk());
    } finally { db.update("delete from app_settings where key like 'llm_limit_%'"); }
  }

  @Test void taskAndExplanationLimitsAreSeparateFromEachOtherAndFromChat() throws Exception {
    String token=createStudentAndLogin("gen-limited"); long student=studentId("gen-limited"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"THROWS_BASIC"); // a topic no other test creates tasks for
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),brief("THROWS_BASIC"))).thenReturn(Optional.empty());
    db.update("insert into app_settings(key,value) values('llm_limit_tasksPerHour','1'),('llm_limit_explanationsPerHour','1'),('llm_limit_chatPerHour','1') on conflict(key) do update set value=excluded.value");
    try {
      db.update("delete from llm_calls"); // other tests leave usage rows in the shared database
      // Heavy chat use and an explanation do not touch the task budget.
      db.update("insert into llm_calls(user_id,purpose,language,status,duration_ms) values(?, 'CHAT','JAVA','OK',100),(?, 'CHAT','JAVA','OK',100),(null,'EXPLANATION','JAVA','OK',100)",student,student);
      assertTrue(llmSettings.taskGenerationAllowed()); assertFalse(llmSettings.explanationGenerationAllowed()); assertFalse(llmSettings.chatQuota(student).allowed());
      start(token);
      json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
      verify(generator,never()).generateExplanation(anyLong(),any());
      verify(generator,atLeastOnce()).generateTask(eq(student),brief("THROWS_BASIC"));
      // A generated task (or a repair) uses the task budget; the next task is then refused.
      db.update("insert into llm_calls(user_id,purpose,language,status,duration_ms) values(null,'TASK_REPAIR','JAVA','OK',100)");
      assertFalse(llmSettings.taskGenerationAllowed());
      db.update("delete from lesson_tasks where lesson_id in (select id from lessons where user_id=?)",student);
      db.update("update tasks set active=0 where skill_code='THROWS_BASIC'");
      var limited=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
      assertEquals("LLM_RATE_LIMITED",limited.path("reason").asText());
    } finally { db.update("delete from app_settings where key like 'llm_limit_%'"); db.update("delete from llm_calls"); }
  }


  @Test void eachPurposeHasItsOwnModelAndLevel() throws Exception {
    String admin=login("admin","admin-pass");
    String put="{\"models\":%s,\"reasoning\":%s}";
    try {
      // App Server list unavailable: configured Terra and current models are offered; Terra gets the safe levels.
      var offline=json.readTree(mvc.perform(get("/api/admin/llm/settings").cookie(cookie(admin))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
      assertEquals("gpt-6-luna",offline.path("purposeModels").path("CHAT").asText()); assertEquals("gpt-6-luna",offline.path("purposeModels").path("TASK").asText());
      var terra=findModel(offline,"gpt-5.6-terra"); assertEquals("GPT-5.6-Terra",terra.path("displayName").asText()); assertFalse(terra.path("listed").asBoolean());
      mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(put.formatted("{\"TASK\":\"other-model\"}","{}"))).andExpect(status().isBadRequest());
      when(tutor.availableModels()).thenReturn(List.of(new ModelOption("gpt-6-luna","Luna","",List.of("low","medium","high"),"medium"),new ModelOption("gpt-5.6-terra","GPT-5.6-Terra","",List.of("low","medium","high","xhigh","max","ultra"),"medium")));
      // Different models for different work, each with a level its model supports.
      var saved=json.readTree(mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON)
          .content(put.formatted("{\"CHAT\":\"gpt-6-luna\",\"TASK\":\"gpt-5.6-terra\",\"EXPLANATION\":\"gpt-5.6-terra\"}","{\"CHAT\":\"low\",\"TASK\":\"ultra\",\"EXPLANATION\":\"medium\"}"))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
      assertEquals("gpt-5.6-terra",saved.path("purposeModels").path("TASK").asText()); assertEquals("ultra",saved.path("reasoning").path("TASK").asText());
      assertEquals("gpt-5.6-terra",llmSettings.model("TASK_REPAIR"),"repairs use the task model"); assertEquals("gpt-6-luna",llmSettings.model("CHAT"));
      // A level is checked against the model of its own purpose.
      mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(put.formatted("{}","{\"CHAT\":\"ultra\"}"))).andExpect(status().isBadRequest());
      mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(put.formatted("{\"TASK\":\"gpt-6-luna\"}","{}"))).andExpect(status().isBadRequest());
      assertEquals("gpt-5.6-terra",llmSettings.model("TASK"),"switching TASK to a model without its current level is refused as a whole");
      mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(put.formatted("{\"TASK\":\"gpt-6-luna\"}","{\"TASK\":\"high\"}"))).andExpect(status().isOk());
      assertEquals("gpt-6-luna",llmSettings.model("TASK"));
      // The single model saved before per-purpose models existed still applies until overridden.
      db.update("delete from app_settings where key like 'llm_model_%'"); db.update("insert into app_settings(key,value) values('llm_model','gpt-5.6-terra')");
      assertEquals("gpt-5.6-terra",llmSettings.model("EXPLANATION"));
    } finally { db.update("delete from app_settings where key like 'llm_%' and key<>'llm_enabled'"); }
  }

  @Test void llmOutputLoggingIsSwitchedSeparatelyForGenerationAndChat() throws Exception {
    String admin=login("admin","admin-pass");
    try {
      assertTrue(llmSettings.logOutput("TASK")); assertTrue(llmSettings.logOutput("TASK_REPAIR")); assertTrue(llmSettings.logOutput("EXPLANATION"));
      assertFalse(llmSettings.logOutput("CHAT"),"chat contains students' messages and code: off by default");
      var saved=json.readTree(mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"logging\":{\"generation\":false,\"chat\":true}}")).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
      assertFalse(saved.path("logging").path("generation").asBoolean()); assertTrue(saved.path("logging").path("chat").asBoolean());
      assertFalse(llmSettings.logOutput("TASK")); assertTrue(llmSettings.logOutput("CHAT"));
      mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"logging\":{\"everything\":true}}")).andExpect(status().isBadRequest());
    } finally { db.update("delete from app_settings where key like 'llm_log_%'"); }
  }


  private static ContentBrief brief(String skill){return argThat(b->b!=null&&skill.equals(b.skillCode()));}

  @Test void everyRequestLogLineNamesTheStudentItIsAbout() throws Exception {
    var appender=new ch.qos.logback.core.read.ListAppender<ch.qos.logback.classic.spi.ILoggingEvent>(); appender.start();
    var root=(ch.qos.logback.classic.Logger)org.slf4j.LoggerFactory.getLogger(org.slf4j.Logger.ROOT_LOGGER_NAME); root.addAppender(appender);
    try {
      String student=createStudentAndLogin("traced-student"); long id=studentId("traced-student"); String admin=login("admin","admin-pass");
      Map<String,String> created=lastHttp(appender,"POST /api/admin/students");
      assertEquals("admin=admin student=traced-student#"+id+" ",created.get("who"),"creating an account is attributed to the new student");
      mvc.perform(get("/api/progress").cookie(cookie(student))).andExpect(status().isOk());
      Map<String,String> own=lastHttp(appender,"GET /api/progress");
      assertEquals(String.valueOf(id),own.get("studentId")); assertEquals("student=traced-student#"+id+" ",own.get("who")); assertNull(own.get("admin"));
      long lesson=db.queryForObject("insert into lessons(user_id,lesson_number,language,language_lesson_number) values(?,1,'JAVA',1) returning id",Long.class,id);
      mvc.perform(post("/api/admin/students/"+id+"/lessons/"+lesson+"/finish").cookie(cookie(admin))).andExpect(status().isOk());
      var finished=appender.list.stream().filter(e->e.getFormattedMessage().startsWith("Lesson "+lesson+" of student")).reduce((a,b)->b).orElseThrow().getMDCPropertyMap();
      assertEquals("admin=admin student=traced-student#"+id+" ",finished.get("who"),"an admin action names the student it changes");
      mvc.perform(get("/api/admin/llm/settings").cookie(cookie(admin))).andExpect(status().isOk());
      Map<String,String> course=lastHttp(appender,"GET /api/admin/llm/settings");
      assertEquals("admin=admin ",course.get("who")); assertNull(course.get("studentId"),"course-wide admin work has no student");
      // The Codex reader thread logs with the context of the turn's student, then returns to its own (system) context.
      var context=new AtomicReference<Map<String,String>>();
      org.slf4j.MDC.clear(); LogContext.student(id,"traced-student"); var captured=LogContext.capture(); org.slf4j.MDC.clear();
      Thread.ofVirtual().start(()->{LogContext.with(captured,()->context.set(LogContext.capture())); assertNull(org.slf4j.MDC.get("who"));}).join();
      assertEquals("student=traced-student#"+id+" ",context.get().get("who"));
    } finally { root.detachAppender(appender); org.slf4j.MDC.clear(); }
  }
  private static Map<String,String> lastHttp(ch.qos.logback.core.read.ListAppender<ch.qos.logback.classic.spi.ILoggingEvent> appender,String request){
    return appender.list.stream().filter(e->"http".equals(e.getLoggerName())&&e.getFormattedMessage().startsWith(request+" ")).reduce((a,b)->b).orElseThrow(()->new AssertionError("no log line for "+request)).getMDCPropertyMap();
  }

  /** «Calculate» tasks: running decides whether the output is right, the LLM whether it was calculated, the syntax tree when the LLM cannot. */
  @Test void calculateTasksAreCheckedByRunningAndTheirApproachByTheLlm() throws Exception {
    String token=createStudentAndLogin("calculate-student"); long student=studentId("calculate-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"SET_BASIC");
    addTask("SET_BASIC","tickets task");
    db.update("update tasks set goal_json=? where title='tickets task'","{\"kind\":\"FIXED_ARITHMETIC\",\"operation\":\"*\",\"operands\":[5,6],\"expectedOutput\":\"30\\n\",\"functionName\":null,\"requiredConstructs\":[]}");
    start(token);
    long task=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()).path("task").path("id").asLong();
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    String ready="public class Solution { public static void main(String[] a) { System.out.println(30); } }";
    String calculated="public class Solution { public static void main(String[] a) { int bilet = 5 * 6; System.out.println(bilet); } }";
    // Right output, ready-made answer: the LLM rejects and says why.
    when(generator.checkCalculation(eq(student),argThat(r->r!=null&&ready.equals(r.source())))).thenReturn(new SolutionReview(false,"Ответ напечатан готовым.",
        List.of(new SolutionReview.Issue(1,"В println стоит готовое число 30.","Посчитай стоимость в программе."))));
    var rejected=attempt(token,task,ready);
    assertFalse(rejected.path("passed").asBoolean()); assertEquals("LLM",rejected.path("grader").asText());
    assertTrue(rejected.path("output").asText().contains("Строка 1: В println стоит готовое число 30."),rejected.toString());
    verify(generator).checkCalculation(eq(student),argThat(r->r!=null&&"*".equals(r.operation())&&"5, 6".equals(r.operands())));
    // A wrong output never reaches the LLM; the student sees the expected and the actual output side by side.
    when(runner.console(any(Language.class),eq("WRONG"))).thenReturn(new PistonCodeRunner.Console("OK","24\n",null,false));
    var wrong=attempt(token,task,"WRONG");
    assertFalse(wrong.path("passed").asBoolean()); assertEquals("30\n",wrong.path("mismatch").path("expected").asText()); assertEquals("24\n",wrong.path("mismatch").path("actual").asText());
    verify(generator,never()).checkCalculation(eq(student),argThat(r->r!=null&&"WRONG".equals(r.source())));
    // The LLM cannot answer: the syntax tree decides, with a clear message.
    when(generator.checkCalculation(eq(student),argThat(r->r!=null&&ready.equals(r.source())))).thenThrow(new LlmUnavailableException("timeout"));
    var byTree=attempt(token,task,ready);
    assertFalse(byTree.path("passed").asBoolean()); assertEquals("TESTS",byTree.path("grader").asText());
    assertTrue(byTree.path("output").asText().startsWith("Неверный подход: вычисли ответ"),byTree.toString());
    // Calculated through a variable: accepted.
    when(generator.checkCalculation(eq(student),argThat(r->r!=null&&calculated.equals(r.source())))).thenReturn(new SolutionReview(true,"Принято.",List.of()));
    assertTrue(attempt(token,task,calculated).path("passed").asBoolean());
    assertEquals(1,db.queryForObject("select count(*) from successful_task_credit where user_id=? and task_id=?",Integer.class,student,task));
  }

  @Test void theAssistantCanBeSwitchedOffForHardModeOnly() throws Exception {
    String admin=login("admin","admin-pass");
    String token=createStudentAndLogin("hard-no-chat"); long student=studentId("hard-no-chat"); submitDiagnostic(token,student,false); passedCourseOnceExcept(student,"SWITCH_BASIC");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    try {
      mvc.perform(put("/api/admin/llm/settings").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"hardModeChat\":false}")).andExpect(status().isOk());
      start(token);
      assertTrue(json.readTree(mvc.perform(get("/api/chat").cookie(cookie(token))).andReturn().getResponse().getContentAsString()).path("llm").path("available").asBoolean(),"not in hard mode: the assistant works");
      db.update("update users set hard_mode_allowed=1, hard_mode_on=1 where id=?",student);
      var chat=json.readTree(mvc.perform(get("/api/chat").cookie(cookie(token))).andReturn().getResponse().getContentAsString());
      assertEquals("DISABLED_IN_HARD_MODE",chat.path("llm").path("reason").asText());
      mvc.perform(post("/api/chat").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"content\":\"подскажи\"}")).andExpect(status().isServiceUnavailable());
      verify(tutor,never()).reply(eq(student),any(),anyString());
    } finally { db.update("delete from app_settings where key='hard_mode_chat'"); }
  }

  @Test void hardModeNeedsTheTeachersPermissionAndUsesItsOwnAlgorithmicTasks() throws Exception {
    String admin=login("admin","admin-pass");
    String token=createStudentAndLogin("hard-student"); long student=studentId("hard-student"); submitDiagnostic(token,student,false);
    mvc.perform(patch("/api/me/hard-mode").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"enabled\":true,\"language\":\"JAVA\"}")).andExpect(status().isBadRequest());
    mvc.perform(patch("/api/admin/students/{id}/hard-mode",student).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"allowed\":true}")).andExpect(status().isOk());
    // Allowed, but the course is not passed once yet: the mode stays closed and says how much is left.
    var notReady=json.readTree(mvc.perform(patch("/api/me/hard-mode").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"enabled\":true,\"language\":\"JAVA\"}"))
        .andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
    assertEquals("HARD_MODE_NOT_READY",notReady.path("error").asText()); assertTrue(notReady.path("message").asText().contains("Осталось тем: 44"),notReady.toString());
    var before=json.readTree(mvc.perform(get("/api/auth/me").cookie(cookie(token))).andReturn().getResponse().getContentAsString());
    assertFalse(before.path("user").path("hardModeCourses").path("JAVA").path("ready").asBoolean()); assertEquals(44,before.path("user").path("hardModeCourses").path("JAVA").path("remaining").asInt());
    passedCourseOnceExcept(student,"MAP_BASIC");
    mvc.perform(patch("/api/me/hard-mode").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"enabled\":true,\"language\":\"JAVA\"}")).andExpect(status().isOk());
    var me=json.readTree(mvc.perform(get("/api/auth/me").cookie(cookie(token))).andReturn().getResponse().getContentAsString());
    assertTrue(me.path("user").path("hardModeOn").asBoolean()); assertTrue(me.path("user").path("hardModeCourses").path("JAVA").path("ready").asBoolean());
    addTask("MAP_BASIC","regular map task"); // the regular pool is not used in hard mode
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),any())).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),argThat(b->b!=null&&b.hard()&&"MAP_BASIC".equals(b.skillCode())))).thenReturn(hardTask("MAP_BASIC"));
    when(runner.runRaw(any(Language.class),anyString(),anyString())).thenReturn(recordedProducts());
    // The platform's own trap — the first example's answer printed for any input — must fail the test cases.
    when(runner.run(any(Language.class),contains("println(\"20\")"),anyString())).thenReturn(new PistonCodeRunner.Run(false,"Неверный результат: Тест 2 из 6 не пройден"));
    start(token);
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    long hardTaskId=next.path("task").path("id").asLong();
    assertTrue(next.path("task").path("hard").asBoolean(),next.toString());
    assertEquals("HARD",db.queryForObject("select mode from tasks where id=?",String.class,hardTaskId));
    assertEquals(6,db.queryForObject("select count(*) from task_cases where task_id=?",Integer.class,hardTaskId),"answers recorded from the reference");
    assertEquals("20\n",db.queryForObject("select expected from task_cases where task_id=? and is_public=1",String.class,hardTaskId));
    attempt(token,hardTaskId,"import java.util.Scanner; public class Solution { public static void main(String[] a) { } }");
    var progress=json.readTree(mvc.perform(get("/api/progress").cookie(cookie(token))).andReturn().getResponse().getContentAsString());
    assertEquals(1,progress.path("hardSolved").asInt()); assertEquals(1,progress.path("solvedTasks").asInt());
    // Taking the permission away switches the mode off.
    mvc.perform(patch("/api/admin/students/{id}/hard-mode",student).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"allowed\":false}")).andExpect(status().isOk());
    assertEquals(0,db.queryForObject("select hard_mode_on from users where id=?",Integer.class,student));
    var list=json.readTree(mvc.perform(get("/api/admin/students").cookie(cookie(admin))).andReturn().getResponse().getContentAsString());
    for(var row:list.path("students")) if(row.path("id").asLong()==student) assertEquals(0,row.path("hardModeAllowed").asInt());
  }

  @Test void hardModeTasksComeFromTheExercismBankBeforeAnyGeneration() throws Exception {
    assertEquals(51,db.queryForObject("select count(*) from tasks where source='EXERCISM' and mode='HARD' and active=1",Integer.class),"every bank task found its topic");
    assertEquals(0,db.queryForObject("select count(*) from tasks t where t.source='EXERCISM' and (select count(*) from task_cases c where c.task_id=t.id)<6",Integer.class));
    assertEquals(0,db.queryForObject("select count(*) from tasks t where t.source='EXERCISM' and not exists(select 1 from task_cases c where c.task_id=t.id and c.is_public=1)",Integer.class));
    String token=createStudentAndLogin("bank-student"); long student=studentId("bank-student"); submitDiagnostic(token,student,false); passedCourseOnceExcept(student,"WHILE_LOOP_BASIC");
    db.update("update users set hard_mode_allowed=1, hard_mode_on=1 where id=?",student);
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),any())).thenReturn(Optional.empty());
    start(token);
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(next.path("task").path("hard").asBoolean());
    assertEquals("Квадратный корень без функций",next.path("task").path("title").asText(),"a repetition starts at step 2: the step-2 bank task of the topic");
    assertTrue(next.path("task").path("starterCode").asText().contains("Scanner in = new Scanner(System.in)"));
    assertTrue(next.path("task").path("statement").asText().contains("Exercism"),"the source is credited");
    verify(generator,never()).generateTask(eq(student),any());
    // Loading the bank again updates the same tasks instead of adding new ones.
    hardTaskBank.run(null);
    assertEquals(51,db.queryForObject("select count(*) from tasks where source='EXERCISM'",Integer.class));
  }

  @Test void switchingHardModeReplacesTheCurrentTaskOfTheOtherMode() throws Exception {
    String token=createStudentAndLogin("hard-switch-student"); long student=studentId("hard-switch-student"); submitDiagnostic(token,student,false); passedCourseOnceExcept(student,"WHILE_LOOP_BASIC");
    db.update("update users set hard_mode_allowed=1, hard_mode_on=0 where id=?",student);
    addTask("WHILE_LOOP_BASIC","regular while switch 1"); addTask("WHILE_LOOP_BASIC","regular while switch 2");
    db.update("update tasks set difficulty=2 where title like 'regular while switch %'"); // the step a repetition starts at, so nothing is generated
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),any())).thenReturn(Optional.empty());
    start(token);
    var regular=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    long regularTaskId=regular.path("task").path("id").asLong();
    assertFalse(regular.path("task").path("hard").asBoolean()); assertEquals("regular while switch 1",regular.path("task").path("title").asText(),regular.toString());
    var on=json.readTree(mvc.perform(patch("/api/me/hard-mode").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"enabled\":true,\"language\":\"JAVA\"}")).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(on.path("replacedTask").asBoolean(),on.toString());
    long lessonId=db.queryForObject("select id from lessons where user_id=? and finished_at is null",Long.class,student);
    assertNotNull(db.queryForObject("select replaced_at from lesson_tasks where lesson_id=? and task_id=?",String.class,lessonId,regularTaskId));
    var hard=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    long hardTaskId=hard.path("task").path("id").asLong();
    assertTrue(hard.path("task").path("hard").asBoolean(),hard.toString());
    // A stale page cannot submit the replaced task.
    var stale=json.readTree(mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",regularTaskId,"sourceCode","public class Solution {}"))))
        .andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
    assertEquals("TASK_NOT_IN_LESSON",stale.path("error").asText());
    var off=json.readTree(mvc.perform(patch("/api/me/hard-mode").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content("{\"enabled\":false,\"language\":\"JAVA\"}")).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(off.path("replacedTask").asBoolean(),off.toString());
    var back=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertFalse(back.path("task").path("hard").asBoolean(),back.toString()); assertEquals("regular while switch 2",back.path("task").path("title").asText());
    // The teacher sees both replaced tasks in the lesson history.
    var detail=json.readTree(mvc.perform(get("/api/admin/students/{id}/lessons/{l}",student,lessonId).cookie(cookie(login("admin","admin-pass")))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(findTask(detail,regularTaskId).path("replaced").asBoolean()); assertTrue(findTask(detail,hardTaskId).path("replaced").asBoolean());
    assertFalse(findTask(detail,back.path("task").path("id").asLong()).path("replaced").asBoolean());
  }

  @Test void functionTasksAreNotGivenBeforeMethodsAreTaught() throws Exception {
    String token=createStudentAndLogin("no-methods-yet"); long student=studentId("no-methods-yet"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"LOGICAL_AND");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),any())).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("LOGICAL_AND"))).thenReturn(generated("LOGICAL_AND",true));
    start(token);
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("LLM_GENERATION_FAILED_VALIDATION",next.path("reason").asText());
    assertEquals(0,db.queryForObject("select count(*) from tasks where title='generated LOGICAL_AND'",Integer.class),"a function task on «Логическое И» comes before the methods topic");
  }

  @Test void storedTasksNeedingMethodsBeforeTheirTopicAreRetired() {
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,source,mode) values('VARIABLE_BASIC','early method','s','public class Solution {\n    static int total(int a, int b) {\n        // Напиши решение здесь\n    }\n}','','TestHarness.java','JAVA','LLM','NORMAL')");
    long early=db.queryForObject("select last_insert_rowid()",Long.class);
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,source,mode,goal_json) values('PY_VARIABLE_BASIC','early function goal','s','# Напиши решение здесь\n','','test_solution.py','PYTHON','LLM','NORMAL','{\"kind\":\"FUNCTION_BEHAVIOR\",\"requiredConstructs\":[]}')");
    long earlyGoal=db.queryForObject("select last_insert_rowid()",Long.class);
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,source,mode) values('METHOD_PARAMETERS','method on time','s','public class Solution {\n    static int total(int a, int b) {\n        return 0;\n    }\n}','','TestHarness.java','JAVA','LLM','NORMAL')");
    long onTime=db.queryForObject("select last_insert_rowid()",Long.class);
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,source,mode) values('VARIABLE_BASIC','main only','s','public class Solution {\n    public static void main(String[] args) {\n        int x = 1;\n    }\n}','','TestHarness.java','JAVA','LLM','NORMAL')");
    long mainOnly=db.queryForObject("select last_insert_rowid()",Long.class);
    assertEquals(2,taskAudit.retireBeyondTopic());
    assertEquals(0,db.queryForObject("select active from tasks where id=?",Integer.class,early));
    assertEquals(0,db.queryForObject("select active from tasks where id=?",Integer.class,earlyGoal));
    assertEquals(1,db.queryForObject("select active from tasks where id=?",Integer.class,onTime));
    assertEquals(1,db.queryForObject("select active from tasks where id=?",Integer.class,mainOnly));
  }

  @Test void regularTasksNeverReadInput() throws Exception {
    String token=createStudentAndLogin("no-input-student"); long student=studentId("no-input-student"); submitDiagnostic(token,student,false); prepareOnlySkill(student,"LIST_OPERATIONS");
    when(tutor.status(student)).thenReturn(new LlmStatus(true,true,true,"READY","gpt-6-luna"));
    when(generator.generateExplanation(eq(student),any())).thenReturn(Optional.empty());
    when(generator.generateTask(eq(student),brief("LIST_OPERATIONS"))).thenReturn(hardTask("LIST_OPERATIONS"));
    start(token);
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals("LLM_GENERATION_FAILED_VALIDATION",next.path("reason").asText());
    assertEquals(0,db.queryForObject("select count(*) from tasks where title='hard LIST_OPERATIONS'",Integer.class));
  }

  private com.fasterxml.jackson.databind.JsonNode attempt(String token,long task,String source) throws Exception {
    return json.readTree(mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",task,"sourceCode",source))))
        .andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
  }
  /** A hard-mode task: reads two numbers, prints their product; the platform records the answers from the reference. */
  private GeneratedTask hardTask(String skill) throws Exception {
    var goal=json.readTree("{\"kind\":\"IO_BEHAVIOR\",\"operation\":null,\"operands\":[],\"expectedOutput\":null,\"functionName\":null,\"requiredConstructs\":[]}");
    var inputs=List.of(new TestCases.Input("4 5\n",true),new TestCases.Input("2 3\n",false),new TestCases.Input("0 9\n",false),new TestCases.Input("7 7\n",false),new TestCases.Input("10 1\n",false),new TestCases.Input("3 3\n",false));
    return new GeneratedTask(skill,"hard "+skill,"Перемножь два числа.","import java.util.Scanner;\npublic class Solution { public static void main(String[] args) { Scanner in = new Scanner(System.in); int a = in.nextInt(); int b = in.nextInt(); } }",
        "","TestHarness.java","import java.util.Scanner; public class Solution { public static void main(String[] args) { Scanner in = new Scanner(System.in); System.out.println(in.nextInt() * in.nextInt()); } }",List.of(skill),List.of(),goal,
        List.of(new TaskGoal.Mutant("adds instead of multiplying","public class Solution { public static void main(String[] args) { } } // WRONG"),new TaskGoal.Mutant("ignores the second number","public class Solution { public static void main(String[] args) { } } // WRONG 2")),inputs);
  }
  /** What the reference prints for hardTask's inputs, as the platform's recorder reports it. */
  private static PistonCodeRunner.Raw recordedProducts() {
    StringBuilder out=new StringBuilder(); String[] answers={"20\n","6\n","0\n","49\n","10\n","9\n"};
    for(int i=0;i<answers.length;i++) out.append("__CASE__").append(i).append(':').append(java.util.Base64.getEncoder().encodeToString(answers[i].getBytes(java.nio.charset.StandardCharsets.UTF_8))).append('\n');
    return new PistonCodeRunner.Raw(true,out.toString(),"");
  }

  private String createStudentAndLogin(String login) throws Exception { String admin=login("admin","admin-pass"); mvc.perform(post("/api/admin/students").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login",login,"password","student-pass","displayName",login)))).andExpect(status().isOk()); return login(login,"student-pass"); }
  private String login(String login,String password) throws Exception { var r=mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login",login,"password",password)))).andExpect(status().isOk()).andReturn().getResponse(); return r.getCookie("adaptive_session").getValue(); }
  private long studentId(String login){return db.queryForObject("select id from users where login=?",Long.class,login);}
  private void submitDiagnostic(String token,long user,boolean correctBlockZero) throws Exception { var rows=db.queryForList("select id,correct_option,block_no from diagnostic_questions where language='JAVA' order by id"); var answers=new ArrayList<Map<String,Object>>();for(var q:rows){boolean correct=correctBlockZero&&((Number)q.get("block_no")).intValue()==0;var answer=new LinkedHashMap<String,Object>();answer.put("questionId",q.get("id"));if(correct)answer.put("selectedOption",q.get("correct_option"));answers.add(answer);}mvc.perform(post("/api/diagnostic").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("answers",answers)))).andExpect(status().isOk());}
  private int start(String token) throws Exception { return json.readTree(mvc.perform(post("/api/lessons/start").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()).path("lesson").path("number").asInt(); }
  private void finish(String token,int lesson) throws Exception { long id=db.queryForObject("select id from lessons where user_id=(select user_id from sessions where token_hash=?) and lesson_number=?",Long.class,Hashing.sha256(token),lesson);mvc.perform(post("/api/lessons/{id}/finish",id).cookie(cookie(token))).andExpect(status().isOk()); }
  private void solveThree(String token) throws Exception { solve(token,3); }
  private void solve(String token,int tasks) throws Exception { for(int i=0;i<tasks;i++){var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());long task=next.path("task").path("id").asLong();assertTrue(task>0);mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId",task,"sourceCode","public class Solution {}")))).andExpect(status().isOk());} }
  private void assertProgress(long user,int iterations,int mastered,int current){var row=db.queryForMap("select completed_iterations,mastered,iteration_successes from student_skills where user_id=? and skill_code='BASIC_CODE_READING'",user);assertEquals(iterations,((Number)row.get("completed_iterations")).intValue());assertEquals(mastered,((Number)row.get("mastered")).intValue());assertEquals(current,((Number)row.get("iteration_successes")).intValue());}
  private void addTask(String title){addTask("BASIC_CODE_READING", title);}
  private void addTask(String skillCode,String title){db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name) values(?,?,?, '', 'class TestHarness {}','TestHarness.java')",skillCode,title,title);long id=db.queryForObject("select last_insert_rowid()",Long.class);db.update("insert into task_target_skills(task_id,skill_code) values(?, ?)",id,skillCode);}
  private jakarta.servlet.http.Cookie cookie(String value){return new jakarta.servlet.http.Cookie("adaptive_session",value);}
  private int countLessonTasks(long student){return db.queryForObject("select count(*) from lesson_tasks where lesson_id=(select id from lessons where user_id=? and finished_at is null)",Integer.class,student);}
  /** The course passed once: every other topic mastered, this one with its first iteration done in lesson 0 (so it is due in lesson 1). */
  private void passedCourseOnceExcept(long student,String skill){prepareOnlySkill(student,skill);db.update("insert into student_skills(user_id,skill_code,completed_iterations,first_iteration_lesson_number,mastered) values(?,?,1,0,0)",student,skill);}
  private void prepareOnlySkill(long student,String skill){db.update("insert into student_skills(user_id,skill_code,completed_iterations,mastered) select ?,code,3,1 from skills where code<>?",student,skill);}
  /** A function task; invalid — without the test inputs the platform needs. */
  private GeneratedTask generated(String skill,boolean valid){return new GeneratedTask(skill,"generated "+skill,"statement","","","TestHarness.java","public class Solution { static int answer(int x) { return x; } }",List.of(skill),List.of(),functionGoal(),wrongSolutions(),valid?functionInputs():List.of());}
  private static List<TestCases.Input> functionInputs(){return List.of(new TestCases.Input("1",true),new TestCases.Input("2",false),new TestCases.Input("3",false),new TestCases.Input("0",false),new TestCases.Input("-4",false),new TestCases.Input("10",false));}
  /** The recorder's report for n cases with distinct answers. */
  static PistonCodeRunner.Raw recordedAnswers(int n){StringBuilder out=new StringBuilder();for(int i=0;i<n;i++)out.append("__CASE__").append(i).append(':').append(java.util.Base64.getEncoder().encodeToString(String.valueOf(i*7+1).getBytes(java.nio.charset.StandardCharsets.UTF_8))).append('\n');return new PistonCodeRunner.Raw(true,out.toString(),"");}
  private com.fasterxml.jackson.databind.JsonNode functionGoal(){try{return json.readTree("{\"kind\":\"FUNCTION_BEHAVIOR\",\"operation\":null,\"operands\":[],\"expectedOutput\":null,\"functionName\":\"answer\",\"requiredConstructs\":[]}");}catch(Exception e){throw new IllegalStateException(e);}}
  private static List<TaskGoal.Mutant> wrongSolutions(){return List.of(new TaskGoal.Mutant("hard-codes the first example","public class Solution { static int answer(int x) { return 1; } } // WRONG"),new TaskGoal.Mutant("off by one","public class Solution { static int answer(int x) { return x + 1; } } // WRONG"));}
  private static com.fasterxml.jackson.databind.JsonNode findSkill(com.fasterxml.jackson.databind.JsonNode progress,String code){for(var skill:progress.path("skills"))if(code.equals(skill.path("skillCode").asText()))return skill;throw new AssertionError(code);}
}
