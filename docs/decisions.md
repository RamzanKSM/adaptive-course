# Decisions agreed with the owner

Why things are the way they are. Newest first within each section. Mechanics live in `backend/README.md`; this file keeps
the reasoning and the open questions so a new agent does not re-ask settled points.

## Test at the board («вызов к доске», in design since 2026-10-15)
The owner finds grades for work during the pair inappropriate. New model: students study at home on the platform; in
class the teacher calls students one by one to a short individual test, projected for the group.
- «Аттестация» (owner, 2026-10-27): a call format of «К доске», not a separate mode. Rejected first: the whole group at
  once (he cannot watch everyone for cheating). Agreed: selected students, usually several at once at their own
  computers; one integrative «Напиши код» task touching all topics of the group's plan for today (option B; rejected A —
  items from parts of the plan); about 10 minutes, any other number, extendable — everything as in «К доске», no upper
  limits; completely different stories for students called together («чтобы даже подсказки не было») — a pool of
  stories, one value set each, a student gets one he never had and nobody is solving now; no logging of tab switches or
  pastes (he watches in person); lessons, the assistant and the console closed while it runs; no sign-out afterwards;
  a separate «Аттестация» line in the journal and for the student; the wheel counts only board tests. The pool for the
  first attestation is written by hand, later ones will be generated («потом разберёмся»). The plan line of one fixed
  day for every group (owner: «не усложнять, всем группам задачи темпа на пн 26.10») — the setting «План на дату»; the
  pool for 26.10 has a level per distinct plan: Java 9, 12, 14 topics, Python 10, 11, 14.
- One rule for the topics (owner, 2026-10-22, after the production data: in 19 of 63 tests «по уровню» gave «Собери
  программу»/«Исправь ошибку» on topics the student had not started — the early topics had no bank task with wrong
  solutions, so the search ran on through the course; students complained). The items come from a range: from the
  minimum for today (the group's plan line, the old «по темпу») up to the student's farthest topic (practice and the
  diagnostic count the same), never beyond. A student who does not know a topic he should already know gets a 2; one
  ahead gets interesting tasks: «Напиши код» from his farthest topic, «Исправь ошибку» from the middle, «Собери
  программу» from the minimum. The «по уровню / по темпу» switch is gone.
- No pace cap any more (owner: no double penalty for a student behind — the minimum is now tested by the items
  themselves). Reward for being ahead (owner chose variant 1 of three; rejected: a 5 only with an item above the
  minimum — again a cap for those on the line; calling those ahead less often): when the items from the minimum are all
  right, the suggested grade is at least 4 — a harder topic is a chance, not a risk.
- «Напиши код» was too easy (owner: «вывести остаток от деления — полная фигня»): difficulty 2, 3, then 1; neither trivial
  (< 3 lines) nor long preferred; a bank task before a generated one across the topics.
- The assessor of «Исправь ошибку» took the given program for the student's work and gave «частично верно» for doing
  nothing (4 of 12 such verdicts had no change at all): it now gets the student's changes separately and is told that
  the given code is not his merit and an unfixed bug is «неверно». The draft comment for the student is longer (4–6
  sentences: per item what worked, the error, what to revise; owner: «слишком короткое»).
- The early topics (Java 1–9, 19 Python topics) get bank stories with wrong solutions so that the minimum can be tested
  by «Собери программу» and «Исправь ошибку».
- «Компьютер у доски» (owner, 2026-10-22: logging students in and out on the classroom PC for every call is tedious): the
  teacher turns a browser into a board station once (button in «К доске»; a separate station cookie, no login/password —
  the owner chose a separate board account over a student test inside the admin account, because the admin session would
  leave the reference solutions and grades in the student's hands). The station shows only active calls and the running
  test; the student presses «Начать тест» at his name; nobody is signed out, the student's own lessons stay open.
  This replaces the 2026-10-15 «no board device» decision.
- Starting the test from the student's own account is off by default (setting «Студент может начать тест из своего
  аккаунта»); off — the student only sees that he is called.
- Editing a call (owner, 2026-10-22: delete + call again was frequent): the kinds and the topic source can be changed until
  the test starts. During the test the teacher can «Заменить задание» (another task of the kind, that answer reset, the
  timer goes on). Adding/removing items mid-test is not offered (the same time for the same set). Changing the student is
  not needed (cancel + call).
- (Superseded 2026-10-22: no pace criterion.) Two criteria: the pace (above the session line) is required for a 5; the test gives the grade.
- Not every student every pair; the platform should suggest whom to call (longest not asked + randomness), the teacher
  decides — fair rotation, no impression of bias.
- The list of students shows each member's standing as in «Прогресс» (owner, 2026-10-24: choosing whom to call meant
  switching to «Прогресс»; chose variant A of three — one line under the name, no new controls): the lag behind the plan
  line in the status colour and the farthest closed topic. The suggestion and the order did not change.
- One timer, the same for everyone given the same set of items (the minutes of the chosen items, below); at the end
  the answers are submitted and checked.
- A task that passes the checks counts fully. An unfinished one (e.g. a missing semicolon) gets a detailed LLM assessment:
  a proposed grade and why (approach, logic, remaining errors; the history of attempts is used), shown only to the
  teacher, never on the projector; the teacher reads it and announces the final grade. Student code is data, not
  instructions (same protection as the «calculate» review); without the LLM the teacher grades alone.
- After the time is up the teacher reviews the mistakes with the student (projector or not — to decide later).
- (Removed 2026-10-22.) Pace caps the grade: on track (or course closed) → up to 5; borderline → at most 4; behind → at most 3.
- Grades come only from this test. The pair window stays as teacher-only analytics («Работа на паре», below).
- Two devices (decided 2026-10-15): the teacher calls a student from the admin on his laptop; the called student logs in on
  the classroom PC (projector) and only then can start the test; the call expires after 5 minutes. No «board device»
  binding. The teacher has full control over calls (cancel, replace, call again, edit, delete) — the system must not
  forbid him anything that is not destructive. After the test the student is logged out on that PC automatically.
- Students see their board-test grades and the teacher's comment. Since 2026-10-19 also a report (owner: «почему бы не
  показывать студентам отчёт») — per item the statement, their own answer, the verdict (with the LLM, as in the score)
  and the lesson-style check message; never the reference, the bug, the solution order, the points, the suggested grade
  or the LLM's explanations, because the board takes unsolved bank stories that may still come up in the student's
  lessons and in classmates' tests. The teacher hides it per test with «Показать студенту разбор» (on by default); the
  teacher's view itself stays as it is (owner: no big changes there).
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
- One PC per test (bug fixed 2026-10-20): the called student's own PC stays signed in, so the test opened there too and
  at 0:00 both screens submitted — the idle one with blank answers could win. Now the browser that clicks «Начать тест»
  owns the test (a random per-browser token); other sessions show «Тест идёт на компьютере у доски», cannot save or
  submit, and return to the lesson afterwards (no sign-out there). Signing the other sessions out at the call was not
  needed.
- (Replaced by the one range rule 2026-10-22.) Topics of the items (owner, 2026-10-20): besides «по уровню» (the topics the student has reached) the teacher may call
  «по темпу на сегодня» — the minimum everyone should have covered by today, even topics the student has not reached.
  There was no such line in the analytics (the forecast is a per-student pace), so it is a uniform plan: the first
  ⌈total × (today − start) / (session − start)⌉ topics of the course, start = the group's first lesson in the course
  (owner chose this over a separate «начало курса» date). Default «по уровню», the choice is remembered in the browser;
  the grade and the pace cap do not depend on it.
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
- «Колесо фортуны» (owner, 2026-10-25): too many 5s at the board made a chocolate per 5 too costly, so one chocolate per
  pair goes to a wheel: the 5s at the board in the pair + the top 20% by the pair's points of those not called (owner's
  numbers). Agreed details: points rather than the number of tasks (easy tasks shouldn't pay), at least 1 point, 20%
  rounded up, ties at the border pass, the projected wheel shows names only (no ranking for students), the teacher may
  add or remove names, the server picks and keeps the winner. Test accounts and students outside the session take part
  (owner's choice) — unlike the pair's own analytics. The teacher names the prize (owner, same day; default «Шоколадка»,
  the last one is offered again); it is shown on the wheel and kept with the spin. Renamed «Жребий» the same day: the
  owner wanted a halal name instead of «Колесо фортуны» (drawing lots, no stake; code names stay `FortuneWheel`, `wheel_*`).
- Settings of «Жребий» (owner, same day): spin time, format «Стрелка» / «Выбывание» (the name under the arrow drops out
  until the winners are left; the decisive drop-out takes the full spin time), drop-out time, number of winners, every
  spin started by the teacher's button (or «сама»), top share, minimum points, the grade at the board, default prize,
  «приз-сюрприз» (hidden on the projector until the winners are known — the owner's idea), sounds and volume. The owner
  wants no limits on the values, only defaults, and rejected leaving out recent winners. A winner not in class is marked
  «Нет на паре» and a replacement is drawn from every name that has not won; runs can be deleted. Every step is picked by
  the server when it is spun (`draw_runs`, `draw_steps`, V34).

## Teacher analytics and the session (since 2026-10-13)
- Status by a global plan line (owner, 2026-10-22): the individual needed pace (remaining / weeks left vs the recent
  practice pace) was unfair — a student who closed 90% by the diagnostic and rested two weeks was «не успевает» and capped
  at 3 at the board. Now the plan is one line from 0 topics at the group's start (its first lesson in the course) to all
  topics at the session; status by the lag = plan for today − topics closed (diagnostic included): ≤ 0 on track, 1–2
  borderline (the owner chose an absolute lag over 75%: early in the course percentages jump), ≥ 3 behind. The same line is
  the board's «по темпу на сегодня» minimum and the classroom's week goal. The forecast at the current pace (dotted line,
  date) stays for display only, computed as before.
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

## Topic re-take («Повторить тему», 2026-10-27…28)
Several students asked to go through topics again. Agreed with the owner:
- Any closed topic, mastered by practice or confirmed by the diagnostic. A re-take is a series of 3 tasks, difficulty 1 → 2 → 3, inside the current lesson. It is allowed at any moment, with no caps. A student behind the plan line gets a soft hint («сначала лучше пройти новые») and is not blocked.
- A re-take never changes the topic's practice progress. That means iterations, mastery, closed topics, pace, the plan line, the forecast, the board range, hard-mode readiness and grades all stay as they are. Its solved tasks count in the solved number and XP (+10 each, no iteration/mastery bonus), and in the pair's points and «Жребий» (owner: «считать в очках пары»).
- Topics confirmed by the diagnostic have 0 iterations; a re-take of one must not start them either.
- «Заполни банк ещё и для повторного прохождения»: a separate re-take pool, 3 new stories per topic (one per difficulty) × 3 variants (`tasks.mode='RETAKE'`). Regular lessons and «К доске» never take it, otherwise mastery would use it up and re-takes would get «the same task with other numbers» again. Order: the pool's and the bank's unsolved stories, then generation, then a variant of the story solved longest ago, marked «похожая на решённую».
- The lesson's unsolved task waits during a re-take and comes back afterwards. Teacher screens change minimally: a chip on re-take tasks in the lesson review and a count in the student card.

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
- «Сессия истекла» (2026-10-21: students were signed out in class and lost their code): sign-in lasted exactly 7 days from
  the login, so a login at a weekly class expired in the middle of the next one, and the lesson code lived only in the
  page's memory. Now (2026-10-22) sessions slide (30 days without any request), the lesson code is kept as a draft in the
  browser per task, an expired session asks to sign in again over the screen without resetting it, and the sign-out after
  a board test does not finish the student's lessons.
- No ligatures in code (owner, 2026-10-22): JetBrains Mono drew `!=` as `≠`; beginners must see what they type.
- After a failed check, «Запустить» on edited code hides the old verdict (it confused students); the attempt counter stays.
- Java editor hints (keywords, types, System.out.println, members after a dot, words from the code); no construct
  templates — beginners should type `for`/`if` themselves.
- Teacher card ⇄ «Прогресс» links both ways.
- 2026-10-28 «Мой прогресс» was split (owner: «слишком разрослась»; he chose top-level tabs over sub-tabs or one
  compact page): «Текущий урок | Темы | Оценки и план | Достижения». «Темы» — the four numbers and the topic list with
  «Повторить»; «Оценки и план» — answers at the board and attestations, then «До сессии»; «Достижения» — both grids. On a
  phone the titles shorten to «Урок / Темы / Оценки / Награды». Board grades reload each time their tab opens.
