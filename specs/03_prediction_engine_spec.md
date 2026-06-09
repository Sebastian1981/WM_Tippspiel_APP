# 03_prediction_engine_spec.md

## Ziel
Die Prediction Engine berechnet eine nachvollziehbare, deterministische Vorhersage auf Basis strukturierter Teamdaten.

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

## Basismodell
Der Team-Score wird berechnet als:

```
S =
0.35 * pointsPerGame
+ 0.25 * goalDifferencePerGame
+ 0.20 * goalsForPerGame
- 0.20 * goalsAgainstPerGame
```

## Score-Differenz

```
diff = scoreTeamA - scoreTeamB
```

## Interpretation

```
diff > 0.70          → Team A klar stärker
0.25 < diff ≤ 0.70   → Team A leicht stärker
-0.25 ≤ diff ≤ 0.25  → ausgeglichen
-0.70 ≤ diff < -0.25 → Team B leicht stärker
diff < -0.70         → Team B klar stärker
```

## Basistipp-Regeln

```
Team A klar stärker      → 2:0
Team A leicht stärker    → 2:1
ausgeglichen             → 1:1
Team B leicht stärker    → 1:2
Team B klar stärker      → 0:2
```

## Ergebnisauswahl nach Strategie

### konservativ
Bevorzugt knappe und risikoarme Ergebnisse:

- 1:0
- 1:1
- 0:1
- 2:1
- 1:2

### ausgewogen
Nutzt Standardregeln:

- 2:0
- 2:1
- 1:1
- 1:2
- 0:2

### mutig
Erlaubt etwas stärkere Ergebnisdifferenzen:

- 2:0
- 3:1
- 2:1
- 1:2
- 1:3
- 0:2

## Wahrscheinlichkeiten
Im MVP können Wahrscheinlichkeiten approximiert werden.

Beispiel:

```
diff nahe 0:
Team A Sieg: 33 %
Unentschieden: 34 %
Team B Sieg: 33 %

diff = +0.4:
Team A Sieg: 45 %
Unentschieden: 29 %
Team B Sieg: 26 %

diff = +0.8:
Team A Sieg: 55 %
Unentschieden: 25 %
Team B Sieg: 20 %
```

Die konkrete Kalibrierung darf später durch Backtesting verbessert werden.

## Output

```json
{
  "model": "baseline_v1",
  "teamAScore": 1.42,
  "teamBScore": 1.00,
  "diff": 0.42,
  "interpretation": "Team A leicht stärker",
  "probabilities": {
    "teamAWin": 0.45,
    "draw": 0.29,
    "teamBWin": 0.26
  },
  "baselineTip": "2:1",
  "confidence": "low_to_medium"
}
```
