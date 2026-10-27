---
name: task-bank
description: Add, fix or translate tasks of the curated task bank (tools/curated_python, Python and Java) or the hard-mode bank, verify them on Piston and import them into production. Use for anything about «банк задач», new task families/stories, broken or disputed bank tasks, the hard bank.
---

# Curated task bank

`tools/curated_python/` (Python and Java despite the name):
- `topics/tNN_*.py` (Python) and `topics_java/tNN_*.py` (Java): one file per course topic, `TASKS = [...]` of families.
  A family = one story in 3 `variants` (same wording, different values); each topic has two families per difficulty
  1/2/3 (18 tasks). Key in the database: `curated:<slug>:<variant>` — never rename a slug (import updates by key, so
  students' credit and the story-aware selection stay attached).
- `build.py` (Python dataclasses `OutputTask`, `FunctionTask`; loads all topics), `java_tasks.py` (`JavaOutputTask`,
  `JavaFunctionTask`), authoring guides `NEW_STORIES_GUIDE.md` and `JAVA_TASKS_GUIDE.md`, `check_ascii.py`,
  `Verify.java` (platform verification), `import_bank.py` (production import).
- Hard requirements: all text in code/output is English ASCII (statements Russian, quoting the English strings); hidden
  value sets cover every branch and differ from the example; ≥ 2 wrong solutions that fail a check (not crash); nothing
  from later topics (see the module docstring of each topic); deterministic output; never print the word OOM.

## Pipeline
1. Edit topic files (for big jobs split topic files between parallel `claude -p` helpers — disjoint files — and give them
   `NEW_STORIES_GUIDE.md`).
2. Build and self-check locally (Java compiles with `javac --release 15`):
   ```sh
   cd tools/curated_python && python3 build.py --only <SKILL,...> --out <scratch>/bank.json   # no ✗ lines
   python3 check_ascii.py <scratch>/bank.json                                                  # 0 with Cyrillic in code
   ```
   Without `--only` it builds the whole bank (several minutes).
3. Verify on the production Piston (tunnel: see the `deploy` skill) with the platform's own `TaskVerifier`:
   ```sh
   cd backend && export JAVA_HOME=/Users/ramzankibiev/Library/Java/JavaVirtualMachines/corretto-21.0.5/Contents/Home
   mvn -q -o compile && mvn -q -o dependency:build-classpath -Dmdep.outputFile=<scratch>/cp.txt
   javac -cp "target/classes:$(cat <scratch>/cp.txt)" -d <scratch>/vout ../tools/curated_python/Verify.java
   java -cp "<scratch>/vout:target/classes:$(cat <scratch>/cp.txt)" ru.teacherstaff.adaptive.Verify <scratch>/bank.json <course.db> http://127.0.0.1:2779 <scratch>/verified.json
   ```
   `<course.db>` = any locally migrated database (start the backend once on an empty `APP_DATABASE_PATH`, it creates the
   schema and course topics) — never a copy of production. Expect «N verified, 0 failed».
4. Import (after the owner approved; back up first — see the `deploy` skill step 3):
   ```sh
   scp <scratch>/verified.json root@rmzn.net:/root/adaptive-course-backups/verified.json
   ssh root@rmzn.net 'cd /root/adaptive-course && git pull -q --ff-only; D=/var/lib/docker/volumes/adaptive-course_adaptive-data/_data/adaptive-tutor.db
   test -e $D-wal && test -e $D-shm && python3 tools/curated_python/import_bank.py /root/adaptive-course-backups/verified.json $D
   rm -f /root/adaptive-course-backups/verified.json'
   ```
   Run as root only with the `-wal`/`-shm` guard (keeps file ownership uid 10001). Prints «curated tasks: X inserted, Y
   updated». Commit the topic files too.

## Hard-mode bank
`tools/build_hard_bank.py` builds `backend/src/main/resources/hard-tasks/exercism.json` from Exercism
problem-specifications (see `backend/src/main/resources/hard-tasks/README.md`); it is loaded at backend startup by key
`exercism:<slug>:<language>`, so a rebuild ships with a normal deploy. English output (`yes`/`no`, `error`, …).

## Attestation pool («Аттестация» in «К доске»)
`tools/curated_python/attestation/*.py`: families written like the bank's (`JavaOutputTask`, `OutputTask` …) but with ONE
value set each — the stories differ, not the values (students called together must not get a hint from a neighbour).
`skill` = the last course topic the task covers; it must use nothing beyond it (Verify checks) and should touch every
topic up to it in about 10 minutes of work; `constructs` lists the control constructs it must use. Build:
`python3 build_attestation.py --out <scratch>/attest.json` (local self-check, keys `attest:<slug>`), `check_ascii.py`,
then Verify.java on Piston as above, and copy the verified file to
`backend/src/main/resources/attestation-tasks/bank.json` — it ships with a normal deploy (no import step);
`AttestationBank` loads it at startup with `tasks.mode = 'ATTESTATION'` and deactivates tasks that left the file.

## Other task sources
`source='LLM'` (generated, now with the English-in-code rule), `SEED` (`DiagnosticImporter.seedTasks`, updated by title
at startup). 82 older LLM tasks still print Russian text — translation pending (see `docs/decisions.md`).
