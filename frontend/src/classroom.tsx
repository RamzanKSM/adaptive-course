import { useEffect, useRef, useState } from 'react'
import { api, ApiError } from './api'
import { Icon } from './fx'
import { dayNumber, decimal, longDay, plural, shortDay, topics } from './session'
import type { Classroom, CourseLanguage } from './types'

const COURSE_TITLES: Record<CourseLanguage, string> = { JAVA: 'Java', PYTHON: 'Python' }
const REFRESH_MS = 60_000

/** «3,2 попытки», «1 попытка», «5 попыток». */
function attempts(n: number) {
  const rounded = Math.round(n * 10) / 10
  return `${decimal(rounded)} ${Number.isInteger(rounded) ? plural(rounded, 'попытка', 'попытки', 'попыток') : 'попытки'}`
}
/** The big number and its word: «10» «недель», «4» «дня». */
function weeksLeft(weeks: number): [string, string] {
  if (weeks < 1) { const days = Math.max(1, Math.round(weeks * 7)); return [String(days), plural(days, 'день', 'дня', 'дней')] }
  const whole = Math.floor(weeks)
  return [String(whole), plural(whole, 'неделя', 'недели', 'недель')]
}

/**
 * The screen projected to a whole group: anonymous aggregates only — no names, no per-student lines, no counts of who is behind.
 * Covers the page, refreshes every minute, Esc or «Назад» returns to the teacher's view.
 */
export function ClassroomScreen({ language, group, onClose }: { language: CourseLanguage; group: string; onClose: () => void }) {
  const [data, setData] = useState<Classroom | null>(null)
  const [error, setError] = useState<{ notFound: boolean; message: string } | null>(null)
  const [fullscreen, setFullscreen] = useState(false)
  const root = useRef<HTMLDivElement>(null)
  const close = useRef(onClose)
  close.current = onClose

  useEffect(() => {
    let alive = true
    const load = () => api<Classroom>(`/admin/classroom?language=${language}&group=${encodeURIComponent(group)}`)
      .then(value => { if (alive) { setData(value); setError(null) } })
      .catch(e => { if (alive) setError({ notFound: e instanceof ApiError && e.status === 404, message: e instanceof Error ? e.message : 'Не удалось загрузить данные' }) })
    load()
    const timer = setInterval(load, REFRESH_MS)
    return () => { alive = false; clearInterval(timer) }
  }, [language, group])

  // The page underneath does not scroll; focus moves into the screen and goes back where it was on close.
  useEffect(() => {
    const html = document.documentElement, previousOverflow = html.style.overflow
    const previousFocus = document.activeElement as HTMLElement | null
    html.style.overflow = 'hidden'
    root.current?.focus()
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape' && !document.fullscreenElement) close.current() }
    const onFullscreen = () => setFullscreen(!!document.fullscreenElement)
    window.addEventListener('keydown', onKey)
    document.addEventListener('fullscreenchange', onFullscreen)
    return () => {
      html.style.overflow = previousOverflow
      window.removeEventListener('keydown', onKey)
      document.removeEventListener('fullscreenchange', onFullscreen)
      if (document.fullscreenElement) document.exitFullscreen().catch(() => {})
      previousFocus?.focus?.()
    }
  }, [])
  const toggleFullscreen = () => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {})
    else root.current?.requestFullscreen?.().catch(() => {})
  }

  const course = COURSE_TITLES[language]
  return <div className="classroom" ref={root} role="dialog" aria-modal="true" aria-label={`Показ группе ${group}`} tabIndex={-1}>
    <div className="classroom-inner">
      <header className="classroom-head">
        <div>
          <p className="eyebrow">{course} · общий прогресс группы</p>
          <h1 className="display">{group}</h1>
          {data && !data.tooSmall && <p className="classroom-sub">{data.members} {plural(data.members, 'участник', 'участника', 'участников')} · в курсе {topics(data.totalTopics)}</p>}
        </div>
        <div className="classroom-actions">
          {document.fullscreenEnabled && <button type="button" className="ghost" onClick={toggleFullscreen}>{fullscreen ? 'Обычный режим' : 'Во весь экран'}</button>}
          <button type="button" className="primary" onClick={onClose}><Icon name="back" size={18} /> Назад</button>
        </div>
      </header>

      {error && !data ? <div className="card classroom-calm">
        <span className="empty-icon"><Icon name="user" size={28} /></span>
        <h2 className="title">{error.notFound ? 'Пока нечего показать' : 'Не удалось загрузить данные'}</h2>
        <p className="muted">{error.notFound ? `В группе «${group}» нет участников курса ${course}.` : error.message}</p>
      </div>
        : !data ? <div className="sk sk-card tall" />
          : data.tooSmall ? <div className="card classroom-calm">
            <span className="empty-icon"><Icon name="user" size={28} /></span>
            <h2 className="title">Группа слишком маленькая для общего экрана</h2>
            <p className="muted">В группе меньше пяти участников. По общим цифрам такой группы легко узнать результаты отдельных студентов, поэтому здесь их не показываем.</p>
          </div>
            : <ClassroomBoard data={data} />}
    </div>
  </div>
}

function ClassroomBoard({ data }: { data: Classroom }) {
  const week = data.week
  const goal = week?.goal ?? null
  const reached = !!week && goal !== null && week.closedTopics >= goal
  return <div className="classroom-grid">
    <section className="card classroom-week">
      <h2 className="card-title">Эта неделя{week && <span className="muted"> · с {shortDay(dayNumber(week.from))}</span>}</h2>
      {week ? <>
        <p className="classroom-big tabular">{week.closedTopics}<small>{goal !== null ? ` из ${goal}` : ''}</small></p>
        <p className="classroom-caption">{plural(week.closedTopics, 'тему', 'темы', 'тем')} группа прошла вместе с понедельника</p>
        {goal !== null && <>
          <div className="classroom-meter" role="progressbar" aria-label="Цель недели" aria-valuemin={0} aria-valuemax={goal} aria-valuenow={week.closedTopics}>
            <i style={{ width: `${goal ? Math.min(100, (week.closedTopics / goal) * 100) : 100}%` }} />
          </div>
          <p className="classroom-caption">{reached ? 'Цель недели выполнена!' : `Цель недели — ${topics(goal)}: столько нужно группе, чтобы успеть к сессии. Осталось ${week ? goal - week.closedTopics : goal}.`}</p>
        </>}
        {goal === null && <p className="classroom-caption muted">Цели недели нет: дата сессии не задана.</p>}
      </> : <p className="muted">Нет данных.</p>}
    </section>

    <section className="card classroom-session">
      <h2 className="card-title">До сессии</h2>
      {data.session.date && data.session.weeksLeft !== null ? <>
        {data.session.weeksLeft > 0
          ? <p className="classroom-big tabular">{weeksLeft(data.session.weeksLeft)[0]}<small> {weeksLeft(data.session.weeksLeft)[1]}</small></p>
          : <p className="classroom-caption">Сессия уже началась.</p>}
        <p className="classroom-caption">{longDay(data.session.date)}</p>
      </> : <p className="classroom-caption muted">Дата сессии пока не задана.</p>}
    </section>

    {data.daily && data.daily.length > 0 && <section className="card classroom-daily">
      <h2 className="card-title">Пройденные темы по дням <span className="muted">· последние 4 недели</span></h2>
      <DailyClosures daily={data.daily} />
    </section>}

    {data.blocks && data.blocks.length > 0 && <section className="card classroom-blocks">
      <h2 className="card-title">Навыки по блокам</h2>
      <ul className="class-blocks">{data.blocks.map(b => {
        const percent = Math.round(b.avgShare * 100)
        return <li key={b.block} title={b.topics.join('\n')}>
          <span className="block-name">Блок {b.block}</span>
          <div className="classroom-meter" role="progressbar" aria-label={`Блок ${b.block}`} aria-valuemin={0} aria-valuemax={100} aria-valuenow={percent}><i style={{ width: `${percent}%` }} /></div>
          <b className="tabular">{percent}%</b>
          <small>{b.topics.slice(0, 3).join(' · ')}{b.topics.length > 3 ? ` и ещё ${b.topics.length - 3}` : ''}</small>
        </li>
      })}</ul>
    </section>}

    {data.hardTopics && data.hardTopics.length > 0 && <section className="card classroom-hard">
      <h2 className="card-title">Трудные темы</h2>
      <p className="classroom-caption muted">Здесь группе понадобилось больше всего попыток — хороший повод разобрать их вместе.</p>
      <ol className="hard-topics">{data.hardTopics.map(t => <li key={t.code}>
        <b>{t.title}</b>
        <span>{attempts(t.attemptsPerSolve)} на решённую задачу</span>
      </li>)}</ol>
    </section>}
  </div>
}

/** Topics closed per day over the last 4 weeks: bars with their values written above, Mondays labelled. */
function DailyClosures({ daily }: { daily: NonNullable<Classroom['daily']> }) {
  const max = Math.max(1, ...daily.map(d => d.closedTopics))
  return <ol className="class-bars" aria-label="Пройденные темы по дням">
    {daily.map(d => {
      const n = dayNumber(d.day)
      const monday = new Date(n * 86_400_000).getUTCDay() === 1
      return <li key={d.day} className={monday ? 'monday' : ''} aria-label={`${shortDay(n)}: ${d.closedTopics} ${plural(d.closedTopics, 'тема', 'темы', 'тем')}`} title={`${shortDay(n)}: ${d.closedTopics}`}>
        <span className="class-bar" aria-hidden="true">
          <i style={{ height: `${(d.closedTopics / max) * 100}%` }} />
          {d.closedTopics > 0 && <b className="tabular" style={{ bottom: `calc(${(d.closedTopics / max) * 100}% + 4px)` }}>{d.closedTopics}</b>}
        </span>
        <small aria-hidden="true">{monday ? shortDay(n) : ''}</small>
      </li>
    })}
  </ol>
}
