package ru.teacherstaff.adaptive;

import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.util.List;
import java.util.Optional;

/** Generates reusable shared learning content. Implementations must never return a task without its hidden harness. */
interface LearningContentGenerator {
  GeneratedTask generateTask(long studentId, String skillCode);
  Optional<GeneratedExplanation> generateExplanation(long studentId, String skillCode);
}

record GeneratedTask(String skillCode, String title, String statement, String starterCode,
                     String testSource, String testFileName, String referenceSolutionSource,
                     List<String> targetSkillCodes, List<String> prerequisiteSkillCodes) {}
record GeneratedExplanation(String skillCode, String content) {}

class UnavailableLearningContentGenerator implements LearningContentGenerator {
  @Override public GeneratedTask generateTask(long studentId,String skillCode) { throw new LlmUnavailableException("LLM content generation is unavailable"); }
  @Override public Optional<GeneratedExplanation> generateExplanation(long studentId,String skillCode) { return Optional.empty(); }
}

@Configuration
class LearningContentGeneratorConfiguration {
  @Bean
  @ConditionalOnMissingBean(LearningContentGenerator.class)
  LearningContentGenerator unavailableLearningContentGenerator() { return new UnavailableLearningContentGenerator(); }
}
