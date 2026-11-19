import { useState } from 'react'
import { api, post } from './api'
import { Markdown } from './editor'
import { currentLocale, tr } from './locale'
import type { BoardMember, CourseLanguage, Id } from './types'

interface Entry { id: Id; title: string; statement: string; topic: string; mode: string; active: boolean }
interface Page { tasks: Entry[]; total: number }

export function BoardTaskBank({ language, members, onCalled }: { language: CourseLanguage; members: BoardMember[]; onCalled: (id: Id) => void }) {
  const t = (ru: string, fr: string, ar: string) => tr(currentLocale(), ru, fr, ar)
  const [query, setQuery] = useState('')
  const [submitted, setSubmitted] = useState('')
  const [offset, setOffset] = useState(0)
  const [page, setPage] = useState<Page | null>(null)
  const [student, setStudent] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  async function search(term: string, start: number) {
    setBusy(true); setError('')
    try {
      const params = new URLSearchParams({ language, query: term, offset: String(start) })
      const result = await api<Page>(`/admin/board/bank?${params}`)
      setPage(result); setOffset(start); setSubmitted(term)
    } catch (e) { setError(String(e)) } finally { setBusy(false) }
  }
  async function call(taskId: Id) {
    setBusy(true); setError('')
    try {
      const test = await post<{ id: Id }>('/admin/board/call', { userId: Number(student), language, taskId })
      onCalled(test.id)
    } catch (e) { setError(String(e)) } finally { setBusy(false) }
  }
  return <details className="card"><summary>{t('Поиск по банку задач', 'Rechercher dans la banque d’exercices', 'البحث في بنك التمارين')}</summary>
    <form onSubmit={e => { e.preventDefault(); void search(query, 0) }}>
      <label>{t('Название, условие, тема или ID', 'Titre, énoncé, thème ou ID', 'العنوان أو نص التمرين أو الموضوع أو المعرّف')}
        <input value={query} maxLength={200} onChange={e => setQuery(e.target.value)} /></label>
      <button disabled={busy}>{t('Найти', 'Rechercher', 'بحث')}</button>
    </form>
    {error && <p role="alert">{error}</p>}
    {page && <><p>{t('Найдено задач', 'Exercices trouvés', 'عدد التمارين')} · {page.total}</p>
      {page.tasks.length > 0 && <label>{t('Кого вызвать', 'Étudiant à convoquer', 'الطالب المطلوب')}
        <select value={student} onChange={e => setStudent(e.target.value)}>
          <option value="">{t('Выбери студента', 'Choisir un étudiant', 'اختار طالب')}</option>
          {members.map(m => <option key={m.userId} value={m.userId}>{m.displayName}</option>)}
        </select></label>}
      {page.tasks.map(task => <details key={task.id}><summary>#{task.id} · {task.title}</summary>
        <p>{task.topic} · {task.mode}{!task.active && ' · ' + t('Архив', 'Archive', 'الأرشيف')}</p>
        <Markdown>{task.statement}</Markdown>
        <button type="button" disabled={busy || !members.some(m => String(m.userId) === student)} onClick={() => call(task.id)}>
          {t('Вызвать с этой задачей', 'Convoquer avec cet exercice', 'استدعاء بهذا التمرين')}</button>
      </details>)}
      {offset > 0 && <button disabled={busy} onClick={() => search(submitted, offset - 20)}>{t('Назад', 'Précédent', 'السابق')}</button>}
      {offset + page.tasks.length < page.total && <button disabled={busy} onClick={() => search(submitted, offset + page.tasks.length)}>{t('Далее', 'Suivant', 'التالي')}</button>}
    </>}
  </details>
}
