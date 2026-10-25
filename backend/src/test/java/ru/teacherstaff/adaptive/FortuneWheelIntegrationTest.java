package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.JsonNode;
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
import org.springframework.test.web.servlet.ResultMatcher;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import java.nio.file.Path;
import java.time.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * «Жребий» of a saved pair: who gets on the wheel (a grade at the board, the top share by points of those not called,
 * ties at the border, a minimum of points; everyone of the group, in the session or not), the settings, runs of steps in
 * both modes, an absent winner's replacement, deleting a run, validation.
 */
@SpringBootTest
@AutoConfigureMockMvc
class FortuneWheelIntegrationTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json;
  @MockBean PistonCodeRunner runner;
  @MockBean LlmTutor tutor;
  @MockBean LearningContentGenerator generator;
  @MockBean Clock clock;
  static final Instant NOW = Instant.parse("2040-01-01T12:00:00Z");

  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:wheel-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
    p.add("app.task-audit.enabled", () -> "false");
    p.add("app.lesson.idle-close.enabled", () -> "false");
    p.add("app.board.auto-finish.enabled", () -> "false"); // the mocked clock is not stubbed between tests
  }
  @BeforeEach void prepare() {
    db.update("update users set password_hash=? where login='admin'", new BCryptPasswordEncoder().encode("admin-pass"));
    when(runner.configured()).thenReturn(true);
    when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true, "READY", "17.0.1"));
    when(tutor.status(anyLong())).thenReturn(new LlmStatus(false, false, false, "DISABLED", "gpt-6-luna"));
    when(clock.instant()).thenReturn(NOW);
    when(clock.getZone()).thenReturn(ZoneOffset.UTC);
    db.update("delete from app_settings where key=?", DrawSettings.KEY);
  }

  @Test void theTopRule() {
    assertEquals(0, FortuneWheel.topCount(0, 20)); assertEquals(1, FortuneWheel.topCount(1, 20)); assertEquals(1, FortuneWheel.topCount(5, 20));
    assertEquals(2, FortuneWheel.topCount(6, 20)); assertEquals(2, FortuneWheel.topCount(10, 20)); assertEquals(3, FortuneWheel.topCount(11, 20));
    assertEquals(3, FortuneWheel.topCount(10, 30), "no rounding up of 3.0000000004"); assertEquals(0, FortuneWheel.topCount(10, 0)); assertEquals(10, FortuneWheel.topCount(10, 100));
    assertNull(FortuneWheel.threshold(List.of(), 20, 1));
    assertEquals(9, FortuneWheel.threshold(List.of(3, 10, 9, 0, 9, 5, 0, 1), 20, 1), "8 → top 2: 10 and 9, the other 9 ties");
    assertEquals(1, FortuneWheel.threshold(List.of(0, 0, 0), 20, 1), "nobody with a point makes the top");
    assertEquals(0, FortuneWheel.threshold(List.of(0, 0, 0), 20, 0), "with no minimum everybody ties at 0");
    assertEquals(5, FortuneWheel.threshold(List.of(3, 10, 9, 0, 9, 5, 0, 1), 50, 1));
  }

  @Test void whoIsOnTheWheel() throws Exception {
    String admin = login("admin", "admin-pass");
    Instant start = Instant.parse("2041-02-05T08:00:00Z");
    long outsider = studentRow("w-out", "Вне сессии", "WH-1"); earn(outsider, "JAVA", start, 10);
    db.update("update users set session_participant=0 where id=?", outsider);
    long nine = studentRow("w-9a", "Девять А", "WH-1"); earn(nine, "JAVA", start, 9);
    long tie = studentRow("w-9b", "Девять Б", "WH-1"); earn(tie, "JAVA", start, 9);
    long five = studentRow("w-5", "Пять", "WH-1"); earn(five, "JAVA", start, 5);
    long three = studentRow("w-3", "Три", "WH-1"); earn(three, "JAVA", start, 3);
    long zero = studentRow("w-0", "Ноль", "WH-1"); earn(zero, "JAVA", start, 0);
    long cancelled = studentRow("w-cancel", "Отменённый", "WH-1"); earn(cancelled, "JAVA", start, 1);
    board(cancelled, "CANCELLED", at(start, 20), null);
    studentRow("w-absent", "Не пришёл", "WH-1");
    long boardFive = studentRow("w-b5", "Пятёрка у доски", "WH-1"); earn(boardFive, "JAVA", start, 1); board(boardFive, "FINISHED", at(start, 30), "5");
    long boardFour = studentRow("w-b4", "Четвёрка у доски", "WH-1"); earn(boardFour, "JAVA", start, 30); board(boardFour, "FINISHED", at(start, 40), "4");
    long twice = studentRow("w-b45", "Дважды у доски", "WH-1"); board(twice, "FINISHED", at(start, 41), "5"); board(twice, "FINISHED", at(start, 50), "3");
    long early = studentRow("w-early", "Пятёрка вчера", "WH-1"); earn(early, "JAVA", start, 2); board(early, "FINISHED", start.minus(Duration.ofDays(1)), "5");
    long other = studentRow("w-other", "Чужой", "WH-2"); earn(other, "JAVA", start, 50);

    long id = save(admin, "WH-1", "JAVA", start);
    var wheel = read(admin, get("/api/admin/pairs/{id}/wheel", id));
    // Pool (attended, not called): 10, 9, 9, 5, 3, 0, 1 (the cancelled call), 2 (yesterday's 5) → 8 → the top 2 and the tie.
    assertEquals(8, wheel.path("pool").asInt()); assertEquals(2, wheel.path("topCount").asInt()); assertEquals(9, wheel.path("threshold").asInt());
    assertEquals(List.of("w-out", "w-9a", "w-9b", "w-b45", "w-b5"), wheel.path("candidates").findValuesAsText("login"), "the top by name, then the grades at the board");
    assertEquals(List.of("TOP", "TOP", "TOP", "BOARD", "BOARD"), wheel.path("candidates").findValuesAsText("reason"));
    assertEquals("5", wheel.path("candidates").get(3).path("grade").asText(), "the best grade of the pair counts");
    assertEquals(List.of("w-b4"), wheel.path("called").findValuesAsText("login"));
    assertEquals(Set.of("w-5", "w-3", "w-0", "w-cancel", "w-absent", "w-early"), new HashSet<>(wheel.path("others").findValuesAsText("login")));
    assertTrue(wheel.path("runs").isEmpty()); assertEquals("Шоколадка", wheel.path("prize").asText()); assertEquals("ARROW", wheel.path("settings").path("mode").asText());

    // Settings: a 4 at the board is enough, the top half, no minimum of points.
    settings(admin, Map.of("boardMinGrade", 4, "topPercent", 50, "minPoints", 0));
    wheel = read(admin, get("/api/admin/pairs/{id}/wheel", id));
    assertEquals(4, wheel.path("topCount").asInt()); assertEquals(5, wheel.path("threshold").asInt());
    assertEquals(List.of("w-out", "w-9a", "w-9b", "w-5", "w-b45", "w-b5", "w-b4"), wheel.path("candidates").findValuesAsText("login"));

    expect(admin, get("/api/admin/pairs/{id}/wheel", 987_654), status().isNotFound(), "PAIR_NOT_FOUND");
    String student = createStudent("w-student", "Студент", "WH-3");
    expect(student, get("/api/admin/pairs/{id}/wheel", id), status().isBadRequest(), "FORBIDDEN");
    expect(student, get("/api/admin/draw/settings"), status().isBadRequest(), "FORBIDDEN");
    expect(student, post("/api/admin/pairs/{id}/wheel/runs", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userIds", List.of(nine)))), status().isBadRequest(), "FORBIDDEN");
  }

  @Test void settingsHaveDefaultsAndNoLimits() throws Exception {
    String admin = login("admin", "admin-pass");
    var s = read(admin, get("/api/admin/draw/settings"));
    assertEquals(6.5, s.path("spinSeconds").asDouble()); assertEquals("ARROW", s.path("mode").asText()); assertEquals(2.0, s.path("eliminationSeconds").asDouble());
    assertEquals(1, s.path("winners").asInt()); assertFalse(s.path("autoNext").asBoolean()); assertEquals(20.0, s.path("topPercent").asDouble());
    assertEquals(1, s.path("minPoints").asInt()); assertEquals(5, s.path("boardMinGrade").asInt()); assertEquals("Шоколадка", s.path("defaultPrize").asText());
    assertTrue(s.path("surprisePrize").asBoolean()); assertTrue(s.path("sound").asBoolean()); assertEquals(70, s.path("volume").asInt());
    assertEquals(6.5, s.path("defaults").path("spinSeconds").asDouble());

    var saved = settings(admin, Map.of("spinSeconds", 600, "eliminationSeconds", 0.3, "winners", 40, "mode", "ELIMINATION", "autoNext", true, "defaultPrize", "  Кофе  ", "unknown", 1));
    assertEquals(600.0, saved.path("spinSeconds").asDouble()); assertEquals(0.3, saved.path("eliminationSeconds").asDouble()); assertEquals(40, saved.path("winners").asInt());
    assertEquals("ELIMINATION", saved.path("mode").asText()); assertTrue(saved.path("autoNext").asBoolean()); assertEquals("Кофе", saved.path("defaultPrize").asText());
    assertFalse(saved.has("unknown"));
    assertEquals(600.0, read(admin, get("/api/admin/draw/settings")).path("spinSeconds").asDouble(), "kept");
    assertEquals("Шоколадка", settings(admin, Map.of("defaultPrize", " ")).path("defaultPrize").asText(), "an empty prize is the chocolate");

    for (var bad : List.<Map<String, Object>>of(Map.of("spinSeconds", -1), Map.of("winners", 0), Map.of("winners", 1.5), Map.of("mode", "SLOT"), Map.of("topPercent", 101),
        Map.of("boardMinGrade", 6), Map.of("volume", 120), Map.of("sound", "да"), Map.of("spinSeconds", "fast")))
      expect(admin, put("/api/admin/draw/settings").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(bad)), status().isBadRequest(), "INVALID_DRAW_SETTINGS");
    assertEquals(600.0, read(admin, get("/api/admin/draw/settings")).path("spinSeconds").asDouble(), "a refused save changes nothing");
  }

  @Test void arrowRunsPickWinnersOneByOneAndReplaceAnAbsentOne() throws Exception {
    String admin = login("admin", "admin-pass");
    Instant start = Instant.parse("2042-03-05T08:00:00Z");
    var ids = new ArrayList<Long>(); for (int i = 0; i < 5; i++) ids.add(studentRow("ar-" + i, "Стрелка " + i, "AR-1"));
    long id = save(admin, "AR-1", "JAVA", start);
    settings(admin, Map.of("winners", 2));

    var run = read(admin, post("/api/admin/pairs/{id}/wheel/runs", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userIds", ids, "prize", "  Кофе   с преподавателем ")))).path("run");
    long runId = run.path("id").asLong();
    assertEquals("ARROW", run.path("mode").asText()); assertEquals(2, run.path("winners").asInt()); assertEquals("Кофе с преподавателем", run.path("prize").asText());
    assertEquals(ids, longs(run.path("wheel"))); assertFalse(run.path("finished").asBoolean());

    var first = step(admin, id, runId); long w1 = first.path("pick").path("userId").asLong();
    assertEquals("WIN", first.path("pick").path("kind").asText()); assertEquals(List.of(w1), longs(first.path("won")));
    assertFalse(longs(first.path("run").path("wheel")).contains(w1), "a winner leaves the wheel"); assertFalse(first.path("run").path("finished").asBoolean());
    var second = step(admin, id, runId); long w2 = second.path("pick").path("userId").asLong();
    assertNotEquals(w1, w2); assertTrue(second.path("run").path("finished").asBoolean()); assertEquals(3, second.path("run").path("wheel").size());
    expect(admin, post("/api/admin/pairs/{id}/wheel/runs/{run}/step", id, runId), status().isBadRequest(), "DRAW_FINISHED");

    // The first winner is not in class: one more step draws a replacement among those who have not won.
    var absent = read(admin, post("/api/admin/pairs/{id}/wheel/runs/{run}/absent", id, runId).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userId", w1)))).path("run");
    assertFalse(absent.path("finished").asBoolean()); assertEquals(3, absent.path("wheel").size());
    long w3 = step(admin, id, runId).path("pick").path("userId").asLong();
    assertFalse(List.of(w1, w2).contains(w3));
    var runs = read(admin, get("/api/admin/pairs/{id}/wheel", id)).path("runs");
    assertEquals(1, runs.size()); assertEquals(List.of(w1, w2, w3), longs(runs.get(0).path("wins").findValues("userId")));
    assertEquals(List.of(true, false, false), runs.get(0).path("wins").findValues("absent").stream().map(JsonNode::asBoolean).toList());
    expect(admin, post("/api/admin/pairs/{id}/wheel/runs/{run}/absent", id, runId).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userId", w1))), status().isBadRequest(), "INVALID_WHEEL");

    for (var bad : List.<Map<String, Object>>of(Map.of("userIds", List.of()), Map.of("userIds", List.of(ids.get(0), ids.get(0))), Map.of("userIds", List.of("ar-0")), Map.of(),
        Map.of("userIds", ids, "prize", "п".repeat(201)), Map.of("userIds", ids, "prize", 5)))
      expect(admin, post("/api/admin/pairs/{id}/wheel/runs", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(bad)), status().isBadRequest(), "INVALID_WHEEL");
    long stranger = studentRow("ar-other", "Чужой", "AR-2");
    expect(admin, post("/api/admin/pairs/{id}/wheel/runs", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userIds", List.of(stranger)))), status().isBadRequest(), "INVALID_WHEEL");
    expect(admin, post("/api/admin/pairs/{id}/wheel/runs/{run}/step", id, 987_654), status().isNotFound(), "DRAW_NOT_FOUND");

    // Deleting a run deletes its steps; deleting the pair deletes its runs.
    var deleted = read(admin, delete("/api/admin/pairs/{id}/wheel/runs/{run}", id, runId));
    assertTrue(deleted.path("runs").isEmpty()); assertEquals(0, count("select count(*) from draw_steps where run_id=?", runId));
    long again = read(admin, post("/api/admin/pairs/{id}/wheel/runs", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userIds", ids)))).path("run").path("id").asLong();
    step(admin, id, again);
    read(admin, delete("/api/admin/pairs/{id}", id));
    assertEquals(0, count("select count(*) from draw_runs where pair_id=?", id)); assertEquals(0, count("select count(*) from draw_steps where run_id=?", again));
  }

  @Test void eliminationDropsNamesUntilTheWinnersAreLeft() throws Exception {
    String admin = login("admin", "admin-pass");
    Instant start = Instant.parse("2043-04-05T08:00:00Z");
    var ids = new ArrayList<Long>(); for (int i = 0; i < 6; i++) ids.add(studentRow("el-" + i, "Выбывание " + i, "EL-1"));
    long id = save(admin, "EL-1", "JAVA", start);
    settings(admin, Map.of("mode", "ELIMINATION", "winners", 2, "defaultPrize", "Кофе"));
    var run = read(admin, post("/api/admin/pairs/{id}/wheel/runs", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userIds", ids)))).path("run");
    long runId = run.path("id").asLong(); assertEquals("Кофе", run.path("prize").asText(), "the default prize of the settings");
    var outs = new ArrayList<Long>();
    for (int k = 0; k < 3; k++) {
      var s = step(admin, id, runId);
      assertEquals("OUT", s.path("pick").path("kind").asText()); assertTrue(s.path("won").isEmpty()); outs.add(s.path("pick").path("userId").asLong());
      assertEquals(5 - k, s.path("run").path("wheel").size()); assertFalse(s.path("run").path("finished").asBoolean());
    }
    var last = step(admin, id, runId); outs.add(last.path("pick").path("userId").asLong());
    assertEquals("OUT", last.path("pick").path("kind").asText()); assertEquals(2, last.path("won").size(), "the two left win with the decisive drop-out");
    assertTrue(last.path("run").path("finished").asBoolean()); assertEquals(outs, longs(last.path("run").path("outs")));
    var winners = longs(last.path("won")); assertTrue(Collections.disjoint(winners, outs));

    // A winner is absent: every name that has not won is back on the wheel and the next step picks a winner.
    var absent = read(admin, post("/api/admin/pairs/{id}/wheel/runs/{run}/absent", id, runId).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userId", winners.get(0))))).path("run");
    assertTrue(absent.path("replacing").asBoolean()); assertEquals(new HashSet<>(outs), new HashSet<>(longs(absent.path("wheel"))));
    var replacement = step(admin, id, runId);
    assertEquals("WIN", replacement.path("pick").path("kind").asText()); assertTrue(outs.contains(replacement.path("pick").path("userId").asLong()));
    assertTrue(replacement.path("run").path("finished").asBoolean());

    // Fewer names than winners: the first step makes them all winners without a drop-out.
    var small = read(admin, post("/api/admin/pairs/{id}/wheel/runs", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userIds", ids.subList(0, 2))))).path("run").path("id").asLong();
    var all = step(admin, id, small);
    assertTrue(all.path("pick").isNull()); assertEquals(2, all.path("won").size()); assertTrue(all.path("run").path("finished").asBoolean());
  }

  private JsonNode settings(String admin, Map<String, Object> values) throws Exception {
    return read(admin, put("/api/admin/draw/settings").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(values)));
  }
  private JsonNode step(String admin, long pair, long run) throws Exception { return read(admin, post("/api/admin/pairs/{id}/wheel/runs/{run}/step", pair, run)); }
  private static List<Long> longs(JsonNode array) { var list = new ArrayList<Long>(); array.forEach(n -> list.add(n.asLong())); return list; }
  private static List<Long> longs(List<JsonNode> nodes) { return nodes.stream().map(JsonNode::asLong).toList(); }

  private void board(long user, String status, Instant calledAt, String grade) {
    db.update("insert into board_tests(user_id,group_name,language,status,called_at,call_expires_at,final_grade) values(?,'WH-1','JAVA',?,?,?,?)",
        user, status, calledAt.toString(), calledAt.plusSeconds(300).toString(), grade);
  }

  // ---------------------------------------------------------------- helpers

  private static Instant at(Instant start, int minutes) { return start.plus(Duration.ofMinutes(minutes)); }
  /** A regular student's points in a window starting at `start`: tasks of difficulty 3 and 1, passed and credited 10 minutes in. */
  private void earn(long user, String language, Instant start, int points) {
    long lesson = lesson(user, language, start.minusSeconds(1800));
    for (int left = points; left > 0; ) {
      int d = left >= 3 ? 3 : 1; long t = task(language, d, false);
      submit(lesson, t, true, at(start, 10)); credit(user, t); left -= d;
    }
    if (points == 0) submit(lesson, task(language, 1, false), false, at(start, 10));
  }
  /** Saved results of another group, straight into the tables: one pair with a row per value. */
  private void history(String language, Instant start, int[] points, boolean attended, boolean hard) {
    long pair = db.queryForObject("insert into pairs(group_name,language,starts_at,ends_at,median,median_source) values('Архив',?,?,?,null,'NONE') returning id", Long.class,
        language, start.toString(), start.plusSeconds(5400).toString());
    for (int p : points) {
      long user = studentRow("hist-" + UUID.randomUUID(), "История", "Архив");
      db.update("insert into pair_results(pair_id,user_id,attended,points,tasks_json,hard) values(?,?,?,?,'{}',?)", pair, user, attended ? 1 : 0, p, hard ? 1 : 0);
    }
  }
  private long save(String admin, String group, String language, Instant start) throws Exception {
    return read(admin, post("/api/admin/pairs").contentType(MediaType.APPLICATION_JSON).content(body(group, language, start.toString(), start.plusSeconds(5400).toString()))).path("id").asLong();
  }
  private String body(String group, String language, String startsAt, String endsAt) throws Exception {
    return json.writeValueAsString(Map.of("group", group, "language", language, "startsAt", startsAt, "endsAt", endsAt));
  }
  private long task(String language, Integer difficulty, boolean hard) {
    String skill = db.queryForObject("select code from skills where language=? order by sort_order,id limit 1", String.class, language);
    long id = db.queryForObject("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,difficulty,mode) values(?,?,?,'','class TestHarness {}','TestHarness.java',?,?,?) returning id",
        Long.class, skill, "task " + UUID.randomUUID(), "statement", language, difficulty, hard ? "HARD" : "NORMAL");
    db.update("insert into task_target_skills(task_id,skill_code) values(?,?)", id, skill);
    return id;
  }
  private long lesson(long user, String language, Instant started) {
    return db.queryForObject("insert into lessons(user_id,lesson_number,language,language_lesson_number,started_at,finished_at,last_activity_at) values(?,(select coalesce(max(lesson_number),0)+1 from lessons where user_id=?),?,1,?,?,?) returning id",
        Long.class, user, user, language, sql(started), sql(started.plusSeconds(7200)), sql(started));
  }
  private void submit(long lesson, long task, boolean passed, Instant at) {
    db.update("insert into submissions(lesson_id,task_id,source_code,passed,runner_output,created_at) values(?,?,'code',?,?,?)", lesson, task, passed ? 1 : 0, passed ? "ok" : "fail", sql(at));
  }
  private void credit(long user, long task) { db.update("insert into successful_task_credit(user_id,task_id) values(?,?)", user, task); }
  /** SQLite CURRENT_TIMESTAMP format, as the tables store it by default. */
  private static String sql(Instant at) { return at.toString().replace('T', ' ').substring(0, 19); }
  private long studentRow(String login, String name, String group) {
    return db.queryForObject("insert into users(login,password_hash,role,display_name,group_name) values(?,'-','STUDENT',?,?) returning id", Long.class, login, name, group);
  }
  private int count(String sql, Object... params) { return db.queryForObject(sql, Integer.class, params); }
  private static JsonNode row(JsonNode pair, String login) { for (var r : pair.path("rows")) if (login.equals(r.path("login").asText())) return r; throw new AssertionError("no row " + login); }
  private static List<String> logins(JsonNode pair) { return pair.path("rows").findValuesAsText("login"); }
  private static Set<String> fields(JsonNode node) { var names = new HashSet<String>(); node.fieldNames().forEachRemaining(names::add); return names; }

  private JsonNode read(String token, MockHttpServletRequestBuilder request) throws Exception {
    return json.readTree(mvc.perform(request.cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
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
