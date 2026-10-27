package ru.teacherstaff.adaptive;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import java.time.Clock;
import java.util.*;

/**
 * «Повторить тему» (owner, 2026-10-28): a student re-takes a topic already closed — mastered by practice or confirmed by
 * the diagnostic — at any moment of a lesson: a series of TASKS tasks of difficulty 1, 2, 3 inside the current lesson
 * (the lesson's unsolved task waits and comes back afterwards). The series ends when all are solved, on «Закончить
 * повторение» or with the lesson; failing costs nothing.
 * <p>A re-take never changes the topic's practice progress, the pace, the board range or anything else read from
 * student_skills/skill_iterations: its tasks are marked in lesson_tasks.retake_id and the iteration rule skips them
 * (ApiController.credit, replayProgress, ProgressAnalytics). Solved tasks are credited as usual — the solved count, XP
 * (no iteration or mastery bonus) and the pair's points (owner: they count).
 * <p>Task order (candidates): unsolved stories first — the re-take pool (tasks.mode='RETAKE', which lessons and the board
 * never take), then the regular bank — at the step's difficulty or the nearest; the generator is asked when the best one
 * is not a new story of that difficulty; the last resort is a variant of the story solved longest ago, which the student
 * sees as «похожая на решённую». Rules: backend/README.md, «Повторение темы».
 */
@Component
class TopicRetakes {
  private static final Logger log = LoggerFactory.getLogger(TopicRetakes.class);
  /** Tasks in a re-take, one per difficulty step 1, 2, 3. */
  static final int TASKS = 3;
  static final String DONE = "DONE", STUDENT = "STUDENT", LESSON = "LESSON", NO_TASK = "NO_TASK";

  private final JdbcTemplate db; private final Clock clock;
  TopicRetakes(JdbcTemplate db, Clock clock) { this.db = db; this.clock = clock; }

  /** Whether the student may re-take the topic: mastered by practice or confirmed by the diagnostic. */
  boolean closed(long user, String skill) {
    return count("select count(*) from student_skills where user_id=? and skill_code=? and mastered=1", user, skill) > 0
        || count("select count(*) from diagnostic_skill_results where user_id=? and skill_code=? and confirmed=1", user, skill) > 0;
  }

  /** The open re-take of a lesson, {id, skill_code, paused_task_id}, or null. */
  Map<String, Object> active(long lessonId) {
    var rows = db.queryForList("select id,skill_code,paused_task_id from topic_retakes where lesson_id=? and finished_at is null order by id desc limit 1", lessonId);
    return rows.isEmpty() ? null : rows.getFirst();
  }

  /**
   * Starts a re-take of the topic in the open lesson: an open re-take of another topic ends first, one of the same topic
   * goes on. pausedTaskId — the lesson's unsolved task, taken out now (replaced_at) and given back when the re-take ends.
   */
  long start(long user, long lessonId, String skill, Long pausedTaskId) {
    var open = active(lessonId);
    if (open != null && skill.equals(open.get("skill_code"))) return ((Number) open.get("id")).longValue();
    if (open != null) finish(((Number) open.get("id")).longValue(), STUDENT);
    if (pausedTaskId != null) db.update("update lesson_tasks set replaced_at=? where lesson_id=? and task_id=? and replaced_at is null", now(), lessonId, pausedTaskId);
    long id = db.queryForObject("insert into topic_retakes(user_id,skill_code,lesson_id,started_at,paused_task_id) values(?,?,?,?,?) returning id", Long.class,
        user, skill, lessonId, now(), pausedTaskId);
    log.info("Re-take {} of skill={} started by student {} in lesson {}{}", id, skill, user, lessonId, pausedTaskId == null ? "" : " (task " + pausedTaskId + " waits)");
    return id;
  }

  /**
   * Ends an open re-take: its unsolved task leaves the lesson, the paused task comes back. Returns its summary, or null
   * when it was not open.
   */
  Map<String, Object> finish(long id, String reason) {
    var rows = db.queryForList("select lesson_id,paused_task_id from topic_retakes where id=? and finished_at is null", id);
    if (rows.isEmpty()) return null;
    long lessonId = ((Number) rows.getFirst().get("lesson_id")).longValue();
    db.update("update topic_retakes set finished_at=?,finish_reason=? where id=? and finished_at is null", now(), reason, id);
    db.update("update lesson_tasks set replaced_at=? where retake_id=? and replaced_at is null and not exists(select 1 from submissions s where s.lesson_id=lesson_tasks.lesson_id and s.task_id=lesson_tasks.task_id and s.passed=1)", now(), id);
    if (rows.getFirst().get("paused_task_id") instanceof Number paused)
      db.update("update lesson_tasks set replaced_at=null where lesson_id=? and task_id=? and exists(select 1 from lessons where id=? and finished_at is null)", lessonId, paused.longValue(), lessonId);
    var view = view(id);
    log.info("Re-take {} finished ({}): {} of {} solved", id, reason, view.get("passed"), TASKS);
    return view;
  }

  /** Ends the open re-takes of a lesson that ends (nothing comes back into a finished lesson). */
  void finishLesson(long lessonId) {
    for (long id : db.queryForList("select id from topic_retakes where lesson_id=? and finished_at is null", Long.class, lessonId)) finish(id, LESSON);
  }

  /** The difficulty of the re-take's next task, 1..TASKS, or 0 when all its tasks were given. */
  int nextDifficulty(long id) {
    int given = count("select count(*) from lesson_tasks where retake_id=?", id);
    return given >= TASKS ? 0 : given + 1;
  }

  /** The re-take for the student's screen: {id, skillCode, skillTitle, total, given, passed, finished}. */
  Map<String, Object> view(long id) {
    var r = db.queryForMap("select r.id,r.skill_code,s.title,r.finished_at from topic_retakes r join skills s on s.code=r.skill_code where r.id=?", id);
    return obj("id", r.get("id"), "skillCode", r.get("skill_code"), "skillTitle", r.get("title"), "total", TASKS,
        "given", count("select count(*) from lesson_tasks where retake_id=?", id), "passed", passed(id), "finished", r.get("finished_at") != null);
  }
  private int passed(long id) {
    return count("select count(distinct lt.task_id) from lesson_tasks lt join submissions s on s.lesson_id=lt.lesson_id and s.task_id=lt.task_id and s.passed=1 and s.revoked_at is null where lt.retake_id=?", id);
  }

  /** The re-take a task of a lesson belongs to, or null (a regular task). */
  Long retakeOf(long lessonId, long taskId) {
    var ids = db.queryForList("select retake_id from lesson_tasks where lesson_id=? and task_id=? and retake_id is not null", Long.class, lessonId, taskId);
    return ids.isEmpty() ? null : ids.getFirst();
  }

  /** Marks a task just assigned to the lesson as the re-take's. */
  void mark(long lessonId, long taskId, long id) { db.update("update lesson_tasks set retake_id=? where lesson_id=? and task_id=?", id, lessonId, taskId); }

  /**
   * Candidate tasks for a re-take step (see the class comment for the order). story_solved — a variant of a solved
   * story; the best candidate is good enough without generation when it is a new story of the step's difficulty (fresh).
   */
  List<Map<String, Object>> candidates(long user, long lessonId, String skill, int difficulty) {
    long[] variants = ApiController.variantOrder(user);
    return db.queryForList("with candidates as (select t.id,t.title,t.statement,t.starter_code,t.difficulty,t.mode,"
        + "case when t.source='CURATED' and t.external_key like 'curated:%:%' then substr(t.external_key,1,8+instr(substr(t.external_key,9),':')) end as story "
        + "from tasks t join task_target_skills ts on ts.task_id=t.id where t.active=1 and t.mode in ('RETAKE','NORMAL') and ts.skill_code=? "
        + "and not exists(select 1 from successful_task_credit c where c.user_id=? and c.task_id=t.id) and not exists(select 1 from lesson_tasks x where x.lesson_id=? and x.task_id=t.id) "
        + "and not exists(select 1 from task_prerequisite_skills req where req.task_id=t.id and not exists(select 1 from student_skills p where p.user_id=? and p.skill_code=req.skill_code and p.mastered=1) "
        + "and not exists(select 1 from diagnostic_skill_results d where d.user_id=? and d.skill_code=req.skill_code and d.confirmed=1))), "
        + "ranked as (select c.*,c.story is not null and exists(select 1 from successful_task_credit x join tasks s on s.id=x.task_id where x.user_id=? and s.source='CURATED' and substr(s.external_key,1,length(c.story))=c.story) as story_solved,"
        + "coalesce((select min(s.id) from tasks s where s.source='CURATED' and substr(s.external_key,1,length(c.story))=c.story),c.id) as story_first from candidates c) "
        + "select r.*,case when r.story_solved then (select max(p.created_at) from submissions p join lessons l on l.id=p.lesson_id join tasks s on s.id=p.task_id "
        + "where l.user_id=? and p.passed=1 and s.source='CURATED' and substr(s.external_key,1,length(r.story))=r.story) end as story_last "
        + "from ranked r order by r.story_solved, r.difficulty is null, abs(r.difficulty-?), r.mode='RETAKE' desc, story_last, r.story_first, (r.id%?*?+?)%?, r.id",
        skill, user, lessonId, user, user, user, user, difficulty, ApiController.VARIANT_PRIME, variants[0], variants[1], ApiController.VARIANT_PRIME);
  }
  static boolean fresh(List<Map<String, Object>> candidates, int difficulty) {
    if (candidates.isEmpty()) return false;
    var best = candidates.getFirst();
    return !similar(best) && best.get("difficulty") instanceof Number d && d.intValue() == difficulty;
  }
  /** A variant of a story the student solved: the same task with other values («похожая на решённую»). */
  static boolean similar(Map<String, Object> task) { return task.get("story_solved") instanceof Number n && n.intValue() != 0; }

  /** Re-takes per topic for «Мой прогресс»: [{skillCode, times, lastAt}], counting re-takes with at least one solved task. */
  List<Map<String, Object>> history(long user, Language lang) {
    return db.queryForList("select r.skill_code as skillCode,count(*) as times,max(r.started_at) as lastAt from topic_retakes r join skills k on k.code=r.skill_code "
        + "where r.user_id=? and k.language=? and exists(select 1 from lesson_tasks lt join submissions s on s.lesson_id=lt.lesson_id and s.task_id=lt.task_id and s.passed=1 and s.revoked_at is null where lt.retake_id=r.id) "
        + "group by r.skill_code", user, lang.name());
  }
  /** How many topic re-takes (with a solved task) the student made in a course: the teacher's student card. */
  int times(long user, Language lang) { return history(user, lang).stream().mapToInt(h -> ((Number) h.get("times")).intValue()).sum(); }

  private String now() { return clock.instant().toString(); }
  private int count(String sql, Object... args) { Integer n = db.queryForObject(sql, Integer.class, args); return n == null ? 0 : n; }
  private static Map<String, Object> obj(Object... entries) { var m = new LinkedHashMap<String, Object>(); for (int i = 0; i < entries.length; i += 2) m.put((String) entries[i], entries[i + 1]); return m; }
}
