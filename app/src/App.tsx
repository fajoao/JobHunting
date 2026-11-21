import { useState } from 'react'
import { Hero, type Tema } from './components/Hero'
import { Progresso } from './components/Progresso'
import { Funil, Empresas, Histograma, Kpis } from './components/Stats'
import { ComoFunciona, Execucoes, Vagas } from './components/Vagas'
import { usePersistentState } from './hooks'

export function App() {
  const [trilha, setTrilha] = useState('')
  const [tema, setTema] = usePersistentState<Tema>('jh-tema', 'sistema')
  return (
    <div className={`jh ${tema === 'claro' ? 'jh-claro' : tema === 'escuro' ? 'jh-escuro' : ''}`}>
      <Hero trilha={trilha} setTrilha={setTrilha} tema={tema} setTema={setTema} />
      <Progresso />
      <Kpis trilha={trilha} />
      <Funil trilha={trilha} />
      <section className="jh-grid2">
        <Histograma trilha={trilha} />
        <Empresas trilha={trilha} />
      </section>
      <Vagas trilha={trilha} />
      <Execucoes />
      <ComoFunciona />
    </div>
  )
}
