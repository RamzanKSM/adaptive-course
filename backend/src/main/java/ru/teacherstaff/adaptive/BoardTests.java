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
 * «К доске»: the teacher calls a student from his laptop with the kinds of items he chose (BoardItems: parsons «Собери
 * программу», fix «Исправь ошибку», code «Напиши код»); the student starts the test on the classroom PC within CALL; one
 * timer — the sum of the kinds' minutes. The answers are autosaved; the client submits at 0, and the server finishes a
 * test whose time is over (after GRACE) with the last autosaved answers — lazily on every board request and every 15 s
 * (BoardTestFinisher).
 * <p>After the finish every item's program is checked like a lesson attempt; nothing is credited. The weighted grade by
 * the checks, the LLM's verdicts (asynchronous, a platform thread: «частично верно» gives half of a failed item's weight)
 * and the pace cap give a suggested grade; the teacher sets the final one. The student sees only the test itself and,
 * later, the date, the final grade and the comment. Rules: backend/README.md, «К доске».
 */
@Component
class BoardTests implements DisposableBean {
  private static final Logger log = LoggerFactory.getLogger(BoardTests.class);
  static final Duration CALL = Duration.ofMinutes(5), GRACE = Duration.ofSeconds(15);
  /** A topic passed by practice more than this many days ago is «older»: the parsons item comes preferably from it. */
  static final int RECENT_DAYS = 14;
  /** A member is present with activity in the course within this many minutes or an open lesson. */
  static final int PRESENT_MINUTES = 60;
  /** Runs the LLM sees; the oldest of a longer history are left out. */
  static final int LLM_RUNS = 10;
  static final int COMMENT_MAX = 500, EXTEND_MAX_SECONDS = 1800;
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

  /** The highest grade the pace allows: borderline → 4, behind → 3; on track, course closed, no session date or not a member → none. */
  static Integer cap(String paceStatus) { return "BORDERLINE".equals(paceStatus) ? Integer.valueOf(4) : "BEHIND".equals(paceStatus) ? Integer.valueOf(3) : null; }
  static int suggested(int grade, Integer cap) { return cap == null ? grade : Math.min(grade, cap); }
  /**
   * Per item of a checked test (in its order) the score: passed → 1; else the LLM's verdict «частично верно» (a DONE
   * assessment) → 0.5; else 0. Without an assessment — the grade by the checks alone.
   */
  static Map<String, Double> scores(List<Map<String, Object>> results, Map<?, ?> assessment) {
    var partly = new HashSet<Object>();
    if (assessment != null && "DONE".equals(assessment.get("status")) && assessment.get("items") instanceof List<?> verdicts)
      for (var v : verdicts) if (v instanceof Map<?, ?> m && BoardAssessment.PARTLY.equals(m.get("verdict"))) partly.add(m.get("item"));
    var scores = new LinkedHashMap<String, Double>();
    for (var r : results) scores.put((String) r.get("kind"), Boolean.TRUE.equals(r.get("passed")) ? 1.0 : partly.contains(r.get("kind")) ? 0.5 : 0.0);
    return scores;
  }
  static int grade(List<Map<String, Object>> results, Map<?, ?> assessment) { return BoardItems.grade(BoardItems.percent(scores(results, assessment))); }

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
  private boolean claim(long id, Map<String, Object> answers, Instant now) {
    var set = answersUpdate(answers);
    var params = new ArrayList<Object>(); params.add(iso(now)); params.addAll(set.params()); params.add(write(Map.of("status", "PENDING"))); params.add(id);
    return db.update("update board_tests set status='FINISHED',finished_at=?,answers_json=" + set.sql() + ",assessment_json=? where id=? and status='STARTED'", params.toArray()) > 0;
  }
  private record JsonSet(String sql, List<Object> params) {}
  /** json_set over answers_json for the fields given (code, fix: text; parsons: the placed line ids); the others keep their saved value. */
  private JsonSet answersUpdate(Map<String, Object> answers) {
    var sql = new StringBuilder("json_set(coalesce(answers_json,'{}')"); var params = new ArrayList<Object>();
    for (var key : BoardItems.ALL) {
      Object value = answers.get(key);
      if (value instanceof String text) { sql.append(",'$.").append(key).append("',?"); params.add(text); }
      else if (value != null) { sql.append(",'$.").append(key).append("',json(?)"); params.add(write(value)); }
    }
    return new JsonSet(sql.append(")").toString(), params);
  }

  // ---------------------------------------------------------------- student

  /** GET /api/board/current: the student's active call and running test. */
  Map<String, Object> current(long user) {
    settle();
    var calls = db.queryForList("select id,called_at,call_expires_at,kinds,duration_seconds from board_tests where user_id=? and status='CALLED' order by id desc limit 1", user);
    var running = db.queryForList("select id from board_tests where user_id=? and status='STARTED' order by id desc limit 1", Long.class, user);
    var c = calls.isEmpty() ? null : calls.getFirst();
    var call = c == null ? null : obj("id", c.get("id"), "calledAt", c.get("called_at"), "expiresAt", c.get("call_expires_at"), "kinds", kinds(c), "durationSeconds", duration(c));
    return obj("call", call, "test", running.isEmpty() ? null : studentView(load(running.getFirst())));
  }

  /** POST /api/board/tests/{id}/start: only the called student, while the call is active; the items are chosen now. */
  Map<String, Object> start(long user, long id) {
    Instant now = now(); settle(now);
    var t = own(user, id);
    if ("STARTED".equals(t.get("status"))) return studentView(t);
    requireCalled(t);
    Language lang = Language.of(t.get("language"));
    var items = chooseItems(user, lang, kinds(t), now);
    String pace = paceStatus(user, lang, now);
    var answers = new LinkedHashMap<String, Object>();
    for (var item : items)
      switch ((String) item.get("kind")) {
        case "parsons" -> answers.put("parsons", List.of());
        case "fix" -> answers.put("fix", item.get("program"));
        default -> answers.put("code", item.get("starterCode") == null ? "" : item.get("starterCode"));
      }
    int started = db.update("update board_tests set status='STARTED',started_at=?,ends_at=?,items_json=?,answers_json=?,runs_json='[]',pace_status=? where id=? and status='CALLED' and call_expires_at>=?",
        iso(now), iso(now.plusSeconds(duration(t))), write(items), write(answers), pace, id, iso(now));
    var after = load(id);
    if (started == 0 && !"STARTED".equals(after.get("status"))) requireCalled(after);
    if (started > 0) log.info("Board test {} started by student {}: tasks {}, pace {}", id, user, items.stream().map(i -> i.get("kind") + " " + i.get("taskId")).toList(), pace);
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
    var set = answersUpdate(submitted(body, items(t)));
    var params = new ArrayList<Object>(set.params()); params.add(id);
    if (db.update("update board_tests set answers_json=" + set.sql() + " where id=? and status='STARTED'", params.toArray()) == 0) throw over();
    return obj("savedAt", iso(now));
  }

  /** POST /api/board/tests/{id}/run: «Запустить» for the code or fix item — the console, recorded in the test's runs with its item; that answer is saved too. */
  Map<String, Object> run(long user, long id, Object item, String code) {
    Instant now = now(); settle(now);
    var t = own(user, id); requireRunning(t, now);
    String kind = item == null ? "code" : item instanceof String s ? s : "";
    if (!List.of("code", "fix").contains(kind) || !kinds(t).contains(kind)) throw new ApiError("INVALID_ITEM", "Запускать можно только код заданий этого теста «Исправь ошибку» и «Напиши код»");
    Language lang = Language.of(t.get("language"));
    long started = System.nanoTime(); var console = runner.console(lang, code, "");
    log.info("Board test {} console run ({}, {}): {} in {} ms", id, lang, kind, console.status(), (System.nanoTime() - started) / 1_000_000);
    db.update("update board_tests set runs_json=json_insert(coalesce(runs_json,'[]'),'$[#]',json(?)),answers_json=json_set(coalesce(answers_json,'{}'),'$." + kind + "',?) where id=? and status='STARTED'",
        write(obj("at", iso(now), "item", kind, "code", code, "console", console.view())), code, id);
    return obj("console", console.view());
  }

  /** POST /api/board/tests/{id}/finish: the final answers (inside the time) and the checks now; the LLM later. */
  Map<String, Object> finish(long user, long id, Map<String, Object> body) {
    Instant now = now(); settle(now);
    var t = own(user, id);
    if ("STARTED".equals(t.get("status"))) {
      var answers = submitted(body, items(t));
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
  /**
   * The answers of a request body, validated against the test's items: code and fix — text; parsons — ids of the item's
   * lines, each at most once. A field of a kind the test does not have is an error; absent and null fields are left out.
   */
  private static Map<String, Object> submitted(Map<String, Object> body, List<Map<String, Object>> items) {
    var answers = new HashMap<String, Object>();
    if (body == null) return answers;
    for (var key : BoardItems.ALL) {
      Object value = body.get(key);
      if (value == null) continue;
      var item = items.stream().filter(i -> key.equals(i.get("kind"))).findFirst().orElse(null);
      if (item == null) throw new ApiError("INVALID_ANSWER", "В этом тесте нет задания «" + BoardItems.kind(key).title() + "»");
      if ("parsons".equals(key)) {
        if (!(value instanceof List<?> list)) throw new ApiError("INVALID_ANSWER", "parsons — список строк программы");
        var known = new HashSet<Object>(); for (var line : lineList(item)) known.add(line.get("id"));
        var ids = new ArrayList<String>();
        for (Object v : list) {
          if (!(v instanceof String lineId) || !known.contains(lineId)) throw new ApiError("INVALID_ANSWER", "Нет такой строки: " + v);
          if (ids.contains(lineId)) throw new ApiError("INVALID_ANSWER", "Строка " + lineId + " поставлена дважды");
          ids.add(lineId);
        }
        answers.put(key, ids);
      } else {
        if (!(value instanceof String text)) throw new ApiError("INVALID_ANSWER", key + " должен быть строкой");
        if (text.length() > ApiController.SOURCE_LIMIT) throw new ApiError("ANSWER_TOO_LONG", "Код длиннее " + ApiController.SOURCE_LIMIT + " символов");
        answers.put(key, text);
      }
    }
    return answers;
  }

  /** The student's view: the items as shown, the answers and the time — never the solution order, the extra line, the reference, the bug, checks, grades or the assessment. */
  private Map<String, Object> studentView(Map<String, Object> t) {
    var items = new ArrayList<Map<String, Object>>();
    var answers = answers(t); var shown = new LinkedHashMap<String, Object>();
    for (var item : items(t)) {
      String kind = (String) item.get("kind");
      var view = obj("kind", kind, "title", item.get("title"), "statement", item.get("statement"), "language", item.get("language"));
      switch (kind) {
        case "parsons" -> {
          view.put("before", item.get("before")); view.put("after", item.get("after"));
          view.put("lines", lineList(item).stream().map(l -> obj("id", l.get("id"), "text", l.get("text"))).toList()); view.put("extraLines", item.get("extraLines"));
        }
        case "fix" -> view.put("program", item.get("program"));
        default -> view.put("starterCode", item.get("starterCode"));
      }
      items.add(view); shown.put(kind, answers.get(kind));
    }
    return obj("id", t.get("id"), "status", t.get("status"), "startedAt", t.get("started_at"), "endsAt", t.get("ends_at"), "now", iso(now()), "durationSeconds", duration(t),
        "items", items, "answers", shown);
  }

  // ---------------------------------------------------------------- items

  /** A task the test may use; story: «curated:<slug>:» for the bank's variants, null for a task that is a story of its own. */
  private record Candidate(long id, String skill, String title, String statement, String starter, Integer difficulty, boolean curated, String key, String reference, String wrongJson, String story) {
    String storyOrTask() { return story == null ? "task:" + id : story; }
  }
  private record Passed(String skill, int block, long at) {}
  /** A candidate that fits a kind; detail — the Bug (fix), the Parsons (parsons) or the added lines (code); rank — the kind's own preference, lower first. */
  private record Fit(Candidate task, Object detail, int rank) {}

  /**
   * The items of the chosen kinds, in the canonical order. code: the first «recent» topic (passed by practice, the most
   * recent first; then confirmed by the diagnostic; then the course's first topic) with a candidate; fix: the same
   * topics, another topic than the code item's first; parsons: an «older» topic first (passed more than RECENT_DAYS ago).
   * Regular tasks only, so a hard-mode student gets the same kind of test; no task or story twice in a test.
   */
  private List<Map<String, Object>> chooseItems(long user, Language lang, List<String> kinds, Instant now) {
    var practiced = db.query("select s.code,s.block_no,coalesce("
        + "(select max(" + epoch("x.created_at") + ") from skill_iterations i join submissions x on x.lesson_id=i.lesson_id and x.passed=1 join task_target_skills ts on ts.task_id=x.task_id and ts.skill_code=i.skill_code where i.user_id=p.user_id and i.skill_code=s.code and i.iteration_number=1),"
        + "(select " + epoch("l.started_at") + " from skill_iterations i join lessons l on l.id=i.lesson_id where i.user_id=p.user_id and i.skill_code=s.code and i.iteration_number=1),0) as at "
        + "from student_skills p join skills s on s.code=p.skill_code where p.user_id=? and s.language=? and (p.completed_iterations>=1 or p.mastered=1) order by at desc,s.block_no desc,s.sort_order desc",
        (rs, i) -> new Passed(rs.getString(1), rs.getInt(2), rs.getLong(3)), user, lang.name());
    var practicedCodes = practiced.stream().map(Passed::skill).toList();
    var confirmed = db.queryForList("select s.code from diagnostic_skill_results d join skills s on s.code=d.skill_code where d.user_id=? and d.confirmed=1 and s.language=? order by s.block_no desc,s.sort_order desc", String.class, user, lang.name())
        .stream().filter(code -> !practicedCodes.contains(code)).toList();
    var course = db.queryForList("select code from skills where language=? order by block_no,sort_order,code", String.class, lang.name());
    Set<Long> solvedTasks = new HashSet<>(db.queryForList("select task_id from successful_task_credit where user_id=?", Long.class, user));
    Set<String> solvedStories = new HashSet<>();
    for (String key : db.queryForList("select t.external_key from successful_task_credit c join tasks t on t.id=c.task_id where c.user_id=? and t.source='CURATED' and t.external_key like 'curated:%:%'", String.class, user))
      solvedStories.add(story(key));
    Map<String, List<Candidate>> byTopic = new HashMap<>();
    for (var c : db.query("select t.id,ts.skill_code,t.title,t.statement,t.starter_code,t.difficulty,t.source='CURATED',t.external_key,t.reference_code,t.wrong_json from tasks t join task_target_skills ts on ts.task_id=t.id "
        + "where t.language=? and t.active=1 and t.mode='NORMAL' and coalesce(t.goal_json,'') not like '%IO_BEHAVIOR%'", (rs, i) -> candidate(rs), lang.name()))
      byTopic.computeIfAbsent(c.skill(), k -> new ArrayList<>()).add(c);
    Set<Long> usedTasks = new HashSet<>(); Set<String> usedStories = new HashSet<>();
    Map<String, Fit> chosen = new HashMap<>();

    // Passed by practice (most recent first), confirmed by the diagnostic, then the course from its start (its first topics
    // may have no bank task with a reference and wrong solutions for «Исправь ошибку»).
    var passedTopics = new LinkedHashSet<String>(practicedCodes); passedTopics.addAll(confirmed);
    var recent = new LinkedHashSet<String>(passedTopics); recent.addAll(course);
    if (kinds.contains("code")) chosen.put("code", pick(lang, "code", recent, byTopic, solvedTasks, solvedStories, usedTasks, usedStories));
    if (kinds.contains("fix")) {
      // Another passed topic than the code item's first, else the same topic with another story, then the course.
      var topics = new LinkedHashSet<String>(passedTopics);
      if (chosen.containsKey("code")) { String codeTopic = chosen.get("code").task().skill(); topics.remove(codeTopic); topics.add(codeTopic); }
      topics.addAll(course);
      chosen.put("fix", pick(lang, "fix", topics, byTopic, solvedTasks, solvedStories, usedTasks, usedStories));
    }
    if (kinds.contains("parsons")) {
      // Passed more than RECENT_DAYS ago, then the other passed or confirmed topics, then the topics of this test's other items, then the course from its start.
      long border = now.minus(Duration.ofDays(RECENT_DAYS)).getEpochSecond();
      var taken = chosen.values().stream().map(f -> f.task().skill()).toList();
      var others = new ArrayList<String>(practiced.stream().filter(p -> p.at() > border).map(Passed::skill).toList()); others.addAll(confirmed); others.removeAll(taken);
      var topics = new LinkedHashSet<String>(shuffled(practiced.stream().filter(p -> p.at() <= border).map(Passed::skill).toList()));
      topics.addAll(shuffled(others)); topics.addAll(taken); topics.addAll(course);
      chosen.put("parsons", pick(lang, "parsons", topics, byTopic, solvedTasks, solvedStories, usedTasks, usedStories));
    }

    Map<String, String> titles = new HashMap<>();
    db.query("select code,title from skills where language=?", (RowCallbackHandler) rs -> titles.put(rs.getString(1), rs.getString(2)), lang.name());
    var items = new ArrayList<Map<String, Object>>();
    for (String kind : kinds) {
      var fit = chosen.get(kind); var c = fit.task();
      var item = obj("kind", kind, "language", lang.name(), "taskId", c.id(), "externalKey", c.key(), "skillCode", c.skill(), "skillTitle", titles.get(c.skill()),
          "difficulty", c.difficulty(), "title", c.title(), "statement", c.statement());
      switch (kind) {
        case "parsons" -> parsonsItem(item, (BoardItems.Parsons) fit.detail(), c.reference());
        case "fix" -> { var bug = (BoardItems.Bug) fit.detail(); item.put("program", bug.program()); item.put("bugDescription", bug.description()); item.put("reference", c.reference()); }
        default -> item.put("starterCode", c.starter());
      }
      items.add(item);
    }
    return items;
  }

  /** The first topic with a candidate of the kind: curated first, an unsolved story, the kind's difficulty order, the kind's own preference, then random. */
  private Fit pick(Language lang, String kind, Collection<String> topics, Map<String, List<Candidate>> byTopic, Set<Long> solvedTasks, Set<String> solvedStories,
                   Set<Long> usedTasks, Set<String> usedStories) {
    var difficulties = BoardItems.kind(kind).difficulties();
    for (String topic : topics) {
      var fits = new ArrayList<Fit>();
      for (var c : shuffled(byTopic.getOrDefault(topic, List.of()))) {
        if (usedTasks.contains(c.id()) || usedStories.contains(c.storyOrTask())) continue;
        var fit = fit(lang, kind, c);
        if (fit != null) fits.add(fit);
      }
      fits.sort(Comparator.comparing((Fit f) -> !f.task().curated()).thenComparing(f -> solved(f.task(), solvedTasks, solvedStories))
          .thenComparingInt(f -> f.task().difficulty() == null || !difficulties.contains(f.task().difficulty()) ? difficulties.size() : difficulties.indexOf(f.task().difficulty()))
          .thenComparingInt(Fit::rank));
      if (!fits.isEmpty()) { var f = fits.getFirst(); usedTasks.add(f.task().id()); usedStories.add(f.task().storyOrTask()); return f; }
    }
    throw new ApiError("NO_BOARD_TASK", "Для задания «" + BoardItems.kind(kind).title() + "» не нашлось задачи по пройденным темам");
  }
  /** Whether a task fits a kind: parsons — the starter/reference shape (a distractor preferred), fix — a small bug among the wrong solutions, code — any (a short one preferred). */
  private Fit fit(Language lang, String kind, Candidate c) {
    switch (kind) {
      case "parsons" -> { var p = BoardItems.parsons(lang, c.starter(), c.reference(), wrong(c)); return p == null ? null : new Fit(c, p, p.extra() == null ? 1 : 0); }
      case "fix" -> { var bug = BoardItems.bug(lang, c.reference(), wrong(c)); return bug == null ? null : new Fit(c, bug, bug.changed()); }
      default -> { Integer added = BoardItems.added(lang, c.starter(), c.reference()); return new Fit(c, added, added == null || added <= BoardItems.SHORT_CODE_LINES ? 0 : 1); }
    }
  }
  private List<BoardItems.Wrong> wrong(Candidate c) {
    if (c.wrongJson() == null || c.wrongJson().isBlank()) return List.of();
    try {
      var list = new ArrayList<BoardItems.Wrong>();
      for (var w : json.readTree(c.wrongJson())) if (w.path("source").isTextual()) list.add(new BoardItems.Wrong(w.path("description").asText(""), w.path("source").asText()));
      return list;
    } catch (Exception e) { log.warn("Task {}: wrong_json is not readable: {}", c.id(), e.toString()); return List.of(); }
  }
  /**
   * The lines of a parsons item shuffled once (never in the solution order when another order exists), then numbered
   * l1…lN in the order shown; solution — the ids in the reference order; extraLineId — the extra line or null.
   */
  private void parsonsItem(Map<String, Object> item, BoardItems.Parsons p, String reference) {
    var pool = new ArrayList<String>(p.block()); if (p.extra() != null) pool.add(p.extra());
    var order = new ArrayList<Integer>(); for (int i = 0; i < pool.size(); i++) order.add(i);
    boolean another = new HashSet<>(p.block()).size() > 1;
    for (int attempt = 0; attempt < 100; attempt++) {
      Collections.shuffle(order, random);
      if (!another || !order.stream().filter(i -> i < p.block().size()).map(p.block()::get).toList().equals(p.block())) break;
    }
    var lines = new ArrayList<Map<String, Object>>(); var ids = new String[pool.size()];
    for (int shown = 0; shown < order.size(); shown++) { ids[order.get(shown)] = "l" + (shown + 1); lines.add(obj("id", "l" + (shown + 1), "text", pool.get(order.get(shown)))); }
    item.put("before", p.before()); item.put("after", p.after()); item.put("lines", lines); item.put("extraLines", p.extra() == null ? 0 : 1);
    item.put("solution", Arrays.asList(ids).subList(0, p.block().size())); item.put("extraLineId", p.extra() == null ? null : ids[pool.size() - 1]); item.put("reference", reference);
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

  /** The checks of a finished test: every item's program like a lesson attempt (not credited); the grade by the checks; then the LLM. */
  void check(long id) {
    if (!processing.add("check:" + id)) return;
    try {
      var t = load(id);
      if (!"FINISHED".equals(t.get("status")) || t.get("results_json") != null) return;
      Language lang = Language.of(t.get("language"));
      var answers = answers(t); var results = new ArrayList<Map<String, Object>>();
      for (var item : items(t)) {
        String kind = (String) item.get("kind");
        try { results.add(checkItem(lang, item, answers.get(kind))); }
        catch (RuntimeException e) {
          log.error("Board test {}: the {} item could not be checked", id, kind, e);
          results.add(failedCheck(kind, "Проверка не удалась: " + e.getMessage()));
        }
      }
      int rule = grade(results, null);
      db.update("update board_tests set results_json=?,rule_grade=?,suggested_grade=? where id=?", write(results), String.valueOf(rule),
          String.valueOf(suggested(rule, cap((String) t.get("pace_status")))), id);
      log.info("Board test {} checked: {}, rule grade {}", id, results.stream().map(r -> r.get("kind") + (Boolean.TRUE.equals(r.get("passed")) ? " passed" : " failed")).toList(), rule);
      startAssessment(id);
    } catch (RuntimeException e) {
      // Stored as a failed check, so that the test is not checked again and again; the teacher grades it alone.
      log.error("Board test {} could not be checked", id, e);
      String error = "Проверка не удалась: " + e.getMessage();
      var results = new ArrayList<Map<String, Object>>();
      try { for (var item : items(load(id))) results.add(failedCheck((String) item.get("kind"), error)); } catch (RuntimeException ignored) {}
      db.update("update board_tests set results_json=?,rule_grade='2',suggested_grade='2',assessment_json=? where id=? and results_json is null", write(results), write(unavailable(error)), id);
    } finally { processing.remove("check:" + id); }
  }
  private static Map<String, Object> failedCheck(String kind, String error) {
    var result = obj("kind", kind, "passed", false, "output", error, "outcome", null, "console", null, "unavailable", true);
    if ("parsons".equals(kind)) result.put("program", null);
    return result;
  }

  /** One item: parsons — the program assembled from before + the placed lines + after; fix and code — the student's final code. */
  private Map<String, Object> checkItem(Language lang, Map<String, Object> item, Object answer) {
    String kind = (String) item.get("kind");
    if (!"parsons".equals(kind)) return checkProgram(lang, kind, item, answer instanceof String code ? code : null);
    var texts = new HashMap<Object, String>(); for (var line : lineList(item)) texts.put(line.get("id"), (String) line.get("text"));
    var placed = answer instanceof List<?> ids ? ids.stream().filter(texts::containsKey).map(texts::get).toList() : List.<String>of();
    if (placed.isEmpty()) { var result = obj("kind", kind, "passed", false, "output", "Программа не собрана", "outcome", null, "console", null, "unavailable", false); result.put("program", null); return result; }
    String program = BoardItems.assemble((String) item.get("before"), placed, (String) item.get("after"));
    var result = checkProgram(lang, kind, item, program); result.put("program", program);
    return result;
  }
  private Map<String, Object> checkProgram(Language lang, String kind, Map<String, Object> item, String code) {
    var result = obj("kind", kind, "passed", false, "output", null, "outcome", null, "console", null, "unavailable", false);
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

  /** The LLM's verdicts in the background; UNAVAILABLE at once when the LLM is off. */
  private void startAssessment(long id) {
    if (!generator.available()) { db.update("update board_tests set assessment_json=? where id=?", write(unavailable("LLM выключена или недоступна")), id); return; }
    db.update("update board_tests set assessment_json=? where id=?", write(Map.of("status", "PENDING")), id);
    executor.execute(() -> assess(id));
  }
  private static Map<String, Object> unavailable(String error) { return obj("status", "UNAVAILABLE", "summary", null, "items", List.of(), "questions", List.of(), "studentComment", null, "error", error); }

  /** The LLM's verdicts and questions; the grade again with «частично верно» as half of a failed item → the suggested grade (the rule grade stays the checks' one). */
  void assess(long id) {
    if (!processing.add("assess:" + id)) return;
    try {
      var t = load(id);
      if (!(t.get("assessment") instanceof Map<?, ?> a) || !"PENDING".equals(a.get("status")) || t.get("results_json") == null) return;
      var items = items(t); var answers = answers(t); var results = results(t);
      var runs = runs(t); var recentRuns = new ArrayList<BoardAssessmentRequest.Run>();
      for (var run : runs.subList(Math.max(0, runs.size() - LLM_RUNS), runs.size())) {
        var console = run.get("console") instanceof Map<?, ?> c ? c : Map.of();
        recentRuns.add(new BoardAssessmentRequest.Run(run.get("item") == null ? "code" : (String) run.get("item"), (String) run.get("code"), String.valueOf(console.get("status")), (String) console.get("stdout"), (String) console.get("error")));
      }
      var requestItems = new ArrayList<BoardAssessmentRequest.Item>();
      for (var item : items) {
        String kind = (String) item.get("kind");
        var result = results.stream().filter(r -> kind.equals(r.get("kind"))).findFirst().orElse(Map.of());
        boolean passed = Boolean.TRUE.equals(result.get("passed")); String output = (String) result.get("output"); int weight = BoardItems.kind(kind).weight();
        requestItems.add(switch (kind) {
          case "parsons" -> {
            var texts = new HashMap<Object, String>(); for (var line : lineList(item)) texts.put(line.get("id"), (String) line.get("text"));
            var solution = item.get("solution") instanceof List<?> ids ? ids.stream().map(texts::get).toList() : List.<String>of();
            yield new BoardAssessmentRequest.Item(kind, (String) item.get("title"), (String) item.get("statement"), weight, solution, texts.get(item.get("extraLineId")), null, null,
                (String) result.get("program"), passed, output);
          }
          case "fix" -> new BoardAssessmentRequest.Item(kind, (String) item.get("title"), (String) item.get("statement"), weight, null, null, (String) item.get("program"), (String) item.get("bugDescription"),
              answers.get("fix") instanceof String s ? s : null, passed, output);
          default -> new BoardAssessmentRequest.Item(kind, (String) item.get("title"), (String) item.get("statement"), weight, null, null, null, null,
              answers.get("code") instanceof String s ? s : null, passed, output);
        });
      }
      String skill = (String) items.stream().filter(i -> "code".equals(i.get("kind"))).findFirst().orElse(items.getFirst()).get("skillCode");
      var request = new BoardAssessmentRequest(Language.of(t.get("language")), skill, requestItems, recentRuns, Integer.parseInt((String) t.get("rule_grade")));
      long user = ((Number) t.get("user_id")).longValue();
      Map<String, Object> assessment;
      try {
        assessment = generator.assessBoardTest(user, request).view();
      } catch (LlmUnavailableException e) {
        log.warn("Board test {} not assessed: {}", id, e.getMessage());
        assessment = unavailable(e.getMessage());
      }
      int grade = grade(results, assessment);
      String suggestedGrade = String.valueOf(suggested(grade, cap((String) t.get("pace_status"))));
      log.info("Board test {} assessed: {}, grade with the verdicts {}, suggested {}", id, assessment.get("status"), grade, suggestedGrade);
      db.update("update board_tests set assessment_json=?,suggested_grade=? where id=?", write(assessment), suggestedGrade, id);
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

  /** POST /api/admin/board/call: a new call with the kinds chosen (all three when absent); the student's earlier calls that were not started are cancelled. */
  Map<String, Object> call(long admin, Map<String, Object> body) {
    if (body == null || !(body.get("userId") instanceof Number user)) throw new ApiError("INVALID_STUDENT", "Нужен userId студента");
    if (body.get("language") != null && !(body.get("language") instanceof String)) throw new ApiError("UNKNOWN_LANGUAGE", "Неизвестный язык курса");
    var kinds = BoardItems.parse(body.get("kinds"));
    return summary(load(call(admin, user.longValue(), Language.parse((String) body.get("language")), kinds)));
  }
  private long call(long admin, long user, Language lang, List<String> kinds) {
    var rows = db.queryForList("select group_name from users where id=? and role='STUDENT'", user);
    if (rows.isEmpty()) throw new NotFoundError("STUDENT_NOT_FOUND", "Студент не найден");
    Instant now = now(); settle(now);
    db.update("update board_tests set status='CANCELLED' where user_id=? and status='CALLED'", user);
    long id = db.queryForObject("insert into board_tests(user_id,group_name,language,status,called_at,called_by,call_expires_at,kinds,duration_seconds) values(?,?,?,'CALLED',?,?,?,?,?) returning id", Long.class,
        user, rows.getFirst().get("group_name"), lang.name(), iso(now), admin, iso(now.plus(CALL)), write(kinds), BoardItems.seconds(kinds));
    log.info("Student {} called to the board ({}, {}) by admin {}: test {}", user, lang, kinds, admin, id);
    return id;
  }

  /** POST /api/admin/board/tests/{id}/recall: a new call for the same student, course and kinds. */
  Map<String, Object> recall(long admin, long id) {
    var t = load(id);
    return adminView(load(call(admin, ((Number) t.get("user_id")).longValue(), Language.of(t.get("language")), kinds(t))));
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
        "suggestedGrade", t.get("suggested_grade"), "finalGrade", t.get("final_grade"), "assessmentStatus", assessment, "kinds", kinds(t), "durationSeconds", duration(t));
  }
  /** Everything for the teacher: the items with the solution and the task, the answers, checks, the score, runs, pace, grades. */
  private Map<String, Object> adminView(Map<String, Object> t) {
    var view = summary(t);
    String pace = (String) t.get("pace_status");
    view.put("login", t.get("login")); view.put("group", t.get("group_name")); view.put("language", t.get("language"));
    view.put("items", t.get("items_json") == null ? null : items(t)); view.put("answers", t.get("answers_json") == null ? null : answers(t));
    view.put("results", t.get("results_json") == null ? null : results(t)); view.put("score", t.get("results_json") == null ? null : score(results(t), (Map<?, ?>) t.get("assessment")));
    view.put("runs", runs(t));
    view.put("paceStatus", pace); view.put("paceCap", cap(pace)); view.put("ruleGrade", t.get("rule_grade")); view.put("assessment", t.get("assessment"));
    view.put("comment", t.get("comment")); view.put("gradedAt", t.get("graded_at"));
    return view;
  }

  /** The score table: per item its weight and score (0, 0.5, 1); the points, the maximum and the percent (one decimal). */
  private static Map<String, Object> score(List<Map<String, Object>> results, Map<?, ?> assessment) {
    var scores = scores(results, assessment); var items = new ArrayList<Map<String, Object>>(); double points = 0; int max = 0;
    for (var e : scores.entrySet()) { int weight = BoardItems.kind(e.getKey()).weight(); items.add(obj("kind", e.getKey(), "weight", weight, "score", e.getValue())); points += weight * e.getValue(); max += weight; }
    return obj("items", items, "points", points, "max", max, "percent", Math.round(BoardItems.percent(scores) * 10) / 10.0);
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
  private Map<String, Object> answers(Map<String, Object> t) { return t.get("answers_json") == null ? Map.of() : read((String) t.get("answers_json"), new TypeReference<LinkedHashMap<String, Object>>() {}); }
  @SuppressWarnings("unchecked")
  private static List<Map<String, Object>> lineList(Map<String, Object> item) { return item.get("lines") instanceof List<?> lines ? (List<Map<String, Object>>) lines : List.of(); }
  /** The test's kinds in the canonical order (a row without them: all three). */
  private List<String> kinds(Map<String, Object> t) { return t.get("kinds") == null ? BoardItems.ALL : read((String) t.get("kinds"), new TypeReference<List<String>>() {}); }
  private int duration(Map<String, Object> t) { return t.get("duration_seconds") instanceof Number n ? n.intValue() : BoardItems.seconds(kinds(t)); }
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
