import { createContext, CSSProperties, FormEvent, KeyboardEvent, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import CodeMirror from '@uiw/react-codemirror'
import { java } from '@codemirror/lang-java'
import { python } from '@codemirror/lang-python'
import ReactMarkdown from 'react-markdown'
import { api, ApiError, humanize, onUnauthorized, patch, post, remove } from './api'
import { achievements, commonAchievements, experience, skillState, type SkillState, ITERATIONS, iterationTasks, parseDate, skillPercent, skillStarted, streak, XP } from './game'
import { Burst, Icon, initials, Ring, ToastProvider, useCountUp, useToast } from './fx'
import { LlmAnalytics } from './analytics'
import { LlmSettingsView } from './settings'
import { ConsolePanel, consoleText, type ConsoleOrigin } from './console'
import { DangerFrame, HardModeDialog, HardModeSwitch, HeaderTapes } from './hardmode'
import { GroupFilter, GroupOptions, groupCounts, inGroup, NO_GROUP, useGroupFilter } from './groups'
import type { ActiveLesson, Attempt, ChatMessage, ChatQuota, ConsoleRun, CourseLanguage, Diagnostic, Id, LearningNext, Lesson, LessonDetail, LlmStatus, MeResponse, Progress, SkillProgress, Student, Task, User, Review, OutputMismatch } from './types'

const UNKNOWN = 'Не знаю'
const fmt = (value?: string | null) => {
  if (!value) return ''
  const date = parseDate(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString('ru-RU')
}

const COURSES = {
  JAVA: {
    id: 'JAVA', key: 'java', title: 'Java', logo: 'J',
    fallback: 'public class Solution {\n    public static void main(String[] args) {\n        // Напишите решение здесь\n    }\n}\n',
    pitch: 'Строгая типизация и классический ООП. Язык бэкенда, Android и больших систем.', tags: ['ООП', 'Бэкенд', 'Android'],
  },
  PYTHON: {
    id: 'PYTHON', key: 'python', title: 'Python', logo: 'Py',
    fallback: '# Напиши решение здесь\n',
    pitch: 'Короткий понятный синтаксис. Автоматизация, анализ данных, бэкенд и машинное обучение.', tags: ['Простой синтаксис', 'Данные', 'Автоматизация'],
  },
} as const
type Course = (typeof COURSES)[CourseLanguage]
// Stable references: a new extensions array on every render would make CodeMirror reconfigure the editor.
const EDITOR_EXTENSIONS = { JAVA: [java()], PYTHON: [python()] }
const LANGUAGES = Object.keys(COURSES) as CourseLanguage[]
const CourseContext = createContext<Course>(COURSES.JAVA)
const useCourse = () => useContext(CourseContext)
/** Adds the course to a student API path; the backend treats a missing value as Java. */
const withCourse = (path: string, language: CourseLanguage) => `${path}${path.includes('?') ? '&' : '?'}language=${language}`
const LANGUAGE_KEY = 'rmzn.language'
const storedLanguage = (): CourseLanguage | null => {
  try { const value = localStorage.getItem(LANGUAGE_KEY); return value === 'JAVA' || value === 'PYTHON' ? value : null } catch { return null }
}
const storeLanguage = (language: CourseLanguage) => { try { localStorage.setItem(LANGUAGE_KEY, language) } catch { /* private mode: choice lasts for this page only */ } }

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

const Spinner = () => <span className="spinner" aria-hidden="true" />

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>

export default function App() {
  return <ToastProvider><Shell /></ToastProvider>
}

function Shell() {
  const [me, setMe] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [language, setLanguage] = useState<CourseLanguage | null>(storedLanguage)
  const chooseLanguage = (value: CourseLanguage) => { storeLanguage(value); setLanguage(value); window.scrollTo({ top: 0 }) }
  const isStudent = me?.role === 'STUDENT'
  // The accent palette follows the course; the login screen and the teacher view keep the default one.
  useEffect(() => {
    const root = document.documentElement
    if (isStudent && language) root.dataset.lang = COURSES[language].key; else delete root.dataset.lang
  }, [isStudent, language])
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
  // The header stays on top; sticky panels below it (chat, student card, messages) are offset by its real height.
  const header = useRef<HTMLElement>(null)
  const [scrolled, setScrolled] = useState(false)
  useEffect(() => {
    const element = header.current
    if (!element) return
    const root = document.documentElement
    const observer = new ResizeObserver(() => root.style.setProperty('--topbar-h', `${element.offsetHeight}px`))
    observer.observe(element)
    // --scroll-y lets the header's copy of the hard-mode tapes follow the page without re-rendering.
    const onScroll = () => { setScrolled(window.scrollY > 4); root.style.setProperty('--scroll-y', `${window.scrollY}px`) }
    onScroll(); window.addEventListener('scroll', onScroll, { passive: true })
    return () => { observer.disconnect(); window.removeEventListener('scroll', onScroll) }
  }, [me])
  // Hard mode: the teacher allows it, the student switches it on; it works only in a course passed once. The whole screen shows it.
  const hardReady = !!(language && me?.hardModeCourses?.[language]?.ready)
  const hardOn = isStudent && !!me?.hardModeOn && hardReady
  const [hardDialog, setHardDialog] = useState(false); const [hardBusy, setHardBusy] = useState(false)
  /** Bumped after a hard-mode switch: the lesson loads again, since the server may have replaced the current task. */
  const [lessonReload, setLessonReload] = useState(0)
  const toast = useToast()
  /** Re-reads the user quietly (readiness changes as the student learns); null on failure. */
  const refreshMe = useCallback(() => api<MeResponse>('/auth/me').then(value => { setMe(value.user); return value.user }).catch(() => null), [])
  const shownLanguage = useRef(language)
  useEffect(() => {
    if (shownLanguage.current === language) return
    shownLanguage.current = language
    if (isStudent && language) refreshMe()
  }, [isStudent, language, refreshMe])
  useEffect(() => {
    const root = document.documentElement
    if (hardOn) root.dataset.hard = 'on'; else delete root.dataset.hard
    return () => { delete root.dataset.hard }
  }, [hardOn])
  async function setHardMode(enabled: boolean) {
    setHardDialog(false); setHardBusy(true)
    const result = await request(() => patch<{ hardModeOn: boolean; replacedTask?: boolean }>('/me/hard-mode', { enabled, language }))
    setHardBusy(false)
    if (!result) { if (enabled) refreshMe(); return } // e.g. HARD_MODE_NOT_READY: the switch falls back to locked
    setMe(m => m && { ...m, hardModeOn: result.hardModeOn })
    setLessonReload(n => n + 1)
    toast(result.hardModeOn
      ? { tone: 'reward', icon: 'flame', title: 'Hard mode включён', text: `${result.replacedTask ? 'Текущая задача заменена на hard-задачу. ' : ''}Следующие задачи — алгоритмические, +${XP.hardTask} XP за каждую` }
      : { tone: 'info', icon: 'check', title: 'Hard mode выключен', text: result.replacedTask ? 'Текущая задача заменена на обычную задачу' : 'Следующие задачи будут обычными' })
  }
  /** A locked switch: the course may have become ready meanwhile — otherwise explain what is left. */
  async function unlockHardMode() {
    if (!language) return
    setHardBusy(true)
    const fresh = await refreshMe()
    setHardBusy(false)
    const course = (fresh ?? me)?.hardModeCourses?.[language]
    if (course?.ready) { if (!fresh?.hardModeOn) setHardDialog(true); return }
    const left = course ? `: осталось тем — ${course.remaining}` : ''
    toast({ tone: 'info', icon: 'lock', title: 'Hard mode пока закрыт', text: `Пройди хотя бы одну итерацию по каждой теме курса ${COURSES[language].title}${left}. Темы, подтверждённые диагностикой, уже засчитаны.` })
  }
  const login = (user: User) => { setError(''); setMe(user) }
  const logout = async () => { await request(() => post<void>('/auth/logout')); setError(''); setMe(null) }
  if (loading) return <div className="center"><Spinner /><span>Загружаем…</span></div>
  if (!me) return <Login onLogin={login} onError={setError} error={error} />
  return <main className={`app ${hardOn ? 'hard' : ''}`}>
    {hardOn && <DangerFrame />}
    {hardDialog && <HardModeDialog onConfirm={() => setHardMode(true)} onCancel={() => setHardDialog(false)} />}
    <header ref={header} className={`topbar ${scrolled ? 'scrolled' : ''}`}>
      {hardOn && <HeaderTapes />}
      <div className="brand"><span className="logo" aria-hidden="true">R</span><b>Rmzn Tutor</b></div>
      {isStudent && language && <LanguageSwitch value={language} onChange={chooseLanguage} />}
      <div className={`user-chip ${hardOn ? 'on-fire' : ''}`}>
        {isStudent && me.hardModeAllowed && language && <HardModeSwitch on={hardOn} locked={!hardReady} busy={hardBusy} onToggle={() => !hardReady ? unlockHardMode() : hardOn ? setHardMode(false) : setHardDialog(true)} />}
        <span className="avatar" aria-hidden="true">{initials(me.displayName)}</span>
        <span className="user-meta"><b>{me.displayName}</b><small>{hardOn ? 'Hard mode' : me.role === 'STUDENT' ? 'Студент' : 'Преподаватель'}</small></span>
        <button className="icon-button" onClick={logout} aria-label="Выйти" title="Выйти"><Icon name="logout" /></button>
      </div>
    </header>
    {error && <div className="flash error" role="alert"><span>{error}</span><button className="flash-close" aria-label="Скрыть сообщение" onClick={() => setError('')}><Icon name="x" size={16} /></button></div>}
    {!isStudent ? <TeacherPage request={request} />
      : !language ? <LanguagePicker request={request} onPick={chooseLanguage} />
        : <CourseContext.Provider value={COURSES[language]}><StudentPage key={`${language}:${lessonReload}`} request={request} /></CourseContext.Provider>}
  </main>
}

function LanguageSwitch({ value, onChange }: { value: CourseLanguage; onChange: (language: CourseLanguage) => void }) {
  return <nav className="lang-switch" aria-label="Курс" style={{ '--active': LANGUAGES.indexOf(value) } as CSSProperties}>
    <span className="segmented-thumb" aria-hidden="true" />
    {LANGUAGES.map(language => <button key={language} className={language === value ? 'active' : ''} aria-pressed={language === value} onClick={() => language !== value && onChange(language)}>
      <span className={`lang-dot ${COURSES[language].key}`} aria-hidden="true" />{COURSES[language].title}
    </button>)}
  </nav>
}

/** First visit: the student chooses a course. Both stay available later through the switch in the header. */
function LanguagePicker({ request, onPick }: { request: Request; onPick: (language: CourseLanguage) => void }) {
  const [solved, setSolved] = useState<Partial<Record<CourseLanguage, number>>>({})
  useEffect(() => {
    for (const language of LANGUAGES) request(() => api<Progress>(withCourse('/progress', language))).then(value => { if (value) setSolved(s => ({ ...s, [language]: experience(value).solved })) })
  }, [request])
  return <section className="picker">
    <div className="enter">
      <p className="eyebrow">Выбор курса</p>
      <h1 className="display small">Что будем учить?</h1>
      <p className="muted">Оба курса устроены одинаково: диагностика, объяснения и задачи от простых к сложным. Переключиться можно в любой момент — прогресс у каждого курса свой.</p>
    </div>
    <div className="picker-grid">{LANGUAGES.map((language, i) => {
      const course = COURSES[language]
      return <button key={language} className={`lang-card ${course.key}`} onClick={() => onPick(language)} style={{ animationDelay: `${120 + i * 80}ms` }}>
        <span className="lang-logo" aria-hidden="true">{course.logo}</span>
        <h2>{course.title}</h2>
        <p>{course.pitch}</p>
        <ul>{course.tags.map(tag => <li key={tag}>{tag}</li>)}</ul>
        {!!solved[language] && <span className="stat-line">Уже решено задач: {solved[language]}</span>}
        <span className="go">{solved[language] ? 'Продолжить' : 'Начать'} {course.title} <Icon name="arrow" /></span>
      </button>
    })}</div>
  </section>
}

function Login({ onLogin, onError, error }: { onLogin: (me: User) => void; onError: (message: string) => void; error: string }) {
  const [login, setLogin] = useState(''); const [password, setPassword] = useState(''); const [sending, setSending] = useState(false)
  async function submit(e: FormEvent) {
    e.preventDefault(); setSending(true); onError('')
    try { onLogin((await post<MeResponse>('/auth/login', { login: login.trim(), password })).user) }
    catch (err) { onError(err instanceof Error ? err.message : 'Не удалось войти'); setSending(false) }
  }
  return <main className="login">
    <section className="login-hero" aria-hidden="false">
      <div className="blob blob-a" /><div className="blob blob-b" />
      <div className="brand light"><span className="logo" aria-hidden="true">R</span><b>Rmzn Tutor</b></div>
      <h1 className="display">Учим код.<br /><span className="accent">В твоём темпе.</span></h1>
      <p className="hero-lead">Java и Python с нуля: короткая диагностика, понятные объяснения и задачи, которые становятся сложнее ровно тогда, когда ты готов.</p>
      <div className="code-card" aria-hidden="true">
        <span className="dots"><i /><i /><i /></span>
        <code>streak = <span className="n">1</span>{'\n'}<span className="k">while</span> learning:{'\n'}    streak += <span className="n">1</span>{'\n'}print(<span className="s">"Level up!"</span>)<span className="caret" /></code>
      </div>
      <ul className="hero-points"><li><Icon name="code" size={16} /> Java и Python</li><li><Icon name="target" size={16} /> 3 задачи на итерацию</li><li><Icon name="flame" size={16} /> Серии и достижения</li><li><Icon name="chat" size={16} /> Помощник рядом</li></ul>
    </section>
    <section className="login-panel">
      <form className="card login-card enter" onSubmit={submit}>
        <p className="eyebrow">Вход</p>
        <h2 className="title">С возвращением</h2>
        <p className="muted">Войди по данным, которые выдал преподаватель.</p>
        <label>Логин<input required value={login} onChange={e => setLogin(e.target.value)} autoComplete="username" autoCapitalize="none" spellCheck={false} /></label>
        <label>Пароль<input required type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" /></label>
        {error && <p className="form-error shake" role="alert" key={error}>{error}</p>}
        <button className="primary big" disabled={sending}>{sending ? <><Spinner /> Входим…</> : <>Войти <Icon name="arrow" /></>}</button>
      </form>
    </section>
  </main>
}

type LoadState = 'loading' | 'ready' | 'failed'

function StudentPage({ request }: { request: Request }) {
  const [diagnostic, setDiagnostic] = useState<Diagnostic | null>(null)
  const [lesson, setLesson] = useState<LearningNext | null>(null)
  const [state, setState] = useState<LoadState>('loading')
  /** The open lesson while its next task is being prepared: it can be finished without waiting. */
  const [preparing, setPreparing] = useState<Lesson | null>(null)
  const [progress, setProgress] = useState<Progress | null>(null)
  const [otherProgress, setOtherProgress] = useState<Partial<Record<CourseLanguage, Progress>>>({})
  const [othersReady, setOthersReady] = useState(false)
  const [tab, setTab] = useState<'lesson' | 'progress'>('lesson')
  const toast = useToast()
  const course = useCourse()
  const loadId = useRef(0)
  const loadProgress = useCallback(() => request(() => api<Progress>(withCourse('/progress', course.id))).then(value => { if (value) setProgress(value) }), [request, course.id])
  // Other courses only feed the shared achievements, so they load once and quietly.
  useEffect(() => {
    Promise.allSettled(LANGUAGES.filter(language => language !== course.id).map(language =>
      api<Progress>(withCourse('/progress', language)).then(value => setOtherProgress(p => ({ ...p, [language]: value })))))
      .then(() => setOthersReady(true))
  }, [course.id])
  const load = useCallback(async () => {
    const id = ++loadId.current
    const stale = () => id !== loadId.current
    setState('loading'); setPreparing(null)
    loadProgress()
    const d = await request(() => api<Diagnostic>(withCourse('/diagnostic', course.id)))
    if (stale()) return
    if (!d) return setState('failed')
    setDiagnostic(d)
    if (!d.completed) return setState('ready')
    const current = await request(() => api<{ lesson: Lesson | null }>(withCourse('/lessons/current', course.id)))
    if (stale()) return
    if (!current) return setState('failed')
    if (!current.lesson) { setLesson(null); return setState('ready') }
    setPreparing(current.lesson)
    // A request the student left (finished the lesson, switched course) is ignored, its error too.
    const next = await request(() => api<LearningNext>(withCourse('/learning/next', course.id)).catch(e => { if (stale()) return undefined; throw e }))
    if (stale()) return
    setPreparing(null)
    if (!next) return setState('failed')
    // Finished elsewhere (another tab, the teacher, a logout) while the task was being prepared.
    setLesson(next.reason === 'LESSON_FINISHED' ? null : next); setState('ready')
  }, [request, loadProgress, course.id])
  useEffect(() => { load() }, [load])

  // Celebrate milestones that the attempt response reveals (iteration closed, topic mastered), then refresh stats.
  const onProgress = useCallback((skills: SkillProgress[]) => {
    setProgress(previous => {
      if (previous) for (const skill of skills) {
        const before = previous.skills.find(s => s.skillCode === skill.skillCode)
        if (!before) continue
        if (skill.mastered && !before.mastered) toast({ tone: 'reward', icon: 'award', title: `Тема освоена: ${skill.title}`, text: `+${XP.mastery} XP за полное освоение` })
        else if (skill.completedIterations > before.completedIterations) toast({ tone: 'reward', icon: 'target', title: `Итерация ${skill.completedIterations} из ${ITERATIONS} завершена`, text: `${skill.title} · +${XP.iteration} XP` })
      }
      return previous ? { ...previous, skills } : { skills }
    })
    loadProgress()
  }, [toast, loadProgress])

  // Announce achievements unlocked during this session (not the ones already unlocked on first load).
  const unlocked = useRef<Set<string> | null>(null)
  useEffect(() => {
    // Wait for every course: otherwise shared badges would look "new" the moment the other course loads.
    if (!progress || !othersReady) return
    const now = [...achievements(progress, course.id), ...commonAchievements({ ...otherProgress, [course.id]: progress })].filter(a => a.unlocked)
    if (unlocked.current) for (const a of now) if (!unlocked.current.has(a.id)) toast({ tone: 'reward', icon: a.icon, title: `Достижение: ${a.title}`, text: a.description })
    unlocked.current = new Set(now.map(a => a.id))
  }, [progress, otherProgress, othersReady, toast, course.id])

  if (!diagnostic) return state === 'failed'
    ? <section className="empty-state enter"><h1 className="title">Не удалось загрузить данные</h1><button className="primary" onClick={load}><Icon name="refresh" /> Повторить</button></section>
    : <div className="center"><Spinner /><span>Загружаем…</span></div>
  if (!diagnostic.completed) return <DiagnosticForm diagnostic={diagnostic} request={request} onDone={load} />
  const currentSkill = lesson?.skill ? progress?.skills.find(s => s.skillCode === lesson.skill?.code) : undefined
  return <>
    {progress && <Hud progress={progress} />}
    <nav className="segmented" role="tablist" style={{ '--active': tab === 'lesson' ? 0 : 1 } as CSSProperties}>
      <span className="segmented-thumb" aria-hidden="true" />
      <button role="tab" aria-selected={tab === 'lesson'} className={tab === 'lesson' ? 'active' : ''} onClick={() => setTab('lesson')}><Icon name="code" size={16} /> Текущий урок</button>
      <button role="tab" aria-selected={tab === 'progress'} className={tab === 'progress' ? 'active' : ''} onClick={() => setTab('progress')}><Icon name="chart" size={16} /> Мой прогресс</button>
    </nav>
    {/* Both tabs stay mounted so switching to progress does not discard the code in the editor. */}
    <div hidden={tab !== 'progress'} className={tab === 'progress' ? 'enter' : ''}><ProgressView progress={progress} otherProgress={otherProgress} /></div>
    <div hidden={tab !== 'lesson'} className={tab === 'lesson' ? 'enter' : ''}>
      {state === 'loading' ? <LessonSkeleton lesson={preparing} request={request} onFinished={load} />
        : state === 'failed' ? <section className="empty-state enter"><h2 className="title">Не удалось загрузить урок</h2><button className="primary" onClick={load}><Icon name="refresh" /> Повторить</button></section>
          : <LessonView lesson={lesson} skillProgress={currentSkill} request={request} refresh={load} onProgress={onProgress} />}
    </div>
  </>
}

function Hud({ progress }: { progress: Progress }) {
  const level = experience(progress)
  const days = streak(progress.activity)
  const xp = useCountUp(level.xp)
  return <section className="hud enter" aria-label="Твой прогресс">
    <div className="hud-level">
      <Ring value={level.into / level.need} size={58}><b>{level.level}</b></Ring>
      <div className="hud-level-text">
        <small>Уровень {level.level}</small>
        <b>{level.rank}</b>
        <div className="xp-bar" role="progressbar" aria-valuemin={0} aria-valuemax={level.need} aria-valuenow={level.into} aria-label="Опыт до следующего уровня"><i style={{ width: `${(level.into / level.need) * 100}%` }} /></div>
        <small className="xp-caption"><span className="tabular">{xp}</span> XP · ещё {level.need - level.into} до уровня {level.level + 1}</small>
      </div>
    </div>
    <div className={`hud-stat streak ${days.activeToday ? 'lit' : ''}`}>
      <span className="hud-icon flame"><Icon name="flame" size={22} /></span>
      <div><b className="tabular">{days.count}</b><small>{days.count === 1 ? 'день подряд' : days.count >= 2 && days.count <= 4 ? 'дня подряд' : 'дней подряд'}</small></div>
      <div className="week" aria-label="Активность за неделю">{days.week.map((d, i) => <span key={i} className={`${d.active ? 'on' : ''} ${d.today ? 'today' : ''}`} title={d.label}><i />{d.label}</span>)}</div>
    </div>
    <div className="hud-stat course-cover" title="Тема закрыта, если освоена практикой или подтверждена диагностикой">
      <span className="hud-icon bolt"><Icon name="bolt" size={22} /></span>
      <div className="cover-text"><b className="tabular">{level.solved}</b><small>задач решено</small>
        <div className="cover-bar" role="progressbar" aria-label="Закрыто тем курса" aria-valuemin={0} aria-valuemax={level.topics} aria-valuenow={level.closed}><i style={{ width: `${level.topics ? (level.closed / level.topics) * 100 : 0}%` }} /></div>
        <small className="tabular">тем закрыто {level.closed} из {level.topics}</small>
      </div>
    </div>
  </section>
}

function DiagnosticForm({ diagnostic, request, onDone }: { diagnostic: Diagnostic; request: Request; onDone: () => void }) {
  const [index, setIndex] = useState(0); const [answers, setAnswers] = useState<Record<string, number | null>>({}); const [sending, setSending] = useState(false)
  const [direction, setDirection] = useState<'forward' | 'back'>('forward')
  const course = useCourse()
  const toast = useToast()
  const total = diagnostic.questions.length
  const question = diagnostic.questions[index]
  const last = index === total - 1
  useEffect(() => { window.scrollTo({ top: 0, behavior: 'smooth' }) }, [index])
  const answered = question ? answers[question.id] !== undefined : false
  const go = (to: number) => { setDirection(to > index ? 'forward' : 'back'); setIndex(to) }
  const save = async () => {
    setSending(true)
    const body = { answers: diagnostic.questions.map(q => ({ questionId: q.id, selectedOption: answers[q.id] ?? null })) }
    const done = await request(() => post<{ confirmedTopics?: number; gapTopics?: number }>(withCourse('/diagnostic', course.id), body))
    setSending(false)
    if (!done) return
    const confirmed = done.confirmedTopics ?? 0, gaps = done.gapTopics ?? 0
    toast(confirmed
      ? { tone: 'reward', icon: 'sparkle', title: `Диагностика: подтверждено тем — ${confirmed}`, text: `+${confirmed * XP.confirmed} XP · эти темы пропустим, к практике: ${gaps}` }
      : { tone: 'info', icon: 'target', title: 'Диагностика завершена', text: `Начнём с самого начала — тем к практике: ${gaps}` })
    onDone()
  }
  // Keyboard: 1–5 choose an option, Enter moves on — handy for ~60 questions in a row.
  useEffect(() => {
    if (!question) return
    const onKey = (e: globalThis.KeyboardEvent) => {
      if (e.target instanceof HTMLElement && e.target.closest('input[type=text], textarea')) return
      const n = Number(e.key)
      if (n >= 1 && n <= question.options.length + 1) setAnswers(a => ({ ...a, [question.id]: n === question.options.length + 1 ? null : n - 1 }))
      else if (e.key === 'Enter' && answered && !sending) { if (last) save(); else go(index + 1) }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  })
  if (!question) return <section className="empty-state enter"><h1 className="title">Диагностика пока недоступна</h1><p className="muted">Вопросы ещё не загружены. Обратись к преподавателю.</p></section>
  const answeredCount = Object.keys(answers).length
  return <section className="diagnostic">
    <div className="enter">
      <p className="eyebrow">Первичная диагностика · {course.title}</p>
      <h1 className="display small">Поймём, с чего начать</h1>
      <p className="muted">Здесь нет оценки. Если не уверен — смело выбирай «Не знаю», так мы точнее подберём старт.</p>
    </div>
    <div className="diag-progress">
      <div className="meter"><i style={{ width: `${((index + 1) / total) * 100}%` }} /></div>
      <span className="tabular"><b>{index + 1}</b> / {total}</span>
    </div>
    <article className={`card question slide-${direction}`} key={question.id}>
      <div className="question-prompt"><Markdown>{question.prompt}</Markdown></div>
      <div className="choices" role="radiogroup">{[...question.options, UNKNOWN].map((option, optionIndex) => {
        const value = optionIndex === question.options.length ? null : optionIndex
        const unknown = value === null
        return <label key={optionIndex} className={`choice ${unknown ? 'unknown' : ''}`} style={{ animationDelay: `${optionIndex * 40}ms` }}>
          <input type="radio" name={`question-${question.id}`} checked={answers[question.id] === value} onChange={() => setAnswers({ ...answers, [question.id]: value })} />
          <span className="choice-key" aria-hidden="true">{unknown ? '?' : String.fromCharCode(65 + optionIndex)}</span>
          <Markdown inline>{option}</Markdown>
        </label>
      })}</div>
    </article>
    <div className="actions">
      {index > 0 && <button className="ghost" disabled={sending} onClick={() => go(index - 1)}><Icon name="back" /> Назад</button>}
      <span className="kbd-hint">Клавиши <kbd>1</kbd>–<kbd>{question.options.length + 1}</kbd> и <kbd>Enter</kbd> · отвечено {answeredCount}</span>
      {last
        ? <button className="primary" disabled={!answered || sending} onClick={save}>{sending ? <><Spinner /> Сохраняем…</> : <>Завершить диагностику <Icon name="check" /></>}</button>
        : <button className="primary" disabled={!answered} onClick={() => go(index + 1)}>Далее <Icon name="arrow" /></button>}
    </div>
  </section>
}

/**
 * Shown while the lesson content is prepared. The lesson can be finished right away: the server keeps preparing,
 * and a task generated for a finished lesson is given first in the next one. The pending response is ignored.
 */
function LessonSkeleton({ lesson, request, onFinished }: { lesson: Lesson | null; request: Request; onFinished: () => void }) {
  const [working, setWorking] = useState(false)
  const course = useCourse()
  const toast = useToast()
  async function finish(current: Lesson) {
    setWorking(true); const finished = await request(() => post(`/lessons/${current.id}/finish`)); setWorking(false)
    if (!finished) return
    toast({ tone: 'info', icon: 'flag', title: 'Урок завершён', text: 'Если задача ещё готовилась, она будет ждать тебя в начале следующего урока' })
    onFinished()
  }
  return <section className="lesson" aria-busy="true">
    {lesson
      ? <div className="lesson-heading">
        <div className="preparing-title"><p className="eyebrow">{course.title} · Урок {lesson.number}</p><span className="sk sk-title" /></div>
        <button className="ghost" disabled={working} onClick={() => finish(lesson)}>{working ? <><Spinner /> Завершаем…</> : <><Icon name="flag" size={16} /> Завершить урок</>}</button>
      </div>
      : <div className="skeleton-head"><span className="sk sk-line short" /><span className="sk sk-title" /></div>}
    <div className="loading-note"><Spinner /> Готовим урок… Подбор новой задачи может занять до минуты.</div>
    <div className="lesson-grid"><div className="sk sk-card tall" /><div className="sk sk-card" /></div>
  </section>
}

function LessonView({ lesson, skillProgress, request, refresh, onProgress }: { lesson: LearningNext | null; skillProgress?: SkillProgress; request: Request; refresh: () => void; onProgress: (skills: SkillProgress[]) => void }) {
  const [working, setWorking] = useState(false)
  const course = useCourse()
  async function start() { setWorking(true); const started = await request(() => post<{ lesson: Lesson }>(withCourse('/lessons/start', course.id))); setWorking(false); if (started) refresh() }
  async function finish(current: Lesson, hasTask: boolean) {
    if (hasTask && !window.confirm('Текущая задача ещё не решена. Завершить урок?')) return
    setWorking(true); const finished = await request(() => post(`/lessons/${current.id}/finish`)); setWorking(false); if (finished) refresh()
  }
  if (!lesson) return <section className="empty-state start enter">
    <span className="empty-icon"><Icon name="play" size={28} /></span>
    <h1 className="display small">Готов к уроку {course.title}?</h1>
    <p className="muted">Сервис выберет следующую тему по результатам диагностики и предыдущим занятиям.</p>
    <button className="primary big" disabled={working} onClick={start}>{working ? <><Spinner /> Готовим урок…</> : <>Начать урок <Icon name="arrow" /></>}</button>
  </section>
  const finished = lesson.reason === 'NO_DUE_SKILL' || lesson.reason === 'COURSE_COMPLETE'
  const title = lesson.skill?.title ?? (lesson.reason === 'COURSE_COMPLETE' ? 'Все темы курса закрыты' : lesson.reason === 'NO_DUE_SKILL' ? 'На сегодня задач больше нет' : 'Текущий урок')
  const retryable = lesson.reason === 'LLM_GENERATION_FAILED_VALIDATION' || lesson.reason === 'RUNNER_UNAVAILABLE' || lesson.reason === 'LLM_RATE_LIMITED'
  const emptyMessage = lesson.reason === 'NO_TASK_AVAILABLE' ? 'Подходящей задачи в банке пока нет. Преподаватель увидит это состояние.'
    : lesson.reason === 'LLM_GENERATION_FAILED_VALIDATION' ? 'Новая задача не прошла проверку. Попробуй запросить её ещё раз.'
      : lesson.reason === 'RUNNER_UNAVAILABLE' ? `Проверка ${course.title} сейчас недоступна. Попробуй ещё раз позже.`
        : lesson.reason === 'LLM_RATE_LIMITED' ? 'Новые задачи сейчас создаются слишком часто — сработал лимит курса. Попробуй через несколько минут или спроси преподавателя.'
        : lesson.reason === 'COURSE_COMPLETE' ? 'Каждая тема освоена практикой или подтверждена диагностикой — задач для обязательной практики не осталось.'
          : lesson.reason === 'NO_DUE_SKILL' ? 'Все задачи этого урока выполнены — отличная работа! Повторения запланированы на следующие уроки.' : 'Контент урока загружается.'
  return <section className="lesson">
    <div className="lesson-heading enter">
      <div>
        <p className="eyebrow">{course.title} · Урок {lesson.lesson.number}{lesson.skill ? ` · Блок ${lesson.skill.blockNo}` : ''}</p>
        <h1 className="display small">{title}</h1>
      </div>
      <button className="ghost" disabled={working} onClick={() => finish(lesson.lesson, !!lesson.task)}>{working ? <><Spinner /> Завершаем…</> : <><Icon name="flag" size={16} /> Завершить урок</>}</button>
    </div>
    {lesson.explanation && <article className="card explanation enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="book" size={16} /></span> Объяснение</h2>
      <Markdown>{lesson.explanation.content}</Markdown>
    </article>}
    {lesson.task
      ? <TaskWorkspace key={lesson.task.id} task={lesson.task} skillProgress={skillProgress} llm={lesson.llm} request={request} onNext={refresh} onProgress={onProgress} />
      : <div className="lesson-grid enter">
        <article className={`card task empty-task ${finished ? 'done' : ''}`}>
          {finished && <span className="empty-icon success"><Icon name={lesson.reason === 'COURSE_COMPLETE' ? 'award' : 'check'} size={28} /></span>}
          {lesson.reason === 'COURSE_COMPLETE' && <Burst trigger={1} />}
          <h2 className="title">{lesson.reason === 'COURSE_COMPLETE' ? 'Курс пройден' : finished ? 'Урок можно завершить' : 'Задача ещё не подготовлена'}</h2>
          <p className="muted">{emptyMessage}</p>
          {retryable && <button className="secondary" onClick={refresh}><Icon name="refresh" /> Повторить</button>}
        </article>
        <Chat llm={lesson.llm} request={request} />
      </div>}
  </section>
}

type ConsoleState = { run: ConsoleRun; origin: ConsoleOrigin }

function TaskWorkspace({ task, skillProgress, llm, request, onNext, onProgress }: { task: Task; skillProgress?: SkillProgress; llm?: LlmStatus; request: Request; onNext: () => void; onProgress: (skills: SkillProgress[]) => void }) {
  const course = useCourse()
  const [code, setCode] = useState(task.starterCode || course.fallback)
  // The console on screen; the assistant sees the same text when the student asks about it.
  const [screen, setScreen] = useState<ConsoleState | null>(null)
  // «Разобрать с помощником»: the check says why a solution was rejected, the assistant helps to understand it.
  const [prefill, setPrefill] = useState<{ text: string; nonce: number } | undefined>()
  const askAssistant = useCallback((text: string) => setPrefill({ text, nonce: Date.now() }), [])
  return <div className="lesson-grid enter">
    <TaskEditor task={task} skillProgress={skillProgress} code={code} onCodeChange={setCode} request={request} onNext={onNext} onProgress={onProgress} console={screen} onConsole={setScreen} onAskAssistant={llm?.available ? askAssistant : undefined} />
    <Chat llm={llm} request={request} taskId={task.id} sourceCode={code} consoleOutput={screen ? consoleText(screen.run) : undefined} prefill={prefill} />
  </div>
}

function IterationSteps({ done, iteration, pulse }: { done: number; iteration: number; pulse: boolean }) {
  const tasks = iterationTasks(iteration - 1)
  return <div className="steps" aria-label={`Итерация ${iteration} из ${ITERATIONS}, решено ${done} из ${tasks}`}>
    <span className="steps-label">Итерация {iteration}/{ITERATIONS}</span>
    <span className="steps-track">{Array.from({ length: tasks }, (_, i) => <i key={i} className={`${i < done ? 'on' : ''} ${pulse && i === done - 1 ? 'pop' : ''}`} />)}</span>
  </div>
}

function TaskEditor({ task, skillProgress, code, onCodeChange, request, onNext, onProgress, console: screen, onConsole, onAskAssistant }: { task: Task; skillProgress?: SkillProgress; code: string; onCodeChange: (code: string) => void; request: Request; onNext: () => void; onProgress: (skills: SkillProgress[]) => void; console: ConsoleState | null; onConsole: (console: ConsoleState) => void; onAskAssistant?: (text: string) => void }) {
  // Hard tasks read their input: the student types it here to try the program with «Запустить».
  const [stdin, setStdin] = useState('')
  const [attempt, setAttempt] = useState<Attempt | null>(null); const [sending, setSending] = useState(false); const [tries, setTries] = useState(0)
  const [running, setRunning] = useState(false); const [runs, setRuns] = useState(0)
  const resultRef = useRef<HTMLDivElement>(null)
  const consoleRef = useRef<HTMLElement>(null)
  const course = useCourse()
  // Snapshot the step on mount: after the iteration closes the server resets successes to 0, but this task still was step 3 of 3.
  const [step] = useState(() => { const completed = skillProgress?.completedIterations ?? 0; return { done: Math.min(skillProgress?.iterationSuccesses ?? 0, iterationTasks(completed) - 1), iteration: Math.min(completed + 1, ITERATIONS) } })
  async function submit() {
    setSending(true)
    const result = await request(() => post<Attempt & { progress?: SkillProgress[] }>('/attempts', { taskId: task.id, sourceCode: code }))
    setSending(false)
    if (!result) return
    setAttempt(result); setTries(t => t + 1)
    // A hard task reads input: a run without it shows only an input error, so its console is not shown here.
    if (result.console && !task.hard) onConsole({ run: result.console, origin: 'attempt' })
    if (result.progress) onProgress(result.progress)
  }
  /** «Запустить»: runs the code as is and shows the console. Not a submission: no attempt, no credit, no «Попытка N». */
  async function run() {
    setRunning(true)
    const result = await request(() => post<{ console: ConsoleRun }>(withCourse('/run', course.id), task.hard ? { sourceCode: code, stdin } : { sourceCode: code }))
    setRunning(false)
    if (!result) return
    onConsole({ run: result.console, origin: 'run' }); setRuns(n => n + 1)
  }
  useEffect(() => { if (runs) consoleRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }) }, [runs])
  useEffect(() => { if (attempt) resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }) }, [attempt, tries])
  const passed = !!attempt?.passed
  const ask = () => onAskAssistant?.(`Мою отправку не приняли. Вот что сказала проверка:\n\n${attempt?.output ?? ''}\n\nПомоги понять, в чём ошибка, но не пиши готовое решение.`)
  return <section className={`card task ${passed ? 'is-passed' : ''} ${task.hard ? 'hard-task' : ''}`}>
    <div className="task-head">
      {task.hard
        ? <span className="task-tag hard"><Icon name="flame" size={14} /> Hard · задача {step.done + 1}</span>
        : <span className="task-tag"><Icon name="code" size={14} /> Задача {step.done + 1}</span>}
      {skillProgress && <IterationSteps done={step.done + (passed ? 1 : 0)} iteration={step.iteration} pulse={passed} />}
    </div>
    {task.redo && <p className="redo-note"><Icon name="refresh" size={15} /> Преподаватель попросил решить эту задачу заново — прежнее решение не засчитано.</p>}
    <h2 className="title">{task.title}</h2>
    <Markdown>{task.statement}</Markdown>
    <div className="code-label"><span>Решение на {course.title}</span><CodeMirror className="code-editor" value={code} height="clamp(18rem, 48vh, 32rem)" extensions={EDITOR_EXTENSIONS[course.id]} onChange={onCodeChange} editable={!passed} aria-label={`Редактор решения на ${course.title}`} /></div>
    {task.hard && !passed && <label className="stdin-field">
      <span>Входные данные для «Запустить»</span>
      <textarea value={stdin} onChange={e => setStdin(e.target.value)} rows={3} spellCheck={false} placeholder="Например, ввод из примера в условии" />
    </label>}
    <div className="task-actions">
      {passed
        ? <button className="reward big" onClick={onNext}>Следующая задача <Icon name="arrow" /></button>
        : <>
          <button className="primary big" disabled={sending || running || !code.trim()} onClick={submit}>{sending ? <><Spinner /> Проверяем…</> : <><Icon name="play" size={16} /> Отправить на проверку</>}</button>
          <button className="ghost big" disabled={sending || running || !code.trim()} onClick={run} title="Запустить программу и посмотреть вывод. Попытка не засчитывается.">{running ? <><Spinner /> Запускаем…</> : <><Icon name="terminal" size={16} /> Запустить</>}</button>
        </>}
      {tries > 0 && !passed && <span className="muted small">Попытка {tries}</span>}
    </div>
    {attempt && <div ref={resultRef} key={tries} className={`result ${passed ? 'success' : 'failed'}`} role="status">
      {passed && <Burst trigger={tries} />}
      <div className="result-head">
        <span className="result-icon"><Icon name={passed ? 'check' : 'x'} size={18} /></span>
        <b>{passed ? 'Решение принято!' : 'Пока не проходит — это нормально'}</b>
        {passed && <span className={`xp-gain ${task.hard ? 'hard' : ''}`}>+{task.hard ? XP.hardTask : XP.task} XP</span>}
      </div>
      {attempt.grader === 'LLM' && <p className="grader-label"><Icon name="sparkle" size={13} /> Подход проверен LLM</p>}
      {attempt.review
        ? <ReviewVerdict review={attempt.review} />
        : attempt.mismatch
          ? <OutputCompare mismatch={attempt.mismatch} />
          : <>
            {!passed && <p className="muted small">Посмотри на вывод проверки ниже или спроси помощника, где искать ошибку.</p>}
            {attempt.output && <pre>{attempt.output}</pre>}
          </>}
      {!passed && onAskAssistant && <button type="button" className="ghost small-button ask-assistant" onClick={ask}><Icon name="chat" size={15} /> Разобрать с помощником</button>}
    </div>}
    {screen && (!passed || screen.origin === 'attempt') && <ConsolePanel ref={consoleRef} key={`${screen.origin}-${runs}-${tries}`} run={screen.run} origin={screen.origin} language={course.id} />}
  </section>
}

/** A wrong output next to the expected one, line by line, with line breaks and trailing spaces made visible. */
function OutputCompare({ mismatch }: { mismatch: OutputMismatch }) {
  const visible = (text: string) => text.length ? text.replace(/ +$/gm, m => '·'.repeat(m.length)).replace(/\n/g, '↵\n') : '(пусто)'
  return <div className="output-compare">
    <p className="review-summary">Вывод программы отличается от нужного.</p>
    <div className="compare-grid">
      <div><small>Нужно</small><pre>{visible(mismatch.expected)}</pre></div>
      <div><small>Твоя программа</small><pre>{visible(mismatch.actual)}</pre></div>
    </div>
    <p className="muted small">↵ — перевод строки, · — пробел в конце строки.</p>
  </div>
}

/** The reviewer's verdict: why the solution was (not) accepted, each problem with its line and where to look. */
function ReviewVerdict({ review }: { review: Review }) {
  return <div className="review">
    {review.summary && <p className="review-summary">{review.summary}</p>}
    {review.issues.length > 0 && <ul className="review-issues">{review.issues.map((issue, i) => <li key={i}>
      {issue.line != null && <span className="review-line">Строка {issue.line}</span>}
      <span className="review-problem">{issue.problem}</span>
      {issue.hint && <span className="review-hint"><Icon name="target" size={13} /> {issue.hint}</span>}
    </li>)}</ul>}
  </div>
}

type ChatState = { messages: ChatMessage[]; llm: LlmStatus; quota?: ChatQuota }

function Chat({ llm, request, taskId, sourceCode, consoleOutput, prefill }: { llm?: LlmStatus; request: Request; taskId?: Id; sourceCode?: string; consoleOutput?: string; prefill?: { text: string; nonce: number } }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]); const [text, setText] = useState(''); const [status, setStatus] = useState<LlmStatus | undefined>(llm); const [sending, setSending] = useState(false)
  const composer = useRef<HTMLTextAreaElement>(null)
  // A question prepared from a rejected check; the student can edit it before sending.
  useEffect(() => { if (prefill) { setText(prefill.text); composer.current?.focus() } }, [prefill])
  const listRef = useRef<HTMLDivElement>(null)
  const course = useCourse()
  const [quota, setQuota] = useState<ChatQuota | undefined>()
  const sync = useCallback(async () => {
    const value = await request(() => api<ChatState>(withCourse('/chat', course.id)))
    if (value) { setMessages(value.messages); setStatus(value.llm); setQuota(value.quota) }
    return value
  }, [request, course.id])
  useEffect(() => { sync() }, [sync])
  // When the limit is reached, check again as soon as the oldest counted message leaves the window.
  useEffect(() => {
    if (!quota?.retryAfterSeconds) return
    const timer = setTimeout(() => { sync() }, Math.min(quota.retryAfterSeconds, 3600) * 1000 + 1000)
    return () => clearTimeout(timer)
  }, [quota?.retryAfterSeconds, sync])
  useEffect(() => { const list = listRef.current; if (list) list.scrollTo({ top: list.scrollHeight, behavior: 'smooth' }) }, [messages, sending])
  async function send(e?: FormEvent) {
    e?.preventDefault()
    const content = text.trim(); if (!content || sending) return
    setSending(true)
    setMessages(m => [...m, { id: `local-${Date.now()}`, role: 'STUDENT', content, createdAt: new Date().toISOString() }]); setText('')
    const body = taskId !== undefined ? { content, taskId, sourceCode, consoleOutput } : { content }
    const result = await request(() => post<{ message: ChatMessage; llm?: LlmStatus; quota?: ChatQuota }>(withCourse('/chat', course.id), body))
    if (result) {
      setMessages(m => [...m, result.message]); if (result.llm) setStatus(result.llm); if (result.quota) setQuota(result.quota)
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
  const limited = !!quota?.retryAfterSeconds
  const left = quota?.hourLimit ? Math.max(0, quota.hourLimit - quota.hourUsed) : null
  return <aside className="card chat">
    <div className="chat-head">
      <span className="bot-avatar" aria-hidden="true"><Icon name="sparkle" size={18} /></span>
      <div><h2 className="card-title">Учебный помощник</h2><small className={`presence ${unavailable ? 'off' : 'on'}`}>{unavailable ? 'Недоступен' : 'На связи'}</small></div>
    </div>
    <div className="messages" ref={listRef} aria-live="polite">
      {messages.length ? messages.map(m => <div key={m.id} className={`message ${m.role.toLowerCase()}`}><Markdown>{m.content}</Markdown><small>{m.role === 'STUDENT' ? 'Ты' : 'Помощник'} · {fmt(m.createdAt)}</small></div>)
        : <div className="chat-empty"><Icon name="chat" size={22} /><p>Помощник подскажет ход мысли, а не готовый ответ. Спроси, что непонятно в условии или почему код не работает.</p></div>}
      {sending && <div className="message assistant typing" aria-label="Помощник думает"><span /><span /><span /></div>}
    </div>
    {unavailable ? <p className="muted small chat-off">{unavailable}</p> : <form onSubmit={send} className="composer">
      {taskId !== undefined && <p className="chat-code-note"><Icon name="code" size={13} /> Помощник видит текущий код из редактора</p>}
      <div className="composer-row">
        <textarea ref={composer} value={text} onChange={e => setText(e.target.value)} onKeyDown={onKeyDown} placeholder={limited ? 'Лимит сообщений исчерпан' : 'Опиши, где возникло затруднение…'} aria-label="Ваш вопрос учебному помощнику" rows={2} disabled={limited} />
        <button className="primary icon-only" disabled={sending || !text.trim() || limited} aria-label="Отправить" title="Отправить (Ctrl+Enter)">{sending ? <Spinner /> : <Icon name="send" />}</button>
      </div>
      {limited ? <p className="quota-note limited">Лимит сообщений помощнику исчерпан. Снова можно через {Math.max(1, Math.ceil(quota!.retryAfterSeconds / 60))} мин. — а пока перечитай объяснение или спроси преподавателя.</p>
        : left !== null && left <= 5 && <p className="quota-note">Осталось сообщений в этот час: {left} из {quota!.hourLimit}</p>}
    </form>}
  </aside>
}

const TOPIC_FILTERS: { id: 'todo' | 'confirmed' | 'mastered' | 'all'; label: string; match: (state: SkillState) => boolean }[] = [
  { id: 'todo', label: 'Нужна практика', match: state => state === 'gap' || state === 'started' || state === 'new' },
  { id: 'confirmed', label: 'Подтверждено диагностикой', match: state => state === 'confirmed' },
  { id: 'mastered', label: 'Освоено практикой', match: state => state === 'mastered' },
  { id: 'all', label: 'Все', match: () => true },
]

function ProgressView({ progress, otherProgress }: { progress: Progress | null; otherProgress: Partial<Record<CourseLanguage, Progress>> }) {
  const [filter, setFilter] = useState<(typeof TOPIC_FILTERS)[number]['id']>('todo')
  const course = useCourse()
  const list = useMemo(() => progress ? achievements(progress, course.id) : [], [progress, course.id])
  const shared = useMemo(() => progress ? commonAchievements({ ...otherProgress, [course.id]: progress }) : [], [progress, otherProgress, course.id])
  if (!progress) return <section><h1 className="display small">Мой прогресс</h1><div className="sk sk-card" /></section>
  const level = experience(progress)
  const counts = Object.fromEntries(TOPIC_FILTERS.map(f => [f.id, progress.skills.filter(skill => f.match(skillState(skill))).length]))
  const active = TOPIC_FILTERS.find(f => f.id === filter)!
  const skills = progress.skills.filter(skill => active.match(skillState(skill)))
  const coverage = level.topics ? Math.round((level.closed / level.topics) * 100) : 0
  return <section className="progress-page">
    <h1 className="display small">Мой прогресс · {course.title}</h1>
    <div className="stat-grid">
      <Stat icon="sparkle" label={level.diagnosticXp ? `Опыт · ${level.diagnosticXp} за диагностику` : 'Опыт'} value={level.xp} suffix="XP" />
      <Stat icon="bolt" label="Задач решено" value={level.solved} />
      <Stat icon="flag" label={`Курс закрыт · ${level.closed} из ${level.topics} тем`} value={coverage} suffix="%" />
      <Stat icon="award" label={`Освоено практикой${level.confirmed ? ` · ${level.confirmed} подтверждено диагностикой` : ''}`} value={level.mastered} />
    </div>
    <h2 className="section-title">Достижения <span className="muted">{[...list, ...shared].filter(a => a.unlocked).length} из {list.length + shared.length}</span></h2>
    <p className="achievement-group"><span className={`lang-dot ${course.key}`} aria-hidden="true" />Курс {course.title}</p>
    <AchievementGrid items={list} />
    <p className="achievement-group"><Icon name="globe" size={15} />Общие — для обоих курсов</p>
    <AchievementGrid items={shared} />
    <h2 className="section-title">Темы</h2>
    <div className="topic-filters" role="tablist" aria-label="Темы">{TOPIC_FILTERS.map(f => <button key={f.id} role="tab" aria-selected={f.id === filter} className={f.id === filter ? 'active' : ''} onClick={() => setFilter(f.id)}>
      {f.label}<span className="tabular">{counts[f.id]}</span></button>)}</div>
    <div className="card skills">{skills.length
      ? skills.map(skill => <TopicRow key={skill.skillCode} skill={skill} />)
      : <p className="muted">{filter === 'todo' ? 'Все темы закрыты — практикой или диагностикой. Отличная работа!' : filter === 'confirmed' ? 'Диагностика пока не подтвердила ни одной темы.' : filter === 'mastered' ? 'Пока ни одна тема не освоена полностью: для этого нужны три итерации на разных уроках.' : 'Тем пока нет.'}</p>}</div>
  </section>
}

/** Practice progress and the diagnostic result side by side; a confirmed topic is never drawn as practiced. */
function TopicRow({ skill }: { skill: SkillProgress }) {
  const state = skillState(skill)
  const diagnostic = skill.diagnosticTotal ? `${skill.diagnosticCorrect ?? 0}/${skill.diagnosticTotal}` : null
  return <div className={`skill-row ${state}`}>
    <span className="skill-name">{state === 'mastered' ? <Icon name="check" size={15} /> : state === 'confirmed' ? <Icon name="sparkle" size={15} /> : null}{skill.title}</span>
    {state === 'confirmed'
      ? <span className="confirmed-note">Подтверждено диагностикой · практика не нужна</span>
      : <div className="bar" role="progressbar" aria-valuenow={skillPercent(skill)} aria-valuemin={0} aria-valuemax={100} aria-label={skill.title}><i style={{ width: `${skillPercent(skill)}%` }} /></div>}
    <small className="tabular topic-meta">
      {state === 'mastered' ? 'Освоено практикой' : state === 'confirmed' ? null : `Итерации ${skill.completedIterations}/${ITERATIONS} · задачи ${skill.iterationSuccesses}/${iterationTasks(skill.completedIterations)}`}
      {diagnostic && <span className={`diag-chip ${skill.confirmedByDiagnostic ? 'ok' : 'gap'}`} title="Результат первичной диагностики по теме">диагностика {diagnostic}</span>}
    </small>
  </div>
}

function AchievementGrid({ items }: { items: ReturnType<typeof achievements> }) {
  return <div className="achievements">{items.map((a, i) => <div key={a.id} className={`achievement ${a.unlocked ? 'unlocked' : ''}`} style={{ animationDelay: `${i * 40}ms` }}>
    <span className="badge"><Icon name={a.unlocked ? a.icon : 'lock'} size={20} /></span>
    <b>{a.title}</b><small>{a.description}</small>
    {!a.unlocked && a.goal > 1 && <div className="mini-bar"><i style={{ width: `${(a.current / a.goal) * 100}%` }} /><span className="tabular">{a.current}/{a.goal}</span></div>}
  </div>)}</div>
}

function Stat({ icon, label, value, suffix }: { icon: Parameters<typeof Icon>[0]['name']; label: string; value: number; suffix?: string }) {
  const shown = useCountUp(value)
  return <div className="card stat"><span className="chip-icon"><Icon name={icon} size={18} /></span><b className="tabular">{shown}{suffix && <small> {suffix}</small>}</b><span className="muted small">{label}</span></div>
}

function TeacherPage({ request }: { request: Request }) {
  const [students, setStudents] = useState<Student[] | null>(null); const [selected, setSelected] = useState<Student | null>(null)
  const [globalLlm, setGlobalLlm] = useState<LlmStatus | null>(null)
  const [name, setName] = useState(''); const [login, setLogin] = useState(''); const [password, setPassword] = useState(''); const [group, setGroup] = useState(''); const [creating, setCreating] = useState(false)
  const [view, setView] = useState<'students' | 'llm' | 'settings'>('students')
  const toast = useToast()
  const [groupFilter, setGroupFilter] = useGroupFilter('rmzn-admin-group', students ? [...new Set(students.map(s => s.group).filter((g): g is string => !!g))] : null)
  /** Picking a group also fills it in for the next new account, the usual way to add students to a group. */
  const chooseGroup = (value: string) => { setGroupFilter(value); setGroup(value === NO_GROUP ? '' : value) }
  // The open card follows the list: a renamed group or changed login shows there too.
  const load = useCallback(() => request(() => api<{ students: Student[] }>('/admin/students')).then(s => {
    if (!s) return
    setStudents(s.students); setSelected(current => current && (s.students.find(x => x.id === current.id) ?? current))
  }), [request])
  useEffect(() => {
    load()
    request(() => api<MeResponse>('/auth/me')).then(value => { if (value) setGlobalLlm(value.llm) })
  }, [load, request])
  // Keeps «урок идёт» current while the teacher has the list open.
  useEffect(() => {
    if (view !== 'students') return
    const timer = setInterval(() => { api<{ students: Student[] }>('/admin/students').then(s => setStudents(s.students)).catch(() => {}) }, 60_000)
    return () => clearInterval(timer)
  }, [view])
  async function create(e: FormEvent) {
    e.preventDefault(); setCreating(true)
    const student = await request(() => post<Student>('/admin/students', { displayName: name.trim(), login: login.trim(), password, group: group.trim() || null }))
    setCreating(false)
    if (student) { setName(''); setLogin(''); setPassword(''); load(); toast({ tone: 'info', icon: 'user', title: 'Учётная запись создана', text: [student.displayName, student.login, student.group].filter(Boolean).join(' · ') }) }
  }
  const onUpdated = useCallback((updated: Student) => {
    setStudents(xs => xs && xs.map(x => x.id === updated.id ? { ...x, ...updated } : x))
    setSelected(s => s && s.id === updated.id ? { ...s, ...updated } : s)
  }, [])
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
  const tabs = <nav className="segmented admin-tabs three" role="tablist" style={{ '--active': ['students', 'llm', 'settings'].indexOf(view) } as CSSProperties}>
    <span className="segmented-thumb" aria-hidden="true" />
    <button role="tab" aria-selected={view === 'students'} className={view === 'students' ? 'active' : ''} onClick={() => setView('students')}><Icon name="user" size={16} /> Студенты</button>
    <button role="tab" aria-selected={view === 'llm'} className={view === 'llm' ? 'active' : ''} onClick={() => setView('llm')}><Icon name="chart" size={16} /> Аналитика LLM</button>
    <button role="tab" aria-selected={view === 'settings'} className={view === 'settings' ? 'active' : ''} onClick={() => setView('settings')}><Icon name="sparkle" size={16} /> Настройки LLM</button>
  </nav>
  if (view === 'llm') return <>{tabs}<LlmAnalytics request={request} /></>
  if (view === 'settings') return <>{tabs}<LlmSettingsView request={request} /></>
  const counts = groupCounts(students ?? [], s => s.group)
  const groupNames = counts.groups.map(g => g.name)
  const visible = students?.filter(s => inGroup(groupFilter, s.group)) ?? null
  const studying = visible?.filter(s => s.activeLessons?.length).length ?? 0
  const filtered = !!students && !!visible && visible.length !== students.length
  return <>{tabs}<section className="admin">
    <div className="admin-main">
      <div className="enter">
        <p className="eyebrow">Преподаватель</p>
        <h1 className="display small">Студенты{students && <span className="count-badge" title={filtered ? `показано ${visible!.length} из ${students.length}` : undefined}>{filtered ? `${visible!.length}/${students.length}` : students.length}</span>}</h1>
        {studying > 0 && <p className="studying-now"><span className="live-dot" aria-hidden="true" />Сейчас занимаются: {studying}</p>}
      </div>
      <div className="card setting enter">
        <span className="chip-icon"><Icon name="sparkle" size={18} /></span>
        <div><h2 className="card-title">LLM для курса</h2>
          <p className="muted small">{!globalLlm ? 'Загружаем…' : globalLlm.globallyEnabled ? 'Помощник и генерация контента включены' : configDisabled ? 'Отключена в настройках сервера (APP_LLM_ENABLED)' : 'Выключена для всех студентов'}</p></div>
        <Switch checked={!!globalLlm?.globallyEnabled} disabled={!globalLlm || configDisabled} onChange={toggleGlobal} label="LLM для курса" />
      </div>
      <div className="card enter">
        <h2 className="card-title"><span className="chip-icon"><Icon name="plus" size={16} /></span> Новая учётная запись</h2>
        <form className="inline-form" onSubmit={create} autoComplete="off">
          <input placeholder="Имя" aria-label="Имя" required value={name} onChange={e => setName(e.target.value)} />
          <input placeholder="Логин" aria-label="Логин" required value={login} onChange={e => setLogin(e.target.value)} autoComplete="off" autoCapitalize="none" spellCheck={false} />
          <input placeholder="Пароль" aria-label="Пароль" required value={password} onChange={e => setPassword(e.target.value)} autoComplete="new-password" />
          <input placeholder="Группа" title="Группа — необязательно" aria-label="Группа, необязательно" list="known-groups" maxLength={60} value={group} onChange={e => setGroup(e.target.value)} autoComplete="off" />
          <GroupOptions id="known-groups" groups={groupNames} />
          <button className="primary" disabled={creating}>{creating ? <><Spinner /> Создаём…</> : 'Создать'}</button>
        </form>
      </div>
      {students && <div className="group-bar enter">
        <GroupFilter total={students.length} groups={counts.groups} ungrouped={counts.ungrouped} value={groupFilter} onChange={chooseGroup} />
        {groupFilter && groupFilter !== NO_GROUP && <RenameGroup group={groupFilter} groups={groupNames} request={request} onRenamed={to => { chooseGroup(to ?? ''); load() }} />}
      </div>}
      <div className="student-list enter">{!students || !visible ? <p className="muted list-note">Загружаем…</p> : visible.length
        ? visible.map((s, i) => <button key={s.id} className={selected?.id === s.id ? 'student selected' : 'student'} aria-pressed={selected?.id === s.id} onClick={() => setSelected(s)} style={{ animationDelay: `${i * 30}ms` }}>
          <span className="avatar" aria-hidden="true">{initials(s.displayName)}</span>
          <span className="student-meta"><b>{s.displayName}</b><small>{s.login}{s.group && <span className="group-tag">{s.group}</span>}</small>
            {s.activeLessons?.map(l => <ActiveLessonBadge key={l.language} lesson={l} />)}</span>
          {!!s.hardModeAllowed && <i className={`pill hard ${s.hardModeOn ? 'on' : ''}`} title={s.hardModeOn ? 'Hard mode включён' : 'Допуск к hard mode есть, режим выключен'}><Icon name="flame" size={12} /> HARD</i>}
          <i className={s.llmEnabled ? 'pill on' : 'pill'}>LLM</i>
        </button>)
        : <p className="muted list-note">{students.length ? 'В этой группе студентов нет.' : 'Студентов пока нет. Создай первую учётную запись выше.'}</p>}</div>
    </div>
    {selected ? <StudentDetail key={selected.id} student={selected} groups={groupNames} request={request} toggle={() => toggle(selected)} onLlmStatus={onLlmStatus} onUpdated={onUpdated} onDeleted={() => { setStudents(xs => xs && xs.filter(x => x.id !== selected.id)); setSelected(null) }} />
      : <aside className="card student-detail placeholder"><span className="empty-icon"><Icon name="user" size={26} /></span><p className="muted">Выбери студента, чтобы увидеть его уроки, решения и переписку с помощником.</p></aside>}
  </section></>
}

// No look-alike characters (0/O, 1/l/I) so a password read aloud or copied by hand survives.
const PASSWORD_ALPHABET = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
function generatePassword(length = 10) {
  const bytes = new Uint32Array(length); crypto.getRandomValues(bytes)
  return Array.from(bytes, b => PASSWORD_ALPHABET[b % PASSWORD_ALPHABET.length]).join('')
}

function PasswordReset({ student, request }: { student: Student; request: Request }) {
  const [open, setOpen] = useState(false); const [password, setPassword] = useState(''); const [saving, setSaving] = useState(false); const [saved, setSaved] = useState('')
  const toast = useToast()
  async function save(e: FormEvent) {
    e.preventDefault(); setSaving(true)
    const result = await request(() => patch<{ sessionsClosed: number }>(`/admin/students/${student.id}/password`, { password }))
    setSaving(false)
    if (!result) return
    setSaved(password); setPassword('')
    toast({ tone: 'info', icon: 'lock', title: 'Пароль изменён', text: result.sessionsClosed ? `Студент вышел из системы на ${result.sessionsClosed} устр.` : `${student.displayName} войдёт с новым паролем` })
  }
  const copy = () => navigator.clipboard?.writeText(saved).then(() => toast({ tone: 'info', icon: 'check', title: 'Пароль скопирован' })).catch(() => {})
  if (!open) return <button className="ghost small-button" onClick={() => { setOpen(true); setPassword(generatePassword()); setSaved('') }}><Icon name="lock" size={15} /> Сменить пароль</button>
  return <div className="password-reset enter">
    {saved ? <div className="password-saved">
      <span className="muted small">Новый пароль — передай его студенту. После закрытия он больше не будет показан.</span>
      <div className="password-row"><code>{saved}</code><button className="secondary" onClick={copy}>Скопировать</button><button className="ghost" onClick={() => { setOpen(false); setSaved('') }}>Готово</button></div>
    </div> : <form onSubmit={save} autoComplete="off">
      <label className="small">Новый пароль для {student.displayName}
        <div className="password-row">
          <input value={password} onChange={e => setPassword(e.target.value)} minLength={6} required autoComplete="new-password" spellCheck={false} aria-describedby="password-hint" />
          <button type="button" className="ghost" onClick={() => setPassword(generatePassword())} title="Сгенерировать">↻</button>
        </div>
      </label>
      <p id="password-hint" className="muted small">Не короче 6 символов. Все открытые сессии студента будут завершены.</p>
      <div className="password-row"><button className="primary" disabled={saving || password.length < 6}>{saving ? <><Spinner /> Сохраняем…</> : 'Сохранить пароль'}</button><button type="button" className="ghost" onClick={() => setOpen(false)}>Отмена</button></div>
    </form>}
  </div>
}

/** What the diagnostic confirmed and which topics it flagged, so the teacher sees why practice starts where it does. */
function DiagnosticSummary({ skills }: { skills: SkillProgress[] }) {
  const taken = skills.filter(s => s.diagnosticTotal)
  if (!taken.length) return <p className="diag-summary muted small">Диагностика не пройдена</p>
  const confirmed = taken.filter(s => s.confirmedByDiagnostic).length
  const gaps = taken.filter(s => !s.confirmedByDiagnostic && !s.mastered)
  return <div className="diag-summary">
    <span className="small"><b>Диагностика:</b> подтверждено {confirmed} из {taken.length} тем{gaps.length ? `, пробелов — ${gaps.length}` : ', пробелов нет'}</span>
    {gaps.length > 0 && <div className="gap-chips">{gaps.slice(0, 8).map(g => <span key={g.skillCode} className="diag-chip gap" title={`диагностика ${g.diagnosticCorrect ?? 0}/${g.diagnosticTotal}`}>{g.title} {g.diagnosticCorrect ?? 0}/{g.diagnosticTotal}</span>)}{gaps.length > 8 && <span className="muted small">и ещё {gaps.length - 8}</span>}</div>}
  </div>
}

/** «урок идёт · Java, 12 мин» — the open lesson and how long it has been going. */
function ActiveLessonBadge({ lesson }: { lesson: ActiveLesson }) {
  const minutes = Math.max(0, Math.round((Date.now() - parseDate(lesson.startedAt).getTime()) / 60_000))
  const since = minutes < 60 ? `${minutes} мин` : minutes < 24 * 60 ? `${Math.floor(minutes / 60)} ч ${minutes % 60} мин` : `${Math.floor(minutes / (24 * 60))} дн`
  return <span className="active-lesson" title={`Урок ${lesson.number} начат ${fmt(lesson.startedAt)}`}><span className="live-dot" aria-hidden="true" />урок идёт · {COURSES[lesson.language].title}, {since}</span>
}

function Switch({ checked, disabled, onChange, label }: { checked: boolean; disabled?: boolean; onChange: () => void; label: string }) {
  return <button type="button" role="switch" aria-checked={checked} aria-label={label} className={`switch ${checked ? 'on' : ''}`} disabled={disabled} onClick={onChange}><span /></button>
}

/** Renames the selected group for all its students; an existing name merges the groups, an empty one removes the group. */
function RenameGroup({ group, groups, request, onRenamed }: { group: string; groups: string[]; request: Request; onRenamed: (to: string | null) => void }) {
  const [open, setOpen] = useState(false); const [name, setName] = useState(group); const [saving, setSaving] = useState(false)
  const toast = useToast()
  useEffect(() => { setOpen(false); setName(group) }, [group])
  async function save(e: FormEvent) {
    e.preventDefault()
    const to = name.trim()
    if (!to && !window.confirm(`Убрать группу «${group}» у всех её студентов? Сами студенты останутся.`)) return
    const merging = to && groups.some(g => g !== group && g.toLocaleLowerCase('ru') === to.toLocaleLowerCase('ru'))
    if (merging && !window.confirm(`Группа «${to}» уже есть. Объединить с ней «${group}»?`)) return
    setSaving(true)
    const result = await request(() => post<{ group: string | null; students: number }>('/admin/groups/rename', { from: group, to }))
    setSaving(false)
    if (!result) return
    toast({ tone: 'info', icon: 'user', title: result.group ? `Группа теперь «${result.group}»` : `Группа «${group}» убрана`, text: `Студентов: ${result.students}` })
    onRenamed(result.group)
  }
  if (!open) return <button type="button" className="ghost small-button" onClick={() => setOpen(true)}>Переименовать группу</button>
  return <form className="rename-group enter" onSubmit={save} autoComplete="off">
    <input aria-label={`Новое название группы «${group}»`} value={name} onChange={e => setName(e.target.value)} maxLength={60} autoFocus list="known-groups" />
    <button className="primary" disabled={saving || name.trim() === group}>{saving ? <><Spinner /> Сохраняем…</> : 'Сохранить'}</button>
    <button type="button" className="ghost" onClick={() => setOpen(false)}>Отмена</button>
    <small className="muted">Пустое название убирает группу. Название существующей группы объединяет их.</small>
  </form>
}

/** Name, login and group of a student. A new login works from the next sign-in; open sessions stay. */
function EditStudent({ student, groups, request, onUpdated }: { student: Student; groups: string[]; request: Request; onUpdated: (student: Student) => void }) {
  const [open, setOpen] = useState(false); const [saving, setSaving] = useState(false)
  const [draft, setDraft] = useState({ displayName: student.displayName, login: student.login, group: student.group ?? '' })
  const toast = useToast()
  const reset = () => setDraft({ displayName: student.displayName, login: student.login, group: student.group ?? '' })
  const changed = draft.displayName.trim() !== student.displayName || draft.login.trim() !== student.login || draft.group.trim() !== (student.group ?? '')
  async function save(e: FormEvent) {
    e.preventDefault(); setSaving(true)
    const updated = await request(() => patch<Student>(`/admin/students/${student.id}`, { displayName: draft.displayName.trim(), login: draft.login.trim(), group: draft.group.trim() || null }))
    setSaving(false)
    if (!updated) return
    onUpdated(updated); setOpen(false)
    toast({ tone: 'info', icon: 'user', title: 'Данные студента сохранены', text: updated.login !== student.login ? `Новый логин «${updated.login}» — со следующего входа` : [updated.displayName, updated.group].filter(Boolean).join(' · ') })
  }
  if (!open) return <button className="ghost small-button" onClick={() => { reset(); setOpen(true) }}><Icon name="user" size={15} /> Изменить данные</button>
  return <form className="password-reset edit-student enter" onSubmit={save} autoComplete="off">
    <label className="small">Имя<input value={draft.displayName} onChange={e => setDraft(d => ({ ...d, displayName: e.target.value }))} required maxLength={100} /></label>
    <label className="small">Логин<input value={draft.login} onChange={e => setDraft(d => ({ ...d, login: e.target.value }))} required maxLength={64} autoCapitalize="none" spellCheck={false} /></label>
    <label className="small"><span>Группа <span className="muted">— необязательно</span></span><input value={draft.group} onChange={e => setDraft(d => ({ ...d, group: e.target.value }))} maxLength={60} list="student-groups" placeholder="Без группы" /></label>
    <GroupOptions id="student-groups" groups={groups} />
    {draft.login.trim() !== student.login && <p className="muted small">Студент войдёт с новым логином в следующий раз; открытые сессии сохранятся, пароль не меняется.</p>}
    <div className="password-row"><button className="primary" disabled={saving || !changed || !draft.displayName.trim() || !draft.login.trim()}>{saving ? <><Spinner /> Сохраняем…</> : 'Сохранить'}</button><button type="button" className="ghost" onClick={() => setOpen(false)}>Отмена</button></div>
  </form>
}

function StudentDetail({ student, groups, request, toggle, onLlmStatus, onUpdated, onDeleted }: { student: Student; groups: string[]; request: Request; toggle: () => void; onLlmStatus: (llm: LlmStatus) => void; onUpdated: (student: Student) => void; onDeleted: () => void }) {
  const [lessons, setLessons] = useState<Lesson[] | null>(null)
  const [progress, setProgress] = useState<Partial<Record<CourseLanguage, SkillProgress[]>> | null>(null)
  const [hardCourses, setHardCourses] = useState<Student['hardModeCourses']>(student.hardModeCourses)
  const [openLesson, setOpenLesson] = useState<Id | null>(null)
  const [detail, setDetail] = useState<LessonDetail | null>(null)
  const openRef = useRef<Id | null>(null)
  useEffect(() => {
    let alive = true
    setLessons(null); setDetail(null); setOpenLesson(null); openRef.current = null
    request(() => api<{ lessons: Lesson[] }>(`/admin/students/${student.id}/lessons`)).then(value => { if (alive && value) setLessons(value.lessons) })
    request(() => api<{ llm: LlmStatus; student?: Student; progress: SkillProgress[]; progressByLanguage?: Partial<Record<CourseLanguage, SkillProgress[]>> }>(`/admin/students/${student.id}`)).then(value => { if (alive && value) { onLlmStatus(value.llm); setProgress(value.progressByLanguage ?? { JAVA: value.progress }); if (value.student?.hardModeCourses) setHardCourses(value.student.hardModeCourses) } })
    return () => { alive = false }
  }, [student.id, request, onLlmStatus])
  const toast = useToast()
  const chatRef = useRef<HTMLDivElement>(null)
  async function open(lesson: Lesson, keepView = false) {
    openRef.current = lesson.id; setOpenLesson(lesson.id); if (!keepView) setDetail(null)
    const value = await request(() => api<LessonDetail>(`/admin/students/${student.id}/lessons/${lesson.id}`))
    if (value && openRef.current === lesson.id) setDetail(value)
  }
  const reloadLessons = () => request(() => api<{ lessons: Lesson[] }>(`/admin/students/${student.id}/lessons`)).then(value => { if (value) setLessons(value.lessons) })
  const reloadProgress = () => request(() => api<{ student?: Student; progress: SkillProgress[]; progressByLanguage?: Partial<Record<CourseLanguage, SkillProgress[]>> }>(`/admin/students/${student.id}`)).then(value => { if (value) { setProgress(value.progressByLanguage ?? { JAVA: value.progress }); if (value.student?.hardModeCourses) setHardCourses(value.student.hardModeCourses) } })
  // Opening a lesson jumps to the latest messages: the end of the conversation is what the teacher usually needs.
  useEffect(() => {
    const chat = chatRef.current
    if (!detail || !chat) return
    chat.scrollTop = chat.scrollHeight
    chat.scrollIntoView({ block: 'end', behavior: 'smooth' })
  }, [detail?.lesson.id])
  async function finishLesson(lesson: Lesson) {
    if (!window.confirm(`Завершить урок ${lesson.number} студента ${student.displayName}? Студент начнёт следующий урок сам.`)) return
    const result = await request(() => post<{ lesson: Lesson }>(`/admin/students/${student.id}/lessons/${lesson.id}/finish`))
    if (!result) return
    toast({ tone: 'info', icon: 'flag', title: `Урок ${lesson.number} завершён`, text: student.displayName })
    await reloadLessons(); open(result.lesson, true)
  }
  async function toggleHard() {
    const allowed = !student.hardModeAllowed
    const result = await request(() => patch<{ hardModeAllowed: boolean }>(`/admin/students/${student.id}/hard-mode`, { allowed }))
    if (!result) return
    onUpdated({ ...student, hardModeAllowed: result.hardModeAllowed, hardModeOn: result.hardModeAllowed ? student.hardModeOn : 0 })
    toast({ tone: 'info', icon: 'flame', title: result.hardModeAllowed ? 'Допуск к hard mode выдан' : 'Hard mode отключён', text: result.hardModeAllowed ? `${student.displayName} может включить его сам` : student.displayName })
  }
  async function revoke(lesson: Lesson, task: { id: Id; title: string }) {
    if (!window.confirm(`Отменить зачёт задачи «${task.title}»? Студенту придётся решить её заново, прогресс по теме будет пересчитан.`)) return
    const result = await request(() => post<{ redoInOpenLesson: boolean }>(`/admin/students/${student.id}/lessons/${lesson.id}/tasks/${task.id}/revoke`))
    if (!result) return
    toast({ tone: 'info', icon: 'refresh', title: 'Зачёт отменён', text: result.redoInOpenLesson ? 'Задача снова ждёт решения в текущем уроке' : 'Задача будет первой в следующем уроке студента' })
    reloadProgress(); open(lesson, true)
  }
  return <aside className="card student-detail enter-side">
    <div className="detail-head">
      <span className="avatar big" aria-hidden="true">{initials(student.displayName)}</span>
      <div><h2 className="title">{student.displayName}</h2><p className="muted small">{student.login}{student.group && <span className="group-tag">{student.group}</span>}</p></div>
      <div className="detail-switches">
        <label className="switch-label"><span className="muted small">LLM</span><Switch checked={!!student.llmEnabled} onChange={toggle} label={`LLM для ${student.displayName}`} /></label>
        <label className="switch-label hard" title="Допуск к hard mode: студент сам включает алгоритмические задачи"><span className="muted small"><Icon name="flame" size={13} /> Hard</span><Switch checked={!!student.hardModeAllowed} onChange={toggleHard} label={`Допуск к hard mode для ${student.displayName}`} /></label>
      </div>
    </div>
    {!!student.hardModeAllowed && hardCourses && LANGUAGES.some(language => hardCourses[language]) && <p className="hard-ready muted small">
      Hard mode: {LANGUAGES.filter(language => hardCourses[language]).map(language => {
        const course = hardCourses[language]!
        return `${COURSES[language].title} — ${course.ready ? 'открыт' : `осталось тем: ${course.remaining}`}`
      }).join(', ')}</p>}
    {!!student.hardModeOn && <p className="hard-note"><Icon name="flame" size={14} /> Студент сейчас в hard mode</p>}
    <div className="detail-actions"><EditStudent key={`${student.login}|${student.displayName}|${student.group ?? ''}`} student={student} groups={groups} request={request} onUpdated={onUpdated} /><PasswordReset student={student} request={request} /></div>
    {progress && <div className="lang-stats">{LANGUAGES.filter(language => progress[language]).map(language => {
      const level = experience({ skills: progress[language]! })
      return <div key={language}>
        <span className="lang-badge"><span className={`lang-dot ${COURSES[language].key}`} aria-hidden="true" />{COURSES[language].title}</span>
        <span className="mini-stats-cell"><b>{level.level}</b><small>уровень</small></span>
        <span className="mini-stats-cell"><b>{level.iterations}</b><small>итераций</small></span>
        <span className="mini-stats-cell"><b>{level.mastered}</b><small>тем освоено</small></span>
        <DiagnosticSummary skills={progress[language]!} />
      </div>
    })}</div>}
    {!lessons ? <p className="muted">Загружаем данные…</p> : <>
      <h3 className="section-title">Уроки</h3>
      {lessons.length ? <div className="lesson-list">{lessons.map(l => <button key={l.id} className={openLesson === l.id ? 'lesson-item selected' : 'lesson-item'} aria-pressed={openLesson === l.id} onClick={() => open(l)}>
        <b><span className={`lang-dot ${COURSES[l.language ?? 'JAVA'].key}`} title={COURSES[l.language ?? 'JAVA'].title} /> {COURSES[l.language ?? 'JAVA'].title} · урок {l.number}</b><span className={l.finishedAt ? '' : 'live'}>{l.finishedAt ? `завершён ${fmt(l.finishedAt)}` : `идёт · начат ${fmt(l.startedAt)}`}</span>
      </button>)}</div> : <p className="muted">Уроков пока нет.</p>}
      {openLesson !== null && !detail && <p className="muted"><Spinner /> Загружаем урок…</p>}
      {detail && <div className="enter">
        <div className="lesson-detail-head">
          <div><b>{COURSES[detail.lesson.language ?? 'JAVA'].title} · урок {detail.lesson.number}</b>
            <span className={detail.lesson.finishedAt ? 'muted small' : 'live small'}>{detail.lesson.finishedAt ? `завершён ${fmt(detail.lesson.finishedAt)}` : 'идёт сейчас'}</span></div>
          {!detail.lesson.finishedAt && <button className="ghost small-button" onClick={() => finishLesson(detail.lesson)}><Icon name="flag" size={15} /> Завершить урок</button>}
        </div>
        <h3 className="section-title">Задачи и попытки</h3>
        {detail.tasks.length ? detail.tasks.map(t => <article key={t.id} className="detail-task">
          <div className="detail-task-head"><b>{!!t.hard && <span className="hard-chip"><Icon name="flame" size={12} /> HARD</span>}{t.title}{!!t.replaced && <span className="replaced-chip" title="Студент переключил hard mode, и вместо этой задачи выдана задача нового режима">заменена при смене режима</span>}</b>
            {t.submissions.some(a => a.passed && !a.revokedAt) && <button className="ghost danger small-button" onClick={() => revoke(detail.lesson, t)} title="Студенту придётся решить задачу заново"><Icon name="refresh" size={14} /> Отменить зачёт</button>}
          </div>
          <Markdown>{t.statement}</Markdown>
          {t.submissions.length ? t.submissions.map(a => <details key={a.id}><summary className={a.revokedAt ? 'revoked' : a.passed ? 'passed' : 'not-passed'}><Icon name={a.revokedAt ? 'refresh' : a.passed ? 'check' : 'x'} size={14} /> {a.revokedAt ? `зачёт отменён ${fmt(a.revokedAt)}` : a.passed ? 'принято' : 'не принято'} · {fmt(a.createdAt)}</summary><pre>{a.sourceCode}</pre>{a.grader === 'LLM' && <p className="grader-label"><Icon name="sparkle" size={13} /> Подход проверен LLM</p>}{a.review ? <ReviewVerdict review={a.review} /> : a.output && <pre>{a.output}</pre>}{a.console && <ConsolePanel run={a.console} origin="attempt" language={detail.lesson.language ?? 'JAVA'} />}</details>) : <p className="muted small">Попыток не было.</p>}
        </article>) : <p className="muted">Задач в этом уроке не было.</p>}
        <h3 className="section-title">Чат</h3>
        {detail.chat.length ? <div className="messages static" ref={chatRef}>{detail.chat.map(m => <div key={m.id} className={`message ${m.role === 'STUDENT' ? 'student' : 'assistant'}`}><Markdown>{m.content}</Markdown><small>{m.role === 'STUDENT' ? 'Студент' : 'Помощник'} · {fmt(m.createdAt)}</small></div>)}</div> : <p className="muted">Переписки не было.</p>}
      </div>}
    </>}
    <DeleteAccount student={student} request={request} onDeleted={onDeleted} />
  </aside>
}

/** Irreversible, so the teacher types the student's login to confirm; the server checks it too. */
function DeleteAccount({ student, request, onDeleted }: { student: Student; request: Request; onDeleted: () => void }) {
  const [open, setOpen] = useState(false); const [typed, setTyped] = useState(''); const [deleting, setDeleting] = useState(false)
  const toast = useToast()
  const matches = typed.trim() === student.login
  async function confirm(e: FormEvent) {
    e.preventDefault(); if (!matches) return
    setDeleting(true)
    const result = await request(() => remove<{ lessons: number; submissions: number }>(`/admin/students/${student.id}`, { confirmLogin: typed.trim() }))
    setDeleting(false)
    if (!result) return
    toast({ tone: 'info', icon: 'user', title: `Аккаунт ${student.displayName} удалён`, text: `Уроков: ${result.lessons}, отправок решений: ${result.submissions}` })
    onDeleted()
  }
  if (!open) return <div className="danger-zone"><button className="ghost danger small-button" onClick={() => setOpen(true)}><Icon name="x" size={15} /> Удалить аккаунт</button></div>
  return <form className="danger-zone open enter" onSubmit={confirm} autoComplete="off">
    <b>Удалить аккаунт {student.displayName}?</b>
    <p className="muted small">Будут удалены вход в систему, диагностика, все уроки, решения, переписка с помощником и прогресс по обоим курсам. Восстановить их нельзя. Статистика обращений к LLM останется в аналитике без привязки к студенту.</p>
    <label className="small">Чтобы подтвердить, введи логин <code>{student.login}</code>
      <input value={typed} onChange={e => setTyped(e.target.value)} autoCapitalize="none" spellCheck={false} aria-invalid={typed.length > 0 && !matches} autoFocus />
    </label>
    <div className="password-row">
      <button className="danger-solid" disabled={!matches || deleting}>{deleting ? <><Spinner /> Удаляем…</> : 'Удалить навсегда'}</button>
      <button type="button" className="ghost" onClick={() => { setOpen(false); setTyped('') }}>Отмена</button>
    </div>
  </form>
}
