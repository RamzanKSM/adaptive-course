package ru.teacherstaff.adaptive;

/** Server-derived context sent to the teacher adapter; never populated from client input. */
record TutorContext(long lessonId, int lessonNumber, String skillCode, String skillTitle,
                    Long taskId, String taskTitle, String taskStatement,
                    String latestSubmissionSource, Boolean latestSubmissionPassed, String latestSubmissionOutput) {}
