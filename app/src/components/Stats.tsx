import { useState, type ReactNode } from 'react'
import { contar, useVagas } from '../hooks'
import { Icon } from './ui'

/** A figure the dashboard can trace back to the `resumo` calc row for this trilha. */
function Mark({ field, trilha, children }: { field: string; trilha: string; children: ReactNode }) {
  return (
    <span data-source="resumo" data-field={field} data-where={'trilha=' + (trilha || 'Todas')}>
      {children}
    </span>
  )
}

export function Kpis({ trilha }: { trilha: string }) {
  const { status, rows } = useVagas(trilha)
  const c = contar(rows)
  const ok = status === 'ok'
  const cards: { id: string; label: string; field: string; v: number; note: string; icon: ReactNode; tone: string }[] = [
    { id: 'kpi-perfil', label: 'Dentro do perfil', field: 'no_perfil', v: c.perfil, note: 'Match de 65 ou mais', icon: Icon.target, tone: 'accent' },
    { id: 'kpi-aplicadas', label: 'Aplicadas por Claude', field: 'aplicadas_claude', v: c.claude, note: 'Envio automático, match acima de 80', icon: Icon.send, tone: 'ok' },
    {
      id: 'kpi-pendentes', label: 'Pendentes você aplicar', field: 'pendentes', v: c.pend, icon: Icon.clock, tone: 'warn',
      note: c.pendBloq ? `Inclui ${c.pendBloq} acima de 80 que o portal não deixou enviar` : 'Match entre 65 e 80',
    },
    { id: 'kpi-voce', label: 'Você já aplicou', field: 'aplicadas_voce', v: c.voce, note: 'Marcadas por você nesta página', icon: Icon.check, tone: 'ref' },
  ]
  return (
    <section className="jh-kpis" id="indicadores" aria-label="Indicadores">
      {cards.map((k, i) => (
        <div key={k.id} id={k.id} className={`jh-card jh-kpi tone-${k.tone} jh-enter`} style={{ ['--d' as string]: `${i * 60}ms` }}>
          <div className="jh-kpi-h">
            <span className="jh-ico">{k.icon}</span>
            <span className="jh-kpi-label">{k.label}</span>
          </div>
          <div className="jh-kpi-num">{ok ? <Mark field={k.field} trilha={trilha}>{k.v}</Mark> : '—'}</div>
          <div className="jh-kpi-note">{ok ? k.note : '—'}</div>
        </div>
      ))}
    </section>
  )
}

export function Funil({ trilha }: { trilha: string }) {
  const { status, rows } = useVagas(trilha)
  const c = contar(rows)
  const max = Math.max(1, c.total)
  const steps = [
    ['Analisadas', 'total', c.total, 'var(--jh-ref)'],
    ['No perfil', 'no_perfil', c.perfil, 'var(--jh-accent)'],
    ['Pendentes', 'pendentes', c.pend, 'var(--jh-warn)'],
    ['Aplicadas por Claude', 'aplicadas_claude', c.claude, 'var(--jh-ok)'],
    ['Aplicadas por você', 'aplicadas_voce', c.voce, 'var(--jh-ok)'],
  ] as const
  return (
    <section className="jh-card" id="funil">
      <h2>Funil da busca</h2>
      <p className="jh-sub">Da vaga lida nos portais até a candidatura enviada.</p>
      {status !== 'ok' ? (
        <div className="jh-skel" />
      ) : (
        <div className="jh-funnel">
          {steps.map(([lab, field, v, col]) => (
            <div className="jh-step" key={field}>
              <div className="jh-step-l">{lab}</div>
              <div className="jh-track">
                <i style={{ width: `${v ? Math.max(2, (v / max) * 100) : 0}%`, background: col }} />
              </div>
              <div className="jh-step-v"><Mark field={field} trilha={trilha}>{v}</Mark></div>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}

function Tip({ tip }: { tip: { x: number; y: number; text: string } | null }) {
  if (!tip) return null
  return <div className="jh-tip" style={{ left: tip.x, top: tip.y }}>{tip.text}</div>
}

export function Histograma({ trilha }: { trilha: string }) {
  const { status, rows } = useVagas(trilha)
  const [tip, setTip] = useState<{ x: number; y: number; text: string } | null>(null)
  const W = 560, H = 220, m = { t: 26, r: 8, b: 26, l: 28 }
  const bins = Array.from({ length: 20 }, (_, i) => {
    const x0 = i * 5
    return { x0, n: rows.filter((r) => r.match >= x0 && (r.match < x0 + 5 || (x0 === 95 && r.match <= 100))).length }
  })
  const maxN = Math.max(1, ...bins.map((b) => b.n))
  const niceMax = Math.ceil(maxN / 5) * 5 || 5
  const x = (v: number) => m.l + (v / 100) * (W - m.l - m.r)
  const y = (v: number) => H - m.b - (v / niceMax) * (H - m.t - m.b)
  const ticks = [0, niceMax / 2, niceMax].map(Math.round)
  return (
    <div className="jh-card" id="distribuicao">
      <h2>Distribuição do match</h2>
      <p className="jh-sub">Faixas de 5 pontos. Corte em 65 (você aplica) e em 80 (Claude aplica).</p>
      <div className="jh-chart" data-source="vagas" onMouseLeave={() => setTip(null)}>
        {status !== 'ok' ? (
          <div className="jh-skel tall" />
        ) : (
          <svg viewBox={`0 0 ${W} ${H}`} width="100%" role="img" aria-label="Histograma do match das vagas, com cortes em 65 e 80">
            {ticks.map((t) => (
              <g key={t}>
                <line x1={m.l} x2={W - m.r} y1={y(t)} y2={y(t)} className="grid" />
                <text x={m.l - 6} y={y(t) + 4} textAnchor="end">{t}</text>
              </g>
            ))}
            {[0, 25, 50, 75, 100].map((t) => (
              <text key={t} x={x(t)} y={H - 6} textAnchor="middle">{t}</text>
            ))}
            {bins.filter((b) => b.n).map((b, i) => (
              <rect
                key={b.x0}
                className={`bar ${b.x0 >= 80 ? 'hi' : b.x0 >= 65 ? 'mid' : 'lo'}`}
                style={{ ['--d' as string]: `${i * 25}ms` }}
                x={x(b.x0) + 2}
                width={Math.max(1, x(b.x0 + 5) - x(b.x0) - 4)}
                y={y(b.n)}
                height={y(0) - y(b.n)}
                rx={4}
                onMouseMove={(e) => {
                  const box = (e.currentTarget.ownerSVGElement!.parentElement as HTMLElement).getBoundingClientRect()
                  setTip({ x: Math.min(e.clientX - box.left + 10, box.width - 180), y: e.clientY - box.top - 36, text: `${b.n} vaga(s) com match ${b.x0}–${b.x0 + 4}` })
                }}
              />
            ))}
            {([[65, 'você aplica'], [80, 'Claude aplica']] as const).map(([v, lab], i) => (
              <g key={v}>
                <line x1={x(v)} x2={x(v)} y1={m.t - 6} y2={H - m.b} className="ref" />
                <text x={x(v) + (i ? 4 : -4)} y={m.t - 10} textAnchor={i ? 'start' : 'end'}>{lab}</text>
              </g>
            ))}
          </svg>
        )}
        <Tip tip={tip} />
      </div>
    </div>
  )
}

export function Empresas({ trilha }: { trilha: string }) {
  const { status, rows } = useVagas(trilha)
  const perfil = rows.filter((r) => r.match >= 65)
  const contagem = new Map<string, number>()
  perfil.forEach((r) => contagem.set(r.empresa, (contagem.get(r.empresa) ?? 0) + 1))
  const data = [...contagem.entries()].map(([empresa, n]) => ({ empresa, n })).sort((a, b) => b.n - a.n).slice(0, 10)
  const max = Math.max(1, ...data.map((d) => d.n))
  return (
    <div className="jh-card" id="empresas">
      <h2>Vagas no perfil por empresa</h2>
      <p className="jh-sub">Só vagas com match de 65 ou mais.</p>
      <div className="jh-chart" data-source="vagas">
        {status !== 'ok' ? (
          <div className="jh-skel tall" />
        ) : !data.length ? (
          <div className="jh-empty">Nenhuma vaga com match de 65 ou mais nesta trilha.</div>
        ) : (
          <ul className="jh-bars" role="img" aria-label="Vagas no perfil por empresa">
            {data.map((d, i) => (
              <li key={d.empresa} style={{ ['--d' as string]: `${i * 40}ms` }}>
                <span className="lab">{d.empresa}</span>
                <span className="bar"><i style={{ width: `${(d.n / max) * 100}%` }} /></span>
                <b>{d.n}</b>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
