// IDs are SQLite rowids and booleans stored as INTEGER come back as 0/1 from raw JDBC queries.
export type Id = number
export type Flag = boolean | 0 | 1
export type Role = 'STUDENT' | 'TEACHER' | 'ADMIN'
export type CourseLanguage = 'JAVA' | 'PYTHON'
/** Hard mode readiness of one course: ready once every topic has a completed iteration, is mastered or confirmed by the diagnostic. */
export interface HardModeCourse { ready: boolean; remaining: number }
/** hardModeAllowed — the teacher's permission; hardModeOn — the student's own switch (only while allowed);
 *  hard mode is effective in a course only while hardModeCourses[course].ready (students only). */
export interface User { id: Id; login: string; role: Role; displayName: string; llmEnabled: Flag; hardModeAllowed?: boolean; hardModeOn?: boolean; hardModeCourses?: Partial<Record<CourseLanguage, HardModeCourse>> }
export interface MeResponse { user: User; llm: LlmStatus; runner: ServiceStatus }
export interface LlmStatus { globallyEnabled: boolean; studentEnabled: boolean; available: boolean; reason?: string; model?: string }
export interface ServiceStatus { available: boolean; reason?: string }
export interface DiagnosticQuestion { id: Id; ordinal: number; skillCode: string; prompt: string; options: string[] }
export interface Diagnostic { completed: boolean; questions: DiagnosticQuestion[] }
/** integrative — a complex task of a topic's 3rd iteration (the topic with 1–2 earlier ones, as at the attestation). */
export interface Task { id: Id; title: string; statement: string; starterCode?: string; redo?: boolean; hard?: boolean; integrative?: boolean }
/** Who or what closed a lesson; null while it is open and for lessons finished before the field existed. */
export type LessonFinishReason = 'STUDENT' | 'LOGOUT' | 'IDLE' | 'TEACHER'
/** lastActivityAt + idleMinutes: the server finishes the lesson (finishReason 'IDLE') once that moment has passed. */
export interface Lesson { id: Id; number: number; language?: CourseLanguage; startedAt: string; finishedAt?: string | null; finishReason?: LessonFinishReason | null; lastActivityAt?: string | null; idleMinutes?: number }
export interface LearningNext { lesson: Lesson; skill: { code: string; title: string; blockNo: number } | null; explanation: { content: string; source: string } | null; task: Task | null; reason?: string; llm?: LlmStatus
  /** retake — the task belongs to an open re-take; retakeDone — the re-take that was open and is over now. */
  retake?: Retake; retakeDone?: Retake
  /** practice — the task belongs to the open «Тренировочная аттестация» (retake is absent then); practiceDone — the practice that was open and is over now. */
  practice?: Practice; practiceDone?: Practice }
/** The program run as is, without hidden checks (POST /run, or alongside a check). */
export interface ConsoleRun { status: 'OK' | 'COMPILE_ERROR' | 'RUNTIME_ERROR' | 'LIMIT' | 'NO_MAIN' | 'UNAVAILABLE'; stdout: string; error?: string | null; truncated: boolean }
/** The LLM reviewer's verdict (experimental grading). A rejection always says why: summary plus issues. */
export interface Review { accepted: boolean; summary: string; issues: { line: number | null; problem: string; hint: string }[] }
export type Grader = 'TESTS' | 'LLM'
/** A wrong output in a task without hidden tests: the statement's expected output next to what the program printed. */
export interface OutputMismatch { expected: string; actual: string }
export interface Attempt { id: Id; passed: Flag; output?: string | null; console?: ConsoleRun | null; grader?: Grader; review?: Review | null; mismatch?: OutputMismatch | null }
export interface ChatMessage { id: Id | string; role: 'STUDENT' | 'ASSISTANT'; content: string; createdAt?: string }
/** Practice progress and, separately, the diagnostic result. confirmedByDiagnostic skips practice; it is not practice credit. */
export interface SkillProgress { skillCode: string; title: string; blockNo?: number; completedIterations: number; iterationSuccesses: number; mastered: Flag; diagnosticCorrect?: number | null; diagnosticTotal?: number | null; confirmedByDiagnostic?: Flag }
/** «Повторить тему» (POST /retakes): a series of `total` tasks on a closed topic; given — tasks given so far (the current one
 *  included), passed — solved; similar — the current task is a variant of a story the student solved («похожая на решённую»). */
export interface Retake { id: Id; skillCode: string; skillTitle: string; total: number; given: number; passed: number; finished: boolean; similar?: boolean }
/** Re-takes of a topic with at least one solved task: how many and when the last one started. */
export interface RetakeHistory { skillCode: string; times: number; lastAt: string }
/** «Тренировочная аттестация»: IN_TIME — the first passing submission by the deadline, LATE — after it, NOT_SOLVED — finished
 *  (or the lesson ended) without a solution; null — still open. */
export type PracticeResult = 'IN_TIME' | 'LATE' | 'NOT_SOLVED'
/** POST /attestation-practice, …/{id}/finish, /learning/next → practice / practiceDone: one task over topics 1…levelTopics.
 *  secondsLeft — server-computed, ≥ 0 (the client counts down from it); seconds — from the start to the first pass. */
export interface Practice {
  id: Id; levelTopics: number; levelTitle: string; minutes: number; startedAt: string; deadlineAt: string; secondsLeft: number
  finished: boolean; passed: boolean; result: PracticeResult | null; seconds: number | null
}
/** One attempt of the history (newest first): the student's own in GET /progress, the teacher's per course in the student card. */
export interface PracticeAttempt { id: Id; startedAt: string; levelTopics: number; levelTitle: string; taskTitle: string; result: PracticeResult | null; seconds: number | null }
export type PracticeByLanguage = Partial<Record<CourseLanguage, PracticeAttempt[]>>
/** GET /progress → attestationPractice. available — the pool has a task within the passed prefix of topics; levelTopics/levelTitle —
 *  the level (topics 1…levelTopics, the title of that topic); needTopics — while not available, how many more topics in order to
 *  pass to reach the lowest level (null: the course has no pool). */
export interface AttestationPractice { available: boolean; levelTopics: number | null; levelTitle: string | null; minutes: number; needTopics: number | null; history: PracticeAttempt[] }
export interface Progress { language?: CourseLanguage; skills: SkillProgress[]; solvedTasks?: number; hardSolved?: number; activity?: string[]; session?: StudentSession | null; retakes?: RetakeHistory[]; attestationPractice?: AttestationPractice }
export interface ActiveLesson { language: CourseLanguage; number: number; startedAt: string }
/** sessionParticipant — counted in the progress statistics (the teacher switches it off for themself, volunteers, test accounts). */
export interface Student { id: Id; login: string; role?: Role; displayName: string; llmEnabled: Flag; group?: string | null; activeLessons?: ActiveLesson[]; hardModeAllowed?: Flag; hardModeOn?: Flag; hardModeCourses?: Partial<Record<CourseLanguage, HardModeCourse>>; sessionParticipant?: boolean }
export interface Submission extends Attempt { sourceCode: string; createdAt: string; revokedAt?: string | null }
/** integrative — a complex task of a 3rd iteration; practice — a task of «Тренировочная аттестация». */
export interface LessonDetail { lesson: Lesson; chat: ChatMessage[]; tasks: { id: Id; title: string; statement: string; hard?: Flag; replaced?: Flag; retakeSkill?: string | null; integrative?: Flag; practice?: Flag; submissions: Submission[] }[] }
export interface LlmUsageTotals { calls: number; errors: number; timeouts: number; avgMs: number; p95Ms: number; inputTokens: number; cachedTokens: number; outputTokens: number; reasoningTokens: number; totalTokens: number; callsWithTokens: number; students: number; tasksAccepted: number; tasksRejected: number }
export type LlmPurpose = 'CHAT' | 'TASK' | 'EXPLANATION' | 'TASK_REPAIR' | 'REVIEW'
export interface LlmUsage {
  days: number; totals: LlmUsageTotals; llm: LlmStatus
  byDay: { day: string; calls: number; errors: number; tokens: number }[]
  byPurpose: { purpose: LlmPurpose; effort?: string | null; model?: string | null; calls: number; errors: number; avgMs: number; tokens: number }[]
  byLanguage: { language: CourseLanguage; calls: number; tokens: number }[]
  byStudent: { userId: Id | null; displayName: string; login?: string; groupName?: string | null; calls: number; chatTurns: number; errors: number; tokens: number; lastAt: string }[]
  recentErrors: { createdAt: string; purpose: LlmPurpose; language: CourseLanguage; status: 'ERROR' | 'TIMEOUT'; error?: string; durationMs: number; displayName?: string }[]
}
export interface ChatQuota { hourUsed: number; hourLimit: number; dayUsed: number; dayLimit: number; retryAfterSeconds: number }
export interface LlmLimits { chatPerHour: number; chatPerDay: number; tasksPerHour: number; explanationsPerHour: number; reviewsPerHour: number }
export interface LlmModel { id: string; displayName: string; description: string; efforts: string[]; defaultEffort: string; listed: boolean }
export type LlmPurposeKey = 'CHAT' | 'TASK' | 'EXPLANATION' | 'REVIEW'
export interface LlmLogging { generation: boolean; chat: boolean; review: boolean }
export interface LlmSettings {
  purposeModels: Record<LlmPurposeKey, string>; purposeModelDefaults: Record<LlmPurposeKey, string>; models: LlmModel[]
  reasoning: Record<LlmPurposeKey, string>; reasoningDefaults: Record<LlmPurposeKey, string>
  reasoningOptions: string[]; reasoningOptionsFromModel: boolean
  limits: LlmLimits; limitDefaults: LlmLimits; usageLastHour: { tasks: number; explanations: number; reviews: number }
  hardModeChat: boolean; hardModeChatDefault: boolean
  logging: LlmLogging; loggingDefaults: LlmLogging
}

// ───────── Progress analytics (GET /admin/progress, /admin/classroom, /admin/session; session in GET /progress) ─────────
/** Forecast status: DONE — every topic closed; null — no session date. */
export type SessionStatus = 'ON_TRACK' | 'BORDERLINE' | 'BEHIND' | 'DONE'
/** Teacher-only flags of a member. */
export type ProgressFlag = 'NOT_STARTED' | 'GONE' | 'STUCK' | 'BEHIND' | 'BORDERLINE'
/** The session date (YYYY-MM-DD) and weeks left until it; both null while the date is not set. */
export interface SessionInfo { date: string | null; weeksLeft: number | null }
export interface ProgressTopic { code: string; title: string; block: number }
/** Values at the end of each day of ProgressReport.days: skills in percent (one decimal), solved tasks, XP. */
/** closed: topics closed for the session at the end of each day (see SessionForecast). */
export interface ProgressSeries { skills: number[]; skillsWithDiagnostic: number[]; solved: number[]; xp: number[]; closed: number[] }
/**
 * The uniform plan to the session: from 0 topics on planStart (the group's first lesson in the course) to all topics on the
 * session day; planToday — topics the plan asks for by today; lag = planToday − closed (positive — behind, negative — ahead).
 * All three are null without a plan (no session date or no lessons yet).
 */
export interface SessionPlanFields { planStart: string | null; planToday: number | null; lag: number | null }
/** Topics «closed» for the session: at least one completed iteration, mastered, or confirmed by the diagnostic. Pace in topics per week. */
export interface SessionForecast extends SessionPlanFields {
  total: number; closed: number; closedByPractice: number; closedByDiagnostic: number; remaining: number
  pace: number; paceWeeks: number; status: SessionStatus | null; forecastDate: string | null
}
/** Activity within [from, to]: distinct active days, tasks first credited, of them solved with the first submission, submissions. */
export interface ProgressPeriod { activeDays: number; solved: number; firstTry: number; submissions: number }
/** member = participant && sessionCourse is this language; only members count in group statistics. forecast and flags only for members. */
export interface ProgressStudent {
  id: Id; login: string; displayName: string; group: string | null
  participant: boolean; sessionCourse: CourseLanguage | null; member: boolean
  firstLessonDay: string | null; lastActivityAt: string | null; lessons: number
  series: ProgressSeries
  /** Aligned with ProgressReport.topics, state at the end of `to`. */
  topicShare: number[]; topicConfirmed: boolean[]
  period: ProgressPeriod
  forecast: SessionForecast | null
  flags: ProgressFlag[]
}
/** days: every UTC day from min(from, the first lesson day in this language) to `to`; every series has days.length values. */
export interface ProgressReport {
  language: CourseLanguage; from: string; to: string; today: string
  days: string[]; session: SessionInfo; topics: ProgressTopic[]; students: ProgressStudent[]
}
/** The screen projected to a whole group: anonymous aggregates over its members only. tooSmall (members < 5) leaves week/daily/blocks/hardTopics empty. */
export interface Classroom {
  group: string; language: CourseLanguage; members: number; tooSmall: boolean
  session: SessionInfo; totalTopics: number
  week: { from: string; closedTopics: number; goal: number | null } | null
  daily: { day: string; closedTopics: number }[] | null
  blocks: { block: number; topics: string[]; avgShare: number }[] | null
  hardTopics: { code: string; title: string; attemptsPerSolve: number; students: number }[] | null
}
/** The student's own pace to the session (GET /progress → session). closedSeries: closed topics at the end of each of `days`. */
export interface StudentSession extends SessionPlanFields {
  date: string | null; weeksLeft: number | null
  total: number; closed: number; remaining: number
  pace: number; status: SessionStatus | null; forecastDate: string | null
  days: string[]; closedSeries: number[]
}

// ───────── Work in a pair (GET/POST /admin/pairs…): teacher-only analytics of a class period ─────────
/** WEEK — median of a previous week's saved results (medianWeek is that Monday); PAIR — of this pair itself; NONE — no median. */
export type MedianSource = 'WEEK' | 'PAIR' | 'NONE'
/** Tasks first solved in the window by difficulty, points (hard ×10), percent of the median; activeMinutes — 5 × the 5-minute
 *  slots with a submission or a chat message; submissions/failed and chatQuestions — this course, inside the window. */
export interface PairResult {
  userId: Id; login: string; displayName: string
  attended: boolean; points: number; tasks: { '1': number; '2': number; '3': number; hard: number }
  hard: boolean; percent: number | null; activeMinutes: number; submissions: number; failed: number; chatQuestions: number
}
/** id null — a preview, nothing saved. startsAt/endsAt — UTC instants. rows are absent in the list of pairs. */
export interface Pair {
  id: Id | null; group: string; language: CourseLanguage; startsAt: string; endsAt: string
  median: number | null; medianSource: MedianSource; medianWeek: string | null
  createdAt?: string | null; rows?: PairResult[]
}
export interface PairCell { attended: boolean; points: number; percent: number | null; activeMinutes: number }
/** Students × pairs; cells are aligned with pairs (oldest first), null — not a member then; pairs — how many pairs attended. */
export interface PairJournal {
  group: string; language: CourseLanguage
  pairs: { id: Id; startsAt: string; endsAt: string }[]
  students: { userId: Id; login: string; displayName: string; cells: (PairCell | null)[]; pairs: number }[]
}

// ───────── Test at the board (/board…, /admin/board…) ─────────
export type BoardStatus = 'CALLED' | 'CANCELLED' | 'EXPIRED' | 'STARTED' | 'FINISHED'
export type BoardGrade = '2' | '3' | '4' | '5'
/** The kinds of items the teacher chooses when calling; a test always has them in this order (parsons → fix → code). */
export type BoardItemKind = 'parsons' | 'fix' | 'code'
/** TEST — the test at the board; ATTESTATION — one «Напиши код» over the whole plan at the student's own computer (since 2026-10-27). */
export type BoardFormat = 'TEST' | 'ATTESTATION'
/** A movable line of «Собери программу»: text with its original indentation. */
export interface BoardLine { id: string; text: string }
/** One item of the student's view; never the solution order, which line is extra, the reference or the bug description. */
export type BoardStudentItem =
  | { kind: 'parsons'; title: string; statement: string; language: CourseLanguage; before: string; after: string; lines: BoardLine[]; extraLines: number }
  | { kind: 'fix'; title: string; statement: string; language: CourseLanguage; program: string }
  | { kind: 'code'; title: string; statement: string; language: CourseLanguage; starterCode?: string | null }
/** Only the chosen kinds: code/fix — the program text, parsons — ids of the placed lines in the student's order. */
export interface BoardAnswers { code?: string | null; fix?: string | null; parsons?: string[] | null }
/** The student's view: never the checks, scores, grades or the assessment. now — the server clock. */
export interface BoardStudentTest {
  id: Id; status: BoardStatus; startedAt: string; endsAt: string; now: string; durationSeconds?: number | null
  items: BoardStudentItem[]; answers: BoardAnswers
  /** The test runs in another browser (the board PC): only id, status, startedAt, endsAt and now come with it. */
  elsewhere?: boolean
  /** Bumped when the teacher replaces an item: the screen reloads the replaced items from this view. */
  revision?: number
  /** The student's name (station views only). */
  displayName?: string
  format?: BoardFormat
}
/** GET /board/current: the student's active call or their running test. canStart false — the test starts only at the board station. */
export interface BoardCurrent { call: { id: Id; calledAt: string; expiresAt: string; kinds?: BoardItemKind[] | null; durationSeconds?: number | null; canStart?: boolean; format?: BoardFormat } | null; test: BoardStudentTest | null }
/** A call shown on the board station. */
export interface StationCall {
  id: Id; displayName: string; group: string | null; language: CourseLanguage; kinds?: BoardItemKind[] | null; durationSeconds?: number | null
  calledAt: string; expiresAt: string; canStart: boolean; format?: BoardFormat
}
/** GET /station/current: the active calls and the test running on this station (at most one). now — the server clock. */
export interface StationCurrent { station: { id: Id; name: string }; now: string; calls: StationCall[]; test: BoardStudentTest | null }
/** A board station (a browser of the classroom PC that shows only the calls and the tests). */
export interface BoardStation { id: Id; name: string; createdAt: string; lastSeenAt: string | null; current?: boolean }
/** attestationPlanDate — the day whose plan line attestations cover (null: the day of each attestation). */
export interface BoardSettings { studentStart: boolean; attestationPlanDate?: string | null }
/** The student's own board grades in «Оценки и план»: Moscow date, the teacher's final grade and comment. */
/** One item of the report a student sees for a graded test (when the teacher shows it): never the reference or the scores. */
export interface BoardReportItem {
  kind: BoardItemKind; title: string | null; statement: string | null; language: CourseLanguage; answer: string | null
  verdict: 'верно' | 'частично верно' | 'неверно'; passed: boolean; check: string | null; extraUsed: boolean | null
}
export interface BoardStudentGrade { id: Id; date: string; grade: BoardGrade; comment: string | null; report: BoardReportItem[] | null; format?: BoardFormat }
export type AssessmentStatus = 'PENDING' | 'DONE' | 'UNAVAILABLE'
export interface BoardTestSummary {
  id: Id; userId: Id; displayName: string; status: BoardStatus
  calledAt: string; expiresAt: string | null; startedAt: string | null; endsAt: string | null; finishedAt: string | null
  suggestedGrade: BoardGrade | null; finalGrade: BoardGrade | null; assessmentStatus: AssessmentStatus | null
  kinds?: BoardItemKind[] | null; durationSeconds?: number | null; source?: BoardSource
  /** The station the test was started at; null — from the student's own account. */
  stationId?: Id | null; stationName?: string | null
  format?: BoardFormat
}
export interface BoardMember { userId: Id; login: string; displayName: string; present: boolean; lastTestAt: string | null; tests: number; lastGrade: BoardGrade | null
  /** Session members only (as in «Прогресс»): lag = plan for today − closed; farthest — the title of the farthest closed topic. */
  lag?: number | null; status?: SessionStatus | null; farthest?: string | null
  /** The latest attestation that was not cancelled or expired; at — started or called. tests, lastTestAt, lastGrade count only TEST. */
  attestation?: { testId: Id; status: BoardStatus; grade: BoardGrade | null; at: string } | null }
/** Where the items come from: the topics the student has reached, or the minimum for today (a uniform plan to the session). */
/** RANGE — the one rule since 2026-10-22 (from the minimum for today to the student's farthest topic); LEVEL, PACE — older calls. */
export type BoardSource = 'RANGE' | 'LEVEL' | 'PACE'
/** The minimum for today of the group: the first `topics` of `total` topics; null without a session date or lessons. */
export interface BoardPacePlan { topics: number; total: number; lastTopic: string | null; start: string; session: string }
/**
 * The attestation pool: tasks — fitting the plan (the whole course without a plan), total — the course's pool, minutes —
 * the default time; planDate — the set day of the plan (null: the day of the attestation), planTopics/planLastTopic — that plan.
 */
export interface BoardAttestationPool { tasks: number; total: number; minutes: number; planDate?: string | null; planTopics?: number | null; planLastTopic?: string | null }
export interface BoardOverview { group: string; language: CourseLanguage; members: BoardMember[]; suggested: Id | null; active: BoardTestSummary[]; pace?: BoardPacePlan | null; settings?: BoardSettings; attestation?: BoardAttestationPool | null }
/** An item with full data: parsons — before/after, lines, solution (ids in the reference order), extraLineId, reference;
 *  fix — program (the buggy one), bugDescription, reference; code — statement and starter. */
export interface BoardAdminItem {
  kind: BoardItemKind; language?: CourseLanguage; title?: string | null; statement?: string | null; starterCode?: string | null
  program?: string | null; bugDescription?: string | null; reference?: string | null
  before?: string | null; after?: string | null; lines?: BoardLine[] | null; solution?: string[] | null; extraLineId?: string | null
  taskId?: Id | null; externalKey?: string | null; skillCode?: string | null; skillTitle?: string | null; difficulty?: number | null
  /** The topic within the minimum for today or above it (tests since 2026-10-22). */
  zone?: 'minimum' | 'above' | null
  /** Tasks the teacher replaced in this item during the test. */
  replacedTaskIds?: Id[] | null
  /** Attestation item: it covers topics 1…covers of the course; planTopics — the plan's K at the start. */
  attestation?: boolean; covers?: number | null; coversTitle?: string | null; planTopics?: number | null
}
/** The check of one item; program — the assembled program of parsons. */
export interface BoardCheck { kind?: BoardItemKind; passed: Flag; output?: string | null; outcome?: string | null; feedback?: string | null; console?: ConsoleRun | null; unavailable?: Flag | null; program?: string | null }
export interface BoardRun { at?: string | null; createdAt?: string | null; item?: BoardItemKind | null; code: string; console: ConsoleRun }
export type BoardVerdict = 'верно' | 'частично верно' | 'неверно'
export interface BoardAssessment {
  status: AssessmentStatus; summary?: string | null; error?: string | null
  items?: { item: BoardItemKind; verdict: BoardVerdict | string; explanation: string }[] | null
  /** 1–2 short questions to ask the student aloud (teacher-only). */
  questions?: string[] | null
  /** The LLM's draft of the comment for the student; the student sees only what the teacher saves. */
  studentComment?: string | null
}
/** score per item: 1 passed, 0.5 «частично верно» by the LLM, 0 otherwise; points = Σ weight × score. */
export interface BoardScore { items: { kind: BoardItemKind; weight: number; score: number }[]; points: number; max: number; percent: number }
export interface BoardAdminTest extends BoardTestSummary {
  login?: string; group?: string | null; language?: CourseLanguage
  items: BoardAdminItem[] | null; answers: BoardAnswers | null
  /** Aligned with items, or keyed by kind. */
  results: BoardCheck[] | Partial<Record<BoardItemKind, BoardCheck>> | null
  runs: BoardRun[] | null; score?: BoardScore | null
  paceStatus: SessionStatus | null; ruleGrade: BoardGrade | null
  /** A student ahead of the minimum: every item from the minimum right → at least `grade`; met — null until checked; null — does not apply. */
  floor?: { grade: number; met: boolean | null } | null
  assessment: BoardAssessment | null; comment: string | null; gradedAt?: string | null
  /** «Показать студенту разбор»; true by default. */
  reportVisible?: boolean
  /** Attestation only: the constructs of the covered topics — expected: the reference uses it, used: the student's code (null without an answer). */
  coverage?: BoardCoverage[] | null
}
export interface BoardCoverage { construct: string; title: string; topicTitle: string | null; expected: boolean; used: boolean | null }
export interface BoardJournal {
  tests: { id: Id; userId: Id; displayName: string; calledAt: string; status: BoardStatus; finalGrade: BoardGrade | null; suggestedGrade: BoardGrade | null; format?: BoardFormat }[]
  /** grades — TEST only; attestations — final grades of finished attestations, oldest first. */
  students: { userId: Id; displayName: string; grades: (BoardGrade | null)[]; lastTestAt: string | null; attestations?: (BoardGrade | null)[] }[]
}
