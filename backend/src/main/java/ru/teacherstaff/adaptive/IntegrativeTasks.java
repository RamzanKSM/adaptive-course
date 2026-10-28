package ru.teacherstaff.adaptive;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import java.util.Map;

/**
 * The 3rd iteration of a topic is one integrative task (owner, 2026-10-28: students found the attestation too hard
 * because they never met such tasks): the topic at its core plus 1–2 earlier topics, in the attestation's format (a
 * story, data in fields or variables, numbered steps), about 4–5 minutes. The tasks come from the integrative pool
 * (AttestationBank.INTEGRATIVE, tasks.mode = 'INTEGRATIVE'), which nothing else takes; a task's only target skill is the
 * topic at its core, so crediting is unchanged: solving it completes the 3rd iteration and the topic is mastered
 * (IterationRule), and a revoked credit is redone as for any task.
 * <p>Only for topics outside block 0 (the first five topics of each course keep their ordinary tasks). There is no way
 * back to an ordinary task because the student cannot solve it (owner) — he solves it like any lesson task, with the
 * assistant; only when the pool has no unsolved task of the topic (not written yet, or all solved) the lesson takes an
 * ordinary task as before.
 */
@Component
class IntegrativeTasks {
  private static final Logger log = LoggerFactory.getLogger(IntegrativeTasks.class);
  /** Completed iterations of a topic whose last (3rd) iteration is due. */
  static final int COMPLETED = ApiController.ITERATION_TASKS.length - 1;
  private final JdbcTemplate db;
  IntegrativeTasks(JdbcTemplate db) { this.db = db; }

  /**
   * The integrative task the lesson gives for the topic: when its 3rd iteration is due (the lesson chose the topic with
   * COMPLETED iterations) and it is not in block 0 — a pool task of the topic the student has not solved and that is not
   * in this lesson yet, in an order of the student's own (ApiController.variantOrder, as the re-take candidates), so
   * neighbours get different stories. Null when the rule does not apply or the pool has no such task; the row has what
   * the lesson's task view needs.
   */
  Map<String, Object> next(long user, long lessonId, String skill) {
    var topic = db.queryForList("select coalesce(x.completed_iterations,0) as completed,s.block_no from skills s left join student_skills x on x.skill_code=s.code and x.user_id=? where s.code=?", user, skill);
    if (topic.isEmpty() || ((Number) topic.getFirst().get("completed")).intValue() != COMPLETED || ((Number) topic.getFirst().get("block_no")).intValue() == 0) return null;
    long[] order = ApiController.variantOrder(user);
    var rows = db.queryForList("select t.id,t.title,t.statement,t.starter_code,t.mode,ts.skill_code,s.title as skill_title,s.block_no from tasks t join task_target_skills ts on ts.task_id=t.id join skills s on s.code=ts.skill_code "
        + "where t.active=1 and t.mode=? and ts.skill_code=? and not exists(select 1 from successful_task_credit c where c.user_id=? and c.task_id=t.id) "
        + "and not exists(select 1 from lesson_tasks x where x.lesson_id=? and x.task_id=t.id) order by (t.id%?*?+?)%?, t.id limit 1",
        AttestationBank.INTEGRATIVE.mode(), skill, user, lessonId, ApiController.VARIANT_PRIME, order[0], order[1], ApiController.VARIANT_PRIME);
    if (rows.isEmpty()) { log.info("No unsolved integrative task of skill={} for its 3rd iteration in lesson {}: an ordinary task is given", skill, lessonId); return null; }
    log.info("Integrative task {} for the 3rd iteration of skill={} in lesson {}", rows.getFirst().get("id"), skill, lessonId);
    return rows.getFirst();
  }
}
