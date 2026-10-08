package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.support.TransactionSynchronizationManager;

import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Runs on a real SQLite file (not the shared in-memory database of the other tests) so locking behaves like
 * production. Long external work — LLM turns and Piston runs — must happen outside any database transaction,
 * otherwise every other writer (logins, chat, other students' submissions, LLM statistics) fails with SQLITE_BUSY.
 */
@SpringBootTest
@AutoConfigureMockMvc
class TransactionBoundariesTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json;
  @MockBean PistonCodeRunner runner;
  @MockBean LlmTutor tutor;
  @MockBean LearningContentGenerator generator;

  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) throws Exception {
    Path file = Files.createTempDirectory("tx-boundaries").resolve("tutor.db");
    p.add("spring.datasource.url", () -> "jdbc:sqlite:" + file);
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
    p.add("app.task-audit.enabled", () -> "false");
  }

  @BeforeEach void prepare() {
    db.update("update users set password_hash=? where login='admin'", new BCryptPasswordEncoder().encode("admin-pass"));
    when(runner.configured()).thenReturn(true);
    when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true, "READY", "17"));
    when(runner.runRaw(any(Language.class), anyString(), anyString())).thenReturn(LearningFlowIntegrationTest.recordedAnswers(6));
    when(runner.run(any(Language.class), anyString(), anyString())).thenAnswer(call -> ((String) call.getArgument(1)).contains("WRONG")
        ? new PistonCodeRunner.Run(false, "Неверный вывод программы.") : new PistonCodeRunner.Run(true, "Решение прошло скрытые проверки"));
    when(tutor.status(anyLong())).thenReturn(new LlmStatus(true, true, true, "READY", "gpt-6-luna"));
    when(generator.generateExplanation(anyLong(), any())).thenReturn(Optional.empty());
  }

  @Test void sqliteRunsInWalModeWithBusyTimeoutAndForeignKeys() {
    assertEquals("wal", db.queryForObject("PRAGMA journal_mode", String.class));
    assertTrue(db.queryForObject("PRAGMA busy_timeout", Integer.class) >= 10_000);
    assertEquals(1, db.queryForObject("PRAGMA foreign_keys", Integer.class));
  }

  /** The reported failure: a 40-second generation inside @Transactional locked out every other writer. */
  @Test void otherWritersAreNotBlockedWhileATaskIsGenerated() throws Exception {
    String token = studentInLesson("gen-writer");
    long student = studentId("gen-writer");
    db.update("update tasks set active=0 where skill_code='BASIC_CODE_READING'"); // force generation
    AtomicReference<Throwable> concurrentWrite = new AtomicReference<>();
    AtomicReference<Boolean> transactionDuringLlm = new AtomicReference<>();
    when(generator.generateTask(eq(student), any())).thenAnswer(call -> {
      transactionDuringLlm.set(TransactionSynchronizationManager.isActualTransactionActive());
      concurrentWrite.set(writeFromAnotherConnection());
      return functionTask(((ContentBrief) call.getArgument(1)).skillCode());
    });
    var next = json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(next.path("task").path("id").asLong() > 0, next.toString());
    assertEquals(Boolean.FALSE, transactionDuringLlm.get(), "the LLM call must not run inside a database transaction");
    assertNull(concurrentWrite.get(), () -> "a concurrent write failed during generation: " + concurrentWrite.get());
  }

  @Test void otherWritersAreNotBlockedWhileASolutionRuns() throws Exception {
    String token = studentInLesson("run-writer");
    long task = json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andReturn().getResponse().getContentAsString()).path("task").path("id").asLong();
    AtomicReference<Throwable> concurrentWrite = new AtomicReference<>();
    AtomicReference<Boolean> transactionDuringRun = new AtomicReference<>();
    when(runner.run(any(Language.class), eq("public class Solution {}"), anyString())).thenAnswer(call -> {
      transactionDuringRun.set(TransactionSynchronizationManager.isActualTransactionActive());
      concurrentWrite.set(writeFromAnotherConnection());
      return new PistonCodeRunner.Run(true, "Решение прошло скрытые проверки");
    });
    var attempt = json.readTree(mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON)
        .content(json.writeValueAsString(Map.of("taskId", task, "sourceCode", "public class Solution {}")))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertTrue(attempt.path("passed").asBoolean());
    assertEquals(Boolean.FALSE, transactionDuringRun.get(), "the Piston run must not happen inside a database transaction");
    assertNull(concurrentWrite.get(), () -> "a concurrent write failed during the run: " + concurrentWrite.get());
    long student = studentId("run-writer");
    assertEquals(1, db.queryForObject("select count(*) from successful_task_credit where user_id=? and task_id=?", Integer.class, student, task));
    assertEquals(1, db.queryForObject("select iteration_successes from student_skills where user_id=? and skill_code='BASIC_CODE_READING'", Integer.class, student));
  }

  /** Without one long transaction, two requests for the same lesson (double click, React StrictMode) must still yield one task. */
  @Test void parallelNextRequestsGenerateAndAssignOnlyOneTask() throws Exception {
    String token = studentInLesson("parallel");
    long student = studentId("parallel");
    db.update("update tasks set active=0 where skill_code='BASIC_CODE_READING'"); // force generation
    AtomicInteger generations = new AtomicInteger();
    when(generator.generateTask(eq(student), any())).thenAnswer(call -> {
      generations.incrementAndGet();
      Thread.sleep(300);
      return functionTask(((ContentBrief) call.getArgument(1)).skillCode());
    });
    ExecutorService pool = Executors.newFixedThreadPool(2);
    try {
      Callable<Long> request = () -> json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()).path("task").path("id").asLong();
      var a = pool.submit(request); var b = pool.submit(request);
      assertEquals(a.get(30, TimeUnit.SECONDS), b.get(30, TimeUnit.SECONDS), "both requests see the same task");
    } finally { pool.shutdownNow(); }
    assertEquals(1, generations.get(), "the second request waits for the first instead of generating again");
    assertEquals(1, db.queryForObject("select count(*) from lesson_tasks where lesson_id=(select id from lessons where user_id=? and finished_at is null)", Integer.class, student));
  }

  /** Logging out (or «Завершить урок») must not wait for a generation in progress, and the generated task must not be lost. */
  @Test void logoutDuringGenerationIsImmediateAndKeepsTheTask() throws Exception {
    String token = studentInLesson("logout-generating");
    long student = studentId("logout-generating");
    db.update("update tasks set active=0 where skill_code='BASIC_CODE_READING'"); // force generation
    CountDownLatch generating = new CountDownLatch(1), release = new CountDownLatch(1);
    AtomicReference<String> title = new AtomicReference<>();
    when(generator.generateTask(eq(student), any())).thenAnswer(call -> {
      generating.countDown();
      assertTrue(release.await(30, TimeUnit.SECONDS));
      GeneratedTask task = functionTask(((ContentBrief) call.getArgument(1)).skillCode()); title.set(task.title()); return task;
    });
    ExecutorService pool = Executors.newFixedThreadPool(2);
    try {
      var next = pool.submit(() -> json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString()));
      assertTrue(generating.await(30, TimeUnit.SECONDS));
      // The model is still writing the task: logout answers at once and ends the lesson.
      pool.submit(() -> mvc.perform(post("/api/auth/logout").cookie(cookie(token))).andExpect(status().isNoContent())).get(5, TimeUnit.SECONDS);
      assertEquals(0, db.queryForObject("select count(*) from lessons where user_id=? and finished_at is null", Integer.class, student));
      release.countDown();
      assertEquals("LESSON_FINISHED", next.get(30, TimeUnit.SECONDS).path("reason").asText());
    } finally { pool.shutdownNow(); }
    long kept = db.queryForObject("select id from tasks where title=?", Long.class, title.get());
    String again = login("logout-generating", "student-pass");
    mvc.perform(post("/api/lessons/start").cookie(cookie(again))).andExpect(status().isOk());
    var next = json.readTree(mvc.perform(get("/api/learning/next").cookie(cookie(again))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
    assertEquals(kept, next.path("task").path("id").asLong(), "the next lesson starts with the task generated during the logout");
    verify(generator, times(1)).generateTask(eq(student), any());
  }

  /** A write from a different thread (so a different pooled connection) while the request is mid-flight. */
  private Throwable writeFromAnotherConnection() {
    try {
      CompletableFuture.runAsync(() -> db.update("insert into sessions(token_hash,user_id,expires_at) values(?,?,?)",
          UUID.randomUUID().toString(), 1, Instant.now().plusSeconds(60).toString())).get(30, TimeUnit.SECONDS);
      return null;
    } catch (ExecutionException e) { return e.getCause(); }
    catch (Exception e) { return e; }
  }

  private GeneratedTask functionTask(String skill) throws Exception {
    var goal = json.readTree("{\"kind\":\"FUNCTION_BEHAVIOR\",\"operation\":null,\"operands\":[],\"expectedOutput\":null,\"functionName\":\"answer\",\"requiredConstructs\":[]}");
    var inputs = List.of(new TestCases.Input("1", true), new TestCases.Input("2", false), new TestCases.Input("3", false), new TestCases.Input("0", false), new TestCases.Input("-4", false), new TestCases.Input("10", false));
    return new GeneratedTask(skill, "generated " + skill + " " + UUID.randomUUID(), "statement", "", "", "TestHarness.java", "public class Solution { static int answer(int x) { return x; } }",
        List.of(skill), List.of(), goal, List.of(new TaskGoal.Mutant("constant", "class Solution { static int answer(int x) { return 1; } } // WRONG"), new TaskGoal.Mutant("off by one", "class Solution { static int answer(int x) { return x + 1; } } // WRONG")), inputs);
  }

  private String studentInLesson(String login) throws Exception {
    String admin = login("admin", "admin-pass");
    mvc.perform(post("/api/admin/students").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login", login, "password", "student-pass", "displayName", login)))).andExpect(status().isOk());
    String token = login(login, "student-pass");
    var answers = new ArrayList<Map<String, Object>>();
    for (var id : db.queryForList("select id from diagnostic_questions where language='JAVA' order by id", Long.class)) answers.add(Map.of("questionId", id));
    mvc.perform(post("/api/diagnostic").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("answers", answers)))).andExpect(status().isOk());
    mvc.perform(post("/api/lessons/start").cookie(cookie(token))).andExpect(status().isOk());
    return token;
  }
  private String login(String login, String password) throws Exception {
    return mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login", login, "password", password)))).andExpect(status().isOk()).andReturn().getResponse().getCookie("adaptive_session").getValue();
  }
  private long studentId(String login) { return db.queryForObject("select id from users where login=?", Long.class, login); }
  private static jakarta.servlet.http.Cookie cookie(String value) { return new jakarta.servlet.http.Cookie("adaptive_session", value); }
}
