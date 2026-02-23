import { useState, useEffect } from 'react'
import { Button, Card } from '@ui-kit'
import * as api from '@core/api/client'
import type { SystemConfig, ProviderInfo, HealthResponse } from '@core/api/types'
import './SystemScreen.css'

export function SystemScreen() {
  const [config, setConfig] = useState<SystemConfig | null>(null)
  const [providers, setProviders] = useState<ProviderInfo[]>([])
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = async () => {
    try {
      const [c, p, h] = await Promise.all([
        api.getConfig(),
        api.listProviders(),
        api.getHealth(),
      ])
      setConfig(c)
      setProviders(p)
      setHealth(h)
      setError(null)
    } catch (e) {
      setError(String(e))
    }
  }

  useEffect(() => {
    load()
  }, [])

  const handleProviderChange = (provider: string) => {
    const p = providers.find((x) => x.id === provider)
    const model = p?.models?.[0] ?? ''
    updateConfig({ provider, model })
  }

  const handleModelChange = (model: string) => {
    updateConfig({ model })
  }

  const handleDebugToggle = () => {
    updateConfig({ debug: !config?.debug })
  }

  const updateConfig = async (updates: Partial<SystemConfig>) => {
    setLoading(true)
    setError(null)
    try {
      const c = await api.updateConfig(updates)
      setConfig(c)
    } catch (e) {
      setError(String(e))
    } finally {
      setLoading(false)
    }
  }

  if (!config) {
    return <Card><p>Laden …</p></Card>
  }

  const currentProvider = providers.find((p) => p.id === config.provider)

  return (
    <div className="system-screen">
      {error && <div className="system-error">{error}</div>}
      <Card title="Anbieter-Status">
        <div className="system-health">
          <span className={`system-status ${health?.status === 'ok' ? 'ok' : 'error'}`}>
            {health?.status === 'ok' ? 'OK' : (health?.status ?? 'unbekannt')}
          </span>
          {health?.ollama_available !== undefined && (
            <span>Ollama: {health.ollama_available ? 'verfügbar' : 'nicht verfügbar'}</span>
          )}
        </div>
        <Button size="sm" variant="secondary" onClick={load}>
          Aktualisieren
        </Button>
      </Card>
      <Card title="Anbieter & Modell">
        <div className="system-field">
          <label>Anbieter</label>
          <select
            value={config.provider}
            onChange={(e) => handleProviderChange(e.target.value)}
            disabled={loading}
          >
            {providers.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </div>
        <div className="system-field">
          <label>Modell</label>
          <select
            value={config.model}
            onChange={(e) => handleModelChange(e.target.value)}
            disabled={loading || !currentProvider?.models?.length}
          >
            {(currentProvider?.models ?? []).map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </div>
      </Card>
      <Card title="Debug">
        <label className="system-toggle">
          <input
            type="checkbox"
            checked={config.debug}
            onChange={handleDebugToggle}
            disabled={loading}
          />
          Debug aktivieren (protokolliert prompt_id, Modell, Parameter, Dauer)
        </label>
      </Card>
    </div>
  )
}
