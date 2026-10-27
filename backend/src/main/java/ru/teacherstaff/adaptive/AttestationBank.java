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
import java.util.HashSet;
import java.util.Set;

/**
 * The attestation pool («Аттестация» in «К доске», BoardTests): integrative tasks over the course from its first topic up
 * to the task's own topic (skill), one story each, built and verified like the curated bank
 * (tools/curated_python/build_attestation.py → Verify.java) and shipped as resources/attestation-tasks/bank.json.
 * Loaded at startup with tasks.mode = 'ATTESTATION', so lessons and regular board tests never take them; a task keeps
 * its id by key (attest:<slug>), and a task that left the bank is deactivated (its tests stay readable).
 */
@Component
@Order(11)
class AttestationBank implements ApplicationRunner {
  private static final Logger log = LoggerFactory.getLogger(AttestationBank.class);
  static final String RESOURCE = "attestation-tasks/bank.json", KEY_PREFIX = "attest:", MODE = "ATTESTATION";
  private final JdbcTemplate db;
  private final ObjectMapper json;
  private final TransactionTemplate tx;

  AttestationBank(JdbcTemplate db, ObjectMapper json, TransactionTemplate tx) { this.db = db; this.json = json; this.tx = tx; }

  @Override public void run(ApplicationArguments args) throws Exception {
    JsonNode bank;
    try (InputStream in = new ClassPathResource(RESOURCE).getInputStream()) { bank = json.readTree(in); }
    load(bank);
  }

  /** Stores every task of the bank (by key) and deactivates pool tasks that are not in it any more. */
  void load(JsonNode bank) {
    Set<String> keys = new HashSet<>(); int loaded = 0, skipped = 0;
    for (JsonNode task : bank.path("tasks")) {
      String key = task.path("key").asText();
      if (!key.startsWith(KEY_PREFIX)) { log.warn("Attestation task {} skipped: the key must start with {}", key, KEY_PREFIX); skipped++; continue; }
      if (store(key, task)) { keys.add(key); loaded++; } else skipped++;
    }
    int retired = 0;
    for (var row : db.queryForList("select id,external_key from tasks where mode=? and active=1", MODE))
      if (!keys.contains((String) row.get("external_key"))) retired += db.update("update tasks set active=0 where id=?", row.get("id"));
    log.info("Attestation pool: {} tasks loaded from {}{}{}", loaded, RESOURCE, skipped > 0 ? ", " + skipped + " skipped" : "", retired > 0 ? ", " + retired + " retired" : "");
  }

  private boolean store(String key, JsonNode t) {
    Language language = Language.of(t.path("language").asText("PYTHON"));
    String skill = t.path("skill").asText();
    if (db.queryForObject("select count(*) from skills where code=? and language=?", Integer.class, skill, language.name()) == 0) {
      log.warn("Attestation task {} skipped: topic {} is not in the {} course", key, skill, language);
      return false;
    }
    String wrong = wrongJson(t.path("wrong"));
    tx.executeWithoutResult(status -> {
      var existing = db.queryForList("select id from tasks where external_key=?", Long.class, key);
      Object[] values = {skill, t.path("title").asText(), t.path("statement").asText(), t.path("starter").asText(), t.path("testSource").asText(), t.path("testFileName").asText(),
          t.path("difficulty").asInt(3), t.path("goalJson").asText(), LearningContentGenerator.TASK_QUALITY_VERSION, language.name(), t.path("reference").asText(null), wrong};
      long id;
      if (existing.isEmpty()) {
        Object[] insert = java.util.Arrays.copyOf(values, values.length + 1); insert[values.length] = key;
        id = db.queryForObject("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,difficulty,goal_json,quality_version,language,reference_code,wrong_json,source,mode,active,external_key) "
            + "values(?,?,?,?,?,?,?,?,?,?,?,?,'CURATED','" + MODE + "',1,?) returning id", Long.class, insert);
      } else {
        id = existing.getFirst();
        Object[] update = java.util.Arrays.copyOf(values, values.length + 1); update[values.length] = id;
        db.update("update tasks set skill_code=?,title=?,statement=?,starter_code=?,test_source=?,test_file_name=?,difficulty=?,goal_json=?,quality_version=?,language=?,reference_code=?,wrong_json=?,"
            + "source='CURATED',mode='" + MODE + "',active=1 where id=?", update);
        db.update("delete from task_target_skills where task_id=?", id);
        db.update("delete from task_cases where task_id=?", id);
      }
      db.update("insert into task_target_skills(task_id,skill_code) values(?,?)", id, skill);
      for (JsonNode c : t.path("cases"))
        db.update("insert into task_cases(task_id,ordinal,input,expected,is_public) values(?,?,?,?,?)", id, c.path("ordinal").asInt(), c.path("input").asText(), c.path("expected").asText(), c.path("public").asBoolean() ? 1 : 0);
    });
    return true;
  }

  /** tasks.wrong_json as import_bank.py writes it: [{description, source}], null without wrong solutions. */
  private String wrongJson(JsonNode wrong) {
    var list = new java.util.ArrayList<java.util.Map<String, String>>();
    for (JsonNode w : wrong) if (w.path("source").isTextual() && !w.path("source").asText().isBlank()) list.add(java.util.Map.of("description", w.path("description").asText(""), "source", w.path("source").asText()));
    try { return list.isEmpty() ? null : json.writeValueAsString(list); } catch (Exception e) { throw new IllegalStateException(e); }
  }
}
