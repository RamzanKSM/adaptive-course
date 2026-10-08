-- Optional study group of a student, for filtering the teacher's list. A plain name, no separate table: groups exist
-- while at least one student is in them. NULL — no group.
ALTER TABLE users ADD COLUMN group_name TEXT;
CREATE INDEX users_group_name ON users(group_name);
