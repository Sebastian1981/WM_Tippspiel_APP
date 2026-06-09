import { useState, useEffect } from 'react'
import { getMatchdayTips } from '../api'

export default function MatchdayTips() {
  const [day, setDay] = useState(1)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const load = async (d) => {
    setLoading(true)
    setError(null)
    try {
      setData(await getMatchdayTips(d))
    } catch {
      setError('Backend nicht erreichbar.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load(day) }, [day])

  const pct = (v) => `${(v * 100).toFixed(1)}%`

  return (
    <div className="card">
      <h2>📅 Spieltag-Tipps</h2>
      <div className="tab-row">
        {[1, 2, 3].map(d => (
          <button key={d} className={day === d ? 'active' : ''} onClick={() => setDay(d)}>
            Spieltag {d}
          </button>
        ))}
      </div>

      {loading && <div className="loading">Berechne…</div>}
      {error && <div className="error">{error}</div>}

      {data && data.tips.length === 0 && (
        <div className="empty">Noch keine Spiele für Spieltag {day} eingetragen.</div>
      )}

      {data && data.tips.map((tip, i) => (
        <div key={i} className="match-row">
          <div className="match-teams">
            <span className="team">{tip.team_a}</span>
            <span className="tip-badge">{tip.optimal_tip}</span>
            <span className="team">{tip.team_b}</span>
            <span className="group-badge">Gruppe {tip.group}</span>
          </div>
          <div className="match-probs">
            <span>{tip.team_a}: {pct(tip.probabilities.team_a_win)}</span>
            <span>X: {pct(tip.probabilities.draw)}</span>
            <span>{tip.team_b}: {pct(tip.probabilities.team_b_win)}</span>
            <span className="ep">E[Pkt]: {tip.expected_points}</span>
          </div>
        </div>
      ))}
    </div>
  )
}
