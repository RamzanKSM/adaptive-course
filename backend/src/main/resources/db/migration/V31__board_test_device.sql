-- The browser that started a board test (2026-10-20): the SHA-256 of a random per-browser token (header X-Board-Device).
-- Only that browser saves, runs and finishes the test; the student's other open sessions see «Тест идёт на другом
-- компьютере» — two screens of one test raced at the end of the time and a blank one could overwrite the answers.
-- Null (tests started before, or by a client without the header) — any of the student's sessions, as before.
ALTER TABLE board_tests ADD COLUMN device TEXT;
