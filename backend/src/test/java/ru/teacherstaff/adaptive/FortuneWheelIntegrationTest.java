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
 * «Колесо фортуны» of a saved pair: who gets on the wheel (a 5 at the board, the top 20% by points of those not called,
 * ties at the border, at least a point; everyone of the group, in the session or not), the spin and its validation.
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
  }

  @Test void theTopRule() {
    assertEquals(0, FortuneWheel.topCount(0)); assertEquals(1, FortuneWheel.topCount(1)); assertEquals(1, FortuneWheel.topCount(5));
    assertEquals(2, FortuneWheel.topCount(6)); assertEquals(2, FortuneWheel.topCount(10)); assertEquals(3, FortuneWheel.topCount(11));
    assertNull(FortuneWheel.threshold(List.of()));
    assertEquals(9, FortuneWheel.threshold(List.of(3, 10, 9, 0, 9, 5, 0, 1)), "8 → top 2: 10 and 9, the other 9 ties");
    assertEquals(1, FortuneWheel.threshold(List.of(0, 0, 0)), "nobody with a point makes the top");
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
    long absent = studentRow("w-absent", "Не пришёл", "WH-1");
    long boardFive = studentRow("w-b5", "Пятёрка у доски", "WH-1"); earn(boardFive, "JAVA", start, 1); board(boardFive, "FINISHED", at(start, 30), "5");
    long boardFour = studentRow("w-b4", "Четвёрка у доски", "WH-1"); earn(boardFour, "JAVA", start, 30); board(boardFour, "FINISHED", at(start, 40), "4");
    long early = studentRow("w-early", "Пятёрка вчера", "WH-1"); earn(early, "JAVA", start, 2); board(early, "FINISHED", start.minus(Duration.ofDays(1)), "5");
    long other = studentRow("w-other", "Чужой", "WH-2"); earn(other, "JAVA", start, 50);

    long id = save(admin, "WH-1", "JAVA", start);
    var wheel = read(admin, get("/api/admin/pairs/{id}/wheel", id));
    // Pool (attended, not called): 10, 9, 9, 5, 3, 0, 1 (the cancelled call), 2 (yesterday's 5) → 8 → the top 2 and the tie.
    assertEquals(8, wheel.path("pool").asInt()); assertEquals(2, wheel.path("topCount").asInt()); assertEquals(9, wheel.path("threshold").asInt());
    assertEquals(List.of("w-out", "w-9a", "w-9b", "w-b5"), wheel.path("candidates").findValuesAsText("login"), "the top by name, then the 5s at the board");
    assertEquals(List.of("TOP", "TOP", "TOP", "BOARD"), wheel.path("candidates").findValuesAsText("reason"));
    assertEquals(List.of("w-b4"), wheel.path("called").findValuesAsText("login"));
    assertEquals(Set.of("w-5", "w-3", "w-0", "w-cancel", "w-absent", "w-early"), new HashSet<>(wheel.path("others").findValuesAsText("login")));
    assertTrue(wheel.path("spins").isEmpty()); assertEquals("Шоколадка", wheel.path("prize").asText(), "the default before the first spin");

    var ids = List.of(nine, tie, outsider, boardFive, five);
    var spin = read(admin, post("/api/admin/pairs/{id}/wheel/spin", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userIds", ids))));
    long winner = spin.path("winner").path("userId").asLong();
    assertEquals(ids.get(spin.path("index").asInt()), winner);
    assertEquals(1, spin.path("spins").size()); assertEquals(winner, spin.path("spins").get(0).path("userId").asLong()); assertEquals(5, spin.path("spins").get(0).path("names").asInt());
    assertEquals("Шоколадка", spin.path("prize").asText()); assertEquals("Шоколадка", spin.path("spins").get(0).path("prize").asText());
    assertEquals(1, read(admin, get("/api/admin/pairs/{id}/wheel", id)).path("spins").size());
    // A named prize is kept with the spin and offered again next time.
    var named = read(admin, post("/api/admin/pairs/{id}/wheel/spin", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("userIds", ids, "prize", "  Пятёрка   автоматом "))));
    assertEquals("Пятёрка автоматом", named.path("prize").asText()); assertEquals(List.of("Шоколадка", "Пятёрка автоматом"), named.path("spins").findValuesAsText("prize"));
    assertEquals("Пятёрка автоматом", read(admin, get("/api/admin/pairs/{id}/wheel", id)).path("prize").asText());

    for (var bad : List.of(Map.of("userIds", List.of()), Map.of("userIds", List.of(nine, nine)), Map.of("userIds", List.of(nine, other)), Map.of("userIds", List.of("w-9a")), Map.of(), Map.of("userIds", ids, "prize", "п".repeat(61)), Map.of("userIds", ids, "prize", 5)))
      expect(admin, post("/api/admin/pairs/{id}/wheel/spin", id).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(bad)), status().isBadRequest(), "INVALID_WHEEL");
    expect(admin, get("/api/admin/pairs/{id}/wheel", 987_654), status().isNotFound(), "PAIR_NOT_FOUND");
    String student = createStudent("w-student", "Студент", "WH-3");
    expect(student, get("/api/admin/pairs/{id}/wheel", id), status().isBadRequest(), "FORBIDDEN");

    read(admin, delete("/api/admin/pairs/{id}", id));
    assertEquals(0, count("select count(*) from wheel_spins where pair_id=?", id), "the spins go with the pair");
  }

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
