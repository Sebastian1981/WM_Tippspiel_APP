# 03_prediction_engine_spec.md

## Ziel
Die Prediction Engine berechnet eine **probabilistische Vorhersage** (vollständige Score-Wahrscheinlichkeitsverteilung) und wählt daraus den Tipp mit dem **maximalen erwarteten Punkteertrag** gemäß Kicktipp-Regelwerk (2–4 Punkte, Turnier-Modus).

## Team-Feature-Modell
Für jedes Team werden berechnet:

```json
{
  "team": "Germany",
  "games": 3,
  "wins": 2,
  "draws": 1,
  "losses": 0,
  "goalsFor": 6,
  "goalsAgainst": 2,
  "points": 7,
  "pointsPerGame": 2.33,
  "goalsForPerGame": 2.0,
  "goalsAgainstPerGame": 0.67,
  "goalDifferencePerGame": 1.33,
  "form": ["W", "W", "D"]
}
```

## Poisson-Modell

Grundlage ist das **doppelte Poisson-Modell** für Torerwartungen.

### Torerwartung aus Elo-Ratings

```
BASE = 1.35   # Ø Tore pro Team pro Spiel (international)
SCALE = 600   # Elo-Skalierungsfaktor

elo_diff = elo_A - elo_B
lambda_A = max(0.25, BASE + elo_diff / SCALE)
lambda_B = max(0.25, BASE - elo_diff / SCALE)
```

### Score-Verteilung

```
P(i, j) = Poisson(i; lambda_A) * Poisson(j; lambda_B)
          normiert auf Ergebnisse 0:0 bis 7:7
```

### Bayesianisches Updating mit WM-Form

Sobald WM-Spiele gespielt wurden, wird der Elo-Prior angepasst:

```
α-Werte nach Anzahl gespielter WM-Spiele:
  0 Spiele  → α = 0.00  (nur historischer Elo)
  1 Spiel   → α = 0.40
  2 Spiele  → α = 0.65
  3+ Spiele → α = 0.85

Effektive Stärke = α * wm_form_score + (1-α) * elo_prior
```

## Expected-Points-Optimierer

Der optimale Tipp ist **nicht** das wahrscheinlichste Ergebnis, sondern das Ergebnis mit dem höchsten erwarteten Kicktipp-Punkteertrag.

```
E[pts(a,b)] = Σ_(i,j) P(i,j) * pts(a,b,i,j)

Optimaler Tipp: argmax_(a,b) E[pts(a,b)]
Suchraum: a ∈ {0..5}, b ∈ {0..5}  (36 mögliche Tipps)
```

### Punktefunktion pts(a,b,i,j)

```
pts(a,b,i,j):
  wenn a==i und b==j                      → 4  (exaktes Ergebnis)
  wenn a==b und i==j                      → 2  (Unentschieden, nicht exakt)
  wenn (a-b)==(i-j) und sign(a-b)==sign(i-j) und a!=b  → 3  (Tordifferenz)
  wenn sign(a-b) == sign(i-j)             → 2  (nur Tendenz)
  sonst                                   → 0
```

## KO-Phasen-Modus

Ab dem Achtelfinale (KO-Spiele) wird das **Ergebnis nach Elfmeterschießen** getippt.

- Die Wahrscheinlichkeitsmasse für Unentschieden (i==j) wird proportional auf Siegtipps verteilt.
- Die Elo-basierte Siegwahrscheinlichkeit bestimmt die Verteilung:

```
P_elo(A gewinnt) = 1 / (1 + 10^((elo_B - elo_A) / 400))
```

- Unentschieden-Masse wird aufgeteilt: P_elo(A) * P(draw) auf Tipp mit A-Sieg, (1-P_elo(A)) * P(draw) auf Tipp mit B-Sieg.

## Turniersimulation (Monte-Carlo)

Für Sonderfragen (Gruppensieger, Halbfinalisten, Weltmeister) wird eine Monte-Carlo-Simulation durchgeführt.

```
Anzahl Simulationen: 30.000–50.000

Gruppenphase:
  - Jedes Spiel wird mit Poisson-Modell simuliert.
  - Gruppe wird nach Punkte / Tordifferenz / Tore sortiert.
  - Die 2 Gruppenbesten und die 8 besten Dritten kommen weiter.

KO-Phase:
  - Jedes KO-Spiel: Sieger via Elo-Wahrscheinlichkeit.

Output je Team:
  P(Gruppensieger)
  P(Halbfinale)
  P(Weltmeister)
  E[Tore] (für Torschützenkönig-Team-Proxy)
```

## Wahrscheinlichkeits-Output

Zusätzlich zum optimalen Tipp werden ausgegeben:

```
P(Team A Sieg)      = Σ P(i,j) für i > j
P(Unentschieden)    = Σ P(i,j) für i == j
P(Team B Sieg)      = Σ P(i,j) für i < j
E[pts] des Tipps
Top-3 alternative Tipps mit E[pts]
```

## Output

```json
{
  "model": "poisson_elo_v1",
  "teamA": "Deutschland",
  "teamB": "Ecuador",
  "elo_A": 1932,
  "elo_B": 1938,
  "lambda_A": 1.34,
  "lambda_B": 1.36,
  "probabilities": {
    "teamAWin": 0.43,
    "draw": 0.28,
    "teamBWin": 0.29
  },
  "optimalTip": "1:1",
  "expectedPoints": 1.87,
  "alternativeTips": [
    {"tip": "2:1", "expectedPoints": 1.74},
    {"tip": "1:2", "expectedPoints": 1.72}
  ],
  "matchPhase": "group"
}
```
