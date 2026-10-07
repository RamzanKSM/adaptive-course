import { forwardRef } from 'react'
import { Icon } from './fx'
import type { ConsoleRun, CourseLanguage } from './types'

export type ConsoleOrigin = 'run' | 'attempt'

const problemTitle = (run: ConsoleRun, language: CourseLanguage) => ({
  COMPILE_ERROR: language === 'PYTHON' ? 'Синтаксическая ошибка' : 'Ошибка компиляции',
  RUNTIME_ERROR: 'Ошибка выполнения',
  LIMIT: 'Программа остановлена',
  UNAVAILABLE: 'Запуск недоступен',
} as Record<string, string>)[run.status]

/** Printed text as a console shows it, with each line break marked, so a missing or extra «\n» is visible. */
function Output({ text }: { text: string }) {
  const lines = text.split('\n')
  const endsWithBreak = text.endsWith('\n')
  if (endsWithBreak) lines.pop()
  return <>{lines.map((line, i) => {
    const trailing = line.match(/[ \t]+$/)?.[0] ?? ''
    const body = trailing ? line.slice(0, -trailing.length) : line
    const broken = i < lines.length - 1 || endsWithBreak
    return <span key={i} className="console-line">{body}{trailing && <span className="console-trail" title="Пробелы в конце строки">{trailing}</span>}{broken && <span className="console-eol" aria-hidden="true">↵</span>}{broken && '\n'}</span>
  })}</>
}

/** What the student's program printed when run as is, without hidden checks. */
export const ConsolePanel = forwardRef<HTMLElement, { run: ConsoleRun; origin: ConsoleOrigin; language: CourseLanguage }>(function ConsolePanel({ run, origin, language }, ref) {
  const problem = problemTitle(run, language)
  const printed = run.stdout ?? ''
  return <section ref={ref} className={`console ${problem ? 'has-problem' : ''}`} aria-label="Консоль" aria-live="polite">
    <header className="console-head">
      <span className="console-title"><Icon name="terminal" size={15} /> Консоль</span>
      <small>{origin === 'run' ? 'запуск без проверки — попытка не засчитывается' : 'что напечатала программа при проверке'}</small>
      {problem && <span className="console-badge">{problem}</span>}
    </header>
    {run.status === 'NO_MAIN'
      ? <p className="console-note">В программе нет метода <code>main</code> — запускать нечего. Проверка сама вызовет твои методы с разными данными.</p>
      : run.status !== 'UNAVAILABLE' && <pre className="console-out">{printed ? <Output text={printed} /> : <span className="console-empty">Программа ничего не вывела</span>}</pre>}
    {run.error && <pre className="console-error">{run.error}</pre>}
    {(printed || run.truncated) && run.status !== 'NO_MAIN' && <footer className="console-foot">
      {run.truncated ? <span>Вывод слишком длинный — показано начало.</span>
        : printed.endsWith('\n') ? <span><b>↵</b> вывод заканчивается переводом строки</span> : <span>без перевода строки в конце</span>}
    </footer>}
  </section>
})

/** The same console as plain text, for the assistant's context. */
export function consoleText(run: ConsoleRun) {
  return `статус=${run.status}${run.truncated ? ' (вывод обрезан)' : ''}\nвывод:\n${run.stdout || '(пусто)'}${run.error ? `\nошибка:\n${run.error}` : ''}`
}
