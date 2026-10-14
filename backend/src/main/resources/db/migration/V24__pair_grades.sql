-- Grades for a class period («пара»): the teacher enters the window and the group, the platform computes a grade per
-- student (н, 2..5) from the tasks first passed inside the window. A pair is saved once and recomputed only on request;
-- students see only the grades of published pairs. Rules: backend/README.md, «Оценки за пару».
CREATE TABLE pairs (
  id INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT NOT NULL, language TEXT NOT NULL CHECK(language IN ('JAVA','PYTHON')),
  starts_at TEXT NOT NULL, ends_at TEXT NOT NULL, median REAL, median_source TEXT NOT NULL, median_week TEXT,
  created_by INTEGER REFERENCES users(id), created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, published_at TEXT
);
CREATE INDEX pairs_group ON pairs(group_name, starts_at);
CREATE TABLE pair_grades (
  pair_id INTEGER NOT NULL REFERENCES pairs(id) ON DELETE CASCADE, user_id INTEGER NOT NULL REFERENCES users(id),
  attended INTEGER NOT NULL, points INTEGER NOT NULL, tasks_json TEXT NOT NULL, hard INTEGER NOT NULL,
  auto_grade TEXT NOT NULL, grade TEXT NOT NULL, comment TEXT, PRIMARY KEY(pair_id, user_id)
);
