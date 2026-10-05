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
                    List<String> earlierSkills, List<String> diagnosticExamples, List<String> existingTasks, String explanation) {}

/**
 * goal states what the task teaches (see TaskGoal); wrongSolutions are plausible bypasses that the checks must reject.
 * Both are required: a task is stored only after its reference passes and every wrong solution fails a check.
 */
record GeneratedTask(String skillCode, String title, String statement, String starterCode,
                     String testSource, String testFileName, String referenceSolutionSource,
                     List<String> targetSkillCodes, List<String> prerequisiteSkillCodes,
                     JsonNode goal, List<TaskGoal.Mutant> wrongSolutions) {
  GeneratedTask {
    wrongSolutions = wrongSolutions == null ? List.of() : List.copyOf(wrongSolutions);
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
