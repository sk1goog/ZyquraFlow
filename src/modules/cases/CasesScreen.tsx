import { useState, useEffect } from 'react'
import { Button, Card } from '@ui-kit'
import * as api from '@core/api/client'
import type { CaseDto, SessionDto } from '@core/api/types'
import './CasesScreen.css'

export function CasesScreen() {
  const [cases, setCases] = useState<CaseDto[]>([])
  const [selected, setSelected] = useState<CaseDto | null>(null)
  const [sessions, setSessions] = useState<SessionDto[]>([])
  const [allSessions, setAllSessions] = useState<SessionDto[]>([])
  const [alias, setAlias] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadCases = async () => {
    try {
      const list = await api.listCases()
      setCases(list)
    } catch (e) {
      setError(String(e))
    }
  }

  const loadSessions = async () => {
    try {
      const list = await api.listSessions()
      setAllSessions(list)
    } catch (e) {
      setError(String(e))
    }
  }

  useEffect(() => {
    loadCases()
    loadSessions()
  }, [])

  useEffect(() => {
    if (!selected) {
      setSessions([])
      return
    }
    api.getCase(selected.case_id).then((c) => setSessions(c.sessions ?? [])).catch(setError)
  }, [selected?.case_id])

  const handleCreateCase = async () => {
    if (!alias.trim()) return
    setError(null)
    setLoading(true)
    try {
      const c = await api.createCase({ alias: alias.trim() })
      setCases((prev) => [c, ...prev])
      setSelected(c)
      setAlias('')
    } catch (e) {
      setError(String(e))
    } finally {
      setLoading(false)
    }
  }

  const handleLinkSession = async (sessionId: string) => {
    if (!selected) return
    setError(null)
    setLoading(true)
    try {
      await api.linkSession(sessionId, selected.case_id)
      const c = await api.getCase(selected.case_id)
      setSessions(c.sessions ?? [])
      setAllSessions((prev) => prev.map((s) => (s.session_id === sessionId ? { ...s, case_id: selected.case_id } : s)))
    } catch (e) {
      setError(String(e))
    } finally {
      setLoading(false)
    }
  }

  const handleUnlinkSession = async (sessionId: string) => {
    setError(null)
    setLoading(true)
    try {
      await api.unlinkSession(sessionId)
      if (selected) {
        const c = await api.getCase(selected.case_id)
        setSessions(c.sessions ?? [])
      }
      setAllSessions((prev) => prev.map((s) => (s.session_id === sessionId ? { ...s, case_id: null } : s)))
    } catch (e) {
      setError(String(e))
    } finally {
      setLoading(false)
    }
  }

  const linkableSessions = selected
    ? allSessions.filter((s) => s.case_id !== selected.case_id)
    : []

  return (
    <div className="cases-screen">
      <div className="cases-side">
        <Card title="Fälle">
          <div className="cases-create">
            <input
              type="text"
              placeholder="Bezeichnung"
              value={alias}
              onChange={(e) => setAlias(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleCreateCase()}
            />
            <Button onClick={handleCreateCase} disabled={loading || !alias.trim()}>
              Anlegen
            </Button>
          </div>
          <ul className="cases-list">
            {cases.map((c) => (
              <li
                key={c.case_id}
                className={selected?.case_id === c.case_id ? 'active' : ''}
                onClick={() => setSelected(c)}
              >
                {c.alias}
                <span className="cases-list-id">{c.case_id}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>
      <div className="cases-main">
        {error && <div className="cases-error">{error}</div>}
        {selected ? (
          <Card title={`Fall: ${selected.alias}`}>
            <p className="cases-meta">ID: {selected.case_id}</p>
            <h4>Verknüpfte Sitzungen</h4>
            <ul className="cases-sessions">
              {sessions.map((s) => (
                <li key={s.session_id}>
                  <span>{s.session_id.slice(0, 8)}…</span>
                  <Button size="sm" variant="ghost" onClick={() => handleUnlinkSession(s.session_id)}>
                    Verknüpfung aufheben
                  </Button>
                </li>
              ))}
            </ul>
            <h4>Sitzung verknüpfen</h4>
            <ul className="cases-sessions">
              {linkableSessions.map((s) => (
                  <li key={s.session_id}>
                    <span>{s.session_id.slice(0, 8)}…</span>
                    <Button size="sm" onClick={() => handleLinkSession(s.session_id)}>
                      Verknüpfen
                    </Button>
                  </li>
                ))}
            </ul>
            {linkableSessions.length === 0 && (
              <p className="cases-empty">Keine Sitzungen zum Verknüpfen. Zuerst Sitzungen anlegen.</p>
            )}
          </Card>
        ) : (
          <Card>
            <p className="cases-empty">Fall auswählen oder anlegen.</p>
          </Card>
        )}
      </div>
    </div>
  )
}
