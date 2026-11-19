import { useEffect, useRef, useState } from 'react'
import { api } from './api'
import { Markdown } from './editor'
import { currentLocale, tr } from './locale'
import type { CourseLanguage, Id } from './types'
import './boardTaskBank.css'

interface Entry { id: Id; title: string; statement: string; topic: string; mode: string; active: boolean }
interface Page { tasks: Entry[]; total: number }
interface Selection { id: Id; title: string }

export function BoardTaskBank({ language, selected, onSelect }: { language: CourseLanguage; selected: Selection | null; onSelect: (task: Selection | null) => void }) {
  const t = (ru: string, fr: string, ar: string) => tr(currentLocale(), ru, fr, ar)
  const [query, setQuery] = useState('')
  const [submitted, setSubmitted] = useState('')
  const [offset, setOffset] = useState(0)
  const [page, setPage] = useState<Page | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const request = useRef(0)

  async function search(term: string, start: number) {
    const number = ++request.current
    setBusy(true); setError('')
    try {
      const params = new URLSearchParams({ language, query: term, offset: String(start) })
      const result = await api<Page>(`/admin/board/bank?${params}`)
      if (number === request.current) { setPage(result); setOffset(start); setSubmitted(term) }
    } catch (e) { if (number === request.current) setError(String(e)) }
    finally { if (number === request.current) setBusy(false) }
  }

  useEffect(() => {
    setQuery(''); setPage(null); setSubmitted(''); setOffset(0)
    void search('', 0)
    return () => { request.current++ }
  }, [language])

  return <section className="board-bank" aria-label={t('Банк задач', 'Banque d’exercices', 'بنك التمارين')}>
    {selected && <div className="board-bank-selected">
      <div><span>{t('Выбранная задача', 'Exercice choisi', 'التمرين المختار')}</span><strong>#{selected.id} · {selected.title}</strong></div>
      <button type="button" className="board-bank-clear" onClick={() => onSelect(null)}>{t('Убрать', 'Retirer', 'إزالة')}</button>
    </div>}
    <label className="board-bank-search-label">{t('Поиск по банку задач', 'Rechercher dans la banque d’exercices', 'البحث في بنك التمارين')}
      <span className="board-bank-search">
        <input value={query} maxLength={200} placeholder={t('Название, условие, тема или ID', 'Titre, énoncé, thème ou ID', 'العنوان أو نص التمرين أو الموضوع أو المعرّف')} onChange={e => setQuery(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); void search(query, 0) } }} />
        <button type="button" className="secondary" disabled={busy} onClick={() => void search(query, 0)}>{t('Найти', 'Rechercher', 'بحث')}</button>
      </span>
    </label>
    {error && <p className="form-error board-bank-message" role="alert">{error}</p>}
    {busy && <p className="board-bank-message" role="status">{t('Загрузка…', 'Chargement…', 'جارٍ التحميل…')}</p>}
    {page && !busy && <>
      <p className="board-bank-count">{t('Найдено задач', 'Exercices trouvés', 'عدد التمارين')} · {page.total}</p>
      {page.tasks.length === 0 && <p className="board-bank-empty">{t('Ничего не найдено. Попробуйте изменить запрос.', 'Aucun résultat. Essayez une autre recherche.', 'لم يتم العثور على نتائج. جرّب بحثاً آخر.')}</p>}
      <div className="board-bank-results">{page.tasks.map(task => <details className="board-bank-task" key={task.id}>
        <summary><span className="board-bank-task-name"><span className="board-bank-id">#{task.id}</span><strong>{task.title}</strong></span>{selected?.id === task.id && <span className="board-bank-badge">{t('Выбрана', 'Choisi', 'مختار')}</span>}</summary>
        <div className="board-bank-preview">
          <p className="board-bank-meta">{[task.topic, task.mode, !task.active ? t('Архив', 'Archive', 'الأرشيف') : ''].filter(Boolean).join(' · ')}</p>
          <div className="board-bank-statement"><Markdown>{task.statement}</Markdown></div>
          <button type="button" className={selected?.id === task.id ? 'ghost' : 'secondary'} disabled={selected?.id === task.id} onClick={() => onSelect({ id: task.id, title: task.title })}>{selected?.id === task.id ? t('Задача выбрана', 'Exercice choisi', 'تم اختيار التمرين') : t('Выбрать задачу', 'Choisir cet exercice', 'اختيار التمرين')}</button>
        </div>
      </details>)}</div>
      {(offset > 0 || offset + page.tasks.length < page.total) && <div className="board-bank-pagination">
        <button type="button" className="ghost" disabled={offset === 0} onClick={() => void search(submitted, Math.max(0, offset - 20))}>{t('Назад', 'Précédent', 'السابق')}</button>
        <span>{offset + 1}–{offset + page.tasks.length} / {page.total}</span>
        <button type="button" className="ghost" disabled={offset + page.tasks.length >= page.total || page.tasks.length === 0} onClick={() => void search(submitted, offset + page.tasks.length)}>{t('Далее', 'Suivant', 'التالي')}</button>
      </div>}
    </>}
  </section>
}
