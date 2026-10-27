-- «Повторить тему» (2026-10-28): a student re-takes a topic already closed (mastered by practice or confirmed by the
-- diagnostic) — a series of three tasks, difficulty 1, 2, 3, inside the current lesson. A re-take never changes the
-- topic's practice progress (student_skills, skill_iterations): its tasks are marked in lesson_tasks.retake_id and the
-- iteration rule skips them. Its solved tasks are credited as usual (solved count, XP, the pair's points).
-- finish_reason: DONE (all three solved), STUDENT («Закончить повторение»), LESSON (the lesson ended), NO_TASK.
-- paused_task_id: the lesson's unsolved task taken out when the re-take started; it comes back when the re-take ends.
CREATE TABLE topic_retakes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id),
  skill_code TEXT NOT NULL REFERENCES skills(code),
  lesson_id INTEGER NOT NULL REFERENCES lessons(id),
  started_at TEXT NOT NULL,
  finished_at TEXT,
  finish_reason TEXT,
  paused_task_id INTEGER REFERENCES tasks(id)
);
CREATE INDEX topic_retakes_user ON topic_retakes(user_id, skill_code);
CREATE INDEX topic_retakes_lesson ON topic_retakes(lesson_id);
ALTER TABLE lesson_tasks ADD COLUMN retake_id INTEGER REFERENCES topic_retakes(id);
-- tasks.mode gains 'RETAKE': the re-take pool of the curated bank (tools/curated_python/retake*/), taken only by re-takes.
