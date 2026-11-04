-- «Снять освоение» (2026-11-03): the teacher takes a closed topic (mastered by practice or confirmed by the diagnostic)
-- back from a student, and the topic is practised from the start. Solutions up to last_submission_id (the student's last
-- submission at that moment) no longer count for this topic when its progress is rebuilt, though they stay credited.
-- was_*: the state before, for the analytics history and for undoing a mistake by hand.
CREATE TABLE topic_reopens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id),
  skill_code TEXT NOT NULL REFERENCES skills(code),
  reopened_at TEXT NOT NULL,
  reopened_by INTEGER NOT NULL REFERENCES users(id),
  last_submission_id INTEGER NOT NULL,
  was_completed INTEGER NOT NULL,
  was_successes INTEGER NOT NULL,
  was_first_lesson INTEGER,
  was_mastered INTEGER NOT NULL,
  was_confirmed INTEGER NOT NULL
);
CREATE INDEX topic_reopens_user ON topic_reopens(user_id, skill_code);
