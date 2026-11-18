import { forwardRef } from 'react'
import { tr, useLocale, type Locale } from './locale'
import { Icon } from './fx'
import type { ConsoleRun, CourseLanguage } from './types'

export type ConsoleOrigin = 'run' | 'attempt'

const problemTitle = (run: ConsoleRun, language: CourseLanguage, locale: Locale) => ({
  COMPILE_ERROR: language === 'PYTHON' ? tr(locale, 'Синтаксическая ошибка', 'Erreur de syntaxe', 'خطأ في الصياغة') : tr(locale, 'Ошибка компиляции', 'Erreur de compilation', 'خطأ في الترجمة'),
  RUNTIME_ERROR: tr(locale, 'Ошибка выполнения', 'Erreur d’exécution', 'خطأ أثناء التنفيذ'),
  LIMIT: tr(locale, 'Программа остановлена', 'Programme arrêté', 'البرنامج اتوقف'),
  UNAVAILABLE: tr(locale, 'Запуск недоступен', 'Exécution indisponible', 'التشغيل غير متاح'),
} as Record<string, string>)[run.status]

/** Printed text as a console shows it, with each line break marked, so a missing or extra «\n» is visible. */
function Output({ text }: { text: string }) {
  const { locale } = useLocale()
  const lines = text.split('\n')
  const endsWithBreak = text.endsWith('\n')
  if (endsWithBreak) lines.pop()
  return <>{lines.map((line, i) => {
    const trailing = line.match(/[ \t]+$/)?.[0] ?? ''
    const body = trailing ? line.slice(0, -trailing.length) : line
    const broken = i < lines.length - 1 || endsWithBreak
    return <span key={i} className="console-line">{body}{trailing && <span className="console-trail" title={tr(locale, "Пробелы в конце строки", "Espaces en fin de ligne", "مسافات في نهاية السطر")}>{trailing}</span>}{broken && <span className="console-eol" aria-hidden="true">↵</span>}{broken && '\n'}</span>
  })}</>
}

/** What the student's program printed when run as is, without hidden checks. */
export const ConsolePanel = forwardRef<HTMLElement, { run: ConsoleRun; origin: ConsoleOrigin; language: CourseLanguage }>(function ConsolePanel({ run, origin, language }, ref) {
  const { locale } = useLocale()
  const problem = problemTitle(run, language, locale)
  const printed = run.stdout ?? ''
  return <section ref={ref} className={`console ${problem ? 'has-problem' : ''}`} aria-label={tr(locale, "Консоль", "Console", "وحدة الإخراج")} aria-live="polite">
    <header className="console-head">
      <span className="console-title"><Icon name="terminal" size={15} /> {tr(locale, "Консоль", "Console", "وحدة الإخراج")}</span>
      <small>{origin === 'run' ? tr(locale, 'запуск без проверки — попытка не засчитывается', 'exécution sans vérification — ne compte pas comme tentative', 'تشغيل بدون فحص — ما بتحسب محاولة') : tr(locale, 'что напечатала программа при проверке', 'sortie du programme pendant la vérification', 'الناتج وقت الفحص')}</small>
      {problem && <span className="console-badge">{problem}</span>}
    </header>
    {run.status === 'NO_MAIN'
      ? <p className="console-note">{tr(locale, "В программе нет метода", "Le programme n’a pas de méthode", "البرنامج ما فيهو الدالة")} <code>main</code> {tr(locale, "— запускать нечего. Проверка сама вызовет твои методы с разными данными.", "— rien à exécuter. La vérification appellera tes méthodes avec différentes données.", "— ما في شي يتشغل. الفحص حينادي دوالك ببيانات مختلفة.")}</p>
      : run.status !== 'UNAVAILABLE' && <pre className="console-out">{printed ? <Output text={printed} /> : <span className="console-empty">{tr(locale, "Программа ничего не вывела", "Le programme n’a rien affiché", "البرنامج ما طبع أي حاجة")}</span>}</pre>}
    {run.error && <pre className="console-error">{run.error}</pre>}
    {(printed || run.truncated) && run.status !== 'NO_MAIN' && <footer className="console-foot">
      {run.truncated ? <span>{tr(locale, "Вывод слишком длинный — показано начало.", "La sortie est trop longue : seul le début est affiché.", "الناتج طويل شديد — ظاهر الجزء الأول.")}</span>
        : printed.endsWith('\n') ? <span><b>↵</b> {tr(locale, "вывод заканчивается переводом строки", "la sortie se termine par un saut de ligne", "الناتج بنتهي بسطر جديد")}</span> : <span>{tr(locale, "без перевода строки в конце", "sans saut de ligne à la fin", "بدون سطر جديد في النهاية")}</span>}
    </footer>}
  </section>
})

/** The same console as plain text, for the assistant's context. */
export function consoleText(run: ConsoleRun) {
  return `статус=${run.status}${run.truncated ? ' (вывод обрезан)' : ''}\nвывод:\n${run.stdout || '(пусто)'}${run.error ? `\nошибка:\n${run.error}` : ''}`
}
