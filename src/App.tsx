import { useState } from 'react'
import { PageLayout, type NavItem } from '@ui-kit'
import { SessionsScreen } from '@modules/sessions/SessionsScreen'
import { CasesScreen } from '@modules/cases/CasesScreen'
import { ReportsScreen } from '@modules/reports/ReportsScreen'
import { SystemScreen } from '@modules/system/SystemScreen'

const NAV_ITEMS: NavItem[] = [
  { id: 'sessions', label: 'Sitzungen' },
  { id: 'cases', label: 'Fälle' },
  { id: 'reports', label: 'Berichte' },
  { id: 'system', label: 'System' },
]

const TITLES: Record<string, string> = {
  sessions: 'Sitzungen',
  cases: 'Fälle',
  reports: 'Berichte',
  system: 'System',
}

function App() {
  const [activeNav, setActiveNav] = useState('sessions')

  const renderScreen = () => {
    switch (activeNav) {
      case 'sessions':
        return <SessionsScreen />
      case 'cases':
        return <CasesScreen />
      case 'reports':
        return <ReportsScreen />
      case 'system':
        return <SystemScreen />
      default:
        return <SessionsScreen />
    }
  }

  return (
    <PageLayout
      navItems={NAV_ITEMS}
      activeNav={activeNav}
      title={TITLES[activeNav] ?? 'ZyquraFlow'}
      onNavSelect={setActiveNav}
    >
      {renderScreen()}
    </PageLayout>
  )
}

export default App
