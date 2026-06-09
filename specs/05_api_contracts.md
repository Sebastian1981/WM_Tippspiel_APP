# 05_api_contracts.md

## Endpoint: POST /api/predict

### Zweck
Erzeugt eine vollständige Vorhersage für ein Spiel.

### Request

```json
{
  "teamA": "Germany",
  "teamB": "Brazil",
  "strategy": "balanced",
  "useMetadata": true,
  "useOdds": false
}
```

### Felder

| Feld          | Typ                                   | Pflicht |
|---------------|---------------------------------------|---------|
| teamA         | string                                | ja      |
| teamB         | string                                | ja      |
| strategy      | `conservative` \| `balanced` \| `bold` | nein    |
| useMetadata   | boolean                               | nein    |
| useOdds       | boolean                               | nein    |

### Response

```json
{
  "match": {
    "teamA": "Germany",
    "teamB": "Brazil"
  },
  "dataQuality": {
    "matchDataAvailable": true,
    "oddsAvailable": false,
    "metadataAvailable": true,
    "warnings": []
  },
  "features": {
    "teamA": {},
    "teamB": {}
  },
  "models": {
    "baseline": {},
    "elo": null,
    "odds": null,
    "metadataAdjustment": {}
  },
  "ensemble": {
    "probabilities": {
      "teamAWin": 0.45,
      "draw": 0.29,
      "teamBWin": 0.26
    },
    "tip": "2:1",
    "confidence": "low_to_medium"
  },
  "llmExplanation": {
    "shortSummary": "...",
    "mainReasons": [],
    "mainUncertainties": [],
    "recommendedTip": "2:1",
    "explanation": "..."
  }
}
```

---

## Endpoint: GET /api/health

### Zweck
Prüft, ob Backend verfügbar ist.

### Response

```json
{
  "status": "ok"
}
```

---

## Endpoint: GET /api/teams

### Zweck
Gibt verfügbare Teams zurück.

### Response

```json
{
  "teams": [
    "Germany",
    "Brazil",
    "Argentina",
    "France"
  ]
}
```

---

## Endpoint: POST /api/backtest

### Zweck
Startet Backtest auf historischen Spielen.

MVP: optional.

### Request

```json
{
  "competition": "world_cup",
  "fromYear": 2014,
  "toYear": 2022,
  "model": "baseline_v1"
}
```

### Response

```json
{
  "model": "baseline_v1",
  "matches": 192,
  "accuracy1x2": 0.52,
  "exactScoreAccuracy": 0.11,
  "brierScore": 0.21,
  "logLoss": 0.98
}
```
