# 07_backtesting_spec.md

## Ziel
Das System soll später historisch überprüfbar sein.

## Warum Backtesting wichtig ist
Nicht die plausibelste Erklärung gewinnt, sondern das Modell mit der besten historischen Trefferquote und Kalibrierung.

## Zu vergleichende Modelle

Mindestens:

1. baseline_v1
2. baseline_v1 + ranking
3. baseline_v1 + odds
4. baseline_v1 + metadata
5. ensemble_v1

## Metriken

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

Beispiel:

> Wenn das Modell 60 % Siegwahrscheinlichkeit prognostiziert, sollten solche Spiele ungefähr in 60 % der Fälle gewonnen werden.

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
  "model": "ensemble_v1",
  "matches": 192,
  "accuracy1x2": 0.55,
  "exactScoreAccuracy": 0.12,
  "brierScore": 0.19,
  "logLoss": 0.92,
  "notes": [
    "Odds model performed best on 1X2.",
    "Metadata adjustment did not improve exact score accuracy."
  ]
}
```

## Entscheidungskriterium
Ein neues Modell darf nur Standard werden, wenn es im Backtest besser ist als das aktuelle Modell.
