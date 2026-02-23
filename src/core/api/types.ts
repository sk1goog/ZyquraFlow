/* DTOs matching backend response shapes */

export interface SummaryJson {
  title: string
  participants: string[]
  key_points: string[]
  action_items: string[]
  summary: string
}

export interface SessionDto {
  session_id: string
  case_id: string | null
  created_at: string
  audio_path: string
  summary_path: string | null
  file_size: number
  duration: number | null
  status: string
  transcript?: string
  summary?: SummaryJson
}

export interface SessionCreate {
  case_id?: string | null
}

export interface CaseDto {
  case_id: string
  alias: string
  created_at: string
  session_count?: number
}

export interface CaseCreate {
  alias: string
}

export interface LinkSessionRequest {
  session_id: string
  case_id: string
}

export interface UnlinkSessionRequest {
  session_id: string
}

export interface ProviderInfo {
  id: string
  name: string
  models: string[]
}

export interface SystemConfig {
  provider: string
  model: string
  debug: boolean
  whisper_model: string
}

export interface HealthResponse {
  status: string
  provider?: string
  ollama_available?: boolean
}
