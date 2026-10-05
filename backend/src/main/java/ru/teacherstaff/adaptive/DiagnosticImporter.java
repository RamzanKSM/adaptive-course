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
  private final JdbcTemplate db; private final ObjectMapper json; private final String source; private final String pythonSource;
  @org.springframework.beans.factory.annotation.Autowired DiagnosticImporter(JdbcTemplate db, ObjectMapper json, @Value("${app.diagnostic.source}") String source, @Value("${app.diagnostic.python-source:../python_initial_diagnostic_mvp.md}") String pythonSource) { this.db=db; this.json=json; this.source=source; this.pythonSource=pythonSource; }
  DiagnosticImporter(JdbcTemplate db, ObjectMapper json, String source) { this(db, json, source, "missing-python-diagnostic.md"); }
  @Override public void run(org.springframework.boot.ApplicationArguments args) throws Exception {
    importDiagnostic(Language.JAVA, source, 0);
    // diagnostic_questions.ordinal is globally UNIQUE, so Python questions are stored as 1000 + their number in the file.
    importDiagnostic(Language.PYTHON, pythonSource, 1000);
    seedTasks();
    seedPythonTasks();
    // Diagnostic import stores codes as titles; give learners and the LLM readable topic names.
    SKILL_TITLES.forEach((code,title) -> db.update("update skills set title=? where code=? and title=code", title, code));
    PYTHON_SKILL_TITLES.forEach((code,title) -> db.update("update skills set title=? where code=? and title=code", title, code));
    db.update("update skills set title=? where code=? and title=?", "Вывод в консоль", "BASIC_CODE_READING", "BASIC_CODE_READING");
    seedExplanation("BASIC_CODE_READING", SEED_EXPLANATION);
    seedExplanation("PY_BASIC_CODE_READING", PYTHON_SEED_EXPLANATION);
  }
  private void importDiagnostic(Language language, String file, int ordinalOffset) throws Exception {
    if (db.queryForObject("select count(*) from diagnostic_questions where language=?", Integer.class, language.name()) > 0) return;
    Path path=Path.of(file); if (!Files.isRegularFile(path)) { System.err.println(language.title+" diagnostic source not found: "+path.toAbsolutePath()); return; }
    String text=Files.readString(path); int block=-1, order=0, at=0;
    Pattern heading=Pattern.compile("(?m)^# Блок (\\d+).*$"), question=Pattern.compile("(?ms)^### (\\d+)\\. (.*?)\\n\\nA\\. (.*?)[ \\t]*\\nB\\. (.*?)[ \\t]*\\nC\\. (.*?)[ \\t]*\\nD\\. (.*?)\\n\\n\\*\\*Ответ:\\*\\* ([A-D])[ \\t]*\\n\\*\\*Навык:\\*\\* `([^`]+)`");
    Matcher m=question.matcher(text);
    while(m.find()) {
      Matcher h=heading.matcher(text.substring(at,m.start())); while(h.find()) block=Integer.parseInt(h.group(1)); at=m.start();
      String skill=m.group(8); db.update("insert or ignore into skills(code,title,sort_order,prerequisite_code,block_no,language) values(?,?,?,?,?,?)",skill,skill,++order,null,block,language.name());
      db.update("insert into diagnostic_questions(ordinal,skill_code,prompt,options_json,correct_option,block_no,language) values(?,?,?,?,?,?,?)",ordinalOffset+Integer.parseInt(m.group(1)),skill,m.group(2),json.writeValueAsString(List.of(m.group(3),m.group(4),m.group(5),m.group(6))),m.group(7).charAt(0)-'A',block,language.name());
    }
  }
  private void seedExplanation(String skill, String content) {
    if (db.queryForObject("select count(*) from skills where code=?", Integer.class, skill) == 0) return;
    db.update("insert or ignore into explanations(skill_code,content,source) values(?,?,?)", skill, content, "SEED");
    db.update("update explanations set content=? where skill_code=? and source='SEED'", content, skill);
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
  private static final Map<String,String> PYTHON_SKILL_TITLES = Map.ofEntries(
    Map.entry("PY_BASIC_CODE_READING","Вывод с print"), Map.entry("PY_VARIABLE_BASIC","Переменные"), Map.entry("PY_ASSIGNMENT","Присваивание"),
    Map.entry("PY_ARITHMETIC_BASIC","Арифметика"), Map.entry("PY_EXECUTION_FLOW_BASIC","Порядок выполнения"), Map.entry("PY_NUMBER_TYPES","Числа: int и float"),
    Map.entry("PY_STRING_BASIC","Строки"), Map.entry("PY_TYPE_CONVERSION","Преобразование типов"), Map.entry("PY_INTEGER_DIVISION","Деление // и остаток %"),
    Map.entry("PY_ASSIGNMENT_OPERATORS","Составное присваивание += -="), Map.entry("PY_FSTRINGS","f-строки"), Map.entry("PY_IF_ELSE_BASIC","Условия if / else"),
    Map.entry("PY_COMPARISON_OPERATORS","Операторы сравнения"), Map.entry("PY_LOGICAL_AND","Логическое and"), Map.entry("PY_LOGICAL_OR","Логическое or и not"),
    Map.entry("PY_ELIF","Цепочки elif"), Map.entry("PY_TRUTHINESS","Истинность значений"), Map.entry("PY_FOR_RANGE","Цикл for и range"),
    Map.entry("PY_ACCUMULATOR_PATTERN","Накопление результата в цикле"), Map.entry("PY_WHILE_LOOP_BASIC","Цикл while"), Map.entry("PY_LOOP_CONTROL","break и continue"),
    Map.entry("PY_LOOP_TERMINATION","Завершение цикла"), Map.entry("PY_LIST_INDEXING","Индексы списка"), Map.entry("PY_LIST_BASIC","Списки"),
    Map.entry("PY_LIST_ITERATION","Перебор списка"), Map.entry("PY_STRING_SLICING","Срезы строк"), Map.entry("PY_STRING_METHODS","Методы строк"),
    Map.entry("PY_FUNCTION_BASIC","Функции"), Map.entry("PY_FUNCTION_RETURN","return и print"), Map.entry("PY_FUNCTION_PARAMETERS","Параметры функций"),
    Map.entry("PY_CLASS_BASIC","Классы"), Map.entry("PY_OBJECT_CREATION","Создание объектов"), Map.entry("PY_INIT_METHOD","Метод __init__"),
    Map.entry("PY_SELF_BASIC","self и методы"), Map.entry("PY_ENCAPSULATION_BASIC","Инкапсуляция"), Map.entry("PY_PROPERTY_BASIC","Свойства @property"),
    Map.entry("PY_CLASS_ATTRIBUTES","Атрибуты класса"), Map.entry("PY_INHERITANCE_BASIC","Наследование"), Map.entry("PY_METHOD_OVERRIDE","Переопределение методов"),
    Map.entry("PY_POLYMORPHISM_BASIC","Полиморфизм"), Map.entry("PY_SUPER_BASIC","super()"), Map.entry("PY_DUCK_TYPING","Утиная типизация"),
    Map.entry("PY_LIST_OPERATIONS","Операции со списком"), Map.entry("PY_TUPLE_BASIC","Кортежи"), Map.entry("PY_SET_BASIC","Множества set"),
    Map.entry("PY_DICT_BASIC","Словари dict"), Map.entry("PY_COLLECTION_SELECTION","Выбор коллекции"), Map.entry("PY_COMPREHENSIONS","Генераторы списков"),
    Map.entry("PY_TRY_EXCEPT_BASIC","Обработка ошибок try / except"), Map.entry("PY_EXCEPTION_TYPES","Типы исключений"), Map.entry("PY_FINALLY_BASIC","Блок finally"),
    Map.entry("PY_RAISE_BASIC","Выброс исключения raise"));
  private static final String PYTHON_SEED_EXPLANATION = """
      ### Зачем это нужно

      Программа — это список команд для компьютера. Пока программа ничего не показывает, мы не знаем, что она сделала. Вывод в консоль — способ программы «сказать» нам результат, как если бы ты попросил друга не просто посчитать в уме, а произнести ответ вслух.

      Консоль — это текстовое окно, куда программа печатает строки. Именно её вывод проверяет система, когда ты отправляешь решение.

      ### Главная идея

      В Python печать в консоль — одна короткая команда:

      ```python
      print("Привет")
      ```

      Разберём по частям:

      - `print` — встроенная функция «напечатай». Python знает её с самого начала, ничего подключать не нужно.
      - `( ... )` — в круглых скобках передаём то, что нужно напечатать.
      - `"Привет"` — текст, или **строка**. Строку пишут в кавычках: двойных `"..."` или одинарных `'...'` — это одно и то же. Сами кавычки на экран не выводятся.

      После печати `print` сам переходит на новую строку. Если это не нужно, укажи, чем закончить вывод: `print("Привет", end="")` — тогда следующий вывод продолжится вплотную.

      ### Разбираем по шагам

      **Пример 1. Одна строка.**

      ```python
      print("Привет")
      ```

      Python печатает текст между кавычками и переходит на новую строку. Вывод:

      ```text
      Привет
      ```

      **Пример 2. Управляем концом строки.** Команды выполняются строго сверху вниз, по очереди.

      ```python
      print("Раз", end="")
      print("Два", end="")
      print("!")
      print("Три")
      ```

      1. `print("Раз", end="")` печатает «Раз» и остаётся на той же строке.
      2. `print("Два", end="")` дописывает «Два» вплотную — без пробела, потому что пробел мы не просили.
      3. `print("!")` дописывает «!» и, как обычно, переходит на новую строку.
      4. `print("Три")` печатает «Три» уже на новой строке.

      ```text
      РазДва!
      Три
      ```

      **Пример 3. Не только текст.** Числа и логические значения `True` / `False` пишутся без кавычек. В один `print` можно передать несколько значений через запятую — Python поставит между ними пробел:

      ```python
      print(7)
      print(True)
      print(3, "кота")
      print()
      print("конец", end="")
      ```

      `print()` без ничего внутри печатает пустую строку — просто переход на новую строку. Вывод:

      ```text
      7
      True
      3 кота

      конец
      ```

      ### Частые ошибки

      - **Забыли кавычки у текста:** `print(Привет)` — Python решит, что `Привет` это имя переменной, и выдаст `NameError: name 'Привет' is not defined`.
      - **Лишний перевод строки:** если в задаче сказано «без перевода строки», а ты написал просто `print("A")`, в конце появится `\\n` — и проверка не пройдёт, хотя на глаз текст тот же. Нужен `print("A", end="")`.
      - **Склеили без пробела:** `print("3", "кота", sep="")` даст `3кота`. По умолчанию разделитель — пробел, а `sep=""` его убирает.
      - **Большая буква и отступ:** `Print("A")` не сработает — Python различает большие и маленькие буквы. А пробелы в начале строки (отступ) без причины дадут `IndentationError`.

      ### Как это пригодится в задачах

      В задачах ты пишешь код в файле `solution.py`. На этой теме это просто одна или несколько строк с `print` — без функций и классов, прямо с начала файла. Проверка сравнивает вывод **символ в символ**, поэтому внимательно смотри, где в условии нужен перевод строки, а где нет.

      ### Проверь себя

      1. Что выведет `print("a", end="")` и следом `print("b")`?
      2. Как напечатать `X` так, чтобы после него курсор **не** переходил на новую строку?

      **Ответы.** 1) `ab` и перевод строки: первый `print` не переходит на новую строку, второй — переходит. 2) `print("X", end="")`.

      ### Коротко

      - `print(...)` печатает значение и переходит на новую строку; `end=""` убирает этот переход.
      - Текст — в кавычках, числа и `True` / `False` — без кавычек.
      - Несколько значений через запятую печатаются через пробел.
      - Команды выполняются сверху вниз; пробелы и переводы строк — тоже часть вывода.
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
      """.formatted(javaLiteral(expected)); addTask(Language.JAVA,"BASIC_CODE_READING",title,difficulty,statement,starter,test,"TestHarness.java"); }
  private String javaLiteral(String value) { return value.replace("\\","\\\\").replace("\n","\\n").replace("\"","\\\""); }
  /** Idempotent by title: re-running the importer refreshes seed content instead of adding duplicates. */
  private void addTask(Language language,String skill,String title,int difficulty,String statement,String starter,String test,String testFile) {
    var existing=db.queryForList("select id from tasks where title=?",title);
    if(!existing.isEmpty()){
      long id=((Number)existing.getFirst().get("id")).longValue();
      db.update("update tasks set skill_code=?,statement=?,starter_code=?,test_source=?,test_file_name=?,difficulty=?,language=?,active=1 where id=?",skill,statement,starter,test,testFile,difficulty,language.name(),id);
      db.update("insert or ignore into task_target_skills(task_id,skill_code) values(?,?)",id,skill);
      return;
    }
    db.update("insert into tasks(skill_code,title,statement,starter_code,test_source,test_file_name,difficulty,language) values(?,?,?,?,?,?,?,?)",skill,title,statement,starter,test,testFile,difficulty,language.name());
    db.update("insert into task_target_skills(task_id,skill_code) values(last_insert_rowid(),?)",skill);
  }

  private void seedPythonTasks() {
    if (db.queryForObject("select count(*) from skills where code='PY_BASIC_CODE_READING'", Integer.class) == 0) return;
    addPythonOutputTask("Python: приветствие", 1, "Напечатай в консоль слово «Привет» без перевода строки в конце.", "Привет");
    addPythonOutputTask("Python: число", 1, "Напечатай число 7. Обычный `print` сам добавит перевод строки в конце — так и нужно.", "7\n");
    addPythonOutputTask("Python: символ", 1, "Напечатай букву A без перевода строки в конце.", "A");
    addPythonOutputTask("Python: две строки", 2, "Напечатай «Раз» и «Два» на двух разных строках.", "Раз\nДва\n");
    addPythonOutputTask("Python: логическое значение", 2, "Напечатай логическое значение True и заверши строку переводом строки.", "True\n");
    addPythonOutputTask("Python: знак Python", 2, "Напечатай Python и сразу после него восклицательный знак — без пробела и без перевода строки.", "Python!");
    addPythonOutputTask("Python: пустая строка", 3, "Сначала напечатай пустую строку, затем на следующей строке напечатай «готово» без перевода строки после него.", "\nготово");
    addPythonOutputTask("Python: кота", 3, "Напечатай 3, затем пробел и слово «кота», после чего перейди на новую строку.", "3 кота\n");
    addPythonOutputTask("Python: три значения", 3, "Напечатай подряд X, затем Y с переводом строки, затем False без перевода строки после него.", "XY\nFalse");
  }
  private void addPythonOutputTask(String title,int difficulty,String action,String expected) {
    String statement=action+"\n\nНапиши код в `solution.py` с помощью `print(...)`. Чтобы `print` не переходил на новую строку, передай ему `end=\"\"`.\n\n**Должно получиться в консоли:**\n\n```text\n"+expected.stripTrailing()+"\n```\n\nПроверка сравнивает вывод символ в символ, включая пробелы и переводы строк — перечитай в условии, нужен ли перевод строки в конце.";
    String test="""
        import contextlib
        import io


        def run_checks():
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                import solution  # noqa: F401  (the student's top-level code runs on import)
            assert buffer.getvalue() == "%s", "Вывод не совпадает с ожидаемым: проверь текст, пробелы и переводы строк"
        """.formatted(javaLiteral(expected));
    addTask(Language.PYTHON,"PY_BASIC_CODE_READING",title,difficulty,statement,"# Напиши решение здесь\n",test,"test_solution.py");
  }
}
