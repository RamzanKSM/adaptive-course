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
    assertEquals(56, db.queryForObject("select count(*) from diagnostic_questions where language='JAVA'", Integer.class));
    assertEquals(44, db.queryForObject("select count(*) from skills where language='JAVA'", Integer.class));
    assertEquals(9, db.queryForObject("select count(*) from tasks where language='JAVA'", Integer.class));
    assertEquals(1, db.queryForObject("select count(*) from explanations e join skills s on s.code=e.skill_code where s.language='JAVA'", Integer.class));
    String harness=db.queryForObject("select test_source from tasks where title='Консоль: кота'",String.class);
    assertTrue(harness.contains("class TestHarness"));
    assertTrue(harness.contains("main("));
    assertTrue(harness.contains(PistonCodeRunner.PASS_MARKER_PLACEHOLDER));
    var seeds=db.queryForList("select t.statement,t.starter_code from tasks t join task_target_skills ts on ts.task_id=t.id where ts.skill_code='BASIC_CODE_READING'");
    assertEquals(9,seeds.size());
    for(var seed:seeds) { assertTrue(((String)seed.get("statement")).contains("System.out.print")); assertTrue(((String)seed.get("starter_code")).contains("void main(String[] args)")); }
    var twoLines=db.queryForMap("select statement,starter_code from tasks where title='Консоль: две строки'");
    assertTrue(((String)twoLines.get("statement")).contains("Дополни тело `Solution.main(String[] args)`"));
    assertTrue(((String)twoLines.get("starter_code")).contains("public class Solution {\n    public static void main(String[] args)"));
    assertTrue(harness.contains("ByteArrayOutputStream"));
    assertTrue(harness.contains("Solution.main(new String[0])"));
    assertTrue(harness.contains("finally"));
  }

  @Test void importsThePythonTrackSeparately() {
    assertEquals(62, db.queryForObject("select count(*) from diagnostic_questions where language='PYTHON'", Integer.class));
    assertEquals(0, db.queryForObject("select count(*) from diagnostic_questions where language='PYTHON' and ordinal<=1000", Integer.class));
    assertEquals(52, db.queryForObject("select count(*) from skills where language='PYTHON' and code like 'PY_%'", Integer.class));
    assertEquals(0, db.queryForObject("select count(*) from skills where language='PYTHON' and title=code", Integer.class), "every Python skill has a readable title");
    assertEquals(9, db.queryForObject("select count(*) from tasks where language='PYTHON' and skill_code='PY_BASIC_CODE_READING'", Integer.class));
    assertEquals(3, db.queryForObject("select count(*) from tasks where language='PYTHON' and difficulty=1", Integer.class));
    var harnesses=db.queryForList("select test_source from tasks where language='PYTHON'", String.class);
    for (String harness : harnesses) assertTrue(ApiController.validHarness(Language.PYTHON, harness));
    assertTrue(db.queryForObject("select content from explanations where skill_code='PY_BASIC_CODE_READING'", String.class).contains("end=\"\""));
    assertEquals(0, db.queryForObject("select min(block_no) from skills where language='PYTHON'", Integer.class));
    assertEquals(8, db.queryForObject("select max(block_no) from skills where language='PYTHON'", Integer.class));
  }
}
