package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;
import org.springframework.stereotype.Component;
import java.text.Collator;
import java.time.*;
import java.time.format.DateTimeParseException;
import java.time.temporal.ChronoUnit;
import java.util.*;

/**
 * «Работа на паре»: the teacher enters a class period's window and group after it and sees how every member of the group
 * worked in it — attendance, the points of the tasks first passed inside the window, the pace against a reference (the
 * median of regular students: the previous Moscow week, or the pair itself while there is no history) and the activity
 * (active 5-minute slots, submissions, questions to the assistant). Teacher-only, students see nothing of it; grades
 * come from the test at the board (BoardTests).
 * <p>A pair is computed in a fixed number of queries whatever the size of the group, stored when the teacher saves it
 * and never recomputed by itself; the activity is computed on the fly. The rules: backend/README.md, «Работа на паре».
 */
@Component
class PairWork {
  static final ZoneId MOSCOW = ZoneId.of("Europe/Moscow");
  static final Duration MAX_WINDOW = Duration.ofHours(6);
  /** A week's saved results are the norm when it has at least this many regular attended rows; weeks looked back. */
  static final int WEEK_MIN_ROWS = 15, WEEK_LOOKBACK = 12;
  /** A HARD task is worth its difficulty this many times. */
  static final int HARD_WEIGHT = 10;
  /** Activity is counted in slots of this many seconds: a slot with a submission or a question is 5 active minutes. */
  static final int SLOT_SECONDS = 300;

  private final JdbcTemplate db; private final Clock clock; private final ObjectMapper json;
  PairWork(JdbcTemplate db, Clock clock, ObjectMapper json) { this.db = db; this.clock = clock; this.json = json; }

  record Window(Instant start, Instant end) {}
  record Median(Double value, String source, LocalDate week) {}
  /** One student's saved result: attendance, points, tasks by difficulty and the hard flag. */
  record Row(long userId, String login, String name, boolean attended, int points, Map<String, Integer> tasks, boolean hard) {}
  /** Activity inside the window, computed on the fly: active minutes, submissions, failed ones, the student's chat messages. */
  record Activity(int activeMinutes, int submissions, int failed, int chatQuestions) { static final Activity NONE = new Activity(0, 0, 0, 0); }
  /** A pair without its rows; id and createdAt are null in a preview. */
  record Head(Long id, String group, Language language, Window window, Median median, String createdAt) {}

  // ---------------------------------------------------------------- rules

  static double median(List<Integer> values) {
    var sorted = values.stream().sorted().toList(); int n = sorted.size();
    return n % 2 == 1 ? sorted.get(n / 2) : (sorted.get(n / 2 - 1) + sorted.get(n / 2)) / 2.0;
  }

  /** Monday of the Moscow week of a moment. */
  static LocalDate week(Instant at) { return at.atZone(MOSCOW).toLocalDate().with(DayOfWeek.MONDAY); }
  private static Instant startOf(LocalDate monday) { return monday.atStartOfDay(MOSCOW).toInstant(); }

  /** The weight of a task: difficulty (null → 1), ×HARD_WEIGHT for a HARD one. */
  static int weight(Integer difficulty, boolean hard) { return (difficulty == null ? 1 : difficulty) * (hard ? HARD_WEIGHT : 1); }

  // ---------------------------------------------------------------- computation

  /** Members of a group: students taking the session. */
  private List<Long> members(String group) {
    return db.queryForList("select id from users where role='STUDENT' and group_name=? and session_participant=1 order by id", Long.class, group);
  }

  /** Points, attendance and the hard flag of the given students in a window and the median: five queries for the whole group. */
  private Computed compute(Language lang, Window w, Collection<Long> users, Long pairId) {
    var rows = new ArrayList<Row>();
    if (users.isEmpty()) return new Computed(rows, median(lang, w, List.of(), pairId));
    String in = in(users.size()), language = lang.name();
    long from = w.start().getEpochSecond(), to = w.end().getEpochSecond();
    Map<Long, String[]> people = new LinkedHashMap<>();
    db.query("select id,login,display_name from users where id in " + in + " order by id",
        (RowCallbackHandler) rs -> people.put(rs.getLong(1), new String[]{rs.getString(2), rs.getString(3)}), users.toArray());

    // Tasks whose first passed, non-revoked submission (over all time) is inside the window and which are still credited.
    Map<Long, int[]> points = new HashMap<>(); Map<Long, Map<String, Integer>> tasks = new HashMap<>(); Set<Long> hardTask = new HashSet<>();
    db.query("select f.user_id,t.difficulty,t.mode='HARD' from (select l.user_id,s.task_id,min(" + epoch("s.created_at") + ") as first from submissions s join lessons l on l.id=s.lesson_id "
        + "where s.passed=1 and s.revoked_at is null and l.user_id in " + in + " group by l.user_id,s.task_id) f join tasks t on t.id=f.task_id "
        + "where t.language=? and f.first between ? and ? and exists(select 1 from successful_task_credit c where c.user_id=f.user_id and c.task_id=f.task_id)",
        (RowCallbackHandler) rs -> {
          long user = rs.getLong(1); int d = rs.getInt(2); Integer difficulty = rs.wasNull() ? null : d; boolean hard = rs.getInt(3) == 1;
          points.computeIfAbsent(user, k -> new int[1])[0] += weight(difficulty, hard);
          tasks.computeIfAbsent(user, k -> emptyTasks()).merge(hard ? "hard" : String.valueOf(difficulty == null ? 1 : difficulty), 1, Integer::sum);
          if (hard) hardTask.add(user);
        }, args(users, language, from, to));

    Object[] attendance = concat(new Object[]{language}, users.toArray(), new Object[]{from, to});
    // Attended: a lesson of the course started, a submission or a chat message of the student inside the window.
    Set<Long> attended = new HashSet<>(db.queryForList(
        "select l.user_id from lessons l where l.language=? and l.user_id in " + in + " and " + epoch("l.started_at") + " between ? and ? "
        + "union select l.user_id from submissions s join lessons l on l.id=s.lesson_id where l.language=? and l.user_id in " + in + " and " + epoch("s.created_at") + " between ? and ? "
        + "union select l.user_id from chat_messages m join lessons l on l.id=m.lesson_id where m.role='STUDENT' and l.language=? and l.user_id in " + in + " and " + epoch("m.created_at") + " between ? and ?",
        Long.class, concat(attendance, attendance, attendance)));

    // Hard mode active in this course now, as ApiController.hardModeActive: allowed, switched on and the course passed once.
    Set<Long> hardMode = new HashSet<>(db.queryForList("select u.id from users u where u.id in " + in + " and u.hard_mode_allowed=1 and u.hard_mode_on=1 "
        + "and not exists(select 1 from skills s where s.language=? and not exists(select 1 from student_skills x where x.user_id=u.id and x.skill_code=s.code and (x.completed_iterations>=1 or x.mastered=1)) "
        + "and not exists(select 1 from diagnostic_skill_results d where d.user_id=u.id and d.skill_code=s.code and d.confirmed=1))", Long.class, args(users, language)));

    for (var e : people.entrySet()) {
      long user = e.getKey(); boolean came = attended.contains(user);
      int p = came ? points.getOrDefault(user, new int[1])[0] : 0;
      rows.add(new Row(user, e.getValue()[0], e.getValue()[1], came, p, came ? tasks.getOrDefault(user, emptyTasks()) : emptyTasks(),
          hardMode.contains(user) || came && hardTask.contains(user)));
    }
    var median = median(lang, w, rows, pairId);
    return new Computed(rows, median);
  }
  private record Computed(List<Row> rows, Median median) {}

  /**
   * The activity of the given students in a window, in this course: 5-minute slots (counted from the window's start) with
   * a submission or a student chat message, the submissions and the failed ones, the student's chat messages. Two queries.
   */
  private Map<Long, Activity> activity(Language lang, Window w, Collection<Long> users) {
    if (users.isEmpty()) return Map.of();
    String in = in(users.size());
    long from = w.start().getEpochSecond(), to = w.end().getEpochSecond();
    Object[] params = concat(new Object[]{lang.name()}, users.toArray(), new Object[]{from, to});
    Map<Long, int[]> counts = new HashMap<>();
    db.query("select l.user_id,count(*),coalesce(sum(s.passed=0),0) from submissions s join lessons l on l.id=s.lesson_id where l.language=? and l.user_id in " + in
        + " and " + epoch("s.created_at") + " between ? and ? group by l.user_id",
        (RowCallbackHandler) rs -> { var c = counts.computeIfAbsent(rs.getLong(1), k -> new int[4]); c[1] = rs.getInt(2); c[2] = rs.getInt(3); }, params);
    db.query("select user_id,count(distinct slot),sum(chat) from (select l.user_id,(" + epoch("s.created_at") + "-?)/" + SLOT_SECONDS + " as slot,0 as chat from submissions s join lessons l on l.id=s.lesson_id where l.language=? and l.user_id in " + in + " and " + epoch("s.created_at") + " between ? and ? "
        + "union all select l.user_id,(" + epoch("m.created_at") + "-?)/" + SLOT_SECONDS + ",1 from chat_messages m join lessons l on l.id=m.lesson_id where m.role='STUDENT' and l.language=? and l.user_id in " + in + " and " + epoch("m.created_at") + " between ? and ?) group by user_id",
        (RowCallbackHandler) rs -> { var c = counts.computeIfAbsent(rs.getLong(1), k -> new int[4]); c[0] = rs.getInt(2) * SLOT_SECONDS / 60; c[3] = rs.getInt(3); },
        concat(new Object[]{from}, params, new Object[]{from}, params));
    Map<Long, Activity> result = new HashMap<>();
    counts.forEach((user, c) -> result.put(user, new Activity(c[0], c[1], c[2], c[3])));
    return result;
  }

  /**
   * The norm: saved regular attended rows of the course (all groups) of the previous Moscow week if there are enough,
   * else of the latest earlier week with enough, else this pair's own regular attended students. The pair's own week
   * never feeds its norm.
   */
  private Median median(Language lang, Window w, List<Row> rows, Long pairId) {
    LocalDate monday = week(w.start());
    Map<LocalDate, List<Integer>> weeks = new HashMap<>();
    db.query("select p.starts_at,g.points from pair_results g join pairs p on p.id=g.pair_id where p.language=? and g.attended=1 and g.hard=0 and p.starts_at>=? and p.starts_at<? and p.id<>?",
        (RowCallbackHandler) rs -> weeks.computeIfAbsent(week(Instant.parse(rs.getString(1))), k -> new ArrayList<>()).add(rs.getInt(2)),
        lang.name(), iso(startOf(monday.minusWeeks(WEEK_LOOKBACK))), iso(startOf(monday)), pairId == null ? -1 : pairId);
    for (int k = 1; k <= WEEK_LOOKBACK; k++) {
      var points = weeks.get(monday.minusWeeks(k));
      if (points != null && points.size() >= WEEK_MIN_ROWS) return new Median(median(points), "WEEK", monday.minusWeeks(k));
    }
    var own = rows.stream().filter(r -> r.attended() && !r.hard()).map(Row::points).toList();
    return own.isEmpty() ? new Median(null, "NONE", null) : new Median(median(own), "PAIR", null);
  }

  // ---------------------------------------------------------------- endpoints

  /** GET /api/admin/pairs/course: the course most members study (their session course), else the one with most lessons. */
  Map<String, Object> course(String group) {
    String name = existingGroup(group);
    var users = members(name);
    if (users.isEmpty()) users = db.queryForList("select id from users where role='STUDENT' and group_name=?", Long.class, name);
    Map<Long, Map<Language, long[]>> lessons = new HashMap<>(); Map<Language, Long> lessonTotals = new EnumMap<>(Language.class);
    db.query("select user_id,language,count(*),max(" + epoch("started_at") + ") from lessons where user_id in " + in(users.size()) + " group by user_id,language",
        (RowCallbackHandler) rs -> {
          Language lang = Language.of(rs.getString(2)); long last = rs.getLong(4);
          lessons.computeIfAbsent(rs.getLong(1), k -> new EnumMap<>(Language.class)).put(lang, new long[]{rs.getLong(3), rs.wasNull() ? Long.MIN_VALUE : last});
          lessonTotals.merge(lang, rs.getLong(3), Long::sum);
        }, users.toArray());
    Map<Long, Map<Language, Long>> diagnostics = new HashMap<>();
    db.query("select user_id,language," + epoch("diagnostic_completed_at") + " from student_languages where diagnostic_completed_at is not null and user_id in " + in(users.size()),
        (RowCallbackHandler) rs -> { long at = rs.getLong(3); diagnostics.computeIfAbsent(rs.getLong(1), k -> new EnumMap<>(Language.class)).put(Language.of(rs.getString(2)), rs.wasNull() ? null : at); },
        users.toArray());
    Map<Language, Integer> votes = new EnumMap<>(Language.class);
    for (long user : users) {
      var lang = ProgressAnalytics.sessionCourse(lessons.getOrDefault(user, Map.of()), diagnostics.getOrDefault(user, Map.of()));
      if (lang != null) votes.merge(lang, 1, Integer::sum);
    }
    Language best = Language.values()[0];
    for (Language lang : Language.values()) {
      int v = votes.getOrDefault(lang, 0), bv = votes.getOrDefault(best, 0);
      if (v > bv || v == bv && lessonTotals.getOrDefault(lang, 0L) > lessonTotals.getOrDefault(best, 0L)) best = lang;
    }
    return obj("language", best.name());
  }

  /** POST /api/admin/pairs/preview: computed, nothing saved. */
  Map<String, Object> preview(Map<String, Object> body) {
    var request = request(body);
    var computed = compute(request.language(), request.window(), members(request.group()), null);
    return view(new Head(null, request.group(), request.language(), request.window(), computed.median(), null), computed.rows(), true);
  }

  /** POST /api/admin/pairs: computed again and saved. */
  Map<String, Object> save(Map<String, Object> body, long adminId) {
    var request = request(body);
    var computed = compute(request.language(), request.window(), members(request.group()), null);
    var median = computed.median();
    long id = db.queryForObject("insert into pairs(group_name,language,starts_at,ends_at,median,median_source,median_week,created_by,created_at) values(?,?,?,?,?,?,?,?,?) returning id", Long.class,
        request.group(), request.language().name(), iso(request.window().start()), iso(request.window().end()), median.value(), median.source(),
        median.week() == null ? null : median.week().toString(), adminId, iso(now()));
    for (var row : computed.rows())
      db.update("insert into pair_results(pair_id,user_id,attended,points,tasks_json,hard) values(?,?,?,?,?,?)",
          id, row.userId(), row.attended() ? 1 : 0, row.points(), write(row.tasks()), row.hard() ? 1 : 0);
    return pair(id);
  }

  /** GET /api/admin/pairs: newest first, without rows. */
  Map<String, Object> list(String group, String language) {
    var params = new ArrayList<Object>(); var where = new StringBuilder(" where 1=1");
    if (group != null && !group.isBlank()) { where.append(" and group_name=?"); params.add(group.strip()); }
    if (language != null && !language.isBlank()) { where.append(" and language=?"); params.add(Language.parse(language).name()); }
    var heads = db.query("select " + HEAD + " from pairs" + where + " order by starts_at desc,id desc", (rs, i) -> head(rs), params.toArray());
    return obj("pairs", heads.stream().map(head -> view(head, List.of(), false)).toList());
  }

  /** GET /api/admin/pairs/{id}. */
  Map<String, Object> pair(long id) { return view(head(id), rows(id), true); }

  /** POST /api/admin/pairs/{id}/recalculate: the same students again — points, attendance, hard and the median. */
  Map<String, Object> recalculate(long id) {
    var head = head(id);
    var users = rows(id).stream().map(Row::userId).toList();
    var computed = compute(head.language(), head.window(), users, id);
    var median = computed.median();
    db.update("update pairs set median=?,median_source=?,median_week=? where id=?", median.value(), median.source(), median.week() == null ? null : median.week().toString(), id);
    for (var row : computed.rows())
      db.update("update pair_results set attended=?,points=?,tasks_json=?,hard=? where pair_id=? and user_id=?",
          row.attended() ? 1 : 0, row.points(), write(row.tasks()), row.hard() ? 1 : 0, id, row.userId());
    return pair(id);
  }

  /** DELETE /api/admin/pairs/{id}. */
  Map<String, Object> delete(long id) {
    head(id);
    db.update("delete from pair_results where pair_id=?", id);
    db.update("delete from pairs where id=?", id);
    return obj("deleted", true);
  }

  /**
   * GET /api/admin/pairs/journal: the group's pairs of the course, oldest first, and a line per student with a cell per
   * pair (attended, points, percent, active minutes; null — not in that pair) and the number of pairs attended.
   */
  Map<String, Object> journal(String group, String language) {
    String name = group == null ? "" : group.strip();
    if (name.isEmpty() || count("select count(*) from users where role='STUDENT' and group_name=?", name) == 0 && count("select count(*) from pairs where group_name=?", name) == 0)
      throw groupNotFound();
    Language lang = language == null || language.isBlank() ? Language.valueOf((String) course(name).get("language")) : Language.parse(language);
    var heads = db.query("select " + HEAD + " from pairs where group_name=? and language=? order by starts_at,id", (rs, i) -> head(rs), name, lang.name());
    Map<Long, Integer> column = new HashMap<>();
    for (var h : heads) column.put(h.id(), column.size());
    Map<Long, String[]> people = new LinkedHashMap<>(); Map<Long, Map<String, Object>[]> cells = new HashMap<>(); Map<Long, List<Long>> usersOf = new HashMap<>();
    db.query("select id,login,display_name from users where id in (select id from users where role='STUDENT' and group_name=? and session_participant=1 "
        + "union select g.user_id from pair_results g join pairs p on p.id=g.pair_id where p.group_name=? and p.language=?)",
        (RowCallbackHandler) rs -> people.put(rs.getLong(1), new String[]{rs.getString(2), rs.getString(3)}), name, name, lang.name());
    db.query("select g.pair_id,g.user_id,g.attended,g.points from pair_results g join pairs p on p.id=g.pair_id where p.group_name=? and p.language=?",
        (RowCallbackHandler) rs -> {
          long pair = rs.getLong(1), user = rs.getLong(2); var head = heads.get(column.get(pair)); boolean attended = rs.getInt(3) == 1; int points = rs.getInt(4);
          usersOf.computeIfAbsent(pair, k -> new ArrayList<>()).add(user);
          @SuppressWarnings("unchecked") Map<String, Object>[] row = cells.computeIfAbsent(user, k -> new Map[heads.size()]);
          row[column.get(pair)] = obj("attended", attended, "points", points, "percent", percent(attended, points, head.median().value()), "activeMinutes", 0);
        }, name, lang.name());
    for (var head : heads) activity(lang, head.window(), usersOf.getOrDefault(head.id(), List.of()))
        .forEach((user, a) -> { var cell = cells.get(user)[column.get(head.id())]; if (cell != null) cell.put("activeMinutes", a.activeMinutes()); });
    var students = new ArrayList<Map<String, Object>>();
    for (var e : sorted(people)) {
      @SuppressWarnings("unchecked") Map<String, Object>[] row = cells.getOrDefault(e.getKey(), new Map[heads.size()]);
      long attended = Arrays.stream(row).filter(c -> c != null && Boolean.TRUE.equals(c.get("attended"))).count();
      students.add(obj("userId", e.getKey(), "login", e.getValue()[0], "displayName", e.getValue()[1], "cells", Arrays.asList(row), "pairs", attended));
    }
    var pairs = heads.stream().map(h -> obj("id", h.id(), "startsAt", iso(h.window().start()), "endsAt", iso(h.window().end()))).toList();
    return obj("group", name, "language", lang.name(), "pairs", pairs, "students", students);
  }

  // ---------------------------------------------------------------- views and loading

  private Map<String, Object> view(Head head, List<Row> rows, boolean withRows) {
    Double m = head.median().value();
    var v = obj("id", head.id(), "group", head.group(), "language", head.language().name(), "startsAt", iso(head.window().start()), "endsAt", iso(head.window().end()),
        "median", m, "medianSource", head.median().source(), "medianWeek", head.median().week() == null ? null : head.median().week().toString(), "createdAt", head.createdAt());
    if (!withRows) return v;
    var activity = activity(head.language(), head.window(), rows.stream().map(Row::userId).toList());
    var collator = collator();
    v.put("rows", rows.stream().sorted(Comparator.comparing((Row r) -> r.name() == null ? "" : r.name(), collator).thenComparing(Row::login)).map(r -> {
      var a = activity.getOrDefault(r.userId(), Activity.NONE);
      return obj("userId", r.userId(), "login", r.login(), "displayName", r.name(), "attended", r.attended(), "points", r.points(), "tasks", r.tasks(), "hard", r.hard(),
          "percent", percent(r.attended(), r.points(), m), "activeMinutes", a.activeMinutes(), "submissions", a.submissions(), "failed", a.failed(), "chatQuestions", a.chatQuestions());
    }).toList());
    return v;
  }
  /** Points in percent of the median; null when absent or there is no norm. */
  private static Long percent(boolean attended, int points, Double median) { return attended && median != null && median > 0 ? Math.round(points * 100 / median) : null; }

  private static final String HEAD = "id,group_name,language,starts_at,ends_at,median,median_source,median_week,created_at";
  private static Head head(java.sql.ResultSet rs) throws java.sql.SQLException {
    double median = rs.getDouble(6); Double value = rs.wasNull() ? null : median; String week = rs.getString(8);
    return new Head(rs.getLong(1), rs.getString(2), Language.of(rs.getString(3)), new Window(Instant.parse(rs.getString(4)), Instant.parse(rs.getString(5))),
        new Median(value, rs.getString(7), week == null ? null : LocalDate.parse(week)), rs.getString(9));
  }
  private Head head(long id) {
    var heads = db.query("select " + HEAD + " from pairs where id=?", (rs, i) -> head(rs), id);
    if (heads.isEmpty()) throw new NotFoundError("PAIR_NOT_FOUND", "Пара не найдена");
    return heads.getFirst();
  }
  private List<Row> rows(long id) {
    return db.query("select g.user_id,u.login,u.display_name,g.attended,g.points,g.tasks_json,g.hard from pair_results g join users u on u.id=g.user_id where g.pair_id=? order by g.user_id",
        (rs, i) -> new Row(rs.getLong(1), rs.getString(2), rs.getString(3), rs.getInt(4) == 1, rs.getInt(5), read(rs.getString(6)), rs.getInt(7) == 1), id);
  }

  // ---------------------------------------------------------------- validation

  private record Request(String group, Language language, Window window) {}
  private Request request(Map<String, Object> body) {
    if (body == null) throw new ApiError("INVALID_PAIR", "Нужны group, language, startsAt, endsAt");
    String group = existingGroup(body.get("group") instanceof String s ? s : null);
    if (body.get("language") != null && !(body.get("language") instanceof String)) throw new ApiError("UNKNOWN_LANGUAGE", "Неизвестный язык курса");
    Language lang = Language.parse((String) body.get("language"));
    Instant start = instant(body.get("startsAt")), end = instant(body.get("endsAt"));
    if (!end.isAfter(start)) throw new ApiError("INVALID_WINDOW", "Конец пары должен быть позже начала");
    if (Duration.between(start, end).compareTo(MAX_WINDOW) > 0) throw new ApiError("INVALID_WINDOW", "Пара не может быть длиннее 6 часов");
    return new Request(group, lang, new Window(start, end));
  }
  private static Instant instant(Object value) {
    if (!(value instanceof String text) || text.isBlank()) throw new ApiError("INVALID_WINDOW", "Нужны startsAt и endsAt — дата и время ISO-8601 со смещением");
    try { return OffsetDateTime.parse(text.strip()).toInstant().truncatedTo(ChronoUnit.SECONDS); }
    catch (DateTimeParseException e) { throw new ApiError("INVALID_WINDOW", "startsAt и endsAt — дата и время ISO-8601 со смещением, например 2026-10-14T11:00:00+03:00"); }
  }
  private String existingGroup(String group) {
    String name = group == null ? "" : group.strip();
    if (name.isEmpty() || count("select count(*) from users where role='STUDENT' and group_name=?", name) == 0) throw groupNotFound();
    return name;
  }
  static NotFoundError groupNotFound() { return new NotFoundError("GROUP_NOT_FOUND", "Группа не найдена"); }

  // ---------------------------------------------------------------- helpers

  private Instant now() { return clock.instant(); }
  static String iso(Instant at) { return at.truncatedTo(ChronoUnit.SECONDS).toString(); }
  private static String epoch(String column) { return "cast(strftime('%s'," + column + ") as integer)"; }
  private static String in(int n) { return n == 0 ? "(null)" : "(" + String.join(",", Collections.nCopies(n, "?")) + ")"; }
  private static Object[] args(Collection<?> first, Object... rest) { var all = new ArrayList<Object>(first); all.addAll(Arrays.asList(rest)); return all.toArray(); }
  private static Object[] concat(Object[]... parts) { var all = new ArrayList<Object>(); for (var p : parts) all.addAll(Arrays.asList(p)); return all.toArray(); }
  private int count(String sql, Object... params) { return db.queryForObject(sql, Integer.class, params); }
  private static Map<String, Integer> emptyTasks() { var t = new LinkedHashMap<String, Integer>(); for (String k : List.of("1", "2", "3", "hard")) t.put(k, 0); return t; }
  private String write(Map<String, Integer> tasks) { try { return json.writeValueAsString(tasks); } catch (Exception e) { throw new IllegalStateException(e); } }
  private Map<String, Integer> read(String text) { try { return json.readValue(text, new TypeReference<LinkedHashMap<String, Integer>>() {}); } catch (Exception e) { throw new IllegalStateException(e); } }
  private static Collator collator() { return Collator.getInstance(Locale.forLanguageTag("ru")); }
  private static List<Map.Entry<Long, String[]>> sorted(Map<Long, String[]> people) {
    var collator = collator();
    return people.entrySet().stream().sorted(Comparator.comparing((Map.Entry<Long, String[]> e) -> e.getValue()[1] == null ? "" : e.getValue()[1], collator)
        .thenComparing(e -> e.getValue()[0])).toList();
  }
  private static Map<String, Object> obj(Object... entries) { var m = new LinkedHashMap<String, Object>(); for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]); return m; }
}
