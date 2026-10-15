package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.DisposableBean;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;
import org.springframework.stereotype.Component;
import java.security.SecureRandom;
import java.text.Collator;
import java.time.*;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * «К доске»: the teacher calls a student from his laptop; the student starts the test on the classroom PC within
 * CALL; one timer of TEST for two items — a regular task to solve (`code`) and «Что выведет этот код?» (`output`). The
 * answers are autosaved; the client submits at 0, and the server finishes a test whose time is over (after GRACE) with
 * the last autosaved answers — lazily on every board request and every 15 s (BoardTestFinisher).
 * <p>After the finish the code is checked like a lesson attempt and the output compared; nothing is credited. The grade
 * by the rule, the LLM's proposal (asynchronous, a platform thread) and the pace cap give a suggested grade; the teacher
 * sets the final one. The student sees only the test itself and, later, the date, the final grade and the comment.
 * Rules: backend/README.md, «К доске».
 */
@Component
class BoardTests implements DisposableBean {
  private static final Logger log = LoggerFactory.getLogger(BoardTests.class);
  static final Duration CALL = Duration.ofMinutes(5), TEST = Duration.ofMinutes(6), GRACE = Duration.ofSeconds(15);
  /** A topic passed by practice this many days ago or less is «recent»: the code item comes from it, the output item preferably not. */
  static final int RECENT_DAYS = 14;
  /** A member is present with activity in the course within this many minutes or an open lesson. */
  static final int PRESENT_MINUTES = 60;
  /** From this block on a topic's code item is of difficulty 1 (the later topics take longer), before it of difficulty 2. */
  static final int EASY_FROM_BLOCK = 5;
  /** Runs the LLM sees; the oldest of a longer history are left out. */
  static final int LLM_RUNS = 10;
  static final int ANSWER_MAX = 10_000, COMMENT_MAX = 500, EXTEND_MAX_SECONDS = 1800;
  /** Recent finished, cancelled and expired tests stay in the teacher's «active» panel this long. */
  static final Duration ACTIVE_RECENT = Duration.ofHours(2);
  static final List<String> GRADES = List.of("2", "3", "4", "5");

  private final JdbcTemplate db; private final Clock clock; private final ObjectMapper json; private final PistonCodeRunner runner; private final TaskVerifier verifier;
  private final LearningContentGenerator generator; private final ProgressAnalytics analytics; private final PairWork pairs;
  /** Checks after a timed-out finish and the LLM assessments: platform threads (see BackgroundThreads). */
  private final ExecutorService background = Executors.newCachedThreadPool(BackgroundThreads.named("board-", 0));
  private volatile java.util.concurrent.Executor executor = background;
  /** «check:<id>» / «assess:<id>» being processed in this process, so that a test is never checked or assessed twice at once. */
  private final Set<String> processing = ConcurrentHashMap.newKeySet();
  private final Random random = new SecureRandom();

  BoardTests(JdbcTemplate db, Clock clock, ObjectMapper json, PistonCodeRunner runner, TaskVerifier verifier, LearningContentGenerator generator,
             ProgressAnalytics analytics, PairWork pairs) {
    this.db = db; this.clock = clock; this.json = json; this.runner = runner; this.verifier = verifier; this.generator = generator; this.analytics = analytics; this.pairs = pairs;
  }
  @Override public void destroy() { background.shutdownNow(); }
  /** Tests run the background work in the calling thread (an in-memory SQLite with a shared cache does not wait for locks); null — the platform threads again. */
  void runBackgroundWorkWith(java.util.concurrent.Executor executor) { this.executor = executor == null ? background : executor; }

  // ---------------------------------------------------------------- rules

  /** Both items right → 5; one right and the other partly right (the LLM's verdict) → 4; one right → 3; none → 2. */
  static int ruleGrade(boolean code, boolean output, boolean otherPartly) {
    return code && output ? 5 : code || output ? (otherPartly ? 4 : 3) : 2;
  }
  /** The highest grade the pace allows: borderline → 4, behind → 3; on track, course closed, no session date or not a member → none. */
  static Integer cap(String paceStatus) { return "BORDERLINE".equals(paceStatus) ? Integer.valueOf(4) : "BEHIND".equals(paceStatus) ? Integer.valueOf(3) : null; }
  static int suggested(int grade, Integer cap) { return cap == null ? grade : Math.min(grade, cap); }
  /** The output answer is right when it equals the expected output after CRLF → LF and without trailing newlines; spaces and case matter. */
  static boolean sameOutput(String expected, String actual) { return normalized(expected).equals(normalized(actual)); }
  private static String normalized(String text) {
    String s = (text == null ? "" : text).replace("\r\n", "\n");
    int end = s.length(); while (end > 0 && s.charAt(end - 1) == '\n') end--;
    return s.substring(0, end);
  }

  // ---------------------------------------------------------------- finishing on time

  /**
   * Expires calls whose time is over and finishes running tests past their end + GRACE with the last autosaved answers
   * (their checks run in the background); picks up checks and assessments a restart interrupted. Cheap when nothing is due.
   */
  void settle() { settle(now()); }
  void settle(Instant now) {
    int expired = db.update("update board_tests set status='EXPIRED' where status='CALLED' and call_expires_at<?", iso(now));
    if (expired > 0) log.info("{} board call(s) expired", expired);
    for (long id : db.queryForList("select id from board_tests where status='STARTED' and ends_at<?", Long.class, iso(now.minus(GRACE))))
      if (claim(id, Map.of(), now)) { log.info("Board test {} finished by the server: its time is over", id); executor.execute(() -> check(id)); }
    for (long id : db.queryForList("select id from board_tests where status='FINISHED' and results_json is null", Long.class))
      if (!processing.contains("check:" + id)) executor.execute(() -> check(id));
    for (long id : db.queryForList("select id from board_tests where status='FINISHED' and results_json is not null and json_extract(assessment_json,'$.status')='PENDING'", Long.class))
      if (!processing.contains("assess:" + id)) executor.execute(() -> assess(id));
  }

  /** STARTED → FINISHED with the given answers on top of the autosaved ones; false if another request finished it first. */
  private boolean claim(long id, Map<String, String> answers, Instant now) {
    var set = answersUpdate(answers);
    var params = new ArrayList<Object>(); params.add(iso(now)); params.addAll(set.params()); params.add(write(Map.of("status", "PENDING"))); params.add(id);
    return db.update("update board_tests set status='FINISHED',finished_at=?,answers_json=" + set.sql() + ",assessment_json=? where id=? and status='STARTED'", params.toArray()) > 0;
  }
  private record JsonSet(String sql, List<Object> params) {}
  /** json_set over answers_json for the fields given (code, output); the others keep their saved value. */
  private static JsonSet answersUpdate(Map<String, String> answers) {
    var sql = new StringBuilder("json_set(coalesce(answers_json,'{}')"); var params = new ArrayList<Object>();
    for (var key : List.of("code", "output")) if (answers.get(key) != null) { sql.append(",'$.").append(key).append("',?"); params.add(answers.get(key)); }
    return new JsonSet(sql.append(")").toString(), params);
  }

  // ---------------------------------------------------------------- student

  /** GET /api/board/current: the student's active call and running test. */
  Map<String, Object> current(long user) {
    settle();
    var calls = db.queryForList("select id,called_at,call_expires_at from board_tests where user_id=? and status='CALLED' order by id desc limit 1", user);
    var running = db.queryForList("select id from board_tests where user_id=? and status='STARTED' order by id desc limit 1", Long.class, user);
    var call = calls.isEmpty() ? null : obj("id", calls.getFirst().get("id"), "calledAt", calls.getFirst().get("called_at"), "expiresAt", calls.getFirst().get("call_expires_at"));
    return obj("call", call, "test", running.isEmpty() ? null : studentView(load(running.getFirst())));
  }

  /** POST /api/board/tests/{id}/start: only the called student, while the call is active; the items are chosen now. */
  Map<String, Object> start(long user, long id) {
    Instant now = now(); settle(now);
    var t = own(user, id);
    if ("STARTED".equals(t.get("status"))) return studentView(t);
    requireCalled(t);
    Language lang = Language.of(t.get("language"));
    var items = chooseItems(user, lang, now);
    String pace = paceStatus(user, lang, now);
    var answers = new LinkedHashMap<String, Object>(); answers.put("code", items.getFirst().get("starterCode") == null ? "" : items.getFirst().get("starterCode")); answers.put("output", "");
    int started = db.update("update board_tests set status='STARTED',started_at=?,ends_at=?,items_json=?,answers_json=?,runs_json='[]',pace_status=? where id=? and status='CALLED' and call_expires_at>=?",
        iso(now), iso(now.plus(TEST)), write(items), write(answers), pace, id, iso(now));
    var after = load(id);
    if (started == 0 && !"STARTED".equals(after.get("status"))) requireCalled(after);
    if (started > 0) log.info("Board test {} started by student {}: code task {}, output task {}, pace {}", id, user, items.get(0).get("taskId"), items.get(1).get("taskId"), pace);
    return studentView(after);
  }
  private static void requireCalled(Map<String, Object> t) {
    switch ((String) t.get("status")) {
      case "FINISHED" -> throw new ApiError("BOARD_TEST_FINISHED", "Тест уже сдан");
      case "CANCELLED" -> throw new ApiError("BOARD_CALL_CANCELLED", "Преподаватель отменил вызов");
      case "EXPIRED" -> throw new ApiError("BOARD_CALL_EXPIRED", "Время вызова истекло — попроси преподавателя вызвать тебя снова");
      default -> {}
    }
  }

  /** PUT /api/board/tests/{id}/answers: autosave, while the test runs (its end + GRACE). */
  Map<String, Object> saveAnswers(long user, long id, Map<String, Object> body) {
    Instant now = now(); settle(now);
    var t = own(user, id); requireRunning(t, now);
    var set = answersUpdate(submitted(body));
    var params = new ArrayList<Object>(set.params()); params.add(id);
    if (db.update("update board_tests set answers_json=" + set.sql() + " where id=? and status='STARTED'", params.toArray()) == 0) throw over();
    return obj("savedAt", iso(now));
  }

  /** POST /api/board/tests/{id}/run: «Запустить» during the test — the console, recorded in the test's runs; the code is saved too. */
  Map<String, Object> run(long user, long id, String code) {
    Instant now = now(); settle(now);
    var t = own(user, id); requireRunning(t, now);
    Language lang = Language.of(t.get("language"));
    long started = System.nanoTime(); var console = runner.console(lang, code, "");
    log.info("Board test {} console run ({}): {} in {} ms", id, lang, console.status(), (System.nanoTime() - started) / 1_000_000);
    db.update("update board_tests set runs_json=json_insert(coalesce(runs_json,'[]'),'$[#]',json(?)),answers_json=json_set(coalesce(answers_json,'{}'),'$.code',?) where id=? and status='STARTED'",
        write(obj("at", iso(now), "code", code, "console", console.view())), code, id);
    return obj("console", console.view());
  }

  /** POST /api/board/tests/{id}/finish: the final answers (inside the time) and the checks now; the LLM later. */
  Map<String, Object> finish(long user, long id, Map<String, Object> body) {
    Instant now = now(); settle(now);
    var t = own(user, id);
    if ("STARTED".equals(t.get("status"))) {
      var answers = submitted(body);
      if (now.isAfter(instant(t.get("ends_at")).plus(GRACE))) answers = Map.of();
      if (claim(id, answers, now)) { log.info("Board test {} finished by the student", id); check(id); }
    } else if (!"FINISHED".equals(t.get("status"))) throw new ApiError("BOARD_TEST_NOT_STARTED", "Тест не начат");
    return obj("finished", true);
  }

  /** GET /api/board/grades: the student's graded tests — the date (Moscow), the final grade and the comment, nothing else. */
  Map<String, Object> studentGrades(long user, Language lang) {
    return obj("grades", db.query("select coalesce(started_at,called_at),final_grade,comment from board_tests where user_id=? and language=? and final_grade is not null order by called_at desc,id desc",
        (rs, i) -> obj("date", Instant.parse(rs.getString(1)).atZone(PairWork.MOSCOW).toLocalDate().toString(), "grade", rs.getString(2), "comment", rs.getString(3)), user, lang.name()));
  }

  private void requireRunning(Map<String, Object> t, Instant now) {
    if (!"STARTED".equals(t.get("status"))) throw over();
    if (now.isAfter(instant(t.get("ends_at")).plus(GRACE))) throw new ApiError("BOARD_TEST_OVER", "Время теста вышло");
  }
  private static ApiError over() { return new ApiError("BOARD_TEST_OVER", "Тест уже завершён"); }
  /** The answers of a request body (code, output), validated; absent fields are left out. */
  private static Map<String, String> submitted(Map<String, Object> body) {
    var answers = new HashMap<String, String>();
    if (body == null) return answers;
    for (var key : List.of("code", "output")) {
      Object value = body.get(key);
      if (value == null) continue;
      if (!(value instanceof String text)) throw new ApiError("INVALID_ANSWER", key + " должен быть строкой");
      int max = "code".equals(key) ? ApiController.SOURCE_LIMIT : ANSWER_MAX;
      if (text.length() > max) throw new ApiError("ANSWER_TOO_LONG", ("code".equals(key) ? "Код" : "Ответ") + " длиннее " + max + " символов");
      answers.put(key, text);
    }
    return answers;
  }

  /** The student's view: the items as shown, the answers and the time — never the expected output, the reference, checks, grades or the assessment. */
  private Map<String, Object> studentView(Map<String, Object> t) {
    var items = new ArrayList<Map<String, Object>>();
    for (var item : items(t))
      items.add("code".equals(item.get("kind"))
          ? obj("kind", "code", "title", item.get("title"), "statement", item.get("statement"), "starterCode", item.get("starterCode"), "language", item.get("language"))
          : obj("kind", "output", "program", item.get("program"), "language", item.get("language")));
    var answers = answers(t);
    return obj("id", t.get("id"), "status", t.get("status"), "startedAt", t.get("started_at"), "endsAt", t.get("ends_at"), "now", iso(now()),
        "items", items, "answers", obj("code", answers.get("code"), "output", answers.get("output")));
  }

  // ---------------------------------------------------------------- items

  /** A task the test may use; story: «curated:<slug>:» for the bank's variants, null for a task that is a story of its own. */
  private record Candidate(long id, String skill, String title, String statement, String starter, Integer difficulty, boolean curated, String key, String reference, String goalJson, String story) {}
  private record Passed(String skill, int block, long at) {}

  /**
   * The code item from the most recent topic passed by practice (then the older ones, then the topics confirmed by the
   * diagnostic, then the course's first topic); the output item from another topic passed earlier. Regular tasks only,
   * so a hard-mode student gets the same kind of test.
   */
  private List<Map<String, Object>> chooseItems(long user, Language lang, Instant now) {
    var practiced = db.query("select s.code,s.block_no,coalesce("
        + "(select max(" + epoch("x.created_at") + ") from skill_iterations i join submissions x on x.lesson_id=i.lesson_id and x.passed=1 join task_target_skills ts on ts.task_id=x.task_id and ts.skill_code=i.skill_code where i.user_id=p.user_id and i.skill_code=s.code and i.iteration_number=1),"
        + "(select " + epoch("l.started_at") + " from skill_iterations i join lessons l on l.id=i.lesson_id where i.user_id=p.user_id and i.skill_code=s.code and i.iteration_number=1),0) as at "
        + "from student_skills p join skills s on s.code=p.skill_code where p.user_id=? and s.language=? and (p.completed_iterations>=1 or p.mastered=1) order by at desc,s.block_no desc,s.sort_order desc",
        (rs, i) -> new Passed(rs.getString(1), rs.getInt(2), rs.getLong(3)), user, lang.name());
    var practicedCodes = practiced.stream().map(Passed::skill).toList();
    var confirmed = db.queryForList("select s.code from diagnostic_skill_results d join skills s on s.code=d.skill_code where d.user_id=? and d.confirmed=1 and s.language=? order by s.block_no desc,s.sort_order desc", String.class, user, lang.name())
        .stream().filter(code -> !practicedCodes.contains(code)).toList();
    var course = db.queryForList("select code from skills where language=? order by block_no,sort_order,code", String.class, lang.name());
    Map<String, Integer> blocks = new HashMap<>();
    db.query("select code,block_no from skills where language=?", (RowCallbackHandler) rs -> blocks.put(rs.getString(1), rs.getInt(2)), lang.name());
    Set<Long> solvedTasks = new HashSet<>(db.queryForList("select task_id from successful_task_credit where user_id=?", Long.class, user));
    Set<String> solvedStories = new HashSet<>();
    for (String key : db.queryForList("select t.external_key from successful_task_credit c join tasks t on t.id=c.task_id where c.user_id=? and t.source='CURATED' and t.external_key like 'curated:%:%'", String.class, user))
      solvedStories.add(story(key));

    var codeTopics = new LinkedHashSet<String>(practicedCodes); codeTopics.addAll(confirmed); if (!course.isEmpty()) codeTopics.add(course.getFirst());
    Candidate code = null;
    for (String topic : codeTopics) {
      int preferred = blocks.getOrDefault(topic, 1) >= EASY_FROM_BLOCK ? 1 : 2;
      var candidates = shuffled(db.query("select t.id,ts.skill_code,t.title,t.statement,t.starter_code,t.difficulty,t.source='CURATED',t.external_key,t.reference_code,t.goal_json from tasks t join task_target_skills ts on ts.task_id=t.id "
          + "where ts.skill_code=? and t.language=? and t.active=1 and t.mode='NORMAL' and coalesce(t.goal_json,'') not like '%IO_BEHAVIOR%'", (rs, i) -> candidate(rs), topic, lang.name()));
      candidates.sort(Comparator.comparing((Candidate c) -> solved(c, solvedTasks, solvedStories)).thenComparing(c -> !c.curated())
          .thenComparing(c -> c.difficulty() == null).thenComparingInt(c -> c.difficulty() == null ? 0 : Math.abs(c.difficulty() - preferred)).thenComparingInt(c -> c.difficulty() == null ? 0 : c.difficulty()));
      if (!candidates.isEmpty()) { code = candidates.getFirst(); break; }
    }
    if (code == null) throw new ApiError("NO_BOARD_TASK", "Для теста не нашлось задачи по пройденным темам");

    // The output item: a topic passed earlier (more than RECENT_DAYS ago first), then any other passed or confirmed one,
    // then the code item's topic, then the course from its start.
    long recent = now.minus(Duration.ofDays(RECENT_DAYS)).getEpochSecond();
    String codeTopic = code.skill();
    var older = shuffled(practiced.stream().filter(p -> p.at() <= recent).map(Passed::skill).toList());
    var others = new ArrayList<String>(practiced.stream().filter(p -> p.at() > recent).map(Passed::skill).toList()); others.addAll(confirmed);
    var outputTopics = new LinkedHashSet<String>(older); outputTopics.addAll(shuffled(others)); outputTopics.remove(codeTopic); outputTopics.add(codeTopic); outputTopics.addAll(course);
    Map<String, List<Candidate>> outputs = new HashMap<>();
    for (var c : db.query("select t.id,ts.skill_code,t.title,t.statement,t.starter_code,t.difficulty,1,t.external_key,t.reference_code,t.goal_json from tasks t join task_target_skills ts on ts.task_id=t.id "
        + "where t.language=? and t.active=1 and t.source='CURATED' and t.mode='NORMAL' and t.reference_code is not null and trim(t.reference_code)<>'' and t.goal_json like '%OUTPUT_TEXT%'", (rs, i) -> candidate(rs), lang.name())) {
      var goal = TaskGoal.fromJson(json, c.goalJson());
      if (goal != null && goal.kind() == TaskGoal.Kind.OUTPUT_TEXT && goal.expectedOutput() != null && !goal.expectedOutput().isBlank() && c.id() != code.id()
          && (c.story() == null || !c.story().equals(code.story())))
        outputs.computeIfAbsent(c.skill(), k -> new ArrayList<>()).add(c);
    }
    Candidate output = null;
    for (String topic : outputTopics) {
      var candidates = shuffled(outputs.getOrDefault(topic, List.of()));
      candidates.sort(Comparator.comparing((Candidate c) -> solved(c, solvedTasks, solvedStories)));
      if (!candidates.isEmpty()) { output = candidates.getFirst(); break; }
    }
    if (output == null) throw new ApiError("NO_BOARD_TASK", "В банке нет задач «что выведет этот код» с эталонной программой");

    Map<String, String> titles = new HashMap<>();
    db.query("select code,title from skills where code in (?,?)", (RowCallbackHandler) rs -> titles.put(rs.getString(1), rs.getString(2)), code.skill(), output.skill());
    var codeItem = obj("kind", "code", "language", lang.name(), "taskId", code.id(), "externalKey", code.key(), "skillCode", code.skill(), "skillTitle", titles.get(code.skill()),
        "difficulty", code.difficulty(), "title", code.title(), "statement", code.statement(), "starterCode", code.starter());
    var outputItem = obj("kind", "output", "language", lang.name(), "taskId", output.id(), "externalKey", output.key(), "skillCode", output.skill(), "skillTitle", titles.get(output.skill()),
        "difficulty", output.difficulty(), "title", output.title(), "program", output.reference(), "expectedOutput", TaskGoal.fromJson(json, output.goalJson()).expectedOutput());
    return List.of(codeItem, outputItem);
  }
  private static Candidate candidate(java.sql.ResultSet rs) throws java.sql.SQLException {
    int d = rs.getInt(6); Integer difficulty = rs.wasNull() ? null : d; boolean curated = rs.getInt(7) == 1; String key = rs.getString(8);
    return new Candidate(rs.getLong(1), rs.getString(2), rs.getString(3), rs.getString(4), rs.getString(5), difficulty, curated, key, rs.getString(9), rs.getString(10),
        curated && key != null && key.matches("curated:[^:]+:.+") ? story(key) : null);
  }
  /** «curated:<slug>:<n>» → «curated:<slug>:». */
  private static String story(String key) { return key.substring(0, key.indexOf(':', "curated:".length()) + 1); }
  private static boolean solved(Candidate c, Set<Long> tasks, Set<String> stories) { return c.story() == null ? tasks.contains(c.id()) : stories.contains(c.story()); }
  private <T> List<T> shuffled(List<T> list) { var copy = new ArrayList<>(list); Collections.shuffle(copy, random); return copy; }

  /** The session status at the start of the test (ProgressAnalytics), null when the student is not a member of the course. */
  private String paceStatus(long user, Language lang, Instant now) {
    var session = analytics.studentSession(user, lang, now);
    return session == null ? null : (String) session.get("status");
  }

  // ---------------------------------------------------------------- checks and assessment

  /** The checks of a finished test: the code like a lesson attempt (not credited), the output compared; then the LLM. */
  void check(long id) {
    if (!processing.add("check:" + id)) return;
    try {
      var t = load(id);
      if (!"FINISHED".equals(t.get("status")) || t.get("results_json") != null) return;
      Language lang = Language.of(t.get("language"));
      var items = items(t); var answers = answers(t);
      Map<String, Object> code;
      try { code = checkCode(lang, items.get(0), answers.get("code")); }
      catch (RuntimeException e) {
        log.error("Board test {}: the code could not be checked", id, e);
        code = obj("kind", "code", "passed", false, "output", "Проверка не удалась: " + e.getMessage(), "outcome", null, "console", null, "unavailable", true);
      }
      String expected = (String) items.get(1).get("expectedOutput"), actual = answers.get("output") == null ? "" : answers.get("output");
      var output = obj("kind", "output", "passed", sameOutput(expected, actual), "expected", expected, "actual", actual);
      boolean codeOk = Boolean.TRUE.equals(code.get("passed")), outputOk = Boolean.TRUE.equals(output.get("passed"));
      int rule = ruleGrade(codeOk, outputOk, false);
      db.update("update board_tests set results_json=?,rule_grade=?,suggested_grade=? where id=?", write(List.of(code, output)), String.valueOf(rule),
          String.valueOf(suggested(rule, cap((String) t.get("pace_status")))), id);
      log.info("Board test {} checked: code {}, output {}, rule grade {}", id, codeOk ? "passed" : "failed", outputOk ? "right" : "wrong", rule);
      startAssessment(id);
    } catch (RuntimeException e) {
      // Stored as a failed check, so that the test is not checked again and again; the teacher grades it alone.
      log.error("Board test {} could not be checked", id, e);
      String error = "Проверка не удалась: " + e.getMessage();
      db.update("update board_tests set results_json=?,rule_grade='2',suggested_grade='2',assessment_json=? where id=? and results_json is null",
          write(List.of(obj("kind", "code", "passed", false, "output", error, "outcome", null, "console", null, "unavailable", true), obj("kind", "output", "passed", false, "expected", null, "actual", null))),
          write(unavailable(error)), id);
    } finally { processing.remove("check:" + id); }
  }

  private Map<String, Object> checkCode(Language lang, Map<String, Object> item, String code) {
    var result = obj("kind", "code", "passed", false, "output", null, "outcome", null, "console", null, "unavailable", false);
    if (code == null || code.isBlank()) { result.put("output", "Код не написан"); return result; }
    var rows = db.queryForList("select test_source,goal_json from tasks where id=?", ((Number) item.get("taskId")).longValue());
    if (rows.isEmpty()) { result.put("output", "Задача удалена из банка"); return result; }
    if (!runner.status(lang).available()) { result.put("output", "Проверка " + lang.title + " была недоступна"); result.put("unavailable", true); return result; }
    // The console run goes alongside the check, as for a lesson attempt.
    var console = CompletableFuture.supplyAsync(() -> { try { return runner.console(lang, code); } catch (RuntimeException e) { log.warn("Board console run failed: {}", e.toString()); return null; } }, executor);
    TaskGoal goal = TaskGoal.fromJson(json, (String) rows.getFirst().get("goal_json"));
    var cases = db.query("select ordinal,input,expected,is_public from task_cases where task_id=? order by ordinal",
        (rs, i) -> new TestCases.Case(rs.getInt(1), rs.getString(2), rs.getString(3), rs.getInt(4) == 1), item.get("taskId"));
    // «Calculate» tasks: the syntax tree decides whether the answer was calculated (a lesson asks the LLM first; here the LLM assesses the whole test).
    var run = !cases.isEmpty() ? verifier.runCases(lang, code, goal, TestCases.sample(cases, random)) : verifier.run(lang, code, (String) rows.getFirst().get("test_source"), goal);
    var printed = console.join();
    result.put("passed", run.passed()); result.put("output", run.output()); result.put("outcome", run.outcome().name());
    result.put("console", printed == null ? null : printed.view()); result.put("unavailable", run.outcome() == PistonCodeRunner.Outcome.UNAVAILABLE);
    return result;
  }

  /** The LLM's proposal in the background; UNAVAILABLE at once when the LLM is off. */
  private void startAssessment(long id) {
    if (!generator.available()) { db.update("update board_tests set assessment_json=? where id=?", write(unavailable("LLM выключена или недоступна")), id); return; }
    db.update("update board_tests set assessment_json=? where id=?", write(Map.of("status", "PENDING")), id);
    executor.execute(() -> assess(id));
  }
  private static Map<String, Object> unavailable(String error) { return obj("status", "UNAVAILABLE", "grade", null, "summary", null, "items", List.of(), "error", error); }

  void assess(long id) {
    if (!processing.add("assess:" + id)) return;
    try {
      var t = load(id);
      if (!(t.get("assessment") instanceof Map<?, ?> a) || !"PENDING".equals(a.get("status")) || t.get("results_json") == null) return;
      var items = items(t); var answers = answers(t); var results = results(t);
      boolean codeOk = Boolean.TRUE.equals(results.get(0).get("passed")), outputOk = Boolean.TRUE.equals(results.get(1).get("passed"));
      var runs = runs(t); var recentRuns = new ArrayList<BoardAssessmentRequest.Run>();
      for (var run : runs.subList(Math.max(0, runs.size() - LLM_RUNS), runs.size())) {
        var console = run.get("console") instanceof Map<?, ?> c ? c : Map.of();
        recentRuns.add(new BoardAssessmentRequest.Run((String) run.get("code"), String.valueOf(console.get("status")), (String) console.get("stdout"), (String) console.get("error")));
      }
      var code = items.get(0); var output = items.get(1);
      var request = new BoardAssessmentRequest(Language.of(t.get("language")), (String) code.get("skillCode"), (String) code.get("title"), (String) code.get("statement"),
          answers.get("code"), codeOk, (String) results.get(0).get("output"), (String) output.get("program"), (String) output.get("expectedOutput"), answers.get("output"), outputOk,
          recentRuns, Integer.parseInt((String) t.get("rule_grade")));
      long user = ((Number) t.get("user_id")).longValue();
      Map<String, Object> assessment; String rule = (String) t.get("rule_grade"), suggestedGrade = (String) t.get("suggested_grade");
      try {
        var proposal = generator.assessBoardTest(user, request);
        // One item right and the other partly right by the LLM's verdict: 4 by the rule.
        String other = codeOk ? "output" : "code";
        boolean partly = codeOk != outputOk && proposal.items().stream().anyMatch(i -> other.equals(i.item()) && BoardAssessment.PARTLY.equals(i.verdict()));
        rule = String.valueOf(ruleGrade(codeOk, outputOk, partly));
        assessment = proposal.view();
        suggestedGrade = String.valueOf(suggested(proposal.grade(), cap((String) t.get("pace_status"))));
        log.info("Board test {} assessed by the LLM: grade {}, suggested {}", id, proposal.grade(), suggestedGrade);
      } catch (LlmUnavailableException e) {
        log.warn("Board test {} not assessed: {}", id, e.getMessage());
        assessment = unavailable(e.getMessage());
      }
      db.update("update board_tests set assessment_json=?,rule_grade=?,suggested_grade=? where id=?", write(assessment), rule, suggestedGrade, id);
    } catch (RuntimeException e) {
      log.error("Board test {} could not be assessed", id, e);
      db.update("update board_tests set assessment_json=? where id=? and json_extract(assessment_json,'$.status')='PENDING'", write(unavailable("Ошибка оценки: " + e.getMessage())), id);
    } finally { processing.remove("assess:" + id); }
  }

  // ---------------------------------------------------------------- teacher

  /** GET /api/admin/board: the group's students with presence and history, whom to call, the active calls and tests. */
  Map<String, Object> overview(String group, String language) {
    Instant now = now(); settle(now);
    String name = existingGroup(group);
    Language lang = course(name, language);
    var members = db.queryForList("select id,login,display_name,session_participant from users where role='STUDENT' and group_name=?", name);
    var ids = members.stream().map(m -> ((Number) m.get("id")).longValue()).toList();
    String in = in(ids.size()); long since = now.minus(Duration.ofMinutes(PRESENT_MINUTES)).getEpochSecond();
    Set<Long> present = new HashSet<>(db.queryForList("select distinct user_id from lessons where language=? and user_id in " + in + " and (finished_at is null or "
        + epoch("last_activity_at") + ">=? or " + epoch("started_at") + ">=?)", Long.class, concat(new Object[]{lang.name()}, ids.toArray(), new Object[]{since, since})));
    Map<Long, Object[]> history = new HashMap<>();
    db.query("select user_id,max(case when status in ('STARTED','FINISHED') then started_at end),coalesce(sum(status='FINISHED'),0) from board_tests where language=? and user_id in " + in + " group by user_id",
        (RowCallbackHandler) rs -> history.put(rs.getLong(1), new Object[]{rs.getString(2), rs.getInt(3), null}), concat(new Object[]{lang.name()}, ids.toArray()));
    db.query("select b.user_id,b.final_grade from board_tests b where b.language=? and b.user_id in " + in + " and b.id=(select x.id from board_tests x where x.user_id=b.user_id and x.language=b.language and x.final_grade is not null order by coalesce(x.started_at,x.called_at) desc,x.id desc limit 1)",
        (RowCallbackHandler) rs -> history.computeIfAbsent(rs.getLong(1), k -> new Object[]{null, 0, null})[2] = rs.getString(2), concat(new Object[]{lang.name()}, ids.toArray()));
    Set<Long> busy = new HashSet<>(db.queryForList("select user_id from board_tests where status in ('CALLED','STARTED') and user_id in " + in, Long.class, ids.toArray()));
    var collator = collator();
    var view = new ArrayList<Map<String, Object>>();
    for (var m : members.stream().sorted(Comparator.comparing((Map<String, Object> m) -> m.get("display_name") == null ? "" : (String) m.get("display_name"), collator).thenComparing(m -> (String) m.get("login"))).toList()) {
      long user = ((Number) m.get("id")).longValue(); var h = history.getOrDefault(user, new Object[]{null, 0, null});
      view.add(obj("userId", user, "login", m.get("login"), "displayName", m.get("display_name"), "present", present.contains(user), "lastTestAt", h[0], "tests", h[1], "lastGrade", h[2]));
    }
    // Whom to call: members taking the session and not called right now; present ones first; never tested, then the
    // longest ago; one of the three oldest at random — stable until a test is called, so the polling page does not flicker.
    var pool = members.stream().filter(m -> ((Number) m.get("session_participant")).intValue() == 1).map(m -> ((Number) m.get("id")).longValue()).filter(u -> !busy.contains(u)).toList();
    if (pool.stream().anyMatch(present::contains)) pool = pool.stream().filter(present::contains).toList();
    var oldest = pool.stream().sorted(Comparator.comparing((Long u) -> (String) history.getOrDefault(u, new Object[]{null, 0, null})[0], Comparator.nullsFirst(Comparator.naturalOrder())).thenComparing(u -> u)).limit(3).toList();
    long seed = Objects.hash(name, lang.name(), db.queryForObject("select coalesce(max(id),0) from board_tests", Long.class), ProgressAnalytics.day(now));
    Long suggestion = oldest.isEmpty() ? null : oldest.get(new SplittableRandom(seed).nextInt(oldest.size()));
    var active = db.queryForList("select id from board_tests where group_name=? and language=? and (status in ('CALLED','STARTED') or called_at>=? or (status='FINISHED' and final_grade is null)) order by called_at desc,id desc",
        Long.class, name, lang.name(), iso(now.minus(ACTIVE_RECENT))).stream().map(id -> summary(load(id))).toList();
    return obj("group", name, "language", lang.name(), "members", view, "suggested", suggestion, "active", active);
  }

  /** POST /api/admin/board/call: a new call; the student's earlier calls that were not started are cancelled. */
  Map<String, Object> call(long admin, Map<String, Object> body) {
    if (body == null || !(body.get("userId") instanceof Number user)) throw new ApiError("INVALID_STUDENT", "Нужен userId студента");
    if (body.get("language") != null && !(body.get("language") instanceof String)) throw new ApiError("UNKNOWN_LANGUAGE", "Неизвестный язык курса");
    return summary(load(call(admin, user.longValue(), Language.parse((String) body.get("language")))));
  }
  private long call(long admin, long user, Language lang) {
    var rows = db.queryForList("select group_name from users where id=? and role='STUDENT'", user);
    if (rows.isEmpty()) throw new NotFoundError("STUDENT_NOT_FOUND", "Студент не найден");
    Instant now = now(); settle(now);
    db.update("update board_tests set status='CANCELLED' where user_id=? and status='CALLED'", user);
    long id = db.queryForObject("insert into board_tests(user_id,group_name,language,status,called_at,called_by,call_expires_at) values(?,?,?,'CALLED',?,?,?) returning id", Long.class,
        user, rows.getFirst().get("group_name"), lang.name(), iso(now), admin, iso(now.plus(CALL)));
    log.info("Student {} called to the board ({}) by admin {}: test {}", user, lang, admin, id);
    return id;
  }

  /** POST /api/admin/board/tests/{id}/recall: a new call for the same student and course. */
  Map<String, Object> recall(long admin, long id) {
    var t = load(id);
    return adminView(load(call(admin, ((Number) t.get("user_id")).longValue(), Language.of(t.get("language")))));
  }

  /** POST /api/admin/board/tests/{id}/cancel: a call or a running test; a finished test can only be deleted. */
  Map<String, Object> cancel(long id) {
    settle(); var t = load(id);
    if ("FINISHED".equals(t.get("status"))) throw new ApiError("BOARD_TEST_FINISHED", "Тест уже сдан — его можно удалить");
    db.update("update board_tests set status='CANCELLED' where id=? and status<>'FINISHED'", id);
    log.info("Board test {} cancelled", id);
    return adminView(load(id));
  }

  /** POST /api/admin/board/tests/{id}/extend: more time for a call (an expired one comes back) or for a running test. */
  Map<String, Object> extend(long id, Map<String, Object> body) {
    Object value = body == null || body.get("seconds") == null ? 60 : body.get("seconds");
    if (!(value instanceof Integer seconds) || seconds < 1 || seconds > EXTEND_MAX_SECONDS) throw new ApiError("INVALID_SECONDS", "seconds — целое число от 1 до " + EXTEND_MAX_SECONDS);
    Instant now = now(); settle(now); var t = load(id);
    switch ((String) t.get("status")) {
      case "CALLED", "EXPIRED" -> db.update("update board_tests set status='CALLED',call_expires_at=? where id=?", iso(later(instant(t.get("call_expires_at")), now).plusSeconds(seconds)), id);
      case "STARTED" -> db.update("update board_tests set ends_at=? where id=? and status='STARTED'", iso(later(instant(t.get("ends_at")), now).plusSeconds(seconds)), id);
      default -> throw new ApiError("BOARD_TEST_NOT_RUNNING", "Продлить можно только вызов или идущий тест");
    }
    log.info("Board test {} extended by {} s", id, seconds);
    return adminView(load(id));
  }

  /** POST /api/admin/board/tests/{id}/finish: a running test now, with the last autosaved answers; the checks run now. */
  Map<String, Object> finishNow(long id) {
    Instant now = now(); settle(now); var t = load(id);
    if ("STARTED".equals(t.get("status"))) { if (claim(id, Map.of(), now)) { log.info("Board test {} finished by the teacher", id); check(id); } }
    else if (!"FINISHED".equals(t.get("status"))) throw new ApiError("BOARD_TEST_NOT_STARTED", "Тест не начат — вызов можно отменить");
    return adminView(load(id));
  }

  /** PATCH /api/admin/board/tests/{id}: the teacher's final grade and comment, only the fields present; any time. */
  Map<String, Object> grade(long id, Map<String, Object> body) {
    load(id);
    if (body == null || !body.containsKey("finalGrade") && !body.containsKey("comment")) throw new ApiError("INVALID_GRADE", "Нужны finalGrade и/или comment");
    if (body.containsKey("finalGrade")) {
      Object value = body.get("finalGrade"); String grade = value == null ? null : value.toString().strip();
      if (grade != null && !GRADES.contains(grade)) throw new ApiError("INVALID_GRADE", "Оценка — 2, 3, 4 или 5");
      db.update("update board_tests set final_grade=?,graded_at=? where id=?", grade, grade == null ? null : iso(now()), id);
    }
    if (body.containsKey("comment")) {
      Object value = body.get("comment");
      if (value != null && !(value instanceof String)) throw new ApiError("INVALID_COMMENT", "Комментарий должен быть строкой");
      String comment = value == null || ((String) value).isBlank() ? null : ((String) value).strip();
      if (comment != null && comment.length() > COMMENT_MAX) throw new ApiError("INVALID_COMMENT", "Комментарий длиннее " + COMMENT_MAX + " символов");
      db.update("update board_tests set comment=? where id=?", comment, id);
    }
    return adminView(load(id));
  }

  /** POST /api/admin/board/tests/{id}/assess: the LLM's assessment again. */
  Map<String, Object> reassess(long id) {
    var t = load(id);
    if (!"FINISHED".equals(t.get("status")) || t.get("results_json") == null) throw new ApiError("BOARD_TEST_NOT_CHECKED", "Тест ещё не сдан или не проверен");
    startAssessment(id);
    return adminView(load(id));
  }

  /** DELETE /api/admin/board/tests/{id}. */
  Map<String, Object> delete(long id) {
    load(id);
    db.update("delete from board_tests where id=?", id);
    return obj("deleted", true);
  }

  /** GET /api/admin/board/tests/{id}. */
  Map<String, Object> test(long id) { settle(); return adminView(load(id)); }

  /** GET /api/admin/board/journal: the group's tests of the course, newest first, and per student their final grades (oldest first). */
  Map<String, Object> journal(String group, String language) {
    String name = group == null ? "" : group.strip();
    if (name.isEmpty() || count("select count(*) from users where role='STUDENT' and group_name=?", name) == 0 && count("select count(*) from board_tests where group_name=?", name) == 0)
      throw PairWork.groupNotFound();
    Language lang = course(name, language);
    settle();
    var tests = db.query("select b.id,b.user_id,u.display_name,b.called_at,b.status,b.final_grade,b.suggested_grade from board_tests b join users u on u.id=b.user_id where b.group_name=? and b.language=? order by b.called_at desc,b.id desc",
        (rs, i) -> obj("id", rs.getLong(1), "userId", rs.getLong(2), "displayName", rs.getString(3), "calledAt", rs.getString(4), "status", rs.getString(5), "finalGrade", rs.getString(6), "suggestedGrade", rs.getString(7)),
        name, lang.name());
    Map<Long, String> people = new HashMap<>(); Map<Long, List<String>> grades = new HashMap<>(); Map<Long, String> last = new HashMap<>();
    db.query("select id,display_name from users where role='STUDENT' and group_name=? union select u.id,u.display_name from board_tests b join users u on u.id=b.user_id where b.group_name=? and b.language=?",
        (RowCallbackHandler) rs -> people.put(rs.getLong(1), rs.getString(2)), name, name, lang.name());
    db.query("select user_id,final_grade,started_at from board_tests where group_name=? and language=? and status='FINISHED' order by called_at,id",
        (RowCallbackHandler) rs -> { grades.computeIfAbsent(rs.getLong(1), k -> new ArrayList<>()).add(rs.getString(2)); last.put(rs.getLong(1), rs.getString(3)); }, name, lang.name());
    var collator = collator();
    var students = people.entrySet().stream().sorted(Comparator.comparing((Map.Entry<Long, String> e) -> e.getValue() == null ? "" : e.getValue(), collator).thenComparing(Map.Entry::getKey))
        .map(e -> obj("userId", e.getKey(), "displayName", e.getValue(), "grades", grades.getOrDefault(e.getKey(), List.of()), "lastTestAt", last.get(e.getKey()))).toList();
    return obj("group", name, "language", lang.name(), "tests", tests, "students", students);
  }

  private Map<String, Object> summary(Map<String, Object> t) {
    var assessment = t.get("assessment") instanceof Map<?, ?> a ? a.get("status") : null;
    return obj("id", t.get("id"), "userId", t.get("user_id"), "displayName", t.get("display_name"), "status", t.get("status"), "calledAt", t.get("called_at"),
        "expiresAt", t.get("call_expires_at"), "startedAt", t.get("started_at"), "endsAt", t.get("ends_at"), "finishedAt", t.get("finished_at"),
        "suggestedGrade", t.get("suggested_grade"), "finalGrade", t.get("final_grade"), "assessmentStatus", assessment);
  }
  /** Everything for the teacher: the items with the expected output and the task, the answers, checks, runs, pace, grades. */
  private Map<String, Object> adminView(Map<String, Object> t) {
    var view = summary(t);
    String pace = (String) t.get("pace_status");
    view.put("login", t.get("login")); view.put("group", t.get("group_name")); view.put("language", t.get("language"));
    view.put("items", t.get("items_json") == null ? null : items(t)); view.put("answers", t.get("answers_json") == null ? null : answers(t));
    view.put("results", t.get("results_json") == null ? null : results(t)); view.put("runs", runs(t));
    view.put("paceStatus", pace); view.put("paceCap", cap(pace)); view.put("ruleGrade", t.get("rule_grade")); view.put("assessment", t.get("assessment"));
    view.put("comment", t.get("comment")); view.put("gradedAt", t.get("graded_at"));
    return view;
  }

  // ---------------------------------------------------------------- loading and helpers

  private Map<String, Object> load(long id) {
    var rows = db.queryForList("select b.*,u.login,u.display_name from board_tests b join users u on u.id=b.user_id where b.id=?", id);
    if (rows.isEmpty()) throw new NotFoundError("BOARD_TEST_NOT_FOUND", "Тест не найден");
    var t = rows.getFirst();
    t.put("assessment", t.get("assessment_json") == null ? null : read((String) t.get("assessment_json"), new TypeReference<LinkedHashMap<String, Object>>() {}));
    return t;
  }
  /** The student's own test; someone else's is «not found». */
  private Map<String, Object> own(long user, long id) {
    var t = load(id);
    if (((Number) t.get("user_id")).longValue() != user) throw new NotFoundError("BOARD_TEST_NOT_FOUND", "Тест не найден");
    return t;
  }
  private List<Map<String, Object>> items(Map<String, Object> t) { return t.get("items_json") == null ? List.of() : read((String) t.get("items_json"), new TypeReference<List<Map<String, Object>>>() {}); }
  private Map<String, String> answers(Map<String, Object> t) { return t.get("answers_json") == null ? Map.of() : read((String) t.get("answers_json"), new TypeReference<LinkedHashMap<String, String>>() {}); }
  private List<Map<String, Object>> results(Map<String, Object> t) { return read((String) t.get("results_json"), new TypeReference<List<Map<String, Object>>>() {}); }
  private List<Map<String, Object>> runs(Map<String, Object> t) { return t.get("runs_json") == null ? List.of() : read((String) t.get("runs_json"), new TypeReference<List<Map<String, Object>>>() {}); }

  private String existingGroup(String group) {
    String name = group == null ? "" : group.strip();
    if (name.isEmpty() || count("select count(*) from users where role='STUDENT' and group_name=?", name) == 0) throw PairWork.groupNotFound();
    return name;
  }
  /** The course asked for, else the group's course (as «Работа на паре» suggests it). */
  private Language course(String group, String language) {
    if (language != null && !language.isBlank()) return Language.parse(language);
    return count("select count(*) from users where role='STUDENT' and group_name=?", group) == 0 ? Language.JAVA : Language.valueOf((String) pairs.course(group).get("language"));
  }

  private Instant now() { return clock.instant(); }
  private static String iso(Instant at) { return PairWork.iso(at); }
  private static Instant instant(Object stored) { return Instant.parse((String) stored); }
  private static Instant later(Instant a, Instant b) { return a.isAfter(b) ? a : b; }
  private static String epoch(String column) { return "cast(strftime('%s'," + column + ") as integer)"; }
  private static String in(int n) { return n == 0 ? "(null)" : "(" + String.join(",", Collections.nCopies(n, "?")) + ")"; }
  private static Object[] concat(Object[]... parts) { var all = new ArrayList<Object>(); for (var p : parts) all.addAll(Arrays.asList(p)); return all.toArray(); }
  private int count(String sql, Object... params) { return db.queryForObject(sql, Integer.class, params); }
  private String write(Object value) { try { return json.writeValueAsString(value); } catch (Exception e) { throw new IllegalStateException(e); } }
  private <T> T read(String text, TypeReference<T> type) { try { return json.readValue(text, type); } catch (Exception e) { throw new IllegalStateException(e); } }
  private static Collator collator() { return Collator.getInstance(Locale.forLanguageTag("ru")); }
  private static Map<String, Object> obj(Object... entries) { var m = new LinkedHashMap<String, Object>(); for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]); return m; }
}
