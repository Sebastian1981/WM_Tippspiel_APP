# 02_functional_requirements.md

## FR-001: Team-Eingabe
Der Nutzer MUSS zwei Teams eingeben können.

Akzeptanzkriterien:

- Team A darf nicht leer sein.
- Team B darf nicht leer sein.
- Team A und Team B dürfen nicht identisch sein.
- Die App zeigt eine Fehlermeldung bei ungültiger Eingabe.

## FR-002: Tippstrategie
Der Nutzer SOLL eine Tippstrategie auswählen können:

- konservativ
- ausgewogen
- mutig

Akzeptanzkriterien:

- Default ist "ausgewogen".
- Die Tippstrategie beeinflusst nur die finale Ergebnisauswahl, nicht die Rohwahrscheinlichkeiten.

## FR-003: Matchdaten abrufen
Das Backend MUSS Matchdaten für beide Teams abrufen oder aus einem lokalen Cache laden.

Akzeptanzkriterien:

- Für jedes Team werden bisherige WM-Spiele geladen.
- Falls keine Daten verfügbar sind, wird die Datenlage als dünn markiert.
- Die App darf nicht abstürzen, wenn die API nicht verfügbar ist.

## FR-004: Feature Engineering
Das Backend MUSS aus Matchdaten Kennzahlen berechnen.

Mindestkennzahlen:

- Spiele
- Siege
- Unentschieden
- Niederlagen
- Tore
- Gegentore
- Punkte
- Punkte pro Spiel
- Tore pro Spiel
- Gegentore pro Spiel
- Tordifferenz pro Spiel
- Formsequenz

## FR-005: Deterministischer Basistipp
Das Backend MUSS einen deterministischen Basistipp berechnen.

Akzeptanzkriterien:

- Gleiche Eingabedaten erzeugen immer denselben Basistipp.
- Der Basistipp ist ohne LLM berechenbar.
- Der Basistipp enthält:
  - Team-A-Score
  - Team-B-Score
  - Score-Differenz
  - Interpretation
  - Basistipp

## FR-006: Ensemble-Prognose
Das Backend SOLL mehrere Modelle kombinieren können.

MVP-Gewichtung:

- 60 Prozent Basismodell/Formmodell
- 30 Prozent Ranking-/Elo-Modell, falls verfügbar
- 10 Prozent LLM-Metadaten-Adjustment, falls verfügbar

Wenn ein Modell nicht verfügbar ist, müssen die verbleibenden Gewichte normalisiert werden.

## FR-007: LLM-Erklärung
Das Backend MUSS eine LLM-basierte Erklärung erzeugen können.

Akzeptanzkriterien:

- Das LLM erhält strukturierte Modelldaten.
- Das LLM darf keine erfundenen Verletzungen nennen.
- Das LLM muss Unsicherheiten benennen.
- Das LLM muss klar zwischen Datenfakten und Interpretation unterscheiden.

## FR-008: LLM-Metadaten
Das LLM SOLL Metadaten aus externen Texten extrahieren können.

Beispiele:

- Verletzungshinweise
- Rotation
- Motivation
- bereits qualifiziert
- Sperren
- Reisetage
- Ruhezeit
- Wetter
- Trainerwechsel

MVP: optional.

## FR-009: Begrenzte LLM-Anpassung
Das LLM DARF den deterministischen Tipp nicht frei überschreiben.

Es darf maximal eine leichte Anpassung vorschlagen.

Die Policy Engine MUSS jede Anpassung validieren.

## FR-010: Finaler Tipp
Die App MUSS einen empfohlenen Tippspiel-Tipp ausgeben.

Die Antwort enthält:

- Basistipp
- Ensemble-Tipp
- finaler empfohlener Tipp
- Begründung
- Konfidenz
- Risikohinweis

## FR-011: Fehlerfälle
Die App MUSS folgende Fehlerfälle behandeln:

- keine API-Daten
- ungültige Teams
- LLM nicht verfügbar
- Quoten nicht verfügbar
- unvollständige Daten
- Backend nicht erreichbar
