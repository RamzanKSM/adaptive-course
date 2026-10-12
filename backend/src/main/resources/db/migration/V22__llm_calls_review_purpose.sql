-- llm_calls gains REVIEW: the LLM check of «calculate» solutions (is the answer computed or printed ready-made).
-- The code recorded REVIEW calls since that check appeared, but the CHECK constraint rejected them, so their
-- statistics were lost. SQLite cannot change a CHECK constraint in place and nothing references llm_calls, so the
-- table is rebuilt as in V12, keeping every row and id.
CREATE TABLE llm_calls_v3 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER REFERENCES users(id),
  purpose TEXT NOT NULL CHECK(purpose IN ('CHAT','TASK','EXPLANATION','TASK_REPAIR','REVIEW')),
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
INSERT INTO llm_calls_v3(id,user_id,purpose,language,skill_code,model,reasoning_effort,status,error,outcome,duration_ms,prompt_chars,response_chars,input_tokens,cached_input_tokens,output_tokens,reasoning_tokens,total_tokens,created_at)
  SELECT id,user_id,purpose,language,skill_code,model,reasoning_effort,status,error,outcome,duration_ms,prompt_chars,response_chars,input_tokens,cached_input_tokens,output_tokens,reasoning_tokens,total_tokens,created_at FROM llm_calls;
DROP TABLE llm_calls;
ALTER TABLE llm_calls_v3 RENAME TO llm_calls;
CREATE INDEX llm_calls_created_at ON llm_calls(created_at);
CREATE INDEX llm_calls_user ON llm_calls(user_id, created_at);
