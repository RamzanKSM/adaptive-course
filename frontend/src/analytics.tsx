import { useEffect, useMemo, useState } from 'react'
import { api, download } from './api'
import { Icon, useToast } from './fx'
import { parseDate } from './game'
import { GroupFilter, groupCounts, inGroup, useGroupFilter } from './groups'
import type { LlmPurpose, LlmUsage } from './types'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>

const PERIODS = [7, 30, 90]
const PURPOSES: Record<LlmPurpose, string> = { CHAT: 'Ответы в чате', TASK: 'Генерация задач', EXPLANATION: 'Объяснения тем', TASK_REPAIR: 'Перепроверка старых задач', REVIEW: 'Проверка решений (LLM)' }
const EFFORTS: Record<string, string> = { minimal: 'минимальный', low: 'низкий', medium: 'средний', high: 'высокий', xhigh: 'очень высокий' }
const LANGUAGE_TITLES: Record<string, string> = { JAVA: 'Java', PYTHON: 'Python' }
const number = new Intl.NumberFormat('ru-RU')
const compact = new Intl.NumberFormat('ru-RU', { notation: 'compact', maximumFractionDigits: 1 })
const seconds = (ms: number) => ms < 1000 ? `${Math.round(ms)} мс` : `${(ms / 1000).toLocaleString('ru-RU', { maximumFractionDigits: 1 })} с`
const when = (value?: string) => value ? parseDate(value).toLocaleString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—'
const percent = (part: number, whole: number) => whole ? `${Math.round((part / whole) * 100)}%` : '0%'

/** UTC calendar days of the period, oldest first, so days without calls still get an (empty) column. */
function periodDays(days: number) {
  const today = new Date()
  return Array.from({ length: days }, (_, i) => {
    const d = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate() - (days - 1 - i)))
    return d.toISOString().slice(0, 10)
  })
}
const dayLabel = (day: string) => new Date(`${day}T00:00:00Z`).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', timeZone: 'UTC' })

export function LlmAnalytics({ request }: { request: Request }) {
  const [days, setDays] = useState(30)
  const [usage, setUsage] = useState<LlmUsage | null>(null)
  const [loading, setLoading] = useState(true)
  const [group, setGroup] = useGroupFilter('rmzn-analytics-group', usage ? [...new Set(usage.byStudent.map(s => s.groupName).filter((g): g is string => !!g))] : null)
  useEffect(() => {
    let alive = true
    setLoading(true)
    request(() => api<LlmUsage>(`/admin/llm/usage?days=${days}`)).then(value => { if (alive) { if (value) setUsage(value); setLoading(false) } })
    return () => { alive = false }
  }, [days, request])

  const t = usage?.totals
  return <section className="analytics">
    <div className="analytics-head enter">
      <div>
        <p className="eyebrow">Преподаватель</p>
        <h1 className="display small">Аналитика LLM</h1>
        {usage && <p className="muted small">{usage.llm.globallyEnabled ? 'LLM включена' : 'LLM сейчас выключена'}{usage.llm.model ? ` · модель ${usage.llm.model}` : ''}</p>}
      </div>
      <div className="period" role="group" aria-label="Период">
        {PERIODS.map(p => <button key={p} className={p === days ? 'active' : ''} aria-pressed={p === days} onClick={() => setDays(p)}>{p} дн.</button>)}
      </div>
    </div>
    {!usage || !t ? <div className="sk sk-card" />
      : <div className={loading ? 'is-refreshing' : ''}>
        <div className="stat-grid">
          <Tile icon="sparkle" label="Обращений к LLM" value={number.format(t.calls)} note={`${t.students} ${plural(t.students, 'студент', 'студента', 'студентов')}`} />
          <Tile icon="x" label="Ошибки" value={number.format(t.errors)} note={`${percent(t.errors, t.calls)} обращений${t.timeouts ? ` · таймаутов: ${t.timeouts}` : ''}`} tone={t.errors ? 'warn' : undefined} />
          <Tile icon="bolt" label="Время ответа" value={seconds(t.avgMs)} note={`в среднем · 95% быстрее ${seconds(t.p95Ms)}`} />
          <Tile icon="chart" label="Токены" value={t.callsWithTokens ? compact.format(t.totalTokens) : '—'}
            note={t.callsWithTokens ? `вход ${compact.format(t.inputTokens)} (кэш ${compact.format(t.cachedTokens)}) · выход ${compact.format(t.outputTokens)}` : 'App Server ещё не сообщал о токенах'} />
        </div>
        {t.calls === 0 ? <div className="card empty-task"><span className="empty-icon"><Icon name="chart" size={26} /></span><p className="muted">За этот период к LLM не обращались.</p></div> : <>
          <DailyChart usage={usage} />
          <div className="analytics-grid">
            <div className="card">
              <h2 className="card-title">Для чего используется</h2>
              <table className="data-table"><thead><tr><th>Назначение</th><th>Модель</th><th>Размышления</th><th>Вызовы</th><th>Ошибки</th><th>Ср. время</th><th>Токены</th></tr></thead>
                <tbody>{usage.byPurpose.map(p => <tr key={p.purpose}><td>{PURPOSES[p.purpose] ?? p.purpose}</td><td>{p.model ?? '—'}</td><td>{p.effort ? EFFORTS[p.effort] ?? p.effort : '—'}</td><td>{number.format(p.calls)}</td><td>{p.errors ? number.format(p.errors) : '—'}</td><td>{seconds(p.avgMs)}</td><td>{p.tokens ? compact.format(p.tokens) : '—'}</td></tr>)}</tbody>
              </table>
              {(t.tasksAccepted + t.tasksRejected) > 0 && <p className="muted small table-note">Сгенерированные задачи: принято {t.tasksAccepted}, отклонено проверкой {t.tasksRejected} ({percent(t.tasksRejected, t.tasksAccepted + t.tasksRejected)}).</p>}
              {usage.byLanguage.length > 0 && <p className="muted small table-note">По курсам: {usage.byLanguage.map(l => `${LANGUAGE_TITLES[l.language] ?? l.language} — ${number.format(l.calls)}`).join(' · ')}</p>}
            </div>
            <div className="card">
              <h2 className="card-title">Ошибки</h2>
              {usage.recentErrors.length ? <ul className="error-list">{usage.recentErrors.map((e, i) => <li key={i}>
                <span className={`status-pill ${e.status === 'TIMEOUT' ? 'timeout' : 'error'}`}>{e.status === 'TIMEOUT' ? 'Таймаут' : 'Ошибка'}</span>
                <div><b>{PURPOSES[e.purpose] ?? e.purpose}</b> · {LANGUAGE_TITLES[e.language] ?? e.language}{e.displayName ? ` · ${e.displayName}` : ''}<small>{when(e.createdAt)} · {seconds(e.durationMs)}</small>{e.error && <code>{e.error}</code>}</div>
              </li>)}</ul> : <p className="muted small">Ошибок за период не было.</p>}
            </div>
          </div>
          <div className="card">
            <h2 className="card-title">Студенты</h2>
            {(() => { const counts = groupCounts(usage.byStudent.filter(s => s.userId !== null), s => s.groupName)
              return <GroupFilter total={usage.byStudent.filter(s => s.userId !== null).length} groups={counts.groups} ungrouped={counts.ungrouped} value={group} onChange={setGroup} /> })()}
            <div className="table-scroll"><table className="data-table">
              <thead><tr><th>Студент</th><th>Обращений</th><th>Из них в чате</th><th>Токены</th><th>Ошибки</th><th>Последнее</th></tr></thead>
              <tbody>{usage.byStudent.filter(s => group === '' || (s.userId !== null && inGroup(group, s.groupName))).map(s => <tr key={String(s.userId)}><td><b>{s.displayName}</b>{s.login && <small className="muted"> {s.login}</small>}{s.groupName && <span className="group-tag">{s.groupName}</span>}</td><td>{number.format(s.calls)}</td><td>{number.format(s.chatTurns)}</td><td>{s.tokens ? compact.format(s.tokens) : '—'}</td><td>{s.errors || '—'}</td><td>{when(s.lastAt)}</td></tr>)}</tbody>
            </table></div>
            <p className="muted small table-note">Генерация задач и объяснений записывается на студента, который её запустил, хотя результат потом достаётся всем.</p>
          </div>
        </>}
      </div>}
    <TaskExport request={request} />
  </section>
}

const EXPORT_LANGUAGES = [['ALL', 'Все'], ['JAVA', 'Java'], ['PYTHON', 'Python']] as const

/** The whole task bank with its topics as CSV, to hand to an assistant that reviews the order of topics and tasks. */
function TaskExport({ request }: { request: Request }) {
  const [language, setLanguage] = useState<typeof EXPORT_LANGUAGES[number][0]>('ALL')
  const [busy, setBusy] = useState(false)
  const toast = useToast()
  async function save() {
    setBusy(true)
    const fallback = `rmzn-tasks-${language.toLowerCase()}.csv`
    const name = await request(() => download(`/admin/tasks/export?language=${language}`, fallback))
    setBusy(false)
    if (name) toast({ tone: 'info', icon: 'download', title: 'Задачи выгружены', text: name })
  }
  return <div className="card task-export">
    <div>
      <h2 className="card-title">Темы и задачи</h2>
      <p className="muted small">Все темы курса и задачи к ним в CSV (для Excel): ступень, режим, условие, заготовка, нужные конструкции и где задача требует то, что ещё не пройдено. Файл можно отдать ИИ-ассистенту, чтобы проверить порядок тем и задач.</p>
    </div>
    <div className="task-export-actions">
      <div className="period" role="group" aria-label="Курс">
        {EXPORT_LANGUAGES.map(([value, title]) => <button key={value} type="button" className={value === language ? 'active' : ''} aria-pressed={value === language} disabled={busy} onClick={() => setLanguage(value)}>{title}</button>)}
      </div>
      <button type="button" className="primary" disabled={busy} onClick={save}>{busy ? <><span className="spinner" aria-hidden="true" /> Готовим файл…</> : <><Icon name="download" size={16} /> Выгрузить задачи (CSV)</>}</button>
    </div>
  </div>
}

function plural(n: number, one: string, few: string, many: string) {
  const mod10 = n % 10, mod100 = n % 100
  return mod10 === 1 && mod100 !== 11 ? one : mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14) ? few : many
}

function Tile({ icon, label, value, note, tone }: { icon: Parameters<typeof Icon>[0]['name']; label: string; value: string; note: string; tone?: 'warn' }) {
  return <div className={`card stat ${tone === 'warn' ? 'warn' : ''}`}>
    <span className="chip-icon"><Icon name={icon} size={18} /></span>
    <b className="tabular">{value}</b>
    <span className="muted small">{label}</span>
    <span className="stat-note">{note}</span>
  </div>
}

/** Calls per day: successful calls in the brand colour, errors stacked on top in the status red. */
function DailyChart({ usage }: { usage: LlmUsage }) {
  const [hover, setHover] = useState<number | null>(null)
  const [asTable, setAsTable] = useState(false)
  const rows = useMemo(() => {
    const byDay = new Map(usage.byDay.map(d => [d.day, d]))
    return periodDays(usage.days).map(day => ({ day, calls: byDay.get(day)?.calls ?? 0, errors: byDay.get(day)?.errors ?? 0, tokens: byDay.get(day)?.tokens ?? 0 }))
  }, [usage])
  const max = Math.max(1, ...rows.map(r => r.calls))
  const ticks = [max, Math.round(max / 2), 0].filter((v, i, a) => a.indexOf(v) === i)
  const active = hover === null ? null : rows[hover]
  return <div className="card chart-card">
    <div className="chart-head">
      <h2 className="card-title">Обращения по дням</h2>
      <div className="legend"><span><i className="swatch ok" />Успешные</span><span><i className="swatch err" />Ошибки</span>
        <button className="link" onClick={() => setAsTable(v => !v)}>{asTable ? 'Показать график' : 'Показать таблицей'}</button></div>
    </div>
    {asTable ? <div className="table-scroll"><table className="data-table">
      <thead><tr><th>День (UTC)</th><th>Обращений</th><th>Ошибок</th><th>Токенов</th></tr></thead>
      <tbody>{rows.filter(r => r.calls).map(r => <tr key={r.day}><td>{dayLabel(r.day)}</td><td>{r.calls}</td><td>{r.errors || '—'}</td><td>{r.tokens ? compact.format(r.tokens) : '—'}</td></tr>)}</tbody>
    </table></div> : <div className="chart">
      <div className="chart-y" aria-hidden="true">{ticks.map(v => <span key={v} style={{ bottom: `${(v / max) * 100}%` }}>{compact.format(v)}</span>)}</div>
      <div className="chart-plot" onMouseLeave={() => setHover(null)}>
        {ticks.map(v => <i key={v} className="gridline" style={{ bottom: `${(v / max) * 100}%` }} />)}
        <div className="bars" style={{ gridTemplateColumns: `repeat(${rows.length}, minmax(0, 1fr))` }}>
          {rows.map((r, i) => <button key={r.day} className={`bar-col ${hover === i ? 'hover' : ''}`} onMouseEnter={() => setHover(i)} onFocus={() => setHover(i)} onBlur={() => setHover(null)}
            aria-label={`${dayLabel(r.day)}: ${r.calls} обращений, ошибок ${r.errors}`}>
            {r.calls > 0 && <span className="stack" style={{ height: `${(r.calls / max) * 100}%` }}>
              {r.errors > 0 && <span className="seg err" style={{ flexGrow: r.errors }} />}
              {r.calls - r.errors > 0 && <span className="seg ok" style={{ flexGrow: r.calls - r.errors }} />}
            </span>}
          </button>)}
        </div>
        {active && hover !== null && <div className="chart-tip" style={{ left: `${Math.min(88, Math.max(12, ((hover + 0.5) / rows.length) * 100))}%` }} role="status">
          <b>{dayLabel(active.day)}</b>
          <span><i className="swatch ok" />Успешных: {active.calls - active.errors}</span>
          <span><i className="swatch err" />Ошибок: {active.errors}</span>
          {active.tokens > 0 && <span>Токенов: {compact.format(active.tokens)}</span>}
        </div>}
      </div>
      <div className="chart-x" aria-hidden="true"><span>{dayLabel(rows[0].day)}</span><span>{dayLabel(rows[Math.floor(rows.length / 2)].day)}</span><span>{dayLabel(rows[rows.length - 1].day)}</span></div>
    </div>}
  </div>
}
