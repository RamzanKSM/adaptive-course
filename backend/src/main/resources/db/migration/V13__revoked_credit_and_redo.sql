-- A teacher can cancel an accepted solution. The submission stays in history but stops counting as passed.
ALTER TABLE submissions ADD COLUMN revoked_at TEXT;
ALTER TABLE submissions ADD COLUMN revoked_by INTEGER REFERENCES users(id);

-- Tasks whose credit was cancelled and that the student must solve again. /learning/next assigns them before
-- choosing new work; the row is removed once the task is assigned to a lesson.
CREATE TABLE pending_redos (
  user_id INTEGER NOT NULL REFERENCES users(id),
  task_id INTEGER NOT NULL REFERENCES tasks(id),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(user_id, task_id)
);
