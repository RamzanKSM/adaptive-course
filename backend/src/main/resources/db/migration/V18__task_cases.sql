-- Test cases of function and input/output tasks. The generator gives only the inputs; expected is what the task's
-- reference solution returned or printed, recorded by the platform. Public cases are the statement's examples:
-- a failed example shows the expected answer, a failed hidden case only says which test failed.
CREATE TABLE task_cases (
  task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  ordinal INTEGER NOT NULL,
  input TEXT NOT NULL,
  expected TEXT NOT NULL,
  is_public INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (task_id, ordinal)
);
