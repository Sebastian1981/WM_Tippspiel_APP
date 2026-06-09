# 06_data_sources.md

## Ziel
Die App soll Online-Daten verwenden können, aber auch mit Cache oder Mockdaten lauffähig bleiben.

## Datenquellen-Typen

### Matchdaten

Benötigt:

- bisherige WM-Spiele
- Tore
- Gegentore
- Datum
- Turnierphase
- Teamnamen

### Ranking-/Elo-Daten

Optional:

- FIFA-Ranking
- Elo-Rating
- historische Teamstärke

### Quoten

Optional:

- Sieg Team A
- Unentschieden
- Sieg Team B
- Zeitpunkt der Quote
- Anbieter

### News/Metadaten

Optional:

- Verletzungen
- Sperren
- Rotation
- Motivation
- bereits qualifiziert
- Trainer-Aussagen

## MVP-Datenstrategie

**Phase 1:**

- Lokale Mockdaten
- Manuelle JSON-Daten
- Keine Pflicht zur Live-API

**Phase 2:**

- Fußball-API anbinden

**Phase 3:**

- Quoten-API anbinden

**Phase 4:**

- News-/Metadaten-Recherche ergänzen

## Cache-Regeln

Das Backend SOLL Daten cachen.

Empfehlung:

| Datentyp   | Cache-Dauer |
|------------|-------------|
| Matchdaten | 15 Minuten  |
| Quoten     | 5 Minuten   |
| News       | 30 Minuten  |
| Ranking    | 24 Stunden  |

## Datenqualitätsbewertung

Jede Vorhersage MUSS eine Datenqualitätsbewertung enthalten:

```json
{
  "matchDataAvailable": true,
  "oddsAvailable": false,
  "metadataAvailable": false,
  "sampleSize": "low",
  "warnings": [
    "Only two tournament matches available."
  ]
}
```
