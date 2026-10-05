-- A second course (Python) runs next to Java. Existing rows belong to Java.
ALTER TABLE skills ADD COLUMN language TEXT NOT NULL DEFAULT 'JAVA';
ALTER TABLE diagnostic_questions ADD COLUMN language TEXT NOT NULL DEFAULT 'JAVA';
ALTER TABLE tasks ADD COLUMN language TEXT NOT NULL DEFAULT 'JAVA';

-- lesson_number stays a per-student sequence across all languages (it is UNIQUE and referenced history);
-- language_lesson_number drives the per-language iteration schedule (N, N+1, N+3) and is what students see.
ALTER TABLE lessons ADD COLUMN language TEXT NOT NULL DEFAULT 'JAVA';
ALTER TABLE lessons ADD COLUMN language_lesson_number INTEGER;
UPDATE lessons SET language_lesson_number = lesson_number;

-- Diagnostic result, starting block and the tutor thread are per student and language.
CREATE TABLE student_languages_v2 (
  user_id INTEGER NOT NULL REFERENCES users(id), language TEXT NOT NULL DEFAULT 'JAVA',
  diagnostic_completed_at TEXT, starting_block INTEGER, conversation_id TEXT, conversation_namespace TEXT,
  PRIMARY KEY(user_id, language)
);
INSERT INTO student_languages_v2(user_id, language, diagnostic_completed_at, starting_block, conversation_id, conversation_namespace)
  SELECT user_id, 'JAVA', diagnostic_completed_at, starting_block, conversation_id, conversation_namespace FROM student_languages;
DROP TABLE student_languages;
ALTER TABLE student_languages_v2 RENAME TO student_languages;
