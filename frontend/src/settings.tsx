import { FormEvent, useEffect, useState } from 'react'
import { api } from './api'
import { Icon, useToast } from './fx'
import type { LlmLimits, LlmLogging, LlmModel, LlmSettings, LlmPurposeKey } from './types'

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>
type Draft = { models: Record<LlmPurposeKey, string>; reasoning: Record<LlmPurposeKey, string>; limits: LlmLimits; logging: LlmLogging; hardModeChat: boolean }

const PURPOSES: { key: LlmPurposeKey; title: string; hint: string }[] = [
  { key: 'CHAT', title: 'Ответы помощника в чате', hint: 'Студент ждёт ответа: быстрая модель и низкий уровень дают ответ быстрее.' },
  { key: 'TASK', title: 'Генерация и перепроверка задач', hint: 'Нужны точные проверки и неверные примеры решений: сильная модель и высокий уровень дают меньше брака.' },
  { key: 'EXPLANATION', title: 'Объяснения тем', hint: 'Пишутся один раз на тему и потом переиспользуются.' },
  { key: 'REVIEW', title: 'Проверка подхода в задачах «посчитай»', hint: 'Когда вывод верный, решает, посчитан ли ответ или напечатан готовым. Студент ждёт ответа: нужна быстрая и точная модель.' },
]
/** How each kind of task is checked; shown to the teacher, nothing to configure. */
const CHECKS: [string, string][] = [
  ['Вывод текста', 'Запуск программы: вывод сравнивается с нужным, при ошибке студент видит «нужно / получилось».'],
  ['«Посчитай»', 'Запуск проверяет вывод, LLM — что ответ посчитан, а не напечатан готовым. Если LLM недоступна — синтаксическое дерево.'],
  ['«Используй цикл / условие…»', 'Запуск проверяет результат, синтаксическое дерево — что нужная конструкция есть. Отказ объясняет, чего не хватает.'],
  ['Функции и hard-задачи', 'Тест-кейсы: входы даёт модель, ответы считает эталонное решение. В каждой проверке — примеры из условия и 8 случайных скрытых кейсов.'],
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
const REVIEW_LIMITS: LimitField[] = [
  { key: 'reviewsPerHour', title: 'Проверок подхода на студента', unit: 'в час', hint: 'Сверх лимита подход в задачах «посчитай» проверяет синтаксическое дерево.' },
]

/** Levels of a model; when the App Server did not report them, the server's safe set. */
function effortsFor(settings: LlmSettings, model: string) {
  const found = settings.models.find(m => m.id === model)
  return found?.efforts.length ? found.efforts : settings.reasoningOptions
}
/** When the model changes, keep the level if the new model has it, otherwise use the model's default. */
function levelFor(model: LlmModel | undefined, current: string) {
  if (!model?.efforts.length || model.efforts.includes(current)) return current
  return model.efforts.includes(model.defaultEffort) ? model.defaultEffort : model.efforts[Math.floor(model.efforts.length / 2)]
}
const draftOf = (s: LlmSettings): Draft => ({ models: { ...s.purposeModels }, reasoning: { ...s.reasoning }, limits: { ...s.limits }, logging: { ...s.logging }, hardModeChat: s.hardModeChat })

export function LlmSettingsView({ request }: { request: Request }) {
  const [settings, setSettings] = useState<LlmSettings | null>(null)
  const [draft, setDraft] = useState<Draft | null>(null)
  const [saving, setSaving] = useState(false)
  const toast = useToast()
  const load = (value: LlmSettings) => { setSettings(value); setDraft(draftOf(value)) }
  useEffect(() => { request(() => api<LlmSettings>('/admin/llm/settings')).then(value => { if (value) load(value) }) }, [request])
  if (!settings || !draft) return <section className="analytics"><div className="sk sk-card" /></section>

  const dirty = JSON.stringify(draft) !== JSON.stringify(draftOf(settings))
  async function save(e: FormEvent) {
    e.preventDefault(); setSaving(true)
    const value = await request(() => api<LlmSettings>('/admin/llm/settings', { method: 'PUT', body: JSON.stringify(draft) }))
    setSaving(false)
    if (value) { load(value); toast({ tone: 'info', icon: 'check', title: 'Настройки LLM сохранены', text: 'Применяются к следующим обращениям, в том числе в уже начатых чатах' }) }
  }
  const chooseModel = (purpose: LlmPurposeKey, id: string) => setDraft(d => d && {
    ...d, models: { ...d.models, [purpose]: id }, reasoning: { ...d.reasoning, [purpose]: levelFor(settings.models.find(m => m.id === id), d.reasoning[purpose]) },
  })
  const resetToDefaults = () => setDraft(() => ({ models: { ...settings.purposeModelDefaults }, reasoning: { ...settings.reasoningDefaults }, limits: { ...settings.limitDefaults }, logging: { ...settings.loggingDefaults }, hardModeChat: settings.hardModeChatDefault }))
  const anyListed = settings.models.some(m => m.listed)
  const limitRow = (l: LimitField) => <label key={l.key} className="setting-row">
    <div><b>{l.title} <span className="muted">{l.unit}</span></b><small className="muted">{l.hint}</small></div>
    <div className="limit-input">
      <input type="number" min={0} max={10000} step={1} inputMode="numeric" value={draft.limits[l.key]}
        onChange={e => { const value = Math.max(0, Math.floor(Number(e.target.value) || 0)); setDraft(d => d && { ...d, limits: { ...d.limits, [l.key]: value } }) }} />
      <small className="muted">по умолчанию {settings.limitDefaults[l.key] || 'без ограничения'}</small>
    </div>
  </label>
  const usage = (used: number, limit: number) => `${used}${limit ? ` из ${limit}` : ''}`
  const logSwitch = (key: keyof LlmLogging, title: string, hint: string) => <div className="setting-row" key={key}>
    <div><b>{title}</b><small className="muted">{hint}</small></div>
    <button type="button" role="switch" aria-checked={draft.logging[key]} aria-label={title} className={`switch ${draft.logging[key] ? 'on' : ''}`}
      onClick={() => setDraft(d => d && { ...d, logging: { ...d.logging, [key]: !d.logging[key] } })}><span /></button>
  </div>

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
      <h2 className="card-title"><span className="chip-icon"><Icon name="check" size={16} /></span> Как проверяются решения</h2>
      <div className="check-kinds">{CHECKS.map(([kind, how]) => <div key={kind}><b>{kind}</b><small>{how}</small></div>)}</div>
      <div className="setting-rows">
        <div className="setting-row">
          <div><b>Помощник в hard mode</b><small className="muted">Выключите, чтобы студенты в hard mode решали без подсказок. Генерация задач не меняется.</small></div>
          <button type="button" role="switch" aria-checked={draft.hardModeChat} aria-label="Помощник в hard mode" className={`switch ${draft.hardModeChat ? 'on' : ''}`}
            onClick={() => setDraft(d => d && { ...d, hardModeChat: !d.hardModeChat })}><span /></button>
        </div>
      </div>
    </div>

    <div className="card enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="sparkle" size={16} /></span> Модель и уровень размышлений</h2>
      <p className="muted small">Для каждого вида работы — своя модель и свой уровень. Смена действует и в уже начатых чатах студентов.
        {!anyListed && ' Список моделей App Server сейчас недоступен — показаны текущие модели и модели из настроек сервера.'}</p>
      <div className="setting-rows">{PURPOSES.map(p => {
        const model = settings.models.find(m => m.id === draft.models[p.key])
        return <div key={p.key} className="setting-row purpose-row">
          <div><b>{p.title}</b><small className="muted">{p.hint}</small></div>
          <div className="purpose-controls">
            <label className="model-select">
              <span className="sr-only">Модель для «{p.title}»</span>
              <select value={draft.models[p.key]} onChange={e => chooseModel(p.key, e.target.value)}>
                {settings.models.map(m => <option key={m.id} value={m.id}>{m.displayName}{m.id === settings.purposeModelDefaults[p.key] ? ' · по умолчанию' : ''}{m.listed ? '' : ' · не подтверждена'}</option>)}
              </select>
            </label>
            <div className="effort-options" role="radiogroup" aria-label={`Уровень размышлений: ${p.title}`}>{effortsFor(settings, draft.models[p.key]).map(option => <button type="button" key={option} role="radio" aria-checked={draft.reasoning[p.key] === option}
              className={draft.reasoning[p.key] === option ? 'active' : ''} onClick={() => setDraft(d => d && { ...d, reasoning: { ...d.reasoning, [p.key]: option } })}>
              {EFFORT_TITLES[option] ?? option}{settings.reasoningDefaults[p.key] === option && <span className="default-mark" title="Значение по умолчанию">•</span>}
            </button>)}</div>
            {anyListed && model && !model.listed && <small className="model-warn">App Server не подтвердил эту модель: проверьте доступ аккаунта Codex. Уровни — базовые.</small>}
          </div>
        </div>
      })}</div>
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
      <div className="card enter">
        <h2 className="card-title"><span className="chip-icon"><Icon name="check" size={16} /></span> Проверка подхода LLM</h2>
        <p className="muted small">Задачи «посчитай» с верным выводом. 0 — без ограничения.</p>
        <div className="setting-rows">{REVIEW_LIMITS.map(limitRow)}</div>
        <p className="muted small usage-now">За последний час по курсу: <b className="tabular">{settings.usageLastHour.reviews}</b></p>
      </div>
    </div>

    <div className="card enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="code" size={16} /></span> Логирование LLM</h2>
      <p className="muted small">Полный ответ модели и сводка её размышлений пишутся в лог backend (<code>docker compose logs backend</code>). Модели Codex отдают не сырой ход мысли, а его сводку.</p>
      <div className="setting-rows">
        {logSwitch('generation', 'Генерация задач и объяснений', 'Что сгенерировала модель и как рассуждала: условия, проверки, эталонные и неверные решения, объяснения.')}
        {logSwitch('chat', 'Ответы помощника в чате', 'Вместе с ответами в лог попадут вопросы и код студентов — включайте на время разбора проблемы.')}
        {logSwitch('review', 'Проверка подхода', 'Вердикты и рассуждения проверяющего вместе с кодом студентов.')}
      </div>
    </div>
  </form>
}
