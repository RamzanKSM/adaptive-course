import { useEffect, useRef } from 'react'
import { Icon } from './fx'
import { XP } from './game'

/** Hard mode frame: a pulsing red vignette and warning tape along the top. Purely decorative. */
export function DangerFrame() {
  return <div className="danger-frame" aria-hidden="true"><div className="danger-vignette" /><div className="danger-tape" /></div>
}

/** The student's switch in the header; shown only when the teacher allowed hard mode. */
export function HardModeSwitch({ on, busy, onToggle }: { on: boolean; busy: boolean; onToggle: () => void }) {
  return <button type="button" className={`hard-switch ${on ? 'on' : ''}`} role="switch" aria-checked={on} disabled={busy} onClick={onToggle}
    title={on ? 'Hard mode включён — выключить' : 'Включить hard mode'}>
    <Icon name="flame" size={16} /><span>{on ? 'HARD MODE' : 'Hard'}</span>
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
