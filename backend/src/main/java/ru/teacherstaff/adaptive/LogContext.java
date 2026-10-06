package ru.teacherstaff.adaptive;

import org.slf4j.MDC;
import java.util.Map;

/**
 * Who a log line is about. Keys: studentId/student — the student the work belongs to (the caller for student
 * requests, the student being managed for /api/admin/students/{id}/...); admin — the admin making the request.
 * {@code who} is the ready-made prefix used by the log pattern ("student=ivan#12 " or "admin=teacher student=ivan#12 ");
 * background work (startup, task re-verification) has no student and no prefix.
 */
final class LogContext {
  private LogContext() {}
  static final String STUDENT_ID = "studentId", STUDENT = "student", ADMIN = "admin", WHO = "who";

  static void student(Object id, Object login) {
    MDC.put(STUDENT_ID, String.valueOf(id));
    MDC.put(STUDENT, (login == null ? "" : login) + "#" + id);
    refresh();
  }
  static void admin(Object login) { MDC.put(ADMIN, String.valueOf(login)); refresh(); }

  /** The current context, to carry it to another thread (e.g. the Codex App Server reader). */
  static Map<String, String> capture() { Map<String, String> copy = MDC.getCopyOfContextMap(); return copy == null ? Map.of() : copy; }
  /** Runs {@code action} with a captured context and restores the thread's own context afterwards. */
  static void with(Map<String, String> context, Runnable action) {
    Map<String, String> own = MDC.getCopyOfContextMap();
    MDC.setContextMap(context);
    try { action.run(); }
    finally { if (own == null) MDC.clear(); else MDC.setContextMap(own); }
  }

  private static void refresh() {
    StringBuilder who = new StringBuilder();
    if (MDC.get(ADMIN) != null) who.append("admin=").append(MDC.get(ADMIN)).append(' ');
    if (MDC.get(STUDENT) != null) who.append("student=").append(MDC.get(STUDENT)).append(' ');
    MDC.put(WHO, who.toString());
  }
}
