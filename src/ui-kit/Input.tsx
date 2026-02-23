import type { InputHTMLAttributes, TextareaHTMLAttributes } from 'react'
import './Input.css'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

export function Input({ label, error, className = '', id, ...props }: InputProps) {
  const inputId = id ?? `input-${Math.random().toString(36).slice(2)}`
  return (
    <div className="ui-input-wrap">
      {label && (
        <label htmlFor={inputId} className="ui-input-label">{label}</label>
      )}
      <input
        id={inputId}
        className={`ui-input ${error ? 'ui-input--error' : ''} ${className}`.trim()}
        {...props}
      />
      {error && <span className="ui-input-error">{error}</span>}
    </div>
  )
}

interface TextAreaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
}

export function TextArea({ label, error, className = '', id, ...props }: TextAreaProps) {
  const inputId = id ?? `textarea-${Math.random().toString(36).slice(2)}`
  return (
    <div className="ui-input-wrap">
      {label && (
        <label htmlFor={inputId} className="ui-input-label">{label}</label>
      )}
      <textarea
        id={inputId}
        className={`ui-input ui-textarea ${error ? 'ui-input--error' : ''} ${className}`.trim()}
        {...props}
      />
      {error && <span className="ui-input-error">{error}</span>}
    </div>
  )
}
