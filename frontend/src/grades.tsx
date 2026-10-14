import { FormEvent, ReactNode, useEffect, useRef, useState } from 'react'
import { api, post, patch, remove } from './api'
import { Icon, useToast } from './fx'
import { parseDate } from './game'
import { NO_GROUP, useGroupFilter } from './groups'
import { dayNumber, dayString, plural, shortDay } from './session'
import type { CourseLanguage, Id, Pair, PairGrade, PairJournal, PairResult, StudentGrade } from './types'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>
type Edit = { grade: PairGrade; comment: string }

const COURSES: [CourseLanguage, string][] = [['JAVA', 'Java'], ['PYTHON', 'Python']]
const courseTitle = (language: CourseLanguage) => COURSES.find(c => c[0] === language)?.[1] ?? language
const GRADES: PairGrade[] = ['н', '2', '3', '4', '5']
/** Best first, the way the counts read in the header. */
const COUNT_ORDER: PairGrade[] = ['5', '4', '3', '2', 'н']
const TEACHER_ONLY = 'только для преподавателя — студенты этого не видят'
const points = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 2 })
const average = new Intl.NumberFormat('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

// ───────── Moscow time: UTC+3 all year (no daylight saving since 2014) ─────────
const MSK_MS = 3 * 3_600_000
const STEP_MS = 5 * 60_000
/** Moscow date «YYYY-MM-DD» and time «HH:MM» of an instant. */
function moscow(value: string | number) {
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
const sameEdit = (row: PairResult, edit?: Edit) => !edit || (edit.grade === row.autoGrade && !edit.comment.trim())

function GradeChip({ grade, manual, small }: { grade: PairGrade | null; manual?: boolean; small?: boolean }) {
  if (!grade) return <span className="muted">—</span>
  return <span className={`grade-chip g${grade === 'н' ? 'n' : grade} ${small ? 'small' : ''}`} title={manual ? 'Выставлено вручную' : undefined}>{grade}{manual && <i aria-label="вручную">*</i>}</span>
}

function Segment<T extends string>({ label, value, options, onChange, disabled }: { label: string; value: T | null; options: [T, string][]; onChange: (value: T) => void; disabled?: boolean }) {
  return <div className="period" role="group" aria-label={label}>
    {options.map(([key, title]) => <button key={key} type="button" disabled={disabled} className={key === value ? 'active' : ''} aria-pressed={key === value} onClick={() => key !== value && onChange(key)}>{title}</button>)}
  </div>
}

/** The course most members of the group study; null when it cannot be learnt (the caller keeps its choice). */
const groupCourse = (group: string) => api<{ language: CourseLanguage }>(`/admin/pairs/course?group=${encodeURIComponent(group)}`).then(v => v.language, () => null)

/** Teacher: grades for a pair (class period) from the tasks solved in its window, saved pairs and the group's journal. */
export function PairGrades({ request, groups }: { request: Request; groups: string[] | null }) {
  const [stored, setGroup] = useGroupFilter('rmzn-grades-group', groups)
  const group = groups && stored && stored !== NO_GROUP && groups.includes(stored) ? stored : groups?.[0] ?? ''
  /** The course chosen for the group: pre-selected from the backend, then the teacher's choice. */
  const [course, setCourse] = useState<{ group: string; language: CourseLanguage } | null>(null)
  const language = course && course.group === group ? course.language : null
  const [form, setForm] = useState<{ date: string; start: string; end: string; group: string; language: CourseLanguage } | null>(null)
  const [preview, setPreview] = useState<Pair | null>(null)
  const [edits, setEdits] = useState<Map<Id, Edit>>(() => new Map())
  const [open, setOpen] = useState<Pair | null>(null)
  const [busy, setBusy] = useState<string | null>(null)
  const [list, setList] = useState<Pair[] | null>(null)
  const [journal, setJournal] = useState<PairJournal | null>(null)
  const [reload, setReload] = useState(0)
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
    if (value) { setPreview(value); setEdits(new Map()); setOpen(null) }
  }
  async function save() {
    if (!body || !preview?.rows) return
    const grades = preview.rows.filter(r => !sameEdit(r, edits.get(r.userId)))
      .map(r => { const edit = edits.get(r.userId)!; return { userId: r.userId, grade: edit.grade, comment: edit.comment.trim() || null } })
    setBusy('save')
    const saved = await request(() => post<Pair>('/admin/pairs', { ...body, grades }))
    setBusy(null)
    if (!saved) return
    toast({ tone: 'info', icon: 'award', title: 'Оценки сохранены', text: `${saved.group} · ${windowText(saved)} · пока скрыты от студентов` })
    setPreview(null); setForm(null); setOpen(saved)
    setGroup(saved.group); setCourse({ group: saved.group, language: saved.language }); setReload(n => n + 1)
  }
  async function openPair(id: Id) {
    setPreview(null)
    if (open?.id === id) return
    const value = await request(() => api<Pair>(`/admin/pairs/${id}`))
    if (value) setOpen(value)
  }
  /** Runs an action on the open pair; the returned pair replaces it and the list and journal reload. */
  async function act(key: string, action: () => Promise<Pair>, done?: (pair: Pair) => void) {
    setBusy(key)
    const value = await request(action)
    setBusy(null)
    if (!value) return
    setOpen(value); setReload(n => n + 1); done?.(value)
  }
  async function setGrade(row: PairResult, grade: PairGrade, comment: string) {
    if (!open?.id) return
    const id = open.id
    await act(`row-${row.userId}`, () => patch<Pair>(`/admin/pairs/${id}/grades/${row.userId}`, { grade, comment: comment.trim() || null }))
  }
  async function deletePair(pair: Pair) {
    setBusy('delete')
    const value = await request(() => remove<{ deleted: boolean }>(`/admin/pairs/${pair.id}`))
    setBusy(null)
    if (!value) return
    setOpen(null); setReload(n => n + 1)
    toast({ tone: 'info', icon: 'x', title: 'Пара удалена', text: `${pair.group} · ${windowText(pair)}` })
  }

  if (groups && !groups.length) return <section className="analytics grades-admin">
    <p className="eyebrow">Преподаватель</p><h1 className="display small">Оценки за пары</h1>
    <div className="card empty-task"><span className="empty-icon"><Icon name="user" size={26} /></span><p className="muted">Оценки ставятся группе. Сначала укажи группы студентам во вкладке «Студенты».</p></div>
  </section>

  return <section className="analytics grades-admin">
    <div className="analytics-head enter">
      <div>
        <p className="eyebrow">Преподаватель</p>
        <h1 className="display small">Оценки за пары</h1>
        <p className="muted small">Оценка считается по задачам, решённым за время пары, относительно медианы курса.</p>
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
        <button type="button" className="primary" disabled={!group || !!form} onClick={startForm}><Icon name="award" size={16} /> Высчитать оценки за пару</button>
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
      {preview && <PairCard pair={preview} edits={edits} onEdit={(row, grade, comment) => setEdits(m => new Map(m).set(row.userId, { grade, comment }))}
        actions={<>
          <button type="button" className="primary" disabled={busy === 'save'} onClick={save}>{busy === 'save' ? <><span className="spinner" aria-hidden="true" /> Сохраняем…</> : 'Сохранить'}</button>
          <button type="button" className="ghost" onClick={() => setPreview(null)}>Отмена</button>
        </>} />}
      {!preview && open && <PairCard key={open.id} pair={open} busyRow={busy?.startsWith('row-') ? Number(busy.slice(4)) : null} onEdit={setGrade} onClose={() => setOpen(null)}
        actions={<SavedActions pair={open} busy={busy}
          onPublish={() => act('publish', () => post<Pair>(`/admin/pairs/${open.id}/publish`, { published: !open.published }),
            p => toast({ tone: 'info', icon: p.published ? 'check' : 'lock', title: p.published ? 'Оценки показаны студентам' : 'Оценки скрыты от студентов', text: `${p.group} · ${windowText(p)}` }))}
          onRecalculate={() => act('recalculate', () => post<Pair>(`/admin/pairs/${open.id}/recalculate`),
            () => toast({ tone: 'info', icon: 'refresh', title: 'Пара пересчитана', text: 'Оценки, выставленные вручную, не изменились' }))}
          onDelete={() => deletePair(open)} />} />}
    </div>

    <div className="grades-lists">
      <div className="card">
        <h2 className="card-title">Пары группы{group && <span className="muted small">{group}{language ? ` · ${courseTitle(language)}` : ''}</span>}</h2>
        {!list ? <p className="muted">Загружаем…</p> : !list.length ? <p className="muted">Сохранённых пар пока нет. Нажми «Высчитать оценки за пару» после занятия.</p>
          : <div className="table-scroll"><table className="data-table pair-list">
            <thead><tr><th className="text">Дата</th><th className="text">Время, МСК</th><th>Оценки</th><th className="text">Студентам</th></tr></thead>
            <tbody>{list.map(p => {
              const from = moscow(p.startsAt), to = moscow(p.endsAt)
              return <tr key={p.id} className={open?.id === p.id ? 'selected' : ''} onClick={() => p.id !== null && openPair(p.id)}>
                <td className="text"><button type="button" className="row-link" onClick={e => { e.stopPropagation(); if (p.id !== null) openPair(p.id) }}>{shortDay(dayNumber(from.date))}</button></td>
                <td className="text">{from.time}–{to.time}</td>
                <td><GradeCounts counts={p.counts} /></td>
                <td className="text"><PublishedTag published={p.published} /></td>
              </tr>
            })}</tbody>
          </table></div>}
      </div>
      <Journal journal={journal} openId={open?.id ?? null} onOpen={openPair} />
    </div>
  </section>
}

function PublishedTag({ published }: { published: boolean }) {
  return <span className={`pub-tag ${published ? 'on' : ''}`}>{published ? 'опубликовано' : 'скрыто'}</span>
}

function GradeCounts({ counts }: { counts: Pair['counts'] }) {
  return <span className="grade-counts">{COUNT_ORDER.map(g => <span key={g} className={(counts[g] ?? 0) ? '' : 'zero'}><GradeChip grade={g} small /><b className="tabular">{counts[g] ?? 0}</b></span>)}</span>
}

function SavedActions({ pair, busy, onPublish, onRecalculate, onDelete }: { pair: Pair; busy: string | null; onPublish: () => void; onRecalculate: () => void; onDelete: () => void }) {
  const [confirming, setConfirming] = useState(false)
  if (confirming) return <div className="danger-zone open pair-delete">
    <b>Удалить пару {windowText(pair)}?</b>
    <p className="muted small">Оценки этой пары, в том числе выставленные вручную, будут удалены{pair.published ? ' и пропадут у студентов' : ''}. Восстановить их нельзя.</p>
    <div className="password-row">
      <button type="button" className="danger-solid" disabled={busy === 'delete'} onClick={onDelete}>{busy === 'delete' ? <><span className="spinner" aria-hidden="true" /> Удаляем…</> : 'Удалить навсегда'}</button>
      <button type="button" className="ghost" onClick={() => setConfirming(false)}>Отмена</button>
    </div>
  </div>
  return <>
    <button type="button" className={pair.published ? 'ghost' : 'primary'} disabled={!!busy} onClick={onPublish}>
      {busy === 'publish' ? <span className="spinner" aria-hidden="true" /> : <Icon name={pair.published ? 'lock' : 'check'} size={16} />}{pair.published ? 'Скрыть от студентов' : 'Показать студентам'}</button>
    <button type="button" className="ghost" disabled={!!busy} onClick={onRecalculate} title="Заново посчитать баллы, посещение и медиану (например, после отзыва зачёта). Оценки, выставленные вручную, останутся.">
      {busy === 'recalculate' ? <span className="spinner" aria-hidden="true" /> : <Icon name="refresh" size={16} />}Пересчитать</button>
    <button type="button" className="ghost danger" disabled={!!busy} onClick={() => setConfirming(true)}><Icon name="x" size={16} />Удалить</button>
  </>
}

/** The header of a pair (window, median, thresholds, counts) and its table. edits — the preview's unsaved changes; without them the rows are the saved state. */
function PairCard({ pair, edits, busyRow = null, onEdit, onClose, actions }: {
  pair: Pair; edits?: Map<Id, Edit>; busyRow?: Id | null; onEdit: (row: PairResult, grade: PairGrade, comment: string) => void; onClose?: () => void; actions: ReactNode
}) {
  const saved = pair.id !== null
  const rows = pair.rows ?? []
  const t = pair.thresholds
  const counts = edits ? rows.reduce((c, r) => { const g = edits.get(r.userId)?.grade ?? r.grade; c[g] = (c[g] ?? 0) + 1; return c }, { 'н': 0, '2': 0, '3': 0, '4': 0, '5': 0 } as Pair['counts']) : pair.counts
  return <section className="card pair-card enter" aria-label={`Пара ${windowText(pair)}`}>
    <div className="chart-head">
      <div>
        <p className="eyebrow">{saved ? 'Сохранённая пара' : 'Предварительный расчёт · не сохранено'}</p>
        <h2 className="title">{windowText(pair)} <span className="muted small">МСК</span></h2>
        <p className="muted small">{pair.group} · {courseTitle(pair.language)}{saved && <> · <PublishedTag published={pair.published} /></>}</p>
      </div>
      {onClose && <button type="button" className="icon-button" aria-label="Закрыть" title="Закрыть" onClick={onClose}><Icon name="x" /></button>}
    </div>
    <div className="panel-facts">
      <span className="mini-stats-cell teacher-only" title={TEACHER_ONLY}>
        <b className="tabular">{pair.median !== null ? `${points.format(pair.median)} ${plural(Math.round(pair.median), 'балл', 'балла', 'баллов')}` : '—'}</b>
        <small>{medianSource(pair)}</small>
      </span>
      <span className="mini-stats-cell teacher-only" title={TEACHER_ONLY}>
        {t ? <><b className="tabular thresholds">5 от {points.format(t.five)} · 4 от {points.format(t.four)} · 3 от {points.format(t.three)}</b><small>баллов · 135% / 100% / 60% медианы</small></>
          : <><b>Без медианы</b><small>был на паре и решил хоть одну задачу — 4, ничего — 2</small></>}
      </span>
      <span className="mini-stats-cell"><GradeCounts counts={counts} /><small>{rows.length} {plural(rows.length, 'студент', 'студента', 'студентов')}</small></span>
    </div>
    <p className="teacher-note"><Icon name="lock" size={14} />Медиана, баллы, задачи и % медианы — {TEACHER_ONLY}. Студенту показывается только оценка{saved ? ', и только после публикации' : ''}.</p>
    {!rows.length ? <p className="muted">В группе нет участников сессии — оценивать некого.</p>
      : <div className="table-scroll"><table className="data-table pair-table">
        <thead>
          <tr><th className="text" rowSpan={2}>Студент</th><th rowSpan={2}>Был на паре</th><th colSpan={4} className="group-head" title="Задачи, впервые решённые за время пары, по сложности">Задачи</th>
            <th rowSpan={2} title="Сумма сложностей; задача hard mode — ×10">Баллы</th><th rowSpan={2} title={`Баллы от медианы — ${TEACHER_ONLY}`}>% медианы</th><th className="text" rowSpan={2}>Оценка</th></tr>
          <tr><th>1</th><th>2</th><th>3</th><th title="Задачи hard mode">hard</th></tr>
        </thead>
        <tbody>{rows.map(row => <ResultRow key={`${row.userId}|${row.grade}|${row.comment ?? ''}`} row={row} edit={edits?.get(row.userId)} saved={saved} busy={busyRow === row.userId} onEdit={onEdit} />)}</tbody>
      </table></div>}
    <div className="pair-actions">{actions}</div>
  </section>
}

/** In a preview the grade and comment are local edits; in a saved pair the grade saves at once, the comment when the field is left. */
function ResultRow({ row, edit, saved, busy, onEdit }: { row: PairResult; edit?: Edit; saved: boolean; busy: boolean; onEdit: (row: PairResult, grade: PairGrade, comment: string) => void }) {
  const grade = edit?.grade ?? row.grade
  const comment = edit?.comment ?? row.comment ?? ''
  const [draft, setDraft] = useState(comment)
  const manual = saved ? row.manual : grade !== row.autoGrade || !!comment.trim()
  const showComment = grade !== row.autoGrade || (saved && !!row.comment)
  const commit = () => { if (saved && draft.trim() !== (row.comment ?? '').trim()) onEdit(row, grade, draft) }
  return <tr className={row.attended ? '' : 'absent'}>
    <td className="text"><b>{row.displayName}</b> <small className="muted">{row.login}</small>
      {row.hard && <span className="pill hard" title="Hard mode: оценивается как все, но в медиану не входит"><Icon name="flame" size={11} /> HARD</span>}</td>
    <td>{row.attended ? <span className="attended"><Icon name="check" size={15} /><span className="sr-only">да</span></span> : <span className="muted">нет</span>}</td>
    <td>{row.tasks['1'] || '·'}</td><td>{row.tasks['2'] || '·'}</td><td>{row.tasks['3'] || '·'}</td><td>{row.tasks.hard || '·'}</td>
    <td><b>{row.points}</b></td>
    <td>{row.percent !== null ? `${row.percent}%` : '—'}</td>
    <td className="text grade-cell">
      <div className="grade-line">
        <select aria-label={`Оценка: ${row.displayName}`} className={`grade-select g${grade === 'н' ? 'n' : grade}`} value={grade} disabled={busy}
          onChange={e => { const g = e.target.value as PairGrade; const c = g === row.autoGrade && !saved ? '' : draft; setDraft(c); onEdit(row, g, c) }}>
          {GRADES.map(g => <option key={g} value={g}>{g}</option>)}
        </select>
        {busy && <span className="spinner" aria-hidden="true" />}
        {manual && <span className="manual-tag" title={`Рассчитано: ${row.autoGrade}`}>вручную · было {row.autoGrade}</span>}
      </div>
      {showComment && <input className="grade-comment" placeholder="Комментарий" aria-label={`Комментарий к оценке: ${row.displayName}`} maxLength={500} value={draft} disabled={busy}
        onChange={e => { setDraft(e.target.value); if (!saved) onEdit(row, grade, e.target.value) }} onBlur={commit}
        onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); commit() } }} />}
    </td>
  </tr>
}

function Journal({ journal, openId, onOpen }: { journal: PairJournal | null; openId: Id | null; onOpen: (id: Id) => void }) {
  return <div className="card">
    <h2 className="card-title">Журнал{journal && <span className="muted small">{journal.group} · {courseTitle(journal.language)}</span>}</h2>
    {!journal ? <p className="muted">Загружаем…</p> : !journal.pairs.length ? <p className="muted">Журнал появится после первой сохранённой пары.</p>
      : <div className="table-scroll"><table className="data-table journal-table">
        <thead><tr><th className="text">Студент</th>
          {journal.pairs.map(p => { const from = moscow(p.startsAt); return <th key={p.id} className={openId === p.id ? 'selected' : ''}>
            <button type="button" className="journal-pair" onClick={() => onOpen(p.id)} title={`Открыть пару ${windowText(p)}${p.published ? '' : ' · скрыта от студентов'}`}>
              <span>{shortDay(dayNumber(from.date))}</span><small>{from.time}</small>{!p.published && <small className="hidden-mark">скрыто</small>}</button></th> })}
          <th title="Средняя по оценкам 2–5; «н» не считается">Средняя</th><th title="Сколько раз «н»">Пропуски</th></tr></thead>
        <tbody>{journal.students.map(s => <tr key={s.userId}>
          <td className="text"><b>{s.displayName}</b> <small className="muted">{s.login}</small></td>
          {s.grades.map((g, i) => <td key={journal.pairs[i]?.id ?? i} className={openId === journal.pairs[i]?.id ? 'selected' : ''}><GradeChip grade={g} manual={s.manual[i]} small /></td>)}
          <td><b>{s.average !== null ? average.format(s.average) : '—'}</b></td>
          <td>{s.absences || <span className="muted">0</span>}</td>
        </tr>)}</tbody>
      </table></div>}
    {journal && journal.pairs.length > 0 && <p className="muted small table-note">* — оценка выставлена вручную. Нажми на дату, чтобы открыть пару.</p>}
  </div>
}

/** «Мой прогресс»: the student's own grades of published pairs — the date and the grade only. Hidden while there are none. */
export function StudentPairGrades({ language }: { language: CourseLanguage }) {
  const [grades, setGrades] = useState<StudentGrade[]>([])
  useEffect(() => {
    let alive = true
    setGrades([])
    api<{ grades: StudentGrade[] }>(`/grades?language=${language}`).then(v => { if (alive) setGrades(v.grades) }, () => {})
    return () => { alive = false }
  }, [language])
  if (!grades.length) return null
  return <section className="card student-grades enter" aria-label="Оценки за пары">
    <h2 className="card-title"><span className="chip-icon"><Icon name="award" size={16} /></span> Оценки за пары</h2>
    <ul>{grades.map((g, i) => <li key={`${g.date}-${i}`}><span className="muted">{shortDay(dayNumber(g.date))}</span><GradeChip grade={g.grade} /></li>)}</ul>
  </section>
}
