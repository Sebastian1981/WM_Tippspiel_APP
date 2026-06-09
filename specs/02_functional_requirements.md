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

---

## FR-009: Kicktipp-Punktesystem (2–4 Punkte, Turnier-Regel)

Das System MUSS das exakte Kicktipp-Regelwerk kennen und anwenden.

### Punktetabelle

| Situation | Tendenz | Tordifferenz | Ergebnis |
|---|---|---|---|
| Sieg (neutral, kein Heim/Auswärts) | 2 | 3 | 4 |
| Unentschieden | 2 | — | 4 |

**Hinweise:**
- Bei Unentschieden entfällt die Tordifferenz-Stufe (Tordiff ist immer 0).
- Da alle WM-Spiele auf neutralen Plätzen stattfinden, gibt es keinen Unterschied zwischen Heim- und Auswärtssieg.
- Es wird das Ergebnis **nach Elfmeterschießen** getippt (relevant ab Achtelfinale).

### Formale Punktefunktion

Für Tipp (a, b) und eingetretenes Ergebnis (i, j):

```
pts(a,b,i,j):
  wenn a==i und b==j           → 4 (exaktes Ergebnis)
  wenn Tendenz korrekt und a==b → 2 (Unentschieden, nicht exakt)
  wenn (a-b)==(i-j) und a!=b   → 3 (Tordifferenz korrekt)
  wenn Tendenz korrekt          → 2 (nur Tendenz)
  sonst                         → 0
```

### Tiebreaker
Bei Gleichstand in der Gesamtpunktzahl entscheidet die Anzahl der **Spieltagssiege** über die Platzierung.

### Sonderfragen-Regel (4 Punkte)
Für jede richtige Antwort auf eine Sonderfrage: **4 Punkte**. Reihenfolge irrelevant.

---

## FR-010: Expected-Points-Optimierer

Das Backend MUSS für jeden Spieltipp den Tipp berechnen, der den **erwarteten Punkteertrag maximiert**.

```
E[pts(a,b)] = Σ P(i,j) * pts(a,b,i,j)  für alle (i,j)

Optimaler Tipp: argmax_(a,b) E[pts(a,b)]
```

Akzeptanzkriterien:
- Der Optimierer iteriert über alle Tipps (0:0 bis mindestens 5:5).
- Das wahrscheinlichste Ergebnis ist **nicht zwingend** der optimale Tipp.
- Der erwartete Punkteertrag wird im Output angezeigt.

---

## FR-011: Sonderfragen

Das System MUSS Empfehlungen für alle Kicktipp-Sonderfragen liefern.

**Deadline:** Alle Sonderfragen müssen vor dem ersten Spiel (11.06.2026, 21:00 Uhr) abgegeben werden.

| # | Frage | Typ | Max. Punkte |
|---|---|---|---|
| 1 | Welche Mannschaft stellt den Spieler mit den meisten Toren? | 4-Pkt | 4 |
| 2 | Wer erreicht das Halbfinale? (4 Tipps) | 4-Pkt | 16 |
| 3–14 | Wer gewinnt Gruppe A–L? (je 1 Tipp) | 4-Pkt | 48 |
| 15 | Wer wird Weltmeister? | 4-Pkt | 4 |

**Methode:** Monte-Carlo-Turniersimulation (≥ 30.000 Iterationen) auf Basis von Elo-Ratings.

---

## FR-012: KO-Phasen-Behandlung

Das System MUSS KO-Spiele separat behandeln.

- In KO-Spielen gibt es kein Unentschieden nach 90 Minuten im Tipp (→ Elfmeterschießen).
- Die Wahrscheinlichkeitsmasse für Unentschieden wird proportional auf Siegtipps umverteilt.
- Das Modell muss erkennen, ob es sich um ein Gruppenspiel oder KO-Spiel handelt.

---

## FR-013: Bayesianisches Updating (WM-Form)

Das System MUSS WM-interne Ergebnisse stärker gewichten als historische Daten.

```
Effektive Stärke = α * WM_form_score + (1-α) * elo_prior

α-Werte:
  0 WM-Spiele  → α = 0.00  (nur historisch)
  1 WM-Spiel   → α = 0.40
  2 WM-Spiele  → α = 0.65
  3+ WM-Spiele → α = 0.85
```

Akzeptanzkriterium: Ein Team, das in der WM deutlich unter- oder übertrifft, bekommt eine angepasste Stärke.

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
