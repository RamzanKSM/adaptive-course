import { useEffect, useState } from 'react'

/** Filter value: '' — everyone, NO_GROUP — students without a group, otherwise a group name. */
export const NO_GROUP = '\u0000no-group'
export type GroupFilterValue = string

const collator = new Intl.Collator('ru', { numeric: true, sensitivity: 'base' })

/** Group names with their sizes, in natural order (ИВТ-2 before ИВТ-10). */
export function groupCounts<T>(items: T[], groupOf: (item: T) => string | null | undefined) {
  const counts = new Map<string, number>()
  let ungrouped = 0
  for (const item of items) { const group = groupOf(item); if (group) counts.set(group, (counts.get(group) ?? 0) + 1); else ungrouped++ }
  return { groups: [...counts].sort(([a], [b]) => collator.compare(a, b)).map(([name, count]) => ({ name, count })), ungrouped }
}

export const inGroup = (filter: GroupFilterValue, group: string | null | undefined) =>
  filter === '' || (filter === NO_GROUP ? !group : group === filter)

/** The chosen filter, remembered in this browser; a group that no longer exists falls back to everyone. */
export function useGroupFilter(storageKey: string, known: string[] | null) {
  const [value, setValue] = useState<GroupFilterValue>(() => { try { return localStorage.getItem(storageKey) ?? '' } catch { return '' } })
  useEffect(() => { try { localStorage.setItem(storageKey, value) } catch { /* private mode: the filter lasts for this page only */ } }, [storageKey, value])
  const effective = known && value && value !== NO_GROUP && !known.includes(value) ? '' : value
  return [effective, setValue] as const
}

/** «Все · 12», «ИВТ-1 · 5», «Без группы · 3». Hidden while nobody has a group: there is nothing to filter yet. */
export function GroupFilter({ total, groups, ungrouped, value, onChange, label = 'Группа' }: {
  total: number; groups: { name: string; count: number }[]; ungrouped: number; value: GroupFilterValue; onChange: (value: GroupFilterValue) => void; label?: string
}) {
  if (!groups.length) return null
  const chip = (key: GroupFilterValue, title: string, count: number) =>
    <button key={key || 'all'} type="button" className={value === key ? 'active' : ''} aria-pressed={value === key} onClick={() => onChange(key)}>{title}<span>{count}</span></button>
  return <div className="topic-filters group-filters" role="group" aria-label={label}>
    {chip('', 'Все', total)}
    {groups.map(g => chip(g.name, g.name, g.count))}
    {ungrouped > 0 && chip(NO_GROUP, 'Без группы', ungrouped)}
  </div>
}

/** Suggestions for a group field, so an existing group is picked rather than retyped. */
export function GroupOptions({ id, groups }: { id: string; groups: string[] }) {
  return <datalist id={id}>{groups.map(g => <option key={g} value={g} />)}</datalist>
}
