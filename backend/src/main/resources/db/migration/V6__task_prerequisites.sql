CREATE TABLE task_prerequisite_skills (
  task_id INTEGER NOT NULL REFERENCES tasks(id),
  skill_code TEXT NOT NULL REFERENCES skills(code),
  PRIMARY KEY(task_id, skill_code)
);
