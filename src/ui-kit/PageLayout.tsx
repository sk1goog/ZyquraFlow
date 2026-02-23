import type { NavItem } from './Sidebar'
import { Sidebar } from './Sidebar'
import { Topbar } from './Topbar'
import './PageLayout.css'

interface PageLayoutProps {
  navItems: NavItem[]
  activeNav: string
  title: string
  onNavSelect: (id: string) => void
  children: React.ReactNode
}

export function PageLayout({ navItems, activeNav, title, onNavSelect, children }: PageLayoutProps) {
  return (
    <div className="ui-page-layout">
      <Sidebar items={navItems} activeId={activeNav} onSelect={onNavSelect} />
      <div className="ui-page-main">
        <Topbar title={title} />
        <main className="ui-page-content">{children}</main>
      </div>
    </div>
  )
}
