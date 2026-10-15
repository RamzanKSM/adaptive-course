-- The full program of a curated task (the bank's reference solution): the «Что выведет этот код?» item of the test at
-- the board shows it. Set by tools/curated_python (import_bank.py, backfill_reference.py); null for other tasks.
ALTER TABLE tasks ADD COLUMN reference_code TEXT;
-- «К доске»: the teacher calls a student, the student starts a 6-minute test of two items (a task to solve, the output
-- of a program), the platform checks it, the LLM proposes a grade, the teacher sets the final one. Nothing is credited.
-- Rules: backend/README.md, «К доске». Timestamps are UTC ISO-8601; the *_json columns are written by BoardTests.
CREATE TABLE board_tests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id),
  group_name TEXT,
  language TEXT NOT NULL CHECK(language IN ('JAVA','PYTHON')),
  status TEXT NOT NULL CHECK(status IN ('CALLED','CANCELLED','EXPIRED','STARTED','FINISHED')),
  called_at TEXT NOT NULL, called_by INTEGER REFERENCES users(id), call_expires_at TEXT NOT NULL,
  started_at TEXT, ends_at TEXT, finished_at TEXT,
  items_json TEXT, answers_json TEXT, results_json TEXT, runs_json TEXT,
  pace_status TEXT, rule_grade TEXT, assessment_json TEXT, suggested_grade TEXT,
  final_grade TEXT CHECK(final_grade IS NULL OR final_grade IN ('2','3','4','5')), comment TEXT, graded_at TEXT
);
CREATE INDEX board_tests_group ON board_tests(group_name, called_at);
CREATE INDEX board_tests_user ON board_tests(user_id);
