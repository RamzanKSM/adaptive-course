export type Role = 'STUDENT' | 'TEACHER' | 'ADMIN'
export interface User { id: string; login: string; role: Role; displayName: string; llmEnabled: boolean }
export interface MeResponse { user: User; llm: LlmStatus; runner: ServiceStatus }
export interface LlmStatus { globallyEnabled: boolean; studentEnabled: boolean; available: boolean; reason?: string; model?: string }
export interface ServiceStatus { available: boolean; reason?: string }
export interface DiagnosticQuestion { id: string; ordinal: number; skillCode: string; prompt: string; options: string[]; }
export interface Diagnostic { completed: boolean; questions: DiagnosticQuestion[]; }
export interface Task { id: string; title: string; statement: string; starterCode?: string; }
export interface Lesson { id: string; number: number; startedAt: string; finishedAt?: string; }
export interface LearningNext { lesson: Lesson; skill: { code: string; title: string; blockNo: number } | null; explanation: { content: string; source: string } | null; task: Task | null; reason?: string; llm?: LlmStatus }
export interface Attempt { id: string; passed: boolean; output?: string; }
export interface ChatMessage { id: string; role: 'STUDENT' | 'ASSISTANT'; content: string; createdAt?: string }
export interface Progress { skills: { skillCode: string; title: string; completedIterations: number; iterationSuccesses: number; mastered: boolean }[] }
export interface Student { id: string; login: string; role: Role; displayName: string; llmEnabled: boolean; }
