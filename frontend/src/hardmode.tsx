import { useEffect, useRef } from 'react'
import { Icon } from './fx'
import { XP } from './game'

const TAPE_TEXT = Array.from({ length: 14 }, () => 'Hard mode · опасная зона').join(' · ')
type Corner = 'tl' | 'tr' | 'bl' | 'br'
const Tapes = ({ corners }: { corners: Corner[] }) => <>{corners.map(corner => <div key={corner} className={`tape-corner ${corner}`}>
  <span className="tape a">{TAPE_TEXT}</span><span className="tape b">{TAPE_TEXT}</span>
</div>)}</>

/**
 * Hard mode decoration: a pulsing red frame around the window, and crossed warning tapes over the corners of the page —
 * at its top and at its end. The tapes belong to the page: they scroll (and spring back) with it, and both ends of each
 * tape run off the page's edges. They lie under the content, so they never cover cards or text.
 */
export function DangerFrame() {
  return <>
    <div className="danger-frame" aria-hidden="true"><div className="danger-vignette" /></div>
    <div className="danger-tapes" aria-hidden="true"><Tapes corners={['tl', 'tr', 'bl', 'br']} /></div>
  </>
}

/**
 * The top tapes again, inside the sticky header: over its backdrop but under its logo, switches and user chip. Shifted
 * by the page scroll (--scroll-y), so they match the page's tapes and leave with the page.
 */
export function HeaderTapes() {
  return <div className="header-tapes" aria-hidden="true"><div className="header-tapes-page"><Tapes corners={['tl', 'tr']} /></div></div>
}

/** The student's switch in the header; shown only when the teacher allowed hard mode.
 *  Locked until the current course has been passed once; a locked switch still reacts to clicks (explains why). */
export function HardModeSwitch({ on, locked, busy, onToggle }: { on: boolean; locked: boolean; busy: boolean; onToggle: () => void }) {
  return <button type="button" className={`hard-switch ${on ? 'on' : ''} ${locked ? 'locked' : ''}`} role="switch" aria-checked={on} disabled={busy} onClick={onToggle}
    title={locked ? 'Hard mode откроется после первого прохода курса' : on ? 'Hard mode включён — выключить' : 'Включить hard mode'}>
    <Icon name={locked ? 'lock' : 'flame'} size={16} /><span>{on ? 'HARD MODE' : 'Hard'}</span>
  </button>
}

/** Before switching on: what changes and that it is meant to be hard. */
export function HardModeDialog({ onConfirm, onCancel }: { onConfirm: () => void; onCancel: () => void }) {
  const confirmRef = useRef<HTMLButtonElement>(null)
  useEffect(() => {
    confirmRef.current?.focus()
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onCancel() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onCancel])
  return <div className="hard-dialog-backdrop" onClick={onCancel}>
    <div className="hard-dialog" role="dialog" aria-modal="true" aria-labelledby="hard-dialog-title" onClick={e => e.stopPropagation()}>
      <span className="hard-dialog-icon"><Icon name="flame" size={30} /></span>
      <p className="eyebrow">Только для тех, кто шарит</p>
      <h2 id="hard-dialog-title" className="display small">Будет жарко</h2>
      <ul>
        <li>Это режим для тех, кто уже прошёл весь курс хотя бы раз.</li>
        <li>Вместо обычных задач — алгоритмические: придётся думать, а не вспоминать синтаксис.</li>
        <li>Решение прогоняют на разных входных данных — подогнать под пример не выйдет.</li>
        <li>За каждую решённую задачу <b>+{XP.hardTask} XP</b> вместо {XP.task} и отдельные достижения.</li>
      </ul>
      <p className="muted small">Текущая задача останется, следующие будут hard. Выключить можно в любой момент.</p>
      <div className="hard-dialog-actions">
        <button className="ghost" onClick={onCancel}>Не сейчас</button>
        <button ref={confirmRef} className="danger big" onClick={onConfirm}><Icon name="flame" size={16} /> Включить hard mode</button>
      </div>
    </div>
  </div>
}
