# Adding stories to the curated bank (Rmzn Tutor)

Written for the 2026-10-14 expansion (a second story per topic and difficulty); the same rules apply to any new family.

Project: `/Users/ramzankibiev/Stuff/TeacherStaff/adaptive_course` — adaptive Java/Python course for Russian-speaking
beginners. Curated bank: `tools/curated_python/` — `topics/tNN_*.py` (Python), `topics_java/tNN_*.py` (Java); builder
`build.py` (Python dataclasses `OutputTask`, `FunctionTask`) and `java_tasks.py` (`JavaOutputTask`, `JavaFunctionTask`).
Read both builders and every topic file you own before writing. For Java also read
`JAVA_TASKS_GUIDE.md` next to this file (how Java tasks are written and checked; its section «What to make» is
replaced by this guide).

## Why
Every topic now has exactly 3 families (difficulty 1, 2, 3), each with 3 `variants` — the same wording with different
values. A student practises a topic in up to three iterations of 3 + 2 + 1 tasks; repetitions need more tasks of
difficulty 2–3, and today they get another variant of a story they already solved — students complain about «the same
task again with other numbers». Your job: add a SECOND, genuinely different story for each difficulty of each topic you own.

## What to add (per topic file you own)
- Exactly 3 new families appended to `TASKS`: one of difficulty 1, one of 2, one of 3, each with exactly 3 `variants`
  (same wording, different values) and the usual `hidden` sets / `inputs`, `wrong` solutions, `constructs`, `checks`.
- Each new family trains the SAME topic at the SAME level as the existing family of that difficulty, but is a different
  situation and a different program: different everyday context, different data, different steps — not the old story with
  renamed nouns. Re-read the topic's module docstring and existing families: same allowed constructs (nothing from later
  topics), same task kind where it matters (output task vs function task), comparable size.
- New unique slugs following the file's pattern (e.g. `py-li-...`, `java-sel-...`); never change existing families,
  slugs or variants.
- Text in code and output: plain English, ASCII only (no Cyrillic, no «» — №), as in the existing tasks: printed text,
  string data, compared strings, names. Statement prose (title, intro, steps, hint) and check messages stay Russian, and
  every output example / value quoted in the prose must be exactly the English string. Currency `rub`, units like `kg`,
  `km/h`, people Anya, Boris…, cities Kazan, Sochi…
- Quality bar of the existing bank: a student who follows the steps literally gets exactly the expected output; hidden
  sets cover every branch and boundary and at least one hidden output differs from each variant; every wrong solution fails
  a check (not by crashing); no printing of default object toString or unordered sets/maps; never the standalone word OOM.

## Workflow
1. Edit only the topic files assigned to you; do NOT edit `build.py`, `java_tasks.py`, other files, the backend, git, the
   database or any server. Save each file as soon as it is done (other agents work in the same folder on other files).
2. Build only your topics:
   `cd /Users/ramzankibiev/Stuff/TeacherStaff/adaptive_course/tools/curated_python && python3 build.py --only <SKILLS> --out <your scratch folder>/<you>.json`
   Each topic must report 18 tasks with difficulties `[1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3]` (order may
   differ) and no `✗` lines.
3. `python3 check_ascii.py <that json>` (in this folder) must report
   `0 with Cyrillic in code`.
4. Read a few rendered statements of your new families from the JSON as a beginner would.
5. Final reply: files changed, the new slugs with one line about each story, builder summary lines, the check result,
   anything you were unsure about.
