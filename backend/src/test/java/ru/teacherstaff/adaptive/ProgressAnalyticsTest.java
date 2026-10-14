package ru.teacherstaff.adaptive;

import org.junit.jupiter.api.Test;
import java.time.LocalDate;
import java.util.EnumMap;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.*;

/** The pure rules behind the progress analytics: the iteration rule shared with live crediting, the forecast and the session course. */
class ProgressAnalyticsTest {
  static final LocalDate TODAY = LocalDate.of(2030, 3, 14);
  static final LocalDate IN_TEN_WEEKS = TODAY.plusDays(70);

  @Test void iterationsFollowTheLessonScheduleAndCountOncePerLesson() {
    var topic = IterationRule.Topic.NEW;
    topic = IterationRule.credit(topic, 1, 4, false); assertEquals(new IterationRule.Topic(0, 1, null), topic);
    topic = IterationRule.credit(topic, 2, 4, false); assertEquals(new IterationRule.Topic(0, 2, null), topic);
    topic = IterationRule.credit(topic, 3, 4, false); assertEquals(new IterationRule.Topic(1, 0, 4), topic, "three tasks in one lesson: the first iteration, in any lesson");
    assertEquals(topic, IterationRule.credit(topic, 2, 5, true), "one iteration per lesson, even a due one");
    assertEquals(new IterationRule.Topic(1, 1, 4), IterationRule.credit(topic, 1, 6, false), "short of the iteration's tasks: progress inside it");
    assertEquals(new IterationRule.Topic(1, 0, 4), IterationRule.credit(topic, 2, 4, false), "the second iteration not before lesson N+1");
    assertEquals(new IterationRule.Topic(2, 0, 4), IterationRule.credit(topic, 2, 6, false), "a repetition missed in lesson N+1 is still due later");
    topic = IterationRule.credit(topic, 2, 5, false); assertEquals(new IterationRule.Topic(2, 0, 4), topic);
    assertEquals(topic, IterationRule.credit(topic, 1, 6, false), "the third not before lesson N+3");
    assertEquals(new IterationRule.Topic(3, 0, 4), IterationRule.credit(topic, 1, 12, false), "and also any lesson after it");
    topic = IterationRule.credit(topic, 1, 7, false); assertEquals(new IterationRule.Topic(3, 0, 4), topic); assertTrue(topic.mastered());
    assertEquals(topic, IterationRule.credit(topic, 5, 8, false), "a mastered topic stays as it is");
    assertFalse(IterationRule.due(new IterationRule.Topic(1, 0, null), 2), "a schedule without its first lesson is never due");
  }

  @Test void topicShareIsTheStudentsTopicBar() {
    assertEquals(0, IterationRule.share(0, 0));
    assertEquals(2 / 6.0, IterationRule.share(0, 2), 1e-9);
    assertEquals(3 / 6.0, IterationRule.share(0, 5), 1e-9, "never more than the iteration's own tasks");
    assertEquals(4 / 6.0, IterationRule.share(1, 1), 1e-9);
    assertEquals(5 / 6.0, IterationRule.share(2, 0), 1e-9);
    assertEquals(1, IterationRule.share(3, 0));
    assertEquals(150, ProgressAnalytics.xp(7, 1, 2, 0, 4), "game.ts: 6×10 + 30 + 2×20 + 4×5");
  }

  @Test void forecastStatusesFollowThePaceAgainstTheNeededPace() {
    // 40 topics left in 10 weeks: 4 a week needed; the pace window is three weeks for a student who started long ago.
    var onTrack = ProgressAnalytics.forecast(44, 2, 2, 12, 5, TODAY, IN_TEN_WEEKS);
    assertEquals(40, onTrack.remaining()); assertEquals(4, onTrack.closed()); assertEquals(3, onTrack.paceWeeks());
    assertEquals(4.0, onTrack.pace(), 1e-9); assertEquals(10.0, onTrack.weeksLeft(), 1e-9); assertEquals(4.0, onTrack.neededPace(), 1e-9);
    assertEquals("ON_TRACK", onTrack.status(), "the needed pace exactly is on track");
    assertEquals(TODAY.plusDays(70), onTrack.forecastDate(), "40 topics at 4 a week: 70 days");
    assertEquals("BORDERLINE", ProgressAnalytics.forecast(44, 2, 2, 9, 5, TODAY, IN_TEN_WEEKS).status(), "3 a week is 75% of the needed 4");
    assertEquals("BEHIND", ProgressAnalytics.forecast(44, 2, 2, 8, 5, TODAY, IN_TEN_WEEKS).status());

    var done = ProgressAnalytics.forecast(44, 40, 4, 0, 5, TODAY, null);
    assertEquals("DONE", done.status(), "nothing left is done, with or without a session date"); assertNull(done.forecastDate()); assertEquals(0, done.remaining());
    var noDate = ProgressAnalytics.forecast(44, 2, 2, 6, 5, TODAY, null);
    assertNull(noDate.status()); assertNull(noDate.neededPace()); assertNull(noDate.weeksLeft());
    assertEquals(TODAY.plusDays(140), noDate.forecastDate(), "the forecast date needs no session: 40 topics at 2 a week");
    var sessionToday = ProgressAnalytics.forecast(44, 2, 2, 30, 5, TODAY, TODAY);
    assertEquals("BEHIND", sessionToday.status(), "no weeks left and topics remain: behind, whatever the pace"); assertNull(sessionToday.neededPace());
    var sessionPassed = ProgressAnalytics.forecast(44, 2, 2, 30, 5, TODAY, TODAY.minusDays(7));
    assertEquals("BEHIND", sessionPassed.status()); assertEquals(-1.0, sessionPassed.weeksLeft(), 1e-9); assertNull(sessionPassed.neededPace());
    var stopped = ProgressAnalytics.forecast(44, 2, 2, 0, 5, TODAY, IN_TEN_WEEKS);
    assertEquals(0, stopped.pace()); assertNull(stopped.forecastDate(), "no pace, no forecast date"); assertEquals("BEHIND", stopped.status());
  }

  @Test void thePaceWindowShrinksForNewcomers() {
    assertEquals(1, ProgressAnalytics.forecast(44, 0, 0, 3, 0.2, TODAY, null).paceWeeks(), "less than a week counts as one");
    assertEquals(3.0, ProgressAnalytics.forecast(44, 0, 0, 3, 0.2, TODAY, null).pace(), 1e-9);
    assertEquals(2, ProgressAnalytics.forecast(44, 0, 0, 3, 2, TODAY, null).paceWeeks());
    assertEquals(1.5, ProgressAnalytics.forecast(44, 0, 0, 3, 2, TODAY, null).pace(), 1e-9);
    assertEquals(3, ProgressAnalytics.forecast(44, 0, 0, 3, 12, TODAY, null).paceWeeks(), "at most the three weeks of the window");
    // 10 topics at 1.5 a week: 46.7 days, rounded up.
    assertEquals(TODAY.plusDays(47), ProgressAnalytics.forecast(13, 3, 0, 3, 2, TODAY, null).forecastDate());
  }

  @Test void theSessionCourseIsWhereMostLessonsAre() {
    assertEquals(Language.JAVA, ProgressAnalytics.sessionCourse(lessons(2, 100, 1, 500), Map.of()));
    assertEquals(Language.PYTHON, ProgressAnalytics.sessionCourse(lessons(1, 100, 1, 500), Map.of()), "a tie goes to the most recent lesson");
    assertEquals(Language.JAVA, ProgressAnalytics.sessionCourse(lessons(1, 100, 0, 0), diagnostics(900L, 950L)), "lessons decide before the diagnostic");
    assertEquals(Language.PYTHON, ProgressAnalytics.sessionCourse(Map.of(), diagnostics(900L, 950L)), "without lessons: the most recent diagnostic");
    assertEquals(Language.JAVA, ProgressAnalytics.sessionCourse(Map.of(), diagnostics(900L, null)));
    assertNull(ProgressAnalytics.sessionCourse(Map.of(), Map.of()));
  }

  private static Map<Language, long[]> lessons(long java, long javaLast, long python, long pythonLast) {
    var map = new EnumMap<Language, long[]>(Language.class);
    if (java > 0) map.put(Language.JAVA, new long[]{java, javaLast});
    if (python > 0) map.put(Language.PYTHON, new long[]{python, pythonLast});
    return map;
  }
  private static Map<Language, Long> diagnostics(Long java, Long python) {
    var map = new EnumMap<Language, Long>(Language.class);
    if (java != null) map.put(Language.JAVA, java);
    if (python != null) map.put(Language.PYTHON, python);
    return map;
  }
}
