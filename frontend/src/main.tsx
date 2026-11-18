import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '@fontsource-variable/unbounded'
import '@fontsource-variable/manrope'
import '@fontsource-variable/jetbrains-mono'
import './styles.css'
import './markdown.css'
import App from './App'
import { LocaleProvider } from './locale'

createRoot(document.getElementById('root')!).render(<StrictMode><LocaleProvider><App /></LocaleProvider></StrictMode>)
