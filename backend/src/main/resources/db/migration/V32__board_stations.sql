-- «Компьютер у доски» (2026-10-22): the teacher turns a browser of the classroom PC into a board station; it shows only
-- the active calls and the running test, and the student starts his test there without signing in. The station's
-- cookie adaptive_station holds a random token; the table keeps its SHA-256. A revoked station (revoked_at) is no
-- station any more.
CREATE TABLE board_stations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  token_hash TEXT NOT NULL UNIQUE,
  created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
  created_at TEXT NOT NULL,
  last_seen_at TEXT,
  revoked_at TEXT
);
-- The station a test was started at (null: from the student's own account).
ALTER TABLE board_tests ADD COLUMN station_id INTEGER REFERENCES board_stations(id) ON DELETE SET NULL;
-- Grows when the teacher replaces an item of a running test, so that the test screen reloads it.
ALTER TABLE board_tests ADD COLUMN items_revision INTEGER NOT NULL DEFAULT 0;
