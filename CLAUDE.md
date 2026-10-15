# Rmzn Tutor — notes for Claude Code agents

Adaptive Java/Python course for university groups (teacher = the repo owner, Ramzan; students are beginners). Production:
https://rmzn.net. Talk to the owner in Russian; student-facing UI text is Russian, addressing the student as «ты».

Read before changing behaviour: `backend/README.md` (rules of checking, bank, hard mode, analytics, board tests — the source of
truth), `docs/decisions.md` (what was agreed with the owner and why), `ARCHITECTURE.md`.

## Working rules (agreed with the owner)
- **Propose before applying.** For any change of behaviour (what students/teacher see, grading, task selection, checks)
  describe the plan and wait for an explicit «делай». Bug investigation and read-only analysis need no approval.
- Commit, push and deploy when the owner says so («делай и выкатывай» means: implement, test, commit, deploy). End commit
  messages with the `Co-Authored-By` line Claude Code gives you. Never force-push, never rewrite history.
- Don't analyse student data unless asked; when asked, query production read-only and don't keep local copies of the
  production database (it holds personal data).
- Never read `.env` files or real passwords. For local testing generate your own test credentials (store them in your
  scratchpad, not in chat or the repo) and use a throwaway local database.
- Parallel work: launch helper agents as terminal runs of `claude -p` (owner's global rule), prompts and logs in a
  persistent folder such as `/Users/ramzankibiev/Stuff/TeacherStaff/agent-runs/<task>/`; give each a self-contained
  brief and disjoint files; review and verify their results yourself.
- Verify before reporting: tests, `npm run build`, and for UI changes a look in a browser against a local test database.

## Layout
- `backend/` — Spring Boot 3, Java 21, SQLite (WAL) via JdbcTemplate, Flyway migrations in
  `src/main/resources/db/migration` (never edit an applied migration; add the next `V<n>__*.sql`). `ApiController.java` is
  large and written in a compact style — keep new logic in its own class (e.g. `ProgressAnalytics`, `PairWork`,
  `IterationRule`) and match the surrounding style.
- `frontend/` — React + TypeScript + Vite, no UI/chart libraries; own SVG charts (`charts.tsx`); CSS tokens in
  `src/styles.css`. Tabs: student lesson/progress (`App.tsx`), teacher «Студенты», «Прогресс» (`progress.tsx`),
  «Работа на паре» (`pairs.tsx`), «К доске» (`board.tsx`), LLM analytics/settings.
- `tools/curated_python/` — the curated task bank (Python and Java despite the name), see the `task-bank` skill.
- `tools/build_hard_bank.py` — the hard-mode bank (Exercism problem-specifications) → `backend/src/main/resources/hard-tasks/exercism.json`.
- Root `*.md` specs: `adaptive_java_tutor_mvp_spec_v4.md`, `java_initial_diagnostic_mvp_v2.md`,
  `python_initial_diagnostic_mvp.md` (the diagnostics are imported at startup).

## Build and test
```sh
cd backend && export JAVA_HOME=/Users/ramzankibiev/Library/Java/JavaVirtualMachines/corretto-21.0.5/Contents/Home && mvn -q -o test
cd frontend && npm run build          # tsc -b && vite build
```
Run the backend locally (from `backend/` — the diagnostic sources are resolved as `../*.md`):
`APP_DATABASE_PATH=<scratch>/local.db APP_BOOTSTRAP_ADMIN_LOGIN=<test> APP_BOOTSTRAP_ADMIN_PASSWORD=<test> APP_LLM_ENABLED=false PORT=8091 java -jar target/adaptive-java-tutor-0.1.0.jar`
(after `mvn -q -o package -DskipTests`); frontend: `API_PROXY_TARGET=http://localhost:8091 npx vite --port 5191`.
Checking code needs Piston; locally use the production Piston through an SSH tunnel (see the `deploy` skill).

## Production (VPS rmzn.net)
- `ssh root@rmzn.net` (key auth). Checkout `/root/adaptive-course`, `docker compose` services `backend` and `piston`.
  Other services on that VPS (adlantgbot, bjj-sync-db, remnanode, openclaw, caddy-selfsteal) are not ours — don't touch.
- Database: `/var/lib/docker/volumes/adaptive-course_adaptive-data/_data/adaptive-tutor.db` (+ `-wal`, `-shm`, owner
  uid 10001). Read with `sqlite3`/Python in `mode=ro`. Before ANY write (migration deploy, task import, data fix) make a
  backup with the SQLite backup API into `/root/adaptive-course-backups/` and check `-wal`/`-shm` exist so ownership is kept.
- Deploy and data procedures: skills `deploy`, `task-bank`, `prod-data` in `.claude/skills/`.

## Product rules worth knowing (details in `backend/README.md` and `docs/decisions.md`)
- Progress: a topic is practised in iterations of 3 + 2 + 1 tasks (lessons N, N+1, N+3; a missed repetition stays due),
  3 iterations = mastered; the diagnostic may confirm topics. Rule in `IterationRule` (shared by crediting and analytics).
- Task selection: unsolved bank stories first (curated key `curated:<slug>:<n>`), then generation, a variant of a solved
  story only as the last resort; variants are ordered per student. Hard mode is a separate track over the hard bank.
- Task text: everything a student types or reads as program text/output is plain English ASCII; statements, hints and
  check messages are Russian and quote the English strings. Applies to the curated bank, hard bank, seeds and the LLM
  generator prompt.
- Teacher analytics «Прогресс» and the session forecast; «Показ группе» shows only anonymous group aggregates; students
  see only their own data — never medians, rankings or other students.
- Grades: individual tests at the board («К доске», `BoardTests`): the teacher calls a student from his laptop, the
  student takes a timed test on the classroom PC (projected) with the items the teacher chose: «Собери программу»,
  «Исправь ошибку», «Напиши код» (2/2/3 minutes, weights 1/2/3); checks + an LLM assessment and a suggested grade by
  points, capped by the session pace (borderline ≤ 4, behind ≤ 3) — visible only to the teacher, who sets the final
  grade and comment; the student sees date, grade, comment. «Работа на паре» (`PairWork`) is teacher-only analytics of
  a pair window.
