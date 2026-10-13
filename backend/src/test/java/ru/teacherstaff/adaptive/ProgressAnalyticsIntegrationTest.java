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
 * Progress analytics end to end: the replayed history ends exactly where the live progress is, the forecast, flags and
 * membership follow the definitions, and the classroom screen never shows a person.
 */
@SpringBootTest
@AutoConfigureMockMvc
class ProgressAnalyticsIntegrationTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json;
  @MockBean PistonCodeRunner runner;
  @MockBean LlmTutor tutor;
  @MockBean LearningContentGenerator generator;
  @MockBean Clock clock;
  /** «Now» of the analytics: the real time unless a test fixes it. */
  private final AtomicReference<Instant> fixedNow = new AtomicReference<>();
  /** A fixed moment for tests that write their history straight into the tables: Thursday, 14 March 2030. */
  static final Instant NOW = Instant.parse("2030-03-14T12:00:00Z");
  static final LocalDate TODAY = LocalDate.of(2030, 3, 14);

  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:progress-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
    p.add("app.task-audit.enabled", () -> "false");
    p.add("app.lesson.idle-close.enabled", () -> "false"); // lessons written for 2030 must stay open
  }
  @BeforeEach void prepare() {
    db.update("update users set password_hash=? where login='admin'", new BCryptPasswordEncoder().encode("admin-pass"));
    when(runner.configured()).thenReturn(true);
    when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true, "READY", "17.0.1"));
    when(runner.run(any(Language.class), anyString(), anyString())).thenAnswer(call -> ((String) call.getArgument(1)).contains("WRONG")
        ? new PistonCodeRunner.Run(false, "Неверный вывод программы.") : new PistonCodeRunner.Run(true, "Решение прошло скрытые проверки"));
    when(tutor.status(anyLong())).thenReturn(new LlmStatus(false, false, false, "DISABLED", "gpt-6-luna"));
    when(clock.instant()).thenAnswer(call -> fixedNow.get() == null ? Instant.now() : fixedNow.get());
    when(clock.getZone()).thenReturn(ZoneOffset.UTC);
    db.update("delete from app_settings where key='session_date'");
  }

  @Test void theLastDayOfEverySeriesIsTheLiveProgress() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("flow-analytics", "Поток", "Поток-1"); long student = studentId("flow-analytics");
    submitDiagnostic(token); // block 0 right: four topics confirmed, VARIABLE_BASIC is not
    for (int i = 1; i <= 6; i++) addTask("VARIABLE_BASIC", "var " + i);
    for (int i = 1; i <= 4; i++) addTask("PRIMITIVE_TYPES", "types " + i);
    // Lesson 1: the first iteration of VARIABLE_BASIC, then a PRIMITIVE_TYPES task solved after a failed attempt.
    start(token);
    long hardTask = solve(token, "VARIABLE_BASIC", false); solve(token, "VARIABLE_BASIC", false); solve(token, "VARIABLE_BASIC", false);
    long revokedTask = solve(token, "PRIMITIVE_TYPES", true);
    long lesson1 = openLesson(student); finish(token, lesson1);
    // Lesson 2 (N+1): the second iteration, completed across lessons, and one more PRIMITIVE_TYPES task.
    start(token); solve(token, "VARIABLE_BASIC", false); solve(token, "VARIABLE_BASIC", false); solve(token, "PRIMITIVE_TYPES", false);
    finish(token, openLesson(student));
    db.update("update tasks set mode='HARD' where id=?", hardTask); // a hard task is worth 30 XP
    // The teacher cancels the first PRIMITIVE_TYPES solution: the topic is replayed, and lesson 3 starts with the task again.
    mvc.perform(post("/api/admin/students/{id}/lessons/{l}/tasks/{t}/revoke", student, lesson1, revokedTask).cookie(cookie(admin))).andExpect(status().isOk());
    start(token); assertEquals(revokedTask, solve(token, "PRIMITIVE_TYPES", false));
    // Spread the history over days: lesson 1 two days ago, the diagnostic and lesson 2 yesterday, lesson 3 today.
    long lesson2 = db.queryForObject("select id from lessons where user_id=? and language_lesson_number=2", Long.class, student);
    for (var shift : Map.of(lesson1, "-2 days", lesson2, "-1 days").entrySet()) {
      db.update("update submissions set created_at=datetime(created_at,?) where lesson_id=?", shift.getValue(), shift.getKey());
      db.update("update lessons set started_at=datetime(started_at,?),finished_at=datetime(finished_at,?),last_activity_at=datetime(last_activity_at,?) where id=?", shift.getValue(), shift.getValue(), shift.getValue(), shift.getKey());
    }
    db.update("update student_languages set diagnostic_completed_at=datetime(diagnostic_completed_at,'-1 days') where user_id=?", student);
    LocalDate today = LocalDate.now(ZoneOffset.UTC);
    setSession(admin, today.plusDays(70));

    var live = read(token, get("/api/progress"));
    var view = read(admin, get("/api/admin/progress").param("language", "JAVA"));
    var me = findStudent(view, "flow-analytics");
    var days = view.path("days"); int last = days.size() - 1;
    assertEquals(today.toString(), days.get(last).asText()); assertEquals(today.toString(), view.path("today").asText());
    for (String series : List.of("skills", "skillsWithDiagnostic", "solved", "xp", "closed")) assertEquals(days.size(), me.path("series").path(series).size(), series);
    int topics = live.path("skills").size(), closed = 0, confirmed = 0;
    double shares = 0, withDiagnostic = 0;
    assertEquals(topics, view.path("topics").size());
    for (int i = 0; i < topics; i++) {
      var skill = live.path("skills").get(i);
      double share = skillShare(skill); boolean isConfirmed = skill.path("confirmedByDiagnostic").asInt() == 1, isMastered = skill.path("mastered").asInt() == 1;
      shares += share; withDiagnostic += isConfirmed && !isMastered ? 1 : share;
      if (isConfirmed) confirmed++; else if (skill.path("completedIterations").asInt() >= 1 || isMastered) closed++;
      assertEquals(skill.path("skillCode").asText(), view.path("topics").get(i).path("code").asText());
      assertEquals(Math.round(share * 100) / 100.0, me.path("topicShare").get(i).asDouble(), 1e-9, skill.path("skillCode").asText());
      assertEquals(isConfirmed, me.path("topicConfirmed").get(i).asBoolean(), skill.path("skillCode").asText());
    }
    var series = me.path("series");
    assertEquals(Math.round(100 * shares / topics * 10) / 10.0, series.path("skills").get(last).asDouble(), 1e-9, "skills % from student_skills");
    assertEquals(Math.round(100 * withDiagnostic / topics * 10) / 10.0, series.path("skillsWithDiagnostic").get(last).asDouble(), 1e-9);
    assertEquals(db.queryForObject("select count(*) from successful_task_credit c join tasks t on t.id=c.task_id where c.user_id=? and t.language='JAVA'", Integer.class, student), series.path("solved").get(last).asInt());
    assertEquals(experience(live), series.path("xp").get(last).asInt(), "XP is the student's own «Мой прогресс»");
    // The same numbers worked out by hand: VARIABLE_BASIC 5/6, PRIMITIVE_TYPES 1/6, four topics confirmed, 7 tasks (one hard).
    assertEquals(2.3, series.path("skills").get(last).asDouble()); assertEquals(11.4, series.path("skillsWithDiagnostic").get(last).asDouble());
    assertEquals(7, series.path("solved").get(last).asInt()); assertEquals(6 * 10 + 30 + 2 * 20 + 4 * 5, series.path("xp").get(last).asInt());
    // Earlier days are replayed: two days ago only lesson 1 (the revoked task is not there), yesterday lesson 2 as well.
    assertEquals(today.minusDays(2).toString(), days.get(last - 2).asText(), "the period starts at the course's first lesson");
    assertEquals(List.of(1.1, 2.3, 2.3), doubles(series.path("skills"), last - 2));
    assertEquals(List.of(1.1, 11.4, 11.4), doubles(series.path("skillsWithDiagnostic"), last - 2), "the diagnostic counts from its own date");
    assertEquals(List.of(3.0, 6.0, 7.0), doubles(series.path("solved"), last - 2), "the re-solved task counts from today");
    assertEquals(List.of(2 * 10 + 30 + 20.0, 5 * 10 + 30 + 2 * 20 + 4 * 5.0, 150.0), doubles(series.path("xp"), last - 2));
    assertEquals(List.of(1.0, 5.0, 5.0), doubles(series.path("closed"), last - 2), "closed topics: the first iteration, then the diagnostic's four");

    assertTrue(me.path("member").asBoolean()); assertEquals("JAVA", me.path("sessionCourse").asText()); assertEquals("Поток-1", me.path("group").asText());
    assertEquals(3, me.path("lessons").asInt()); assertEquals(today.minusDays(2).toString(), me.path("firstLessonDay").asText()); assertFalse(me.path("lastActivityAt").isNull());
    var period = me.path("period");
    assertEquals(3, period.path("activeDays").asInt()); assertEquals(7, period.path("solved").asInt());
    assertEquals(6, period.path("firstTry").asInt(), "the revoked task was first submitted wrong"); assertEquals(9, period.path("submissions").asInt());
    var forecast = me.path("forecast");
    assertEquals(topics, forecast.path("total").asInt()); assertEquals(confirmed, forecast.path("closedByDiagnostic").asInt()); assertEquals(closed, forecast.path("closedByPractice").asInt());
    assertEquals(confirmed + closed, forecast.path("closed").asInt()); assertEquals(topics - confirmed - closed, forecast.path("remaining").asInt());
    assertEquals(forecast.path("closed").asInt(), series.path("closed").get(last).asInt(), "the closed line ends at the forecast's closed");
    assertEquals(1.0, forecast.path("pace").asDouble(), "one topic closed by practice, a newcomer's week"); assertEquals(1.0, forecast.path("paceWeeks").asDouble());
    assertEquals(3.9, forecast.path("neededPace").asDouble()); assertEquals("BEHIND", forecast.path("status").asText());
    assertEquals(today.plusDays(39 * 7).toString(), forecast.path("forecastDate").asText());
    assertEquals(List.of("BEHIND"), strings(me.path("flags")), "the open lesson's last task is solved: not stuck");

    // The student sees the same forecast and their own closed topics per day.
    var session = live.path("session");
    assertEquals(today.plusDays(70).toString(), session.path("date").asText()); assertEquals(10.0, session.path("weeksLeft").asDouble());
    assertEquals(confirmed + closed, session.path("closed").asInt()); assertEquals(forecast.path("remaining").asInt(), session.path("remaining").asInt());
    assertEquals("BEHIND", session.path("status").asText()); assertEquals(3.9, session.path("neededPace").asDouble());
    assertEquals(today.toString(), session.path("days").get(session.path("days").size() - 1).asText());
    assertEquals(session.path("days").size(), session.path("closedSeries").size());
    assertEquals(confirmed + closed, session.path("closedSeries").get(session.path("closedSeries").size() - 1).asInt());
    assertEquals(today.minusDays(2).toString(), session.path("days").get(0).asText(), "from the first lesson");
    assertEquals(List.of(1.0, 5.0, 5.0), doubles(session.path("closedSeries"), 0));
  }

  @Test void forecastCountsPracticeClosuresOfTheLastThreeWeeks() throws Exception {
    fixedNow.set(NOW); String admin = login("admin", "admin-pass"); setSession(admin, TODAY.plusDays(70));
    long id = studentRow("pace-student", "Темп", null); diagnostic(id, "JAVA", NOW.minus(Duration.ofDays(31)));
    lesson(id, "JAVA", 1, NOW.minus(Duration.ofDays(30)), false);
    long older = lesson(id, "JAVA", 2, NOW.minus(Duration.ofDays(22)), false), recent = lesson(id, "JAVA", 3, NOW.minus(Duration.ofDays(20)), false);
    for (int i = 0; i < 3; i++) { long t = task("VARIABLE_BASIC", "JAVA"); submit(older, t, true, NOW.minus(Duration.ofDays(22)).plusSeconds(60 * i)); credit(id, t); }
    for (int i = 0; i < 3; i++) { long t = task("PRIMITIVE_TYPES", "JAVA"); submit(recent, t, true, NOW.minus(Duration.ofDays(20)).plusSeconds(60 * i)); credit(id, t); }
    var view = read(admin, get("/api/admin/progress").param("language", "JAVA"));
    assertEquals(TODAY.minusDays(29).toString(), view.path("from").asText());
    var days = new ArrayList<String>(); view.path("days").forEach(d -> days.add(d.asText()));
    assertTrue(days.getFirst().compareTo(TODAY.minusDays(30).toString()) <= 0, "the whole history from the course's first lesson, not from the period's start");
    assertEquals(TODAY.toString(), days.getLast());
    var me = findStudent(view, "pace-student"); var series = me.path("series");
    assertEquals(TODAY.minusDays(30).toString(), me.path("firstLessonDay").asText());
    int older22 = days.indexOf(TODAY.minusDays(22).toString()), recent20 = days.indexOf(TODAY.minusDays(20).toString());
    assertEquals(0, series.path("solved").get(older22 - 1).asInt()); assertEquals(3, series.path("solved").get(older22).asInt()); assertEquals(6, series.path("solved").get(recent20).asInt());
    assertEquals(1.1, series.path("skills").get(older22).asDouble(), "half of one topic out of 44"); assertEquals(2.3, series.path("skills").get(recent20).asDouble());
    assertEquals(6 * 10 + 2 * 20, series.path("xp").get(recent20).asInt());
    assertEquals(0, series.path("closed").get(older22 - 1).asInt()); assertEquals(1, series.path("closed").get(older22).asInt()); assertEquals(2, series.path("closed").get(recent20).asInt());
    var forecast = me.path("forecast");
    assertEquals(2, forecast.path("closedByPractice").asInt()); assertEquals(42, forecast.path("remaining").asInt());
    assertEquals(forecast.path("closed").asInt(), series.path("closed").get(series.path("closed").size() - 1).asInt());
    assertEquals(3.0, forecast.path("paceWeeks").asDouble(), "a month in the course: the whole three-week window");
    assertEquals(0.33, forecast.path("pace").asDouble(), "only the topic closed 20 days ago is in the window");
    assertEquals(4.2, forecast.path("neededPace").asDouble()); assertEquals("BEHIND", forecast.path("status").asText());
    assertEquals(TODAY.plusDays(42 * 3 * 7).toString(), forecast.path("forecastDate").asText());
    assertEquals(10.0, view.path("session").path("weeksLeft").asDouble());
  }

  @Test void flagsShowStuckGoneAndNotStartedMembersOnly() throws Exception {
    fixedNow.set(NOW); String admin = login("admin", "admin-pass");
    long current = task("VARIABLE_BASIC", "JAVA"), solved = task("VARIABLE_BASIC", "JAVA");
    long stuck = member("flag-stuck"), almost = member("flag-almost"), recovered = member("flag-recovered"),
        gone = member("flag-gone"), recent = member("flag-recent"), helper = member("flag-helper");
    member("flag-fresh");
    // Five failed submissions in a row on the current task of an open lesson: stuck. Four, or a pass after them: not.
    long lesson = lesson(stuck, "JAVA", 1, NOW.minus(Duration.ofHours(2)), true);
    submit(lesson, solved, true, NOW.minus(Duration.ofMinutes(100))); credit(stuck, solved);
    for (int i = 0; i < 5; i++) submit(lesson, current, false, NOW.minus(Duration.ofMinutes(90 - 10 * i)));
    lesson = lesson(almost, "JAVA", 1, NOW.minus(Duration.ofHours(2)), true);
    for (int i = 0; i < 4; i++) submit(lesson, current, false, NOW.minus(Duration.ofMinutes(90 - 10 * i)));
    lesson = lesson(recovered, "JAVA", 1, NOW.minus(Duration.ofHours(2)), true);
    for (int i = 0; i < 5; i++) submit(lesson, current, false, NOW.minus(Duration.ofMinutes(90 - 10 * i)));
    submit(lesson, current, true, NOW.minus(Duration.ofMinutes(30))); credit(recovered, current);
    lesson = lesson(helper, "JAVA", 1, NOW.minus(Duration.ofHours(2)), true);
    for (int i = 0; i < 5; i++) submit(lesson, current, false, NOW.minus(Duration.ofMinutes(90 - 10 * i)));
    // Silent for 8 days: gone; for 6 days: not yet.
    lesson = lesson(gone, "JAVA", 1, NOW.minus(Duration.ofDays(8)), false); submit(lesson, current, false, NOW.minus(Duration.ofDays(8)).plusSeconds(600));
    lesson = lesson(recent, "JAVA", 1, NOW.minus(Duration.ofDays(6)), false); submit(lesson, current, false, NOW.minus(Duration.ofDays(6)).plusSeconds(600));
    // The helper is a volunteer: listed, but no flags and no forecast.
    mvc.perform(patch("/api/admin/students/{id}", helper).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"sessionParticipant\":false}")).andExpect(status().isOk());

    var view = read(admin, get("/api/admin/progress").param("language", "JAVA"));
    assertEquals(List.of("STUCK"), strings(findStudent(view, "flag-stuck").path("flags")));
    assertEquals(List.of(), strings(findStudent(view, "flag-almost").path("flags")));
    assertEquals(List.of(), strings(findStudent(view, "flag-recovered").path("flags")));
    assertEquals(List.of("NOT_STARTED"), strings(findStudent(view, "flag-fresh").path("flags")));
    assertTrue(findStudent(view, "flag-fresh").path("member").asBoolean(), "the diagnostic makes Java the session course");
    assertEquals(List.of("GONE"), strings(findStudent(view, "flag-gone").path("flags")));
    assertEquals(NOW.minus(Duration.ofDays(8)).plusSeconds(600).toString(), findStudent(view, "flag-gone").path("lastActivityAt").asText());
    assertEquals(List.of(), strings(findStudent(view, "flag-recent").path("flags")));
    var volunteer = findStudent(view, "flag-helper");
    assertFalse(volunteer.path("participant").asBoolean()); assertFalse(volunteer.path("member").asBoolean());
    assertTrue(volunteer.path("forecast").isNull()); assertEquals(List.of(), strings(volunteer.path("flags")));
    assertEquals(view.path("days").size(), volunteer.path("series").path("skills").size(), "a non-member still has their lines");
    assertEquals(view.path("days").size(), volunteer.path("series").path("closed").size());
    assertTrue(findStudent(view, "flag-stuck").path("forecast").path("status").isNull(), "no session date: no status, no BEHIND flag");
  }

  @Test void membersAreParticipantsWhoseSessionCourseIsTheView() throws Exception {
    fixedNow.set(NOW); String admin = login("admin", "admin-pass");
    String javaToken = createStudent("course-java", "Ява", null); long java = studentId("course-java");
    diagnostic(java, "JAVA", NOW.minus(Duration.ofDays(6)));
    lesson(java, "JAVA", 1, NOW.minus(Duration.ofDays(5)), false); lesson(java, "JAVA", 2, NOW.minus(Duration.ofDays(4)), false); lesson(java, "PYTHON", 1, NOW.minus(Duration.ofDays(1)), false);
    long tie = studentRow("course-tie", "Ничья", null);
    lesson(tie, "JAVA", 1, NOW.minus(Duration.ofDays(5)), false); lesson(tie, "PYTHON", 1, NOW.minus(Duration.ofDays(1)), false);
    long both = studentRow("course-diagnostics", "Две диагностики", null);
    diagnostic(both, "JAVA", NOW.minus(Duration.ofDays(3))); diagnostic(both, "PYTHON", NOW.minus(Duration.ofDays(2)));
    long none = studentRow("course-none", "Без курса", null); db.update("insert into student_languages(user_id,language) values(?, 'JAVA')", none);

    var javaView = read(admin, get("/api/admin/progress").param("language", "JAVA"));
    var pythonView = read(admin, get("/api/admin/progress").param("language", "PYTHON"));
    var javaMember = findStudent(javaView, "course-java");
    assertEquals("JAVA", javaMember.path("sessionCourse").asText()); assertTrue(javaMember.path("member").asBoolean()); assertFalse(javaMember.path("forecast").isNull());
    var javaInPython = findStudent(pythonView, "course-java");
    assertFalse(javaInPython.path("member").asBoolean(), "listed in Python for completeness"); assertTrue(javaInPython.path("forecast").isNull()); assertEquals(List.of(), strings(javaInPython.path("flags")));
    assertEquals("PYTHON", findStudent(javaView, "course-tie").path("sessionCourse").asText(), "a tie goes to the most recent lesson");
    assertFalse(findStudent(javaView, "course-tie").path("member").asBoolean()); assertTrue(findStudent(pythonView, "course-tie").path("member").asBoolean());
    assertEquals("PYTHON", findStudent(javaView, "course-diagnostics").path("sessionCourse").asText(), "without lessons: the latest diagnostic");
    assertEquals(List.of("NOT_STARTED"), strings(findStudent(pythonView, "course-diagnostics").path("flags")));
    assertTrue(findStudent(javaView, "course-none").path("sessionCourse").isNull()); assertFalse(findStudent(javaView, "course-none").path("member").asBoolean());
    assertThrows(AssertionError.class, () -> findStudent(pythonView, "course-none"), "no Python row, no Python lessons: not listed");

    // The student's own page has the session block only in the session course.
    var own = read(javaToken, get("/api/progress"));
    assertEquals(44, own.path("session").path("total").asInt()); assertTrue(own.path("session").path("date").isNull()); assertTrue(own.path("session").path("status").isNull());
    assertEquals(TODAY.minusDays(6).toString(), own.path("session").path("days").get(0).asText(), "from the diagnostic when it came before the first lesson");
    assertEquals(7, own.path("session").path("closedSeries").size()); assertEquals(TODAY.toString(), own.path("session").path("days").get(6).asText());
    assertTrue(read(javaToken, get("/api/progress").param("language", "PYTHON")).path("session").isNull());
    // Not a participant: still listed, out of the statistics, no session block.
    mvc.perform(patch("/api/admin/students/{id}", java).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"sessionParticipant\":false}")).andExpect(status().isOk());
    var off = findStudent(read(admin, get("/api/admin/progress").param("language", "JAVA")), "course-java");
    assertFalse(off.path("participant").asBoolean()); assertFalse(off.path("member").asBoolean()); assertTrue(off.path("forecast").isNull()); assertEquals(List.of(), strings(off.path("flags")));
    assertTrue(read(javaToken, get("/api/progress")).path("session").isNull());
    assertTrue(read(admin, get("/api/progress")).path("session").isNull(), "an admin has no session block");
  }

  @Test void theClassroomShowsOnlyAnonymousAggregatesOfMembers() throws Exception {
    fixedNow.set(NOW); String admin = login("admin", "admin-pass"); setSession(admin, TODAY.plusDays(70));
    String group = "Класс-7Б"; var people = new ArrayList<String>();
    Instant tuesday = Instant.parse("2030-03-12T10:00:00Z");
    for (int i = 0; i < 5; i++) {
      long id = studentRow("secret-login-" + i, "Скрытая Персона " + i, group); people.add("secret-login-" + i); people.add("Скрытая Персона " + i);
      diagnostic(id, "JAVA", NOW.minus(Duration.ofDays(10)));
      long lesson = lesson(id, "JAVA", 1, tuesday, false);
      if (i < 3) for (int k = 0; k < 3; k++) { long t = task("VARIABLE_BASIC", "JAVA"); submit(lesson, t, true, tuesday.plusSeconds(60 * k)); credit(id, t); }
      else { long t = task("VARIABLE_BASIC", "JAVA"); submit(lesson, t, false, tuesday); submit(lesson, t, false, tuesday.plusSeconds(60)); }
    }
    // In the group but not members of the Java statistics: a volunteer and a student whose session is Python.
    long volunteer = studentRow("secret-volunteer", "Скрытый Волонтёр", group); people.add("secret-volunteer"); people.add("Скрытый Волонтёр");
    db.update("update users set session_participant=0 where id=?", volunteer); diagnostic(volunteer, "JAVA", NOW.minus(Duration.ofDays(10)));
    long volunteerLesson = lesson(volunteer, "JAVA", 1, tuesday, false);
    for (int k = 0; k < 3; k++) { long t = task("ASSIGNMENT_OPERATORS", "JAVA"); submit(volunteerLesson, t, true, tuesday.plusSeconds(60 * k)); credit(volunteer, t); }
    long pythonist = studentRow("secret-python", "Скрытый Питонист", group); people.add("secret-python"); people.add("Скрытый Питонист");
    lesson(pythonist, "JAVA", 1, tuesday, false); lesson(pythonist, "PYTHON", 1, tuesday.plusSeconds(3600), false); lesson(pythonist, "PYTHON", 2, tuesday.plusSeconds(7200), false);

    String body = mvc.perform(get("/api/admin/classroom").param("language", "JAVA").param("group", group).cookie(cookie(admin))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString(java.nio.charset.StandardCharsets.UTF_8);
    for (String person : people) assertFalse(body.contains(person), "the projected screen names nobody: " + person);
    var view = json.readTree(body);
    assertNoPersonalFields(view);
    assertEquals(group, view.path("group").asText()); assertEquals(5, view.path("members").asInt(), "only participants whose session course is Java");
    assertFalse(view.path("tooSmall").asBoolean()); assertEquals(44, view.path("totalTopics").asInt());
    assertEquals(TODAY.plusDays(70).toString(), view.path("session").path("date").asText());
    var week = view.path("week");
    assertEquals("2030-03-11", week.path("from").asText(), "the UTC week from Monday");
    assertEquals(3, week.path("closedTopics").asInt(), "three first iterations this week");
    assertEquals(22, week.path("goal").asInt(), "220 topics left at the week start over 73 days");
    var daily = view.path("daily");
    assertEquals(28, daily.size()); assertEquals("2030-03-14", daily.get(27).path("day").asText());
    assertEquals("2030-03-12", daily.get(25).path("day").asText()); assertEquals(3, daily.get(25).path("closedTopics").asInt());
    var firstBlock = view.path("blocks").get(0);
    assertEquals(0, firstBlock.path("block").asInt()); assertEquals(5, firstBlock.path("topics").size());
    assertEquals(0.06, firstBlock.path("avgShare").asDouble(), "three halves of VARIABLE_BASIC over 5 members × 5 topics");
    var hard = view.path("hardTopics");
    assertEquals(1, hard.size(), "only VARIABLE_BASIC was tried by three members or more");
    assertEquals("VARIABLE_BASIC", hard.get(0).path("code").asText()); assertEquals(5, hard.get(0).path("students").asInt());
    assertEquals(1.4, hard.get(0).path("attemptsPerSolve").asDouble(), "13 submissions, 9 solved");

    // Fewer than five members: no totals at all, they would identify people.
    for (int i = 0; i < 4; i++) { long id = studentRow("mini-" + i, "Мини " + i, "Класс-Мини"); diagnostic(id, "JAVA", NOW.minus(Duration.ofDays(3))); }
    var small = read(admin, get("/api/admin/classroom").param("language", "JAVA").param("group", "Класс-Мини"));
    assertTrue(small.path("tooSmall").asBoolean()); assertEquals(4, small.path("members").asInt());
    assertTrue(small.path("week").isNull()); assertEquals(0, small.path("daily").size()); assertEquals(0, small.path("blocks").size()); assertEquals(0, small.path("hardTopics").size());
    assertNoPersonalFields(small);
    // An unknown group, or a group without members in the course: 404.
    var unknown = json.readTree(mvc.perform(get("/api/admin/classroom").param("language", "JAVA").param("group", "Нет-такой").cookie(cookie(admin))).andExpect(status().isNotFound()).andReturn().getResponse().getContentAsString());
    assertEquals("GROUP_NOT_FOUND", unknown.path("error").asText());
    mvc.perform(get("/api/admin/classroom").param("language", "PYTHON").param("group", "Класс-Мини").cookie(cookie(admin))).andExpect(status().isNotFound());
    mvc.perform(get("/api/admin/classroom").param("language", "JAVA").cookie(cookie(admin))).andExpect(status().isNotFound());
  }

  @Test void theSessionDateIsValidatedAndTheAnalyticsAreForAdminsOnly() throws Exception {
    String admin = login("admin", "admin-pass"); String student = createStudent("nosy-analytics", "Любопытный", "Поток-1");
    for (String bad : List.of("{\"date\":\"2030-02-30\"}", "{\"date\":\"30.06.2030\"}", "{\"date\":5}", "{}")) {
      var error = json.readTree(mvc.perform(put("/api/admin/session").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content(bad)).andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
      assertEquals("INVALID_SESSION_DATE", error.path("error").asText(), bad); assertFalse(error.path("message").asText().isEmpty());
    }
    assertEquals("2030-06-20", setSession(admin, LocalDate.of(2030, 6, 20)).path("date").asText());
    assertEquals("2030-06-20", read(admin, get("/api/admin/session")).path("date").asText());
    assertEquals("2030-06-20", db.queryForObject("select value from app_settings where key='session_date'", String.class));
    assertTrue(read(admin, put("/api/admin/session").contentType(MediaType.APPLICATION_JSON).content("{\"date\":null}")).path("date").isNull());
    assertTrue(read(admin, get("/api/admin/session")).path("date").isNull(), "null removes the date");
    assertEquals(0, db.queryForObject("select count(*) from app_settings where key='session_date'", Integer.class));

    for (var request : List.of(get("/api/admin/progress"), get("/api/admin/session"), put("/api/admin/session").contentType(MediaType.APPLICATION_JSON).content("{\"date\":null}"),
        get("/api/admin/classroom").param("group", "Поток-1"))) {
      var refused = json.readTree(mvc.perform(request.cookie(cookie(student))).andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
      assertEquals("FORBIDDEN", refused.path("error").asText());
    }
    for (String period : List.of("from=2030-13-01", "from=2030-03-10&to=2030-03-09", "to=yesterday"))
      assertEquals("INVALID_PERIOD", json.readTree(mvc.perform(get("/api/admin/progress?language=JAVA&" + period).cookie(cookie(admin))).andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString()).path("error").asText(), period);
    var custom = read(admin, get("/api/admin/progress").param("language", "JAVA").param("from", "2030-03-01").param("to", "2030-03-03"));
    assertEquals("2030-03-01", custom.path("from").asText()); assertEquals("2030-03-03", custom.path("to").asText());
  }

  @Test void theTeacherSwitchesSessionParticipationPerStudent() throws Exception {
    String admin = login("admin", "admin-pass"); createStudent("participant-a", "Участник", null); long id = studentId("participant-a");
    var listed = findStudent(read(admin, get("/api/admin/students")), "participant-a");
    assertTrue(listed.path("sessionParticipant").isBoolean()); assertTrue(listed.path("sessionParticipant").asBoolean(), "everyone takes the session by default");
    var updated = read(admin, patch("/api/admin/students/{id}", id).contentType(MediaType.APPLICATION_JSON).content("{\"sessionParticipant\":false}"));
    assertFalse(updated.path("sessionParticipant").asBoolean()); assertEquals("participant-a", updated.path("login").asText());
    assertFalse(findStudent(read(admin, get("/api/admin/students")), "participant-a").path("sessionParticipant").asBoolean());
    assertFalse(read(admin, get("/api/admin/students/{id}", id)).path("student").path("sessionParticipant").asBoolean());
    assertFalse(read(admin, patch("/api/admin/students/{id}", id).contentType(MediaType.APPLICATION_JSON).content("{\"group\":\"Поток-2\"}")).path("sessionParticipant").asBoolean(), "fields not sent stay as they were");
    var invalid = json.readTree(mvc.perform(patch("/api/admin/students/{id}", id).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"sessionParticipant\":\"no\"}")).andExpect(status().isBadRequest()).andReturn().getResponse().getContentAsString());
    assertEquals("INVALID_SESSION_PARTICIPANT", invalid.path("error").asText());
    assertTrue(read(admin, patch("/api/admin/students/{id}", id).contentType(MediaType.APPLICATION_JSON).content("{\"sessionParticipant\":true}")).path("sessionParticipant").asBoolean());
  }

  // ---------------------------------------------------------------- helpers

  /** game.ts experience() on the student's own /api/progress. */
  private static int experience(JsonNode progress) {
    int solved = progress.path("solvedTasks").asInt(), hard = Math.min(progress.path("hardSolved").asInt(), solved), iterations = 0, mastered = 0, confirmed = 0;
    for (var s : progress.path("skills")) {
      iterations += s.path("completedIterations").asInt();
      if (s.path("mastered").asInt() == 1) mastered++; else if (s.path("confirmedByDiagnostic").asInt() == 1) confirmed++;
    }
    return (solved - hard) * 10 + hard * 30 + iterations * 20 + mastered * 50 + confirmed * 5;
  }
  /** game.ts skillPercent, without rounding. */
  private static double skillShare(JsonNode s) {
    if (s.path("mastered").asInt() == 1) return 1;
    int[] tasks = {3, 2, 1}; int completed = s.path("completedIterations").asInt(), done = 0;
    for (int i = 0; i < Math.min(completed, 3); i++) done += tasks[i];
    return (done + Math.min(s.path("iterationSuccesses").asInt(), tasks[Math.min(completed, 2)])) / 6.0;
  }
  private static void assertNoPersonalFields(JsonNode node) {
    if (node.isObject()) node.fieldNames().forEachRemaining(name -> assertFalse(Set.of("id", "userId", "login", "displayName", "name").contains(name), "field " + name));
    for (var child : node) assertNoPersonalFields(child);
  }
  private static List<Double> doubles(JsonNode array, int from) { var list = new ArrayList<Double>(); for (int i = from; i < array.size(); i++) list.add(array.get(i).asDouble()); return list; }
  private static List<String> strings(JsonNode array) { var list = new ArrayList<String>(); for (var x : array) list.add(x.asText()); return list; }
  private static JsonNode findStudent(JsonNode view, String login) { for (var s : view.path("students")) if (login.equals(s.path("login").asText())) return s; throw new AssertionError("no student " + login); }

  private JsonNode read(String token, MockHttpServletRequestBuilder request) throws Exception {
    return json.readTree(mvc.perform(request.cookie(cookie(token))).andExpect(status().isOk()).andReturn().getResponse().getContentAsString());
  }
  private JsonNode setSession(String admin, LocalDate date) throws Exception {
    return read(admin, put("/api/admin/session").contentType(MediaType.APPLICATION_JSON).content("{\"date\":\"" + date + "\"}"));
  }
  private long solve(String token, String skill, boolean failFirst) throws Exception {
    var next = read(token, get("/api/learning/next"));
    assertEquals(skill, next.path("skill").path("code").asText());
    long task = next.path("task").path("id").asLong();
    if (failFirst) attempt(token, task, "WRONG");
    attempt(token, task, "public class Solution {}");
    return task;
  }
  private void attempt(String token, long task, String source) throws Exception {
    mvc.perform(post("/api/attempts").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId", task, "sourceCode", source)))).andExpect(status().isOk());
  }
  private void start(String token) throws Exception { mvc.perform(post("/api/lessons/start").cookie(cookie(token))).andExpect(status().isOk()); }
  private void finish(String token, long lesson) throws Exception { mvc.perform(post("/api/lessons/{id}/finish", lesson).cookie(cookie(token))).andExpect(status().isOk()); }
  private long openLesson(long student) { return db.queryForObject("select id from lessons where user_id=? and finished_at is null", Long.class, student); }
  private void submitDiagnostic(String token) throws Exception {
    var answers = new ArrayList<Map<String, Object>>();
    for (var q : db.queryForList("select id,correct_option,block_no from diagnostic_questions where language='JAVA' order by id")) {
      var answer = new LinkedHashMap<String, Object>(); answer.put("questionId", q.get("id"));
      if (((Number) q.get("block_no")).intValue() == 0) answer.put("selectedOption", q.get("correct_option"));
      answers.add(answer);
    }
    mvc.perform(post("/api/diagnostic").cookie(cookie(token)).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("answers", answers)))).andExpect(status().isOk());
  }
  private void addTask(String skill, String title) { task(skill, "JAVA", title); }
  private long task(String skill, String language) { return task(skill, language, "task " + UUID.randomUUID()); }
  private long task(String skill, String language, String title) {
    long id = db.queryForObject("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language) values(?,?,?,'','class TestHarness {}','TestHarness.java',?) returning id", Long.class, skill, title, title, language);
    db.update("insert into task_target_skills(task_id,skill_code) values(?,?)", id, skill);
    return id;
  }

  // History written straight into the tables, at chosen moments.
  private long lesson(long user, String language, int number, Instant started, boolean open) {
    return db.queryForObject("insert into lessons(user_id,lesson_number,language,language_lesson_number,started_at,finished_at,last_activity_at) values(?,(select coalesce(max(lesson_number),0)+1 from lessons where user_id=?),?,?,?,?,?) returning id",
        Long.class, user, user, language, number, sql(started), open ? null : sql(started.plusSeconds(1800)), started.toString());
  }
  private void submit(long lesson, long task, boolean passed, Instant at) {
    db.update("insert into submissions(lesson_id,task_id,source_code,passed,runner_output,created_at) values(?,?,'code',?,?,?)", lesson, task, passed ? 1 : 0, passed ? "ok" : "fail", sql(at));
  }
  private void credit(long user, long task) { db.update("insert into successful_task_credit(user_id,task_id) values(?,?)", user, task); }
  private void diagnostic(long user, String language, Instant at) { db.update("insert into student_languages(user_id,language,diagnostic_completed_at) values(?,?,?)", user, language, at.toString()); }
  /** SQLite CURRENT_TIMESTAMP format, as the tables store it by default. */
  private static String sql(Instant at) { return at.toString().replace('T', ' ').substring(0, 19); }
  /** A student who never signs in, straight into the table. */
  private long studentRow(String login, String name, String group) {
    return db.queryForObject("insert into users(login,password_hash,role,display_name,group_name) values(?,'-','STUDENT',?,?) returning id", Long.class, login, name, group);
  }
  /** A Java member: a participant with the Java diagnostic and nothing else yet. */
  private long member(String login) { long id = studentRow(login, login, null); diagnostic(id, "JAVA", NOW.minus(Duration.ofDays(20))); return id; }
  private String createStudent(String login, String name, String group) throws Exception {
    var body = new LinkedHashMap<String, Object>(Map.of("login", login, "password", "student-pass", "displayName", name));
    if (group != null) body.put("group", group);
    mvc.perform(post("/api/admin/students").cookie(cookie(login("admin", "admin-pass"))).contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(body))).andExpect(status().isOk());
    return login(login, "student-pass");
  }
  private String login(String login, String password) throws Exception {
    return mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login", login, "password", password)))).andExpect(status().isOk()).andReturn().getResponse().getCookie("adaptive_session").getValue();
  }
  private long studentId(String login) { return db.queryForObject("select id from users where login=?", Long.class, login); }
  private jakarta.servlet.http.Cookie cookie(String value) { return new jakarta.servlet.http.Cookie("adaptive_session", value); }
}
