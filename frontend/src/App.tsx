import { uiText } from './uiText'
import { createContext, CSSProperties, FormEvent, KeyboardEvent, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import { currentLocale, LocaleSwitch, tr, useLocale } from './locale'
import CodeMirror from '@uiw/react-codemirror'
import { EDITOR_EXTENSIONS, FALLBACK_CODE, Markdown } from './editor'
import { api, ApiError, humanize, onUnauthorized, patch, post, remove, stationToken } from './api'
import { achievements, commonAchievements, experience, skillState, type SkillState, ITERATIONS, iterationTasks, parseDate, skillClosed, skillPercent, skillStarted, streak, XP } from './game'
import { Burst, Icon, initials, Ring, ToastProvider, useCountUp, useToast } from './fx'
import { LlmAnalytics } from './analytics'
import { ProgressAnalytics } from './progress'
import { PairWork } from './pairs'
import { AttestationDone, BoardAdmin, BoardCallDialog, BoardDone, BoardElsewhere, BoardTestScreen, clock, StudentBoardGrades, useBoardCurrent, useNow } from './board'
import { StudentSessionCard } from './session'
import { RelayLayer } from './relay'
import { StationScreen } from './station'
import { LlmSettingsView } from './settings'
import { DrawSettingsView } from './wheel'
import { ConsolePanel, consoleText, type ConsoleOrigin } from './console'
import { DangerFrame, HardModeDialog, HardModeSwitch, HeaderTapes } from './hardmode'
import { GroupFilter, GroupOptions, groupCounts, inGroup, NO_GROUP, useGroupFilter } from './groups'
import type { ActiveLesson, Attempt, AttestationPractice, BoardFormat, ChatMessage, ChatQuota, ConsoleRun, CourseLanguage, Diagnostic, Id, LearningNext, Lesson, LessonDetail, LlmStatus, MeResponse, Practice, PracticeAttempt, PracticeByLanguage, Progress, Retake, RetakeHistory, SkillProgress, Student, Task, User, Review, OutputMismatch } from './types'

const UNKNOWN = 'Не знаю'
const fmt = (value?: string | null) => {
  if (!value) return ''
  const date = parseDate(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString(currentLocale())
}

/** «завершён …» for the teacher's lesson history: says how the lesson was closed when it was not the student's own button. */
const finishedLabel = (lesson: Lesson) => { const reason = lesson.finishReason; const label = reason === 'IDLE' ? tr(currentLocale(), 'завершён по бездействию', 'terminé pour inactivité', 'انتهى بسبب عدم النشاط') : reason === 'LOGOUT' ? tr(currentLocale(), 'завершён при выходе', 'terminé à la déconnexion', 'انتهى عند الخروج') : reason === 'TEACHER' ? tr(currentLocale(), 'завершён преподавателем', 'terminé par l’enseignant', 'الأستاذ أنهى الدرس') : tr(currentLocale(), 'завершён', 'terminé', 'انتهى'); return `${label} ${fmt(lesson.finishedAt)}` }
/** 20 минут, 21 минуту, 22 минуты. */
const minutesText = (n: number) => { const locale = currentLocale(); if (locale === 'fr') return `${n} min`; if (locale === 'ar-SD') return `${n} دقيقة`; const d = n % 10, h = n % 100; return `${n} ${d === 1 && h !== 11 ? 'минуту' : d >= 2 && d <= 4 && (h < 12 || h > 14) ? 'минуты' : 'минут'}` }

const COURSES = {
  JAVA: {
    id: 'JAVA', key: 'java', title: 'Java', logo: 'J',
    fallback: FALLBACK_CODE.JAVA,
    pitch: 'Строгая типизация и классический ООП. Язык бэкенда, Android и больших систем.', tags: ['ООП', 'Бэкенд', 'Android'],
  },
  PYTHON: {
    id: 'PYTHON', key: 'python', title: 'Python', logo: 'Py',
    fallback: FALLBACK_CODE.PYTHON,
    pitch: 'Короткий понятный синтаксис. Автоматизация, анализ данных, бэкенд и машинное обучение.', tags: ['Простой синтаксис', 'Данные', 'Автоматизация'],
  },
} as const
type Course = (typeof COURSES)[CourseLanguage]
const LANGUAGES = Object.keys(COURSES) as CourseLanguage[]
const CourseContext = createContext<Course>(COURSES.JAVA)
const useCourse = () => useContext(CourseContext)
/** Reports a run, submission or chat message to the lesson page: success restarts the inactivity countdown, a failure re-checks the lesson. */
const LessonActivity = createContext<(ok: boolean) => void>(() => {})
const IDLE_WARNING_MS = 3 * 60_000, IDLE_GRACE_MS = 70_000, IDLE_TICK_MS = 10_000
type LessonEnd = { reason: Lesson['finishReason']; minutes: number }
const lessonEndText = ({ reason, minutes }: LessonEnd) => {
  const locale = currentLocale()
  if (locale === 'fr') return `${reason === 'IDLE' ? `Le cours s’est terminé automatiquement après ${minutesText(minutes)} d’inactivité.` : reason === 'TEACHER' ? 'L’enseignant a terminé le cours.' : reason === 'LOGOUT' ? 'Le cours s’est terminé lors de la déconnexion.' : 'Le cours est déjà terminé, peut-être dans un autre onglet.'} Commence un nouveau cours quand tu seras prêt.`
  if (locale === 'ar-SD') return `${reason === 'IDLE' ? `الدرس انتهى تلقائياً بعد ${minutesText(minutes)} بدون نشاط.` : reason === 'TEACHER' ? 'الأستاذ أنهى الدرس.' : reason === 'LOGOUT' ? 'الدرس انتهى عند تسجيل الخروج.' : 'الدرس انتهى بالفعل، يمكن في علامة تبويب تانية.'} ابدأ درس جديد لما تكون جاهز.`
  return `${reason === 'IDLE' ? `Урок завершён автоматически: ${minutesText(minutes)} без активности.` : reason === 'TEACHER' ? 'Урок завершил преподаватель.' : reason === 'LOGOUT' ? 'Урок завершён: был выход из аккаунта.' : 'Урок уже завершён — например, в другой вкладке.'} Начни новый урок, когда будешь готов.`
}
/** Adds the course to a student API path; the backend treats a missing value as Java. */
const withCourse = (path: string, language: CourseLanguage) => `${path}${path.includes('?') ? '&' : '?'}language=${language}`
const LANGUAGE_KEY = 'rmzn.language'
const storedLanguage = (): CourseLanguage | null => {
  try { const value = localStorage.getItem(LANGUAGE_KEY); return value === 'JAVA' || value === 'PYTHON' ? value : null } catch { return null }
}
const storeLanguage = (language: CourseLanguage) => { try { localStorage.setItem(LANGUAGE_KEY, language) } catch { /* private mode: choice lasts for this page only */ } }

const Spinner = () => <span className="spinner" aria-hidden="true" />

/** The signed-in user's id, for what this browser keeps per user (drafts of the lesson code). */
const UserContext = createContext<Id | null>(null)

// ───────── Drafts of the lesson code: localStorage «rmzn-draft:<userId>:<taskId>» → { code, savedAt } ─────────
const DRAFT_PREFIX = 'rmzn-draft:', DRAFT_DAYS = 30
type Draft = { code: string; savedAt: string }
const draftKey = (userId: Id, taskId: Id) => `${DRAFT_PREFIX}${userId}:${taskId}`
function readDraft(key: string): Draft | null {
  try { const value = JSON.parse(localStorage.getItem(key) ?? 'null'); return value && typeof value.code === 'string' ? value : null } catch { return null }
}
const writeDraft = (key: string, code: string) => { try { localStorage.setItem(key, JSON.stringify({ code, savedAt: new Date().toISOString() })) } catch { /* full or private mode: no draft */ } }
const dropDraft = (key: string) => { try { localStorage.removeItem(key) } catch { /* private mode */ } }
/** Drafts older than 30 days (or unreadable) are removed when the app starts. */
function pruneDrafts() {
  try {
    const oldest = Date.now() - DRAFT_DAYS * 86_400_000
    const keys = Array.from({ length: localStorage.length }, (_, i) => localStorage.key(i)).filter((k): k is string => !!k?.startsWith(DRAFT_PREFIX))
    for (const key of keys) { const saved = Date.parse(readDraft(key)?.savedAt ?? ''); if (!(saved >= oldest)) localStorage.removeItem(key) }
  } catch { /* private mode: nothing stored */ }
}

type Request = <T>(action: () => Promise<T>) => Promise<T | undefined>

export default function App() {
  useLocale().revision // Re-render the tree as background translation batches arrive.
  return <ToastProvider><Shell /></ToastProvider>
}

function Shell() {
  const { locale } = useLocale()
  const [me, setMe] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  /** This tab is the board station (it holds a token that /station/current accepts): without a signed-in user it shows the station screen. */
  const [station, setStation] = useState(false)
  /** «Войти как преподаватель» on the station: the usual login form instead of the station screen. */
  const [stationLogin, setStationLogin] = useState(false)
  /** The session expired (a 401): the re-login form over the current screen, nothing unmounted. */
  const [expired, setExpired] = useState(false)
  /** Bumped when another user signs in through the re-login form: the pages mount afresh. */
  const [epoch, setEpoch] = useState(0)
  const detectStation = useCallback(() => (stationToken() ? api<unknown>('/station/current').then(() => true, () => false) : Promise.resolve(false)).then(found => { setStation(found); setStationLogin(false); return found }), [])
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
    try { return await action() } catch (e) { setError(e instanceof Error ? e.message : tr(currentLocale(), "Не удалось выполнить запрос", "Échec de la requête", "تعذر تنفيذ الطلب")); return undefined }
  }, [])
  useEffect(() => {
    pruneDrafts()
    api<MeResponse>('/auth/me')
      .then(value => setMe(value.user))
      .catch(async err => {
        if (!(err instanceof ApiError && err.status === 401)) setError(err instanceof Error ? err.message : tr(currentLocale(), "Не удалось проверить сессию", "Impossible de vérifier la session", "تعذر التحقق من الجلسة"))
        else await detectStation()
      })
      .finally(() => setLoading(false))
  }, [detectStation])
  const signedIn = !!me
  useEffect(() => {
    if (!signedIn) return
    onUnauthorized(() => setExpired(true))
    return () => onUnauthorized(null)
  }, [signedIn])
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
      ? { tone: 'reward', icon: 'flame', title: uiText("Hard mode включён"), text: tr(currentLocale(), `${result.replacedTask ? 'Текущая задача заменена на hard-задачу. ' : ''}Следующие задачи — алгоритмические, +${XP.hardTask} XP за каждую`, `${result.replacedTask ? 'L’exercice actuel a été remplacé par un exercice difficile. ' : ''}Les prochains exercices sont algorithmiques, +${XP.hardTask} XP chacun`, `${result.replacedTask ? 'التمرين الحالي اتبدل بتمرين صعب. ' : ''}التمارين الجاية خوارزمية، +${XP.hardTask} XP لكل تمرين`) }
      : { tone: 'info', icon: 'check', title: uiText("Hard mode выключен"), text: result.replacedTask ? tr(currentLocale(), "Текущая задача заменена на обычную задачу", "L’exercice actuel a été remplacé par un exercice ordinaire", "التمرين الحالي اتبدل بتمرين عادي") : tr(currentLocale(), "Следующие задачи будут обычными", "Les prochains exercices seront ordinaires", "التمارين الجاية حتكون عادية") })
  }
  /** A locked switch: the course may have become ready meanwhile — otherwise explain what is left. */
  async function unlockHardMode() {
    if (!language) return
    setHardBusy(true)
    const fresh = await refreshMe()
    setHardBusy(false)
    const course = (fresh ?? me)?.hardModeCourses?.[language]
    if (course?.ready) { if (!fresh?.hardModeOn) setHardDialog(true); return }
    const left = course ? tr(currentLocale(), `: осталось тем — ${course.remaining}`, ` : notions restantes — ${course.remaining}`, `: الموضوعات المتبقية — ${course.remaining}`) : ''
    toast({ tone: 'info', icon: 'lock', title: uiText("Hard mode пока закрыт"), text: tr(currentLocale(), `Пройди хотя бы одну итерацию по каждой теме курса ${COURSES[language].title}${left}. Темы, подтверждённые диагностикой, уже засчитаны.`, `Termine au moins une étape de chaque notion du cours ${COURSES[language].title}${left}. Les notions validées par le diagnostic sont déjà comptées.`, `أكمل مرحلة واحدة على الأقل في كل موضوع من كورس ${COURSES[language].title}${left}. الموضوعات المؤكدة بالتشخيص محسوبة بالفعل.`) })
  }
  const login = (user: User) => { setError(''); setStationLogin(false); setMe(user) }
  /** After a sign-out the station screen comes back on a station browser. */
  const signedOut = useCallback(() => { setExpired(false); setError(''); setMe(null); detectStation() }, [detectStation])
  const logout = async () => { await request(() => post<void>('/auth/logout')); signedOut() }
  /** The re-login form: the same user — just close it (the screen keeps its state); another user — the pages start afresh. */
  const relogin = (user: User) => {
    setExpired(false); setError('')
    if (user.id === me?.id) { setMe(user); return }
    setMe(user); setEpoch(n => n + 1); setBoardDone(null); setBoard(null); boardTest.current = null
  }
  /** «Сделать этот компьютер компьютером у доски»: the station's token is in this tab; the teacher signs out here and the station screen shows. */
  const becomeStation = useCallback(async () => {
    await post<void>('/auth/logout').catch(() => {})
    setError(''); setMe(null); setStation(true); setStationLogin(false)
  }, [])
  // Test at the board: the called student sees the call on any page; the test and its «Тест сдан» replace the whole screen.
  // boardDone — the format of the test that just finished here (null — none): a TEST ends in the sign-out, an ATTESTATION back in the lessons.
  const [boardDone, setBoardDone] = useState<BoardFormat | null>(null)
  const [board, setBoard] = useBoardCurrent(isStudent && !boardDone)
  const boardTest = useRef<Id | null>(null)
  const boardFormat = useRef<BoardFormat>('TEST')
  useEffect(() => {
    // Only the test this browser runs ends in «Тест сдан» and the sign-out; another session simply goes back.
    if (board?.test && !board.test.elsewhere) { boardTest.current = board.test.id; boardFormat.current = board.test.format ?? 'TEST' }
    // The running test disappeared (the teacher finished or removed it, the server closed it): it is over for this screen too.
    else if (board && boardTest.current !== null) { boardTest.current = null; setBoardDone(boardFormat.current) }
  }, [board])
  const boardFinished = useCallback(() => { boardTest.current = null; setBoardDone(boardFormat.current) }, [])
  // After a test taken from the student's own account on the classroom PC: signed out, the lessons stay open (they may be on the student's PC).
  const boardLogout = useCallback(async () => {
    await post<void>('/auth/logout?keepLessons=true').catch(() => {})
    boardTest.current = null; setBoardDone(null); signedOut()
  }, [signedOut])
  // After an attestation (taken at the student's own computer): nobody is signed out, back to the lessons.
  const attestationBack = useCallback(() => { boardTest.current = null; setBoardDone(null) }, [])
  const leaveStation = useCallback(() => { setStation(false); setStationLogin(false) }, [])
  const openStationLogin = useCallback(() => { setError(''); setStationLogin(true) }, [])
  if (loading) return <div className="center"><Spinner /><span>{tr(locale, "Загружаем…", "Chargement…", "جاري التحميل…")}</span></div>
  if (!me) return station && !stationLogin ? <StationScreen onTeacherLogin={openStationLogin} onGone={leaveStation} />
    : <Login onLogin={login} onError={setError} error={error} onBack={station ? () => { setError(''); setStationLogin(false) } : undefined} />
  const reloginForm = expired && <Relogin user={me} onLogin={relogin} onLogout={logout} />
  if (isStudent && boardDone === 'ATTESTATION') return <>{reloginForm}<AttestationDone onBack={attestationBack} /></>
  if (isStudent && boardDone) return <>{reloginForm}<BoardDone onLogout={boardLogout} /></>
  if (isStudent && board?.test?.elsewhere) return <>{reloginForm}<BoardElsewhere test={board.test} name={me.displayName} /></>
  if (isStudent && board?.test) return <>{reloginForm}<BoardTestScreen key={board.test.id} test={board.test} name={me.displayName} onFinished={boardFinished} /></>
  return <UserContext.Provider value={me.id}><main className={`app ${hardOn ? 'hard' : ''}`}>
    {reloginForm}
    {hardOn && <DangerFrame />}
    {isStudent && board?.call && <BoardCallDialog key={board.call.id} call={board.call} onStarted={test => setBoard({ call: null, test })} />}
    {hardDialog && <HardModeDialog onConfirm={() => setHardMode(true)} onCancel={() => setHardDialog(false)} />}
    <header ref={header} className={`topbar ${scrolled ? 'scrolled' : ''}`}>
      {hardOn && <HeaderTapes />}
      <LocaleSwitch />
      <div className="brand"><span className="logo" aria-hidden="true">R</span><b>Rmzn Tutor</b></div>
      {isStudent && language && <LanguageSwitch value={language} onChange={chooseLanguage} />}
      <div className={`user-chip ${hardOn ? 'on-fire' : ''}`}>
        {isStudent && me.hardModeAllowed && language && <HardModeSwitch on={hardOn} locked={!hardReady} busy={hardBusy} onToggle={() => !hardReady ? unlockHardMode() : hardOn ? setHardMode(false) : setHardDialog(true)} />}
        <span className="avatar" aria-hidden="true">{initials(me.displayName)}</span>
        <span className="user-meta"><b>{me.displayName}</b><small>{hardOn ? 'Hard mode' : me.role === 'STUDENT' ? tr(locale, 'Студент', 'Étudiant', 'طالب') : tr(locale, 'Преподаватель', 'Enseignant', 'أستاذ')}</small></span>
        <button className="icon-button" onClick={logout} aria-label={tr(locale, "Выйти", "Se déconnecter", "خروج")} title={tr(locale, "Выйти", "Se déconnecter", "خروج")}><Icon name="logout" /></button>
      </div>
    </header>
    {error && <div className="flash error" role="alert"><span>{error}</span><button className="flash-close" aria-label={uiText("Скрыть сообщение")} onClick={() => setError('')}><Icon name="x" size={16} /></button></div>}
    {!isStudent ? <TeacherPage key={epoch} request={request} onBecomeStation={becomeStation} />
      : !language ? <LanguagePicker key={epoch} request={request} onPick={chooseLanguage} />
        : <CourseContext.Provider value={COURSES[language]}><StudentPage key={`${language}:${lessonReload}:${epoch}`} request={request} /></CourseContext.Provider>}
  </main><RelayLayer /></UserContext.Provider>
}

/** «Сессия истекла»: signs in again over the current screen; nothing under it is unmounted, so the code on screen stays. */
function Relogin({ user, onLogin, onLogout }: { user: User; onLogin: (me: User) => void; onLogout: () => void }) {
  const { locale } = useLocale()
  const [login, setLogin] = useState(user.login); const [password, setPassword] = useState(''); const [sending, setSending] = useState(false); const [error, setError] = useState('')
  async function submit(e: FormEvent) {
    e.preventDefault(); setSending(true); setError('')
    try { onLogin((await post<MeResponse>('/auth/login', { login: login.trim(), password })).user) }
    catch (err) { setError(err instanceof Error ? err.message : tr(currentLocale(), "Не удалось войти", "Connexion impossible", "تعذر تسجيل الدخول")); setSending(false) }
  }
  return <div className="board-call-backdrop relogin" role="dialog" aria-modal="true" aria-labelledby="relogin-title">
    <form className="card login-card relogin-card" onSubmit={submit}>
      <span className="board-call-icon"><Icon name="lock" size={28} /></span>
      <h2 id="relogin-title" className="title">{user.role === 'STUDENT' ? tr(locale, 'Сессия истекла — войди снова, твой код сохранён', 'La session a expiré : reconnecte-toi, ton code est conservé', 'الجلسة انتهت — ادخل تاني، الكود محفوظ') : tr(locale, 'Сессия истекла — войдите снова', 'La session a expiré — reconnectez-vous', 'الجلسة انتهت — سجل الدخول تاني')}</h2>
      <p className="muted">{user.role === 'STUDENT' ? tr(locale, 'Всё на экране останется как было. После входа повтори последнее действие.', 'Tout restera à l’écran. Après la connexion, répète ta dernière action.', 'كل شي في الشاشة حيفضل زي ما هو. بعد الدخول كرر آخر خطوة.') : tr(locale, 'Экран останется как был. После входа повторите последнее действие.', 'L’écran restera inchangé. Après la connexion, répétez votre dernière action.', 'الشاشة حتفضل زي ما هي. بعد الدخول كرر آخر خطوة.')}</p>
      <label>{tr(locale, "Логин", "Identifiant", "اسم المستخدم")}<input required value={login} onChange={e => setLogin(e.target.value)} autoComplete="username" autoCapitalize="none" spellCheck={false} /></label>
      <label>{tr(locale, "Пароль", "Mot de passe", "كلمة المرور")}<input required type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" autoFocus /></label>
      {error && <p className="form-error shake" role="alert" key={error}>{error}</p>}
      <button className="primary big" disabled={sending}>{sending ? <><Spinner /> {tr(locale, "Входим…", "Connexion…", "جاري الدخول…")}</> : <>{tr(locale, "Войти", "Se connecter", "دخول")} <Icon name="arrow" /></>}</button>
      <button type="button" className="ghost small-button" onClick={onLogout}><Icon name="logout" size={15} /> {tr(locale, "Выйти", "Se déconnecter", "خروج")}</button>
    </form>
  </div>
}

function LanguageSwitch({ value, onChange }: { value: CourseLanguage; onChange: (language: CourseLanguage) => void }) {
  return <nav className="lang-switch" aria-label={uiText("Курс")} style={{ '--active': LANGUAGES.indexOf(value) } as CSSProperties}>
    <span className="segmented-thumb" aria-hidden="true" />
    {LANGUAGES.map(language => <button key={language} className={language === value ? 'active' : ''} aria-pressed={language === value} onClick={() => language !== value && onChange(language)}>
      <span className={`lang-dot ${COURSES[language].key}`} aria-hidden="true" />{COURSES[language].title}
    </button>)}
  </nav>
}

/** First visit: the student chooses a course. Both stay available later through the switch in the header. */
function LanguagePicker({ request, onPick }: { request: Request; onPick: (language: CourseLanguage) => void }) {
  const { locale } = useLocale()
  const [solved, setSolved] = useState<Partial<Record<CourseLanguage, number>>>({})
  useEffect(() => {
    for (const language of LANGUAGES) request(() => api<Progress>(withCourse('/progress', language))).then(value => { if (value) setSolved(s => ({ ...s, [language]: experience(value).solved })) })
  }, [request])
  return <section className="picker">
    <div className="enter">
      <p className="eyebrow">{tr(locale, "Выбор курса", "Choix du cours", "اختيار الكورس")}</p>
      <h1 className="display small">{tr(locale, "Что будем учить?", "Qu’allons-nous apprendre ?", "عايز تتعلم شنو؟")}</h1>
      <p className="muted">{tr(locale, "Оба курса устроены одинаково: диагностика, объяснения и задачи от простых к сложным. Переключиться можно в любой момент — прогресс у каждого курса свой.", "Les deux cours suivent le même principe : diagnostic, explications et exercices progressifs. Tu peux changer de cours à tout moment ; chaque progression est conservée séparément.", "الكورسين بنفس الطريقة: اختبار وشرح وتمارين بتتدرج في الصعوبة. ممكن تبدل في أي وقت، وتقدمك في كل كورس محفوظ براهو.")}</p>
    </div>
    <div className="picker-grid">{LANGUAGES.map((language, i) => {
      const course = COURSES[language]
      return <button key={language} className={`lang-card ${course.key}`} onClick={() => onPick(language)} style={{ animationDelay: `${120 + i * 80}ms` }}>
        <span className="lang-logo" aria-hidden="true">{course.logo}</span>
        <h2>{course.title}</h2>
        <p>{language === "JAVA" ? tr(locale, course.pitch, "Typage strict et programmation orientée objet. Pour le backend, Android et les grands systèmes.", "أنواع صارمة وبرمجة كائنية. للباك إند وأندرويد والأنظمة الكبيرة.") : tr(locale, course.pitch, "Une syntaxe simple et concise. Automatisation, analyse de données, backend et apprentissage automatique.", "صياغة بسيطة وواضحة. للأتمتة وتحليل البيانات والباك إند وتعلم الآلة.")}</p>
        <ul>{(locale === "ru" ? course.tags : language === "JAVA" ? (locale === "fr" ? ["POO", "Backend", "Android"] : ["البرمجة الكائنية", "باك إند", "Android"]) : (locale === "fr" ? ["Syntaxe simple", "Données", "Automatisation"] : ["صياغة بسيطة", "بيانات", "أتمتة"])).map(tag => <li key={tag}>{tag}</li>)}</ul>
        {!!solved[language] && <span className="stat-line">{tr(locale, "Уже решено задач", "Exercices déjà résolus", "التمارين الحليتها")}: {solved[language]}</span>}
        <span className="go">{solved[language] ? tr(locale, 'Продолжить', 'Continuer', 'واصل') : tr(locale, 'Начать', 'Commencer', 'ابدأ')} {course.title} <Icon name="arrow" /></span>
      </button>
    })}</div>
  </section>
}

function Login({ onLogin, onError, error, onBack }: { onLogin: (me: User) => void; onError: (message: string) => void; error: string; onBack?: () => void }) {
  const { locale } = useLocale()
  const [login, setLogin] = useState(''); const [password, setPassword] = useState(''); const [sending, setSending] = useState(false)
  async function submit(e: FormEvent) {
    e.preventDefault(); setSending(true); onError('')
    try { onLogin((await post<MeResponse>('/auth/login', { login: login.trim(), password })).user) }
    catch (err) { onError(err instanceof Error ? err.message : tr(currentLocale(), "Не удалось войти", "Connexion impossible", "تعذر تسجيل الدخول")); setSending(false) }
  }
  return <main className="login">
    <section className="login-hero" aria-hidden="false">
      <div className="blob blob-a" /><div className="blob blob-b" />
      <div className="brand light"><span className="logo" aria-hidden="true">R</span><b>Rmzn Tutor</b></div>
      <h1 className="display">{tr(locale, 'Учим код.', 'Apprendre à coder.', 'نتعلم البرمجة.')}<br /><span className="accent">{tr(locale, 'В твоём темпе.', 'À ton rythme.', 'على راحتك.')}</span></h1>
      <p className="hero-lead">{tr(locale, 'Java и Python с нуля: короткая диагностика, понятные объяснения и задачи, которые становятся сложнее ровно тогда, когда ты готов.', 'Java et Python depuis zéro : un court diagnostic, des explications claires et des exercices qui évoluent à ton rythme.', 'اتعلم Java وPython من البداية: اختبار قصير، شرح واضح وتمارين بتتدرج مع مستواك.')}</p>
      <div className="code-card" aria-hidden="true">
        <span className="dots"><i /><i /><i /></span>
        <code>streak = <span className="n">1</span>{'\n'}<span className="k">while</span> learning:{'\n'}    streak += <span className="n">1</span>{'\n'}print(<span className="s">"Level up!"</span>)<span className="caret" /></code>
      </div>
      <ul className="hero-points"><li><Icon name="code" size={16} /> {uiText("Java и Python")}</li><li><Icon name="target" size={16} /> {tr(locale, '3 задачи на итерацию', '3 exercices par étape', '٣ تمارين في كل مرحلة')}</li><li><Icon name="flame" size={16} /> {tr(locale, 'Серии и достижения', 'Séries et réussites', 'سلاسل وإنجازات')}</li><li><Icon name="chat" size={16} /> {tr(locale, 'Помощник рядом', 'Un assistant à tes côtés', 'مساعد معاك')}</li></ul>
    </section>
    <section className="login-panel">
      <LocaleSwitch />
      <form className="card login-card enter" onSubmit={submit}>
        <p className="eyebrow">{tr(locale, "Вход", "Connexion", "تسجيل الدخول")}</p>
        <h2 className="title">{tr(locale, "С возвращением", "Bon retour", "مرحب بيك تاني")}</h2>
        <p className="muted">{tr(locale, "Войди по данным, которые выдал преподаватель.", "Connecte-toi avec les identifiants fournis par ton enseignant.", "ادخل بالبيانات المداك ليها الأستاذ.")}</p>
        <label>{tr(locale, "Логин", "Identifiant", "اسم المستخدم")}<input required value={login} onChange={e => setLogin(e.target.value)} autoComplete="username" autoCapitalize="none" spellCheck={false} /></label>
        <label>{tr(locale, "Пароль", "Mot de passe", "كلمة المرور")}<input required type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" /></label>
        {error && <p className="form-error shake" role="alert" key={error}>{error}</p>}
        <button className="primary big" disabled={sending}>{sending ? <><Spinner /> {tr(locale, "Входим…", "Connexion…", "جاري الدخول…")}</> : <>{tr(locale, "Войти", "Se connecter", "دخول")} <Icon name="arrow" /></>}</button>
        {onBack && <button type="button" className="ghost small-button" onClick={onBack}><Icon name="back" size={15} /> {tr(locale, "Назад к компьютеру у доски", "Retour à l’ordinateur du tableau", "الرجوع لكمبيوتر السبورة")}</button>}
      </form>
    </section>
  </main>
}

type LoadState = 'loading' | 'ready' | 'failed'

function StudentPage({ request }: { request: Request }) {
  const { locale } = useLocale()
  const [diagnostic, setDiagnostic] = useState<Diagnostic | null>(null)
  const [lesson, setLesson] = useState<LearningNext | null>(null)
  const [state, setState] = useState<LoadState>('loading')
  /** The open lesson while its next task is being prepared: it can be finished without waiting. */
  const [preparing, setPreparing] = useState<Lesson | null>(null)
  const [progress, setProgress] = useState<Progress | null>(null)
  const [otherProgress, setOtherProgress] = useState<Partial<Record<CourseLanguage, Progress>>>({})
  const [othersReady, setOthersReady] = useState(false)
  const [tab, setTab] = useState<StudentTab>('lesson')
  const toast = useToast()
  const course = useCourse()
  const loadId = useRef(0)
  // Inactivity: the server finishes an open lesson idleMinutes after its last activity (task load, run, submission, chat message).
  // The page mirrors that countdown with the client clock to warn the student and to notice when the server has closed the lesson.
  const idleMs = useRef(0) // 0 = no countdown: no open lesson, content being prepared, or the server does not finish idle lessons
  const idleMinutes = useRef(20) // for the notice text
  const deadline = useRef(0); const warned = useRef(false); const checking = useRef(false)
  const [idleWarning, setIdleWarning] = useState(false)
  const [ended, setEnded] = useState<LessonEnd | null>(null)
  /** Starts the countdown for a freshly loaded lesson (null stops it). The load itself is activity, so it starts no earlier than now. */
  const armIdle = useCallback((open: Lesson | null) => {
    const minutes = open?.idleMinutes ?? 0
    idleMs.current = minutes > 0 ? minutes * 60_000 : 0
    if (minutes > 0) idleMinutes.current = minutes
    const last = open ? parseDate(open.lastActivityAt ?? open.startedAt).getTime() : NaN
    deadline.current = Math.max(Number.isNaN(last) ? 0 : last, Date.now()) + idleMs.current
    warned.current = false; setIdleWarning(false)
  }, [])
  const touch = useCallback(() => { if (!idleMs.current) return; deadline.current = Date.now() + idleMs.current; warned.current = false; setIdleWarning(false) }, [])
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
    setState('loading'); setPreparing(null); armIdle(null)
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
    // Finished elsewhere (another tab, the teacher, a logout, inactivity) while the task was being prepared.
    if (next.reason === 'LESSON_FINISHED') { setLesson(null); setEnded({ reason: next.lesson?.finishReason ?? null, minutes: next.lesson?.idleMinutes || idleMinutes.current }); return setState('ready') }
    if (next.retakeDone) { toast(retakeToast(next.retakeDone)); loadProgress() }
    if (next.practiceDone) { toast(practiceToast(next.practiceDone)); loadProgress() }
    armIdle(next.lesson); setEnded(null); setLesson(next); setState('ready')
  }, [request, loadProgress, course.id, armIdle, toast])
  /** «Повторить»: starts a re-take of a closed topic (and a lesson if none is open) and shows its first task. */
  const startRetake = useCallback(async (skillCode: string) => {
    const started = await request(() => post<{ retake: Retake }>('/retakes', { language: course.id, skillCode }))
    if (started) { setTab('lesson'); load() }
  }, [request, course.id, load])
  /** «Тренировочная аттестация»: asked from the lesson or «Темы», confirmed in the dialog; the lesson's task waits meanwhile. */
  const [practiceAsk, setPracticeAsk] = useState(false); const [practiceBusy, setPracticeBusy] = useState(false)
  const askPractice = useCallback(() => setPracticeAsk(true), [])
  const cancelPractice = useCallback(() => setPracticeAsk(false), [])
  const startPractice = useCallback(async () => {
    setPracticeBusy(true)
    const started = await request(() => post<{ practice: Practice }>('/attestation-practice', { language: course.id }))
    setPracticeBusy(false); setPracticeAsk(false)
    if (started) { setTab('lesson'); load() }
  }, [request, course.id, load])
  useEffect(() => { load() }, [load])
  // Responses that arrive after the page is gone (logout, course switch) are ignored.
  useEffect(() => () => { loadId.current++ }, [])

  /** The lesson is no longer open on the server: back to «Начать урок», as after «Завершить урок», with a notice why. */
  const lessonEnded = useCallback((reason: Lesson['finishReason']) => { armIdle(null); setLesson(null); setEnded({ reason, minutes: idleMinutes.current }); load() }, [armIdle, load])
  const openId = state === 'ready' && lesson ? lesson.lesson.id : null
  /** Asks the server whether the lesson is still open; called after the deadline (+ grace for its minute check) and after failed actions. */
  const recheck = useCallback(async () => {
    if (openId === null || checking.current) return
    const id = loadId.current; checking.current = true
    const value = await api<{ lesson: Lesson | null }>(withCourse('/lessons/current', course.id)).catch(() => undefined)
    checking.current = false
    if (!value || id !== loadId.current) return // offline: the next tick tries again; a newer load wins
    const current = value.lesson
    if (current && current.id !== openId) return load() // finished and a new one started in another tab
    if (!current) return lessonEnded(Date.now() >= deadline.current ? 'IDLE' : null)
    const minutes = current.idleMinutes ?? 0
    if (minutes <= 0) return armIdle(null)
    idleMs.current = minutes * 60_000; idleMinutes.current = minutes
    // Activity elsewhere moves the deadline; otherwise the server closes the lesson at its next minute check — look again in a minute.
    const last = parseDate(current.lastActivityAt ?? current.startedAt).getTime()
    deadline.current = Math.max(Number.isNaN(last) ? 0 : last + idleMs.current, Date.now() - IDLE_GRACE_MS + 60_000)
    if (Date.now() < deadline.current - IDLE_WARNING_MS) { warned.current = false; setIdleWarning(false) }
  }, [openId, course.id, load, lessonEnded, armIdle])
  const activity = useCallback((ok: boolean) => { if (ok) touch(); else recheck() }, [touch, recheck])
  // One timer per open lesson: the warning 3 minutes before the deadline, the re-check after it. Hidden tabs throttle timers, so waking up checks at once.
  useEffect(() => {
    if (openId === null) return
    const tick = () => {
      if (!idleMs.current) return
      const now = Date.now()
      if (now >= deadline.current + IDLE_GRACE_MS) recheck()
      else if (now >= deadline.current - IDLE_WARNING_MS && !warned.current) { warned.current = true; setIdleWarning(true) }
    }
    const timer = setInterval(tick, IDLE_TICK_MS)
    const onWake = () => { if (document.visibilityState === 'visible') tick() }
    document.addEventListener('visibilitychange', onWake); window.addEventListener('focus', onWake)
    return () => { clearInterval(timer); document.removeEventListener('visibilitychange', onWake); window.removeEventListener('focus', onWake) }
  }, [openId, recheck])

  // Celebrate milestones that the attempt response reveals (iteration closed, topic mastered), then refresh stats.
  const onProgress = useCallback((skills: SkillProgress[]) => {
    setProgress(previous => {
      if (previous) for (const skill of skills) {
        const before = previous.skills.find(s => s.skillCode === skill.skillCode)
        if (!before) continue
        if (skill.mastered && !before.mastered) toast({ tone: 'reward', icon: 'award', title: tr(currentLocale(), `Тема освоена: ${skill.title}`, `Notion maîtrisée : ${skill.title}`, `اكتمل الموضوع: ${skill.title}`), text: tr(currentLocale(), `+${XP.mastery} XP за полное освоение`, `+${XP.mastery} XP pour la maîtrise complète`, `+${XP.mastery} XP للإتقان الكامل`) })
        else if (skill.completedIterations > before.completedIterations) toast({ tone: 'reward', icon: 'target', title: tr(currentLocale(), `Итерация ${skill.completedIterations} из ${ITERATIONS} завершена`, `Étape ${skill.completedIterations} sur ${ITERATIONS} terminée`, `اكتملت المرحلة ${skill.completedIterations} من ${ITERATIONS}`), text: `${skill.title} · +${XP.iteration} XP` })
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
    if (unlocked.current) for (const a of now) if (!unlocked.current.has(a.id)) toast({ tone: 'reward', icon: a.icon, title: `${uiText("Достижение")}: ${uiText(a.title)}`, text: uiText(a.description) })
    unlocked.current = new Set(now.map(a => a.id))
  }, [progress, otherProgress, othersReady, toast, course.id])

  if (!diagnostic) return state === 'failed'
    ? <section className="empty-state enter"><h1 className="title">{uiText("Не удалось загрузить данные")}</h1><button className="primary" onClick={load}><Icon name="refresh" /> {uiText("Повторить")}</button></section>
    : <div className="center"><Spinner /><span>{tr(locale, "Загружаем…", "Chargement…", "جاري التحميل…")}</span></div>
  if (!diagnostic.completed) return <DiagnosticForm diagnostic={diagnostic} request={request} onDone={load} />
  const currentSkill = lesson?.skill ? progress?.skills.find(s => s.skillCode === lesson.skill?.code) : undefined
  const practiceInfo = progress?.attestationPractice
  const ongoing = openId === null ? null : lesson?.practice ? 'practice' : lesson?.retake ? 'retake' : null
  return <>
    {practiceAsk && practiceInfo?.available && <PracticeDialog info={practiceInfo} busy={practiceBusy} onStart={startPractice} onCancel={cancelPractice} />}
    {progress && <Hud progress={progress} />}
    <nav className="segmented four student-tabs" role="tablist" style={{ '--active': STUDENT_TABS.findIndex(t => t.id === tab) } as CSSProperties}>
      <span className="segmented-thumb" aria-hidden="true" />
      {STUDENT_TABS.map(t => <button key={t.id} role="tab" aria-label={uiText(t.title)} aria-selected={tab === t.id} className={tab === t.id ? 'active' : ''} onClick={() => setTab(t.id)}>
        <Icon name={t.icon} size={16} /> <span className="tab-long">{uiText(t.title)}</span><span className="tab-short">{uiText(t.short)}</span></button>)}
    </nav>
    {idleWarning && openId !== null && <div className="lesson-notice warn" role="alert"><Icon name="clock" size={18} /><span>{uiText("Урок завершится через 3 минуты: нет запусков кода, отправок и сообщений помощнику. Запусти код или напиши помощнику, чтобы продолжить.")}</span></div>}
    {ended && !lesson && <div className="lesson-notice" role="status"><Icon name="flag" size={18} /><span>{lessonEndText(ended)}</span><button className="flash-close" aria-label={uiText("Скрыть сообщение")} onClick={() => setEnded(null)}><Icon name="x" size={16} /></button></div>}
    {/* All tabs stay mounted so leaving the lesson does not discard the code in the editor. */}
    <div hidden={tab !== 'topics'} className={tab === 'topics' ? 'enter' : ''}><TopicsView progress={progress} onRetake={startRetake} lessonOpen={openId !== null} ongoing={ongoing} onPractice={askPractice} /></div>
    <div hidden={tab !== 'grades'} className={tab === 'grades' ? 'enter' : ''}><GradesView progress={progress} visible={tab === 'grades'} /></div>
    <div hidden={tab !== 'achievements'} className={tab === 'achievements' ? 'enter' : ''}><AchievementsView progress={progress} otherProgress={otherProgress} /></div>
    <div hidden={tab !== 'lesson'} className={tab === 'lesson' ? 'enter' : ''}>
      {state === 'loading' ? <LessonSkeleton lesson={preparing} request={request} onFinished={load} />
        : state === 'failed' ? <section className="empty-state enter"><h2 className="title">{uiText("Не удалось загрузить урок")}</h2><button className="primary" onClick={load}><Icon name="refresh" /> {uiText("Повторить")}</button></section>
          : <LessonActivity.Provider value={activity}><LessonView lesson={lesson} skillProgress={currentSkill} progress={progress} request={request} refresh={load} onProgress={onProgress} onRetake={startRetake} onPractice={askPractice} /></LessonActivity.Provider>}
    </div>
  </>
}

function Hud({ progress }: { progress: Progress }) {
  const level = experience(progress)
  const days = streak(progress.activity)
  const xp = useCountUp(level.xp)
  return <section className="hud enter" aria-label={uiText("Твой прогресс")}>
    <div className="hud-level">
      <Ring value={level.into / level.need} size={58}><b>{level.level}</b></Ring>
      <div className="hud-level-text">
        <small>{uiText("Уровень")} {level.level}</small>
        <b>{tr(currentLocale(), level.rank, ["Débutant", "Explorateur", "Praticien", "Codeur", "Développeur", "Ingénieur", "Maître du code"][Math.min(level.level - 1, 6)], ["مبتدئ", "مستكشف", "ممارس", "مبرمج", "مطوّر", "مهندس", "أستاذ البرمجة"][Math.min(level.level - 1, 6)])}</b>
        <div className="xp-bar" role="progressbar" aria-valuemin={0} aria-valuemax={level.need} aria-valuenow={level.into} aria-label={uiText("Опыт до следующего уровня")}><i style={{ width: `${(level.into / level.need) * 100}%` }} /></div>
        <small className="xp-caption"><span className="tabular">{xp}</span> {uiText("XP · ещё")} {level.need - level.into} {uiText("до уровня")} {level.level + 1}</small>
      </div>
    </div>
    <div className={`hud-stat streak ${days.activeToday ? 'lit' : ''}`}>
      <span className="hud-icon flame"><Icon name="flame" size={22} /></span>
      <div><b className="tabular">{days.count}</b><small>{days.count === 1 ? uiText("день подряд") : days.count >= 2 && days.count <= 4 ? uiText("дня подряд") : uiText("дней подряд")}</small></div>
      <div className="week" aria-label={uiText("Активность за неделю")}>{days.week.map((d, i) => <span key={i} className={`${d.active ? 'on' : ''} ${d.today ? 'today' : ''}`} title={d.label}><i />{d.label}</span>)}</div>
    </div>
    <div className="hud-stat course-cover" title={uiText("Тема закрыта, если освоена практикой или подтверждена диагностикой")}>
      <span className="hud-icon bolt"><Icon name="bolt" size={22} /></span>
      <div className="cover-text"><b className="tabular">{level.solved}</b><small>{uiText("задач решено")}</small>
        <div className="cover-bar" role="progressbar" aria-label={uiText("Закрыто тем курса")} aria-valuemin={0} aria-valuemax={level.topics} aria-valuenow={level.closed}><i style={{ width: `${level.topics ? (level.closed / level.topics) * 100 : 0}%` }} /></div>
        <small className="tabular">{uiText("тем закрыто")} {level.closed} {uiText("из")} {level.topics}</small>
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
      ? { tone: 'reward', icon: 'sparkle', title: tr(currentLocale(), `Диагностика: подтверждено тем — ${confirmed}`, `Diagnostic : ${confirmed} notions validées`, `التشخيص: ${confirmed} موضوع مؤكد`), text: tr(currentLocale(), `+${confirmed * XP.confirmed} XP · эти темы пропустим, к практике: ${gaps}`, `+${confirmed * XP.confirmed} XP · notions à pratiquer : ${gaps}`, `+${confirmed * XP.confirmed} XP · موضوعات للتدريب: ${gaps}`) }
      : { tone: 'info', icon: 'target', title: uiText("Диагностика завершена"), text: tr(currentLocale(), `Начнём с самого начала — тем к практике: ${gaps}`, `Commençons par le début : ${gaps} notions à pratiquer`, `نبدأ من البداية: ${gaps} موضوع للتدريب`) })
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
  if (!question) return <section className="empty-state enter"><h1 className="title">{uiText("Диагностика пока недоступна")}</h1><p className="muted">{uiText("Вопросы ещё не загружены. Обратись к преподавателю.")}</p></section>
  const answeredCount = Object.keys(answers).length
  return <section className="diagnostic">
    <div className="enter">
      <p className="eyebrow">{uiText("Первичная диагностика ·")} {course.title}</p>
      <h1 className="display small">{uiText("Поймём, с чего начать")}</h1>
      <p className="muted">{uiText("Здесь нет оценки. Если не уверен — смело выбирай «Не знаю», так мы точнее подберём старт.")}</p>
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
      {index > 0 && <button className="ghost" disabled={sending} onClick={() => go(index - 1)}><Icon name="back" /> {uiText("Назад")}</button>}
      <span className="kbd-hint">{uiText("Клавиши")} <kbd>1</kbd>–<kbd>{question.options.length + 1}</kbd> {uiText("и")} <kbd>Enter</kbd> {uiText("· отвечено")} {answeredCount}</span>
      {last
        ? <button className="primary" disabled={!answered || sending} onClick={save}>{sending ? <><Spinner /> {uiText("Сохраняем…")}</> : <>{uiText("Завершить диагностику")} <Icon name="check" /></>}</button>
        : <button className="primary" disabled={!answered} onClick={() => go(index + 1)}>{uiText("Далее")} <Icon name="arrow" /></button>}
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
    toast({ tone: 'info', icon: 'flag', title: uiText("Урок завершён"), text: uiText("Если задача ещё готовилась, она будет ждать тебя в начале следующего урока") })
    onFinished()
  }
  return <section className="lesson" aria-busy="true">
    {lesson
      ? <div className="lesson-heading">
        <div className="preparing-title"><p className="eyebrow">{course.title} {uiText("· Урок")} {lesson.number}</p><span className="sk sk-title" /></div>
        <button className="ghost" disabled={working} onClick={() => finish(lesson)}>{working ? <><Spinner /> {uiText("Завершаем…")}</> : <><Icon name="flag" size={16} /> {uiText("Завершить урок")}</>}</button>
      </div>
      : <div className="skeleton-head"><span className="sk sk-line short" /><span className="sk sk-title" /></div>}
    <div className="loading-note"><Spinner /> {uiText("Готовим урок… Подбор новой задачи может занять до минуты.")}</div>
    <div className="lesson-grid"><div className="sk sk-card tall" /><div className="sk sk-card" /></div>
  </section>
}

function LessonView({ lesson, skillProgress, progress, request, refresh, onProgress, onRetake, onPractice }: { lesson: LearningNext | null; skillProgress?: SkillProgress; progress: Progress | null; request: Request; refresh: () => void; onProgress: (skills: SkillProgress[]) => void; onRetake: (skillCode: string) => void; onPractice: () => void }) {
  const [working, setWorking] = useState(false)
  const course = useCourse()
  const toast = useToast()
  // «Тренировочная аттестация»: the countdown starts from the server's secondsLeft; at 0 the hint and the assistant open, nothing closes.
  const practice = lesson?.practice && !lesson.practice.finished ? lesson.practice : undefined
  const practiceEnds = useMemo(() => practice ? Date.now() + Math.max(0, practice.secondsLeft) * 1000 : null, [practice])
  const timeUp = usePassed(practiceEnds)
  /** When this screen saw the practice's task accepted: the plate stops counting. */
  const [solvedAt, setSolvedAt] = useState<number | null>(null)
  const practicePassed = useCallback(() => setSolvedAt(at => at ?? Date.now()), [])
  const practiceRunning = !!practice && !timeUp && solvedAt === null
  async function endRetake(retake: Retake) {
    setWorking(true); const ended = await request(() => post<{ retake: Retake }>(`/retakes/${retake.id}/finish`)); setWorking(false)
    if (ended) { toast(retakeToast(ended.retake)); refresh() }
  }
  async function endPractice(open: Practice) {
    if (!window.confirm(tr(currentLocale(), "Завершить тренировочную аттестацию? Задача не решена — попытка запишется без решения, урок продолжится.", "Terminer l’évaluation blanche ? L’exercice n’est pas résolu : la tentative sera enregistrée sans solution et le cours continuera.", "تنهي الامتحان التدريبي؟ التمرين ما اتحل — المحاولة حتتسجل بدون حل والدرس حيواصل."))) return
    setWorking(true); const ended = await request(() => post<{ practice: Practice }>(`/attestation-practice/${open.id}/finish`)); setWorking(false)
    if (ended) { toast(practiceToast(ended.practice)); refresh() }
  }
  async function start() { setWorking(true); const started = await request(() => post<{ lesson: Lesson }>(withCourse('/lessons/start', course.id))); setWorking(false); if (started) refresh() }
  async function finish(current: Lesson, hasTask: boolean) {
    if (hasTask && !window.confirm(tr(currentLocale(), "Текущая задача ещё не решена. Завершить урок?", "L’exercice actuel n’est pas encore résolu. Terminer le cours ?", "التمرين الحالي لسه ما اتحل. تنهي الدرس؟"))) return
    setWorking(true); const finished = await request(() => post(`/lessons/${current.id}/finish`)); setWorking(false); if (finished) refresh()
  }
  if (!lesson) return <section className="empty-state start enter">
    <span className="empty-icon"><Icon name="play" size={28} /></span>
    <h1 className="display small">{uiText("Готов к уроку")} {course.title}?</h1>
    <p className="muted">{uiText("Сервис выберет следующую тему по результатам диагностики и предыдущим занятиям.")}</p>
    <button className="primary big" disabled={working} onClick={start}>{working ? <><Spinner /> {uiText("Готовим урок…")}</> : <>{uiText("Начать урок")} <Icon name="arrow" /></>}</button>
  </section>
  const finished = lesson.reason === 'NO_DUE_SKILL' || lesson.reason === 'COURSE_COMPLETE' || lesson.reason === 'HARD_BANK_COMPLETE'
  const title = practice ? tr(currentLocale(), "Тренировочная аттестация", "Évaluation blanche", "امتحان تدريبي") : lesson.skill?.title ?? (lesson.reason === 'COURSE_COMPLETE' ? tr(currentLocale(), "Все темы курса закрыты", "Toutes les notions du cours sont acquises", "كل موضوعات الكورس مكتملة") : lesson.reason === 'HARD_BANK_COMPLETE' ? tr(currentLocale(), "Все hard-задачи решены", "Tous les exercices difficiles sont résolus", "كل التمارين الصعبة اتحلت") : lesson.reason === 'NO_DUE_SKILL' ? tr(currentLocale(), "На сегодня задач больше нет", "Plus d’exercices pour aujourd’hui", "ما في تمارين تانية اليوم") : tr(currentLocale(), "Текущий урок", "Cours en cours", "الدرس الحالي"))
  const practiceInfo = progress?.attestationPractice
  const free = !practice && !lesson.retake
  const need = free && practiceInfo && !practiceInfo.available ? practiceInfo.needTopics : null
  const retryable = lesson.reason === 'LLM_GENERATION_FAILED_VALIDATION' || lesson.reason === 'RUNNER_UNAVAILABLE' || lesson.reason === 'LLM_RATE_LIMITED'
  const emptyMessage = lesson.reason === 'NO_TASK_AVAILABLE' ? tr(currentLocale(), "Подходящей задачи в банке пока нет. Преподаватель увидит это состояние.", "Aucun exercice adapté dans la banque pour le moment. L’enseignant en sera informé.", "ما في تمرين مناسب في البنك حالياً. الأستاذ حيشوف الحالة دي.")
    : lesson.reason === 'LLM_GENERATION_FAILED_VALIDATION' ? tr(currentLocale(), "Новая задача не прошла проверку. Попробуй запросить её ещё раз.", "Le nouvel exercice n’a pas passé la vérification. Demande-en un autre.", "التمرين الجديد ما اجتاز الفحص. حاول تطلبه تاني.")
      : lesson.reason === 'RUNNER_UNAVAILABLE' ? tr(currentLocale(), `Проверка ${course.title} сейчас недоступна. Попробуй ещё раз позже.`, `La vérification ${course.title} est indisponible. Réessaie plus tard.`, `فحص ${course.title} غير متاح حالياً. حاول تاني بعدين.`)
        : lesson.reason === 'LLM_RATE_LIMITED' ? tr(currentLocale(), "Новые задачи сейчас создаются слишком часто — сработал лимит курса. Попробуй через несколько минут или спроси преподавателя.", "Trop d’exercices sont créés en ce moment : la limite du cours est atteinte. Réessaie dans quelques minutes ou demande à l’enseignant.", "تم إنشاء تمارين كتيرة والحد المسموح للكورس انتهى. حاول بعد دقائق أو اسأل الأستاذ.")
        : lesson.reason === 'COURSE_COMPLETE' ? tr(currentLocale(), "Каждая тема освоена практикой или подтверждена диагностикой — задач для обязательной практики не осталось.", "Chaque notion est maîtrisée par la pratique ou validée par le diagnostic : il ne reste plus d’exercice obligatoire.", "كل موضوع مكتمل بالتدريب أو مؤكد بالتشخيص — ما في تمارين إجبارية متبقية.")
          : lesson.reason === 'NO_DUE_SKILL' ? tr(currentLocale(), "Все задачи этого урока выполнены — отличная работа! Повторения запланированы на следующие уроки.", "Tous les exercices de ce cours sont terminés. Les révisions sont prévues dans les prochains cours.", "كل تمارين الدرس اكتملت! المراجعات مخططة للدروس الجاية.")
            : lesson.reason === 'HARD_BANK_COMPLETE' ? tr(currentLocale(), "Ты решил все задачи hard-режима этого курса. Выключи hard-режим, чтобы вернуться к обычным задачам и повторам тем.", "Tu as résolu tous les exercices difficiles de ce cours. Désactive le mode difficile pour revenir aux exercices et révisions ordinaires.", "حليت كل تمارين الوضع الصعب. اقفل الوضع الصعب عشان ترجع للتمارين والمراجعات العادية.") : tr(currentLocale(), "Контент урока загружается.", "Le contenu du cours se charge.", "محتوى الدرس جاري تحميله.")
  return <section className="lesson">
    <div className="lesson-heading enter">
      <div>
        <p className="eyebrow">{course.title} {uiText("· Урок")} {lesson.lesson.number}{lesson.skill && !practice ? tr(currentLocale(), ` · Блок ${lesson.skill.blockNo}`, ` · Bloc ${lesson.skill.blockNo}`, ` · القسم ${lesson.skill.blockNo}`) : ''}</p>
        <h1 className="display small">{title}</h1>
        {!!need && <p className="muted small practice-need">{practiceNeedText(need)}</p>}
      </div>
      <div className="lesson-heading-actions">
        {free && practiceInfo?.available && <button className="secondary" disabled={working} onClick={onPractice} title={tr(currentLocale(), `Одна задача как на аттестации, ${minutesText(practiceInfo.minutes)}, без оценки`, `Un exercice comme à l’évaluation, ${minutesText(practiceInfo.minutes)}, sans note`, `تمرين زي الامتحان، ${minutesText(practiceInfo.minutes)}، بدون درجة`)}><Icon name="award" size={16} /> {uiText("Тренировочная аттестация")}</button>}
        <button className="ghost" disabled={working} onClick={() => finish(lesson.lesson, !!lesson.task)}>{working ? <><Spinner /> {uiText("Завершаем…")}</> : <><Icon name="flag" size={16} /> {uiText("Завершить урок")}</>}</button>
      </div>
    </div>
    {practice && practiceEnds !== null && <PracticePlate practice={practice} endsAt={practiceEnds} timeUp={timeUp} solvedAt={solvedAt} busy={working} onFinish={() => endPractice(practice)} />}
    {lesson.retake && !practice && <div className="retake-plate enter" role="status">
      <Icon name="refresh" size={18} />
      <span><b>{uiText("Повторение")}</b> · {lesson.retake.skillTitle} · {Math.min(lesson.retake.given, lesson.retake.total)} {uiText("из")} {lesson.retake.total}
        {lesson.retake.similar && <span className="retake-similar" title={uiText("Новых задач по этой теме пока нет — это та же история с другими числами")}>{uiText("похожая на решённую")}</span>}</span>
      <button className="ghost small-button" disabled={working} onClick={() => endRetake(lesson.retake!)}>{uiText("Закончить повторение")}</button>
    </div>}
    {lesson.explanation && <article className="card explanation enter">
      <h2 className="card-title"><span className="chip-icon"><Icon name="book" size={16} /></span> {uiText("Объяснение")}</h2>
      <Markdown>{lesson.explanation.content}</Markdown>
    </article>}
    {lesson.task
      ? <TaskWorkspace key={lesson.task.id} task={lesson.task} skillProgress={lesson.retake || practice ? undefined : skillProgress} llm={lesson.llm} request={request} onNext={refresh} onProgress={onProgress}
        practiceEnds={practiceRunning ? practiceEnds : null} onPassed={practice ? practicePassed : undefined} />
      : <div className="lesson-grid enter">
        <article className={`card task empty-task ${finished ? 'done' : ''}`}>
          {finished && <span className="empty-icon success"><Icon name={lesson.reason === 'COURSE_COMPLETE' ? 'award' : 'check'} size={28} /></span>}
          {lesson.reason === 'COURSE_COMPLETE' && <Burst trigger={1} />}
          <h2 className="title">{lesson.reason === 'COURSE_COMPLETE' ? uiText("Курс пройден") : finished ? uiText("Урок можно завершить") : uiText("Задача ещё не подготовлена")}</h2>
          <p className="muted">{emptyMessage}</p>
          {retryable && <button className="secondary" onClick={refresh}><Icon name="refresh" /> {uiText("Повторить")}</button>}
          {(lesson.reason === 'NO_DUE_SKILL' || lesson.reason === 'COURSE_COMPLETE') && progress && <RetakeChoices progress={progress} onRetake={onRetake} />}
        </article>
        <Chat llm={lesson.llm} request={request} />
      </div>}
  </section>
}

type ConsoleState = { run: ConsoleRun; origin: ConsoleOrigin }

/** practiceEnds — while a practice's timer runs (client clock): the hint is hidden and the assistant closed; onPassed — the task was accepted. */
function TaskWorkspace({ task, skillProgress, llm, request, onNext, onProgress, practiceEnds, onPassed }: { task: Task; skillProgress?: SkillProgress; llm?: LlmStatus; request: Request; onNext: () => void; onProgress: (skills: SkillProgress[]) => void; practiceEnds?: number | null; onPassed?: () => void }) {
  const course = useCourse()
  const starter = task.starterCode || course.fallback
  // The code survives a reload or a re-login: a draft in this browser, per user and task, until the task is accepted.
  const userId = useContext(UserContext)
  const key = userId !== null ? draftKey(userId, task.id) : null
  const [draft] = useState(() => key ? readDraft(key) : null)
  const [restored, setRestored] = useState(!!draft && draft.code !== starter)
  const [code, setCode] = useState(restored && draft ? draft.code : starter)
  const accepted = useRef(false)
  useEffect(() => {
    if (!key || accepted.current) return
    const timer = setTimeout(() => { if (code === starter) dropDraft(key); else writeDraft(key, code) }, 500)
    return () => clearTimeout(timer)
  }, [key, code, starter])
  const onAccepted = useCallback(() => { accepted.current = true; if (key) dropDraft(key); onPassed?.() }, [key, onPassed])
  const startOver = useCallback(() => { if (key) dropDraft(key); setCode(starter); setRestored(false) }, [key, starter])
  // The console on screen; the assistant sees the same text when the student asks about it.
  const [screen, setScreen] = useState<ConsoleState | null>(null)
  // «Разобрать с помощником»: the check says why a solution was rejected, the assistant helps to understand it.
  const [prefill, setPrefill] = useState<{ text: string; nonce: number } | undefined>()
  const askAssistant = useCallback((text: string) => setPrefill({ text, nonce: Date.now() }), [])
  const practiceRunning = practiceEnds != null
  return <div className="lesson-grid enter">
    <TaskEditor task={task} skillProgress={skillProgress} code={code} onCodeChange={setCode} request={request} onNext={onNext} onProgress={onProgress} console={screen} onConsole={setScreen} onAskAssistant={llm?.available && !practiceRunning ? askAssistant : undefined}
      restored={restored} onStartOver={startOver} onAccepted={onAccepted} hideHint={practiceRunning} />
    <Chat llm={llm} request={request} taskId={task.id} sourceCode={code} consoleOutput={screen ? consoleText(screen.run) : undefined} prefill={prefill} lockedUntil={practiceEnds} />
  </div>
}

function IterationSteps({ done, iteration, pulse }: { done: number; iteration: number; pulse: boolean }) {
  const tasks = iterationTasks(iteration - 1)
  return <div className="steps" aria-label={tr(currentLocale(), `Итерация ${iteration} из ${ITERATIONS}, решено ${done} из ${tasks}`, `Étape ${iteration} sur ${ITERATIONS}, ${done} exercices résolus sur ${tasks}`, `المرحلة ${iteration} من ${ITERATIONS}، حليت ${done} من ${tasks}`)}>
    <span className="steps-label">{uiText("Итерация")} {iteration}/{ITERATIONS}</span>
    <span className="steps-track">{Array.from({ length: tasks }, (_, i) => <i key={i} className={`${i < done ? 'on' : ''} ${pulse && i === done - 1 ? 'pop' : ''}`} />)}</span>
  </div>
}

function TaskEditor({ task, skillProgress, code, onCodeChange, request, onNext, onProgress, console: screen, onConsole, onAskAssistant, restored, onStartOver, onAccepted, hideHint }: {
  task: Task; skillProgress?: SkillProgress; code: string; onCodeChange: (code: string) => void; request: Request; onNext: () => void; onProgress: (skills: SkillProgress[]) => void
  console: ConsoleState | null; onConsole: (console: ConsoleState) => void; onAskAssistant?: (text: string) => void
  /** The code came from this browser's draft; «Начать заново» goes back to the starter. onAccepted — the draft is no longer needed. */
  restored: boolean; onStartOver: () => void; onAccepted: () => void
  /** A practice's timer runs: the statement's «Подсказка» section is not shown. */
  hideHint?: boolean
}) {
  // Hard tasks read their input: the student types it here to try the program with «Запустить».
  const [stdin, setStdin] = useState('')
  const [attempt, setAttempt] = useState<Attempt | null>(null); const [sending, setSending] = useState(false); const [tries, setTries] = useState(0)
  const [running, setRunning] = useState(false); const [runs, setRuns] = useState(0)
  const resultRef = useRef<HTMLDivElement>(null)
  const consoleRef = useRef<HTMLElement>(null)
  const course = useCourse()
  const activity = useContext(LessonActivity)
  // Snapshot the step on mount: after the iteration closes the server resets successes to 0, but this task still was step 3 of 3.
  const [step] = useState(() => { const completed = skillProgress?.completedIterations ?? 0; return { done: Math.min(skillProgress?.iterationSuccesses ?? 0, iterationTasks(completed) - 1), iteration: Math.min(completed + 1, ITERATIONS) } })
  async function submit() {
    setSending(true)
    const result = await request(() => post<Attempt & { progress?: SkillProgress[] }>('/attempts', { taskId: task.id, sourceCode: code }))
    setSending(false); activity(!!result)
    if (!result) return
    setAttempt(result); setTries(t => t + 1)
    if (result.passed) onAccepted()
    // A hard task reads input: a run without it shows only an input error, so its console is not shown here.
    if (result.console && !task.hard) onConsole({ run: result.console, origin: 'attempt' })
    if (result.progress) onProgress(result.progress)
  }
  /**
   * «Запустить»: runs the code as is and shows the console. Not a submission: no attempt, no credit, no «Попытка N».
   * The failed check's verdict belongs to the code as it was then; after a run of the edited code it would only confuse.
   */
  async function run() {
    setRunning(true)
    const result = await request(() => post<{ console: ConsoleRun }>(withCourse('/run', course.id), task.hard ? { sourceCode: code, stdin } : { sourceCode: code }))
    setRunning(false); activity(!!result)
    if (!result) return
    setAttempt(null)
    onConsole({ run: result.console, origin: 'run' }); setRuns(n => n + 1)
  }
  useEffect(() => { if (runs) consoleRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }) }, [runs])
  useEffect(() => { if (attempt) resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }) }, [attempt, tries])
  const passed = !!attempt?.passed
  const ask = () => onAskAssistant?.(tr(currentLocale(), `Мою отправку не приняли. Вот что сказала проверка:\n\n${attempt?.output ?? ''}\n\nПомоги понять, в чём ошибка, но не пиши готовое решение.`, `Ma soumission n’a pas été acceptée. Voici le résultat de la vérification :\n\n${attempt?.output ?? ''}\n\nAide-moi à comprendre l’erreur sans écrire la solution complète.`, `حلي ما اتقبل. دي نتيجة الفحص:\n\n${attempt?.output ?? ''}\n\nساعدني أفهم الخطأ بدون ما تكتب الحل كامل.`))
  const statement = hideHint ? withoutHint(task.statement) : task.statement
  const hintHidden = hideHint && statement !== task.statement.trimEnd()
  return <section className={`card task ${passed ? 'is-passed' : ''} ${task.hard ? 'hard-task' : ''}`}>
    <div className="task-head">
      {task.hard
        ? <span className="task-tag hard"><Icon name="flame" size={14} /> {uiText("Hard · задача")} {step.done + 1}</span>
        : <span className="task-tag"><Icon name="code" size={14} /> {uiText("Задача")} {step.done + 1}</span>}
      {skillProgress && <IterationSteps done={step.done + (passed ? 1 : 0)} iteration={step.iteration} pulse={passed} />}
    </div>
    {task.redo && <p className="redo-note"><Icon name="refresh" size={15} /> {uiText("Преподаватель попросил решить эту задачу заново — прежнее решение не засчитано.")}</p>}
    <h2 className="title">{task.integrative && <span className="integ-chip"><Icon name="target" size={13} /> {uiText("Комплексная задача")}</span>}{task.title}</h2>
    {task.integrative && <p className="integ-note">{uiText("Тема урока вместе с тем, что ты уже прошёл, — как на аттестации")}</p>}
    <Markdown>{statement}</Markdown>
    {hintHidden && <p className="practice-hint-note"><Icon name="lock" size={14} /> {uiText("Подсказка откроется, когда выйдет время")}</p>}
    {restored && !passed && <p className="draft-note" role="status"><Icon name="refresh" size={15} /><span>{uiText("Восстановлен твой код — он сохранился в этом браузере.")}</span>
      <button type="button" className="ghost small-button" onClick={() => { if (window.confirm(tr(currentLocale(), "Вернуть начальный код задачи? Твой код будет удалён.", "Restaurer le code initial ? Ton code sera supprimé.", "ترجع الكود المبدئي؟ الكود الحالي حيتحذف."))) onStartOver() }}>{uiText("Начать заново")}</button></p>}
    <div className="code-label"><span>{uiText("Решение на")} {course.title}</span><CodeMirror className="code-editor" value={code} height="clamp(18rem, 48vh, 32rem)" extensions={EDITOR_EXTENSIONS[course.id]} onChange={onCodeChange} editable={!passed} aria-label={tr(currentLocale(), `Редактор решения на ${course.title}`, `Éditeur de solution ${course.title}`, `محرر الحل بلغة ${course.title}`)} /></div>
    {task.hard && !passed && <label className="stdin-field">
      <span>{uiText("Входные данные для «Запустить»")}</span>
      <textarea value={stdin} onChange={e => setStdin(e.target.value)} rows={3} spellCheck={false} placeholder="Например, ввод из примера в условии" />
    </label>}
    <div className="task-actions">
      {passed
        ? <button className="reward big" onClick={onNext}>{uiText("Следующая задача")} <Icon name="arrow" /></button>
        : <>
          <button className="primary big" disabled={sending || running || !code.trim()} onClick={submit}>{sending ? <><Spinner /> {uiText("Проверяем…")}</> : <><Icon name="play" size={16} /> {uiText("Отправить на проверку")}</>}</button>
          <button className="ghost big" disabled={sending || running || !code.trim()} onClick={run} title={uiText("Запустить программу и посмотреть вывод. Попытка не засчитывается.")}>{running ? <><Spinner /> {uiText("Запускаем…")}</> : <><Icon name="terminal" size={16} /> {uiText("Запустить")}</>}</button>
        </>}
      {tries > 0 && !passed && <span className="muted small">{uiText("Попытка")} {tries}</span>}
    </div>
    {attempt && <div ref={resultRef} key={tries} className={`result ${passed ? 'success' : 'failed'}`} role="status">
      {passed && <Burst trigger={tries} />}
      <div className="result-head">
        <span className="result-icon"><Icon name={passed ? 'check' : 'x'} size={18} /></span>
        <b>{passed ? uiText("Решение принято!") : uiText("Пока не проходит — это нормально")}</b>
        {passed && <span className={`xp-gain ${task.hard ? 'hard' : ''}`}>+{task.hard ? XP.hardTask : XP.task} XP</span>}
      </div>
      {attempt.grader === 'LLM' && <p className="grader-label"><Icon name="sparkle" size={13} /> {uiText("Подход проверен LLM")}</p>}
      {attempt.review
        ? <ReviewVerdict review={attempt.review} />
        : attempt.mismatch
          ? <OutputCompare mismatch={attempt.mismatch} />
          : <>
            {!passed && <p className="muted small">{uiText("Посмотри на вывод проверки ниже или спроси помощника, где искать ошибку.")}</p>}
            {attempt.output && <pre>{attempt.output}</pre>}
          </>}
      {!passed && onAskAssistant && <button type="button" className="ghost small-button ask-assistant" onClick={ask}><Icon name="chat" size={15} /> {uiText("Разобрать с помощником")}</button>}
    </div>}
    {screen && (!passed || screen.origin === 'attempt') && <ConsolePanel ref={consoleRef} key={`${screen.origin}-${runs}-${tries}`} run={screen.run} origin={screen.origin} language={course.id} />}
  </section>
}

/** A wrong output next to the expected one, line by line, with line breaks and trailing spaces made visible. */
function OutputCompare({ mismatch }: { mismatch: OutputMismatch }) {
  const visible = (text: string) => text.length ? text.replace(/ +$/gm, m => '·'.repeat(m.length)).replace(/\n/g, '↵\n') : '(пусто)'
  return <div className="output-compare">
    <p className="review-summary">{uiText("Вывод программы отличается от нужного.")}</p>
    <div className="compare-grid">
      <div><small>{uiText("Нужно")}</small><pre>{visible(mismatch.expected)}</pre></div>
      <div><small>{uiText("Твоя программа")}</small><pre>{visible(mismatch.actual)}</pre></div>
    </div>
    <p className="muted small">{uiText("↵ — перевод строки, · — пробел в конце строки.")}</p>
  </div>
}

/** The reviewer's verdict: why the solution was (not) accepted, each problem with its line and where to look. */
function ReviewVerdict({ review }: { review: Review }) {
  return <div className="review">
    {review.summary && <p className="review-summary">{review.summary}</p>}
    {review.issues.length > 0 && <ul className="review-issues">{review.issues.map((issue, i) => <li key={i}>
      {issue.line != null && <span className="review-line">{uiText("Строка")} {issue.line}</span>}
      <span className="review-problem">{issue.problem}</span>
      {issue.hint && <span className="review-hint"><Icon name="target" size={13} /> {issue.hint}</span>}
    </li>)}</ul>}
  </div>
}

type ChatState = { messages: ChatMessage[]; llm: LlmStatus; quota?: ChatQuota }

/** lockedUntil — a practice's timer runs until then (client clock): the composer gives way to «Помощник откроется, когда выйдет время». */
function Chat({ llm, request, taskId, sourceCode, consoleOutput, prefill, lockedUntil }: { llm?: LlmStatus; request: Request; taskId?: Id; sourceCode?: string; consoleOutput?: string; prefill?: { text: string; nonce: number }; lockedUntil?: number | null }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]); const [text, setText] = useState(''); const [status, setStatus] = useState<LlmStatus | undefined>(llm); const [sending, setSending] = useState(false)
  /** The server still holds the assistant for a practice (its clock is ahead of this one): its message, the question stays in the box. */
  const [held, setHeld] = useState('')
  const composer = useRef<HTMLTextAreaElement>(null)
  // A question prepared from a rejected check; the student can edit it before sending.
  useEffect(() => { if (prefill) { setText(prefill.text); composer.current?.focus() } }, [prefill])
  const listRef = useRef<HTMLDivElement>(null)
  const course = useCourse()
  const activity = useContext(LessonActivity)
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
    const hold = { message: '' }
    const result = await request(() => post<{ message: ChatMessage; llm?: LlmStatus; quota?: ChatQuota }>(withCourse('/chat', course.id), body)
      .catch(e => { if (e instanceof ApiError && e.code === 'PRACTICE_RUNNING') { hold.message = e.message; return undefined } throw e }))
    activity(!!result || !!hold.message)
    setHeld(hold.message)
    if (hold.message) {
      // Not stored: the question goes back to the box, to send once the time is up.
      setMessages(m => m.filter(x => !(typeof x.id === 'string' && x.id.startsWith('local-')))); setText(t => t || content)
    } else if (result) {
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
  const unavailable = status && !status.available ? humanize(status.reason) || tr(currentLocale(), "Помощник временно недоступен.", "L’assistant est temporairement indisponible.", "المساعد غير متاح مؤقتاً.") : ''
  const limited = !!quota?.retryAfterSeconds
  const left = quota?.hourLimit ? Math.max(0, quota.hourLimit - quota.hourUsed) : null
  const locked = lockedUntil != null
  return <aside className="card chat">
    <div className="chat-head">
      <span className="bot-avatar" aria-hidden="true"><Icon name="sparkle" size={18} /></span>
      <div><h2 className="card-title">{uiText("Учебный помощник")}</h2><small className={`presence ${unavailable || locked ? 'off' : 'on'}`}>{unavailable ? uiText("Недоступен") : locked ? uiText("Закрыт до конца времени") : uiText("На связи")}</small></div>
    </div>
    <div className="messages" ref={listRef} aria-live="polite">
      {messages.length ? messages.map(m => <div key={m.id} className={`message ${m.role.toLowerCase()}`}><Markdown>{m.content}</Markdown><small>{m.role === 'STUDENT' ? uiText("Ты") : uiText("Помощник")} · {fmt(m.createdAt)}</small></div>)
        : <div className="chat-empty"><Icon name="chat" size={22} /><p>{uiText("Помощник подскажет ход мысли, а не готовый ответ. Спроси, что непонятно в условии или почему код не работает.")}</p></div>}
      {sending && <div className="message assistant typing" aria-label={uiText("Помощник думает")}><span /><span /><span /></div>}
    </div>
    {unavailable ? <p className="muted small chat-off">{unavailable}</p>
      : locked ? <p className="chat-off practice-lock"><Icon name="lock" size={15} /><span>{uiText("Помощник откроется, когда выйдет время — через")} <PracticeClock endsAt={lockedUntil} /></span></p>
      : <form onSubmit={send} className="composer">
      {taskId !== undefined && <p className="chat-code-note"><Icon name="code" size={13} /> {uiText("Помощник видит текущий код из редактора")}</p>}
      <div className="composer-row">
        <textarea ref={composer} value={text} onChange={e => setText(e.target.value)} onKeyDown={onKeyDown} placeholder={limited ? tr(currentLocale(), 'Лимит сообщений исчерпан', 'Limite de messages atteinte', 'وصلت حد الرسائل') : tr(currentLocale(), 'Опиши, где возникло затруднение…', 'Décris ce qui te pose problème…', 'اشرح وين واجهتك الصعوبة…')} aria-label={tr(currentLocale(), 'Ваш вопрос учебному помощнику', 'Votre question à l’assistant', 'سؤالك للمساعد')} rows={2} disabled={limited} />
        <button className="primary icon-only" disabled={sending || !text.trim() || limited} aria-label={uiText("Отправить")} title={uiText("Отправить (Ctrl+Enter)")}>{sending ? <Spinner /> : <Icon name="send" />}</button>
      </div>
      {held ? <p className="quota-note limited" role="status">{held}</p>
        : limited ? <p className="quota-note limited">{uiText("Лимит сообщений помощнику исчерпан. Снова можно через")} {Math.max(1, Math.ceil(quota!.retryAfterSeconds / 60))} {uiText("мин. — а пока перечитай объяснение или спроси преподавателя.")}</p>
        : left !== null && left <= 5 && <p className="quota-note">{uiText("Осталось сообщений в этот час:")} {left} {uiText("из")} {quota!.hourLimit}</p>}
    </form>}
  </aside>
}

/** The student's tabs; on a phone the short titles. */
type StudentTab = 'lesson' | 'topics' | 'grades' | 'achievements'
const STUDENT_TABS: { id: StudentTab; icon: Parameters<typeof Icon>[0]['name']; title: string; short: string }[] = [
  { id: 'lesson', icon: 'code', title: 'Текущий урок', short: 'Урок' },
  { id: 'topics', icon: 'chart', title: 'Темы', short: 'Темы' },
  { id: 'grades', icon: 'award', title: 'Оценки и план', short: 'Оценки' },
  { id: 'achievements', icon: 'star', title: 'Достижения', short: 'Награды' },
]

const TOPIC_FILTERS: { id: 'todo' | 'confirmed' | 'mastered' | 'all'; label: string; match: (state: SkillState) => boolean }[] = [
  { id: 'todo', label: 'Нужна практика', match: state => state === 'gap' || state === 'started' || state === 'new' },
  { id: 'confirmed', label: 'Подтверждено диагностикой', match: state => state === 'confirmed' },
  { id: 'mastered', label: 'Освоено практикой', match: state => state === 'mastered' },
  { id: 'all', label: 'Все', match: () => true },
]

/** lessonOpen — a lesson of this course is open; ongoing — what that lesson runs now besides its own tasks. */
type Ongoing = 'practice' | 'retake' | null
function TopicsView({ progress, onRetake, lessonOpen, ongoing, onPractice }: { progress: Progress | null; onRetake: (skillCode: string) => void; lessonOpen: boolean; ongoing: Ongoing; onPractice: () => void }) {
  const [filter, setFilter] = useState<(typeof TOPIC_FILTERS)[number]['id']>('todo')
  const course = useCourse()
  if (!progress) return <section><h1 className="display small">{uiText("Темы")}</h1><div className="sk sk-card" /></section>
  const level = experience(progress)
  const counts = Object.fromEntries(TOPIC_FILTERS.map(f => [f.id, progress.skills.filter(skill => f.match(skillState(skill))).length]))
  const active = TOPIC_FILTERS.find(f => f.id === filter)!
  const skills = progress.skills.filter(skill => active.match(skillState(skill)))
  const coverage = level.topics ? Math.round((level.closed / level.topics) * 100) : 0
  return <section className="progress-page">
    <h1 className="display small">{uiText("Темы ·")} {course.title}</h1>
    <div className="stat-grid">
      <Stat icon="sparkle" label={level.diagnosticXp ? tr(currentLocale(), `Опыт · ${level.diagnosticXp} за диагностику`, `Expérience · ${level.diagnosticXp} pour le diagnostic`, `الخبرة · ${level.diagnosticXp} للتشخيص`) : uiText("Опыт")} value={level.xp} suffix="XP" />
      <Stat icon="bolt" label={uiText("Задач решено")} value={level.solved} />
      <Stat icon="flag" label={tr(currentLocale(), `Курс закрыт · ${level.closed} из ${level.topics} тем`, `Cours terminé · ${level.closed} notions sur ${level.topics}`, `الكورس مكتمل · ${level.closed} من ${level.topics} موضوع`)} value={coverage} suffix="%" />
      <Stat icon="award" label={tr(currentLocale(), `Освоено практикой${level.confirmed ? ` · ${level.confirmed} подтверждено диагностикой` : ''}`, `Acquis par la pratique${level.confirmed ? ` · ${level.confirmed} validés par le diagnostic` : ''}`, `مكتمل بالتدريب${level.confirmed ? ` · ${level.confirmed} مؤكد بالتشخيص` : ''}`)} value={level.mastered} />
    </div>
    <PracticeCard info={progress.attestationPractice} lessonOpen={lessonOpen} ongoing={ongoing} onStart={onPractice} />
    <div className="topic-filters" role="tablist" aria-label={uiText("Темы")}>{TOPIC_FILTERS.map(f => <button key={f.id} role="tab" aria-selected={f.id === filter} className={f.id === filter ? 'active' : ''} onClick={() => setFilter(f.id)}>
      {uiText(f.label)}<span className="tabular">{counts[f.id]}</span></button>)}</div>
    {skills.some(skillClosed) && <RetakeLagHint progress={progress} />}
    <div className="card skills">{skills.length
      ? skills.map(skill => <TopicRow key={skill.skillCode} skill={skill} retake={progress.retakes?.find(r => r.skillCode === skill.skillCode)} lag={lagOf(progress)} onRetake={onRetake} practiceOpen={ongoing === 'practice'} />)
      : <p className="muted">{filter === 'todo' ? uiText("Все темы закрыты — практикой или диагностикой. Отличная работа!") : filter === 'confirmed' ? uiText("Диагностика пока не подтвердила ни одной темы.") : filter === 'mastered' ? uiText("Пока ни одна тема не освоена полностью: для этого нужны три итерации на разных уроках.") : uiText("Тем пока нет.")}</p>}</div>
  </section>
}

/** «Оценки и план»: answers at the board and attestations, then the pace to the session. Grades reload each time the tab opens. */
function GradesView({ progress, visible }: { progress: Progress | null; visible: boolean }) {
  const course = useCourse()
  return <section className="progress-page">
    <h1 className="display small">{uiText("Оценки и план ·")} {course.title}</h1>
    <StudentBoardGrades language={course.id} visible={visible} />
    {!progress ? <div className="sk sk-card" /> : progress.session && <StudentSessionCard session={progress.session} />}
  </section>
}

function AchievementsView({ progress, otherProgress }: { progress: Progress | null; otherProgress: Partial<Record<CourseLanguage, Progress>> }) {
  const course = useCourse()
  const list = useMemo(() => progress ? achievements(progress, course.id) : [], [progress, course.id])
  const shared = useMemo(() => progress ? commonAchievements({ ...otherProgress, [course.id]: progress }) : [], [progress, otherProgress, course.id])
  if (!progress) return <section><h1 className="display small">{uiText("Достижения")}</h1><div className="sk sk-card" /></section>
  return <section className="progress-page">
    <h1 className="display small">{uiText("Достижения ·")} {course.title}</h1>
    <p className="achievement-group"><span className={`lang-dot ${course.key}`} aria-hidden="true" />{uiText("Курс")} {course.title}<span className="muted">{uiText("· получено")} {unlocked(list)} {uiText("из")} {list.length}</span></p>
    <AchievementGrid items={list} />
    <p className="achievement-group"><Icon name="globe" size={15} />{uiText("Общие — для обоих курсов")}<span className="muted">{uiText("· получено")} {unlocked(shared)} {uiText("из")} {shared.length}</span></p>
    <AchievementGrid items={shared} />
  </section>
}

/** Practice progress and the diagnostic result side by side; a confirmed topic is never drawn as practiced. */
function TopicRow({ skill, retake, lag, onRetake, practiceOpen }: { skill: SkillProgress; retake?: RetakeHistory; lag: number; onRetake: (skillCode: string) => void; practiceOpen?: boolean }) {
  const state = skillState(skill)
  const diagnostic = skill.diagnosticTotal ? `${skill.diagnosticCorrect ?? 0}/${skill.diagnosticTotal}` : null
  return <div className={`skill-row ${state}`}>
    <span className="skill-name">{state === 'mastered' ? <Icon name="check" size={15} /> : state === 'confirmed' ? <Icon name="sparkle" size={15} /> : null}{skill.title}</span>
    {state === 'confirmed'
      ? <span className="confirmed-note">{uiText("Подтверждено диагностикой · практика не нужна")}</span>
      : <div className="bar" role="progressbar" aria-valuenow={skillPercent(skill)} aria-valuemin={0} aria-valuemax={100} aria-label={skill.title}><i style={{ width: `${skillPercent(skill)}%` }} /></div>}
    <small className="tabular topic-meta">
      {state === 'mastered' ? uiText("Освоено практикой") : state === 'confirmed' ? null : tr(currentLocale(), `Итерации ${skill.completedIterations}/${ITERATIONS} · задачи ${skill.iterationSuccesses}/${iterationTasks(skill.completedIterations)}`, `Étapes ${skill.completedIterations}/${ITERATIONS} · exercices ${skill.iterationSuccesses}/${iterationTasks(skill.completedIterations)}`, `المراحل ${skill.completedIterations}/${ITERATIONS} · التمارين ${skill.iterationSuccesses}/${iterationTasks(skill.completedIterations)}`)}
      {diagnostic && <span className={`diag-chip ${skill.confirmedByDiagnostic ? 'ok' : 'gap'}`} title={uiText("Результат первичной диагностики по теме")}>{uiText("диагностика")} {diagnostic}</span>}
      {retake && <span className="retake-meta">{retakeTimes(retake)}</span>}
      {skillClosed(skill) && <button className="secondary retake-button" disabled={practiceOpen} onClick={() => onRetake(skill.skillCode)} title={practiceOpen ? uiText("Повторить тему можно после тренировочной аттестации") : lag > 0 ? lagText(lag) : uiText("Три задачи по теме: от простой к сложной. На освоение темы не влияет.")}><Icon name="refresh" size={14} /> {uiText("Повторить")}</button>}
    </small>
  </div>
}

/** The plan line's lag of the student (positive — topics behind), 0 without a plan. */
const lagOf = (progress: Progress) => Math.max(0, progress.session?.lag ?? 0)
const lagText = (lag: number) => tr(currentLocale(), `Ты отстаёшь от плана на ${lag} ${plural(lag, 'тему', 'темы', 'тем')} — сначала лучше пройти новые.`, `Tu as ${lag} notions de retard sur le plan : mieux vaut d’abord étudier les nouvelles.`, `إنت متأخر ${lag} موضوع عن الخطة — الأحسن تبدأ بالموضوعات الجديدة.`)
function plural(n: number, one: string, few: string, many: string) { const m10 = n % 10, m100 = n % 100; return m10 === 1 && m100 !== 11 ? one : m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14) ? few : many }
const retakeTimes = (r: RetakeHistory) => tr(currentLocale(), `Повторено ${r.times} ${plural(r.times, 'раз', 'раза', 'раз')} · последний раз ${parseDate(r.lastAt).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })}`, `Révisé ${r.times} fois · dernière fois le ${parseDate(r.lastAt).toLocaleDateString(currentLocale(), { day: 'numeric', month: 'long' })}`, `اتراجع ${r.times} مرة · آخر مرة ${parseDate(r.lastAt).toLocaleDateString(currentLocale(), { day: 'numeric', month: 'long' })}`)
const retakeToast = (r: Retake) => ({ tone: 'reward' as const, icon: 'refresh' as const, title: tr(currentLocale(), `Повторение пройдено: ${r.passed} из ${r.total}`, `Révision terminée : ${r.passed} sur ${r.total}`, `المراجعة اكتملت: ${r.passed} من ${r.total}`), text: r.skillTitle })

/** A soft hint for a student behind the plan line: re-takes are allowed, new topics come first. */
function RetakeLagHint({ progress }: { progress: Progress }) {
  const lag = lagOf(progress)
  return lag > 0 ? <p className="retake-hint"><Icon name="clock" size={15} /> {lagText(lag)} {uiText("Повторить пройденную тему можно в любой момент.")}</p> : null
}

/** Closed topics to re-take when the lesson has nothing due: the ones re-taken least recently (never first) on top. */
function RetakeChoices({ progress, onRetake }: { progress: Progress; onRetake: (skillCode: string) => void }) {
  const [all, setAll] = useState(false)
  const last = (code: string) => progress.retakes?.find(r => r.skillCode === code)?.lastAt ?? ''
  const closed = progress.skills.filter(skillClosed).sort((a, b) => last(a.skillCode).localeCompare(last(b.skillCode)))
  if (!closed.length) return null
  const shown = all ? closed : closed.slice(0, 5)
  return <div className="retake-choices">
    <h3 className="card-title">{uiText("Повторить пройденную тему")}</h3>
    <RetakeLagHint progress={progress} />
    <ul>{shown.map(s => {
      const r = progress.retakes?.find(x => x.skillCode === s.skillCode)
      return <li key={s.skillCode}><span>{s.title}{r && <small className="muted"> · {retakeTimes(r)}</small>}</span>
        <button className="secondary retake-button" onClick={() => onRetake(s.skillCode)}><Icon name="refresh" size={14} /> {uiText("Повторить")}</button></li>
    })}</ul>
    {closed.length > shown.length && <button className="ghost small-button" onClick={() => setAll(true)}>{uiText("Показать все (")}{closed.length})</button>}
  </div>
}

// ───────── «Тренировочная аттестация»: one attestation-sized task, a 10-minute timer, no grade, no effect on progress ─────────

/** True once the moment `at` (client clock) has passed; re-renders once, at that moment. null — no moment. */
function usePassed(at: number | null) {
  const [passed, setPassed] = useState(() => at !== null && Date.now() >= at)
  useEffect(() => {
    if (at === null) { setPassed(false); return }
    const left = at - Date.now()
    setPassed(left <= 0)
    if (left <= 0) return
    const timer = setTimeout(() => setPassed(true), left)
    // A hidden tab throttles timers: coming back checks at once.
    const onWake = () => { if (Date.now() >= at) setPassed(true) }
    document.addEventListener('visibilitychange', onWake); window.addEventListener('focus', onWake)
    return () => { clearTimeout(timer); document.removeEventListener('visibilitychange', onWake); window.removeEventListener('focus', onWake) }
  }, [at])
  return passed
}

/** The statement without its «Подсказка» section (from that heading to the next heading of the same or a higher level); code blocks are not headings. */
function withoutHint(statement: string) {
  let fence = false, skip = 0
  return statement.split('\n').filter(line => {
    if (/^\s*(```|~~~)/.test(line)) { fence = !fence; return !skip }
    const heading = fence ? null : /^(#{1,6})\s+(.*)$/.exec(line)
    if (heading) {
      const level = heading[1].length
      if (skip && level <= skip) skip = 0
      if (!skip && /^подсказк/i.test(heading[2].trim())) skip = level
    }
    return !skip
  }).join('\n').trimEnd()
}

const practiceNeedText = (n: number) => tr(currentLocale(), `Тренировочная аттестация откроется, когда пройдёшь ещё ${n} ${plural(n, 'тему', 'темы', 'тем')} по порядку`, `L’évaluation blanche sera accessible après ${n} notions supplémentaires suivies dans l’ordre`, `الامتحان التدريبي بيفتح بعد ما تكمل ${n} موضوع إضافي بالترتيب`)
const practiceTopics = (p: { levelTopics: number | null }) => tr(currentLocale(), `темы 1–${p.levelTopics}`, `notions 1–${p.levelTopics}`, `الموضوعات 1–${p.levelTopics}`)
/** «6 мин 12 с», «42 с». */
const durationText = (seconds: number) => { const m = Math.floor(seconds / 60), s = Math.round(seconds % 60); return m ? tr(currentLocale(), `${m} мин ${s} с`, `${m} min ${s} s`, `${m} دقيقة ${s} ثانية`) : tr(currentLocale(), `${s} с`, `${s} s`, `${s} ثانية`) }
const practiceToast = (p: Practice) => {
  const text = tr(currentLocale(), `Тренировочная аттестация · ${practiceTopics(p)}`, `Évaluation blanche · ${practiceTopics(p)}`, `امتحان تدريبي · ${practiceTopics(p)}`)
  return p.result === 'IN_TIME' ? { tone: 'reward' as const, icon: 'award' as const, title: tr(currentLocale(), `Решено${p.seconds != null ? ` за ${durationText(p.seconds)}` : ''} — уложился в ${minutesText(p.minutes)}`, `Résolu${p.seconds != null ? ` en ${durationText(p.seconds)}` : ''} — dans la limite de ${minutesText(p.minutes)}`, `اتحل${p.seconds != null ? ` خلال ${durationText(p.seconds)}` : ''} — في الزمن المحدد ${minutesText(p.minutes)}`), text }
    : p.result === 'LATE' ? { tone: 'info' as const, icon: 'clock' as const, title: tr(currentLocale(), `Решено после времени${p.seconds != null ? `: ${Math.ceil(p.seconds / 60)} мин` : ''}`, `Résolu après le délai${p.seconds != null ? ` : ${Math.ceil(p.seconds / 60)} min` : ''}`, `اتحل بعد الزمن${p.seconds != null ? `: ${Math.ceil(p.seconds / 60)} دقيقة` : ''}`), text }
      : { tone: 'info' as const, icon: 'flag' as const, title: tr(currentLocale(), "Тренировка завершена без решения", "Entraînement terminé sans solution", "التدريب انتهى بدون حل"), text }
}

/** «07:32» counting down to `endsAt` (client clock); red in the last minute. */
function PracticeClock({ endsAt }: { endsAt: number }) {
  const left = endsAt - useNow(250)
  return <b className={`practice-clock tabular ${left < 60_000 ? 'low' : ''}`} role="timer" aria-live="off">{clock(left).padStart(5, '0')}</b>
}

/** Over the practice's task, like the re-take plate: the topics and the time left; after the deadline «Время вышло»; once solved — the time it took. */
function PracticePlate({ practice, endsAt, timeUp, solvedAt, busy, onFinish }: { practice: Practice; endsAt: number; timeUp: boolean; solvedAt: number | null; busy: boolean; onFinish: () => void }) {
  const elapsed = solvedAt === null ? 0 : practice.minutes * 60_000 - (endsAt - solvedAt)
  return <div className={`retake-plate practice-plate enter ${solvedAt !== null ? 'solved' : timeUp ? 'over' : ''}`}>
    <Icon name={solvedAt !== null ? 'check' : 'clock'} size={18} />
    <span><b>{uiText("Тренировочная аттестация")}</b> · {practiceTopics(practice)} · {solvedAt !== null ? <>{uiText("решено за")} <b className="tabular">{clock(elapsed)}</b></>
      : timeUp ? <span role="status"><b>{uiText("Время вышло")}</b> {uiText("— можно дорешать, помощник открыт")}</span>
        : <>{uiText("осталось")} <PracticeClock endsAt={endsAt} /></>}</span>
    {solvedAt === null && <button className="ghost small-button" disabled={busy} onClick={onFinish}>{uiText("Завершить")}</button>}
  </div>
}

/** Before the start: what the practice is; Esc or a click outside cancels. */
function PracticeDialog({ info, busy, onStart, onCancel }: { info: AttestationPractice; busy: boolean; onStart: () => void; onCancel: () => void }) {
  const startRef = useRef<HTMLButtonElement>(null)
  useEffect(() => {
    startRef.current?.focus()
    const onKey = (e: globalThis.KeyboardEvent) => { if (e.key === 'Escape') onCancel() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onCancel])
  return <div className="board-call-backdrop" onClick={busy ? undefined : onCancel}>
    <div className="board-call practice-dialog" role="dialog" aria-modal="true" aria-labelledby="practice-dialog-title" onClick={e => e.stopPropagation()}>
      <span className="board-call-icon"><Icon name="award" size={30} /></span>
      <p className="eyebrow">{uiText("Без оценки")}</p>
      <h2 id="practice-dialog-title" className="display small">{uiText("Тренировочная аттестация")}</h2>
      <p>{uiText("Одна задача как на аттестации:")} {practiceTopics(info)} {uiText("(до «")}{info.levelTitle}»). {minutesText(info.minutes)}{uiText(", помощник закрыт до конца времени. Оценки нет, на прогресс не влияет — можно бросить в любой момент.")}</p>
      <div className="board-confirm-actions">
        <button type="button" className="ghost big" disabled={busy} onClick={onCancel}>{uiText("Отмена")}</button>
        <button type="button" ref={startRef} className="primary big" disabled={busy} onClick={onStart}>{busy ? <><Spinner /> {uiText("Начинаем…")}</> : <>{uiText("Начать")} <Icon name="arrow" /></>}</button>
      </div>
    </div>
  </div>
}

/** «Темы»: the start (or what is left before it opens) and the student's own attempts. Nothing when the course has no pool. */
function PracticeCard({ info, lessonOpen, ongoing, onStart }: { info?: AttestationPractice; lessonOpen: boolean; ongoing: Ongoing; onStart: () => void }) {
  if (!info || (!info.available && info.needTopics == null && !info.history.length)) return null
  const note = !info.available ? null : ongoing === 'practice' ? tr(currentLocale(), "Тренировка идёт — она во вкладке «Урок».", "L’entraînement est en cours dans l’onglet « Cours ».", "التدريب جاري في علامة «الدرس».") : ongoing === 'retake' ? tr(currentLocale(), "Начать можно, когда закончишь повторение темы.", "Tu pourras commencer après la révision de la notion.", "ممكن تبدأ بعد ما تخلص مراجعة الموضوع.") : !lessonOpen ? tr(currentLocale(), "Начни урок — тренировка проходит внутри урока.", "Commence un cours : l’entraînement se fait pendant le cours.", "ابدأ الدرس — التدريب بيكون داخل الدرس.") : null
  return <section className="card practice-card" aria-label={uiText("Тренировочная аттестация")}>
    <div className="practice-card-head">
      <span className="chip-icon"><Icon name="award" size={16} /></span>
      <div>
        <h2 className="card-title">{uiText("Тренировочная аттестация")}</h2>
        <p className="muted small">{info.available ? tr(currentLocale(), `Одна задача как на аттестации: ${practiceTopics(info)} (до «${info.levelTitle}»), ${minutesText(info.minutes)}. Без оценки, на прогресс не влияет.`, `Un exercice comme à l’évaluation : ${practiceTopics(info)} (jusqu’à « ${info.levelTitle} »), ${minutesText(info.minutes)}. Sans note ni effet sur la progression.`, `تمرين زي الامتحان: ${practiceTopics(info)} (حتى «${info.levelTitle}»)، ${minutesText(info.minutes)}. بدون درجة وما بأثر على التقدم.`)
          : info.needTopics ? tr(currentLocale(), `Откроется, когда пройдёшь ещё ${info.needTopics} ${plural(info.needTopics, 'тему', 'темы', 'тем')} по порядку.`, `Disponible après ${info.needTopics} notions supplémentaires suivies dans l’ordre.`, `بيفتح بعد ما تكمل ${info.needTopics} موضوع إضافي بالترتيب.`) : uiText("Пока недоступна.")}</p>
      </div>
      {info.available && !ongoing && <button className="secondary" disabled={!lessonOpen} onClick={onStart}><Icon name="award" size={16} /> {uiText("Начать")}</button>}
    </div>
    {note && <p className="muted small practice-card-note">{note}</p>}
    {info.history.length > 0 && <PracticeAttempts items={info.history} />}
  </section>
}

const PRACTICE_RESULT: Record<NonNullable<PracticeAttempt['result']> | 'OPEN', { label: string; tone: string }> = {
  IN_TIME: { label: 'в срок', tone: 'ok' }, LATE: { label: 'после времени', tone: 'warn' }, NOT_SOLVED: { label: 'без решения', tone: 'bad' }, OPEN: { label: 'идёт', tone: '' },
}
/** «28 окт., 11:20». */
const shortDateTime = (value: string) => parseDate(value).toLocaleString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })

/** Attempts newest first: date, level, task, result and the time to the first pass; the latest five until «Показать все». */
function PracticeAttempts({ items }: { items: PracticeAttempt[] }) {
  const [all, setAll] = useState(false)
  const shown = all ? items : items.slice(0, 5)
  return <>
    <ul className="practice-attempts">{shown.map(a => {
      const result = PRACTICE_RESULT[a.result ?? 'OPEN']
      return <li key={a.id}>
        <span className="muted tabular">{shortDateTime(a.startedAt)}</span>
        <span className="practice-level" title={tr(currentLocale(), `до «${a.levelTitle}»`, `jusqu’à « ${a.levelTitle} »`, `حتى «${a.levelTitle}»`)}>{practiceTopics(a)}</span>
        <span className="practice-task" title={a.taskTitle}>{a.taskTitle}</span>
        <span className={`check-tag ${result.tone}`}>{a.result === 'IN_TIME' ? tr(currentLocale(), result.label, 'dans les temps', 'في الزمن') : a.result === 'LATE' ? tr(currentLocale(), result.label, 'hors délai', 'بعد الزمن') : a.result === 'NOT_SOLVED' ? tr(currentLocale(), result.label, 'sans solution', 'بدون حل') : tr(currentLocale(), result.label, 'en cours', 'جاري')}{a.seconds != null && <span className="tabular"> · {clock(a.seconds * 1000)}</span>}</span>
      </li>
    })}</ul>
    {items.length > shown.length && <button className="ghost small-button practice-more" onClick={() => setAll(true)}>{uiText("Показать все (")}{items.length})</button>}
  </>
}

const unlocked = (items: ReturnType<typeof achievements>) => items.filter(a => a.unlocked).length

function AchievementGrid({ items }: { items: ReturnType<typeof achievements> }) {
  return <div className="achievements">{items.map((a, i) => <div key={a.id} className={`achievement ${a.unlocked ? 'unlocked' : ''}`} style={{ animationDelay: `${i * 40}ms` }}>
    <span className="badge"><Icon name={a.unlocked ? a.icon : 'lock'} size={20} /></span>
    <b>{uiText(a.title)}</b><small>{uiText(a.description)}</small>
    {!a.unlocked && a.goal > 1 && <div className="mini-bar"><i style={{ width: `${(a.current / a.goal) * 100}%` }} /><span className="tabular">{a.current}/{a.goal}</span></div>}
  </div>)}</div>
}

function Stat({ icon, label, value, suffix }: { icon: Parameters<typeof Icon>[0]['name']; label: string; value: number; suffix?: string }) {
  const shown = useCountUp(value)
  return <div className="card stat"><span className="chip-icon"><Icon name={icon} size={18} /></span><b className="tabular">{shown}{suffix && <small> {suffix}</small>}</b><span className="muted small">{label}</span></div>
}

function TeacherPage({ request, onBecomeStation }: { request: Request; onBecomeStation: () => void }) {
  const [students, setStudents] = useState<Student[] | null>(null); const [selected, setSelected] = useState<Student | null>(null)
  const [globalLlm, setGlobalLlm] = useState<LlmStatus | null>(null)
  const [name, setName] = useState(''); const [login, setLogin] = useState(''); const [password, setPassword] = useState(''); const [group, setGroup] = useState(''); const [creating, setCreating] = useState(false)
  const [view, setView] = useState<'students' | 'progress' | 'pairs' | 'board' | 'llm' | 'settings'>('students')
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
    if (student) { setName(''); setLogin(''); setPassword(''); load(); toast({ tone: 'info', icon: 'user', title: uiText("Учётная запись создана"), text: [student.displayName, student.login, student.group].filter(Boolean).join(' · ') }) }
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
  /** From the progress tab: opens the student's card in the list. */
  const openStudent = useCallback((id: Id) => {
    const student = students?.find(x => x.id === id)
    if (!student) return
    if (!inGroup(groupFilter, student.group)) setGroupFilter('')
    setSelected(student); setView('students'); window.scrollTo({ top: 0 })
  }, [students, groupFilter, setGroupFilter])
  /** From a student's card: the progress tab opens on that student (course, group, panel). */
  const [progressFocus, setProgressFocus] = useState<{ id: Id; nonce: number } | null>(null)
  const openProgress = useCallback((id: Id) => {
    setProgressFocus(focus => ({ id, nonce: (focus?.nonce ?? 0) + 1 })); setView('progress'); window.scrollTo({ top: 0 })
  }, [])
  const configDisabled = globalLlm?.reason === 'DISABLED_BY_CONFIGURATION'
  const VIEWS = ['students', 'progress', 'pairs', 'board', 'llm', 'settings'] as const
  const active = VIEWS.indexOf(view)
  const tab = (key: typeof view, icon: Parameters<typeof Icon>[0]['name'], title: string, short: string, onClick = () => setView(key)) =>
    <button role="tab" aria-label={uiText(title)} aria-selected={view === key} className={view === key ? 'active' : ''} onClick={onClick}><Icon name={icon} size={16} /> <span className="tab-long">{uiText(title)}</span><span className="tab-short">{uiText(short)}</span></button>
  const tabs = <nav className="segmented admin-tabs six" role="tablist" style={{ '--active': active, '--col': active % 3, '--row': Math.floor(active / 3) } as CSSProperties}>
    <span className="segmented-thumb" aria-hidden="true" />
    {tab('students', 'user', 'Студенты', 'Студенты')}
    {tab('progress', 'target', 'Прогресс', 'Прогресс', () => { setProgressFocus(null); setView('progress') })}
    {tab('pairs', 'chart', 'Работа на паре', 'На паре')}
    {tab('board', 'flag', 'К доске', 'К доске')}
    {tab('llm', 'chart', 'Аналитика LLM', 'LLM')}
    {tab('settings', 'sparkle', 'Настройки LLM и жребия', 'Настройки')}
  </nav>
  const groupList = students ? groupCounts(students, s => s.group).groups.map(g => g.name) : null
  if (view === 'progress') return <>{tabs}<ProgressAnalytics request={request} onOpenStudent={openStudent} focus={progressFocus} /></>
  if (view === 'pairs') return <>{tabs}<PairWork request={request} groups={groupList} /></>
  if (view === 'board') return <>{tabs}<BoardAdmin request={request} groups={groupList} onBecomeStation={onBecomeStation} /></>
  if (view === 'llm') return <>{tabs}<LlmAnalytics request={request} /></>
  if (view === 'settings') return <>{tabs}<LlmSettingsView request={request} /><DrawSettingsView request={request} /></>
  const counts = groupCounts(students ?? [], s => s.group)
  const groupNames = counts.groups.map(g => g.name)
  const visible = students?.filter(s => inGroup(groupFilter, s.group)) ?? null
  const studying = visible?.filter(s => s.activeLessons?.length).length ?? 0
  const filtered = !!students && !!visible && visible.length !== students.length
  return <>{tabs}<section className="admin">
    <div className="admin-main">
      <div className="enter">
        <p className="eyebrow">{uiText("Преподаватель")}</p>
        <h1 className="display small">{uiText("Студенты")}{students && <span className="count-badge" title={filtered ? tr(currentLocale(), `показано ${visible!.length} из ${students.length}`, `${visible!.length} affichés sur ${students.length}`, `المعروض ${visible!.length} من ${students.length}`) : undefined}>{filtered ? `${visible!.length}/${students.length}` : students.length}</span>}</h1>
        {studying > 0 && <p className="studying-now"><span className="live-dot" aria-hidden="true" />{uiText("Сейчас занимаются:")} {studying}</p>}
      </div>
      <div className="card setting enter">
        <span className="chip-icon"><Icon name="sparkle" size={18} /></span>
        <div><h2 className="card-title">{uiText("LLM для курса")}</h2>
          <p className="muted small">{!globalLlm ? uiText("Загружаем…") : globalLlm.globallyEnabled ? uiText("Помощник и генерация контента включены") : configDisabled ? uiText("Отключена в настройках сервера (APP_LLM_ENABLED)") : uiText("Выключена для всех студентов")}</p></div>
        <Switch checked={!!globalLlm?.globallyEnabled} disabled={!globalLlm || configDisabled} onChange={toggleGlobal} label={uiText("LLM для курса")} />
      </div>
      <div className="card enter">
        <h2 className="card-title"><span className="chip-icon"><Icon name="plus" size={16} /></span> {uiText("Новая учётная запись")}</h2>
        <form className="inline-form" onSubmit={create} autoComplete="off">
          <input placeholder={uiText("Имя")} aria-label={uiText("Имя")} required value={name} onChange={e => setName(e.target.value)} />
          <input placeholder={uiText("Логин")} aria-label={uiText("Логин")} required value={login} onChange={e => setLogin(e.target.value)} autoComplete="off" autoCapitalize="none" spellCheck={false} />
          <input placeholder={uiText("Пароль")} aria-label={uiText("Пароль")} required value={password} onChange={e => setPassword(e.target.value)} autoComplete="new-password" />
          <input placeholder={uiText("Группа")} title={uiText("Группа — необязательно")} aria-label={uiText("Группа, необязательно")} list="known-groups" maxLength={60} value={group} onChange={e => setGroup(e.target.value)} autoComplete="off" />
          <GroupOptions id="known-groups" groups={groupNames} />
          <button className="primary" disabled={creating}>{creating ? <><Spinner /> {uiText("Создаём…")}</> : uiText("Создать")}</button>
        </form>
      </div>
      {students && <div className="group-bar enter">
        <GroupFilter total={students.length} groups={counts.groups} ungrouped={counts.ungrouped} value={groupFilter} onChange={chooseGroup} />
        {groupFilter && groupFilter !== NO_GROUP && <RenameGroup group={groupFilter} groups={groupNames} request={request} onRenamed={to => { chooseGroup(to ?? ''); load() }} />}
      </div>}
      <div className="student-list enter">{!students || !visible ? <p className="muted list-note">{uiText("Загружаем…")}</p> : visible.length
        ? visible.map((s, i) => <button key={s.id} className={selected?.id === s.id ? 'student selected' : 'student'} aria-pressed={selected?.id === s.id} onClick={() => setSelected(s)} style={{ animationDelay: `${i * 30}ms` }}>
          <span className="avatar" aria-hidden="true">{initials(s.displayName)}</span>
          <span className="student-meta"><b>{s.displayName}</b><small>{s.login}{s.group && <span className="group-tag">{s.group}</span>}</small>
            {s.activeLessons?.map(l => <ActiveLessonBadge key={l.language} lesson={l} />)}</span>
          {!!s.hardModeAllowed && <i className={`pill hard ${s.hardModeOn ? 'on' : ''}`} title={s.hardModeOn ? uiText("Hard mode включён") : uiText("Допуск к hard mode есть, режим выключен")}><Icon name="flame" size={12} /> HARD</i>}
          <i className={s.llmEnabled ? 'pill on' : 'pill'}>LLM</i>
        </button>)
        : <p className="muted list-note">{students.length ? uiText("В этой группе студентов нет.") : uiText("Студентов пока нет. Создай первую учётную запись выше.")}</p>}</div>
    </div>
    {selected ? <StudentDetail key={selected.id} student={selected} groups={groupNames} request={request} toggle={() => toggle(selected)} onOpenProgress={() => openProgress(selected.id)} onLlmStatus={onLlmStatus} onUpdated={onUpdated} onDeleted={() => { setStudents(xs => xs && xs.filter(x => x.id !== selected.id)); setSelected(null) }} />
      : <aside className="card student-detail placeholder"><span className="empty-icon"><Icon name="user" size={26} /></span><p className="muted">{uiText("Выбери студента, чтобы увидеть его уроки, решения и переписку с помощником.")}</p></aside>}
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
    toast({ tone: 'info', icon: 'lock', title: uiText("Пароль изменён"), text: result.sessionsClosed ? tr(currentLocale(), `Студент вышел из системы на ${result.sessionsClosed} устр.`, `L’étudiant a été déconnecté sur ${result.sessionsClosed} appareils.`, `تم خروج الطالب من ${result.sessionsClosed} جهاز.`) : tr(currentLocale(), `${student.displayName} войдёт с новым паролем`, `${student.displayName} se connectera avec le nouveau mot de passe`, `${student.displayName} حيدخل بكلمة المرور الجديدة`) })
  }
  const copy = () => navigator.clipboard?.writeText(saved).then(() => toast({ tone: 'info', icon: 'check', title: uiText("Пароль скопирован") })).catch(() => {})
  if (!open) return <button className="ghost small-button" onClick={() => { setOpen(true); setPassword(generatePassword()); setSaved('') }}><Icon name="lock" size={15} /> {uiText("Сменить пароль")}</button>
  return <div className="password-reset enter">
    {saved ? <div className="password-saved">
      <span className="muted small">{uiText("Новый пароль — передай его студенту. После закрытия он больше не будет показан.")}</span>
      <div className="password-row"><code>{saved}</code><button className="secondary" onClick={copy}>{uiText("Скопировать")}</button><button className="ghost" onClick={() => { setOpen(false); setSaved('') }}>{uiText("Готово")}</button></div>
    </div> : <form onSubmit={save} autoComplete="off">
      <label className="small">{uiText("Новый пароль для")} {student.displayName}
        <div className="password-row">
          <input value={password} onChange={e => setPassword(e.target.value)} minLength={6} required autoComplete="new-password" spellCheck={false} aria-describedby="password-hint" />
          <button type="button" className="ghost" onClick={() => setPassword(generatePassword())} title={uiText("Сгенерировать")}>↻</button>
        </div>
      </label>
      <p id="password-hint" className="muted small">{uiText("Не короче 6 символов. Все открытые сессии студента будут завершены.")}</p>
      <div className="password-row"><button className="primary" disabled={saving || password.length < 6}>{saving ? <><Spinner /> {uiText("Сохраняем…")}</> : uiText("Сохранить пароль")}</button><button type="button" className="ghost" onClick={() => setOpen(false)}>{uiText("Отмена")}</button></div>
    </form>}
  </div>
}

/** What the diagnostic confirmed and which topics it flagged, so the teacher sees why practice starts where it does. */
function DiagnosticSummary({ skills }: { skills: SkillProgress[] }) {
  const taken = skills.filter(s => s.diagnosticTotal)
  if (!taken.length) return <p className="diag-summary muted small">{uiText("Диагностика не пройдена")}</p>
  const confirmed = taken.filter(s => s.confirmedByDiagnostic).length
  const gaps = taken.filter(s => !s.confirmedByDiagnostic && !s.mastered)
  return <div className="diag-summary">
    <span className="small"><b>{uiText("Диагностика:")}</b> {uiText("подтверждено")} {confirmed} {uiText("из")} {taken.length} {uiText("тем")}{gaps.length ? tr(currentLocale(), `, пробелов — ${gaps.length}`, `, lacunes — ${gaps.length}`, `، الفجوات — ${gaps.length}`) : uiText(", пробелов нет")}</span>
    {gaps.length > 0 && <div className="gap-chips">{gaps.slice(0, 8).map(g => <span key={g.skillCode} className="diag-chip gap" title={tr(currentLocale(), `диагностика ${g.diagnosticCorrect ?? 0}/${g.diagnosticTotal}`, `diagnostic ${g.diagnosticCorrect ?? 0}/${g.diagnosticTotal}`, `التشخيص ${g.diagnosticCorrect ?? 0}/${g.diagnosticTotal}`)}>{g.title} {g.diagnosticCorrect ?? 0}/{g.diagnosticTotal}</span>)}{gaps.length > 8 && <span className="muted small">{uiText("и ещё")} {gaps.length - 8}</span>}</div>}
  </div>
}

/** The course's closed topics in the teacher's card, each with «Снять освоение»: the topic starts over for the student. */
function ClosedTopics({ skills, onReopen }: { skills: SkillProgress[]; onReopen: (skill: SkillProgress) => void }) {
  const closed = skills.filter(skillClosed)
  if (!closed.length) return null
  return <details className="closed-topics">
    <summary className="small"><b>{uiText("Закрытые темы:")}</b> {closed.length}</summary>
    <ul>{closed.map(s => <li key={s.skillCode}>
      <span className="small">{s.title} <span className="muted">{s.mastered ? uiText("освоена") : uiText("подтверждена диагностикой")}</span></span>
      <button type="button" className="ghost danger small-button" onClick={() => onReopen(s)} title={uiText("Тема начнётся у студента заново: 3 + 2 + 1 задачи")}>{uiText("Снять освоение")}</button>
    </li>)}</ul>
  </details>
}

/** The teacher's view of a course's «Тренировочная аттестация»: how many attempts, how many in time, then the list. */
function PracticeSummary({ attempts }: { attempts: PracticeAttempt[] }) {
  const inTime = attempts.filter(a => a.result === 'IN_TIME').length
  return <div className="practice-summary">
    <span className="small"><b>{uiText("Тренировочная аттестация:")}</b> {uiText("попыток")} {attempts.length}{uiText(", в срок")} {inTime}</span>
    <PracticeAttempts items={attempts} />
  </div>
}

/** «урок идёт · Java, 12 мин» — the open lesson and how long it has been going. */
function ActiveLessonBadge({ lesson }: { lesson: ActiveLesson }) {
  const minutes = Math.max(0, Math.round((Date.now() - parseDate(lesson.startedAt).getTime()) / 60_000))
  const since = minutes < 60 ? tr(currentLocale(), `${minutes} мин`, `${minutes} min`, `${minutes} دقيقة`) : minutes < 24 * 60 ? tr(currentLocale(), `${Math.floor(minutes / 60)} ч ${minutes % 60} мин`, `${Math.floor(minutes / 60)} h ${minutes % 60} min`, `${Math.floor(minutes / 60)} ساعة ${minutes % 60} دقيقة`) : tr(currentLocale(), `${Math.floor(minutes / (24 * 60))} дн`, `${Math.floor(minutes / (24 * 60))} j`, `${Math.floor(minutes / (24 * 60))} يوم`)
  return <span className="active-lesson" title={tr(currentLocale(), `Урок ${lesson.number} начат ${fmt(lesson.startedAt)}`, `Cours ${lesson.number} commencé ${fmt(lesson.startedAt)}`, `الدرس ${lesson.number} بدأ ${fmt(lesson.startedAt)}`)}><span className="live-dot" aria-hidden="true" />{uiText("урок идёт ·")} {COURSES[lesson.language].title}, {since}</span>
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
    if (!to && !window.confirm(tr(currentLocale(), `Убрать группу «${group}» у всех её студентов? Сами студенты останутся.`, `Retirer le groupe « ${group} » de tous ses étudiants ? Les étudiants resteront.`, `تشيل المجموعة «${group}» من كل طلابها؟ الطلاب نفسهم حيفضلوا.`))) return
    const merging = to && groups.some(g => g !== group && g.toLocaleLowerCase('ru') === to.toLocaleLowerCase('ru'))
    if (merging && !window.confirm(tr(currentLocale(), `Группа «${to}» уже есть. Объединить с ней «${group}»?`, `Le groupe « ${to} » existe déjà. Y fusionner « ${group} » ?`, `المجموعة «${to}» موجودة بالفعل. تدمج معاها «${group}»؟`))) return
    setSaving(true)
    const result = await request(() => post<{ group: string | null; students: number }>('/admin/groups/rename', { from: group, to }))
    setSaving(false)
    if (!result) return
    toast({ tone: 'info', icon: 'user', title: result.group ? tr(currentLocale(), `Группа теперь «${result.group}»`, `Le groupe est maintenant « ${result.group} »`, `المجموعة بقت «${result.group}»`) : tr(currentLocale(), `Группа «${group}» убрана`, `Groupe « ${group} » retiré`, `المجموعة «${group}» اتشالت`), text: tr(currentLocale(), `Студентов: ${result.students}`, `Étudiants : ${result.students}`, `الطلاب: ${result.students}`) })
    onRenamed(result.group)
  }
  if (!open) return <button type="button" className="ghost small-button" onClick={() => setOpen(true)}>{uiText("Переименовать группу")}</button>
  return <form className="rename-group enter" onSubmit={save} autoComplete="off">
    <input aria-label={tr(currentLocale(), `Новое название группы «${group}»`, `Nouveau nom du groupe « ${group} »`, `اسم جديد للمجموعة «${group}»`)} value={name} onChange={e => setName(e.target.value)} maxLength={60} autoFocus list="known-groups" />
    <button className="primary" disabled={saving || name.trim() === group}>{saving ? <><Spinner /> {uiText("Сохраняем…")}</> : uiText("Сохранить")}</button>
    <button type="button" className="ghost" onClick={() => setOpen(false)}>{uiText("Отмена")}</button>
    <small className="muted">{uiText("Пустое название убирает группу. Название существующей группы объединяет их.")}</small>
  </form>
}

/** sessionParticipant is on unless the server says otherwise (new accounts take part by default). */
const participates = (student: Student) => student.sessionParticipant !== false

/** Name, login, group and session participation of a student. A new login works from the next sign-in; open sessions stay. */
function EditStudent({ student, groups, request, onUpdated }: { student: Student; groups: string[]; request: Request; onUpdated: (student: Student) => void }) {
  const [open, setOpen] = useState(false); const [saving, setSaving] = useState(false)
  const initial = () => ({ displayName: student.displayName, login: student.login, group: student.group ?? '', sessionParticipant: participates(student) })
  const [draft, setDraft] = useState(initial)
  const toast = useToast()
  const reset = () => setDraft(initial())
  const changed = draft.displayName.trim() !== student.displayName || draft.login.trim() !== student.login || draft.group.trim() !== (student.group ?? '') || draft.sessionParticipant !== participates(student)
  async function save(e: FormEvent) {
    e.preventDefault(); setSaving(true)
    const updated = await request(() => patch<Student>(`/admin/students/${student.id}`, { displayName: draft.displayName.trim(), login: draft.login.trim(), group: draft.group.trim() || null, sessionParticipant: draft.sessionParticipant }))
    setSaving(false)
    if (!updated) return
    // The answer may omit the flag: keep what was sent rather than the old value.
    const saved = { ...updated, sessionParticipant: updated.sessionParticipant ?? draft.sessionParticipant }
    onUpdated(saved); setOpen(false)
    const participation = participates(saved) !== participates(student) ? (participates(saved) ? tr(currentLocale(), "участвует в сессии", "participe à la session", "مشارك في الامتحان") : tr(currentLocale(), "не участвует в сессии", "ne participe pas à la session", "غير مشارك في الامتحان")) : null
    toast({ tone: 'info', icon: 'user', title: uiText("Данные студента сохранены"), text: updated.login !== student.login ? tr(currentLocale(), `Новый логин «${updated.login}» — со следующего входа`, `Nouvel identifiant « ${updated.login} » dès la prochaine connexion`, `اسم الدخول الجديد «${updated.login}» من الدخول الجاي`) : [updated.displayName, updated.group, participation].filter(Boolean).join(' · ') })
  }
  if (!open) return <button className="ghost small-button" onClick={() => { reset(); setOpen(true) }}><Icon name="user" size={15} /> {uiText("Изменить данные")}</button>
  return <form className="password-reset edit-student enter" onSubmit={save} autoComplete="off">
    <label className="small">{uiText("Имя")}<input value={draft.displayName} onChange={e => setDraft(d => ({ ...d, displayName: e.target.value }))} required maxLength={100} /></label>
    <label className="small">{uiText("Логин")}<input value={draft.login} onChange={e => setDraft(d => ({ ...d, login: e.target.value }))} required maxLength={64} autoCapitalize="none" spellCheck={false} /></label>
    <label className="small"><span>{uiText("Группа")} <span className="muted">{uiText("— необязательно")}</span></span><input value={draft.group} onChange={e => setDraft(d => ({ ...d, group: e.target.value }))} maxLength={60} list="student-groups" placeholder={uiText("Без группы")} /></label>
    <GroupOptions id="student-groups" groups={groups} />
    <div className="participant-row">
      <span><b className="small">{uiText("Участвует в сессии")}</b><small className="muted">{uiText("Выключи для себя, добровольцев и тестовых аккаунтов")}</small></span>
      <Switch checked={draft.sessionParticipant} onChange={() => setDraft(d => ({ ...d, sessionParticipant: !d.sessionParticipant }))} label={uiText("Участвует в сессии")} />
    </div>
    {draft.login.trim() !== student.login && <p className="muted small">{uiText("Студент войдёт с новым логином в следующий раз; открытые сессии сохранятся, пароль не меняется.")}</p>}
    <div className="password-row"><button className="primary" disabled={saving || !changed || !draft.displayName.trim() || !draft.login.trim()}>{saving ? <><Spinner /> {uiText("Сохраняем…")}</> : uiText("Сохранить")}</button><button type="button" className="ghost" onClick={() => setOpen(false)}>{uiText("Отмена")}</button></div>
  </form>
}

function StudentDetail({ student, groups, request, toggle, onOpenProgress, onLlmStatus, onUpdated, onDeleted }: { student: Student; groups: string[]; request: Request; toggle: () => void; onOpenProgress?: () => void; onLlmStatus: (llm: LlmStatus) => void; onUpdated: (student: Student) => void; onDeleted: () => void }) {
  const [lessons, setLessons] = useState<Lesson[] | null>(null)
  const [progress, setProgress] = useState<Partial<Record<CourseLanguage, SkillProgress[]>> | null>(null)
  const [retakes, setRetakes] = useState<Partial<Record<CourseLanguage, number>>>({})
  const [practice, setPractice] = useState<PracticeByLanguage>({})
  const [hardCourses, setHardCourses] = useState<Student['hardModeCourses']>(student.hardModeCourses)
  const [openLesson, setOpenLesson] = useState<Id | null>(null)
  const [detail, setDetail] = useState<LessonDetail | null>(null)
  const openRef = useRef<Id | null>(null)
  useEffect(() => {
    let alive = true
    setLessons(null); setDetail(null); setOpenLesson(null); openRef.current = null
    request(() => api<{ lessons: Lesson[] }>(`/admin/students/${student.id}/lessons`)).then(value => { if (alive && value) setLessons(value.lessons) })
    request(() => api<{ llm: LlmStatus; student?: Student; progress: SkillProgress[]; progressByLanguage?: Partial<Record<CourseLanguage, SkillProgress[]>>; retakesByLanguage?: Partial<Record<CourseLanguage, number>>; practiceByLanguage?: PracticeByLanguage }>(`/admin/students/${student.id}`)).then(value => { if (alive && value) { onLlmStatus(value.llm); setProgress(value.progressByLanguage ?? { JAVA: value.progress }); setRetakes(value.retakesByLanguage ?? {}); setPractice(value.practiceByLanguage ?? {}); if (value.student?.hardModeCourses) setHardCourses(value.student.hardModeCourses) } })
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
    if (!window.confirm(tr(currentLocale(), `Завершить урок ${lesson.number} студента ${student.displayName}? Студент начнёт следующий урок сам.`, `Terminer le cours ${lesson.number} de ${student.displayName} ? L’étudiant commencera lui-même le cours suivant.`, `تنهي الدرس ${lesson.number} للطالب ${student.displayName}؟ الطالب حيبدأ الدرس الجاي بنفسه.`))) return
    const result = await request(() => post<{ lesson: Lesson }>(`/admin/students/${student.id}/lessons/${lesson.id}/finish`))
    if (!result) return
    toast({ tone: 'info', icon: 'flag', title: tr(currentLocale(), `Урок ${lesson.number} завершён`, `Cours ${lesson.number} terminé`, `الدرس ${lesson.number} انتهى`), text: student.displayName })
    await reloadLessons(); open(result.lesson, true)
  }
  async function toggleHard() {
    const allowed = !student.hardModeAllowed
    const result = await request(() => patch<{ hardModeAllowed: boolean }>(`/admin/students/${student.id}/hard-mode`, { allowed }))
    if (!result) return
    onUpdated({ ...student, hardModeAllowed: result.hardModeAllowed, hardModeOn: result.hardModeAllowed ? student.hardModeOn : 0 })
    toast({ tone: 'info', icon: 'flame', title: result.hardModeAllowed ? tr(currentLocale(), "Допуск к hard mode выдан", "Accès au mode difficile accordé", "تم السماح بالوضع الصعب") : tr(currentLocale(), "Hard mode отключён", "Mode difficile désactivé", "الوضع الصعب اتقفل"), text: result.hardModeAllowed ? tr(currentLocale(), `${student.displayName} может включить его сам`, `${student.displayName} peut l’activer lui-même`, `${student.displayName} ممكن يشغلو بنفسه`) : student.displayName })
  }
  async function revoke(lesson: Lesson, task: { id: Id; title: string }) {
    if (!window.confirm(tr(currentLocale(), `Отменить зачёт задачи «${task.title}»? Студенту придётся решить её заново, прогресс по теме будет пересчитан.`, `Annuler la validation de « ${task.title} » ? L’étudiant devra résoudre l’exercice à nouveau et sa progression sera recalculée.`, `تلغي إجازة التمرين «${task.title}»؟ الطالب حيحلو تاني والتقدم في الموضوع حيتحسب من جديد.`))) return
    const result = await request(() => post<{ redoInOpenLesson: boolean }>(`/admin/students/${student.id}/lessons/${lesson.id}/tasks/${task.id}/revoke`))
    if (!result) return
    toast({ tone: 'info', icon: 'refresh', title: uiText("Зачёт отменён"), text: result.redoInOpenLesson ? tr(currentLocale(), "Задача снова ждёт решения в текущем уроке", "L’exercice attend à nouveau une solution dans le cours actuel", "التمرين منتظر الحل تاني في الدرس الحالي") : tr(currentLocale(), "Задача будет первой в следующем уроке студента", "L’exercice sera le premier du prochain cours de l’étudiant", "التمرين حيكون أول تمرين في درس الطالب الجاي") })
    reloadProgress(); open(lesson, true)
  }
  async function reopen(skill: SkillProgress) {
    if (!window.confirm(tr(currentLocale(), `Снять освоение темы «${skill.title}» у студента ${student.displayName}? Тема начнётся заново: 3 + 2 + 1 задачи в ближайших уроках. Решённые задачи и баллы останутся, XP за тему вернётся при новом освоении. Отменить это кнопкой нельзя.`, `Retirer la maîtrise de « ${skill.title} » à ${student.displayName} ? La notion recommencera avec 3 + 2 + 1 exercices. Les solutions et les points restent ; les XP seront rendus après une nouvelle maîtrise. Cette action ne peut pas être annulée par un bouton.`, `تلغي إتقان «${skill.title}» للطالب ${student.displayName}؟ الموضوع حيبدأ من جديد بـ 3 + 2 + 1 تمارين. الحلول والدرجات بتبقى، وXP الموضوع برجع بعد الإتقان من جديد. ما في زر للتراجع عن الخطوة دي.`))) return
    const result = await request(() => post<{ skillCode: string }>(`/admin/students/${student.id}/topics/${encodeURIComponent(skill.skillCode)}/reopen`))
    if (!result) return
    toast({ tone: 'info', icon: 'refresh', title: uiText("Освоение снято"), text: tr(currentLocale(), `«${skill.title}» начнётся заново в ближайшем уроке`, `« ${skill.title} » recommencera au prochain cours`, `«${skill.title}» حيبدأ من جديد في الدرس الجاي`) })
    reloadProgress()
  }
  return <aside className="card student-detail enter-side">
    <div className="detail-head">
      <span className="avatar big" aria-hidden="true">{initials(student.displayName)}</span>
      <div><h2 className="title">{student.displayName}</h2><p className="muted small">{student.login}{student.group && <span className="group-tag">{student.group}</span>}</p>
        {onOpenProgress && <button type="button" className="ghost small-button detail-link" onClick={onOpenProgress}><Icon name="target" size={15} /> {uiText("Прогресс")}</button>}</div>
      <div className="detail-switches">
        <label className="switch-label"><span className="muted small">LLM</span><Switch checked={!!student.llmEnabled} onChange={toggle} label={tr(currentLocale(), `LLM для ${student.displayName}`, `LLM pour ${student.displayName}`, `المساعد لـ ${student.displayName}`)} /></label>
        <label className="switch-label hard" title={uiText("Допуск к hard mode: студент сам включает алгоритмические задачи")}><span className="muted small"><Icon name="flame" size={13} /> Hard</span><Switch checked={!!student.hardModeAllowed} onChange={toggleHard} label={tr(currentLocale(), `Допуск к hard mode для ${student.displayName}`, `Accès au mode difficile pour ${student.displayName}`, `السماح بالوضع الصعب لـ ${student.displayName}`)} /></label>
      </div>
    </div>
    {!!student.hardModeAllowed && hardCourses && LANGUAGES.some(language => hardCourses[language]) && <p className="hard-ready muted small">
      Hard mode: {LANGUAGES.filter(language => hardCourses[language]).map(language => {
        const course = hardCourses[language]!
        return `${COURSES[language].title} — ${course.ready ? uiText("открыт") : tr(currentLocale(), `осталось тем: ${course.remaining}`, `notions restantes : ${course.remaining}`, `الموضوعات المتبقية: ${course.remaining}`)}`
      }).join(', ')}</p>}
    {!!student.hardModeOn && <p className="hard-note"><Icon name="flame" size={14} /> {uiText("Студент сейчас в hard mode")}</p>}
    {!participates(student) && <p className="muted small participant-note">{uiText("Не участвует в сессии — не учитывается в статистике прогресса.")}</p>}
    <div className="detail-actions"><EditStudent key={`${student.login}|${student.displayName}|${student.group ?? ''}|${participates(student)}`} student={student} groups={groups} request={request} onUpdated={onUpdated} /><PasswordReset student={student} request={request} /></div>
    {progress && <div className="lang-stats">{LANGUAGES.filter(language => progress[language]).map(language => {
      const level = experience({ skills: progress[language]! })
      return <div key={language}>
        <span className="lang-badge"><span className={`lang-dot ${COURSES[language].key}`} aria-hidden="true" />{COURSES[language].title}</span>
        <span className="mini-stats-cell"><b>{level.level}</b><small>{uiText("уровень")}</small></span>
        <span className="mini-stats-cell"><b>{level.iterations}</b><small>{uiText("итераций")}</small></span>
        <span className="mini-stats-cell"><b>{level.mastered}</b><small>{uiText("тем освоено")}</small></span>
        {!!retakes[language] && <span className="mini-stats-cell" title={uiText("Повторений пройденных тем с хотя бы одной решённой задачей")}><b>{retakes[language]}</b><small>{uiText("повторений тем")}</small></span>}
        <DiagnosticSummary skills={progress[language]!} />
        <ClosedTopics skills={progress[language]!} onReopen={reopen} />
        {!!practice[language]?.length && <PracticeSummary attempts={practice[language]!} />}
      </div>
    })}</div>}
    {!lessons ? <p className="muted">{uiText("Загружаем данные…")}</p> : <>
      <h3 className="section-title">{uiText("Уроки")}</h3>
      {lessons.length ? <div className="lesson-list">{lessons.map(l => <button key={l.id} className={openLesson === l.id ? 'lesson-item selected' : 'lesson-item'} aria-pressed={openLesson === l.id} onClick={() => open(l)}>
        <b><span className={`lang-dot ${COURSES[l.language ?? 'JAVA'].key}`} title={COURSES[l.language ?? 'JAVA'].title} /> {COURSES[l.language ?? 'JAVA'].title} {uiText("· урок")} {l.number}</b><span className={l.finishedAt ? '' : 'live'}>{l.finishedAt ? finishedLabel(l) : tr(currentLocale(), `идёт · начат ${fmt(l.startedAt)}`, `en cours · commencé ${fmt(l.startedAt)}`, `جاري · بدأ ${fmt(l.startedAt)}`)}</span>
      </button>)}</div> : <p className="muted">{uiText("Уроков пока нет.")}</p>}
      {openLesson !== null && !detail && <p className="muted"><Spinner /> {uiText("Загружаем урок…")}</p>}
      {detail && <div className="enter">
        <div className="lesson-detail-head">
          <div><b>{COURSES[detail.lesson.language ?? 'JAVA'].title} {uiText("· урок")} {detail.lesson.number}</b>
            <span className={detail.lesson.finishedAt ? 'muted small' : 'live small'}>{detail.lesson.finishedAt ? finishedLabel(detail.lesson) : uiText("идёт сейчас")}</span></div>
          {!detail.lesson.finishedAt && <button className="ghost small-button" onClick={() => finishLesson(detail.lesson)}><Icon name="flag" size={15} /> {uiText("Завершить урок")}</button>}
        </div>
        <h3 className="section-title">{uiText("Задачи и попытки")}</h3>
        {detail.tasks.length ? detail.tasks.map(t => <article key={t.id} className="detail-task">
          <div className="detail-task-head"><b>{!!t.hard && <span className="hard-chip"><Icon name="flame" size={12} /> HARD</span>}{!!t.integrative && <span className="integ-chip" title={uiText("Задача 3-й итерации: тема вместе с 1–2 пройденными, как на аттестации")}><Icon name="target" size={11} /> {uiText("Комплексная задача")}</span>}{!!t.practice && <span className="retake-chip practice" title={uiText("Задача тренировочной аттестации: на итерации, освоение и оценки не влияет")}>{uiText("тренировочная аттестация")}</span>}{t.retakeSkill && !t.practice && <span className="retake-chip" title={uiText("Задача из повторения пройденной темы: на итерации и освоение не влияет")}>{uiText("повторение ·")} {t.retakeSkill}</span>}{t.title}{!!t.replaced && <span className="replaced-chip" title={t.practice ? uiText("Тренировка закончилась раньше, чем задача была решена") : t.retakeSkill ? uiText("Повторение закончилось раньше, чем задача была решена") : uiText("Студент переключил hard mode, начал повторение темы или тренировочную аттестацию — задача снята с урока")}>{t.practice ? uiText("снята в конце тренировки") : t.retakeSkill ? uiText("снята в конце повторения") : uiText("снята с урока")}</span>}</b>
            {t.submissions.some(a => a.passed && !a.revokedAt) && <button className="ghost danger small-button" onClick={() => revoke(detail.lesson, t)} title={uiText("Студенту придётся решить задачу заново")}><Icon name="refresh" size={14} /> {uiText("Отменить зачёт")}</button>}
          </div>
          <Markdown>{t.statement}</Markdown>
          {t.submissions.length ? t.submissions.map(a => <details key={a.id}><summary className={a.revokedAt ? 'revoked' : a.passed ? 'passed' : 'not-passed'}><Icon name={a.revokedAt ? 'refresh' : a.passed ? 'check' : 'x'} size={14} /> {a.revokedAt ? tr(currentLocale(), `зачёт отменён ${fmt(a.revokedAt)}`, `validation annulée ${fmt(a.revokedAt)}`, `الإجازة أُلغيت ${fmt(a.revokedAt)}`) : a.passed ? uiText("принято") : uiText("не принято")} · {fmt(a.createdAt)}</summary><pre>{a.sourceCode}</pre>{a.grader === 'LLM' && <p className="grader-label"><Icon name="sparkle" size={13} /> {uiText("Подход проверен LLM")}</p>}{a.review ? <ReviewVerdict review={a.review} /> : a.output && <pre>{a.output}</pre>}{a.console && <ConsolePanel run={a.console} origin="attempt" language={detail.lesson.language ?? 'JAVA'} />}</details>) : <p className="muted small">{uiText("Попыток не было.")}</p>}
        </article>) : <p className="muted">{uiText("Задач в этом уроке не было.")}</p>}
        <h3 className="section-title">{uiText("Чат")}</h3>
        {detail.chat.length ? <div className="messages static" ref={chatRef}>{detail.chat.map(m => <div key={m.id} className={`message ${m.role === 'STUDENT' ? 'student' : 'assistant'}`}><Markdown>{m.content}</Markdown><small>{m.role === 'STUDENT' ? uiText("Студент") : uiText("Помощник")} · {fmt(m.createdAt)}</small></div>)}</div> : <p className="muted">{uiText("Переписки не было.")}</p>}
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
    toast({ tone: 'info', icon: 'user', title: tr(currentLocale(), `Аккаунт ${student.displayName} удалён`, `Compte de ${student.displayName} supprimé`, `حساب ${student.displayName} اتحذف`), text: tr(currentLocale(), `Уроков: ${result.lessons}, отправок решений: ${result.submissions}`, `Cours : ${result.lessons}, solutions envoyées : ${result.submissions}`, `الدروس: ${result.lessons}، الحلول المرسلة: ${result.submissions}`) })
    onDeleted()
  }
  if (!open) return <div className="danger-zone"><button className="ghost danger small-button" onClick={() => setOpen(true)}><Icon name="x" size={15} /> {uiText("Удалить аккаунт")}</button></div>
  return <form className="danger-zone open enter" onSubmit={confirm} autoComplete="off">
    <b>{uiText("Удалить аккаунт")} {student.displayName}?</b>
    <p className="muted small">{tr(currentLocale(), "Будут удалены вход в систему, диагностика, все уроки, решения, переписка с помощником и прогресс по обоим курсам. Восстановить их нельзя. Статистика обращений к LLM останется в аналитике без привязки к студенту.", "Le compte, le diagnostic, les leçons, les solutions, les échanges avec l’assistant et la progression des deux cours seront supprimés définitivement. Les statistiques LLM resteront dans les analyses sans lien avec l’étudiant.", "سيتم حذف الحساب والتشخيص والدروس والحلول والمحادثات والتقدم في الكورسين نهائياً. ستبقى إحصاءات المساعد دون ربطها بالطالب.")}</p>
    <label className="small">{uiText("Чтобы подтвердить, введи логин")} <code>{student.login}</code>
      <input value={typed} onChange={e => setTyped(e.target.value)} autoCapitalize="none" spellCheck={false} aria-invalid={typed.length > 0 && !matches} autoFocus />
    </label>
    <div className="password-row">
      <button className="danger-solid" disabled={!matches || deleting}>{deleting ? <><Spinner /> {uiText("Удаляем…")}</> : uiText("Удалить навсегда")}</button>
      <button type="button" className="ghost" onClick={() => { setOpen(false); setTyped('') }}>{uiText("Отмена")}</button>
    </div>
  </form>
}
