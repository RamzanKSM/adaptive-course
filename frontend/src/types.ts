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
export interface LearningNext { lesson: Lesson; skill: { code: string; title: string; blockNo: number } | null; explanation: { content: string; source: string } | null; task: Task | null; reason?: string; llm?: LlmStatus }
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
export interface Progress { language?: CourseLanguage; skills: SkillProgress[]; solvedTasks?: number; hardSolved?: number; activity?: string[] }
export interface ActiveLesson { language: CourseLanguage; number: number; startedAt: string }
export interface Student { id: Id; login: string; role?: Role; displayName: string; llmEnabled: Flag; group?: string | null; activeLessons?: ActiveLesson[]; hardModeAllowed?: Flag; hardModeOn?: Flag; hardModeCourses?: Partial<Record<CourseLanguage, HardModeCourse>> }
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
