import { CSSProperties, useEffect, useMemo, useRef, useState } from 'react'
import { api, post } from './api'
import { Burst, Icon } from './fx'
import { plural } from './session'
import type { Id, Pair } from './types'
import './wheel.css'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>
type Person = { userId: Id; login: string; displayName: string; attended: boolean; points: number; grade: string | null; reason?: 'BOARD' | 'TOP' }
type Spin = { id: Id; userId: Id; login: string; displayName: string; names: number; spunAt: string; prize: string }
type Wheel = { pairId: Id; topPercent: number; pool: number; topCount: number; threshold: number | null; candidates: Person[]; called: Person[]; others: Person[]; spins: Spin[]; prize: string }
type SpinResult = { winner: { userId: Id; login: string; displayName: string }; index: number; prize: string; spins: Spin[] }

const DEFAULT_PRIZE = 'Шоколадка'
const prizeIcon = (prize: string) => prize.toLowerCase().includes('шоколад') ? '🍫' : '🎁'

const time = (iso: string) => new Date(iso).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Moscow' })
const reasonText = (p: Person) => p.reason === 'BOARD' ? '5 у доски' : p.reason === 'TOP' ? `топ: ${p.points} ${plural(p.points, 'балл', 'балла', 'баллов')}`
  : p.grade ? `у доски: ${p.grade}` : !p.attended ? 'не был' : `${p.points} ${plural(p.points, 'балл', 'балла', 'баллов')}`

/** Teacher: who is on the wheel of a saved pair and why; names can be added or removed, then the wheel opens full screen. */
export function WheelPanel({ pair, request, onClose }: { pair: Pair; request: Request; onClose: () => void }) {
  const [wheel, setWheel] = useState<Wheel | null>(null)
  const [chosen, setChosen] = useState<Id[]>([])
  const [stage, setStage] = useState(false)
  /** The prize: the one of the latest spin, as the backend offers it; the teacher may rename it. */
  const [prize, setPrize] = useState('')

  useEffect(() => {
    let alive = true
    request(() => api<Wheel>(`/admin/pairs/${pair.id}/wheel`)).then(v => { if (alive && v) { setWheel(v); setChosen(v.candidates.map(c => c.userId)); setPrize(v.prize) } })
    return () => { alive = false }
  }, [pair.id, request])

  if (!wheel) return <section className="card wheel-panel enter"><p className="muted">Собираем претендентов…</p></section>
  const everyone = [...wheel.candidates, ...wheel.called, ...wheel.others]
  const byId = new Map(everyone.map(p => [p.userId, p]))
  const added = [...wheel.called, ...wheel.others].filter(p => chosen.includes(p.userId))
  const addable = [...wheel.called, ...wheel.others].filter(p => !chosen.includes(p.userId))
  const toggle = (id: Id) => setChosen(c => c.includes(id) ? c.filter(x => x !== id) : [...c, id])
  const names = chosen.map(id => byId.get(id)).filter((p): p is Person => !!p)
  const prizeName = prize.trim().replace(/\s+/g, ' ') || DEFAULT_PRIZE

  return <section className="card wheel-panel enter" aria-label="Жребий">
    <div className="chart-head">
      <div>
        <p className="eyebrow">Жребий</p>
        <h2 className="card-title">Кто крутится за приз</h2>
      </div>
      <button type="button" className="icon-button" aria-label="Закрыть" title="Закрыть" onClick={onClose}><Icon name="x" /></button>
    </div>
    <p className="muted small">На колесе: все с пятёркой у доски за эту пару и топ‑{wheel.topPercent}% по баллам за пару среди тех, кого не вызывали
      ({wheel.pool} {plural(wheel.pool, 'студент', 'студента', 'студентов')} → {wheel.topCount}{wheel.threshold !== null ? `, порог ${wheel.threshold} ${plural(wheel.threshold, 'балл', 'балла', 'баллов')}, при равенстве проходят все` : ', ни у кого нет баллов'}).
      На проекторе видны только имена и приз.</p>
    <label className="wheel-add">Приз
      <input type="text" value={prize} maxLength={60} placeholder={DEFAULT_PRIZE} onChange={e => setPrize(e.target.value)} /></label>
    {!wheel.candidates.length && !added.length && <p className="muted">Пока никто не заработал место на колесе. Можно добавить студента вручную.</p>}
    <ul className="wheel-people">
      {[...wheel.candidates, ...added].map(p => <li key={p.userId}>
        <label><input type="checkbox" checked={chosen.includes(p.userId)} onChange={() => toggle(p.userId)} />
          <b>{p.displayName}</b> <small className="muted">{p.login}</small></label>
        <span className={`pill ${p.reason === 'BOARD' ? 'wheel-board' : p.reason === 'TOP' ? 'wheel-top' : ''}`}>{p.reason ? reasonText(p) : `вручную · ${reasonText(p)}`}</span>
      </li>)}
    </ul>
    {addable.length > 0 && <label className="wheel-add">Добавить вручную
      <select value="" onChange={e => { const id = Number(e.target.value); if (id) setChosen(c => [...c, id]) }}>
        <option value="">Выбери студента…</option>
        {addable.map(p => <option key={p.userId} value={p.userId}>{p.displayName} — {reasonText(p)}</option>)}
      </select></label>}
    {wheel.spins.length > 0 && <div className="wheel-history"><span className="control-label">Победители этой пары</span>
      {wheel.spins.map(s => <span key={s.id} className="pill wheel-winner-pill">{prizeIcon(s.prize)} {s.displayName} · {s.prize} · {time(s.spunAt)}</span>)}</div>}
    <div className="pair-actions">
      <button type="button" className="primary" disabled={!names.length} onClick={() => setStage(true)}><Icon name="sparkle" size={16} /> Открыть колесо · {names.length}</button>
    </div>
    {stage && <WheelStage pairId={pair.id!} people={names} prize={prizeName} request={request}
      onSpun={spins => setWheel(w => w && { ...w, spins })} onClose={() => setStage(false)} />}
  </section>
}

const COLORS = ['#5b3df5', '#ff6bd6', '#ffb224', '#10a067', '#2f6fde', '#ff6b2c', '#7cf2c8', '#c6f24e', '#e5484d', '#9b6dff']
const INK = new Set(['#ffb224', '#7cf2c8', '#c6f24e'])
/** Neighbours never share a colour: the last segment skips the first one's. */
const colorOf = (i: number, n: number) => COLORS[(n > 1 && i === n - 1 && i % COLORS.length === 0 ? 1 : i) % COLORS.length]
const SPIN_MS = 6500
const C = 300, R = 290
/** Room for a name along the radius: from the rim's inner margin (22) to past the hub (r 34 + 14). */
const NAME_SPACE = R - 22 - 48

function shuffle<T>(items: T[]) { const a = [...items]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1));[a[i], a[j]] = [a[j], a[i]] } return a }
const point = (deg: number, r = R) => { const a = deg * Math.PI / 180; return `${C + r * Math.sin(a)} ${C - r * Math.cos(a)}` }
const short = (name: string, max: number) => name.length <= max ? name : name.slice(0, max - 1) + '…'
/** A name too long for one large line goes on two (surname, then the rest), each at most 20 characters. */
function nameLines(name: string, fits: (lines: string[]) => boolean) {
  const words = name.trim().split(/\s+/), one = [short(name, 24)]
  return words.length < 2 || fits(one) ? one : [short(words[0], 20), short(words.slice(1).join(' '), 20)]
}

/** The projected wheel: names and the prize only, the server picks the winner, the disc lands on it. «Ещё раз» spins without the winner. */
function WheelStage({ pairId, people, prize, request, onSpun, onClose }: { pairId: Id; people: Person[]; prize: string; request: Request; onSpun: (spins: Spin[]) => void; onClose: () => void }) {
  const [names, setNames] = useState(() => shuffle(people))
  const [rotation, setRotation] = useState(0)
  const [spinning, setSpinning] = useState(false)
  const [winner, setWinner] = useState<Person | null>(null)
  const [burst, setBurst] = useState(0)
  const ref = useRef<HTMLDivElement>(null)
  const pending = useRef<Person | null>(null)
  const reduced = useMemo(() => window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false, [])

  useEffect(() => {
    const el = ref.current
    el?.requestFullscreen?.().catch(() => undefined)
    const key = (e: KeyboardEvent) => { if (e.key === 'Escape') close() }
    window.addEventListener('keydown', key)
    return () => { window.removeEventListener('keydown', key); if (document.fullscreenElement) document.exitFullscreen().catch(() => undefined) }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  function close() { if (document.fullscreenElement) document.exitFullscreen().catch(() => undefined); onClose() }

  async function spin() {
    if (spinning || !names.length) return
    setWinner(null); setSpinning(true)
    const result = await request(() => post<SpinResult>(`/admin/pairs/${pairId}/wheel/spin`, { userIds: names.map(p => p.userId), prize }))
    if (!result) { setSpinning(false); return }
    onSpun(result.spins)
    const n = names.length, seg = 360 / n
    const target = (result.index + 0.5) * seg + (Math.random() - 0.5) * seg * 0.6
    const now = ((rotation % 360) + 360) % 360
    const delta = ((360 - target - now) % 360 + 360) % 360
    pending.current = names[result.index]
    setRotation(rotation + 360 * 7 + delta)
    if (reduced) land()
  }
  function land() {
    if (!pending.current) return
    setWinner(pending.current); pending.current = null; setSpinning(false); setBurst(b => b + 1)
  }
  function again() {
    if (!winner) return
    setNames(list => list.filter(p => p.userId !== winner.userId)); setWinner(null)
  }

  const n = names.length, seg = 360 / Math.max(n, 1)
  /** Per name: as large as the segment allows, but the name must fit between the hub and the rim (bold glyph ≈ 0.68 em). */
  const fontOf = (lines: string[]) => Math.max(11, Math.min(30, Math.floor(seg * 1.6 / lines.length),
    Math.floor(NAME_SPACE / (0.62 * Math.max(...lines.map(l => l.length), 4)))))
  return <div ref={ref} className="wheel-stage" role="dialog" aria-modal="true" aria-label="Жребий">
    <button type="button" className="wheel-close" aria-label="Закрыть колесо" onClick={close}><Icon name="x" size={22} /></button>
    <div className="wheel-head"><h2 className="wheel-title">Жребий <span>{prizeIcon(prize)}</span></h2><p className="wheel-prize">Разыгрываем: <b>{prize}</b></p></div>
    <div className="wheel-area">
      <div className="wheel-pointer" aria-hidden="true" />
      <div className="wheel-disc" style={{ transform: `rotate(${rotation}deg)`, transitionDuration: reduced ? '0ms' : `${SPIN_MS}ms` } as CSSProperties}
        onTransitionEnd={land}>
        <svg viewBox="0 0 600 600" role="img" aria-label={`На колесе ${n} ${plural(n, 'имя', 'имени', 'имён')}`}>
          {n === 1 ? <circle cx={C} cy={C} r={R} fill={COLORS[0]} />
            : names.map((p, i) => <path key={`s${p.userId}`} d={`M ${C} ${C} L ${point(i * seg)} A ${R} ${R} 0 ${seg > 180 ? 1 : 0} 1 ${point((i + 1) * seg)} Z`} fill={colorOf(i, n)} stroke="#1b1830" strokeWidth="2" />)}
          {names.map((p, i) => {
            const color = colorOf(i, n)
            return <g key={`n${p.userId}`} transform={`rotate(${(i + 0.5) * seg - 90} ${C} ${C})`}>
              {(() => {
                const lines = nameLines(p.displayName, one => fontOf(one) >= 22), size = fontOf(lines)
                return <text x={C + R - 22} y={C} textAnchor="end" dominantBaseline="middle" fontSize={size} fill={INK.has(color) ? '#15141a' : '#fff'} className="wheel-name">
                  {lines.map((line, k) => <tspan key={k} x={C + R - 22} dy={k === 0 ? `${-(lines.length - 1) * 0.55}em` : '1.1em'}>{line}</tspan>)}</text>
              })()}
            </g>
          })}
          <circle cx={C} cy={C} r={34} fill="#1b1830" stroke="#fff" strokeWidth="4" />
        </svg>
      </div>
    </div>
    <div className="wheel-bottom">
      {winner ? <div className="wheel-result" aria-live="polite">
        <Burst trigger={burst} count={40} />
        <span className="wheel-result-label">Приз «{prize}» получает</span>
        <b className="wheel-result-name">{winner.displayName}</b>
        <div className="wheel-buttons">
          {names.length > 1 && <button type="button" className="ghost" onClick={again} title="Если победителя нет в аудитории: колесо без него">Крутить ещё без него</button>}
          <button type="button" className="primary" onClick={close}>Готово</button>
        </div>
      </div>
        : <button type="button" className="primary wheel-spin" disabled={spinning || !n} onClick={spin}>{spinning ? 'Крутится…' : 'Крутить!'}</button>}
    </div>
  </div>
}
