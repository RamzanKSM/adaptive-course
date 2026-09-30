CREATE TABLE task_target_skills (
  task_id INTEGER NOT NULL REFERENCES tasks(id),
  skill_code TEXT NOT NULL REFERENCES skills(code),
  PRIMARY KEY(task_id, skill_code)
);
CREATE TABLE skill_iterations (
  user_id INTEGER NOT NULL REFERENCES users(id),
  skill_code TEXT NOT NULL REFERENCES skills(code),
  iteration_number INTEGER NOT NULL,
  lesson_id INTEGER NOT NULL REFERENCES lessons(id),
  PRIMARY KEY(user_id, skill_code, iteration_number),
  UNIQUE(user_id, skill_code, lesson_id)
);
INSERT INTO task_target_skills(task_id, skill_code) SELECT id, skill_code FROM tasks;
