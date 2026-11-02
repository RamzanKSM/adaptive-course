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
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import java.nio.file.Path;
import java.time.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicReference;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * «Эстафета»: every task's steps pass one by one on the reference snapshots (and not before), the normalization, and a
 * relay of three students — joining, the queue, a step done by the writer, a pass and a timeout dropping the streak,
 * an absent student passed over, the teacher's credit / skip / pause / finish, the final run, and who may write; what
 * the board station shows: the relay only when the teacher put it on the board, and never instead of a call.
 */
@SpringBootTest
@AutoConfigureMockMvc
class CodeRelayIntegrationTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json; @Autowired CodeRelay relay;
  @MockBean PistonCodeRunner runner;
  @MockBean LlmTutor tutor;
  @MockBean LearningContentGenerator generator;
  @MockBean Clock clock;
  final AtomicReference<Instant> now = new AtomicReference<>(Instant.parse("2040-01-01T12:00:00Z"));

  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:relay-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
    p.add("app.task-audit.enabled", () -> "false");
    p.add("app.lesson.idle-close.enabled", () -> "false");
    p.add("app.board.auto-finish.enabled", () -> "false");
  }
  @BeforeEach void prepare() {
    db.update("update users set password_hash=? where login='admin'", new BCryptPasswordEncoder().encode("admin-pass"));
    when(runner.configured()).thenReturn(true);
    when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true, "READY", "17.0.1"));
    when(tutor.status(anyLong())).thenReturn(new LlmStatus(false, false, false, "DISABLED", "gpt-6-luna"));
    when(clock.instant()).thenAnswer(i -> now.get());
    when(clock.getZone()).thenReturn(ZoneOffset.UTC);
  }

  @Test void everyStepPassesOnItsSnapshotOnly() {
    assertEquals(6, relay.tasks().size());
    for (var task : relay.tasks()) {
      assertEquals(0, CodeRelay.doneSteps(task, task.starter(), Set.of()), task.key() + ": the starter does no step");
      for (int k = 0; k < task.steps().size(); k++)
        assertEquals(k + 1, CodeRelay.doneSteps(task, task.steps().get(k).code(), Set.of()), task.key() + " step " + (k + 1) + "\n" + CodeRelay.normalize(task.steps().get(k).code(), task.language()));
    }
  }

  @Test void normalization() {
    assertEquals("int sum=0;for(int i=1;i<=n;i++){sum+=i;}System.out.println(\"Sum:  \"+sum);",
        CodeRelay.normalize("int  sum = 0 ;\nfor (int i = 1; i <= n; i++) {\n  sum += i; // add\n}\nSystem.out.println(\"Sum:  \" + sum);\n", Language.JAVA));
    assertEquals("for i in range(3):\n>if i%2==0:\n>>print(\"a # b\",i)\nprint(\"end\")",
        CodeRelay.normalize("for i in range(3):\n\n    if i % 2 == 0:  # even\n        print(\"a # b\", i)\nprint(\"end\")\n", Language.PYTHON));
    var evens = relay.task("java-evens");
    String alternative = "public class Solution {\n  public static void main(String[] args) {\n    int n = 10;\n    int evens = 0;\n    int oddSum = 0;\n"
        + "    for (int i = 1; i < n + 1; i += 1) {\n      if (i % 2 == 0) {\n        evens = evens + 1;\n      } else {\n        oddSum = oddSum + i;\n      }\n    }\n  }\n}\n";
    assertEquals(7, CodeRelay.doneSteps(evens, alternative, Set.of()), "equivalent forms count");
    assertEquals(0, CodeRelay.doneSteps(evens, alternative.replace("int evens = 0;", "int evens = 1;"), Set.of()), "a later step does not count before an earlier one");
    assertEquals(7, CodeRelay.doneSteps(evens, alternative.replace("int evens = 0;", "int evens = 1;"), Set.of(0)), "a credited step counts");
  }

  @Test void aRelayOfThree() throws Exception {
    String admin = login("admin", "admin-pass");
    var tokens = new LinkedHashMap<String, String>();
    for (String name : List.of("r1", "r2", "r3")) tokens.put(name, createStudent(name, "Студент " + name, "RL-1"));
    String outsider = createStudent("r-out", "Чужой", "RL-2");

    var created = read(admin, post("/api/admin/relay").contentType(MediaType.APPLICATION_JSON).content("{\"group\":\"RL-1\",\"taskKey\":\"java-evens\",\"turnSeconds\":25}"));
    long id = created.path("id").asLong();
    assertEquals("LOBBY", created.path("status").asText());
    expect(admin, post("/api/admin/relay").contentType(MediaType.APPLICATION_JSON).content("{\"group\":\"RL-1\",\"taskKey\":\"java-max\"}"), "RELAY_ALREADY_ACTIVE");
    assertTrue(read(outsider, get("/api/relay/me")).path("relay").isNull(), "another group sees nothing");
    expect(outsider, post("/api/relay/" + id + "/join"), "RELAY_NOT_YOURS");
    assertTrue(read(tokens.get("r1"), get("/api/relay/me")).path("relay").path("me").path("member").asBoolean() == false);
    for (String t : tokens.values()) assertTrue(read(t, post("/api/relay/" + id + "/join")).path("me").path("member").asBoolean());
    assertEquals("ADMIN", read(admin, get("/api/relay/me")).path("role").asText());

    var started = read(admin, post("/api/admin/relay/" + id + "/start"));
    assertEquals("RUNNING", started.path("status").asText());
    assertEquals(1, started.path("turn").asInt());
    assertEquals(2, started.path("queue").size());
    assertTrue(started.path("hint").asText().contains("int evens = 0;"), "the teacher sees the reference");
    var order = new ArrayList<String>(); order.add(loginOf(started.path("writer").path("userId").asLong()));
    for (var q : started.path("queue")) order.add(loginOf(q.path("userId").asLong()));

    // The student view never carries the reference; others may not write.
    var view = read(tokens.get(order.get(1)), get("/api/relay/me")).path("relay");
    assertFalse(view.has("hint") || view.has("reference"));
    assertEquals(0, view.path("me").path("turnsAhead").asInt());
    expect(tokens.get(order.get(1)), put("/api/relay/" + id + "/code").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("turn", 1, "code", "x"))), "RELAY_NOT_YOUR_TURN");

    // The writer does step 1: the pen goes to the next at once, the streak grows.
    var task = relay.task("java-evens");
    String code = task.starter().replace("int n = 10;\n", "int n = 10;\n        int evens = 0\n");
    var partial = write(tokens.get(order.get(0)), id, 1, code);
    assertEquals(1, partial.path("turn").asInt(), "not yet: no semicolon");
    var done = write(tokens.get(order.get(0)), id, 1, code.replace("int evens = 0\n", "int evens = 0;\n"));
    assertEquals(1, done.path("step").asInt()); assertEquals(2, done.path("turn").asInt()); assertEquals(1, done.path("streak").asInt());
    assertEquals(loginOf(done.path("writer").path("userId").asLong()), order.get(1));
    assertEquals("DONE", done.path("lastTurn").path("outcome").asText());

    // A pass keeps the step and drops the streak; the record stays.
    var passed = read(tokens.get(order.get(1)), post("/api/relay/" + id + "/pass").contentType(MediaType.APPLICATION_JSON).content("{\"turn\":2}"));
    assertEquals(1, passed.path("step").asInt()); assertEquals(0, passed.path("streak").asInt()); assertEquals(1, passed.path("record").asInt()); assertEquals(1, passed.path("skips").asInt());
    assertEquals(order.get(2), loginOf(passed.path("writer").path("userId").asLong()));

    // The time runs out (with the grace): a timeout, the next writer is the first again.
    advance(30, tokens.values());
    var timedOut = read(admin, get("/api/admin/relay").param("group", "RL-1")).path("relay");
    assertEquals(4, timedOut.path("turn").asInt()); assertEquals(2, timedOut.path("skips").asInt());
    assertEquals(order.get(0), loginOf(timedOut.path("writer").path("userId").asLong()));

    // A student who stopped polling is passed over without a skip.
    advance(15, List.of(tokens.get(order.get(0)), tokens.get(order.get(2))));
    String twoSteps = task.steps().get(1).code();
    var skippedAbsent = write(tokens.get(order.get(0)), id, 4, twoSteps);
    assertEquals(2, skippedAbsent.path("step").asInt());
    assertEquals(order.get(2), loginOf(skippedAbsent.path("writer").path("userId").asLong()), order.get(1) + " is not here");

    // The teacher credits a step by hand, pauses, resumes, skips without a penalty.
    var credited = read(admin, post("/api/admin/relay/" + id + "/credit"));
    assertEquals(3, credited.path("step").asInt()); assertEquals(2, credited.path("streak").asInt());
    read(admin, post("/api/admin/relay/" + id + "/pause"));
    expect(tokens.get(order.get(0)), put("/api/relay/" + id + "/code").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("turn", 6, "code", "x"))), "RELAY_NOT_YOUR_TURN");
    var resumed = read(admin, post("/api/admin/relay/" + id + "/resume"));
    assertEquals("RUNNING", resumed.path("status").asText());
    var skipped = read(admin, post("/api/admin/relay/" + id + "/skip"));
    assertEquals(2, skipped.path("streak").asInt(), "the teacher's skip is no penalty");

    // The rest of the steps by whoever writes: SOLVED and the final run.
    when(runner.console(eq(Language.JAVA), anyString())).thenReturn(new PistonCodeRunner.Console("OK", "Even: 5\nOdd sum: 25\n", "", false));
    JsonNode state = skipped;
    while (!state.path("status").asText().equals("SOLVED")) {
      int step = state.path("step").asInt();
      String writer = loginOf(state.path("writer").path("userId").asLong());
      for (String t : tokens.values()) read(t, get("/api/relay/me"));
      state = write(tokens.get(writer), id, state.path("turn").asInt(), task.steps().get(step).code());
    }
    assertEquals(9, state.path("step").asInt());
    for (int i = 0; i < 50 && !read(admin, get("/api/admin/relay").param("id", String.valueOf(id))).path("relay").path("run").path("status").asText().equals("OK"); i++) Thread.sleep(50);
    var solved = read(admin, get("/api/admin/relay").param("id", String.valueOf(id))).path("relay");
    assertTrue(solved.path("run").path("matches").asBoolean(), solved.path("run").toString());
    assertEquals(3, solved.path("people").size());
    assertTrue(solved.path("log").size() >= 8);

    var finished = read(admin, post("/api/admin/relay/" + id + "/finish"));
    assertEquals("FINISHED", finished.path("status").asText());
    assertTrue(read(tokens.get("r1"), get("/api/relay/me")).path("relay").isNull());
    assertTrue(read(admin, get("/api/admin/relay").param("group", "RL-1")).path("relay").isNull());
  }

  @Test void theBoardShowsTheRelayOnlyByTheTeachersChoiceAndNeverOverACall() throws Exception {
    String admin = login("admin", "admin-pass"), student = createStudent("b1", "Студент b1", "RL-B");
    createStudent("b2", "Студент b2", "RL-C");
    long user = db.queryForObject("select id from users where login='b1'", Long.class);
    String station = mvc.perform(post("/api/admin/board/stations").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{}")).andExpect(status().isOk())
        .andReturn().getResponse().getCookie("adaptive_station").getValue();
    long id = read(admin, post("/api/admin/relay").contentType(MediaType.APPLICATION_JSON).content("{\"group\":\"RL-B\",\"taskKey\":\"java-evens\"}")).path("id").asLong();
    read(student, post("/api/relay/" + id + "/join"));
    read(admin, post("/api/admin/relay/" + id + "/start"));
    assertTrue(station(station).path("relay").isNull(), "a running relay stays off the board until the teacher puts it there");

    assertTrue(read(admin, post("/api/admin/relay/" + id + "/board")).path("onBoard").asBoolean());
    var shown = station(station).path("relay");
    assertEquals(id, shown.path("id").asLong());
    assertFalse(shown.has("hint") || shown.has("reference") || shown.has("people"), "only what everybody may see");

    // A call takes the screen at once; the relay comes back when nobody is called.
    long call = read(admin, post("/api/admin/board/call").contentType(MediaType.APPLICATION_JSON).content("{\"userId\":" + user + ",\"language\":\"JAVA\"}")).path("id").asLong();
    var called = station(station);
    assertTrue(called.path("relay").isNull());
    assertEquals(call, called.path("calls").get(0).path("id").asLong());
    read(admin, post("/api/admin/board/tests/{id}/cancel", call));
    assertEquals(id, station(station).path("relay").path("id").asLong());

    // One relay on the board: another one replaces it; taken off and finished relays are gone from it.
    long other = read(admin, post("/api/admin/relay").contentType(MediaType.APPLICATION_JSON).content("{\"group\":\"RL-C\",\"taskKey\":\"java-max\"}")).path("id").asLong();
    read(admin, post("/api/admin/relay/" + other + "/board"));
    assertEquals(other, station(station).path("relay").path("id").asLong(), "a relay in the lobby can be shown too");
    assertFalse(read(admin, get("/api/admin/relay").param("id", String.valueOf(id))).path("relay").path("onBoard").asBoolean());
    assertFalse(read(admin, post("/api/admin/relay/" + other + "/unboard")).path("onBoard").asBoolean());
    assertTrue(station(station).path("relay").isNull());
    read(admin, post("/api/admin/relay/" + id + "/board"));
    read(admin, post("/api/admin/relay/" + id + "/finish"));
    assertTrue(station(station).path("relay").isNull());
    expect(admin, post("/api/admin/relay/" + id + "/board"), "RELAY_FINISHED");
    read(admin, post("/api/admin/relay/" + other + "/finish"));
  }

  private JsonNode station(String token) throws Exception {
    return json.readTree(mvc.perform(get("/api/station/current").cookie(new jakarta.servlet.http.Cookie("adaptive_station", token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
  }
  /** Moves the clock in steps of 5 seconds, the given students polling as their pages do. */
  private void advance(int seconds, Collection<String> polling) throws Exception {
    for (int s = 0; s < seconds; s += 5) { now.set(now.get().plusSeconds(5)); for (String t : polling) read(t, get("/api/relay/me")); }
  }
  private JsonNode write(String token, long id, int turn, String code) throws Exception {
    return read(token, put("/api/relay/" + id + "/code").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("turn", turn, "code", code))));
  }
  private String loginOf(long id) { return db.queryForObject("select login from users where id=?", String.class, id); }
  private JsonNode read(String token, MockHttpServletRequestBuilder request) throws Exception {
    return json.readTree(mvc.perform(request.cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
  }
  private void expect(String token, MockHttpServletRequestBuilder request, String error) throws Exception {
    var body = json.readTree(mvc.perform(request.cookie(cookie(token))).andReturn().getResponse().getContentAsString());
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
  private jakarta.servlet.http.Cookie cookie(String value) { return new jakarta.servlet.http.Cookie("adaptive_session", value); }
}
