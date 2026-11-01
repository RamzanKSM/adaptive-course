-- «Эстафета» (CodeRelay): the whole group solves one task in one editor, one writer at a time, a small step per turn.
CREATE TABLE relays (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  group_name TEXT NOT NULL,
  language TEXT NOT NULL CHECK(language IN ('JAVA','PYTHON')),
  task_key TEXT NOT NULL,
  turn_seconds INTEGER NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('LOBBY','RUNNING','PAUSED','SOLVED','FINISHED')),
  code TEXT NOT NULL,
  version INTEGER NOT NULL DEFAULT 0,
  step INTEGER NOT NULL DEFAULT 0,
  turn_no INTEGER NOT NULL DEFAULT 0,
  writer_id INTEGER REFERENCES users(id),
  turn_started_at TEXT,
  turn_ends_at TEXT,
  paused_left_ms INTEGER,
  streak INTEGER NOT NULL DEFAULT 0,
  best_streak INTEGER NOT NULL DEFAULT 0,
  skips INTEGER NOT NULL DEFAULT 0,
  credited TEXT NOT NULL DEFAULT '',  -- steps the teacher credited by hand, «3,5»: they count as matched for the steps after them
  run_json TEXT,
  created_by INTEGER NOT NULL REFERENCES users(id),
  created_at TEXT NOT NULL,
  started_at TEXT,
  finished_at TEXT
);
CREATE INDEX relays_group ON relays(group_name, status);

CREATE TABLE relay_members (
  relay_id INTEGER NOT NULL REFERENCES relays(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL REFERENCES users(id),
  position INTEGER NOT NULL,
  joined_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  PRIMARY KEY (relay_id, user_id)
);

-- One row per turn: who, which step, how it ended (DONE, PASS, TIMEOUT, TEACHER_DONE, TEACHER_SKIP, STOPPED), the code before and after.
CREATE TABLE relay_turns (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  relay_id INTEGER NOT NULL REFERENCES relays(id) ON DELETE CASCADE,
  turn_no INTEGER NOT NULL,
  user_id INTEGER NOT NULL REFERENCES users(id),
  step INTEGER NOT NULL,
  started_at TEXT NOT NULL,
  ended_at TEXT,
  outcome TEXT,
  code_before TEXT NOT NULL,
  code_after TEXT,
  UNIQUE (relay_id, turn_no)
);
