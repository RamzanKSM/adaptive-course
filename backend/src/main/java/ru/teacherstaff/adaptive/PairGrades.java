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
 * Grades for a class period («пара»): the teacher enters the pair's window and group after it, the platform grades every
 * graded member of the group (н, 2..5) by the points of the tasks first passed inside the window, against a norm (the
 * median of regular students: the previous Moscow week, or the pair itself while there is no history).
 * <p>A pair is computed in a fixed number of queries whatever the size of the group, stored when the teacher saves it
 * and never recomputed by itself. Students see only the date and the grade of published pairs: points, tasks, the
 * median and the thresholds are the teacher's. The rules: backend/README.md, «Оценки за пару».
 */
@Component
class PairGrades {
  static final ZoneId MOSCOW = ZoneId.of("Europe/Moscow");
  static final Duration MAX_WINDOW = Duration.ofHours(6);
  /** A week's saved results are the norm when it has at least this many regular attended rows; weeks looked back. */
  static final int WEEK_MIN_ROWS = 15, WEEK_LOOKBACK = 12;
  /** A HARD task is worth its difficulty this many times. */
  static final int HARD_WEIGHT = 10;
  /** Thresholds, in percent of the median: 5 from FIVE, 4 from FOUR, 3 from THREE, 2 below. */
  static final int FIVE = 135, FOUR = 100, THREE = 60;
  static final String ABSENT = "н";
  static final List<String> GRADES = List.of(ABSENT, "2", "3", "4", "5");
  static final int COMMENT_MAX = 500;

  private final JdbcTemplate db; private final Clock clock; private final ObjectMapper json;
  PairGrades(JdbcTemplate db, Clock clock, ObjectMapper json) { this.db = db; this.clock = clock; this.json = json; }

  record Window(Instant start, Instant end) {}
  record Median(Double value, String source, LocalDate week) {}
  /** One student's result; grade and comment are the teacher's, everything else is computed. */
  record Row(long userId, String login, String name, boolean attended, int points, Map<String, Integer> tasks, boolean hard,
             String autoGrade, String grade, String comment) {
    boolean manual() { return !grade.equals(autoGrade) || comment != null; }
    Row withAuto(String auto) { return new Row(userId, login, name, attended, points, tasks, hard, auto, auto, null); }
    Row withGrade(String grade, String comment) { return new Row(userId, login, name, attended, points, tasks, hard, autoGrade, grade, comment); }
  }
  /** A pair without its rows; id, createdAt and publishedAt are null in a preview. */
  record Head(Long id, String group, Language language, Window window, Median median, String createdAt, String publishedAt) {}

  // ---------------------------------------------------------------- rules

  /** The grade of a student against the median (null or 0: no norm yet). */
  static String grade(boolean attended, int points, Double median) {
    if (!attended) return ABSENT;
    if (median == null || median <= 0) return points > 0 ? "4" : "2";
    // in hundredths, so that the boundaries are exact (the median is an integer or a half)
    double p = points * 100.0;
    return p >= FIVE * median ? "5" : p >= FOUR * median ? "4" : p >= THREE * median ? "3" : "2";
  }

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

  /** Graded members of a group: students taking the session. */
  private List<Long> members(String group) {
    return db.queryForList("select id from users where role='STUDENT' and group_name=? and session_participant=1 order by id", Long.class, group);
  }

  /**
   * Points, attendance, the hard flag and the auto grade of the given students in a window: five queries for the whole
   * group. Grades are the auto ones; the caller applies the teacher's.
   */
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
          hardMode.contains(user) || came && hardTask.contains(user), null, null, null));
    }
    var median = median(lang, w, rows, pairId);
    rows.replaceAll(r -> r.withAuto(grade(r.attended(), r.points(), median.value())));
    return new Computed(rows, median);
  }
  private record Computed(List<Row> rows, Median median) {}

  /**
   * The norm: saved regular attended rows of the course (all groups) of the previous Moscow week if there are enough,
   * else of the latest earlier week with enough, else this pair's own regular attended students. The pair's own week
   * never feeds its norm.
   */
  private Median median(Language lang, Window w, List<Row> rows, Long pairId) {
    LocalDate monday = week(w.start());
    Map<LocalDate, List<Integer>> weeks = new HashMap<>();
    db.query("select p.starts_at,g.points from pair_grades g join pairs p on p.id=g.pair_id where p.language=? and g.attended=1 and g.hard=0 and p.starts_at>=? and p.starts_at<? and p.id<>?",
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

  /** GET /api/admin/pairs/course: the course most graded members study (their session course), else the one with most lessons. */
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
    return view(new Head(null, request.group(), request.language(), request.window(), computed.median(), null, null), computed.rows(), true);
  }

  /** POST /api/admin/pairs: computed again, the teacher's grades applied, saved. Grades of students not in the pair are ignored. */
  Map<String, Object> save(Map<String, Object> body, long adminId) {
    var request = request(body);
    Map<Long, String[]> manual = new HashMap<>();
    if (body.get("grades") != null) {
      if (!(body.get("grades") instanceof List<?> list)) throw new ApiError("INVALID_GRADE", "grades — список {userId, grade, comment}");
      for (Object item : list) {
        if (!(item instanceof Map<?, ?> m) || !(m.get("userId") instanceof Number user)) throw new ApiError("INVALID_GRADE", "У оценки нет userId");
        manual.put(user.longValue(), new String[]{gradeValue(m.get("grade")), comment(m.get("comment"))});
      }
    }
    var computed = compute(request.language(), request.window(), members(request.group()), null);
    var median = computed.median();
    long id = db.queryForObject("insert into pairs(group_name,language,starts_at,ends_at,median,median_source,median_week,created_by,created_at) values(?,?,?,?,?,?,?,?,?) returning id", Long.class,
        request.group(), request.language().name(), iso(request.window().start()), iso(request.window().end()), median.value(), median.source(),
        median.week() == null ? null : median.week().toString(), adminId, iso(now()));
    for (var row : computed.rows()) {
      var m = manual.get(row.userId());
      var saved = m == null ? row : row.withGrade(m[0], m[1]);
      db.update("insert into pair_grades(pair_id,user_id,attended,points,tasks_json,hard,auto_grade,grade,comment) values(?,?,?,?,?,?,?,?,?)",
          id, saved.userId(), saved.attended() ? 1 : 0, saved.points(), write(saved.tasks()), saved.hard() ? 1 : 0, saved.autoGrade(), saved.grade(), saved.comment());
    }
    return pair(id);
  }

  /** GET /api/admin/pairs: newest first, without rows. */
  Map<String, Object> list(String group, String language) {
    var params = new ArrayList<Object>(); var where = new StringBuilder(" where 1=1"); var joined = new StringBuilder(" where 1=1");
    if (group != null && !group.isBlank()) { where.append(" and group_name=?"); joined.append(" and p.group_name=?"); params.add(group.strip()); }
    if (language != null && !language.isBlank()) { where.append(" and language=?"); joined.append(" and p.language=?"); params.add(Language.parse(language).name()); }
    var heads = db.query("select " + HEAD + " from pairs" + where + " order by starts_at desc,id desc", (rs, i) -> head(rs), params.toArray());
    Map<Long, Map<String, Integer>> counts = new HashMap<>();
    db.query("select g.pair_id,g.grade,count(*) from pair_grades g join pairs p on p.id=g.pair_id" + joined + " group by g.pair_id,g.grade",
        (RowCallbackHandler) rs -> counts.computeIfAbsent(rs.getLong(1), k -> new HashMap<>()).put(rs.getString(2), rs.getInt(3)), params.toArray());
    var pairs = new ArrayList<Map<String, Object>>();
    for (var head : heads) { var v = view(head, List.of(), false); v.put("counts", counts(counts.getOrDefault(head.id(), Map.of()))); pairs.add(v); }
    return obj("pairs", pairs);
  }

  /** GET /api/admin/pairs/{id}. */
  Map<String, Object> pair(long id) { return view(head(id), rows(id), true); }

  /** PATCH /api/admin/pairs/{id}/grades/{userId}: the teacher's grade; back to auto when it equals the auto grade without a comment. */
  Map<String, Object> setGrade(long id, long userId, Map<String, Object> body) {
    head(id);
    if (body == null) throw new ApiError("INVALID_GRADE", "Нужна оценка: н, 2, 3, 4 или 5");
    String grade = gradeValue(body.get("grade")), comment = comment(body.get("comment"));
    if (db.update("update pair_grades set grade=?,comment=? where pair_id=? and user_id=?", grade, comment, id, userId) == 0)
      throw new NotFoundError("STUDENT_NOT_FOUND", "Этого студента нет в паре");
    return pair(id);
  }

  /** POST /api/admin/pairs/{id}/recalculate: the same students again; the teacher's grades stay, the rest take the new auto grade. */
  Map<String, Object> recalculate(long id) {
    var head = head(id);
    Map<Long, Row> old = new HashMap<>();
    for (var row : rows(id)) old.put(row.userId(), row);
    var computed = compute(head.language(), head.window(), old.keySet(), id);
    var median = computed.median();
    db.update("update pairs set median=?,median_source=?,median_week=? where id=?", median.value(), median.source(), median.week() == null ? null : median.week().toString(), id);
    for (var row : computed.rows()) {
      var before = old.get(row.userId());
      var saved = before.manual() ? row.withGrade(before.grade(), before.comment()) : row;
      db.update("update pair_grades set attended=?,points=?,tasks_json=?,hard=?,auto_grade=?,grade=?,comment=? where pair_id=? and user_id=?",
          saved.attended() ? 1 : 0, saved.points(), write(saved.tasks()), saved.hard() ? 1 : 0, saved.autoGrade(), saved.grade(), saved.comment(), id, row.userId());
    }
    return pair(id);
  }

  /** POST /api/admin/pairs/{id}/publish. */
  Map<String, Object> publish(long id, Map<String, Object> body) {
    var head = head(id);
    if (body == null || !(body.get("published") instanceof Boolean published)) throw new ApiError("INVALID_PUBLISHED", "published должен быть true или false");
    if (!published) db.update("update pairs set published_at=null where id=?", id);
    else if (head.publishedAt() == null) db.update("update pairs set published_at=? where id=?", iso(now()), id);
    return pair(id);
  }

  /** DELETE /api/admin/pairs/{id}. */
  Map<String, Object> delete(long id) {
    head(id);
    db.update("delete from pair_grades where pair_id=?", id);
    db.update("delete from pairs where id=?", id);
    return obj("deleted", true);
  }

  /** GET /api/admin/pairs/journal: the group's pairs of the course, oldest first, and a line per student. */
  Map<String, Object> journal(String group, String language) {
    String name = group == null ? "" : group.strip();
    if (name.isEmpty() || count("select count(*) from users where role='STUDENT' and group_name=?", name) == 0 && count("select count(*) from pairs where group_name=?", name) == 0)
      throw groupNotFound();
    Language lang = language == null || language.isBlank() ? Language.valueOf((String) course(name).get("language")) : Language.parse(language);
    var pairs = db.queryForList("select id,starts_at as startsAt,ends_at as endsAt,published_at is not null as published from pairs where group_name=? and language=? order by starts_at,id", name, lang.name());
    Map<Long, Integer> column = new HashMap<>();
    for (var p : pairs) { column.put(((Number) p.get("id")).longValue(), column.size()); p.put("published", ((Number) p.get("published")).intValue() == 1); }
    Map<Long, String[]> people = new LinkedHashMap<>(); Map<Long, String[]> grades = new HashMap<>(); Map<Long, boolean[]> manual = new HashMap<>();
    db.query("select id,login,display_name from users where id in (select id from users where role='STUDENT' and group_name=? and session_participant=1 "
        + "union select g.user_id from pair_grades g join pairs p on p.id=g.pair_id where p.group_name=? and p.language=?)",
        (RowCallbackHandler) rs -> people.put(rs.getLong(1), new String[]{rs.getString(2), rs.getString(3)}), name, name, lang.name());
    db.query("select g.pair_id,g.user_id,g.grade,g.auto_grade,g.comment from pair_grades g join pairs p on p.id=g.pair_id where p.group_name=? and p.language=?",
        (RowCallbackHandler) rs -> {
          int i = column.get(rs.getLong(1)); long user = rs.getLong(2);
          grades.computeIfAbsent(user, k -> new String[pairs.size()])[i] = rs.getString(3);
          manual.computeIfAbsent(user, k -> new boolean[pairs.size()])[i] = !rs.getString(3).equals(rs.getString(4)) || rs.getString(5) != null;
        }, name, lang.name());
    var students = new ArrayList<Map<String, Object>>();
    for (var e : sorted(people)) {
      String[] g = grades.getOrDefault(e.getKey(), new String[pairs.size()]); boolean[] m = manual.getOrDefault(e.getKey(), new boolean[pairs.size()]);
      int sum = 0, numeric = 0, absences = 0; var flags = new ArrayList<Boolean>();
      for (int i = 0; i < g.length; i++) {
        flags.add(m[i]);
        if (ABSENT.equals(g[i])) absences++; else if (g[i] != null) { sum += Integer.parseInt(g[i]); numeric++; }
      }
      students.add(obj("userId", e.getKey(), "login", e.getValue()[0], "displayName", e.getValue()[1], "grades", Arrays.asList(g), "manual", flags,
          "average", numeric == 0 ? null : ProgressAnalytics.round(sum / (double) numeric, 2), "absences", absences));
    }
    return obj("group", name, "language", lang.name(), "pairs", pairs, "students", students);
  }

  /** GET /api/grades: the student's own grades of published pairs — the date and the grade, nothing else. */
  Map<String, Object> studentGrades(long userId, Language lang) {
    var grades = db.query("select p.starts_at,g.grade from pair_grades g join pairs p on p.id=g.pair_id where g.user_id=? and p.language=? and p.published_at is not null order by p.starts_at desc,p.id desc",
        (rs, i) -> obj("date", Instant.parse(rs.getString(1)).atZone(MOSCOW).toLocalDate().toString(), "grade", rs.getString(2)), userId, lang.name());
    return obj("grades", grades);
  }

  // ---------------------------------------------------------------- views and loading

  private Map<String, Object> view(Head head, List<Row> rows, boolean withRows) {
    Double m = head.median().value(); boolean norm = m != null && m > 0;
    var v = obj("id", head.id(), "group", head.group(), "language", head.language().name(), "startsAt", iso(head.window().start()), "endsAt", iso(head.window().end()),
        "median", m, "medianSource", head.median().source(), "medianWeek", head.median().week() == null ? null : head.median().week().toString(),
        "thresholds", norm ? obj("five", ProgressAnalytics.round(m * FIVE / 100, 2), "four", ProgressAnalytics.round(m * FOUR / 100, 2), "three", ProgressAnalytics.round(m * THREE / 100, 2)) : null,
        "published", head.publishedAt() != null, "publishedAt", head.publishedAt(), "createdAt", head.createdAt());
    if (!withRows) return v;
    Map<String, Integer> counts = new HashMap<>();
    for (var r : rows) counts.merge(r.grade(), 1, Integer::sum);
    v.put("counts", counts(counts));
    var collator = collator();
    v.put("rows", rows.stream().sorted(Comparator.comparing((Row r) -> r.name() == null ? "" : r.name(), collator).thenComparing(Row::login)).map(r -> obj(
        "userId", r.userId(), "login", r.login(), "displayName", r.name(), "attended", r.attended(), "points", r.points(), "tasks", r.tasks(), "hard", r.hard(),
        "percent", r.attended() && norm ? (Object) Math.round(r.points() * 100 / m) : null,
        "autoGrade", r.autoGrade(), "grade", r.grade(), "comment", r.comment(), "manual", r.manual())).toList());
    return v;
  }
  private static Map<String, Object> counts(Map<String, Integer> byGrade) {
    var counts = new LinkedHashMap<String, Object>();
    for (String g : GRADES) counts.put(g, byGrade.getOrDefault(g, 0));
    return counts;
  }

  private static final String HEAD = "id,group_name,language,starts_at,ends_at,median,median_source,median_week,created_at,published_at";
  private static Head head(java.sql.ResultSet rs) throws java.sql.SQLException {
    double median = rs.getDouble(6); Double value = rs.wasNull() ? null : median; String week = rs.getString(8);
    return new Head(rs.getLong(1), rs.getString(2), Language.of(rs.getString(3)), new Window(Instant.parse(rs.getString(4)), Instant.parse(rs.getString(5))),
        new Median(value, rs.getString(7), week == null ? null : LocalDate.parse(week)), rs.getString(9), rs.getString(10));
  }
  private Head head(long id) {
    var heads = db.query("select " + HEAD + " from pairs where id=?", (rs, i) -> head(rs), id);
    if (heads.isEmpty()) throw new NotFoundError("PAIR_NOT_FOUND", "Пара не найдена");
    return heads.getFirst();
  }
  private List<Row> rows(long id) {
    return db.query("select g.user_id,u.login,u.display_name,g.attended,g.points,g.tasks_json,g.hard,g.auto_grade,g.grade,g.comment from pair_grades g join users u on u.id=g.user_id where g.pair_id=? order by g.user_id",
        (rs, i) -> new Row(rs.getLong(1), rs.getString(2), rs.getString(3), rs.getInt(4) == 1, rs.getInt(5), read(rs.getString(6)), rs.getInt(7) == 1,
            rs.getString(8), rs.getString(9), rs.getString(10)), id);
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
  private static NotFoundError groupNotFound() { return new NotFoundError("GROUP_NOT_FOUND", "Группа не найдена"); }
  private static String gradeValue(Object value) {
    if (!(value instanceof String g) || !GRADES.contains(g.strip())) throw new ApiError("INVALID_GRADE", "Оценка — н, 2, 3, 4 или 5");
    return g.strip();
  }
  private static String comment(Object value) {
    if (value == null) return null;
    if (!(value instanceof String text)) throw new ApiError("INVALID_COMMENT", "Комментарий должен быть строкой");
    if (text.strip().length() > COMMENT_MAX) throw new ApiError("INVALID_COMMENT", "Комментарий длиннее " + COMMENT_MAX + " символов");
    return text.isBlank() ? null : text.strip();
  }

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
