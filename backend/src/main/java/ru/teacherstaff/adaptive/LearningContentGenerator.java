package ru.teacherstaff.adaptive;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.util.List;
import java.util.Optional;

/** Generates reusable shared learning content. Implementations must never return a task without its hidden harness. */
interface LearningContentGenerator {
  /** Bump when the explanation prompt changes so cached LLM explanations are regenerated. */
  int EXPLANATION_PROMPT_VERSION = 3;
  /** Bump when task verification gets stricter; tasks accepted by an older version are re-verified at startup. */
  int TASK_QUALITY_VERSION = 2;
  GeneratedTask generateTask(long studentId, ContentBrief brief);
  Optional<GeneratedExplanation> generateExplanation(long studentId, ContentBrief brief);
  /** New goal, checks, reference and wrong solutions for an existing task whose statement stays unchanged. */
  default GeneratedTask repairTask(ContentBrief brief, ExistingTask task) { throw new LlmUnavailableException("LLM content generation is unavailable"); }
  /**
   * A «calculate» task whose output is already right: did the program calculate the answer from the statement's
   * numbers, or print it ready-made? The syntax tree answers when the LLM cannot. A rejection always explains why.
   */
  default SolutionReview checkCalculation(long studentId, ReviewRequest request) { throw new LlmUnavailableException("LLM review is unavailable"); }
  /** Whether background work (task repair) may call the LLM now; student-triggered calls check the student's own access. */
  default boolean available() { return false; }
}

/** A stored task as the student sees it; repair keeps its statement and replaces only what checks it. */
record ExistingTask(long id, String title, String statement, String starterCode, String testSource) {}

/**
 * Server-derived course context for generation, so content stays inside the topic, builds on what the
 * student has already studied and matches the requested step of the iteration (difficulty 1..3).
 */
record ContentBrief(Language language, String skillCode, String skillTitle, int blockNo, int difficulty, int iteration,
                    List<String> earlierSkills, List<String> diagnosticExamples, List<String> existingTasks, String explanation, boolean hard) {
  ContentBrief(Language language, String skillCode, String skillTitle, int blockNo, int difficulty, int iteration,
               List<String> earlierSkills, List<String> diagnosticExamples, List<String> existingTasks, String explanation) {
    this(language, skillCode, skillTitle, blockNo, difficulty, iteration, earlierSkills, diagnosticExamples, existingTasks, explanation, false);
  }
}

/** What the reviewer sees for a «calculate» task: the task, what it teaches (operation and numbers) and the solution. */
record ReviewRequest(Language language, String skillCode, String title, String statement, String source, String operation, String operands) {}

/** The reviewer's verdict. A rejection carries the reason: summary plus the concrete problems with hints. */
record SolutionReview(boolean accepted, String summary, List<Issue> issues) {
  record Issue(Integer line, String problem, String hint) {}
  SolutionReview { issues = issues == null ? List.of() : List.copyOf(issues); }
  /** Plain text for the submission history and older clients. */
  String text() {
    StringBuilder text = new StringBuilder(summary == null ? "" : summary.strip());
    for (Issue issue : issues) {
      text.append("\n\n• ").append(issue.line() == null ? "" : "Строка " + issue.line() + ": ").append(issue.problem());
      if (issue.hint() != null && !issue.hint().isBlank()) text.append("\n  Подсказка: ").append(issue.hint());
    }
    return text.toString().strip();
  }
  java.util.Map<String, Object> view() {
    var list = new java.util.ArrayList<java.util.Map<String, Object>>();
    for (Issue issue : issues) { var m = new java.util.LinkedHashMap<String, Object>(); m.put("line", issue.line()); m.put("problem", issue.problem()); m.put("hint", issue.hint()); list.add(m); }
    var view = new java.util.LinkedHashMap<String, Object>(); view.put("accepted", accepted); view.put("summary", summary); view.put("issues", list);
    return view;
  }
}

/**
 * goal states what the task teaches (see TaskGoal); wrongSolutions are plausible bypasses that the checks must reject.
 * Both are required: a task is stored only after its reference passes and every wrong solution fails a check.
 * testInputs: for function and input/output tasks, the inputs the platform turns into test cases (see TestCases);
 * testSource is then unused.
 */
record GeneratedTask(String skillCode, String title, String statement, String starterCode,
                     String testSource, String testFileName, String referenceSolutionSource,
                     List<String> targetSkillCodes, List<String> prerequisiteSkillCodes,
                     JsonNode goal, List<TaskGoal.Mutant> wrongSolutions, List<TestCases.Input> testInputs) {
  GeneratedTask {
    wrongSolutions = wrongSolutions == null ? List.of() : List.copyOf(wrongSolutions);
    testInputs = testInputs == null ? List.of() : List.copyOf(testInputs);
  }
  /** A task whose checks are written by the generator (output, «calculate» and construct tasks). */
  GeneratedTask(String skillCode, String title, String statement, String starterCode, String testSource, String testFileName, String referenceSolutionSource,
                List<String> targetSkillCodes, List<String> prerequisiteSkillCodes, JsonNode goal, List<TaskGoal.Mutant> wrongSolutions) {
    this(skillCode, title, statement, starterCode, testSource, testFileName, referenceSolutionSource, targetSkillCodes, prerequisiteSkillCodes, goal, wrongSolutions, List.of());
  }
}
record GeneratedExplanation(String skillCode, String content) {}

class UnavailableLearningContentGenerator implements LearningContentGenerator {
  @Override public GeneratedTask generateTask(long studentId,ContentBrief brief) { throw new LlmUnavailableException("LLM content generation is unavailable"); }
  @Override public Optional<GeneratedExplanation> generateExplanation(long studentId,ContentBrief brief) { return Optional.empty(); }
}

@Configuration
class LearningContentGeneratorConfiguration {
  @Bean
  @ConditionalOnMissingBean(LearningContentGenerator.class)
  LearningContentGenerator unavailableLearningContentGenerator() { return new UnavailableLearningContentGenerator(); }
}
