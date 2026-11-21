// Sample rows for local development only (`npm run dev`). The published page reads the real store.
const agora = Date.now()
const iso = (minAtras: number) => new Date(agora - minAtras * 60_000).toISOString()

const empresas = ['Nubank', 'Itaú', 'Stone', 'C6 Bank', 'iFood', 'Mercado Livre', 'XP Inc', 'PicPay', 'Ebanx', 'Gympass']
const titulosPm = ['Senior Product Manager', 'Group Product Manager', 'Technical Product Manager', 'Gerente de Produto']
const titulosLid = ['Engineering Manager', 'Head de Tecnologia', 'Coordenador de TI', 'AI Transformation Manager']
const statusPorMatch = (m: number) => (m > 85 ? 'aplicada_claude' : m >= 65 ? 'pendente' : 'abaixo')

const vagas: Record<string, Record<string, unknown>> = {}
for (let i = 0; i < 28; i++) {
  const pm = i % 2 === 0
  const match = Math.round(40 + ((i * 37) % 55))
  vagas[`demo-${i}`] = {
    titulo: (pm ? titulosPm : titulosLid)[i % 4],
    empresa: empresas[i % empresas.length],
    local: i % 3 ? 'Remoto – Brasil' : 'São Paulo/SP – híbrido',
    trilha: pm ? 'Product Manager' : 'Liderança',
    match,
    status: i === 5 ? 'aplicada_voce' : statusPorMatch(match),
    url: 'https://example.com/vaga/' + i,
    fonte: i % 2 ? 'LinkedIn (e-mail)' : 'Greenhouse',
    motivo: match >= 65 ? 'Match 65–80: você aplica' : 'Abaixo do corte',
    motivo_match: 'Exemplo de explicação do match.',
    alertas: i % 4 === 0 ? 'Inglês fluente' : '',
    encontrada_em: iso(i * 90),
  }
}

export const mockData: Record<string, Record<string, Record<string, unknown>>> = {
  'data/radar/vagas': vagas,
  'data/radar/execucoes': {
    'pm-demo': { em: iso(120), trilha: 'Product Manager', coletadas: 1849, novas: 3, aplicadas: 1, obs: 'Exemplo' },
    'lid-demo': { em: iso(90), trilha: 'Liderança', coletadas: 1720, novas: 2, aplicadas: 0, obs: 'Exemplo' },
  },
  'data/radar/pedidos': {},
  'data/radar/perfil': {
    perfil: {
      nome: 'Maria Teste',
      trilhas: [
        { id: 'product-manager', nome: 'Product Manager' },
        { id: 'lideranca', nome: 'Liderança' },
        { id: 'outras', nome: 'Outras vagas' },
      ],
    },
  },
  'data/radar/progresso': {
    pm: {
      trilha: 'Product Manager', etapa: 'analisando', detalhe: 'Revisando: Senior Product Manager – Nubank',
      processadas: 7, total: 18, novas: 2, iniciado_em: iso(9), atualizado_em: iso(1),
    },
  },
}
