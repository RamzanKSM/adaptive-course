export class ApiError extends Error {
  constructor(message: string, public readonly status: number) { super(message) }
}

// Backend status codes (LLM/runner availability) that may reach the UI as reasons or error messages.
const REASONS: Record<string, string> = {
  DISABLED_GLOBALLY: 'Учебный помощник выключен преподавателем для всего курса.',
  DISABLED_BY_CONFIGURATION: 'Учебный помощник отключён в настройках сервера.',
  DISABLED_FOR_STUDENT: 'Учебный помощник выключен для вашей учётной записи.',
  DISABLED_IN_HARD_MODE: 'В hard mode помощник отключён — разбирайся сам.',
  STUDENT_RUNTIME_NOT_VALIDATED: 'Учебный помощник ещё не допущен к работе со студентами.',
  APP_SERVER_NOT_CONFIGURED: 'Учебный помощник не настроен на сервере.',
  APP_SERVER_UNAVAILABLE: 'Учебный помощник временно недоступен.',
  LESSON_FINISHED: 'Урок уже завершён. Начни новый урок.',
}
export const humanize = (reason?: string | null) => reason ? REASONS[reason] ?? reason : ''

let unauthorizedHandler: (() => void) | null = null
export const onUnauthorized = (handler: (() => void) | null) => { unauthorizedHandler = handler }

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...options,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) }
  })
  if (!response.ok) throw await failure(response)
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

async function failure(response: Response): Promise<ApiError> {
  const body = await response.json().catch(() => null) as { message?: string } | null
  if (response.status === 401) {
    unauthorizedHandler?.()
    return new ApiError('Сессия истекла. Войдите снова.', 401)
  }
  return new ApiError(humanize(body?.message) ||`Ошибка сервера (${response.status})`, response.status)
}

/** Fetches a file (same session cookie and error handling as api) and saves it through a temporary download link. */
export async function download(path: string, fallbackName: string): Promise<string> {
  const response = await fetch(`/api${path}`, { credentials: 'include' })
  if (!response.ok) throw await failure(response)
  const disposition = response.headers.get('Content-Disposition') ?? ''
  const name = /filename\*=UTF-8''([^;]+)/i.exec(disposition)?.[1] ?? /filename="?([^";]+)"?/i.exec(disposition)?.[1] ?? fallbackName
  const filename = decodeURIComponent(name)
  const url = URL.createObjectURL(await response.blob())
  const link = Object.assign(document.createElement('a'), { href: url, download: filename })
  document.body.appendChild(link); link.click(); link.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
  return filename
}

export const post = <T>(path: string, body?: unknown) => api<T>(path, { method: 'POST', body: body === undefined ? undefined : JSON.stringify(body) })
export const patch = <T>(path: string, body: unknown) => api<T>(path, { method: 'PATCH', body: JSON.stringify(body) })
export const remove = <T>(path: string, body?: unknown) => api<T>(path, { method: 'DELETE', body: body === undefined ? undefined : JSON.stringify(body) })
