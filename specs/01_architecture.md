# 01_architecture.md

## Zielarchitektur
Die Anwendung besteht aus:

1. React-Frontend (Vite)
2. **Python/FastAPI-Backend** (statt Node/Express – wegen nativer scipy/numpy-Integration für Poisson-Modell)
3. Data-Service (JSON-Datendateien, später API)
4. Poisson-Prediction-Engine
5. Expected-Points-Optimizer
6. Tournament-Simulation-Service (Monte-Carlo)
7. LLM-Metadata-Service
8. optional später MCP-Server

> **Architekturentscheidung:** Backend in Python/FastAPI statt Node/Express.
> Begründung: Poisson-Modell und Monte-Carlo-Simulation nutzen scipy/numpy nativ.
> Kein Portierungsaufwand, keine externe Abhängigkeit für Mathematik.

## MVP-Architektur

```
React Frontend (Vite, localhost:5173)
  ↓ HTTP
FastAPI Backend (localhost:8000)
  ↓
Prediction Orchestrator
  ↓
Data Service (elo_ratings.json + wm_results.json)
  ↓
Poisson Model (lambda_A, lambda_B aus Elo + WM-Form)
  ↓
Expected-Points-Optimizer (argmax über 36 Tipps)
  ↓
Tournament Simulator (Monte-Carlo, Sonderfragen)
  ↓
LLM Explanation Service (optional)
  ↓
JSON Response an Frontend
```

## Verzeichnisstruktur

```
WM_Tippspiel_APP/
  specs/
  backend/
    main.py                  # FastAPI App + Endpunkte
    requirements.txt
    src/
      data/
        elo_ratings.json     # Elo-Ratings aller 48 Teams
        groups.json          # Gruppen A-L
        schedule.json        # Spielplan (alle Spieltage)
        wm_results.json      # WM-Ergebnisse (wird befüllt)
      model/
        poisson.py           # Torerwartung + Score-Verteilung
        bayesian_update.py   # α-gewichtetes WM-Form-Updating
      optimizer/
        expected_points.py   # Punktefunktion + argmax E[pts]
      simulation/
        tournament.py        # Monte-Carlo Gruppenphase + KO
  frontend/
    (React Vite App)
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
