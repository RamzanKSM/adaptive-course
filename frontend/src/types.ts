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
export interface Task { id: Id; title: string; statement: string; starterCode?: string; redo?: boolean; hard?: boolean }
/** Who or what closed a lesson; null while it is open and for lessons finished before the field existed. */
export type LessonFinishReason = 'STUDENT' | 'LOGOUT' | 'IDLE' | 'TEACHER'
/** lastActivityAt + idleMinutes: the server finishes the lesson (finishReason 'IDLE') once that moment has passed. */
export interface Lesson { id: Id; number: number; language?: CourseLanguage; startedAt: string; finishedAt?: string | null; finishReason?: LessonFinishReason | null; lastActivityAt?: string | null; idleMinutes?: number }
export interface LearningNext { lesson: Lesson; skill: { code: string; title: string; blockNo: number } | null; explanation: { content: string; source: string } | null; task: Task | null; reason?: string; llm?: LlmStatus
  /** Hard mode is on, but every hard task of the closed topics is already solved. */
  hardPracticeExhausted?: boolean }
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
export interface Progress { language?: CourseLanguage; skills: SkillProgress[]; solvedTasks?: number; hardSolved?: number; activity?: string[]; session?: StudentSession | null }
export interface ActiveLesson { language: CourseLanguage; number: number; startedAt: string }
/** sessionParticipant — counted in the progress statistics (the teacher switches it off for themself, volunteers, test accounts). */
export interface Student { id: Id; login: string; role?: Role; displayName: string; llmEnabled: Flag; group?: string | null; activeLessons?: ActiveLesson[]; hardModeAllowed?: Flag; hardModeOn?: Flag; hardModeCourses?: Partial<Record<CourseLanguage, HardModeCourse>>; sessionParticipant?: boolean }
export interface Submission extends Attempt { sourceCode: string; createdAt: string; revokedAt?: string | null }
export interface LessonDetail { lesson: Lesson; chat: ChatMessage[]; tasks: { id: Id; title: string; statement: string; hard?: Flag; replaced?: Flag; submissions: Submission[] }[] }
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
/** Topics «closed» for the session: at least one completed iteration, mastered, or confirmed by the diagnostic. Pace and needed pace in topics per week. */
export interface SessionForecast {
  total: number; closed: number; closedByPractice: number; closedByDiagnostic: number; remaining: number
  pace: number; paceWeeks: number; neededPace: number | null; status: SessionStatus | null; forecastDate: string | null
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
export interface StudentSession {
  date: string | null; weeksLeft: number | null
  total: number; closed: number; remaining: number
  pace: number; neededPace: number | null; status: SessionStatus | null; forecastDate: string | null
  days: string[]; closedSeries: number[]
}

// ───────── Pair grades (GET/POST /admin/pairs…, GET /grades) ─────────
/** «н» — absent; numeric grades as strings, the way the backend stores them. */
export type PairGrade = 'н' | '2' | '3' | '4' | '5'
/** WEEK — median of a previous week's saved results (medianWeek is that Monday); PAIR — of this pair itself; NONE — no median. */
export type MedianSource = 'WEEK' | 'PAIR' | 'NONE'
/** Teacher-only: points, tasks by difficulty, percent of the median. manual — grade differs from autoGrade or a comment is set. */
export interface PairResult {
  userId: Id; login: string; displayName: string
  attended: boolean; points: number; tasks: { '1': number; '2': number; '3': number; hard: number }
  hard: boolean; percent: number | null; autoGrade: PairGrade; grade: PairGrade; comment: string | null; manual: boolean
}
/** id null — a preview, nothing saved. startsAt/endsAt — UTC instants. rows are absent in the list of pairs. */
export interface Pair {
  id: Id | null; group: string; language: CourseLanguage; startsAt: string; endsAt: string
  median: number | null; medianSource: MedianSource; medianWeek: string | null
  thresholds: { five: number; four: number; three: number } | null
  published: boolean; publishedAt: string | null; createdAt?: string | null
  counts: Record<PairGrade, number>; rows?: PairResult[]
}
/** Students × pairs; grades and manual are aligned with pairs (oldest first). average over 2–5, absences — the number of «н». */
export interface PairJournal {
  group: string; language: CourseLanguage
  pairs: { id: Id; startsAt: string; endsAt: string; published: boolean }[]
  students: { userId: Id; login: string; displayName: string; grades: (PairGrade | null)[]; manual: boolean[]; average: number | null; absences: number }[]
}
/** The student's own grades of published pairs: the date and the grade, nothing else. */
export interface StudentGrade { date: string; grade: PairGrade }
