import { StrictMode } from 'react'
import { createRoot, type Root } from 'react-dom/client'
import css from './styles.css?inline'
import { App } from './App'
import { RuntimeContext } from './hooks'
import { dashboardRuntime, mockRuntime } from './runtime'
import type { Runtime, Vaga } from './types'

declare const dash: {
  calc(id: string, opts: { title: string; description: string; inputs: string[]; fn: (...rows: Vaga[][]) => unknown }): void
  draw(name: string, opts: { mount(el: HTMLElement): unknown; update?(el: HTMLElement, made: unknown): void; unmount?(el: HTMLElement, made: unknown): void }): void
}

function render(root: Root, runtime: Runtime) {
  root.render(
    <StrictMode>
      <RuntimeContext.Provider value={runtime}>
        <App />
      </RuntimeContext.Provider>
    </StrictMode>,
  )
}

if (window.dash && window.claude) {
  // Counts each KPI and funnel figure is checked against; readers can see this function in Sources.
  dash.calc('resumo', {
    title: 'Resumo por trilha',
    description: 'Contagem de vagas por trilha (as trilhas vêm do perfil do usuário): analisadas, no perfil (match 65+), aplicadas por Claude, pendentes e aplicadas por você. Vagas excluídas na página ficam de fora.',
    inputs: ['vagas'],
    fn: (vagas) => {
      vagas = vagas.filter((r) => r.status !== 'excluida')
      const conta = (rs: Vaga[]) => {
        const p = rs.filter((r) => Number(r.match) >= 65)
        return {
          no_perfil: p.length,
          aplicadas_claude: p.filter((r) => r.status === 'aplicada_claude').length,
          pendentes: p.filter((r) => r.status === 'pendente').length,
          aplicadas_voce: p.filter((r) => r.status === 'aplicada_voce').length,
          total: rs.length,
        }
      }
      const trilhas = [...new Set(vagas.map((r) => r.trilha).filter(Boolean))].sort()
      return ['Todas', ...trilhas].map((t) =>
        Object.assign({ trilha: t }, conta(t === 'Todas' ? vagas : vagas.filter((r) => r.trilha === t))),
      )
    },
  })

  const { runtime, bump } = dashboardRuntime(window.dash, window.claude)
  dash.draw('app', {
    mount(el) {
      const style = document.createElement('style')
      style.textContent = css
      const host = document.createElement('div')
      el.replaceChildren(style, host)
      const root = createRoot(host)
      render(root, runtime)
      return root
    },
    update() {
      bump()
    },
    unmount(_el, made) {
      ;(made as Root).unmount()
    },
  })
} else {
  const style = document.createElement('style')
  style.textContent = css
  document.head.appendChild(style)
  render(createRoot(document.getElementById('root')!), mockRuntime())
}
