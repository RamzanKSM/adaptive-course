-- «Показать студенту разбор» (2026-10-19): the teacher decides per graded test whether the student sees the report — per
-- item the statement, his own answer, the verdict and the check message (never the reference, the bug or the scores).
ALTER TABLE board_tests ADD COLUMN report_visible INTEGER NOT NULL DEFAULT 1;
