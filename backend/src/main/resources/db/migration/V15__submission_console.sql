-- What the program printed when run as is, without hidden checks (PistonCodeRunner.Console as JSON). Shown to the
-- student with the check result and to the teacher in the lesson history. Null for older submissions.
ALTER TABLE submissions ADD COLUMN console_json TEXT;
