import { useState } from 'react'
import { predict } from '../api'

const TEAMS = [
  "Mexiko","Südkorea","Tschechien","Südafrika",
  "Schweiz","Kanada","Bosnien","Katar",
  "Brasilien","Marokko","Schottland","Haiti",
  "Türkei","Paraguay","Australien","USA",
  "Ecuador","Deutschland","Elfenbeinküste","Curaçao",
  "Niederlande","Japan","Schweden","Tunesien",
  "Belgien","Iran","Ägypten","Neuseeland",
  "Spanien","Uruguay","Kap Verde","Saudi-Arabien",
  "Frankreich","Norwegen","Senegal","Irak",
  "Argentinien","Österreich","Algerien","Jordanien",
  "Portugal","Kolumbien","Usbekistan","DR Kongo",
  "England","Kroatien","Panama","Ghana",
].sort()

export default function PredictForm() {
  const [teamA, setTeamA] = useState('')
  const [teamB, setTeamB] = useState('')
  const [phase, setPhase] = useState('group')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!teamA || !teamB) { setError('Bitte beide Teams auswählen.'); return }
    if (teamA === teamB) { setError('Team A und B dürfen nicht identisch sein.'); return }
    setError(null)
    setLoading(true)
    try {
      const data = await predict(teamA, teamB, phase)
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Backend nicht erreichbar.')
    } finally {
      setLoading(false)
    }
  }

  const pct = (v) => `${(v * 100).toFixed(1)}%`

  return (
    <div className="card">
      <h2>⚽ Spieltipp berechnen</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label>Team A</label>
            <select value={teamA} onChange={e => setTeamA(e.target.value)}>
              <option value="">-- Team wählen --</option>
              {TEAMS.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="vs">vs</div>
          <div className="form-group">
            <label>Team B</label>
            <select value={teamB} onChange={e => setTeamB(e.target.value)}>
              <option value="">-- Team wählen --</option>
              {TEAMS.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
        </div>
        <div className="form-group">
          <label>Spielphase</label>
          <select value={phase} onChange={e => setPhase(e.target.value)}>
            <option value="group">Gruppenspiel</option>
            <option value="ko">KO-Runde (Elfmeterschießen möglich)</option>
          </select>
        </div>
        {error && <div className="error">{error}</div>}
        <button type="submit" disabled={loading}>
          {loading ? 'Berechne…' : 'Tipp berechnen'}
        </button>
      </form>

      {result && (
        <div className="result">
          <h3>{result.team_a} vs {result.team_b}</h3>

          <div className="tip-box">
            <div className="tip-label">Optimaler Tipp</div>
            <div className="tip-value">{result.optimal_tip}</div>
            <div className="tip-ep">Erwartete Punkte: <strong>{result.expected_points}</strong></div>
          </div>

          <div className="probs">
            <div className="prob-bar">
              <span>{result.team_a}</span>
              <div className="bar" style={{ width: pct(result.probabilities.team_a_win) }}></div>
              <span>{pct(result.probabilities.team_a_win)}</span>
            </div>
            <div className="prob-bar draw">
              <span>Unentschieden</span>
              <div className="bar" style={{ width: pct(result.probabilities.draw) }}></div>
              <span>{pct(result.probabilities.draw)}</span>
            </div>
            <div className="prob-bar">
              <span>{result.team_b}</span>
              <div className="bar" style={{ width: pct(result.probabilities.team_b_win) }}></div>
              <span>{pct(result.probabilities.team_b_win)}</span>
            </div>
          </div>

          <div className="alternatives">
            <strong>Top-Alternativen:</strong>
            {result.top_alternatives.map(a => (
              <span key={a.tip} className="alt-tip">{a.tip} ({a.expected_points} Pkt)</span>
            ))}
          </div>

          <div className="meta">
            Elo: {result.team_a} {result.elo_a} | {result.team_b} {result.elo_b} |
            WM-Spiele: {result.data_sources.wm_games_a} / {result.data_sources.wm_games_b}
          </div>
        </div>
      )}
    </div>
  )
}
