import { config } from '../config'
import type {
  SessionDto,
  SessionCreate,
  CaseDto,
  CaseCreate,
  SummaryJson,
  SystemConfig,
  HealthResponse,
  ProviderInfo,
} from './types'

const baseUrl = () => config.backendUrl

async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${baseUrl()}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? `HTTP ${res.status}`)
  }
  return res.json()
}

/* Sessions */
export async function createSession(body?: SessionCreate): Promise<SessionDto> {
  return fetchApi<SessionDto>('/api/sessions', {
    method: 'POST',
    body: JSON.stringify(body ?? {}),
  })
}

export async function listSessions(caseId?: string): Promise<SessionDto[]> {
  const q = caseId ? `?case_id=${encodeURIComponent(caseId)}` : ''
  return fetchApi<SessionDto[]>(`/api/sessions${q}`)
}

export async function getSession(sessionId: string): Promise<SessionDto> {
  return fetchApi<SessionDto>(`/api/sessions/${sessionId}`)
}

export async function uploadAudio(sessionId: string, file: File): Promise<SessionDto> {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${baseUrl()}/api/sessions/${sessionId}/audio`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? `HTTP ${res.status}`)
  }
  return res.json()
}

export async function updateTranscript(sessionId: string, transcript: string): Promise<SessionDto> {
  return fetchApi<SessionDto>(`/api/sessions/${sessionId}/transcript`, {
    method: 'PUT',
    body: JSON.stringify({ transcript }),
  })
}

export async function transcribeSession(sessionId: string): Promise<SessionDto> {
  return fetchApi<SessionDto>(`/api/sessions/${sessionId}/transcribe`, {
    method: 'POST',
  })
}

export async function summarizeSession(sessionId: string): Promise<SessionDto> {
  return fetchApi<SessionDto>(`/api/sessions/${sessionId}/summarize`, {
    method: 'POST',
  })
}

/* Cases */
export async function listCases(): Promise<CaseDto[]> {
  return fetchApi<CaseDto[]>('/api/cases')
}

export async function createCase(body: CaseCreate): Promise<CaseDto> {
  return fetchApi<CaseDto>('/api/cases', {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

export async function getCase(caseId: string): Promise<CaseDto & { sessions: SessionDto[] }> {
  return fetchApi<CaseDto & { sessions: SessionDto[] }>(`/api/cases/${caseId}`)
}

export async function linkSession(sessionId: string, caseId: string): Promise<void> {
  return fetchApi<void>(`/api/cases/${caseId}/sessions/${sessionId}`, { method: 'POST' })
}

export async function unlinkSession(sessionId: string): Promise<void> {
  return fetchApi<void>(`/api/sessions/${sessionId}/unlink`, { method: 'POST' })
}

/* System */
export async function getHealth(): Promise<HealthResponse> {
  return fetchApi<HealthResponse>('/health')
}

export async function getConfig(): Promise<SystemConfig> {
  return fetchApi<SystemConfig>('/api/system/config')
}

export async function updateConfig(updates: Partial<SystemConfig>): Promise<SystemConfig> {
  return fetchApi<SystemConfig>('/api/system/config', {
    method: 'PATCH',
    body: JSON.stringify(updates),
  })
}

export async function listProviders(): Promise<ProviderInfo[]> {
  return fetchApi<ProviderInfo[]>('/api/system/providers')
}

export async function listWhisperModels(): Promise<{ models: string[] }> {
  return fetchApi<{ models: string[] }>('/api/system/whisper-models')
}

export type { SummaryJson, SessionDto, CaseDto }
