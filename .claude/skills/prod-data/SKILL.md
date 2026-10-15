---
name: prod-data
description: Look at or (with approval) fix data in the Rmzn Tutor production database on rmzn.net — students, lessons, submissions, tasks, grades, LLM calls. Use when the owner asks what students did, why something happened in production, or to correct data.
---

# Production data (SQLite on rmzn.net)

Database: `/var/lib/docker/volumes/adaptive-course_adaptive-data/_data/adaptive-tutor.db` (WAL: `-wal`, `-shm`; owner
uid 10001). The schema is the Flyway migrations in `backend/src/main/resources/db/migration`.

## Reading (no approval needed when the owner asked a question)
Run Python on the server with a read-only URI; print only what answers the question. No local copies of the database.
```sh
ssh root@rmzn.net 'python3 - <<EOF
import sqlite3
db = sqlite3.connect("file:/var/lib/docker/volumes/adaptive-course_adaptive-data/_data/adaptive-tutor.db?mode=ro", uri=True)
q = lambda s, *a: db.execute(s, a).fetchall()
print(q("select language, count(*) from lessons where date(started_at) = date(\"now\") group by 1"))
EOF'
```
Inside the heredoc use `\"` for SQL string literals. Times are UTC (`2026-10-14 08:00:00` or ISO with `Z`); the owner
thinks in Moscow time (UTC+3). Useful tables: `users` (role, group_name, session_participant, hard_mode_*),
`lessons` (language, language_lesson_number, started_at, finished_at, finish_reason), `lesson_tasks`, `submissions`
(passed, revoked_at, source_code), `successful_task_credit`, `student_skills`, `skill_iterations`,
`diagnostic_skill_results`, `tasks` (source CURATED/LLM/SEED/EXERCISM, mode NORMAL/HARD, external_key, difficulty),
`chat_messages`, `llm_calls`, `pairs`, `pair_results`, `board_tests`. «Запустить» runs are not stored in the database.

Students' names are fine to show to the owner (he is their teacher); don't compute rankings or «who is behind» lists unless
he asks for them.

## Writing (only with the owner's explicit approval)
1. Back up with the SQLite backup API into `/root/adaptive-course-backups/adaptive-tutor-<UTC time>-pre-<what>.db`.
2. Check `-wal` and `-shm` exist (so running as root does not change file ownership), then in one
   `begin immediate … commit` transaction with `pragma busy_timeout=15000`; print the rows you change first.
3. Report what changed and the backup path. Prefer the application's API/UI over raw SQL when one exists.
