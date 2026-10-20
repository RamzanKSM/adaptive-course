-- Where the items of a board test come from (2026-10-19): LEVEL — the topics the student has reached (as before);
-- PACE — the minimum for today: the first K topics of the course by a uniform plan from the group's first lesson in the
-- course to the session date (BoardTests.pacePlan). Chosen by the teacher at the call; null for older tests = LEVEL.
ALTER TABLE board_tests ADD COLUMN source TEXT;
