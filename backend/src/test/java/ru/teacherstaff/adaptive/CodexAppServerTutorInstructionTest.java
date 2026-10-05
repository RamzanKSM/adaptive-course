package ru.teacherstaff.adaptive;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CodexAppServerTutorInstructionTest {
  @Test void versionsStudentThreadsAndWithholdsAnswersAlways() {
    assertEquals("account-a:tutor-v3", CodexAppServerTutor.tutorConversationNamespace("account-a"));
    String instructions = CodexAppServerTutor.tutorInstructions();
    assertTrue(instructions.contains("строковый литерал"));
    assertTrue(instructions.contains("даже если задача пройдена"));
    assertTrue(instructions.contains("обратиться к живому преподавателю"));
  }

  @Test void sumsTokenUsageOfEveryModelRequestInATurn() throws Exception {
    var json=new com.fasterxml.jackson.databind.ObjectMapper();
    var usage=new CodexAppServerTutor.TokenUsage();
    usage.add(json.readTree("{\"inputTokens\":100,\"cachedInputTokens\":40,\"outputTokens\":20,\"reasoningOutputTokens\":5,\"totalTokens\":120}"));
    usage.add(json.readTree("{\"inputTokens\":30,\"cachedInputTokens\":0,\"outputTokens\":10,\"reasoningOutputTokens\":0,\"totalTokens\":40}"));
    usage.add(null);
    assertTrue(usage.seen); assertEquals(130,usage.input); assertEquals(40,usage.cached); assertEquals(30,usage.output); assertEquals(5,usage.reasoning); assertEquals(160,usage.total);
    assertTrue(!CodexAppServerTutor.tutorInstructions(Language.PYTHON).contains("solution.py"));
  }
}
