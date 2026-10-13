-- Whether the student takes the session: only participants count in the progress analytics (group statistics, the
-- classroom screen, flags and the session forecast). The teacher switches it off for themself, volunteers and test accounts.
ALTER TABLE users ADD COLUMN session_participant INTEGER NOT NULL DEFAULT 1;
