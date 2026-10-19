import { CSSProperties, DragEvent, FormEvent, KeyboardEvent, ReactNode, RefObject, useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react'
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
  BoardAdminItem, BoardAdminTest, BoardAnswers, BoardAssessment, BoardCheck, BoardCurrent, BoardGrade, BoardItemKind, BoardJournal, BoardLine,
  BoardMember, BoardOverview, BoardReportItem, BoardRun, BoardScore, BoardStatus, BoardStudentGrade, BoardStudentItem, BoardStudentTest, BoardTestSummary,
  ConsoleRun, CourseLanguage, Id,
} from './types'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>

const COURSES: [CourseLanguage, string][] = [['JAVA', 'Java'], ['PYTHON', 'Python']]
const courseTitle = (language: CourseLanguage) => COURSES.find(c => c[0] === language)?.[1] ?? language
const GRADES: BoardGrade[] = ['2', '3', '4', '5']
const STUDENT_POLL_MS = 5_000, ADMIN_POLL_MS = 2_000, AUTOSAVE_MS = 5_000, AUTOSAVE_DEBOUNCE_MS = 1_200, LOGOUT_SECONDS = 10

/** The kinds of items in their fixed order: title, the phrase of the call dialog, minutes and weight (as the backend). */
const KINDS: BoardItemKind[] = ['parsons', 'fix', 'code']
const KIND: Record<BoardItemKind, { title: string; phrase: string; minutes: number; weight: number }> = {
  parsons: { title: 'Собери программу', phrase: 'собери программу', minutes: 2, weight: 1 },
  fix: { title: 'Исправь ошибку', phrase: 'исправь ошибку', minutes: 2, weight: 2 },
  code: { title: 'Напиши код', phrase: 'напиши код', minutes: 3, weight: 3 },
}
/** Known kinds in the canonical order; missing or empty → all three (as the backend's default). */
const canonical = (kinds: readonly string[] | null | undefined) => { const known = KINDS.filter(k => kinds?.includes(k)); return known.length ? known : [...KINDS] }
const minutesOf = (kinds: BoardItemKind[], durationSeconds?: number | null) => durationSeconds ? Math.round(durationSeconds / 60) : kinds.reduce((sum, k) => sum + KIND[k].minutes, 0)
const minutesText = (n: number) => `${n} ${plural(n, 'минуту', 'минуты', 'минут')}`

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

/** A line of code with its indentation kept and marked by guides (Python needs it). */
function CodeText({ text }: { text: string }) {
  const indent = /^[ \t]*/.exec(text)?.[0] ?? ''
  return <code className="parsons-code">{indent && <span className="parsons-indent">{indent}</span>}{text.slice(indent.length) || ' '}</code>
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
  const kinds = canonical(call.kinds)
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
      <p>Тест на {minutesText(minutesOf(kinds, call.durationSeconds))}: {kinds.map(k => KIND[k].phrase).join(', ')}. Таймер запустится, когда нажмёшь «Начать тест».</p>
      {error && <p className="form-error" role="alert">{error}</p>}
      <button type="button" className="primary big" disabled={busy} onClick={start} autoFocus>{busy ? <><span className="spinner" aria-hidden="true" /> Начинаем…</> : <>Начать тест <Icon name="arrow" /></>}</button>
      {left > 0 && <small className="muted tabular">Вызов действует ещё {clock(left)}</small>}
    </div>
  </div>
}

/** The code font on the projector (editor, console, «Собери программу»): A− / A+, remembered in this browser. */
const CODE_KEY = 'rmzn-board-code-size', CODE_MIN = 16, CODE_MAX = 32, CODE_DEFAULT = 21
function useCodeSize() {
  const [size, setSize] = useState(() => {
    try { const stored = Number(localStorage.getItem(CODE_KEY)); return stored >= CODE_MIN && stored <= CODE_MAX ? stored : CODE_DEFAULT } catch { return CODE_DEFAULT }
  })
  const zoom = useCallback((delta: number) => setSize(current => {
    const next = Math.max(CODE_MIN, Math.min(CODE_MAX, current + delta))
    try { localStorage.setItem(CODE_KEY, String(next)) } catch { /* private mode: not remembered */ }
    return next
  }), [])
  return [size, zoom] as const
}

type SaveState = 'saved' | 'dirty' | 'saving' | 'error'
type ParsonsItem = Extract<BoardStudentItem, { kind: 'parsons' }>
type FixItem = Extract<BoardStudentItem, { kind: 'fix' }>
type CodeItem = Extract<BoardStudentItem, { kind: 'code' }>
type RunKind = 'code' | 'fix'

/**
 * The test on the classroom PC (projector): one timer for the chosen items, shown one at a time with steps, autosave,
 * «Завершить тест». At 0 the answers lock and are submitted; the server would finish the test with the last autosave anyway.
 * Nothing here shows the solution, the checks or a grade.
 */
export function BoardTestScreen({ test, name, onFinished }: { test: BoardStudentTest; name: string; onFinished: () => void }) {
  const items = test.items
  const parsonsItem = items.find((i): i is ParsonsItem => i.kind === 'parsons')
  const fixItem = items.find((i): i is FixItem => i.kind === 'fix')
  const codeItem = items.find((i): i is CodeItem => i.kind === 'code')
  const initialCode = codeItem ? codeItem.starterCode || FALLBACK_CODE[codeItem.language] : ''
  const [code, setCode] = useState(() => test.answers.code ?? initialCode)
  const [fix, setFix] = useState(() => test.answers.fix ?? fixItem?.program ?? '')
  const [parsons, setParsons] = useState<string[]>(() => {
    const known = new Set(parsonsItem?.lines.map(l => l.id))
    return [...new Set(test.answers.parsons ?? [])].filter(id => known.has(id))
  })
  /** Only the chosen kinds go to the server. */
  const payload = (): BoardAnswers => ({ ...(parsonsItem && { parsons }), ...(fixItem && { fix }), ...(codeItem && { code }) })
  const latest = useRef(payload())
  latest.current = payload()
  const touched: Record<BoardItemKind, boolean> = { parsons: parsons.length > 0, fix: !!fixItem && fix !== fixItem.program, code: !!codeItem && code !== initialCode }
  const [step, setStep] = useState(0)
  const active = items[Math.min(step, items.length - 1)]

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

  // ───── autosave: shortly after an edit stops and every few seconds while something is unsaved ─────
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
  }, [code, fix, parsons, persist])
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

  // ───── «Запустить» (code and fix; each item keeps its own console) ─────
  const [runs, setRuns] = useState<Partial<Record<RunKind, { console: ConsoleRun; n: number }>>>({})
  const [running, setRunning] = useState<RunKind | null>(null)
  async function runItem(item: RunKind, text: string) {
    setRunning(item); setError('')
    try {
      const result = await post<{ console: ConsoleRun }>(`/board/tests/${test.id}/run`, { item, code: text })
      setRuns(r => ({ ...r, [item]: { console: result.console, n: (r[item]?.n ?? 0) + 1 } }))
    }
    catch (e) { setError(e instanceof Error ? e.message : 'Не удалось запустить программу') }
    finally { setRunning(null) }
  }

  // Steps: ← → between the tabs (WAI-ARIA tabs pattern).
  const tabs = useRef<(HTMLButtonElement | null)[]>([])
  const onTabKey = (e: KeyboardEvent<HTMLButtonElement>, i: number) => {
    const to = e.key === 'ArrowRight' ? (i + 1) % items.length : e.key === 'ArrowLeft' ? (i - 1 + items.length) % items.length
      : e.key === 'Home' ? 0 : e.key === 'End' ? items.length - 1 : null
    if (to === null) return
    e.preventDefault(); setStep(to); tabs.current[to]?.focus()
  }

  const low = left < 60_000
  const [codeSize, zoom] = useCodeSize()
  const toolbar = (item: BoardStudentItem, run?: ReactNode) => <div className="board-toolbar">
    <span className="board-file">{item.language === 'PYTHON' ? 'main.py' : 'Main.java'}</span>
    <span className="board-zoom" role="group" aria-label="Размер шрифта кода">
      <button type="button" disabled={codeSize <= CODE_MIN} onClick={() => zoom(-2)} aria-label="Уменьшить шрифт кода" title="Мельче">A−</button>
      <button type="button" disabled={codeSize >= CODE_MAX} onClick={() => zoom(2)} aria-label="Увеличить шрифт кода" title="Крупнее">A+</button>
    </span>
    {run}
  </div>
  return <main className="board-screen board-split" style={{ '--board-code': `${codeSize}px` } as CSSProperties}>
    <header className="board-bar">
      <div className="board-who">
        <span className="avatar" aria-hidden="true">{initials(name)}</span>
        <span><small>Ответ у доски</small><b>{name}</b></span>
      </div>
      {items.length > 1 ? <div className="board-steps" role="tablist" aria-label="Задания теста">
        {items.map((item, i) => <button key={item.kind} ref={el => { tabs.current[i] = el }} type="button" role="tab" id={`board-tab-${item.kind}`}
          aria-selected={item === active} aria-controls={`board-panel-${item.kind}`} tabIndex={item === active ? 0 : -1}
          className={`board-step ${item === active ? 'active' : ''} ${touched[item.kind] ? 'touched' : ''}`} onClick={() => setStep(i)} onKeyDown={e => onTabKey(e, i)}>
          <span className="board-num">{i + 1}</span>
          <span className="board-step-title">{KIND[item.kind].title}</span>
          {touched[item.kind] && <span className="board-step-mark" title="Ты уже начал это задание"><Icon name="check" size={15} /><span className="sr-only">начато</span></span>}
        </button>)}
      </div> : <span />}
      <div className={`board-timer ${low ? 'low' : ''} ${over ? 'over' : ''}`} role="timer" aria-live="off" aria-label={`Осталось ${clock(left)}`}>
        <Icon name="clock" size={26} /><span className="tabular">{clock(left)}</span>
      </div>
      <div className="board-bar-actions">
        <SaveBadge state={locked ? 'saved' : save} />
        <button type="button" className="primary" disabled={locked} onClick={() => setConfirming(true)}><Icon name="flag" size={18} /> Завершить тест</button>
      </div>
    </header>
    {error && <p className="board-error" role="alert">{error}</p>}
    <div className="board-body">
      {items.map((item, i) => {
        const next = items[i + 1], prev = items[i - 1]
        const head = <>
          <p className="board-item-eyebrow">{items.length > 1 && `${i + 1} из ${items.length} · `}{KIND[item.kind].title}</p>
          {item.title && <h2 className="board-task-title">{item.title}</h2>}
          {item.kind === 'fix' && <p className="board-callout"><Icon name="target" size={22} /> В программе есть ошибка: она работает не так, как требует условие. Найди и исправь её.</p>}
          {item.statement && <div className="board-statement"><Markdown>{item.statement}</Markdown></div>}
        </>
        return <section key={item.kind} id={`board-panel-${item.kind}`} className={`board-item ${items.length > 1 ? 'has-nav' : ''}`} hidden={item !== active}
          role={items.length > 1 ? 'tabpanel' : undefined} aria-labelledby={items.length > 1 ? `board-tab-${item.kind}` : undefined} aria-label={items.length > 1 ? undefined : KIND[item.kind].title}>
          {item.kind === 'parsons' ? <Parsons item={item} placed={parsons} locked={locked} head={head} toolbar={toolbar(item)} onChange={ids => { setParsons(ids); edited() }} />
            : <>
              <div className="board-task">{head}</div>
              <div className="board-work">
                {toolbar(item, <button type="button" className="ghost board-run-button" disabled={locked || running !== null || !(item.kind === 'fix' ? fix : code).trim()} onClick={() => runItem(item.kind, item.kind === 'fix' ? fix : code)}>
                  {running === item.kind ? <><span className="spinner" aria-hidden="true" /> Запускаем…</> : <><Icon name="terminal" size={18} /> Запустить</>}</button>)}
                <CodeMirror className="code-editor board-editor" value={item.kind === 'fix' ? fix : code} extensions={EDITOR_EXTENSIONS[item.language]} editable={!locked} readOnly={locked}
                  onChange={value => { if (item.kind === 'fix') setFix(value); else setCode(value); edited() }}
                  aria-label={item.kind === 'fix' ? `Программа с ошибкой на ${courseTitle(item.language)}` : `Редактор решения на ${courseTitle(item.language)}`} />
                {runs[item.kind] && <ConsolePanel key={runs[item.kind]!.n} run={runs[item.kind]!.console} origin="run" language={item.language} />}
              </div>
            </>}
          {items.length > 1 && <nav className="board-step-nav" aria-label="Переход между заданиями">
            {prev ? <button type="button" className="ghost big" onClick={() => setStep(i - 1)}><Icon name="back" size={18} /> {i}. {KIND[prev.kind].title}</button> : <span />}
            {next && <button type="button" className="secondary big" onClick={() => setStep(i + 1)}>{i + 2}. {KIND[next.kind].title} <Icon name="arrow" size={18} /></button>}
          </nav>}
        </section>
      })}
    </div>
    {confirming && <div className="board-call-backdrop" role="dialog" aria-modal="true" aria-labelledby="board-confirm-title">
      <div className="board-call">
        <h2 id="board-confirm-title" className="title">Завершить тест?</h2>
        <p>Ответы отправятся преподавателю, изменить их будет нельзя. Осталось {clock(left)}.</p>
        {items.some(i => !touched[i.kind]) && <p className="board-confirm-warn">Не начато: {items.filter(i => !touched[i.kind]).map(i => `«${KIND[i.kind].title}»`).join(', ')}.</p>}
        <div className="board-confirm-actions">
          <button type="button" className="ghost big" onClick={() => setConfirming(false)} autoFocus>Продолжить тест</button>
          <button type="button" className="primary big" onClick={() => finish(false)}>Завершить</button>
        </div>
      </div>
    </div>}
    {finishing && <div className="board-call-backdrop" role="status"><div className="board-call"><span className="spinner big-spinner" aria-hidden="true" /><h2 className="title">{over ? 'Время вышло — сдаём тест…' : 'Сдаём тест…'}</h2></div></div>}
  </main>
}

/**
 * «Собери программу»: the statement in the left pane; in the right one the sheet (the fixed code before and after, the
 * student's program between them) and the pool of lines right under it; the root has no box of its own, so both panes are columns of the item.
 * Click a pool line to append it; ↑ ↓ ✕ in the program; native drag & drop to reorder and to move between pool and program.
 * Every control is a focusable button, and focus follows the line it acted on.
 */
function Parsons({ item, placed, locked, head, toolbar, onChange }: { item: ParsonsItem; placed: string[]; locked: boolean; head: ReactNode; toolbar: ReactNode; onChange: (ids: string[]) => void }) {
  const byId = useMemo(() => new Map(item.lines.map(l => [l.id, l])), [item.lines])
  const program = placed.map(id => byId.get(id)).filter((l): l is BoardLine => !!l)
  const pool = item.lines.filter(l => !placed.includes(l.id))
  const root = useRef<HTMLDivElement>(null)
  const list = useRef<HTMLOListElement>(null)
  const focus = useRef<string | null>(null)
  useLayoutEffect(() => { if (focus.current) { root.current?.querySelector<HTMLElement>(focus.current)?.focus(); focus.current = null } })
  const [drag, setDrag] = useState<string | null>(null)
  const [dropAt, setDropAt] = useState<number | null>(null)
  const [overPool, setOverPool] = useState(false)
  const [said, setSaid] = useState('')
  const text = (id: string) => byId.get(id)?.text.trim() ?? ''

  function add(id: string) {
    const i = pool.findIndex(l => l.id === id), other = pool[i + 1] ?? pool[i - 1]
    focus.current = other ? `[data-pool="${other.id}"]` : `[data-placed="${id}"] [data-act="remove"]`
    onChange([...placed, id]); setSaid(`Строка добавлена в программу: ${text(id)}`)
  }
  function move(index: number, delta: -1 | 1) {
    const to = index + delta
    if (to < 0 || to >= placed.length) return
    const ids = [...placed]; [ids[index], ids[to]] = [ids[to], ids[index]]
    const id = placed[index]
    // A button at the edge becomes disabled: keep focus on the line by moving it to the other arrow.
    focus.current = `[data-placed="${id}"] [data-act="${to === 0 ? 'down' : to === placed.length - 1 ? 'up' : delta < 0 ? 'up' : 'down'}"]`
    onChange(ids); setSaid(`Строка ${to + 1} из ${placed.length}: ${text(id)}`)
  }
  function back(index: number) {
    const id = placed[index], other = placed[index + 1] ?? placed[index - 1]
    focus.current = other ? `[data-placed="${other}"] [data-act="remove"]` : `[data-pool="${id}"]`
    onChange(placed.filter(x => x !== id)); setSaid(`Строка убрана из программы: ${text(id)}`)
  }
  function dropInto(at: number, id: string) {
    const from = placed.indexOf(id)
    const ids = placed.filter(x => x !== id)
    ids.splice(from >= 0 && from < at ? at - 1 : at, 0, id)
    if (ids.join() !== placed.join()) onChange(ids)
  }

  // ───── drag & drop: the insertion point is found by the pointer against the rows' middles ─────
  const reset = () => { setDrag(null); setDropAt(null); setOverPool(false) }
  const start = (e: DragEvent, id: string) => {
    if (locked) { e.preventDefault(); return }
    e.dataTransfer.setData('text/plain', id); e.dataTransfer.effectAllowed = 'move'; setDrag(id)
  }
  const dragged = (e: DragEvent) => { const id = drag ?? e.dataTransfer.getData('text/plain'); return byId.has(id) ? id : null }
  function overProgram(e: DragEvent<HTMLOListElement>) {
    if (!drag) return
    e.preventDefault(); e.dataTransfer.dropEffect = 'move'
    const rows = [...(list.current?.querySelectorAll<HTMLElement>('[data-placed]') ?? [])]
    const at = rows.findIndex(row => { const r = row.getBoundingClientRect(); return e.clientY < r.top + r.height / 2 })
    setDropAt(at < 0 ? rows.length : at)
  }
  function dropProgram(e: DragEvent<HTMLOListElement>) {
    e.preventDefault()
    const id = dragged(e)
    if (id) dropInto(dropAt ?? placed.length, id)
    reset()
  }
  const leave = (e: DragEvent, clear: () => void) => { if (!e.currentTarget.contains(e.relatedTarget as Node | null)) clear() }

  const fixed = (code: string, where: string) => code ? <div className="parsons-fixed" aria-label={where}>
    {code.split('\n').map((line, i) => <div key={i} className="parsons-row"><span className="parsons-grip" aria-hidden="true" /><CodeText text={line} /></div>)}
  </div> : null

  return <div ref={root} className={`parsons ${locked ? 'locked' : ''} ${drag ? 'dragging' : ''}`}>
    <div className="board-task">
      {head}
    </div>
    <div className="board-work">
      {toolbar}
      <div className="parsons-sheet">
        {fixed(item.before, 'Код до твоей программы — менять не нужно')}
        <div className="parsons-zone">
          <div className="parsons-zone-head"><b>Твоя программа</b><small>{program.length ? `${program.length} ${plural(program.length, 'строка', 'строки', 'строк')}` : 'пока пусто'}</small></div>
          <ol ref={list} className={`parsons-program ${dropAt !== null ? 'drop-target' : ''}`} aria-label="Твоя программа"
            onDragOver={overProgram} onDrop={dropProgram} onDragLeave={e => leave(e, () => setDropAt(null))}>
            {program.map((line, i) => <li key={line.id} data-placed={line.id} draggable={!locked} onDragStart={e => start(e, line.id)} onDragEnd={reset}
              className={`parsons-row placed ${drag === line.id ? 'is-dragged' : ''} ${dropAt === i ? 'drop-before' : ''} ${dropAt === program.length && i === program.length - 1 ? 'drop-after' : ''}`}>
              <span className="parsons-grip" aria-hidden="true">⋮⋮</span>
              <CodeText text={line.text} />
              <span className="parsons-tools">
                <button type="button" data-act="up" disabled={locked || i === 0} onClick={() => move(i, -1)} aria-label={`Поднять строку ${i + 1}`} title="Поднять">↑</button>
                <button type="button" data-act="down" disabled={locked || i === program.length - 1} onClick={() => move(i, 1)} aria-label={`Опустить строку ${i + 1}`} title="Опустить">↓</button>
                <button type="button" data-act="remove" className="parsons-remove" disabled={locked} onClick={() => back(i)} aria-label={`Убрать строку ${i + 1} обратно в «Строки»`} title="Убрать в «Строки»">✕</button>
              </span>
            </li>)}
            {!program.length && <li className={`parsons-empty ${dropAt !== null ? 'drop-before' : ''}`}>Нажми на строку ниже или перетащи её сюда</li>}
          </ol>
        </div>
        {fixed(item.after, 'Код после твоей программы — менять не нужно')}
      </div>
      <div className={`parsons-pool ${overPool ? 'drop-target' : ''}`}
        onDragOver={e => { if (drag && placed.includes(drag)) { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; setOverPool(true) } }}
        onDragLeave={e => leave(e, () => setOverPool(false))}
        onDrop={e => { e.preventDefault(); const id = dragged(e); if (id && placed.includes(id)) onChange(placed.filter(x => x !== id)); reset() }}>
        <div className="parsons-zone-head"><b>Строки</b><small>{pool.length ? 'нажми, чтобы добавить в конец программы' : 'все строки в программе'}</small></div>
        {item.extraLines > 0 && <p className="parsons-extra-note"><Icon name="x" size={18} /> Одна строка лишняя — её не используй.</p>}
        <ul className="parsons-pool-list" aria-label="Строки">
          {pool.map(line => <li key={line.id}>
            <div role="button" tabIndex={locked ? -1 : 0} aria-disabled={locked} data-pool={line.id} className="parsons-row pooled" draggable={!locked}
              onDragStart={e => start(e, line.id)} onDragEnd={reset} aria-label={`Добавить строку: ${line.text.trim()}`}
              onClick={() => !locked && add(line.id)} onKeyDown={e => { if (!locked && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); add(line.id) } }}>
              <span className="parsons-grip" aria-hidden="true">⋮⋮</span>
              <CodeText text={line.text} />
              <span className="parsons-add" aria-hidden="true"><Icon name="plus" size={18} /></span>
            </div>
          </li>)}
        </ul>
      </div>
    </div>
    <p className="sr-only" aria-live="polite">{said}</p>
  </div>
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
    <ul className="board-grades">{grades.map((g, i) => <StudentGrade key={g.id ?? `${g.date}-${i}`} grade={g} open={i === 0} />)}</ul>
  </section>
}

const VERDICT_TONE: Record<BoardReportItem['verdict'], string> = { 'верно': 'ok', 'частично верно': 'warn', 'неверно': 'bad' }
const VERDICT_TEXT: Record<BoardReportItem['verdict'], string> = { 'верно': 'верно', 'частично верно': 'частично верно', 'неверно': 'не верно' }

/** One graded test: date, grade, comment and, when the teacher shows it, the report by item (the latest one opened). */
function StudentGrade({ grade: g, open: initiallyOpen }: { grade: BoardStudentGrade; open: boolean }) {
  const report = g.report?.length ? g.report : null
  const [open, setOpen] = useState(initiallyOpen && !!report)
  const id = `board-report-${g.id}`
  return <li className="board-grade-row">
    <div className="board-grade-head">
      <span className="muted">{shortDay(dayNumber(g.date))}</span><GradeChip grade={g.grade} />
      {g.comment && <span className="board-grade-comment">{g.comment}</span>}
      {report && <button type="button" className="ghost small-button board-report-button" aria-expanded={open} aria-controls={id} onClick={() => setOpen(o => !o)}>
        {open ? 'Свернуть' : 'Разбор'} <Icon name={open ? 'back' : 'arrow'} size={14} /></button>}
    </div>
    {report && open && <div className="board-report" id={id}>
      {report.map((item, i) => <div key={item.kind} className="board-report-item">
        <div className="board-report-item-head">
          <h3><span className="board-num small">{i + 1}</span> {KIND[item.kind]?.title ?? item.kind}{item.title && <span className="muted"> · {item.title}</span>}</h3>
          <span className={`check-tag ${VERDICT_TONE[item.verdict] ?? ''}`}><Icon name={item.verdict === 'верно' ? 'check' : 'x'} size={14} />{VERDICT_TEXT[item.verdict] ?? item.verdict}</span>
        </div>
        {item.statement && <details className="board-report-statement"><summary>Условие задачи</summary><Markdown>{item.statement}</Markdown></details>}
        <div className="board-code"><small>{item.kind === 'parsons' ? 'Твоя программа' : item.kind === 'fix' ? 'Твой исправленный код' : 'Твой код'}</small>
          <pre>{item.answer ?? (item.kind === 'parsons' ? '(программа не собрана)' : '(пусто)')}</pre></div>
        {item.extraUsed && <p className="board-report-hint bad">В программе есть лишняя строка — та, которую не нужно было использовать.</p>}
        {item.passed ? <p className="board-report-hint ok">Все проверки пройдены.</p>
          : item.check && <div className="board-code"><small>Проверка</small><pre>{item.check}</pre></div>}
      </div>)}
      <p className="muted small">Правильные решения здесь не показываются — эти задачи ещё могут встретиться тебе на уроках. Разбери их с преподавателем или в чате с помощником.</p>
    </div>}
  </li>
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

/** The kinds the teacher calls with, remembered in this browser (default: all three, never empty). */
const KINDS_KEY = 'rmzn-board-kinds'
function useBoardKinds() {
  const [kinds, setKinds] = useState<BoardItemKind[]>(() => {
    try { const stored = JSON.parse(localStorage.getItem(KINDS_KEY) ?? 'null'); return Array.isArray(stored) ? canonical(stored) : [...KINDS] } catch { return [...KINDS] }
  })
  const toggle = useCallback((kind: BoardItemKind) => setKinds(current => {
    const next = current.includes(kind) ? current.filter(k => k !== kind) : KINDS.filter(k => k === kind || current.includes(k))
    if (!next.length) return current
    try { localStorage.setItem(KINDS_KEY, JSON.stringify(next)) } catch { /* private mode: not remembered */ }
    return next
  }), [])
  return [kinds, toggle] as const
}

/** «Собери программу · Исправь ошибку · 7 мин» for a call or test; nothing for tests without kinds. */
function KindsNote({ test }: { test: Pick<BoardTestSummary, 'kinds' | 'durationSeconds'> }) {
  if (!test.kinds?.length) return null
  const kinds = canonical(test.kinds)
  return <small className="board-kinds-note">{kinds.map(k => KIND[k].title).join(' · ')} · {minutesOf(kinds, test.durationSeconds)} мин</small>
}

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
  const [kinds, toggleKind] = useBoardKinds()
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
  /** Opening a test scrolls to its detail as soon as it is rendered (the detail mounts with the new id). */
  const scrollTo = useRef(false)
  const scroll = () => { if (scrollTo.current && detailRef.current) { scrollTo.current = false; detailRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' }) } }
  useEffect(scroll)
  const open = (id: Id) => { scrollTo.current = true; setOpenId(id); requestAnimationFrame(scroll) }

  async function call(member: BoardMember) {
    if (!language) return
    setBusy(`call:${member.userId}`)
    const test = await request(() => post<BoardTestSummary>('/admin/board/call', { userId: member.userId, language, kinds }))
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
  return <section className="analytics board-admin board-wide">
    <div className="board-console">
      <div className="card board-left enter">
        <p className="eyebrow">Преподаватель</p>
        <h1 className="display small">К доске</h1>
        <p className="muted small board-lead">Вызови студента — он войдёт на компьютере у доски и решит тест из выбранных заданий. Оценка LLM и предложенная оценка видны только тебе.</p>
        {!groups ? <p className="muted small">Загружаем группы…</p>
          : <div className="topic-filters group-filters" role="group" aria-label="Группа">{groups.map(g =>
            <button key={g} type="button" className={g === group ? 'active' : ''} aria-pressed={g === group} onClick={() => chooseGroup(g)}>{g}</button>)}</div>}
        <div className="period" role="group" aria-label="Курс">
          {COURSES.map(([key, title]) => <button key={key} type="button" disabled={!language} className={key === language ? 'active' : ''} aria-pressed={key === language} onClick={() => key !== language && chooseCourse(key)}>{title}</button>)}
        </div>
        <fieldset className="board-kinds">
          <legend>Задания теста</legend>
          {KINDS.map(k => { const on = kinds.includes(k), last = on && kinds.length === 1
            return <label key={k} className={`board-kind ${on ? 'on' : ''}`} title={last ? 'Нужно хотя бы одно задание' : undefined}>
              <input type="checkbox" checked={on} disabled={last} onChange={() => toggleKind(k)} />
              <span>{KIND[k].title} <small>· {KIND[k].minutes} мин</small></span>
            </label> })}
          <span className="board-kinds-total">тест <b className="tabular">{minutesText(minutesOf(kinds))}</b></span>
        </fieldset>
        <h2 className="card-title">Студенты{overview && <span className="muted small">на месте {present} из {overview.members.length}</span>}</h2>
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

      <div className="card board-active">
        <h2 className="card-title"><span className="live-dot" aria-hidden="true" /> Сейчас у доски</h2>
        {!overview ? <p className="muted">Загружаем…</p> : !overview.active.length ? <p className="muted">Никто не вызван. Нажми «Вызвать» у студента.</p>
          : <ul className="board-active-list">{overview.active.map(t => <li key={t.id} className={openId === t.id ? 'selected' : ''}>
            <div className="board-active-head">
              <button type="button" className="row-link" onClick={() => open(t.id)}>{t.displayName}</button>
              <BoardStatusTag status={t.status} />
              <Countdown test={t} now={now} />
              <KindsNote test={t} />
              {t.status === 'FINISHED' && <span className="board-active-grade">{t.assessmentStatus === 'PENDING' ? <><span className="spinner" aria-hidden="true" /> LLM оценивает</> : <>предложено <GradeChip grade={t.suggestedGrade} small /></>}{t.finalGrade && <> · итог <GradeChip grade={t.finalGrade} small /></>}</span>}
            </div>
            <BoardActions test={t} busy={busy} onAct={act} />
          </li>)}</ul>}
      </div>

      {openId !== null
        ? <BoardTestDetail key={openId} id={openId} anchor={detailRef} request={request} busy={busy} onAct={act} onClose={() => setOpenId(null)} register={register} onSaved={() => setReload(n => n + 1)} />
        : <aside className="card board-summary" aria-label="Итог"><h2 className="card-title">Итог</h2><p className="muted small">{SUMMARY_HINT}</p></aside>}
    </div>

    <BoardJournalCard journal={journal} openId={openId} onOpen={open} />
  </section>
}

const SUMMARY_HINT = 'Открой сданный тест — здесь будут баллы, оценка LLM и итоговая оценка.'

/** Results of one item, whether the backend sends them aligned with items or keyed by kind. */
function checkOf(test: BoardAdminTest, kind: BoardItemKind, index: number): BoardCheck | null {
  const results = test.results
  if (!results) return null
  if (Array.isArray(results)) return results.find(r => r?.kind === kind) ?? results[index] ?? null
  return results[kind] ?? null
}
/** «1», «0,5», «0». */
const decimal = (n: number) => String(Math.round(n * 100) / 100).replace('.', ',')

/** The centre of an opened test: its items as tabs, one at a time, then the points and the runs. */
function BoardTestItems({ test }: { test: BoardAdminTest }) {
  const items = test.items ?? []
  const explanation = (kind: BoardItemKind) => test.assessment?.status === 'DONE' ? test.assessment.items?.find(i => i.item === kind) : undefined
  const [tab, setTab] = useState(0)
  const tabs = useRef<(HTMLButtonElement | null)[]>([])
  const onTabKey = (e: KeyboardEvent<HTMLButtonElement>, i: number) => {
    const to = e.key === 'ArrowRight' ? (i + 1) % items.length : e.key === 'ArrowLeft' ? (i - 1 + items.length) % items.length
      : e.key === 'Home' ? 0 : e.key === 'End' ? items.length - 1 : null
    if (to === null) return
    e.preventDefault(); setTab(to); tabs.current[to]?.focus()
  }
  const shown = Math.min(tab, items.length - 1)
  return <>
    {items.length > 0 && <div className="board-item-tabs" role="tablist" aria-label="Задания теста">
      {items.map((item, i) => <button key={item.kind} ref={el => { tabs.current[i] = el }} type="button" role="tab" id={`board-review-tab-${test.id}-${item.kind}`}
        aria-selected={i === shown} aria-controls={`board-review-${test.id}-${item.kind}`} tabIndex={i === shown ? 0 : -1}
        className={`board-item-tab ${i === shown ? 'active' : ''}`} onClick={() => setTab(i)} onKeyDown={e => onTabKey(e, i)}>
        <span className="board-num small">{i + 1}</span>{KIND[item.kind]?.title ?? item.kind}<CheckTag check={checkOf(test, item.kind, i)} />
      </button>)}
    </div>}
    {items.map((item, i) => {
      const check = checkOf(test, item.kind, i)
      return <BoardItemBlock key={item.kind} id={`board-review-${test.id}-${item.kind}`} labelledBy={`board-review-tab-${test.id}-${item.kind}`} hidden={i !== shown}
        item={item} check={check} explanation={explanation(item.kind)}>
        {item.statement && <div className="board-statement-open"><small>Условие</small><Markdown>{item.statement}</Markdown></div>}
        {item.kind === 'parsons' ? <ParsonsReview item={item} placed={test.answers?.parsons ?? null} assembled={check?.program ?? null} />
          : item.kind === 'fix' ? <>
            <div className="compare-grid">
              <div><small>Исправленный код студента</small><pre>{test.answers?.fix || '(пусто)'}</pre></div>
              <div><small>{item.reference ? 'Эталонное решение' : 'Программа с ошибкой'}</small><pre>{item.reference || item.program || '—'}</pre></div>
            </div>
            {item.bugDescription && <p className="board-bug"><b>Ошибка:</b> {item.bugDescription}</p>}
            {item.reference && item.program && <details className="board-statement-small"><summary>Программа с ошибкой</summary><pre>{item.program}</pre></details>}
          </>
            : <div className="compare-grid">
              <div><small>Код студента</small><pre>{test.answers?.code || '(пусто)'}</pre></div>
              <div><small>Проверка</small><pre>{check ? check.feedback || check.output || (check.passed ? 'Все проверки пройдены.' : '—') : 'Ещё не проверено.'}</pre></div>
            </div>}
      </BoardItemBlock>
    })}

    {test.score && <ScoreTable score={test.score} />}
    <Runs runs={test.runs ?? []} language={test.language ?? items[0]?.language ?? 'JAVA'} />
  </>
}

/** The right column of an opened test: the facts, the LLM assessment and the final grade. */
function BoardSummary({ test, assess, saveGrade }: { test: BoardAdminTest; assess: () => Promise<void>; saveGrade: (grade: BoardGrade | null, comment: string, reportVisible: boolean) => Promise<boolean> }) {
  const assessmentStatus = test.assessment?.status ?? test.assessmentStatus
  const score = test.score
  const ran = test.status === 'STARTED' || test.status === 'FINISHED'
  return <aside className="card board-summary" aria-label={`Итог: ${test.displayName}`}>
    <h2 className="card-title">Итог · {test.displayName}</h2>
    {ran && <>
      <div className="panel-facts">
        <span className="mini-stats-cell"><b><StatusChip status={test.paceStatus} /></b><small>темп к сессии · {test.paceCap ? `оценка не выше ${test.paceCap}` : 'без ограничения'}</small></span>
        <span className="mini-stats-cell"><b>{score ? <span className="tabular">{Math.round(score.percent)}%</span> : '—'}</b><small>{score ? `баллы ${decimal(score.points)} из ${decimal(score.max)}` : 'баллы — после проверки'}</small></span>
        <span className="mini-stats-cell"><b><GradeChip grade={test.ruleGrade} small /></b><small>по проверкам (без LLM)</small></span>
        <span className="mini-stats-cell"><b>{assessmentStatus === 'PENDING' ? <span className="spinner" aria-hidden="true" /> : <GradeChip grade={test.suggestedGrade} small />}</b><small>предложено (с учётом LLM и темпа)</small></span>
      </div>
      <p className="teacher-note"><Icon name="lock" size={14} />Только для преподавателя — на экране у доски этого нет.</p>
    </>}
    {test.status === 'FINISHED' ? <>
      <Assessment assessment={test.assessment} status={assessmentStatus} finished onAssess={assess} />
      <GradeForm key={`${test.id}:${test.gradedAt ?? ''}:${test.finalGrade ?? ''}:${test.reportVisible !== false}`} test={test} onSave={saveGrade} />
    </> : <p className="muted small">{test.status === 'STARTED' ? 'Тест идёт — оценка LLM и итоговая оценка появятся, когда студент сдаст тест.' : SUMMARY_HINT}</p>}
  </aside>
}

function CheckTag({ check }: { check: BoardCheck | null }) {
  return !check ? <span className="check-tag">не проверено</span>
    : check.unavailable ? <span className="check-tag warn" title="Проверка не запускалась"><Icon name="x" size={14} />проверка недоступна</span>
      : <span className={`check-tag ${check.passed ? 'ok' : 'bad'}`}><Icon name={check.passed ? 'check' : 'x'} size={14} />{check.passed ? 'верно' : 'не верно'}</span>
}

function BoardItemBlock({ id, labelledBy, hidden, item, check, explanation, children }: {
  id: string; labelledBy: string; hidden: boolean; item: BoardAdminItem; check: BoardCheck | null; explanation?: { verdict: string; explanation: string }; children: ReactNode
}) {
  const topic = item.skillTitle ?? item.skillCode
  return <div className="board-detail-item" id={id} role="tabpanel" aria-labelledby={labelledBy} hidden={hidden}>
    <p className="muted small board-item-ref">{item.title && <><b>{item.title}</b> · </>}{[`вес ${KIND[item.kind]?.weight ?? '—'}`, topic && `тема: ${topic}`, item.difficulty != null && `сложность ${item.difficulty}`,
      item.externalKey ?? (item.taskId != null ? `задача #${item.taskId}` : null)].filter(Boolean).join(' · ')}</p>
    {children}
    {item.kind !== 'code' && check && (check.feedback || check.output) && <div className="board-code"><small>Проверка</small><pre>{check.feedback || check.output}</pre></div>}
    {check?.console && <ConsolePanel run={check.console} origin="attempt" language={item.language ?? 'JAVA'} />}
    {explanation && <div className={`board-llm-item ${verdictTone(explanation.verdict)}`}><b><Icon name="sparkle" size={14} /> {explanation.verdict}</b><p>{explanation.explanation}</p></div>}
  </div>
}
const verdictTone = (verdict: string) => verdict === 'верно' ? 'ok' : verdict === 'частично верно' ? 'partly' : verdict === 'неверно' ? 'bad' : ''

/** «Собери программу» for the teacher: the correct program next to the student's assembled one, the extra line marked. */
function ParsonsReview({ item, placed, assembled }: { item: BoardAdminItem; placed: string[] | null; assembled: string | null }) {
  const lines = new Map((item.lines ?? []).map(l => [l.id, l]))
  const solution = (item.solution ?? []).map(id => lines.get(id)?.text).filter((t): t is string => t != null)
  const correct = item.reference || [item.before, ...solution, item.after].filter(part => part).join('\n')
  const ids = placed ?? []
  const extra = item.extraLineId ? lines.get(item.extraLineId) : null
  const usedExtra = !!item.extraLineId && ids.includes(item.extraLineId)
  const fixedLines = (code: string | null | undefined) => code ? code.split('\n').map((line, i) => <span key={i} className="parsons-review-fixed">{line}{'\n'}</span>) : null
  return <>
    <div className="compare-grid">
      <div><small>Собрал студент</small>
        {!ids.length ? <pre>{assembled || '(программа не собрана)'}</pre>
          : lines.size ? <pre>{fixedLines(item.before)}{ids.map((id, i) => {
            const text = lines.get(id)?.text ?? `(строка ${id})`
            return id === item.extraLineId ? <mark key={i} className="parsons-review-extra">{text}  ← лишняя{'\n'}</mark> : <span key={i}>{text}{'\n'}</span>
          })}{fixedLines(item.after)}</pre>
            : <pre>{assembled}</pre>}
      </div>
      <div><small>Правильная программа</small><pre>{correct || '—'}</pre></div>
    </div>
    <p className="muted small">{ids.length ? `Использовано строк: ${ids.length} из ${lines.size}` : 'Студент не поставил ни одной строки.'}
      {extra && <> · лишняя строка <code>{extra.text.trim()}</code> — {usedExtra ? <b className="board-extra-used">использована</b> : 'не использована'}</>}
      {!item.extraLineId && ' · лишней строки не было'}</p>
  </>
}

function ScoreTable({ score }: { score: BoardScore }) {
  return <div className="board-score">
    <h3 className="card-title"><span className="chip-icon"><Icon name="target" size={16} /></span> Баллы</h3>
    <div className="table-scroll"><table className="data-table board-score-table">
      <thead><tr><th className="text">Задание</th><th>Вес</th><th>Оценка</th><th>Баллы</th></tr></thead>
      <tbody>{score.items.map(s => <tr key={s.kind}>
        <td className="text">{KIND[s.kind]?.title ?? s.kind}</td>
        <td>{s.weight}</td>
        <td><span className={`check-tag ${s.score >= 1 ? 'ok' : s.score > 0 ? 'warn' : 'bad'}`}>{decimal(s.score)}</span></td>
        <td>{decimal(s.weight * s.score)}</td>
      </tr>)}</tbody>
      <tfoot><tr><td className="text"><b>Итого</b></td><td>{decimal(score.max)}</td><td /><td><b>{decimal(score.points)} из {decimal(score.max)} · {Math.round(score.percent)}%</b></td></tr></tfoot>
    </table></div>
    <p className="muted small table-note">Прошло проверку или «верно» по LLM (например, расходится только формат вывода) — 1, «частично верно» по LLM — 0,5, иначе 0. Оценка по проценту: ≥ 90 — 5, ≥ 75 — 4, ≥ 50 — 3, ниже — 2.</p>
  </div>
}

function Runs({ runs, language }: { runs: BoardRun[]; language: CourseLanguage }) {
  if (!runs.length) return <p className="muted small board-runs-none">«Запустить» во время теста не нажимали.</p>
  return <details className="board-runs">
    <summary>Запуски во время теста · {runs.length}</summary>
    {runs.map((r, i) => <details key={i} className="board-run">
      <summary><span className={`check-tag ${r.console.status === 'OK' ? 'ok' : 'bad'}`}>{r.console.status}</span> запуск {i + 1}{r.item && KIND[r.item] && <span> · {KIND[r.item].title}</span>}{(r.at ?? r.createdAt) && <span className="muted"> · {moscow(r.at ?? r.createdAt ?? '').time}</span>}</summary>
      <pre>{r.code}</pre>
      <ConsolePanel run={r.console} origin="run" language={language} />
    </details>)}
  </details>
}

function Assessment({ assessment, status, finished, onAssess }: { assessment: BoardAssessment | null; status: BoardAssessment['status'] | null | undefined; finished: boolean; onAssess: () => Promise<void> }) {
  const [busy, setBusy] = useState(false)
  const again = finished && <button type="button" className="ghost small-button" disabled={busy || status === 'PENDING'} onClick={async () => { setBusy(true); await onAssess(); setBusy(false) }}>
    {busy ? <span className="spinner" aria-hidden="true" /> : <Icon name="refresh" size={15} />}Оценить заново</button>
  const questions = assessment?.questions?.filter(q => q?.trim()) ?? []
  return <div className="board-assessment">
    <h3 className="card-title"><span className="chip-icon"><Icon name="sparkle" size={16} /></span> Оценка LLM</h3>
    {!finished ? <p className="muted small">Появится после окончания теста.</p>
      : status === 'PENDING' ? <p className="loading-note"><span className="spinner" aria-hidden="true" /> LLM разбирает ответы…</p>
        : status === 'DONE' && assessment ? <>
          {assessment.summary && <p className="board-assessment-summary">{assessment.summary}</p>}
          {!!assessment.items?.length && <ul className="board-verdicts">{assessment.items.map(v => <li key={v.item}>
            {KIND[v.item]?.title ?? v.item} <span className={`board-verdict ${verdictTone(v.verdict)}`}>{v.verdict}</span></li>)}</ul>}
          <p className="muted small">Пояснения по каждому заданию — во вкладках заданий.</p>
          {questions.length > 0 && <div className="board-questions">
            <b><Icon name="chat" size={15} /> Вопросы для устного разбора</b>
            <ol>{questions.map((q, i) => <li key={i}>{q}</li>)}</ol>
          </div>}
        </>
          : <p className="board-unavailable"><Icon name="x" size={15} /> LLM недоступна{assessment?.error ? `: ${assessment.error}` : ''}. Оцени сам — проверки и код во вкладках заданий.</p>}
    {again}
  </div>
}


function BoardTestDetail({ id, anchor, request, busy, onAct, onClose, register, onSaved }: {
  id: Id; anchor: RefObject<HTMLDivElement | null>; request: Request; busy: string | null; onAct: (act: Act, test: BoardTestSummary) => void; onClose: () => void
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
  async function saveGrade(finalGrade: BoardGrade | null, comment: string, reportVisible: boolean) {
    if (!test) return false
    const value = await request(() => patch<BoardAdminTest>(`/admin/board/tests/${test.id}`, { finalGrade, comment: comment.trim() || null, reportVisible }))
    if (!value) return false
    setTest(value); onSaved()
    toast({ tone: 'info', icon: 'award', title: finalGrade ? `Оценка ${finalGrade} сохранена` : 'Оценка снята', text: `${value.displayName} · студент увидит её в «Моём прогрессе»` })
    return true
  }

  const hint = <aside className="card board-summary" aria-label="Итог"><h2 className="card-title">Итог</h2><p className="muted small">{SUMMARY_HINT}</p></aside>
  if (failed) return <><div ref={anchor} className="pair-anchor board-detail-area"><section className="card board-detail"><div className="chart-head"><h2 className="card-title">Тест не найден</h2>
    <button type="button" className="icon-button" aria-label="Закрыть" onClick={onClose}><Icon name="x" /></button></div><p className="muted">Возможно, его удалили.</p></section></div>{hint}</>
  if (!test) return <><div ref={anchor} className="pair-anchor board-detail-area"><section className="card board-detail"><p className="loading-note"><span className="spinner" aria-hidden="true" /> Загружаем тест…</p></section></div>{hint}</>

  const duration = test.startedAt && test.finishedAt ? Math.round((ms(test.finishedAt) - ms(test.startedAt)) / 1000) : null
  return <>
    <div ref={anchor} className="pair-anchor board-detail-area">
      <section className="card board-detail enter" aria-label={`Тест: ${test.displayName}`}>
        <div className="chart-head">
          <div>
            <p className="eyebrow">Ответ у доски</p>
            <h2 className="title">{test.displayName} <BoardStatusTag status={test.status} /></h2>
            <p className="muted small">Вызван {dayTime(test.calledAt)}{test.login && ` · ${test.login}`}{test.language && ` · ${courseTitle(test.language)}`}
              {duration !== null && ` · тест занял ${clock(duration * 1000)}`}</p>
            <KindsNote test={test} />
          </div>
          <button type="button" className="icon-button" aria-label="Закрыть" title="Закрыть" onClick={onClose}><Icon name="x" /></button>
        </div>
        {live(test) && <div className="board-detail-live"><Countdown test={test} now={now} /></div>}
        <BoardActions test={test} busy={busy} onAct={onAct} />

        {test.status === 'CALLED' || test.status === 'CANCELLED' || test.status === 'EXPIRED'
          ? <p className="muted">{test.status === 'CALLED' ? 'Студент ещё не начал тест: задания выбираются, когда он нажмёт «Начать тест».' : 'Тест не проводился.'}</p>
          : <BoardTestItems test={test} />}
      </section>
    </div>
    <BoardSummary test={test} assess={assess} saveGrade={saveGrade} />
  </>
}


function GradeForm({ test, onSave }: { test: BoardAdminTest; onSave: (grade: BoardGrade | null, comment: string, reportVisible: boolean) => Promise<boolean> }) {
  const [grade, setGrade] = useState<BoardGrade | null>(test.finalGrade)
  // The LLM's draft for the student fills the comment until the teacher grades for the first time; later it can be inserted.
  const draft = test.assessment?.status === 'DONE' ? test.assessment.studentComment?.trim() ?? '' : ''
  const fresh = !test.finalGrade && !test.comment
  const [comment, setComment] = useState(test.comment ?? (fresh ? draft : ''))
  useEffect(() => { if (fresh && draft) setComment(current => current.trim() ? current : draft) }, [fresh, draft])
  const [report, setReport] = useState(test.reportVisible !== false)
  const [saving, setSaving] = useState(false)
  const changed = grade !== test.finalGrade || comment.trim() !== (test.comment ?? '').trim() || report !== (test.reportVisible !== false)
  async function submit(e: FormEvent) {
    e.preventDefault(); setSaving(true)
    await onSave(grade, comment, report)
    setSaving(false)
  }
  return <form className="board-grade-form" onSubmit={submit}>
    <h3 className="card-title"><span className="chip-icon"><Icon name="award" size={16} /></span> Итоговая оценка</h3>
    <div className="board-grade-picks" role="radiogroup" aria-label="Итоговая оценка">
      {GRADES.map(g => <button key={g} type="button" role="radio" aria-checked={grade === g} className={`board-grade-pick g${g} ${grade === g ? 'active' : ''}`} onClick={() => setGrade(grade === g ? null : g)}>
        {g}{test.suggestedGrade === g && <small>предложено</small>}</button>)}
    </div>
    <label>Комментарий для студента<textarea rows={4} maxLength={500} value={comment} onChange={e => setComment(e.target.value)} placeholder="Что получилось и что подтянуть — студент увидит это в «Моём прогрессе»" /></label>
    {draft && comment.trim() === draft && comment.trim() !== (test.comment ?? '').trim()
      ? <p className="muted small board-comment-draft"><Icon name="sparkle" size={14} /> Черновик от нейросети — поправь, если нужно. Студент увидит комментарий только после сохранения.</p>
      : draft && comment.trim() !== draft && <button type="button" className="ghost small-button board-comment-draft" onClick={() => setComment(draft)}><Icon name="sparkle" size={14} /> Вставить черновик нейросети</button>}
    <label className="board-report-toggle"><input type="checkbox" checked={report} onChange={e => setReport(e.target.checked)} />
      <span><b>Показать студенту разбор</b><small>В «Моём прогрессе»: по каждому заданию условие, его код, «верно / частично / не верно» и сообщение проверки. Без эталона, описания ошибки, баллов и пояснений LLM.</small></span></label>
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
