export type Status =
  | 'pendente'
  | 'aplicada_claude'
  | 'aplicada_voce'
  | 'abaixo'
  | 'descartada'
  | 'excluida'

/** Trilhas come from the user's profile (setup interview), so any name is valid. */
export type Trilha = string

/** Public part of the profile shown on the dashboard: name and the trilhas chosen in the interview. */
export interface PerfilPainel {
  id?: string
  nome?: string
  trilhas?: { id: string; nome: string }[]
}

export interface Vaga {
  id: string
  titulo: string
  empresa: string
  local: string
  trilha: Trilha
  match: number
  status: Status
  url: string
  fonte?: string
  motivo?: string
  motivo_match?: string
  alertas?: string
  pontos_fortes?: string
  resumo?: string
  cv_url?: string
  encontrada_em?: string
  aplicada_em?: string
  marcada_em?: string
}

export interface Execucao {
  id: string
  em: string
  trilha: string
  coletadas: number
  novas: number
  aplicadas: number
  obs?: string
}

export interface Pedido {
  id: string
  status: 'pendente' | 'em_andamento' | 'disparada' | 'erro' | string
  pedido_em: string
  trilha: string
  disparada_em?: string
  rotinas?: string[]
  obs?: string
}

export type Etapa = 'na_fila' | 'coletando' | 'analisando' | 'gravando' | 'concluida' | 'erro'

export interface Progresso {
  id: string
  trilha: string
  etapa: Etapa | string
  detalhe?: string
  processadas?: number
  total?: number
  novas?: number
  iniciado_em?: string
  atualizado_em?: string
}

export interface Source<T> {
  status: 'ok' | 'loading' | 'connect' | 'declined' | 'error' | 'missing'
  data: T[]
  message?: string
}

/** The dashboard runtime the page is mounted in (or a mock during `npm run dev`). */
export interface Runtime {
  data<T>(id: string): Source<T>
  /** Writes a document under the dashboard's store. Throws when the viewer can't save. */
  setDoc(path: string, value: Record<string, unknown>): Promise<void>
  updateDoc(path: string, value: Record<string, unknown>): Promise<void>
  subscribe(fn: () => void): () => void
  version(): number
}
