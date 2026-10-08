package ru.teacherstaff.adaptive;

import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.Pattern;

/**
 * Test cases the platform runs for function (FUNCTION_BEHAVIOR) and input/output (IO_BEHAVIOR) tasks. The LLM gives
 * only the inputs; the expected answers are recorded by running the task's reference solution, and the checking
 * program is built here from a fixed template — so neither the answers nor the checks depend on what the model wrote.
 * <p>
 * Input of a function case is the argument list as source code (what goes between the call's parentheses); input of
 * an I/O case is the text fed to stdin. Data travels through the generated programs as Base64, so no escaping of
 * arbitrary text in Java or Python literals is ever needed.
 */
final class TestCases {
  private TestCases() {}

  /** An input from the generator; public — it is one of the examples shown in the statement. */
  record Input(String input, boolean isPublic) {}
  /** A stored case: the input and the reference solution's answer. */
  record Case(int ordinal, String input, String expected, boolean isPublic) {}

  static final int MIN_CASES = 6, MAX_CASES = 40, HIDDEN_PER_RUN = 8;
  private static final Pattern RECORDED = Pattern.compile("^__CASE__(\\d+):(.*)$");
  private static final Pattern FAILED = Pattern.compile("^__CASE_ERR__(\\d+) (.*)$");

  static boolean usesCases(TaskGoal goal) { return goal != null && (goal.kind() == TaskGoal.Kind.FUNCTION_BEHAVIOR || goal.kind() == TaskGoal.Kind.IO_BEHAVIOR); }

  /** The inputs a generator must provide: enough of them, distinct, at least one shown in the statement. */
  static void validateInputs(List<Input> inputs) {
    if (inputs == null || inputs.size() < MIN_CASES) throw rejected("need at least " + MIN_CASES + " test inputs, got " + (inputs == null ? 0 : inputs.size()));
    if (inputs.size() > MAX_CASES) throw rejected("at most " + MAX_CASES + " test inputs, got " + inputs.size());
    if (inputs.stream().noneMatch(Input::isPublic)) throw rejected("mark the statement's examples as public test inputs");
    if (inputs.stream().map(Input::input).distinct().count() < inputs.size()) throw rejected("test inputs must be distinct");
    for (Input input : inputs) if (input.input() == null) throw rejected("empty test input");
  }

  // ───────── Recording the reference's answers ─────────

  /** A program that runs the solution on every input and prints each answer as «__CASE__i:base64». */
  static String recorder(Language language, TaskGoal goal, List<Input> inputs) {
    return language == Language.PYTHON ? pythonProgram(goal, inputs.stream().map(Input::input).toList(), null) : javaProgram(goal, inputs.stream().map(Input::input).toList(), null);
  }

  /** Parses the recorder's output; any case the reference could not answer makes the task unusable. */
  static List<Case> recorded(List<Input> inputs, String stdout) {
    Map<Integer, String> answers = new HashMap<>();
    for (String line : stdout.split("\\R")) {
      var failed = FAILED.matcher(line);
      if (failed.matches()) throw rejected("reference solution failed on test input " + (Integer.parseInt(failed.group(1)) + 1) + ": " + failed.group(2));
      var ok = RECORDED.matcher(line);
      if (ok.matches()) answers.put(Integer.parseInt(ok.group(1)), new String(Base64.getDecoder().decode(ok.group(2)), StandardCharsets.UTF_8));
    }
    List<Case> cases = new ArrayList<>();
    for (int i = 0; i < inputs.size(); i++) {
      String answer = answers.get(i);
      if (answer == null) throw rejected("reference solution gave no answer for test input " + (i + 1));
      cases.add(new Case(i + 1, inputs.get(i).input(), answer, inputs.get(i).isPublic()));
    }
    if (cases.stream().map(Case::expected).distinct().count() < 2) throw rejected("every test input has the same answer, so a hard-coded answer would pass");
    return cases;
  }

  // ───────── Checking a solution ─────────

  /** What one check runs: every public example and up to HIDDEN_PER_RUN hidden cases in random order. */
  static List<Case> sample(List<Case> all, Random random) {
    List<Case> run = new ArrayList<>(all.stream().filter(Case::isPublic).toList());
    List<Case> hidden = new ArrayList<>(all.stream().filter(c -> !c.isPublic()).toList());
    Collections.shuffle(hidden, random);
    run.addAll(hidden.subList(0, Math.min(HIDDEN_PER_RUN, hidden.size())));
    return run;
  }

  /**
   * The checking program: compares the solution's answer with the recorded one case by case and stops at the first
   * difference. A failed example shows what was expected and what came out; a failed hidden case only says which test
   * of how many failed, so the hidden data cannot be collected.
   */
  static String checker(Language language, TaskGoal goal, List<Case> cases) {
    List<String> inputs = cases.stream().map(Case::input).toList();
    return language == Language.PYTHON ? pythonProgram(goal, inputs, cases) : javaProgram(goal, inputs, cases);
  }

  // ───────── Program templates ─────────

  private static String b64(String text) { return Base64.getEncoder().encodeToString(text.getBytes(StandardCharsets.UTF_8)); }

  /** cases == null: the recorder; otherwise the checker with these expected answers. */
  private static String javaProgram(TaskGoal goal, List<String> inputs, List<Case> cases) {
    boolean io = goal.kind() == TaskGoal.Kind.IO_BEHAVIOR;
    StringBuilder body = new StringBuilder();
    for (int i = 0; i < inputs.size(); i++) {
      String call = io ? "runMain(\"" + b64(inputs.get(i)) + "\")" : "fmt(Solution." + goal.functionName() + "(" + inputs.get(i) + "))";
      if (cases == null) body.append("    try { System.out.println(\"__CASE__").append(i).append(":\" + enc(").append(call).append(")); } catch (Throwable t) { System.out.println(\"__CASE_ERR__").append(i).append(" \" + t); }\n");
      else body.append("    { String out = null; try { out = ").append(call).append("; } catch (Throwable t) { fail(").append(i).append(", null, t); } check(").append(i).append(", out); }\n");
    }
    String helpers = """
          static String dec(String b) { return new String(Base64.getDecoder().decode(b), StandardCharsets.UTF_8); }
          static String enc(String s) { return Base64.getEncoder().encodeToString(s.getBytes(StandardCharsets.UTF_8)); }
          static String fmt(Object o) {
            if (o == null) return "null";
            if (o instanceof String) return "\\"" + o + "\\"";
            if (o instanceof Character) return "'" + o + "'";
            if (o.getClass().isArray()) { String d = Arrays.deepToString(new Object[]{o}); return d.substring(1, d.length() - 1); }
            return String.valueOf(o);
          }
        """;
    if (io) helpers += """
          static String runMain(String input) throws Exception {
            PrintStream out = System.out; InputStream in = System.in;
            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            try {
              System.setIn(new ByteArrayInputStream(dec(input).getBytes(StandardCharsets.UTF_8)));
              System.setOut(new PrintStream(buffer, true, "UTF-8"));
              Solution.main(new String[0]);
            } finally { System.setOut(out); System.setIn(in); }
            return buffer.toString("UTF-8");
          }
        """;
    String checking = "";
    if (cases != null) {
      StringBuilder table = new StringBuilder("  static final String[] EXPECTED = {");
      for (Case c : cases) table.append('"').append(b64(c.expected())).append("\",");
      table.append("};\n  static final String[] LABEL = {");
      int example = 0;
      for (int i = 0; i < cases.size(); i++) table.append('"').append(b64(cases.get(i).isPublic() ? "Пример " + (++example) : "Тест " + (i + 1) + " из " + cases.size())).append("\",");
      table.append("};\n  static final boolean[] PUBLIC = {");
      for (Case c : cases) table.append(c.isPublic()).append(',');
      table.append("};\n");
      checking = table + """
            static String show(String s) { String t = s.replace("\\n", "\u21b5"); return t.length() > 200 ? t.substring(0, 200) + "\u2026" : t; }
            static void fail(int i, String actual, Throwable error) {
              String label = dec(LABEL[i]);
              if (PUBLIC[i]) throw new AssertionError(label + (error != null ? ": программа завершилась с ошибкой " + error : ": ожидалось «" + show(dec(EXPECTED[i])) + "», получилось «" + show(actual) + "»"));
              throw new AssertionError(label + (error != null ? ": программа завершилась с ошибкой " + error.getClass().getSimpleName() : " не пройден: ответ отличается от правильного"));
            }
            static void check(int i, String actual) { if (!dec(EXPECTED[i]).equals(actual)) fail(i, actual, null); }
          """;
    }
    return "import java.io.*;\nimport java.nio.charset.StandardCharsets;\nimport java.util.*;\n\npublic class TestHarness {\n" + helpers + checking
        + "  public static void main(String[] args) throws Exception {\n" + body
        + (cases == null ? "" : "    System.out.print(\"" + PistonCodeRunner.PASS_MARKER_PLACEHOLDER + "\");\n") + "  }\n}\n";
  }

  private static String pythonProgram(TaskGoal goal, List<String> inputs, List<Case> cases) {
    boolean io = goal.kind() == TaskGoal.Kind.IO_BEHAVIOR;
    StringBuilder calls = new StringBuilder();
    for (int i = 0; i < inputs.size(); i++)
      calls.append("    (lambda: ").append(io ? "_run_main(" + pyString(b64(inputs.get(i))) + ")" : "repr(_solution()." + goal.functionName() + "(" + inputs.get(i) + "))").append("),\n");
    String common = """
        import base64
        import contextlib
        import io
        import runpy
        import sys


        def _dec(text):
            return base64.b64decode(text).decode("utf-8")


        def _solution():
            with contextlib.redirect_stdout(io.StringIO()):
                import solution
            return solution


        def _run_main(encoded):
            buffer, stdin = io.StringIO(), sys.stdin
            sys.stdin = io.StringIO(_dec(encoded))
            try:
                with contextlib.redirect_stdout(buffer):
                    runpy.run_path("solution.py", run_name="__main__")
            finally:
                sys.stdin = stdin
            return buffer.getvalue()


        CALLS = [
        %s]
        """.formatted(calls);
    if (cases == null) return common + """


        for _i, _call in enumerate(CALLS):
            try:
                with contextlib.redirect_stdout(io.StringIO()) if %s else contextlib.nullcontext():
                    _out = _call()
            except BaseException as _e:
                print("__CASE_ERR__%%d %%s: %%s" %% (_i, type(_e).__name__, _e))
                continue
            print("__CASE__%%d:%%s" %% (_i, base64.b64encode(_out.encode("utf-8")).decode("ascii")))
        """.formatted(io ? "False" : "True");
    StringBuilder expected = new StringBuilder("EXPECTED = [");
    StringBuilder labels = new StringBuilder("LABELS = [");
    int example = 0;
    for (int i = 0; i < cases.size(); i++) {
      Case c = cases.get(i);
      expected.append(pyString(b64(c.expected()))).append(", ");
      labels.append("(").append(c.isPublic() ? "True, " + pyString("Пример " + (++example)) : "False, " + pyString("Тест " + (i + 1) + " из " + cases.size())).append("), ");
    }
    return common + expected + "]\n" + labels + "]\n" + """


        def _show(text):
            text = text.replace("\\n", "↵")
            return text if len(text) <= 200 else text[:200] + "…"


        def run_checks():
            for (public, label), call, encoded in zip(LABELS, CALLS, EXPECTED):
                try:
                    with contextlib.redirect_stdout(io.StringIO()) if %s else contextlib.nullcontext():
                        actual = call()
                except BaseException as error:
                    if public:
                        raise AssertionError("%%s: программа завершилась с ошибкой %%s: %%s" %% (label, type(error).__name__, error))
                    raise AssertionError("%%s: программа завершилась с ошибкой %%s" %% (label, type(error).__name__))
                if actual != _dec(encoded):
                    if public:
                        raise AssertionError("%%s: ожидалось «%%s», получилось «%%s»" %% (label, _show(_dec(encoded)), _show(actual)))
                    raise AssertionError("%%s не пройден: ответ отличается от правильного" %% label)
        """.formatted(io ? "False" : "True");
  }

  private static String pyString(String text) { return "\"" + text.replace("\\", "\\\\").replace("\"", "\\\"") + "\""; }
  private static InvalidGeneratedContentException rejected(String reason) { return new InvalidGeneratedContentException(reason); }
}
