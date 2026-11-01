import CodeMirror from '@uiw/react-codemirror'
import { useCallback, useEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from 'react'
import { api, post } from './api'
import { ConsolePanel } from './console'
import { EDITOR_EXTENSIONS, Markdown } from './editor'
import { Icon, initials } from './fx'
import { plural } from './session'
import type { ConsoleRun, CourseLanguage, Id } from './types'
import './relay.css'

/**
 * «Эстафета» (CodeRelay on the backend): the whole group solves one task in one editor, one writer at a time, one small
 * step per turn. A skip («Пас» or the time is out) drops the group's streak. The student's screen and the teacher's
 * console open over the app (RelayLayer, mounted next to App); the board station projects the running relay.
 */

type RelayStatus = 'LOBBY' | 'RUNNING' | 'PAUSED' | 'SOLVED' | 'FINISHED'
type Outcome = 'DONE' | 'PASS' | 'TIMEOUT' | 'TEACHER_DONE' | 'TEACHER_SKIP' | 'STOPPED'
interface RelayPerson { userId: Id; name: string; present: boolean }
interface RelayRun extends Partial<Omit<ConsoleRun, 'status'>> { status: ConsoleRun['status'] | 'PENDING'; matches?: boolean; at?: string }
export interface RelayView {
  id: Id; group: string; language: CourseLanguage; status: RelayStatus
  task: { key: string; title: string; statement: string; steps: number }
  code: string; version: number; step: number; steps: number
  stepPrompt: string | null; nextPrompt: string | null; donePrompts: string[]
  turn: number; turnSeconds: number; writer: { userId: Id; name: string } | null
  turnEndsAt: string | null; pausedLeftMs: number | null
  queue: RelayPerson[]; members: number
  streak: number; bestStreak: number; record: number; skips: number
  lastTurn: { outcome: Outcome; step: number; at: string; name: string } | null
  run: RelayRun | null; now: string
  me?: { userId: Id; member: boolean; writing: boolean; turnsAhead: number }
  hint?: string | null; reference?: string; credited?: number[]
  people?: (RelayPerson & { done: number; skipped: number; other: number })[]
  log?: { turn: number; step: number; outcome: Outcome | null; startedAt: string; endedAt: string | null; name: string }[]
}
interface RelayTask { key: string; language: CourseLanguage; title: string; statement: string; steps: number }
interface RelayAdmin { tasks: RelayTask[]; groups: string[]; relay: RelayView | null }
interface RelayMe { role: 'ADMIN' | 'STUDENT'; relay: RelayView | null }

const POLL_MS = 1_000, LAYER_POLL_MS = 5_000, SAVE_DEBOUNCE_MS = 300, LOCK_BEFORE_MS = 300, FLASH_MS = 2_600
const COURSE: Record<CourseLanguage, string> = { JAVA: 'Java', PYTHON: 'Python' }
const GROUP_KEY = 'relay.group'

const ms = (iso: string | null | undefined) => iso ? Date.parse(iso) : NaN
const stepWord = (n: number) => plural(n, 'шаг', 'шага', 'шагов')

/** Polls a loader every period while enabled; drops answers that came back after a newer request. */
function usePoll<T>(load: () => Promise<T>, period: number, enabled: boolean, onValue: (value: T) => void, onError?: (error: unknown) => void) {
  const seq = useRef(0)
  const latest = useRef({ load, onValue, onError })
  latest.current = { load, onValue, onError }
  const tick = useCallback(() => {
    const id = ++seq.current
    latest.current.load().then(v => { if (id === seq.current) latest.current.onValue(v) }, e => { if (id === seq.current) latest.current.onError?.(e) })
  }, [])
  useEffect(() => {
    if (!enabled) return
    tick()
    const timer = setInterval(tick, period)
    return () => { clearInterval(timer); seq.current++ }
  }, [enabled, period, tick])
  /** Answers of requests sent before now are ignored (a fresher state came from another request). */
  const invalidate = useCallback(() => { seq.current++ }, [])
  return { tick, invalidate }
}

/** Milliseconds left in the turn by the server's clock (the offset is taken from the view's «now»). */
function useTurnLeft(view: RelayView | null) {
  const offset = useMemo(() => { const server = ms(view?.now); return Number.isNaN(server) ? 0 : server - Date.now() }, [view?.now])
  const [now, setNow] = useState(() => Date.now())
  useEffect(() => { const timer = setInterval(() => setNow(Date.now()), 200); return () => clearInterval(timer) }, [])
  if (!view) return null
  if (view.status === 'PAUSED') return view.pausedLeftMs
  const ends = ms(view.turnEndsAt)
  return view.status === 'RUNNING' && !Number.isNaN(ends) ? Math.max(0, ends - (now + offset)) : null
}

/** A short line about the turn that just ended, shown for a moment to everybody. */
function useFlash(view: RelayView | null) {
  const [flash, setFlash] = useState<{ text: string; tone: 'good' | 'bad' | 'plain' } | null>(null)
  const seen = useRef<string | null | undefined>(undefined)
  const at = view?.lastTurn?.at ?? null
  useEffect(() => {
    if (seen.current === undefined) { seen.current = at; return }
    if (at === seen.current || !view?.lastTurn) return
    seen.current = at
    const { outcome, name, step } = view.lastTurn
    const text = outcome === 'DONE' ? `${name}: шаг ${step + 1} ✓` : outcome === 'TEACHER_DONE' ? `Шаг ${step + 1} засчитан преподавателем`
      : outcome === 'PASS' ? `${name} пасует — серия сброшена` : outcome === 'TIMEOUT' ? `Время вышло — серия сброшена`
        : outcome === 'TEACHER_SKIP' ? `Ход ${name} пропущен` : null
    if (!text) return
    setFlash({ text, tone: outcome === 'DONE' || outcome === 'TEACHER_DONE' ? 'good' : outcome === 'TEACHER_SKIP' ? 'plain' : 'bad' })
    const timer = setTimeout(() => setFlash(null), FLASH_MS)
    return () => clearTimeout(timer)
  }, [at, view?.lastTurn])
  return flash
}

/** Two short notes when the pen comes to this student. */
function beep() {
  try {
    const Ctx = window.AudioContext ?? (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext
    if (!Ctx) return
    const ctx = new Ctx(), gain = ctx.createGain(); gain.connect(ctx.destination); gain.gain.value = 0.08
    ;[660, 880].forEach((f, i) => { const o = ctx.createOscillator(); o.frequency.value = f; o.connect(gain); o.start(ctx.currentTime + i * 0.14); o.stop(ctx.currentTime + i * 0.14 + 0.12) })
    setTimeout(() => ctx.close(), 600)
  } catch { /* no sound is fine */ }
}

// ---------------------------------------------------------------- the board everybody sees

function Timer({ left, total, paused }: { left: number | null; total: number; paused: boolean }) {
  if (left === null) return <span className="relay-timer idle"><Icon name="clock" size={22} /><b>—</b></span>
  const seconds = Math.ceil(left / 1000), share = Math.max(0, Math.min(1, left / (total * 1000)))
  return <span className={`relay-timer ${paused ? 'paused' : seconds <= 5 ? 'low' : ''}`} style={{ '--share': share } as CSSProperties}>
    <Icon name="clock" size={22} /><b className="tabular">{seconds}</b><small>{paused ? 'пауза' : 'сек'}</small>
  </span>
}

function Banner({ view }: { view: RelayView }) {
  if (view.status === 'LOBBY') return <p className="relay-banner"><span className="spinner" aria-hidden="true" /> Ждём начала: присоединились {view.members} {plural(view.members, 'человек', 'человека', 'человек')}</p>
  if (view.status === 'PAUSED') return <p className="relay-banner warn">Пауза — преподаватель скоро продолжит</p>
  if (view.status === 'SOLVED') return <p className="relay-banner good"><Icon name="check" size={20} /> Задача решена! Пропусков: {view.skips}</p>
  if (view.status === 'RUNNING' && !view.writer) return <p className="relay-banner"><span className="spinner" aria-hidden="true" /> Ждём участников — никого нет на месте</p>
  return null
}

function RunResult({ run, language }: { run: RelayRun; language: CourseLanguage }) {
  const status = run.status
  if (status === 'PENDING') return <p className="relay-run-note"><span className="spinner" aria-hidden="true" /> Запускаем программу…</p>
  return <div className="relay-run">
    {run.matches !== undefined && <p className={`relay-run-note ${run.matches ? 'good' : 'bad'}`}>{run.matches ? 'Вывод совпал с ожидаемым ✓' : 'Вывод не совпал с ожидаемым'}</p>}
    <ConsolePanel run={{ status, stdout: run.stdout ?? '', error: run.error, truncated: run.truncated ?? false }} origin="run" language={language} />
  </div>
}

/**
 * The shared screen: the task, the steps (done, the current one, the next), the code, who writes and the timer, the
 * streak and the group's record, the queue. mode «teacher» adds nothing here — the console puts its panel beside it.
 */
function RelayBoard({ view, code, editable, onCode, footer, flash }: {
  view: RelayView; code: string; editable: boolean; onCode?: (code: string) => void; footer?: ReactNode; flash: ReturnType<typeof useFlash>
}) {
  const left = useTurnLeft(view)
  const upcoming = view.queue.filter(p => p.present).slice(0, 6)
  return <div className={`relay-board ${editable ? 'writing' : ''}`}>
    <header className="relay-head">
      <div className="relay-title">
        <p className="eyebrow">Эстафета · {view.group} · {COURSE[view.language]}</p>
        <h1 className="display small">{view.task.title}</h1>
      </div>
      <div className="relay-stats">
        <span className="relay-stat"><small>Шаг</small><b className="tabular">{Math.min(view.step + 1, view.steps)}<em>/{view.steps}</em></b></span>
        <span className={`relay-stat streak ${view.streak > 0 ? 'hot' : ''}`}><small>Серия</small><b className="tabular"><Icon name="flame" size={18} />{view.streak}</b></span>
        <span className="relay-stat"><small>Рекорд группы</small><b className="tabular"><Icon name="crown" size={18} />{view.record}</b></span>
        <Timer left={left} total={view.turnSeconds} paused={view.status === 'PAUSED'} />
      </div>
    </header>
    <Banner view={view} />
    <div className="relay-main">
      <section className="relay-steps" aria-label="Задача и шаги">
        <div className="relay-statement"><Markdown>{view.task.statement}</Markdown></div>
        <ol className="relay-step-list">
          {view.donePrompts.map((p, i) => <li key={i} className="done"><Icon name="check" size={15} /><Markdown inline>{p}</Markdown></li>)}
          {view.stepPrompt && <li className="current">
            <span className="relay-step-no">{view.step + 1}</span>
            <span><Markdown inline>{view.stepPrompt}</Markdown>{view.writer && <small className="relay-step-who">пишет {view.writer.name}</small>}</span>
          </li>}
          {view.nextPrompt && <li className="next"><span className="relay-step-no">{view.step + 2}</span><span><Markdown inline>{view.nextPrompt}</Markdown><small className="relay-step-who">дальше</small></span></li>}
          {view.step + 2 < view.steps && <li className="more">…ещё {view.steps - view.step - 2} {stepWord(view.steps - view.step - 2)}</li>}
        </ol>
      </section>
      <section className="relay-code" aria-label="Общий код">
        <div className="relay-writer">
          {view.writer ? <><span className="avatar" aria-hidden="true">{initials(view.writer.name)}</span><b>{editable ? 'Пишешь ты' : `Пишет ${view.writer.name}`}</b></> : <b className="muted">Сейчас никто не пишет</b>}
          {flash && <span className={`relay-flash ${flash.tone}`} role="status">{flash.text}</span>}
        </div>
        <CodeMirror className={`code-editor relay-editor ${editable ? 'editable' : ''}`} value={code} extensions={EDITOR_EXTENSIONS[view.language]} editable={editable} readOnly={!editable}
          onChange={value => onCode?.(value)} autoFocus={editable} aria-label="Общий код группы" />
        {view.run && <RunResult run={view.run} language={view.language} />}
      </section>
    </div>
    <footer className="relay-foot">
      {view.status !== 'SOLVED' && <div className="relay-queue" aria-label="Очередь">
        <small>Дальше</small>
        {upcoming.length ? upcoming.map((p, i) => <span key={p.userId} className={`relay-chip ${i === 0 ? 'first' : ''}`}><span className="avatar" aria-hidden="true">{initials(p.name)}</span>{p.name}</span>)
          : <span className="muted">—</span>}
        {view.queue.length > upcoming.length && <small className="muted">и ещё {view.queue.length - upcoming.length}</small>}
      </div>}
      {footer}
    </footer>
  </div>
}

// ---------------------------------------------------------------- the student

/**
 * The student's screen. While it is his turn the editor is his: the text goes to the server 300 ms after he stops typing
 * (a passed step ends the turn at once), the editor locks a moment before the time is out; otherwise the code comes
 * from the polls. «Пас» gives the step to the next student (and drops the streak).
 */
function RelayStudent({ initial, onHide, onGone }: { initial: RelayView; onHide: () => void; onGone: () => void }) {
  const [view, setView] = useState(initial)
  const [local, setLocal] = useState<string | null>(null)
  const [error, setError] = useState('')
  const myTurn = useRef<number | null>(null)
  const pending = useRef<{ code: string; timer: ReturnType<typeof setTimeout> } | null>(null)
  const flash = useFlash(view)
  const left = useTurnLeft(view)
  const writing = !!view.me?.writing && myTurn.current === view.turn

  const accept = useCallback((next: RelayView) => {
    setView(next)
    if (next.me?.writing && myTurn.current !== next.turn) { myTurn.current = next.turn; setLocal(next.code); beep() }
    else if (!next.me?.writing && myTurn.current !== null) { myTurn.current = null; setLocal(null) }
  }, [])
  const poll = usePoll(() => api<RelayMe>('/relay/me'), POLL_MS, true, me => { if (!me.relay) onGone(); else accept(me.relay) })
  useEffect(() => { accept(initial) }, [accept, initial])

  const send = useCallback(async (code: string, turn: number) => {
    poll.invalidate()
    try { accept(await api<RelayView>(`/relay/${view.id}/code`, { method: 'PUT', body: JSON.stringify({ turn, code }) })); setError('') }
    catch (e) { if (myTurn.current === turn) setError(e instanceof Error ? e.message : 'Не удалось сохранить') }
  }, [accept, poll, view.id])
  const flush = useCallback(() => {
    const p = pending.current
    if (!p || myTurn.current === null) return
    clearTimeout(p.timer); pending.current = null
    void send(p.code, myTurn.current)
  }, [send])
  const typed = useCallback((code: string) => {
    if (myTurn.current === null) return
    setLocal(code)
    if (pending.current) clearTimeout(pending.current.timer)
    pending.current = { code, timer: setTimeout(flush, SAVE_DEBOUNCE_MS) }
  }, [flush])
  const locked = !writing || (left !== null && left <= LOCK_BEFORE_MS)
  useEffect(() => { if (writing && locked) flush() }, [writing, locked, flush])

  async function pass() {
    if (myTurn.current === null) return
    const turn = myTurn.current
    if (pending.current) { clearTimeout(pending.current.timer); pending.current = null }
    poll.invalidate()
    try { accept(await post<RelayView>(`/relay/${view.id}/pass`, { turn })) } catch (e) { setError(e instanceof Error ? e.message : 'Не получилось') }
  }

  const ahead = view.me?.turnsAhead ?? -1
  const note = writing ? <p className="relay-you now"><Icon name="bolt" size={20} /> Твой ход: сделай шаг {view.step + 1}</p>
    : ahead === 0 ? <p className="relay-you soon"><Icon name="flag" size={20} /> Готовься — ты следующий</p>
      : ahead > 0 ? <p className="relay-you">Твой ход через {ahead + 1} {plural(ahead + 1, 'ход', 'хода', 'ходов')}</p>
        : null
  return <div className="relay-layer" role="dialog" aria-modal="true" aria-label="Эстафета">
    <RelayBoard view={view} code={writing && local !== null ? local : view.code} editable={writing && !locked} onCode={typed} flash={flash}
      footer={<div className="relay-actions">
        {note}
        {error && <p className="board-error" role="alert">{error}</p>}
        {writing && <button type="button" className="ghost big" onClick={pass} disabled={locked}>Пас</button>}
        <button type="button" className="ghost" onClick={onHide}><Icon name="back" size={16} /> К уроку</button>
      </div>} />
  </div>
}

// ---------------------------------------------------------------- the teacher

const ACTIONS: { action: string; label: string; when: (v: RelayView) => boolean; primary?: boolean; confirm?: string }[] = [
  { action: 'start', label: 'Начать', when: v => v.status === 'LOBBY', primary: true },
  { action: 'pause', label: 'Пауза', when: v => v.status === 'RUNNING' },
  { action: 'resume', label: 'Продолжить', when: v => v.status === 'PAUSED', primary: true },
  { action: 'extend', label: '+10 с', when: v => (v.status === 'RUNNING' || v.status === 'PAUSED') && !!v.writer },
  { action: 'credit', label: 'Засчитать шаг', when: v => (v.status === 'RUNNING' || v.status === 'PAUSED') && !!v.writer },
  { action: 'skip', label: 'Пропустить ход', when: v => (v.status === 'RUNNING' || v.status === 'PAUSED') && !!v.writer },
  { action: 'restore', label: 'Вернуть код начала хода', when: v => v.turn > 0 && v.status !== 'FINISHED' },
  { action: 'run', label: 'Запустить код', when: v => v.status !== 'FINISHED' && v.status !== 'LOBBY' },
  { action: 'finish', label: 'Завершить', when: v => v.status !== 'FINISHED', confirm: 'Завершить эстафету?' },
]
const OUTCOME: Record<Outcome, string> = { DONE: 'шаг сделан', PASS: 'пас', TIMEOUT: 'время вышло', TEACHER_DONE: 'засчитан', TEACHER_SKIP: 'пропущен', STOPPED: 'остановлен' }

function readGroup() { try { return localStorage.getItem(GROUP_KEY) ?? '' } catch { return '' } }
function saveGroup(group: string) { try { localStorage.setItem(GROUP_KEY, group) } catch { /* not kept */ } }

/** The teacher's console: open a relay for a group, run it, see the reference of the step and who did what; «Показ» projects it. */
function RelayConsole({ onClose }: { onClose: () => void }) {
  const [data, setData] = useState<RelayAdmin | null>(null)
  const [group, setGroup] = useState(readGroup)
  const [taskKey, setTaskKey] = useState('')
  const [seconds, setSeconds] = useState('25')
  const [busy, setBusy] = useState<string | null>(null)
  const [error, setError] = useState('')
  const [show, setShow] = useState(false)
  const view = data?.relay ?? null
  const flash = useFlash(view)
  const poll = usePoll(() => api<RelayAdmin>(`/admin/relay?group=${encodeURIComponent(group)}`), POLL_MS, true,
    d => { setData(d); if (!group && d.groups.length) setGroup(d.groups[0]) }, e => setError(e instanceof Error ? e.message : 'Нет связи'))
  useEffect(() => { if (group) saveGroup(group) }, [group])
  useEffect(() => { if (!show) return; const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') setShow(false) }; window.addEventListener('keydown', esc); return () => window.removeEventListener('keydown', esc) }, [show])

  async function act(action: string, confirmText?: string) {
    if (!view || (confirmText && !window.confirm(confirmText))) return
    setBusy(action); setError(''); poll.invalidate()
    try { const next = await post<RelayView>(`/admin/relay/${view.id}/${action}`); setData(d => d && { ...d, relay: next.status === 'FINISHED' ? null : next }) }
    catch (e) { setError(e instanceof Error ? e.message : 'Не получилось') }
    finally { setBusy(null) }
  }
  async function create() {
    setBusy('create'); setError(''); poll.invalidate()
    try { const relay = await post<RelayView>('/admin/relay', { group, taskKey, turnSeconds: Number(seconds) }); setData(d => d && { ...d, relay }) }
    catch (e) { setError(e instanceof Error ? e.message : 'Не получилось') }
    finally { setBusy(null) }
  }

  if (show && view) return <div className="relay-layer projector" role="dialog" aria-modal="true" aria-label="Эстафета на проекторе">
    <RelayBoard view={view} code={view.code} editable={false} flash={flash} footer={<button type="button" className="ghost small-button relay-show-close" onClick={() => setShow(false)}>Esc — назад</button>} />
  </div>

  const tasks = data?.tasks ?? []
  return <div className="relay-layer teacher" role="dialog" aria-modal="true" aria-label="Эстафета: пульт">
    <div className="relay-console-bar">
      <b><Icon name="flag" size={18} /> Эстафета</b>
      <label>Группа <select value={group} onChange={e => setGroup(e.target.value)}>{(data?.groups ?? []).map(g => <option key={g} value={g}>{g}</option>)}</select></label>
      {view && <button type="button" className="secondary" onClick={() => setShow(true)}><Icon name="globe" size={16} /> Показ</button>}
      <button type="button" className="ghost" onClick={onClose}><Icon name="x" size={16} /> Закрыть</button>
    </div>
    {error && <p className="board-error" role="alert">{error}</p>}
    {!data ? <p className="loading-note"><span className="spinner" aria-hidden="true" /> Загружаем…</p>
      : !view ? <section className="card relay-new">
        <h2 className="title">Новая эстафета для группы {group || '—'}</h2>
        <p className="muted">Студенты группы увидят приглашение у себя в уроке и присоединятся. Очередь перемешается, когда ты нажмёшь «Начать».</p>
        <div className="relay-task-list" role="radiogroup" aria-label="Задача">
          {tasks.map(t => <label key={t.key} className={`relay-task ${taskKey === t.key ? 'chosen' : ''}`}>
            <input type="radio" name="relay-task" checked={taskKey === t.key} onChange={() => setTaskKey(t.key)} />
            <span><b>{COURSE[t.language]} · {t.title}</b><small>{t.steps} {stepWord(t.steps)}</small><Markdown>{t.statement}</Markdown></span>
          </label>)}
        </div>
        <label className="relay-seconds">Секунд на ход <input type="number" min={5} max={120} value={seconds} onChange={e => setSeconds(e.target.value)} /></label>
        <button type="button" className="primary big" disabled={!group || !taskKey || busy !== null} onClick={create}>{busy === 'create' ? 'Открываем…' : 'Открыть эстафету'}</button>
      </section>
        : <div className="relay-console">
          <RelayBoard view={view} code={view.code} editable={false} flash={flash} />
          <aside className="relay-panel card">
            <div className="relay-buttons">
              {ACTIONS.filter(a => a.when(view)).map(a => <button key={a.action} type="button" className={a.primary ? 'primary' : 'ghost'} disabled={busy !== null || (a.action === 'run' && view.run?.status === 'PENDING')}
                onClick={() => act(a.action, a.confirm)}>{busy === a.action ? '…' : a.label}</button>)}
            </div>
            {view.hint && <div className="relay-hint"><small>Эталон шага {view.step + 1} (видишь только ты)</small><pre>{view.hint}</pre></div>}
            <h3 className="card-title">Участники · {view.people?.length ?? 0}</h3>
            <ul className="relay-people">
              {(view.people ?? []).map(p => <li key={p.userId}>
                <span className={`relay-dot ${p.present ? 'on' : ''}`} title={p.present ? 'на месте' : 'не на месте'} />
                <span className="relay-person">{p.name}</span>
                <span className="tabular" title="шагов сделано">✓ {p.done}</span>
                <span className="tabular muted" title="пропусков">⨯ {p.skipped}</span>
              </li>)}
            </ul>
            {!!view.log?.length && <>
              <h3 className="card-title">Ходы</h3>
              <ol className="relay-log">{view.log.map(t => <li key={t.turn}><span className="tabular">{t.turn}.</span> {t.name} · шаг {t.step + 1} · {t.outcome ? OUTCOME[t.outcome] : 'пишет'}</li>)}</ol>
            </>}
          </aside>
        </div>}
  </div>
}

// ---------------------------------------------------------------- the projector (board station)

/** The board station's screen while a relay runs: the shared board, nothing that only the teacher may see. */
export function RelayProjector({ view }: { view: RelayView }) {
  const flash = useFlash(view)
  return <main className="relay-layer projector station"><RelayBoard view={view} code={view.code} editable={false} flash={flash} /></main>
}

// ---------------------------------------------------------------- the layer over the app

/**
 * Mounted next to App: finds out (every 5 s, quietly — no sign-in prompts) whether the signed-in student's group has a
 * relay, and offers to join or come back to it; the pen coming to him opens his screen by itself. The teacher gets a
 * button to his console. Nothing is shown when nobody is signed in (the login form, the board station).
 */
export function RelayLayer() {
  const [me, setMe] = useState<RelayMe | null>(null)
  const [open, setOpen] = useState(false)
  const [busy, setBusy] = useState(false)
  const quiet = useCallback(async () => {
    const response = await fetch('/api/relay/me', { credentials: 'include' })
    return response.ok ? await response.json() as RelayMe : null
  }, [])
  const relay = me?.relay ?? null
  const member = !!relay?.me?.member
  // A member with the screen closed is polled every second: the pen may come to him any moment.
  usePoll(quiet, member && relay?.status === 'RUNNING' ? POLL_MS : LAYER_POLL_MS, !open, setMe, () => setMe(null))
  // The pen came to him while his screen was closed: open it.
  useEffect(() => { if (relay?.me?.writing) setOpen(true) }, [relay?.me?.writing])

  async function join() {
    if (!relay) return
    setBusy(true)
    try { const view = await post<RelayView>(`/relay/${relay.id}/join`); setMe(m => m && { ...m, relay: view }); setOpen(true) }
    catch { /* the next poll tells */ }
    finally { setBusy(false) }
  }

  if (!me) return null
  if (me.role === 'ADMIN') return open ? <RelayConsole onClose={() => setOpen(false)} />
    : <button type="button" className="relay-fab" onClick={() => setOpen(true)}><Icon name="flag" size={16} /> Эстафета</button>
  if (!relay) return null
  if (open && member) return <RelayStudent initial={relay} onHide={() => setOpen(false)} onGone={() => { setOpen(false); setMe(m => m && { ...m, relay: null }) }} />
  return <div className="relay-invite" role="status">
    <Icon name="flag" size={20} />
    <span><b>Эстафета для группы {relay.group}</b><small>{relay.task.title} · {relay.status === 'LOBBY' ? 'скоро начнём' : 'уже идёт'}</small></span>
    {member ? <button type="button" className="primary" onClick={() => setOpen(true)}>Вернуться</button>
      : <button type="button" className="primary" disabled={busy} onClick={join}>{busy ? '…' : 'Присоединиться'}</button>}
  </div>
}
