import { ChartPoint, ChartRule, ChartSeries, LineChart, LineKey } from './charts'
import type { SessionStatus, StudentSession } from './types'

// ───────── UTC calendar days (as the backend counts them) ─────────
const DAY_MS = 86_400_000
/** Days since 1970-01-01 for a UTC day «YYYY-MM-DD»: whole numbers that charts can use as x. */
export const dayNumber = (day: string) => Math.round(Date.parse(`${day}T00:00:00Z`) / DAY_MS)
export const dayString = (n: number) => new Date(n * DAY_MS).toISOString().slice(0, 10)
export const todayUtc = () => new Date().toISOString().slice(0, 10)
const yearOf = (n: number) => new Date(n * DAY_MS).getUTCFullYear()
/** «12 окт» (with the year when it is not the current one: «3 янв 2027»). */
export function shortDay(n: number) {
  const withYear = yearOf(n) !== new Date().getUTCFullYear()
  return new Date(n * DAY_MS).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: withYear ? 'numeric' : undefined, timeZone: 'UTC' })
    .replace(/\s+г\.$/, '').replace(/\./g, '')
}
/** «25 декабря» (or «1 апреля 2027»). */
export function longDay(day: string) {
  const n = dayNumber(day)
  const withYear = yearOf(n) !== new Date().getUTCFullYear()
  return new Date(n * DAY_MS).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: withYear ? 'numeric' : undefined, timeZone: 'UTC' }).replace(/\s+г\.$/, '')
}
/** «через 10 нед.», «через 5 дн.», «завтра», «сегодня», «уже прошла». */
export function untilText(day: string, today = todayUtc()) {
  const days = dayNumber(day) - dayNumber(today)
  if (days < 0) return 'уже прошла'
  if (days === 0) return 'сегодня'
  if (days === 1) return 'завтра'
  return days < 14 ? `через ${days} дн.` : `через ${Math.floor(days / 7)} нед.`
}
/** «Сессия: 25 декабря · через 10 нед.» */
export const sessionText = (date: string, today?: string) => `Сессия: ${longDay(date)} · ${untilText(date, today)}`

// ───────── Numbers and words ─────────
export function plural(n: number, one: string, few: string, many: string) {
  const mod10 = n % 10, mod100 = n % 100
  return mod10 === 1 && mod100 !== 11 ? one : mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14) ? few : many
}
const oneDecimal = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 1 })
export const decimal = (n: number) => oneDecimal.format(n)
/** «1,3 темы», «2 темы», «5 тем»: a fractional count takes the genitive singular. */
export function topics(n: number) {
  const rounded = Math.round(n * 10) / 10
  return `${decimal(rounded)} ${Number.isInteger(rounded) ? plural(rounded, 'тема', 'темы', 'тем') : 'темы'}`
}
/** «из 44 тем», «из 21 темы». */
export const ofTopics = (n: number) => `из ${n} ${plural(n, 'темы', 'тем', 'тем')}`
/** «+3», «−2», «0»: the lag against the plan, positive — behind. */
export const signedLag = (lag: number) => lag > 0 ? `+${lag}` : lag < 0 ? `−${-lag}` : '0'
/** «отстаёшь на 3 темы» / «опережаешь на 2 темы» / «идёшь по плану» (teacher: «отстаёт…»). */
export function lagText(lag: number, who: 'teacher' | 'student' = 'teacher') {
  const n = Math.abs(lag), count = `${n} ${plural(n, 'тему', 'темы', 'тем')}`
  if (lag > 0) return `${who === 'student' ? 'отстаёшь' : 'отстаёт'} на ${count}`
  if (lag < 0) return `${who === 'student' ? 'опережаешь' : 'опережает'} на ${count}`
  return who === 'student' ? 'идёшь по плану' : 'идёт по плану'
}

// ───────── Status ─────────
const STATUS: Record<SessionStatus, { tone: string; teacher: string; student: string }> = {
  ON_TRACK: { tone: 'ok', teacher: 'Успевает', student: 'Успеваешь' },
  BORDERLINE: { tone: 'warn', teacher: 'На грани', student: 'На грани' },
  BEHIND: { tone: 'bad', teacher: 'Не успевает', student: 'Не успеваешь' },
  DONE: { tone: 'done', teacher: 'Курс закрыт', student: 'Курс закрыт' },
}
/** Worst first: sorting by status puts the students who need help on top. */
export const STATUS_ORDER: Record<SessionStatus, number> = { BEHIND: 0, BORDERLINE: 1, ON_TRACK: 2, DONE: 3 }
export const statusLabel = (status: SessionStatus, who: 'teacher' | 'student' = 'teacher') => STATUS[status][who]

/** A coloured dot plus the word, so the status never relies on colour alone. */
export function StatusChip({ status, who = 'teacher' }: { status: SessionStatus | null; who?: 'teacher' | 'student' }) {
  if (!status) return <span className="muted">—</span>
  return <span className={`status-chip ${STATUS[status].tone}`}><i aria-hidden="true" />{STATUS[status][who]}</span>
}

// ───────── Session chart: closed topics, the plan line and the forecast ─────────
export interface SessionPlan {
  today: string; sessionDate: string | null
  total: number; closed: number; pace: number
  /** The start of the plan line (0 topics); without it there is no plan line. */
  planStart?: string | null
  /** Closed topics at the end of each day, when the history is known. */
  history?: { days: string[]; values: number[] }
}

/**
 * The lines of a session chart. The plan: from 0 topics at planStart to all topics at the session date (the same line for the
 * whole group); when the chart begins later than planStart, the line begins there with its value on that day.
 * Forecast at the current pace: up to the day all topics would be closed, or to the session date (without a date —
 * at most half a year ahead), whichever comes first; a zero pace is a flat line.
 */
export function sessionLines({ today, sessionDate, total, closed, pace, history, planStart }: SessionPlan) {
  const now = dayNumber(today)
  const session = sessionDate ? dayNumber(sessionDate) : null
  const series: ChartSeries[] = []
  const past: ChartPoint[] = history ? history.days.map((day, i) => ({ x: dayNumber(day), y: history.values[i] })) : []
  if (!past.length || past[past.length - 1].x < now) past.push({ x: now, y: closed })
  series.push({ id: 'closed', label: 'пройдено тем', points: past, color: 'var(--brand)', width: 2.5, dot: true, sticky: true })
  const remaining = Math.max(0, total - closed)
  const start = planStart ? dayNumber(planStart) : null
  if (start !== null && session !== null && session > start) {
    const from = Math.max(start, past[0].x)
    if (from < session) series.push({ id: 'plan', label: 'план к сессии', points: [{ x: from, y: (total * (from - start)) / (session - start) }, { x: session, y: total }], color: 'var(--ink-2)', width: 1.75, dash: 'dashed', sticky: true })
  }
  const horizon = session !== null && session > now ? session : pace > 0 ? now + 182 : null
  if (remaining > 0 && horizon !== null) {
    const reach = pace > 0 ? now + (remaining / pace) * 7 : Infinity
    const end = reach <= horizon ? { x: reach, y: total } : { x: horizon, y: closed + (pace * (horizon - now)) / 7 }
    series.push({ id: 'forecast', label: 'при текущем темпе', points: [{ x: now, y: closed }, end], color: 'var(--series-2)', width: 2, dash: 'dotted', sticky: true })
  }
  const vRules: ChartRule[] = []
  if (past.length > 1 && series.length > 1) vRules.push({ at: now, label: 'сегодня' })
  if (session !== null && session > now) vRules.push({ at: session, label: 'сессия' })
  return { series, vRules, hRules: [{ at: total, label: `все темы · ${total}` }] }
}

export function SessionChart({ plan, height = 220, label = 'Пройденные темы и прогноз до сессии' }: { plan: SessionPlan; height?: number; label?: string }) {
  const { series, vRules, hRules } = sessionLines(plan)
  const xs = series.flatMap(s => s.points.map(p => p.x))
  return <div className="session-chart">
    <LineChart series={series} label={label} height={height} tooltipAll integer
      xDomain={[Math.min(...xs), Math.ceil(Math.max(...xs, ...vRules.map(r => r.at)))]} yDomain={[0, plan.total]}
      formatX={shortDay} formatY={y => decimal(Math.round(y * 10) / 10)} vRules={vRules} hRules={hRules} />
    <div className="legend chart-legend">{series.map(s => <span key={s.id}><LineKey color={s.color} dash={s.dash} bold={s.id === 'closed'} />{s.label}</span>)}</div>
  </div>
}

// ───────── The student's own session card («Оценки и план») ─────────
/** Only the student's own numbers: status, position against the plan, pace, forecast and their own line. Never others' data. */
export function StudentSessionCard({ session }: { session: StudentSession }) {
  const today = session.days.length ? session.days[session.days.length - 1] : todayUtc()
  const done = session.status === 'DONE' || session.remaining <= 0
  const share = session.total ? Math.min(1, session.closed / session.total) : 0
  const afterSession = !!(session.date && session.forecastDate && session.forecastDate > session.date)
  const passed = !!session.date && dayNumber(session.date) <= dayNumber(today)
  return <section className="card session-card enter" aria-label="Темп до сессии">
    <div className="session-card-head">
      <div>
        <h2 className="card-title">{session.date ? 'До сессии' : 'Темп по курсу'}</h2>
        {session.date && <p className="muted small">{sessionText(session.date, today)}</p>}
      </div>
      {session.date && <StatusChip status={done ? 'DONE' : session.status} who="student" />}
    </div>
    <div className="session-facts">
      <div className="session-done">
        <b className="tabular">Пройдено {session.closed} {ofTopics(session.total)}</b>
        <div className="cover-bar" role="progressbar" aria-label="Пройдено тем курса" aria-valuemin={0} aria-valuemax={session.total} aria-valuenow={session.closed}><i style={{ width: `${share * 100}%` }} /></div>
      </div>
      {done ? <p className="session-line">Все темы курса пройдены — отличная работа!</p> : <>
        {session.date && session.planToday !== null && !passed
          ? <>
            <p className="session-line">По плану к сегодня — <b>{topics(session.planToday)}</b>, у тебя <b>{session.closed}</b>{session.lag !== null && <> — <span className={`lag-phrase ${session.lag > 0 ? 'behind' : 'ahead'}`}>{lagText(session.lag, 'student')}</span></>}</p>
            <p className="session-line">Твой темп — <b>{topics(session.pace)}</b> в неделю, осталось <b>{topics(session.remaining)}</b></p>
          </>
          : session.date && passed
            ? <p className="session-line">Дата сессии наступила, осталось <b>{topics(session.remaining)}</b>. Сейчас у тебя <b>{topics(session.pace)}</b> в неделю</p>
            : <p className="session-line">Твой темп — <b>{topics(session.pace)}</b> в неделю, осталось <b>{topics(session.remaining)}</b></p>}
        {session.date && <p className="session-line">{session.forecastDate
          ? <>При текущем темпе закончишь <b>{longDay(session.forecastDate)}</b>{afterSession ? ' — позже сессии' : ''}</>
          : 'При текущем темпе курс не будет закрыт'}</p>}
      </>}
    </div>
    {session.days.length > 0 && <SessionChart height={200} label="Твои пройденные темы и прогноз"
      plan={{ today, sessionDate: session.date, total: session.total, closed: session.closed, pace: session.date ? session.pace : 0, planStart: session.planStart, history: { days: session.days, values: session.closedSeries } }} />}
    <p className="muted small session-note">Тема пройдена, когда в ней завершена хотя бы одна итерация или её подтвердила диагностика. План — равномерно от начала курса в группе до сессии. Темп — сколько тем в неделю ты проходишь практикой, по последним трём неделям.</p>
  </section>
}
