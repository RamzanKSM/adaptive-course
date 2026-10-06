-- pending_redos is the queue of tasks a student gets first in the next lesson of the course. Besides tasks whose
-- credit a teacher cancelled (REVOKED), it now holds tasks generated for a lesson that was finished while the
-- generation was running (GENERATED): the work is kept for the student instead of being lost.
ALTER TABLE pending_redos ADD COLUMN reason TEXT NOT NULL DEFAULT 'REVOKED';
