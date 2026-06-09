import { useState } from 'react'
import { getSpecialQuestions } from '../api'

export default function SpecialQuestions() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const load = async () => {
    setLoading(true)
    setError(null)
    try {
      setData(await getSpecialQuestions())
    } catch {
      setError('Backend nicht erreichbar. Ist der Server gestartet?')
    } finally {
      setLoading(false)
    }
  }

  const pct = (v) => `${(v * 100).toFixed(1)}%`

  return (
    <div className="card">
      <h2>🏆 Sonderfragen</h2>
      <p className="deadline">⚠️ Deadline: 11.06.2026, 21:00 Uhr</p>

      {!data && !loading && (
        <button onClick={load}>Sonderfragen berechnen (ca. 30 Sek.)</button>
      )}
      {loading && <div className="loading">Monte-Carlo-Simulation läuft… (30.000 Iterationen)</div>}
      {error && <div className="error">{error}</div>}

      {data && (
        <>
          {/* Weltmeister */}
          <div className="special-section">
            <h3>🌍 Weltmeister</h3>
            <div className="recommendation">
              Tipp: <strong>{data.world_champion.recommendation}</strong>
            </div>
            <div className="prob-list">
              {data.world_champion.probabilities.slice(0, 6).map(({ team, probability }) => (
                <div key={team} className="prob-row">
                  <span className="prob-team">{team}</span>
                  <div className="prob-bar-bg">
                    <div className="prob-bar-fill" style={{ width: pct(probability) }}></div>
                  </div>
                  <span>{pct(probability)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Halbfinale */}
          <div className="special-section">
            <h3>🥈 Halbfinale (4 Tipps)</h3>
            <div className="recommendation">
              Tipps: <strong>{data.semifinalists.recommendations.join(', ')}</strong>
            </div>
            <div className="prob-list">
              {data.semifinalists.probabilities.slice(0, 8).map(({ team, probability }) => (
                <div key={team} className="prob-row">
                  <span className="prob-team">{team}</span>
                  <div className="prob-bar-bg">
                    <div className="prob-bar-fill" style={{ width: pct(probability) }}></div>
                  </div>
                  <span>{pct(probability)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Gruppensieger */}
          <div className="special-section">
            <h3>📊 Gruppensieger A–L</h3>
            <div className="group-grid">
              {Object.entries(data.group_winners).map(([grp, info]) => (
                <div key={grp} className="group-card">
                  <div className="group-label">Gruppe {grp}</div>
                  <div className="group-tip">{info.recommendation}</div>
                  <div className="group-prob">
                    {pct(info.probabilities[0]?.probability || 0)}
                  </div>
                  <div className="group-others">
                    {info.probabilities.slice(1, 3).map(({ team, probability }) => (
                      <span key={team}>{team} {pct(probability)}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Torschützenkönig */}
          <div className="special-section">
            <h3>⚽ Torschützenkönig-Team</h3>
            <div className="recommendation">
              Tipp: <strong>{data.top_scorer_team.recommendation}</strong>
            </div>
            <div className="prob-list">
              {data.top_scorer_team.top_5.map(({ team, score }) => (
                <div key={team} className="prob-row">
                  <span className="prob-team">{team}</span>
                  <span className="score-val">Score: {score}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="meta">Basis: {data.simulations.toLocaleString()} Monte-Carlo-Simulationen</div>
        </>
      )}
    </div>
  )
}
