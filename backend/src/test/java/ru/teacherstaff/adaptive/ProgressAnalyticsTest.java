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

  @Test void theStatusIsThePositionAgainstThePlanLine() {
    // The plan from 0 topics 30 days ago to all 44 in 70 days: K today = ⌈44 × 30 / 100⌉ = 14.
    LocalDate start = TODAY.minusDays(30);
    var onLine = ProgressAnalytics.forecast(44, 10, 4, 12, 5, TODAY, IN_TEN_WEEKS, start);
    assertEquals(14, onLine.planToday()); assertEquals(0, onLine.lag()); assertEquals(start, onLine.planStart());
    assertEquals("ON_TRACK", onLine.status(), "exactly on the line is on track");
    assertEquals(30, onLine.remaining()); assertEquals(3, onLine.paceWeeks()); assertEquals(4.0, onLine.pace(), 1e-9); assertEquals(10.0, onLine.weeksLeft(), 1e-9);
    assertEquals(TODAY.plusDays(53), onLine.forecastDate(), "the forecast stays the pace's: 30 topics at 4 a week, 52.5 days rounded up");
    assertEquals("BORDERLINE", ProgressAnalytics.forecast(44, 8, 4, 12, 5, TODAY, IN_TEN_WEEKS, start).status(), "2 topics behind");
    assertEquals(2, ProgressAnalytics.forecast(44, 8, 4, 12, 5, TODAY, IN_TEN_WEEKS, start).lag());
    assertEquals("BEHIND", ProgressAnalytics.forecast(44, 7, 4, 12, 5, TODAY, IN_TEN_WEEKS, start).status(), "3 topics behind");
    // The owner's case: 90% of the course by the diagnostic, no practice for weeks — far ahead of the line, whatever the pace.
    var rested = ProgressAnalytics.forecast(44, 0, 40, 0, 5, TODAY, IN_TEN_WEEKS, start);
    assertEquals("ON_TRACK", rested.status()); assertEquals(-26, rested.lag()); assertEquals(0, rested.pace()); assertNull(rested.forecastDate(), "no pace, no forecast date");
    var stopped = ProgressAnalytics.forecast(44, 2, 2, 0, 5, TODAY, IN_TEN_WEEKS, start);
    assertEquals("BEHIND", stopped.status()); assertEquals(10, stopped.lag());

    var done = ProgressAnalytics.forecast(44, 40, 4, 0, 5, TODAY, null, null);
    assertEquals("DONE", done.status(), "nothing left is done, with or without a plan"); assertNull(done.forecastDate()); assertEquals(0, done.remaining());
    var noDate = ProgressAnalytics.forecast(44, 2, 2, 6, 5, TODAY, null, start);
    assertNull(noDate.status()); assertNull(noDate.planToday()); assertNull(noDate.lag()); assertNull(noDate.planStart()); assertNull(noDate.weeksLeft());
    assertEquals(TODAY.plusDays(140), noDate.forecastDate(), "the forecast date needs no session: 40 topics at 2 a week");
    assertNull(ProgressAnalytics.forecast(44, 2, 2, 6, 5, TODAY, IN_TEN_WEEKS, null).status(), "no lessons for the start: no plan, no status");
    assertNull(ProgressAnalytics.forecast(44, 2, 2, 6, 5, TODAY, IN_TEN_WEEKS, IN_TEN_WEEKS).status(), "the start not before the session: no plan");
    var sessionToday = ProgressAnalytics.forecast(44, 42, 0, 30, 5, TODAY, TODAY, start);
    assertEquals(44, sessionToday.planToday(), "on the session day the plan is the whole course"); assertEquals("BORDERLINE", sessionToday.status());
    var sessionPassed = ProgressAnalytics.forecast(44, 2, 2, 30, 5, TODAY, TODAY.minusDays(7), start);
    assertEquals("BEHIND", sessionPassed.status()); assertEquals(-1.0, sessionPassed.weeksLeft(), 1e-9); assertEquals(40, sessionPassed.lag());
  }

  @Test void thePaceWindowShrinksForNewcomers() {
    assertEquals(1, ProgressAnalytics.forecast(44, 0, 0, 3, 0.2, TODAY, null, null).paceWeeks(), "less than a week counts as one");
    assertEquals(3.0, ProgressAnalytics.forecast(44, 0, 0, 3, 0.2, TODAY, null, null).pace(), 1e-9);
    assertEquals(2, ProgressAnalytics.forecast(44, 0, 0, 3, 2, TODAY, null, null).paceWeeks());
    assertEquals(1.5, ProgressAnalytics.forecast(44, 0, 0, 3, 2, TODAY, null, null).pace(), 1e-9);
    assertEquals(3, ProgressAnalytics.forecast(44, 0, 0, 3, 12, TODAY, null, null).paceWeeks(), "at most the three weeks of the window");
    // 10 topics at 1.5 a week: 46.7 days, rounded up.
    assertEquals(TODAY.plusDays(47), ProgressAnalytics.forecast(13, 3, 0, 3, 2, TODAY, null, null).forecastDate());
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
