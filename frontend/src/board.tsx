import { FormEvent, ReactNode, useCallback, useEffect, useMemo, useRef, useState } from 'react'
import CodeMirror from '@uiw/react-codemirror'
import { api, ApiError, patch, post, remove } from './api'
import { ConsolePanel } from './console'
import { EDITOR_EXTENSIONS, FALLBACK_CODE, Markdown } from './editor'
import { Icon, initials, useToast } from './fx'
import { parseDate } from './game'
import { groupCourse, moscow } from './pairs'
import { NO_GROUP, useGroupFilter } from './groups'
import { dayNumber, plural, shortDay, StatusChip } from './session'
import type {
  BoardAdminItem, BoardAdminTest, BoardAssessment, BoardCheck, BoardCurrent, BoardGrade, BoardItemKind, BoardJournal, BoardMember,
  BoardOverview, BoardRun, BoardStatus, BoardStudentGrade, BoardStudentTest, BoardTestSummary, ConsoleRun, CourseLanguage, Id,
} from './types'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>

const COURSES: [CourseLanguage, string][] = [['JAVA', 'Java'], ['PYTHON', 'Python']]
const courseTitle = (language: CourseLanguage) => COURSES.find(c => c[0] === language)?.[1] ?? language
const GRADES: BoardGrade[] = ['2', '3', '4', '5']
const STUDENT_POLL_MS = 5_000, ADMIN_POLL_MS = 2_000, AUTOSAVE_MS = 5_000, AUTOSAVE_DEBOUNCE_MS = 1_200, LOGOUT_SECONDS = 10

const ms = (value: string | null | undefined) => value ? parseDate(value).getTime() : NaN
/** «5:07», never negative. */
const clock = (left: number) => { const s = Math.max(0, Math.ceil(left / 1000)); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}` }
/** «15 окт · 11:20» in Moscow time. */
const dayTime = (value: string | null | undefined) => { if (!value) return '—'; const m = moscow(value); return `${shortDay(dayNumber(m.date))} · ${m.time}` }
const dayOnly = (value: string | null | undefined) => value ? shortDay(dayNumber(moscow(value).date)) : '—'

/** Re-renders every `step` ms and returns the client clock. */
function useNow(step = 1000) {
  const [now, setNow] = useState(Date.now)
  useEffect(() => { const timer = setInterval(() => setNow(Date.now()), step); return () => clearInterval(timer) }, [step])
  return now
}

export function GradeChip({ grade, small }: { grade: BoardGrade | string | null | undefined; small?: boolean }) {
  if (!grade) return <span className="muted">—</span>
  return <span className={`grade-chip g${grade} ${small ? 'small' : ''}`}>{grade}</span>
}

// ═════════ Student ═════════

/** Polls GET /board/current while a student is signed in. set() replaces the state at once and drops answers already on the way. */
export function useBoardCurrent(enabled: boolean) {
  const [current, setCurrent] = useState<BoardCurrent | null>(null)
  const seq = useRef(0)
  useEffect(() => {
    if (!enabled) { seq.current++; setCurrent(null); return }
    let alive = true
    const tick = () => {
      const id = ++seq.current
      api<BoardCurrent>('/board/current').then(value => { if (alive && id === seq.current) setCurrent(value) }, () => {})
    }
    tick()
    const timer = setInterval(tick, STUDENT_POLL_MS)
    return () => { alive = false; clearInterval(timer) }
  }, [enabled])
  const set = useCallback((value: BoardCurrent | null) => { seq.current++; setCurrent(value) }, [])
  return [current, set] as const
}

/** «Тебя вызвали к доске»: over any page while the call is active. */
export function BoardCallDialog({ call, onStarted }: { call: NonNullable<BoardCurrent['call']>; onStarted: (test: BoardStudentTest) => void }) {
  const now = useNow()
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const left = ms(call.expiresAt) - now
  async function start() {
    setBusy(true); setError('')
    try { onStarted(await post<BoardStudentTest>(`/board/tests/${call.id}/start`)) }
    catch (e) { setError(e instanceof Error ? e.message : 'Не удалось начать тест'); setBusy(false) }
  }
  return <div className="board-call-backdrop" role="dialog" aria-modal="true" aria-labelledby="board-call-title">
    <div className="board-call">
      <span className="board-call-icon"><Icon name="flag" size={30} /></span>
      <p className="eyebrow">Ответ у доски</p>
      <h2 id="board-call-title" className="display small">Тебя вызвали к доске</h2>
      <p>Тест на 6 минут: напиши программу по условию и определи, что выведет готовый код. Таймер запустится, когда нажмёшь «Начать тест».</p>
      {error && <p className="form-error" role="alert">{error}</p>}
      <button type="button" className="primary big" disabled={busy} onClick={start} autoFocus>{busy ? <><span className="spinner" aria-hidden="true" /> Начинаем…</> : <>Начать тест <Icon name="arrow" /></>}</button>
      {left > 0 && <small className="muted tabular">Вызов действует ещё {clock(left)}</small>}
    </div>
  </div>
}

type SaveState = 'saved' | 'dirty' | 'saving' | 'error'

/**
 * The test on the classroom PC (projector): one 6-minute timer for both items, autosave, «Завершить тест».
 * At 0 the editors lock and the answers are submitted; the server would finish the test with the last autosave anyway.
 * Nothing here shows the expected output, the checks or a grade.
 */
export function BoardTestScreen({ test, name, onFinished }: { test: BoardStudentTest; name: string; onFinished: () => void }) {
  const [codeItem, outputItem] = test.items
  const language = codeItem.language
  const [code, setCode] = useState(() => test.answers.code ?? (codeItem.starterCode || FALLBACK_CODE[language]))
  const [output, setOutput] = useState(() => test.answers.output ?? '')
  const latest = useRef({ code, output })
  latest.current = { code, output }
  // The server clock decides: endsAt is compared with the client clock shifted by the server's «now» of the last poll.
  const offset = useMemo(() => { const server = ms(test.now); return Number.isNaN(server) ? 0 : server - Date.now() }, [test.now])
  const now = useNow(250)
  const left = ms(test.endsAt) - (now + offset)
  const over = left <= 0
  const [finishing, setFinishing] = useState(false)
  const [confirming, setConfirming] = useState(false)
  const [error, setError] = useState('')
  const locked = over || finishing
  const done = useRef(false)

  // ───── autosave: shortly after typing stops and every few seconds while something is unsaved ─────
  const [save, setSave] = useState<SaveState>('saved')
  const dirty = useRef(false), saving = useRef(false)
  const persist = useCallback(async () => {
    if (!dirty.current || saving.current || done.current) return
    dirty.current = false; saving.current = true; setSave('saving')
    try {
      await api<{ savedAt: string }>(`/board/tests/${test.id}/answers`, { method: 'PUT', body: JSON.stringify(latest.current) })
      setSave(dirty.current ? 'dirty' : 'saved')
    } catch { dirty.current = true; setSave('error') }
    finally { saving.current = false }
  }, [test.id])
  const edited = () => { dirty.current = true; setSave('dirty') }
  useEffect(() => {
    if (!dirty.current) return
    const timer = setTimeout(persist, AUTOSAVE_DEBOUNCE_MS)
    return () => clearTimeout(timer)
  }, [code, output, persist])
  useEffect(() => { const timer = setInterval(persist, AUTOSAVE_MS); return () => clearInterval(timer) }, [persist])

  const finish = useCallback(async (auto: boolean) => {
    if (done.current) return
    done.current = true; setFinishing(true); setConfirming(false); setError('')
    try { await post<{ finished: boolean }>(`/board/tests/${test.id}/finish`, latest.current); onFinished() }
    catch (e) {
      // Time is up or the server already closed the test (e.g. the teacher finished it): the answers are on the server.
      if (auto || e instanceof ApiError) { onFinished(); return }
      done.current = false; setFinishing(false); setError('Нет связи с сервером — нажми «Завершить тест» ещё раз.')
    }
  }, [test.id, onFinished])
  useEffect(() => { if (over) finish(true) }, [over, finish])

  // ───── «Запустить» ─────
  const [run, setRun] = useState<{ console: ConsoleRun; n: number } | null>(null)
  const [running, setRunning] = useState(false)
  const consoleRef = useRef<HTMLElement>(null)
  async function runCode() {
    setRunning(true); setError('')
    try { const result = await post<{ console: ConsoleRun }>(`/board/tests/${test.id}/run`, { code }); setRun(r => ({ console: result.console, n: (r?.n ?? 0) + 1 })) }
    catch (e) { setError(e instanceof Error ? e.message : 'Не удалось запустить программу') }
    finally { setRunning(false) }
  }
  useEffect(() => { if (run) consoleRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }) }, [run])

  const low = left < 60_000
  return <main className="board-screen">
    <header className="board-bar">
      <div className="board-who">
        <span className="avatar" aria-hidden="true">{initials(name)}</span>
        <span><small>Ответ у доски</small><b>{name}</b></span>
      </div>
      <div className={`board-timer ${low ? 'low' : ''} ${over ? 'over' : ''}`} role="timer" aria-live="off" aria-label={`Осталось ${clock(left)}`}>
        <Icon name="clock" size={34} /><span className="tabular">{clock(left)}</span>
      </div>
      <div className="board-bar-actions">
        <SaveBadge state={locked ? 'saved' : save} />
        <button type="button" className="primary big" disabled={locked} onClick={() => setConfirming(true)}><Icon name="flag" size={18} /> Завершить тест</button>
      </div>
    </header>
    {error && <p className="board-error" role="alert">{error}</p>}
    <div className="board-items">
      <section className="board-item" aria-labelledby="board-item-1">
        <h2 id="board-item-1" className="board-item-title"><span className="board-num">1</span> Задача</h2>
        {codeItem.title && <h3 className="board-task-title">{codeItem.title}</h3>}
        <div className="board-statement"><Markdown>{codeItem.statement}</Markdown></div>
        <CodeMirror className="code-editor board-editor" value={code} extensions={EDITOR_EXTENSIONS[language]} editable={!locked} readOnly={locked}
          onChange={value => { setCode(value); edited() }} aria-label={`Редактор решения на ${courseTitle(language)}`} />
        <div className="task-actions">
          <button type="button" className="ghost big" disabled={locked || running || !code.trim()} onClick={runCode}>
            {running ? <><span className="spinner" aria-hidden="true" /> Запускаем…</> : <><Icon name="terminal" size={18} /> Запустить</>}</button>
        </div>
        {run && <ConsolePanel ref={consoleRef} key={run.n} run={run.console} origin="run" language={language} />}
      </section>
      <section className="board-item" aria-labelledby="board-item-2">
        <h2 id="board-item-2" className="board-item-title"><span className="board-num">2</span> Что выведет этот код?</h2>
        <CodeMirror className="code-editor board-program" value={outputItem.program} extensions={EDITOR_EXTENSIONS[outputItem.language]} editable={false} readOnly
          basicSetup={{ highlightActiveLine: false, highlightActiveLineGutter: false, foldGutter: false }} aria-label="Программа" />
        <label className="board-answer">
          <span>Точный вывод программы</span>
          <textarea value={output} disabled={locked} rows={6} spellCheck={false} autoComplete="off" autoCapitalize="off"
            onChange={e => { setOutput(e.target.value); edited() }} placeholder="Каждая напечатанная строка — с новой строки" />
        </label>
        <p className="board-hint">Пиши ровно то, что появится в консоли: пробелы, регистр и порядок строк важны.</p>
      </section>
    </div>
    {confirming && <div className="board-call-backdrop" role="dialog" aria-modal="true" aria-labelledby="board-confirm-title">
      <div className="board-call">
        <h2 id="board-confirm-title" className="title">Завершить тест?</h2>
        <p>Ответы отправятся преподавателю, изменить их будет нельзя. Осталось {clock(left)}.</p>
        <div className="board-confirm-actions">
          <button type="button" className="ghost big" onClick={() => setConfirming(false)} autoFocus>Продолжить тест</button>
          <button type="button" className="primary big" onClick={() => finish(false)}>Завершить</button>
        </div>
      </div>
    </div>}
    {finishing && <div className="board-call-backdrop" role="status"><div className="board-call"><span className="spinner big-spinner" aria-hidden="true" /><h2 className="title">{over ? 'Время вышло — сдаём тест…' : 'Сдаём тест…'}</h2></div></div>}
  </main>
}

function SaveBadge({ state }: { state: SaveState }) {
  const text = { saved: 'Сохранено', dirty: 'Сохраняем…', saving: 'Сохраняем…', error: 'Не сохранено — повторим' }[state]
  return <span className={`board-save ${state}`} aria-live="polite">{state === 'saved' ? <Icon name="check" size={16} /> : state === 'error' ? <Icon name="x" size={16} /> : <span className="spinner" aria-hidden="true" />}{text}</span>
}

/** After the test: no grade on this screen; the student is signed out after a short countdown. */
export function BoardDone({ onLogout }: { onLogout: () => void }) {
  const [left, setLeft] = useState(LOGOUT_SECONDS)
  const fired = useRef(false)
  useEffect(() => { const timer = setInterval(() => setLeft(s => Math.max(0, s - 1)), 1000); return () => clearInterval(timer) }, [])
  useEffect(() => { if (left === 0 && !fired.current) { fired.current = true; onLogout() } }, [left, onLogout])
  return <main className="board-screen board-done">
    <div className="board-done-card">
      <span className="board-done-icon"><Icon name="check" size={44} /></span>
      <h1 className="display">Тест сдан</h1>
      <p>Преподаватель посмотрит ответы и скажет оценку.</p>
      <p className="board-done-count">Выход из аккаунта через <b className="tabular">{left}</b> {plural(left, 'секунду', 'секунды', 'секунд')}</p>
      <button type="button" className="ghost big" onClick={() => { if (!fired.current) { fired.current = true; onLogout() } }}><Icon name="logout" size={18} /> Выйти сейчас</button>
    </div>
  </main>
}

/** «Мой прогресс»: the student's own answers at the board — date, grade and the teacher's comment. Hidden while there are none. */
export function StudentBoardGrades({ language }: { language: CourseLanguage }) {
  const [grades, setGrades] = useState<BoardStudentGrade[]>([])
  useEffect(() => {
    let alive = true
    setGrades([])
    api<{ grades: BoardStudentGrade[] }>(`/board/grades?language=${language}`).then(v => { if (alive) setGrades(v.grades) }, () => {})
    return () => { alive = false }
  }, [language])
  if (!grades.length) return null
  return <section className="card student-grades enter" aria-label="Ответы у доски">
    <h2 className="card-title"><span className="chip-icon"><Icon name="award" size={16} /></span> Ответы у доски</h2>
    <ul className="board-grades">{grades.map((g, i) => <li key={`${g.date}-${i}`}>
      <span className="muted">{shortDay(dayNumber(g.date))}</span><GradeChip grade={g.grade} />
      {g.comment && <span className="board-grade-comment">{g.comment}</span>}
    </li>)}</ul>
  </section>
}

// ═════════ Teacher ═════════

const STATUS: Record<BoardStatus, { text: string; tone: string }> = {
  CALLED: { text: 'Вызван', tone: 'warn' },
  STARTED: { text: 'Идёт тест', tone: 'ok' },
  FINISHED: { text: 'Сдан', tone: 'done' },
  CANCELLED: { text: 'Отменён', tone: '' },
  EXPIRED: { text: 'Не пришёл', tone: 'bad' },
}
function BoardStatusTag({ status }: { status: BoardStatus }) {
  return <span className={`status-chip ${STATUS[status]?.tone ?? ''}`}><i aria-hidden="true" />{STATUS[status]?.text ?? status}</span>
}
const live = (t: BoardTestSummary) => t.status === 'CALLED' || t.status === 'STARTED'

/** What is counting down: the call's expiry or the end of the test. */
function Countdown({ test, now }: { test: BoardTestSummary; now: number }) {
  const target = test.status === 'CALLED' ? ms(test.expiresAt) : test.status === 'STARTED' ? ms(test.endsAt) : NaN
  if (Number.isNaN(target)) return null
  const left = target - now
  return <span className={`board-countdown ${left < 60_000 ? 'low' : ''}`} title={test.status === 'CALLED' ? 'Вызов истекает через' : 'До конца теста'}>
    <Icon name="clock" size={15} /><b className="tabular">{left > 0 ? clock(left) : '0:00'}</b><small>{test.status === 'CALLED' ? (left > 0 ? 'ждём входа' : 'вызов истёк') : (left > 0 ? 'до конца' : 'время вышло')}</small>
  </span>
}

type Act = 'cancel' | 'recall' | 'extend' | 'finish' | 'delete' | 'assess'

/** Every action the teacher may take on a call or test; nothing is hidden behind the status except what has no meaning. */
function BoardActions({ test, busy, onAct }: { test: BoardTestSummary; busy: string | null; onAct: (act: Act, test: BoardTestSummary) => void }) {
  const [confirm, setConfirm] = useState(false)
  const mine = busy?.endsWith(`:${test.id}`) ? busy.split(':')[0] : null
  const button = (act: Act, icon: Parameters<typeof Icon>[0]['name'], text: string, className = 'ghost') =>
    <button type="button" className={`${className} small-button`} disabled={!!mine} onClick={() => act === 'delete' ? setConfirm(true) : onAct(act, test)}>
      {mine === act ? <span className="spinner" aria-hidden="true" /> : <Icon name={icon} size={15} />}{text}</button>
  if (confirm) return <div className="danger-zone open board-delete">
    <b>Удалить {test.status === 'CALLED' ? 'вызов' : 'тест'} — {test.displayName}?</b>
    <p className="muted small">Ответы, проверки, оценка LLM и итоговая оценка будут удалены. Восстановить нельзя.</p>
    <div className="password-row">
      <button type="button" className="danger-solid" disabled={mine === 'delete'} onClick={() => onAct('delete', test)}>{mine === 'delete' ? <><span className="spinner" aria-hidden="true" /> Удаляем…</> : 'Удалить'}</button>
      <button type="button" className="ghost" onClick={() => setConfirm(false)}>Отмена</button>
    </div>
  </div>
  return <div className="board-actions">
    {live(test) && button('extend', 'plus', '+1 мин')}
    {test.status === 'STARTED' && button('finish', 'flag', 'Завершить сейчас')}
    {test.status === 'CALLED' && button('cancel', 'x', 'Отменить')}
    {button('recall', 'refresh', 'Вызвать снова')}
    {button('delete', 'x', 'Удалить', 'ghost danger')}
  </div>
}

/** Teacher: «К доске» — call a student to the board, follow the test live, read the checks and the LLM assessment, set the grade. */
export function BoardAdmin({ request, groups }: { request: Request; groups: string[] | null }) {
  const [stored, setGroup] = useGroupFilter('rmzn-board-group', groups)
  const group = groups && stored && stored !== NO_GROUP && groups.includes(stored) ? stored : groups?.[0] ?? ''
  const [course, setCourse] = useState<{ group: string; language: CourseLanguage } | null>(null)
  const language = course && course.group === group ? course.language : null
  const [overview, setOverview] = useState<BoardOverview | null>(null)
  const [journal, setJournal] = useState<BoardJournal | null>(null)
  const [openId, setOpenId] = useState<Id | null>(null)
  const [busy, setBusy] = useState<string | null>(null)
  const [reload, setReload] = useState(0)
  const toast = useToast()
  const now = useNow()
  /** The detail view registers here to receive the test an action returns. */
  const detailUpdate = useRef<((test: BoardAdminTest) => void) | null>(null)
  const register = useCallback((update: ((test: BoardAdminTest) => void) | null) => { detailUpdate.current = update }, [])
  const detailRef = useRef<HTMLDivElement>(null)
  const query = group && language ? `group=${encodeURIComponent(group)}&language=${language}` : ''

  useEffect(() => {
    if (!group || course?.group === group) return
    let alive = true
    groupCourse(group).then(found => { if (alive) setCourse({ group, language: found ?? 'JAVA' }) })
    return () => { alive = false }
  }, [group, course?.group])

  // Members and active calls/tests, every 2 s: the first load reports errors, the polls stay quiet.
  useEffect(() => {
    if (!query) return
    let alive = true
    request(() => api<BoardOverview>(`/admin/board?${query}`)).then(v => { if (alive && v) setOverview(v) })
    const timer = setInterval(() => api<BoardOverview>(`/admin/board?${query}`).then(v => { if (alive) setOverview(v) }, () => {}), ADMIN_POLL_MS)
    return () => { alive = false; clearInterval(timer) }
  }, [query, reload, request])
  // The journal follows the active list: a finished or graded test shows up there.
  const activeKey = overview?.active.map(t => `${t.id}:${t.status}:${t.finalGrade ?? ''}:${t.suggestedGrade ?? ''}`).join() ?? ''
  useEffect(() => {
    if (!query) return
    let alive = true
    api<BoardJournal>(`/admin/board/journal?${query}`).then(v => { if (alive) setJournal(v) }, () => {})
    return () => { alive = false }
  }, [query, activeKey, reload])

  function chooseGroup(value: string) { if (value === group) return; setGroup(value); setOverview(null); setJournal(null); setOpenId(null) }
  function chooseCourse(value: CourseLanguage) { setCourse({ group, language: value }); setOverview(null); setJournal(null); setOpenId(null) }
  const open = (id: Id) => { setOpenId(id); requestAnimationFrame(() => detailRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })) }

  async function call(member: BoardMember) {
    if (!language) return
    setBusy(`call:${member.userId}`)
    const test = await request(() => post<BoardTestSummary>('/admin/board/call', { userId: member.userId, language }))
    setBusy(null)
    if (!test) return
    setReload(n => n + 1); open(test.id)
    toast({ tone: 'info', icon: 'flag', title: `Вызван к доске: ${member.displayName}`, text: 'Пусть войдёт в свой аккаунт на компьютере у доски — вызов действует 5 минут' })
  }
  const act = useCallback(async (action: Act, test: BoardTestSummary) => {
    setBusy(`${action}:${test.id}`)
    const path = `/admin/board/tests/${test.id}`
    const result = await request<BoardAdminTest | { deleted?: boolean } | undefined>(() =>
      action === 'delete' ? remove(path) : post(`${path}/${action}`, action === 'extend' ? { seconds: 60 } : undefined))
    setBusy(null)
    if (result === undefined && action !== 'delete') return
    setReload(n => n + 1)
    if (action === 'delete') {
      if (openId === test.id) setOpenId(null)
      toast({ tone: 'info', icon: 'x', title: 'Удалено', text: test.displayName }); return
    }
    const view = result as BoardAdminTest
    if (action === 'recall' && view?.id) { open(view.id); toast({ tone: 'info', icon: 'flag', title: `Снова вызван: ${test.displayName}`, text: 'Новый вызов на 5 минут' }); return }
    if (view?.id === openId) detailUpdate.current?.(view)
    if (action === 'extend') toast({ tone: 'info', icon: 'clock', title: '+1 минута', text: test.displayName })
  }, [request, openId, toast]) // eslint-disable-line react-hooks/exhaustive-deps

  const members = useMemo(() => {
    if (!overview) return null
    const suggested = overview.suggested
    return [...overview.members].sort((a, b) => Number(b.userId === suggested) - Number(a.userId === suggested) || Number(b.present) - Number(a.present)
      || (a.lastTestAt ? ms(a.lastTestAt) : -Infinity) - (b.lastTestAt ? ms(b.lastTestAt) : -Infinity) || a.displayName.localeCompare(b.displayName, 'ru'))
  }, [overview])
  const activeOf = (userId: Id) => overview?.active.find(t => t.userId === userId && live(t))

  if (groups && !groups.length) return <section className="analytics board-admin">
    <p className="eyebrow">Преподаватель</p><h1 className="display small">К доске</h1>
    <div className="card empty-task"><span className="empty-icon"><Icon name="user" size={26} /></span><p className="muted">К доске вызывают студентов группы. Сначала укажи группы студентам во вкладке «Студенты».</p></div>
  </section>

  const present = overview?.members.filter(m => m.present).length ?? 0
  return <section className="analytics board-admin">
    <div className="analytics-head enter">
      <div>
        <p className="eyebrow">Преподаватель</p>
        <h1 className="display small">К доске</h1>
        <p className="muted small">Вызови студента — он войдёт на компьютере у доски и решит тест за 6 минут. Оценка LLM и предложенная оценка видны только тебе.</p>
      </div>
      <div className="period" role="group" aria-label="Курс">
        {COURSES.map(([key, title]) => <button key={key} type="button" disabled={!language} className={key === language ? 'active' : ''} aria-pressed={key === language} onClick={() => key !== language && chooseCourse(key)}>{title}</button>)}
      </div>
    </div>

    <div className="card progress-controls enter">
      <div className="control-row">
        <span className="control-label">Группа</span>
        {!groups ? <span className="muted small">Загружаем…</span>
          : <div className="topic-filters group-filters" role="group" aria-label="Группа">{groups.map(g =>
            <button key={g} type="button" className={g === group ? 'active' : ''} aria-pressed={g === group} onClick={() => chooseGroup(g)}>{g}</button>)}</div>}
      </div>
    </div>

    <div className="board-grid">
      <div className="card board-members">
        <h2 className="card-title">Студенты{overview && <span className="muted small">{group} · {courseTitle(overview.language)} · на месте {present} из {overview.members.length}</span>}</h2>
        {!members ? <p className="muted">Загружаем…</p> : !members.length ? <p className="muted">В группе нет участников курса {language ? courseTitle(language) : ''}.</p>
          : <ul className="board-member-list">{members.map(m => {
            const suggested = m.userId === overview?.suggested, active = activeOf(m.userId)
            return <li key={m.userId} className={suggested ? 'suggested' : ''}>
              <span className={`presence ${m.present ? 'on' : ''}`} title={m.present ? 'На месте: занимается сейчас или был активен последний час' : 'Не активен последний час'}><span className="sr-only">{m.present ? 'на месте' : 'не на месте'}</span></span>
              <span className="board-member-meta">
                <b>{m.displayName}{suggested && <span className="suggest-tag">предлагаем</span>}</b>
                <small>{m.lastTestAt ? `у доски ${dayOnly(m.lastTestAt)} · ${m.tests} ${plural(m.tests, 'раз', 'раза', 'раз')}` : 'ещё не был у доски'}</small>
              </span>
              {active ? <button type="button" className="row-link board-member-state" onClick={() => open(active.id)}><BoardStatusTag status={active.status} /></button>
                : m.lastGrade && <span title="Последняя оценка у доски"><GradeChip grade={m.lastGrade} small /></span>}
              <button type="button" className={`${suggested ? 'primary' : 'ghost'} small-button`} disabled={busy === `call:${m.userId}`} onClick={() => call(m)}>
                {busy === `call:${m.userId}` ? <span className="spinner" aria-hidden="true" /> : <Icon name="flag" size={15} />}Вызвать</button>
            </li>
          })}</ul>}
        <p className="muted small table-note">Предложение: сначала те, кто на месте, затем кто дольше всех не был у доски (случайно среди трёх). Решаешь ты.</p>
      </div>

      <div className="board-side">
        <div className="card board-active">
          <h2 className="card-title"><span className="live-dot" aria-hidden="true" /> Сейчас у доски</h2>
          {!overview ? <p className="muted">Загружаем…</p> : !overview.active.length ? <p className="muted">Никто не вызван. Нажми «Вызвать» у студента.</p>
            : <ul className="board-active-list">{overview.active.map(t => <li key={t.id} className={openId === t.id ? 'selected' : ''}>
              <div className="board-active-head">
                <button type="button" className="row-link" onClick={() => open(t.id)}>{t.displayName}</button>
                <BoardStatusTag status={t.status} />
                <Countdown test={t} now={now} />
                {t.status === 'FINISHED' && <span className="board-active-grade">{t.assessmentStatus === 'PENDING' ? <><span className="spinner" aria-hidden="true" /> LLM оценивает</> : <>предложено <GradeChip grade={t.suggestedGrade} small /></>}{t.finalGrade && <> · итог <GradeChip grade={t.finalGrade} small /></>}</span>}
              </div>
              <BoardActions test={t} busy={busy} onAct={act} />
            </li>)}</ul>}
        </div>
        <div ref={detailRef} className="pair-anchor">
          {openId !== null && <BoardTestDetail key={openId} id={openId} request={request} busy={busy} onAct={act} onClose={() => setOpenId(null)} register={register} onSaved={() => setReload(n => n + 1)} />}
        </div>
      </div>
    </div>

    <BoardJournalCard journal={journal} openId={openId} onOpen={open} />
  </section>
}

/** Results of one item, whether the backend sends them aligned with items or keyed by kind. */
function checkOf(test: BoardAdminTest, kind: BoardItemKind, index: number): BoardCheck | null {
  const results = test.results
  if (!results) return null
  if (Array.isArray(results)) return results.find(r => r?.kind === kind) ?? results[index] ?? null
  return results[kind] ?? null
}
const visible = (text: string | null | undefined) => text == null ? '' : text.length ? text.replace(/ +$/gm, m => '·'.repeat(m.length)).replace(/\n/g, '↵\n') : '(пусто)'

function BoardTestDetail({ id, request, busy, onAct, onClose, register, onSaved }: {
  id: Id; request: Request; busy: string | null; onAct: (act: Act, test: BoardTestSummary) => void; onClose: () => void
  register: (update: ((test: BoardAdminTest) => void) | null) => void; onSaved: () => void
}) {
  const [test, setTest] = useState<BoardAdminTest | null>(null)
  const [failed, setFailed] = useState(false)
  const toast = useToast()
  useEffect(() => { register(setTest); return () => register(null) }, [register])
  const polling = !test || live(test) || test.assessment?.status === 'PENDING' || test.assessmentStatus === 'PENDING'
  useEffect(() => {
    let alive = true
    const load = () => api<BoardAdminTest>(`/admin/board/tests/${id}`).then(v => { if (alive) { setTest(v); setFailed(false) } }, e => { if (alive && e instanceof ApiError && e.status === 404) setFailed(true) })
    load()
    if (!polling) return () => { alive = false }
    const timer = setInterval(load, ADMIN_POLL_MS)
    return () => { alive = false; clearInterval(timer) }
  }, [id, polling])
  const now = useNow()

  async function assess() {
    if (!test) return
    const value = await request(() => post<BoardAdminTest>(`/admin/board/tests/${test.id}/assess`))
    if (value) setTest(value)
  }
  async function saveGrade(finalGrade: BoardGrade | null, comment: string) {
    if (!test) return false
    const value = await request(() => patch<BoardAdminTest>(`/admin/board/tests/${test.id}`, { finalGrade, comment: comment.trim() || null }))
    if (!value) return false
    setTest(value); onSaved()
    toast({ tone: 'info', icon: 'award', title: finalGrade ? `Оценка ${finalGrade} сохранена` : 'Оценка снята', text: `${value.displayName} · студент увидит её в «Моём прогрессе»` })
    return true
  }

  if (failed) return <section className="card board-detail"><div className="chart-head"><h2 className="card-title">Тест не найден</h2>
    <button type="button" className="icon-button" aria-label="Закрыть" onClick={onClose}><Icon name="x" /></button></div><p className="muted">Возможно, его удалили.</p></section>
  if (!test) return <section className="card board-detail"><p className="loading-note"><span className="spinner" aria-hidden="true" /> Загружаем тест…</p></section>

  const duration = test.startedAt && test.finishedAt ? Math.round((ms(test.finishedAt) - ms(test.startedAt)) / 1000) : null
  return <section className="card board-detail enter" aria-label={`Тест: ${test.displayName}`}>
    <div className="chart-head">
      <div>
        <p className="eyebrow">Ответ у доски</p>
        <h2 className="title">{test.displayName} <BoardStatusTag status={test.status} /></h2>
        <p className="muted small">Вызван {dayTime(test.calledAt)}{test.login && ` · ${test.login}`}{test.language && ` · ${courseTitle(test.language)}`}
          {duration !== null && ` · тест занял ${clock(duration * 1000)}`}</p>
      </div>
      <button type="button" className="icon-button" aria-label="Закрыть" title="Закрыть" onClick={onClose}><Icon name="x" /></button>
    </div>
    {live(test) && <div className="board-detail-live"><Countdown test={test} now={now} /></div>}
    <BoardActions test={test} busy={busy} onAct={onAct} />

    {test.status === 'CALLED' || test.status === 'CANCELLED' || test.status === 'EXPIRED'
      ? <p className="muted">{test.status === 'CALLED' ? 'Студент ещё не начал тест: задания выбираются, когда он нажмёт «Начать тест».' : 'Тест не проводился.'}</p>
      : <BoardTestBody test={test} assess={assess} saveGrade={saveGrade} />}
  </section>
}

function BoardTestBody({ test, assess, saveGrade }: { test: BoardAdminTest; assess: () => Promise<void>; saveGrade: (grade: BoardGrade | null, comment: string) => Promise<boolean> }) {
  const items = test.items ?? []
  const codeIndex = items.findIndex(i => i.kind === 'code'), outputIndex = items.findIndex(i => i.kind === 'output')
  const codeItem = items[codeIndex], outputItem = items[outputIndex]
  const assessmentStatus = test.assessment?.status ?? test.assessmentStatus
  return <>
    <div className="panel-facts">
      <span className="mini-stats-cell"><b><StatusChip status={test.paceStatus} /></b><small>темп к сессии · {test.paceCap ? `оценка не выше ${test.paceCap}` : 'без ограничения'}</small></span>
      <span className="mini-stats-cell"><b><GradeChip grade={test.ruleGrade} small /></b><small>по правилу (обе верно — 5 … ни одной — 2)</small></span>
      <span className="mini-stats-cell"><b>{assessmentStatus === 'PENDING' ? <span className="spinner" aria-hidden="true" /> : <GradeChip grade={assessmentStatus === 'DONE' && test.assessment?.grade != null ? String(test.assessment.grade) : null} small />}</b><small>оценка LLM</small></span>
      <span className="mini-stats-cell"><b><GradeChip grade={test.suggestedGrade} small /></b><small>предложено (с учётом темпа)</small></span>
    </div>
    <p className="teacher-note"><Icon name="lock" size={14} />Только для преподавателя — на экране у доски этого нет.</p>

    {codeItem && <BoardItemBlock n={1} title="Задача" item={codeItem} check={checkOf(test, 'code', codeIndex)} explanation={test.assessment?.items?.find(i => i.item === 'code')}>
      {codeItem.statement && <details className="board-statement-small"><summary>Условие</summary><Markdown>{codeItem.statement}</Markdown></details>}
      <div className="board-code"><small>Код студента</small><pre>{test.answers?.code || '(пусто)'}</pre></div>
    </BoardItemBlock>}
    {outputItem && <BoardItemBlock n={2} title="Что выведет этот код?" item={outputItem} check={checkOf(test, 'output', outputIndex)} explanation={test.assessment?.items?.find(i => i.item === 'output')}>
      <details className="board-statement-small"><summary>Программа</summary><pre>{outputItem.program}</pre></details>
      <div className="compare-grid">
        <div><small>Ответ студента</small><pre>{test.answers?.output ? visible(test.answers.output) : '(пусто)'}</pre></div>
        <div><small>Правильный вывод</small><pre>{visible(outputItem.expectedOutput ?? checkOf(test, 'output', outputIndex)?.expected) || '—'}</pre></div>
      </div>
      <p className="muted small">↵ — перевод строки, · — пробел в конце строки.</p>
    </BoardItemBlock>}

    <Runs runs={test.runs ?? []} language={test.language ?? codeItem?.language ?? 'JAVA'} />
    <Assessment assessment={test.assessment} status={assessmentStatus} finished={test.status === 'FINISHED'} onAssess={assess} />
    {test.status === 'FINISHED' && <GradeForm key={`${test.id}:${test.gradedAt ?? ''}:${test.finalGrade ?? ''}`} test={test} onSave={saveGrade} />}
  </>
}

function BoardItemBlock({ n, title, item, check, explanation, children }: { n: number; title: string; item: BoardAdminItem; check: BoardCheck | null; explanation?: { verdict: string; explanation: string }; children: ReactNode }) {
  const topic = item.skillTitle ?? item.skillCode
  return <div className="board-detail-item">
    <div className="board-detail-item-head">
      <h3><span className="board-num small">{n}</span> {title}{item.title && <span className="muted"> · {item.title}</span>}</h3>
      {check ? <span className={`check-tag ${check.passed ? 'ok' : 'bad'}`}><Icon name={check.passed ? 'check' : 'x'} size={14} />{check.passed ? 'верно' : 'не верно'}</span>
        : <span className="check-tag">не проверено</span>}
    </div>
    <p className="muted small board-item-ref">{[topic && `тема: ${topic}`, item.externalKey ?? (item.taskId != null ? `задача #${item.taskId}` : null)].filter(Boolean).join(' · ')}</p>
    {children}
    {check && (check.feedback || check.output) && <div className="board-code"><small>Проверка</small><pre>{check.feedback || check.output}</pre></div>}
    {check?.console && <ConsolePanel run={check.console} origin="attempt" language={item.language ?? 'JAVA'} />}
    {explanation && <div className="board-llm-item"><b><Icon name="sparkle" size={14} /> {explanation.verdict}</b><p>{explanation.explanation}</p></div>}
  </div>
}

function Runs({ runs, language }: { runs: BoardRun[]; language: CourseLanguage }) {
  if (!runs.length) return <p className="muted small board-runs-none">«Запустить» во время теста не нажимали.</p>
  return <details className="board-runs">
    <summary>Запуски во время теста · {runs.length}</summary>
    {runs.map((r, i) => <details key={i} className="board-run">
      <summary><span className={`check-tag ${r.console.status === 'OK' ? 'ok' : 'bad'}`}>{r.console.status}</span> запуск {i + 1}{(r.at ?? r.createdAt) && <span className="muted"> · {moscow(r.at ?? r.createdAt ?? '').time}</span>}</summary>
      <pre>{r.code}</pre>
      <ConsolePanel run={r.console} origin="run" language={language} />
    </details>)}
  </details>
}

function Assessment({ assessment, status, finished, onAssess }: { assessment: BoardAssessment | null; status: BoardAssessment['status'] | null | undefined; finished: boolean; onAssess: () => Promise<void> }) {
  const [busy, setBusy] = useState(false)
  const again = finished && <button type="button" className="ghost small-button" disabled={busy || status === 'PENDING'} onClick={async () => { setBusy(true); await onAssess(); setBusy(false) }}>
    {busy ? <span className="spinner" aria-hidden="true" /> : <Icon name="refresh" size={15} />}Оценить заново</button>
  return <div className="board-assessment">
    <h3 className="card-title"><span className="chip-icon"><Icon name="sparkle" size={16} /></span> Оценка LLM</h3>
    {!finished ? <p className="muted small">Появится после окончания теста.</p>
      : status === 'PENDING' ? <p className="loading-note"><span className="spinner" aria-hidden="true" /> LLM разбирает ответы…</p>
        : status === 'DONE' && assessment ? <>
          <p className="board-assessment-grade">Предлагает <GradeChip grade={assessment.grade != null ? String(assessment.grade) : null} /></p>
          {assessment.summary && <p className="board-assessment-summary">{assessment.summary}</p>}
          <p className="muted small">Пояснения по каждому заданию — выше, под заданием.</p>
        </>
          : <p className="board-unavailable"><Icon name="x" size={15} /> LLM недоступна{assessment?.error ? `: ${assessment.error}` : ''}. Оцени сам — проверки и код выше.</p>}
    {again}
  </div>
}

function GradeForm({ test, onSave }: { test: BoardAdminTest; onSave: (grade: BoardGrade | null, comment: string) => Promise<boolean> }) {
  const [grade, setGrade] = useState<BoardGrade | null>(test.finalGrade)
  const [comment, setComment] = useState(test.comment ?? '')
  const [saving, setSaving] = useState(false)
  const changed = grade !== test.finalGrade || comment.trim() !== (test.comment ?? '').trim()
  async function submit(e: FormEvent) {
    e.preventDefault(); setSaving(true)
    await onSave(grade, comment)
    setSaving(false)
  }
  return <form className="board-grade-form" onSubmit={submit}>
    <h3 className="card-title"><span className="chip-icon"><Icon name="award" size={16} /></span> Итоговая оценка</h3>
    <div className="board-grade-picks" role="radiogroup" aria-label="Итоговая оценка">
      {GRADES.map(g => <button key={g} type="button" role="radio" aria-checked={grade === g} className={`board-grade-pick g${g} ${grade === g ? 'active' : ''}`} onClick={() => setGrade(grade === g ? null : g)}>
        {g}{test.suggestedGrade === g && <small>предложено</small>}</button>)}
    </div>
    <label>Комментарий для студента<textarea rows={3} maxLength={1000} value={comment} onChange={e => setComment(e.target.value)} placeholder="Что получилось и что подтянуть — студент увидит это в «Моём прогрессе»" /></label>
    <div className="pair-form-actions">
      <button className="primary" disabled={saving || !changed}>{saving ? <><span className="spinner" aria-hidden="true" /> Сохраняем…</> : test.finalGrade ? 'Сохранить изменения' : 'Поставить оценку'}</button>
      <span className="muted small">{test.finalGrade ? `Сейчас: ${test.finalGrade}${test.gradedAt ? ` · ${dayTime(test.gradedAt)}` : ''}` : 'Оценка пока не выставлена — студент ничего не видит.'}</span>
    </div>
  </form>
}

/** Journal entries may be bare grades or objects with a grade. */
const gradeOf = (value: unknown): string | null => value && typeof value === 'object' ? (value as { grade?: string | null }).grade ?? null : (value as string | null) ?? null

function BoardJournalCard({ journal, openId, onOpen }: { journal: BoardJournal | null; openId: Id | null; onOpen: (id: Id) => void }) {
  const [all, setAll] = useState(false)
  const tests = journal?.tests ?? []
  const shown = all ? tests : tests.slice(0, 12)
  return <div className="list-stack board-journal">
    <div className="card">
      <h2 className="card-title">Журнал</h2>
      {!journal ? <p className="muted">Загружаем…</p> : !journal.students.length ? <p className="muted">Пока никого не вызывали.</p>
        : <div className="table-scroll"><table className="data-table board-journal-table">
          <thead><tr><th className="text">Студент</th><th className="text">Оценки у доски</th><th>Последний раз</th></tr></thead>
          <tbody>{journal.students.map(s => <tr key={s.userId}>
            <td className="text"><b>{s.displayName}</b></td>
            <td className="text"><span className="board-journal-grades">{s.grades.length ? s.grades.map((g, i) => <GradeChip key={i} grade={gradeOf(g)} small />) : <span className="muted">—</span>}</span></td>
            <td>{dayOnly(s.lastTestAt)}</td>
          </tr>)}</tbody>
        </table></div>}
    </div>
    {tests.length > 0 && <div className="card">
      <h2 className="card-title">Все вызовы<span className="muted small">{tests.length}</span></h2>
      <div className="table-scroll"><table className="data-table pair-list">
        <thead><tr><th className="text">Когда, МСК</th><th className="text">Студент</th><th className="text">Статус</th><th>Предложено</th><th>Итог</th></tr></thead>
        <tbody>{shown.map(t => <tr key={t.id} className={openId === t.id ? 'selected' : ''} onClick={() => onOpen(t.id)}>
          <td className="text"><button type="button" className="row-link" onClick={e => { e.stopPropagation(); onOpen(t.id) }}>{dayTime(t.calledAt)}</button></td>
          <td className="text">{t.displayName}</td>
          <td className="text"><BoardStatusTag status={t.status} /></td>
          <td><GradeChip grade={t.suggestedGrade} small /></td>
          <td><GradeChip grade={t.finalGrade} small /></td>
        </tr>)}</tbody>
      </table></div>
      {tests.length > shown.length && <button type="button" className="ghost small-button" onClick={() => setAll(true)}>Показать все ({tests.length})</button>}
    </div>}
  </div>
}
