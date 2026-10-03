// IDs are SQLite rowids and booleans stored as INTEGER come back as 0/1 from raw JDBC queries.
export type Id = number
export type Flag = boolean | 0 | 1
export type Role = 'STUDENT' | 'TEACHER' | 'ADMIN'
export interface User { id: Id; login: string; role: Role; displayName: string; llmEnabled: Flag }
export interface MeResponse { user: User; llm: LlmStatus; runner: ServiceStatus }
export interface LlmStatus { globallyEnabled: boolean; studentEnabled: boolean; available: boolean; reason?: string; model?: string }
export interface ServiceStatus { available: boolean; reason?: string }
export interface DiagnosticQuestion { id: Id; ordinal: number; skillCode: string; prompt: string; options: string[] }
export interface Diagnostic { completed: boolean; questions: DiagnosticQuestion[] }
export interface Task { id: Id; title: string; statement: string; starterCode?: string }
export interface Lesson { id: Id; number: number; startedAt: string; finishedAt?: string | null }
export interface LearningNext { lesson: Lesson; skill: { code: string; title: string; blockNo: number } | null; explanation: { content: string; source: string } | null; task: Task | null; reason?: string; llm?: LlmStatus }
export interface Attempt { id: Id; passed: Flag; output?: string | null }
export interface ChatMessage { id: Id | string; role: 'STUDENT' | 'ASSISTANT'; content: string; createdAt?: string }
export interface SkillProgress { skillCode: string; title: string; completedIterations: number; iterationSuccesses: number; mastered: Flag }
export interface Progress { skills: SkillProgress[]; solvedTasks?: number; activity?: string[] }
export interface Student { id: Id; login: string; role?: Role; displayName: string; llmEnabled: Flag }
export interface Submission extends Attempt { sourceCode: string; createdAt: string }
export interface LessonDetail { lesson: Lesson; chat: ChatMessage[]; tasks: { id: Id; title: string; statement: string; submissions: Submission[] }[] }
