package ru.teacherstaff.adaptive;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import java.nio.file.Path;
import java.util.UUID;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.NONE)
class DiagnosticImportIntegrationTest {
  @Autowired JdbcTemplate db;
  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:diagnostic-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
  }
  @Test void importsTheSpecifiedDiagnosticAndSeedContent() {
    assertEquals(56, db.queryForObject("select count(*) from diagnostic_questions", Integer.class));
    assertEquals(44, db.queryForObject("select count(*) from skills", Integer.class));
    assertEquals(9, db.queryForObject("select count(*) from tasks", Integer.class));
    assertEquals(1, db.queryForObject("select count(*) from explanations", Integer.class));
    String harness=db.queryForObject("select test_source from tasks where title='Число и текст'",String.class);
    assertTrue(harness.contains("class TestHarness"));
    assertTrue(harness.contains("main("));
    assertTrue(harness.contains(PistonCodeRunner.PASS_MARKER_PLACEHOLDER));
    var seeds=db.queryForList("select t.statement,t.starter_code from tasks t join task_target_skills ts on ts.task_id=t.id where ts.skill_code='BASIC_CODE_READING'");
    assertEquals(9,seeds.size());
    for(var seed:seeds) { assertTrue(((String)seed.get("statement")).contains("System.out.print")); assertTrue(((String)seed.get("starter_code")).contains("String answer()")); }
  }
}
