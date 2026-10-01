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
    // Diagnostic import stores codes as titles; give learners and the LLM readable topic names.
    SKILL_TITLES.forEach((code,title) -> db.update("update skills set title=? where code=? and title=code", title, code));
    db.update("update skills set title=? where code=? and title=?", "Вывод в консоль", "BASIC_CODE_READING", "BASIC_CODE_READING");
    db.update("insert or ignore into explanations(skill_code,content,source) values(?,?,?)", "BASIC_CODE_READING", SEED_EXPLANATION, "SEED");
    db.update("update explanations set content=? where skill_code=? and source='SEED'", SEED_EXPLANATION, "BASIC_CODE_READING");
  }
  private static final Map<String,String> SKILL_TITLES = Map.ofEntries(
    Map.entry("VARIABLE_BASIC","Переменные"), Map.entry("ASSIGNMENT","Присваивание"), Map.entry("ARITHMETIC_BASIC","Арифметика"),
    Map.entry("EXECUTION_FLOW_BASIC","Порядок выполнения"), Map.entry("PRIMITIVE_TYPES","Примитивные типы"), Map.entry("STRING_BASIC","Строки"),
    Map.entry("INTEGER_DIVISION","Целочисленное деление и остаток"), Map.entry("ASSIGNMENT_OPERATORS","Составное присваивание и инкремент"),
    Map.entry("IF_ELSE_BASIC","Условия if / else"), Map.entry("COMPARISON_OPERATORS","Операторы сравнения"), Map.entry("LOGICAL_AND","Логическое И (&&)"),
    Map.entry("LOGICAL_OR","Логическое ИЛИ (||)"), Map.entry("SWITCH_BASIC","Оператор switch"), Map.entry("FOR_LOOP_BASIC","Цикл for"),
    Map.entry("ACCUMULATOR_PATTERN","Накопление результата в цикле"), Map.entry("WHILE_LOOP_BASIC","Цикл while"), Map.entry("LOOP_TERMINATION","Завершение цикла"),
    Map.entry("ARRAY_INDEXING","Индексы массива"), Map.entry("ARRAY_BASIC","Массивы"), Map.entry("ARRAY_ITERATION","Перебор массива"),
    Map.entry("METHOD_BASIC","Методы"), Map.entry("METHOD_PARAMETERS","Параметры и возвращаемое значение"), Map.entry("CLASS_BASIC","Классы"),
    Map.entry("OBJECT_CREATION","Создание объектов"), Map.entry("CONSTRUCTOR_BASIC","Конструкторы"), Map.entry("THIS_BASIC","Ключевое слово this"),
    Map.entry("ENCAPSULATION_BASIC","Инкапсуляция"), Map.entry("GETTER_SETTER_BASIC","Геттеры и сеттеры"), Map.entry("STATIC_BASIC","static"),
    Map.entry("INHERITANCE_BASIC","Наследование"), Map.entry("METHOD_OVERRIDE","Переопределение методов"), Map.entry("POLYMORPHISM_BASIC","Полиморфизм"),
    Map.entry("INTERFACE_BASIC","Интерфейсы"), Map.entry("SUPER_BASIC","Ключевое слово super"), Map.entry("LIST_BASIC","Список List"),
    Map.entry("SET_BASIC","Множество Set"), Map.entry("MAP_BASIC","Словарь Map"), Map.entry("LIST_OPERATIONS","Операции со списком"),
    Map.entry("COLLECTION_SELECTION","Выбор коллекции"), Map.entry("TRY_CATCH_BASIC","Обработка исключений try / catch"), Map.entry("FINALLY_BASIC","Блок finally"),
    Map.entry("THROW_BASIC","Выброс исключения throw"), Map.entry("THROWS_BASIC","Объявление throws"));
  private static final String SEED_EXPLANATION = """
      ### Зачем это нужно

      Программа — это список команд для компьютера. Но пока программа ничего не показывает, мы не знаем, что она сделала. Вывод в консоль — это способ программы «сказать» нам результат: как если бы ты попросил друга не просто посчитать в уме, а произнести ответ вслух.

      Консоль — это текстовое окно, куда программа печатает строки. Именно её вывод проверяет система, когда ты отправляешь решение.

      ### Главная идея

      В Java печать в консоль выглядит так:

      ```java
      System.out.println("Привет");
      ```

      Разберём по частям:

      - `System.out` — «стандартный вывод», то есть консоль. Пока просто запомни это как имя места, куда пишем.
      - `.println(...)` — команда «напечатай и перейди на новую строку» (`ln` — от английского *line*, строка).
      - `"Привет"` — то, что печатаем. Текст всегда пишется в **двойных кавычках**; сами кавычки на экран не выводятся.
      - `;` — точка с запятой завершает команду, как точка в конце предложения.

      Есть вторая команда — `System.out.print(...)` (без `ln`). Она печатает значение, но **не** переходит на новую строку: следующий вывод продолжится сразу за ним.

      ### Разбираем по шагам

      **Пример 1. Одна строка.**

      ```java
      System.out.println("Привет");
      ```

      Java печатает текст между кавычками и переводит курсор на следующую строку. Вывод:

      ```text
      Привет
      ```

      **Пример 2. print и println вместе.** Команды выполняются строго сверху вниз, по очереди.

      ```java
      System.out.print("Раз");
      System.out.print("Два");
      System.out.println("!");
      System.out.println("Три");
      ```

      1. `print("Раз")` печатает «Раз» и остаётся на той же строке.
      2. `print("Два")` дописывает «Два» сразу вплотную — без пробела, потому что пробел мы не просили.
      3. `println("!")` дописывает «!» и переходит на новую строку.
      4. `println("Три")` печатает «Три» уже на новой строке.

      ```text
      РазДва!
      Три
      ```

      **Пример 3. Не только текст.** Числа и логические значения (`true` / `false`) пишутся без кавычек, а один символ — в **одинарных** кавычках:

      ```java
      System.out.println(7);
      System.out.println('A');
      System.out.println(true);
      System.out.println();
      System.out.print("конец");
      ```

      `println()` без ничего внутри печатает пустую строку — просто переход на новую строку. Вывод:

      ```text
      7
      A
      true

      конец
      ```

      ### Частые ошибки

      - **Забыли кавычки у текста:** `System.out.println(Привет);` — Java решит, что `Привет` это имя чего-то в программе, и выдаст ошибку компиляции `cannot find symbol`.
      - **Перепутали print и println:** если в задаче сказано «без переноса строки», а ты написал `println`, в конце появится лишний перевод строки — и проверка не пройдёт, хотя на глаз текст тот же.
      - **Лишний или пропущенный пробел:** `print("3")` и затем `print("кота")` дадут `3кота`. Пробел — такой же символ, его нужно напечатать явно: `print(" кота")`.
      - **Пропущена `;` или большая буква:** `system.out.println` (с маленькой `s`) не сработает — Java различает большие и маленькие буквы.

      ### Как это пригодится в задачах

      В задачах ты увидишь заготовку класса `Solution` с методом `main` — это точка, с которой Java начинает выполнять программу. Свои команды вывода пиши внутри фигурных скобок `main`, на месте комментария. Проверка сравнивает вывод **символ в символ**, поэтому внимательно смотри, где в условии нужен перевод строки, а где нет.

      ### Проверь себя

      1. Что выведет `System.out.print("a"); System.out.print("b");`?
      2. Как напечатать символ `X`, чтобы после него курсор перешёл на новую строку?

      **Ответы.** 1) `ab` — оба `print` пишут в одну строку вплотную. 2) `System.out.println('X');` — одинарные кавычки для символа и `println` для перехода строки.

      ### Коротко

      - `System.out.println(...)` печатает и переходит на новую строку, `System.out.print(...)` — печатает и остаётся на строке.
      - Текст — в двойных кавычках, символ — в одинарных, числа и `true` / `false` — без кавычек.
      - Команды выполняются сверху вниз.
      - Пробелы и переводы строк — тоже часть вывода, их нужно печатать явно.
      """.strip();
  private void seedTasks() {
    retireLegacyReadingTasks();
    // Three tasks per difficulty step so each of the three iterations can go easy → medium → harder.
    addOutputTask("Консоль: приветствие", 1, "Напечатай в консоль слово «Привет» без переноса строки.", "Привет");
    addOutputTask("Консоль: число", 1, "Напечатай число 7 и заверши строку переводом строки.", "7\n");
    addOutputTask("Консоль: символ", 1, "Напечатай символ A без перевода строки.", "A");
    addOutputTask("Консоль: две строки", 2, "Напечатай «Раз» и «Два» на двух разных строках.", "Раз\nДва\n");
    addOutputTask("Консоль: логическое значение", 2, "Напечатай логическое значение true и заверши строку переводом строки.", "true\n");
    addOutputTask("Консоль: знак Java", 2, "Напечатай Java и сразу после него восклицательный знак, без пробела и переноса строки.", "Java!");
    addOutputTask("Консоль: пустая строка", 3, "Сначала напечатай пустую строку, затем на следующей строке напечатай «готово» без переноса после него.", "\nготово");
    addOutputTask("Консоль: кота", 3, "Напечатай 3, затем пробел и слово «кота», после чего перейди на новую строку.", "3 кота\n");
    addOutputTask("Консоль: три значения", 3, "Напечатай подряд символ X, затем Y с переводом строки, затем false без перевода после него.", "XY\nfalse");
  }
  private void retireLegacyReadingTasks() {
    for(String title:List.of("Вывод строки","Две строки","Число","Символ","Логическое значение","Склеенный вывод","Пустая строка","Число и текст","Три вывода"))
      db.update("update tasks set active=0 where title=? and test_source like '%Solution.answer()%'", title);
    db.update("update tasks set active=0 where skill_code='BASIC_CODE_READING' and test_source like '%Solution.answer()%' and (statement like '%Что выведет%' or statement like '%предскажи вывод%' or statement like '%предсказать вывод%')");
  }
  private void addOutputTask(String title,int difficulty,String action,String expected) { String statement=action+"\n\nДополни тело `Solution.main(String[] args)`. Используй `System.out.print` или `System.out.println`.\n\n**Должно получиться в консоли:**\n\n```text\n"+expected.stripTrailing()+"\n```\n\nПроверка сравнивает вывод символ в символ, включая пробелы и переводы строк — перечитай в условии, нужен ли перевод строки в конце.";String starter="""
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
      """.formatted(javaLiteral(expected)); addTask(title,difficulty,statement,starter,test); }
  private String javaLiteral(String value) { return value.replace("\\","\\\\").replace("\n","\\n").replace("\"","\\\""); }
  private void addTask(String title,int difficulty,String statement,String starter,String test) { var existing=db.queryForList("select id from tasks where title=?",title);if(!existing.isEmpty()){long id=((Number)existing.getFirst().get("id")).longValue();db.update("update tasks set skill_code=?,statement=?,starter_code=?,test_source=?,test_file_name=?,difficulty=?,active=1 where id=?","BASIC_CODE_READING",statement,starter,test,"TestHarness.java",difficulty,id);db.update("insert or ignore into task_target_skills(task_id,skill_code) values(?,?)",id,"BASIC_CODE_READING");return;} db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,difficulty) values(?,?,?,?,?,?,?)","BASIC_CODE_READING",title,statement,starter,test,"TestHarness.java",difficulty); db.update("insert into task_target_skills(task_id,skill_code) values(last_insert_rowid(),?)", "BASIC_CODE_READING"); }
}
