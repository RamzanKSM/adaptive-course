import { CSSProperties, FormEvent, useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { api, post, remove } from './api'
import { DrawSound } from './drawSound'
import { Burst, Icon, useToast } from './fx'
import { plural } from './session'
import type { Id, Pair } from './types'
import './wheel.css'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>
type Mode = 'ARROW' | 'ELIMINATION'
export type DrawSettings = {
  spinSeconds: number; mode: Mode; eliminationSeconds: number; winners: number; autoNext: boolean; topPercent: number; minPoints: number
  boardMinGrade: number; defaultPrize: string; surprisePrize: boolean; sound: boolean; volume: number
  chances: 'POINTS' | 'EQUAL'; bonus5: number; bonus4: number; bonus3: number
}
type SettingsView = DrawSettings & { defaults: DrawSettings }
type Person = { userId: Id; login: string; displayName: string; attended: boolean; points: number; grade: string | null; weight: number; reason?: 'BOARD' | 'TOP' }
type Win = { userId: Id; login: string; displayName: string; absent: boolean }
type Run = { id: Id; mode: Mode; winners: number; prize: string; names: Id[]; wheel: Id[]; outs: Id[]; wins: Win[]; replacing: boolean; finished: boolean; createdAt: string }
type Step = { pick: { userId: Id; kind: 'WIN' | 'OUT' } | null; won: Id[]; run: Run }
type Wheel = {
  pairId: Id; topPercent: number; minPoints: number; boardMinGrade: number; pool: number; topCount: number; threshold: number | null
  candidates: Person[]; called: Person[]; others: Person[]; runs: Run[]; prize: string; settings: SettingsView
}

const time = (iso: string) => new Date(iso).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Moscow' })
const pts = (n: number) => `${n} ${plural(n, 'балл', 'балла', 'баллов')}`
const decimal = (n: number) => String(n).replace('.', ',')
const reasonText = (p: Person) => p.reason === 'BOARD' ? `${p.grade} у доски` : p.reason === 'TOP' ? `топ: ${pts(p.points)}`
  : p.grade ? `у доски: ${p.grade}` : !p.attended ? 'не был' : pts(p.points)
const prizeIcon = (prize: string) => prize.toLowerCase().includes('шоколад') ? '🍫' : '🎁'
const MODES: [Mode, string][] = [['ARROW', 'Стрелка'], ['ELIMINATION', 'Выбывание']]
const GRADES: [number, string][] = [[5, 'только 5'], [4, '4 и 5'], [3, '3, 4 и 5'], [2, 'любая']]
const gradeRule = (min: number) => min >= 5 ? 'пятёркой' : `оценкой ${min} и выше`

function Choice<T extends string | number | boolean>({ label, value, options, onChange }: { label: string; value: T; options: [T, string][]; onChange: (value: T) => void }) {
  return <div className="period" role="group" aria-label={label}>
    {options.map(([key, title]) => <button key={String(key)} type="button" className={key === value ? 'active' : ''} aria-pressed={key === value} onClick={() => onChange(key)}>{title}</button>)}
  </div>
}

/** The settings of «Жребий»: on the settings tab and inside the panel. No limits, only defaults (the owner's wish). */
export function DrawSettingsForm({ request, initial, onSaved }: { request: Request; initial?: SettingsView; onSaved?: (value: SettingsView) => void }) {
  const [saved, setSaved] = useState<SettingsView | null>(initial ?? null)
  const [draft, setDraft] = useState<DrawSettings | null>(initial ?? null)
  const [busy, setBusy] = useState(false)
  const toast = useToast()
  useEffect(() => {
    if (initial) return
    request(() => api<SettingsView>('/admin/draw/settings')).then(v => { if (v) { setSaved(v); setDraft(v) } })
  }, [request, initial])
  if (!saved || !draft) return <div className="sk sk-card" />
  const { defaults } = saved
  const fields = (s: DrawSettings) => JSON.stringify({ ...s, defaults: undefined })
  const dirty = fields(draft) !== fields(saved)
  const set = <K extends keyof DrawSettings>(key: K, value: DrawSettings[K]) => setDraft(d => d && { ...d, [key]: value })
  const num = (key: 'spinSeconds' | 'eliminationSeconds' | 'topPercent', title: string, unit: string, hint: string, max?: number) =>
    <label className="setting-row" key={key}>
      <div><b>{title} <span className="muted">{unit}</span></b><small className="muted">{hint}</small></div>
      <div className="limit-input"><input type="number" min={0} max={max} step="any" value={draft[key]} onChange={e => set(key, Math.max(0, Number(e.target.value) || 0))} />
        <small className="muted">по умолчанию {decimal(defaults[key])}</small></div>
    </label>
  const whole = (key: 'winners' | 'minPoints' | 'bonus5' | 'bonus4' | 'bonus3', title: string, hint: string, min: number) =>
    <label className="setting-row" key={key}>
      <div><b>{title}</b><small className="muted">{hint}</small></div>
      <div className="limit-input"><input type="number" min={min} step={1} inputMode="numeric" value={draft[key]} onChange={e => set(key, Math.max(min, Math.floor(Number(e.target.value) || 0)))} />
        <small className="muted">по умолчанию {defaults[key]}</small></div>
    </label>
  async function save(e: FormEvent) {
    e.preventDefault(); if (!draft) return
    setBusy(true)
    const value = await request(() => api<SettingsView>('/admin/draw/settings', { method: 'PUT', body: JSON.stringify({ ...draft, defaults: undefined }) }))
    setBusy(false)
    if (!value) return
    setSaved(value); setDraft(value); onSaved?.(value)
    toast({ tone: 'info', icon: 'check', title: 'Настройки жребия сохранены', text: 'Применяются к следующему запуску' })
  }
  function testSound() { const s = new DrawSound(true, draft!.volume); s.unlock(); setTimeout(() => s.win(), 60) }

  return <form className="draw-settings" onSubmit={save} noValidate>
    <div className="setting-rows">
      <div className="setting-row"><div><b>Формат</b><small className="muted">«Стрелка» — победитель там, где остановилась стрелка. «Выбывание» — имя под стрелкой выбывает, пока не останутся победители.</small></div>
        <Choice label="Формат" value={draft.mode} options={MODES} onChange={v => set('mode', v)} /></div>
      {num('spinSeconds', 'Время прокрутки', 'с', 'Прокрутка, которая выбирает победителя, и решающее выбывание.')}
      {num('eliminationSeconds', 'Время одного выбывания', 'с', 'Только для «Выбывания»: все выбывания, кроме решающего.')}
      {whole('winners', 'Число победителей', 'Каждый победитель уходит с колеса, следующего выбирает новая прокрутка.', 1)}
      <div className="setting-row"><div><b>Следующая прокрутка</b><small className="muted">Вручную — каждую прокрутку запускаешь кнопкой. Сама — следующая начинается через секунду.</small></div>
        <Choice label="Следующая прокрутка" value={draft.autoNext} options={[[false, 'вручную'], [true, 'сама']]} onChange={v => set('autoNext', v)} /></div>
      {num('topPercent', 'Доля топа', '%', 'Сколько процентов пришедших и не вызванных к доске попадают на колесо по баллам за пару (с округлением вверх, при равенстве проходят все).', 100)}
      {whole('minPoints', 'Минимум баллов для топа', 'Меньше этого за пару — в топ не попадает.', 0)}
      <div className="setting-row"><div><b>Шансы</b><small className="muted">По баллам — шанс растёт с баллами за пару и бонусом за оценку у доски или на аттестации, сектор на колесе тем шире. В «Выбывании» наоборот: шире сектор у того, кто скорее выбудет.</small></div>
        <Choice label="Шансы" value={draft.chances} options={[['POINTS', 'по баллам'], ['EQUAL', 'равные']]} onChange={v => set('chances', v)} /></div>
      {draft.chances === 'POINTS' && <>
        {whole('bonus5', 'Бонус за 5', 'Сколько баллов к весу добавляет пятёрка у доски или на аттестации за эту пару.', 0)}
        {whole('bonus4', 'Бонус за 4', 'То же за четвёрку.', 0)}
        {whole('bonus3', 'Бонус за 3', 'То же за тройку.', 0)}
      </>}
      <div className="setting-row"><div><b>Оценка у доски</b><small className="muted">Какая оценка у доски или на аттестации на этой паре даёт место на колесе.</small></div>
        <Choice label="Оценка у доски" value={draft.boardMinGrade} options={GRADES} onChange={v => set('boardMinGrade', v)} /></div>
      <label className="setting-row"><div><b>Приз по умолчанию</b><small className="muted">Подставляется в панель жребия; перед запуском можно поменять.</small></div>
        <input className="draw-prize-input" type="text" value={draft.defaultPrize} placeholder={defaults.defaultPrize} onChange={e => set('defaultPrize', e.target.value)} /></label>
      <div className="setting-row"><div><b>Приз-сюрприз</b><small className="muted">На проекторе вместо приза «🎁 ???», пока не выявлены все победители.</small></div>
        <button type="button" role="switch" aria-checked={draft.surprisePrize} aria-label="Приз-сюрприз" className={`switch ${draft.surprisePrize ? 'on' : ''}`} onClick={() => set('surprisePrize', !draft.surprisePrize)}><span /></button></div>
      <div className="setting-row"><div><b>Звуки</b><small className="muted">Трещотка при вращении, «поп» на выбывании, фанфары на победу.</small></div>
        <button type="button" role="switch" aria-checked={draft.sound} aria-label="Звуки" className={`switch ${draft.sound ? 'on' : ''}`} onClick={() => set('sound', !draft.sound)}><span /></button></div>
      <label className="setting-row"><div><b>Громкость <span className="muted">{draft.volume}%</span></b></div>
        <div className="draw-volume"><input type="range" min={0} max={100} step={5} value={draft.volume} disabled={!draft.sound} onChange={e => set('volume', Number(e.target.value))} />
          <button type="button" className="ghost" disabled={!draft.sound} onClick={testSound}>Проверить</button></div></label>
    </div>
    <div className="pair-actions">
      <button className="primary" disabled={!dirty || busy}>{busy ? 'Сохраняем…' : 'Сохранить'}</button>
      <button type="button" className="ghost" onClick={() => setDraft({ ...defaults })}>Значения по умолчанию</button>
    </div>
  </form>
}

/** The settings tab block. */
export function DrawSettingsView({ request }: { request: Request }) {
  return <section className="analytics settings-page draw-settings-page">
    <div className="card enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="sparkle" size={16} /></span> Жребий</h2>
      <p className="muted small">Приз на паре: колесо из отличившихся у доски и лучших по задачам. Настройки общие для всех групп.</p>
      <DrawSettingsForm request={request} />
    </div>
  </section>
}

/** Teacher: who is on the wheel of a saved pair and why; names can be added or removed, then the wheel opens full screen. */
export function WheelPanel({ pair, request, onClose }: { pair: Pair; request: Request; onClose: () => void }) {
  const [wheel, setWheel] = useState<Wheel | null>(null)
  const [chosen, setChosen] = useState<Id[]>([])
  const [stage, setStage] = useState(false)
  const [prize, setPrize] = useState('')
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [deleting, setDeleting] = useState<Id | null>(null)
  const toast = useToast()

  const load = useCallback((keepChoice: boolean) => request(() => api<Wheel>(`/admin/pairs/${pair.id}/wheel`)).then(v => {
    if (!v) return
    setWheel(v); setPrize(p => keepChoice && p ? p : v.prize)
    if (!keepChoice) setChosen(v.candidates.map(c => c.userId))
  }), [pair.id, request])
  useEffect(() => { load(false) }, [load])

  if (!wheel) return <section className="card wheel-panel enter"><p className="muted">Собираем претендентов…</p></section>
  const everyone = [...wheel.candidates, ...wheel.called, ...wheel.others]
  const byId = new Map(everyone.map(p => [p.userId, p]))
  const added = [...wheel.called, ...wheel.others].filter(p => chosen.includes(p.userId))
  const addable = [...wheel.called, ...wheel.others].filter(p => !chosen.includes(p.userId))
  const toggle = (id: Id) => setChosen(c => c.includes(id) ? c.filter(x => x !== id) : [...c, id])
  const names = chosen.map(id => byId.get(id)).filter((p): p is Person => !!p)
  const prizeName = prize.trim().replace(/\s+/g, ' ') || wheel.settings.defaultPrize
  const s = wheel.settings
  const total = names.reduce((sum, p) => sum + Math.max(1, p.weight), 0)
  /** A chosen student's weight and, with the arrow, the chance to win the first spin. */
  const chance = (p: Person) => !chosen.includes(p.userId) || s.chances === 'EQUAL' ? null
    : `вес ${p.weight}${s.mode === 'ARROW' ? ` · шанс ${Math.round(Math.max(1, p.weight) * 100 / total)}%` : ''}`
  const updateRun = (run: Run) => setWheel(w => w && { ...w, runs: w.runs.some(r => r.id === run.id) ? w.runs.map(r => r.id === run.id ? run : r) : [...w.runs, run] })
  async function deleteRun(id: Id) {
    const value = await request(() => remove<{ runs: Run[] }>(`/admin/pairs/${pair.id}/wheel/runs/${id}`))
    setDeleting(null)
    if (value) { setWheel(w => w && { ...w, runs: value.runs }); toast({ tone: 'info', icon: 'x', title: 'Запуск жребия удалён' }) }
  }

  return <section className="card wheel-panel enter" aria-label="Жребий">
    <div className="chart-head">
      <div>
        <p className="eyebrow">Жребий</p>
        <h2 className="card-title">Кто крутится за приз</h2>
      </div>
      <button type="button" className="icon-button" aria-label="Закрыть" title="Закрыть" onClick={onClose}><Icon name="x" /></button>
    </div>
    <p className="muted small">На колесе: все с {gradeRule(wheel.boardMinGrade)} у доски за эту пару и топ‑{decimal(wheel.topPercent)}% по баллам за пару среди тех, кого не вызывали
      ({wheel.pool} {plural(wheel.pool, 'студент', 'студента', 'студентов')} → {wheel.topCount}{wheel.threshold !== null ? `, порог ${pts(wheel.threshold)}, при равенстве проходят все` : ', никто не проходит'}).
      На проекторе видны только имена и приз.</p>
    <p className="muted small draw-summary">
      {s.mode === 'ARROW' ? 'Стрелка' : 'Выбывание'} · {s.winners} {plural(s.winners, 'победитель', 'победителя', 'победителей')} · прокрутка {decimal(s.spinSeconds)} с
      {s.mode === 'ELIMINATION' ? `, выбывание ${decimal(s.eliminationSeconds)} с` : ''} · {s.autoNext ? 'следующая сама' : 'каждая прокрутка по кнопке'}
      {s.chances === 'POINTS' ? ` · шансы по баллам (+${s.bonus5}/${s.bonus4}/${s.bonus3} за 5/4/3)` : ' · равные шансы'}{s.surprisePrize ? ' · приз-сюрприз' : ''} · {s.sound ? `звук ${s.volume}%` : 'без звука'}
      <button type="button" className="row-link" onClick={() => setSettingsOpen(o => !o)}>{settingsOpen ? 'Скрыть настройки' : 'Настройки'}</button>
    </p>
    {settingsOpen && <div className="draw-settings-inline"><DrawSettingsForm request={request} initial={wheel.settings} onSaved={() => { load(true); setSettingsOpen(false) }} /></div>}
    <label className="wheel-add">Приз
      <input type="text" value={prize} placeholder={wheel.settings.defaultPrize} onChange={e => setPrize(e.target.value)} /></label>
    {!wheel.candidates.length && !added.length && <p className="muted">Пока никто не заработал место на колесе. Можно добавить студента вручную.</p>}
    <ul className="wheel-people">
      {[...wheel.candidates, ...added].map(p => <li key={p.userId}>
        <label><input type="checkbox" checked={chosen.includes(p.userId)} onChange={() => toggle(p.userId)} />
          <b>{p.displayName}</b> <small className="muted">{p.login}</small></label>
        <span className="wheel-person-tags">{chance(p) && <small className="muted tabular">{chance(p)}</small>}
          <span className={`pill ${p.reason === 'BOARD' ? 'wheel-board' : p.reason === 'TOP' ? 'wheel-top' : ''}`}>{p.reason ? reasonText(p) : `вручную · ${reasonText(p)}`}</span></span>
      </li>)}
    </ul>
    {addable.length > 0 && <label className="wheel-add">Добавить вручную
      <select value="" onChange={e => { const id = Number(e.target.value); if (id) setChosen(c => [...c, id]) }}>
        <option value="">Выбери студента…</option>
        {addable.map(p => <option key={p.userId} value={p.userId}>{p.displayName} — {reasonText(p)}</option>)}
      </select></label>}
    {wheel.runs.length > 0 && <div className="draw-history"><span className="control-label">Запуски этой пары</span>
      {wheel.runs.map(r => <div key={r.id} className="draw-run">
        <span className="pill wheel-winner-pill">{prizeIcon(r.prize)} {r.prize}</span>
        <span className="draw-run-winners">{r.wins.length ? r.wins.map(w => <span key={w.userId} className={w.absent ? 'absent' : ''} title={w.absent ? 'Не было на паре' : undefined}>{w.displayName}</span>) : <span className="muted">без победителя</span>}</span>
        <small className="muted">{time(r.createdAt)} · {r.mode === 'ARROW' ? 'стрелка' : 'выбывание'}{r.finished ? '' : ' · не завершён'}</small>
        {deleting === r.id ? <span className="draw-run-confirm">Удалить запуск?
          <button type="button" className="danger-solid" onClick={() => deleteRun(r.id)}>Удалить</button>
          <button type="button" className="ghost" onClick={() => setDeleting(null)}>Нет</button></span>
          : <button type="button" className="icon-button" aria-label="Удалить запуск" title="Удалить запуск" onClick={() => setDeleting(r.id)}><Icon name="x" size={16} /></button>}
      </div>)}</div>}
    <div className="pair-actions">
      <button type="button" className="primary" disabled={!names.length} onClick={() => setStage(true)}><Icon name="sparkle" size={16} /> Открыть колесо · {names.length}</button>
    </div>
    {stage && <WheelStage pairId={pair.id!} people={names} prize={prizeName} settings={wheel.settings} request={request} onRun={updateRun} onClose={() => setStage(false)} />}
  </section>
}

const COLORS = ['#5b3df5', '#ff6bd6', '#ffb224', '#10a067', '#2f6fde', '#ff6b2c', '#7cf2c8', '#c6f24e', '#e5484d', '#9b6dff']
const INK = new Set(['#ffb224', '#7cf2c8', '#c6f24e'])
/** A student's colour by place in the first wheel order, kept for the whole draw; the last skips the first one's colour. */
const colorOf = (i: number, n: number) => COLORS[(n > 1 && i === n - 1 && i % COLORS.length === 0 ? 1 : i) % COLORS.length]
/** Segments in proportion to the weights (or their inverse: the chance to drop out); start and size in degrees. */
function layout(ids: Id[], weightOf: (id: Id) => number, inverse: boolean) {
  const shares = ids.map(id => inverse ? 1 / weightOf(id) : weightOf(id)), total = shares.reduce((a, b) => a + b, 0) || 1
  const size = shares.map(x => x * 360 / total), start: number[] = []
  size.reduce((at, sz) => { start.push(at); return at + sz }, 0)
  return { start, size }
}
const C = 300, R = 290
/** Room for a name along the radius: from the rim's inner margin (22) to past the hub (r 34 + 14). */
const NAME_SPACE = R - 22 - 48
/** Pauses: how long a picked name stays on the wheel before it leaves; before an automatic next spin. */
const LEAVE_MS = 900, AUTO_NEXT_MS = 1200

function shuffle<T>(items: T[]) { const a = [...items]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1));[a[i], a[j]] = [a[j], a[i]] } return a }
const point = (deg: number, r = R) => { const a = deg * Math.PI / 180; return `${C + r * Math.sin(a)} ${C - r * Math.cos(a)}` }
const short = (name: string, max: number) => name.length <= max ? name : name.slice(0, max - 1) + '…'
/** A name too long for one large line goes on two (surname, then the rest), each at most 20 characters. */
function nameLines(name: string, fits: (lines: string[]) => boolean) {
  const words = name.trim().split(/\s+/), one = [short(name, 24)]
  return words.length < 2 || fits(one) ? one : [short(words[0], 20), short(words.slice(1).join(' '), 20)]
}
/** The rotation of an element now, in degrees, read from its computed transform (also during a CSS transition). */
function angleOf(el: Element) {
  const t = getComputedStyle(el).transform
  if (!t || t === 'none') return 0
  const m = new DOMMatrixReadOnly(t)
  return Math.atan2(m.b, m.a) * 180 / Math.PI
}

type Phase = 'ready' | 'spinning' | 'between' | 'done'

/**
 * The projected wheel: names and the prize only. Each spin is a step the server picks; the disc lands on it. ARROW: the
 * name under the arrow wins and leaves the wheel; ELIMINATION: it drops out until the winners are left. A winner not in
 * class is marked absent and a replacement is drawn.
 */
function WheelStage({ pairId, people, prize, settings, request, onRun, onClose }: {
  pairId: Id; people: Person[]; prize: string; settings: DrawSettings; request: Request; onRun: (run: Run) => void; onClose: () => void
}) {
  const names = useMemo(() => new Map(people.map(p => [p.userId, p.displayName])), [people])
  const [order] = useState<Id[]>(() => shuffle(people.map(p => p.userId)))
  const [wheelIds, setWheelIds] = useState<Id[]>(order)
  const colorIndex = useMemo(() => new Map(order.map((id, i) => [id, i])), [order])
  const colorFor = (id: Id) => colorOf(colorIndex.get(id) ?? 0, order.length)
  const weights = useMemo(() => new Map(people.map(p => [p.userId, Math.max(1, p.weight || 1)])), [people])
  const weightOf = useCallback((id: Id) => weights.get(id) ?? 1, [weights])
  const [run, setRun] = useState<Run | null>(null)
  const [rotation, setRotation] = useState(0)
  const [duration, setDuration] = useState(0)
  const [phase, setPhase] = useState<Phase>('ready')
  const [last, setLast] = useState<Step['pick']>(null)
  const [leaving, setLeaving] = useState<Id | null>(null)
  const [burst, setBurst] = useState(0)
  const [revealed, setRevealed] = useState(!settings.surprisePrize)
  const [full, setFull] = useState(false)
  const ref = useRef<HTMLDivElement>(null), disc = useRef<HTMLDivElement>(null)
  const pending = useRef<Step | null>(null), before = useRef<Id[]>([]), runRef = useRef<Run | null>(null), timer = useRef(0), alive = useRef(true), nextRef = useRef<() => void>(() => undefined)
  const sound = useMemo(() => new DrawSound(settings.sound, settings.volume), [settings.sound, settings.volume])
  const reduced = useMemo(() => window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false, [])

  useEffect(() => {
    alive.current = true
    ref.current?.requestFullscreen?.().catch(() => undefined)
    const key = (e: KeyboardEvent) => { if (e.key === 'Escape' && !document.fullscreenElement) close() }
    const fs = () => setFull(!!document.fullscreenElement)
    window.addEventListener('keydown', key); document.addEventListener('fullscreenchange', fs)
    return () => {
      alive.current = false; window.clearTimeout(timer.current)
      window.removeEventListener('keydown', key); document.removeEventListener('fullscreenchange', fs)
      if (document.fullscreenElement) document.exitFullscreen().catch(() => undefined)
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // The ratchet: a click whenever another segment passes the arrow while the disc turns.
  const n = wheelIds.length
  const inverse = (run?.mode ?? settings.mode) === 'ELIMINATION' && !run?.replacing
  const segs = useMemo(() => layout(wheelIds, weightOf, inverse), [wheelIds, weightOf, inverse])
  useEffect(() => {
    if (phase !== 'spinning' || !disc.current || reduced) return
    let frame = 0, lastIndex = -1
    const loop = () => {
      if (!disc.current) return
      const pointer = ((-angleOf(disc.current) % 360) + 360) % 360
      let index = segs.start.length - 1
      while (index > 0 && segs.start[index] > pointer) index--
      if (index !== lastIndex) { if (lastIndex !== -1) sound.tick(); lastIndex = index }
      frame = requestAnimationFrame(loop)
    }
    frame = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(frame)
  }, [phase, segs, sound, reduced])

  function close() { if (document.fullscreenElement) document.exitFullscreen().catch(() => undefined); onClose() }
  function enterFull() { ref.current?.requestFullscreen?.().catch(() => undefined) }
  const remember = (r: Run) => { runRef.current = r; setRun(r); onRun(r) }

  async function next() {
    if (phase === 'spinning') return
    sound.unlock(); window.clearTimeout(timer.current)
    setPhase('spinning'); setLast(null)
    let r = runRef.current
    if (!r) {
      const created = await request(() => post<{ run: Run }>(`/admin/pairs/${pairId}/wheel/runs`, { userIds: wheelIds, prize }))
      if (!created) { setPhase('ready'); return }
      r = created.run; remember(r)
    }
    const wheel = r.wheel
    before.current = wheel; setWheelIds(wheel)
    const step = await request(() => post<Step>(`/admin/pairs/${pairId}/wheel/runs/${r!.id}/step`))
    if (!alive.current) return
    if (!step) { setPhase(r.wins.length || r.outs.length ? 'between' : 'ready'); return }
    if (!step.pick) { pending.current = step; land(); return }
    const at = layout(wheel, weightOf, r.mode === 'ELIMINATION' && !r.replacing), index = wheel.indexOf(step.pick.userId)
    const size = at.size[index]
    const decisive = step.pick.kind === 'WIN' || step.won.length > 0
    const seconds = decisive ? settings.spinSeconds : settings.eliminationSeconds
    const target = at.start[index] + size * (0.5 + (Math.random() - 0.5) * 0.6)
    const now = ((rotation % 360) + 360) % 360
    const delta = ((360 - target - now) % 360 + 360) % 360
    const turns = Math.max(1, Math.round(seconds * 1.1))
    pending.current = step
    setDuration(reduced ? 0 : seconds * 1000)
    setRotation(rotation + 360 * turns + delta)
    if (reduced || seconds <= 0) land()
  }
  nextRef.current = next

  function land() {
    const step = pending.current
    if (!step) return
    pending.current = null
    setLast(step.pick)
    if (step.pick?.kind === 'OUT') sound.pop()
    if (step.won.length) { sound.win(); setBurst(b => b + 1) }
    if (step.pick) setLeaving(step.pick.userId)
    timer.current = window.setTimeout(() => {
      if (!alive.current) return
      setLeaving(null); remember(step.run)
      if (step.run.finished) {
        // The finished wheel keeps its winners (an elimination's survivors, the arrow's last pick) so the class sees them.
        const out = step.pick?.kind === 'OUT' ? step.pick.userId : null
        setWheelIds(before.current.filter(id => id !== out))
        setPhase('done')
        if (!revealed) { setRevealed(true); sound.reveal(); setBurst(b => b + 1) }
      } else {
        setWheelIds(step.run.wheel); setPhase('between')
        if (settings.autoNext) timer.current = window.setTimeout(() => { if (alive.current) nextRef.current() }, AUTO_NEXT_MS)
      }
    }, step.pick ? LEAVE_MS : 0)
  }

  async function absent(userId: Id) {
    const r = runRef.current
    if (!r) return
    const value = await request(() => post<{ run: Run }>(`/admin/pairs/${pairId}/wheel/runs/${r.id}/absent`, { userId }))
    if (!value) return
    remember(value.run); setWheelIds(value.run.wheel); setLast(null); setPhase(value.run.finished ? 'done' : 'between')
  }

  const winners = (run?.wins ?? []).filter(w => !w.absent)
  const winnerIds = new Set(winners.map(w => w.userId))
  const segClass = (id: Id) => leaving === id ? 'wheel-seg-leaving' : phase !== 'done' ? '' : winnerIds.has(id) ? 'wheel-seg-win' : 'wheel-seg-dim'
  const wanted = run?.winners ?? settings.winners
  const fontOf = (lines: string[], seg: number) => Math.max(11, Math.min(30, Math.floor(seg * 1.6 / lines.length), Math.floor(NAME_SPACE / (0.62 * Math.max(...lines.map(l => l.length), 4)))))
  const pickName = last ? names.get(last.userId) ?? '' : ''
  const message = !last ? null : last.kind === 'OUT' ? <>Выбывает: <b>{pickName}</b></>
    : <>{wanted > 1 ? `Победитель ${winners.length} из ${wanted}` : 'Победитель'}: <b>{pickName}</b></>
  const nextLabel = !run ? 'Крутить!' : run.replacing && !run.finished ? 'Крутить замену' : 'Крутить дальше'

  return <div ref={ref} className="wheel-stage" role="dialog" aria-modal="true" aria-label="Жребий">
    {!full && document.fullscreenEnabled && <button type="button" className="wheel-full" onClick={enterFull}>⛶ На весь экран</button>}
    <button type="button" className="wheel-close" aria-label="Закрыть колесо" onClick={close}><Icon name="x" size={22} /></button>
    <div className="wheel-head">
      <h2 className="wheel-title">Жребий <span>{revealed ? prizeIcon(prize) : '🎁'}</span></h2>
      <p className={`wheel-prize ${revealed && settings.surprisePrize ? 'revealed' : ''}`}>Разыгрываем: <b>{revealed ? prize : '???'}</b></p>
    </div>
    <div className="wheel-area">
      <div className="wheel-pointer" aria-hidden="true" />
      <div ref={disc} className="wheel-disc" style={{ transform: `rotate(${rotation}deg)`, transitionDuration: `${duration}ms` } as CSSProperties}
        onTransitionEnd={e => { if (e.target === disc.current) land() }}>
        <svg viewBox="0 0 600 600" role="img" aria-label={`На колесе ${n} ${plural(n, 'имя', 'имени', 'имён')}`}>
          {n === 1 ? <circle cx={C} cy={C} r={R} fill={colorFor(wheelIds[0])} className={segClass(wheelIds[0])} />
            : wheelIds.map((id, i) => { const a = segs.start[i], sz = segs.size[i]
              return <path key={`s${id}`} d={`M ${C} ${C} L ${point(a)} A ${R} ${R} 0 ${sz > 180 ? 1 : 0} 1 ${point(a + sz)} Z`}
                fill={colorFor(id)} stroke="#1b1830" strokeWidth="2" className={segClass(id)} /> })}
          {wheelIds.map((id, i) => {
            const sz = n === 1 ? 360 : segs.size[i], color = colorFor(id)
            const lines = nameLines(names.get(id) ?? '', one => fontOf(one, sz) >= 22), size = fontOf(lines, sz)
            return <g key={`n${id}`} transform={`rotate(${segs.start[i] + sz / 2 - 90} ${C} ${C})`} className={segClass(id) === 'wheel-seg-dim' ? 'wheel-seg-dim' : ''}>
              <text x={C + R - 22} y={C} textAnchor="end" dominantBaseline="middle" fontSize={size} fill={INK.has(color) ? '#15141a' : '#fff'} className="wheel-name">
                {lines.map((line, k) => <tspan key={k} x={C + R - 22} dy={k === 0 ? `${-(lines.length - 1) * 0.55}em` : '1.1em'}>{line}</tspan>)}</text>
            </g>
          })}
          <circle cx={C} cy={C} r={34} fill="#1b1830" stroke="#fff" strokeWidth="4" />
        </svg>
      </div>
    </div>
    <div className="wheel-bottom" aria-live="polite">
      <Burst trigger={burst} count={40} />
      {phase === 'done' ? <div className="wheel-result">
        {winners.length > 0 && <span className="wheel-result-label">{winners.length > 1 ? 'Приз получают' : 'Приз получает'}{revealed ? <> — <b className="wheel-result-prize">{prize}</b></> : ''}</span>}
        <div className="wheel-winners">{winners.map(w => <span key={w.userId} className="wheel-winner">
          <b className={`wheel-result-name ${winners.length > 1 ? 'small' : ''}`}>{w.displayName}</b>
          <button type="button" className="wheel-absent" onClick={() => absent(w.userId)} title="Победителя нет в аудитории: разыграть замену">Нет на паре</button>
        </span>)}</div>
        {!winners.length && <span className="wheel-result-label">Победителей не осталось</span>}
        <div className="wheel-buttons"><button type="button" className="primary" onClick={close}>Готово</button></div>
      </div> : <div className="wheel-progress">
        {message && <p className="wheel-message">{message}</p>}
        {winners.length > 0 && <p className="wheel-so-far">{winners.length > 1 ? 'Победители' : 'Победитель'}: {winners.map(w => w.displayName).join(', ')}</p>}
        {phase !== 'spinning' && <button type="button" className="primary wheel-spin" disabled={!n} onClick={next}>{nextLabel}</button>}
        {phase === 'between' && settings.autoNext && <small className="wheel-auto">Следующая прокрутка сейчас начнётся…</small>}
      </div>}
    </div>
  </div>
}
