package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.jdbc.core.JdbcTemplate;
import org.sqlite.SQLiteDataSource;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * Runs every task of the curated bank through the platform's own validation, exactly as a generated task is
 * validated before it is stored (ApiController.storeGeneratedTask): no platform internals in the statement, nothing
 * the topic has not taught yet, and TaskVerifier.verify on Piston — the reference passes, wrong solutions fail a check,
 * function tasks get their cases recorded from the reference. Writes the rows to import, with the reference program
 * (tasks.reference_code).
 *
 * Compile and run against the backend's classes:
 *   javac -cp "target/classes:$(cat cp.txt)" -d out Verify.java
 *   java -cp "out:target/classes:$(cat cp.txt)" ru.teacherstaff.adaptive.Verify bank.json course-copy.db http://127.0.0.1:2779 verified.json
 */
public class Verify {
  public static void main(String[] args) throws Exception {
    ObjectMapper json = new ObjectMapper();
    JsonNode bank = json.readTree(Files.readString(Path.of(args[0])));
    SQLiteDataSource source = new SQLiteDataSource(); source.setUrl("jdbc:sqlite:" + args[1]);
    JdbcTemplate db = new JdbcTemplate(source);
    PistonCodeRunner runner = new PistonCodeRunner(json, args[2], "", "", 5000, 3000, 268435456L, 134217728L);
    TaskVerifier verifier = new TaskVerifier(runner, json);
    ArrayNode out = json.createArrayNode();
    int failed = 0;
    for (JsonNode t : bank.path("tasks")) {
      String key = t.path("key").asText(), skill = t.path("skill").asText();
      Language language = Language.valueOf(t.path("language").asText("PYTHON"));
      try {
        String leak = ApiController.internalTerm(t.path("statement").asText());
        if (leak != null) throw new IllegalStateException("statement mentions platform internals: " + leak);
        var late = CourseConstructs.beyondTopic(db, language, skill, t.path("goal"), t.path("testSource").asText(), t.path("starter").asText(), t.path("reference").asText());
        if (!late.isEmpty()) throw new IllegalStateException("needs what the topic has not taught: " + CourseConstructs.describe(language, late));
        List<TaskGoal.Mutant> wrong = new ArrayList<>();
        for (JsonNode w : t.path("wrong")) wrong.add(new TaskGoal.Mutant(w.path("description").asText(), w.path("source").asText()));
        List<TestCases.Input> inputs = new ArrayList<>();
        for (JsonNode i : t.path("testInputs")) inputs.add(new TestCases.Input(i.path("input").asText(), i.path("public").asBoolean()));
        var task = new GeneratedTask(skill, t.path("title").asText(), t.path("statement").asText(), t.path("starter").asText(), t.path("testSource").asText(),
            t.path("testFileName").asText(), t.path("reference").asText(), List.of(skill), List.of(), t.path("goal"), wrong, inputs);
        TaskVerifier.Verified verified = verifier.verify(language, task);
        ObjectNode row = out.addObject();
        row.put("key", key); row.put("language", language.name()); row.put("skill", skill); row.put("difficulty", t.path("difficulty").asInt());
        row.put("title", t.path("title").asText()); row.put("statement", t.path("statement").asText()); row.put("starter", t.path("starter").asText());
        row.put("testSource", verified.testSource()); row.put("testFileName", t.path("testFileName").asText()); row.put("goalJson", verified.goalJson());
        row.put("reference", t.path("reference").asText()); // shown by the «Что выведет этот код?» item of the test at the board
        ArrayNode cases = row.putArray("cases");
        for (var c : verified.cases()) { ObjectNode n = cases.addObject(); n.put("ordinal", c.ordinal()); n.put("input", c.input()); n.put("expected", c.expected()); n.put("public", c.isPublic()); }
        System.out.println("✓ " + key);
      } catch (Exception e) {
        failed++;
        System.out.println("✗ " + key + ": " + e.getMessage());
      }
    }
    Files.writeString(Path.of(args[3]), json.writerWithDefaultPrettyPrinter().writeValueAsString(json.createObjectNode().set("tasks", out)));
    System.out.println(out.size() + " verified, " + failed + " failed");
    if (failed > 0) System.exit(1);
  }
}
