import type { CourseLanguage, Progress, SkillProgress } from './types'

// SQLite CURRENT_TIMESTAMP values are UTC without a zone ("2026-10-01 05:00:00"); Safari cannot parse them as-is.
export const parseDate = (value: string) => new Date(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$/.test(value) ? `${value.replace(' ', 'T')}Z` : value)

export const ITERATIONS = 3, TASKS_PER_ITERATION = 3
// A topic confirmed by the diagnostic earns a small XP bonus (shown separately), never task credit or iterations:
// a strong diagnostic should not outrank someone who has actually solved tasks.
export const XP = { task: 10, iteration: 20, mastery: 50, confirmed: 5 }
const RANKS = ['Новичок', 'Исследователь', 'Практик', 'Кодер', 'Разработчик', 'Инженер', 'Мастер кода']

export const skillStarted = (s: SkillProgress) => s.completedIterations > 0 || s.iterationSuccesses > 0
export const confirmedByDiagnostic = (s: SkillProgress) => !!s.confirmedByDiagnostic && !s.mastered

/**
 * Where a topic stands: mastered by practice, confirmed by the diagnostic (practice skipped), being practiced,
 * a gap the diagnostic found, or simply not reached yet.
 */
export type SkillState = 'mastered' | 'confirmed' | 'started' | 'gap' | 'new'
export function skillState(s: SkillProgress): SkillState {
  if (s.mastered) return 'mastered'
  if (s.confirmedByDiagnostic) return 'confirmed'
  if (skillStarted(s)) return 'started'
  return s.diagnosticTotal ? 'gap' : 'new'
}
/** A topic no longer needs practice when it is mastered or confirmed by the diagnostic. */
export const skillClosed = (s: SkillProgress) => !!s.mastered || !!s.confirmedByDiagnostic
export const skillPercent = (s: SkillProgress) => s.mastered ? 100
  : Math.round((s.completedIterations * TASKS_PER_ITERATION + Math.min(s.iterationSuccesses, TASKS_PER_ITERATION)) / (ITERATIONS * TASKS_PER_ITERATION) * 100)

/** XP is derived from server progress only, so it can never drift from what the backend credited. */
export function experience(progress: Progress) {
  const solved = progress.solvedTasks ?? progress.skills.reduce((n, s) => n + s.completedIterations * TASKS_PER_ITERATION + s.iterationSuccesses, 0)
  const iterations = progress.skills.reduce((n, s) => n + s.completedIterations, 0)
  const mastered = progress.skills.filter(s => s.mastered).length
  const confirmed = progress.skills.filter(confirmedByDiagnostic).length
  const closed = progress.skills.filter(skillClosed).length
  const practiceXp = solved * XP.task + iterations * XP.iteration + mastered * XP.mastery
  const diagnosticXp = confirmed * XP.confirmed
  const xp = practiceXp + diagnosticXp
  // Each level needs 40 XP more than the previous one: 100, 140, 180…
  let level = 1, floor = 0, need = 100
  while (xp >= floor + need) { floor += need; level++; need += 40 }
  return { xp, practiceXp, diagnosticXp, level, rank: RANKS[Math.min(level - 1, RANKS.length - 1)], into: xp - floor, need, solved, iterations, mastered, confirmed, closed, topics: progress.skills.length }
}

const dayKey = (date: Date) => `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`

/** Consecutive local days with at least one accepted solution, ending today (or yesterday, if today is still open). */
export function streak(activity: string[] = []) {
  const days = new Set(activity.map(value => dayKey(parseDate(value))))
  const today = new Date()
  const shift = (offset: number) => { const d = new Date(today); d.setDate(d.getDate() - offset); return d }
  const activeToday = days.has(dayKey(today))
  let count = 0
  for (let offset = activeToday ? 0 : 1; days.has(dayKey(shift(offset))); offset++) count++
  const week = Array.from({ length: 7 }, (_, i) => { const d = shift(6 - i); return { label: d.toLocaleDateString('ru-RU', { weekday: 'short' }).slice(0, 2), active: days.has(dayKey(d)), today: i === 6 } })
  return { count, activeToday, week }
}

export type IconName = 'bolt' | 'star' | 'flag' | 'target' | 'award' | 'flame' | 'sparkle' | 'compass' | 'globe' | 'crown'
export interface Achievement { id: string; title: string; description: string; icon: IconName; current: number; goal: number; unlocked: boolean }

/** Achievements inside one course; ids are namespaced by language so the same badge can be earned in Java and in Python. */
export function achievements(progress: Progress, language: CourseLanguage = 'JAVA'): Achievement[] {
  const { solved, iterations, mastered, confirmed, closed, topics } = experience(progress)
  const days = streak(progress.activity).count
  const started = progress.skills.filter(skillStarted).length
  // Gaps the diagnostic found and practice then closed: the core loop of the adaptive course.
  const gapsClosed = progress.skills.filter(s => s.mastered && s.diagnosticTotal && !s.confirmedByDiagnostic).length
  const list: Omit<Achievement, 'unlocked'>[] = [
    { id: 'strong-start', title: 'Сильный старт', description: 'Подтверди диагностикой 5 тем', icon: 'sparkle', current: confirmed, goal: 5 },
    { id: 'first-task', title: 'Первый шаг', description: 'Реши первую задачу', icon: 'bolt', current: solved, goal: 1 },
    { id: 'iteration', title: 'Цикл замкнут', description: 'Заверши итерацию из трёх задач', icon: 'target', current: iterations, goal: 1 },
    { id: 'tasks-10', title: 'Разогрев', description: 'Реши 10 задач', icon: 'star', current: solved, goal: 10 },
    { id: 'streak-3', title: 'В ритме', description: 'Решай задачи 3 дня подряд', icon: 'flame', current: days, goal: 3 },
    { id: 'skills-5', title: 'Широкий кругозор', description: 'Начни 5 разных тем', icon: 'compass', current: started, goal: 5 },
    { id: 'mastery', title: 'Мастер темы', description: 'Полностью освой первую тему', icon: 'award', current: mastered, goal: 1 },
    { id: 'gap-closed', title: 'Пробел закрыт', description: 'Освой практикой тему, где диагностика нашла пробел', icon: 'target', current: gapsClosed, goal: 1 },
    { id: 'streak-7', title: 'Неделя без пропусков', description: 'Решай задачи 7 дней подряд', icon: 'flame', current: days, goal: 7 },
    { id: 'tasks-50', title: 'Марафон', description: 'Реши 50 задач', icon: 'flag', current: solved, goal: 50 },
    { id: 'no-gaps', title: 'Без пробелов', description: 'Закрой все темы курса — практикой или диагностикой', icon: 'crown', current: closed, goal: Math.max(1, topics) },
  ]
  return list.map(a => ({ ...a, id: `${language}:${a.id}`, current: Math.min(a.current, a.goal), unlocked: a.current >= a.goal }))
}

/** Achievements that look across both courses. Languages without loaded progress count as empty. */
export function commonAchievements(byLanguage: Partial<Record<CourseLanguage, Progress>>): Achievement[] {
  const courses = Object.values(byLanguage).filter((p): p is Progress => !!p).map(experience)
  const solved = courses.reduce((n, c) => n + c.solved, 0)
  const withTasks = courses.filter(c => c.solved > 0).length
  const withMastery = courses.filter(c => c.mastered > 0).length
  const topLevel = courses.reduce((n, c) => Math.max(n, c.level), 1)
  const list: Omit<Achievement, 'unlocked'>[] = [
    { id: 'polyglot', title: 'Полиглот', description: 'Реши задачу и на Java, и на Python', icon: 'globe', current: withTasks, goal: 2 },
    { id: 'total-25', title: 'Четверть сотни', description: 'Реши 25 задач на любых языках', icon: 'star', current: solved, goal: 25 },
    { id: 'level-5', title: 'Пятый уровень', description: 'Достигни 5 уровня в любом курсе', icon: 'bolt', current: topLevel, goal: 5 },
    { id: 'double-master', title: 'Двойной мастер', description: 'Освой тему и в Java, и в Python', icon: 'crown', current: withMastery, goal: 2 },
    { id: 'total-100', title: 'Сотня', description: 'Реши 100 задач на любых языках', icon: 'flag', current: solved, goal: 100 },
  ]
  return list.map(a => ({ ...a, id: `common:${a.id}`, current: Math.min(a.current, a.goal), unlocked: a.current >= a.goal }))
}
