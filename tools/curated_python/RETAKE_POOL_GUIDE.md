# The re-take pool (Rmzn Tutor)

Written for the 2026-10-28 «Повторить тему» feature. Read `NEW_STORIES_GUIDE.md` first: every rule there applies (quality
bar, English ASCII in code and output, Russian prose, nothing from later topics, hidden sets, wrong solutions, slugs).
For Java also read `JAVA_TASKS_GUIDE.md`.

## Why
A student may re-take a topic already closed (mastered by practice or confirmed by the diagnostic): a series of three
tasks, difficulty 1 → 2 → 3. Mastery uses up the regular bank's stories, so re-takes get a pool of their own that regular
lessons and the test at the board never take (`tasks.mode = 'RETAKE'`).

## What to write (per topic you own)
- A NEW file with the SAME name as the topic's regular file: `retake/tNN_*.py` for `topics/tNN_*.py`, `retake_java/tNN_*.py`
  for `topics_java/tNN_*.py`. Copy the regular file's module docstring (what the topic allows) and `SKILL`, import the same
  builder classes, and define `TASKS` with exactly 3 families: difficulty 1, 2 and 3, each with exactly 3 `variants`.
- Each family is a genuinely new story: a situation, data and program different from ALL six stories of the topic's
  regular file (read them all) and from each other — not an old story with renamed nouns. Same level and kind as the
  regular family of that difficulty (output vs function task, comparable size), same allowed constructs.
- Slugs: the regular file's prefix plus `-rt-`, e.g. `py-if-rt-museum-ticket`, `java-if-rt-elevator-load`; unique in the
  whole bank (grep `slug=` across topics*/ and retake*/).

## Workflow
1. Edit only your files in `retake/` / `retake_java/`. Never touch topics*/, the builders, other files, git, the backend,
   any database or server.
2. `cd /Users/ramzankibiev/Stuff/TeacherStaff/adaptive_course/tools/curated_python && python3 build.py --pool retake --only <SKILLS> --out <scratch>/<you>.json`
   — every topic: `<SKILL> (re-take pool): 9 tasks, difficulties [1, 1, 1, 2, 2, 2, 3, 3, 3]`, no `✗` lines.
3. `python3 check_ascii.py <that json>` → `0 with Cyrillic in code`.
4. Read the rendered statements of your families as a beginner would: following the steps literally gives exactly the
   expected output.
5. Final reply: files written, each slug with one line about its story, the builder summary lines, the check result,
   anything you were unsure about.
