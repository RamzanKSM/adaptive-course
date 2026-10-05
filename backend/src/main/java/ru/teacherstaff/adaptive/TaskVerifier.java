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

  record Verified(String testSource, String goalJson) {}

  /** A student submission (or any candidate) against a stored task: goal checks first, then the task's own checks. */
  PistonCodeRunner.Run run(Language language, String source, String testSource, String goalJson) {
    return run(language, source, testSource, TaskGoal.fromJson(json, goalJson));
  }

  PistonCodeRunner.Run run(Language language, String source, String testSource, TaskGoal goal) {
    if (goal == null || !goal.structural()) return runner.run(language, source, testSource);
    if (language == Language.JAVA) {
      String problem = JavaStructureCheck.problem(goal, source);
      if (problem != null) return new PistonCodeRunner.Run(false, "Неверный подход: " + problem + ".", PistonCodeRunner.Outcome.CHECK_FAILED);
      return runner.run(language, source, testSource);
    }
    return runner.run(language, source, testSource + goal.pythonCheck());
  }

  /** Throws InvalidGeneratedContentException with the precise reason when the task must not be stored. */
  Verified verify(Language language, GeneratedTask task) {
    TaskGoal goal = TaskGoal.parse(task.goal());
    goal.validate(language, task.testSource());
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

  private static String abbreviate(String value) { String flat = value == null ? "" : value.replaceAll("\\s+", " ").strip(); return flat.length() <= 300 ? flat : flat.substring(0, 300) + "…"; }
}
