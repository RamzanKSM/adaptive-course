import { FormEvent, ReactNode, useEffect, useRef, useState } from 'react'
import { api, post, remove } from './api'
import { Icon, useToast } from './fx'
import { parseDate } from './game'
import { NO_GROUP, useGroupFilter } from './groups'
import { dayNumber, dayString, plural, shortDay } from './session'
import type { CourseLanguage, Id, Pair, PairCell, PairJournal, PairResult } from './types'
import { WheelPanel } from './wheel'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>

const COURSES: [CourseLanguage, string][] = [['JAVA', 'Java'], ['PYTHON', 'Python']]
const courseTitle = (language: CourseLanguage) => COURSES.find(c => c[0] === language)?.[1] ?? language
const TEACHER_ONLY = 'только для преподавателя — студенты этого не видят'
const points = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 2 })

// ───────── Moscow time: UTC+3 all year (no daylight saving since 2014) ─────────
const MSK_MS = 3 * 3_600_000
const STEP_MS = 5 * 60_000
/** Moscow date «YYYY-MM-DD» and time «HH:MM» of an instant. */
export function moscow(value: string | number) {
  const time = typeof value === 'number' ? value : parseDate(value).getTime()
  if (Number.isNaN(time)) return { date: String(value).slice(0, 10), time: '—' }
  const iso = new Date(time + MSK_MS).toISOString()
  return { date: iso.slice(0, 10), time: iso.slice(11, 16) }
}
const instant = (date: string, time: string) => `${date}T${time}:00+03:00`
/** The last 90 minutes ending now, rounded to 5 minutes; a window crossing midnight starts at 00:00. */
function defaultWindow() {
  const end = Math.round(Date.now() / STEP_MS) * STEP_MS
  const to = moscow(end), from = moscow(end - 90 * 60_000)
  return { date: to.date, start: from.date === to.date ? from.time : '00:00', end: to.time }
}
const minutes = (time: string) => { const [h, m] = time.split(':').map(Number); return h * 60 + m }
/** «14 окт · 11:00–12:30». */
function windowText(pair: { startsAt: string; endsAt: string }) {
  const from = moscow(pair.startsAt), to = moscow(pair.endsAt)
  return `${shortDay(dayNumber(from.date))} · ${from.time}–${to.time}${to.date !== from.date ? ` (${shortDay(dayNumber(to.date))})` : ''}`
}
/** The Monday of the week before the given Moscow day. */
function previousMonday(day: string) {
  const n = dayNumber(day)
  return dayString(n - ((new Date(n * 86_400_000).getUTCDay() + 6) % 7) - 7)
}
function medianSource(pair: Pair) {
  if (pair.median === null || pair.medianSource === 'NONE') return 'нет медианы'
  if (pair.medianSource === 'PAIR') return 'медиана этой пары'
  if (!pair.medianWeek) return 'медиана прошлых недель'
  const since = `с ${shortDay(dayNumber(pair.medianWeek))}`
  return pair.medianWeek === previousMonday(moscow(pair.startsAt).date) ? `медиана прошлой недели (${since})` : `медиана недели ${since} — последней с достаточными данными`
}

function Segment<T extends string>({ label, value, options, onChange, disabled }: { label: string; value: T | null; options: [T, string][]; onChange: (value: T) => void; disabled?: boolean }) {
  return <div className="period" role="group" aria-label={label}>
    {options.map(([key, title]) => <button key={key} type="button" disabled={disabled} className={key === value ? 'active' : ''} aria-pressed={key === value} onClick={() => key !== value && onChange(key)}>{title}</button>)}
  </div>
}

/** The course most members of the group study; null when it cannot be learnt (the caller keeps its choice). */
export const groupCourse = (group: string) => api<{ language: CourseLanguage }>(`/admin/pairs/course?group=${encodeURIComponent(group)}`).then(v => v.language, () => null)

/** Teacher: how the group worked during a pair (class period) — attendance, tasks, pace, activity; saved pairs and the journal. */
export function PairWork({ request, groups }: { request: Request; groups: string[] | null }) {
  const [stored, setGroup] = useGroupFilter('rmzn-pairs-group', groups)
  const group = groups && stored && stored !== NO_GROUP && groups.includes(stored) ? stored : groups?.[0] ?? ''
  /** The course chosen for the group: pre-selected from the backend, then the teacher's choice. */
  const [course, setCourse] = useState<{ group: string; language: CourseLanguage } | null>(null)
  const language = course && course.group === group ? course.language : null
  const [form, setForm] = useState<{ date: string; start: string; end: string; group: string; language: CourseLanguage } | null>(null)
  const [preview, setPreview] = useState<Pair | null>(null)
  const [open, setOpen] = useState<Pair | null>(null)
  const [busy, setBusy] = useState<string | null>(null)
  const [list, setList] = useState<Pair[] | null>(null)
  const [journal, setJournal] = useState<PairJournal | null>(null)
  const [reload, setReload] = useState(0)
  /** The wheel of fortune of the open pair. */
  const [wheel, setWheel] = useState(false)
  const toast = useToast()
  const pairRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!group || course?.group === group) return
    let alive = true
    groupCourse(group).then(found => { if (alive) setCourse({ group, language: found ?? 'JAVA' }) })
    return () => { alive = false }
  }, [group, course?.group])

  useEffect(() => {
    if (!group || !language) return
    let alive = true
    const query = `group=${encodeURIComponent(group)}&language=${language}`
    request(() => api<{ pairs: Pair[] }>(`/admin/pairs?${query}`)).then(v => { if (alive && v) setList(v.pairs) })
    request(() => api<PairJournal>(`/admin/pairs/journal?${query}`)).then(v => { if (alive && v) setJournal(v) })
    return () => { alive = false }
  }, [group, language, reload, request])

  const shown = preview ?? open
  useEffect(() => setWheel(false), [open?.id, preview])
  useEffect(() => { if (shown) pairRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }) }, [shown?.id, preview]) // eslint-disable-line react-hooks/exhaustive-deps

  function chooseGroup(value: string) { if (value === group) return; setGroup(value); setOpen(null); setList(null); setJournal(null) }
  function chooseCourse(value: CourseLanguage) { setCourse({ group, language: value }); setOpen(null); setList(null); setJournal(null) }
  function startForm() { setForm({ ...defaultWindow(), group, language: language ?? 'JAVA' }); setOpen(null) }
  function formGroup(value: string) {
    setForm(f => f && { ...f, group: value })
    groupCourse(value).then(found => { if (found) setForm(f => f && f.group === value ? { ...f, language: found } : f) })
  }

  const formError = !form ? '' : !form.date || !form.start || !form.end ? 'Укажи дату, начало и конец пары'
    : minutes(form.end) <= minutes(form.start) ? 'Конец пары должен быть позже начала'
      : minutes(form.end) - minutes(form.start) > 360 ? 'Пара не может быть длиннее 6 часов' : !form.group ? 'Выбери группу' : ''
  const body = form && { group: form.group, language: form.language, startsAt: instant(form.date, form.start), endsAt: instant(form.date, form.end) }

  async function calculate(e: FormEvent) {
    e.preventDefault()
    if (!body || formError) return
    setBusy('preview')
    const value = await request(() => post<Pair>('/admin/pairs/preview', body))
    setBusy(null)
    if (value) { setPreview(value); setOpen(null) }
  }
  async function save() {
    if (!body || !preview?.rows) return
    setBusy('save')
    const saved = await request(() => post<Pair>('/admin/pairs', body))
    setBusy(null)
    if (!saved) return
    toast({ tone: 'info', icon: 'check', title: 'Пара сохранена', text: `${saved.group} · ${windowText(saved)}` })
    setPreview(null); setForm(null); setOpen(saved)
    setGroup(saved.group); setCourse({ group: saved.group, language: saved.language }); setReload(n => n + 1)
  }
  async function openPair(id: Id) {
    setPreview(null)
    if (open?.id === id) return
    const value = await request(() => api<Pair>(`/admin/pairs/${id}`))
    if (value) setOpen(value)
  }
  async function recalculate(pair: Pair) {
    setBusy('recalculate')
    const value = await request(() => post<Pair>(`/admin/pairs/${pair.id}/recalculate`))
    setBusy(null)
    if (!value) return
    setOpen(value); setReload(n => n + 1)
    toast({ tone: 'info', icon: 'refresh', title: 'Пара пересчитана', text: `${value.group} · ${windowText(value)}` })
  }
  async function deletePair(pair: Pair) {
    setBusy('delete')
    const value = await request(() => remove<{ deleted: boolean }>(`/admin/pairs/${pair.id}`))
    setBusy(null)
    if (!value) return
    setOpen(null); setReload(n => n + 1)
    toast({ tone: 'info', icon: 'x', title: 'Пара удалена', text: `${pair.group} · ${windowText(pair)}` })
  }

  if (groups && !groups.length) return <section className="analytics pairs-admin">
    <p className="eyebrow">Преподаватель</p><h1 className="display small">Работа на паре</h1>
    <div className="card empty-task"><span className="empty-icon"><Icon name="user" size={26} /></span><p className="muted">Пара считается для группы. Сначала укажи группы студентам во вкладке «Студенты».</p></div>
  </section>

  return <section className="analytics pairs-admin">
    <div className="analytics-head enter">
      <div>
        <p className="eyebrow">Преподаватель</p>
        <h1 className="display small">Работа на паре</h1>
        <p className="muted small">Как группа работала за время пары: посещение, задачи, темп относительно группы, активность. Видишь только ты.</p>
      </div>
      <Segment label="Курс" value={language} options={COURSES} onChange={chooseCourse} disabled={!language} />
    </div>

    <div className="card progress-controls enter">
      <div className="control-row">
        <span className="control-label">Группа</span>
        {!groups ? <span className="muted small">Загружаем…</span>
          : <div className="topic-filters group-filters" role="group" aria-label="Группа">{groups.map(g =>
            <button key={g} type="button" className={g === group ? 'active' : ''} aria-pressed={g === group} onClick={() => chooseGroup(g)}>{g}</button>)}</div>}
      </div>
      <div className="control-row">
        <button type="button" className="primary" disabled={!group || !!form} onClick={startForm}><Icon name="chart" size={16} /> Посчитать пару</button>
      </div>
    </div>

    {form && <form className="card pair-form enter" onSubmit={calculate}>
      <div className="chart-head"><h2 className="card-title">Новая пара</h2>
        <button type="button" className="icon-button" aria-label="Закрыть" title="Закрыть" onClick={() => { setForm(null); setPreview(null) }}><Icon name="x" /></button></div>
      <div className="pair-form-grid">
        <label>Дата<input type="date" value={form.date} onChange={e => setForm({ ...form, date: e.target.value })} required /></label>
        <label>Начало, МСК<input type="time" step={300} value={form.start} onChange={e => setForm({ ...form, start: e.target.value })} required /></label>
        <label>Конец, МСК<input type="time" step={300} value={form.end} onChange={e => setForm({ ...form, end: e.target.value })} required /></label>
        <label>Группа<select value={form.group} onChange={e => formGroup(e.target.value)}>{(groups ?? []).map(g => <option key={g} value={g}>{g}</option>)}</select></label>
        <div className="pair-form-course"><span>Курс</span><Segment label="Курс пары" value={form.language} options={COURSES} onChange={value => setForm({ ...form, language: value })} /></div>
      </div>
      <div className="pair-form-actions">
        <button className="primary" disabled={!!formError || busy === 'preview'}>{busy === 'preview' ? <><span className="spinner" aria-hidden="true" /> Считаем…</> : 'Рассчитать'}</button>
        <span className={formError ? 'form-error' : 'muted small'}>{formError || 'Время — московское. Ничего не сохраняется, пока не нажмёшь «Сохранить».'}</span>
      </div>
    </form>}

    <div ref={pairRef} className="pair-anchor">
      {preview && <PairCard pair={preview}
        actions={<>
          <button type="button" className="primary" disabled={busy === 'save'} onClick={save}>{busy === 'save' ? <><span className="spinner" aria-hidden="true" /> Сохраняем…</> : 'Сохранить'}</button>
          <button type="button" className="ghost" onClick={() => setPreview(null)}>Отмена</button>
        </>} />}
      {!preview && open && <PairCard key={open.id} pair={open} onClose={() => setOpen(null)}
        actions={<SavedActions pair={open} busy={busy} onWheel={() => setWheel(true)} onRecalculate={() => recalculate(open)} onDelete={() => deletePair(open)} />} />}
      {!preview && open && wheel && <WheelPanel key={`wheel-${open.id}`} pair={open} request={request} onClose={() => setWheel(false)} />}
    </div>

    <div className="list-stack">
      <div className="card">
        <h2 className="card-title">Пары группы{group && <span className="muted small">{group}{language ? ` · ${courseTitle(language)}` : ''}</span>}</h2>
        {!list ? <p className="muted">Загружаем…</p> : !list.length ? <p className="muted">Сохранённых пар пока нет. Нажми «Посчитать пару» после занятия.</p>
          : <div className="table-scroll"><table className="data-table pair-list">
            <thead><tr><th className="text">Дата</th><th className="text">Время, МСК</th><th title={`Медиана баллов — ${TEACHER_ONLY}`}>Медиана</th></tr></thead>
            <tbody>{list.map(p => {
              const from = moscow(p.startsAt), to = moscow(p.endsAt)
              return <tr key={p.id} className={open?.id === p.id ? 'selected' : ''} onClick={() => p.id !== null && openPair(p.id)}>
                <td className="text"><button type="button" className="row-link" onClick={e => { e.stopPropagation(); if (p.id !== null) openPair(p.id) }}>{shortDay(dayNumber(from.date))}</button></td>
                <td className="text">{from.time}–{to.time}</td>
                <td>{p.median !== null ? points.format(p.median) : '—'}</td>
              </tr>
            })}</tbody>
          </table></div>}
      </div>
      <Journal journal={journal} openId={open?.id ?? null} onOpen={openPair} />
    </div>
  </section>
}

function SavedActions({ pair, busy, onWheel, onRecalculate, onDelete }: { pair: Pair; busy: string | null; onWheel: () => void; onRecalculate: () => void; onDelete: () => void }) {
  const [confirming, setConfirming] = useState(false)
  if (confirming) return <div className="danger-zone open pair-delete">
    <b>Удалить пару {windowText(pair)}?</b>
    <p className="muted small">Сохранённые результаты этой пары будут удалены. Решения студентов останутся — пару можно посчитать заново.</p>
    <div className="password-row">
      <button type="button" className="danger-solid" disabled={busy === 'delete'} onClick={onDelete}>{busy === 'delete' ? <><span className="spinner" aria-hidden="true" /> Удаляем…</> : 'Удалить'}</button>
      <button type="button" className="ghost" onClick={() => setConfirming(false)}>Отмена</button>
    </div>
  </div>
  return <>
    <button type="button" className="primary" disabled={!!busy} onClick={onWheel} title="Шоколадка: колесо из пятёрок у доски и топ‑20% по задачам за пару"><Icon name="sparkle" size={16} />Колесо фортуны</button>
    <button type="button" className="ghost" disabled={!!busy} onClick={onRecalculate} title="Заново посчитать задачи, посещение, активность и медиану (например, после отзыва зачёта)">
      {busy === 'recalculate' ? <span className="spinner" aria-hidden="true" /> : <Icon name="refresh" size={16} />}Пересчитать</button>
    <button type="button" className="ghost danger" disabled={!!busy} onClick={() => setConfirming(true)}><Icon name="x" size={16} />Удалить</button>
  </>
}

/** The header of a pair (window, median, attendance) and its table. */
function PairCard({ pair, onClose, actions }: { pair: Pair; onClose?: () => void; actions: ReactNode }) {
  const saved = pair.id !== null
  const rows = pair.rows ?? []
  const attended = rows.filter(r => r.attended).length
  const solved = rows.reduce((sum, r) => sum + r.tasks['1'] + r.tasks['2'] + r.tasks['3'] + r.tasks.hard, 0)
  return <section className="card pair-card enter" aria-label={`Пара ${windowText(pair)}`}>
    <div className="chart-head">
      <div>
        <p className="eyebrow">{saved ? 'Сохранённая пара' : 'Предварительный расчёт · не сохранено'}</p>
        <h2 className="title">{windowText(pair)} <span className="muted small">МСК</span></h2>
        <p className="muted small">{pair.group} · {courseTitle(pair.language)}</p>
      </div>
      {onClose && <button type="button" className="icon-button" aria-label="Закрыть" title="Закрыть" onClick={onClose}><Icon name="x" /></button>}
    </div>
    <div className="panel-facts">
      <span className="mini-stats-cell"><b className="tabular">{attended} из {rows.length}</b><small>были на паре</small></span>
      <span className="mini-stats-cell"><b className="tabular">{solved}</b><small>{plural(solved, 'задача решена', 'задачи решены', 'задач решено')} за пару</small></span>
      <span className="mini-stats-cell" title="Темп относительно группы: баллы студента делятся на эту медиану">
        <b className="tabular">{pair.median !== null ? `${points.format(pair.median)} ${plural(Math.round(pair.median), 'балл', 'балла', 'баллов')}` : '—'}</b>
        <small>{medianSource(pair)}</small>
      </span>
    </div>
    <p className="teacher-note"><Icon name="lock" size={14} />Только для преподавателя — студенты этого не видят.</p>
    {!rows.length ? <p className="muted">В группе нет участников сессии.</p>
      : <div className="table-scroll"><table className="data-table pair-table">
        <thead>
          <tr><th className="text" rowSpan={2}>Студент</th><th rowSpan={2}>Был</th><th colSpan={4} className="group-head" title="Задачи, впервые решённые за время пары, по сложности">Задачи</th>
            <th rowSpan={2} title="Сумма сложностей; задача hard mode — ×10">Баллы</th><th rowSpan={2} title="Баллы от медианы — темп относительно группы">% медианы</th>
            <th rowSpan={2} title="5 минут за каждый пятиминутный отрезок пары, в котором была отправка или вопрос помощнику">Активно, мин</th>
            <th rowSpan={2} title="Отправки на проверку за пару: всего / из них не принято">Отправки</th>
            <th rowSpan={2} title="Сообщения студента учебному помощнику за пару">Вопросы</th></tr>
          <tr><th>1</th><th>2</th><th>3</th><th title="Задачи hard mode">hard</th></tr>
        </thead>
        <tbody>{rows.map(row => <tr key={row.userId} className={row.attended ? '' : 'absent'}>
          <td className="text"><b>{row.displayName}</b> <small className="muted">{row.login}</small>
            {row.hard && <span className="pill hard" title="Hard mode: в медиану не входит"><Icon name="flame" size={11} /> HARD</span>}</td>
          <td>{row.attended ? <span className="attended"><Icon name="check" size={15} /><span className="sr-only">был</span></span> : <span className="muted">не был</span>}</td>
          <td>{row.tasks['1'] || '·'}</td><td>{row.tasks['2'] || '·'}</td><td>{row.tasks['3'] || '·'}</td><td>{row.tasks.hard || '·'}</td>
          <td><b>{row.points}</b></td>
          <td>{row.percent !== null ? `${row.percent}%` : '—'}</td>
          <td>{row.activeMinutes || <span className="muted">0</span>}</td>
          <td>{row.submissions ? <>{row.submissions}<small className="muted"> / {row.failed}</small></> : <span className="muted">0</span>}</td>
          <td>{row.chatQuestions || <span className="muted">0</span>}</td>
        </tr>)}</tbody>
      </table></div>}
    <div className="pair-actions">{actions}</div>
  </section>
}

function JournalCell({ cell }: { cell: PairCell | null }) {
  if (!cell) return <span className="muted">—</span>
  if (!cell.attended) return <span className="muted" title="Не был на паре">н</span>
  return <span className="work-cell" title={`${cell.points} ${plural(cell.points, 'балл', 'балла', 'баллов')}${cell.percent !== null ? ` · ${cell.percent}% медианы` : ''} · активно ${cell.activeMinutes} мин`}>
    <b>{cell.points}</b><small>{cell.activeMinutes} мин</small></span>
}

function Journal({ journal, openId, onOpen }: { journal: PairJournal | null; openId: Id | null; onOpen: (id: Id) => void }) {
  return <div className="card">
    <h2 className="card-title">Журнал{journal && <span className="muted small">{journal.group} · {courseTitle(journal.language)}</span>}</h2>
    {!journal ? <p className="muted">Загружаем…</p> : !journal.pairs.length ? <p className="muted">Журнал появится после первой сохранённой пары.</p>
      : <div className="table-scroll"><table className="data-table journal-table">
        <thead><tr><th className="text">Студент</th>
          {journal.pairs.map(p => { const from = moscow(p.startsAt); return <th key={p.id} className={openId === p.id ? 'selected' : ''}>
            <button type="button" className="journal-pair" onClick={() => onOpen(p.id)} title={`Открыть пару ${windowText(p)}`}>
              <span>{shortDay(dayNumber(from.date))}</span><small>{from.time}</small></button></th> })}
          <th title="Сколько пар студент был на занятии">Был</th></tr></thead>
        <tbody>{journal.students.map(s => <tr key={s.userId}>
          <td className="text"><b>{s.displayName}</b> <small className="muted">{s.login}</small></td>
          {journal.pairs.map((p, i) => <td key={p.id} className={openId === p.id ? 'selected' : ''}><JournalCell cell={s.cells?.[i] ?? null} /></td>)}
          <td><b>{s.pairs}</b><small className="muted"> / {journal.pairs.length}</small></td>
        </tr>)}</tbody>
      </table></div>}
    {journal && journal.pairs.length > 0 && <p className="muted small table-note">В клетке — баллы за пару и активные минуты; «н» — не был. Нажми на дату, чтобы открыть пару.</p>}
  </div>
}
