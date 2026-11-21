import { useRef, useState, type ButtonHTMLAttributes, type AnchorHTMLAttributes, type PointerEvent, type ReactNode } from 'react'

type Variant = 'primary' | 'ghost' | 'danger' | 'soft'

interface Ripple {
  id: number
  x: number
  y: number
  size: number
}

/** Ripple from the press point; the CSS keeps it off for people who turned motion off. */
function useRipples() {
  const [ripples, setRipples] = useState<Ripple[]>([])
  const next = useRef(0)
  const add = (e: PointerEvent<HTMLElement>) => {
    const r = e.currentTarget.getBoundingClientRect()
    const size = Math.max(r.width, r.height) * 2
    const id = next.current++
    setRipples((rs) => [...rs, { id, x: e.clientX - r.left - size / 2, y: e.clientY - r.top - size / 2, size }])
    setTimeout(() => setRipples((rs) => rs.filter((x) => x.id !== id)), 650)
  }
  const layer = (
    <span className="jh-ripples" aria-hidden="true">
      {ripples.map((r) => (
        <i key={r.id} style={{ left: r.x, top: r.y, width: r.size, height: r.size }} />
      ))}
    </span>
  )
  return { add, layer }
}

interface BtnProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  icon?: ReactNode
  busy?: boolean
  size?: 'sm' | 'md' | 'lg'
}

export function Btn({ variant = 'soft', icon, busy, size = 'md', className = '', children, onPointerDown, ...rest }: BtnProps) {
  const { add, layer } = useRipples()
  return (
    <button
      type="button"
      {...rest}
      className={`jh-btn jh-btn-${variant} jh-btn-${size} ${busy ? 'is-busy' : ''} ${className}`}
      onPointerDown={(e) => {
        add(e)
        onPointerDown?.(e)
      }}
    >
      {layer}
      {busy ? <span className="jh-spin" aria-hidden="true" /> : icon}
      <span className="jh-btn-label">{children}</span>
    </button>
  )
}

interface LinkBtnProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  variant?: Variant
  icon?: ReactNode
  size?: 'sm' | 'md' | 'lg'
}

export function LinkBtn({ variant = 'primary', icon, size = 'md', className = '', children, ...rest }: LinkBtnProps) {
  const { add, layer } = useRipples()
  return (
    <a
      target="_blank"
      rel="noopener noreferrer"
      {...rest}
      className={`jh-btn jh-btn-${variant} jh-btn-${size} ${className}`}
      onPointerDown={add}
    >
      {layer}
      {icon}
      <span className="jh-btn-label">{children}</span>
    </a>
  )
}

/** Segmented control; the chosen option gets a raised pill that pops in. */
export function Segmented<T extends string>({
  options,
  value,
  onChange,
  label,
  small,
}: {
  options: { value: T; label: string }[]
  value: T
  onChange: (v: T) => void
  label: string
  small?: boolean
}) {
  return (
    <div className={`jh-seg ${small ? 'small' : ''}`} role="group" aria-label={label} style={{ ['--n' as string]: options.length }}>
      {options.map((o) => (
        <button key={o.value} type="button" aria-pressed={o.value === value} onClick={() => onChange(o.value)}>
          {o.label}
        </button>
      ))}
    </div>
  )
}

const svg = (d: ReactNode) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {d}
  </svg>
)

export const Icon = {
  search: svg(<><circle cx="11" cy="11" r="6.5" /><path d="M20 20l-4.2-4.2" /></>),
  refresh: svg(<><path d="M21 12a9 9 0 1 1-2.64-6.36" /><path d="M21 4v5h-5" /></>),
  target: svg(<><circle cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="4" /><circle cx="12" cy="12" r="0.5" /></>),
  send: svg(<><path d="M22 2L11 13" /><path d="M22 2l-7 20-4-9-9-4 20-7z" /></>),
  clock: svg(<><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>),
  check: svg(<path d="M20 6L9 17l-5-5" />),
  external: svg(<><path d="M14 4h6v6" /><path d="M20 4l-9 9" /><path d="M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5" /></>),
  trash: svg(<><path d="M4 7h16" /><path d="M10 11v6M14 11v6" /><path d="M6 7l1 13h10l1-13" /><path d="M9 7V4h6v3" /></>),
  file: svg(<><path d="M14 3H7a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V7z" /><path d="M14 3v4h4" /></>),
  sun: svg(<><circle cx="12" cy="12" r="4" /><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" /></>),
  moon: svg(<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />),
  monitor: svg(<><rect x="3" y="4" width="18" height="12" rx="2" /><path d="M8 20h8M12 16v4" /></>),
}
