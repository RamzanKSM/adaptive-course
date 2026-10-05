package ru.teacherstaff.adaptive;

import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.util.List;
import java.util.Optional;

/** Generates reusable shared learning content. Implementations must never return a task without its hidden harness. */
interface LearningContentGenerator {
  /** Bump when the explanation prompt changes so cached LLM explanations are regenerated. */
  int EXPLANATION_PROMPT_VERSION = 2;
  GeneratedTask generateTask(long studentId, ContentBrief brief);
  Optional<GeneratedExplanation> generateExplanation(long studentId, ContentBrief brief);
}

/**
 * Server-derived course context for generation, so content stays inside the topic, builds on what the
 * student has already studied and matches the requested step of the iteration (difficulty 1..3).
 */
record ContentBrief(Language language, String skillCode, String skillTitle, int blockNo, int difficulty, int iteration,
                    List<String> earlierSkills, List<String> diagnosticExamples, List<String> existingTasks, String explanation) {}

record GeneratedTask(String skillCode, String title, String statement, String starterCode,
                     String testSource, String testFileName, String referenceSolutionSource,
                     List<String> targetSkillCodes, List<String> prerequisiteSkillCodes) {}
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
