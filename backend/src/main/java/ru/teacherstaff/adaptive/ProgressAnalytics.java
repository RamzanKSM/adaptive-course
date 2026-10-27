package ru.teacherstaff.adaptive;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;
import org.springframework.stereotype.Component;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.*;
import java.util.*;

/**
 * Progress analytics of a course: the teacher's «Прогресс» (growth per day, forecast to the session, flags), the
 * classroom screen projected to a group (anonymous aggregates only) and the student's own pace to the session.
 * <p>Nothing is stored for it. The history is rebuilt from the rows the course keeps anyway: credited tasks are dated by
 * their first passed, non-revoked submission; iterations are replayed lesson by lesson with IterationRule, the rule live
 * crediting uses, each credited task at the moment of its first pass in the lesson; diagnostic confirmations count from
 * student_languages.diagnostic_completed_at. A course is loaded in a fixed number of queries and computed in memory.
 * All days are UTC days. The definitions of the metrics: backend/README.md, «Аналитика прогресса».
 */
@Component
class ProgressAnalytics {
  /** Pace: topics closed by practice in the last PACE_DAYS, per week of the student's course, at most PACE_MAX_WEEKS weeks. */
  static final int PACE_DAYS = 21, PACE_MAX_WEEKS = 3;
  /** Behind the plan line by at most this many topics is BORDERLINE, by more BEHIND. */
  static final int BORDERLINE_LAG = 2;
  /** A member silent this many days is GONE; this many failed submissions in a row on the current task is STUCK. */
  static final int GONE_DAYS = 7, STUCK_FAILURES = 5;
  /** The classroom shows no totals for fewer members: in a tiny group they would identify people. */
  static final int CLASSROOM_MIN_MEMBERS = 5, CLASSROOM_DAYS = 28, HARD_TOPICS = 5, HARD_TOPIC_MIN_STUDENTS = 3;
  /** Longest stretch of the teacher's charts, in days: an earlier `from` starts the lines this many days before `to`. */
  static final int MAX_DAYS = 1100;
  /** XP as the student's game.ts experience(): a task, a hard task, an iteration, a mastered topic, a confirmed one. */
  static final int XP_TASK = 10, XP_HARD_TASK = 30, XP_ITERATION = 20, XP_MASTERY = 50, XP_CONFIRMED = 5;
  static final String SESSION_DATE_KEY = "session_date";
  private static final long DAY = 86_400;

  private final JdbcTemplate db; private final Clock clock;
  ProgressAnalytics(JdbcTemplate db, Clock clock) { this.db = db; this.clock = clock; }

  Instant now() { return clock.instant(); }
  static LocalDate day(long epochSecond) { return LocalDate.ofEpochDay(Math.floorDiv(epochSecond, DAY)); }
  static LocalDate day(Instant instant) { return day(instant.getEpochSecond()); }
  private static long startOf(LocalDate day) { return day.toEpochDay() * DAY; }

  /** The session date set by the teacher (app_settings), or null. */
  LocalDate sessionDate() {
    var stored = db.queryForList("select value from app_settings where key=?", String.class, SESSION_DATE_KEY);
    try { return stored.isEmpty() ? null : LocalDate.parse(stored.getFirst()); } catch (RuntimeException e) { return null; }
  }
  void setSessionDate(LocalDate date) {
    if (date == null) db.update("delete from app_settings where key=?", SESSION_DATE_KEY);
    else db.update("insert into app_settings(key,value) values(?,?) on conflict(key) do update set value=excluded.value", SESSION_DATE_KEY, date.toString());
  }
  static double weeksLeft(LocalDate session, LocalDate day) { return (session.toEpochDay() - day.toEpochDay()) / 7.0; }

  /**
   * The plan line to the session, the same for everybody of a group: from 0 topics at `start` to all `total` at the
   * session, K(day) = BoardTests.minimum. The pace status and «К доске» by pace both use it.
   */
  record Plan(LocalDate start, LocalDate session, int total) {
    int topics(LocalDate day) { return BoardTests.minimum(total, start, session, day); }
  }
  /** Null without a session date, without a start or when the start is not before the session. */
  static Plan plan(LocalDate session, LocalDate start, int total) { return session == null || start == null || !start.isBefore(session) ? null : new Plan(start, session, total); }
  Plan plan(String group, Language lang) {
    return plan(sessionDate(), planStart(group, lang), db.queryForObject("select count(*) from skills where language=?", Integer.class, lang.name()));
  }
  /**
   * The start of the plan: the UTC day of the first lesson in the course of any student of the group; without a group
   * (null or blank), of any student of the course. Null when there is no such lesson.
   */
  LocalDate planStart(String group, Language lang) {
    boolean all = group == null || group.isBlank();
    // lessons.started_at is «YYYY-MM-DD HH:MM:SS» (UTC); date() reads it and the ISO form alike.
    String first = db.queryForObject("select min(date(l.started_at)) from lessons l join users u on u.id=l.user_id where u.role='STUDENT' and l.language=?" + (all ? "" : " and u.group_name=?"),
        String.class, all ? new Object[]{lang.name()} : new Object[]{lang.name(), group});
    return first == null ? null : LocalDate.parse(first);
  }
  private static Map<String, Object> sessionView(LocalDate session, LocalDate today) {
    return obj("date", session == null ? null : session.toString(), "weeksLeft", session == null ? null : round(weeksLeft(session, today), 1));
  }

  // ---------------------------------------------------------------- views

  /**
   * GET /api/admin/progress: every student of the course with a line per day from the course's first lesson (or `from`
   * when nobody has had a lesson yet) to `to` — the whole history, so the page can compute growth from the day before
   * the period and align students by their own first lesson; the period itself only limits the period numbers.
   */
  Map<String, Object> course(Language lang, LocalDate from, LocalDate to, Instant at) {
    long now = at.getEpochSecond(); LocalDate today = day(now), session = sessionDate();
    var course = load(lang, Scope.ALL);
    Map<String, Optional<LocalDate>> starts = new HashMap<>();
    var firstLesson = course.students().stream().map(s -> s.firstLessonAt).filter(Objects::nonNull).min(Long::compare).map(ProgressAnalytics::day).orElse(null);
    LocalDate start = firstLesson != null && !firstLesson.isAfter(to) ? firstLesson : from;
    if (start.isBefore(to.minusDays(MAX_DAYS - 1))) start = to.minusDays(MAX_DAYS - 1);
    var days = new ArrayList<LocalDate>();
    for (var d = start; !d.isAfter(to); d = d.plusDays(1)) days.add(d);
    var students = new ArrayList<Map<String, Object>>();
    for (var s : course.students()) students.add(studentView(course, s, days, from, to, now, today, session,
        starts.computeIfAbsent(groupOf(s), g -> Optional.ofNullable(planStart(g, lang))).orElse(null)));
    return obj("language", lang.name(), "from", from.toString(), "to", to.toString(), "today", today.toString(),
        "days", days.stream().map(LocalDate::toString).toList(), "session", sessionView(session, today),
        "topics", course.topics().stream().map(t -> obj("code", t.code(), "title", t.title(), "block", t.block())).toList(),
        "students", students);
  }

  /** «К доске»: the lag and status of a session member (as in «Прогресс») and the title of the farthest topic he closed. */
  record Standing(Integer lag, String status, String farthest) {}
  /** Standings of the group's session members in this course, by user id (others are absent). */
  Map<Long, Standing> standings(String group, Language lang, Instant at) {
    var course = load(lang, Scope.group(group));
    long now = at.getEpochSecond(); LocalDate today = day(now), session = sessionDate(), start = planStart(group, lang);
    var standings = new HashMap<Long, Standing>();
    for (var s : course.students()) {
      if (!member(s, lang)) continue;
      var f = forecast(course, s, now, today, session, start);
      var cursor = new Cursor(s).at(now + 1); String farthest = null;
      for (int i = course.topics().size() - 1; i >= 0 && farthest == null; i--) if (cursor.confirmed(i) || cursor.completed[i] >= 1) farthest = course.topics().get(i).title();
      standings.put(s.id, new Standing(f.lag(), f.status(), farthest));
    }
    return standings;
  }

  /**
   * The «session» block of the student's own GET /api/progress: their pace, status and closed topics per day. Null unless
   * the student takes the session in this course.
   */
  Map<String, Object> studentSession(long userId, Language lang, Instant at) {
    var course = load(lang, Scope.user(userId));
    if (course.students().isEmpty() || !member(course.students().getFirst(), lang)) return null;
    var s = course.students().getFirst();
    long now = at.getEpochSecond(); LocalDate today = day(now), session = sessionDate();
    var f = forecast(course, s, now, today, session, planStart(groupOf(s), lang));
    Long first = s.firstLessonAt == null ? s.diagnosticAt : s.diagnosticAt == null ? s.firstLessonAt : (Long) Math.min(s.firstLessonAt, s.diagnosticAt);
    LocalDate start = first == null || day(first).isAfter(today) ? today : day(first);
    var days = new ArrayList<String>(); var closed = new ArrayList<Integer>(); var cursor = new Cursor(s);
    for (var d = start; !d.isAfter(today); d = d.plusDays(1)) { cursor.at(startOf(d.plusDays(1))); days.add(d.toString()); closed.add(cursor.closed()); }
    return obj("date", session == null ? null : session.toString(), "weeksLeft", f.weeksLeft() == null ? null : round(f.weeksLeft(), 1),
        "total", f.total(), "closed", f.closed(), "remaining", f.remaining(), "pace", round(f.pace(), 2),
        "planStart", f.planStart() == null ? null : f.planStart().toString(), "planToday", f.planToday(), "lag", f.lag(), "status", f.status(),
        "forecastDate", f.forecastDate() == null ? null : f.forecastDate().toString(), "days", days, "closedSeries", closed);
  }

  /**
   * GET /api/admin/classroom: aggregates over the group's members, projected to the whole group, so it never holds an id,
   * a login or a name. Null when the group has no members in this course (unknown group included).
   */
  Map<String, Object> classroom(Language lang, String group, Instant at) {
    if (group == null || group.isBlank()) return null;
    long now = at.getEpochSecond(); LocalDate today = day(now), session = sessionDate();
    var course = load(lang, Scope.group(group.strip()));
    var members = course.students().stream().filter(s -> member(s, lang)).toList();
    if (members.isEmpty()) return null;
    int total = course.topics().size();
    boolean tooSmall = members.size() < CLASSROOM_MIN_MEMBERS;
    var view = obj("group", group.strip(), "language", lang.name(), "members", members.size(), "tooSmall", tooSmall,
        "session", sessionView(session, today), "totalTopics", total, "week", null, "daily", List.of(), "blocks", List.of(), "hardTopics", List.of());
    if (tooSmall) return view;

    // Topics closed by practice (a first iteration of a topic the diagnostic did not confirm), by moment.
    LocalDate monday = today.with(DayOfWeek.MONDAY); long weekStart = startOf(monday);
    var plan = plan(session, planStart(group.strip(), lang), total);
    var closures = new ArrayList<Long>(); int behindBySunday = 0;
    for (var s : members) {
      // The goal of the week: what each member lacks at the week start to be on the plan line on Sunday.
      if (plan != null) behindBySunday += Math.max(0, plan.topics(monday.plusDays(6)) - new Cursor(s).at(weekStart).closed());
      for (int i = 0; i < total; i++) if (!s.confirmed[i] && s.firstIteration[i] != Long.MAX_VALUE) closures.add(s.firstIteration[i]);
    }
    Integer goal = plan == null ? null : behindBySunday;
    view.put("week", obj("from", monday.toString(), "closedTopics", closures.stream().filter(t -> t >= weekStart && t <= now).count(), "goal", goal));

    Map<Long, Integer> perDay = new HashMap<>();
    for (long t : closures) perDay.merge(Math.floorDiv(t, DAY), 1, Integer::sum);
    var daily = new ArrayList<Map<String, Object>>();
    for (var d = today.minusDays(CLASSROOM_DAYS - 1); !d.isAfter(today); d = d.plusDays(1)) daily.add(obj("day", d.toString(), "closedTopics", perDay.getOrDefault(d.toEpochDay(), 0)));
    view.put("daily", daily);

    var cursors = members.stream().map(s -> new Cursor(s).at(now + 1)).toList();
    var blocks = new TreeMap<Integer, List<Integer>>();
    for (int i = 0; i < total; i++) blocks.computeIfAbsent(course.topics().get(i).block(), b -> new ArrayList<>()).add(i);
    var blockViews = new ArrayList<Map<String, Object>>();
    for (var block : blocks.entrySet()) {
      double sum = 0;
      for (var c : cursors) for (int i : block.getValue()) sum += c.confirmed(i) ? 1 : c.share(i);
      blockViews.add(obj("block", block.getKey(), "topics", block.getValue().stream().map(i -> course.topics().get(i).title()).toList(),
          "avgShare", round(sum / (cursors.size() * block.getValue().size()), 2)));
    }
    view.put("blocks", blockViews);

    int[] attempts = new int[total], solved = new int[total], students = new int[total];
    for (var s : members) {
      boolean[] tried = new boolean[total];
      for (var x : s.submissions) for (int i : course.targets(x.taskId())) { attempts[i]++; tried[i] = true; }
      for (var credit : s.credits) for (int i : course.targets(credit.taskId())) solved[i]++;
      for (int i = 0; i < total; i++) if (tried[i]) students[i]++;
    }
    view.put("hardTopics", java.util.stream.IntStream.range(0, total).filter(i -> students[i] >= HARD_TOPIC_MIN_STUDENTS).boxed()
        .sorted(Comparator.<Integer>comparingDouble(i -> -attempts[i] / (double) Math.max(1, solved[i])).thenComparingInt(i -> i)).limit(HARD_TOPICS)
        .map(i -> obj("code", course.topics().get(i).code(), "title", course.topics().get(i).title(),
            "attemptsPerSolve", round(attempts[i] / (double) Math.max(1, solved[i]), 1), "students", students[i])).toList());
    return view;
  }

  private Map<String, Object> studentView(Course course, Student s, List<LocalDate> days, LocalDate from, LocalDate to, long now, LocalDate today, LocalDate session, LocalDate planStart) {
    int n = course.topics().size();
    double[] skills = new double[days.size()], withDiagnostic = new double[days.size()]; int[] solved = new int[days.size()], xp = new int[days.size()], closed = new int[days.size()];
    var cursor = new Cursor(s);
    for (int d = 0; d < days.size(); d++) {
      long end = startOf(days.get(d).plusDays(1)); cursor.at(end);
      double sum = 0, sumWithDiagnostic = 0; int iterations = 0, mastered = 0, confirmed = 0;
      for (int i = 0; i < n; i++) {
        boolean isMastered = cursor.mastered(i), confirmedOnly = !isMastered && cursor.confirmed(i);
        double share = cursor.share(i); sum += share; sumWithDiagnostic += confirmedOnly ? 1 : share;
        iterations += cursor.completed[i]; if (isMastered) mastered++; if (confirmedOnly) confirmed++;
      }
      int solvedThen = before(s.solvedAt, end), hard = Math.min(before(s.hardAt, end), solvedThen);
      skills[d] = percent(sum, n); withDiagnostic[d] = percent(sumWithDiagnostic, n); solved[d] = solvedThen;
      xp[d] = xp(solvedThen, hard, iterations, mastered, confirmed); closed[d] = cursor.closed();
    }
    cursor.at(startOf(to.plusDays(1)));
    var share = new ArrayList<Double>(); var confirmed = new ArrayList<Boolean>();
    for (int i = 0; i < n; i++) { share.add(round(cursor.share(i), 2)); confirmed.add(cursor.confirmed(i)); }

    long fromAt = startOf(from), toAt = startOf(to.plusDays(1));
    long activeDays = s.activeDays.stream().filter(d -> d >= from.toEpochDay() && d <= to.toEpochDay()).count();
    int periodSolved = 0, firstTry = 0;
    for (var credit : s.credits) if (credit.at() >= fromAt && credit.at() < toAt) { periodSolved++; if (credit.firstTry()) firstTry++; }
    long submissions = s.submissions.stream().filter(x -> x.at() >= fromAt && x.at() < toAt).count();

    boolean member = member(s, course.language());
    var forecast = member ? forecast(course, s, now, today, session, planStart) : null;
    return obj("id", s.id, "login", s.login, "displayName", s.name, "group", s.group, "participant", s.participant,
        "sessionCourse", s.sessionCourse == null ? null : s.sessionCourse.name(), "member", member,
        "firstLessonDay", s.firstLessonAt == null ? null : day(s.firstLessonAt).toString(),
        "lastActivityAt", s.lastActivityAt == null ? null : Instant.ofEpochSecond(s.lastActivityAt).toString(), "lessons", s.lessons.size(),
        "series", obj("skills", skills, "skillsWithDiagnostic", withDiagnostic, "solved", solved, "xp", xp, "closed", closed),
        "topicShare", share, "topicConfirmed", confirmed,
        "period", obj("activeDays", activeDays, "solved", periodSolved, "firstTry", firstTry, "submissions", submissions),
        "forecast", forecast == null ? null : forecast.view(), "flags", member ? flags(s, forecast, now) : List.of());
  }

  // ---------------------------------------------------------------- definitions

  private static String groupOf(Student s) { return s.group == null || s.group.isBlank() ? null : s.group; }

  /** A member of a course's statistics: takes the session, and this is the course of their session. */
  static boolean member(Student s, Language lang) { return s.participant && s.sessionCourse == lang; }

  /**
   * The course of the student's session: the one with most lessons (a tie goes to the most recent lesson); without
   * lessons, the course of the diagnostic (the most recent one if both). lessons: count and the last start per course.
   */
  static Language sessionCourse(Map<Language, long[]> lessons, Map<Language, Long> diagnostics) {
    Language best = null; long bestCount = 0, bestLast = Long.MIN_VALUE;
    for (Language lang : Language.values()) {
      long[] l = lessons.get(lang);
      if (l == null || l[0] == 0) continue;
      if (l[0] > bestCount || (l[0] == bestCount && l[1] > bestLast)) { best = lang; bestCount = l[0]; bestLast = l[1]; }
    }
    if (best != null) return best;
    long latest = Long.MIN_VALUE;
    for (Language lang : Language.values()) {
      if (!diagnostics.containsKey(lang)) continue;
      long at = diagnostics.get(lang) == null ? Long.MIN_VALUE : diagnostics.get(lang);
      if (best == null || at > latest) { best = lang; latest = at; }
    }
    return best;
  }

  /** XP exactly as the student's game.ts experience(). */
  static int xp(int solved, int hard, int iterations, int mastered, int confirmedNotMastered) {
    return (solved - hard) * XP_TASK + hard * XP_HARD_TASK + iterations * XP_ITERATION + mastered * XP_MASTERY + confirmedNotMastered * XP_CONFIRMED;
  }

  /**
   * Where the student stands against the session. weeksLeft is null without a date; planStart, planToday (K today) and
   * lag (K today − closed: positive behind, negative ahead) are null without a plan; see README.
   */
  record Forecast(int total, int closed, int closedByPractice, int closedByDiagnostic, int remaining, double pace, double paceWeeks,
                  Double weeksLeft, LocalDate planStart, Integer planToday, Integer lag, String status, LocalDate forecastDate) {
    Map<String, Object> view() {
      return obj("total", total, "closed", closed, "closedByPractice", closedByPractice, "closedByDiagnostic", closedByDiagnostic, "remaining", remaining,
          "pace", round(pace, 2), "paceWeeks", round(paceWeeks, 2), "planStart", planStart == null ? null : planStart.toString(), "planToday", planToday, "lag", lag,
          "status", status, "forecastDate", forecastDate == null ? null : forecastDate.toString());
    }
  }

  /**
   * The forecast rules. recentClosures — topics whose first iteration was completed by practice in the last PACE_DAYS;
   * weeksSinceFirstLesson — the student's time in the course, which caps the pace window for newcomers; planStart — the
   * start of the group's plan line (planStart(group, lang)). The status compares the closed topics with the plan line
   * today; the pace gives only the forecast date.
   */
  static Forecast forecast(int total, int closedByPractice, int closedByDiagnostic, int recentClosures, double weeksSinceFirstLesson, LocalDate today, LocalDate session, LocalDate planStart) {
    int closed = closedByPractice + closedByDiagnostic, remaining = Math.max(0, total - closed);
    double paceWeeks = Math.min(PACE_MAX_WEEKS, Math.max(1, weeksSinceFirstLesson)), pace = recentClosures / paceWeeks;
    Double weeksLeft = session == null ? null : weeksLeft(session, today);
    var plan = plan(session, planStart, total);
    Integer planToday = plan == null ? null : plan.topics(today), lag = plan == null ? null : planToday - closed;
    String status = remaining == 0 ? "DONE" : lag == null ? null : lag <= 0 ? "ON_TRACK" : lag <= BORDERLINE_LAG ? "BORDERLINE" : "BEHIND";
    // remaining / pace * 7 days, written so that exact quotients stay exact
    LocalDate date = remaining == 0 || recentClosures == 0 ? null : today.plusDays((long) Math.ceil(remaining * paceWeeks * 7 / recentClosures - 1e-9));
    return new Forecast(total, closed, closedByPractice, closedByDiagnostic, remaining, pace, paceWeeks, weeksLeft, plan == null ? null : plan.start(), planToday, lag, status, date);
  }

  private static Forecast forecast(Course course, Student s, long now, LocalDate today, LocalDate session, LocalDate planStart) {
    var cursor = new Cursor(s).at(now + 1);
    int n = course.topics().size(), byPractice = 0, byDiagnostic = 0, recent = 0;
    for (int i = 0; i < n; i++) {
      if (cursor.confirmed(i)) { byDiagnostic++; continue; }
      if (cursor.completed[i] >= 1) byPractice++;
      if (s.firstIteration[i] > now - PACE_DAYS * DAY && s.firstIteration[i] <= now) recent++;
    }
    double weeks = s.firstLessonAt == null ? 0 : (now - s.firstLessonAt) / (7.0 * DAY);
    return forecast(n, byPractice, byDiagnostic, recent, weeks, today, session, planStart);
  }

  private static List<String> flags(Student s, Forecast forecast, long now) {
    var flags = new ArrayList<String>();
    if ("BEHIND".equals(forecast.status()) || "BORDERLINE".equals(forecast.status())) flags.add(forecast.status());
    if (stuck(s)) flags.add("STUCK");
    if (!s.lessons.isEmpty() && s.lastActivityAt != null && now - s.lastActivityAt >= GONE_DAYS * DAY) flags.add("GONE");
    if (s.lessons.isEmpty()) flags.add("NOT_STARTED");
    return flags;
  }

  /** An open lesson whose most recently submitted task ends with STUCK_FAILURES failed, non-revoked submissions and has no passed one. */
  private static boolean stuck(Student s) {
    for (var lesson : s.lessons) {
      if (!lesson.open()) continue;
      var inLesson = s.submissions.stream().filter(x -> x.lessonId() == lesson.id()).toList();
      if (inLesson.isEmpty()) continue;
      long task = inLesson.getLast().taskId();
      var attempts = inLesson.stream().filter(x -> x.taskId() == task).toList();
      if (attempts.stream().anyMatch(Submission::passed)) continue;
      int failed = 0;
      for (int i = attempts.size() - 1; i >= 0 && !attempts.get(i).revoked(); i--) failed++;
      if (failed >= STUCK_FAILURES) return true;
    }
    return false;
  }

  // ---------------------------------------------------------------- loading and replay

  record Topic(String code, String title, int block) {}
  record Lesson(long id, int number, Long startedAt, boolean open, Long lastActivityAt) {}
  record Submission(long id, long lessonId, long taskId, boolean passed, boolean revoked, long at) {}
  /** A credited task: its first pass (Long.MIN_VALUE when no passed submission is left: counted from the start), hard mode, solved by the first submission. */
  record Credit(long taskId, long at, boolean hard, boolean firstTry) {}
  /** A topic's practice after a credited task, at the moment of that task's pass. */
  record Step(long at, int topic, int completed, int successes) {}

  static final class Student {
    final long id; final String login, name, group; final boolean participant;
    Language sessionCourse; Long diagnosticAt, firstLessonAt, lastActivityAt;
    /** Topics the diagnostic confirmed (from diagnosticAt on). */
    final boolean[] confirmed;
    final List<Lesson> lessons = new ArrayList<>();
    final List<Submission> submissions = new ArrayList<>();
    /** Credited tasks of the course: task → hard. */
    final Map<Long, Boolean> credited = new HashMap<>();
    /** Tasks given in a re-take of a closed topic (TopicRetakes), as lessonId → task ids: they never move iterations. */
    final Map<Long, Set<Long>> retakeTasks = new HashMap<>();
    /** UTC days (epoch days) with a submission or a chat message of the student. */
    final Set<Long> activeDays = new HashSet<>();
    Long chatLast;
    final List<Credit> credits = new ArrayList<>(); long[] solvedAt, hardAt;
    final List<Step> steps = new ArrayList<>();
    /** Moment of each topic's first iteration, Long.MAX_VALUE if none. */
    long[] firstIteration;
    Student(long id, String login, String name, String group, boolean participant, int topics) {
      this.id = id; this.login = login; this.name = name; this.group = group; this.participant = participant; this.confirmed = new boolean[topics];
    }
  }

  record Course(Language language, List<Topic> topics, List<Student> students, Map<Long, List<Integer>> targets) {
    List<Integer> targets(long task) { return targets.getOrDefault(task, List.of()); }
  }

  /** Which students to load: the whole course, one student or one group. */
  private record Scope(String kind, Object value) {
    static final Scope ALL = new Scope(null, null);
    static Scope user(long id) { return new Scope("user", id); }
    static Scope group(String name) { return new Scope("group", name); }
    String on(String userColumn) {
      return kind == null ? "" : "user".equals(kind) ? " and " + userColumn + "=?" : " and " + userColumn + " in (select id from users where group_name=?)";
    }
    Object[] with(Object... args) {
      if (kind == null) return args;
      var all = Arrays.copyOf(args, args.length + 1); all[args.length] = value; return all;
    }
  }

  private static String epoch(String column) { return "cast(strftime('%s'," + column + ") as integer)"; }
  private static Long epoch(ResultSet rs, int column) throws SQLException { long v = rs.getLong(column); return rs.wasNull() ? null : v; }

  /** One course in a fixed number of queries, whatever the number of students and submissions. */
  private Course load(Language lang, Scope scope) {
    String language = lang.name();
    var topics = db.query("select code,title,block_no from skills where language=? order by sort_order,id", (rs, i) -> new Topic(rs.getString(1), rs.getString(2), rs.getInt(3)), language);
    Map<String, Integer> topicIndex = new HashMap<>();
    for (int i = 0; i < topics.size(); i++) topicIndex.put(topics.get(i).code(), i);
    Map<Long, Student> students = new LinkedHashMap<>();
    db.query("select u.id,u.login,u.display_name,u.group_name,u.session_participant from users u where u.role='STUDENT' and (exists(select 1 from student_languages x where x.user_id=u.id and x.language=?) "
        + "or exists(select 1 from lessons l where l.user_id=u.id and l.language=?))" + scope.on("u.id") + " order by u.id",
        (RowCallbackHandler) rs -> students.put(rs.getLong(1), new Student(rs.getLong(1), rs.getString(2), rs.getString(3), rs.getString(4), rs.getInt(5) == 1, topics.size())),
        scope.with(language, language));
    Map<Long, List<Integer>> targets = new HashMap<>();
    if (students.isEmpty()) return new Course(lang, topics, List.of(), targets);

    // The course of the session needs lessons and diagnostics of every course.
    Map<Long, Map<Language, long[]>> lessonCounts = new HashMap<>();
    db.query("select user_id,language,count(*),max(" + epoch("started_at") + ") from lessons where 1=1" + scope.on("user_id") + " group by user_id,language",
        (RowCallbackHandler) rs -> { Long last = epoch(rs, 4); lessonCounts.computeIfAbsent(rs.getLong(1), k -> new EnumMap<>(Language.class)).put(Language.of(rs.getString(2)), new long[]{rs.getLong(3), last == null ? Long.MIN_VALUE : last}); },
        scope.with());
    Map<Long, Map<Language, Long>> diagnostics = new HashMap<>();
    db.query("select user_id,language," + epoch("diagnostic_completed_at") + " from student_languages where diagnostic_completed_at is not null" + scope.on("user_id"),
        (RowCallbackHandler) rs -> diagnostics.computeIfAbsent(rs.getLong(1), k -> new EnumMap<>(Language.class)).put(Language.of(rs.getString(2)), epoch(rs, 3)),
        scope.with());
    for (var s : students.values()) {
      s.sessionCourse = sessionCourse(lessonCounts.getOrDefault(s.id, Map.of()), diagnostics.getOrDefault(s.id, Map.of()));
      s.diagnosticAt = diagnostics.getOrDefault(s.id, Map.of()).get(lang);
    }

    db.query("select id,user_id,coalesce(language_lesson_number,lesson_number) as number," + epoch("started_at") + ",finished_at is null," + epoch("last_activity_at")
        + " from lessons where language=?" + scope.on("user_id") + " order by user_id,number,id",
        (RowCallbackHandler) rs -> { var s = students.get(rs.getLong(2)); if (s != null) s.lessons.add(new Lesson(rs.getLong(1), rs.getInt(3), epoch(rs, 4), rs.getInt(5) == 1, epoch(rs, 6))); },
        scope.with(language));
    db.query("select s.id,s.lesson_id,l.user_id,s.task_id,s.passed,s.revoked_at is not null," + epoch("s.created_at") + " from submissions s join lessons l on l.id=s.lesson_id where l.language=?"
        + scope.on("l.user_id") + " order by s.id",
        (RowCallbackHandler) rs -> { var s = students.get(rs.getLong(3)); Long at = epoch(rs, 7); if (s != null && at != null) s.submissions.add(new Submission(rs.getLong(1), rs.getLong(2), rs.getLong(4), rs.getInt(5) == 1, rs.getInt(6) == 1, at)); },
        scope.with(language));
    db.query("select c.user_id,c.task_id,t.mode='HARD' from successful_task_credit c join tasks t on t.id=c.task_id where t.language=?" + scope.on("c.user_id"),
        (RowCallbackHandler) rs -> { var s = students.get(rs.getLong(1)); if (s != null) s.credited.put(rs.getLong(2), rs.getInt(3) == 1); },
        scope.with(language));
    db.query("select l.user_id,lt.lesson_id,lt.task_id from lesson_tasks lt join lessons l on l.id=lt.lesson_id where l.language=? and lt.retake_id is not null" + scope.on("l.user_id"),
        (RowCallbackHandler) rs -> { var s = students.get(rs.getLong(1)); if (s != null) s.retakeTasks.computeIfAbsent(rs.getLong(2), k -> new HashSet<>()).add(rs.getLong(3)); },
        scope.with(language));
    db.query("select d.user_id,d.skill_code from diagnostic_skill_results d join skills k on k.code=d.skill_code where k.language=? and d.confirmed=1" + scope.on("d.user_id"),
        (RowCallbackHandler) rs -> { var s = students.get(rs.getLong(1)); Integer i = topicIndex.get(rs.getString(2)); if (s != null && i != null) s.confirmed[i] = true; },
        scope.with(language));
    db.query("select l.user_id," + epoch("m.created_at") + "/86400 as day,max(" + epoch("m.created_at") + ") from chat_messages m join lessons l on l.id=m.lesson_id where l.language=? and m.role='STUDENT'"
        + scope.on("l.user_id") + " group by l.user_id,day",
        (RowCallbackHandler) rs -> { var s = students.get(rs.getLong(1)); Long last = epoch(rs, 3); if (s != null && last != null) { s.activeDays.add(rs.getLong(2)); s.chatLast = s.chatLast == null ? last : Math.max(s.chatLast, last); } },
        scope.with(language));
    // Topics of the tasks the loaded students submitted or were credited for (all tasks of the course for the whole course).
    String touched = scope.kind() == null ? "" : " and (ts.task_id in (select c.task_id from successful_task_credit c where 1=1" + scope.on("c.user_id")
        + ") or ts.task_id in (select s.task_id from submissions s join lessons l on l.id=s.lesson_id where 1=1" + scope.on("l.user_id") + "))";
    db.query("select ts.task_id,ts.skill_code from task_target_skills ts join tasks t on t.id=ts.task_id where t.language=?" + touched,
        (RowCallbackHandler) rs -> { Integer i = topicIndex.get(rs.getString(2)); if (i != null) targets.computeIfAbsent(rs.getLong(1), k -> new ArrayList<>()).add(i); },
        scope.kind() == null ? new Object[]{language} : new Object[]{language, scope.value(), scope.value()});
    for (var s : students.values()) replay(s, targets, topics.size());
    return new Course(lang, topics, List.copyOf(students.values()), targets);
  }

  /** Credits, activity and the topic steps of one student, rebuilt from the loaded rows. */
  private static void replay(Student s, Map<Long, List<Integer>> targets, int topicCount) {
    Map<Long, Submission> firstSubmission = new HashMap<>(), firstPass = new HashMap<>();
    Map<Long, LinkedHashMap<Long, Long>> passes = new HashMap<>(); // lesson → credited task → its first pass in the lesson
    for (var x : s.submissions) {
      firstSubmission.putIfAbsent(x.taskId(), x);
      s.activeDays.add(Math.floorDiv(x.at(), DAY));
      if (!x.passed() || x.revoked() || !s.credited.containsKey(x.taskId())) continue;
      firstPass.putIfAbsent(x.taskId(), x);
      if (s.retakeTasks.getOrDefault(x.lessonId(), Set.of()).contains(x.taskId())) continue; // solved, but not practice of the topic
      passes.computeIfAbsent(x.lessonId(), k -> new LinkedHashMap<>()).putIfAbsent(x.taskId(), x.at());
    }
    for (var e : s.credited.entrySet()) {
      var pass = firstPass.get(e.getKey());
      s.credits.add(new Credit(e.getKey(), pass == null ? Long.MIN_VALUE : pass.at(), e.getValue(), pass != null && firstSubmission.get(e.getKey()).id() == pass.id()));
    }
    s.solvedAt = s.credits.stream().mapToLong(Credit::at).sorted().toArray();
    s.hardAt = s.credits.stream().filter(Credit::hard).mapToLong(Credit::at).sorted().toArray();

    // Lesson by lesson in lesson order, as ApiController.replayProgress; inside a lesson task by task, as live credit() ran.
    var state = new IterationRule.Topic[topicCount]; Arrays.fill(state, IterationRule.Topic.NEW);
    s.firstIteration = new long[topicCount]; Arrays.fill(s.firstIteration, Long.MAX_VALUE);
    for (var lesson : s.lessons) {
      var credited = passes.get(lesson.id());
      if (credited == null) continue;
      Map<Integer, Integer> solved = new HashMap<>(); Set<Integer> iterated = new HashSet<>();
      for (var task : credited.entrySet()) for (int topic : targets.getOrDefault(task.getKey(), List.of())) {
        var before = state[topic];
        var after = IterationRule.credit(before, solved.merge(topic, 1, Integer::sum), lesson.number(), iterated.contains(topic));
        if (after.equals(before)) continue;
        if (after.completed() > before.completed()) { iterated.add(topic); if (before.completed() == 0) s.firstIteration[topic] = task.getValue(); }
        state[topic] = after;
        s.steps.add(new Step(task.getValue(), topic, after.completed(), after.successes()));
      }
    }
    s.steps.sort(Comparator.comparingLong(Step::at));

    for (var l : s.lessons) {
      if (l.startedAt() != null) { s.firstLessonAt = s.firstLessonAt == null ? l.startedAt() : Math.min(s.firstLessonAt, l.startedAt()); s.lastActivityAt = later(s.lastActivityAt, l.startedAt()); }
      s.lastActivityAt = later(s.lastActivityAt, l.lastActivityAt());
    }
    if (!s.submissions.isEmpty()) s.lastActivityAt = later(s.lastActivityAt, s.submissions.getLast().at());
    s.lastActivityAt = later(s.lastActivityAt, s.chatLast);
  }
  private static Long later(Long a, Long b) { return a == null ? b : b == null ? a : (Long) Math.max(a, b); }

  /** Walks a student's history forward: every topic's state after everything that happened before a moment. */
  private static final class Cursor {
    private final Student s; final int[] completed, successes; private int next; private long until = Long.MIN_VALUE;
    Cursor(Student s) { this.s = s; completed = new int[s.confirmed.length]; successes = new int[s.confirmed.length]; }
    /** Moves to the moment `until` (epoch seconds, exclusive); moments only go forward. */
    Cursor at(long until) {
      this.until = until;
      while (next < s.steps.size() && s.steps.get(next).at() < until) { var step = s.steps.get(next++); completed[step.topic()] = step.completed(); successes[step.topic()] = step.successes(); }
      return this;
    }
    double share(int topic) { return IterationRule.share(completed[topic], successes[topic]); }
    boolean mastered(int topic) { return completed[topic] >= ApiController.ITERATION_TASKS.length; }
    boolean confirmed(int topic) { return s.confirmed[topic] && (s.diagnosticAt == null || s.diagnosticAt < until); }
    /** Topics closed so far: an iteration completed (or mastered), or confirmed by the diagnostic. */
    int closed() { int n = 0; for (int i = 0; i < completed.length; i++) if (completed[i] >= 1 || confirmed(i)) n++; return n; }
  }

  /** How many of the sorted moments are before `until`. */
  private static int before(long[] sorted, long until) {
    int lo = 0, hi = sorted.length;
    while (lo < hi) { int mid = (lo + hi) >>> 1; if (sorted[mid] < until) lo = mid + 1; else hi = mid; }
    return lo;
  }
  private static double percent(double sum, int topics) { return topics == 0 ? 0 : round(100 * sum / topics, 1); }
  static double round(double value, int digits) { double f = Math.pow(10, digits); return Math.round(value * f) / f; }
  private static Map<String, Object> obj(Object... entries) { var m = new LinkedHashMap<String, Object>(); for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]); return m; }
}

@Configuration
class ClockConfiguration {
  /** The current time of the progress analytics; tests replace it to fix «today». */
  @Bean Clock clock() { return Clock.systemUTC(); }
}
