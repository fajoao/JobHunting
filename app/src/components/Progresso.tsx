import { fmtDataHora, relativo, useNow, useSource, useTrilhas } from '../hooks'
import type { Execucao, Pedido, Progresso as Prog } from '../types'
import { ultimoPedido } from './Hero'

const ETAPAS = [
  ['na_fila', 'Na fila'],
  ['coletando', 'Lendo portais'],
  ['analisando', 'Analisando vagas'],
  ['gravando', 'Gravando'],
  ['concluida', 'Concluída'],
] as const

const SEM_NOTICIA_MIN = 60
const MOSTRAR_CONCLUIDA_H = 6

/** Where a run stands, also inferring "done" from the run log when an older routine didn't report it. */
function situacao(p: Prog, execucoes: Execucao[], now: number, nomes: Record<string, string> = {}) {
  const trilha = p.trilha || nomes[p.id] || p.id
  const terminouNoLog = execucoes.some((e) => e.trilha === trilha && p.iniciado_em && e.em > p.iniciado_em)
  let etapa = String(p.etapa)
  if (etapa !== 'concluida' && etapa !== 'erro' && terminouNoLog) etapa = 'concluida'
  const idadeMin = p.atualizado_em ? (now - new Date(p.atualizado_em).getTime()) / 60_000 : Infinity
  const parada = etapa !== 'concluida' && etapa !== 'erro' && idadeMin > SEM_NOTICIA_MIN
  const total = Number(p.total) || 0
  const proc = Math.min(Number(p.processadas) || 0, total)
  const pct =
    etapa === 'na_fila' ? 4
    : etapa === 'coletando' ? 15
    : etapa === 'analisando' ? 35 + (total ? (proc / total) * 55 : 0)
    : etapa === 'gravando' ? 94
    : etapa === 'concluida' ? 100
    : 0
  return { trilha, etapa, parada, pct: Math.round(pct), total, proc }
}

function Cartao({ p, execucoes, now, nomes }: { p: Prog; execucoes: Execucao[]; now: number; nomes: Record<string, string> }) {
  const s = situacao(p, execucoes, now, nomes)
  const idx = ETAPAS.findIndex(([k]) => k === s.etapa)
  const rodando = s.etapa !== 'concluida' && s.etapa !== 'erro' && !s.parada
  const estado = s.etapa === 'erro' ? 'erro' : s.parada ? 'parada' : s.etapa === 'concluida' ? 'ok' : 'run'
  return (
    <div className={`jh-prog-card is-${estado}`}>
      <div className="jh-prog-head">
        <div>
          <div className="jh-prog-t">{s.trilha}</div>
          <div className="jh-muted">
            {p.iniciado_em ? `Iniciada ${relativo(p.iniciado_em, now)}` : ''}
            {p.atualizado_em ? ` · atualizado ${relativo(p.atualizado_em, now)}` : ''}
          </div>
        </div>
        <span className={`jh-pill ${estado === 'ok' ? 'ok' : estado === 'run' ? 'accent' : estado === 'erro' ? 'bad' : 'warn'}`}>
          {estado === 'ok' ? 'Concluída' : estado === 'erro' ? 'Erro' : estado === 'parada' ? 'Sem notícias' : `${s.pct}%`}
        </span>
      </div>
      <div
        className={`jh-prog-bar ${rodando ? 'is-live' : ''}`}
        role="progressbar"
        aria-label={`Progresso da busca ${s.trilha}`}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={s.pct}
      >
        <i style={{ width: `${s.pct}%` }} />
      </div>
      <ol className="jh-steps">
        {ETAPAS.map(([k, lab], i) => (
          <li key={k} className={i < idx || s.etapa === 'concluida' ? 'done' : i === idx ? (rodando ? 'now' : 'here') : ''}>
            <span className="dot" aria-hidden="true" />
            {lab}
          </li>
        ))}
      </ol>
      <div className="jh-prog-detail">
        {s.parada
          ? `A rotina não dá notícias desde ${fmtDataHora(p.atualizado_em)}. Ela pode ter parado; a próxima execução agendada recomeça a busca.`
          : s.etapa === 'analisando' && s.total
            ? `${s.proc} de ${s.total} vagas revisadas, ${Number(p.novas) || 0} no perfil. ${p.detalhe ?? ''}`
            : p.detalhe}
      </div>
    </div>
  )
}

export function Progresso() {
  const now = useNow(15_000)
  const prog = useSource<Prog>('progresso')
  const exec = useSource<Execucao>('execucoes')
  const pedidos = useSource<Pedido>('pedidos')
  const pedido = ultimoPedido(pedidos.data)
  const nomes = Object.fromEntries(useTrilhas().map((t) => [t.id, t.nome]))

  const visiveis = prog.data.filter((p) => {
    const s = situacao(p, exec.data, now, nomes)
    if (s.etapa !== 'concluida' && s.etapa !== 'erro') return !s.parada || (p.atualizado_em && now - new Date(p.atualizado_em).getTime() < 24 * 3_600_000)
    return p.atualizado_em ? now - new Date(p.atualizado_em).getTime() < MOSTRAR_CONCLUIDA_H * 3_600_000 : false
  }).sort((a, b) => String(a.id).localeCompare(String(b.id)))

  const esperando = pedido?.status === 'pendente'
  if (!visiveis.length && !esperando) return null

  const proxima = new Date(now)
  proxima.setMinutes(proxima.getMinutes() < 30 ? 30 : 60, 0, 0)

  return (
    <section className="jh-card jh-prog" id="progresso" aria-live="polite">
      <h2>Progresso da busca</h2>
      <p className="jh-sub">Cada rotina conta aqui em que etapa está. A página atualiza sozinha.</p>
      {esperando && (
        <div className="jh-prog-card is-run">
          <div className="jh-prog-head">
            <div>
              <div className="jh-prog-t">Pedido na fila</div>
              <div className="jh-muted">Pedido {relativo(pedido!.pedido_em, now)}</div>
            </div>
            <span className="jh-pill accent">Aguardando</span>
          </div>
          <div className="jh-prog-bar is-live"><i style={{ width: '3%' }} /></div>
          <div className="jh-prog-detail">
            O verificador confere os pedidos a cada 30 minutos, das 7h às 22h. Próxima verificação por volta de{' '}
            {proxima.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}.
          </div>
        </div>
      )}
      <div className="jh-prog-grid" data-source="progresso">
        {visiveis.map((p) => <Cartao key={p.id} p={p} execucoes={exec.data} now={now} nomes={nomes} />)}
      </div>
    </section>
  )
}
