import { createContext, CSSProperties, ReactNode, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'

const PATHS = {
  bolt: 'M13 2 3 14h9l-1 8 10-12h-9l1-8z',
  star: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
  flag: 'M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1zM4 22v-7',
  target: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z',
  award: 'M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12zM8.21 13.89 7 23l5-3 5 3-1.21-9.12',
  flame: 'M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z',
  sparkle: 'M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9zM19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z',
  compass: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM16.24 7.76l-2.12 6.36-6.36 2.12 2.12-6.36 6.36-2.12z',
  check: 'M20 6 9 17l-5-5',
  x: 'M18 6 6 18M6 6l12 12',
  lock: 'M5 11h14v10H5zM8 11V7a4 4 0 0 1 8 0v4',
  logout: 'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9',
  send: 'M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z',
  arrow: 'M5 12h14M12 5l7 7-7 7',
  back: 'M19 12H5M12 19l-7-7 7-7',
  play: 'M6 4l14 8-14 8V4z',
  book: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5v14zM4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5',
  chat: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z',
  code: 'M16 18l6-6-6-6M8 6l-6 6 6 6',
  terminal: 'M4 17l6-6-6-6M12 19h8',
  refresh: 'M21 12a9 9 0 1 1-2.64-6.36L21 8M21 3v5h-5',
  plus: 'M12 5v14M5 12h14',
  user: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z',
  chart: 'M3 3v18h18M7 15l4-4 3 3 5-6',
  globe: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z',
  crown: 'M2 18h20M3 7l4 5 5-7 5 7 4-5-2 11H5L3 7z',
}
export type Icon = keyof typeof PATHS

export function Icon({ name, size = 18, className }: { name: Icon; size?: number; className?: string }) {
  return <svg className={`icon ${className ?? ''}`} width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={PATHS[name]} /></svg>
}

const reducedMotion = () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

/** Animates a number towards its new value so XP and counters visibly "tick" when they change. */
export function useCountUp(value: number, duration = 700) {
  const [shown, setShown] = useState(value)
  const from = useRef(value)
  useEffect(() => {
    if (reducedMotion() || from.current === value) { from.current = value; setShown(value); return }
    const start = performance.now(), origin = from.current
    let frame = 0
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration), eased = 1 - Math.pow(1 - t, 3)
      setShown(Math.round(origin + (value - origin) * eased))
      if (t < 1) frame = requestAnimationFrame(tick); else from.current = value
    }
    frame = requestAnimationFrame(tick)
    return () => { cancelAnimationFrame(frame); from.current = value }
  }, [value, duration])
  return shown
}

const BURST_COLORS = ['var(--brand)', 'var(--lime)', 'var(--amber)', 'var(--success)', 'var(--brand-2)']

/** A short confetti burst from the element's centre. Re-runs whenever `trigger` changes; hidden for reduced motion. */
export function Burst({ trigger, count = 26 }: { trigger: number; count?: number }) {
  const pieces = useMemo(() => Array.from({ length: count }, (_, i) => {
    const angle = (Math.PI * 2 * i) / count + Math.random() * 0.4, distance = 70 + Math.random() * 90
    return { x: Math.cos(angle) * distance, y: Math.sin(angle) * distance - 40, r: Math.random() * 540 - 270, color: BURST_COLORS[i % BURST_COLORS.length], delay: Math.random() * 80, round: i % 3 === 0 }
  }), [trigger, count])
  if (!trigger) return null
  return <span className="burst" key={trigger} aria-hidden="true">{pieces.map((p, i) => <i key={i} className={p.round ? 'round' : ''} style={{ '--x': `${p.x}px`, '--y': `${p.y}px`, '--r': `${p.r}deg`, '--c': p.color, animationDelay: `${p.delay}ms` } as CSSProperties} />)}</span>
}

/** Circular progress used for the level badge. */
export function Ring({ value, size = 56, stroke = 6, children }: { value: number; size?: number; stroke?: number; children?: ReactNode }) {
  const radius = (size - stroke) / 2, length = 2 * Math.PI * radius
  return <div className="ring" style={{ width: size, height: size }}>
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
      <circle cx={size / 2} cy={size / 2} r={radius} strokeWidth={stroke} className="ring-track" />
      <circle cx={size / 2} cy={size / 2} r={radius} strokeWidth={stroke} className="ring-value" strokeDasharray={length} strokeDashoffset={length * (1 - Math.max(0, Math.min(1, value)))} />
    </svg>
    <div className="ring-label">{children}</div>
  </div>
}

type Toast = { id: number; title: string; text?: string; icon: Icon; tone: 'reward' | 'info' }
const ToastContext = createContext<(toast: Omit<Toast, 'id'>) => void>(() => {})
export const useToast = () => useContext(ToastContext)

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])
  const nextId = useRef(0)
  const push = useCallback((toast: Omit<Toast, 'id'>) => {
    const id = ++nextId.current
    setToasts(list => [...list.slice(-2), { ...toast, id }])
    setTimeout(() => setToasts(list => list.filter(t => t.id !== id)), 4200)
  }, [])
  return <ToastContext.Provider value={push}>
    {children}
    <div className="toasts" aria-live="polite">{toasts.map(t => <div key={t.id} className={`toast ${t.tone}`} role="status">
      <span className="toast-icon"><Icon name={t.icon} size={20} /></span>
      <span><b>{t.title}</b>{t.text && <small>{t.text}</small>}</span>
    </div>)}</div>
  </ToastContext.Provider>
}

export const initials = (name: string) => name.trim().split(/\s+/).slice(0, 2).map(part => part[0]?.toUpperCase() ?? '').join('') || '?'
