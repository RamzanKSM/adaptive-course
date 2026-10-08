package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.core.annotation.Order;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import org.springframework.transaction.support.TransactionTemplate;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

/**
 * Hard-mode tasks from Exercism problem-specifications (MIT), see resources/hard-tasks. Each task comes with its
 * statement, starter code and test cases whose answers were checked against Exercism's canonical data when the bank
 * was built. Loaded at startup after the course topics exist; a task keeps its id (external_key), so submissions and
 * credit stay attached when a newer bank changes its statement or cases.
 */
@Component
@Order(10)
class HardTaskBank implements ApplicationRunner {
  private static final Logger log = LoggerFactory.getLogger(HardTaskBank.class);
  static final String RESOURCE = "hard-tasks/exercism.json";
  private static final TaskGoal GOAL = new TaskGoal(TaskGoal.Kind.IO_BEHAVIOR, null, List.of(), null, null, List.of());
  private final JdbcTemplate db;
  private final ObjectMapper json;
  private final TransactionTemplate tx;

  HardTaskBank(JdbcTemplate db, ObjectMapper json, TransactionTemplate tx) { this.db = db; this.json = json; this.tx = tx; }

  @Override public void run(ApplicationArguments args) throws Exception {
    JsonNode bank;
    try (InputStream in = new ClassPathResource(RESOURCE).getInputStream()) { bank = json.readTree(in); }
    int loaded = 0, skipped = 0;
    for (JsonNode task : bank.path("tasks")) {
      var variants = task.path("variants").fields();
      while (variants.hasNext()) {
        var variant = variants.next();
        if (store(task.path("slug").asText(), task.path("title").asText(), Language.of(variant.getKey()), variant.getValue())) loaded++; else skipped++;
      }
    }
    log.info("Hard-mode bank: {} tasks loaded from {}{}", loaded, RESOURCE, skipped > 0 ? ", " + skipped + " skipped (unknown topic)" : "");
  }

  private boolean store(String slug, String title, Language language, JsonNode variant) {
    String skill = variant.path("skill").asText();
    if (db.queryForObject("select count(*) from skills where code=? and language=?", Integer.class, skill, language.name()) == 0) {
      log.warn("Hard-mode task {} ({}) skipped: topic {} is not in the course", slug, language, skill);
      return false;
    }
    List<TestCases.Case> cases = new ArrayList<>();
    int ordinal = 0;
    for (JsonNode c : variant.path("cases")) cases.add(new TestCases.Case(++ordinal, c.path("input").asText(), c.path("expected").asText(), c.path("public").asBoolean()));
    String key = "exercism:" + slug + ":" + language.name();
    String checker = TestCases.checker(language, GOAL, cases);
    String testFile = language == Language.PYTHON ? "test_solution.py" : "TestHarness.java";
    tx.executeWithoutResult(status -> {
      var existing = db.queryForList("select id from tasks where external_key=?", Long.class, key);
      long id;
      if (existing.isEmpty()) {
        id = db.queryForObject("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,difficulty,language,source,goal_json,quality_version,mode,external_key) "
            + "values(?,?,?,?,?,?,?,?,'EXERCISM',?,?,'HARD',?) returning id", Long.class,
            skill, title, variant.path("statement").asText(), variant.path("starter").asText(), checker, testFile, variant.path("difficulty").asInt(), language.name(),
            GOAL.toJson(json), LearningContentGenerator.TASK_QUALITY_VERSION, key);
      } else {
        id = existing.getFirst();
        db.update("update tasks set skill_code=?, title=?, statement=?, starter_code=?, test_source=?, test_file_name=?, difficulty=?, goal_json=?, quality_version=?, mode='HARD', active=1 where id=?",
            skill, title, variant.path("statement").asText(), variant.path("starter").asText(), checker, testFile, variant.path("difficulty").asInt(), GOAL.toJson(json),
            LearningContentGenerator.TASK_QUALITY_VERSION, id);
        db.update("delete from task_target_skills where task_id=?", id);
        db.update("delete from task_cases where task_id=?", id);
      }
      db.update("insert into task_target_skills(task_id,skill_code) values(?,?)", id, skill);
      for (var c : cases) db.update("insert into task_cases(task_id,ordinal,input,expected,is_public) values(?,?,?,?,?)", id, c.ordinal(), c.input(), c.expected(), c.isPublic() ? 1 : 0);
    });
    return true;
  }
}
