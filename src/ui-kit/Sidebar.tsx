import './Sidebar.css'

export interface NavItem {
  id: string
  label: string
  icon?: string
}

interface SidebarProps {
  items: NavItem[]
  activeId: string
  onSelect: (id: string) => void
}

export function Sidebar({ items, activeId, onSelect }: SidebarProps) {
  return (
    <aside className="ui-sidebar">
      <div className="ui-sidebar-brand">ZyquraFlow</div>
      <nav className="ui-sidebar-nav">
        {items.map((item) => (
          <button
            key={item.id}
            className={`ui-sidebar-item ${activeId === item.id ? 'ui-sidebar-item--active' : ''}`}
            onClick={() => onSelect(item.id)}
          >
            {item.icon && <span className="ui-sidebar-icon">{item.icon}</span>}
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  )
}
