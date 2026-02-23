import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SessionsScreen } from './SessionsScreen'
import * as api from '@core/api/client'

vi.mock('@core/api/client')

describe('SessionsScreen', () => {
  beforeEach(() => {
    vi.mocked(api.listSessions).mockResolvedValue([])
  })

  it('rendert „Sitzung anlegen“-Button und lädt Sitzungen', async () => {
    render(<SessionsScreen />)
    await waitFor(() => {
      expect(api.listSessions).toHaveBeenCalled()
    })
    expect(screen.getByRole('button', { name: /sitzung anlegen/i })).toBeInTheDocument()
  })

  it('zeigt nach Anlegen einer Sitzung diese in der Liste', async () => {
    const user = userEvent.setup()
    const mockSession = {
      session_id: 'SESSION-test123',
      case_id: null,
      created_at: '2026-01-01T00:00:00',
      audio_path: '',
      summary_path: null,
      file_size: 0,
      duration: null,
      status: 'draft',
    }
    vi.mocked(api.createSession).mockResolvedValue(mockSession)
    vi.mocked(api.listSessions).mockResolvedValueOnce([]).mockResolvedValueOnce([mockSession])

    render(<SessionsScreen />)
    await waitFor(() => { expect(api.listSessions).toHaveBeenCalled() })
    await user.click(screen.getByRole('button', { name: /sitzung anlegen/i }))

    await waitFor(() => {
      expect(api.createSession).toHaveBeenCalled()
    })
    await waitFor(() => {
      expect(screen.getByText(/test123/)).toBeInTheDocument()
    })
  })
})
