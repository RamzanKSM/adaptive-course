import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { api, ApiError, post } from './api'
import { attestationMinutes, BoardTestScreen, canonical, clock, isAttestation, KIND, minutesOf, minutesText, ms, STATION_BOARD_API, useNow } from './board'
import { Icon, initials } from './fx'
import { plural } from './session'
import type { BoardStudentTest, Id, StationCall, StationCurrent } from './types'

const POLL_MS = 3_000, DONE_SECONDS = 8
const COURSE: Record<string, string> = { JAVA: 'Java', PYTHON: 'Python' }

/**
 * «Компьютер у доски»: a browser the teacher turned into the board station. Nobody is signed in here: it shows the active
 * calls, the called student presses «Начать тест» next to their name and takes the test on this screen; afterwards
 * «Тест сдан» and back to the calls. onGone — the station was switched off (401); onTeacherLogin — the usual login form.
 */
export function StationScreen({ onTeacherLogin, onGone }: { onTeacherLogin: () => void; onGone: () => void }) {
  const [current, setCurrent] = useState<StationCurrent | null>(null)
  const [failed, setFailed] = useState(false)
  const [done, setDone] = useState(false)
  const seq = useRef(0)
  const running = useRef<Id | null>(null)
  /** The running test was an attestation: «Работа сдана» instead of «Тест сдан». */
  const attestation = useRef(false)
  useEffect(() => {
    if (done) return
    let alive = true
    const tick = () => {
      const id = ++seq.current
      api<StationCurrent>('/station/current').then(value => { if (alive && id === seq.current) { setCurrent(value); setFailed(false) } },
        e => { if (!alive) return; if (e instanceof ApiError && e.status === 401) onGone(); else setFailed(true) })
    }
    tick()
    const timer = setInterval(tick, POLL_MS)
    return () => { alive = false; clearInterval(timer) }
  }, [done, onGone])
  // The running test disappeared (the teacher finished or removed it, the time ran out): it is over for this screen too.
  useEffect(() => {
    if (current?.test) { running.current = current.test.id; attestation.current = isAttestation(current.test) }
    else if (current && running.current !== null) { running.current = null; setDone(true) }
  }, [current])
  /** Drops the state and the responses on the way, so the finished test never comes back from an older poll. */
  const finished = useCallback(() => { running.current = null; seq.current++; setCurrent(null); setDone(true) }, [])
  const started = useCallback((test: BoardStudentTest) => { seq.current++; setCurrent(c => c && { ...c, test: { ...test, format: test.format ?? c.calls.find(call => call.id === test.id)?.format } }) }, [])

  if (done) return <StationDone attestation={attestation.current} onBack={() => setDone(false)} />
  if (current?.test) return <BoardTestScreen key={current.test.id} test={current.test} name={current.test.displayName ?? ''} onFinished={finished} endpoints={STATION_BOARD_API} />
  return <StationWaiting current={current} failed={failed} onStarted={started} onTeacherLogin={onTeacherLogin} />
}

function StationWaiting({ current, failed, onStarted, onTeacherLogin }: { current: StationCurrent | null; failed: boolean; onStarted: (test: BoardStudentTest) => void; onTeacherLogin: () => void }) {
  const offset = useMemo(() => { const server = ms(current?.now); return Number.isNaN(server) ? 0 : server - Date.now() }, [current?.now])
  const now = useNow() + offset
  const [confirm, setConfirm] = useState<StationCall | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const calls = current?.calls ?? []
  // A call that left the list (expired, cancelled, started elsewhere) closes its confirmation.
  useEffect(() => { if (confirm && current && !current.calls.some(c => c.id === confirm.id)) setConfirm(null) }, [current, confirm])
  async function start(call: StationCall) {
    setBusy(true); setError('')
    try { onStarted(await post<BoardStudentTest>(`/station/tests/${call.id}/start`)) }
    catch (e) { setError(e instanceof Error ? e.message : 'Не удалось начать тест'); setConfirm(null) }
    finally { setBusy(false) }
  }
  return <main className="board-screen station-screen">
    <header className="station-bar">
      <div className="brand"><span className="logo" aria-hidden="true">R</span><b>Rmzn Tutor</b></div>
      <span className="station-name">{current?.station.name ?? ''}</span>
      <button type="button" className="ghost small-button" onClick={onTeacherLogin}><Icon name="user" size={15} /> Войти как преподаватель</button>
    </header>
    <section className="station-body">
      <p className="eyebrow">Ответ у доски</p>
      <h1 className="display">Компьютер у доски</h1>
      {error && <p className="board-error" role="alert">{error}</p>}
      {failed && <p className="board-error" role="alert">Нет связи с сервером — пробуем снова…</p>}
      {!current ? <p className="loading-note"><span className="spinner" aria-hidden="true" /> Загружаем вызовы…</p>
        : !calls.length ? <div className="station-empty">
          <span className="board-call-icon"><Icon name="clock" size={30} /></span>
          <h2 className="title">Ждём вызова преподавателя</h2>
          <p>Когда преподаватель вызовет тебя к доске, здесь появится твоё имя и кнопка «Начать тест».</p>
        </div>
          : <ul className="station-calls" aria-label="Вызваны к доске">{calls.map(call => {
            const kinds = canonical(call.kinds), left = ms(call.expiresAt) - now, attest = isAttestation(call)
            return <li key={call.id} className="station-call">
              <span className="avatar" aria-hidden="true">{initials(call.displayName)}</span>
              <span className="station-call-meta">
                <b>{call.displayName}</b>
                <small>{[call.group, COURSE[call.language] ?? call.language].filter(Boolean).join(' · ')}</small>
                <small>{attest ? <><span className="attest-tag">аттестация</span> {KIND.code.title} · {minutesText(attestationMinutes(call.durationSeconds))}</>
                  : <>{kinds.map(k => KIND[k].title).join(' · ')} · {minutesText(minutesOf(kinds, call.durationSeconds))}</>}</small>
              </span>
              <span className={`board-countdown ${left < 60_000 ? 'low' : ''}`} title="Вызов действует ещё">
                <Icon name="clock" size={18} /><b className="tabular">{clock(left)}</b><small>{left > 0 ? 'вызов действует' : 'вызов истёк'}</small>
              </span>
              <button type="button" className="primary big" disabled={busy || left <= 0 || call.canStart === false} onClick={() => setConfirm(call)}>{attest ? 'Начать аттестацию' : 'Начать тест'} <Icon name="arrow" /></button>
            </li>
          })}</ul>}
    </section>
    {confirm && <div className="board-call-backdrop" role="dialog" aria-modal="true" aria-labelledby="station-confirm-title">
      <div className="board-call">
        <span className="board-call-icon"><Icon name="flag" size={30} /></span>
        <h2 id="station-confirm-title" className="display small">{confirm.displayName}, начинаем?</h2>
        <p>{isAttestation(confirm) ? `Аттестация: одна задача на ${minutesText(attestationMinutes(confirm.durationSeconds))}.`
          : `Тест на ${minutesText(minutesOf(canonical(confirm.kinds), confirm.durationSeconds))}: ${canonical(confirm.kinds).map(k => KIND[k].phrase).join(', ')}.`} Таймер запустится сразу.</p>
        <div className="board-confirm-actions">
          <button type="button" className="ghost big" disabled={busy} onClick={() => setConfirm(null)}>Это не я</button>
          <button type="button" className="primary big" disabled={busy} onClick={() => start(confirm)} autoFocus>{busy ? <><span className="spinner" aria-hidden="true" /> Начинаем…</> : <>{isAttestation(confirm) ? 'Начать аттестацию' : 'Начать тест'} <Icon name="arrow" /></>}</button>
        </div>
      </div>
    </div>}
  </main>
}

/** After the test: no grade here; back to the calls after a short countdown. */
function StationDone({ attestation, onBack }: { attestation: boolean; onBack: () => void }) {
  const [left, setLeft] = useState(DONE_SECONDS)
  useEffect(() => { const timer = setInterval(() => setLeft(s => Math.max(0, s - 1)), 1000); return () => clearInterval(timer) }, [])
  useEffect(() => { if (left === 0) onBack() }, [left, onBack])
  return <main className="board-screen board-done">
    <div className="board-done-card">
      <span className="board-done-icon"><Icon name="check" size={44} /></span>
      <h1 className="display">{attestation ? 'Работа сдана' : 'Тест сдан'}</h1>
      <p>{attestation ? 'Преподаватель посмотрит и поставит оценку.' : 'Преподаватель посмотрит ответы и скажет оценку.'}</p>
      <p className="board-done-count">К списку вызовов через <b className="tabular">{left}</b> {plural(left, 'секунду', 'секунды', 'секунд')}</p>
      <button type="button" className="ghost big" onClick={onBack}><Icon name="back" size={18} /> К списку вызовов</button>
    </div>
  </main>
}
