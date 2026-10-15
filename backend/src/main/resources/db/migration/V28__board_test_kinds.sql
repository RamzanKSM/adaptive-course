-- «К доске» v2: the teacher chooses the kinds of items at the call (parsons «Собери программу», fix «Исправь ошибку»,
-- code «Напиши код»); the test time is the sum of their minutes. The «Что выведет этот код?» item is gone.
-- kinds: JSON array of the chosen kinds in the canonical order; duration_seconds: set at the call from the kinds.
ALTER TABLE board_tests ADD COLUMN kinds TEXT;
ALTER TABLE board_tests ADD COLUMN duration_seconds INTEGER;
-- The bank's wrong solutions [{"description","source"}] (each fails the task's checks): the «Исправь ошибку» item shows
-- one of them, the «Собери программу» item takes an extra line from one. Set by tools/curated_python; null for other tasks.
ALTER TABLE tasks ADD COLUMN wrong_json TEXT;
