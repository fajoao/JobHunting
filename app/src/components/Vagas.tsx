import { useEffect, useRef, useState } from 'react'
import { fmtDataHora, useRuntime, useSource, useVagas } from '../hooks'
import type { Execucao, Status, Vaga } from '../types'
import { Btn, Icon, LinkBtn } from './ui'

const ROTULO: Record<string, [string, string]> = {
  aplicada_claude: ['Aplicada por Claude', 'ok'],
  pendente: ['Pendente você aplicar', 'warn'],
  aplicada_voce: ['Você aplicou', 'ok'],
  abaixo: ['Abaixo do corte', 'mut'],
  descartada: ['Descartada', 'mut'],
}

/** Só aceita links http(s) ou arquivos do próprio dashboard: bloqueia javascript:, data: e afins vindos das fontes de vagas. */
function linkSeguro(u?: string): string | undefined {
  if (!u) return undefined
  if (u.startsWith('/_blob/')) return u
  try {
    const p = new URL(u)
    return p.protocol === 'https:' || p.protocol === 'http:' ? p.href : undefined
  } catch {
    return undefined
  }
}

type Filtro = 'perfil' | 'pendente' | 'claude' | 'voce' | 'abaixo' | 'todas'

function filtrar(rows: Vaga[], f: Filtro) {
  return rows
    .filter((r) =>
      f === 'todas' ? true
      : f === 'abaixo' ? r.match < 65
      : f === 'pendente' ? r.match >= 65 && r.status === 'pendente'
      : f === 'claude' ? r.status === 'aplicada_claude'
      : f === 'voce' ? r.status === 'aplicada_voce'
      : r.match >= 65)
    .sort((a, b) => b.match - a.match)
}

function ExcluirBtn({ onConfirm }: { onConfirm: () => void }) {
  const [armado, setArmado] = useState(false)
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined)
  useEffect(() => () => clearTimeout(timer.current), [])
  return (
    <Btn
      variant="danger"
      size="sm"
      icon={Icon.trash}
      className={armado ? 'armed' : ''}
      onClick={() => {
        if (!armado) {
          setArmado(true)
          timer.current = setTimeout(() => setArmado(false), 4000)
          return
        }
        clearTimeout(timer.current)
        onConfirm()
      }}
    >
      {armado ? 'Confirmar exclusão' : 'Excluir vaga'}
    </Btn>
  )
}

function Card({ r, onStatus, saindo }: { r: Vaga; onStatus: (id: string, s: Status) => void; saindo: boolean }) {
  const [lab, cls] = ROTULO[r.status] ?? [r.status, 'mut']
  const tone = r.match > 80 ? 'ok' : r.match >= 65 ? 'accent' : 'ref'
  const alertas = String(r.alertas || '').split(';').map((s) => s.trim()).filter(Boolean)
  return (
    <article className={`jh-job ${saindo ? 'is-leaving' : ''}`}>
      <div className={`jh-ring tone-${tone}`} style={{ ['--p' as string]: r.match }} aria-label={'Match ' + r.match}>
        <b data-source="vagas" data-field="match" data-where={'id=' + encodeURIComponent(r.id)}>{r.match}</b>
      </div>
      <div className="jh-job-main">
        <a className="jh-job-t" href={linkSeguro(r.url)} target="_blank" rel="noopener noreferrer">{r.titulo}</a>
        <div className="jh-meta">
          <span>{r.empresa}</span>
          <span>{r.local}</span>
          <span>{r.trilha}</span>
        </div>
        <div className="jh-chips">
          <span className={`jh-pill ${cls}`}>{lab}</span>
          {r.fonte && <span className="jh-chip">{r.fonte}</span>}
          {alertas.map((a) => <span key={a} className="jh-chip">{a}</span>)}
        </div>
        {r.motivo && r.status !== 'abaixo' && <div className="jh-why">{r.motivo}</div>}
        {r.motivo_match && <div className="jh-why">{r.motivo_match}</div>}
      </div>
      <div className="jh-act">
        {linkSeguro(r.url) && <LinkBtn href={linkSeguro(r.url)} size="sm" icon={Icon.external}>Abrir vaga</LinkBtn>}
        {r.status === 'pendente' && (
          <Btn size="sm" icon={Icon.check} onClick={() => onStatus(r.id, 'aplicada_voce')}>Marcar como aplicada</Btn>
        )}
        {linkSeguro(r.cv_url) && (
          <LinkBtn href={linkSeguro(r.cv_url)} variant="ghost" size="sm" icon={Icon.file}>Currículo</LinkBtn>
        )}
        <ExcluirBtn onConfirm={() => onStatus(r.id, 'excluida')} />
      </div>
    </article>
  )
}

export function Vagas({ trilha }: { trilha: string }) {
  const rt = useRuntime()
  const { status, rows } = useVagas(trilha)
  // "Outras vagas" ignores the profile (only the job's area matters), so it opens with every job.
  const semPerfil = trilha === 'Outras vagas'
  const [filtro, setFiltro] = useState<Filtro>(semPerfil ? 'todas' : 'perfil')
  useEffect(() => setFiltro(semPerfil ? 'todas' : 'perfil'), [semPerfil])
  const [erro, setErro] = useState(false)
  const [saindo, setSaindo] = useState<Set<string>>(new Set())
  const lista = filtrar(rows, filtro)

  async function mudar(id: string, s: Status) {
    if (s === 'excluida') setSaindo((x) => new Set(x).add(id))
    try {
      await rt.updateDoc(`data/radar/vagas/${id}`, { status: s, marcada_em: new Date().toISOString() })
      setErro(false)
    } catch {
      setErro(true)
      setSaindo((x) => {
        const n = new Set(x)
        n.delete(id)
        return n
      })
    }
  }

  return (
    <section className="jh-card" id="lista">
      <div className="jh-listhead">
        <div>
          <h2>Vagas</h2>
          <p className="jh-sub" style={{ marginBottom: 0 }}>
            {semPerfil
              ? 'Todas as vagas das empresas com "todas as vagas" (por padrão, só de tecnologia), sem filtro do seu perfil.'
              : 'Ordenadas pelo match. Abra a vaga, use o currículo pronto e marque quando aplicar.'}
          </p>
        </div>
        <select className="dash-select" aria-label="Filtrar por situação" value={filtro} onChange={(e) => setFiltro(e.target.value as Filtro)}>
          <option value="perfil">Dentro do perfil (65+)</option>
          <option value="pendente">Pendentes você aplicar</option>
          <option value="claude">Aplicadas por Claude</option>
          <option value="voce">Você já aplicou</option>
          <option value="abaixo">Abaixo de 65</option>
          <option value="todas">Todas</option>
        </select>
      </div>
      {erro && <p className="jh-err">Não foi salvo. Só editores do dashboard podem marcar vagas.</p>}
      <div className="jh-list" data-source="vagas">
        {status !== 'ok' ? (
          status === 'error' ? <div className="jh-empty">Falha ao carregar as vagas.</div> : <><div className="jh-skel card" /><div className="jh-skel card" /></>
        ) : !lista.length ? (
          <div className="jh-empty">Nenhuma vaga nesta seleção.</div>
        ) : (
          lista.map((r) => <Card key={r.id} r={r} onStatus={mudar} saindo={saindo.has(r.id)} />)
        )}
      </div>
    </section>
  )
}

export function Execucoes() {
  const g = useSource<Execucao>('execucoes')
  const rows = g.data.slice().sort((a, b) => String(b.em).localeCompare(String(a.em))).slice(0, 20)
  return (
    <section className="jh-card" id="execucoes">
      <h2>Execuções das rotinas</h2>
      <p className="jh-sub">Rotinas agendadas de busca, uma por trilha, além das buscas pedidas no botão.</p>
      <div className="jh-tablewrap">
        <table className="jh-table" data-source="execucoes" data-row-key="id">
          <thead>
            <tr>
              <th data-field="em">Quando</th>
              <th data-field="trilha">Rotina</th>
              <th data-field="coletadas">Vagas lidas</th>
              <th data-field="novas">Novas no perfil</th>
              <th data-field="aplicadas">Aplicadas</th>
              <th data-field="obs">Observação</th>
            </tr>
          </thead>
          <tbody>
            {g.status === 'ok' && !rows.length && (
              <tr><td colSpan={6} className="jh-muted">Nenhuma execução registrada ainda.</td></tr>
            )}
            {rows.map((r) => (
              <tr key={r.id} data-key={encodeURIComponent(r.id)}>
                <td>{fmtDataHora(r.em)}</td>
                <td>{r.trilha}</td>
                <td className="num">{r.coletadas}</td>
                <td className="num">{r.novas}</td>
                <td className="num">{r.aplicadas}</td>
                <td className="jh-muted">{r.obs || ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export function ComoFunciona() {
  return (
    <details className="jh-notes" id="como-funciona">
      <summary>Como o match e a situação são definidos</summary>
      <ul>
        <li>O match (0 a 100) soma o encaixe do título com a trilha, a aderência da descrição ao seu histórico (IA, automação, cloud, setor financeiro, gestão de times, operações, dados), a localização e a senioridade.</li>
        <li>Vagas que exigem inglês acima do seu nível perdem pontos. Júnior, pleno e estágio ficam de fora. Vagas afirmativas (PcD, mulheres) entram só se você as marcou no perfil.</li>
        <li>Locais aceitos: os definidos no seu perfil (remoto no Brasil e as cidades que você escolheu).</li>
        <li>Acima de 80, Claude tenta enviar a candidatura. Quando o portal exige login, CAPTCHA, chave de API da empresa ou dados que faltam, a vaga fica pendente para você, com currículo pronto.</li>
        <li>Entre 65 e 80, a vaga entra como pendente para você aplicar. Vagas excluídas somem da página e não voltam nas próximas buscas.</li>
      </ul>
    </details>
  )
}
