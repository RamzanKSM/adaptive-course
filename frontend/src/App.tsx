import { FormEvent, useEffect, useState } from 'react'
import { api, ApiError, post } from './api'
import type { Attempt, ChatMessage, Diagnostic, LearningNext, Lesson, MeResponse, Progress, Student, User } from './types'

const UNKNOWN = 'Не знаю'
const codeFallback = 'public class Solution {\n    public static void main(String[] args) {\n        // Напишите решение здесь\n    }\n}\n'
const fmt = (value?: string) => value && new Date(value).toLocaleString('ru-RU')

export default function App() {
  const [me, setMe] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [notice, setNotice] = useState('')
  const [error, setError] = useState('')
  const request = async <T,>(action: () => Promise<T>) => {
    setError(''); setNotice('')
    try { return await action() } catch (e) { setError(e instanceof Error ? e.message : 'Не удалось выполнить запрос'); return undefined }
  }
  useEffect(() => { request(() => api<MeResponse>('/auth/me')).then(value => { if (value) setMe(value.user); setLoading(false) }) }, [])
  if (loading) return <div className="center">Загружаем…</div>
  if (!me) return <Login onLogin={setMe} onError={setError} error={error} />
  return <main className="app"><header><div><b>Java Tutor</b><span>{me.displayName} · {me.role === 'STUDENT' ? 'Студент' : 'Преподаватель'}</span></div><button className="quiet" onClick={() => request(() => post<void>('/auth/logout')).then(() => setMe(null))}>Выйти</button></header>{error && <div className="flash error">{error}</div>}{notice && <div className="flash">{notice}</div>}{me.role === 'STUDENT' ? <StudentPage request={request} /> : <TeacherPage request={request} />}</main>
}

function Login({ onLogin, onError, error }: { onLogin: (me: User) => void; onError: (message: string) => void; error: string }) {
  const [login, setLogin] = useState(''); const [password, setPassword] = useState(''); const [sending, setSending] = useState(false)
  async function submit(e: FormEvent) { e.preventDefault(); setSending(true); try { onLogin((await post<MeResponse>('/auth/login', { login, password })).user) } catch (err) { onError(err instanceof Error ? err.message : 'Не удалось войти') } finally { setSending(false) } }
  return <main className="login"><section className="card"><p className="eyebrow">АДАПТИВНОЕ ОБУЧЕНИЕ</p><h1>Учимся Java в своём темпе</h1><p>Войдите по данным, которые выдал преподаватель.</p><form onSubmit={submit}><label>Логин<input required value={login} onChange={e => setLogin(e.target.value)} autoComplete="username" /></label><label>Пароль<input required type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" /></label>{error && <p className="form-error">{error}</p>}<button disabled={sending}>{sending ? 'Входим…' : 'Войти'}</button></form></section></main>
}

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>

function StudentPage({ request }: { request: Request }) {
  const [diagnostic, setDiagnostic] = useState<Diagnostic | null>(null); const [lesson, setLesson] = useState<LearningNext | null>(null); const [progress, setProgress] = useState<Progress | null>(null); const [tab, setTab] = useState<'lesson' | 'progress'>('lesson')
  const load = () => { request(() => api<Diagnostic>('/diagnostic')).then(d => { if (!d) return; setDiagnostic(d); if (d.completed) request(() => api<{ lesson: Lesson | null }>('/lessons/current')).then(current => { if (current?.lesson) request(() => api<LearningNext>('/learning/next')).then(value => { if (value) setLesson(value) }); else setLesson(null) }) }); request(() => api<Progress>('/progress')).then(value => { if (value) setProgress(value) }) }
  useEffect(load, [])
  if (diagnostic && !diagnostic.completed) return <DiagnosticForm diagnostic={diagnostic} request={request} onDone={load} />
  return <><nav className="tabs"><button className={tab === 'lesson' ? 'active' : ''} onClick={() => setTab('lesson')}>Текущий урок</button><button className={tab === 'progress' ? 'active' : ''} onClick={() => setTab('progress')}>Мой прогресс</button></nav>{tab === 'progress' ? <ProgressView progress={progress} /> : <LessonView lesson={lesson} request={request} refresh={load} />}</>
}

function DiagnosticForm({ diagnostic, request, onDone }: { diagnostic: Diagnostic; request: Request; onDone: () => void }) {
  const [index, setIndex] = useState(0); const [answers, setAnswers] = useState<Record<string, number | null>>({}); const question = diagnostic.questions[index]; const last = index === diagnostic.questions.length - 1
  const save = async () => { const body = { answers: diagnostic.questions.map(q => ({ questionId: q.id, selectedOption: answers[q.id] ?? null })) }; const done = await request(() => post('/diagnostic', body)); if (done) onDone() }
  return <section className="diagnostic"><p className="eyebrow">ПЕРВИЧНАЯ ДИАГНОСТИКА</p><h1>Поймём, с чего начать</h1><p>Здесь нет оценки. Если не уверены, выберите «Не знаю».</p><div className="meter"><i style={{ width: `${((index + 1) / diagnostic.questions.length) * 100}%` }} /></div><small>Вопрос {index + 1} из {diagnostic.questions.length}</small><article className="card question"><h2>{question.prompt}</h2><div className="choices">{[...question.options, UNKNOWN].map((option, optionIndex) => <label key={option}><input type="radio" checked={answers[question.id] === (optionIndex === question.options.length ? null : optionIndex)} onChange={() => setAnswers({ ...answers, [question.id]: optionIndex === question.options.length ? null : optionIndex })} />{option}</label>)}</div></article><div className="actions">{index > 0 && <button className="secondary" onClick={() => setIndex(index - 1)}>Назад</button>}{last ? <button disabled={answers[question.id] === undefined} onClick={save}>Завершить диагностику</button> : <button disabled={answers[question.id] === undefined} onClick={() => setIndex(index + 1)}>Далее</button>}</div></section>
}

function LessonView({ lesson, request, refresh }: { lesson: LearningNext | null; request: Request; refresh: () => void }) {
  const [working, setWorking] = useState(false)
  async function start() { setWorking(true); await request(() => post<{ lesson: Lesson }>('/lessons/start')).then(l => { if (l) refresh() }); setWorking(false) }
  if (!lesson) return <section className="empty"><h1>Урок ещё не начат</h1><p>Сервис выберет следующую тему по результатам диагностики и предыдущим занятиям.</p><button disabled={working} onClick={start}>{working ? 'Готовим урок…' : 'Начать урок'}</button></section>
  const title = lesson.skill?.title ?? (lesson.reason === 'NO_DUE_SKILL' ? 'На сегодня задач больше нет' : 'Текущий урок')
  return <section className="lesson"><div className="lesson-heading"><div><p className="eyebrow">АКТИВНЫЙ УРОК · {lesson.lesson.number}</p><h1>{title}</h1></div><button className="secondary" onClick={() => request(() => post(`/lessons/${lesson.lesson.id}/finish`)).then(refresh)}>Завершить урок</button></div>{lesson.explanation && <article className="explanation"><h2>Объяснение</h2><p>{lesson.explanation.content}</p></article>}{lesson.task ? <div className="lesson-grid"><TaskEditor key={lesson.task.id} task={lesson.task} request={request} onPassed={refresh} /><Chat llm={lesson.llm} request={request} /></div> : <article className="empty"><h2>{lesson.reason === 'NO_DUE_SKILL' ? 'Урок можно завершить' : 'Задача ещё не подготовлена'}</h2><p>{lesson.reason === 'NO_TASK_AVAILABLE' ? 'Подходящей задачи в банке пока нет. Преподаватель увидит это состояние.' : lesson.reason === 'NO_DUE_SKILL' ? 'Все задачи этого урока выполнены.' : 'Контент урока загружается.'}</p><Chat llm={lesson.llm} request={request} /></article>}</section>
}

function TaskEditor({ task, request, onPassed }: { task: { id: string; title: string; statement: string; starterCode?: string }; request: Request; onPassed: () => void }) {
  const [code, setCode] = useState(task.starterCode || codeFallback); const [attempt, setAttempt] = useState<Attempt | null>(null); const [sending, setSending] = useState(false)
  async function submit() { setSending(true); const result = await request(() => post<Attempt>('/attempts', { taskId: task.id, sourceCode: code })); if (result) { setAttempt(result); if (result.passed) onPassed() }; setSending(false) }
  return <section className="task"><h2>{task.title}</h2><p>{task.statement}</p><label className="code-label">Решение на Java<textarea className="code" spellCheck={false} value={code} onChange={e => setCode(e.target.value)} /></label><button disabled={sending} onClick={submit}>{sending ? 'Проверяем…' : 'Отправить на проверку'}</button>{attempt && <div className={`result ${attempt.passed ? 'success' : 'failed'}`}><b>{attempt.passed ? 'Решение принято' : 'Нужно доработать'}</b>{attempt.output && <pre>{attempt.output}</pre>}</div>}</section>
}

function Chat({ llm, request }: { llm?: { available: boolean; reason?: string }; request: Request }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]); const [text, setText] = useState(''); const [status, setStatus] = useState(''); const [available, setAvailable] = useState(llm?.available); const [sending, setSending] = useState(false)
  useEffect(() => { request(() => api<{ messages: ChatMessage[]; llm: { available: boolean; reason?: string } }>('/chat')).then(value => { if (value) { setMessages(value.messages); setAvailable(value.llm.available); setStatus(value.llm.available ? '' : (value.llm.reason ?? 'LLM сейчас недоступна')) } }) }, [])
  async function send(e: FormEvent) { e.preventDefault(); const content = text.trim(); if (!content) return; setSending(true); setStatus(''); setMessages(m => [...m, { id: `local-${Date.now()}`, role: 'STUDENT', content, createdAt: new Date().toISOString() }]); setText(''); const result = await request(() => post<{ message: ChatMessage }>('/chat', { content })); if (result) setMessages(m => [...m, result.message]); setSending(false) }
  return <aside className="chat"><h2>Спросить преподавателя</h2><div className="messages">{messages.length ? messages.map(m => <div key={m.id} className={`message ${m.role.toLowerCase()}`}><small>{m.role === 'STUDENT' ? 'Вы' : 'Помощник'} {fmt(m.createdAt)}</small><p>{m.content}</p></div>) : <p className="muted">Задайте вопрос по текущей задаче.</p>}</div>{status && <p className="muted">{status}</p>}{available === false ? <p className="muted">{llm?.reason ?? 'Помощник временно недоступен.'}</p> : <form onSubmit={send}><textarea value={text} onChange={e => setText(e.target.value)} placeholder="Ваш вопрос" /><button disabled={sending}>{sending ? 'Отправляем…' : 'Отправить'}</button></form>}</aside>
}

function ProgressView({ progress }: { progress: Progress | null }) { return <section><h1>Мой прогресс</h1>{!progress ? <p>Загружаем…</p> : <div className="card"><div className="skills">{progress.skills.length ? progress.skills.map(skill => <div key={skill.skillCode}><span>{skill.title}</span><div className="bar"><i style={{ width: `${skill.mastered ? 100 : Math.min(90, skill.iterationSuccesses * 30)}%` }} /></div><small>{skill.mastered ? 'Освоено' : `${skill.completedIterations}/3 итераций · ${skill.iterationSuccesses}/3 успешных решений`}</small></div>) : <p className="muted">Прогресс появится после первого решения.</p>}</div></div>}</section> }

function TeacherPage({ request }: { request: Request }) {
  const [students, setStudents] = useState<Student[]>([]); const [selected, setSelected] = useState<Student | null>(null); const [globalLlm, setGlobalLlm] = useState<boolean | null>(null); const [name, setName] = useState(''); const [login, setLogin] = useState(''); const [password, setPassword] = useState('')
  const load = () => request(() => api<{ students: Student[] }>('/admin/students')).then(s => { if (s) setStudents(s.students) })
  useEffect(() => { load() }, [])
  async function create(e: FormEvent) { e.preventDefault(); const student = await request(() => post<Student>('/admin/students', { displayName: name, login, password })); if (student) { setName(''); setLogin(''); setPassword(''); load() } }
  async function toggle(student: Student) { const updated = await request(() => api<{ id: string; enabled: boolean }>(`/admin/students/${student.id}/llm`, { method: 'PATCH', body: JSON.stringify({ enabled: !student.llmEnabled }) })); if (updated) { const merged = { ...student, llmEnabled: updated.enabled }; setStudents(xs => xs.map(x => x.id === updated.id ? { ...x, llmEnabled: updated.enabled } : x)); setSelected(merged) } }
  async function toggleGlobal() { const updated = await request(() => api<{ enabled: boolean }>('/admin/llm', { method: 'PATCH', body: JSON.stringify({ enabled: !globalLlm }) })); if (updated) setGlobalLlm(updated.enabled) }
  return <section className="admin"><div><p className="eyebrow">ПРЕПОДАВАТЕЛЬ</p><h1>Студенты</h1><div className="card"><h2>LLM для курса</h2><p className="muted">{globalLlm === null ? 'Состояние будет получено после выбора студента.' : globalLlm ? 'Включена' : 'Выключена'}</p><button className="secondary" onClick={toggleGlobal}>Переключить LLM</button></div><div className="card"><h2>Создать учётную запись</h2><form className="inline-form" onSubmit={create}><input placeholder="Имя" required value={name} onChange={e => setName(e.target.value)} /><input placeholder="Логин" required value={login} onChange={e => setLogin(e.target.value)} /><input placeholder="Пароль" required value={password} onChange={e => setPassword(e.target.value)} /><button>Создать</button></form></div><div className="student-list">{students.map(s => <button key={s.id} className={selected?.id === s.id ? 'student selected' : 'student'} onClick={() => setSelected(s)}><span><b>{s.displayName}</b><small>{s.login}</small></span><i className={s.llmEnabled ? 'on' : ''}>LLM</i></button>)}</div></div>{selected && <StudentDetail student={selected} request={request} toggle={() => toggle(selected)} onLlmStatus={enabled => setGlobalLlm(enabled)} />}</section>
}

function StudentDetail({ student, request, toggle, onLlmStatus }: { student: Student; request: Request; toggle: () => void; onLlmStatus: (enabled: boolean) => void }) {
  const [data, setData] = useState<{ lessons: Lesson[] } | null>(null); const [detail, setDetail] = useState<{ chat: ChatMessage[]; tasks: { id: string; title: string; statement: string; submissions: (Attempt & { sourceCode: string; createdAt: string })[] }[] } | null>(null)
  useEffect(() => { setDetail(null); request(() => api<{ lessons: Lesson[] }>(`/admin/students/${student.id}/lessons`)).then(value => { if (value) setData(value) }); request(() => api<{ llm: { globallyEnabled: boolean } }>(`/admin/students/${student.id}`)).then(value => { if (value) onLlmStatus(value.llm.globallyEnabled) }) }, [student.id])
  return <aside className="student-detail"><h2>{student.displayName}</h2><p>{student.login}</p><button className="secondary" onClick={toggle}>LLM: {student.llmEnabled ? 'включена' : 'выключена'}</button>{!data ? <p>Загружаем данные…</p> : <><h3>Уроки</h3>{data.lessons.length ? data.lessons.map(l => <article className="clickable" key={l.id} onClick={() => request(() => api<typeof detail>(`/admin/students/${student.id}/lessons/${l.id}`)).then(v => { if (v) setDetail(v) })}><b>Урок {l.number}</b><p>{l.finishedAt ? `завершён ${fmt(l.finishedAt)}` : 'в процессе'}</p></article>) : <p className="muted">Уроков пока нет.</p>}{detail && <><h3>Задачи и попытки</h3>{detail.tasks.map(t => <article key={t.id}><b>{t.title}</b><p>{t.statement}</p>{t.submissions.map(a => <details key={a.id}><summary>{a.passed ? '✓ принято' : '× не принято'} · {fmt(a.createdAt)}</summary><pre>{a.sourceCode}</pre><pre>{a.output}</pre></details>)}</article>)}<h3>Чат</h3>{detail.chat.map(m => <article key={m.id}><b>{m.role === 'STUDENT' ? 'Студент' : 'LLM'}:</b> {m.content}</article>)}</>}</>}</aside>
}
