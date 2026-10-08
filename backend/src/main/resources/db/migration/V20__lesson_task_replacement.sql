-- A task taken out of the lesson because the student switched hard mode: it is no longer the current task and cannot
-- be submitted, its submissions stay in history.
ALTER TABLE lesson_tasks ADD COLUMN replaced_at TEXT;
