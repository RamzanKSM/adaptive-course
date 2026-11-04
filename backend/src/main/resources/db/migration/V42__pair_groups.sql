-- A combined class: a pair of several groups (owner, 2026-11-03). pair_groups holds the groups of a pair and is what lists,
-- the journal and «Жребий» go by; pairs.group_name stays as the label («ПИ-21, ПИ-22»). pair_results.group_name is the group
-- of the student when the pair was saved, so a group's journal shows its own students only. Rules: backend/README.md.
CREATE TABLE pair_groups (
  pair_id INTEGER NOT NULL REFERENCES pairs(id) ON DELETE CASCADE,
  group_name TEXT NOT NULL,
  PRIMARY KEY(pair_id, group_name)
);
CREATE INDEX pair_groups_group ON pair_groups(group_name);
INSERT INTO pair_groups(pair_id, group_name) SELECT id, group_name FROM pairs;
ALTER TABLE pair_results ADD COLUMN group_name TEXT;
UPDATE pair_results SET group_name = (SELECT p.group_name FROM pairs p WHERE p.id = pair_results.pair_id);
