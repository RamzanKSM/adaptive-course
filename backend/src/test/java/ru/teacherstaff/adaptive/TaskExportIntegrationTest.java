package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.time.LocalDate;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class TaskExportIntegrationTest {
  @Autowired MockMvc mvc; @Autowired JdbcTemplate db; @Autowired ObjectMapper json;
  @DynamicPropertySource static void properties(DynamicPropertyRegistry p) {
    p.add("spring.datasource.url", () -> "jdbc:sqlite:file:export-" + UUID.randomUUID() + "?mode=memory&cache=shared");
    p.add("app.diagnostic.source", () -> Path.of("..", "java_initial_diagnostic_mvp_v2.md").toAbsolutePath().toString());
    p.add("app.bootstrap-admin-login", () -> "admin");
    p.add("app.bootstrap-admin-password", () -> "admin-pass");
    p.add("app.task-audit.enabled", () -> "false");
  }
  @BeforeEach void prepare() { db.update("update users set password_hash=? where login='admin'", new BCryptPasswordEncoder().encode("admin-pass")); }

  @Test void adminDownloadsExcelFriendlyCsvWithBomHeaderAndFilename() throws Exception {
    var response = mvc.perform(get("/api/admin/tasks/export").param("language", "JAVA").cookie(cookie(login("admin", "admin-pass"))))
      .andExpect(status().isOk()).andReturn().getResponse();
    assertTrue(response.getContentType().startsWith("text/csv"), response.getContentType());
    assertTrue(response.getContentType().toLowerCase(Locale.ROOT).contains("charset=utf-8"), response.getContentType());
    assertEquals("attachment; filename=\"rmzn-tasks-java-" + LocalDate.now() + ".csv\"", response.getHeader("Content-Disposition"));
    byte[] body = response.getContentAsByteArray();
    assertArrayEquals(new byte[]{(byte) 0xEF, (byte) 0xBB, (byte) 0xBF}, Arrays.copyOf(body, 3), "UTF-8 BOM so Excel reads Cyrillic");
    String text = new String(body, 3, body.length - 3, StandardCharsets.UTF_8);
    assertTrue(text.startsWith(String.join(";", TaskExportController.HEADER) + "\r\n"));
    var rows = parse(text);
    for (var row : rows) assertEquals(TaskExportController.HEADER.size(), row.size(), "every row has every column: " + row);
    assertTrue(rows.stream().skip(1).allMatch(row -> "Java".equals(row.get(0))), "only the Java course was asked for");

    // Every Java topic is in the file, including topics without tasks (a gap shows as a row with empty task columns).
    var codes = new HashSet<String>(); rows.stream().skip(1).forEach(row -> codes.add(row.get(2)));
    assertEquals(new HashSet<>(db.queryForList("select code from skills where language='JAVA'", String.class)), codes);
    var empty = db.queryForList("select code from skills s where language='JAVA' and not exists(select 1 from tasks t where t.skill_code=s.code) order by sort_order limit 1", String.class);
    if (!empty.isEmpty()) assertTrue(rows.stream().anyMatch(row -> empty.getFirst().equals(row.get(2)) && row.get(5).isEmpty()));
    // Topic numbers follow sort_order, starting at 1.
    assertEquals("1", rows.get(1).get(1));

    var all = mvc.perform(get("/api/admin/tasks/export").cookie(cookie(login("admin", "admin-pass")))).andExpect(status().isOk()).andReturn().getResponse();
    assertEquals("attachment; filename=\"rmzn-tasks-all-" + LocalDate.now() + ".csv\"", all.getHeader("Content-Disposition"));
  }

  @Test void studentsAndAnonymousCannotDownload() throws Exception {
    String admin = login("admin", "admin-pass");
    mvc.perform(post("/api/admin/students").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON)
      .content(json.writeValueAsString(Map.of("login", "export-student", "password", "student-pass", "displayName", "export-student")))).andExpect(status().isOk());
    mvc.perform(get("/api/admin/tasks/export").cookie(cookie(login("export-student", "student-pass")))).andExpect(status().isForbidden());
    mvc.perform(get("/api/admin/tasks/export")).andExpect(status().isUnauthorized());
  }

  @Test void earlyMethodIsFlaggedAndMultiLineFieldsRoundTrip() throws Exception {
    String statement = "Посчитай сумму; выведи \"итог\".\nВторая строка;\r\nтретья";
    String starter = "public class Solution {\n    static int total(int a, int b) {\n        return a + b;\n    }\n    public static void main(String[] args) {\n        System.out.println(total(2, 3));\n    }\n}\n";
    long normal = addTask("VARIABLE_BASIC", "NORMAL", statement, starter);
    long hard = addTask("VARIABLE_BASIC", "HARD", "Сложная", starter);
    long plain = addTask("VARIABLE_BASIC", "NORMAL", "Простая", "public class Solution {\n    public static void main(String[] args) {\n        int x = 1;\n    }\n}\n");
    db.update("update tasks set difficulty=2, source='TEST', goal_json=? where id=?", "{\"kind\":\"OUTPUT_BEHAVIOR\",\"requiredConstructs\":[\"if\",\"for\"]}", normal);

    // Statistics: one student got the task, failed once, then solved it; a revoked attempt does not count.
    String admin = login("admin", "admin-pass");
    mvc.perform(post("/api/admin/students").cookie(cookie(admin)).contentType(MediaType.APPLICATION_JSON)
      .content(json.writeValueAsString(Map.of("login", "stats-student", "password", "student-pass", "displayName", "stats-student")))).andExpect(status().isOk());
    long student = db.queryForObject("select id from users where login='stats-student'", Long.class);
    db.update("insert into lessons(user_id,lesson_number,language,language_lesson_number) values(?,1,'JAVA',1)", student);
    long lesson = db.queryForObject("select last_insert_rowid()", Long.class);
    db.update("insert into lesson_tasks(lesson_id,task_id) values(?,?)", lesson, normal);
    db.update("insert into submissions(lesson_id,task_id,source_code,passed,runner_output) values(?,?,'x',0,'')", lesson, normal);
    db.update("insert into submissions(lesson_id,task_id,source_code,passed,runner_output) values(?,?,'x',1,'')", lesson, normal);
    db.update("insert into submissions(lesson_id,task_id,source_code,passed,runner_output,revoked_at) values(?,?,'x',1,'','2026-01-01')", lesson, normal);

    byte[] body = mvc.perform(get("/api/admin/tasks/export").param("language", "java").cookie(cookie(admin))).andExpect(status().isOk()).andReturn().getResponse().getContentAsByteArray();
    var rows = parse(new String(body, 3, body.length - 3, StandardCharsets.UTF_8));
    var header = rows.getFirst();
    var row = rowFor(rows, normal);
    assertEquals(statement, row.get(header.indexOf("Условие")), "quotes, separators and line breaks survive");
    assertEquals(starter, row.get(header.indexOf("Заготовка")));
    assertEquals("VARIABLE_BASIC", row.get(header.indexOf("Код темы")));
    assertEquals("2", row.get(header.indexOf("Ступень")));
    assertEquals("обычная", row.get(header.indexOf("Режим")));
    assertEquals("да", row.get(header.indexOf("Активна")));
    assertEquals("TEST", row.get(header.indexOf("Источник")));
    assertEquals("OUTPUT_BEHAVIOR", row.get(header.indexOf("Тип проверки")));
    assertEquals("if, for", row.get(header.indexOf("Требуемые конструкции")));
    String used = row.get(header.indexOf("Конструкции в задаче"));
    assertTrue(used.contains("собственные методы (функции)") && used.contains("условия") && used.contains("цикл for"), used);
    String early = row.get(header.indexOf("Раньше своей темы"));
    assertTrue(early.contains("собственные методы (функции) — тема METHOD_BASIC"), early);
    assertEquals("1", row.get(header.indexOf("Выдана студентам")));
    assertEquals("1", row.get(header.indexOf("Решили")));
    assertEquals("2", row.get(header.indexOf("Попыток")));

    var hardRow = rowFor(rows, hard);
    assertEquals("hard", hardRow.get(header.indexOf("Режим")));
    assertEquals("", hardRow.get(header.indexOf("Раньше своей темы")), "hard mode is for students who finished the course");
    assertTrue(hardRow.get(header.indexOf("Конструкции в задаче")).contains("собственные методы (функции)"));
    assertEquals("", rowFor(rows, plain).get(header.indexOf("Раньше своей темы")));
    assertTrue(rows.indexOf(rowFor(rows, plain)) < rows.indexOf(hardRow), "NORMAL tasks of a topic come before its HARD tasks");
  }

  private long addTask(String skill, String mode, String statement, String starter) {
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,mode,language) values(?,?,?,?,'class TestHarness {}','TestHarness.java',?,'JAVA')", skill, "export " + mode, statement, starter, mode);
    long id = db.queryForObject("select last_insert_rowid()", Long.class);
    db.update("insert into task_target_skills(task_id,skill_code) values(?,?)", id, skill);
    return id;
  }

  private static List<String> rowFor(List<List<String>> rows, long taskId) {
    return rows.stream().filter(row -> String.valueOf(taskId).equals(row.get(5))).findFirst().orElseThrow(() -> new AssertionError("no row for task " + taskId));
  }

  /** A strict RFC 4180 reader («;», CRLF rows) to check that the file reads back exactly. */
  private static List<List<String>> parse(String text) {
    List<List<String>> rows = new ArrayList<>(); List<String> row = new ArrayList<>(); StringBuilder cell = new StringBuilder();
    int i = 0; boolean quoted = false;
    while (i < text.length()) {
      char c = text.charAt(i);
      if (quoted) {
        if (c == '"' && i + 1 < text.length() && text.charAt(i + 1) == '"') { cell.append('"'); i += 2; continue; }
        if (c == '"') { quoted = false; i++; continue; }
        cell.append(c); i++; continue;
      }
      if (c == '"' && cell.isEmpty()) { quoted = true; i++; }
      else if (c == ';') { row.add(cell.toString()); cell.setLength(0); i++; }
      else if (c == '\r' && i + 1 < text.length() && text.charAt(i + 1) == '\n') { row.add(cell.toString()); cell.setLength(0); rows.add(row); row = new ArrayList<>(); i += 2; }
      else { assertNotEquals('\n', c, "bare LF outside quotes"); cell.append(c); i++; }
    }
    assertTrue(row.isEmpty() && cell.isEmpty(), "the file ends with CRLF");
    return rows;
  }

  private String login(String login, String password) throws Exception {
    var r = mvc.perform(post("/api/auth/login").contentType(MediaType.APPLICATION_JSON).content(json.writeValueAsString(Map.of("login", login, "password", password))))
      .andExpect(status().isOk()).andReturn().getResponse();
    return r.getCookie("adaptive_session").getValue();
  }
  private static jakarta.servlet.http.Cookie cookie(String value) { return new jakarta.servlet.http.Cookie("adaptive_session", value); }
}
