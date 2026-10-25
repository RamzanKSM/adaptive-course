-- «Жребий» with settings (2026-10-25): a draw is a run of steps the teacher starts one by one. A run keeps the names on
-- the wheel in wheel order (names_json), the mode (ARROW: the arrow picks a winner; ELIMINATION: the name under the arrow
-- drops out until the winners are left), how many winners it wants and the prize (null in the spins of V33: a chocolate). A step is a winner
-- (WIN; absent=1 when the teacher marked the student not in class and a replacement was drawn) or a name that dropped out (OUT).
-- The single spins of V33 become one-step ARROW runs. Rules: backend/README.md, «Жребий».
CREATE TABLE draw_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pair_id INTEGER NOT NULL REFERENCES pairs(id) ON DELETE CASCADE,
  mode TEXT NOT NULL CHECK(mode IN ('ARROW','ELIMINATION')),
  winners INTEGER NOT NULL,
  prize TEXT,
  names_json TEXT NOT NULL,
  created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX draw_runs_pair ON draw_runs(pair_id);
CREATE TABLE draw_steps (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id INTEGER NOT NULL REFERENCES draw_runs(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL REFERENCES users(id),
  kind TEXT NOT NULL CHECK(kind IN ('WIN','OUT')),
  absent INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);
CREATE INDEX draw_steps_run ON draw_steps(run_id);

INSERT INTO draw_runs(id, pair_id, mode, winners, prize, names_json, created_by, created_at)
  SELECT id, pair_id, 'ARROW', 1, prize, candidates_json, spun_by, spun_at FROM wheel_spins;
INSERT INTO draw_steps(run_id, user_id, kind, created_at)
  SELECT id, user_id, 'WIN', spun_at FROM wheel_spins;
DROP TABLE wheel_spins;
