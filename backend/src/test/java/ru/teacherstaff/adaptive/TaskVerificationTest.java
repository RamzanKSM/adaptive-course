package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

class TaskVerificationTest {
  private final ObjectMapper json = new ObjectMapper();
  private static final TaskGoal TICKETS = new TaskGoal(TaskGoal.Kind.FIXED_ARITHMETIC, "*", List.of(new BigDecimal(4), new BigDecimal(6)), "24\n", null, List.of());
  private static final String TICKETS_JAVA = "public class Solution {\n    public static void main(String[] args) {\n        System.out.println(4 * 6);\n    }\n}\n";

  @Test void javaTreeCheckRequiresTheOperandsFromTheStatement() {
    assertNull(JavaStructureCheck.problem(TICKETS, TICKETS_JAVA));
    assertNull(JavaStructureCheck.problem(TICKETS, main("System.out.println(6 * 4);")));
    assertNull(JavaStructureCheck.problem(TICKETS, main("int price = 6; int count = 4; System.out.println(count * price);")));
    assertNull(JavaStructureCheck.problem(TICKETS, main("System.out.println(\"Итого: \" + (4 * 6));")));
    assertNotNull(JavaStructureCheck.problem(TICKETS, main("System.out.println(24);")));
    assertNotNull(JavaStructureCheck.problem(TICKETS, main("System.out.println(12 * 2);")));
    assertNotNull(JavaStructureCheck.problem(TICKETS, main("int price = 6; price = 3; System.out.println(4 * price * 2);")));
    assertNull(JavaStructureCheck.problem(TICKETS, "public class Solution { broken"), "syntax errors are left to the compiler");
  }

  @Test void javaTreeCheckFindsRequiredConstructs() {
    var loop = new TaskGoal(TaskGoal.Kind.CONSTRUCT, null, List.of(), null, null, List.of("for"));
    assertNull(JavaStructureCheck.problem(loop, main("for (int i = 1; i <= 3; i++) System.out.println(i);")));
    assertTrue(JavaStructureCheck.problem(loop, main("System.out.println(1); System.out.println(2);")).contains("цикл for"));
    var assignment = new TaskGoal(TaskGoal.Kind.CONSTRUCT, null, List.of(), null, null, List.of("assignment"));
    assertNotNull(JavaStructureCheck.problem(assignment, main("System.out.println(5);")), "the String[] args parameter is not an assignment");
    assertNull(JavaStructureCheck.problem(assignment, main("int x = 5; System.out.println(x);")));
  }

  /** The bug from the field: checks that compare only the printed number let print(12 * 2) through. */
  @Test void rejectsTaskWhoseChecksOnlyCompareOutput() {
    PistonCodeRunner runner = mock(PistonCodeRunner.class);
    when(runner.run(any(Language.class), anyString(), anyString())).thenReturn(new PistonCodeRunner.Run(true, "ok"));
    var verifier = new TaskVerifier(runner, json);
    var error = assertThrows(InvalidGeneratedContentException.class, () -> verifier.verify(Language.JAVA, task(TICKETS, TICKETS_JAVA, List.of())));
    assertTrue(error.getMessage().contains("checks accept a wrong solution"), error.getMessage());
  }

  @Test void acceptsTaskWhenReferencePassesAndEveryBypassFailsAChecks() {
    PistonCodeRunner runner = mock(PistonCodeRunner.class);
    // Checks that compare exact output: only "24\n" passes.
    when(runner.run(any(Language.class), anyString(), anyString())).thenAnswer(call -> {
      String source = call.getArgument(1);
      boolean exact = source.contains("System.out.println(4 * 6);") || source.contains("System.out.println(6 * 4);");
      return exact ? new PistonCodeRunner.Run(true, "ok") : new PistonCodeRunner.Run(false, "Неверный вывод программы.");
    });
    var verifier = new TaskVerifier(runner, json);
    var verified = verifier.verify(Language.JAVA, task(TICKETS, TICKETS_JAVA, List.of(new TaskGoal.Mutant("prints 25", main("System.out.println(25);")))));
    assertEquals(TICKETS, TaskGoal.fromJson(json, verified.goalJson()));
    // print(24) and print(12 * 2) never reach Piston: the tree check rejects them on the backend.
    verify(runner, never()).run(any(Language.class), contains("println(24)"), anyString());
    verify(runner, never()).run(any(Language.class), contains("12 * 2"), anyString());
    var attempt = verifier.run(Language.JAVA, main("System.out.println(12 * 2);"), "checks", verified.goalJson());
    assertFalse(attempt.passed()); assertEquals(PistonCodeRunner.Outcome.CHECK_FAILED, attempt.outcome());
    assertTrue(attempt.output().startsWith("Неверный подход"));
  }

  @Test void rejectsWhenReferenceFailsOrWrongSolutionsOnlyCrash() {
    PistonCodeRunner failing = mock(PistonCodeRunner.class);
    when(failing.run(any(Language.class), anyString(), anyString())).thenReturn(new PistonCodeRunner.Run(false, "Неверный вывод программы."));
    assertTrue(assertThrows(InvalidGeneratedContentException.class, () -> new TaskVerifier(failing, json).verify(Language.JAVA, task(TICKETS, TICKETS_JAVA, List.of()))).getMessage().contains("reference"));

    var function = new TaskGoal(TaskGoal.Kind.FUNCTION_BEHAVIOR, null, List.of(), null, "area", List.of());
    PistonCodeRunner crashing = mock(PistonCodeRunner.class);
    when(crashing.run(any(Language.class), anyString(), anyString())).thenAnswer(call -> ((String) call.getArgument(1)).contains("WRONG")
        ? new PistonCodeRunner.Run(false, "Синтаксическая ошибка в коде Python:\n...") : new PistonCodeRunner.Run(true, "ok"));
    var crashOnly = new GeneratedTask("PY_FUNCTION_BASIC", "t", "s", "", "def run_checks():\n    assert area(1) and area(2) and area(3)\n", "test_solution.py", "def area(x): return x",
        List.of("PY_FUNCTION_BASIC"), List.of(), json.valueToTree(java.util.Map.of("kind", "FUNCTION_BEHAVIOR", "functionName", "area")),
        List.of(new TaskGoal.Mutant("a", "WRONG ("), new TaskGoal.Mutant("b", "WRONG )")));
    assertTrue(assertThrows(InvalidGeneratedContentException.class, () -> new TaskVerifier(crashing, json).verify(Language.PYTHON, crashOnly)).getMessage().contains("wrong solution(s) were rejected"));
  }

  @Test void pythonSubmissionsRunWithTheGoalCheckAppended() {
    PistonCodeRunner runner = mock(PistonCodeRunner.class);
    when(runner.run(any(Language.class), anyString(), anyString())).thenReturn(new PistonCodeRunner.Run(true, "ok"));
    new TaskVerifier(runner, json).run(Language.PYTHON, "print(4 * 6)", "def run_checks():\n    pass\n", TICKETS.toJson(json));
    verify(runner).run(eq(Language.PYTHON), eq("print(4 * 6)"), contains("Platform check (task goal)"));
    new TaskVerifier(runner, json).run(Language.PYTHON, "print('x')", "checks", (String) null);
    verify(runner).run(Language.PYTHON, "print('x')", "checks");
  }

  @Test void diagnosticConfirmsATopicOnlyWithEnoughEvidence() {
    assertTrue(DiagnosticProfile.confirmed(2, 2, 3, 8), "two of two on the topic, regardless of the block");
    assertFalse(DiagnosticProfile.confirmed(1, 2, 8, 8));
    assertTrue(DiagnosticProfile.confirmed(1, 1, 4, 5), "a single right answer counts when the block is at least 80%");
    assertFalse(DiagnosticProfile.confirmed(1, 1, 3, 5), "a single right answer in a weak block may be a guess");
    assertFalse(DiagnosticProfile.confirmed(0, 1, 5, 5));
    assertFalse(DiagnosticProfile.confirmed(0, 0, 0, 0));
  }

  private GeneratedTask task(TaskGoal goal, String reference, List<TaskGoal.Mutant> wrong) {
    try {
      return new GeneratedTask("ARITHMETIC_BASIC", "Билеты", "Посчитай стоимость 4 билетов по 6 рублей умножением.", "", "public class TestHarness { public static void main(String[] a) { System.out.print(\"{{PASS_MARKER}}\"); } }",
          "TestHarness.java", reference, List.of("ARITHMETIC_BASIC"), List.of(), json.readTree(goal.toJson(json)), wrong);
    } catch (Exception e) { throw new IllegalStateException(e); }
  }

  private static String main(String body) { return "public class Solution {\n    public static void main(String[] args) {\n        " + body + "\n    }\n}\n"; }
}
