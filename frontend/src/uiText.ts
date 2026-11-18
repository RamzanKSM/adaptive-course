import baseStrings from './ui-ru.json'
import extraStrings from './ui-ru-extra.json'
import toastStrings from './ui-ru-toast.json'
import errorStrings from './ui-ru-errors.json'
import achievementStrings from './ui-ru-achievements.json'
import mapStrings from './ui-ru-maps.json'
import frenchStrings from './ui-fr.json'
import arabicStrings from './ui-ar-SD.json'
const sourceStrings = [...new Set([...baseStrings, ...extraStrings, ...toastStrings, ...errorStrings, ...achievementStrings, ...mapStrings])]
import { currentLocale, type Locale } from './locale'

const catalog = new Set(sourceStrings)
let translations: Record<string, string> = {}
let generation = 0
let controller: AbortController | undefined
export function clearUiText(): void { controller?.abort(); generation++; translations = {} }
/** Only strings compiled into the UI catalog can be translated. */
export function uiText(source: string): string {
  if (!catalog.has(source)) return source
  const locale = currentLocale()
  if (locale === 'ru') return source
  const builtIn = locale === 'fr' ? frenchStrings : arabicStrings
  return builtIn[source as keyof typeof builtIn] ?? translations[source] ?? source
}

/** Load only missing static strings. Failed batches keep their original Russian text. */
export async function loadUiText(locale: Locale, onUpdate: () => void): Promise<void> {
  controller?.abort()
  controller = new AbortController()
  const signal = controller.signal
  const current = ++generation
  if (locale === 'ru') { translations = {}; onUpdate(); return }
  const key = `rmzn.ui-text.${locale}.v4`
  const builtIn = locale === 'fr' ? frenchStrings : arabicStrings
  let cache: Record<string, string> = Object.fromEntries(Object.entries(builtIn).filter(([k, v]) => catalog.has(k) && typeof v === 'string' && v.length > 0 && v !== k))
  try { const value: unknown = JSON.parse(localStorage.getItem(key) ?? '{}'); if (value && typeof value === 'object' && !Array.isArray(value)) cache = { ...Object.fromEntries(Object.entries(value).filter(([k, v]) => catalog.has(k) && typeof v === 'string' && v.length > 0 && v !== k)), ...cache } } catch { /* storage unavailable */ }
  translations = { ...cache }; onUpdate()
  const missing = sourceStrings.filter(s => !cache[s])
  const batches: string[][] = []
  for (let i = 0; i < missing.length;) {
    const texts: string[] = []; let size = 0
    while (i < missing.length && texts.length < 50 && size + missing[i].length <= 4000) { texts.push(missing[i]); size += missing[i].length; i++ }
    if (!texts.length) { i++; continue }
    batches.push(texts)
  }
  let next = 0
  async function worker() {
    while (next < batches.length && current === generation) {
      const texts = batches[next++]
      try {
        const response = await fetch('/api/i18n/batch', { method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json', 'Accept-Language': locale }, body: JSON.stringify({ locale, texts }), signal })
        if (!response.ok || current !== generation) continue
        const result: unknown = await response.json()
        const values = (result as { translations?: unknown })?.translations
        if (current === generation && Array.isArray(values) && values.length === texts.length) {
          values.forEach((value, index) => { if (typeof value === 'string' && value.trim() && value !== texts[index]) cache[texts[index]] = value })
          translations = { ...cache }; onUpdate()
          try { localStorage.setItem(key, JSON.stringify(cache)) } catch { /* private mode or full storage */ }
        }
      } catch { /* use Russian for unavailable translations */ }
    }
  }
  await Promise.all(Array.from({ length: Math.min(4, batches.length) }, () => worker()))
}
