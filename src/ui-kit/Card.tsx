import type { HTMLAttributes } from 'react'
import './Card.css'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  title?: string
}

export function Card({ title, children, className = '', ...props }: CardProps) {
  return (
    <div className={`ui-card ${className}`.trim()} {...props}>
      {title && <h3 className="ui-card-title">{title}</h3>}
      {children}
    </div>
  )
}
