CREATE TABLE explanations (
  skill_code TEXT PRIMARY KEY REFERENCES skills(code), content TEXT NOT NULL, source TEXT NOT NULL
);
-- Seed explanation is inserted by DiagnosticImporter after its skill row exists.
