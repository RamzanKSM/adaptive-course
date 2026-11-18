import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { clearUiText, loadUiText } from './uiText'

export type Locale = 'ru' | 'fr' | 'ar-SD'
const KEY = 'rmzn.ui-locale'
let activeLocale: Locale = (() => {
  try { const value = localStorage.getItem(KEY); return value === 'fr' || value === 'ar-SD' ? value : 'ru' } catch { return 'ru' }
})()
export function currentLocale(): Locale { return activeLocale }
const Context = createContext<{ locale: Locale; revision: number; setLocale: (value: Locale) => void }>({ locale: 'ru', revision: 0, setLocale: () => {} })
export function useLocale() { return useContext(Context) }
export function LocaleProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>(currentLocale)
  const [revision, setRevision] = useState(0)
  const setLocale = (value: Locale) => { clearUiText(); activeLocale = value; try { localStorage.setItem(KEY, value) } catch { /* private mode */ }; setLocaleState(value) }
  useEffect(() => {
    let cancelled = false
    document.documentElement.lang = locale; document.documentElement.dir = locale === 'ar-SD' ? 'rtl' : 'ltr'
    void loadUiText(locale, () => { if (!cancelled) setRevision(n => n + 1) })
    return () => { cancelled = true }
  }, [locale])
  return <Context.Provider value={{ locale, revision, setLocale }}><div key={locale}>{children}</div></Context.Provider>
}
export function tr(locale: Locale, ru: string, fr: string, ar: string): string { return locale === 'fr' ? fr : locale === 'ar-SD' ? ar : ru }
export function LocaleSwitch() {
  const { locale, setLocale } = useLocale()
  return <label className="ui-locale"><span className="sr-only">{tr(locale, 'Язык интерфейса', 'Langue de l’interface', 'لغة الواجهة')}</span><select value={locale} onChange={e => { const next = e.target.value as Locale; if (next === locale) return; if (window.confirm(tr(locale, "При смене языка страница обновится. Несохранённые данные форм будут потеряны. Продолжить?", "Changer de langue recharge la page. Les données non enregistrées des formulaires seront perdues. Continuer ?", "تغيير اللغة حيعيد تحميل الصفحة. البيانات غير المحفوظة في النماذج حتضيع. نواصل؟"))) setLocale(next); else e.currentTarget.value = locale }}><option value="ru">Русский</option><option value="fr">Français</option><option value="ar-SD">العربية السودانية</option></select></label>
}
