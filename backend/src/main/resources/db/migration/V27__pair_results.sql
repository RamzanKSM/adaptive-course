-- «Работа на паре» is analytics only: the grades a pair once carried are removed entirely.
ALTER TABLE pair_grades DROP COLUMN auto_grade;
ALTER TABLE pair_grades DROP COLUMN grade;
ALTER TABLE pair_grades DROP COLUMN comment;
ALTER TABLE pairs DROP COLUMN published_at;
ALTER TABLE pair_grades RENAME TO pair_results;
