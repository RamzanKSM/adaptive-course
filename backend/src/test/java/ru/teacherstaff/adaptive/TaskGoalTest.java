package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

class TaskGoalTest {
  private final ObjectMapper json = new ObjectMapper();
  private static final TaskGoal TICKETS = new TaskGoal(TaskGoal.Kind.FIXED_ARITHMETIC, "*", List.of(new BigDecimal(4), new BigDecimal(6)), "24\n", null, List.of());

  @Test void parsesValidatesAndRoundTrips() throws Exception {
    TaskGoal goal = TaskGoal.parse(json.readTree("{\"kind\":\"FIXED_ARITHMETIC\",\"operation\":\"*\",\"operands\":[4,6],\"expectedOutput\":\"24\\n\",\"functionName\":null,\"requiredConstructs\":[]}"));
    goal.validate(Language.PYTHON, "");
    assertEquals("24", goal.result(Language.PYTHON));
    assertEquals(goal, TaskGoal.fromJson(json, goal.toJson(json)));
    assertTrue(goal.structural());
    assertFalse(TaskGoal.outputText("Привет").structural());
  }

  @Test void rejectsGoalsThatCannotBeEnforced() throws Exception {
    var inconsistent = new TaskGoal(TaskGoal.Kind.FIXED_ARITHMETIC, "*", List.of(new BigDecimal(4), new BigDecimal(6)), "25\n", null, List.of());
    assertTrue(assertThrows(InvalidGeneratedContentException.class, () -> inconsistent.validate(Language.PYTHON, "")).getMessage().contains("does not contain"));
    var floorInJava = new TaskGoal(TaskGoal.Kind.FIXED_ARITHMETIC, "//", List.of(new BigDecimal(7), new BigDecimal(2)), "3\n", null, List.of());
    assertThrows(InvalidGeneratedContentException.class, () -> floorInJava.validate(Language.JAVA, ""));
    var function = new TaskGoal(TaskGoal.Kind.FUNCTION_BEHAVIOR, null, List.of(), null, "area", List.of());
    assertTrue(assertThrows(InvalidGeneratedContentException.class, () -> function.validate(Language.PYTHON, "assert solution.area(2, 3) == 6")).getMessage().contains("at least three"));
    function.validate(Language.PYTHON, "assert area(1, 1) == 1\nassert area(2, 3) == 6\nassert area(0, 5) == 0");
    assertThrows(InvalidGeneratedContentException.class, () -> TaskGoal.parse(json.readTree("{\"kind\":\"MAGIC\"}")));
    assertThrows(InvalidGeneratedContentException.class, () -> TaskGoal.parse(null));
  }

  @Test void computesResultsWithEachLanguagesSemantics() {
    assertEquals("3", arithmetic("//", 7, 2).result(Language.PYTHON));
    assertEquals("3.5", arithmetic("/", 7, 2).result(Language.PYTHON));
    assertEquals("6.0", arithmetic("/", 24, 4).result(Language.PYTHON));
    assertEquals("3", arithmetic("/", 7, 2).result(Language.JAVA));
    assertEquals("2", arithmetic("%", -7, 3).result(Language.PYTHON));
    assertEquals("-1", arithmetic("%", -7, 3).result(Language.JAVA));
    assertEquals("1024", arithmetic("**", 2, 10).result(Language.PYTHON));
  }

  @Test void platformWritesTheBypassesForFixedArithmetic() {
    var mutants = TICKETS.platformMutants(Language.PYTHON);
    var sources = mutants.stream().map(TaskGoal.Mutant::source).toList();
    assertTrue(sources.contains("print(24)\n"));
    assertTrue(sources.contains("print(12 * 2)\n"));
    assertTrue(sources.contains("print((4 * 6) + 1)\n"));
    assertTrue(sources.contains("print(4 * 6, end=\"\")\n"));
    assertEquals(List.of(new BigDecimal(4), new BigDecimal(4)), arithmetic("+", 3, 5).otherOperands());
    assertTrue(TICKETS.platformMutants(Language.JAVA).getFirst().source().contains("System.out.println(24);"));
  }

  /** Runs the generated AST check exactly like Piston: fixed entry point, the task's checks, the student's file. */
  @Test void pythonCheckAcceptsTheCalculationAndRejectsBypasses(@TempDir Path dir) throws Exception {
    Assumptions.assumeTrue(pythonAvailable(), "python3 is not installed");
    String checks = """
        import contextlib
        import io


        def run_checks():
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                import solution  # noqa: F401
            assert buffer.getvalue() == "24\\n", "Неверный вывод"
        """ + TICKETS.pythonCheck();
    assertTrue(passes(dir, checks, "print(4 * 6)\n"));
    assertTrue(passes(dir, checks, "print(6 * 4)\n"));
    assertTrue(passes(dir, checks, "price = 6\ncount = 4\nprint(count * price)\n"));
    assertFalse(passes(dir, checks, "print(24)\n"), "the ready answer is not a calculation");
    assertFalse(passes(dir, checks, "print(12 * 2)\n"), "other numbers giving the same answer");
    assertFalse(passes(dir, checks, "print(2 * 2 * 6)\n"));
    assertFalse(passes(dir, checks, "price = 6\nprice = 3\nprint(4 * price * 2)\n"));
    assertFalse(passes(dir, checks, "print((4 * 6) + 1)\n"), "right calculation, wrong output is caught by the task's own check");
  }

  @Test void pythonCheckEnforcesRequiredConstructs(@TempDir Path dir) throws Exception {
    Assumptions.assumeTrue(pythonAvailable(), "python3 is not installed");
    var loop = new TaskGoal(TaskGoal.Kind.CONSTRUCT, null, List.of(), null, null, List.of("for"));
    String checks = """
        import contextlib
        import io


        def run_checks():
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                import solution  # noqa: F401
            assert buffer.getvalue() == "1\\n2\\n3\\n", "Неверный вывод"
        """ + loop.pythonCheck();
    assertTrue(passes(dir, checks, "for i in range(1, 4):\n    print(i)\n"));
    assertFalse(passes(dir, checks, "print(1)\nprint(2)\nprint(3)\n"), "same output without the loop the task asks for");
  }

  private static TaskGoal arithmetic(String op, long a, long b) {
    return new TaskGoal(TaskGoal.Kind.FIXED_ARITHMETIC, op, List.of(BigDecimal.valueOf(a), BigDecimal.valueOf(b)), "", null, List.of());
  }

  private static boolean pythonAvailable() {
    try { return new ProcessBuilder("python3", "--version").start().waitFor(10, TimeUnit.SECONDS); } catch (Exception e) { return false; }
  }

  private static boolean passes(Path base, String checks, String solution) throws Exception {
    Path dir = Files.createTempDirectory(base, "job");
    Files.writeString(dir.resolve("main.py"), PistonCodeRunner.PYTHON_ENTRY.strip() + "\n", StandardCharsets.UTF_8);
    Files.writeString(dir.resolve("test_solution.py"), checks, StandardCharsets.UTF_8);
    Files.writeString(dir.resolve("solution.py"), solution, StandardCharsets.UTF_8);
    Process process = new ProcessBuilder("python3", "main.py").directory(dir.toFile()).redirectErrorStream(false).start();
    process.getOutputStream().write("__ADAPTIVE_PASS_test__\n".getBytes(StandardCharsets.UTF_8)); process.getOutputStream().close();
    String out = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
    process.waitFor(20, TimeUnit.SECONDS);
    List<String> lines = out.lines().map(String::strip).filter(l -> !l.isEmpty()).toList();
    return process.exitValue() == 0 && !lines.isEmpty() && lines.getLast().equals("__ADAPTIVE_PASS_test__");
  }
}
