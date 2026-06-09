import { useState } from 'react'
import { addResult } from '../api'

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

export default function ResultEntry() {
  const [teamA, setTeamA] = useState('')
  const [teamB, setTeamB] = useState('')
  const [scoreA, setScoreA] = useState('')
  const [scoreB, setScoreB] = useState('')
  const [msg, setMsg] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await addResult({
        team_a: teamA, team_b: teamB,
        score_a: parseInt(scoreA), score_b: parseInt(scoreB),
      })
      setMsg(`✅ Ergebnis gespeichert: ${teamA} ${scoreA}:${scoreB} ${teamB}`)
      setTeamA(''); setTeamB(''); setScoreA(''); setScoreB('')
    } catch {
      setMsg('❌ Fehler beim Speichern.')
    }
  }

  return (
    <div className="card">
      <h2>📝 WM-Ergebnis eintragen</h2>
      <p>Trage gespielte Ergebnisse ein, damit das Modell die WM-Form berücksichtigt.</p>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <select value={teamA} onChange={e => setTeamA(e.target.value)} required>
            <option value="">Team A</option>
            {TEAMS.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <input type="number" min="0" max="20" placeholder="Tore A"
            value={scoreA} onChange={e => setScoreA(e.target.value)} required />
          <span>:</span>
          <input type="number" min="0" max="20" placeholder="Tore B"
            value={scoreB} onChange={e => setScoreB(e.target.value)} required />
          <select value={teamB} onChange={e => setTeamB(e.target.value)} required>
            <option value="">Team B</option>
            {TEAMS.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
        <button type="submit">Ergebnis speichern</button>
      </form>
      {msg && <div className="msg">{msg}</div>}
    </div>
  )
}
