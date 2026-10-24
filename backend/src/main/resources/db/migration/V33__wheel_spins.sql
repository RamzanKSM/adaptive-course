-- «Колесо фортуны» (2026-10-25): after a saved pair the teacher spins a wheel of the students who earned a chance at a
-- reward — a 5 at the board in the pair, or the top 20% by the pair's points among those not called to the board — and
-- one wins. A spin keeps the names on the wheel (candidates_json, user ids in wheel order), the winner and the prize the
-- teacher named (null: the default, a chocolate). Rules:
-- backend/README.md, «Колесо фортуны».
CREATE TABLE wheel_spins (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pair_id INTEGER NOT NULL REFERENCES pairs(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL REFERENCES users(id),
  candidates_json TEXT NOT NULL,
  prize TEXT,
  spun_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
  spun_at TEXT NOT NULL
);
CREATE INDEX wheel_spins_pair ON wheel_spins(pair_id);
