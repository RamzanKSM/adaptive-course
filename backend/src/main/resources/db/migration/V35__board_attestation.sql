-- «Аттестация» (2026-10-27): a call format of «К доске». The teacher calls selected students (usually several at once, at
-- their own computers) to one integrative «Напиши код» task over all topics of the group's plan, from the attestation
-- pool (tasks.mode = 'ATTESTATION', never in lessons or regular tests); lessons and the assistant are closed for the
-- student while it runs. TEST — every test at the board before.
ALTER TABLE board_tests ADD COLUMN format TEXT NOT NULL DEFAULT 'TEST' CHECK(format IN ('TEST','ATTESTATION'));
