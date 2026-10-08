package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

/**
 * The teacher's CSV of every topic and task (with the constructs each task needs and whether it comes before the topic
 * that teaches them), meant to be handed to an assistant to review the order of topics and tasks. Russian Excel
 * dialect: UTF-8 with BOM, «;» separator, RFC 4180 quoting, CRLF row ends.
 */
@RestController @RequestMapping("/api/admin/tasks")
public class TaskExportController {
  static final List<String> HEADER = List.of("Язык", "№ темы", "Код темы", "Тема", "Блок", "ID задачи", "Ступень", "Режим", "Активна",
    "Источник", "Тип проверки", "Требуемые конструкции", "Название", "Условие", "Заготовка", "Конструкции в задаче", "Раньше своей темы",
    "Выдана студентам", "Решили", "Попыток");

  private final JdbcTemplate db; private final ObjectMapper json;
  public TaskExportController(JdbcTemplate db, ObjectMapper json) { this.db = db; this.json = json; }

  @GetMapping("/export")
  public ResponseEntity<?> export(@RequestParam(defaultValue = "ALL") String language, HttpServletRequest r) {
    if (!isAdmin(r)) return ResponseEntity.status(HttpStatus.FORBIDDEN).body(Map.of("error", "FORBIDDEN", "message", "Нужна роль ADMIN"));
    Language only = "ALL".equalsIgnoreCase(language.trim()) ? null : Language.parse(language);
    StringBuilder csv = new StringBuilder("﻿");
    row(csv, HEADER);
    for (var t : rows(only)) row(csv, line(t));
    String name = "rmzn-tasks-" + (only == null ? "all" : only.name().toLowerCase(Locale.ROOT)) + "-" + LocalDate.now() + ".csv";
    return ResponseEntity.ok()
      .contentType(new MediaType("text", "csv", StandardCharsets.UTF_8))
      .header(HttpHeaders.CONTENT_DISPOSITION, ContentDisposition.attachment().filename(name).build().toString())
      .body(csv.toString().getBytes(StandardCharsets.UTF_8));
  }

  @SuppressWarnings("unchecked")
  private static boolean isAdmin(HttpServletRequest r) {
    var user = (Map<String, Object>) r.getAttribute("user");
    return user != null && "ADMIN".equals(user.get("role"));
  }

  /** Every topic with its tasks; a topic without tasks is one row with the task columns empty. */
  private List<Map<String, Object>> rows(Language only) {
    String sql = """
      with ranked as (
        select code, title, sort_order, block_no, language, row_number() over (partition by language order by sort_order, id) as topic_no from skills
      ), given as (
        select lt.task_id, count(distinct l.user_id) as n from lesson_tasks lt join lessons l on l.id = lt.lesson_id group by lt.task_id
      ), solved as (
        select x.task_id, count(distinct l.user_id) as n from submissions x join lessons l on l.id = x.lesson_id
        where x.passed = 1 and x.revoked_at is null group by x.task_id
      ), tries as (
        select task_id, count(*) as n from submissions where revoked_at is null group by task_id
      )
      select s.language, s.topic_no, s.code as skill_code, s.title as skill_title, s.block_no,
             t.id as task_id, t.difficulty, t.mode, t.active, t.source, t.goal_json, t.title, t.statement, t.starter_code, t.test_source,
             coalesce(g.n, 0) as given, coalesce(v.n, 0) as solved, coalesce(a.n, 0) as tries
      from ranked s
      left join tasks t on t.skill_code = s.code
      left join given g on g.task_id = t.id
      left join solved v on v.task_id = t.id
      left join tries a on a.task_id = t.id
      """ + (only == null ? "" : " where s.language = ?") + """

      order by s.language, s.sort_order, s.code, case t.mode when 'HARD' then 1 else 0 end, t.difficulty is null, t.difficulty, t.id
      """;
    return only == null ? db.queryForList(sql) : db.queryForList(sql, only.name());
  }

  private List<String> line(Map<String, Object> t) {
    Language lang = Language.of(t.get("language"));
    List<String> cells = new ArrayList<>(List.of(lang.title, str(t.get("topic_no")), str(t.get("skill_code")), str(t.get("skill_title")), str(t.get("block_no"))));
    if (t.get("task_id") == null) { while (cells.size() < HEADER.size()) cells.add(""); return cells; }
    JsonNode goal = goal(t.get("goal_json"));
    boolean hard = "HARD".equals(t.get("mode"));
    String starter = str(t.get("starter_code"));
    Set<CourseConstructs.Construct> constructs = EnumSet.noneOf(CourseConstructs.Construct.class);
    constructs.addAll(CourseConstructs.used(lang, starter));
    constructs.addAll(CourseConstructs.required(goal));
    if (CourseConstructs.checksCallMethods(lang, str(t.get("test_source")))) constructs.add(CourseConstructs.Construct.METHOD);
    String early = hard ? "" : CourseConstructs.describe(lang, CourseConstructs.notYetTaught(db, lang, str(t.get("skill_code")), constructs));
    String required = goal == null ? "" : stream(goal.path("requiredConstructs")).collect(Collectors.joining(", "));
    cells.addAll(List.of(
      str(t.get("task_id")), str(t.get("difficulty")), hard ? "hard" : "обычная", isTrue(t.get("active")) ? "да" : "нет",
      str(t.get("source")), goal == null ? "" : goal.path("kind").asText(""), required,
      str(t.get("title")), str(t.get("statement")), starter,
      constructs.stream().map(c -> c.title).collect(Collectors.joining(", ")), early,
      str(t.get("given")), str(t.get("solved")), str(t.get("tries"))));
    return cells;
  }

  private JsonNode goal(Object stored) {
    if (stored == null || stored.toString().isBlank()) return null;
    try { return json.readTree(stored.toString()); } catch (Exception e) { return null; }
  }

  private static java.util.stream.Stream<String> stream(JsonNode array) {
    List<String> out = new ArrayList<>(); for (JsonNode n : array) out.add(n.asText()); return out.stream();
  }

  private static boolean isTrue(Object v) { return v instanceof Number n ? n.intValue() != 0 : Boolean.TRUE.equals(v) || "1".equals(String.valueOf(v)); }
  private static String str(Object v) { return v == null ? "" : v.toString(); }

  static void row(StringBuilder out, List<String> cells) {
    for (int i = 0; i < cells.size(); i++) { if (i > 0) out.append(';'); out.append(quote(cells.get(i))); }
    out.append("\r\n");
  }

  /** RFC 4180: a field with the separator, a quote or a line break is quoted, quotes inside are doubled. */
  static String quote(String value) {
    if (value == null) return "";
    if (value.indexOf(';') < 0 && value.indexOf('"') < 0 && value.indexOf('\n') < 0 && value.indexOf('\r') < 0) return value;
    return '"' + value.replace("\"", "\"\"") + '"';
  }
}
