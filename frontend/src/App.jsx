import { useState } from 'react'
import PredictForm from './components/PredictForm'
import MatchdayTips from './components/MatchdayTips'
import SpecialQuestions from './components/SpecialQuestions'
import ResultEntry from './components/ResultEntry'
import './App.css'

const TABS = [
  { id: 'matchday', label: 'Spieltag-Tipps' },
  { id: 'predict',  label: 'Einzelspiel' },
  { id: 'special',  label: 'Sonderfragen' },
  { id: 'results',  label: 'Ergebnisse' },
]

export default function App() {
  const [tab, setTab] = useState('matchday')

  return (
    <div className="app">
      <header>
        <h1>WM 2026 Tippspiel-Assistent</h1>
        <p>Kicktipp-Punkteoptimierung - Poisson-Modell - Monte-Carlo-Simulation</p>
      </header>
      <nav>
        {TABS.map(t => (
          <button key={t.id} className={tab === t.id ? 'active' : ''} onClick={() => setTab(t.id)}>
            {t.label}
          </button>
        ))}
      </nav>
      <main>
        {tab === 'matchday' && <MatchdayTips />}
        {tab === 'predict'  && <PredictForm />}
        {tab === 'special'  && <SpecialQuestions />}
        {tab === 'results'  && <ResultEntry />}
      </main>
    </div>
  )
}
