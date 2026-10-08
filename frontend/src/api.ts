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
  if (!response.ok) {
    const body = await response.json().catch(() => null) as { message?: string } | null
    if (response.status === 401) {
      unauthorizedHandler?.()
      throw new ApiError('Сессия истекла. Войдите снова.', 401)
    }
    throw new ApiError(humanize(body?.message) ||`Ошибка сервера (${response.status})`, response.status)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export const post = <T>(path: string, body?: unknown) => api<T>(path, { method: 'POST', body: body === undefined ? undefined : JSON.stringify(body) })
export const patch = <T>(path: string, body: unknown) => api<T>(path, { method: 'PATCH', body: JSON.stringify(body) })
export const remove = <T>(path: string, body?: unknown) => api<T>(path, { method: 'DELETE', body: body === undefined ? undefined : JSON.stringify(body) })
