package ru.teacherstaff.adaptive;

import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

/**
 * The platform's recorder and checker programs, run for real the way Piston runs them: Java in single-file mode
 * (java TestHarness.java, harness first), Python as the fixed entry point next to test_solution.py and solution.py.
 */
class TestCasesTest {
  private static final TaskGoal AREA = new TaskGoal(TaskGoal.Kind.FUNCTION_BEHAVIOR, null, List.of(), null, "area", List.of());
  private static final TaskGoal PRODUCT = new TaskGoal(TaskGoal.Kind.IO_BEHAVIOR, null, List.of(), null, null, List.of());
  private static final List<TestCases.Input> AREA_INPUTS = List.of(new TestCases.Input("2, 3", true), new TestCases.Input("0, 5", false), new TestCases.Input("4, 4", false),
      new TestCases.Input("1, 9", false), new TestCases.Input("7, 2", false), new TestCases.Input("10, 10", false));
  private static final List<TestCases.Input> PRODUCT_INPUTS = List.of(new TestCases.Input("2 3\n", true), new TestCases.Input("0 5\n", false), new TestCases.Input("4 4\n", false),
      new TestCases.Input("1 9\n", false), new TestCases.Input("7 2\n", false), new TestCases.Input("10 10\n", false));

  @Test void javaFunctionCasesAreRecordedFromTheReferenceAndCheckTheStudent(@TempDir Path dir) throws Exception {
    Assumptions.assumeTrue(javaAvailable(), "java is not available");
    var cases = TestCases.recorded(AREA_INPUTS, java(dir, "public class Solution { static int area(int w, int h) { return w * h; } }", TestCases.recorder(Language.JAVA, AREA, AREA_INPUTS)).out());
    assertEquals(List.of("6", "0", "16", "9", "14", "100"), cases.stream().map(TestCases.Case::expected).toList());
    String checker = TestCases.checker(Language.JAVA, AREA, cases);
    assertTrue(java(dir, "public class Solution { static int area(int w, int h) { return h * w; } }", checker).out().endsWith(PistonCodeRunner.PASS_MARKER_PLACEHOLDER));
    // A failed example shows what was expected; a failed hidden case does not reveal its data.
    var example = java(dir, "public class Solution { static int area(int w, int h) { return w + h; } }", checker);
    assertTrue(example.err().contains("Пример 1: ожидалось «6», получилось «5»"), example.err());
    var hidden = java(dir, "public class Solution { static int area(int w, int h) { return w == 2 && h == 3 ? 6 : 1; } }", checker);
    assertTrue(hidden.err().contains("Тест 2 из 6 не пройден: ответ отличается от правильного"), hidden.err());
    assertFalse(hidden.err().contains("0, 5"));
    var crash = java(dir, "public class Solution { static int area(int w, int h) { if (w == 0) throw new IllegalStateException(\"zero\"); return w * h; } }", checker);
    assertTrue(crash.err().contains("Тест 2 из 6: программа завершилась с ошибкой IllegalStateException"), crash.err());
    assertEquals("Тест 2 из 6: программа завершилась с ошибкой IllegalStateException", PistonCodeRunner.assertionMessage(crash.err()));
  }

  @Test void javaInputOutputCasesFeedStdinAndCompareTheOutput(@TempDir Path dir) throws Exception {
    Assumptions.assumeTrue(javaAvailable(), "java is not available");
    String reference = "import java.util.Scanner;\npublic class Solution { public static void main(String[] args) { Scanner in = new Scanner(System.in); System.out.println(in.nextInt() * in.nextInt()); } }";
    var cases = TestCases.recorded(PRODUCT_INPUTS, java(dir, reference, TestCases.recorder(Language.JAVA, PRODUCT, PRODUCT_INPUTS)).out());
    assertEquals("6\n", cases.getFirst().expected());
    String checker = TestCases.checker(Language.JAVA, PRODUCT, cases);
    assertTrue(java(dir, reference, checker).out().endsWith(PistonCodeRunner.PASS_MARKER_PLACEHOLDER));
    var printsExample = java(dir, TaskGoal.printText(Language.JAVA, "6\n"), checker);
    assertTrue(printsExample.err().contains("Тест 2 из 6 не пройден"), printsExample.err());
    var noNewline = java(dir, "import java.util.Scanner;\npublic class Solution { public static void main(String[] args) { Scanner in = new Scanner(System.in); System.out.print(\"Итого \" + in.nextInt() * in.nextInt()); } }", checker);
    assertTrue(noNewline.err().contains("Пример 1: ожидалось «6↵», получилось «Итого 6»"), noNewline.err());
  }

  @Test void pythonFunctionAndInputOutputCases(@TempDir Path dir) throws Exception {
    Assumptions.assumeTrue(pythonAvailable(), "python3 is not installed");
    List<TestCases.Input> inputs = AREA_INPUTS;
    var cases = TestCases.recorded(inputs, python(dir, "def area(w, h):\n    print('debug')\n    return w * h\n", TestCases.recorder(Language.PYTHON, AREA, inputs), false).out());
    assertEquals("6", cases.getFirst().expected());
    String checker = TestCases.checker(Language.PYTHON, AREA, cases);
    assertTrue(python(dir, "def area(w, h):\n    return w * h\n", checker, true).passed());
    var example = python(dir, "def area(w, h):\n    return w + h\n", checker, true);
    assertTrue(example.err().contains("Пример 1: ожидалось «6», получилось «5»"), example.err());
    var hidden = python(dir, "def area(w, h):\n    return 6 if (w, h) == (2, 3) else 1\n", checker, true);
    assertTrue(hidden.err().contains("Тест 2 из 6 не пройден: ответ отличается от правильного"), hidden.err());

    String reference = "a, b = map(int, input().split())\nprint(a * b)\n";
    var io = TestCases.recorded(PRODUCT_INPUTS, python(dir, reference, TestCases.recorder(Language.PYTHON, PRODUCT, PRODUCT_INPUTS), false).out());
    assertEquals("100\n", io.getLast().expected());
    String ioChecker = TestCases.checker(Language.PYTHON, PRODUCT, io);
    assertTrue(python(dir, reference, ioChecker, true).passed());
    assertTrue(python(dir, TaskGoal.printText(Language.PYTHON, "6\n"), ioChecker, true).err().contains("Тест 2 из 6 не пройден"));
  }

  @Test void referenceFailuresAndConstantAnswersMakeTheTaskUnusable() {
    var failed = assertThrows(InvalidGeneratedContentException.class, () -> TestCases.recorded(AREA_INPUTS, "__CASE_ERR__3 ArithmeticException: / by zero\n"));
    assertTrue(failed.getMessage().contains("test input 4"));
    StringBuilder same = new StringBuilder();
    for (int i = 0; i < AREA_INPUTS.size(); i++) same.append("__CASE__").append(i).append(":").append(Base64.getEncoder().encodeToString("1".getBytes(StandardCharsets.UTF_8))).append('\n');
    assertTrue(assertThrows(InvalidGeneratedContentException.class, () -> TestCases.recorded(AREA_INPUTS, same.toString())).getMessage().contains("same answer"));
    assertThrows(InvalidGeneratedContentException.class, () -> TestCases.validateInputs(AREA_INPUTS.subList(0, 3)));
    assertThrows(InvalidGeneratedContentException.class, () -> TestCases.validateInputs(AREA_INPUTS.stream().map(i -> new TestCases.Input(i.input(), false)).toList()));
  }

  @Test void eachRunHasEveryExampleAndASampleOfHiddenCases() {
    List<TestCases.Case> all = new ArrayList<>();
    for (int i = 1; i <= 20; i++) all.add(new TestCases.Case(i, "in" + i, "out" + i, i <= 2));
    var run = TestCases.sample(all, new Random(7));
    assertEquals(2 + TestCases.HIDDEN_PER_RUN, run.size());
    assertTrue(run.get(0).isPublic() && run.get(1).isPublic());
    assertEquals(run.size(), run.stream().distinct().count());
    assertNotEquals(run.subList(2, run.size()), TestCases.sample(all, new Random(8)).subList(2, run.size()), "hidden cases differ between runs");
  }

  // ───────── Running like Piston ─────────

  record Result(int code, String out, String err) { boolean passed() { return code == 0 && out.strip().endsWith("__PASS__"); } }

  private static Result java(Path base, String solution, String program) throws Exception {
    Path dir = Files.createTempDirectory(base, "java");
    Files.writeString(dir.resolve("TestHarness.java"), PistonCodeRunner.combinedSource(solution, program), StandardCharsets.US_ASCII);
    return exec(dir, null, Path.of(System.getProperty("java.home"), "bin", "java").toString(), "TestHarness.java");
  }

  /** checker=true: the fixed entry point with test_solution.py, the marker on stdin; false: the recorder as main.py. */
  private static Result python(Path base, String solution, String program, boolean checker) throws Exception {
    Path dir = Files.createTempDirectory(base, "py");
    Files.writeString(dir.resolve("solution.py"), solution, StandardCharsets.UTF_8);
    if (checker) {
      Files.writeString(dir.resolve("main.py"), PistonCodeRunner.PYTHON_ENTRY.strip() + "\n", StandardCharsets.UTF_8);
      Files.writeString(dir.resolve("test_solution.py"), program, StandardCharsets.UTF_8);
      return exec(dir, "__PASS__\n", "python3", "main.py");
    }
    Files.writeString(dir.resolve("main.py"), program, StandardCharsets.UTF_8);
    return exec(dir, "", "python3", "main.py");
  }

  private static Result exec(Path dir, String stdin, String... command) throws Exception {
    var builder = new ProcessBuilder(command).directory(dir.toFile());
    builder.environment().put("LC_ALL", "C");
    Process process = builder.start();
    if (stdin != null) process.getOutputStream().write(stdin.getBytes(StandardCharsets.UTF_8));
    process.getOutputStream().close();
    String out = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8), err = new String(process.getErrorStream().readAllBytes(), StandardCharsets.UTF_8);
    assertTrue(process.waitFor(60, TimeUnit.SECONDS));
    return new Result(process.exitValue(), out, PistonCodeRunner.javaConsoleDiagnostic(err.replace("TestHarness", "Solution")) + err);
  }

  private static boolean javaAvailable() { return Files.isExecutable(Path.of(System.getProperty("java.home"), "bin", "javac")); }
  private static boolean pythonAvailable() {
    try { return new ProcessBuilder("python3", "--version").start().waitFor(10, TimeUnit.SECONDS); } catch (Exception e) { return false; }
  }

  @SuppressWarnings("unused") private static final BigDecimal UNUSED = BigDecimal.ONE;
}
