# 07_backtesting_spec.md

## Ziel
Das System soll später historisch überprüfbar sein. **Primäre Metrik ist der simulierte Kicktipp-Punkteertrag** (nicht generische ML-Metriken wie Brier Score allein).

## Warum Backtesting wichtig ist
Nicht die plausibelste Erklärung gewinnt, sondern das Modell mit dem **höchsten durchschnittlichen Expected-Points-Ertrag** gemäß Kicktipp-Regelwerk.

## Zu vergleichende Modelle

Mindestens:

1. baseline_v1
2. baseline_v1 + ranking
3. baseline_v1 + odds
4. baseline_v1 + metadata
5. ensemble_v1

## Metriken

### Kicktipp Expected Points (Primärmetrik)
Simulierter durchschnittlicher Kicktipp-Punkteertrag pro Spiel gemäß 2–4 Punkte Turnier-Regel.

```
avg_kicktipp_pts = Σ pts(tip(a,b), actual(i,j)) / n_matches
```

### 1X2 Accuracy
Misst, ob Sieg/Unentschieden/Niederlage richtig vorhergesagt wurde.

### Exact Score Accuracy
Misst, ob das exakte Ergebnis richtig vorhergesagt wurde.

### Brier Score
Misst die Qualität probabilistischer Vorhersagen.

### Log Loss
Misst, ob Wahrscheinlichkeiten gut kalibriert sind.

### Calibration
Prüft, ob vorhergesagte Wahrscheinlichkeiten langfristig stimmen.

## Backtest-Datensatz

**MVP:**

- historische WM-Spiele 2014, 2018, 2022

**Später:**

- EM-Spiele
- Nations League
- Qualifikationsspiele
- Freundschaftsspiele

## Output

```json
{
  "model": "poisson_elo_v1",
  "matches": 192,
  "avg_kicktipp_pts": 2.14,
  "accuracy1x2": 0.55,
  "exactScoreAccuracy": 0.12,
  "brierScore": 0.19,
  "logLoss": 0.92,
  "notes": [
    "Expected-Points-Optimierer übertrifft naiven Wahrscheinlichkeitstipp um +0.18 Pkt/Spiel.",
    "Bayesianisches WM-Form-Updating verbessert Prognose ab Spieltag 2."
  ]
}
```

## Entscheidungskriterium
Ein neues Modell darf nur Standard werden, wenn es im Backtest einen **höheren avg_kicktipp_pts** erzielt als das aktuelle Modell.
