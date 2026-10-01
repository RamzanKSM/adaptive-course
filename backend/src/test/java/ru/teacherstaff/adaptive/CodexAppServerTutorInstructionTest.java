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
}
