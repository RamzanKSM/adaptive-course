-- «Тренировочная аттестация» (2026-10-28): the student starts it himself from a lesson — one task of the attestation's
-- size and kind from the practice pool (tasks.mode = 'ATTESTATION_PRACTICE', key practice:<slug>), a 10-minute timer, no
-- grade, no effect on progress. It is a row of topic_retakes with kind = 'ATTESTATION' (a topic re-take is 'TOPIC'): its
-- task is marked in lesson_tasks.retake_id like a re-take's, so the iteration rule skips it, and the lesson's unsolved
-- task waits (paused_task_id). skill_code — the last topic the task covers (it covers topics 1…skill).
-- deadline_at: started_at + 10 minutes; until then the assistant is closed while the task is not solved.
-- result: IN_TIME (solved by the deadline), LATE (solved after it), NOT_SOLVED (ended without a solution); null while the
-- practice is open and its task unsolved, and for re-takes. solved_at: the first passing submission of the task.
ALTER TABLE topic_retakes ADD COLUMN kind TEXT NOT NULL DEFAULT 'TOPIC' CHECK(kind IN ('TOPIC','ATTESTATION'));
ALTER TABLE topic_retakes ADD COLUMN deadline_at TEXT;
ALTER TABLE topic_retakes ADD COLUMN result TEXT CHECK(result IN ('IN_TIME','LATE','NOT_SOLVED'));
ALTER TABLE topic_retakes ADD COLUMN solved_at TEXT;
-- tasks.mode gains 'INTEGRATIVE' (the integrative task of a topic's 3rd iteration in lessons, key integ:<slug>) and
-- 'ATTESTATION_PRACTICE'; AttestationBank loads both pools at startup, nothing else takes them.
