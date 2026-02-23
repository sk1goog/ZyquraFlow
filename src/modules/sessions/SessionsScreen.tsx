import { useState, useEffect, useCallback } from 'react'
import { Button, Card, TextArea } from '@ui-kit'
import * as api from '@core/api/client'
import type { SessionDto, SummaryJson } from '@core/api/types'
import './SessionsScreen.css'

export function SessionsScreen() {
  const [sessions, setSessions] = useState<SessionDto[]>([])
  const [selected, setSelected] = useState<SessionDto | null>(null)
  const [transcript, setTranscript] = useState('')
  const [loading, setLoading] = useState(false)
  const [transcribing, setTranscribing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadSessions = useCallback(async () => {
    try {
      const list = await api.listSessions()
      setSessions(list)
      if (selected && !list.find((s) => s.session_id === selected.session_id)) {
        setSelected(null)
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e))
    }
  }, [selected?.session_id])

  useEffect(() => {
    loadSessions()
  }, [loadSessions])

  const handleCreateSession = async () => {
    setError(null)
    setLoading(true)
    try {
      const s = await api.createSession()
      setSessions((prev) => [s, ...prev])
      setSelected(s)
      setTranscript('')
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setLoading(false)
    }
  }

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file || !selected) return
    setError(null)
    setLoading(true)
    try {
      const s = await api.uploadAudio(selected.session_id, file)
      setSessions((prev) => prev.map((x) => (x.session_id === s.session_id ? s : x)))
      setSelected(s)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setLoading(false)
      e.target.value = ''
    }
  }

  const handleSaveTranscript = async () => {
    if (!selected) return
    setError(null)
    setLoading(true)
    try {
      const s = await api.updateTranscript(selected.session_id, transcript)
      setSelected(s)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setLoading(false)
    }
  }

  const handleTranscribe = async () => {
    if (!selected) return
    setError(null)
    setTranscribing(true)
    try {
      const s = await api.transcribeSession(selected.session_id)
      setSessions((prev) => prev.map((x) => (x.session_id === s.session_id ? s : x)))
      setSelected(s)
      setTranscript(s.transcript ?? '')
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setTranscribing(false)
    }
  }

  const handleSummarize = async () => {
    if (!selected) return
    setError(null)
    setLoading(true)
    try {
      const s = await api.summarizeSession(selected.session_id)
      setSelected(s)
      setSessions((prev) => prev.map((x) => (x.session_id === s.session_id ? s : x)))
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setLoading(false)
    }
  }

  const selectSession = (s: SessionDto) => {
    setSelected(s)
    setTranscript(s.transcript ?? '')
  }

  const summary = selected?.summary

  function statusLabel(status: string) {
    const map: Record<string, string> = {
      draft: 'Entwurf',
      uploaded: 'Hochgeladen',
      summarized: 'Zusammengefasst',
    }
    return map[status] ?? status
  }

  return (
    <div className="sessions-screen">
      <div className="sessions-side">
        <Card title="Sitzungen">
          <Button onClick={handleCreateSession} disabled={loading} fullWidth>
            Sitzung anlegen
          </Button>
          <ul className="sessions-list">
            {sessions.map((s) => (
              <li
                key={s.session_id}
                className={selected?.session_id === s.session_id ? 'active' : ''}
                onClick={() => selectSession(s)}
              >
                <span className="sessions-list-id">{s.session_id.slice(0, 8)}…</span>
                <span className="sessions-list-meta">{statusLabel(s.status)}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>
      <div className="sessions-main">
        {error && <div className="sessions-error">{error}</div>}
        {selected ? (
          <>
            <Card title="Sitzungsdetails">
              <p className="sessions-meta">ID: {selected.session_id}</p>
              <p className="sessions-meta">Status: {statusLabel(selected.status)}</p>
              <p className="sessions-meta">Audio: {selected.audio_path || '—'}</p>
            </Card>
            <Card title="Audio hochladen">
              <input
                type="file"
                accept="audio/*"
                onChange={handleUpload}
                disabled={loading}
              />
            </Card>
            {selected.audio_path && (
              <Card title="Transkription">
                <Button
                  onClick={handleTranscribe}
                  disabled={loading || transcribing}
                >
                  {transcribing ? 'Transkription läuft …' : 'Transkription erstellen'}
                </Button>
              </Card>
            )}
            <Card title="Transkript">
              <TextArea
                value={transcript}
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setTranscript(e.target.value)}
                placeholder="Transkript hier einfügen oder eintippen …"
                rows={8}
              />
              <Button onClick={handleSaveTranscript} disabled={loading} variant="secondary">
                Transkript speichern
              </Button>
            </Card>
            <Card title="Zusammenfassen">
              <Button onClick={handleSummarize} disabled={loading || !transcript.trim()}>
                Zusammenfassen
              </Button>
            </Card>
            {summary && (
              <Card title="Zusammenfassung">
                <SummaryView summary={summary} />
              </Card>
            )}
          </>
        ) : (
          <Card>
            <p className="sessions-empty">Sitzung auswählen oder anlegen.</p>
          </Card>
        )}
      </div>
    </div>
  )
}

function SummaryView({ summary }: { summary: SummaryJson }) {
  return (
    <div className="summary-view">
      <h4>{summary.title}</h4>
      <p className="summary-text">{summary.summary}</p>
      {summary.participants?.length > 0 && (
        <section>
          <strong>Teilnehmer:</strong> {summary.participants.join(', ')}
        </section>
      )}
      {summary.key_points?.length > 0 && (
        <section>
          <strong>Kernpunkte</strong>
          <ul>
            {summary.key_points.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </section>
      )}
      {summary.action_items?.length > 0 && (
        <section>
          <strong>Maßnahmen</strong>
          <ul>
            {summary.action_items.map((a, i) => (
              <li key={i}>{a}</li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
