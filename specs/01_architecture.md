# 01_architecture.md

## Zielarchitektur
Die Anwendung besteht aus:

1. React-Frontend
2. Node/Express-Backend
3. Data-Service
4. Feature-Engineering-Service
5. Poisson-Prediction-Engine
6. Expected-Points-Optimizer
7. Tournament-Simulation-Service (Monte-Carlo)
8. LLM-Metadata-Service
9. Policy-/Ensemble-Engine
10. optional später MCP-Server

## MVP-Architektur

```
React Frontend
  ↓
Express API
  ↓
Prediction Orchestrator
  ↓
Data Service (Elo-Ratings + WM-Ergebnisse)
  ↓
Poisson Model (lambda_A, lambda_B aus Elo + WM-Form)
  ↓
Expected-Points-Optimizer (argmax über 36 Tipps)
  ↓
Tournament Simulator (Monte-Carlo, Sonderfragen)
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
Datenquellen liefern Elo-Ratings + WM-Ergebnisse.
Poisson-Modell berechnet P(i,j) für alle Scorelines.
Expected-Points-Optimizer wählt den punkteoptimalen Tipp.
Tournament-Simulator liefert Sonderfrage-Empfehlungen.
LLM extrahiert Metadaten und erklärt die Empfehlung.
```

**Die Zielfunktion ist immer: Maximiere E[Kicktipp-Punkte], nicht P(wahrscheinlichstes Ergebnis).**

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

- Berechnet Poisson-Torerwartungen aus Elo-Ratings
- Wendet Bayesianisches Updating mit WM-Form an (α-Gewichtung)
- Berechnet vollständige Score-Verteilung P(i,j)
- Expected-Points-Optimizer: argmax_(a,b) E[pts(a,b)]
- KO-Modus: Unentschieden-Masse auf Siegtipps umverteilen
- Tournament-Simulator: Monte-Carlo über Gruppenphase + KO-Bracket

### Policy Engine

- Kombiniert Modellresultate
- Verhindert unkontrollierte LLM-Überschreibungen
- Erzwingt erlaubte Tipp-Anpassungen

### LLM Service

- Erklärt Ergebnisse
- Extrahiert Metadaten aus Texten
- Gibt strukturierte JSON-Antworten zurück
