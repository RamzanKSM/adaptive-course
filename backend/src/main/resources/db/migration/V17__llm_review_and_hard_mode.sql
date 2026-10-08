-- Experimental LLM grading: who checked a submission (hidden TESTS or the LLM reviewer) and the reviewer's verdict.
ALTER TABLE submissions ADD COLUMN grader TEXT NOT NULL DEFAULT 'TESTS';
ALTER TABLE submissions ADD COLUMN review_json TEXT;

-- Hard mode: the teacher allows it for a student, the student switches it on. Hard tasks are algorithmic tasks that
-- replace the regular ones of the iteration; tasks.mode keeps the two pools apart.
ALTER TABLE users ADD COLUMN hard_mode_allowed INTEGER NOT NULL DEFAULT 0;
ALTER TABLE users ADD COLUMN hard_mode_on INTEGER NOT NULL DEFAULT 0;
ALTER TABLE tasks ADD COLUMN mode TEXT NOT NULL DEFAULT 'NORMAL';
