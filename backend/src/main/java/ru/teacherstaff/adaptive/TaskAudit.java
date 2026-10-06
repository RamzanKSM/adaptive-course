package ru.teacherstaff.adaptive;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.DisposableBean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * Re-verifies generated tasks accepted by an older, output-only validation (quality_version below the current one).
 * The statement students see is kept; the generator writes a goal, a reference solution, wrong solutions and new
 * checks, and TaskVerifier must accept them. A task that cannot be repaired is retired and a new one is generated
 * on demand. Past submissions, credit and progress are not recalculated — only future submissions use the new checks.
 */
@Component
class TaskAudit implements ApplicationRunner, DisposableBean {
  private static final Logger log = LoggerFactory.getLogger(TaskAudit.class);
  static final int REPAIR_ATTEMPTS = 2;
  private final JdbcTemplate db;
  private final LearningContentGenerator generator;
  private final TaskVerifier verifier;
  private final PistonCodeRunner runner;
  private final boolean enabled;
  private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor(Thread.ofVirtual().name("task-audit").factory());

  TaskAudit(JdbcTemplate db, LearningContentGenerator generator, TaskVerifier verifier, PistonCodeRunner runner,
            @Value("${app.task-audit.enabled:true}") boolean enabled) {
    this.db = db; this.generator = generator; this.verifier = verifier; this.runner = runner; this.enabled = enabled;
  }

  @Override public void run(ApplicationArguments args) {
    if (!enabled) return;
    // Retries every 15 minutes: the LLM or Piston may be unavailable at startup.
    scheduler.scheduleWithFixedDelay(this::auditPending, 30, 15 * 60, TimeUnit.SECONDS);
  }

  @Override public void destroy() { scheduler.shutdownNow(); }

  /** Returns how many tasks were repaired; stops early when the LLM or Piston is unavailable. */
  int auditPending() {
    var pending = db.queryForList("select t.id,t.title,t.statement,t.starter_code,t.test_source,t.language,t.difficulty,ts.skill_code from tasks t join task_target_skills ts on ts.task_id=t.id "
        + "where t.active=1 and t.source='LLM' and coalesce(t.quality_version,0)<? group by t.id order by t.id", LearningContentGenerator.TASK_QUALITY_VERSION);
    if (pending.isEmpty()) return 0;
    if (!generator.available()) { log.info("{} task(s) await re-verification; LLM is unavailable, will retry", pending.size()); return 0; }
    int repaired = 0;
    for (var row : pending) {
      Language language = Language.of(row.get("language"));
      if (!runner.status(language).available()) { log.info("Task re-verification paused: {} runtime is unavailable", language); break; }
      long id = ((Number) row.get("id")).longValue();
      try {
        if (repair(id, row, language)) repaired++;
      } catch (LlmUnavailableException e) {
        log.warn("Task re-verification paused at task {}: {}", id, e.getMessage());
        break;
      } catch (Exception e) {
        log.error("Task {} re-verification failed unexpectedly", id, e);
      }
    }
    return repaired;
  }

  private boolean repair(long id, java.util.Map<String, Object> row, Language language) {
    String skill = (String) row.get("skill_code");
    int difficulty = row.get("difficulty") instanceof Number n ? n.intValue() : 1;
    var explanation = db.queryForList("select content from explanations where skill_code=?", String.class, skill);
    ContentBrief brief = CourseBriefs.brief(db, null, skill, difficulty, explanation.isEmpty() ? null : explanation.getFirst());
    ExistingTask existing = new ExistingTask(id, (String) row.get("title"), (String) row.get("statement"), (String) row.get("starter_code"), (String) row.get("test_source"));
    log.info("Re-verifying task {} '{}' (skill={}, language={})", id, existing.title(), skill, language);
    for (int attempt = 1; attempt <= REPAIR_ATTEMPTS; attempt++) {
      try {
        GeneratedTask candidate = generator.repairTask(brief, existing);
        if (candidate == null) throw new InvalidGeneratedContentException("empty response");
        if (!ApiController.validHarness(language, candidate.testSource())) throw new InvalidGeneratedContentException("test harness does not follow the " + language.title + " contract");
        TaskVerifier.Verified verified = verifier.verify(language, candidate);
        db.update("update tasks set test_source=?, goal_json=?, quality_version=? where id=?", verified.testSource(), verified.goalJson(), LearningContentGenerator.TASK_QUALITY_VERSION, id);
        markOutcome(skill, "ACCEPTED");
        log.info("Task {} '{}' now has verified checks; earlier submissions and credit are unchanged", id, existing.title());
        return true;
      } catch (InvalidGeneratedContentException e) {
        markOutcome(skill, "REJECTED");
        log.warn("Repair of task {} rejected (attempt {}/{}): {}", id, attempt, REPAIR_ATTEMPTS, e.getMessage());
      }
    }
    db.update("update tasks set active=0 where id=?", id);
    log.warn("Task {} '{}' retired: its checks could not be made reliable; a new task will be generated when needed", id, existing.title());
    return false;
  }

  private void markOutcome(String skill, String outcome) {
    db.update("update llm_calls set outcome=? where id=(select max(id) from llm_calls where purpose='TASK_REPAIR' and skill_code=? and status='OK' and outcome is null)", outcome, skill);
  }
}
