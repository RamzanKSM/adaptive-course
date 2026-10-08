-- A lesson ends by itself after a stretch without activity (code runs, submissions, new content, chat).
-- last_activity_at is an ISO-8601 instant (UTC, "...Z"); open lessons get a fresh countdown on upgrade.
ALTER TABLE lessons ADD COLUMN last_activity_at TEXT;
-- Who or what finished the lesson: STUDENT, LOGOUT, IDLE, TEACHER; NULL for lessons finished before this column.
ALTER TABLE lessons ADD COLUMN finish_reason TEXT;
UPDATE lessons SET last_activity_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now') WHERE finished_at IS NULL;
