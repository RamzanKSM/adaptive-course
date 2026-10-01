import { FormEvent, KeyboardEvent, useCallback, useEffect, useRef, useState } from 'react'
import CodeMirror from '@uiw/react-codemirror'
import { java } from '@codemirror/lang-java'
import ReactMarkdown from 'react-markdown'
import { api, ApiError, humanize, onUnauthorized, patch, post } from './api'
import type { Attempt, ChatMessage, Diagnostic, Id, LearningNext, Lesson, LessonDetail, LlmStatus, MeResponse, Progress, SkillProgress, Student, Task, User } from './types'

const UNKNOWN = 'Не знаю'
const codeFallback = 'public class Solution {\n    public static void main(String[] args) {\n        // Напишите решение здесь\n    }\n}\n'
// SQLite CURRENT_TIMESTAMP values are UTC without a zone ("2026-10-01 05:00:00"); Safari cannot parse them as-is.
const parseDate = (value: string) => new Date(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$/.test(value) ? `${value.replace(' ', 'T')}Z` : value)
const fmt = (value?: string | null) => {
  if (!value) return ''
  const date = parseDate(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString('ru-RU')
}
const javaExtensions = [java()]

function Markdown({ children, inline = false }: { children: string; inline?: boolean }) {
  const content = <ReactMarkdown
    components={{
      p: ({ children: paragraphChildren }) => inline ? <>{paragraphChildren}</> : <p>{paragraphChildren}</p>,
      code: ({ className, children, node: _node, ...props }) => {
        const language = /language-(\w+)/.exec(className || '')?.[1]
        return language ? <code className={`language-${language}`}>{children}</code> : <code {...props}>{children}</code>
      },
    }}
  >{children}</ReactMarkdown>
  return inline ? <span className="markdown inline-markdown">{content}</span> : <div className="markdown">{content}</div>
}

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>

export default function App() {
  const [me, setMe] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const request = useCallback<Request>(async action => {
    setError('')
    try { return await action() } catch (e) { setError(e instanceof Error ? e.message : 'Не удалось выполнить запрос'); return undefined }
  }, [])
  useEffect(() => {
    api<MeResponse>('/auth/me')
      .then(value => setMe(value.user))
      .catch(err => { if (!(err instanceof ApiError && err.status === 401)) setError(err instanceof Error ? err.message : 'Не удалось проверить сессию') })
      .finally(() => setLoading(false))
  }, [])
  useEffect(() => {
    if (!me) return
    onUnauthorized(() => { setMe(null); setError('Сессия истекла. Войдите снова.') })
    return () => onUnauthorized(null)
  }, [me])
  const login = (user: User) => { setError(''); setMe(user) }
  const logout = async () => { await request(() => post<void>('/auth/logout')); setError(''); setMe(null) }
  if (loading) return <div className="center">Загружаем…</div>
  if (!me) return <Login onLogin={login} onError={setError} error={error} />
  return <main className="app">
    <header>
      <div><b>Java Tutor</b><span>{me.displayName} · {me.role === 'STUDENT' ? 'Студент' : 'Преподаватель'}</span></div>
      <button className="quiet" onClick={logout}>Выйти</button>
    </header>
    {error && <div className="flash error" role="alert"><span>{error}</span><button className="flash-close" aria-label="Скрыть сообщение" onClick={() => setError('')}>×</button></div>}
    {me.role === 'STUDENT' ? <StudentPage request={request} /> : <TeacherPage request={request} />}
  </main>
}

function Login({ onLogin, onError, error }: { onLogin: (me: User) => void; onError: (message: string) => void; error: string }) {
  const [login, setLogin] = useState(''); const [password, setPassword] = useState(''); const [sending, setSending] = useState(false)
  async function submit(e: FormEvent) {
    e.preventDefault(); setSending(true); onError('')
    try { onLogin((await post<MeResponse>('/auth/login', { login: login.trim(), password })).user) }
    catch (err) { onError(err instanceof Error ? err.message : 'Не удалось войти'); setSending(false) }
  }
  return <main className="login"><section className="card">
    <p className="eyebrow">АДАПТИВНОЕ ОБУЧЕНИЕ</p><h1>Учимся Java в своём темпе</h1><p>Войдите по данным, которые выдал преподаватель.</p>
    <form onSubmit={submit}>
      <label>Логин<input required value={login} onChange={e => setLogin(e.target.value)} autoComplete="username" autoCapitalize="none" spellCheck={false} /></label>
      <label>Пароль<input required type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" /></label>
      {error && <p className="form-error" role="alert">{error}</p>}
      <button disabled={sending}>{sending ? 'Входим…' : 'Войти'}</button>
    </form>
  </section></main>
}

type LoadState = 'loading' | 'ready' | 'failed'

function StudentPage({ request }: { request: Request }) {
  const [diagnostic, setDiagnostic] = useState<Diagnostic | null>(null)
  const [lesson, setLesson] = useState<LearningNext | null>(null)
  const [state, setState] = useState<LoadState>('loading')
  const [progress, setProgress] = useState<Progress | null>(null)
  const [tab, setTab] = useState<'lesson' | 'progress'>('lesson')
  const loadId = useRef(0)
  const load = useCallback(async () => {
    const id = ++loadId.current
    const stale = () => id !== loadId.current
    setState('loading')
    request(() => api<Progress>('/progress')).then(value => { if (value && !stale()) setProgress(value) })
    const d = await request(() => api<Diagnostic>('/diagnostic'))
    if (stale()) return
    if (!d) return setState('failed')
    setDiagnostic(d)
    if (!d.completed) return setState('ready')
    const current = await request(() => api<{ lesson: Lesson | null }>('/lessons/current'))
    if (stale()) return
    if (!current) return setState('failed')
    if (!current.lesson) { setLesson(null); return setState('ready') }
    const next = await request(() => api<LearningNext>('/learning/next'))
    if (stale()) return
    if (!next) return setState('failed')
    setLesson(next); setState('ready')
  }, [request])
  useEffect(() => { load() }, [load])

  if (!diagnostic) return state === 'failed'
    ? <section className="empty"><h1>Не удалось загрузить данные</h1><button onClick={load}>Повторить</button></section>
    : <div className="center">Загружаем…</div>
  if (!diagnostic.completed) return <DiagnosticForm diagnostic={diagnostic} request={request} onDone={load} />
  const progressSkills = (skills: SkillProgress[]) => setProgress({ skills })
  return <>
    <nav className="tabs" role="tablist">
      <button role="tab" aria-selected={tab === 'lesson'} className={tab === 'lesson' ? 'active' : ''} onClick={() => setTab('lesson')}>Текущий урок</button>
      <button role="tab" aria-selected={tab === 'progress'} className={tab === 'progress' ? 'active' : ''} onClick={() => setTab('progress')}>Мой прогресс</button>
    </nav>
    {/* Both tabs stay mounted so switching to progress does not discard the code in the editor. */}
    <div hidden={tab !== 'progress'}><ProgressView progress={progress} /></div>
    <div hidden={tab !== 'lesson'}>
      {state === 'loading' ? <section className="empty"><h2>Готовим урок…</h2><p className="muted">Подбор новой задачи может занять до минуты.</p></section>
        : state === 'failed' ? <section className="empty"><h2>Не удалось загрузить урок</h2><button onClick={load}>Повторить</button></section>
          : <LessonView lesson={lesson} request={request} refresh={load} onProgress={progressSkills} />}
    </div>
  </>
}

function DiagnosticForm({ diagnostic, request, onDone }: { diagnostic: Diagnostic; request: Request; onDone: () => void }) {
  const [index, setIndex] = useState(0); const [answers, setAnswers] = useState<Record<string, number | null>>({}); const [sending, setSending] = useState(false)
  const total = diagnostic.questions.length
  const question = diagnostic.questions[index]
  const last = index === total - 1
  useEffect(() => { window.scrollTo({ top: 0 }) }, [index])
  if (!question) return <section className="empty"><h1>Диагностика пока недоступна</h1><p>Вопросы ещё не загружены. Обратитесь к преподавателю.</p></section>
  const save = async () => {
    setSending(true)
    const body = { answers: diagnostic.questions.map(q => ({ questionId: q.id, selectedOption: answers[q.id] ?? null })) }
    const done = await request(() => post('/diagnostic', body))
    setSending(false)
    if (done) onDone()
  }
  const answered = answers[question.id] !== undefined
  return <section className="diagnostic">
    <p className="eyebrow">ПЕРВИЧНАЯ ДИАГНОСТИКА</p><h1>Поймём, с чего начать</h1><p>Здесь нет оценки. Если не уверены, выберите «Не знаю».</p>
    <div className="meter"><i style={{ width: `${((index + 1) / total) * 100}%` }} /></div>
    <small>Вопрос {index + 1} из {total}</small>
    <article className="card question">
      <div className="question-prompt"><Markdown>{question.prompt}</Markdown></div>
      <div className="choices" role="radiogroup">{[...question.options, UNKNOWN].map((option, optionIndex) => {
        const value = optionIndex === question.options.length ? null : optionIndex
        return <label key={optionIndex}>
          <input type="radio" name={`question-${question.id}`} checked={answers[question.id] === value} onChange={() => setAnswers({ ...answers, [question.id]: value })} />
          <Markdown inline>{option}</Markdown>
        </label>
      })}</div>
    </article>
    <div className="actions">
      {index > 0 && <button className="secondary" disabled={sending} onClick={() => setIndex(index - 1)}>Назад</button>}
      {last
        ? <button disabled={!answered || sending} onClick={save}>{sending ? 'Сохраняем…' : 'Завершить диагностику'}</button>
        : <button disabled={!answered} onClick={() => setIndex(index + 1)}>Далее</button>}
    </div>
  </section>
}

function LessonView({ lesson, request, refresh, onProgress }: { lesson: LearningNext | null; request: Request; refresh: () => void; onProgress: (skills: SkillProgress[]) => void }) {
  const [working, setWorking] = useState(false)
  async function start() { setWorking(true); const started = await request(() => post<{ lesson: Lesson }>('/lessons/start')); setWorking(false); if (started) refresh() }
  async function finish(current: Lesson, hasTask: boolean) {
    if (hasTask && !window.confirm('Текущая задача ещё не решена. Завершить урок?')) return
    setWorking(true); const finished = await request(() => post(`/lessons/${current.id}/finish`)); setWorking(false); if (finished) refresh()
  }
  if (!lesson) return <section className="empty"><h1>Урок ещё не начат</h1><p>Сервис выберет следующую тему по результатам диагностики и предыдущим занятиям.</p><button disabled={working} onClick={start}>{working ? 'Готовим урок…' : 'Начать урок'}</button></section>
  const title = lesson.skill?.title ?? (lesson.reason === 'NO_DUE_SKILL' ? 'На сегодня задач больше нет' : 'Текущий урок')
  const retryable = lesson.reason === 'LLM_GENERATION_FAILED_VALIDATION' || lesson.reason === 'RUNNER_UNAVAILABLE'
  const emptyMessage = lesson.reason === 'NO_TASK_AVAILABLE' ? 'Подходящей задачи в банке пока нет. Преподаватель увидит это состояние.'
    : lesson.reason === 'LLM_GENERATION_FAILED_VALIDATION' ? 'Новая задача не прошла проверку. Попробуйте запросить её ещё раз.'
      : lesson.reason === 'RUNNER_UNAVAILABLE' ? 'Проверка Java сейчас недоступна. Попробуйте ещё раз позже.'
        : lesson.reason === 'NO_DUE_SKILL' ? 'Все задачи этого урока выполнены.' : 'Контент урока загружается.'
  return <section className="lesson">
    <div className="lesson-heading">
      <div><p className="eyebrow">АКТИВНЫЙ УРОК · {lesson.lesson.number}</p><h1>{title}</h1></div>
      <button className="secondary" disabled={working} onClick={() => finish(lesson.lesson, !!lesson.task)}>{working ? 'Завершаем…' : 'Завершить урок'}</button>
    </div>
    {lesson.explanation && <article className="explanation"><h2>Объяснение</h2><Markdown>{lesson.explanation.content}</Markdown></article>}
    {lesson.task
      ? <TaskWorkspace key={lesson.task.id} task={lesson.task} llm={lesson.llm} request={request} onNext={refresh} onProgress={onProgress} />
      : <div className="lesson-grid"><article className="task empty-task"><h2>{lesson.reason === 'NO_DUE_SKILL' ? 'Урок можно завершить' : 'Задача ещё не подготовлена'}</h2><p>{emptyMessage}</p>{retryable && <button className="secondary" onClick={refresh}>Повторить</button>}</article><Chat llm={lesson.llm} request={request} /></div>}
  </section>
}

function TaskWorkspace({ task, llm, request, onNext, onProgress }: { task: Task; llm?: LlmStatus; request: Request; onNext: () => void; onProgress: (skills: SkillProgress[]) => void }) {
  const [code, setCode] = useState(task.starterCode || codeFallback)
  return <div className="lesson-grid">
    <TaskEditor task={task} code={code} onCodeChange={setCode} request={request} onNext={onNext} onProgress={onProgress} />
    <Chat llm={llm} request={request} taskId={task.id} sourceCode={code} />
  </div>
}

function TaskEditor({ task, code, onCodeChange, request, onNext, onProgress }: { task: Task; code: string; onCodeChange: (code: string) => void; request: Request; onNext: () => void; onProgress: (skills: SkillProgress[]) => void }) {
  const [attempt, setAttempt] = useState<Attempt | null>(null); const [sending, setSending] = useState(false)
  const resultRef = useRef<HTMLDivElement>(null)
  async function submit() {
    setSending(true)
    const result = await request(() => post<Attempt & { progress?: SkillProgress[] }>('/attempts', { taskId: task.id, sourceCode: code }))
    setSending(false)
    if (!result) return
    setAttempt(result)
    if (result.progress) onProgress(result.progress)
  }
  useEffect(() => { if (attempt) resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }) }, [attempt])
  const passed = !!attempt?.passed
  return <section className="task">
    <h2>{task.title}</h2><Markdown>{task.statement}</Markdown>
    <div className="code-label"><span>Решение на Java</span><CodeMirror className="code-editor" value={code} height="clamp(18rem, 48vh, 32rem)" extensions={javaExtensions} onChange={onCodeChange} editable={!passed} aria-label="Редактор решения на Java" /></div>
    {passed
      ? <button onClick={onNext}>Следующая задача</button>
      : <button disabled={sending || !code.trim()} onClick={submit}>{sending ? 'Проверяем…' : 'Отправить на проверку'}</button>}
    {attempt && <div ref={resultRef} className={`result ${passed ? 'success' : 'failed'}`} role="status"><b>{passed ? 'Решение принято' : 'Нужно доработать'}</b>{attempt.output && <pre>{attempt.output}</pre>}</div>}
  </section>
}

type ChatState = { messages: ChatMessage[]; llm: LlmStatus }

function Chat({ llm, request, taskId, sourceCode }: { llm?: LlmStatus; request: Request; taskId?: Id; sourceCode?: string }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]); const [text, setText] = useState(''); const [status, setStatus] = useState<LlmStatus | undefined>(llm); const [sending, setSending] = useState(false)
  const listRef = useRef<HTMLDivElement>(null)
  const sync = useCallback(async () => {
    const value = await request(() => api<ChatState>('/chat'))
    if (value) { setMessages(value.messages); setStatus(value.llm) }
    return value
  }, [request])
  useEffect(() => { sync() }, [sync])
  useEffect(() => { const list = listRef.current; if (list) list.scrollTop = list.scrollHeight }, [messages, sending])
  async function send(e?: FormEvent) {
    e?.preventDefault()
    const content = text.trim(); if (!content || sending) return
    setSending(true)
    setMessages(m => [...m, { id: `local-${Date.now()}`, role: 'STUDENT', content, createdAt: new Date().toISOString() }]); setText('')
    const body = taskId !== undefined ? { content, taskId, sourceCode } : { content }
    const result = await request(() => post<{ message: ChatMessage; llm?: LlmStatus }>('/chat', body))
    if (result) {
      setMessages(m => [...m, result.message]); if (result.llm) setStatus(result.llm)
    } else {
      // The server may or may not have stored the question; resync and give the text back if it was lost.
      const synced = await sync()
      const stored = synced?.messages.some(m => m.role === 'STUDENT' && m.content === content)
      if (!stored) { setMessages(m => m.filter(x => !(typeof x.id === 'string' && x.id.startsWith('local-')))); setText(t => t || content) }
    }
    setSending(false)
  }
  const onKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) send() }
  const unavailable = status && !status.available ? humanize(status.reason) || 'Помощник временно недоступен.' : ''
  return <aside className="chat">
    <h2>Учебный помощник</h2>
    <div className="messages" ref={listRef} aria-live="polite">
      {messages.length ? messages.map(m => <div key={m.id} className={`message ${m.role.toLowerCase()}`}><small>{m.role === 'STUDENT' ? 'Вы' : 'Помощник'} {fmt(m.createdAt)}</small><Markdown>{m.content}</Markdown></div>)
        : <p className="muted">Помощник подскажет ход мысли; за точным разбором обратитесь к преподавателю.</p>}
      {sending && <p className="muted typing">Помощник думает…</p>}
    </div>
    {unavailable ? <p className="muted">{unavailable}</p> : <form onSubmit={send}>
      {taskId !== undefined && <p className="chat-code-note">Помощник видит текущий код из редактора.</p>}
      <textarea value={text} onChange={e => setText(e.target.value)} onKeyDown={onKeyDown} placeholder="Опишите, где возникло затруднение (Ctrl+Enter — отправить)" aria-label="Ваш вопрос учебному помощнику" />
      <button disabled={sending || !text.trim()}>{sending ? 'Отправляем…' : 'Отправить'}</button>
    </form>}
  </aside>
}

const ITERATIONS = 3, SUCCESSES_PER_ITERATION = 3
function skillPercent(skill: SkillProgress) {
  if (skill.mastered) return 100
  const done = skill.completedIterations * SUCCESSES_PER_ITERATION + Math.min(skill.iterationSuccesses, SUCCESSES_PER_ITERATION)
  return Math.round(done / (ITERATIONS * SUCCESSES_PER_ITERATION) * 100)
}

function ProgressView({ progress }: { progress: Progress | null }) {
  return <section><h1>Мой прогресс</h1>{!progress ? <p>Загружаем…</p> : <div className="card"><div className="skills">{progress.skills.length
    ? progress.skills.map(skill => <div key={skill.skillCode}>
      <span>{skill.title}</span>
      <div className="bar" role="progressbar" aria-valuenow={skillPercent(skill)} aria-valuemin={0} aria-valuemax={100} aria-label={skill.title}><i style={{ width: `${skillPercent(skill)}%` }} /></div>
      <small>{skill.mastered ? 'Освоено' : `${skill.completedIterations}/${ITERATIONS} итераций · ${skill.iterationSuccesses}/${SUCCESSES_PER_ITERATION} успешных решений`}</small>
    </div>)
    : <p className="muted">Прогресс появится после первого решения.</p>}</div></div>}</section>
}

function TeacherPage({ request }: { request: Request }) {
  const [students, setStudents] = useState<Student[] | null>(null); const [selected, setSelected] = useState<Student | null>(null)
  const [globalLlm, setGlobalLlm] = useState<LlmStatus | null>(null)
  const [name, setName] = useState(''); const [login, setLogin] = useState(''); const [password, setPassword] = useState(''); const [creating, setCreating] = useState(false)
  const load = useCallback(() => request(() => api<{ students: Student[] }>('/admin/students')).then(s => { if (s) setStudents(s.students) }), [request])
  useEffect(() => {
    load()
    request(() => api<MeResponse>('/auth/me')).then(value => { if (value) setGlobalLlm(value.llm) })
  }, [load, request])
  async function create(e: FormEvent) {
    e.preventDefault(); setCreating(true)
    const student = await request(() => post<Student>('/admin/students', { displayName: name.trim(), login: login.trim(), password }))
    setCreating(false)
    if (student) { setName(''); setLogin(''); setPassword(''); load() }
  }
  async function toggle(student: Student) {
    const updated = await request(() => patch<{ id: Id; enabled: boolean }>(`/admin/students/${student.id}/llm`, { enabled: !student.llmEnabled }))
    if (!updated) return
    setStudents(xs => xs && xs.map(x => x.id === updated.id ? { ...x, llmEnabled: updated.enabled } : x))
    setSelected(s => s && s.id === updated.id ? { ...s, llmEnabled: updated.enabled } : s)
  }
  async function toggleGlobal() {
    if (!globalLlm) return
    const updated = await request(() => patch<{ enabled: boolean }>('/admin/llm', { enabled: !globalLlm.globallyEnabled }))
    if (updated) request(() => api<MeResponse>('/auth/me')).then(value => setGlobalLlm(value ? value.llm : { ...globalLlm, globallyEnabled: updated.enabled }))
  }
  const onLlmStatus = useCallback((llm: LlmStatus) => setGlobalLlm(current => current ? { ...current, globallyEnabled: llm.globallyEnabled } : current), [])
  const configDisabled = globalLlm?.reason === 'DISABLED_BY_CONFIGURATION'
  return <section className="admin">
    <div>
      <p className="eyebrow">ПРЕПОДАВАТЕЛЬ</p><h1>Студенты</h1>
      <div className="card"><h2>LLM для курса</h2>
        <p className="muted">{!globalLlm ? 'Загружаем…' : globalLlm.globallyEnabled ? 'Включена' : configDisabled ? 'Отключена в настройках сервера (APP_LLM_ENABLED)' : 'Выключена'}</p>
        <button className="secondary" disabled={!globalLlm || configDisabled} onClick={toggleGlobal}>{globalLlm?.globallyEnabled ? 'Выключить LLM' : 'Включить LLM'}</button>
      </div>
      <div className="card"><h2>Создать учётную запись</h2>
        <form className="inline-form" onSubmit={create} autoComplete="off">
          <input placeholder="Имя" aria-label="Имя" required value={name} onChange={e => setName(e.target.value)} />
          <input placeholder="Логин" aria-label="Логин" required value={login} onChange={e => setLogin(e.target.value)} autoComplete="off" autoCapitalize="none" spellCheck={false} />
          <input placeholder="Пароль" aria-label="Пароль" required value={password} onChange={e => setPassword(e.target.value)} autoComplete="new-password" />
          <button disabled={creating}>{creating ? 'Создаём…' : 'Создать'}</button>
        </form>
      </div>
      <div className="student-list">{!students ? <p className="muted list-note">Загружаем…</p> : students.length
        ? students.map(s => <button key={s.id} className={selected?.id === s.id ? 'student selected' : 'student'} aria-pressed={selected?.id === s.id} onClick={() => setSelected(s)}><span><b>{s.displayName}</b><small>{s.login}</small></span><i className={s.llmEnabled ? 'on' : ''}>LLM</i></button>)
        : <p className="muted list-note">Студентов пока нет. Создайте первую учётную запись выше.</p>}</div>
    </div>
    {selected ? <StudentDetail student={selected} request={request} toggle={() => toggle(selected)} onLlmStatus={onLlmStatus} />
      : <aside className="student-detail placeholder"><p className="muted">Выберите студента, чтобы увидеть его уроки, решения и переписку с помощником.</p></aside>}
  </section>
}

function StudentDetail({ student, request, toggle, onLlmStatus }: { student: Student; request: Request; toggle: () => void; onLlmStatus: (llm: LlmStatus) => void }) {
  const [lessons, setLessons] = useState<Lesson[] | null>(null)
  const [openLesson, setOpenLesson] = useState<Id | null>(null)
  const [detail, setDetail] = useState<LessonDetail | null>(null)
  const openRef = useRef<Id | null>(null)
  useEffect(() => {
    let alive = true
    setLessons(null); setDetail(null); setOpenLesson(null); openRef.current = null
    request(() => api<{ lessons: Lesson[] }>(`/admin/students/${student.id}/lessons`)).then(value => { if (alive && value) setLessons(value.lessons) })
    request(() => api<{ llm: LlmStatus }>(`/admin/students/${student.id}`)).then(value => { if (alive && value) onLlmStatus(value.llm) })
    return () => { alive = false }
  }, [student.id, request, onLlmStatus])
  async function open(lesson: Lesson) {
    openRef.current = lesson.id; setOpenLesson(lesson.id); setDetail(null)
    const value = await request(() => api<LessonDetail>(`/admin/students/${student.id}/lessons/${lesson.id}`))
    if (value && openRef.current === lesson.id) setDetail(value)
  }
  return <aside className="student-detail">
    <h2>{student.displayName}</h2><p className="muted">{student.login}</p>
    <button className="secondary" onClick={toggle}>LLM: {student.llmEnabled ? 'включена' : 'выключена'}</button>
    {!lessons ? <p>Загружаем данные…</p> : <>
      <h3>Уроки</h3>
      {lessons.length ? <div className="lesson-list">{lessons.map(l => <button key={l.id} className={openLesson === l.id ? 'lesson-item selected' : 'lesson-item'} aria-pressed={openLesson === l.id} onClick={() => open(l)}>
        <b>Урок {l.number}</b><span>{l.finishedAt ? `завершён ${fmt(l.finishedAt)}` : `в процессе · начат ${fmt(l.startedAt)}`}</span>
      </button>)}</div> : <p className="muted">Уроков пока нет.</p>}
      {openLesson !== null && !detail && <p className="muted">Загружаем урок…</p>}
      {detail && <>
        <h3>Задачи и попытки</h3>
        {detail.tasks.length ? detail.tasks.map(t => <article key={t.id}>
          <b>{t.title}</b><Markdown>{t.statement}</Markdown>
          {t.submissions.length ? t.submissions.map(a => <details key={a.id}><summary className={a.passed ? 'passed' : 'not-passed'}>{a.passed ? '✓ принято' : '× не принято'} · {fmt(a.createdAt)}</summary><pre>{a.sourceCode}</pre>{a.output && <pre>{a.output}</pre>}</details>) : <p className="muted">Попыток не было.</p>}
        </article>) : <p className="muted">Задач в этом уроке не было.</p>}
        <h3>Чат</h3>
        {detail.chat.length ? detail.chat.map(m => <article key={m.id}><small>{m.role === 'STUDENT' ? 'Студент' : 'Помощник'} · {fmt(m.createdAt)}</small><Markdown>{m.content}</Markdown></article>) : <p className="muted">Переписки не было.</p>}
      </>}
    </>}
  </aside>
}
