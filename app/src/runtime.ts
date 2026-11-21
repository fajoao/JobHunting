import type { Runtime, Source } from './types'
import { mockData } from './mock'

interface DashApi {
  data(id: string): { status: Source<unknown>['status']; data: unknown; message?: string }
  onData(fn: () => void): void
}
interface DbDoc {
  set(v: Record<string, unknown>): Promise<unknown>
  update(v: Record<string, unknown>): Promise<unknown>
}
interface ClaudeApi {
  use(name: 'db'): Promise<{ doc(path: string): DbDoc }>
}

declare global {
  interface Window {
    dash?: DashApi
    claude?: ClaudeApi
  }
}

function createSignal() {
  let v = 0
  const subs = new Set<() => void>()
  return {
    bump() {
      v++
      subs.forEach((f) => f())
    },
    subscribe(fn: () => void) {
      subs.add(fn)
      return () => subs.delete(fn)
    },
    version: () => v,
  }
}

/** Reads the dashboard's datasets through `window.dash` and writes with the `db` capability. */
export function dashboardRuntime(dash: DashApi, claude: ClaudeApi) {
  const signal = createSignal()
  dash.onData(() => signal.bump())
  const runtime: Runtime = {
    data<T>(id: string): Source<T> {
      const g = dash.data(id)
      return { status: g.status, data: Array.isArray(g.data) ? (g.data as T[]) : [], message: g.message }
    },
    async setDoc(path, value) {
      const db = await claude.use('db')
      await db.doc(path).set(value)
    },
    async updateDoc(path, value) {
      const db = await claude.use('db')
      await db.doc(path).update(value)
    },
    subscribe: signal.subscribe,
    version: signal.version,
  }
  return { runtime, bump: signal.bump }
}

/** In-memory stand-in for `npm run dev`, seeded with sample rows. */
export function mockRuntime(): Runtime {
  const signal = createSignal()
  const store: Record<string, Record<string, Record<string, unknown>>> = structuredClone(mockData)
  const collectionOf = (path: string) => {
    const parts = path.split('/')
    return { col: parts.slice(0, -1).join('/'), id: parts[parts.length - 1] }
  }
  const datasetPath: Record<string, string> = {
    vagas: 'data/radar/vagas',
    execucoes: 'data/radar/execucoes',
    pedidos: 'data/radar/pedidos',
    progresso: 'data/radar/progresso',
  }
  return {
    data<T>(id: string): Source<T> {
      const col = store[datasetPath[id]] ?? {}
      return { status: 'ok', data: Object.entries(col).map(([k, v]) => ({ id: k, ...v }) as T) }
    },
    async setDoc(path, value) {
      const { col, id } = collectionOf(path)
      store[col] = { ...(store[col] ?? {}), [id]: value }
      signal.bump()
    },
    async updateDoc(path, value) {
      const { col, id } = collectionOf(path)
      store[col] = { ...(store[col] ?? {}), [id]: { ...(store[col]?.[id] ?? {}), ...value } }
      signal.bump()
    },
    subscribe: signal.subscribe,
    version: signal.version,
  }
}
