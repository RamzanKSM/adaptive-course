# Decisions agreed with the owner

Why things are the way they are. Newest first within each section. Mechanics live in `backend/README.md`; this file keeps
the reasoning and the open questions so a new agent does not re-ask settled points.

## Test at the board («вызов к доске», in design since 2026-10-15)
The owner finds grades for work during the pair inappropriate. New model: students study at home on the platform; in
class the teacher calls students one by one to a short individual test, projected for the group.
- Two criteria: the pace (above the session line) is required for a 5; the test gives the grade.
- Not every student every pair; the platform should suggest whom to call (longest not asked + randomness), the teacher
  decides — fair rotation, no impression of bias.
- One timer, the same for everyone given the same set of items (the minutes of the chosen items, below); at the end
  the answers are submitted and checked.
- A task that passes the checks counts fully. An unfinished one (e.g. a missing semicolon) gets a detailed LLM assessment:
  a proposed grade and why (approach, logic, remaining errors; the history of attempts is used), shown only to the
  teacher, never on the projector; the teacher reads it and announces the final grade. Student code is data, not
  instructions (same protection as the «calculate» review); without the LLM the teacher grades alone.
- After the time is up the teacher reviews the mistakes with the student (projector or not — to decide later).
- Pace caps the grade: on track (or course closed) → up to 5; borderline → at most 4; behind → at most 3.
- Grades come only from this test. The pair window stays as teacher-only analytics («Работа на паре», below).
- Two devices (decided 2026-10-15): the teacher calls a student from the admin on his laptop; the called student logs in on
  the classroom PC (projector) and only then can start the test; the call expires after 5 minutes. No «board device»
  binding. The teacher has full control over calls (cancel, replace, call again, edit, delete) — the system must not
  forbid him anything that is not destructive. After the test the student is logged out on that PC automatically.
- Students see their board-test grades and the teacher's comment.
- Content (2026-10-15, v2): the teacher chooses the items at each call (any of the three; random choice was rejected):
  «Собери программу» (Parsons: order the lines of a bank solution, one extra line from a wrong solution; an older topic;
  2 min, weight 1), «Исправь ошибку» (a bank wrong solution with a 1–2 line bug; a recent topic; 2 min, weight 2),
  «Напиши код» (a short task; a recent topic; 3 min, weight 3). Within a kind the bank difficulty is the same for
  everyone. «Что выведет этот код?» was dropped: it tested arithmetic and character-exact typing, not knowledge of code.
  Hard-mode students get the same kind of test.
- Grade by points, not by the number of items (owner: items of different difficulty must not count the same): an item
  counts fully when it passes the checks or the LLM finds it right, half when the LLM finds it partly right; 5 ≥ 90%, 4 ≥ 75%, 3 ≥ 50% of the
  chosen set's maximum, else 2; then the pace cap. The LLM also suggests 1–2 questions for an oral follow-up (teacher only).
- The LLM is lenient to the format of the console output (owner, 2026-10-19: at the board students write fast and the
  check compares the output strictly): a program that prints the right values and fails only because of spaces, line
  breaks, case, punctuation, labels or separators is «верно», and an LLM «верно» of a failed item now counts fully (before,
  only «частично верно» gave anything — half). The rule grade stays by the checks alone; the teacher sets the final grade.
- Layout (owner chose variant A of the mockups `docs/mockups/board/`, 2026-10-19): the student's screen fills the
  viewport — one-line header with the tabs and the timer, the statement on the left, the editor full height on the
  right with the console under it, the Parsons pool next to the program; the teacher's tab is a full-width three-column
  console: students to call, the test with items as tabs, a sticky «Итог» with the facts, the LLM and the grade form.
- The LLM drafts the comment for the student (owner, 2026-10-15): it fills the comment field until the teacher grades;
  the teacher edits it; the student sees only what the teacher saved.
- Open: showing the review on the projector — the classroom PC logs the student out right after the test, so a
  «Показать разбор» button needs a way to display there (e.g. the finished screen waits for the teacher).

## Work in a pair («Работа на паре»)
- A pair is a time window the teacher enters after the class (Moscow time) + group; teacher-only analytics of how the
  students worked: attendance, tasks first solved in the window (difficulty 1/2/3 points, hard-bank tasks ×10), active
  5-minute slots, submissions, questions to the assistant. Students see nothing of it.
- «Темп относительно группы» = points vs a weekly course median (previous Moscow week, regular non-hard attended students;
  first pairs use the pair's own median). The owner does not want students to know about the median.
- 2026-10-14…15 a pair also carried grades (thresholds on that median, manual grades, «без оценки», publishing). The owner
  found grading the work in class inappropriate; they were removed completely (V27 dropped the columns, the table is now
  `pair_results`) — don't bring them back; grades come from the test at the board.

## Teacher analytics and the session (since 2026-10-13)
- Tab «Прогресс»: growth per day (skills %, solved, XP — same formula as the student sees), a line per group member +
  median (mean in the tooltip), group comparison per member (never totals), blocks heat map, students table with flags.
- One session date for everyone. «Course closed» = every topic passed at least once (≥ 1 iteration or confirmed by the
  diagnostic), the whole course, no reduced scope. Pace = topics closed by practice in the last 3 weeks ÷ 3 (lessons per
  week do not matter). Status vs needed pace: ≥ 100% on track, 75–100% borderline, < 75% behind.
- Students see their own pace and the red «Не успеваешь» together with the needed pace; teacher-only flags (stuck,
  gone, not started). The «≥ 5 topics below the group median» flag was dropped: it mostly reflected diagnostic results.
- «Участвует в сессии» flag: off for the teacher, volunteers, test accounts — excluded from forecasts, group statistics
  and «Работа на паре»; no pace cap at the board.
- Visibility (pedagogy agreed with the owner): projected «Показ группе» = anonymous group aggregates only, no counts of
  students behind; students never get rankings or group medians; no CSV export (not needed).

## Task bank and selection
- 2026-10-14: a second story per topic and difficulty (18 tasks per topic, 1224 total) and story-aware selection:
  students complained about «the same task again with other numbers». Variants of a story are per student, so
  classmates get different numbers.
- 2026-10-14: all text a student types or reads as program text/output is English ASCII (owner did not want to switch
  keyboard layouts): curated bank, hard bank, seeds and a rule in the LLM generator prompt.
- 2026-10-15: the 83 old LLM tasks with Russian program text were translated in place (same ids, statement prose and
  titles stay Russian, submissions and credit untouched) and passed the platform validation (reference + wrong solutions
  on Piston). The owner's rule: fix such tasks, never deactivate them; bring the ones that cannot be fixed to him.
  Prompts, scripts and results: `agent-runs/llm-english/`.
- Open (2026-10-14): the seed «Чтение кода» tasks are fiddly (4–6 submissions per solve) — maybe rework.
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
