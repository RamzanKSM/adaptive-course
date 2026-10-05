-- Task quality: every task records what it teaches (goal), which platform checks enforce it, and which version
-- of the verification pipeline accepted it. Tasks without quality_version were accepted by the older,
-- output-only validation and are re-verified on startup.
ALTER TABLE tasks ADD COLUMN source TEXT NOT NULL DEFAULT 'LLM';
ALTER TABLE tasks ADD COLUMN goal_json TEXT;
ALTER TABLE tasks ADD COLUMN quality_version INTEGER;
UPDATE tasks SET source = 'SEED' WHERE title LIKE 'Консоль:%' OR title LIKE 'Python:%';

-- llm_calls gains TASK_REPAIR (background re-verification of old tasks, no student) and the reasoning level used,
-- which now differs per purpose. SQLite cannot change a CHECK constraint in place, and nothing references llm_calls,
-- so the table is rebuilt.
CREATE TABLE llm_calls_v2 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER REFERENCES users(id),
  purpose TEXT NOT NULL CHECK(purpose IN ('CHAT','TASK','EXPLANATION','TASK_REPAIR')),
  language TEXT NOT NULL DEFAULT 'JAVA',
  skill_code TEXT,
  model TEXT,
  reasoning_effort TEXT,
  status TEXT NOT NULL CHECK(status IN ('OK','ERROR','TIMEOUT')),
  error TEXT,
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
INSERT INTO llm_calls_v2(id,user_id,purpose,language,skill_code,model,status,error,outcome,duration_ms,prompt_chars,response_chars,input_tokens,cached_input_tokens,output_tokens,reasoning_tokens,total_tokens,created_at)
  SELECT id,user_id,purpose,language,skill_code,model,status,error,outcome,duration_ms,prompt_chars,response_chars,input_tokens,cached_input_tokens,output_tokens,reasoning_tokens,total_tokens,created_at FROM llm_calls;
DROP TABLE llm_calls;
ALTER TABLE llm_calls_v2 RENAME TO llm_calls;
CREATE INDEX llm_calls_created_at ON llm_calls(created_at);
CREATE INDEX llm_calls_user ON llm_calls(user_id, created_at);

-- Diagnostic result per topic. Confirmed topics are skipped by practice; this is not practice credit:
-- student_skills, iterations and successful_task_credit stay untouched.
CREATE TABLE diagnostic_skill_results (
  user_id INTEGER NOT NULL REFERENCES users(id),
  skill_code TEXT NOT NULL REFERENCES skills(code),
  correct INTEGER NOT NULL,
  total INTEGER NOT NULL,
  confirmed INTEGER NOT NULL,
  PRIMARY KEY(user_id, skill_code)
);
