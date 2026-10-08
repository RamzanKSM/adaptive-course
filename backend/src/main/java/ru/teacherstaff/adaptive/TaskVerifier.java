package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import java.util.ArrayList;
import java.util.List;

/**
 * Runs solutions with the task's goal enforced and decides whether a generated task is good enough to store.
 * A task is stored only if its reference solution passes and every wrong solution — the generator's own and the
 * platform's — fails a real check (not a crash or a compile error). Weak tests that would accept print(12 * 2)
 * for "4 tickets at 6 roubles" are rejected here, before any student sees the task.
 */
@Component
class TaskVerifier {
  private static final Logger log = LoggerFactory.getLogger(TaskVerifier.class);
  /** Wrong solutions that must be rejected by the checks themselves, so the checks provably test something. */
  static final int MIN_MEANINGFUL_WRONG_SOLUTIONS = 2;
  private final PistonCodeRunner runner;
  private final ObjectMapper json;

  TaskVerifier(PistonCodeRunner runner, ObjectMapper json) { this.runner = runner; this.json = json; }

  /** cases: the recorded test cases of a function or input/output task; empty for the other kinds. */
  record Verified(String testSource, String goalJson, List<TestCases.Case> cases) {
    Verified(String testSource, String goalJson) { this(testSource, goalJson, List.of()); }
  }

  /** A solution against a sample of the task's recorded cases: every example and some hidden cases, in one run. */
  PistonCodeRunner.Run runCases(Language language, String source, TaskGoal goal, List<TestCases.Case> cases) {
    return runner.run(language, source, TestCases.checker(language, goal, cases));
  }

  /**
   * A «calculate» task checked by its output only; whether the answer was really calculated is decided separately
   * (by the LLM, or by the syntax tree when the LLM cannot be asked). Required constructs are still checked.
   */
  PistonCodeRunner.Run runOutputOnly(Language language, String source, String testSource, TaskGoal goal) {
    return run(language, source, testSource, goal == null ? null : goal.withoutCalculationCheck());
  }

  /** A student submission (or any candidate) against a stored task: goal checks first, then the task's own checks. */
  PistonCodeRunner.Run run(Language language, String source, String testSource, String goalJson) {
    return run(language, source, testSource, TaskGoal.fromJson(json, goalJson));
  }

  PistonCodeRunner.Run run(Language language, String source, String testSource, TaskGoal goal) {
    if (goal == null || !goal.structural()) return runner.run(language, source, testSource);
    if (language == Language.JAVA) {
      String problem = JavaStructureCheck.problem(goal, source);
      if (problem != null) return new PistonCodeRunner.Run(false, problem, PistonCodeRunner.Outcome.CHECK_FAILED);
      return runner.run(language, source, testSource);
    }
    return runner.run(language, source, testSource + goal.pythonCheck());
  }

  /** Throws InvalidGeneratedContentException with the precise reason when the task must not be stored. */
  Verified verify(Language language, GeneratedTask task) {
    TaskGoal goal = TaskGoal.parse(task.goal());
    goal.validate(language, task.testSource());
    if (TestCases.usesCases(goal)) return verifyCases(language, task, goal);
    PistonCodeRunner.Run reference = run(language, task.referenceSolutionSource(), task.testSource(), goal);
    if (reference.outcome() == PistonCodeRunner.Outcome.UNAVAILABLE) throw new LlmUnavailableException("Piston is unavailable for task verification");
    if (!reference.passed()) throw new InvalidGeneratedContentException("reference solution failed its own checks: " + abbreviate(reference.output()));

    List<TaskGoal.Mutant> wrong = new ArrayList<>(task.wrongSolutions());
    wrong.addAll(goal.platformMutants(language));
    int meaningful = 0;
    for (TaskGoal.Mutant mutant : wrong) {
      if (mutant.source() == null || mutant.source().isBlank()) continue;
      PistonCodeRunner.Run result = run(language, mutant.source(), task.testSource(), goal);
      switch (result.outcome()) {
        case PASSED -> throw new InvalidGeneratedContentException("checks accept a wrong solution (" + mutant.description() + "): " + abbreviate(mutant.source()));
        case CHECK_FAILED -> meaningful++;
        case UNAVAILABLE -> throw new LlmUnavailableException("Piston is unavailable for task verification");
        default -> log.debug("Wrong solution '{}' did not reach the checks: {}", mutant.description(), result.outcome());
      }
    }
    if (meaningful < MIN_MEANINGFUL_WRONG_SOLUTIONS)
      throw new InvalidGeneratedContentException("only " + meaningful + " wrong solution(s) were rejected by the checks; need " + MIN_MEANINGFUL_WRONG_SOLUTIONS + " that run and fail a check");
    log.info("Task verified: goal={} reference passed, {} of {} wrong solutions rejected by checks", goal.kind(), meaningful, wrong.size());
    return new Verified(task.testSource(), goal.toJson(json));
  }

  /**
   * Function and input/output tasks: the answers come from running the reference solution on the generator's inputs,
   * the checks are the platform's template, and the wrong solutions must fail on some case.
   */
  private Verified verifyCases(Language language, GeneratedTask task, TaskGoal goal) {
    TestCases.validateInputs(task.testInputs());
    PistonCodeRunner.Raw recorded = runner.runRaw(language, task.referenceSolutionSource(), TestCases.recorder(language, goal, task.testInputs()));
    if (!recorded.ok() && recorded.stdout().isBlank()) {
      if (recorded.error().contains("Piston execution service is unavailable")) throw new LlmUnavailableException("Piston is unavailable for task verification");
      throw new InvalidGeneratedContentException("reference solution does not run with the test inputs: " + abbreviate(recorded.error()));
    }
    List<TestCases.Case> cases = TestCases.recorded(task.testInputs(), recorded.stdout());
    List<TaskGoal.Mutant> wrong = new ArrayList<>(task.wrongSolutions());
    if (goal.kind() == TaskGoal.Kind.IO_BEHAVIOR) {
      String example = cases.stream().filter(TestCases.Case::isPublic).findFirst().map(TestCases.Case::expected).orElse("");
      wrong.add(new TaskGoal.Mutant("prints the first example's answer for any input", TaskGoal.printText(language, example)));
    }
    int meaningful = 0;
    for (TaskGoal.Mutant mutant : wrong) {
      if (mutant.source() == null || mutant.source().isBlank()) continue;
      PistonCodeRunner.Run result = runCases(language, mutant.source(), goal, cases);
      switch (result.outcome()) {
        case PASSED -> throw new InvalidGeneratedContentException("test cases accept a wrong solution (" + mutant.description() + "): " + abbreviate(mutant.source()));
        case CHECK_FAILED -> meaningful++;
        case UNAVAILABLE -> throw new LlmUnavailableException("Piston is unavailable for task verification");
        default -> log.debug("Wrong solution '{}' did not reach the checks: {}", mutant.description(), result.outcome());
      }
    }
    if (meaningful < MIN_MEANINGFUL_WRONG_SOLUTIONS)
      throw new InvalidGeneratedContentException("only " + meaningful + " wrong solution(s) were rejected by the test cases; need " + MIN_MEANINGFUL_WRONG_SOLUTIONS);
    log.info("Task verified: goal={} {} recorded cases ({} public), {} of {} wrong solutions rejected", goal.kind(), cases.size(), cases.stream().filter(TestCases.Case::isPublic).count(), meaningful, wrong.size());
    return new Verified(TestCases.checker(language, goal, cases), goal.toJson(json), cases);
  }

  private static String abbreviate(String value) { String flat = value == null ? "" : value.replaceAll("\\s+", " ").strip(); return flat.length() <= 300 ? flat : flat.substring(0, 300) + "…"; }
}
