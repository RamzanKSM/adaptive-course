package ru.teacherstaff.adaptive;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;
import org.springframework.stereotype.Component;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.*;

/**
 * «Тренировочная аттестация» (owner, 2026-10-28: students find the attestation too hard because they never met such
 * tasks): the student starts it himself in a lesson — one task of the real attestation's size and kind from the practice
 * pool (AttestationBank.PRACTICE; a task covers the course's topics 1…its skill), a MINUTES timer, no grade, no effect on
 * progress. The lesson's unsolved task waits and comes back afterwards, exactly as in «Повторить тему».
 * <p>A practice is a row of topic_retakes with kind = KIND (V37): its task is marked in lesson_tasks.retake_id, so the
 * iteration rule skips it (ApiController.credit, replayProgress, ProgressAnalytics) and nothing read from student_skills
 * or skill_iterations changes — iterations, mastery, closed topics, pace, the plan line, the forecast, the board range,
 * hard-mode readiness, grades. A solved task is credited as usual: the solved count, XP (+10, no bonus), the pair's
 * points. «Повторить тему» shows and counts only its own rows (TopicRetakes.TOPIC).
 * <p>Available once the student passed the course's topics in order (block, topic) without a gap from the first one up to
 * a level of the pool — passed: an iteration, mastered or confirmed by the diagnostic («тема пройдена» of the progress
 * analytics); the level is the highest pool level within that prefix. While the timer runs and the task is not solved
 * the assistant is closed (PRACTICE_RUNNING); afterwards nothing closes and the task can be finished. A practice ends when
 * its task is solved (IN_TIME by the deadline, else LATE), on «Завершить» or with the lesson (NOT_SOLVED unless solved).
 * Rules: backend/README.md, «Тренировочная аттестация».
 */
@Component
class AttestationPractice {
  private static final Logger log = LoggerFactory.getLogger(AttestationPractice.class);
  /** The timer: minutes from the start. */
  static final int MINUTES = 10;
  /** topic_retakes.kind of a practice. */
  static final String KIND = "ATTESTATION";
  static final String IN_TIME = "IN_TIME", LATE = "LATE", NOT_SOLVED = "NOT_SOLVED";

  private final JdbcTemplate db; private final Clock clock; private final TopicRetakes retakes;
  AttestationPractice(JdbcTemplate db, Clock clock, TopicRetakes retakes) { this.db = db; this.clock = clock; this.retakes = retakes; }

  /** A pool task: its topic (skill) and that topic's position in the course — the task covers topics 1…level. */
  record Option(long id, String skill, int level) {}

  /**
   * «attestationPractice» of /api/progress: {available, levelTopics, levelTitle, minutes, needTopics, history}. needTopics —
   * while not available, how many more topics in order lead to the lowest level of the pool (null without a pool).
   */
  Map<String, Object> offer(long user, Language lang) {
    var course = course(lang);
    int passed = prefix(user, lang, course);
    var levels = levels(lang, course);
    Integer level = levels.floor(passed);
    return obj("available", level != null, "levelTopics", level, "levelTitle", level == null ? null : course.get(level - 1)[1], "minutes", MINUTES,
        "needTopics", level != null || levels.isEmpty() ? null : levels.first() - passed, "history", history(user, lang));
  }

  /** The open practice of a lesson, {id, skill_code, paused_task_id, deadline_at, result}, or null. */
  Map<String, Object> active(long lessonId) {
    var rows = db.queryForList("select id,skill_code,paused_task_id,deadline_at,result from topic_retakes where lesson_id=? and kind=? and finished_at is null order by id desc limit 1", lessonId, KIND);
    return rows.isEmpty() ? null : rows.getFirst();
  }

  /**
   * The task of a new practice: pool tasks up to the student's level that are not in this lesson; stories he never solved
   * first, the level before lower levels (they come in when every story of the level was solved), a story never given to
   * him before one he left unsolved, then the one solved longest ago; among equals an order of his own
   * (ApiController.variantOrder), so neighbours get different stories.
   */
  Option choose(long user, long lessonId, Language lang) {
    var course = course(lang);
    int passed = prefix(user, lang, course);
    var levels = levels(lang, course);
    Integer level = levels.floor(passed);
    if (level == null) throw new ApiError("PRACTICE_NOT_AVAILABLE", levels.isEmpty() ? "Тренировочной аттестации в курсе " + lang.title + " пока нет"
        : "Тренировочная аттестация откроется, когда пройдёшь ещё " + topics(levels.first() - passed) + " по порядку");
    var position = positions(course);
    long[] order = ApiController.variantOrder(user);
    record Candidate(Option option, boolean solved, boolean given, String lastSolved, long rank) {}
    var candidates = new ArrayList<Candidate>();
    db.query("select t.id,ts.skill_code,exists(select 1 from successful_task_credit c where c.user_id=? and c.task_id=t.id),"
        + "exists(select 1 from lesson_tasks g join lessons l on l.id=g.lesson_id where l.user_id=? and g.task_id=t.id),"
        + "(select max(s.created_at) from submissions s join lessons l on l.id=s.lesson_id where l.user_id=? and s.task_id=t.id and s.passed=1) "
        + "from tasks t join task_target_skills ts on ts.task_id=t.id where t.language=? and t.active=1 and t.mode=? and not exists(select 1 from lesson_tasks x where x.lesson_id=? and x.task_id=t.id)",
        (RowCallbackHandler) rs -> {
          Integer at = position.get(rs.getString(2)); long id = rs.getLong(1);
          if (at != null && at <= level) candidates.add(new Candidate(new Option(id, rs.getString(2), at), rs.getInt(3) == 1, rs.getInt(4) == 1, rs.getString(5),
              (id % ApiController.VARIANT_PRIME * order[0] + order[1]) % ApiController.VARIANT_PRIME));
        }, user, user, user, lang.name(), AttestationBank.PRACTICE.mode(), lessonId);
    if (candidates.isEmpty()) throw new ApiError("NO_PRACTICE_TASK", "Новой задачи для тренировочной аттестации в этом уроке нет — попробуй на следующем");
    candidates.sort(Comparator.comparing(Candidate::solved).thenComparingInt(c -> -c.option().level()).thenComparing(Candidate::given)
        .thenComparing(Candidate::lastSolved, Comparator.nullsFirst(Comparator.naturalOrder())).thenComparingLong(Candidate::rank).thenComparingLong(c -> c.option().id()));
    return candidates.getFirst().option();
  }

  /**
   * Starts a practice with the chosen task in the open lesson; the task is marked as the practice's (lesson_tasks.retake_id).
   * pausedTaskId — the lesson's unsolved task, taken out now (replaced_at) and given back when the practice ends.
   */
  long start(long user, long lessonId, Option task, Long pausedTaskId) {
    Instant now = clock.instant();
    long id = db.queryForObject("insert into topic_retakes(user_id,skill_code,lesson_id,started_at,paused_task_id,kind,deadline_at) values(?,?,?,?,?,?,?) returning id", Long.class,
        user, task.skill(), lessonId, now.toString(), pausedTaskId, KIND, now.plus(Duration.ofMinutes(MINUTES)).toString());
    if (pausedTaskId != null) db.update("update lesson_tasks set replaced_at=? where lesson_id=? and task_id=? and replaced_at is null", now.toString(), lessonId, pausedTaskId);
    if (db.update("insert into lesson_tasks(lesson_id,task_id,retake_id) select ?,?,? where exists(select 1 from lessons where id=? and finished_at is null) "
        + "on conflict(lesson_id,task_id) do update set replaced_at=null,retake_id=excluded.retake_id", lessonId, task.id(), id, lessonId) == 0) {
      retakes.close(id, TopicRetakes.LESSON); // the lesson ended meanwhile
      throw new ApiError("NO_ACTIVE_LESSON", "Сначала начните урок");
    }
    log.info("Attestation practice {} started by student {} in lesson {}: task {}, topics 1–{}{}", id, user, lessonId, task.id(), task.level(), pausedTaskId == null ? "" : " (task " + pausedTaskId + " waits)");
    return id;
  }

  /**
   * The task of an open practice passed (inside the attempt's transaction): IN_TIME by the deadline, otherwise LATE. The
   * practice stays open until the next /learning/next ends it and gives the waiting task back (practiceDone).
   */
  void solved(long lessonId, long taskId) {
    var rows = db.queryForList("select r.id,r.started_at,r.deadline_at from lesson_tasks lt join topic_retakes r on r.id=lt.retake_id "
        + "where lt.lesson_id=? and lt.task_id=? and r.kind=? and r.finished_at is null and r.result is null", lessonId, taskId, KIND);
    if (rows.isEmpty()) return;
    var r = rows.getFirst(); Instant now = clock.instant();
    String result = now.isAfter(Instant.parse((String) r.get("deadline_at"))) ? LATE : IN_TIME;
    if (db.update("update topic_retakes set result=?,solved_at=? where id=? and result is null", result, now.toString(), r.get("id")) > 0)
      log.info("Attestation practice {} solved {} in {} s", r.get("id"), result, Duration.between(Instant.parse((String) r.get("started_at")), now).getSeconds());
  }

  /** Ends an open practice (NOT_SOLVED unless its task was solved); the waiting task comes back. Its view, or null when it was not open. */
  Map<String, Object> finish(long id, String reason) {
    if (!retakes.close(id, reason)) return null;
    var view = view(id);
    log.info("Attestation practice {} finished ({}): {}", id, reason, view.get("result"));
    return view;
  }

  /** Ends the open practice of a lesson that ends (nothing comes back into a finished lesson). */
  void finishLesson(long lessonId) {
    for (long id : db.queryForList("select id from topic_retakes where lesson_id=? and kind=? and finished_at is null", Long.class, lessonId, KIND)) finish(id, TopicRetakes.LESSON);
  }

  /** Whether the assistant is closed in the lesson: its practice runs (before the deadline) and the task is not solved. */
  boolean timerRunning(long lessonId) {
    var open = active(lessonId);
    return open != null && open.get("result") == null && clock.instant().isBefore(Instant.parse((String) open.get("deadline_at")));
  }

  /** The practice a task of a lesson belongs to, or null. */
  Long practiceOf(long lessonId, long taskId) {
    var ids = db.queryForList("select lt.retake_id from lesson_tasks lt join topic_retakes r on r.id=lt.retake_id and r.kind=? where lt.lesson_id=? and lt.task_id=?", Long.class, KIND, lessonId, taskId);
    return ids.isEmpty() ? null : ids.getFirst();
  }

  /**
   * The practice for the student's screen: {id, levelTopics, levelTitle, minutes, startedAt, deadlineAt, secondsLeft,
   * finished, passed, result, seconds}. secondsLeft — to the deadline while the timer runs (open, task unsolved), else 0;
   * seconds — from the start to the first pass, null without one.
   */
  Map<String, Object> view(long id) {
    var r = db.queryForMap("select r.id,r.skill_code,k.title,k.language,r.started_at,r.deadline_at,r.finished_at,r.result,r.solved_at from topic_retakes r join skills k on k.code=r.skill_code where r.id=?", id);
    Instant started = Instant.parse((String) r.get("started_at")), deadline = Instant.parse((String) r.get("deadline_at"));
    boolean finished = r.get("finished_at") != null, passed = r.get("solved_at") != null;
    long left = finished || passed ? 0 : Math.max(0, Duration.between(clock.instant(), deadline).getSeconds());
    return obj("id", r.get("id"), "levelTopics", positions(course(Language.of(r.get("language")))).get(r.get("skill_code")), "levelTitle", r.get("title"),
        "minutes", Duration.between(started, deadline).toMinutes(), "startedAt", r.get("started_at"), "deadlineAt", r.get("deadline_at"), "secondsLeft", left,
        "finished", finished, "passed", passed, "result", r.get("result"), "seconds", seconds(r));
  }

  /** The student's practices in a course, newest first: [{id, startedAt, levelTopics, levelTitle, taskTitle, result, seconds}] (result null — still open). */
  List<Map<String, Object>> history(long user, Language lang) {
    var position = positions(course(lang));
    return db.queryForList("select r.id,r.skill_code,k.title,r.started_at,r.result,r.solved_at,(select t.title from lesson_tasks lt join tasks t on t.id=lt.task_id where lt.retake_id=r.id limit 1) as task_title "
        + "from topic_retakes r join skills k on k.code=r.skill_code where r.user_id=? and r.kind=? and k.language=? order by r.id desc", user, KIND, lang.name())
        .stream().map(r -> obj("id", r.get("id"), "startedAt", r.get("started_at"), "levelTopics", position.get(r.get("skill_code")), "levelTitle", r.get("title"),
            "taskTitle", r.get("task_title"), "result", r.get("result"), "seconds", seconds(r))).toList();
  }
  private static Long seconds(Map<String, Object> r) {
    return r.get("solved_at") == null ? null : Duration.between(Instant.parse((String) r.get("started_at")), Instant.parse((String) r.get("solved_at"))).getSeconds();
  }

  /** The course's topics in course order (block, topic): [code, title]. */
  private List<String[]> course(Language lang) {
    return db.query("select code,title from skills where language=? order by block_no,sort_order,code", (rs, i) -> new String[]{rs.getString(1), rs.getString(2)}, lang.name());
  }
  /** Topic code → its position in the course, 1-based. */
  private static Map<String, Integer> positions(List<String[]> course) { var at = new HashMap<String, Integer>(); for (int i = 0; i < course.size(); i++) at.put(course.get(i)[0], i + 1); return at; }
  /** How many of the course's first topics the student passed without a gap (an iteration, mastered or confirmed by the diagnostic). */
  private int prefix(long user, Language lang, List<String[]> course) {
    var passed = new HashSet<>(db.queryForList("select s.code from skills s where s.language=? and (exists(select 1 from student_skills x where x.user_id=? and x.skill_code=s.code and (x.completed_iterations>=1 or x.mastered=1)) "
        + "or exists(select 1 from diagnostic_skill_results d where d.user_id=? and d.skill_code=s.code and d.confirmed=1))", String.class, lang.name(), user, user));
    int n = 0; while (n < course.size() && passed.contains(course.get(n)[0])) n++;
    return n;
  }
  /** The levels of the pool: positions of the topics of its active tasks. */
  private TreeSet<Integer> levels(Language lang, List<String[]> course) {
    var position = positions(course); var levels = new TreeSet<Integer>();
    for (String skill : db.queryForList("select distinct ts.skill_code from tasks t join task_target_skills ts on ts.task_id=t.id where t.language=? and t.active=1 and t.mode=?", String.class, lang.name(), AttestationBank.PRACTICE.mode()))
      if (position.get(skill) instanceof Integer at) levels.add(at);
    return levels;
  }
  /** «N тему / темы / тем» after «пройдёшь ещё». */
  private static String topics(int n) { int m = n % 100; return n + (m >= 11 && m <= 14 ? " тем" : n % 10 == 1 ? " тему" : n % 10 >= 2 && n % 10 <= 4 ? " темы" : " тем"); }
  private static Map<String, Object> obj(Object... entries) { var m = new LinkedHashMap<String, Object>(); for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]); return m; }
}
