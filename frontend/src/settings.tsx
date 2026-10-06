import { FormEvent, useEffect, useState } from 'react'
import { api } from './api'
import { Icon, useToast } from './fx'
import type { LlmLimits, LlmModel, LlmSettings } from './types'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>
type Draft = Pick<LlmSettings, 'model' | 'reasoning' | 'limits'>

const PURPOSES: { key: keyof LlmSettings['reasoning']; title: string; hint: string }[] = [
  { key: 'CHAT', title: 'Ответы помощника в чате', hint: 'Студент ждёт ответа — ниже уровень, быстрее ответ.' },
  { key: 'TASK', title: 'Генерация и перепроверка задач', hint: 'Нужны точные проверки и неверные примеры решений — выше уровень, меньше брака.' },
  { key: 'EXPLANATION', title: 'Объяснения тем', hint: 'Пишутся один раз на тему и потом переиспользуются.' },
]
const EFFORT_TITLES: Record<string, string> = { none: 'нет', minimal: 'минимальный', low: 'низкий', medium: 'средний', high: 'высокий', xhigh: 'очень высокий', max: 'максимальный', ultra: 'ультра' }
type LimitField = { key: keyof LlmLimits; title: string; unit: string; hint: string }
const CHAT_LIMITS: LimitField[] = [
  { key: 'chatPerHour', title: 'Сообщений на студента', unit: 'в час', hint: 'Скользящее окно: последние 60 минут.' },
  { key: 'chatPerDay', title: 'Сообщений на студента', unit: 'в сутки', hint: 'Скользящее окно: последние 24 часа.' },
]
const GENERATION_LIMITS: LimitField[] = [
  { key: 'tasksPerHour', title: 'Генераций задач на весь курс', unit: 'в час', hint: 'Новые задачи и перепроверка старых. При исчерпании студенты получают готовые задачи из банка.' },
  { key: 'explanationsPerHour', title: 'Генераций объяснений тем на весь курс', unit: 'в час', hint: 'Объяснение пишется один раз на тему. При исчерпании урок идёт без объяснения, пока лимит не освободится.' },
]

/** Levels of the chosen model; when the list is unknown, the server's fallback set. */
function effortsFor(settings: LlmSettings, model: string) {
  const found = settings.models.find(m => m.id === model)
  return found?.efforts.length ? found.efforts : settings.reasoningOptions
}
/** A level the new model does not support becomes its default (or the middle one it offers). */
function adjustToModel(reasoning: LlmSettings['reasoning'], model: LlmModel | undefined): LlmSettings['reasoning'] {
  if (!model?.efforts.length) return reasoning
  const fallback = model.efforts.includes(model.defaultEffort) ? model.defaultEffort : model.efforts[Math.floor(model.efforts.length / 2)]
  const next = { ...reasoning }
  for (const key of Object.keys(next) as (keyof typeof next)[]) if (!model.efforts.includes(next[key])) next[key] = fallback
  return next
}

export function LlmSettingsView({ request }: { request: Request }) {
  const [settings, setSettings] = useState<LlmSettings | null>(null)
  const [draft, setDraft] = useState<Draft | null>(null)
  const [saving, setSaving] = useState(false)
  const toast = useToast()
  const load = (value: LlmSettings) => { setSettings(value); setDraft({ model: value.model, reasoning: { ...value.reasoning }, limits: { ...value.limits } }) }
  useEffect(() => { request(() => api<LlmSettings>('/admin/llm/settings')).then(value => { if (value) load(value) }) }, [request])
  if (!settings || !draft) return <section className="analytics"><div className="sk sk-card" /></section>

  const dirty = JSON.stringify(draft) !== JSON.stringify({ model: settings.model, reasoning: settings.reasoning, limits: settings.limits })
  async function save(e: FormEvent) {
    e.preventDefault(); setSaving(true)
    const value = await request(() => api<LlmSettings>('/admin/llm/settings', { method: 'PUT', body: JSON.stringify(draft) }))
    setSaving(false)
    if (value) { load(value); toast({ tone: 'info', icon: 'check', title: 'Настройки LLM сохранены', text: 'Применяются к следующим обращениям, в том числе в уже начатых чатах' }) }
  }
  const chooseModel = (id: string) => setDraft(d => d && { ...d, model: id, reasoning: adjustToModel(d.reasoning, settings.models.find(m => m.id === id)) })
  const resetToDefaults = () => setDraft(() => ({ model: settings.models.some(m => m.id === settings.modelDefault) ? settings.modelDefault : settings.model, reasoning: { ...settings.reasoningDefaults }, limits: { ...settings.limitDefaults } }))
  const options = effortsFor(settings, draft.model)
  const limitRow = (l: LimitField) => <label key={l.key} className="setting-row">
    <div><b>{l.title} <span className="muted">{l.unit}</span></b><small className="muted">{l.hint}</small></div>
    <div className="limit-input">
      <input type="number" min={0} max={10000} step={1} inputMode="numeric" value={draft.limits[l.key]}
        onChange={e => { const value = Math.max(0, Math.floor(Number(e.target.value) || 0)); setDraft(d => d && { ...d, limits: { ...d.limits, [l.key]: value } }) }} />
      <small className="muted">по умолчанию {settings.limitDefaults[l.key] || 'без ограничения'}</small>
    </div>
  </label>
  const usage = (used: number, limit: number) => `${used}${limit ? ` из ${limit}` : ''}`

  return <form className="analytics settings-page" onSubmit={save}>
    <div className="analytics-head enter">
      <div>
        <p className="eyebrow">Преподаватель</p>
        <h1 className="display small">Настройки LLM</h1>
        <p className="muted small">Изменения применяются к следующим обращениям, без перезапуска.</p>
      </div>
      <div className="settings-actions">
        <button type="button" className="ghost" onClick={resetToDefaults}>Значения по умолчанию</button>
        <button className="primary" disabled={!dirty || saving}>{saving ? 'Сохраняем…' : 'Сохранить'}</button>
      </div>
    </div>

    <div className="card enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="bolt" size={16} /></span> Модель</h2>
      {settings.models.length ? <>
        <p className="muted small">Модель меняется для всех обращений сразу — и в новых, и в уже начатых чатах студентов.{!settings.models.some(m => m.listed) && ' Список моделей App Server сейчас недоступен — показаны текущая модель и модели из настроек сервера.'}</p>
        <div className="model-grid" role="radiogroup" aria-label="Модель">{settings.models.map(m => <button type="button" key={m.id} role="radio" aria-checked={draft.model === m.id}
          className={`model-card ${draft.model === m.id ? 'active' : ''}`} onClick={() => chooseModel(m.id)}>
          <b>{m.displayName}{m.id === settings.modelDefault && <span className="model-tag">по умолчанию</span>}{!m.listed && <span className="model-tag warn" title="App Server не сообщил об этой модели: проверьте, что аккаунт Codex имеет к ней доступ. Уровни размышлений — базовые.">не подтверждена App Server</span>}</b>
          <code>{m.id}</code>
          {m.description && <small className="muted">{m.description}</small>}
          {m.efforts.length > 0 && <small className="muted">Размышления: {m.efforts.map(e => EFFORT_TITLES[e] ?? e).join(', ')}</small>}
        </button>)}</div>
      </> : <p className="muted small">Сейчас используется <code>{settings.model}</code>. Список моделей появится, когда LLM включена и App Server отвечает, — тогда модель можно будет сменить здесь.</p>}
    </div>

    <div className="card enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="sparkle" size={16} /></span> Уровень размышлений модели</h2>
      <p className="muted small">{settings.models.find(m => m.id === draft.model)?.listed ? 'Варианты — те, что поддерживает выбранная модель.' : 'App Server не сообщил уровни этой модели, поэтому показаны базовые, которые поддерживает любая модель с размышлениями.'}</p>
      <div className="setting-rows">{PURPOSES.map(p => <div key={p.key} className="setting-row">
        <div><b>{p.title}</b><small className="muted">{p.hint}</small></div>
        <div className="effort-options" role="radiogroup" aria-label={p.title}>{options.map(option => <button type="button" key={option} role="radio" aria-checked={draft.reasoning[p.key] === option}
          className={draft.reasoning[p.key] === option ? 'active' : ''} onClick={() => setDraft(d => d && { ...d, reasoning: { ...d.reasoning, [p.key]: option } })}>
          {EFFORT_TITLES[option] ?? option}{settings.reasoningDefaults[p.key] === option && <span className="default-mark" title="Значение по умолчанию">•</span>}
        </button>)}</div>
      </div>)}</div>
    </div>

    <div className="limits-grid">
      <div className="card enter">
        <h2 className="card-title"><span className="chip-icon"><Icon name="chat" size={16} /></span> Помощник в чате</h2>
        <p className="muted small">Ограничивает вопросы каждого студента помощнику. 0 — без ограничения.</p>
        <div className="setting-rows">{CHAT_LIMITS.map(limitRow)}</div>
      </div>
      <div className="card enter">
        <h2 className="card-title"><span className="chip-icon"><Icon name="book" size={16} /></span> Генерация задач и объяснений</h2>
        <p className="muted small">Общий бюджет курса, не зависит от сообщений в чате. 0 — без ограничения.</p>
        <div className="setting-rows">{GENERATION_LIMITS.map(limitRow)}</div>
        <p className="muted small usage-now">За последний час: задач <b className="tabular">{usage(settings.usageLastHour.tasks, draft.limits.tasksPerHour)}</b>, объяснений <b className="tabular">{usage(settings.usageLastHour.explanations, draft.limits.explanationsPerHour)}</b></p>
      </div>
    </div>
  </form>
}
