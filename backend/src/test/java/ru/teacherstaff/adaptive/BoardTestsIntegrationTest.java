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
 * «К доске» end to end: the kinds chosen at the call and the test time, the choice of the items (parsons, fix, code),
 * the call (only the called student, expiry, cancel, recall, extend), the timer (autosave window, the server's finish
 * with the last autosave), the checks per item (nothing credited), the weighted grade, the pace cap, the LLM assessment
 * (verdicts, questions, unavailable), the teacher's grade, what the student may see, the rotation suggestion, the journal
 * and admin-only access. The LLM and Piston are stubbed; the clock is the test's. Every test uses topics and students of
 * its own.
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

  /** The parsons task of the tests: the block (4 meaningful lines, a comment and a blank line dropped) replaces the placeholder. */
  static final String PARSONS_STARTER = "public class Solution {\n    public static void main(String[] args) {\n        // Напиши решение здесь\n    }\n}\n";
  static final List<String> BLOCK = List.of("        int x = 1;", "        int y = 2;", "        System.out.println(x + y);", "        System.out.println(\"done\");");
  static final String BEFORE = "public class Solution {\n    public static void main(String[] args) {", AFTER = "    }\n}\n";
  static final String PARSONS_REFERENCE = BEFORE + "\n" + BLOCK.get(0) + "\n        // the second number\n" + BLOCK.get(1) + "\n\n" + BLOCK.get(2) + "\n" + BLOCK.get(3) + "\n" + AFTER;
  /** The extra line: a wrong solution replaces exactly the second line of the block. */
  static final String EXTRA = "        int y = 3;";
  /** The programs the stubbed checks accept: the reference order and the declarations swapped. */
  static final Set<String> VALID = Set.of(assembled(BLOCK), assembled(List.of(BLOCK.get(1), BLOCK.get(0), BLOCK.get(2), BLOCK.get(3))));
  static String assembled(List<String> lines) { return BEFORE + "\n" + String.join("\n", lines) + "\n" + AFTER; }
  static final String FIX_REFERENCE = "int a = 1;\nint b = 2;\nint c = 3;\nprint(a + b + c);\n";

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
    when(runner.run(any(Language.class), anyString(), anyString())).thenAnswer(call -> ((String) call.getArgument(1)).contains("RIGHT") || VALID.contains((String) call.getArgument(1))
        ? new PistonCodeRunner.Run(true, "Решение прошло скрытые проверки", PistonCodeRunner.Outcome.PASSED)
        : new PistonCodeRunner.Run(false, "Неверный вывод программы", PistonCodeRunner.Outcome.CHECK_FAILED));
    when(runner.console(any(Language.class), anyString())).thenReturn(new PistonCodeRunner.Console("OK", "printed\n", null, false));
    when(runner.console(any(Language.class), anyString(), anyString())).thenReturn(new PistonCodeRunner.Console("OK", "printed\n", null, false));
    when(tutor.status(anyLong())).thenReturn(new LlmStatus(false, false, false, "DISABLED", "gpt-6-luna"));
    when(generator.available()).thenReturn(false);
    board.runBackgroundWorkWith(Runnable::run);
  }

  // ---------------------------------------------------------------- kinds and time

  @Test void theKindsAreChosenAtTheCallAndGiveTheTime() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("kd-a", "Карина", "K-1"); long a = studentId("kd-a");
    simpleBank(a, "BT_KD");
    var all = call(admin, a, null);
    assertEquals(List.of("parsons", "fix", "code"), texts(all.path("kinds")), "no kinds: all three"); assertEquals(420, all.path("durationSeconds").asInt(), "2 + 2 + 3 minutes");
    var current = read(token, get("/api/board/current")).path("call");
    assertEquals(List.of("parsons", "fix", "code"), texts(current.path("kinds"))); assertEquals(420, current.path("durationSeconds").asInt());
    var two = call(admin, a, List.of("code", "parsons", "code"));
    assertEquals(List.of("parsons", "code"), texts(two.path("kinds")), "stored in the canonical order"); assertEquals(300, two.path("durationSeconds").asInt());
    for (var bad : List.of("[]", "[\"output\"]", "\"code\"", "[\"code\",7]"))
      expect(admin, post("/api/admin/board/call").contentType(MediaType.APPLICATION_JSON).content("{\"userId\":" + a + ",\"language\":\"JAVA\",\"kinds\":" + bad + "}"), status().isBadRequest(), "INVALID_KINDS");
    // The recall keeps the kinds; the test lasts their minutes and has their items only.
    var recalled = read(admin, post("/api/admin/board/tests/{id}/recall", two.path("id").asLong()));
    assertEquals(List.of("parsons", "code"), texts(recalled.path("kinds"))); assertEquals(300, recalled.path("durationSeconds").asInt());
    var test = read(token, post("/api/board/tests/{id}/start", recalled.path("id").asLong()));
    assertEquals(START.plusSeconds(300).toString(), test.path("endsAt").asText()); assertEquals(300, test.path("durationSeconds").asInt());
    assertEquals(List.of("parsons", "code"), test.path("items").findValuesAsText("kind"));
    assertEquals(Set.of("parsons", "code"), fields(test.path("answers"))); assertEquals(0, test.path("answers").path("parsons").size());
    finishNow(admin, test.path("id").asLong());
    var fix = read(token, post("/api/board/tests/{id}/start", call(admin, a, List.of("fix")).path("id").asLong()));
    assertEquals(START.plusSeconds(120).toString(), fix.path("endsAt").asText());
    assertEquals(List.of("fix"), fix.path("items").findValuesAsText("kind"));
  }

  // ---------------------------------------------------------------- items

  @Test void theCodeItemComesFromTheRecentPracticeTopicPreferringEasyAndShortTasks() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("it-a", "Ирина", "B-1"); long a = studentId("it-a");
    String recent = skill("BT_IT_RECENT", 2), older = skill("BT_IT_OLDER", 2);
    passed(a, older, START.minus(Duration.ofDays(40)));
    passed(a, recent, START.minus(Duration.ofDays(3)));
    // The recent topic: a solved story, an unsolved one (two variants), a long one, another difficulty, another source, an input task, a hard task.
    long solved = codeTask(recent, 1, "CURATED", "curated:it-solved:1"); codeTask(recent, 1, "CURATED", "curated:it-solved:2"); credit(a, solved);
    long wanted1 = codeTask(recent, 1, "CURATED", "curated:it-fresh:1"), wanted2 = codeTask(recent, 1, "CURATED", "curated:it-fresh:2");
    long longer = codeTask(recent, 1, "CURATED", "curated:it-long:1");
    db.update("update tasks set reference_code=? where id=?", "starter " + longer + "\n" + "x();\n".repeat(11), longer);
    long shortOne = codeTask(recent, 1, "CURATED", "curated:it-fresh:3"); db.update("update tasks set reference_code=? where id=?", "starter " + shortOne + "\n" + "x();\n".repeat(10), shortOne);
    codeTask(recent, 2, "CURATED", "curated:it-harder:1"); codeTask(recent, 1, "LLM", null);
    long io = codeTask(recent, 1, "CURATED", "curated:it-io:1"); db.update("update tasks set goal_json='{\"kind\":\"IO_BEHAVIOR\"}' where id=?", io);
    long hard = codeTask(recent, 1, "CURATED", "curated:it-hard:1"); db.update("update tasks set mode='HARD' where id=?", hard);
    codeTask(older, 1, "CURATED", "curated:it-older:1");

    for (int i = 0; i < 6; i++) {
      var test = startTest(admin, token, a, List.of("code"));
      var code = test.path("items").get(0);
      var item = adminTest(admin, test.path("id").asLong()).path("items").get(0);
      long codeTask = item.path("taskId").asLong();
      assertTrue(Set.of(wanted1, wanted2, shortOne).contains(codeTask), "an unsolved short curated story of the recent topic at difficulty 1, got " + codeTask);
      assertEquals(recent, item.path("skillCode").asText()); assertEquals(1, item.path("difficulty").asInt());
      assertEquals(Set.of("kind", "title", "statement", "language", "starterCode"), fields(code));
      assertEquals("code", code.path("kind").asText()); assertEquals("JAVA", code.path("language").asText()); assertEquals("Задача " + codeTask, code.path("title").asText());
      assertEquals("starter " + codeTask, code.path("starterCode").asText()); assertEquals("starter " + codeTask, test.path("answers").path("code").asText());
      finishNow(admin, test.path("id").asLong());
    }
    assertEquals(0, count("select count(*) from submissions where task_id in (?,?)", wanted1, wanted2), "a board test makes no submissions");
  }

  @Test void withoutPracticeTheDiagnosticThenTheFirstTopic() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("fb-a", "Фёдор", "B-3"); long a = studentId("fb-a");
    String confirmed = skill("BT_FB_CONF", 3);
    confirm(a, confirmed);
    long code = codeTask(confirmed, 1, "CURATED", "curated:fb-code:1"), parsons = parsonsTask(confirmed, 2, "curated:fb-parsons:1", true);
    var view = adminTest(admin, startTest(admin, token, a, List.of("parsons", "code")).path("id").asLong());
    assertEquals(parsons, view.path("items").get(0).path("taskId").asLong(), "a topic confirmed by the diagnostic");
    assertEquals(code, view.path("items").get(1).path("taskId").asLong());

    String first = db.queryForObject("select code from skills where language='JAVA' order by block_no,sort_order,code limit 1", String.class);
    String token2 = createStudent("fb-b", "Фаина", "B-3"); long b = studentId("fb-b");
    codeTask(first, 1, "CURATED", "curated:fb-first:1"); parsonsTask(first, 2, "curated:fb-first-p:1", false);
    var second = adminTest(admin, startTest(admin, token2, b, List.of("parsons", "code")).path("id").asLong());
    assertEquals(first, second.path("items").get(0).path("skillCode").asText(), "nothing passed: the course's first topic");
    assertEquals(first, second.path("items").get(1).path("skillCode").asText());
    // The first topic has no task for «Исправь ошибку»: the search goes on through the course.
    String later = skill("BT_FB_LATER", 9);
    long laterFix = fixTask(later, 2, "curated:fb-later-fix:1", Map.of("b равно 3", "int a = 1;\nint b = 3;\nint c = 3;\nprint(a + b + c);\n"));
    String token3 = createStudent("fb-c", "Фатима", "B-3"); long c = studentId("fb-c");
    var fix = adminTest(admin, startTest(admin, token3, c, List.of("fix")).path("id").asLong()).path("items").get(0);
    assertEquals("fix", fix.path("kind").asText()); assertNotEquals(first, fix.path("skillCode").asText(), "nothing to fix in the first topic");
    assertTrue(db.queryForObject("select count(*) from tasks where id=? or (wrong_json is not null and skill_code=?)", Integer.class, laterFix, fix.path("skillCode").asText()) > 0);
    // No task of a kind in the whole course: the error names it.
    var body = json.readTree(mvc.perform(post("/api/board/tests/{id}/start", read(admin, post("/api/admin/board/call").contentType(MediaType.APPLICATION_JSON)
            .content(json.writeValueAsString(Map.of("userId", b, "language", "PYTHON", "kinds", List.of("fix"))))).path("id").asLong()).cookie(cookie(token2)))
        .andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
    assertEquals("NO_BOARD_TASK", body.path("error").asText()); assertTrue(body.path("message").asText().contains("Исправь ошибку"), body.toString());
  }

  @Test void aHardModeStudentGetsTheSameKindOfTest() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("hm-a", "Хасан", "B-4"); long a = studentId("hm-a");
    String topic = skill("BT_HM", 2);
    passed(a, topic, START.minus(Duration.ofDays(2)));
    db.update("update users set hard_mode_allowed=1,hard_mode_on=1 where id=?", a);
    long hard = codeTask(topic, 1, "CURATED", "curated:hm-hard:1"); db.update("update tasks set mode='HARD' where id=?", hard);
    long regular = codeTask(topic, 3, "CURATED", "curated:hm-regular:1");
    var view = adminTest(admin, startTest(admin, token, a, List.of("code")).path("id").asLong());
    assertEquals(regular, view.path("items").get(0).path("taskId").asLong(), "a regular task, never a hard one");
  }

  @Test void theParsonsItemFromAnOlderTopicWithItsLinesShuffledAndNothingLeaked() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("ps-a", "Патимат", "P-1"); long a = studentId("ps-a");
    String older = skill("BT_PS_OLD", 2), recent = skill("BT_PS_NEW", 2);
    passed(a, older, START.minus(Duration.ofDays(30))); passed(a, recent, START.minus(Duration.ofDays(2)));
    parsonsTask(recent, 2, "curated:ps-recent:1", true); // a recent topic: only when no older one has a task
    // Not eligible: two placeholders; a block of three lines; the reference does not keep the starter.
    long two = parsonsTask(older, 2, "curated:ps-two:1", true); db.update("update tasks set starter_code=? where id=?", PARSONS_STARTER.replace("    }\n}", "        // Напиши решение здесь\n    }\n}"), two);
    long three = parsonsTask(older, 2, "curated:ps-three:1", true); db.update("update tasks set reference_code=replace(reference_code,?,'') where id=?", BLOCK.get(3) + "\n", three);
    long other = parsonsTask(older, 2, "curated:ps-other:1", true); db.update("update tasks set reference_code=replace(reference_code,'public class','class') where id=?", other);
    long plain = parsonsTask(older, 2, "curated:ps-plain:1", false), withExtra = parsonsTask(older, 2, "curated:ps-extra:1", true);
    var orders = new HashSet<List<String>>();
    for (int i = 0; i < 5; i++) {
      var test = startTest(admin, token, a, List.of("parsons")); long id = test.path("id").asLong();
      var item = adminTest(admin, id).path("items").get(0);
      assertEquals(withExtra, item.path("taskId").asLong(), "an eligible task of the older topic, the one with an extra line preferred");
      assertEquals(BEFORE, item.path("before").asText()); assertEquals(AFTER, item.path("after").asText());
      assertEquals(5, item.path("lines").size()); assertEquals(List.of("l1", "l2", "l3", "l4", "l5"), item.path("lines").findValuesAsText("id"), "numbered in the order shown");
      var text = new HashMap<String, String>(); for (var l : item.path("lines")) text.put(l.path("id").asText(), l.path("text").asText());
      assertEquals(BLOCK, texts(item.path("solution")).stream().map(text::get).toList(), "the solution: the block in the reference order, with its indentation");
      assertEquals(EXTRA, text.get(item.path("extraLineId").asText()));
      var shown = item.path("lines").findValuesAsText("text").stream().filter(BLOCK::contains).toList();
      assertNotEquals(BLOCK, shown, "never in the solution order"); orders.add(item.path("lines").findValuesAsText("text"));
      assertEquals(PARSONS_REFERENCE, item.path("reference").asText());
      // The student: the lines and their number, nothing of the solution.
      var p = test.path("items").get(0);
      assertEquals(Set.of("kind", "title", "statement", "language", "before", "after", "lines", "extraLines"), fields(p));
      assertEquals(1, p.path("extraLines").asInt()); assertEquals(item.path("lines"), p.path("lines")); assertEquals(Set.of("id", "text"), fields(p.path("lines").get(0)));
      String body = mvc.perform(get("/api/board/current").cookie(cookie(token))).andReturn().getResponse().getContentAsString();
      for (String leak : List.of("solution", "extraLineId", "reference", "the second number", "taskId", "externalKey", "wrong"))
        assertFalse(body.contains(leak), "the student view leaks " + leak);
      finishNow(admin, id);
    }
    assertTrue(orders.size() > 1, "shuffled at random");
    // Without the extra line: no extra line; a test of another student without the preferred task.
    db.update("update tasks set active=0 where id=?", withExtra);
    var item = adminTest(admin, startTest(admin, token, a, List.of("parsons")).path("id").asLong()).path("items").get(0);
    assertEquals(plain, item.path("taskId").asLong()); assertEquals(0, item.path("extraLines").asInt()); assertTrue(item.path("extraLineId").isNull()); assertEquals(4, item.path("lines").size());
    assertTrue(two > 0 && three > 0 && other > 0);
  }

  @Test void parsonsIsAssembledAndCheckedAnyRightOrderPassesAndTheAnswersAreValidated() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("pa-a", "Пётр", "P-2"); long a = studentId("pa-a");
    String older = skill("BT_PA_OLD", 2); passed(a, older, START.minus(Duration.ofDays(30)));
    parsonsTask(older, 2, "curated:pa:1", true);
    // Another valid order (the declarations swapped) passes.
    long id = startTest(admin, token, a, List.of("parsons")).path("id").asLong();
    var ids = idsOf(adminTest(admin, id).path("items").get(0));
    var swapped = List.of(ids.get(BLOCK.get(1)), ids.get(BLOCK.get(0)), ids.get(BLOCK.get(2)), ids.get(BLOCK.get(3)));
    for (var bad : List.of("{\"parsons\":[\"l1\",\"l9\"]}", "{\"parsons\":[\"l1\",\"l1\"]}", "{\"parsons\":\"l1\"}", "{\"code\":\"RIGHT\"}", "{\"fix\":\"x\"}"))
      expect(token, put("/api/board/tests/{id}/answers", id).contentType(MediaType.APPLICATION_JSON).content(bad), status().isBadRequest(), "INVALID_ANSWER");
    expect(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"item\":\"parsons\",\"code\":\"x\"}"), status().isBadRequest(), "INVALID_ITEM");
    expect(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"x\"}"), status().isBadRequest(), "INVALID_ITEM");
    read(token, put("/api/board/tests/{id}/answers", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("parsons", swapped.subList(0, 2)))));
    assertEquals(swapped.subList(0, 2), texts(read(token, get("/api/board/current")).path("test").path("answers").path("parsons")), "autosaved");
    read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("parsons", swapped))));
    var view = adminTest(admin, id); var result = view.path("results").get(0);
    assertEquals(swapped, texts(view.path("answers").path("parsons")));
    assertEquals(Set.of("kind", "passed", "output", "outcome", "console", "unavailable", "program"), fields(result));
    assertTrue(result.path("passed").asBoolean()); assertEquals(assembled(List.of(BLOCK.get(1), BLOCK.get(0), BLOCK.get(2), BLOCK.get(3))), result.path("program").asText());
    assertEquals("5", view.path("ruleGrade").asText());

    // The extra line instead of its twin: the checks fail.
    id = startTest(admin, token, a, List.of("parsons")).path("id").asLong();
    var item = adminTest(admin, id).path("items").get(0); ids = idsOf(item);
    read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON)
        .content(json.writeValueAsString(Map.of("parsons", List.of(ids.get(BLOCK.get(0)), item.path("extraLineId").asText(), ids.get(BLOCK.get(2)), ids.get(BLOCK.get(3)))))));
    result = adminTest(admin, id).path("results").get(0);
    assertFalse(result.path("passed").asBoolean()); assertTrue(result.path("program").asText().contains(EXTRA)); assertEquals("Неверный вывод программы", result.path("output").asText());
    // Nothing placed: not passed, nothing run.
    id = startTest(admin, token, a, List.of("parsons")).path("id").asLong();
    clearInvocations(runner);
    finishNow(admin, id);
    view = adminTest(admin, id); result = view.path("results").get(0);
    assertFalse(result.path("passed").asBoolean()); assertEquals("Программа не собрана", result.path("output").asText()); assertTrue(result.path("program").isNull());
    assertEquals("2", view.path("ruleGrade").asText());
    verify(runner, never()).run(any(Language.class), anyString(), anyString());
  }

  @Test void theFixItemShowsTheSmallestBugAndIsCheckedLikeCode() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("fx-a", "Фатима", "F-1"); long a = studentId("fx-a");
    String topic = skill("BT_FX", 2); passed(a, topic, START.minus(Duration.ofDays(1)));
    String one = "int a = 1;\nint b = 3;\nint c = 3;\nprint(a + b + c);\n", twoLines = "int a = 1;\nint b = 3;\nint c = 4;\nprint(a + b + c);\n";
    String threeLines = "int a = 0;\nint b = 3;\nint c = 4;\nprint(a + b + c);\n", spaces = "int a = 1;\n  int b = 2;   \nint c = 3;\n\nprint(a + b + c);\n";
    long fix = fixTask(topic, 2, "curated:fx:1", Map.of("три строки", threeLines, "только пробелы", spaces, "две строки", twoLines, "b равно 3", one));
    long id = startTest(admin, token, a, List.of("fix")).path("id").asLong();
    var item = adminTest(admin, id).path("items").get(0);
    assertEquals(fix, item.path("taskId").asLong());
    assertEquals(one, item.path("program").asText(), "the wrong solution with the fewest changed lines"); assertEquals("b равно 3", item.path("bugDescription").asText());
    assertEquals(FIX_REFERENCE, item.path("reference").asText());
    var student = read(token, get("/api/board/current")).path("test");
    assertEquals(Set.of("kind", "title", "statement", "language", "program"), fields(student.path("items").get(0)));
    assertEquals(one, student.path("items").get(0).path("program").asText()); assertEquals(one, student.path("answers").path("fix").asText(), "the editor starts with the buggy program");
    assertFalse(student.toString().contains("b равно 3"), "the bug is not told");
    // «Запустить» for the fix item: recorded with its item, the answer saved.
    read(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"item\":\"fix\",\"code\":\"RIGHT draft\"}"));
    expect(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"item\":\"code\",\"code\":\"x\"}"), status().isBadRequest(), "INVALID_ITEM");
    var view = adminTest(admin, id);
    assertEquals("fix", view.path("runs").get(0).path("item").asText()); assertEquals("RIGHT draft", view.path("answers").path("fix").asText());
    read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON).content("{\"fix\":\"RIGHT fixed\"}"));
    view = adminTest(admin, id);
    assertTrue(view.path("results").get(0).path("passed").asBoolean()); assertEquals("fix", view.path("results").get(0).path("kind").asText());
    assertEquals("printed\n", view.path("results").get(0).path("console").path("stdout").asText());
    // Only bugs of more than two lines: this task is never a fix item (another topic of the course is used).
    db.update("update tasks set wrong_json=? where id=?", json.writeValueAsString(List.of(Map.of("description", "три", "source", threeLines))), fix);
    fixTask(skill("BT_FX_LATER", 9), 2, "curated:fx-later:1", Map.of("b равно 3", "int a = 1;\nint b = 3;\nint c = 3;\nprint(a + b + c);\n"));
    var other = adminTest(admin, startTest(admin, token, a, List.of("fix")).path("id").asLong()).path("items").get(0);
    assertNotEquals(fix, other.path("taskId").asLong(), "a bug of three lines is not a fix item");
  }

  @Test void fixPrefersAnotherRecentTopicThanCodeAndATestNeverRepeatsAStory() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("tp-a", "Тагир", "T-1"); long a = studentId("tp-a");
    String newest = skill("BT_TP_1", 2), next = skill("BT_TP_2", 2);
    passed(a, next, START.minus(Duration.ofDays(4))); passed(a, newest, START.minus(Duration.ofDays(1)));
    long code = codeTask(newest, 1, "CURATED", "curated:tp-code:1");
    fixTask(newest, 2, "curated:tp-fix-same:1", Map.of("b", "int a = 1;\nint b = 3;\nint c = 3;\nprint(a + b + c);\n"));
    long fixNext = fixTask(next, 2, "curated:tp-fix-next:1", Map.of("b", "int a = 1;\nint b = 3;\nint c = 3;\nprint(a + b + c);\n"));
    var view = adminTest(admin, startTest(admin, token, a, List.of("fix", "code")).path("id").asLong());
    assertEquals(code, view.path("items").get(1).path("taskId").asLong(), "code: the most recent topic");
    assertEquals(fixNext, view.path("items").get(0).path("taskId").asLong(), "fix: the next recent topic");
    finishNow(admin, view.path("id").asLong());

    // One topic only: code takes a story (difficulty 1 first), fix takes another story, never the other variant of code's.
    String token2 = createStudent("tp-b", "Тамара", "T-1"); long b = studentId("tp-b");
    String only = skill("BT_TP_ONLY", 2); passed(b, only, START.minus(Duration.ofDays(1)));
    var bug = Map.of("b", "int a = 1;\nint b = 3;\nint c = 3;\nprint(a + b + c);\n");
    long s1 = fixTask(only, 1, "curated:tp-s1:1", bug), s1b = fixTask(only, 1, "curated:tp-s1:2", bug), s2 = fixTask(only, 3, "curated:tp-s2:1", bug);
    for (int i = 0; i < 4; i++) {
      var v = adminTest(admin, startTest(admin, token2, b, List.of("fix", "code")).path("id").asLong());
      assertTrue(Set.of(s1, s1b).contains(v.path("items").get(1).path("taskId").asLong()), "code: difficulty 1");
      assertEquals(s2, v.path("items").get(0).path("taskId").asLong(), "fix: the same topic, another story");
      finishNow(admin, v.path("id").asLong());
    }
  }

  // ---------------------------------------------------------------- the call

  @Test void onlyTheCalledStudentStartsWhileTheCallIsActive() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("call-a", "Алия", "B-5"), other = createStudent("call-b", "Борис", "B-5");
    long a = studentId("call-a");
    simpleBank(a, "BT_CALL");
    var call = call(admin, a);
    assertEquals("CALLED", call.path("status").asText()); assertEquals(START.plus(Duration.ofMinutes(5)).toString(), call.path("expiresAt").asText());
    assertEquals(Set.of("id", "userId", "displayName", "status", "calledAt", "expiresAt", "startedAt", "endsAt", "finishedAt", "suggestedGrade", "finalGrade", "assessmentStatus", "kinds", "durationSeconds"), fields(call));
    long id = call.path("id").asLong();
    var current = read(token, get("/api/board/current"));
    assertEquals(id, current.path("call").path("id").asLong()); assertTrue(current.path("test").isNull());
    assertEquals(Set.of("id", "calledAt", "expiresAt", "kinds", "durationSeconds"), fields(current.path("call")));
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
    assertEquals(now.toString(), started.path("startedAt").asText()); assertEquals(now.plus(Duration.ofMinutes(7)).toString(), started.path("endsAt").asText());
    assertEquals(started.path("items"), read(token, post("/api/board/tests/{id}/start", third)).path("items"), "starting again returns the same test");
    var running = read(token, get("/api/board/current"));
    assertTrue(running.path("call").isNull()); assertEquals(third, running.path("test").path("id").asLong());
    // The teacher extends a running test.
    assertEquals(now.plus(Duration.ofMinutes(8)).toString(), read(admin, post("/api/admin/board/tests/{id}/extend", third).contentType(MediaType.APPLICATION_JSON).content("{\"seconds\":60}")).path("endsAt").asText());
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
    var solution = texts(adminTest(admin, id).path("items").get(0).path("solution"));
    assertEquals(START.toString(), read(token, put("/api/board/tests/{id}/answers", id).contentType(MediaType.APPLICATION_JSON)
        .content(json.writeValueAsString(Map.of("code", "first try")))).path("savedAt").asText());
    now = START.plus(Duration.ofMinutes(7)).plusSeconds(10); // after the end, inside the grace
    read(token, put("/api/board/tests/{id}/answers", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("code", "RIGHT at last", "parsons", solution))));
    var running = read(token, get("/api/board/current")).path("test");
    assertEquals("STARTED", running.path("status").asText()); assertEquals("RIGHT at last", running.path("answers").path("code").asText());
    assertTrue(running.path("answers").path("fix").asText().contains("int b = 3;"), "fields not sent keep their value");
    now = START.plus(Duration.ofMinutes(7)).plusSeconds(16);
    expect(token, put("/api/board/tests/{id}/answers", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"late\"}"), status().isBadRequest(), "BOARD_TEST_OVER");
    var current = read(token, get("/api/board/current"));
    assertTrue(current.path("test").isNull(), "finished by the server"); assertTrue(current.path("call").isNull());
    var view = checked(admin, id);
    assertEquals("FINISHED", view.path("status").asText()); assertEquals(now.toString(), view.path("finishedAt").asText());
    assertEquals("RIGHT at last", view.path("answers").path("code").asText(), "the last autosave");
    assertEquals(List.of("parsons", "fix", "code"), view.path("results").findValuesAsText("kind"));
    assertTrue(view.path("results").get(0).path("passed").asBoolean()); assertFalse(view.path("results").get(1).path("passed").asBoolean(), "the bug was left in");
    assertTrue(view.path("results").get(2).path("passed").asBoolean()); assertEquals("printed\n", view.path("results").get(2).path("console").path("stdout").asText());
    assertEquals("3", view.path("ruleGrade").asText(), "parsons and code: 1 + 3 of 6 points, 66.7 % → 3");
    assertEquals(credits, count("select count(*) from successful_task_credit where user_id=?", a), "nothing is credited");
    assertEquals(submissions, count("select count(*) from submissions"), "no submissions");
    expect(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"x\"}"), status().isBadRequest(), "BOARD_TEST_OVER");
    assertTrue(read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"late\"}")).path("finished").asBoolean(), "a late submit is answered, not applied");
    assertEquals("RIGHT at last", adminTest(admin, id).path("answers").path("code").asText());
  }

  @Test void theChecksTheWeightedGradeAndThePaceCapWithoutTheLlm() throws Exception {
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
        .content(json.writeValueAsString(Map.of("code", "RIGHT final", "fix", "RIGHT fixed", "parsons", texts(adminTest(admin, id).path("items").get(0).path("solution"))))));
    assertEquals(Map.of("finished", true), json.convertValue(finished, Map.class));
    var view = adminTest(admin, id);
    assertEquals("FINISHED", view.path("status").asText()); assertEquals("RIGHT final", view.path("answers").path("code").asText());
    assertEquals(1, view.path("runs").size()); assertEquals("RIGHT draft", view.path("runs").get(0).path("code").asText()); assertEquals("code", view.path("runs").get(0).path("item").asText());
    assertEquals("OK", view.path("runs").get(0).path("console").path("status").asText());
    assertEquals("BEHIND", view.path("paceStatus").asText(), "a week to the session, the course far from closed"); assertEquals(3, view.path("paceCap").asInt());
    assertEquals("5", view.path("ruleGrade").asText()); assertEquals("3", view.path("suggestedGrade").asText(), "the pace caps the grade");
    assertEquals(6, view.path("score").path("points").asDouble()); assertEquals(6, view.path("score").path("max").asInt()); assertEquals(100, view.path("score").path("percent").asDouble());
    assertEquals(List.of("parsons", "fix", "code"), view.path("score").path("items").findValuesAsText("kind"));
    assertEquals(List.of(1, 2, 3), view.path("score").path("items").findValues("weight").stream().map(JsonNode::asInt).toList());
    assertEquals("UNAVAILABLE", view.path("assessment").path("status").asText()); assertFalse(view.path("assessment").path("error").asText().isBlank());
    assertEquals("UNAVAILABLE", view.path("assessmentStatus").asText());
    verify(generator, never()).assessBoardTest(anyLong(), any());

    // Not a session participant: no cap. Only the code right: 3 of 6 points → 3; only parsons: 1 of 6 → 2.
    db.update("update users set session_participant=0 where id=?", a);
    long id2 = startTest(admin, token, a).path("id").asLong();
    read(token, post("/api/board/tests/{id}/finish", id2).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"RIGHT\",\"fix\":\"nope\"}"));
    var v2 = adminTest(admin, id2);
    assertTrue(v2.path("paceStatus").isNull()); assertTrue(v2.path("paceCap").isNull());
    assertFalse(v2.path("results").get(1).path("passed").asBoolean()); assertEquals("Неверный вывод программы", v2.path("results").get(1).path("output").asText());
    assertEquals("3", v2.path("ruleGrade").asText()); assertEquals("3", v2.path("suggestedGrade").asText()); assertEquals(50, v2.path("score").path("percent").asDouble());
    long id3 = startTest(admin, token, a).path("id").asLong();
    read(token, post("/api/board/tests/{id}/finish", id3).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("parsons", texts(adminTest(admin, id3).path("items").get(0).path("solution"))))));
    assertEquals("2", adminTest(admin, id3).path("ruleGrade").asText()); assertEquals(16.7, adminTest(admin, id3).path("score").path("percent").asDouble());
  }

  @Test void aTestOfTheFirstVersionWithAnOutputItemStillOpens() throws Exception {
    String admin = login("admin", "admin-pass");
    createStudent("v1-a", "Вера", "B-11"); long a = studentId("v1-a");
    long id = db.queryForObject("insert into board_tests(user_id,group_name,language,status,called_at,call_expires_at,started_at,ends_at,finished_at,items_json,answers_json,runs_json,results_json,rule_grade,suggested_grade,assessment_json) "
        + "values(?,'B-11','JAVA','FINISHED','2026-10-15T12:44:56Z','2026-10-15T12:49:56Z','2026-10-15T12:45:03Z','2026-10-15T12:51:03Z','2026-10-15T12:50:00Z',?,?,'[]',?,'3','3',?) returning id", Long.class, a,
        "[{\"kind\":\"code\",\"title\":\"t\",\"statement\":\"s\",\"starterCode\":\"\"},{\"kind\":\"output\",\"program\":\"p\",\"expectedOutput\":\"x\"}]",
        "{\"code\":\"c\",\"output\":\"x\"}", "[{\"kind\":\"code\",\"passed\":true},{\"kind\":\"output\",\"passed\":true}]",
        "{\"status\":\"UNAVAILABLE\",\"summary\":null,\"items\":[],\"error\":\"off\"}");
    var view = adminTest(admin, id);
    assertEquals(1, view.path("score").path("items").size(), "the output item has no score today");
    assertEquals(100, view.path("score").path("percent").asDouble());
  }

  @Test void theWeightedGradeRule() {
    assertEquals(5, BoardItems.grade(90)); assertEquals(4, BoardItems.grade(89.9)); assertEquals(4, BoardItems.grade(75)); assertEquals(3, BoardItems.grade(50)); assertEquals(2, BoardItems.grade(49.9));
    var partlyCode = Map.<String, Object>of("status", "DONE", "items", List.of(Map.of("item", "code", "verdict", "частично верно"), Map.of("item", "fix", "verdict", "частично верно")));
    // All three, the code partly right: 1 + 2 + 1.5 = 4.5 of 6 → 75 % → 4; by the checks alone 3 of 6 → 3. A partial verdict of a passed item changes nothing.
    var all = List.of(result("parsons", true), result("fix", true), result("code", false));
    assertEquals(4, BoardTests.grade(all, partlyCode)); assertEquals(3, BoardTests.grade(all, null));
    assertEquals(Map.of("parsons", 1.0, "fix", 1.0, "code", 0.5), BoardTests.scores(all, partlyCode));
    // Only the code, partly right: 1.5 of 3 → 50 % → 3.
    assertEquals(3, BoardTests.grade(List.of(result("code", false)), partlyCode));
    // Parsons and fix, only parsons right: 1 of 3 → 2; an UNAVAILABLE assessment gives no partial scores.
    assertEquals(2, BoardTests.grade(List.of(result("parsons", true), result("fix", false)), null));
    assertEquals(2, BoardTests.grade(List.of(result("parsons", true), result("fix", false)), Map.of("status", "UNAVAILABLE", "items", List.of(Map.of("item", "fix", "verdict", "частично верно")))));
    assertEquals(3, BoardTests.grade(List.of(result("parsons", true), result("fix", false)), partlyCode), "the fix partly right: 1 + 1 of 3, 66.7 % → 3");
    // «верно» by the LLM for a failed item (e.g. only the format of the output differs) gives the whole weight: 1 + 2 + 3 → 5;
    // the rule grade stays by the checks alone. A verdict of an item that is not in the test changes nothing.
    var rightCode = Map.<String, Object>of("status", "DONE", "items", List.of(Map.of("item", "code", "verdict", "верно"), Map.of("item", "fix", "verdict", "неверно")));
    assertEquals(Map.of("parsons", 1.0, "fix", 1.0, "code", 1.0), BoardTests.scores(all, rightCode)); assertEquals(5, BoardTests.grade(all, rightCode));
    assertEquals(2, BoardTests.grade(List.of(result("parsons", true), result("fix", false)), rightCode), "«неверно» of the fix: 1 of 3");
    assertEquals(3, BoardTests.grade(all, Map.of("status", "UNAVAILABLE", "items", List.of(Map.of("item", "code", "verdict", "верно")))), "an UNAVAILABLE assessment gives nothing: 3 of 6 → 3");
    assertNull(BoardTests.cap("ON_TRACK")); assertNull(BoardTests.cap("DONE")); assertNull(BoardTests.cap(null));
    assertEquals(4, BoardTests.cap("BORDERLINE")); assertEquals(3, BoardTests.cap("BEHIND"));
    assertEquals(3, BoardTests.suggested(5, 3)); assertEquals(4, BoardTests.suggested(4, null)); assertEquals(2, BoardTests.suggested(2, 4));
  }

  @Test void theLlmVerdictsRaiseTheSuggestedGradeAndTheTeacherGrades() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("llm-a", "Лейла", "B-8"); long a = studentId("llm-a");
    simpleBank(a, "BT_LLM");
    db.update("insert into app_settings(key,value) values('session_date',?)", LocalDate.ofInstant(START, ZoneOffset.UTC).plusDays(7).toString());
    when(generator.available()).thenReturn(true);
    when(generator.assessBoardTest(eq(a), any())).thenReturn(new BoardAssessment("Подход верный, не хватает «;».",
        List.of(new BoardAssessment.Item("parsons", "верно", "Порядок верный."), new BoardAssessment.Item("fix", "верно", "Исправлено."),
            new BoardAssessment.Item("code", "частично верно", "Строка 3: пропущена «;».")), List.of("Зачем здесь цикл?", "Что будет при n = 0?"),
        "Программу ты собрал и ошибку нашёл. В своём коде проверяй «;» в конце строк."));
    var test = startTest(admin, token, a); long id = test.path("id").asLong();
    var item = adminTest(admin, id).path("items");
    for (int i = 1; i <= 12; i++) read(token, post("/api/board/tests/{id}/run", id).contentType(MediaType.APPLICATION_JSON).content("{\"item\":\"" + (i % 2 == 0 ? "code" : "fix") + "\",\"code\":\"run " + i + "\"}"));
    read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON)
        .content(json.writeValueAsString(Map.of("parsons", texts(item.get(0).path("solution")), "fix", "RIGHT", "code", "almost"))));
    var view = assessed(admin, id);
    assertEquals(Set.of("status", "summary", "items", "questions", "studentComment", "error"), fields(view.path("assessment")));
    assertEquals("Программу ты собрал и ошибку нашёл. В своём коде проверяй «;» в конце строк.", view.path("assessment").path("studentComment").asText(), "the draft for the student");
    assertTrue(view.path("comment").isNull(), "the draft is not the comment until the teacher saves it");
    assertEquals("DONE", view.path("assessment").path("status").asText()); assertEquals("Подход верный, не хватает «;».", view.path("assessment").path("summary").asText());
    assertEquals("частично верно", view.path("assessment").path("items").get(2).path("verdict").asText());
    assertEquals(List.of("Зачем здесь цикл?", "Что будет при n = 0?"), texts(view.path("assessment").path("questions")), "the oral questions are stored");
    assertEquals("3", view.path("ruleGrade").asText(), "by the checks: 3 of 6 points");
    assertEquals(4.5, view.path("score").path("points").asDouble()); assertEquals(75, view.path("score").path("percent").asDouble());
    assertEquals(0.5, view.path("score").path("items").get(2).path("score").asDouble());
    assertEquals("3", view.path("suggestedGrade").asText(), "4 with the verdict, capped at 3 by the pace");
    db.update("delete from app_settings where key='session_date'"); db.update("update board_tests set pace_status=null where id=?", id);
    read(admin, post("/api/admin/board/tests/{id}/assess", id));
    view = assessed(admin, id);
    assertEquals("4", view.path("suggestedGrade").asText(), "the partial verdict raises the suggested grade"); assertEquals("3", view.path("ruleGrade").asText());
    var request = ArgumentCaptor.forClass(BoardAssessmentRequest.class);
    verify(generator, times(2)).assessBoardTest(eq(a), request.capture());
    var r = request.getValue();
    assertEquals(3, r.ruleGrade(), "the LLM gets the grade by the checks alone");
    assertEquals(List.of("parsons", "fix", "code"), r.items().stream().map(BoardAssessmentRequest.Item::kind).toList());
    assertEquals(List.of(1, 2, 3), r.items().stream().map(BoardAssessmentRequest.Item::weight).toList());
    var parsons = r.items().get(0);
    assertEquals(BLOCK, parsons.lines()); assertEquals(EXTRA, parsons.extraLine()); assertEquals(assembled(BLOCK), parsons.answer()); assertTrue(parsons.passed());
    var fix = r.items().get(1);
    assertTrue(fix.program().contains("int b = 3;")); assertEquals("b равно 3", fix.bugDescription()); assertEquals("RIGHT", fix.answer());
    var code = r.items().get(2);
    assertEquals("almost", code.answer()); assertFalse(code.passed()); assertEquals("Неверный вывод программы", code.checkOutput());
    assertEquals(BoardTests.LLM_RUNS, r.runs().size(), "the last ten runs");
    assertEquals("run 3", r.runs().getFirst().code()); assertEquals("fix", r.runs().getFirst().item()); assertEquals("run 12", r.runs().getLast().code()); assertEquals("code", r.runs().getLast().item());
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

    // The assessment again, now with the LLM failing: UNAVAILABLE with the reason, the suggested grade by the checks.
    when(generator.assessBoardTest(eq(a), any())).thenThrow(new LlmUnavailableException("Codex App Server недоступен: timeout"));
    read(admin, post("/api/admin/board/tests/{id}/assess", id));
    var failed = assessed(admin, id);
    assertEquals("UNAVAILABLE", failed.path("assessment").path("status").asText()); assertEquals("Codex App Server недоступен: timeout", failed.path("assessment").path("error").asText());
    assertEquals(0, failed.path("assessment").path("questions").size());
    assertEquals("3", failed.path("ruleGrade").asText()); assertEquals("3", failed.path("suggestedGrade").asText(), "no partial verdicts without the LLM");
    assertEquals(3, failed.path("score").path("points").asDouble());
  }

  @Test void theAssessmentRunsLaterOnAPlatformThread() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("bg-a", "Булат", "B-10"); long a = studentId("bg-a");
    simpleBank(a, "BT_BG");
    var thread = new java.util.concurrent.atomic.AtomicReference<Thread>(); var called = new java.util.concurrent.CountDownLatch(1); var release = new java.util.concurrent.CountDownLatch(1);
    when(generator.available()).thenReturn(true);
    when(generator.assessBoardTest(eq(a), any())).thenAnswer(i -> { thread.set(Thread.currentThread()); called.countDown(); release.await(); return new BoardAssessment("Есть ошибки.", List.of(), List.of()); });
    long id = startTest(admin, token, a).path("id").asLong();
    board.runBackgroundWorkWith(null);
    try {
      read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"RIGHT\"}"));
      assertTrue(called.await(5, java.util.concurrent.TimeUnit.SECONDS), "the LLM is asked after the finish");
      assertFalse(thread.get().isVirtual(), "a platform thread"); assertTrue(thread.get().getName().startsWith("board-"), thread.get().getName());
      assertEquals("PENDING", adminTest(admin, id).path("assessment").path("status").asText(), "the finish does not wait for the LLM");
      release.countDown();
      Thread.sleep(300); // the background thread stores the assessment; nothing else touches the database meanwhile
      assertEquals("DONE", adminTest(admin, id).path("assessment").path("status").asText());
    } finally { release.countDown(); board.runBackgroundWorkWith(Runnable::run); }
  }

  @Test void theStudentNeverSeesTheSolutionTheTaskOrTheAssessment() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("lk-a", "Лука", "B-9"); long a = studentId("lk-a");
    simpleBank(a, "BT_LK");
    long id = call(admin, a).path("id").asLong();
    var started = read(token, post("/api/board/tests/{id}/start", id));
    assertEquals(Set.of("id", "status", "startedAt", "endsAt", "now", "durationSeconds", "items", "answers"), fields(started));
    assertEquals(List.of("parsons", "fix", "code"), started.path("items").findValuesAsText("kind"));
    assertEquals(Set.of("kind", "title", "statement", "language", "before", "after", "lines", "extraLines"), fields(started.path("items").get(0)));
    assertEquals(Set.of("kind", "title", "statement", "language", "program"), fields(started.path("items").get(1)));
    assertEquals(Set.of("kind", "title", "statement", "language", "starterCode"), fields(started.path("items").get(2)));
    assertEquals(Set.of("parsons", "fix", "code"), fields(started.path("answers")));
    String text = mvc.perform(get("/api/board/current").cookie(cookie(token))).andReturn().getResponse().getContentAsString();
    assertEquals(started.path("items"), json.readTree(text).path("test").path("items"));
    for (String leak : List.of("solution", "extraLineId", "bugDescription", "b равно 3", "taskId", "externalKey", "results", "assessment", "suggestedGrade", "ruleGrade", "reference", "score"))
      assertFalse(text.contains(leak), "the student view leaks " + leak);
    read(token, post("/api/board/tests/{id}/finish", id).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"RIGHT\"}"));
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

    // A called student is not suggested; the call is in the active panel with its kinds.
    call(admin, never1); call(admin, never2); call(admin, tenDays, List.of("code"));
    var after = read(admin, get("/api/admin/board").param("group", "R-1").param("language", "JAVA"));
    assertTrue(Set.of(yesterday, today).contains(after.path("suggested").asLong()), "yesterday and today remain: " + after.path("suggested"));
    assertTrue(after.path("active").findValuesAsText("status").containsAll(List.of("CALLED", "FINISHED")));
    assertEquals(3, after.path("active").findValuesAsText("status").stream().filter("CALLED"::equals).count());
    assertEquals(List.of("code"), texts(after.path("active").get(0).path("kinds"))); assertEquals(180, after.path("active").get(0).path("durationSeconds").asInt());
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
    read(token, post("/api/board/tests/{id}/finish", first).contentType(MediaType.APPLICATION_JSON).content("{\"code\":\"RIGHT\"}"));
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

  /**
   * A test of all three kinds can start: the recent topic has a code task, the older one a fix task (difficulty 2, the
   * bug «b равно 3») and a parsons task with an extra line (difficulty 3, so that fix does not take it).
   */
  private void simpleBank(long user, String prefix) {
    String topic = skill(prefix, 2), old = skill(prefix + "_OLD", 2);
    passed(user, old, START.minus(Duration.ofDays(30))); passed(user, topic, START.minus(Duration.ofDays(1)));
    codeTask(topic, 1, "CURATED", "curated:" + prefix.toLowerCase() + ":1");
    fixTask(old, 2, "curated:" + prefix.toLowerCase() + "-fix:1", Map.of("b равно 3", "int a = 1;\nint b = 3;\nint c = 3;\nprint(a + b + c);\n"));
    parsonsTask(old, 3, "curated:" + prefix.toLowerCase() + "-parsons:1", true);
  }
  private JsonNode call(String admin, long user) throws Exception { return call(admin, user, null); }
  private JsonNode call(String admin, long user, List<String> kinds) throws Exception {
    var body = new LinkedHashMap<String, Object>(Map.of("userId", user, "language", "JAVA")); if (kinds != null) body.put("kinds", kinds);
    return read(admin, post("/api/admin/board/call").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(body)));
  }
  private JsonNode startTest(String admin, String token, long user) throws Exception { return startTest(admin, token, user, null); }
  private JsonNode startTest(String admin, String token, long user, List<String> kinds) throws Exception {
    return read(token, post("/api/board/tests/{id}/start", call(admin, user, kinds).path("id").asLong()));
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
  /** A parsons item's line ids by their text. */
  private static Map<String, String> idsOf(JsonNode item) { var ids = new HashMap<String, String>(); for (var l : item.path("lines")) ids.put(l.path("text").asText(), l.path("id").asText()); return ids; }
  private static List<String> texts(JsonNode array) { var list = new ArrayList<String>(); for (var n : array) list.add(n.asText()); return list; }
  private static Map<String, Object> result(String kind, boolean passed) { return Map.of("kind", kind, "passed", passed); }

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
  /** A task without a reference: only for the code item. */
  private long codeTask(String skill, int difficulty, String source, String key) {
    long id = task(skill, difficulty, source, key, "{\"kind\":\"OUTPUT_TEXT\",\"expectedOutput\":\"ok\\n\"}", null);
    db.update("update tasks set starter_code=?,title=? where id=?", "starter " + id, "Задача " + id, id);
    return id;
  }
  /** A task of the parsons shape; extra: a wrong solution replacing one line of the block (else one changing three lines — no extra line, no fix item). */
  private long parsonsTask(String skill, int difficulty, String key, boolean extra) {
    long id = codeTask(skill, difficulty, "CURATED", key);
    String wrong = extra ? PARSONS_REFERENCE.replace(BLOCK.get(1), EXTRA) : PARSONS_REFERENCE.replace(BLOCK.get(0), "        int x = 0;").replace(BLOCK.get(2), "        System.out.println(x);").replace(BLOCK.get(3), "        System.out.println();");
    db.update("update tasks set starter_code=?,reference_code=?,wrong_json=? where id=?", PARSONS_STARTER, PARSONS_REFERENCE, wrongJson(Map.of("ошибка", wrong)), id);
    return id;
  }
  /** A task with FIX_REFERENCE and the given wrong solutions (description → program). */
  private long fixTask(String skill, int difficulty, String key, Map<String, String> wrong) {
    long id = codeTask(skill, difficulty, "CURATED", key);
    db.update("update tasks set reference_code=?,wrong_json=? where id=?", FIX_REFERENCE, wrongJson(wrong), id);
    return id;
  }
  private String wrongJson(Map<String, String> wrong) {
    var list = new ArrayList<Map<String, String>>(); for (var e : new TreeMap<>(wrong).entrySet()) list.add(Map.of("description", e.getKey(), "source", e.getValue()));
    try { return json.writeValueAsString(list); } catch (Exception e) { throw new IllegalStateException(e); }
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
