CREATE TABLE app_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
INSERT INTO app_settings(key, value) VALUES ('llm_enabled', 'false');

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('ADMIN','STUDENT')), display_name TEXT NOT NULL,
  llm_enabled INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE sessions (
  token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE skills (
  id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT NOT NULL UNIQUE, title TEXT NOT NULL, sort_order INTEGER NOT NULL,
  prerequisite_code TEXT, block_no INTEGER NOT NULL
);
CREATE TABLE diagnostic_questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ordinal INTEGER NOT NULL UNIQUE, skill_code TEXT NOT NULL REFERENCES skills(code),
  prompt TEXT NOT NULL, options_json TEXT NOT NULL, correct_option INTEGER NOT NULL, block_no INTEGER NOT NULL
);
CREATE TABLE diagnostic_answers (
  user_id INTEGER NOT NULL REFERENCES users(id), question_id INTEGER NOT NULL REFERENCES diagnostic_questions(id),
  selected_option INTEGER, is_correct INTEGER NOT NULL, PRIMARY KEY(user_id, question_id)
);
CREATE TABLE student_languages (
  user_id INTEGER PRIMARY KEY REFERENCES users(id), diagnostic_completed_at TEXT, starting_block INTEGER,
  conversation_id TEXT, conversation_namespace TEXT
);
CREATE TABLE student_skills (
  user_id INTEGER NOT NULL REFERENCES users(id), skill_code TEXT NOT NULL REFERENCES skills(code),
  completed_iterations INTEGER NOT NULL DEFAULT 0, iteration_successes INTEGER NOT NULL DEFAULT 0,
  first_iteration_lesson_number INTEGER, mastered INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(user_id, skill_code)
);
CREATE TABLE lessons (
  id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL REFERENCES users(id), lesson_number INTEGER NOT NULL,
  started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, finished_at TEXT, UNIQUE(user_id, lesson_number)
);
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT, skill_code TEXT NOT NULL REFERENCES skills(code), title TEXT NOT NULL, statement TEXT NOT NULL,
  starter_code TEXT NOT NULL DEFAULT '', test_source TEXT NOT NULL, test_file_name TEXT NOT NULL DEFAULT 'TestHarness.java',
  active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE lesson_tasks (
  lesson_id INTEGER NOT NULL REFERENCES lessons(id), task_id INTEGER NOT NULL REFERENCES tasks(id), PRIMARY KEY(lesson_id, task_id)
);
CREATE TABLE submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_id INTEGER NOT NULL REFERENCES lessons(id), task_id INTEGER NOT NULL REFERENCES tasks(id),
  source_code TEXT NOT NULL, passed INTEGER NOT NULL, runner_output TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE successful_task_credit (
  user_id INTEGER NOT NULL REFERENCES users(id), task_id INTEGER NOT NULL REFERENCES tasks(id), PRIMARY KEY(user_id, task_id)
);
CREATE TABLE chat_messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_id INTEGER NOT NULL REFERENCES lessons(id), role TEXT NOT NULL CHECK(role IN ('STUDENT','ASSISTANT')),
  content TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
