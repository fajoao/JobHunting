import { createContext, useContext, useEffect, useState, useSyncExternalStore } from 'react'
import type { Runtime, Source, Vaga } from './types'

export const RuntimeContext = createContext<Runtime | null>(null)

export function useRuntime(): Runtime {
  const rt = useContext(RuntimeContext)
  if (!rt) throw new Error('Runtime ausente')
  return rt
}

/** Re-renders whenever the dashboard reports new data, then reads the dataset. */
export function useSource<T>(id: string): Source<T> {
  const rt = useRuntime()
  useSyncExternalStore(rt.subscribe, rt.version)
  return rt.data<T>(id)
}

export function useVagas(trilha: string) {
  const src = useSource<Vaga>('vagas')
  const rows = src.data
    .map((r) => ({ ...r, match: Number(r.match) || 0 }))
    .filter((r) => r.status !== 'excluida' && (!trilha || r.trilha === trilha))
  return { status: src.status, rows }
}

export function contar(rows: Vaga[]) {
  const perfil = rows.filter((r) => r.match >= 65)
  return {
    total: rows.length,
    perfil: perfil.length,
    claude: perfil.filter((r) => r.status === 'aplicada_claude').length,
    pend: perfil.filter((r) => r.status === 'pendente').length,
    pendBloq: perfil.filter((r) => r.status === 'pendente' && r.match > 80).length,
    voce: perfil.filter((r) => r.status === 'aplicada_voce').length,
  }
}

/** Ticks every `ms` so relative times ("há 3 min") stay current. */
export function useNow(ms = 30_000) {
  const [now, setNow] = useState(() => Date.now())
  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), ms)
    return () => clearInterval(t)
  }, [ms])
  return now
}

export function usePersistentState<T extends string>(key: string, initial: T) {
  const [v, setV] = useState<T>(() => {
    try {
      return (localStorage.getItem(key) as T) || initial
    } catch {
      return initial
    }
  })
  const set = (nv: T) => {
    setV(nv)
    try {
      localStorage.setItem(key, nv)
    } catch {
      /* storage unavailable */
    }
  }
  return [v, set] as const
}

export const fmtDataHora = (s?: string) =>
  s ? new Date(s).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' }) : ''

export function relativo(s: string | undefined, now: number) {
  if (!s) return ''
  const min = Math.round((now - new Date(s).getTime()) / 60_000)
  if (min < 1) return 'agora'
  if (min < 60) return `há ${min} min`
  const h = Math.floor(min / 60)
  if (h < 24) return `há ${h} h`
  return fmtDataHora(s)
}
