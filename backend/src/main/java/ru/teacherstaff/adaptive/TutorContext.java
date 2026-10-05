package ru.teacherstaff.adaptive;

/** Context for the teacher adapter. Only currentEditorSource is an untrusted client snapshot; the rest is server-derived. */
record TutorContext(Language language, long lessonId, int lessonNumber, String skillCode, String skillTitle,
                    Long taskId, String taskTitle, String taskStatement,
                    String currentEditorSource, String latestSubmissionSource,
                    Boolean latestSubmissionPassed, String latestSubmissionOutput) {}
