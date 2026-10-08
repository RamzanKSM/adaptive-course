-- Tasks imported from a curated bank (hard mode, Exercism) carry a stable key such as «exercism:leap:JAVA», so a
-- newer bank updates them in place instead of adding duplicates.
ALTER TABLE tasks ADD COLUMN external_key TEXT;
CREATE UNIQUE INDEX tasks_external_key ON tasks(external_key) WHERE external_key IS NOT NULL;
