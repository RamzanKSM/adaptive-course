import { FormEvent, useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { api } from './api'
import { Tile } from './analytics'
import { ChartPoint, ChartSeries, LineChart, LineKey, SERIES_COLORS } from './charts'
import { ClassroomScreen } from './classroom'
import { Icon, initials, useToast } from './fx'
import { parseDate } from './game'
import { GroupFilter, groupCounts, inGroup, NO_GROUP, useGroupFilter } from './groups'
import { dayNumber, dayString, decimal, plural, SessionChart, sessionText, shortDay, StatusChip, STATUS_ORDER, todayUtc, topics } from './session'
import type { CourseLanguage, Id, ProgressFlag, ProgressReport, ProgressStudent } from './types'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>
type Metric = 'skills' | 'solved' | 'xp'
/** What the charts show: the metric, its level or its growth over the range, by calendar dates or by days since the first lesson. */
interface View { metric: Metric; scale: 'level' | 'growth'; axis: 'dates' | 'start'; diagnostic: boolean }
type Range = { kind: 'days'; days: number } | { kind: 'all' } | { kind: 'custom'; from: string; to: string }
/** A report with the indexes every chart and table needs. */
interface Context { report: ProgressReport; dayNums: number[]; startIdx: number }
interface Cohort { key: string; name: string; members: ProgressStudent[]; slot: number }

const COURSES: [CourseLanguage, string][] = [['JAVA', 'Java'], ['PYTHON', 'Python']]
const PRESETS = [7, 30, 90]
const METRICS: [Metric, string][] = [['skills', 'Навыки'], ['solved', 'Задачи'], ['xp', 'Опыт']]
/** Flags shown as chips; BEHIND / BORDERLINE are already the status. */
const FLAG_CHIPS: [ProgressFlag, string, string][] = [
  ['STUCK', 'Застрял', 'Пять и больше неудачных попыток подряд по задаче в открытом уроке'],
  ['NOT_STARTED', 'Не начал', 'Ещё не было ни одного урока на этом курсе'],
  ['GONE', 'Пропал', 'Нет активности 7 дней и больше'],
]
/** Fewer members than this: group numbers are noisy, and the classroom screen hides them. */
const SMALL_GROUP = 5
const LANGUAGE_KEY = 'rmzn-progress-language'
const collator = new Intl.Collator('ru', { numeric: true, sensitivity: 'base' })
const integer = new Intl.NumberFormat('ru-RU')
const compact = new Intl.NumberFormat('ru-RU', { notation: 'compact', maximumFractionDigits: 1 })

const round1 = (v: number) => Math.round(v * 10) / 10
const median = (values: number[]) => {
  if (!values.length) return NaN
  const sorted = [...values].sort((a, b) => a - b), mid = sorted.length >> 1
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2
}
const mean = (values: number[]) => values.length ? values.reduce((a, b) => a + b, 0) / values.length : NaN
const students = (n: number) => `${n} ${plural(n, 'студент', 'студента', 'студентов')}`
const lastOf = (values: number[]) => values.length ? values[values.length - 1] : 0

function valueFormat({ metric, scale }: View) {
  const growth = scale === 'growth'
  const sign = (v: number) => growth && v > 0 ? '+' : ''
  if (metric === 'skills') return (v: number) => `${sign(v)}${decimal(v)}${growth ? ' п.п.' : '%'}`
  if (metric === 'xp') return (v: number) => `${sign(v)}${integer.format(Math.round(v))} XP`
  return (v: number) => `${sign(v)}${decimal(v)}`
}
function tickFormat({ metric, scale }: View) {
  if (metric === 'skills') return (v: number) => `${decimal(v)}${scale === 'growth' ? '' : '%'}`
  return metric === 'xp' ? (v: number) => compact.format(v) : (v: number) => decimal(v)
}
const xFormat = (view: View) => view.axis === 'start' ? (x: number) => `${x} дн.` : shortDay
const xTipFormat = (view: View) => view.axis === 'start' ? (x: number) => x === 0 ? 'День первого урока' : `${x} ${plural(x, 'день', 'дня', 'дней')} от первого урока` : shortDay

const valuesOf = (s: ProgressStudent, metric: Metric, diagnostic: boolean) =>
  metric === 'skills' ? (diagnostic ? s.series.skillsWithDiagnostic : s.series.skills) : s.series[metric]
/** The state before index `from`: the previous day, or the starting state (0 for practice-only metrics). */
function baseline(values: number[], from: number, metric: Metric, diagnostic: boolean) {
  if (from > 0) return values[from - 1]
  return metric === 'solved' || (metric === 'skills' && !diagnostic) ? 0 : values[from] ?? 0
}
/** Skills (level and growth over the range) at the end of the range. */
function skillsAt(s: ProgressStudent, ctx: Context, diagnostic: boolean) {
  const values = valuesOf(s, 'skills', diagnostic)
  const level = lastOf(values)
  return { level, growth: round1(level - baseline(values, ctx.startIdx, 'skills', diagnostic)) }
}

/** The plotted line of a student: calendar days of the range, or days since their first lesson up to the end of the range. */
function studentLine(s: ProgressStudent, ctx: Context, view: View): ChartPoint[] {
  const values = valuesOf(s, view.metric, view.diagnostic)
  let from = ctx.startIdx
  if (view.axis === 'start') {
    from = s.firstLessonDay ? ctx.report.days.indexOf(s.firstLessonDay) : -1
    if (from < 0) return []
  }
  const base = view.scale === 'growth' ? baseline(values, from, view.metric, view.diagnostic) : 0
  const points: ChartPoint[] = []
  for (let i = from; i < values.length; i++) points.push({ x: view.axis === 'start' ? i - from : ctx.dayNums[i], y: round1(values[i] - base) })
  return points
}
/**
 * Median of the lines at each x; the mean and the count go to the tooltip. By days since the first lesson the lines have
 * different lengths: the median stops where fewer than half of them reach, so a couple of veterans do not make it jump.
 */
function medianLine(lines: ChartPoint[][], format: (v: number) => string): ChartPoint[] {
  const byX = new Map<number, number[]>()
  for (const line of lines) for (const p of line) { const list = byX.get(p.x); if (list) list.push(p.y); else byX.set(p.x, [p.y]) }
  const enough = Math.max(1, Math.ceil(lines.filter(l => l.length).length / 2))
  return [...byX].filter(([, ys]) => ys.length >= enough).sort((a, b) => a[0] - b[0])
    .map(([x, ys]) => ({ x, y: round1(median(ys)), note: `среднее ${format(round1(mean(ys)))} · ${students(ys.length)}` }))
}
/** Members by group (ungrouped ones as «Без группы»); a group keeps its colour slot from the course's full group list. */
function cohorts(members: ProgressStudent[], allGroups: string[]): Cohort[] {
  const byKey = new Map<string, ProgressStudent[]>()
  for (const s of members) { const key = s.group || NO_GROUP; byKey.set(key, [...(byKey.get(key) ?? []), s]) }
  return [...byKey].map(([key, list]) => ({ key, name: key === NO_GROUP ? 'Без группы' : key, members: list, slot: key === NO_GROUP ? allGroups.length : allGroups.indexOf(key) }))
    .sort((a, b) => a.slot - b.slot)
}
const cohortColor = (slot: number) => SERIES_COLORS[slot] ?? 'var(--muted)'

function storedLanguage(): CourseLanguage {
  try { return localStorage.getItem(LANGUAGE_KEY) === 'PYTHON' ? 'PYTHON' : 'JAVA' } catch { return 'JAVA' }
}

/** Teacher: growth of a group, forecast to the session per student, comparison of groups, and the classroom screen. */
export function ProgressAnalytics({ request, onOpenStudent }: { request: Request; onOpenStudent?: (id: Id) => void }) {
  const [language, setLanguageState] = useState<CourseLanguage>(storedLanguage)
  const setLanguage = (value: CourseLanguage) => { setLanguageState(value); try { localStorage.setItem(LANGUAGE_KEY, value) } catch { /* private mode */ } }
  const [range, setRange] = useState<Range>({ kind: 'days', days: 30 })
  /** The first lesson day of each course, learnt from responses: «Весь курс» starts there. */
  const [courseStart, setCourseStart] = useState<Partial<Record<CourseLanguage, string>>>({})
  const [report, setReport] = useState<ProgressReport | null>(null)
  const [loading, setLoading] = useState(true)
  const [reload, setReload] = useState(0)
  const [showOthers, setShowOthers] = useState(false)
  const [view, setView] = useState<View>({ metric: 'skills', scale: 'level', axis: 'dates', diagnostic: true })
  const [selectedId, setSelectedId] = useState<Id | null>(null)
  const [classroom, setClassroom] = useState<string | null>(null)
  const [group, setGroup] = useGroupFilter('rmzn-progress-group', report ? [...new Set(report.students.map(s => s.group).filter((g): g is string => !!g))] : null)

  const today = todayUtc()
  const query = range.kind === 'days' ? { from: dayString(dayNumber(today) - (range.days - 1)), to: today }
    : range.kind === 'custom' ? { from: range.from, to: range.to }
      : { from: courseStart[language] ?? dayString(dayNumber(today) - 29), to: today }
  const validRange = /^\d{4}-\d{2}-\d{2}$/.test(query.from) && /^\d{4}-\d{2}-\d{2}$/.test(query.to) && query.from <= query.to
  useEffect(() => {
    if (!validRange) return
    let alive = true
    setLoading(true)
    request(() => api<ProgressReport>(`/admin/progress?language=${language}&from=${query.from}&to=${query.to}`)).then(value => {
      if (!alive) return
      setLoading(false)
      if (!value) return
      setReport(value)
      const first = value.days[0]
      if (first && first < value.from) setCourseStart(c => c[value.language] === first ? c : { ...c, [value.language]: first })
    })
    return () => { alive = false }
  }, [language, query.from, query.to, validRange, reload, request])

  const ctx = useMemo<Context | null>(() => report && { report, dayNums: report.days.map(dayNumber), startIdx: Math.max(0, report.days.indexOf(report.from)) }, [report])
  const scope = useMemo(() => {
    if (!report) return null
    const visible = report.students.filter(s => showOthers || s.member)
    const shown = visible.filter(s => inGroup(group, s.group))
    const members = shown.filter(s => s.member)
    const outside = report.students.filter(s => !s.member && inGroup(group, s.group)).length
    const allGroups = groupCounts(report.students, s => s.group).groups.map(g => g.name)
    return { counts: groupCounts(visible, s => s.group), total: visible.length, shown, members, outside, cohorts: cohorts(members, allGroups) }
  }, [report, showOthers, group])
  const selected = report?.students.find(s => s.id === selectedId) ?? null
  const comparison = group === ''
  const canShow = !!group && group !== NO_GROUP
  const closeClassroom = useCallback(() => setClassroom(null), [])
  const rangeLabel = report ? `${shortDay(dayNumber(report.from))} — ${shortDay(dayNumber(report.to))}` : ''

  return <section className="analytics progress-admin">
    <div className="analytics-head enter">
      <div>
        <p className="eyebrow">Преподаватель</p>
        <h1 className="display small">Прогресс</h1>
        {report && <p className="muted small">{COURSES.find(c => c[0] === report.language)?.[1]} · {rangeLabel}{report.session.date ? ` · ${sessionText(report.session.date, report.today)}` : ' · дата сессии не задана'}</p>}
      </div>
      <Segment label="Курс" value={language} options={COURSES} onChange={value => { setLanguage(value); setSelectedId(null) }} />
    </div>

    <div className="card progress-controls enter">
      <div className="control-row">
        <span className="control-label">Период</span>
        <div className="period" role="group" aria-label="Период">
          {PRESETS.map(days => <button key={days} type="button" className={range.kind === 'days' && range.days === days ? 'active' : ''} aria-pressed={range.kind === 'days' && range.days === days} onClick={() => setRange({ kind: 'days', days })}>{days} дн.</button>)}
          <button type="button" className={range.kind === 'all' ? 'active' : ''} aria-pressed={range.kind === 'all'} onClick={() => setRange({ kind: 'all' })}>Весь курс</button>
        </div>
        <div className="date-range" role="group" aria-label="Свой период">
          <input type="date" aria-label="С" value={query.from} max={query.to || today} aria-invalid={!validRange}
            onChange={e => setRange({ kind: 'custom', from: e.target.value, to: query.to })} />
          <span aria-hidden="true">—</span>
          <input type="date" aria-label="По" value={query.to} min={query.from} max={today} aria-invalid={!validRange}
            onChange={e => setRange({ kind: 'custom', from: query.from, to: e.target.value })} />
        </div>
      </div>
      <SessionEditor request={request} onSaved={() => setReload(n => n + 1)} />
      <div className="control-row">
        <span className="control-label">Навыки</span>
        <Segment label="Навыки" value={view.diagnostic ? 'with' : 'practice'} options={[['with', 'С диагностикой'], ['practice', 'Только практика']]}
          onChange={value => setView(v => ({ ...v, diagnostic: value === 'with' }))} />
        <Toggle checked={showOthers} onChange={setShowOthers} hint="Отключённые от сессии (преподаватель, добровольцы, тестовые) и студенты другого курса. В статистике они не считаются никогда.">Показать не участвующих</Toggle>
      </div>
    </div>

    {report && scope && <div className="group-bar enter">
      <GroupFilter allLabel="Все группы" total={scope.total} groups={scope.counts.groups} ungrouped={scope.counts.ungrouped} value={group} onChange={value => { setGroup(value); setSelectedId(null) }} />
      <button type="button" className="secondary show-group" disabled={!canShow} title={canShow ? 'Экран для проектора: только общие цифры группы, без имён' : 'Выбери одну группу'} onClick={() => setClassroom(group)}>
        <Icon name="play" size={15} /> Показ группе</button>
    </div>}

    {!report || !scope || !ctx ? <div className="sk sk-card" /> : <div className={`progress-body ${loading ? 'is-refreshing' : ''}`}>
      <Tiles scope={scope} ctx={ctx} diagnostic={view.diagnostic} rangeLabel={rangeLabel} />
      {!scope.members.length && !scope.shown.length
        ? <div className="card empty-task"><span className="empty-icon"><Icon name="user" size={26} /></span><p className="muted">{comparison ? 'На этом курсе пока нет участников сессии.' : 'В этой группе нет участников этого курса.'}</p></div>
        : <>
          {comparison
            ? <ComparisonChart cohorts={scope.cohorts} ctx={ctx} view={view} onView={setView} />
            : <GroupChart key={`${group}|${report.language}`} title={group === NO_GROUP ? 'Без группы' : group} students={scope.shown} ctx={ctx} view={view} onView={setView} />}
          {comparison && scope.cohorts.length > 0 && <>
            <CohortTable cohorts={scope.cohorts} ctx={ctx} diagnostic={view.diagnostic} rangeLabel={rangeLabel} />
            <BlockHeat cohorts={scope.cohorts} report={report} diagnostic={view.diagnostic} />
          </>}
          <StudentTable rows={scope.shown} report={report} selectedId={selectedId} onSelect={id => setSelectedId(current => current === id ? null : id)} rangeLabel={rangeLabel} />
          {selected && <StudentPanel key={selected.id} student={selected} ctx={ctx} diagnostic={view.diagnostic} onClose={() => setSelectedId(null)} onOpenStudent={onOpenStudent} />}
        </>}
    </div>}
    {classroom && <ClassroomScreen language={language} group={classroom} onClose={closeClassroom} />}
  </section>
}

/** A row of mutually exclusive buttons in the `.period` look. */
function Segment<T extends string>({ label, value, options, onChange }: { label: string; value: T; options: [T, string][]; onChange: (value: T) => void }) {
  return <div className="period" role="group" aria-label={label}>
    {options.map(([key, title]) => <button key={key} type="button" className={key === value ? 'active' : ''} aria-pressed={key === value} onClick={() => key !== value && onChange(key)}>{title}</button>)}
  </div>
}

function Toggle({ checked, onChange, hint, children }: { checked: boolean; onChange: (value: boolean) => void; hint?: string; children: string }) {
  return <label className="toggle-line" title={hint}>
    <button type="button" role="switch" aria-checked={checked} className={`switch ${checked ? 'on' : ''}`} onClick={() => onChange(!checked)}><span /></button>
    {children}
  </label>
}

/** The session date for every course: read and saved through /admin/session. */
function SessionEditor({ request, onSaved }: { request: Request; onSaved: () => void }) {
  const [saved, setSaved] = useState<string | null | undefined>(undefined)
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const toast = useToast()
  useEffect(() => { request(() => api<{ date: string | null }>('/admin/session')).then(value => { if (value) { setSaved(value.date); setDraft(value.date ?? '') } }) }, [request])
  async function save(date: string | null) {
    setBusy(true)
    const value = await request(() => api<{ date: string | null }>('/admin/session', { method: 'PUT', body: JSON.stringify({ date }) }))
    setBusy(false)
    if (!value) return
    setSaved(value.date); setDraft(value.date ?? ''); onSaved()
    toast({ tone: 'info', icon: 'flag', title: value.date ? 'Дата сессии сохранена' : 'Дата сессии убрана', text: value.date ? sessionText(value.date) : 'Статус и нужный темп не считаются, пока дата не задана' })
  }
  const submit = (e: FormEvent) => { e.preventDefault(); if (draft) save(draft) }
  return <form className="control-row session-editor" onSubmit={submit}>
    <span className="control-label">Сессия</span>
    <input type="date" aria-label="Дата сессии" value={draft} min={todayUtc()} disabled={saved === undefined || busy} onChange={e => setDraft(e.target.value)} />
    <button className="primary" disabled={busy || !draft || draft === saved}>{busy ? <><span className="spinner" aria-hidden="true" /> Сохраняем…</> : 'Сохранить'}</button>
    {saved && <button type="button" className="ghost" disabled={busy} onClick={() => save(null)}>Убрать дату</button>}
    <span className="muted small">{saved === undefined ? 'Загружаем…' : saved ? sessionText(saved) : 'Дата не задана: статус и нужный темп не считаются'}</span>
  </form>
}

function Tiles({ scope, ctx, diagnostic, rangeLabel }: { scope: { members: ProgressStudent[]; outside: number; cohorts: Cohort[] }; ctx: Context; diagnostic: boolean; rangeLabel: string }) {
  const { members } = scope
  const active = members.filter(s => s.period.activeDays > 0).length
  const skills = members.map(s => skillsAt(s, ctx, diagnostic).level)
  const flagged = members.filter(s => s.flags.length > 0)
  const count = (flag: ProgressFlag) => members.filter(s => s.flags.includes(flag)).length
  const breakdown = ([['BEHIND', 'не успевают'], ['BORDERLINE', 'на грани'], ['STUCK', 'застряли'], ['GONE', 'пропали'], ['NOT_STARTED', 'не начали']] as [ProgressFlag, string][])
    .map(([flag, title]) => [count(flag), title] as const).filter(([n]) => n > 0).map(([n, title]) => `${title} ${n}`).join(' · ')
  const skillsMedian = median(skills), skillsMean = mean(skills)
  return <div className="stat-grid">
    <Tile icon="user" label="Участников" value={integer.format(members.length)}
      note={scope.outside ? `ещё ${scope.outside} вне статистики` : scope.cohorts.length > 1 ? `в ${scope.cohorts.length} ${plural(scope.cohorts.length, 'группе', 'группах', 'группах')}` : 'все участвуют в сессии'}
      title="Участник — студент, который участвует в сессии и учится в основном на этом курсе" />
    <Tile icon="flame" label="Активны за период" value={integer.format(active)} note={`${members.length ? Math.round((active / members.length) * 100) : 0}% участников · ${rangeLabel}`} />
    <Tile icon="chart" label="Навыки, медиана" value={members.length ? `${decimal(round1(skillsMedian))}%` : '—'}
      note={members.length ? `среднее ${decimal(round1(skillsMean))}% · ${diagnostic ? 'с диагностикой' : 'только практика'}` : 'нет участников'}
      title={members.length ? `Медиана ${decimal(round1(skillsMedian))}%, среднее ${decimal(round1(skillsMean))}%` : undefined} />
    <Tile icon="flag" label="Требуют внимания" value={integer.format(flagged.length)} note={breakdown || 'флагов нет'} tone={flagged.length ? 'warn' : undefined} />
  </div>
}

function ViewControls({ view, onView }: { view: View; onView: (view: View) => void }) {
  return <div className="view-controls">
    <Segment label="Показатель" value={view.metric} options={METRICS} onChange={metric => onView({ ...view, metric })} />
    <Segment label="Шкала" value={view.scale} options={[['level', 'Уровень'], ['growth', 'Прирост']]} onChange={scale => onView({ ...view, scale })} />
    <Segment label="Ось времени" value={view.axis} options={[['dates', 'По датам'], ['start', 'От начала обучения']]} onChange={axis => onView({ ...view, axis })} />
  </div>
}

function chartNote(view: View) {
  const what = view.metric === 'skills' ? `Навыки, % ${view.diagnostic ? 'с диагностикой' : 'только практика'}` : view.metric === 'solved' ? 'Решено задач' : 'Опыт, XP'
  const how = view.scale === 'growth' ? (view.axis === 'start' ? 'прирост от первого урока' : 'прирост с начала периода') : 'уровень на конец дня'
  return `${what} · ${how}${view.axis === 'start' ? ' · по оси — дни от первого урока каждого студента; медиана — пока данные есть хотя бы у половины' : ''}`
}

/** One thin line per member and a bold median; the list beside it highlights (hover) and pins (click) lines. */
function GroupChart({ title, students: shown, ctx, view, onView }: { title: string; students: ProgressStudent[]; ctx: Context; view: View; onView: (view: View) => void }) {
  const [pins, setPins] = useState<Map<Id, number>>(() => new Map())
  const [listHover, setListHover] = useState<Id | null>(null)
  const [chartHover, setChartHover] = useState<string | null>(null)
  const format = useMemo(() => valueFormat(view), [view])
  const tick = useMemo(() => tickFormat(view), [view])
  const lines = useMemo(() => shown.map(s => ({ s, points: studentLine(s, ctx, view) })), [shown, ctx, view])
  const medianPoints = useMemo(() => medianLine(lines.filter(l => l.s.member).map(l => l.points), format), [lines, format])
  const series = useMemo<ChartSeries[]>(() => [
    ...lines.map(({ s, points }) => {
      const slot = pins.get(s.id)
      return { id: String(s.id), label: s.displayName, points, color: slot === undefined ? undefined : SERIES_COLORS[slot], width: slot === undefined ? 1.25 : 2.25, faint: !s.member, dash: s.member ? undefined : 'dashed' as const, sticky: slot !== undefined }
    }),
    { id: 'median', label: 'медиана', points: medianPoints, color: 'var(--ink)', width: 3.25, sticky: true },
  ], [lines, medianPoints, pins])
  function togglePin(id: Id) {
    setPins(current => {
      const next = new Map(current)
      if (next.has(id)) { next.delete(id); return next }
      const used = new Set(next.values())
      const free = SERIES_COLORS.findIndex((_, i) => !used.has(i))
      if (free < 0) return current
      next.set(id, free)
      return next
    })
  }
  const sorted = [...lines].sort((a, b) => Number(b.s.member) - Number(a.s.member) || collator.compare(a.s.displayName, b.s.displayName))
  const highlighted = listHover !== null ? String(listHover) : null
  return <div className="card chart-card">
    <div className="chart-head">
      <h2 className="card-title">Рост группы {title}</h2>
      <ViewControls view={view} onView={onView} />
    </div>
    <p className="muted small chart-note">{chartNote(view)}</p>
    <div className="group-chart">
      <div className="group-chart-plot">
        <LineChart series={series} label={`Рост группы ${title}: линия на каждого участника и медиана`} formatX={xFormat(view)} formatXTip={xTipFormat(view)} xAnchor={view.axis === 'start' ? 'start' : 'end'}
          formatY={format} formatTick={tick} integer={view.metric !== 'skills'} highlight={highlighted} onHover={setChartHover} height={300}
          empty={view.axis === 'start' ? 'Никто из участников ещё не начал уроки' : undefined} />
        <div className="legend chart-legend">
          <span><LineKey />студент</span><span><LineKey color="var(--ink)" bold />медиана участников</span>
          {lines.some(l => !l.s.member) && <span><LineKey dash="dashed" />не участвует</span>}
          {pins.size > 0 && <button type="button" className="link" onClick={() => setPins(new Map())}>Снять выделение</button>}
        </div>
      </div>
      <ul className="member-list" aria-label="Студенты на графике: наведи, чтобы подсветить линию, нажми, чтобы закрепить">
        {sorted.map(({ s, points }) => {
          const slot = pins.get(s.id)
          const on = chartHover === String(s.id) || listHover === s.id
          const last = points[points.length - 1]
          return <li key={s.id}><button type="button" className={`member ${slot !== undefined ? 'pinned' : ''} ${on ? 'hover' : ''} ${s.member ? '' : 'outsider'}`} aria-pressed={slot !== undefined}
            onMouseEnter={() => setListHover(s.id)} onMouseLeave={() => setListHover(null)} onFocus={() => setListHover(s.id)} onBlur={() => setListHover(null)} onClick={() => togglePin(s.id)}>
            <LineKey color={slot !== undefined ? SERIES_COLORS[slot] : undefined} dash={s.member ? undefined : 'dashed'} bold={slot !== undefined} />
            <span className="member-name">{s.displayName}</span>
            <b className="tabular">{last ? format(last.y) : '—'}</b>
          </button></li>
        })}
      </ul>
    </div>
  </div>
}

/** «Все группы»: the median line of each group with the same metric and toggles. */
function ComparisonChart({ cohorts: list, ctx, view, onView }: { cohorts: Cohort[]; ctx: Context; view: View; onView: (view: View) => void }) {
  const format = useMemo(() => valueFormat(view), [view])
  const series = useMemo<ChartSeries[]>(() => list.map(c => ({
    id: c.key, label: c.members.length < SMALL_GROUP ? `${c.name} (мало данных)` : c.name,
    points: medianLine(c.members.map(s => studentLine(s, ctx, view)), format),
    color: cohortColor(c.slot), width: 2.5, dash: c.members.length < SMALL_GROUP ? 'dashed' as const : undefined,
  })), [list, ctx, view, format])
  return <div className="card chart-card">
    <div className="chart-head">
      <h2 className="card-title">Сравнение групп · медианы</h2>
      <ViewControls view={view} onView={onView} />
    </div>
    <p className="muted small chart-note">{chartNote(view)}. Линия группы — медиана её участников, среднее — в подсказке.</p>
    <LineChart series={series} label="Медианы групп" tooltipAll formatX={xFormat(view)} formatXTip={xTipFormat(view)} formatY={format} formatTick={tickFormat(view)} xAnchor={view.axis === 'start' ? 'start' : 'end'}
      integer={view.metric !== 'skills'} height={300} />
    <div className="legend chart-legend">{list.map(c => <span key={c.key}><LineKey color={cohortColor(c.slot)} dash={c.members.length < SMALL_GROUP ? 'dashed' : undefined} bold />
      {c.name}<small className="muted">{c.members.length}{c.members.length < SMALL_GROUP ? ' · мало данных' : ''}</small></span>)}</div>
  </div>
}

/** Groups side by side, always per member — never totals, which only reflect group size. */
function CohortTable({ cohorts: list, ctx, diagnostic, rangeLabel }: { cohorts: Cohort[]; ctx: Context; diagnostic: boolean; rangeLabel: string }) {
  return <div className="card">
    <h2 className="card-title">Группы</h2>
    <div className="table-scroll"><table className="data-table cohort-table">
      <thead><tr><th>Группа</th><th>Участники</th><th title={`Хотя бы один активный день за период: ${rangeLabel}`}>Активны</th><th title="Медиана навыков на конец периода; среднее — в подсказке">Навыки</th>
        <th title="Медиана прироста навыков за период, в процентных пунктах; среднее — в подсказке">Рост</th><th title="Задач решено за период в среднем на участника">Решено / чел.</th><th title="Опыт в среднем на участника">XP / чел.</th></tr></thead>
      <tbody>{list.map(c => {
        const n = c.members.length
        const skills = c.members.map(s => skillsAt(s, ctx, diagnostic))
        const level = skills.map(v => v.level), growth = skills.map(v => v.growth)
        const active = c.members.filter(s => s.period.activeDays > 0).length
        const solved = c.members.reduce((sum, s) => sum + s.period.solved, 0) / n
        const xp = mean(c.members.map(s => lastOf(s.series.xp)))
        return <tr key={c.key} className={n < SMALL_GROUP ? 'noisy' : ''}>
          <td><span className="cohort-name"><LineKey color={cohortColor(c.slot)} bold />{c.name}</span>{n < SMALL_GROUP && <span className="noisy-tag" title={`Меньше ${SMALL_GROUP} участников: цифры сильно зависят от одного-двух человек`}>мало данных</span>}</td>
          <td>{n}</td>
          <td>{active} <small className="muted">· {Math.round((active / n) * 100)}%</small></td>
          <td title={`Медиана ${decimal(round1(median(level)))}%, среднее ${decimal(round1(mean(level)))}%`}>{decimal(round1(median(level)))}%</td>
          <td title={`Медиана ${decimal(round1(median(growth)))} п.п., среднее ${decimal(round1(mean(growth)))} п.п.`}>{signed(round1(median(growth)))} п.п.</td>
          <td>{decimal(round1(solved))}</td>
          <td>{integer.format(Math.round(xp))}</td>
        </tr>
      })}</tbody>
    </table></div>
    <p className="muted small table-note">Навыки — {diagnostic ? 'с диагностикой' : 'только практика'}, на конец периода. Рост — разница навыков за период ({rangeLabel}).</p>
  </div>
}
const signed = (v: number) => `${v > 0 ? '+' : ''}${decimal(v)}`

/** Rows — course blocks, columns — groups; a cell is the members' average topic share in the block. */
function BlockHeat({ cohorts: list, report, diagnostic }: { cohorts: Cohort[]; report: ProgressReport; diagnostic: boolean }) {
  const blocks = useMemo(() => {
    const byBlock = new Map<number, number[]>()
    report.topics.forEach((t, i) => byBlock.set(t.block, [...(byBlock.get(t.block) ?? []), i]))
    return [...byBlock].sort((a, b) => a[0] - b[0]).map(([block, indexes]) => ({ block, indexes, titles: indexes.map(i => report.topics[i].title) }))
  }, [report.topics])
  const share = (s: ProgressStudent, i: number) => diagnostic && s.topicConfirmed[i] ? 1 : s.topicShare[i] ?? 0
  const cell = (c: Cohort, indexes: number[]) => mean(c.members.map(s => mean(indexes.map(i => share(s, i)))))
  if (!blocks.length) return null
  return <div className="card">
    <h2 className="card-title">Навыки по блокам</h2>
    <p className="muted small chart-note">Средняя доля освоения тем блока у участников группы{diagnostic ? '; тема, подтверждённая диагностикой, считается освоенной' : ''}.</p>
    <div className="table-scroll"><table className="heat-table">
      <thead><tr><th scope="col">Блок</th>{list.map(c => <th key={c.key} scope="col">{c.name}{c.members.length < SMALL_GROUP && <small className="noisy-tag">мало данных</small>}</th>)}</tr></thead>
      <tbody>{blocks.map(b => <tr key={b.block}>
        <th scope="row" title={b.titles.join('\n')}>Блок {b.block}<small className="muted">{b.titles.length} {plural(b.titles.length, 'тема', 'темы', 'тем')}</small></th>
        {list.map(c => {
          const value = cell(c, b.indexes)
          return <td key={c.key} className={`heat ${value > 0.55 ? 'strong' : ''}`} style={{ background: `rgb(var(--brand-rgb) / ${(0.04 + value * 0.86).toFixed(3)})` }}
            title={`${c.name} · Блок ${b.block}: ${Math.round(value * 100)}% (${students(c.members.length)})`}>{Math.round(value * 100)}%</td>
        })}
      </tr>)}</tbody>
    </table></div>
  </div>
}

type SortKey = 'name' | 'group' | 'closed' | 'pace' | 'needed' | 'status' | 'forecast' | 'last' | 'active' | 'solved' | 'xp' | 'flags'
const COLUMNS: { key: SortKey; title: string; hint?: string; asc?: boolean; text?: boolean }[] = [
  { key: 'name', title: 'Студент', asc: true, text: true },
  { key: 'group', title: 'Группа', asc: true, text: true },
  { key: 'closed', title: 'Пройдено', hint: 'Темы с завершённой итерацией или подтверждённые диагностикой — из всех тем курса' },
  { key: 'pace', title: 'Темп', hint: 'Тем в неделю: первые итерации за последние 3 недели' },
  { key: 'needed', title: 'Нужно', hint: 'Тем в неделю, чтобы закрыть курс к сессии' },
  { key: 'status', title: 'Статус', asc: true, text: true },
  { key: 'forecast', title: 'Прогноз', hint: 'Когда курс будет закрыт при текущем темпе', asc: true },
  { key: 'last', title: 'Активность', hint: 'Последняя активность на этом курсе' },
  { key: 'active', title: 'Дней', hint: 'Активных дней за период' },
  { key: 'solved', title: 'Решено', hint: 'Задач решено за период; с первой попытки — в подсказке' },
  { key: 'xp', title: 'XP', hint: 'Опыт на конец периода' },
  { key: 'flags', title: 'Флаги', text: true },
]
const chipFlags = (s: ProgressStudent) => FLAG_CHIPS.filter(([flag]) => s.flags.includes(flag))
function sortValue(s: ProgressStudent, key: SortKey): number | string | null {
  const f = s.forecast
  switch (key) {
    case 'name': return s.displayName
    case 'group': return s.group ?? null
    case 'closed': return f ? f.closed / (f.total || 1) : null
    case 'pace': return f ? f.pace : null
    case 'needed': return f?.neededPace ?? null
    case 'status': return f?.status ? STATUS_ORDER[f.status] : null
    case 'forecast': return f?.forecastDate ? dayNumber(f.forecastDate) : null
    case 'last': return s.lastActivityAt ? parseDate(s.lastActivityAt).getTime() : null
    case 'active': return s.period.activeDays
    case 'solved': return s.period.solved
    case 'xp': return lastOf(s.series.xp)
    case 'flags': return s.member ? -s.flags.length : null
  }
}
/** «сегодня», «вчера», «3 дн. назад», then the date. */
function ago(value: string | null, today: string) {
  if (!value) return '—'
  const day = parseDate(value).toISOString().slice(0, 10)
  const days = dayNumber(today) - dayNumber(day)
  return days <= 0 ? 'сегодня' : days === 1 ? 'вчера' : days < 7 ? `${days} дн. назад` : shortDay(dayNumber(day))
}
const outsiderLabel = (s: ProgressStudent) => !s.participant ? 'не участвует' : 'другой курс'

function StudentTable({ rows, report, selectedId, onSelect, rangeLabel }: { rows: ProgressStudent[]; report: ProgressReport; selectedId: Id | null; onSelect: (id: Id) => void; rangeLabel: string }) {
  const [sort, setSort] = useState<{ key: SortKey; dir: 1 | -1 }>({ key: 'name', dir: 1 })
  const sorted = useMemo(() => [...rows].sort((a, b) => {
    const byName = collator.compare(a.displayName, b.displayName)
    const outside = Number(!a.member) - Number(!b.member)
    if (outside) return outside
    const va = sortValue(a, sort.key), vb = sortValue(b, sort.key)
    if (va === null || vb === null) return va === vb ? byName : va === null ? 1 : -1 // empty values last in both directions
    const result = typeof va === 'string' ? collator.compare(va, String(vb)) : va - (vb as number)
    return result * sort.dir || byName
  }), [rows, sort])
  const order = (key: SortKey) => setSort(s => s.key === key ? { key, dir: s.dir === 1 ? -1 : 1 } : { key, dir: COLUMNS.find(c => c.key === key)?.asc ? 1 : -1 })
  const sessionDate = report.session.date
  return <div className="card">
    <div className="chart-head">
      <h2 className="card-title">Студенты <span className="muted small">{rows.filter(s => s.member).length} участников{rows.some(s => !s.member) ? ` · ${rows.filter(s => !s.member).length} вне статистики` : ''}</span></h2>
      <span className="muted small">Период: {rangeLabel}. Нажми на строку — откроется график студента.</span>
    </div>
    {!rows.length ? <p className="muted">Студентов нет.</p> : <div className="table-scroll"><table className="data-table student-table">
      <thead><tr>{COLUMNS.map(c => <th key={c.key} className={c.text ? 'text' : ''} aria-sort={sort.key === c.key ? (sort.dir === 1 ? 'ascending' : 'descending') : undefined} title={c.hint}>
        <button type="button" className="sort" onClick={() => order(c.key)}>{c.title}<span aria-hidden="true">{sort.key === c.key ? (sort.dir === 1 ? '↑' : '↓') : ''}</span></button>
      </th>)}</tr></thead>
      <tbody>{sorted.map(s => {
        const f = s.forecast
        const late = !!(f?.forecastDate && sessionDate && f.forecastDate > sessionDate)
        return <tr key={s.id} className={`${s.member ? '' : 'outsider'} ${selectedId === s.id ? 'selected' : ''}`} onClick={() => onSelect(s.id)}>
          <td className="text"><button type="button" className="row-link" aria-expanded={selectedId === s.id} onClick={e => { e.stopPropagation(); onSelect(s.id) }}>{s.displayName}</button>
            <small className="muted"> {s.login}</small>{!s.member && <span className="outsider-tag">{outsiderLabel(s)}</span>}</td>
          <td className="text">{s.group ?? <span className="muted">—</span>}</td>
          <td>{f ? `${f.closed}/${f.total}` : '—'}</td>
          <td>{f ? decimal(f.pace) : '—'}</td>
          <td>{f?.neededPace != null ? decimal(f.neededPace) : '—'}</td>
          <td className="text">{f ? <StatusChip status={f.status} /> : <span className="muted">—</span>}</td>
          <td className={late ? 'late' : ''} title={late ? 'Позже сессии' : f && !f.forecastDate && f.remaining > 0 ? 'За последние 3 недели новых тем не было — при таком темпе курс не будет закрыт' : undefined}>
            {f?.forecastDate ? shortDay(dayNumber(f.forecastDate)) : f && f.remaining === 0 ? 'закрыт' : '—'}</td>
          <td title={s.lastActivityAt ? parseDate(s.lastActivityAt).toLocaleString('ru-RU') : undefined}>{ago(s.lastActivityAt, report.today)}</td>
          <td>{s.period.activeDays}</td>
          <td title={`с первой попытки ${s.period.firstTry} · отправок ${s.period.submissions}`}>{s.period.solved}</td>
          <td>{integer.format(lastOf(s.series.xp))}</td>
          <td className="text"><span className="flag-chips">{chipFlags(s).map(([flag, title, hint]) => <span key={flag} className={`flag-chip ${flag.toLowerCase()}`} title={hint}>{title}</span>)}</span></td>
        </tr>
      })}</tbody>
    </table></div>}
    {!sessionDate && <p className="muted small table-note">Дата сессии не задана — статус, нужный темп и сравнение с ним не считаются.</p>}
  </div>
}

/** One student: key numbers, their growth against the group median, and the session forecast. */
function StudentPanel({ student, ctx, diagnostic, onClose, onOpenStudent }: { student: ProgressStudent; ctx: Context; diagnostic: boolean; onClose: () => void; onOpenStudent?: (id: Id) => void }) {
  const [metric, setMetric] = useState<Metric>('skills')
  const heading = useRef<HTMLHeadingElement>(null)
  const panel = useRef<HTMLElement>(null)
  useEffect(() => { heading.current?.focus({ preventScroll: true }); panel.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }) }, [])
  const { report } = ctx
  const view: View = { metric, scale: 'level', axis: 'dates', diagnostic }
  const format = valueFormat(view)
  const groupmates = report.students.filter(s => s.member && (s.group || null) === (student.group || null))
  const series: ChartSeries[] = []
  if (groupmates.length > 1) series.push({ id: 'median', label: `медиана ${student.group ?? 'без группы'}`, points: medianLine(groupmates.map(s => studentLine(s, ctx, view)), format), color: 'var(--ink-2)', width: 1.75, dash: 'dashed', sticky: true })
  series.push({ id: 'student', label: student.displayName, points: studentLine(student, ctx, view), color: 'var(--brand)', width: 2.75, sticky: true, dot: true })
  const f = student.forecast
  return <section ref={panel} className="card student-panel enter" aria-labelledby="student-panel-title">
    <div className="detail-head">
      <span className="avatar big" aria-hidden="true">{initials(student.displayName)}</span>
      <div><h2 className="title" id="student-panel-title" ref={heading} tabIndex={-1}>{student.displayName}</h2>
        <p className="muted small">{student.login}{student.group && <span className="group-tag">{student.group}</span>}{!student.member && <span className="outsider-tag">{outsiderLabel(student)}</span>}</p></div>
      <div className="panel-actions">
        {onOpenStudent && <button type="button" className="ghost small-button" onClick={() => onOpenStudent(student.id)}><Icon name="user" size={15} /> Карточка студента</button>}
        <button type="button" className="icon-button" aria-label="Закрыть" title="Закрыть" onClick={onClose}><Icon name="x" /></button>
      </div>
    </div>
    <div className="panel-facts">
      <span className="mini-stats-cell"><b>{student.lessons}</b><small>{plural(student.lessons, 'урок', 'урока', 'уроков')}{student.firstLessonDay ? ` · с ${shortDay(dayNumber(student.firstLessonDay))}` : ''}</small></span>
      {f && <span className="mini-stats-cell" title={`практикой ${f.closedByPractice}, диагностикой ${f.closedByDiagnostic}`}><b>{f.closed}/{f.total}</b><small>пройдено тем · диагностикой {f.closedByDiagnostic}</small></span>}
      {f && <span className="mini-stats-cell"><b>{decimal(f.pace)}</b><small>тем в неделю{f.neededPace !== null ? ` · нужно ${decimal(f.neededPace)}` : ''}</small></span>}
      <span className="mini-stats-cell" title={`с первой попытки ${student.period.firstTry} · отправок ${student.period.submissions}`}><b>{student.period.solved}</b><small>решено за период · дней {student.period.activeDays}</small></span>
    </div>
    {(f || chipFlags(student).length > 0) && <p className="panel-status">
      {f && <StatusChip status={f.status} />}
      {f && (f.forecastDate ? <span>Прогноз: курс закрыт {shortDay(dayNumber(f.forecastDate))}</span> : f.remaining > 0 ? <span className="muted">При нулевом темпе курс не будет закрыт</span> : null)}
      {chipFlags(student).map(([flag, title, hint]) => <span key={flag} className={`flag-chip ${flag.toLowerCase()}`} title={hint}>{title}</span>)}
    </p>}
    <div className="panel-charts">
      <div>
        <div className="chart-head"><h3 className="card-title">Рост</h3><Segment label="Показатель" value={metric} options={METRICS} onChange={setMetric} /></div>
        <LineChart series={series} label={`Рост: ${student.displayName}`} tooltipAll formatX={shortDay} formatY={format} formatTick={tickFormat(view)} integer={metric !== 'skills'} height={220} />
        <div className="legend chart-legend"><span><LineKey color="var(--brand)" bold />{student.displayName}</span>{groupmates.length > 1 && <span><LineKey color="var(--ink-2)" dash="dashed" />медиана группы</span>}</div>
      </div>
      {f && (report.session.date || f.pace > 0) && f.remaining > 0 && <div>
        <div className="chart-head"><h3 className="card-title">К сессии</h3>{report.session.date && <span className="muted small">{sessionText(report.session.date, report.today)}</span>}</div>
        <SessionChart plan={{ today: report.today, sessionDate: report.session.date, total: f.total, closed: f.closed, pace: f.pace, history: { days: report.days, values: student.series.closed } }} height={220} label={`Прогноз до сессии: ${student.displayName}`} />
        <p className="muted small">{topics(f.remaining)} осталось · темп {decimal(f.pace)} в неделю{f.neededPace !== null ? `, нужно ${decimal(f.neededPace)}` : ''}</p>
      </div>}
    </div>
  </section>
}
