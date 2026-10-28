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
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;

/**
 * The integrative task of a topic's 3rd iteration (IntegrativeTasks) and «Тренировочная аттестация» (AttestationPractice):
 * when the integrative task is given and what it credits, where it is never given; the practice's availability and level
 * by the passed prefix, the waiting lesson task, the closed assistant while the timer runs, the result, the order of its
 * stories, and that a practice never moves iterations or counts as a re-take; the loader of both pools. Piston and the
 * LLM are stubbed; the clock is the test's. Every test uses students of its own; the pools are emptied before each test.
 */
@SpringBootTest
@AutoConfigureMockMvc
class IntegrativeAndPracticeIntegrationTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json; @Autowired AttestationBank bank;
  @MockBean PistonCodeRunner runner;
  @MockBean LlmTutor tutor;
  @MockBean LearningContentGenerator generator;
  @MockBean Clock clock;
  static final Instant START = Instant.parse("2041-03-01T10:00:00Z");
  volatile Instant now = START;

  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:prep-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
    p.add("app.task-audit.enabled", () -> "false");
    p.add("app.lesson.idle-close.enabled", () -> "false");
    p.add("app.board.auto-finish.enabled", () -> "false");
  }
  @BeforeEach void prepare() {
    db.update("update users set password_hash=? where login='admin'", new BCryptPasswordEncoder().encode("admin-pass"));
    db.update("update tasks set active=0 where mode in ('INTEGRATIVE','ATTESTATION_PRACTICE')");
    now = START;
    when(clock.instant()).thenAnswer(i -> now);
    when(clock.getZone()).thenReturn(ZoneOffset.UTC);
    when(runner.configured()).thenReturn(true);
    when(runner.status(any(Language.class))).thenReturn(new PistonCodeRunner.RuntimeStatus(true, "READY", "17.0.1"));
    when(runner.run(any(Language.class), anyString(), anyString())).thenAnswer(call -> ((String) call.getArgument(1)).contains("WRONG")
        ? new PistonCodeRunner.Run(false, "Неверный вывод программы", PistonCodeRunner.Outcome.CHECK_FAILED)
        : new PistonCodeRunner.Run(true, "Решение прошло скрытые проверки", PistonCodeRunner.Outcome.PASSED));
    when(tutor.status(anyLong())).thenReturn(new LlmStatus(false, false, false, "DISABLED", "gpt-6-luna"));
    when(tutor.reply(anyLong(), any(TutorContext.class), anyString())).thenReturn("Подумай о первом шаге.");
  }

  // ---------------------------------------------------------------- the integrative 3rd iteration

  @Test void theThirdIterationOfATopicOutsideBlockZeroIsAnIntegrativeTaskThatMastersTheTopic() throws Exception {
    String topic = topicOfBlock(3, 0);
    long ordinary = task(topic, 3, "ordinary " + topic);
    long a = poolTask(AttestationBank.INTEGRATIVE, topic, "it-a"), b = poolTask(AttestationBank.INTEGRATIVE, topic, "it-b");
    String token = student("it-third"); long user = studentId("it-third");
    thirdIterationDue(user, topic);
    int lesson = start(token);
    var next = read(token, get("/api/learning/next"));
    long given = next.path("task").path("id").asLong();
    assertTrue(given == a || given == b, "the integrative pool, not the ordinary task " + ordinary);
    assertTrue(next.path("task").path("integrative").asBoolean()); assertFalse(next.path("task").path("hard").asBoolean());
    assertEquals(topic, next.path("skill").path("code").asText());
    assertTrue(attempt(token, given, "public class Solution {}").path("passed").asBoolean());
    var skill = db.queryForMap("select completed_iterations,mastered from student_skills where user_id=? and skill_code=?", user, topic);
    assertEquals(3, ((Number) skill.get("completed_iterations")).intValue(), "it is the 3rd iteration"); assertEquals(1, ((Number) skill.get("mastered")).intValue());
    long lessonId = lessonId(user, lesson);
    assertEquals(1, count("select count(*) from skill_iterations where user_id=? and skill_code=? and iteration_number=3 and lesson_id=?", user, topic, lessonId));
    String admin = login("admin", "admin-pass");
    var detail = detailTask(admin, user, lessonId, given);
    assertTrue(detail.path("integrative").asBoolean()); assertFalse(detail.path("practice").asBoolean()); assertTrue(detail.path("retakeSkill").isNull());

    // A revoked credit is redone as for any task: the next lesson starts with it.
    finish(token, lesson);
    read(admin, post("/api/admin/students/{id}/lessons/{lessonId}/tasks/{taskId}/revoke", user, lessonId, given));
    start(token);
    var redo = read(token, get("/api/learning/next")).path("task");
    assertEquals(given, redo.path("id").asLong()); assertTrue(redo.path("redo").asBoolean()); assertTrue(redo.path("integrative").asBoolean());
  }

  @Test void neighboursGetDifferentIntegrativeStories() throws Exception {
    String topic = topicOfBlock(3, 1);
    for (String slug : List.of("nb-a", "nb-b", "nb-c")) poolTask(AttestationBank.INTEGRATIVE, topic, slug);
    var first = new HashSet<Long>();
    for (int i = 1; i <= 6; i++) {
      String token = student("it-neighbour-" + i); thirdIterationDue(studentId("it-neighbour-" + i), topic);
      int lesson = start(token); long task = nextTaskId(token); finish(token, lesson);
      start(token);
      assertEquals(task, nextTaskId(token), "the same student gets the same story again");
      first.add(task);
    }
    assertTrue(first.size() > 1, "six students do not all get the same story: " + first);
  }

  @Test void blockZeroAndAPoolWithoutAnUnsolvedTaskKeepTheOrdinaryTask() throws Exception {
    String early = topicOfBlock(0, 1), later = topicOfBlock(3, 2);
    long earlyTask = task(early, 3, "ordinary " + early), laterTask = task(later, 3, "ordinary " + later);
    poolTask(AttestationBank.INTEGRATIVE, early, "b0-a");
    String token = student("it-block0"); thirdIterationDue(studentId("it-block0"), early);
    start(token);
    var next = read(token, get("/api/learning/next")).path("task");
    assertEquals(earlyTask, next.path("id").asLong(), "block 0 keeps its ordinary tasks"); assertFalse(next.path("integrative").asBoolean());

    // The pool has nothing for the topic: as before.
    String empty = student("it-empty"); thirdIterationDue(studentId("it-empty"), later);
    start(empty);
    assertEquals(laterTask, nextTaskId(empty));
    // Every integrative task of the topic solved: as before too.
    long solved = poolTask(AttestationBank.INTEGRATIVE, later, "b1-solved");
    String all = student("it-solved"); long allId = studentId("it-solved"); thirdIterationDue(allId, later);
    db.update("insert into successful_task_credit(user_id,task_id) values(?,?)", allId, solved);
    start(all);
    assertEquals(laterTask, nextTaskId(all));
  }

  @Test void integrativeTasksAreNotGivenInTheFirstTwoIterationsInReTakesOrAtTheBoard() throws Exception {
    String topic = topicOfBlock(3, 3);
    long integrative = poolTask(AttestationBank.INTEGRATIVE, topic, "nt-a");
    for (int d = 1; d <= 3; d++) task(topic, d, "ordinary " + topic + " " + d);
    // The 1st iteration (three tasks) and the 2nd (two) are ordinary tasks.
    String first = student("it-first"); masteredExcept(studentId("it-first"), topic);
    start(first);
    for (int i = 0; i < 3; i++) { long t = nextTaskId(first); assertNotEquals(integrative, t); assertTrue(attempt(first, t, "public class Solution {}").path("passed").asBoolean()); }
    String second = student("it-second"); long secondId = studentId("it-second"); masteredExcept(secondId, topic);
    db.update("insert into student_skills(user_id,skill_code,completed_iterations,first_iteration_lesson_number) values(?,?,1,-1)", secondId, topic);
    start(second);
    for (int i = 0; i < 2; i++) { long t = nextTaskId(second); assertNotEquals(integrative, t); assertTrue(attempt(second, t, "public class Solution {}").path("passed").asBoolean()); }
    assertEquals(2, count("select completed_iterations from student_skills where user_id=? and skill_code=?", secondId, topic));

    // A re-take of the mastered topic takes the bank, never the integrative pool.
    String retake = student("it-retake"); masteredExcept(studentId("it-retake"), "-");
    read(retake, post("/api/retakes").contentType(MediaType.APPLICATION_JSON).content("{\"language\":\"JAVA\",\"skillCode\":\"" + topic + "\"}"));
    for (int i = 0; i < 3; i++) {
      var next = read(retake, get("/api/learning/next"));
      if (next.path("task").isNull() || next.path("retake").isMissingNode()) break;
      assertNotEquals(integrative, next.path("task").path("id").asLong());
      attempt(retake, next.path("task").path("id").asLong(), "public class Solution {}");
    }
    assertEquals(0, count("select count(*) from lesson_tasks where task_id=?", integrative));

    // At the board: the only reached topic has only an integrative task — no task for «Напиши код».
    String boardTopic = topicOfBlock(4, 0);
    poolTask(AttestationBank.INTEGRATIVE, boardTopic, "nt-board");
    String board = student("it-board"); long boardId = studentId("it-board");
    db.update("insert into student_skills(user_id,skill_code,completed_iterations) values(?,?,1)", boardId, boardTopic);
    db.update("insert into app_settings(key,value) values('board_student_start','true') on conflict(key) do update set value=excluded.value");
    String admin = login("admin", "admin-pass");
    long test = read(admin, post("/api/admin/board/call").contentType(MediaType.APPLICATION_JSON).content("{\"userId\":" + boardId + ",\"language\":\"JAVA\",\"kinds\":[\"code\"]}")).path("id").asLong();
    expect(board, post("/api/board/tests/{id}/start", test).header("X-Board-Device", "board-pc"), 400, "NO_BOARD_TASK");
  }

  // ---------------------------------------------------------------- «Тренировочная аттестация»

  @Test void thePracticeOpensByThePassedPrefixAtTheHighestLevelOfThePool() throws Exception {
    var course = course();
    String token = student("pr-level"); long user = studentId("pr-level");
    var python = read(token, get("/api/progress").param("language", "PYTHON")).path("attestationPractice");
    assertFalse(python.path("available").asBoolean()); assertTrue(python.path("needTopics").isNull(), "no pool: nothing to count down to"); assertEquals(10, python.path("minutes").asInt());
    poolTask(AttestationBank.PRACTICE, course.get(5), "lv-6"); poolTask(AttestationBank.PRACTICE, course.get(8), "lv-9");
    var closed = offer(token);
    assertFalse(closed.path("available").asBoolean()); assertEquals(6, closed.path("needTopics").asInt()); assertTrue(closed.path("levelTopics").isNull()); assertTrue(closed.path("levelTitle").isNull());
    start(token);
    var refused = expect(token, startPractice(), 400, "PRACTICE_NOT_AVAILABLE");
    assertEquals("Тренировочная аттестация откроется, когда пройдёшь ещё 6 тем по порядку", refused.path("message").asText());
    // Passed: an iteration, mastery or the diagnostic — in course order, without a gap.
    iteration(user, course.get(0)); master(user, course.get(1)); confirm(user, course.get(2)); iteration(user, course.get(3)); iteration(user, course.get(4));
    assertEquals(1, offer(token).path("needTopics").asInt());
    assertEquals("Тренировочная аттестация откроется, когда пройдёшь ещё 1 тему по порядку", expect(token, startPractice(), 400, "PRACTICE_NOT_AVAILABLE").path("message").asText());
    iteration(user, course.get(5));
    var six = offer(token);
    assertTrue(six.path("available").asBoolean()); assertEquals(6, six.path("levelTopics").asInt()); assertEquals(title(course.get(5)), six.path("levelTitle").asText()); assertTrue(six.path("needTopics").isNull());
    iteration(user, course.get(7)); iteration(user, course.get(8));
    assertEquals(6, offer(token).path("levelTopics").asInt(), "topic 7 is a gap: topics 8 and 9 do not count yet");
    iteration(user, course.get(6));
    assertEquals(9, offer(token).path("levelTopics").asInt(), "the highest level within the prefix");
    assertEquals(0, offer(token).path("history").size());
  }

  @Test void aPracticePausesTheLessonTaskClosesTheAssistantWhileTheTimerRunsAndMovesNoProgress() throws Exception {
    var course = course();
    String token = student("pr-flow"); long user = studentId("pr-flow");
    String own = course.get(9); masteredExcept(user, own);
    // The level's topic passed by one iteration, its 2nd not due yet: a credited task of it would move its progress.
    db.update("update student_skills set completed_iterations=1,mastered=0,first_iteration_lesson_number=5 where user_id=? and skill_code=?", user, course.get(8));
    long waiting = task(own, 1, "waiting " + own);
    long practiceTask = poolTask(AttestationBank.PRACTICE, course.get(8), "fl-9");
    int lesson = start(token);
    assertEquals(waiting, nextTaskId(token));
    String skillsBefore = skills(user); int iterationsBefore = count("select count(*) from skill_iterations where user_id=?", user);

    var practice = read(token, startPractice()).path("practice");
    long id = practice.path("id").asLong();
    assertEquals(9, practice.path("levelTopics").asInt()); assertEquals(title(course.get(8)), practice.path("levelTitle").asText());
    assertEquals(10, practice.path("minutes").asInt()); assertEquals(600, practice.path("secondsLeft").asInt());
    assertEquals(START.toString(), practice.path("startedAt").asText()); assertEquals(START.plusSeconds(600).toString(), practice.path("deadlineAt").asText());
    assertFalse(practice.path("finished").asBoolean()); assertFalse(practice.path("passed").asBoolean()); assertTrue(practice.path("result").isNull()); assertTrue(practice.path("seconds").isNull());
    assertEquals(id, read(token, startPractice()).path("practice").path("id").asLong(), "starting again gives the open one");

    var next = read(token, get("/api/learning/next"));
    assertEquals(practiceTask, next.path("task").path("id").asLong(), "the practice's task; the lesson's task waits");
    assertEquals(id, next.path("practice").path("id").asLong()); assertTrue(next.path("retake").isMissingNode()); assertFalse(next.path("task").path("integrative").asBoolean());
    // The assistant and a re-take wait for the practice.
    var chat = expect(token, chat(), 400, "PRACTICE_RUNNING");
    assertEquals("Идёт тренировочная аттестация — помощник откроется, когда выйдет время", chat.path("message").asText());
    expect(token, post("/api/retakes").contentType(MediaType.APPLICATION_JSON).content("{\"language\":\"JAVA\",\"skillCode\":\"" + course.get(0) + "\"}"), 400, "PRACTICE_RUNNING");
    expect(token, post("/api/attempts").contentType(MediaType.APPLICATION_JSON).content("{\"taskId\":" + waiting + ",\"sourceCode\":\"public class Solution {}\"}"), 400, "TASK_NOT_IN_LESSON");

    now = START.plusSeconds(200);
    assertEquals(400, read(token, get("/api/learning/next")).path("practice").path("secondsLeft").asInt(), "the server counts the time");
    assertFalse(attempt(token, practiceTask, "public class Solution {} // WRONG").path("passed").asBoolean());
    var solved = attempt(token, practiceTask, "public class Solution {}");
    assertTrue(solved.path("passed").asBoolean()); assertTrue(solved.path("retake").isNull());
    assertEquals("IN_TIME", solved.path("practice").path("result").asText()); assertEquals(200, solved.path("practice").path("seconds").asInt());
    assertTrue(solved.path("practice").path("passed").asBoolean()); assertEquals(0, solved.path("practice").path("secondsLeft").asInt());
    read(token, chat()); // solved: the assistant is open

    var after = read(token, get("/api/learning/next"));
    assertEquals(waiting, after.path("task").path("id").asLong(), "the waiting task comes back");
    assertTrue(after.path("practice").isMissingNode());
    var done = after.path("practiceDone");
    assertEquals(id, done.path("id").asLong()); assertTrue(done.path("finished").asBoolean()); assertEquals("IN_TIME", done.path("result").asText()); assertEquals(200, done.path("seconds").asInt());
    assertTrue(read(token, get("/api/learning/next")).path("practiceDone").isMissingNode(), "practiceDone comes once");

    // Solved and credited, but iterations, mastery and the re-take counters stay.
    assertEquals(skillsBefore, skills(user)); assertEquals(iterationsBefore, count("select count(*) from skill_iterations where user_id=?", user));
    var progress = read(token, get("/api/progress"));
    assertEquals(1, progress.path("solvedTasks").asInt()); assertEquals(0, progress.path("retakes").size(), "a practice is not a re-take");
    var history = progress.path("attestationPractice").path("history");
    assertEquals(1, history.size()); assertEquals(id, history.get(0).path("id").asLong()); assertEquals("IN_TIME", history.get(0).path("result").asText());
    assertEquals(200, history.get(0).path("seconds").asInt()); assertEquals(9, history.get(0).path("levelTopics").asInt()); assertEquals("Сюжет fl-9", history.get(0).path("taskTitle").asText());
    assertEquals(START.toString(), history.get(0).path("startedAt").asText());
    String admin = login("admin", "admin-pass");
    var card = read(admin, get("/api/admin/students/{id}", user));
    assertEquals(0, card.path("retakesByLanguage").path("JAVA").asInt());
    assertEquals("IN_TIME", card.path("practiceByLanguage").path("JAVA").get(0).path("result").asText()); assertEquals(0, card.path("practiceByLanguage").path("PYTHON").size());
    long lessonId = lessonId(user, lesson);
    var chip = detailTask(admin, user, lessonId, practiceTask);
    assertTrue(chip.path("practice").asBoolean()); assertTrue(chip.path("retakeSkill").isNull()); assertFalse(chip.path("integrative").asBoolean());
    assertFalse(detailTask(admin, user, lessonId, waiting).path("practice").asBoolean());
  }

  @Test void afterTheDeadlineTheAssistantOpensAndASolutionIsLate() throws Exception {
    var course = course();
    String token = student("pr-late"); long user = studentId("pr-late");
    masteredExcept(user, course.get(10)); task(course.get(10), 1, "waiting late");
    long practiceTask = poolTask(AttestationBank.PRACTICE, course.get(8), "late-9");
    start(token); nextTaskId(token);
    read(token, startPractice());
    now = START.plusSeconds(599);
    expect(token, chat(), 400, "PRACTICE_RUNNING");
    now = START.plusSeconds(601);
    var open = read(token, get("/api/learning/next")).path("practice");
    assertEquals(0, open.path("secondsLeft").asInt()); assertFalse(open.path("finished").asBoolean(), "nothing closes when the time is up");
    read(token, chat());
    assertEquals("LATE", attempt(token, practiceTask, "public class Solution {}").path("practice").path("result").asText());
    var done = read(token, get("/api/learning/next")).path("practiceDone");
    assertEquals("LATE", done.path("result").asText()); assertEquals(601, done.path("seconds").asInt());
  }

  @Test void finishingAPracticeLeavesItUnsolvedAndTheLessonEndEndsItToo() throws Exception {
    var course = course();
    String token = student("pr-quit"); long user = studentId("pr-quit");
    masteredExcept(user, course.get(11)); long waiting = task(course.get(11), 1, "waiting quit");
    poolTask(AttestationBank.PRACTICE, course.get(8), "q-a"); poolTask(AttestationBank.PRACTICE, course.get(8), "q-b");
    int lesson = start(token); nextTaskId(token);
    long first = read(token, startPractice()).path("practice").path("id").asLong();
    long firstTask = nextTaskId(token);
    var done = read(token, post("/api/attestation-practice/{id}/finish", first)).path("practice");
    assertTrue(done.path("finished").asBoolean()); assertEquals("NOT_SOLVED", done.path("result").asText()); assertFalse(done.path("passed").asBoolean());
    assertTrue(done.path("seconds").isNull()); assertEquals(0, done.path("secondsLeft").asInt());
    var next = read(token, get("/api/learning/next"));
    assertEquals(waiting, next.path("task").path("id").asLong()); assertTrue(next.path("practice").isMissingNode());
    long lessonId = lessonId(user, lesson);
    assertEquals(1, count("select count(*) from lesson_tasks where lesson_id=? and task_id=? and replaced_at is not null", lessonId, firstTask), "the unsolved practice task left the lesson");
    read(token, chat());
    expect(token, post("/api/retakes/{id}/finish", first), 400, "RETAKE_NOT_FOUND");

    long second = read(token, startPractice()).path("practice").path("id").asLong();
    assertNotEquals(firstTask, nextTaskId(token), "a story not in this lesson yet");
    finish(token, lesson);
    var history = read(token, get("/api/progress")).path("attestationPractice").path("history");
    assertEquals(List.of(second, first), List.of(history.get(0).path("id").asLong(), history.get(1).path("id").asLong()), "newest first");
    assertEquals("NOT_SOLVED", history.get(0).path("result").asText(), "the lesson ended it");
    assertEquals("LESSON", db.queryForObject("select finish_reason from topic_retakes where id=?", String.class, second));
    // Deleting the student takes his practices (and re-takes) with his lessons.
    read(login("admin", "admin-pass"), delete("/api/admin/students/{id}", user).contentType(MediaType.APPLICATION_JSON).content("{\"confirmLogin\":\"pr-quit\"}"));
    assertEquals(0, count("select count(*) from topic_retakes where user_id=?", user));
  }

  @Test void aPracticeTakesUnsolvedStoriesOfTheLevelThenLowerLevelsThenTheOneSolvedLongestAgo() throws Exception {
    var course = course();
    String token = student("pr-order"); long user = studentId("pr-order");
    masteredExcept(user, course.get(12)); task(course.get(12), 1, "waiting order");
    long low = poolTask(AttestationBank.PRACTICE, course.get(5), "or-6");
    long a = poolTask(AttestationBank.PRACTICE, course.get(8), "or-9a"), b = poolTask(AttestationBank.PRACTICE, course.get(8), "or-9b");
    int lesson = start(token); nextTaskId(token);
    long first = solvePractice(token), second = solvePractice(token);
    assertEquals(Set.of(a, b), Set.of(first, second), "the level's stories first");
    assertEquals(low, solvePractice(token), "every story of the level solved: a lower level");
    expect(token, startPractice(), 400, "NO_PRACTICE_TASK");
    finish(token, lesson);
    db.update("update submissions set created_at='2000-01-01 10:00:00' where task_id=? and passed=1", second);
    start(token); nextTaskId(token);
    assertEquals(second, solvePractice(token), "all solved: the level's story solved longest ago");
    assertEquals(4, read(token, get("/api/progress")).path("attestationPractice").path("history").size());
  }

  @Test void startingAPracticeEndsAnOpenReTakeAndItsWaitingTaskWaitsForThePractice() throws Exception {
    var course = course();
    String token = student("pr-retake"); long user = studentId("pr-retake");
    masteredExcept(user, course.get(13)); long waiting = task(course.get(13), 1, "waiting retake");
    for (int d = 1; d <= 3; d++) task(course.get(3), d, "retake bank " + d);
    long practiceTask = poolTask(AttestationBank.PRACTICE, course.get(8), "rt-9");
    start(token); assertEquals(waiting, nextTaskId(token));
    long retake = read(token, post("/api/retakes").contentType(MediaType.APPLICATION_JSON).content("{\"language\":\"JAVA\",\"skillCode\":\"" + course.get(3) + "\"}")).path("retake").path("id").asLong();
    long retakeTask = nextTaskId(token);
    read(token, startPractice());
    assertNotNull(db.queryForObject("select finished_at from topic_retakes where id=?", String.class, retake), "the open re-take ends first");
    var next = read(token, get("/api/learning/next"));
    assertEquals(practiceTask, next.path("task").path("id").asLong()); assertTrue(next.path("retake").isMissingNode()); assertTrue(next.path("retakeDone").isMissingNode());
    attempt(token, practiceTask, "public class Solution {}");
    var back = read(token, get("/api/learning/next"));
    assertEquals(waiting, back.path("task").path("id").asLong(), "the lesson's own task comes back, not the re-take's " + retakeTask);
    assertEquals("IN_TIME", back.path("practiceDone").path("result").asText());
  }

  // ---------------------------------------------------------------- the pools

  @Test void bothPoolsAreLoadedByKeyWithTheirModeAndRetireWhatLeftTheirBank() throws Exception {
    String topic = course().get(8);
    var integrative = poolJson("integ:ld-one", topic); var practice = poolJson("practice:ld-two", topic);
    bank.load(AttestationBank.INTEGRATIVE, bankOf(integrative)); bank.load(AttestationBank.INTEGRATIVE, bankOf(integrative));
    var rows = db.queryForList("select id,mode,active,source,reference_code from tasks where external_key='integ:ld-one'");
    assertEquals(1, rows.size(), "updated by key, not duplicated");
    assertEquals("INTEGRATIVE", rows.getFirst().get("mode")); assertEquals(1, ((Number) rows.getFirst().get("active")).intValue()); assertEquals("CURATED", rows.getFirst().get("source"));
    assertEquals(topic, db.queryForObject("select skill_code from task_target_skills where task_id=?", String.class, rows.getFirst().get("id")));
    bank.load(AttestationBank.PRACTICE, bankOf(practice, integrative));
    assertEquals("ATTESTATION_PRACTICE", db.queryForObject("select mode from tasks where external_key='practice:ld-two'", String.class));
    assertEquals("INTEGRATIVE", db.queryForObject("select mode from tasks where external_key='integ:ld-one'", String.class), "a key of another pool is skipped");
    bank.load(AttestationBank.INTEGRATIVE, json.readTree("{\"tasks\":[]}"));
    assertEquals(0, count("select active from tasks where external_key='integ:ld-one'"), "left its bank: deactivated");
    assertEquals(1, count("select active from tasks where external_key='practice:ld-two'"), "the other pool stays");
    // The shipped files load at startup: every pool's tasks are active again in their own mode.
    bank.run(null);
    assertTrue(count("select count(*) from tasks where mode='INTEGRATIVE' and active=1 and external_key like 'integ:%'") > 0, "the integrative pool is loaded");
    assertTrue(count("select count(*) from tasks where mode='ATTESTATION_PRACTICE' and active=1 and external_key like 'practice:%'") > 0, "the practice pool is loaded");
    assertTrue(count("select count(*) from tasks where mode='ATTESTATION' and active=1") > 0, "the attestation pool is loaded as before");
  }

  // ---------------------------------------------------------------- helpers

  /** Java topics in course order (block, topic). */
  private List<String> course() { return db.queryForList("select code from skills where language='JAVA' order by block_no,sort_order,code", String.class); }
  /** The n-th Java topic of a block (course order). */
  private String topicOfBlock(int block, int n) { return db.queryForList("select code from skills where language='JAVA' and block_no=? order by sort_order,code", String.class, block).get(n); }
  private String title(String skill) { return db.queryForObject("select title from skills where code=?", String.class, skill); }
  private long task(String skill, int difficulty, String title) {
    long id = db.queryForObject("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,difficulty) values(?,?,?,'','class TestHarness {}','TestHarness.java','JAVA',?) returning id", Long.class, skill, title, title, difficulty);
    db.update("insert into task_target_skills(task_id,skill_code) values(?,?)", id, skill);
    return id;
  }
  /** A task of a pool as AttestationBank stores it: one story, key <prefix><slug>. */
  private long poolTask(AttestationBank.Pool pool, String skill, String slug) {
    long id = db.queryForObject("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,language,difficulty,mode,source,external_key) "
        + "values(?,?,?,'','class TestHarness {}','TestHarness.java','JAVA',3,?,'CURATED',?) returning id", Long.class, skill, "Сюжет " + slug, "Шаг 1. " + slug, pool.mode(), pool.keyPrefix() + slug);
    db.update("insert into task_target_skills(task_id,skill_code) values(?,?)", id, skill);
    return id;
  }
  private JsonNode poolJson(String key, String skill) throws Exception {
    return json.readTree("{\"key\":\"" + key + "\",\"language\":\"JAVA\",\"skill\":\"" + skill + "\",\"difficulty\":3,\"title\":\"Сквозная\",\"statement\":\"s\",\"starter\":\"st\","
        + "\"testSource\":\"class TestHarness {}\",\"testFileName\":\"TestHarness.java\",\"goalJson\":\"{\\\"kind\\\":\\\"OUTPUT_TEXT\\\"}\",\"reference\":\"ref\",\"wrong\":[],\"cases\":[]}");
  }
  private JsonNode bankOf(JsonNode... tasks) { var bank = json.createObjectNode(); var list = bank.putArray("tasks"); for (var t : tasks) list.add(t); return bank; }
  /** Every topic of both courses mastered except the given ones. */
  private void masteredExcept(long user, String... open) {
    var except = Set.of(open);
    for (String code : db.queryForList("select code from skills", String.class)) if (!except.contains(code))
      db.update("insert into student_skills(user_id,skill_code,completed_iterations,mastered) values(?,?,3,1) on conflict(user_id,skill_code) do update set completed_iterations=3,mastered=1", user, code);
  }
  /** The topic's two iterations done, the 3rd due in the first lesson; every other topic mastered. */
  private void thirdIterationDue(long user, String topic) {
    masteredExcept(user, topic);
    db.update("insert into student_skills(user_id,skill_code,completed_iterations,first_iteration_lesson_number) values(?,?,2,-2)", user, topic);
  }
  private void iteration(long user, String skill) { db.update("insert into student_skills(user_id,skill_code,completed_iterations) values(?,?,1) on conflict(user_id,skill_code) do update set completed_iterations=1", user, skill); }
  private void master(long user, String skill) { db.update("insert into student_skills(user_id,skill_code,completed_iterations,mastered) values(?,?,3,1) on conflict(user_id,skill_code) do update set completed_iterations=3,mastered=1", user, skill); }
  private void confirm(long user, String skill) { db.update("insert into diagnostic_skill_results(user_id,skill_code,correct,total,confirmed) values(?,?,1,1,1) on conflict(user_id,skill_code) do update set confirmed=1", user, skill); }
  private String skills(long user) { return db.queryForList("select skill_code||':'||completed_iterations||':'||mastered||':'||iteration_successes from student_skills where user_id=? order by skill_code", String.class, user).toString(); }
  private JsonNode offer(String token) throws Exception { return read(token, get("/api/progress")).path("attestationPractice"); }
  private MockHttpServletRequestBuilder startPractice() { return post("/api/attestation-practice").contentType(MediaType.APPLICATION_JSON).content("{\"language\":\"JAVA\"}"); }
  private MockHttpServletRequestBuilder chat() { return post("/api/chat").contentType(MediaType.APPLICATION_JSON).content("{\"content\":\"Помоги\"}"); }
  /** Starts a practice, solves its task and lets the next task come back; returns the practice's task. */
  private long solvePractice(String token) throws Exception {
    read(token, startPractice()); long task = nextTaskId(token);
    assertTrue(attempt(token, task, "public class Solution {}").path("passed").asBoolean());
    assertEquals("IN_TIME", read(token, get("/api/learning/next")).path("practiceDone").path("result").asText());
    return task;
  }
  private JsonNode detailTask(String admin, long user, long lessonId, long task) throws Exception {
    for (var t : read(admin, get("/api/admin/students/{id}/lessons/{lessonId}", user, lessonId)).path("tasks")) if (t.path("id").asLong() == task) return t;
    throw new AssertionError("task " + task + " is not in lesson " + lessonId);
  }

  private String student(String login) throws Exception {
    String admin = login("admin", "admin-pass");
    read(admin, post("/api/admin/students").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login", login, "password", "student-pass", "displayName", login))));
    String token = login(login, "student-pass");
    var answers = new ArrayList<Map<String, Object>>();
    for (long q : db.queryForList("select id from diagnostic_questions where language='JAVA' order by id", Long.class)) answers.add(Map.of("questionId", q));
    read(token, post("/api/diagnostic").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("answers", answers))));
    return token;
  }
  private String login(String login, String password) throws Exception {
    return mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login", login, "password", password)))).andReturn().getResponse().getCookie("adaptive_session").getValue();
  }
  private long studentId(String login) { return db.queryForObject("select id from users where login=?", Long.class, login); }
  private int start(String token) throws Exception { return read(token, post("/api/lessons/start")).path("lesson").path("number").asInt(); }
  private long lessonId(long user, int number) { return db.queryForObject("select id from lessons where user_id=? and language='JAVA' and language_lesson_number=?", Long.class, user, number); }
  private void finish(String token, int number) throws Exception { long user = db.queryForObject("select user_id from sessions where token_hash=?", Long.class, Hashing.sha256(token)); read(token, post("/api/lessons/{id}/finish", lessonId(user, number))); }
  private long nextTaskId(String token) throws Exception { long task = read(token, get("/api/learning/next")).path("task").path("id").asLong(); assertTrue(task > 0); return task; }
  private JsonNode attempt(String token, long task, String source) throws Exception {
    return read(token, post("/api/attempts").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("taskId", task, "sourceCode", source))));
  }
  private int count(String sql, Object... args) { return db.queryForObject(sql, Integer.class, args); }
  private JsonNode read(String token, MockHttpServletRequestBuilder request) throws Exception {
    var response = mvc.perform(request.cookie(new jakarta.servlet.http.Cookie("adaptive_session", token))).andReturn().getResponse();
    assertEquals(200, response.getStatus(), response.getContentAsString());
    return json.readTree(response.getContentAsString());
  }
  private JsonNode expect(String token, MockHttpServletRequestBuilder request, int status, String error) throws Exception {
    var response = mvc.perform(request.cookie(new jakarta.servlet.http.Cookie("adaptive_session", token))).andReturn().getResponse();
    assertEquals(status, response.getStatus(), response.getContentAsString());
    var body = json.readTree(response.getContentAsString());
    assertEquals(error, body.path("error").asText());
    return body;
  }
}
