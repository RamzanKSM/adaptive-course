import { KeyboardEvent, PointerEvent, ReactNode, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react'

/** A point of a line; `note` is extra text for the tooltip (e.g. the mean next to a median). */
export interface ChartPoint { x: number; y: number; note?: string }
/**
 * One line. Colours are CSS values (usually `var(--series-N)`); without one the line is a thin neutral member line.
 * faint — background line; sticky — always listed in the tooltip (median, pinned lines);
 * passive — not hoverable (reference projections); dot — marks the last point (also draws a one-point series).
 */
export interface ChartSeries {
  id: string; label: string; points: ChartPoint[]
  color?: string; width?: number; dash?: 'dashed' | 'dotted'
  faint?: boolean; sticky?: boolean; passive?: boolean; dot?: boolean
}
/** A reference line across the plot: vertical at x (`at` is an x value) or horizontal at y. */
export interface ChartRule { at: number; label?: string }

/** Categorical colours in fixed order: a group or a pinned student keeps its slot when others come and go. */
export const SERIES_COLORS = ['var(--series-1)', 'var(--series-2)', 'var(--series-3)', 'var(--series-4)', 'var(--series-5)', 'var(--series-6)', 'var(--series-7)', 'var(--series-8)']

const MARGIN = { top: 16, right: 14, bottom: 28 }
const NO_RULES: ChartRule[] = []
const DASH = { dashed: '7 5', dotted: '1.5 5' }
const HIT_PX = 16

/** Width of an element, kept current with a ResizeObserver (charts redraw for their real width). */
export function useWidth<T extends HTMLElement>() {
  const ref = useRef<T>(null)
  const [width, setWidth] = useState(0)
  useLayoutEffect(() => {
    const element = ref.current
    if (!element) return
    setWidth(Math.floor(element.getBoundingClientRect().width))
    const observer = new ResizeObserver(([entry]) => setWidth(Math.floor(entry.contentRect.width)))
    observer.observe(element)
    return () => observer.disconnect()
  }, [])
  return [ref, width] as const
}

/** The value of a line at x: exact, linearly interpolated between points, or null outside the line. */
export function valueAt(points: ChartPoint[], x: number): number | null {
  if (!points.length || x < points[0].x || x > points[points.length - 1].x) return null
  let lo = 0, hi = points.length - 1
  while (lo < hi) { const mid = (lo + hi) >> 1; if (points[mid].x < x) lo = mid + 1; else hi = mid }
  const p = points[lo]
  if (p.x === x || lo === 0) return p.y
  const q = points[lo - 1]
  return q.y + (p.y - q.y) * (x - q.x) / (p.x - q.x)
}
const pointAt = (points: ChartPoint[], x: number) => points.find(p => p.x === x)

/** «Nice» ticks covering [lo, hi]: steps of 1, 2, 5 × 10ⁿ (whole numbers only for counts). */
export function niceTicks(lo: number, hi: number, count = 4, integer = false) {
  const span = hi - lo || Math.abs(hi) || 1
  const raw = span / count
  const magnitude = 10 ** Math.floor(Math.log10(raw))
  const ratio = raw / magnitude
  let step = magnitude * (ratio >= 7.5 ? 10 : ratio >= 3.5 ? 5 : ratio >= 1.5 ? 2 : 1)
  if (integer) step = Math.max(1, Math.round(step))
  const start = Math.floor(lo / step) * step, end = Math.ceil(hi / step) * step
  const ticks: number[] = []
  for (let v = start; v <= end + step / 1e6; v += step) ticks.push(Math.round(v * 1e6) / 1e6)
  return ticks
}

/** X ticks in day-friendly steps, at most `max`: anchored at the right edge (dates end today) or at the left one (day 0). */
function xTicks(x0: number, x1: number, max: number, anchor: 'start' | 'end') {
  const span = x1 - x0
  const step = [1, 2, 7, 14, 28, 56, 91, 182, 364].find(s => span / s <= max) ?? Math.ceil(span / max)
  const ticks: number[] = []
  if (anchor === 'start') for (let x = x0; x <= x1 + 1e-9; x += step) ticks.push(x)
  else for (let x = x1; x >= x0 - 1e-9; x -= step) ticks.unshift(x)
  return ticks
}

/** A short stroke in the line's colour and dash: the key of a series in legends and tooltips. */
export function LineKey({ color, dash, bold }: { color?: string; dash?: ChartSeries['dash']; bold?: boolean }) {
  return <i className={`line-key ${dash ?? ''} ${bold ? 'bold' : ''}`} style={{ borderColor: color ?? 'var(--chart-line-strong)' }} aria-hidden="true" />
}

/**
 * A dependency-free responsive SVG line chart: several series (solid, dashed, dotted), a crosshair snapped to whole x values,
 * a tooltip (the hovered line plus the sticky ones, or every line with `tooltipAll`), a highlighted line (hover or `highlight`)
 * and reference rules. Keyboard: ←/→ move by one x (Shift — by 7), ↑/↓ go through the lines, Esc hides the tooltip.
 */
export function LineChart({ series, label, formatX, formatXTip, formatY, formatTick, height = 260, xDomain, yDomain, integer, xAnchor = 'end', highlight, onHover, tooltipAll, vRules = NO_RULES, hRules = NO_RULES, empty, className }: {
  series: ChartSeries[]; label: string; xAnchor?: 'start' | 'end'
  formatX: (x: number) => string; formatXTip?: (x: number) => string
  formatY: (y: number) => string; formatTick?: (y: number) => string
  height?: number; xDomain?: [number, number]; yDomain?: [number, number]; integer?: boolean
  highlight?: string | null; onHover?: (id: string | null) => void; tooltipAll?: boolean
  vRules?: ChartRule[]; hRules?: ChartRule[]; empty?: ReactNode; className?: string
}) {
  const [box, width] = useWidth<HTMLDivElement>()
  const [hover, setHover] = useState<{ x: number; id: string | null } | null>(null)
  const hoverId = hover?.id ?? null
  const reported = useRef<string | null>(null)
  useEffect(() => { if (reported.current !== hoverId) { reported.current = hoverId; onHover?.(hoverId) } }, [hoverId, onHover])

  const hasData = series.some(s => s.points.length)
  const geometry = useMemo(() => {
    // Loops rather than Math.min(...spread): a class over a whole course is tens of thousands of points.
    let minX = Infinity, maxX = -Infinity, lo = Math.min(0, yDomain?.[0] ?? 0), hi = yDomain?.[1] ?? 0
    for (const s of series) for (const p of s.points) { minX = Math.min(minX, p.x); maxX = Math.max(maxX, p.x); lo = Math.min(lo, p.y); hi = Math.max(hi, p.y) }
    for (const r of vRules) { minX = Math.min(minX, r.at); maxX = Math.max(maxX, r.at) }
    for (const r of hRules) { lo = Math.min(lo, r.at); hi = Math.max(hi, r.at) }
    let x0 = xDomain?.[0] ?? minX, x1 = xDomain?.[1] ?? maxX
    if (!Number.isFinite(x0) || !Number.isFinite(x1)) { x0 = 0; x1 = 1 }
    if (x1 <= x0) { x0 -= 1; x1 += 1 }
    if (hi <= lo) hi = lo + (integer ? 4 : 1)
    const ticks = niceTicks(lo, hi, height < 200 ? 3 : 4, integer)
    const tick = formatTick ?? formatY
    const left = Math.max(30, Math.max(...ticks.map(t => tick(t).length)) * 7 + 14)
    return { x0, x1, y0: ticks[0], y1: ticks[ticks.length - 1], ticks, left }
  }, [series, xDomain, yDomain, vRules, hRules, integer, height, formatTick, formatY])

  const { x0, x1, y0, y1, ticks, left } = geometry
  const plotW = Math.max(1, width - left - MARGIN.right), plotH = height - MARGIN.top - MARGIN.bottom
  const sx = (x: number) => left + ((x - x0) / (x1 - x0)) * plotW
  const sy = (y: number) => MARGIN.top + (1 - (y - y0) / (y1 - y0 || 1)) * plotH
  const path = (points: ChartPoint[]) => points.map((p, i) => `${i ? 'L' : 'M'}${sx(p.x).toFixed(1)},${sy(p.y).toFixed(1)}`).join('')
  const clampX = (x: number) => Math.min(Math.ceil(x1), Math.max(Math.floor(x0), x))
  const active = hoverId ?? highlight ?? null

  function locate(e: PointerEvent<SVGSVGElement>) {
    const rect = e.currentTarget.getBoundingClientRect()
    const px = e.clientX - rect.left, py = e.clientY - rect.top
    const x = clampX(Math.round(x0 + ((px - left) / plotW) * (x1 - x0)))
    let id: string | null = null, best = HIT_PX
    for (const s of series) {
      if (s.passive) continue
      const y = valueAt(s.points, x)
      if (y === null) continue
      const distance = Math.abs(sy(y) - py)
      if (distance < best) { best = distance; id = s.id }
    }
    setHover({ x, id })
  }
  function onKey(e: KeyboardEvent<HTMLDivElement>) {
    const current = hover ?? { x: clampX(Math.round(x1)), id: null }
    const step = e.shiftKey ? 7 : 1
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') setHover({ ...current, x: clampX(current.x + (e.key === 'ArrowLeft' ? -step : step)) })
    else if (e.key === 'Home' || e.key === 'End') setHover({ ...current, x: clampX(Math.round(e.key === 'Home' ? x0 : x1)) })
    else if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
      const lines = series.filter(s => !s.passive && valueAt(s.points, current.x) !== null)
        .sort((a, b) => (valueAt(b.points, current.x) ?? 0) - (valueAt(a.points, current.x) ?? 0))
      if (!lines.length) return
      const index = lines.findIndex(s => s.id === current.id)
      const next = e.key === 'ArrowDown' ? (index + 1) % lines.length : index <= 0 ? lines.length - 1 : index - 1
      setHover({ ...current, id: lines[next].id })
    } else if (e.key === 'Escape') { setHover(null); return } else return
    e.preventDefault()
  }

  const rows = hover ? series
    .filter(s => tooltipAll || s.sticky || s.id === active)
    .map(s => ({ s, y: valueAt(s.points, hover.x), note: pointAt(s.points, hover.x)?.note }))
    .filter((r): r is { s: ChartSeries; y: number; note: string | undefined } => r.y !== null)
    .sort((a, b) => tooltipAll ? b.y - a.y : Number(b.s.id === active) - Number(a.s.id === active))
    : []
  // Background lines first, the hovered or highlighted one on top of everything.
  const order = [...series].sort((a, b) => rank(a) - rank(b))
  function rank(s: ChartSeries) { return s.id === active ? 3 : s.sticky ? 2 : s.faint ? 0 : 1 }
  const maxTicks = Math.max(2, Math.floor(plotW / 72))
  const tipLeft = hover ? sx(hover.x) : 0

  return <div ref={box} className={`line-chart ${className ?? ''}`} style={{ height }} tabIndex={hasData ? 0 : -1} role="group"
    aria-label={`${label}. Стрелки влево и вправо — по дням, вверх и вниз — между линиями.`}
    onKeyDown={onKey} onFocus={() => setHover(h => h ?? { x: clampX(Math.round(x1)), id: highlight ?? null })} onBlur={() => setHover(null)}>
    {!hasData ? <div className="lc-empty">{empty ?? 'Нет данных за этот период'}</div> : width > 0 && <>
      <svg width={width} height={height} aria-hidden="true" onPointerMove={locate} onPointerDown={locate} onPointerLeave={() => setHover(null)}>
        {ticks.map(t => <g key={t}>
          <line className={t === 0 ? 'lc-base' : 'lc-grid'} x1={left} x2={left + plotW} y1={sy(t)} y2={sy(t)} />
          <text className="lc-tick" x={left - 8} y={sy(t)} dy="0.32em" textAnchor="end">{(formatTick ?? formatY)(t)}</text>
        </g>)}
        {xTicks(x0, x1, maxTicks, xAnchor).map(x => {
          const px = sx(x), anchor = px - left < 24 ? 'start' : left + plotW - px < 24 ? 'end' : 'middle'
          return <text key={x} className="lc-tick" x={px} y={height - 8} textAnchor={anchor}>{formatX(x)}</text>
        })}
        {hRules.map((r, i) => <g key={`h${i}`} className="lc-rule">
          <line x1={left} x2={left + plotW} y1={sy(r.at)} y2={sy(r.at)} />
          {r.label && <text x={left + 6} y={sy(r.at) + 14}>{r.label}</text>}
        </g>)}
        {vRules.filter(r => r.at >= x0 && r.at <= x1).map((r, i) => {
          const px = sx(r.at)
          return <g key={`v${i}`} className="lc-rule">
            <line x1={px} x2={px} y1={MARGIN.top} y2={MARGIN.top + plotH} />
            {r.label && <text x={px + (px > left + plotW - 60 ? -5 : 5)} y={MARGIN.top + 10} textAnchor={px > left + plotW - 60 ? 'end' : 'start'}>{r.label}</text>}
          </g>
        })}
        {order.map(s => {
          const on = s.id === active
          const color = s.color ?? (on ? 'var(--brand)' : 'var(--chart-line)')
          const dimmed = active !== null && !on && !s.sticky
          const last = s.points[s.points.length - 1]
          return <g key={s.id} className={`lc-series ${dimmed ? 'dimmed' : ''} ${s.faint ? 'faint' : ''}`}>
            {s.points.length > 1 && <path d={path(s.points)} style={{ stroke: color }} strokeWidth={on ? Math.max(2.75, (s.width ?? 1.5) + 1) : s.width ?? 1.5}
              strokeDasharray={s.dash ? DASH[s.dash] : undefined} />}
            {s.dot && last && <circle className="lc-dot" cx={sx(last.x)} cy={sy(last.y)} r={5} style={{ fill: color }} />}
          </g>
        })}
        {hover && <g>
          <line className="lc-cross" x1={sx(hover.x)} x2={sx(hover.x)} y1={MARGIN.top} y2={MARGIN.top + plotH} />
          {rows.map(r => <circle key={r.s.id} className="lc-dot" cx={sx(hover.x)} cy={sy(r.y)} r={4.5} style={{ fill: r.s.color ?? 'var(--brand)' }} />)}
        </g>}
      </svg>
      {hover && rows.length > 0 && <div className="lc-tip" role="status" aria-live="polite"
        style={tipLeft > width / 2 ? { right: width - tipLeft + 12 } : { left: tipLeft + 12 }}>
        <b>{(formatXTip ?? formatX)(hover.x)}</b>
        {rows.map(r => <span key={r.s.id}><LineKey color={r.s.color ?? 'var(--brand)'} dash={r.s.dash} /><strong>{formatY(r.y)}</strong>{r.s.label}{r.note && <small>{r.note}</small>}</span>)}
      </div>}
    </>}
  </div>
}
