# Decisions agreed with the owner

Why things are the way they are. Newest first within each section. Mechanics live in `backend/README.md`; this file keeps
the reasoning and the open questions so a new agent does not re-ask settled points.

## Grades per pair («Оценки», since 2026-10-14)
- A pair is a time window the teacher enters after the class (Moscow time) + group → «Высчитать оценки». Grades are
  hidden until «Показать студентам»; the teacher announces them himself.
- Points: tasks first solved inside the window; difficulty 1/2/3 points; hard-bank tasks ×10 (owner: hard must be worth
  much more).
- Grade relative to a weekly course median (per course, previous Moscow week, regular non-hard attended students; first
  pairs use the pair's own median): 5 ≥ 135%, 4 ≥ 100%, 3 ≥ 60%, else 2. The norm adapts as topics get harder.
- Students must never see the median, thresholds, points or percentages (owner fears they would collude to lower the
  median); they see only date + grade.
- «н» = no activity in the window. «-» = без оценки (excused, first day, the teacher's choice): no grade, no absence, not
  in any median, invisible to the student. On 2026-10-14 the teacher's manual «н» for attendees were converted to «-»;
  the two Python pairs of that day must not be recalculated (their pair medians included those students).
- Grade 3 stays (the teacher simply does not copy 3s into the official journal).
- Open (2026-10-14): (1) points by task cost — «normative minutes» (median time for the topic + step, rolling 4 weeks,
  weekly) vs fixed block multipliers; data shows the 1/2/3 step barely reflects effort and later topics take 2–3× longer;
  (2) whether activity (runs, active 5-minute slots, questions) should set a floor — undecided, runs are not stored yet;
  (3) the seed «Чтение кода» tasks are fiddly (4–6 submissions per solve) — maybe rework.

## Teacher analytics and the session (since 2026-10-13)
- Tab «Прогресс»: growth per day (skills %, solved, XP — same formula as the student sees), a line per group member +
  median (mean in the tooltip), group comparison per member (never totals), blocks heat map, students table with flags.
- One session date for everyone. «Course closed» = every topic passed at least once (≥ 1 iteration or confirmed by the
  diagnostic), the whole course, no reduced scope. Pace = topics closed by practice in the last 3 weeks ÷ 3 (lessons per
  week do not matter). Status vs needed pace: ≥ 100% on track, 75–100% borderline, < 75% behind.
- Students see their own pace and the red «Не успеваешь» together with the needed pace; teacher-only flags (stuck,
  gone, not started). The «≥ 5 topics below the group median» flag was dropped: it mostly reflected diagnostic results.
- «Участвует в сессии» flag: off for the teacher, volunteers, test accounts — excluded from forecasts, group statistics
  and grading.
- Visibility (pedagogy agreed with the owner): projected «Показ группе» = anonymous group aggregates only, no counts of
  students behind; students never get rankings or group medians; no CSV export (not needed).

## Task bank and selection
- 2026-10-14: a second story per topic and difficulty (18 tasks per topic, 1224 total) and story-aware selection:
  students complained about «the same task again with other numbers». Variants of a story are per student, so
  classmates get different numbers.
- 2026-10-14: all text a student types or reads as program text/output is English ASCII (owner did not want to switch
  keyboard layouts): curated bank, hard bank, seeds and a rule in the LLM generator prompt. Old LLM tasks with Russian
  output (82): to be translated and re-verified (not deactivated); open: deactivate those that fail re-verification?
- 2026-10-13: the curated bank exists because the LLM generator and the verifier kept disagreeing and students waited;
  same wording, different values; checked by substituting values (Python AST / Java static fields via reflection).
- 2026-10-13: for disputed checks prefer deterministic checks over an LLM review (collection choice via bytecode, a
  `finally` construct, main's `String[] args` is not «an array»). The LLM review stays only for «calculate» tasks.
- Hard mode (2026-10-14): a separate track over the Exercism-based hard bank in course order; generated hard tasks are
  retired; when the bank is solved the student sees HARD_BANK_COMPLETE.

## Students
- 2026-10-15: display names are «Имя Фамилия» (surnames restored from the logins: the first letter of the first name —
  two letters for a double name — plus the surname in Latin; a patronymic initial when two students share the name, e.g.
  «Юнус Алиев Л.»). No group labels inside names — the group is its own field. `mteacher` is a colleague's test account.

## Student UI
- After a failed check, «Запустить» on edited code hides the old verdict (it confused students); the attempt counter stays.
- Java editor hints (keywords, types, System.out.println, members after a dot, words from the code); no construct
  templates — beginners should type `for`/`if` themselves.
- Teacher card ⇄ «Прогресс» links both ways.
