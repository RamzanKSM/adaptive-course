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
 * Pair grades end to end: points and attendance inside the window, the norm (previous Moscow week, earlier week, the pair
 * itself), the teacher's grades through recalculation, publishing, the journal, and what a student may see.
 * Every test works in its own year, so the saved pairs of one never feed the weekly norm of another.
 */
@SpringBootTest
@AutoConfigureMockMvc
class PairGradesIntegrationTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json;
  @MockBean PistonCodeRunner runner;
  @MockBean LlmTutor tutor;
  @MockBean LearningContentGenerator generator;
  @MockBean Clock clock;
  static final Instant NOW = Instant.parse("2040-01-01T12:00:00Z");

  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:pairs-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
    p.add("app.task-audit.enabled", () -> "false");
    p.add("app.lesson.idle-close.enabled", () -> "false");
  }
  @BeforeEach void prepare() {
    db.update("update users set password_hash=? where login='admin'", new BCryptPasswordEncoder().encode("admin-pass"));
    when(runner.configured()).thenReturn(true);
    when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true, "READY", "17.0.1"));
    when(tutor.status(anyLong())).thenReturn(new LlmStatus(false, false, false, "DISABLED", "gpt-6-luna"));
    when(clock.instant()).thenReturn(NOW);
    when(clock.getZone()).thenReturn(ZoneOffset.UTC);
  }

  @Test void gradeThresholdsAreExactAtTheBoundaries() {
    assertEquals("5", PairGrades.grade(true, 27, 20.0)); assertEquals("4", PairGrades.grade(true, 26, 20.0));
    assertEquals("4", PairGrades.grade(true, 20, 20.0)); assertEquals("3", PairGrades.grade(true, 19, 20.0));
    assertEquals("3", PairGrades.grade(true, 12, 20.0)); assertEquals("2", PairGrades.grade(true, 11, 20.0)); assertEquals("2", PairGrades.grade(true, 0, 20.0));
    assertEquals("5", PairGrades.grade(true, 34, 25.0)); assertEquals("4", PairGrades.grade(true, 33, 25.0), "1.35 × 25 = 33.75");
    assertEquals("5", PairGrades.grade(true, 27, 19.5), "26.325"); assertEquals("4", PairGrades.grade(true, 26, 19.5));
    assertEquals("3", PairGrades.grade(true, 3, 5.0)); assertEquals("2", PairGrades.grade(true, 2, 5.0), "0.60 × 5 = 3");
    assertEquals("4", PairGrades.grade(true, 1, null)); assertEquals("2", PairGrades.grade(true, 0, null));
    assertEquals("4", PairGrades.grade(true, 1, 0.0)); assertEquals("2", PairGrades.grade(true, 0, 0.0));
    assertEquals("н", PairGrades.grade(false, 0, 20.0));
    assertEquals(20.0, PairGrades.median(List.of(27, 11, 20, 19, 26))); assertEquals(19.5, PairGrades.median(List.of(20, 11, 19, 27)));
    assertEquals(LocalDate.of(2031, 3, 3), PairGrades.week(Instant.parse("2031-03-09T20:59:59Z")), "Sunday 23:59 in Moscow");
    assertEquals(LocalDate.of(2031, 3, 10), PairGrades.week(Instant.parse("2031-03-09T21:00:00Z")), "Monday 00:00 in Moscow");
  }

  @Test void pointsCountFirstPassesOfCreditedTasksInsideTheWindow() throws Exception {
    String admin = login("admin", "admin-pass");
    Instant start = Instant.parse("2030-03-14T08:00:00Z"), end = start.plus(Duration.ofMinutes(90));
    long a = studentRow("pts-a", "Анна", "P-1"), b = studentRow("pts-b", "Борис", "P-1"), c = studentRow("pts-c", "Вера", "P-1"),
        d = studentRow("pts-d", "Глеб", "P-1"), e = studentRow("pts-e", "Дина", "P-1"), f = studentRow("pts-f", "Ефим", "P-other");
    db.update("update users set session_participant=0 where id=?", e);
    long lessonA = lesson(a, "JAVA", start.minus(Duration.ofHours(1)));
    long t1 = task("JAVA", 1, false), t2 = task("JAVA", 2, false), t3 = task("JAVA", 3, false), tNull = task("JAVA", null, false), tHard = task("JAVA", 2, true);
    submit(lessonA, t1, true, at(start, 10)); credit(a, t1);
    submit(lessonA, t2, false, at(start, 5)); submit(lessonA, t2, true, at(start, 20)); credit(a, t2);
    submit(lessonA, t3, true, at(start, 30)); credit(a, t3);
    submit(lessonA, tNull, true, at(start, 40)); credit(a, tNull);
    submit(lessonA, tHard, true, at(start, 50)); credit(a, tHard);
    // Not counted: a pass whose credit was revoked, a task first passed before the window, a pass after it, another course.
    long uncredited = task("JAVA", 3, false); submit(lessonA, uncredited, true, at(start, 25));
    long earlier = task("JAVA", 3, false); submit(lessonA, earlier, true, at(start, -30)); submit(lessonA, earlier, true, at(start, 35)); credit(a, earlier);
    long late = task("JAVA", 3, false); submit(lessonA, late, true, end.plusSeconds(60)); credit(a, late);
    long python = task("PYTHON", 3, false); long pythonLesson = lesson(a, "PYTHON", start); submit(pythonLesson, python, true, at(start, 15)); credit(a, python);
    // Counted: the revoked first pass is skipped, the re-pass inside the window is the first non-revoked one.
    long redone = task("JAVA", 1, false); submit(lessonA, redone, true, at(start, -20)); db.update("update submissions set revoked_at=? where lesson_id=? and task_id=?", sql(at(start, -10)), lessonA, redone);
    submit(lessonA, redone, true, at(start, 45)); credit(a, redone);
    // b: only a chat message inside the window; c: a lesson started inside it; d: only Python activity; e: not a participant.
    long lessonB = lesson(b, "JAVA", start.minus(Duration.ofHours(2)));
    db.update("insert into chat_messages(lesson_id,role,content,created_at) values(?,'ASSISTANT','hi',?)", lessonB, sql(at(start, 3)));
    db.update("insert into chat_messages(lesson_id,role,content,created_at) values(?,'STUDENT','help',?)", lessonB, sql(at(start, 60)));
    lesson(c, "JAVA", at(start, 70));
    submit(lesson(d, "PYTHON", at(start, 1)), task("PYTHON", 1, false), false, at(start, 2));
    long tE = task("JAVA", 3, false); submit(lesson(e, "JAVA", at(start, 1)), tE, true, at(start, 2)); credit(e, tE);
    long tF = task("JAVA", 3, false); submit(lesson(f, "JAVA", at(start, 1)), tF, true, at(start, 2)); credit(f, tF);

    int pairsBefore = count("select count(*) from pairs");
    var pair = read(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("P-1", "JAVA", "2030-03-14T11:00:00+03:00", "2030-03-14T12:30:00+03:00")));
    assertEquals(pairsBefore, count("select count(*) from pairs"), "a preview saves nothing");
    assertTrue(pair.path("id").isNull()); assertEquals("2030-03-14T08:00:00Z", pair.path("startsAt").asText()); assertEquals("2030-03-14T09:30:00Z", pair.path("endsAt").asText());
    assertEquals(List.of("pts-a", "pts-b", "pts-c", "pts-d"), logins(pair), "participants of the group only, sorted by name");
    var rowA = row(pair, "pts-a");
    assertEquals(1 + 2 + 3 + 1 + 20 + 1, rowA.path("points").asInt(), "difficulty, null → 1, HARD × 10");
    assertEquals(Map.of("1", 3, "2", 1, "3", 1, "hard", 1), json.convertValue(rowA.path("tasks"), Map.class));
    assertTrue(rowA.path("hard").asBoolean(), "a HARD task in the window"); assertTrue(rowA.path("attended").asBoolean());
    assertTrue(row(pair, "pts-b").path("attended").asBoolean(), "a student's chat message"); assertEquals(0, row(pair, "pts-b").path("points").asInt());
    assertTrue(row(pair, "pts-c").path("attended").asBoolean(), "a lesson started in the window");
    assertFalse(row(pair, "pts-d").path("attended").asBoolean(), "Python activity is not a Java pair"); assertEquals("н", row(pair, "pts-d").path("grade").asText());
    // The regular attended students (b, c) have 0 points: the pair's own median is 0, so points > 0 → 4, 0 → 2.
    assertEquals("PAIR", pair.path("medianSource").asText()); assertEquals(0.0, pair.path("median").asDouble()); assertTrue(pair.path("thresholds").isNull());
    assertEquals("4", rowA.path("grade").asText()); assertEquals("2", row(pair, "pts-b").path("grade").asText());
    assertTrue(rowA.path("percent").isNull()); assertFalse(rowA.path("manual").asBoolean());
    assertEquals(Map.of("н", 1, "2", 2, "3", 0, "4", 1, "5", 0), json.convertValue(pair.path("counts"), Map.class));
  }

  @Test void hardStudentsAreGradedButLeftOutOfTheMedian() throws Exception {
    String admin = login("admin", "admin-pass");
    Instant start = Instant.parse("2034-03-16T08:00:00Z");
    var regular = List.of(11, 19, 20, 26, 27);
    for (int points : regular) earn(studentRow("hm-" + points, "hm-" + points, "H-1"), "JAVA", start, points);
    long hardMode = studentRow("hm-mode", "hm-mode", "H-1"); earn(hardMode, "JAVA", start, 2);
    db.update("update users set hard_mode_allowed=1,hard_mode_on=1 where id=?", hardMode);
    db.update("insert or replace into student_skills(user_id,skill_code,completed_iterations) select ?,code,1 from skills where language='JAVA'", hardMode);
    long hardTask = studentRow("hm-task", "hm-task", "H-1"); long lesson = lesson(hardTask, "JAVA", start.minusSeconds(600));
    long t = task("JAVA", 3, true); submit(lesson, t, true, at(start, 5)); credit(hardTask, t);
    long switchedOff = studentRow("hm-off", "hm-off", "H-1"); earn(switchedOff, "JAVA", start, 20);
    db.update("update users set hard_mode_allowed=1,hard_mode_on=0 where id=?", switchedOff);
    db.update("insert or replace into student_skills(user_id,skill_code,completed_iterations) select ?,code,1 from skills where language='JAVA'", switchedOff);

    var pair = read(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("H-1", "JAVA", start.toString(), start.plusSeconds(5400).toString())));
    assertEquals("PAIR", pair.path("medianSource").asText());
    assertEquals(20.0, pair.path("median").asDouble(), "11, 19, 20, 20, 26, 27 — without the hard students' 2 and 30");
    assertEquals(27.0, pair.path("thresholds").path("five").asDouble()); assertEquals(20.0, pair.path("thresholds").path("four").asDouble()); assertEquals(12.0, pair.path("thresholds").path("three").asDouble());
    assertEquals(List.of("2", "3", "4", "4", "5"), regular.stream().map(points -> row(pair, "hm-" + points).path("grade").asText()).toList());
    assertTrue(row(pair, "hm-mode").path("hard").asBoolean()); assertEquals("2", row(pair, "hm-mode").path("grade").asText());
    assertTrue(row(pair, "hm-task").path("hard").asBoolean()); assertEquals(30, row(pair, "hm-task").path("points").asInt()); assertEquals("5", row(pair, "hm-task").path("grade").asText());
    assertFalse(row(pair, "hm-off").path("hard").asBoolean(), "allowed but switched off is regular");
    assertEquals(135, row(pair, "hm-27").path("percent").asInt()); assertEquals(150, row(pair, "hm-task").path("percent").asInt());
  }

  @Test void theNormIsThePreviousMoscowWeek() throws Exception {
    String admin = login("admin", "admin-pass");
    // The pair: Thursday 13 March 2031; its Moscow week starts on Monday the 10th, the previous one on the 3rd.
    Instant start = Instant.parse("2031-03-13T08:00:00Z");
    int[] fourteen = new int[14]; for (int i = 0; i < 14; i++) fourteen[i] = i + 1;
    history("JAVA", Instant.parse("2031-03-05T08:00:00Z"), fourteen, true, false);
    history("JAVA", Instant.parse("2031-03-09T20:30:00Z"), new int[]{15}, true, false); // Sunday 23:30 in Moscow: the 15th row
    history("JAVA", Instant.parse("2031-03-06T08:00:00Z"), new int[]{100, 100, 100}, true, true); // hard rows are not in the norm
    history("JAVA", Instant.parse("2031-03-06T09:00:00Z"), new int[]{0, 0, 0}, false, false); // absent rows are not either
    history("PYTHON", Instant.parse("2031-03-06T08:00:00Z"), new int[]{50, 50, 50, 50}, true, false); // another course
    history("JAVA", Instant.parse("2031-03-09T21:30:00Z"), new int[]{90, 90, 90, 90, 90}, true, false); // Monday 00:30: the pair's own week
    long s = studentRow("week-a", "week-a", "W-1"); earn(s, "JAVA", start, 10);

    var pair = read(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("W-1", "JAVA", start.toString(), start.plusSeconds(5400).toString())));
    assertEquals("WEEK", pair.path("medianSource").asText()); assertEquals("2031-03-03", pair.path("medianWeek").asText());
    assertEquals(8.0, pair.path("median").asDouble(), "1..15");
    assertEquals(125, row(pair, "week-a").path("percent").asInt()); assertEquals("4", row(pair, "week-a").path("grade").asText(), "10 < 1.35 × 8");
    // A week later the previous week has only the five Monday rows: the latest earlier week with enough rows is still the 3rd.
    Instant later = start.plus(Duration.ofDays(7));
    var next = read(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("W-1", "JAVA", later.toString(), later.plusSeconds(5400).toString())));
    assertEquals("WEEK", next.path("medianSource").asText()); assertEquals("2031-03-03", next.path("medianWeek").asText());
  }

  @Test void withoutAFullPreviousWeekTheNormFallsBackToAnEarlierWeekThenToThePair() throws Exception {
    String admin = login("admin", "admin-pass");
    Instant start = Instant.parse("2032-06-10T08:00:00Z"); // Thursday; Moscow weeks: 7 June, 31 May, 24 May, 17 May
    history("JAVA", Instant.parse("2032-06-01T08:00:00Z"), new int[]{1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}, true, false); // 14 rows: not enough
    int[] fifteen = new int[15]; Arrays.fill(fifteen, 6); history("JAVA", Instant.parse("2032-05-25T08:00:00Z"), fifteen, true, false);
    int[] twenty = new int[20]; Arrays.fill(twenty, 40); history("JAVA", Instant.parse("2032-05-18T08:00:00Z"), twenty, true, false);
    long s = studentRow("fall-a", "fall-a", "F-1"); earn(s, "JAVA", start, 9);
    var pair = read(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("F-1", "JAVA", start.toString(), start.plusSeconds(5400).toString())));
    assertEquals("WEEK", pair.path("medianSource").asText()); assertEquals("2032-05-24", pair.path("medianWeek").asText(), "the latest earlier week with 15 rows");
    assertEquals(6.0, pair.path("median").asDouble()); assertEquals("5", row(pair, "fall-a").path("grade").asText());

    // Thirteen weeks after the full weeks there is no norm in the last twelve: the pair's own regular students.
    Instant far = Instant.parse("2032-08-26T08:00:00Z");
    long t = studentRow("fall-b", "fall-b", "F-2"); earn(t, "JAVA", far, 4); long u = studentRow("fall-c", "fall-c", "F-2"); earn(u, "JAVA", far, 8);
    var own = read(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("F-2", "JAVA", far.toString(), far.plusSeconds(5400).toString())));
    assertEquals("PAIR", own.path("medianSource").asText()); assertTrue(own.path("medianWeek").isNull()); assertEquals(6.0, own.path("median").asDouble());
    assertEquals("3", row(own, "fall-b").path("grade").asText()); assertEquals("4", row(own, "fall-c").path("grade").asText());

    // Nobody came: no norm at all.
    var none = read(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("F-2", "JAVA", "2032-09-01T08:00:00Z", "2032-09-01T09:30:00Z")));
    assertEquals("NONE", none.path("medianSource").asText()); assertTrue(none.path("median").isNull()); assertTrue(none.path("thresholds").isNull());
    assertEquals(Map.of("н", 2, "2", 0, "3", 0, "4", 0, "5", 0), json.convertValue(none.path("counts"), Map.class));
  }

  @Test void theTeachersGradesSurviveRecalculation() throws Exception {
    String admin = login("admin", "admin-pass");
    Instant start = Instant.parse("2033-04-07T08:00:00Z");
    long a = studentRow("man-a", "Алла", "M-1"), b = studentRow("man-b", "Богдан", "M-1"), c = studentRow("man-c", "Вика", "M-1");
    earn(a, "JAVA", start, 2); earn(b, "JAVA", start, 10); earn(c, "JAVA", start, 6);
    var request = new LinkedHashMap<String, Object>(Map.of("group", "M-1", "language", "JAVA", "startsAt", start.toString(), "endsAt", start.plusSeconds(5400).toString()));
    request.put("grades", List.of(Map.of("userId", a, "grade", "5", "comment", "  ответ у доски "), Map.of("userId", 999_999, "grade", "3")));
    var saved = read(admin, post("/api/admin/pairs").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(request)));
    long id = saved.path("id").asLong();
    assertEquals(6.0, saved.path("median").asDouble()); assertFalse(saved.path("published").asBoolean()); assertEquals(NOW.toString(), saved.path("createdAt").asText());
    var rowA = row(saved, "man-a");
    assertEquals("2", rowA.path("autoGrade").asText()); assertEquals("5", rowA.path("grade").asText()); assertEquals("ответ у доски", rowA.path("comment").asText()); assertTrue(rowA.path("manual").asBoolean());
    assertEquals("5", row(saved, "man-b").path("grade").asText()); assertEquals("4", row(saved, "man-c").path("grade").asText());
    assertEquals(3, count("select count(*) from pair_grades where pair_id=?", id), "unknown students in grades are ignored");

    // A comment alone makes a row manual; the auto grade without a comment makes it auto again.
    var patched = read(admin, patch("/api/admin/pairs/{id}/grades/{u}", id, c).contentType(MediaType.APPLICATION_JSON).content("{\"grade\":\"4\",\"comment\":\"опоздал\"}"));
    assertTrue(row(patched, "man-c").path("manual").asBoolean());
    patched = read(admin, patch("/api/admin/pairs/{id}/grades/{u}", id, c).contentType(MediaType.APPLICATION_JSON).content("{\"grade\":\"4\",\"comment\":null}"));
    assertFalse(row(patched, "man-c").path("manual").asBoolean());

    // Revoked credits: b loses 6 of 10 points, a loses everything; the median moves to 4, the auto grades follow.
    db.update("delete from successful_task_credit where user_id=? and task_id in (select task_id from successful_task_credit where user_id=? order by task_id limit 2)", b, b);
    db.update("delete from successful_task_credit where user_id=?", a);
    var again = read(admin, post("/api/admin/pairs/{id}/recalculate", id));
    assertEquals(4.0, again.path("median").asDouble(), "0, 4, 6");
    assertEquals(0, row(again, "man-a").path("points").asInt()); assertEquals("2", row(again, "man-a").path("autoGrade").asText());
    assertEquals("5", row(again, "man-a").path("grade").asText(), "the teacher's grade stays"); assertEquals("ответ у доски", row(again, "man-a").path("comment").asText());
    assertEquals(4, row(again, "man-b").path("points").asInt()); assertEquals("4", row(again, "man-b").path("grade").asText());
    assertEquals("5", row(again, "man-c").path("autoGrade").asText()); assertEquals("5", row(again, "man-c").path("grade").asText(), "auto rows take the new grade");

    expect(admin, patch("/api/admin/pairs/{id}/grades/{u}", id, c).contentType(MediaType.APPLICATION_JSON).content("{\"grade\":\"6\"}"), status().isBadRequest(), "INVALID_GRADE");
    expect(admin, patch("/api/admin/pairs/{id}/grades/{u}", id, c).contentType(MediaType.APPLICATION_JSON).content("{\"grade\":\"Н\"}"), status().isBadRequest(), "INVALID_GRADE");
    expect(admin, patch("/api/admin/pairs/{id}/grades/{u}", id, 999_999).contentType(MediaType.APPLICATION_JSON).content("{\"grade\":\"4\"}"), status().isNotFound(), "STUDENT_NOT_FOUND");
    expect(admin, post("/api/admin/pairs").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("group", "M-1", "language", "JAVA", "startsAt", start.toString(),
        "endsAt", start.plusSeconds(60).toString(), "grades", List.of(Map.of("userId", a, "grade", "отл"))))), status().isBadRequest(), "INVALID_GRADE");
  }

  @Test void studentsSeeOnlyTheDateAndGradeOfTheirPublishedPairs() throws Exception {
    String admin = login("admin", "admin-pass");
    String token = createStudent("pub-a", "Публикуемый", "S-1"); long a = studentId("pub-a");
    long b = studentRow("pub-b", "Другой", "S-1");
    Instant first = Instant.parse("2035-03-14T22:00:00Z"), second = Instant.parse("2035-03-20T08:00:00Z"); // the first is 15 March in Moscow
    earn(a, "JAVA", first, 3); earn(b, "JAVA", first, 5); earn(a, "JAVA", second, 4);
    long one = save(admin, "S-1", "JAVA", first), two = save(admin, "S-1", "JAVA", second);
    assertEquals(0, read(token, get("/api/grades").param("language", "JAVA")).path("grades").size(), "nothing is published yet");

    var published = read(admin, post("/api/admin/pairs/{id}/publish", one).contentType(MediaType.APPLICATION_JSON).content("{\"published\":true}"));
    assertTrue(published.path("published").asBoolean()); assertEquals(NOW.toString(), published.path("publishedAt").asText());
    read(admin, post("/api/admin/pairs/{id}/publish", two).contentType(MediaType.APPLICATION_JSON).content("{\"published\":true}"));
    var grades = read(token, get("/api/grades").param("language", "JAVA")).path("grades");
    assertEquals(2, grades.size());
    assertEquals("2035-03-20", grades.get(0).path("date").asText(), "newest first"); assertEquals("2035-03-15", grades.get(1).path("date").asText(), "the Moscow date");
    assertEquals("3", grades.get(1).path("grade").asText(), "the student's own grade: 3 points against the median 4");
    for (var g : grades) assertEquals(Set.of("date", "grade"), fields(g), "no points, tasks, median, percent or thresholds");
    assertEquals(Set.of("grades"), fields(read(token, get("/api/grades").param("language", "JAVA"))));
    assertEquals(0, read(token, get("/api/grades").param("language", "PYTHON")).path("grades").size());

    var unpublished = read(admin, post("/api/admin/pairs/{id}/publish", two).contentType(MediaType.APPLICATION_JSON).content("{\"published\":false}"));
    assertFalse(unpublished.path("published").asBoolean()); assertTrue(unpublished.path("publishedAt").isNull());
    assertEquals(List.of("2035-03-15"), read(token, get("/api/grades").param("language", "JAVA")).path("grades").findValuesAsText("date"));
    expect(admin, post("/api/admin/pairs/{id}/publish", one).contentType(MediaType.APPLICATION_JSON).content("{\"published\":\"yes\"}"), status().isBadRequest(), "INVALID_PUBLISHED");

    // Admin-only: a student gets FORBIDDEN on every teacher endpoint, the teacher has no own grades.
    for (var request : List.<MockHttpServletRequestBuilder>of(get("/api/admin/pairs"), get("/api/admin/pairs/{id}", one), get("/api/admin/pairs/course").param("group", "S-1"),
        get("/api/admin/pairs/journal").param("group", "S-1"), post("/api/admin/pairs/{id}/recalculate", one), delete("/api/admin/pairs/{id}", one),
        post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("S-1", "JAVA", first.toString(), first.plusSeconds(60).toString())),
        post("/api/admin/pairs/{id}/publish", one).contentType(MediaType.APPLICATION_JSON).content("{\"published\":false}"),
        patch("/api/admin/pairs/{id}/grades/{u}", one, a).contentType(MediaType.APPLICATION_JSON).content("{\"grade\":\"5\"}")))
      expect(token, request, status().isBadRequest(), "FORBIDDEN");
    expect(admin, get("/api/grades"), status().isBadRequest(), "FORBIDDEN");
    assertEquals("3", db.queryForObject("select grade from pair_grades where pair_id=? and user_id=?", String.class, one, a));
  }

  @Test void theJournalListsAndDeletion() throws Exception {
    String admin = login("admin", "admin-pass");
    long a = studentRow("jr-a", "Аркадий", "J-1"), b = studentRow("jr-b", "Белла", "J-1"), moved = studentRow("jr-d", "Гена", "J-1");
    Instant p1 = Instant.parse("2036-02-04T08:00:00Z"), p2 = Instant.parse("2036-02-11T08:00:00Z"), p3 = Instant.parse("2036-02-18T08:00:00Z");
    earn(a, "JAVA", p1, 10); earn(b, "JAVA", p1, 5); earn(moved, "JAVA", p1, 0); // median 5: 5, 4, 2
    earn(b, "JAVA", p2, 3);                                                       // median 3: н, 4, н
    earn(a, "JAVA", p3, 2); earn(b, "JAVA", p3, 6); earn(moved, "JAVA", p3, 4);   // median 4: 2, 5, 4
    long one = save(admin, "J-1", "JAVA", p1), two = save(admin, "J-1", "JAVA", p2), three = save(admin, "J-1", "JAVA", p3);
    read(admin, patch("/api/admin/pairs/{id}/grades/{u}", three, a).contentType(MediaType.APPLICATION_JSON).content("{\"grade\":\"3\"}"));
    read(admin, post("/api/admin/pairs/{id}/publish", two).contentType(MediaType.APPLICATION_JSON).content("{\"published\":true}"));
    studentRow("jr-c", "Вадим", "J-1"); // joined after three pairs
    long four = save(admin, "J-1", "JAVA", p3.plusSeconds(6000)); // nobody worked
    db.update("update users set group_name='J-2' where id=?", moved); // left the group: the results stay in its journal

    var journal = read(admin, get("/api/admin/pairs/journal").param("group", "J-1").param("language", "JAVA"));
    assertEquals("J-1", journal.path("group").asText()); assertEquals("JAVA", journal.path("language").asText());
    assertEquals(List.of(one, two, three, four), journal.path("pairs").findValues("id").stream().map(JsonNode::asLong).toList(), "oldest first");
    assertEquals(List.of(false, true, false, false), journal.path("pairs").findValues("published").stream().map(JsonNode::asBoolean).toList());
    var students = journal.path("students");
    assertEquals(List.of("jr-a", "jr-b", "jr-c", "jr-d"), students.findValuesAsText("login"));
    var rowA = students.get(0);
    assertEquals(Arrays.asList("5", "н", "3", "н"), strings(rowA.path("grades"))); assertEquals(List.of(false, false, true, false), booleans(rowA.path("manual")));
    assertEquals(4.0, rowA.path("average").asDouble()); assertEquals(2, rowA.path("absences").asInt());
    assertEquals(Arrays.asList("4", "4", "5", "н"), strings(students.get(1).path("grades"))); assertEquals(4.33, students.get(1).path("average").asDouble()); assertEquals(1, students.get(1).path("absences").asInt());
    assertEquals(Arrays.asList(null, null, null, "н"), strings(students.get(2).path("grades"))); assertTrue(students.get(2).path("average").isNull()); assertEquals(1, students.get(2).path("absences").asInt());
    assertEquals(Arrays.asList("2", "н", "4", "н"), strings(students.get(3).path("grades"))); assertEquals(3.0, students.get(3).path("average").asDouble()); assertEquals(2, students.get(3).path("absences").asInt());
    assertEquals("JAVA", read(admin, get("/api/admin/pairs/journal").param("group", "J-1")).path("language").asText(), "the group's course by default");

    var list = read(admin, get("/api/admin/pairs").param("group", "J-1").param("language", "JAVA")).path("pairs");
    assertEquals(List.of(four, three, two, one), list.findValues("id").stream().map(JsonNode::asLong).toList(), "newest first");
    for (var p : list) assertTrue(p.path("rows").isMissingNode(), "a list has no rows");
    assertEquals(Map.of("н", 0, "2", 0, "3", 1, "4", 1, "5", 1), json.convertValue(list.get(1).path("counts"), Map.class));
    assertEquals(0, read(admin, get("/api/admin/pairs").param("group", "J-1").param("language", "PYTHON")).path("pairs").size());

    assertTrue(read(admin, delete("/api/admin/pairs/{id}", four)).path("deleted").asBoolean());
    assertEquals(0, count("select count(*) from pair_grades where pair_id=?", four));
    expect(admin, get("/api/admin/pairs/{id}", four), status().isNotFound(), "PAIR_NOT_FOUND");
    expect(admin, post("/api/admin/pairs/{id}/recalculate", four), status().isNotFound(), "PAIR_NOT_FOUND");

    // Deleting a student deletes their results.
    mvc.perform(delete("/api/admin/students/{id}", moved).cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON).content("{\"confirmLogin\":\"jr-d\"}")).andExpect(status().isOk());
    assertEquals(0, count("select count(*) from pair_grades where user_id=?", moved));
    assertEquals(2, read(admin, get("/api/admin/pairs/{id}", three)).path("rows").size());
  }

  @Test void theGroupsCourseAndValidation() throws Exception {
    String admin = login("admin", "admin-pass");
    long a = studentRow("crs-a", "a", "C-1"), b = studentRow("crs-b", "b", "C-1"), c = studentRow("crs-c", "c", "C-1");
    Instant t = Instant.parse("2037-01-10T08:00:00Z");
    lesson(a, "PYTHON", t); lesson(b, "PYTHON", t); lesson(c, "JAVA", t); lesson(c, "JAVA", t.plusSeconds(60)); lesson(c, "JAVA", t.plusSeconds(120));
    assertEquals("PYTHON", read(admin, get("/api/admin/pairs/course").param("group", " C-1 ")).path("language").asText(), "two members of three study Python");
    studentRow("crs-d", "d", "C-2");
    assertEquals("JAVA", read(admin, get("/api/admin/pairs/course").param("group", "C-2")).path("language").asText(), "nothing studied yet");
    expect(admin, get("/api/admin/pairs/course").param("group", "Нет такой"), status().isNotFound(), "GROUP_NOT_FOUND");
    expect(admin, get("/api/admin/pairs/course"), status().isNotFound(), "GROUP_NOT_FOUND");
    expect(admin, get("/api/admin/pairs/journal").param("group", "Нет такой"), status().isNotFound(), "GROUP_NOT_FOUND");

    String start = "2037-01-10T11:00:00+03:00";
    read(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("C-1", "PYTHON", start, "2037-01-10T17:00:00+03:00"))); // exactly 6 hours
    for (String end : List.of("2037-01-10T17:00:01+03:00", "2037-01-10T11:00:00+03:00", "2037-01-10T10:00:00+03:00", "вчера"))
      expect(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("C-1", "PYTHON", start, end)), status().isBadRequest(), "INVALID_WINDOW");
    expect(admin, post("/api/admin/pairs").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("group", "C-1", "language", "JAVA", "startsAt", start))), status().isBadRequest(), "INVALID_WINDOW");
    expect(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("C-1", "COBOL", start, "2037-01-10T12:00:00+03:00")), status().isBadRequest(), "UNKNOWN_LANGUAGE");
    expect(admin, post("/api/admin/pairs/preview").contentType(MediaType.APPLICATION_JSON).content(body("Нет такой", "JAVA", start, "2037-01-10T12:00:00+03:00")), status().isNotFound(), "GROUP_NOT_FOUND");
    expect(admin, post("/api/admin/pairs").contentType(MediaType.APPLICATION_JSON).content(body("Нет такой", "JAVA", start, "2037-01-10T12:00:00+03:00")), status().isNotFound(), "GROUP_NOT_FOUND");
    expect(admin, get("/api/admin/pairs/{id}", 987_654), status().isNotFound(), "PAIR_NOT_FOUND");
    expect(admin, delete("/api/admin/pairs/{id}", 987_654), status().isNotFound(), "PAIR_NOT_FOUND");
    expect(admin, get("/api/admin/pairs").param("language", "COBOL"), status().isBadRequest(), "UNKNOWN_LANGUAGE");
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
      db.update("insert into pair_grades(pair_id,user_id,attended,points,tasks_json,hard,auto_grade,grade) values(?,?,?,?,'{}',?,'4','4')", pair, user, attended ? 1 : 0, p, hard ? 1 : 0);
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
  private static List<String> strings(JsonNode array) { var list = new ArrayList<String>(); for (var x : array) list.add(x.isNull() ? null : x.asText()); return list; }
  private static List<Boolean> booleans(JsonNode array) { var list = new ArrayList<Boolean>(); for (var x : array) list.add(x.asBoolean()); return list; }

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
