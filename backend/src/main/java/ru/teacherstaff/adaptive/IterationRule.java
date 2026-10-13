package ru.teacherstaff.adaptive;

/**
 * The iteration rule of a topic. Live crediting (ApiController.credit, also when a revoke replays a topic) and the
 * progress analytics history both go through it, so the teacher's charts cannot drift from what students were credited.
 * <p>A topic is practised in iterations of ApiController.ITERATION_TASKS tasks (3, 2, 1). The first iteration may happen
 * in any lesson; the second only in lesson N+1 and the third only in lesson N+3, where N is the lesson of the first
 * (per-language lesson numbers). Credited tasks count per lesson: an iteration needs its tasks within one lesson.
 */
final class IterationRule {
  private IterationRule() {}

  /** Practice of one topic: completed iterations, credited tasks towards the next one, lesson number of the first iteration. */
  record Topic(int completed, int successes, Integer firstLesson) {
    static final Topic NEW = new Topic(0, 0, null);
    boolean mastered() { return completed >= ApiController.ITERATION_TASKS.length; }
  }

  /**
   * The topic after one more of its tasks is credited in a lesson. solvedInLesson — distinct credited tasks of the topic
   * passed in this lesson, this one included; iterationInLesson — the lesson has already completed an iteration of it.
   * Short of the iteration's tasks, the lesson's count is the progress of the current iteration; with enough tasks in a
   * lesson where an iteration is due, the iteration completes; otherwise nothing changes.
   */
  static Topic credit(Topic topic, int solvedInLesson, int lessonNumber, boolean iterationInLesson) {
    if (solvedInLesson < ApiController.iterationTasks(topic.completed())) return new Topic(topic.completed(), solvedInLesson, topic.firstLesson());
    if (!due(topic, lessonNumber) || iterationInLesson) return topic;
    return new Topic(topic.completed() + 1, 0, topic.firstLesson() == null ? lessonNumber : topic.firstLesson());
  }

  /** Whether this lesson may complete the topic's next iteration (a schedule without the first lesson is never due). */
  static boolean due(Topic topic, int lessonNumber) {
    Integer first = topic.firstLesson();
    return topic.completed() == 0 || (topic.completed() == 1 && first != null && lessonNumber == first + 1) || (topic.completed() == 2 && first != null && lessonNumber == first + 3);
  }

  /** Share of the topic done, 0..1, as the student's topic bar (game.ts skillPercent, unrounded): 1 when mastered. */
  static double share(int completed, int successes) {
    if (completed >= ApiController.ITERATION_TASKS.length) return 1;
    int done = 0, all = 0;
    for (int i = 0; i < ApiController.ITERATION_TASKS.length; i++) { all += ApiController.ITERATION_TASKS[i]; if (i < completed) done += ApiController.ITERATION_TASKS[i]; }
    return (done + Math.min(successes, ApiController.iterationTasks(completed))) / (double) all;
  }
}
