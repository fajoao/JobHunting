import { useState } from 'react'
import { contar, fmtDataHora, relativo, useNow, useRuntime, useSource, useVagas } from '../hooks'
import type { Execucao, Pedido } from '../types'
import { Btn, Icon, Segmented } from './ui'

export type Tema = 'sistema' | 'claro' | 'escuro'

export function ultimoPedido(pedidos: Pedido[]): Pedido | null {
  const reais = pedidos.filter((p) => !String(p.id).startsWith('teste'))
  if (!reais.length) return null
  return reais.slice().sort((a, b) => String(b.pedido_em).localeCompare(String(a.pedido_em)))[0]
}

function BuscarAgora({ trilha }: { trilha: string }) {
  const rt = useRuntime()
  const now = useNow()
  const pedidos = useSource<Pedido>('pedidos')
  const [enviando, setEnviando] = useState(false)
  const [erro, setErro] = useState(false)
  const p = ultimoPedido(pedidos.data)
  const ativo = !!p && (p.status === 'pendente' || p.status === 'em_andamento')

  async function pedir() {
    setEnviando(true)
    setErro(false)
    try {
      const agora = new Date().toISOString()
      const id = 'p-' + agora.replace(/[^0-9]/g, '').slice(0, 14)
      await rt.setDoc(`data/radar/pedidos/${id}`, { id, status: 'pendente', pedido_em: agora, trilha: trilha || 'Todas' })
    } catch {
      setErro(true)
    } finally {
      setEnviando(false)
    }
  }

  const tr = p && p.trilha && p.trilha !== 'Todas' ? ` de ${p.trilha}` : ''
  const msg =
    pedidos.status !== 'ok'
      ? ''
      : !p
        ? 'Roda as rotinas de busca na hora, fora dos horários fixos. Começa em até 30 minutos.'
        : p.status === 'pendente'
          ? `Busca${tr} pedida ${relativo(p.pedido_em, now)}. Começa em até 30 minutos.`
          : p.status === 'em_andamento'
            ? `Iniciando a busca${tr}…`
            : p.status === 'disparada'
              ? `Busca${tr} iniciada em ${fmtDataHora(p.disparada_em)}.`
              : p.status === 'erro'
                ? `A última busca não começou: ${p.obs || 'erro sem detalhe'}`
                : `Último pedido em ${fmtDataHora(p.pedido_em)}.`

  return (
    <div className="jh-run" id="buscar">
      <Btn
        variant="primary"
        size="lg"
        className="jh-run-btn"
        icon={Icon.refresh}
        busy={enviando || ativo}
        disabled={enviando || ativo}
        onClick={pedir}
      >
        {ativo ? 'Busca na fila' : 'Buscar agora'}
      </Btn>
      <span className="jh-muted" aria-live="polite">{msg}</span>
      {erro && <span className="jh-err">Não foi salvo. Só editores do dashboard podem pedir uma busca.</span>}
    </div>
  )
}

export function Hero({ trilha, setTrilha, tema, setTema }: { trilha: string; setTrilha: (t: string) => void; tema: Tema; setTema: (t: Tema) => void }) {
  const { status, rows } = useVagas(trilha)
  const exec = useSource<Execucao>('execucoes')
  const now = useNow()
  const c = contar(rows)
  const ultima = exec.data.map((r) => r.em).sort().slice(-1)[0]
  const perfil = useSource<{ nome?: string }>('perfil')
  const nome = perfil.status === 'ok' ? perfil.data.find((r) => r.nome)?.nome : undefined

  return (
    <header className="jh-card jh-hero" id="topo">
      <div className="jh-hero-glow" aria-hidden="true" />
      <div className="jh-top">
        <div className="jh-brand">
          <span className="jh-logo">{Icon.search}</span>
          <div>
            <div className="jh-eyebrow">{nome || 'Seu painel de vagas'}</div>
            <div className="jh-live">
              <i />
              <span>{ultima ? `Atualizado ${relativo(ultima, now)}` : 'Aguardando a primeira execução'}</span>
            </div>
          </div>
        </div>
        <Segmented<Tema>
          small
          label="Tema"
          value={tema}
          onChange={setTema}
          options={[
            { value: 'sistema', label: 'Sistema' },
            { value: 'claro', label: 'Claro' },
            { value: 'escuro', label: 'Escuro' },
          ]}
        />
      </div>
      <h1>
        Job <span>Hunting</span>
      </h1>
      <p className="jh-lead">
        {status !== 'ok'
          ? '—'
          : c.total
            ? `${c.perfil} de ${c.total} vagas analisadas estão no seu perfil. Claude enviou ${c.claude} candidatura${c.claude === 1 ? '' : 's'} e ${c.pend} esperam por você.`
            : 'Nenhuma vaga ainda. A primeira execução das rotinas vai preencher esta página.'}
      </p>
      <BuscarAgora trilha={trilha} />
      <Segmented<string>
        label="Trilha"
        value={trilha}
        onChange={setTrilha}
        options={[
          { value: '', label: 'Todos' },
          { value: 'Product Manager', label: 'Product Manager' },
          { value: 'Liderança', label: 'Liderança' },
        ]}
      />
    </header>
  )
}
