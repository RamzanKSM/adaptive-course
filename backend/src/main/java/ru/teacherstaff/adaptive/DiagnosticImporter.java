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
    db.update("update skills set title=? where code=? and title=?", "Вывод в консоль", "BASIC_CODE_READING", "BASIC_CODE_READING");
    String explanation="Java выполняет строки сверху вниз. System.out.print(...) выводит значение без перехода на новую строку, а System.out.println(...) после значения добавляет переход строки. Текст пишется в двойных кавычках, один символ — в одинарных. В этих задачах нужно дописать Solution.main(String[] args), чтобы программа напечатала требуемый текст.";
    db.update("insert or ignore into explanations(skill_code,content,source) values(?,?,?)", "BASIC_CODE_READING", explanation, "SEED");
    db.update("update explanations set content=? where skill_code=? and source='SEED'", explanation, "BASIC_CODE_READING");
  }
  private void seedTasks() {
    retireLegacyReadingTasks();
    addOutputTask("Консоль: приветствие", "Напечатай в консоль слово «Привет» без переноса строки.", "Привет");
    addOutputTask("Консоль: две строки", "Напечатай «Раз» и «Два» на двух разных строках.", "Раз\nДва\n");
    addOutputTask("Консоль: число", "Напечатай число 7 и заверши строку переводом строки.", "7\n");
    addOutputTask("Консоль: символ", "Напечатай символ A без перевода строки.", "A");
    addOutputTask("Консоль: логическое значение", "Напечатай логическое значение true и заверши строку переводом строки.", "true\n");
    addOutputTask("Консоль: знак Java", "Напечатай Java и сразу после него восклицательный знак, без пробела и переноса строки.", "Java!");
    addOutputTask("Консоль: пустая строка", "Сначала напечатай пустую строку, затем на следующей строке напечатай «готово» без переноса после него.", "\nготово");
    addOutputTask("Консоль: кота", "Напечатай 3, затем пробел и слово «кота», после чего перейди на новую строку.", "3 кота\n");
    addOutputTask("Консоль: три значения", "Напечатай подряд символ X, затем Y с переводом строки, затем false без перевода после него.", "XY\nfalse");
  }
  private void retireLegacyReadingTasks() {
    for(String title:List.of("Вывод строки","Две строки","Число","Символ","Логическое значение","Склеенный вывод","Пустая строка","Число и текст","Три вывода"))
      db.update("update tasks set active=0 where title=? and test_source like '%Solution.answer()%'", title);
    db.update("update tasks set active=0 where skill_code='BASIC_CODE_READING' and test_source like '%Solution.answer()%' and (statement like '%Что выведет%' or statement like '%предскажи вывод%' or statement like '%предсказать вывод%')");
  }
  private void addOutputTask(String title,String action,String expected) { String statement=action+"\n\nДополни тело `Solution.main(String[] args)`. Используй `System.out.print` или `System.out.println`.";String starter="""
      public class Solution {
          public static void main(String[] args) {

          }
      }
      """.strip();String test="""
      import java.io.ByteArrayOutputStream;
      import java.io.PrintStream;
      import java.nio.charset.StandardCharsets;
      public class TestHarness {
          public static void main(String[] args) throws Exception {
              PrintStream original = System.out;
              ByteArrayOutputStream captured = new ByteArrayOutputStream();
              try {
                  System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
                  Solution.main(new String[0]);
              } finally {
                  System.setOut(original);
              }
              String actual = captured.toString(StandardCharsets.UTF_8);
              if (!"%s".equals(actual)) throw new AssertionError("Неверный вывод");
              System.out.print("{{PASS_MARKER}}");
          }
      }
      """.formatted(javaLiteral(expected)); addTask(title,statement,starter,test); }
  private String javaLiteral(String value) { return value.replace("\\","\\\\").replace("\n","\\n").replace("\"","\\\""); }
  private void addTask(String title,String statement,String starter,String test) { var existing=db.queryForList("select id from tasks where title=?",title);if(!existing.isEmpty()){long id=((Number)existing.getFirst().get("id")).longValue();db.update("update tasks set skill_code=?,statement=?,starter_code=?,test_source=?,test_file_name=?,active=1 where id=?","BASIC_CODE_READING",statement,starter,test,"TestHarness.java",id);db.update("insert or ignore into task_target_skills(task_id,skill_code) values(?,?)",id,"BASIC_CODE_READING");return;} db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name) values(?,?,?,?,?,?)","BASIC_CODE_READING",title,statement,starter,test,"TestHarness.java"); db.update("insert into task_target_skills(task_id,skill_code) values(last_insert_rowid(),?)", "BASIC_CODE_READING"); }
}
