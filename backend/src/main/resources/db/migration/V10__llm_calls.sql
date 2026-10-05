-- One row per LLM turn (chat answer, generated task or explanation) for logging and admin analytics.
CREATE TABLE llm_calls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER REFERENCES users(id),
  purpose TEXT NOT NULL CHECK(purpose IN ('CHAT','TASK','EXPLANATION')),
  language TEXT NOT NULL DEFAULT 'JAVA',
  skill_code TEXT,
  model TEXT,
  status TEXT NOT NULL CHECK(status IN ('OK','ERROR','TIMEOUT')),
  error TEXT,
  -- For TASK calls: whether the generated task passed server validation and was stored.
  outcome TEXT CHECK(outcome IS NULL OR outcome IN ('ACCEPTED','REJECTED')),
  duration_ms INTEGER NOT NULL,
  prompt_chars INTEGER NOT NULL DEFAULT 0,
  response_chars INTEGER NOT NULL DEFAULT 0,
  input_tokens INTEGER,
  cached_input_tokens INTEGER,
  output_tokens INTEGER,
  reasoning_tokens INTEGER,
  total_tokens INTEGER,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX llm_calls_created_at ON llm_calls(created_at);
CREATE INDEX llm_calls_user ON llm_calls(user_id, created_at);

-- Statements must not mention platform internals. Generated tasks that do are retired and regenerated with the
-- new prompt; seed tasks are re-activated with clean statements by the importer on startup.
UPDATE tasks SET active = 0
 WHERE statement LIKE '%solution.py%' OR statement LIKE '%test_solution%' OR statement LIKE '%TestHarness%' OR statement LIKE '%run_checks%';
