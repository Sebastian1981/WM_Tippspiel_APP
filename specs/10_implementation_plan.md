# 10_implementation_plan.md

## Phase 1: Lokaler MVP ohne echte Online-Daten

**Ziel:** Eine funktionierende App mit Mockdaten und deterministischem Basismodell.

Tasks:

1. Projektstruktur anlegen
2. React-Frontend erstellen
3. Express-Backend erstellen
4. Mockdaten für Teams anlegen
5. Feature Engineering implementieren
6. Basismodell implementieren
7. /api/predict implementieren
8. Ergebnis im Frontend anzeigen

**Erfolgskriterium:** Der Nutzer kann zwei Teams eingeben und erhält einen Basistipp mit Erklärung ohne LLM.

---

## Phase 2: LLM-Erklärung

**Ziel:** Das LLM erklärt die deterministische Prognose.

Tasks:

1. OpenAI-Service im Backend einrichten
2. Prompt für Erklärung definieren
3. JSON-Ausgabe validieren
4. Fallback ohne LLM einbauen
5. Frontend um Erklärung erweitern

**Erfolgskriterium:** Die App zeigt eine verständliche Analyse, ohne dass das LLM den Tipp frei überschreibt.

---

## Phase 3: Echte Matchdaten

**Ziel:** Online-Matchdaten abrufen.

Tasks:

1. Datenquelle auswählen
2. API-Key konfigurieren
3. Data-Service implementieren
4. Normalisierung der API-Daten
5. Cache einbauen
6. Datenqualität anzeigen

**Erfolgskriterium:** Die App nutzt echte Matchdaten statt Mockdaten.

---

## Phase 4: Ensemble-Modell

**Ziel:** Mehrere Prognosequellen kombinieren.

Tasks:

1. Ranking-/Elo-Modell ergänzen
2. optional Quotenmodell ergänzen
3. Ensemble-Gewichtung implementieren
4. fehlende Modelle dynamisch behandeln
5. Policy Engine implementieren

**Erfolgskriterium:** Das System gibt Basismodell, Teilmodelle und Ensemble-Tipp aus.

---

## Phase 5: LLM-Metadaten

**Ziel:** Das LLM extrahiert Metadaten aus News/Texten.

Tasks:

1. Newsdaten beschaffen
2. LLM-Metadaten-Prompt implementieren
3. JSON-Schema validieren
4. Adjustment-Grenzen implementieren
5. Policy Engine prüft Adjustments

**Erfolgskriterium:** Metadaten können die Wahrscheinlichkeiten leicht und kontrolliert anpassen.

---

## Phase 6: Backtesting

**Ziel:** Historische Validierung.

Tasks:

1. historische WM-Daten laden
2. Backtest-Service implementieren
3. Metriken berechnen
4. Modelle vergleichen
5. Gewichtungen anhand Backtest verbessern

**Erfolgskriterium:** Das beste Modell wird datenbasiert ausgewählt.

---

## Phase 7: MCP-ready Refactoring

**Ziel:** Tool-Schnittstellen so strukturieren, dass später MCP einfach ergänzt werden kann.

Tasks:

1. interne Tool-Interfaces definieren
2. Datenabrufe kapseln
3. Prediction Tools kapseln
4. MCP-Server optional ergänzen
5. Agent darf Tools nutzen, aber finale Policy bleibt im Code

**Erfolgskriterium:** Das System bleibt ohne MCP lauffähig, kann aber später MCP-Tools bereitstellen.
