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
 * программу», fix «Исправь ошибку», code «Напиши код»); the student starts the test within CALL at the board station
 * (BoardStations, no sign-in) or, when the teacher allows it, from his own account; one
 * timer — the sum of the kinds' minutes. The answers are autosaved; the client submits at 0, and the server finishes a
 * test whose time is over (after GRACE) with the last autosaved answers — lazily on every board request and every 15 s
 * (BoardTestFinisher).
 * <p>After the finish every item's program is checked like a lesson attempt; nothing is credited. The weighted grade by
 * the checks, the LLM's verdicts (asynchronous, a platform thread: «частично верно» gives half of a failed item's weight)
 * and the floor of a student ahead of the minimum (floor) give a suggested grade; the teacher sets the final one. The student sees only the test itself and,
 * later, the date, the final grade and the comment. Rules: backend/README.md, «К доске».
 */
@Component
class BoardTests implements DisposableBean {
  private static final Logger log = LoggerFactory.getLogger(BoardTests.class);
  static final Duration CALL = Duration.ofMinutes(5), GRACE = Duration.ofSeconds(15);
  /** A student at or below the minimum: the last topics of the minimum that «Собери программу» avoids (code and fix take them). */
  static final int PACE_RECENT = 3;
  /** A student ahead of the minimum: «Собери программу» comes from the last topics of the minimum first. */
  static final int PARSONS_LAST = 5;
  /** board_tests.source: RANGE — the one rule since 2026-10-22; LEVEL and PACE — older calls (the student's level / the minimum). */
  static final String SOURCE_RANGE = "RANGE", SOURCE_LEVEL = "LEVEL", SOURCE_PACE = "PACE";
  /** A member is present with activity in the course within this many minutes or an open lesson. */
  static final int PRESENT_MINUTES = 60;
  /** Runs the LLM sees; the oldest of a longer history are left out. */
  static final int LLM_RUNS = 10;
  static final int COMMENT_MAX = 1000, EXTEND_MAX_SECONDS = 1800;
  /** Recent finished, cancelled and expired tests stay in the teacher's «active» panel this long. */
  static final Duration ACTIVE_RECENT = Duration.ofHours(2);
  static final List<String> GRADES = List.of("2", "3", "4", "5");
  /** app_settings: "true" — a student may start his test from his own account; else only at a board station (BoardStations). */
  static final String STUDENT_START_KEY = "board_student_start";
  /** app_settings: the day whose plan line an attestation covers (owner, 2026-10-27: «темп на пн 26.10» for every group); absent — the day of the attestation. */
  static final String ATTESTATION_PLAN_KEY = "attestation_plan_date";
  /**
   * board_tests.format: TEST — the items the teacher chose; ATTESTATION (owner, 2026-10-27) — one integrative «Напиши код»
   * task of the attestation pool over the group's plan, usually several students at once at their own computers, with
   * lessons and the assistant closed meanwhile (requireNoAttestation). Its time: ATTESTATION_MINUTES unless the teacher says.
   */
  static final String FORMAT_TEST = "TEST", FORMAT_ATTESTATION = "ATTESTATION";
  static final int ATTESTATION_MINUTES = 10;

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

  /** The lowest grade of a student ahead of the minimum whose items from the minimum all count fully (see floor). */
  static final int FLOOR = 4;
  /**
   * Whether the floor applies (owner, 2026-10-22: a harder topic above the minimum is a chance, not a risk): the test has
   * items from the minimum and above it, and every item from the minimum counts fully. Null — the test has no such mix
   * (the student is not ahead, the teacher chose no item from the minimum, or a test before the zones). The pace of the
   * student does not cap the grade any more.
   */
  static Boolean floor(List<Map<String, Object>> items, Map<String, Double> scores) {
    boolean minimum = false, above = false, met = true;
    for (var item : items) {
      Double score = scores.get(item.get("kind"));
      if (score == null) continue;
      if (ZONE_ABOVE.equals(item.get("zone"))) above = true;
      else if (ZONE_MINIMUM.equals(item.get("zone"))) { minimum = true; met &= score >= 1; }
    }
    return minimum && above ? met : null;
  }
  /** The suggested grade: by the points, at least FLOOR when the floor is met. */
  static int suggested(List<Map<String, Object>> items, List<Map<String, Object>> results, Map<?, ?> assessment) {
    int grade = grade(results, assessment);
    return Boolean.TRUE.equals(floor(items, scores(results, assessment))) ? Math.max(grade, FLOOR) : grade;
  }
  /**
   * Per item of a checked test (in its order) the score: passed → 1; else the LLM's verdict (a DONE assessment) «верно» → 1
   * (e.g. the logic is right and only the format of the output differs), «частично верно» → 0.5; else 0. Without an
   * assessment — the grade by the checks alone.
   */
  static Map<String, Double> scores(List<Map<String, Object>> results, Map<?, ?> assessment) {
    var llm = new HashMap<Object, Double>();
    if (assessment != null && "DONE".equals(assessment.get("status")) && assessment.get("items") instanceof List<?> verdicts)
      for (var v : verdicts) if (v instanceof Map<?, ?> m) {
        if (BoardAssessment.RIGHT.equals(m.get("verdict"))) llm.put(m.get("item"), 1.0); else if (BoardAssessment.PARTLY.equals(m.get("verdict"))) llm.put(m.get("item"), 0.5);
      }
    var scores = new LinkedHashMap<String, Double>();
    // A test of the first version (2026-10-15) may hold an «output» item: no kind of today, no score.
    for (var r : results) if (BoardItems.ALL.contains(r.get("kind"))) scores.put((String) r.get("kind"), Boolean.TRUE.equals(r.get("passed")) ? 1.0 : llm.getOrDefault(r.get("kind"), 0.0));
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
  Map<String, Object> current(long user) { return current(user, null); }
  Map<String, Object> current(long user, String device) {
    settle();
    var calls = db.queryForList("select id,called_at,call_expires_at,kinds,duration_seconds,format from board_tests where user_id=? and status='CALLED' order by id desc limit 1", user);
    var running = db.queryForList("select id from board_tests where user_id=? and status='STARTED' order by id desc limit 1", Long.class, user);
    var c = calls.isEmpty() ? null : calls.getFirst();
    var call = c == null ? null : obj("id", c.get("id"), "calledAt", c.get("called_at"), "expiresAt", c.get("call_expires_at"), "kinds", kinds(c), "durationSeconds", duration(c),
        "canStart", attestation(c) || studentStart(), "format", format(c));
    return obj("call", call, "test", running.isEmpty() ? null : studentView(load(running.getFirst()), device));
  }

  /**
   * POST /api/board/tests/{id}/start: only the called student, while the call is active, and only when the teacher lets
   * students start from their own account (studentStart; else the test starts at a board station) — an attestation always
   * (the students answer at their own computers); the items are chosen now.
   */
  Map<String, Object> start(long user, long id) { return start(user, id, null); }
  Map<String, Object> start(long user, long id, String device) {
    Instant now = now(); settle(now);
    var t = own(user, id);
    if ("STARTED".equals(t.get("status"))) return studentView(t, device);
    requireCalled(t);
    if (!attestation(t) && !studentStart()) throw new ApiError("BOARD_START_AT_STATION", "Тест начинается на компьютере у доски — подойди к нему");
    return studentView(begin(t, device, null, now), device);
  }

  /**
   * CALLED → STARTED: the items, the initial answers, the pace status, the browser (device) and the station (null — the
   * student's own account). The update requires the kinds, the source and the time read here, so a teacher's edit of the
   * call in between is never lost: the items are chosen again (once). A station starts only while no other test runs at it.
   */
  private Map<String, Object> begin(Map<String, Object> t, String device, Long station, Instant now) {
    long id = ((Number) t.get("id")).longValue(), user = ((Number) t.get("user_id")).longValue();
    for (int attempt = 0; ; attempt++) {
      Language lang = Language.of(t.get("language"));
      var items = attestation(t) ? List.of(attestationItem(user, lang, (String) t.get("group_name"), now, Set.of()))
          : chooseItems(user, lang, kinds(t), minimumTopics((String) t.get("group_name"), lang, now), now);
      String pace = paceStatus(user, lang, now);
      var answers = new LinkedHashMap<String, Object>();
      for (var item : items) answers.put((String) item.get("kind"), initialAnswer(item));
      var params = new ArrayList<Object>(Arrays.asList(iso(now), iso(now.plusSeconds(duration(t))), write(items), write(answers), pace, deviceHash(device), station, id, iso(now), t.get("kinds"), t.get("source"), t.get("duration_seconds")));
      if (station != null) params.add(station);
      int started = db.update("update board_tests set status='STARTED',started_at=?,ends_at=?,items_json=?,answers_json=?,runs_json='[]',pace_status=?,device=?,station_id=? "
          + "where id=? and status='CALLED' and call_expires_at>=? and kinds is ? and source is ? and duration_seconds is ?"
          + (station == null ? "" : " and not exists(select 1 from board_tests x where x.station_id=? and x.status='STARTED')"), params.toArray());
      var after = load(id);
      var tasks = items.stream().map(i -> i.get("kind") + " " + i.get("taskId")).toList();
      if (started > 0) {
        if (station == null) log.info("Board test {} started by student {}: tasks {}, pace {}", id, user, tasks, pace);
        else log.info("Board test {} started at station {} for student {}: tasks {}, pace {}", id, station, user, tasks, pace);
        return after;
      }
      if ("STARTED".equals(after.get("status"))) {
        if (station != null && !station.equals(station(after))) throw elsewhere();
        return after;
      }
      requireCalled(after);
      if (station != null && busy(station)) throw new ApiError("BOARD_STATION_BUSY", "На этом компьютере уже идёт тест");
      if (attempt > 0) throw new ApiError("BOARD_CALL_CHANGED", "Вызов только что изменился — начни тест ещё раз");
      log.info("Board test {}: the call changed while starting, choosing the items again", id);
      t = after;
    }
  }
  /** The answer an item starts with: parsons — nothing placed, fix — the program with the bug, code — the starter. */
  private static Object initialAnswer(Map<String, Object> item) {
    return switch ((String) item.get("kind")) {
      case "parsons" -> List.of();
      case "fix" -> item.get("program");
      default -> item.get("starterCode") == null ? "" : item.get("starterCode");
    };
  }

  /** Whether students may start their test from their own account (app_settings board_student_start; off by default). */
  boolean studentStart() { return db.queryForList("select value from app_settings where key=?", String.class, STUDENT_START_KEY).stream().anyMatch("true"::equals); }
  /** GET /api/admin/board/settings. */
  Map<String, Object> settings() { var day = attestationPlanDate(); return obj("studentStart", studentStart(), "attestationPlanDate", day == null ? null : day.toString()); }
  /** The day of the plan line attestations cover; null — the day of each attestation. */
  LocalDate attestationPlanDate() {
    return db.queryForList("select value from app_settings where key=?", String.class, ATTESTATION_PLAN_KEY).stream().findFirst().map(LocalDate::parse).orElse(null);
  }
  /**
   * PUT /api/admin/board/settings {studentStart?: boolean, attestationPlanDate?: "YYYY-MM-DD" | null}: only the fields
   * present (at least one).
   */
  Map<String, Object> saveSettings(long admin, Map<String, Object> body) {
    if (body == null || !body.containsKey("studentStart") && !body.containsKey("attestationPlanDate")) throw new ApiError("INVALID_SETTINGS", "Нужны studentStart и/или attestationPlanDate");
    if (body.containsKey("studentStart")) {
      if (!(body.get("studentStart") instanceof Boolean on)) throw new ApiError("INVALID_SETTINGS", "studentStart — true или false");
      db.update("insert into app_settings(key,value) values(?,?) on conflict(key) do update set value=excluded.value", STUDENT_START_KEY, on.toString());
      log.info("Board settings changed by admin {}: students start from their own account {}", admin, on);
    }
    if (body.containsKey("attestationPlanDate")) {
      Object value = body.get("attestationPlanDate"); LocalDate day;
      try { day = value == null || value.toString().isBlank() ? null : LocalDate.parse(value.toString().strip()); }
      catch (Exception e) { throw new ApiError("INVALID_SETTINGS", "attestationPlanDate — дата ГГГГ-ММ-ДД или null"); }
      if (day == null) db.update("delete from app_settings where key=?", ATTESTATION_PLAN_KEY);
      else db.update("insert into app_settings(key,value) values(?,?) on conflict(key) do update set value=excluded.value", ATTESTATION_PLAN_KEY, day.toString());
      log.info("Board settings changed by admin {}: attestations cover the plan of {}", admin, day == null ? "their own day" : day);
    }
    return settings();
  }

  // ---------------------------------------------------------------- board station

  /**
   * GET /api/station/current: every active call (newest first) — the student whose name it is starts it here — and the
   * test running at this station (the newest), as the student sees it, with his name.
   */
  Map<String, Object> stationCurrent(Map<String, Object> station) {
    Instant now = now(); settle(now);
    var calls = db.queryForList("select b.*,u.display_name from board_tests b join users u on u.id=b.user_id where b.status='CALLED' and b.call_expires_at>=? order by b.called_at desc,b.id desc", iso(now)).stream()
        .map(c -> obj("id", c.get("id"), "displayName", c.get("display_name"), "group", c.get("group_name"), "language", c.get("language"), "kinds", kinds(c), "durationSeconds", duration(c),
            "calledAt", c.get("called_at"), "expiresAt", c.get("call_expires_at"), "canStart", true, "format", format(c))).toList();
    var running = db.queryForList("select id from board_tests where station_id=? and status='STARTED' order by id desc limit 1", Long.class, station.get("id"));
    return obj("station", station, "now", iso(now), "calls", calls, "test", running.isEmpty() ? null : stationView(load(running.getFirst())));
  }
  /** POST /api/station/tests/{id}/start: a call started at this station for its student; refused while another test runs here. */
  Map<String, Object> stationStart(long station, long id) {
    Instant now = now(); settle(now);
    var t = load(id);
    LogContext.student(t.get("user_id"), t.get("login"));
    if ("STARTED".equals(t.get("status"))) { if (Long.valueOf(station).equals(station(t))) return stationView(t); throw elsewhere(); }
    requireCalled(t);
    if (busy(station)) throw new ApiError("BOARD_STATION_BUSY", "На этом компьютере уже идёт тест");
    return stationView(begin(t, stationDevice(station), station, now));
  }
  /** The student of a test started at this station; any other test is «not found» to it. */
  long stationUser(long station, long id) {
    var t = load(id);
    if (!Long.valueOf(station).equals(station(t))) throw new NotFoundError("BOARD_TEST_NOT_FOUND", "Тест не найден");
    LogContext.student(t.get("user_id"), t.get("login"));
    return ((Number) t.get("user_id")).longValue();
  }
  /** The device of a station's tests (board_tests.device = its SHA-256): the student's own browser sees them «elsewhere». */
  static String stationDevice(long station) { return "station:" + station; }
  Map<String, Object> stationAnswers(long station, long id, Map<String, Object> body) { return saveAnswers(stationUser(station, id), id, body, stationDevice(station)); }
  Map<String, Object> stationFinish(long station, long id, Map<String, Object> body) { return finish(stationUser(station, id), id, body, stationDevice(station)); }
  private Map<String, Object> stationView(Map<String, Object> t) { var view = studentView(t); view.put("displayName", t.get("display_name")); return view; }
  private boolean busy(long station) { return count("select count(*) from board_tests where station_id=? and status='STARTED'", station) > 0; }
  private static Long station(Map<String, Object> t) { return t.get("station_id") instanceof Number n ? n.longValue() : null; }
  private static ApiError elsewhere() { return new ApiError("BOARD_TEST_ELSEWHERE", "Тест идёт на другом компьютере — у доски"); }

  /**
   * The browser that started the test owns it (board_tests.device): another browser of the same student — e.g. his own PC
   * left open while he answers at the board — sees only that the test runs elsewhere and cannot save, run or finish it.
   */
  private static String deviceHash(String device) { return device == null || device.isBlank() ? null : Hashing.sha256(device.strip()); }
  private static boolean elsewhere(Map<String, Object> t, String device) { return t.get("device") != null && !t.get("device").equals(deviceHash(device)); }
  private static void requireDevice(Map<String, Object> t, String device) {
    if (elsewhere(t, device)) throw elsewhere();
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
  Map<String, Object> saveAnswers(long user, long id, Map<String, Object> body) { return saveAnswers(user, id, body, null); }
  Map<String, Object> saveAnswers(long user, long id, Map<String, Object> body, String device) {
    Instant now = now(); settle(now);
    var t = own(user, id); requireDevice(t, device); requireRunning(t, now);
    var set = answersUpdate(submitted(body, items(t)));
    var params = new ArrayList<Object>(set.params()); params.add(id);
    if (db.update("update board_tests set answers_json=" + set.sql() + " where id=? and status='STARTED'", params.toArray()) == 0) throw over();
    return obj("savedAt", iso(now));
  }

  /** POST /api/board/tests/{id}/run: «Запустить» for the code or fix item — the console, recorded in the test's runs with its item; that answer is saved too. */
  Map<String, Object> run(long user, long id, Object item, String code) { return run(user, id, item, code, null); }
  Map<String, Object> run(long user, long id, Object item, String code, String device) { return run(user, id, item, code, device, null); }
  /** revision: the screen's revision of the test; a run of a replaced item's old code is shown but not saved as the answer. */
  Map<String, Object> run(long user, long id, Object item, String code, String device, Object revision) {
    Instant now = now(); settle(now);
    var t = own(user, id); requireDevice(t, device); requireRunning(t, now);
    String kind = item == null ? "code" : item instanceof String s ? s : "";
    if (!List.of("code", "fix").contains(kind) || !kinds(t).contains(kind)) throw new ApiError("INVALID_ITEM", "Запускать можно только код заданий этого теста «Исправь ошибку» и «Напиши код»");
    boolean stale = items(t).stream().anyMatch(i -> kind.equals(i.get("kind")) && stale(i, revision));
    Language lang = Language.of(t.get("language"));
    long started = System.nanoTime(); var console = runner.console(lang, code, "");
    log.info("Board test {} console run ({}, {}): {} in {} ms", id, lang, kind, console.status(), (System.nanoTime() - started) / 1_000_000);
    if (stale) log.info("Board test {}: a run of the replaced {} item, not saved as the answer", id, kind);
    else db.update("update board_tests set runs_json=json_insert(coalesce(runs_json,'[]'),'$[#]',json(?)),answers_json=json_set(coalesce(answers_json,'{}'),'$." + kind + "',?) where id=? and status='STARTED'",
        write(obj("at", iso(now), "item", kind, "code", code, "console", console.view())), code, id);
    return obj("console", console.view());
  }

  /** POST /api/board/tests/{id}/finish: the final answers (inside the time) and the checks now; the LLM later. */
  Map<String, Object> finish(long user, long id, Map<String, Object> body) { return finish(user, id, body, null); }
  Map<String, Object> finish(long user, long id, Map<String, Object> body, String device) {
    Instant now = now(); settle(now);
    var t = own(user, id); requireDevice(t, device);
    if ("STARTED".equals(t.get("status"))) {
      var answers = submitted(body, items(t));
      if (now.isAfter(instant(t.get("ends_at")).plus(GRACE))) answers = Map.of();
      if (claim(id, answers, now)) { log.info("Board test {} finished by the student", id); check(id); }
    } else if (!"FINISHED".equals(t.get("status"))) throw new ApiError("BOARD_TEST_NOT_STARTED", "Тест не начат");
    return obj("finished", true);
  }

  /**
   * GET /api/board/grades: the student's graded tests — the date (Moscow), the final grade, the comment and, when the
   * teacher shows it, the report (studentReport).
   */
  Map<String, Object> studentGrades(long user, Language lang) {
    return obj("grades", db.queryForList("select * from board_tests where user_id=? and language=? and final_grade is not null order by called_at desc,id desc", user, lang.name()).stream()
        .map(t -> { t.put("assessment", t.get("assessment_json") == null ? null : read((String) t.get("assessment_json"), new TypeReference<LinkedHashMap<String, Object>>() {}));
          return obj("id", t.get("id"), "date", instant(firstNonNull(t.get("started_at"), t.get("called_at"))).atZone(PairWork.MOSCOW).toLocalDate().toString(), "grade", t.get("final_grade"),
              "comment", t.get("comment"), "report", visible(t) ? studentReport(t) : null, "format", format(t)); }).toList());
  }
  private static Object firstNonNull(Object a, Object b) { return a != null ? a : b; }
  private static boolean visible(Map<String, Object> t) { return !(t.get("report_visible") instanceof Number n) || n.intValue() != 0; }

  /**
   * What the student may see of his test: per item (of today's kinds) the title, the statement, his own answer (the
   * assembled program for parsons), the verdict as in the score (passed or the LLM's «верно» → «верно», «частично верно»,
   * else «не верно»), the check message as a lesson shows it (a public example — expected/got, a hidden case — only its
   * number) and whether the extra line was used. Never the reference, the order of the solution, the bug, the LLM's
   * explanations or the points: the bank stories may still come up in his lessons and in his classmates' tests.
   */
  private List<Map<String, Object>> studentReport(Map<String, Object> t) {
    if (t.get("results_json") == null || t.get("items_json") == null) return List.of();
    var results = results(t); var scores = scores(results, (Map<?, ?>) t.get("assessment")); var answers = answers(t);
    var report = new ArrayList<Map<String, Object>>();
    for (var item : items(t)) {
      String kind = (String) item.get("kind");
      if (!BoardItems.ALL.contains(kind)) continue;
      var result = results.stream().filter(r -> kind.equals(r.get("kind"))).findFirst().orElse(Map.of());
      double score = scores.getOrDefault(kind, 0.0);
      Object answer = answers.get(kind); String code; Boolean extraUsed = null;
      if ("parsons".equals(kind)) {
        var texts = new HashMap<Object, String>(); for (var line : lineList(item)) texts.put(line.get("id"), (String) line.get("text"));
        var placed = answer instanceof List<?> ids ? ids.stream().filter(texts::containsKey).toList() : List.of();
        code = placed.isEmpty() ? null : BoardItems.assemble((String) item.get("before"), placed.stream().map(texts::get).toList(), (String) item.get("after"));
        if (item.get("extraLineId") != null) extraUsed = placed.contains(item.get("extraLineId"));
      } else code = answer instanceof String text && !text.isBlank() ? text : null;
      report.add(obj("kind", kind, "title", item.get("title"), "statement", item.get("statement"), "language", item.get("language"), "answer", code,
          "verdict", score >= 1 ? BoardAssessment.RIGHT : score > 0 ? BoardAssessment.PARTLY : "неверно", "passed", Boolean.TRUE.equals(result.get("passed")),
          "check", result.get("output"), "extraUsed", extraUsed));
    }
    return report;
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
  /**
   * An answer typed on a screen built before the item was replaced (the body's revision is older than the item's
   * replacedRevision) belongs to the old task: it is dropped. A body without a revision (an older client) is taken as is.
   */
  private static boolean stale(Map<String, Object> item, Object seen) {
    return seen instanceof Number n && item.get("replacedRevision") instanceof Number replacedAt && n.intValue() < replacedAt.intValue();
  }
  private static Map<String, Object> submitted(Map<String, Object> body, List<Map<String, Object>> items) {
    var answers = new HashMap<String, Object>();
    if (body == null) return answers;
    for (var key : BoardItems.ALL) {
      Object value = body.get(key);
      if (value == null) continue;
      var item = items.stream().filter(i -> key.equals(i.get("kind"))).findFirst().orElse(null);
      if (item == null) throw new ApiError("INVALID_ANSWER", "В этом тесте нет задания «" + BoardItems.kind(key).title() + "»");
      if (stale(item, body.get("revision"))) continue;
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
  /** Another browser than the one that started the test gets only {id, status, startedAt, endsAt, now, elsewhere: true}. */
  private Map<String, Object> studentView(Map<String, Object> t, String device) {
    if (elsewhere(t, device)) return obj("id", t.get("id"), "status", t.get("status"), "startedAt", t.get("started_at"), "endsAt", t.get("ends_at"), "now", iso(now()), "elsewhere", true, "format", format(t));
    return studentView(t);
  }
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
        "items", items, "answers", shown, "revision", revision(t), "format", format(t));
  }

  // ---------------------------------------------------------------- items

  /** A task the test may use; story: «curated:<slug>:» for the bank's variants, null for a task that is a story of its own. */
  private record Candidate(long id, String skill, String title, String statement, String starter, Integer difficulty, boolean curated, String key, String reference, String wrongJson, String story) {
    String storyOrTask() { return story == null ? "task:" + id : story; }
  }
  /** A candidate that fits a kind; detail — the Bug (fix), the Parsons (parsons) or the added lines (code); rank — the kind's own preference, lower first. */
  private record Fit(Candidate task, Object detail, int rank) {}
  /** Zones of a topic of an item (items_json «zone»): within the minimum for today, or above it (the student is ahead). */
  static final String ZONE_MINIMUM = "minimum", ZONE_ABOVE = "above";

  /**
   * The items of the chosen kinds, in the canonical order, from one range of topics (owner, 2026-10-22): from the minimum
   * for today (the first K topics of the course by the group's plan line, pacePlan; empty without a plan) up to the
   * student's farthest topic (passed by practice or confirmed by the diagnostic) — never beyond max(K, that topic).
   * A student ahead of the minimum: code — his topics above the minimum, the farthest first; fix — his topics above the
   * minimum, from the middle of the range; parsons — the minimum (its last topics first). A student at or below the
   * minimum: everything from the minimum, its last topics first (parsons: an earlier one). Each item remembers its zone.
   * Regular tasks only, so a hard-mode student gets the same kind of test; no task or story twice in a test.
   */
  private List<Map<String, Object>> chooseItems(long user, Language lang, List<String> kinds, List<String> minimum, Instant now) {
    return chooseItems(user, lang, kinds, minimum, now, new HashMap<>(), new HashSet<>(), new HashSet<>());
  }
  /** chosen, usedTasks, usedStories — what the test already holds (replaceItem): the new items avoid them and order their topics by them. */
  private List<Map<String, Object>> chooseItems(long user, Language lang, List<String> kinds, List<String> minimum, Instant now,
                                                Map<String, Fit> chosen, Set<Long> usedTasks, Set<String> usedStories) {
    var course = db.queryForList("select code from skills where language=? order by block_no,sort_order,code", String.class, lang.name());
    Set<String> reached = new HashSet<>(db.queryForList("select p.skill_code from student_skills p join skills s on s.code=p.skill_code where p.user_id=? and s.language=? and (p.completed_iterations>=1 or p.mastered=1)", String.class, user, lang.name()));
    reached.addAll(db.queryForList("select s.code from diagnostic_skill_results d join skills s on s.code=d.skill_code where d.user_id=? and d.confirmed=1 and s.language=?", String.class, user, lang.name()));
    Set<Long> solvedTasks = new HashSet<>(db.queryForList("select task_id from successful_task_credit where user_id=?", Long.class, user));
    Set<String> solvedStories = new HashSet<>();
    for (String key : db.queryForList("select t.external_key from successful_task_credit c join tasks t on t.id=c.task_id where c.user_id=? and t.source='CURATED' and t.external_key like 'curated:%:%'", String.class, user))
      solvedStories.add(story(key));
    Map<String, List<Candidate>> byTopic = new HashMap<>();
    for (var c : db.query("select t.id,ts.skill_code,t.title,t.statement,t.starter_code,t.difficulty,t.source='CURATED',t.external_key,t.reference_code,t.wrong_json from tasks t join task_target_skills ts on ts.task_id=t.id "
        + "where t.language=? and t.active=1 and t.mode='NORMAL' and coalesce(t.goal_json,'') not like '%IO_BEHAVIOR%'", (rs, i) -> candidate(rs), lang.name()))
      byTopic.computeIfAbsent(c.skill(), k -> new ArrayList<>()).add(c);

    var range = range(course, minimum.size(), reached);
    // The heaviest item first: code takes its topic, fix and parsons prefer other topics.
    for (String kind : List.of("code", "fix", "parsons")) if (kinds.contains(kind) && !chosen.containsKey(kind)) {
      var taken = chosen.values().stream().map(f -> f.task().skill()).toList();
      chosen.put(kind, pick(lang, kind, range.order(kind, taken, random), byTopic, solvedTasks, solvedStories, usedTasks, usedStories));
    }
    var items = itemsOf(lang, kinds, chosen);
    for (var item : items) item.put("zone", course.indexOf((String) item.get("skillCode")) < minimum.size() ? ZONE_MINIMUM : ZONE_ABOVE);
    return items;
  }

  /**
   * The range of a test's topics: minimum — the first K topics of the course (the minimum for today), above — the
   * student's reached topics beyond it (course order). The order of topics per kind is in chooseItems.
   */
  record Range(List<String> minimum, List<String> above) {
    boolean ahead() { return !above.isEmpty(); }
    /** The topics to try for a kind, best first; taken — the topics of the test's other items (they go last). */
    List<String> order(String kind, List<String> taken, Random random) {
      var latest = new ArrayList<>(minimum); Collections.reverse(latest);
      var farthest = new ArrayList<>(above); Collections.reverse(farthest);
      var topics = new LinkedHashSet<String>();
      switch (kind) {
        case "code" -> { topics.addAll(farthest); topics.addAll(latest); }
        case "fix" -> {
          // From the middle of the range above the minimum outwards, then the minimum from its end.
          double middle = (above.size() - 1) / 2.0;
          var byMiddle = new ArrayList<>(above); byMiddle.sort(Comparator.comparingDouble(t -> Math.abs(above.indexOf(t) - middle)));
          topics.addAll(byMiddle); topics.addAll(latest);
        }
        default -> {
          // The minimum: when ahead, its last PARSONS_LAST topics at random first; at or below it, an earlier topic than its
          // last PACE_RECENT (which code and fix take) at random first; then the rest of the minimum from its end, then the
          // topics above it from the nearest (without a plan: the student's topics from the earliest).
          int split = Math.max(0, minimum.size() - (above.isEmpty() ? PACE_RECENT : PARSONS_LAST));
          var head = new ArrayList<>(above.isEmpty() ? minimum.subList(0, split) : minimum.subList(split, minimum.size())); Collections.shuffle(head, random);
          topics.addAll(head); topics.addAll(latest); topics.addAll(above);
        }
      }
      var ordered = new ArrayList<String>(topics); ordered.removeAll(taken); ordered.addAll(taken.stream().filter(topics::contains).toList());
      return ordered;
    }
  }
  /** K topics of the minimum; above — the reached topics after them. Without anything reached and no plan: the course's first topic. */
  static Range range(List<String> course, int k, Set<String> reached) {
    var minimum = new ArrayList<>(course.subList(0, Math.min(k, course.size())));
    var above = course.subList(minimum.size(), course.size()).stream().filter(reached::contains).toList();
    if (minimum.isEmpty() && above.isEmpty() && !course.isEmpty()) minimum.add(course.getFirst());
    return new Range(minimum, above);
  }

  /**
   * The minimum for today of a group: the first K topics of the course (in its order), K — the group's plan line today
   * (ProgressAnalytics.plan: from the group's first lesson in the course to the session). Null without a plan.
   */
  record PacePlan(List<String> topics, int total, LocalDate start, LocalDate session) {}
  PacePlan pacePlan(String group, Language lang, Instant now) { return pacePlan(group, lang, ProgressAnalytics.day(now)); }
  PacePlan pacePlan(String group, Language lang, LocalDate day) {
    var plan = analytics.plan(group, lang);
    if (plan == null) return null;
    var course = db.queryForList("select code from skills where language=? order by block_no,sort_order,code", String.class, lang.name());
    return new PacePlan(course.subList(0, minimum(course.size(), plan.start(), plan.session(), day)), course.size(), plan.start(), plan.session());
  }
  /** The plan an attestation covers: the group's plan line on the day of the setting (attestationPlanDate), else on its own day. */
  private PacePlan attestationPlan(String group, Language lang, Instant now) {
    var day = attestationPlanDate();
    return pacePlan(group, lang, day == null ? ProgressAnalytics.day(now) : day);
  }
  /** The minimum for today of a group; empty without a plan (no session date or no lessons of the group in the course). */
  List<String> minimumTopics(String group, Language lang, Instant now) { var plan = pacePlan(group, lang, now); return plan == null ? List.of() : plan.topics(); }
  /** K of the plan: ⌈total × (day − start) / (session − start)⌉, at least 1, all topics on and after the session day. */
  static int minimum(int total, LocalDate start, LocalDate session, LocalDate today) {
    if (total == 0) return 0;
    long span = session.toEpochDay() - start.toEpochDay(), passed = today.toEpochDay() - start.toEpochDay();
    if (passed >= span) return total;
    return (int) Math.max(1, Math.min(total, Math.ceilDiv(total * Math.max(0, passed), span)));
  }

  // ---------------------------------------------------------------- attestation

  /** A task of the attestation pool; covers — it covers the course's topics 1…covers (its own topic is the last). */
  private record Option(long id, String skill, String title, String statement, String starter, String reference, String key, int covers) {}
  /**
   * The pool tasks that fit the group's plan (attestationPlan: of the set day or of today): the task's topic within the
   * plan (K topics; without a plan the whole course), never one of exclude.
   */
  private List<Option> attestationOptions(Language lang, String group, Instant now, Set<Long> exclude) {
    var course = db.queryForList("select code from skills where language=? order by block_no,sort_order,code", String.class, lang.name());
    var plan = attestationPlan(group, lang, now);
    int k = plan == null ? course.size() : plan.topics().size();
    var options = new ArrayList<Option>();
    db.query("select t.id,ts.skill_code,t.title,t.statement,t.starter_code,t.reference_code,t.external_key from tasks t join task_target_skills ts on ts.task_id=t.id where t.language=? and t.active=1 and t.mode=?",
        (RowCallbackHandler) rs -> {
          int at = course.indexOf(rs.getString(2));
          if (at >= 0 && at < k && !exclude.contains(rs.getLong(1))) options.add(new Option(rs.getLong(1), rs.getString(2), rs.getString(3), rs.getString(4), rs.getString(5), rs.getString(6), rs.getString(7), at + 1));
        }, lang.name(), AttestationBank.MODE);
    return options;
  }
  private ApiError noAttestationTask(Language lang, String group, Instant now, boolean other) {
    var plan = attestationPlan(group, lang, now);
    String scope = plan == null ? "этого курса" : "темы плана (" + plan.topics().size() + " " + topicsWord(plan.topics().size()) + (plan.topics().isEmpty() ? "" : ", до «" + titleOf(plan.topics().getLast()) + "»") + ")";
    return new ApiError("NO_ATTESTATION_TASK", other ? "Других задач аттестации на " + scope + " нет" : "Нет задачи аттестации на " + scope + " — нужны новые задачи");
  }
  private static String topicsWord(int n) { int m = n % 100; return m >= 11 && m <= 14 ? "тем" : n % 10 == 1 ? "тема" : n % 10 >= 2 && n % 10 <= 4 ? "темы" : "тем"; }

  /**
   * The item of an attestation (owner, 2026-10-27: all topics of the plan, completely different stories for students called
   * together): of the options, a task this student never had first, then one nobody is solving right now, then the one
   * covering most of the plan, then the one the group had least; random among equals. A «Напиши код» item (kind code) with
   * what it covers and its reference for the teacher.
   */
  private Map<String, Object> attestationItem(long user, Language lang, String group, Instant now, Set<Long> exclude) {
    var options = attestationOptions(lang, group, now, exclude);
    if (options.isEmpty()) throw noAttestationTask(lang, group, now, !exclude.isEmpty());
    var seen = attestationTasks("user_id=?", user);
    var running = attestationTasks("status='STARTED' and language=?", lang.name());
    var used = attestationTasks("group_name is ? and language=?", group, lang.name());
    Collections.shuffle(options, random);
    options.sort(Comparator.comparing((Option o) -> seen.containsKey(o.id())).thenComparing(o -> running.containsKey(o.id()))
        .thenComparing(Comparator.comparingInt(Option::covers).reversed()).thenComparingInt(o -> used.getOrDefault(o.id(), 0)));
    var o = options.getFirst(); var plan = attestationPlan(group, lang, now);
    return obj("kind", "code", "language", lang.name(), "taskId", o.id(), "externalKey", o.key(), "skillCode", o.skill(), "skillTitle", titleOf(o.skill()), "difficulty", null,
        "title", o.title(), "statement", o.statement(), "starterCode", o.starter(),
        "attestation", true, "covers", o.covers(), "coversTitle", titleOf(o.skill()), "planTopics", plan == null ? null : plan.topics().size(), "reference", o.reference());
  }
  /** Task id → how many attestations matching the condition held it (replaced tasks included). */
  private Map<Long, Integer> attestationTasks(String where, Object... params) {
    var counts = new HashMap<Long, Integer>();
    for (String items : db.queryForList("select items_json from board_tests where format='" + FORMAT_ATTESTATION + "' and items_json is not null and " + where, String.class, params))
      for (var item : read(items, new TypeReference<List<Map<String, Object>>>() {})) {
        var ids = new ArrayList<Object>(); ids.add(item.get("taskId"));
        if (item.get("replacedTaskIds") instanceof List<?> earlier) ids.addAll(earlier);
        for (Object id : ids) if (id instanceof Number n) counts.merge(n.longValue(), 1, Integer::sum);
      }
    return counts;
  }

  /** Lessons, the assistant and the console are closed while the student's attestation runs (owner, 2026-10-27). */
  void requireNoAttestation(long user) {
    if (count("select count(*) from board_tests where user_id=? and format=? and status='STARTED' and ends_at>=?", user, FORMAT_ATTESTATION, iso(now().minus(GRACE))) > 0)
      throw new ApiError("ATTESTATION_RUNNING", "Идёт аттестация — уроки и помощник откроются, когда сдашь работу");
  }

  /**
   * What the student's code shows of the topics an attestation covers (teacher only): per language construct taught
   * within the covered topics (CourseConstructs: if, switch, loops, arrays, methods, …) whether the reference uses it and
   * whether the student's code does (null without an answer). Lexical, a hint for the teacher — the checks decide.
   */
  private List<Map<String, Object>> coverage(Map<String, Object> t) {
    var item = items(t).stream().filter(i -> Boolean.TRUE.equals(i.get("attestation"))).findFirst().orElse(null);
    if (item == null || !(item.get("covers") instanceof Number covers)) return null;
    Language lang = Language.of(t.get("language"));
    var course = db.queryForList("select code from skills where language=? order by block_no,sort_order,code", String.class, lang.name());
    var expected = CourseConstructs.used(lang, (String) item.get("reference"));
    String answer = answers(t).get("code") instanceof String code && !code.isBlank() && !code.equals(item.get("starterCode")) ? code : null;
    var used = answer == null ? null : CourseConstructs.used(lang, answer);
    var rows = new ArrayList<Map<String, Object>>();
    for (var c : CourseConstructs.Construct.values()) {
      String topic = c.topic(lang); int at = topic == null ? -1 : course.indexOf(topic);
      if (at < 0 || at >= covers.intValue()) continue;
      rows.add(obj("construct", c.name(), "title", c.title, "topicTitle", titleOf(topic), "expected", expected.contains(c), "used", used == null ? null : used.contains(c)));
    }
    return rows;
  }

  private List<Map<String, Object>> itemsOf(Language lang, List<String> kinds, Map<String, Fit> chosen) {
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

  /**
   * The first topic with a bank (curated) candidate of the kind, else the first topic with any candidate (a generated
   * task); within a topic: an unsolved story, the kind's difficulty order, the kind's own preference, then random.
   */
  private Fit pick(Language lang, String kind, Collection<String> topics, Map<String, List<Candidate>> byTopic, Set<Long> solvedTasks, Set<String> solvedStories,
                   Set<Long> usedTasks, Set<String> usedStories) {
    var difficulties = BoardItems.kind(kind).difficulties();
    for (boolean bankOnly : new boolean[]{true, false}) for (String topic : topics) {
      var fits = new ArrayList<Fit>();
      for (var c : shuffled(byTopic.getOrDefault(topic, List.of()))) {
        if (usedTasks.contains(c.id()) || usedStories.contains(c.storyOrTask()) || bankOnly && !c.curated()) continue;
        var fit = fit(lang, kind, c);
        if (fit != null) fits.add(fit);
      }
      fits.sort(Comparator.comparing((Fit f) -> !f.task().curated()).thenComparing(f -> solved(f.task(), solvedTasks, solvedStories))
          .thenComparingInt(f -> f.task().difficulty() == null || !difficulties.contains(f.task().difficulty()) ? difficulties.size() : difficulties.indexOf(f.task().difficulty()))
          .thenComparingInt(Fit::rank));
      if (!fits.isEmpty()) { var f = fits.getFirst(); usedTasks.add(f.task().id()); usedStories.add(f.task().storyOrTask()); return f; }
    }
    throw new ApiError("NO_BOARD_TASK", "Для задания «" + BoardItems.kind(kind).title() + "» не нашлось задачи в темах от минимума на сегодня до уровня студента — выбери другие задания");
  }
  /** Whether a task fits a kind: parsons — the starter/reference shape (a distractor preferred), fix — a small bug among the wrong solutions, code — any (neither trivial nor long preferred). */
  private Fit fit(Language lang, String kind, Candidate c) {
    switch (kind) {
      case "parsons" -> { var p = BoardItems.parsons(lang, c.starter(), c.reference(), wrong(c)); return p == null ? null : new Fit(c, p, p.extra() == null ? 1 : 0); }
      case "fix" -> { var bug = BoardItems.bug(lang, c.reference(), wrong(c)); return bug == null ? null : new Fit(c, bug, bug.changed()); }
      // A task of a few lines is too easy for the board, a long one does not fit in its minutes; unknown size (a generated task) in between.
      default -> { Integer added = BoardItems.added(lang, c.starter(), c.reference()); return new Fit(c, added, added == null ? 1 : added < BoardItems.TRIVIAL_CODE_LINES ? 2 : added <= BoardItems.SHORT_CODE_LINES ? 0 : 1); }
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
          String.valueOf(suggested(items(t), results, null)), id);
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
        if (!BoardItems.ALL.contains(kind)) continue;
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
      String suggestedGrade = String.valueOf(suggested(items, results, assessment));
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
    db.query("select user_id,max(case when status in ('STARTED','FINISHED') then started_at end),coalesce(sum(status='FINISHED'),0) from board_tests where language=? and format='TEST' and user_id in " + in + " group by user_id",
        (RowCallbackHandler) rs -> history.put(rs.getLong(1), new Object[]{rs.getString(2), rs.getInt(3), null}), concat(new Object[]{lang.name()}, ids.toArray()));
    db.query("select b.user_id,b.final_grade from board_tests b where b.language=? and b.user_id in " + in + " and b.id=(select x.id from board_tests x where x.user_id=b.user_id and x.language=b.language and x.format='TEST' and x.final_grade is not null order by coalesce(x.started_at,x.called_at) desc,x.id desc limit 1)",
        (RowCallbackHandler) rs -> history.computeIfAbsent(rs.getLong(1), k -> new Object[]{null, 0, null})[2] = rs.getString(2), concat(new Object[]{lang.name()}, ids.toArray()));
    // The latest attestation of each member that was not cancelled or expired.
    Map<Long, Map<String, Object>> attested = new HashMap<>();
    db.query("select b.user_id,b.id,b.status,b.final_grade,coalesce(b.started_at,b.called_at) from board_tests b where b.language=? and b.user_id in " + in + " and b.id=(select x.id from board_tests x where x.user_id=b.user_id and x.language=b.language and x.format='ATTESTATION' and x.status not in ('CANCELLED','EXPIRED') order by coalesce(x.started_at,x.called_at) desc,x.id desc limit 1)",
        (RowCallbackHandler) rs -> attested.put(rs.getLong(1), obj("testId", rs.getLong(2), "status", rs.getString(3), "grade", rs.getString(4), "at", rs.getString(5))), concat(new Object[]{lang.name()}, ids.toArray()));
    Set<Long> busy = new HashSet<>(db.queryForList("select user_id from board_tests where status in ('CALLED','STARTED') and user_id in " + in, Long.class, ids.toArray()));
    var collator = collator();
    var standings = analytics.standings(name, lang, now);
    var view = new ArrayList<Map<String, Object>>();
    for (var m : members.stream().sorted(Comparator.comparing((Map<String, Object> m) -> m.get("display_name") == null ? "" : (String) m.get("display_name"), collator).thenComparing(m -> (String) m.get("login"))).toList()) {
      long user = ((Number) m.get("id")).longValue(); var h = history.getOrDefault(user, new Object[]{null, 0, null}); var standing = standings.get(user);
      view.add(obj("userId", user, "login", m.get("login"), "displayName", m.get("display_name"), "present", present.contains(user), "lastTestAt", h[0], "tests", h[1], "lastGrade", h[2],
          "lag", standing == null ? null : standing.lag(), "status", standing == null ? null : standing.status(), "farthest", standing == null ? null : standing.farthest(),
          "attestation", attested.get(user)));
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
    var plan = pacePlan(name, lang, now);
    var pace = plan == null ? null : obj("topics", plan.topics().size(), "total", plan.total(), "lastTopic", plan.topics().isEmpty() ? null : titleOf(plan.topics().getLast()),
        "start", plan.start().toString(), "session", plan.session().toString());
    int attestationPool = count("select count(*) from tasks where language=? and active=1 and mode=?", lang.name(), AttestationBank.MODE);
    var aPlan = attestationPlan(name, lang, now); var planDay = attestationPlanDate();
    var attestation = obj("tasks", attestationOptions(lang, name, now, Set.of()).size(), "total", attestationPool, "minutes", ATTESTATION_MINUTES,
        "planDate", planDay == null ? null : planDay.toString(), "planTopics", aPlan == null ? null : aPlan.topics().size(),
        "planLastTopic", aPlan == null || aPlan.topics().isEmpty() ? null : titleOf(aPlan.topics().getLast()));
    return obj("group", name, "language", lang.name(), "members", view, "suggested", suggestion, "active", active, "pace", pace, "settings", settings(), "attestation", attestation);
  }

  /**
   * POST /api/admin/board/call: a new call — a test with the kinds chosen (all three when absent) or an attestation
   * (format ATTESTATION, minutes: any positive number, ATTESTATION_MINUTES when absent); the student's earlier calls that
   * were not started are cancelled.
   */
  Map<String, Object> call(long admin, Map<String, Object> body) {
    if (body == null || !(body.get("userId") instanceof Number user)) throw new ApiError("INVALID_STUDENT", "Нужен userId студента");
    if (body.get("language") != null && !(body.get("language") instanceof String)) throw new ApiError("UNKNOWN_LANGUAGE", "Неизвестный язык курса");
    Object format = body.get("format") == null ? FORMAT_TEST : body.get("format");
    if (!FORMAT_TEST.equals(format) && !FORMAT_ATTESTATION.equals(format)) throw new ApiError("INVALID_FORMAT", "format — TEST или ATTESTATION");
    Language lang = Language.parse((String) body.get("language"));
    if (FORMAT_ATTESTATION.equals(format)) return summary(load(call(admin, user.longValue(), lang, List.of("code"), seconds(body.get("minutes")), FORMAT_ATTESTATION)));
    var kinds = BoardItems.parse(body.get("kinds"));
    return summary(load(call(admin, user.longValue(), lang, kinds, BoardItems.seconds(kinds), FORMAT_TEST)));
  }
  /** The time of an attestation: minutes > 0 (no upper limit — the teacher decides), ATTESTATION_MINUTES when absent. */
  private static int seconds(Object minutes) {
    if (minutes == null) return ATTESTATION_MINUTES * 60;
    if (!(minutes instanceof Number n) || !(n.doubleValue() > 0) || Double.isInfinite(n.doubleValue()) || n.doubleValue() * 60 > Integer.MAX_VALUE)
      throw new ApiError("INVALID_MINUTES", "minutes — число минут больше нуля");
    return (int) Math.max(1, Math.round(n.doubleValue() * 60));
  }
  /**
   * The topics always come from the range of chooseItems (source RANGE); an older client's «source» is ignored. An
   * attestation is refused at once when the pool has no task for the group's plan.
   */
  private long call(long admin, long user, Language lang, List<String> kinds, int seconds, String format) {
    var rows = db.queryForList("select group_name from users where id=? and role='STUDENT'", user);
    if (rows.isEmpty()) throw new NotFoundError("STUDENT_NOT_FOUND", "Студент не найден");
    Instant now = now(); settle(now); String source = SOURCE_RANGE, group = (String) rows.getFirst().get("group_name");
    if (FORMAT_ATTESTATION.equals(format) && attestationOptions(lang, group, now, Set.of()).isEmpty()) throw noAttestationTask(lang, group, now, false);
    db.update("update board_tests set status='CANCELLED' where user_id=? and status='CALLED'", user);
    long id = db.queryForObject("insert into board_tests(user_id,group_name,language,status,called_at,called_by,call_expires_at,kinds,duration_seconds,source,format) values(?,?,?,'CALLED',?,?,?,?,?,?,?) returning id", Long.class,
        user, group, lang.name(), iso(now), admin, iso(now.plus(CALL)), write(kinds), seconds, source, format);
    if (FORMAT_ATTESTATION.equals(format)) log.info("Student {} called to an attestation ({}, {} s) by admin {}: test {}", user, lang, seconds, admin, id);
    else log.info("Student {} called to the board ({}, {}, {}) by admin {}: test {}", user, lang, kinds, source, admin, id);
    return id;
  }

  /** POST /api/admin/board/tests/{id}/recall: a new call for the same student, course, format, kinds and time. */
  Map<String, Object> recall(long admin, long id) {
    var t = load(id);
    return adminView(load(call(admin, ((Number) t.get("user_id")).longValue(), Language.of(t.get("language")), kinds(t), duration(t), format(t))));
  }

  /**
   * PATCH /api/admin/board/tests/{id}/call {kinds?} (an attestation: {minutes?}): another set of kinds of a call not
   * started yet (CALLED or EXPIRED); the time of the test follows the kinds (an attestation: the minutes), the expiry stays
   * (the teacher has «Продлить»); an older call gets the range rule.
   */
  Map<String, Object> editCall(long id, Map<String, Object> body) {
    Instant now = now(); settle(now); var t = load(id);
    requireEditable(t);
    if (attestation(t)) {
      int seconds = body != null && body.get("minutes") != null ? seconds(body.get("minutes")) : duration(t);
      if (db.update("update board_tests set duration_seconds=? where id=? and status in ('CALLED','EXPIRED')", seconds, id) == 0) requireEditable(load(id));
      log.info("Board test {} attestation call edited: {} s → {} s", id, duration(t), seconds);
      return adminView(load(id));
    }
    var kinds = body != null && body.get("kinds") != null ? BoardItems.parse(body.get("kinds")) : kinds(t);
    if (db.update("update board_tests set kinds=?,source=?,duration_seconds=? where id=? and status in ('CALLED','EXPIRED')", write(kinds), SOURCE_RANGE, BoardItems.seconds(kinds), id) == 0) requireEditable(load(id));
    log.info("Board test {} call edited: {} → {}", id, kinds(t), kinds);
    return adminView(load(id));
  }
  private static void requireEditable(Map<String, Object> t) {
    if (!List.of("CALLED", "EXPIRED").contains(t.get("status"))) throw new ApiError("BOARD_CALL_NOT_EDITABLE", "Тест уже начат — менять вызов поздно");
  }

  /**
   * POST /api/admin/board/tests/{id}/items/{kind}/replace: another task for one item of a running test — the same kind and
   * source rules (an attestation: another pool task by its rules), never a task or story the test holds or held (the item
   * keeps them in replacedTaskIds); the item's answer
   * starts over, the timer goes on, items_revision grows so that the test screen reloads the item.
   */
  Map<String, Object> replaceItem(long id, String kind) {
    Instant now = now(); settle(now);
    for (int attempt = 0; ; attempt++) {
      var t = load(id);
      if (!"STARTED".equals(t.get("status")) || now.isAfter(instant(t.get("ends_at")).plus(GRACE))) throw new ApiError("BOARD_TEST_NOT_RUNNING", "Заменить задание можно только в идущем тесте");
      var items = new ArrayList<>(items(t));
      int index = -1;
      for (int i = 0; i < items.size(); i++) if (items.get(i).get("kind").equals(kind)) index = i;
      if (!BoardItems.ALL.contains(kind) || index < 0) throw new ApiError("INVALID_ITEM", "В этом тесте нет такого задания");
      Language lang = Language.of(t.get("language")); long user = ((Number) t.get("user_id")).longValue();
      var minimum = minimumTopics((String) t.get("group_name"), lang, now);
      // Every task the test holds or held is excluded, with its story; the other items keep their topics for the order of topics.
      Set<Long> usedTasks = new HashSet<>(); Map<String, Fit> chosen = new HashMap<>();
      for (var item : items) {
        long task = ((Number) item.get("taskId")).longValue(); usedTasks.add(task);
        if (item.get("replacedTaskIds") instanceof List<?> earlier) for (Object e : earlier) usedTasks.add(((Number) e).longValue());
        if (!kind.equals(item.get("kind")) && BoardItems.ALL.contains(item.get("kind")))
          chosen.put((String) item.get("kind"), new Fit(new Candidate(task, (String) item.get("skillCode"), null, null, null, null, false, null, null, null, null), null, 0));
      }
      Set<String> usedStories = new HashSet<>();
      db.query("select id,source='CURATED',external_key from tasks where id in " + in(usedTasks.size()), (RowCallbackHandler) rs -> {
        String key = rs.getString(3);
        usedStories.add(rs.getInt(2) == 1 && key != null && key.matches("curated:[^:]+:.+") ? story(key) : "task:" + rs.getLong(1));
      }, usedTasks.toArray());
      var old = items.get(index);
      var fresh = attestation(t) ? attestationItem(user, lang, (String) t.get("group_name"), now, usedTasks)
          : chooseItems(user, lang, List.of(kind), minimum, now, chosen, usedTasks, usedStories).getFirst();
      var replaced = new ArrayList<Object>(old.get("replacedTaskIds") instanceof List<?> earlier ? earlier : List.of()); replaced.add(old.get("taskId"));
      fresh.put("replacedTaskIds", replaced); fresh.put("replacedRevision", revision(t) + 1);
      items.set(index, fresh);
      var set = answersUpdate(Map.of(kind, initialAnswer(fresh)));
      var params = new ArrayList<Object>(); params.add(write(items)); params.addAll(set.params()); params.add(id); params.add(revision(t));
      if (db.update("update board_tests set items_json=?,answers_json=" + set.sql() + ",items_revision=items_revision+1 where id=? and status='STARTED' and items_revision=?", params.toArray()) > 0) {
        log.info("Board test {}: the {} item replaced, task {} → {}", id, kind, old.get("taskId"), fresh.get("taskId"));
        return adminView(load(id));
      }
      if (attempt > 0) throw new ApiError("BOARD_TEST_CHANGED", "Тест только что изменился — попробуй ещё раз");
    }
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
    if (body == null || !body.containsKey("finalGrade") && !body.containsKey("comment") && !body.containsKey("reportVisible")) throw new ApiError("INVALID_GRADE", "Нужны finalGrade, comment и/или reportVisible");
    if (body.containsKey("reportVisible")) {
      if (!(body.get("reportVisible") instanceof Boolean shown)) throw new ApiError("INVALID_REPORT_VISIBLE", "reportVisible — true или false");
      db.update("update board_tests set report_visible=? where id=?", shown ? 1 : 0, id);
    }
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

  /** GET /api/admin/board/journal: the group's tests of the course, newest first, and per student their final grades (oldest first), the attestations apart. */
  Map<String, Object> journal(String group, String language) {
    String name = group == null ? "" : group.strip();
    if (name.isEmpty() || count("select count(*) from users where role='STUDENT' and group_name=?", name) == 0 && count("select count(*) from board_tests where group_name=?", name) == 0)
      throw PairWork.groupNotFound();
    Language lang = course(name, language);
    settle();
    var tests = db.query("select b.id,b.user_id,u.display_name,b.called_at,b.status,b.final_grade,b.suggested_grade,b.format from board_tests b join users u on u.id=b.user_id where b.group_name=? and b.language=? order by b.called_at desc,b.id desc",
        (rs, i) -> obj("id", rs.getLong(1), "userId", rs.getLong(2), "displayName", rs.getString(3), "calledAt", rs.getString(4), "status", rs.getString(5), "finalGrade", rs.getString(6), "suggestedGrade", rs.getString(7),
            "format", rs.getString(8)),
        name, lang.name());
    Map<Long, String> people = new HashMap<>(); Map<Long, List<String>> grades = new HashMap<>(), attestations = new HashMap<>(); Map<Long, String> last = new HashMap<>();
    db.query("select id,display_name from users where role='STUDENT' and group_name=? union select u.id,u.display_name from board_tests b join users u on u.id=b.user_id where b.group_name=? and b.language=?",
        (RowCallbackHandler) rs -> people.put(rs.getLong(1), rs.getString(2)), name, name, lang.name());
    db.query("select user_id,final_grade,started_at,format from board_tests where group_name=? and language=? and status='FINISHED' order by called_at,id",
        (RowCallbackHandler) rs -> {
          if (FORMAT_ATTESTATION.equals(rs.getString(4))) { attestations.computeIfAbsent(rs.getLong(1), k -> new ArrayList<>()).add(rs.getString(2)); return; }
          grades.computeIfAbsent(rs.getLong(1), k -> new ArrayList<>()).add(rs.getString(2)); last.put(rs.getLong(1), rs.getString(3));
        }, name, lang.name());
    var collator = collator();
    var students = people.entrySet().stream().sorted(Comparator.comparing((Map.Entry<Long, String> e) -> e.getValue() == null ? "" : e.getValue(), collator).thenComparing(Map.Entry::getKey))
        .map(e -> obj("userId", e.getKey(), "displayName", e.getValue(), "grades", grades.getOrDefault(e.getKey(), List.of()), "lastTestAt", last.get(e.getKey()),
            "attestations", attestations.getOrDefault(e.getKey(), List.of()))).toList();
    return obj("group", name, "language", lang.name(), "tests", tests, "students", students);
  }

  private Map<String, Object> summary(Map<String, Object> t) {
    var assessment = t.get("assessment") instanceof Map<?, ?> a ? a.get("status") : null;
    return obj("id", t.get("id"), "userId", t.get("user_id"), "displayName", t.get("display_name"), "status", t.get("status"), "calledAt", t.get("called_at"),
        "expiresAt", t.get("call_expires_at"), "startedAt", t.get("started_at"), "endsAt", t.get("ends_at"), "finishedAt", t.get("finished_at"),
        "suggestedGrade", t.get("suggested_grade"), "finalGrade", t.get("final_grade"), "assessmentStatus", assessment, "kinds", kinds(t), "durationSeconds", duration(t), "source", source(t),
        "stationId", t.get("station_id"), "stationName", t.get("station_name"), "format", format(t));
  }
  /** Everything for the teacher: the items with the solution and the task, the answers, checks, the score, runs, pace, grades. */
  private Map<String, Object> adminView(Map<String, Object> t) {
    var view = summary(t);
    String pace = (String) t.get("pace_status");
    view.put("login", t.get("login")); view.put("group", t.get("group_name")); view.put("language", t.get("language"));
    view.put("items", t.get("items_json") == null ? null : items(t)); view.put("answers", t.get("answers_json") == null ? null : answers(t));
    view.put("results", t.get("results_json") == null ? null : results(t)); view.put("score", t.get("results_json") == null ? null : score(results(t), (Map<?, ?>) t.get("assessment")));
    view.put("runs", runs(t));
    view.put("paceStatus", pace);
    view.put("floor", floorView(items(t), t.get("results_json") == null ? null : scores(results(t), (Map<?, ?>) t.get("assessment")))); view.put("ruleGrade", t.get("rule_grade")); view.put("assessment", t.get("assessment"));
    view.put("comment", t.get("comment")); view.put("gradedAt", t.get("graded_at")); view.put("reportVisible", visible(t));
    view.put("coverage", attestation(t) ? coverage(t) : null);
    return view;
  }

  /** The floor for the teacher: null — it does not apply; met — null until the test is checked. */
  private static Map<String, Object> floorView(List<Map<String, Object>> items, Map<String, Double> scores) {
    var all = new HashMap<String, Double>(); for (var item : items) all.put((String) item.get("kind"), 1.0);
    if (floor(items, all) == null) return null;
    return obj("grade", FLOOR, "met", scores == null ? null : floor(items, scores));
  }
  /** The score table: per item its weight and score (0, 0.5, 1); the points, the maximum and the percent (one decimal). */
  private static Map<String, Object> score(List<Map<String, Object>> results, Map<?, ?> assessment) {
    var scores = scores(results, assessment); var items = new ArrayList<Map<String, Object>>(); double points = 0; int max = 0;
    for (var e : scores.entrySet()) { int weight = BoardItems.kind(e.getKey()).weight(); items.add(obj("kind", e.getKey(), "weight", weight, "score", e.getValue())); points += weight * e.getValue(); max += weight; }
    return obj("items", items, "points", points, "max", max, "percent", Math.round(BoardItems.percent(scores) * 10) / 10.0);
  }

  // ---------------------------------------------------------------- loading and helpers

  private Map<String, Object> load(long id) {
    var rows = db.queryForList("select b.*,u.login,u.display_name,s.name as station_name from board_tests b join users u on u.id=b.user_id left join board_stations s on s.id=b.station_id where b.id=?", id);
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
  private String titleOf(String skill) { return db.queryForList("select title from skills where code=?", String.class, skill).stream().findFirst().orElse(skill); }
  private static String format(Map<String, Object> t) { return FORMAT_ATTESTATION.equals(t.get("format")) ? FORMAT_ATTESTATION : FORMAT_TEST; }
  private static boolean attestation(Map<String, Object> t) { return FORMAT_ATTESTATION.equals(t.get("format")); }
  private static String source(Map<String, Object> t) { return SOURCE_RANGE.equals(t.get("source")) || SOURCE_PACE.equals(t.get("source")) ? (String) t.get("source") : SOURCE_LEVEL; }
  private List<String> kinds(Map<String, Object> t) { return t.get("kinds") == null ? BoardItems.ALL : read((String) t.get("kinds"), new TypeReference<List<String>>() {}); }
  private static int revision(Map<String, Object> t) { return t.get("items_revision") instanceof Number n ? n.intValue() : 0; }
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
