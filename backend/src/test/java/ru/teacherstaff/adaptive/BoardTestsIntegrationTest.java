package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
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
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import java.nio.file.Path;
import java.time.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * «К доске» end to end: the choice of the two items, the call (only the called student, expiry, cancel, recall, extend),
 * the timer (autosave window, the server's finish with the last autosave), the checks (nothing credited), the rule
 * grade, the pace cap, the LLM assessment (stored, unavailable), the teacher's grade, what the student may see, the
 * rotation suggestion, the journal and admin-only access. The LLM and Piston are stubbed; the clock is the test's.
 * Every test uses topics and students of its own.
 */
@SpringBootTest
@AutoConfigureMockMvc
class BoardTestsIntegrationTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json; @Autowired BoardTests board;
  @MockBean PistonCodeRunner runner;
  @MockBean LlmTutor tutor;
  @MockBean LearningContentGenerator generator;
  @MockBean Clock clock;
  static final Instant START = Instant.parse("2041-03-01T10:00:00Z");
  volatile Instant now = START;
  int order = 0;

  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:board-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
    p.add("app.task-audit.enabled", () -> "false");
    p.add("app.lesson.idle-close.enabled", () -> "false");
    p.add("app.board.auto-finish.enabled", () -> "false"); // the tests drive finishing through requests
  }
  @BeforeEach void prepare() {
    db.update("update users set password_hash=? where login='admin'", new BCryptPasswordEncoder().encode("admin-pass"));
    db.update("delete from app_settings where key='session_date'");
    now = START;
    when(clock.instant()).thenAnswer(i -> now);
    when(clock.getZone()).thenReturn(ZoneOffset.UTC);
    when(runner.configured()).thenReturn(true);
    when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true, "READY", "17.0.1"));
    when(runner.run(any(Language.class), anyString(), anyString())).thenAnswer(call -> ((String) call.getArgument(1)).contains("RIGHT")
        ? new PistonCodeRunner.Run(true, "Решение прошло скрытые проверки", PistonCodeRunner.Outcome.PASSED)
        : new PistonCodeRunner.Run(false, "Неверный вывод программы", PistonCodeRunner.Outcome.CHECK_FAILED));
    when(runner.console(any(Language.class), anyString())).thenReturn(new PistonCodeRunner.Console("OK", "printed\n", null, false));
    when(runner.console(any(Language.class), anyString(), anyString())).thenReturn(new PistonCodeRunner.Console("OK", "printed\n", null, false));
    when(tutor.status(anyLong())).thenReturn(new LlmStatus(false, false, false, "DISABLED", "gpt-6-luna"));
    when(generator.available()).thenReturn(false);
    board.runBackgroundWorkWith(Runnable::run);
  }

  // ---------------------------------------------------------------- items

  @Test void theCodeItemComesFromTheRecentPracticeTopicAndTheOutputItemFromAnOlderOne() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("it-a", "Ирина", "B-1"); long a = studentId("it-a");
    String recent = skill("BT_IT_RECENT", 2), older = skill("BT_IT_OLDER", 2), middle = skill("BT_IT_MIDDLE", 2);
    passed(a, older, START.minus(Duration.ofDays(40)));
    passed(a, middle, START.minus(Duration.ofDays(20)));
    passed(a, recent, START.minus(Duration.ofDays(3)));
    // The recent topic: a solved story, an unsolved one (two variants), another difficulty, another source, an input task, a hard task.
    long solved = codeTask(recent, 2, "CURATED", "curated:it-solved:1"); codeTask(recent, 2, "CURATED", "curated:it-solved:2"); credit(a, solved);
    long wanted1 = codeTask(recent, 2, "CURATED", "curated:it-fresh:1"), wanted2 = codeTask(recent, 2, "CURATED", "curated:it-fresh:2");
    codeTask(recent, 3, "CURATED", "curated:it-harder:1"); codeTask(recent, 2, "LLM", null);
    long io = codeTask(recent, 2, "CURATED", "curated:it-io:1"); db.update("update tasks set goal_json='{\"kind\":\"IO_BEHAVIOR\"}' where id=?", io);
    long hard = codeTask(recent, 2, "CURATED", "curated:it-hard:1"); db.update("update tasks set mode='HARD' where id=?", hard);
    // Output tasks: the older topics (one story solved), and the recent topic, which must not be used.
    long outSolved = outputTask(older, "curated:it-out-solved:1", "print(1)\n", "1\n"); credit(a, outSolved);
    long outOld = outputTask(older, "curated:it-out-old:1", "print('old')\n", "old\n");
    long outMiddle = outputTask(middle, "curated:it-out-mid:1", "print('mid')\n", "mid\n");
    outputTask(recent, "curated:it-out-recent:1", "print('recent')\n", "recent\n");
    outputTask(older, "curated:it-out-noref:1", null, "x\n");

    for (int i = 0; i < 6; i++) {
      var test = startTest(admin, token, a);
      var code = test.path("items").get(0); var output = test.path("items").get(1);
      long codeTask = adminTest(admin, test.path("id").asLong()).path("items").get(0).path("taskId").asLong();
      assertTrue(Set.of(wanted1, wanted2).contains(codeTask), "an unsolved curated story of the recent topic at difficulty 2, got " + codeTask);
      assertEquals("code", code.path("kind").asText()); assertEquals("JAVA", code.path("language").asText());
      assertEquals("starter " + codeTask, code.path("starterCode").asText()); assertEquals("starter " + codeTask, test.path("answers").path("code").asText());
      long outputTask = adminTest(admin, test.path("id").asLong()).path("items").get(1).path("taskId").asLong();
      assertTrue(Set.of(outOld, outMiddle).contains(outputTask), "an unsolved story of a topic passed more than 14 days ago, got " + outputTask);
      assertEquals(outputTask == outOld ? "print('old')\n" : "print('mid')\n", output.path("program").asText(), "the full reference program");
      finishNow(admin, test.path("id").asLong());
    }
    assertEquals(0, count("select count(*) from submissions where task_id in (?,?)", wanted1, wanted2), "a board test makes no submissions");
  }

  @Test void laterTopicsUseDifficultyOneAndTheOutputItemFallsBackToOtherTopics() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("df-a", "Дарья", "B-2"); long a = studentId("df-a");
    String late = skill("BT_DF_LATE", 5), other = skill("BT_DF_OTHER", 2), confirmed = skill("BT_DF_CONF", 1);
    passed(a, other, START.minus(Duration.ofDays(5)));
    passed(a, late, START.minus(Duration.ofDays(1)));
    confirm(a, confirmed);
    codeTask(late, 2, "CURATED", "curated:df-two:1"); long one = codeTask(late, 1, "CURATED", "curated:df-one:1"); codeTask(late, 3, "CURATED", "curated:df-three:1");
    long out = outputTask(other, "curated:df-out:1", "print(2)\n", "2\n");
    var test = startTest(admin, token, a);
    var view = adminTest(admin, test.path("id").asLong());
    assertEquals(one, view.path("items").get(0).path("taskId").asLong(), "block 5: difficulty 1");
    assertEquals(1, view.path("items").get(0).path("difficulty").asInt());
    assertEquals(out, view.path("items").get(1).path("taskId").asLong(), "no topic older than 14 days: another passed topic");
    finishNow(admin, test.path("id").asLong());

    // Only a topic confirmed by the diagnostic has output tasks: it is used.
    db.update("update tasks set active=0 where id=?", out);
    long confirmedOut = outputTask(confirmed, "curated:df-conf-out:1", "print(3)\n", "3\n");
    test = startTest(admin, token, a);
    assertEquals(confirmedOut, adminTest(admin, test.path("id").asLong()).path("items").get(1).path("taskId").asLong());
    finishNow(admin, test.path("id").asLong());

    // Nothing else: the code item's own topic.
    db.update("update tasks set active=0 where id=?", confirmedOut);
    long sameTopic = outputTask(late, "curated:df-late-out:1", "print(4)\n", "4\n");
    test = startTest(admin, token, a);
    assertEquals(sameTopic, adminTest(admin, test.path("id").asLong()).path("items").get(1).path("taskId").asLong());
  }

  @Test void withoutPracticeTheDiagnosticThenTheFirstTopic() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("fb-a", "Фёдор", "B-3"); long a = studentId("fb-a");
    String confirmed = skill("BT_FB_CONF", 3);
    confirm(a, confirmed);
    long code = codeTask(confirmed, 2, "CURATED", "curated:fb-code:1"), out = outputTask(confirmed, "curated:fb-out:1", "print(5)\n", "5\n");
    var test = startTest(admin, token, a);
    var view = adminTest(admin, test.path("id").asLong());
    assertEquals(code, view.path("items").get(0).path("taskId").asLong(), "a topic confirmed by the diagnostic");
    assertEquals(out, view.path("items").get(1).path("taskId").asLong());

    String first = db.queryForObject("select code from skills where language='JAVA' order by block_no,sort_order,code limit 1", String.class);
    String token2 = createStudent("fb-b", "Фаина", "B-3"); long b = studentId("fb-b");
    codeTask(first, 1, "CURATED", "curated:fb-first:1"); outputTask(first, "curated:fb-first-out:1", "print(6)\n", "6\n");
    var second = adminTest(admin, startTest(admin, token2, b).path("id").asLong());
    assertEquals(first, second.path("items").get(0).path("skillCode").asText(), "nothing passed: the course's first topic");
    assertEquals(first, second.path("items").get(1).path("skillCode").asText());
  }

  @Test void aHardModeStudentGetsTheSameKindOfTest() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("hm-a", "Хасан", "B-4"); long a = studentId("hm-a");
    String topic = skill("BT_HM", 2), old = skill("BT_HM_OLD", 2);
    passed(a, old, START.minus(Duration.ofDays(30))); passed(a, topic, START.minus(Duration.ofDays(2)));
    db.update("update users set hard_mode_allowed=1,hard_mode_on=1 where id=?", a);
    long hard = codeTask(topic, 2, "CURATED", "curated:hm-hard:1"); db.update("update tasks set mode='HARD' where id=?", hard);
    long regular = codeTask(topic, 3, "CURATED", "curated:hm-regular:1");
    outputTask(old, "curated:hm-out:1", "print(7)\n", "7\n");
    var view = adminTest(admin, startTest(admin, token, a).path("id").asLong());
    assertEquals(regular, view.path("items").get(0).path("taskId").asLong(), "a regular task, never a hard one");
  }

  // ---------------------------------------------------------------- the call

  @Test void onlyTheCalledStudentStartsWhileTheCallIsActive() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("call-a", "Алия", "B-5"), other = createStudent("call-b", "Борис", "B-5");
    long a = studentId("call-a");
    simpleBank(a, "BT_CALL");
    var call = call(admin, a);
    assertEquals("CALLED", call.path("status").asText()); assertEquals(START.plus(Duration.ofMinutes(5)).toString(), call.path("expiresAt").asText());
    assertEquals(Set.of("id", "userId", "displayName", "status", "calledAt", "expiresAt", "startedAt", "endsAt", "finishedAt", "suggestedGrade", "finalGrade", "assessmentStatus"), fields(call));
    long id = call.path("id").asLong();
    var current = read(token, get("/api/board/current"));
    assertEquals(id, current.path("call").path("id").asLong()); assertTrue(current.path("test").isNull());
    assertTrue(read(other, get("/api/board/current")).path("call").isNull(), "another student sees nothing");
    expect(other, post("/api/board/tests/{id}/start", id), status().isNotFound(), "BOARD_TEST_NOT_FOUND");

    // The call expires after 5 minutes.
    now = START.plus(Duration.ofMinutes(5)).plusSeconds(1);
    assertTrue(read(token, get("/api/board/current")).path("call").isNull());
    expect(token, post("/api/board/tests/{id}/start", id), status().isBadRequest(), "BOARD_CALL_EXPIRED");
    assertEquals("EXPIRED", adminTest(admin, id).path("status").asText());
    // The teacher gives it a minute more: the call is back.
    var extended = read(admin, post("/api/admin/board/tests/{id}/extend", id).contentType(MediaType.APPLICATION_JSON).content("{\"seconds\":60}"));
    assertEquals("CALLED", extended.path("status").asText()); assertEquals(now.plusSeconds(60).toString(), extended.path("expiresAt").asText());
    expect(admin, post("/api/admin/board/tests/{id}/extend", id).contentType(MediaType.APPLICATION_JSON).content("{\"seconds\":0}"), status().isBadRequest(), "INVALID_SECONDS");
    // Cancelled: the student cannot start; a recall is a new call.
    assertEquals("CANCELLED", read(admin, post("/api/admin/board/tests/{id}/cancel", id)).path("status").asText());
    expect(token, post("/api/board/tests/{id}/start", id), status().isBadRequest(), "BOARD_CALL_CANCELLED");
    var recalled = read(admin, post("/api/admin/board/tests/{id}/recall", id));
    long second = recalled.path("id").asLong();
    assertNotEquals(id, second); assertEquals("CALLED", recalled.path("status").asText()); assertEquals(a, recalled.path("userId").asLong());
    // A new call of the same student replaces the one not started yet.
    long third = call(admin, a).path("id").asLong();
    assertEquals("CANCELLED", adminTest(admin, second).path("status").asText());
    var started = read(token, post("/api/board/tests/{id}/start", third));
    assertEquals("STARTED", started.path("status").asText());
    assertEquals(now.toString(), started.path("startedAt").asText()); assertEquals(now.plus(Duration.ofMinutes(6)).toString(), started.path("endsAt").asText());
    assertEquals(started.path("items"), read(token, post("/api/board/tests/{id}/start", third)).path("items"), "starting again returns the same test");
    var running = read(token, get("/api/board/current"));
    assertTrue(running.path("call").isNull()); assertEquals(third, running.path("test").path("id").asLong());
    expect(admin, post("/api/admin/board/tests/{id}/finish", second), status().isBadRequest(), "BOARD_TEST_NOT_STARTED");
    expect(admin, post("/api/admin/board/call").contentType(MediaType.APPLICATION_JSON).content("{\"userId\":987654,\"language\":\"JAVA\"}"), status().isNotFound(), "STUDENT_NOT_FOUND");
  }

  // ---------------------------------------------------------------- timer, checks, grades

  @Test void theServerFinishesATestAfterItsTimeWithTheLastAutosave() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("tm-a", "Тимур", "B-6"); long a = studentId("tm-a");
    simpleBank(a, "BT_TM");
    int credits = count("select count(*) from successful_task_credit where user_id=?", a), submissions = count("select count(*) from submissions");
    var test = startTest(admin, token, a); long id = test.path("id").asLong();
    String expected = adminTest(admin, id).path("items").get(1).path("expectedOutput").asText();
    assertEquals(START.toString(), read(token, put("/api/board/tests/{id}/answers", id).contentType(MediaType.APPLICATION_JSON)
        .content(json.writeValueAsString(Map.of("code", "first try")))).path("savedAt").asText());
    now = START.plus(Duration.ofMinutes(6)).plusSeconds(10); // after the end, inside the grace
    read(token, put("/api/board/tests/{id}/answers", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("code", "RIGHT at last", "output", expected.strip() + "\r\n\r\n"))));
    assertEquals("STARTED", read(token, get("/api/board/current")).path("test").path("status").asText());
    now = START.plus(Duration.ofMinutes(6)).plusSeconds(16);
    expect(token, put("/api/board/tests/{id}/answers", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"late\"}"), status().isBadRequest(), "BOARD_TEST_OVER");
    var current = read(token, get("/api/board/current"));
    assertTrue(current.path("test").isNull(), "finished by the server"); assertTrue(current.path("call").isNull());
    var view = checked(admin, id);
    assertEquals("FINISHED", view.path("status").asText()); assertEquals(now.toString(), view.path("finishedAt").asText());
    assertEquals("RIGHT at last", view.path("answers").path("code").asText(), "the last autosave");
    assertTrue(view.path("results").get(0).path("passed").asBoolean()); assertEquals("printed\n", view.path("results").get(0).path("console").path("stdout").asText());
    assertTrue(view.path("results").get(1).path("passed").asBoolean(), "CRLF and trailing newlines do not matter");
    assertEquals("5", view.path("ruleGrade").asText());
    assertEquals(credits, count("select count(*) from successful_task_credit where user_id=?", a), "nothing is credited");
    assertEquals(submissions, count("select count(*) from submissions"), "no submissions");
    expect(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"x\"}"), status().isBadRequest(), "BOARD_TEST_OVER");
    assertTrue(read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"late\"}")).path("finished").asBoolean(), "a late submit is answered, not applied");
    assertEquals("RIGHT at last", adminTest(admin, id).path("answers").path("code").asText());
  }

  @Test void outputIsComparedExactlyExceptLineEndingsAndTrailingNewlines() {
    assertTrue(BoardTests.sameOutput("a\nb\n", "a\r\nb"));
    assertTrue(BoardTests.sameOutput("a\nb", "a\nb\n\n\n"));
    assertFalse(BoardTests.sameOutput("a b\n", "a  b\n"), "spaces matter");
    assertFalse(BoardTests.sameOutput("Total: 5\n", "total: 5\n"), "case matters");
    assertFalse(BoardTests.sameOutput("a\n", "a \n"), "trailing spaces matter");
    assertFalse(BoardTests.sameOutput("a\n", "\na\n"), "leading newlines matter");
    assertFalse(BoardTests.sameOutput("a\nb\n", "a\n\nb\n"));
    assertEquals(5, BoardTests.ruleGrade(true, true, false)); assertEquals(4, BoardTests.ruleGrade(true, false, true)); assertEquals(4, BoardTests.ruleGrade(false, true, true));
    assertEquals(3, BoardTests.ruleGrade(true, false, false)); assertEquals(3, BoardTests.ruleGrade(false, true, false)); assertEquals(2, BoardTests.ruleGrade(false, false, true));
    assertNull(BoardTests.cap("ON_TRACK")); assertNull(BoardTests.cap("DONE")); assertNull(BoardTests.cap(null));
    assertEquals(4, BoardTests.cap("BORDERLINE")); assertEquals(3, BoardTests.cap("BEHIND"));
    assertEquals(3, BoardTests.suggested(5, 3)); assertEquals(4, BoardTests.suggested(4, null)); assertEquals(2, BoardTests.suggested(2, 4));
  }

  @Test void theChecksTheRuleGradeAndThePaceCapWithoutTheLlm() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("pc-a", "Полина", "B-7"); long a = studentId("pc-a");
    simpleBank(a, "BT_PC");
    db.update("insert into app_settings(key,value) values('session_date',?)", LocalDate.ofInstant(START, ZoneOffset.UTC).plusDays(7).toString());
    var test = startTest(admin, token, a); long id = test.path("id").asLong();
    var run = read(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"RIGHT draft\"}"));
    assertEquals("printed\n", run.path("console").path("stdout").asText());
    expect(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"  \"}"), status().isBadRequest(), "EMPTY_SOURCE");
    now = now.plusSeconds(100);
    var finished = read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON)
        .content(json.writeValueAsString(Map.of("code", "RIGHT final", "output", adminTest(admin, id).path("items").get(1).path("expectedOutput").asText()))));
    assertEquals(Map.of("finished", true), json.convertValue(finished, Map.class));
    var view = adminTest(admin, id);
    assertEquals("FINISHED", view.path("status").asText()); assertEquals("RIGHT final", view.path("answers").path("code").asText());
    assertEquals(1, view.path("runs").size()); assertEquals("RIGHT draft", view.path("runs").get(0).path("code").asText());
    assertEquals("OK", view.path("runs").get(0).path("console").path("status").asText());
    assertEquals("BEHIND", view.path("paceStatus").asText(), "a week to the session, the course far from closed"); assertEquals(3, view.path("paceCap").asInt());
    assertEquals("5", view.path("ruleGrade").asText()); assertEquals("3", view.path("suggestedGrade").asText(), "the pace caps the grade");
    assertEquals("UNAVAILABLE", view.path("assessment").path("status").asText()); assertFalse(view.path("assessment").path("error").asText().isBlank());
    assertEquals("UNAVAILABLE", view.path("assessmentStatus").asText());
    verify(generator, never()).assessBoardTest(anyLong(), any());

    // Not a session participant: no cap; a wrong code and a wrong output: 2.
    db.update("update users set session_participant=0 where id=?", a);
    var second = startTest(admin, token, a); long id2 = second.path("id").asLong();
    read(token, post("/api/board/tests/{id}/finish", id2).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"wrong\",\"output\":\"nope\"}"));
    var v2 = adminTest(admin, id2);
    assertTrue(v2.path("paceStatus").isNull()); assertTrue(v2.path("paceCap").isNull());
    assertFalse(v2.path("results").get(0).path("passed").asBoolean()); assertEquals("Неверный вывод программы", v2.path("results").get(0).path("output").asText());
    assertFalse(v2.path("results").get(1).path("passed").asBoolean()); assertEquals("nope", v2.path("results").get(1).path("actual").asText());
    assertEquals("2", v2.path("ruleGrade").asText()); assertEquals("2", v2.path("suggestedGrade").asText());
  }

  @Test void theLlmAssessmentTheSuggestedAndTheFinalGrade() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("llm-a", "Лейла", "B-8"); long a = studentId("llm-a");
    simpleBank(a, "BT_LLM");
    when(generator.available()).thenReturn(true);
    when(generator.assessBoardTest(eq(a), any())).thenReturn(new BoardAssessment(4, "Подход верный, не хватает «;».",
        List.of(new BoardAssessment.Item("code", "частично верно", "Строка 3: пропущена «;»."), new BoardAssessment.Item("output", "верно", "Вывод совпадает."))));
    var test = startTest(admin, token, a); long id = test.path("id").asLong();
    for (int i = 1; i <= 12; i++) read(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"run " + i + "\"}"));
    String expected = adminTest(admin, id).path("items").get(1).path("expectedOutput").asText();
    read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("code", "almost", "output", expected))));
    var view = assessed(admin, id);
    assertEquals("DONE", view.path("assessment").path("status").asText()); assertEquals(4, view.path("assessment").path("grade").asInt());
    assertEquals("Подход верный, не хватает «;».", view.path("assessment").path("summary").asText());
    assertEquals("частично верно", view.path("assessment").path("items").get(0).path("verdict").asText());
    assertEquals("4", view.path("ruleGrade").asText(), "the output right and the code partly right by the LLM");
    assertEquals("4", view.path("suggestedGrade").asText());
    var request = ArgumentCaptor.forClass(BoardAssessmentRequest.class);
    verify(generator).assessBoardTest(eq(a), request.capture());
    assertEquals(3, request.getValue().ruleGrade(), "the LLM gets the grade by the checks alone"); assertFalse(request.getValue().codePassed()); assertTrue(request.getValue().outputCorrect());
    assertEquals("almost", request.getValue().code()); assertEquals(expected, request.getValue().expectedOutput());
    assertEquals(BoardTests.LLM_RUNS, request.getValue().runs().size(), "the last ten runs");
    assertEquals("run 3", request.getValue().runs().getFirst().code()); assertEquals("run 12", request.getValue().runs().getLast().code());
    assertEquals(12, view.path("runs").size(), "all runs are kept");

    // The teacher's grade and comment, changeable any time; the student sees only date, grade and comment.
    var graded = read(admin, patch("/api/admin/board/tests/{id}", id).contentType(MediaType.APPLICATION_JSON).content("{\"finalGrade\":\"5\",\"comment\":\"  Молодец \"}"));
    assertEquals("5", graded.path("finalGrade").asText()); assertEquals("Молодец", graded.path("comment").asText()); assertEquals(now.toString(), graded.path("gradedAt").asText());
    expect(admin, patch("/api/admin/board/tests/{id}", id).contentType(MediaType.APPLICATION_JSON).content("{\"finalGrade\":\"6\"}"), status().isBadRequest(), "INVALID_GRADE");
    expect(admin, patch("/api/admin/board/tests/{id}", id).contentType(MediaType.APPLICATION_JSON).content("{\"comment\":\"" + "я".repeat(501) + "\"}"), status().isBadRequest(), "INVALID_COMMENT");
    assertEquals("4", read(admin, patch("/api/admin/board/tests/{id}", id).contentType(MediaType.APPLICATION_JSON).content("{\"finalGrade\":\"4\"}")).path("finalGrade").asText());
    var grades = read(token, get("/api/board/grades").param("language", "JAVA"));
    assertEquals(Set.of("grades"), fields(grades)); assertEquals(1, grades.path("grades").size());
    assertEquals(Set.of("date", "grade", "comment"), fields(grades.path("grades").get(0)));
    assertEquals("2041-03-01", grades.path("grades").get(0).path("date").asText()); assertEquals("4", grades.path("grades").get(0).path("grade").asText());
    assertEquals("Молодец", grades.path("grades").get(0).path("comment").asText());
    assertEquals(0, read(token, get("/api/board/grades").param("language", "PYTHON")).path("grades").size());
    var cleared = read(admin, patch("/api/admin/board/tests/{id}", id).contentType(MediaType.APPLICATION_JSON).content("{\"finalGrade\":null}"));
    assertTrue(cleared.path("finalGrade").isNull()); assertEquals("Молодец", cleared.path("comment").asText(), "only the fields sent change");
    assertEquals(0, read(token, get("/api/board/grades")).path("grades").size(), "no final grade, nothing to show");

    // The assessment again, now with the LLM failing: UNAVAILABLE with the reason, the rule grade by the checks.
    when(generator.assessBoardTest(eq(a), any())).thenThrow(new LlmUnavailableException("Codex App Server недоступен: timeout"));
    read(admin, post("/api/admin/board/tests/{id}/assess", id));
    var failed = assessed(admin, id);
    assertEquals("UNAVAILABLE", failed.path("assessment").path("status").asText()); assertEquals("Codex App Server недоступен: timeout", failed.path("assessment").path("error").asText());
    assertEquals("4", failed.path("ruleGrade").asText(), "the rule grade from the earlier assessment stays");
  }

  @Test void theAssessmentRunsLaterOnAPlatformThread() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("bg-a", "Булат", "B-10"); long a = studentId("bg-a");
    simpleBank(a, "BT_BG");
    var thread = new java.util.concurrent.atomic.AtomicReference<Thread>(); var called = new java.util.concurrent.CountDownLatch(1); var release = new java.util.concurrent.CountDownLatch(1);
    when(generator.available()).thenReturn(true);
    when(generator.assessBoardTest(eq(a), any())).thenAnswer(i -> { thread.set(Thread.currentThread()); called.countDown(); release.await(); return new BoardAssessment(3, "Есть ошибки.", List.of()); });
    long id = startTest(admin, token, a).path("id").asLong();
    board.runBackgroundWorkWith(null);
    try {
      read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"RIGHT\",\"output\":\"no\"}"));
      assertTrue(called.await(5, java.util.concurrent.TimeUnit.SECONDS), "the LLM is asked after the finish");
      assertFalse(thread.get().isVirtual(), "a platform thread"); assertTrue(thread.get().getName().startsWith("board-"), thread.get().getName());
      assertEquals("PENDING", adminTest(admin, id).path("assessment").path("status").asText(), "the finish does not wait for the LLM");
      release.countDown();
      Thread.sleep(300); // the background thread stores the assessment; nothing else touches the database meanwhile
      assertEquals("DONE", adminTest(admin, id).path("assessment").path("status").asText());
    } finally { release.countDown(); board.runBackgroundWorkWith(Runnable::run); }
  }

  @Test void theStudentNeverSeesTheExpectedOutputTheTaskOrTheAssessment() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("lk-a", "Лука", "B-9"); long a = studentId("lk-a");
    simpleBank(a, "BT_LK");
    long id = call(admin, a).path("id").asLong();
    var started = read(token, post("/api/board/tests/{id}/start", id));
    assertEquals(Set.of("id", "status", "startedAt", "endsAt", "now", "items", "answers"), fields(started));
    assertEquals(Set.of("kind", "title", "statement", "starterCode", "language"), fields(started.path("items").get(0)));
    assertEquals(Set.of("kind", "program", "language"), fields(started.path("items").get(1)));
    assertEquals(Set.of("code", "output"), fields(started.path("answers")));
    String text = mvc.perform(get("/api/board/current").cookie(cookie(token))).andReturn().getResponse().getContentAsString();
    assertEquals(started.path("items"), json.readTree(text).path("test").path("items"));
    for (String leak : List.of("second line", "expectedOutput", "taskId", "externalKey", "results", "assessment", "suggestedGrade", "ruleGrade", "reference"))
      assertFalse(text.contains(leak), "the student view leaks " + leak);
    read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"RIGHT\",\"output\":\"x\"}"));
    var after = read(token, get("/api/board/current"));
    assertTrue(after.path("test").isNull() && after.path("call").isNull(), "nothing after the finish");
    expect(token, post("/api/board/tests/{id}/start", id), status().isBadRequest(), "BOARD_TEST_FINISHED");
  }

  // ---------------------------------------------------------------- teacher

  @Test void theSuggestionPrefersPresentStudentsNotAskedTheLongest() throws Exception {
    String admin = login("admin", "admin-pass");
    long never1 = studentRow("rt-a", "Арсен", "R-1"), never2 = studentRow("rt-b", "Белла", "R-1"), tenDays = studentRow("rt-c", "Вадим", "R-1"),
        yesterday = studentRow("rt-d", "Гуля", "R-1"), today = studentRow("rt-e", "Дима", "R-1"), absent = studentRow("rt-f", "Ева", "R-1"), volunteer = studentRow("rt-g", "Жора", "R-1");
    db.update("update users set session_participant=0 where id=?", volunteer);
    for (long u : List.of(never1, never2, tenDays, yesterday, today, volunteer)) presentLesson(u);
    finishedTest(tenDays, "R-1", START.minus(Duration.ofDays(10)), "4");
    finishedTest(yesterday, "R-1", START.minus(Duration.ofDays(1)), null);
    finishedTest(today, "R-1", START.minus(Duration.ofHours(1)), "5");
    finishedTest(today, "R-1", START.minus(Duration.ofDays(3)), "3");
    var board = read(admin, get("/api/admin/board").param("group", "R-1").param("language", "JAVA"));
    assertEquals(List.of("rt-a", "rt-b", "rt-c", "rt-d", "rt-e", "rt-f", "rt-g"), board.path("members").findValuesAsText("login"));
    var e = member(board, "rt-e");
    assertEquals(Set.of("userId", "login", "displayName", "present", "lastTestAt", "tests", "lastGrade"), fields(e));
    assertTrue(e.path("present").asBoolean()); assertEquals(2, e.path("tests").asInt()); assertEquals("5", e.path("lastGrade").asText());
    assertEquals(START.minus(Duration.ofHours(1)).toString(), e.path("lastTestAt").asText());
    assertFalse(member(board, "rt-f").path("present").asBoolean()); assertTrue(member(board, "rt-a").path("lastTestAt").isNull());
    assertTrue(member(board, "rt-d").path("lastGrade").isNull());
    long suggested = board.path("suggested").asLong();
    assertTrue(Set.of(never1, never2, tenDays).contains(suggested), "present, the three oldest; got " + suggested);
    assertEquals(suggested, read(admin, get("/api/admin/board").param("group", "R-1").param("language", "JAVA")).path("suggested").asLong(), "stable between polls");

    // A called student is not suggested; the call is in the active panel.
    call(admin, never1); call(admin, never2); call(admin, tenDays);
    var after = read(admin, get("/api/admin/board").param("group", "R-1").param("language", "JAVA"));
    assertTrue(Set.of(yesterday, today).contains(after.path("suggested").asLong()), "yesterday and today remain: " + after.path("suggested"));
    assertTrue(after.path("active").findValuesAsText("status").containsAll(List.of("CALLED", "FINISHED")));
    assertEquals(3, after.path("active").findValuesAsText("status").stream().filter("CALLED"::equals).count());
    // Nobody present: everyone taking the session.
    db.update("update lessons set finished_at=?,last_activity_at=?,started_at=? where user_id in (?,?,?,?,?,?)", "2041-02-01 00:00:00", "2041-02-01T00:00:00Z", "2041-02-01 00:00:00", never1, never2, tenDays, yesterday, today, volunteer);
    db.update("update board_tests set status='CANCELLED' where status='CALLED'");
    long nobody = read(admin, get("/api/admin/board").param("group", "R-1").param("language", "JAVA")).path("suggested").asLong();
    assertTrue(Set.of(never1, never2, absent).contains(nobody), "never tested, absent included; got " + nobody);
    expect(admin, get("/api/admin/board").param("group", "Нет такой"), status().isNotFound(), "GROUP_NOT_FOUND");
  }

  @Test void theJournalDeletionAndAdminOnlyAccess() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("jr-a", "Яна", "J-9"); long a = studentId("jr-a"); long b = studentRow("jr-b", "Артур", "J-9");
    simpleBank(a, "BT_JR");
    long first = startTest(admin, token, a).path("id").asLong();
    read(token, post("/api/board/tests/{id}/finish", first).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"RIGHT\",\"output\":\"\"}"));
    read(admin, patch("/api/admin/board/tests/{id}", first).contentType(MediaType.APPLICATION_JSON).content("{\"finalGrade\":\"3\"}"));
    now = now.plus(Duration.ofDays(2));
    long second = startTest(admin, token, a).path("id").asLong();
    read(admin, post("/api/admin/board/tests/{id}/finish", second));
    now = now.plusSeconds(60);
    long cancelled = call(admin, a).path("id").asLong(); read(admin, post("/api/admin/board/tests/{id}/cancel", cancelled));
    var journal = read(admin, get("/api/admin/board/journal").param("group", "J-9").param("language", "JAVA"));
    assertEquals(List.of(cancelled, second, first), journal.path("tests").findValues("id").stream().map(JsonNode::asLong).toList(), "newest first");
    assertEquals(Set.of("id", "userId", "displayName", "calledAt", "status", "finalGrade", "suggestedGrade"), fields(journal.path("tests").get(0)));
    assertEquals(List.of("Артур", "Яна"), journal.path("students").findValuesAsText("displayName"));
    var yana = journal.path("students").get(1);
    assertEquals(2, yana.path("grades").size(), "finished tests only");
    assertEquals("3", yana.path("grades").get(0).asText(), "oldest first"); assertTrue(yana.path("grades").get(1).isNull(), "not graded yet");
    assertEquals(START.plus(Duration.ofDays(2)).toString(), yana.path("lastTestAt").asText());
    assertEquals(0, journal.path("students").get(0).path("grades").size());

    // Admin-only, both ways.
    for (var request : List.<MockHttpServletRequestBuilder>of(get("/api/admin/board").param("group", "J-9"), get("/api/admin/board/journal").param("group", "J-9"),
        get("/api/admin/board/tests/{id}", first), post("/api/admin/board/tests/{id}/cancel", first), post("/api/admin/board/tests/{id}/recall", first),
        post("/api/admin/board/tests/{id}/extend", first).contentType(MediaType.APPLICATION_JSON).content("{}"), post("/api/admin/board/tests/{id}/finish", first),
        post("/api/admin/board/tests/{id}/assess", first), delete("/api/admin/board/tests/{id}", first),
        patch("/api/admin/board/tests/{id}", first).contentType(MediaType.APPLICATION_JSON).content("{\"finalGrade\":\"5\"}"),
        post("/api/admin/board/call").contentType(MediaType.APPLICATION_JSON).content("{\"userId\":" + a + "}")))
      expect(token, request, status().isBadRequest(), "FORBIDDEN");
    for (var request : List.<MockHttpServletRequestBuilder>of(get("/api/board/current"), get("/api/board/grades"), post("/api/board/tests/{id}/start", first),
        put("/api/board/tests/{id}/answers", first).contentType(MediaType.APPLICATION_JSON).content("{}"), post("/api/board/tests/{id}/finish", first).contentType(MediaType.APPLICATION_JSON).content("{}")))
      expect(admin, request, status().isBadRequest(), "FORBIDDEN");
    assertEquals("3", adminTest(admin, first).path("finalGrade").asText());

    assertTrue(read(admin, delete("/api/admin/board/tests/{id}", cancelled)).path("deleted").asBoolean());
    expect(admin, get("/api/admin/board/tests/{id}", cancelled), status().isNotFound(), "BOARD_TEST_NOT_FOUND");
    // Deleting a student deletes their tests.
    mvc.perform(delete("/api/admin/students/{id}", a).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"confirmLogin\":\"jr-a\"}")).andExpect(status().isOk());
    assertEquals(0, count("select count(*) from board_tests where user_id=?", a));
    assertEquals(1, read(admin, get("/api/admin/board/journal").param("group", "J-9").param("language", "JAVA")).path("students").size());
    assertTrue(b > 0);
  }

  // ---------------------------------------------------------------- helpers

  /** A recent topic with a code task and an older topic with an output task, so a test can start. */
  private void simpleBank(long user, String prefix) {
    String topic = skill(prefix, 2), old = skill(prefix + "_OLD", 2);
    passed(user, old, START.minus(Duration.ofDays(30))); passed(user, topic, START.minus(Duration.ofDays(1)));
    codeTask(topic, 2, "CURATED", "curated:" + prefix.toLowerCase() + ":1");
    outputTask(old, "curated:" + prefix.toLowerCase() + "-out:1", "print('" + prefix + "')\n", prefix + "\nsecond line\n");
  }
  private JsonNode call(String admin, long user) throws Exception {
    return read(admin, post("/api/admin/board/call").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userId", user, "language", "JAVA"))));
  }
  private JsonNode startTest(String admin, String token, long user) throws Exception {
    return read(token, post("/api/board/tests/{id}/start", call(admin, user).path("id").asLong()));
  }
  private void finishNow(String admin, long id) throws Exception { read(admin, post("/api/admin/board/tests/{id}/finish", id)); }
  private JsonNode adminTest(String admin, long id) throws Exception { return read(admin, get("/api/admin/board/tests/{id}", id)); }
  /** The admin view once the background checks are done. */
  private JsonNode checked(String admin, long id) throws Exception {
    for (int i = 0; i < 100; i++) { var v = adminTest(admin, id); if (!v.path("results").isNull()) return v; Thread.sleep(50); }
    throw new AssertionError("test " + id + " was not checked");
  }
  /** The admin view once the background assessment is done. */
  private JsonNode assessed(String admin, long id) throws Exception {
    for (int i = 0; i < 100; i++) { var v = adminTest(admin, id); if (!"PENDING".equals(v.path("assessment").path("status").asText())) return v; Thread.sleep(50); }
    throw new AssertionError("test " + id + " was not assessed");
  }
  private static JsonNode member(JsonNode board, String login) { for (var m : board.path("members")) if (login.equals(m.path("login").asText())) return m; throw new AssertionError(login); }

  private String skill(String code, int block) {
    db.update("insert into skills(code,title,sort_order,prerequisite_code,block_no,language) values(?,?,?,null,?,'JAVA')", code, "Тема " + code, 10_000 + ++order, block);
    return code;
  }
  private long task(String skill, Integer difficulty, String source, String key, String goal, String reference) {
    long id = db.queryForObject("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,difficulty,mode,source,external_key,goal_json,reference_code) "
        + "values(?,?,'statement','','class TestHarness {}','TestHarness.java','JAVA',?,'NORMAL',?,?,?,?) returning id", Long.class, skill, "task " + UUID.randomUUID(), difficulty, source, key, goal, reference);
    db.update("insert into task_target_skills(task_id,skill_code) values(?,?)", id, skill);
    return id;
  }
  private long codeTask(String skill, int difficulty, String source, String key) {
    long id = task(skill, difficulty, source, key, "{\"kind\":\"OUTPUT_TEXT\",\"expectedOutput\":\"ok\\n\"}", null);
    db.update("update tasks set starter_code=?,title=? where id=?", "starter " + id, "Задача " + id, id);
    return id;
  }
  private long outputTask(String skill, String key, String reference, String expected) throws RuntimeException {
    // Difficulty 3, so that it does not compete for the code item of the tests (difficulty 1 or 2 is preferred).
    try { return task(skill, 3, "CURATED", key, json.writeValueAsString(Map.of("kind", "OUTPUT_TEXT", "expectedOutput", expected)), reference); }
    catch (Exception e) { throw new IllegalStateException(e); }
  }
  /** The first iteration of a topic completed by practice at `at`: a lesson, a passed submission, the iteration. */
  private void passed(long user, String skill, Instant at) {
    long lesson = lesson(user, at.minusSeconds(600), true);
    long t = task(skill, 1, "LLM", null, null, null); db.update("update tasks set active=0 where id=?", t);
    db.update("insert into submissions(lesson_id,task_id,source_code,passed,runner_output,created_at) values(?,?,'code',1,'ok',?)", lesson, t, sql(at));
    db.update("insert into skill_iterations(user_id,skill_code,iteration_number,lesson_id) values(?,?,1,?)", user, skill, lesson);
    db.update("insert into student_skills(user_id,skill_code,completed_iterations) values(?,?,1) on conflict(user_id,skill_code) do update set completed_iterations=1", user, skill);
  }
  private void confirm(long user, String skill) { db.update("insert into diagnostic_skill_results(user_id,skill_code,correct,total,confirmed) values(?,?,3,3,1)", user, skill); }
  private void credit(long user, long task) { db.update("insert into successful_task_credit(user_id,task_id) values(?,?)", user, task); }
  private long lesson(long user, Instant started, boolean finished) {
    return db.queryForObject("insert into lessons(user_id,lesson_number,language,language_lesson_number,started_at,finished_at,last_activity_at) values(?,(select coalesce(max(lesson_number),0)+1 from lessons where user_id=?),'JAVA',1,?,?,?) returning id",
        Long.class, user, user, sql(started), finished ? sql(started.plusSeconds(3600)) : null, started.toString());
  }
  /** Active in the course ten minutes ago, the lesson finished. */
  private void presentLesson(long user) { lesson(user, START.minus(Duration.ofMinutes(30)), true); db.update("update lessons set last_activity_at=? where user_id=?", START.minus(Duration.ofMinutes(10)).toString(), user); }
  private void finishedTest(long user, String group, Instant started, String grade) {
    db.update("insert into board_tests(user_id,group_name,language,status,called_at,call_expires_at,started_at,ends_at,finished_at,final_grade,results_json) values(?,?,'JAVA','FINISHED',?,?,?,?,?,?,'[]')",
        user, group, started.minusSeconds(60).toString(), started.plusSeconds(240).toString(), started.toString(), started.plusSeconds(360).toString(), started.plusSeconds(360).toString(), grade);
  }
  private static String sql(Instant at) { return at.toString().replace('T', ' ').substring(0, 19); }
  private long studentRow(String login, String name, String group) {
    return db.queryForObject("insert into users(login,password_hash,role,display_name,group_name) values(?,'-','STUDENT',?,?) returning id", Long.class, login, name, group);
  }
  private int count(String sql, Object... params) { return db.queryForObject(sql, Integer.class, params); }
  private static Set<String> fields(JsonNode node) { var names = new HashSet<String>(); node.fieldNames().forEachRemaining(names::add); return names; }

  private JsonNode read(String token, MockHttpServletRequestBuilder request) throws Exception {
    var response = mvc.perform(request.cookie(cookie(token))).andReturn().getResponse();
    assertEquals(200, response.getStatus(), response.getContentAsString());
    return json.readTree(response.getContentAsString());
  }
  private void expect(String token, MockHttpServletRequestBuilder request, ResultMatcher status, String error) throws Exception {
    var body = json.readTree(mvc.perform(request.cookie(cookie(token))).andExpect(status).andReturn().getResponse().getContentAsString());
    assertEquals(error, body.path("error").asText(), body.toString());
  }
  private String createStudent(String login, String name, String group) throws Exception {
    var body = new LinkedHashMap<String, Object>(Map.of("login", login, "password", "student-pass", "displayName", name, "group", group));
    mvc.perform(post("/api/admin/students").cookie(cookie(login("admin", "admin-pass"))).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(body))).andExpect(status().isOk());
    return login(login, "student-pass");
  }
  private String login(String login, String password) throws Exception {
    return mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login", login, "password", password)))).andExpect(status().isOk()).andReturn().getResponse().getCookie("adaptive_session").getValue();
  }
  private long studentId(String login) { return db.queryForObject("select id from users where login=?", Long.class, login); }
  private jakarta.servlet.http.Cookie cookie(String value) { return new jakarta.servlet.http.Cookie("adaptive_session", value); }
}
