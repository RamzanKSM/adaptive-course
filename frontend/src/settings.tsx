import { currentLocale, tr } from './locale'
import { uiText } from './uiText'
import { FormEvent, useEffect, useState } from 'react'
import { api } from './api'
import { Icon, useToast } from './fx'
import type { LlmLimits, LlmLogging, LlmModel, LlmSettings, LlmPurposeKey } from './types'

const SETTINGS_TEXT: Record<string, [string, string]> = {
  "Ответы помощника в чате": ["Réponses de l’assistant", "ردود المساعد في المحادثة"],
  "Студент ждёт ответа: быстрая модель и низкий уровень дают ответ быстрее.": ["L’étudiant attend : un modèle rapide et un niveau bas répondent plus vite.", "الطالب منتظر الرد: الموديل السريع والمستوى المنخفض بيسرعوا الرد."],
  "Генерация и перепроверка задач": ["Génération et vérification des exercices", "إنشاء التمارين وإعادة فحصها"],
  "Нужны точные проверки и неверные примеры решений: сильная модель и высокий уровень дают меньше брака.": ["Des vérifications précises et des exemples incorrects sont nécessaires : un modèle puissant réduit les erreurs.", "الفحص الدقيق والأمثلة الخاطئة محتاجة موديل قوي ومستوى أعلى لتقليل الأخطاء."],
  "Объяснения тем": ["Explications des notions", "شرح الموضوعات"],
  "Пишутся один раз на тему и потом переиспользуются.": ["Rédigées une fois par notion, puis réutilisées.", "بتتكتب مرة لكل موضوع وبعدها بيعاد استخدامها."],
  "Проверка подхода в задачах «посчитай»": ["Vérification de la méthode dans les exercices de calcul", "فحص طريقة الحل في تمارين الحساب"],
  "Когда вывод верный, решает, посчитан ли ответ или напечатан готовым. Студент ждёт ответа: нужна быстрая и точная модель.": ["Quand la sortie est correcte, vérifie si la réponse est calculée ou simplement affichée. Un modèle rapide et précis est nécessaire.", "لما الناتج صحيح، بتتحقق إذا الإجابة اتحسبت أو انطبعت جاهزة. محتاج موديل سريع ودقيق."],
  "Вывод текста": ["Affichage de texte", "طباعة النص"],
  "Запуск программы: вывод сравнивается с нужным, при ошибке студент видит «нужно / получилось».": ["La sortie du programme est comparée au résultat attendu ; en cas d’erreur, l’étudiant voit les deux.", "ناتج البرنامج بيتقارن بالمطلوب؛ عند الخطأ الطالب بيشوف المطلوب والناتج."],
  "«Посчитай»": ["« Calculer »", "«احسب»"],
  "Запуск проверяет вывод, LLM — что ответ посчитан, а не напечатан готовым. Если LLM недоступна — синтаксическое дерево.": ["L’exécution vérifie la sortie ; le modèle vérifie que la réponse est calculée. Sinon, l’arbre syntaxique prend le relais.", "التشغيل بيفحص الناتج والموديل بيتأكد إن الإجابة محسوبة. عند تعذر الموديل بتستخدم شجرة الصياغة."],
  "«Используй цикл / условие…»": ["« Utiliser une boucle / condition… »", "«استخدم حلقة / شرط…»"],
  "Запуск проверяет результат, синтаксическое дерево — что нужная конструкция есть. Отказ объясняет, чего не хватает.": ["L’exécution vérifie le résultat et l’arbre syntaxique la construction demandée. Un refus explique ce qui manque.", "التشغيل بيفحص النتيجة وشجرة الصياغة بتفحص وجود البنية المطلوبة. الرفض بيوضح الناقص."],
  "Функции и hard-задачи": ["Fonctions et exercices difficiles", "الدوال والتمارين الصعبة"],
  "Тест-кейсы: входы даёт модель, ответы считает эталонное решение. В каждой проверке — примеры из условия и 8 случайных скрытых кейсов.": ["Les entrées viennent du modèle et les réponses de la solution de référence. Chaque vérification comprend les exemples et huit cas cachés aléatoires.", "الموديل بيولد المدخلات والحل المرجعي بيحسب الإجابات. كل فحص فيه أمثلة السؤال وثمانية اختبارات مخفية عشوائية."],
  "Сообщений на студента": ["Messages par étudiant", "الرسائل لكل طالب"],
  "в час": ["par heure", "في الساعة"],
  "в сутки": ["par jour", "في اليوم"],
  "Скользящее окно: последние 60 минут.": ["Fenêtre glissante : les 60 dernières minutes.", "نافذة متحركة: آخر ٦٠ دقيقة."],
  "Скользящее окно: последние 24 часа.": ["Fenêtre glissante : les 24 dernières heures.", "نافذة متحركة: آخر ٢٤ ساعة."],
  "Генераций задач на весь курс": ["Générations d’exercices pour le cours", "إنشاء التمارين للكورس كله"],
  "Новые задачи и перепроверка старых. При исчерпании студенты получают готовые задачи из банка.": ["Nouveaux exercices et revérification. Une fois la limite atteinte, les étudiants reçoivent des exercices de la banque.", "للتمارين الجديدة وإعادة الفحص. بعد الحد الطلاب بياخدوا تمارين جاهزة من البنك."],
  "Генераций объяснений тем на весь курс": ["Générations d’explications pour le cours", "إنشاء الشروح للكورس كله"],
  "Объяснение пишется один раз на тему. При исчерпании урок идёт без объяснения, пока лимит не освободится.": ["Une explication est générée par notion. Après la limite, le cours continue sans explication jusqu’à son renouvellement.", "الشرح بيتكتب مرة للموضوع. بعد الحد الدرس بيستمر بدون شرح لحد ما الحد يتجدد."],
  "Проверок подхода на студента": ["Vérifications de méthode par étudiant", "فحص طريقة الحل لكل طالب"],
  "Сверх лимита подход в задачах «посчитай» проверяет синтаксическое дерево.": ["Au-delà de la limite, l’arbre syntaxique vérifie la méthode.", "بعد الحد شجرة الصياغة بتفحص الطريقة."]
}
const settingsText = (value: string) => { const translation = SETTINGS_TEXT[value]; return translation ? tr(currentLocale(), value, translation[0], translation[1]) : uiText(value) }

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
    if (value) { load(value); toast({ tone: 'info', icon: 'check', title: uiText("Настройки LLM сохранены"), text: uiText("Применяются к следующим обращениям, в том числе в уже начатых чатах") }) }
  }
  const chooseModel = (purpose: LlmPurposeKey, id: string) => setDraft(d => d && {
    ...d, models: { ...d.models, [purpose]: id }, reasoning: { ...d.reasoning, [purpose]: levelFor(settings.models.find(m => m.id === id), d.reasoning[purpose]) },
  })
  const resetToDefaults = () => setDraft(() => ({ models: { ...settings.purposeModelDefaults }, reasoning: { ...settings.reasoningDefaults }, limits: { ...settings.limitDefaults }, logging: { ...settings.loggingDefaults }, hardModeChat: settings.hardModeChatDefault }))
  const anyListed = settings.models.some(m => m.listed)
  const limitRow = (l: LimitField) => <label key={l.key} className="setting-row">
    <div><b>{settingsText(l.title)} <span className="muted">{settingsText(l.unit)}</span></b><small className="muted">{settingsText(l.hint)}</small></div>
    <div className="limit-input">
      <input type="number" min={0} max={10000} step={1} inputMode="numeric" value={draft.limits[l.key]}
        onChange={e => { const value = Math.max(0, Math.floor(Number(e.target.value) || 0)); setDraft(d => d && { ...d, limits: { ...d.limits, [l.key]: value } }) }} />
      <small className="muted">{uiText("по умолчанию")} {settings.limitDefaults[l.key] || uiText("без ограничения")}</small>
    </div>
  </label>
  const usage = (used: number, limit: number) => `${used}${limit ? tr(currentLocale(), ` из ${limit}`, ` sur ${limit}`, ` من ${limit}`) : ''}`
  const logSwitch = (key: keyof LlmLogging, title: string, hint: string) => <div className="setting-row" key={key}>
    <div><b>{title}</b><small className="muted">{hint}</small></div>
    <button type="button" role="switch" aria-checked={draft.logging[key]} aria-label={title} className={`switch ${draft.logging[key] ? 'on' : ''}`}
      onClick={() => setDraft(d => d && { ...d, logging: { ...d.logging, [key]: !d.logging[key] } })}><span /></button>
  </div>

  return <form className="analytics settings-page" onSubmit={save}>
    <div className="analytics-head enter">
      <div>
        <p className="eyebrow">{uiText("Преподаватель")}</p>
        <h1 className="display small">{uiText("Настройки LLM")}</h1>
        <p className="muted small">{uiText("Изменения применяются к следующим обращениям, без перезапуска.")}</p>
      </div>
      <div className="settings-actions">
        <button type="button" className="ghost" onClick={resetToDefaults}>{uiText("Значения по умолчанию")}</button>
        <button className="primary" disabled={!dirty || saving}>{saving ? uiText("Сохраняем…") : uiText("Сохранить")}</button>
      </div>
    </div>

    <div className="card enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="check" size={16} /></span> {uiText("Как проверяются решения")}</h2>
      <div className="check-kinds">{CHECKS.map(([kind, how]) => <div key={kind}><b>{settingsText(kind)}</b><small>{settingsText(how)}</small></div>)}</div>
      <div className="setting-rows">
        <div className="setting-row">
          <div><b>{uiText("Помощник в hard mode")}</b><small className="muted">{uiText("Выключите, чтобы студенты в hard mode решали без подсказок. Генерация задач не меняется.")}</small></div>
          <button type="button" role="switch" aria-checked={draft.hardModeChat} aria-label={uiText("Помощник в hard mode")} className={`switch ${draft.hardModeChat ? 'on' : ''}`}
            onClick={() => setDraft(d => d && { ...d, hardModeChat: !d.hardModeChat })}><span /></button>
        </div>
      </div>
    </div>

    <div className="card enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="sparkle" size={16} /></span> {uiText("Модель и уровень размышлений")}</h2>
      <p className="muted small">{uiText("Для каждого вида работы — своя модель и свой уровень. Смена действует и в уже начатых чатах студентов.")}
        {!anyListed && uiText(" Список моделей App Server сейчас недоступен — показаны текущие модели и модели из настроек сервера.")}</p>
      <div className="setting-rows">{PURPOSES.map(p => {
        const model = settings.models.find(m => m.id === draft.models[p.key])
        return <div key={p.key} className="setting-row purpose-row">
          <div><b>{settingsText(p.title)}</b><small className="muted">{settingsText(p.hint)}</small></div>
          <div className="purpose-controls">
            <label className="model-select">
              <span className="sr-only">{uiText("Модель для «")}{settingsText(p.title)}»</span>
              <select value={draft.models[p.key]} onChange={e => chooseModel(p.key, e.target.value)}>
                {settings.models.map(m => <option key={m.id} value={m.id}>{m.displayName}{m.id === settings.purposeModelDefaults[p.key] ? uiText(" · по умолчанию") : ''}{m.listed ? '' : uiText(" · не подтверждена")}</option>)}
              </select>
            </label>
            <div className="effort-options" role="radiogroup" aria-label={tr(currentLocale(), `Уровень размышлений: ${settingsText(p.title)}`, `Niveau de raisonnement : ${settingsText(p.title)}`, `مستوى التفكير: ${settingsText(p.title)}`)}>{effortsFor(settings, draft.models[p.key]).map(option => <button type="button" key={option} role="radio" aria-checked={draft.reasoning[p.key] === option}
              className={draft.reasoning[p.key] === option ? 'active' : ''} onClick={() => setDraft(d => d && { ...d, reasoning: { ...d.reasoning, [p.key]: option } })}>
              {EFFORT_TITLES[option] ?? option}{settings.reasoningDefaults[p.key] === option && <span className="default-mark" title={uiText("Значение по умолчанию")}>•</span>}
            </button>)}</div>
            {anyListed && model && !model.listed && <small className="model-warn">{uiText("App Server не подтвердил эту модель: проверьте доступ аккаунта Codex. Уровни — базовые.")}</small>}
          </div>
        </div>
      })}</div>
    </div>

    <div className="limits-grid">
      <div className="card enter">
        <h2 className="card-title"><span className="chip-icon"><Icon name="chat" size={16} /></span> {uiText("Помощник в чате")}</h2>
        <p className="muted small">{uiText("Ограничивает вопросы каждого студента помощнику. 0 — без ограничения.")}</p>
        <div className="setting-rows">{CHAT_LIMITS.map(limitRow)}</div>
      </div>
      <div className="card enter">
        <h2 className="card-title"><span className="chip-icon"><Icon name="book" size={16} /></span> {uiText("Генерация задач и объяснений")}</h2>
        <p className="muted small">{uiText("Общий бюджет курса, не зависит от сообщений в чате. 0 — без ограничения.")}</p>
        <div className="setting-rows">{GENERATION_LIMITS.map(limitRow)}</div>
        <p className="muted small usage-now">{uiText("За последний час: задач")} <b className="tabular">{usage(settings.usageLastHour.tasks, draft.limits.tasksPerHour)}</b>{uiText(", объяснений")} <b className="tabular">{usage(settings.usageLastHour.explanations, draft.limits.explanationsPerHour)}</b></p>
      </div>
      <div className="card enter">
        <h2 className="card-title"><span className="chip-icon"><Icon name="check" size={16} /></span> {uiText("Проверка подхода LLM")}</h2>
        <p className="muted small">{uiText("Задачи «посчитай» с верным выводом. 0 — без ограничения.")}</p>
        <div className="setting-rows">{REVIEW_LIMITS.map(limitRow)}</div>
        <p className="muted small usage-now">{uiText("За последний час по курсу:")} <b className="tabular">{settings.usageLastHour.reviews}</b></p>
      </div>
    </div>

    <div className="card enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="code" size={16} /></span> {uiText("Логирование LLM")}</h2>
      <p className="muted small">{uiText("Полный ответ модели и сводка её размышлений пишутся в лог backend (")}<code>docker compose logs backend</code>{uiText("). Модели Codex отдают не сырой ход мысли, а его сводку.")}</p>
      <div className="setting-rows">
        {logSwitch('generation', 'Генерация задач и объяснений', 'Что сгенерировала модель и как рассуждала: условия, проверки, эталонные и неверные решения, объяснения.')}
        {logSwitch('chat', 'Ответы помощника в чате', 'Вместе с ответами в лог попадут вопросы и код студентов — включайте на время разбора проблемы.')}
        {logSwitch('review', 'Проверка подхода', 'Вердикты и рассуждения проверяющего вместе с кодом студентов.')}
      </div>
    </div>
  </form>
}
