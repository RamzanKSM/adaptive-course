package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.jdbc.core.JdbcTemplate;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Which language constructs a task's code uses and in which course topic each is taught, so a task never needs what the
 * student has not been shown yet. Detection is lexical (comments and string literals removed first): it is meant for
 * a task's own starter code and reference solution, not for arbitrary student code.
 */
final class CourseConstructs {
  private CourseConstructs() {}

  /** A construct and the topic (per language) that teaches it; null topic = not part of the regular course. */
  enum Construct {
    METHOD("собственные методы (функции)", "METHOD_BASIC", "PY_FUNCTION_BASIC"),
    CLASS("собственные классы", "CLASS_BASIC", "PY_CLASS_BASIC"),
    IF("условия", "IF_ELSE_BASIC", "PY_IF_ELSE_BASIC"),
    SWITCH("switch", "SWITCH_BASIC", null),
    FOR("цикл for", "FOR_LOOP_BASIC", "PY_FOR_RANGE"),
    WHILE("цикл while", "WHILE_LOOP_BASIC", "PY_WHILE_LOOP_BASIC"),
    ARRAY("массивы (списки)", "ARRAY_INDEXING", "PY_LIST_INDEXING"),
    LIST("коллекция List", "LIST_BASIC", null),
    SET("множества", "SET_BASIC", "PY_SET_BASIC"),
    MAP("словари (Map)", "MAP_BASIC", "PY_DICT_BASIC"),
    FSTRING("f-строки", null, "PY_FSTRINGS"),
    TRY("обработка исключений", "TRY_CATCH_BASIC", "PY_TRY_EXCEPT_BASIC"),
    INPUT("чтение ввода", null, null);

    final String title; private final String javaTopic; private final String pythonTopic;
    Construct(String title, String javaTopic, String pythonTopic) { this.title = title; this.javaTopic = javaTopic; this.pythonTopic = pythonTopic; }
    String topic(Language lang) { return lang == Language.PYTHON ? pythonTopic : javaTopic; }
  }

  /** Constructs whose use in a regular task before their topic is rejected; the rest are reported (export) but not enforced. */
  static final Set<Construct> ENFORCED = EnumSet.of(Construct.METHOD, Construct.CLASS, Construct.INPUT);

  private static final Set<String> JAVA_PLATFORM_CLASSES = Set.of("Solution", "TestHarness", "PlatformLauncher");
  private static final Set<String> NOT_METHOD_NAMES = Set.of("main", "if", "for", "while", "switch", "catch", "synchronized", "return");
  private static final Pattern JAVA_METHOD = Pattern.compile("\\b([A-Za-z_][\\w<>\\[\\]]*)\\s+([A-Za-z_]\\w*)\\s*\\([^;{}()]*\\)\\s*(?:throws\\s+[\\w.,\\s]+)?\\{");
  private static final Pattern JAVA_TYPE = Pattern.compile("\\b(?:class|interface|enum|record)\\s+([A-Za-z_]\\w*)");
  private static final Pattern JAVA_MAIN_ARGS = Pattern.compile("main\\s*\\(\\s*(?:final\\s+)?String\\s*(?:\\[\\s*]|\\.\\.\\.)\\s*\\w+\\s*\\)");
  private static final Pattern PY_LIST_LITERAL = Pattern.compile("(?:^|[=(,:\\[]|\\breturn|\\bin)\\s*\\[", Pattern.MULTILINE);
  private static final Pattern PY_DEF = Pattern.compile("^\\s*(?:async\\s+)?def\\s+\\w+", Pattern.MULTILINE);
  private static final Pattern PY_CLASS = Pattern.compile("^\\s*class\\s+\\w+", Pattern.MULTILINE);

  /** Constructs used by any of the sources (starter code, reference solution). */
  static Set<Construct> used(Language lang, String... sources) {
    Set<Construct> found = EnumSet.noneOf(Construct.class);
    for (String source : sources) if (source != null && !source.isBlank()) found.addAll(lang == Language.PYTHON ? python(source) : java(source));
    return found;
  }

  /** What the goal itself requires: a function task needs methods; required constructs map to their topics. */
  static Set<Construct> required(JsonNode goal) {
    Set<Construct> found = EnumSet.noneOf(Construct.class);
    if (goal == null) return found;
    String kind = goal.path("kind").asText();
    if ("FUNCTION_BEHAVIOR".equals(kind)) found.add(Construct.METHOD);
    if ("IO_BEHAVIOR".equals(kind)) found.add(Construct.INPUT);
    for (JsonNode construct : goal.path("requiredConstructs")) switch (construct.asText()) {
      case "function", "return" -> found.add(Construct.METHOD);
      case "class" -> found.add(Construct.CLASS);
      case "if" -> found.add(Construct.IF);
      case "for" -> found.add(Construct.FOR);
      case "while" -> found.add(Construct.WHILE);
      case "list" -> found.add(Construct.ARRAY);
      case "dict" -> found.add(Construct.MAP);
      case "try" -> found.add(Construct.TRY);
      default -> { }
    }
    return found;
  }

  /** Methods the checks call on the student's code (Java: Solution.x(...) other than main; Python: imported names). */
  static boolean checksCallMethods(Language lang, String testSource) {
    if (testSource == null || testSource.isBlank()) return false;
    String code = stripJavaLike(testSource);
    if (lang == Language.PYTHON) return Pattern.compile("from\\s+solution\\s+import\\b|\\bsolution\\.\\w+\\s*\\(").matcher(stripPython(testSource)).find();
    Matcher calls = Pattern.compile("\\bSolution\\.(\\w+)\\s*\\(").matcher(code);
    while (calls.find()) if (!"main".equals(calls.group(1))) return true;
    return false;
  }

  /**
   * The constructs taught after the topic skillCode (the topic itself counts as taught). A construct with no topic in
   * the course (reading input) is never taught in regular lessons.
   */
  static List<Construct> notYetTaught(JdbcTemplate db, Language lang, String skillCode, Collection<Construct> used) {
    Integer order = topicOrder(db, skillCode);
    List<Construct> late = new ArrayList<>();
    if (order == null) return late;
    for (Construct construct : new TreeSet<>(used)) {
      String topic = construct.topic(lang);
      if (topic == null) { late.add(construct); continue; }
      Integer taughtAt = topicOrder(db, topic);
      if (taughtAt != null && taughtAt > order) late.add(construct);
    }
    return late;
  }

  /**
   * The enforced constructs (methods, classes, reading input) a regular task of topic skillCode needs before the course
   * teaches them: from its goal, from what its checks call and from its code (starter code, reference solution).
   */
  static List<Construct> beyondTopic(JdbcTemplate db, Language lang, String skillCode, JsonNode goal, String testSource, String... sources) {
    Set<Construct> needed = used(lang, sources);
    needed.addAll(required(goal));
    if (checksCallMethods(lang, testSource)) needed.add(Construct.METHOD);
    List<Construct> late = notYetTaught(db, lang, skillCode, needed);
    late.retainAll(ENFORCED);
    return late;
  }

  /** A short Russian list: «собственные методы (функции) — тема METHOD_BASIC». */
  static String describe(Language lang, Collection<Construct> constructs) {
    return constructs.stream().map(c -> c.title + (c.topic(lang) == null ? " — нет в курсе" : " — тема " + c.topic(lang))).reduce((a, b) -> a + "; " + b).orElse("");
  }

  private static Integer topicOrder(JdbcTemplate db, String code) {
    var rows = db.queryForList("select sort_order from skills where code=?", Integer.class, code);
    return rows.isEmpty() ? null : rows.getFirst();
  }

  private static Set<Construct> java(String source) {
    Set<Construct> found = EnumSet.noneOf(Construct.class);
    String code = JAVA_MAIN_ARGS.matcher(stripJavaLike(source)).replaceAll("main()");
    Matcher method = JAVA_METHOD.matcher(code);
    while (method.find()) {
      String type = method.group(1), name = method.group(2);
      if (!NOT_METHOD_NAMES.contains(name) && !Set.of("new", "else", "return").contains(type)) { found.add(Construct.METHOD); break; }
    }
    Matcher type = JAVA_TYPE.matcher(code);
    while (type.find()) if (!JAVA_PLATFORM_CLASSES.contains(type.group(1))) { found.add(Construct.CLASS); break; }
    if (find(code, "\\bif\\s*\\(") || find(code, "\\?[^;:]*:")) found.add(Construct.IF);
    if (find(code, "\\bswitch\\s*\\(")) found.add(Construct.SWITCH);
    if (find(code, "\\bfor\\s*\\(")) found.add(Construct.FOR);
    if (find(code, "\\bwhile\\s*\\(")) found.add(Construct.WHILE);
    if (find(code, "\\w\\s*\\[\\s*]|\\bnew\\s+\\w+\\s*\\[")) found.add(Construct.ARRAY);
    if (find(code, "\\b(?:List|ArrayList|LinkedList)\\b")) found.add(Construct.LIST);
    if (find(code, "\\b(?:Set|HashSet|TreeSet|LinkedHashSet)\\b")) found.add(Construct.SET);
    if (find(code, "\\b(?:Map|HashMap|TreeMap|LinkedHashMap)\\b")) found.add(Construct.MAP);
    if (find(code, "\\btry\\s*\\{")) found.add(Construct.TRY);
    if (find(code, "\\bScanner\\b|\\bSystem\\.in\\b|\\bBufferedReader\\b")) found.add(Construct.INPUT);
    return found;
  }

  private static Set<Construct> python(String source) {
    Set<Construct> found = EnumSet.noneOf(Construct.class);
    if (find(source, "(?i)(?<![\\w])(?:f|rf|fr)[\"']")) found.add(Construct.FSTRING);
    String code = stripPython(source);
    if (PY_DEF.matcher(code).find() || find(code, "\\blambda\\b")) found.add(Construct.METHOD);
    if (PY_CLASS.matcher(code).find()) found.add(Construct.CLASS);
    if (find(code, "\\b(?:if|elif)\\b")) found.add(Construct.IF);
    if (find(code, "\\bfor\\b")) found.add(Construct.FOR);
    if (find(code, "\\bwhile\\b")) found.add(Construct.WHILE);
    if (PY_LIST_LITERAL.matcher(code).find() || find(code, "\\blist\\s*\\(")) found.add(Construct.ARRAY);
    if (find(code, "\\bset\\s*\\(")) found.add(Construct.SET);
    if (find(code, "\\{") || find(code, "\\bdict\\s*\\(")) found.add(Construct.MAP);
    if (find(code, "^\\s*try\\s*:")) found.add(Construct.TRY);
    if (find(code, "\\binput\\s*\\(|\\bsys\\.stdin\\b")) found.add(Construct.INPUT);
    return found;
  }

  private static boolean find(String code, String regex) { return Pattern.compile(regex, Pattern.MULTILINE).matcher(code).find(); }

  /** Java: comments, string and char literals removed (literals become ""). */
  static String stripJavaLike(String source) {
    StringBuilder out = new StringBuilder(source.length());
    int i = 0, n = source.length();
    while (i < n) {
      char c = source.charAt(i);
      if (source.startsWith("\"\"\"", i)) { int end = source.indexOf("\"\"\"", i + 3); i = end < 0 ? n : end + 3; out.append("\"\""); }
      else if (source.startsWith("//", i)) { int end = source.indexOf('\n', i); i = end < 0 ? n : end; }
      else if (source.startsWith("/*", i)) { int end = source.indexOf("*/", i + 2); i = end < 0 ? n : end + 2; out.append(' '); }
      else if (c == '"' || c == '\'') { i = skipQuoted(source, i, c); out.append(c).append(c); }
      else { out.append(c); i++; }
    }
    return out.toString();
  }

  /** Python: comments and string literals (including triple-quoted and f-strings) removed. */
  static String stripPython(String source) {
    StringBuilder out = new StringBuilder(source.length());
    int i = 0, n = source.length();
    while (i < n) {
      char c = source.charAt(i);
      if (c == '#') { int end = source.indexOf('\n', i); i = end < 0 ? n : end; }
      else if (source.startsWith("\"\"\"", i) || source.startsWith("'''", i)) { String q = source.substring(i, i + 3); int end = source.indexOf(q, i + 3); i = end < 0 ? n : end + 3; out.append("\"\""); }
      else if (c == '"' || c == '\'') { i = skipQuoted(source, i, c); out.append("\"\""); }
      else { out.append(c); i++; }
    }
    return out.toString();
  }

  private static int skipQuoted(String source, int start, char quote) {
    int i = start + 1;
    while (i < source.length()) {
      char c = source.charAt(i);
      if (c == '\\') { i += 2; continue; }
      if (c == quote || c == '\n') return i + 1;
      i++;
    }
    return source.length();
  }
}
