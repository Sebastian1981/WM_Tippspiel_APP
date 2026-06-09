# 01_architecture.md

## Zielarchitektur
Die Anwendung besteht aus:

1. React-Frontend
2. Node/Express-Backend
3. Data-Service
4. Feature-Engineering-Service
5. Prediction-Engine
6. LLM-Metadata-Service
7. Policy-/Ensemble-Engine
8. optional später MCP-Server

## MVP-Architektur

```
React Frontend
  ↓
Express API
  ↓
Prediction Orchestrator
  ↓
Data Service
  ↓
Feature Engineering
  ↓
Prediction Engine
  ↓
LLM Explanation Service
  ↓
Response an Frontend
```

## Spätere MCP-ready Architektur

```
React Frontend
  ↓
Express API
  ↓
Prediction Orchestrator
  ↓
MCP Tool Layer
  ↓
Externe Datenquellen / lokale Tools / Suchtools
  ↓
Prediction Engine
  ↓
Policy Engine
  ↓
LLM Explanation
```

## Wichtige Architekturentscheidung
Die finale Prognose wird nicht frei vom LLM erzeugt.

Stattdessen gilt:

```
Datenquellen liefern Rohdaten.
Feature Engineering berechnet Kennzahlen.
Prediction Engine berechnet Basismodelle.
Policy Engine kombiniert Modelle.
LLM extrahiert Metadaten und erklärt.
```

## Verantwortlichkeiten

### Frontend

- Eingabe Team A / Team B
- Auswahl Tippstrategie
- Anzeige der Modell-Ergebnisse
- Anzeige der LLM-Erklärung
- Anzeige der Unsicherheit

### Backend

- Validiert Eingaben
- Holt Daten
- Berechnet Features
- Berechnet Vorhersagen
- Ruft LLM auf
- Gibt strukturierte JSON-Antwort zurück

### Data Service

- Holt Matchdaten
- Holt Teamdaten
- Holt optional Quoten
- Holt optional Metadaten/News
- Nutzt Cache, wenn API nicht verfügbar ist

### Prediction Engine

- Berechnet Basismodell
- Berechnet Formmodell
- Berechnet optional Elo-/Ranking-Modell
- Berechnet optional Odds-Modell

### Policy Engine

- Kombiniert Modellresultate
- Verhindert unkontrollierte LLM-Überschreibungen
- Erzwingt erlaubte Tipp-Anpassungen

### LLM Service

- Erklärt Ergebnisse
- Extrahiert Metadaten aus Texten
- Gibt strukturierte JSON-Antworten zurück
