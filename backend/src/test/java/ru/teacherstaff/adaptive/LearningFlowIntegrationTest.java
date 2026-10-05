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
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json;
  @MockBean PistonCodeRunner runner;
  @MockBean LlmTutor tutor;
  @MockBean LearningContentGenerator generator;
  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:flow-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
  }
  @BeforeEach void prepare() { db.update("update users set password_hash=? where login='admin'",new BCryptPasswordEncoder().encode("admin-pass")); when(runner.configured()).thenReturn(true); when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true,"READY","17.0.1")); when(runner.run(any(Language.class),anyString(),anyString())).thenReturn(new PistonCodeRunner.Run(true,"Решение прошло скрытые проверки")); when(tutor.status(anyLong())).thenReturn(new LlmStatus(false,false,false,"DISABLED", "gpt-6-luna")); }

  @Test void diagnosticDeterminesFirstAvailableBlock() throws Exception {
    String cookie=createStudentAndLogin("block-student"); long student=studentId("block-student");
    submitDiagnostic(cookie, student, true);
    addTask("PRIMITIVE_TYPES", "block 1 task");
    var response=json.readTree(mvc.perform(post("/api/lessons/start").cookie(cookie(cookie))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(response.path("lesson").path("id").asLong()>0);
    var next=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(cookie))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(1,next.path("skill").path("blockNo").asInt());
    long assigned=next.path("task").path("id").asLong();
    var restored=json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(cookie))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(assigned,restored.path("task").path("id").asLong());
    assertEquals(1,countLessonTasks(student));
    verifyNoInteractions(generator);
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
    verify(generator,times(2)).generateTask(eq(student),brief("FOR_LOOP_BASIC"));
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
  private GeneratedTask generated(String skill,boolean valid){String test="public class TestHarness { public static void main(String[] a) { System.out.print(\""+(valid?PistonCodeRunner.PASS_MARKER_PLACEHOLDER:"missing")+"\"); } }";return new GeneratedTask(skill,"generated "+skill,"statement","",test,"TestHarness.java","public class Solution {}",List.of(skill),List.of());}
}
