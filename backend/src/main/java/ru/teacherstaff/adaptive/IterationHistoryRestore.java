package ru.teacherstaff.adaptive;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;

/** Rebuilds persisted iteration state once from accepted, credited practice. */
public final class IterationHistoryRestore {
  private IterationHistoryRestore() {}
  private record Key(long user, String skill) {}
  private record Event(long lesson, int number, long task) {}

  /** Run explicitly against a stopped service and a verified database backup. */
  public static void main(String[] args) throws Exception {
    if (args.length != 1) throw new IllegalArgumentException("Provide the SQLite database path");
    if (!java.nio.file.Files.isRegularFile(java.nio.file.Path.of(args[0]))) throw new IllegalArgumentException("Database file does not exist");
    try (var connection = java.sql.DriverManager.getConnection("jdbc:sqlite:" + args[0])) {
      connection.setAutoCommit(false);
      try { restore(connection); connection.commit(); }
      catch (Exception e) { connection.rollback(); throw e; }
    }
  }

  public static void restore(Connection connection) throws SQLException {
    Map<Key, java.util.List<Event>> history = new LinkedHashMap<>();
    String sql = "select l.user_id,ts.skill_code,l.id,coalesce(l.language_lesson_number,l.lesson_number),s.task_id "
        + "from submissions s join lessons l on l.id=s.lesson_id join successful_task_credit c on c.user_id=l.user_id and c.task_id=s.task_id "
        + "join task_target_skills ts on ts.task_id=s.task_id where s.passed=1 and s.revoked_at is null "
        + "and not exists(select 1 from lesson_tasks lt where lt.lesson_id=l.id and lt.task_id=s.task_id and lt.retake_id is not null) "
        + "group by l.user_id,ts.skill_code,l.id,s.task_id order by l.user_id,ts.skill_code,coalesce(l.language_lesson_number,l.lesson_number),l.id,min(s.id)";
    try (var statement = connection.createStatement(); var rs = statement.executeQuery(sql)) {
      while (rs.next()) history.computeIfAbsent(new Key(rs.getLong(1), rs.getString(2)), k -> new java.util.ArrayList<>())
          .add(new Event(rs.getLong(3), rs.getInt(4), rs.getLong(5)));
    }
    // Include stale progress with no remaining valid practice, so revoked or excluded tasks cannot leave credit behind.
    try (var statement = connection.createStatement(); var rs = statement.executeQuery(
        "select user_id,skill_code from student_skills union select user_id,skill_code from skill_iterations")) {
      while (rs.next()) history.computeIfAbsent(new Key(rs.getLong(1), rs.getString(2)), k -> new java.util.ArrayList<>());
    }
    try (var delete = connection.prepareStatement("delete from skill_iterations where user_id=? and skill_code=?");
         var insert = connection.prepareStatement("insert into skill_iterations(user_id,skill_code,iteration_number,lesson_id) values(?,?,?,?)");
         var update = connection.prepareStatement("insert into student_skills(user_id,skill_code,completed_iterations,iteration_successes,first_iteration_lesson_number,mastered) values(?,?,?,?,?,?) on conflict(user_id,skill_code) do update set completed_iterations=excluded.completed_iterations,iteration_successes=excluded.iteration_successes,first_iteration_lesson_number=excluded.first_iteration_lesson_number,mastered=excluded.mastered")) {
      for (var entry : history.entrySet()) {
        var key = entry.getKey(); delete.setLong(1, key.user()); delete.setString(2, key.skill()); delete.executeUpdate();
        var state = IterationRule.Topic.NEW; Set<Long> seen = new HashSet<>(), iterated = new HashSet<>();
        for (var event : entry.getValue()) {
          if (!seen.add(event.task())) continue;
          var after = IterationRule.credit(state, event.number(), iterated.contains(event.lesson()));
          if (after.completed() > state.completed()) {
            iterated.add(event.lesson()); insert.setLong(1,key.user()); insert.setString(2,key.skill()); insert.setInt(3,after.completed()); insert.setLong(4,event.lesson()); insert.executeUpdate();
          }
          state = after;
        }
        update.setLong(1,key.user()); update.setString(2,key.skill()); update.setInt(3,state.completed()); update.setInt(4,state.successes());
        if (state.firstLesson() == null) update.setNull(5,java.sql.Types.INTEGER); else update.setInt(5,state.firstLesson());
        update.setInt(6,state.mastered()?1:0); update.executeUpdate();
      }
    }
  }
}
