package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

@Component
class DiagnosticImporter implements ApplicationRunner {
  private final JdbcTemplate db; private final ObjectMapper json; private final String source;
  DiagnosticImporter(JdbcTemplate db, ObjectMapper json, @Value("${app.diagnostic.source}") String source) { this.db=db; this.json=json; this.source=source; }
  @Override public void run(org.springframework.boot.ApplicationArguments args) throws Exception {
    if (db.queryForObject("select count(*) from diagnostic_questions", Integer.class) == 0) {
      Path path=Path.of(source); if (!Files.isRegularFile(path)) { System.err.println("Diagnostic source not found: "+path.toAbsolutePath()); return; }
      String text=Files.readString(path); int block=-1, order=0, at=0;
      Pattern heading=Pattern.compile("(?m)^# Блок (\\d+).*$"), question=Pattern.compile("(?ms)^### (\\d+)\\. (.*?)\\n\\nA\\. (.*?)[ \\t]*\\nB\\. (.*?)[ \\t]*\\nC\\. (.*?)[ \\t]*\\nD\\. (.*?)\\n\\n\\*\\*Ответ:\\*\\* ([A-D])[ \\t]*\\n\\*\\*Навык:\\*\\* `([^`]+)`");
      Matcher m=question.matcher(text);
      while(m.find()) {
        Matcher h=heading.matcher(text.substring(at,m.start())); while(h.find()) block=Integer.parseInt(h.group(1)); at=m.start();
        String skill=m.group(8); db.update("insert or ignore into skills(code,title,sort_order,prerequisite_code,block_no) values(?,?,?,?,?)",skill,skill,++order,null,block);
        db.update("insert into diagnostic_questions(ordinal,skill_code,prompt,options_json,correct_option,block_no) values(?,?,?,?,?,?)",Integer.parseInt(m.group(1)),skill,m.group(2),json.writeValueAsString(List.of(m.group(3),m.group(4),m.group(5),m.group(6))),m.group(7).charAt(0)-'A',block);
      }
    }
    seedTasks();
    db.update("insert or ignore into explanations(skill_code,content,source) values(?,?,?)", "BASIC_CODE_READING", "Java выполняет строки сверху вниз. System.out.print(...) выводит значение без перехода на новую строку, а System.out.println(...) после значения добавляет переход строки. Текст пишется в двойных кавычках, один символ — в одинарных. В задачах класс и метод уже готовы: нужно только вернуть точную строку вывода; перевод строки записывается как \\n.", "SEED");
  }
  private void seedTasks() {
    addReadingTask("Вывод строки", "System.out.print(\"Привет\");", "Привет");
    addReadingTask("Две строки", "System.out.println(\"Раз\");\nSystem.out.println(\"Два\");", "Раз\nДва\n");
    addReadingTask("Число", "System.out.println(7);", "7\n");
    addReadingTask("Символ", "System.out.print('A');", "A");
    addReadingTask("Логическое значение", "System.out.println(true);", "true\n");
    addReadingTask("Склеенный вывод", "System.out.print(\"Java\");\nSystem.out.print(\"!\");", "Java!");
    addReadingTask("Пустая строка", "System.out.println(\"\");\nSystem.out.print(\"готово\");", "\nготово");
    addReadingTask("Число и текст", "System.out.print(3);\nSystem.out.println(\" кота\");", "3 кота\n");
    addReadingTask("Три вывода", "System.out.print('X');\nSystem.out.println(\"Y\");\nSystem.out.print(false);", "XY\nfalse");
  }
  private void addReadingTask(String title,String snippet,String expected) { String statement="Что выведет этот код?\n\n```java\n"+snippet+"\n```\n\nВ готовом `Solution.answer()` впиши точный вывод одной строкой. Для перевода строки используй `\\n`.";String starter="public class Solution { public static String answer() { return \"\"; } }";String test="public class TestHarness { public static void main(String[] args) { if (!\""+javaLiteral(expected)+"\".equals(Solution.answer())) throw new AssertionError(); System.out.println(\"{{PASS_MARKER}}\"); } }"; addTask(title,statement,starter,test); }
  private String javaLiteral(String value) { return value.replace("\\","\\\\").replace("\n","\\n").replace("\"","\\\""); }
  private void addTask(String title,String statement,String starter,String test) { var existing=db.queryForList("select id from tasks where title=?",title);if(!existing.isEmpty()){long id=((Number)existing.getFirst().get("id")).longValue();db.update("update tasks set skill_code=?,statement=?,starter_code=?,test_source=?,test_file_name=?,active=1 where id=?","BASIC_CODE_READING",statement,starter,test,"TestHarness.java",id);db.update("insert or ignore into task_target_skills(task_id,skill_code) values(?,?)",id,"BASIC_CODE_READING");return;} db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name) values(?,?,?,?,?,?)","BASIC_CODE_READING",title,statement,starter,test,"TestHarness.java"); db.update("insert into task_target_skills(task_id,skill_code) values(last_insert_rowid(),?)", "BASIC_CODE_READING"); }
}
