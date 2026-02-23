import './Topbar.css'

interface TopbarProps {
  title: string
}

export function Topbar({ title }: TopbarProps) {
  return (
    <header className="ui-topbar">
      <h1 className="ui-topbar-title">{title}</h1>
    </header>
  )
}
