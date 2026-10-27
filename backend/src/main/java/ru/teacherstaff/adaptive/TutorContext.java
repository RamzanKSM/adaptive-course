package ru.teacherstaff.adaptive;

/**
 * Context for the teacher adapter. retake — the task belongs to «Повторить тему» (a closed topic the student chose to practise again).
 * currentEditorSource and currentConsole (what the student's last «Запустить» or
 * check printed, as shown on screen) are untrusted client snapshots; the rest is server-derived.
 */
record TutorContext(Language language, long lessonId, int lessonNumber, String skillCode, String skillTitle,
                    Long taskId, String taskTitle, String taskStatement,
                    String currentEditorSource, String latestSubmissionSource,
                    Boolean latestSubmissionPassed, String latestSubmissionOutput,
                    String latestSubmissionConsole, String currentConsole, boolean retake) {}
