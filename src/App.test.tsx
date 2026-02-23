import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('rendert Navigation mit Sitzungen, Fälle, Berichte, System', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: 'Sitzungen' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Fälle' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Berichte' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'System' })).toBeInTheDocument()
  })

  it('zeigt standardmäßig den Seitentitel Sitzungen in der Topbar', () => {
    render(<App />)
    expect(screen.getByRole('heading', { name: 'Sitzungen', level: 1 })).toBeInTheDocument()
  })

  it('zeigt ZyquraFlow im Seitenbereich', () => {
    render(<App />)
    expect(screen.getByText('ZyquraFlow')).toBeInTheDocument()
  })
})
