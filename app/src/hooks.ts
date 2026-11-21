import { createContext, useContext, useEffect, useState, useSyncExternalStore } from 'react'
import type { PerfilPainel, Runtime, Source, Vaga } from './types'

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

/**
 * Trilhas for the filters: the ones saved in the profile (from the setup interview), plus any trilha
 * that already has jobs. Without a profile, falls back to the trilhas found in the jobs.
 */
export function useTrilhas(): { id: string; nome: string }[] {
  const perfil = useSource<PerfilPainel>('perfil')
  const vagas = useSource<Vaga>('vagas')
  const out = new Map<string, { id: string; nome: string }>()
  for (const p of perfil.data)
    for (const t of [...lerTrilhas(p.trilhas), ...lerTrilhas(p.trilhas_ordem)]) if (!out.has(t.nome)) out.set(t.nome, t)
  for (const r of vagas.data) if (r.trilha && !out.has(r.trilha)) out.set(r.trilha, { id: slug(r.trilha), nome: r.trilha })
  return [...out.values()]
}

/** Accepts the trilhas as a list of {id, nome}, a list of names, JSON text or names separated by "|". */
function lerTrilhas(v: unknown): { id: string; nome: string }[] {
  if (typeof v === 'string') {
    try {
      return lerTrilhas(JSON.parse(v))
    } catch {
      return lerTrilhas(v.split('|'))
    }
  }
  if (!Array.isArray(v)) return []
  return v
    .map((x) => (typeof x === 'string' ? { nome: x.trim() } : (x as { id?: string; nome?: string }) ?? {}))
    .filter((x): x is { id?: string; nome: string } => Boolean(x.nome))
    .map((x) => ({ id: x.id || slug(x.nome), nome: x.nome }))
}

export const slug = (s: string) =>
  s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

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
