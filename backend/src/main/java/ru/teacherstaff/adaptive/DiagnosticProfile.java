package ru.teacherstaff.adaptive;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import java.util.*;

/**
 * Turns diagnostic answers into a result per topic and decides which topics the diagnostic already confirmed.
 * Confirmed topics are skipped by practice. This is deliberately separate from practice progress: it never writes
 * iterations, task credit or mastery.
 *
 * <p>Rule for "the topic is confirmed":
 * <ul>
 *   <li>two or more questions on the topic — every one answered correctly;</li>
 *   <li>a single question — answered correctly <em>and</em> at least 80% correct in that question's block, because one
 *       right answer out of four options can be a guess.</li>
 * </ul>
 * A wrong answer or «Не знаю» on any question of the topic means it needs practice.
 */
@Component
class DiagnosticProfile implements ApplicationRunner {
  private static final Logger log = LoggerFactory.getLogger(DiagnosticProfile.class);
  static final int SINGLE_QUESTION_BLOCK_PERCENT = 80;
  private final JdbcTemplate db;

  DiagnosticProfile(JdbcTemplate db) { this.db = db; }

  record TopicResult(String skillCode, int correct, int total, boolean confirmed) {}

  static boolean confirmed(int correct, int total, int blockCorrect, int blockTotal) {
    if (total <= 0 || correct < total) return false;
    if (total >= 2) return true;
    return blockTotal > 0 && blockCorrect * 100 >= blockTotal * SINGLE_QUESTION_BLOCK_PERCENT;
  }

  /** Computes per-topic results from the stored answers and saves them, replacing earlier ones. */
  List<TopicResult> store(long userId, Language language) {
    var answers = db.queryForList("select q.skill_code, q.block_no, a.is_correct from diagnostic_answers a join diagnostic_questions q on q.id=a.question_id where a.user_id=? and q.language=?", userId, language.name());
    Map<Integer, int[]> blocks = new HashMap<>();
    Map<String, int[]> topics = new LinkedHashMap<>();
    Map<String, Integer> topicBlock = new HashMap<>();
    for (var row : answers) {
      String skill = (String) row.get("skill_code");
      int block = ((Number) row.get("block_no")).intValue();
      boolean ok = ((Number) row.get("is_correct")).intValue() == 1;
      int[] b = blocks.computeIfAbsent(block, x -> new int[2]); b[1]++; if (ok) b[0]++;
      int[] t = topics.computeIfAbsent(skill, x -> new int[2]); t[1]++; if (ok) t[0]++;
      topicBlock.put(skill, block);
    }
    List<TopicResult> results = new ArrayList<>();
    for (var entry : topics.entrySet()) {
      int[] t = entry.getValue(); int[] b = blocks.get(topicBlock.get(entry.getKey()));
      results.add(new TopicResult(entry.getKey(), t[0], t[1], confirmed(t[0], t[1], b[0], b[1])));
    }
    for (TopicResult r : results)
      db.update("insert into diagnostic_skill_results(user_id,skill_code,correct,total,confirmed) values(?,?,?,?,?) on conflict(user_id,skill_code) do update set correct=excluded.correct,total=excluded.total,confirmed=excluded.confirmed",
          userId, r.skillCode(), r.correct(), r.total(), r.confirmed() ? 1 : 0);
    log.info("Diagnostic profile for user={} language={}: {} of {} topics confirmed", userId, language, results.stream().filter(TopicResult::confirmed).count(), results.size());
    return results;
  }

  /** Students who took the diagnostic before per-topic results existed get them computed from their saved answers. */
  @Override public void run(ApplicationArguments args) {
    var pending = db.queryForList("select l.user_id, l.language from student_languages l where l.diagnostic_completed_at is not null and not exists("
        + "select 1 from diagnostic_skill_results d join skills s on s.code=d.skill_code where d.user_id=l.user_id and s.language=l.language)");
    for (var row : pending) store(((Number) row.get("user_id")).longValue(), Language.of(row.get("language")));
    if (!pending.isEmpty()) log.info("Backfilled per-topic diagnostic results for {} student course(s)", pending.size());
  }
}
