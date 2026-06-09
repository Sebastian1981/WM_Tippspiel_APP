# 10_implementation_plan.md

## Überblick

| Phase | Titel | Ziel | Deadline |
|---|---|---|---|
| 0 | Sofort-Tipp-Skript | Alle Kicktipp-Tipps für morgen | **10.06.2026** |
| 1 | Python-Kern-MVP | Sauberes, wiederverwendbares Poisson-Modell | laufend |
| 2 | Bayesianisches Updating | WM-Ergebnisse fließen live ein | ab 11.06.2026 |
| 3 | LLM-Erklärung | Erklärbare Tipps | nach WM-Start |
| 4 | Web-App (React + Express) | Bedienbare UI | nach Phase 3 |
| 5 | Live-Daten-Anbindung | Automatisches Datenholen | nach Phase 4 |
| 6 | Backtesting | Modellvalidierung | Post-WM |
| 7 | MCP-ready Refactoring | Langfristige Erweiterbarkeit | Post-WM |

---

## Phase 0: Sofort-Tipp-Skript ⚡

**Ziel:** Ein lauffähiges Python-Skript, das heute noch alle benötigten Kicktipp-Tipps berechnet und ausgibt.

**Deadline: 10.06.2026 (morgen früh)**

Tasks:

1. `wm_tipps.py` erstellen mit hardcodierten Elo-Ratings aller 48 Teams
2. Poisson-Modell implementieren (`lambda_A`, `lambda_B` aus Elo-Differenz)
3. Score-Verteilung `P(i,j)` berechnen (0:0 bis 7:7)
4. Kicktipp-Punktefunktion `pts(a,b,i,j)` implementieren (2–4 Punkte, Turnier-Regel)
5. Expected-Points-Optimierer: `argmax_(a,b) E[pts(a,b)]` über 36 Tipps
6. Monte-Carlo-Turniersimulation (50.000 Iterationen) für Gruppenphase
7. KO-Bracket-Simulation für Halbfinale und Weltmeister
8. Torschützenkönig-Team-Proxy berechnen
9. Alle Ergebnisse auf der Konsole ausgeben

**Erfolgskriterium:** Das Skript liefert für alle 15 Sonderfragen und alle Spieltag-1-Spiele konkrete Tipps. `pip install scipy numpy` ist die einzige Abhängigkeit.

---

## Phase 1: Python-Kern-MVP

**Ziel:** Das Skript aus Phase 0 in ein sauberes, modulares Python-Paket umstrukturieren.

Tasks:

1. Projektstruktur anlegen (`/src/model/`, `/src/data/`, `/src/optimizer/`, `/src/simulation/`)
2. `data/elo_ratings.json` und `data/groups.json` als Datendateien anlegen
3. `model/poisson.py` — Poisson-Modell mit Elo-Input
4. `optimizer/expected_points.py` — Expected-Points-Optimierer + Punktefunktion
5. `simulation/tournament.py` — Monte-Carlo-Turniersimulation
6. `data/wm_results.json` — leere Datei für WM-Ergebnisse (wird in Phase 2 befüllt)
7. `main.py` als Einstiegspunkt mit CLI-Argumenten (z.B. `--match "Deutschland Ecuador"`)
8. Unit-Tests für Punktefunktion (alle Grenzfälle)

**Erfolgskriterium:** `python main.py --match "Deutschland Ecuador"` gibt optimalen Tipp + E[pts] aus.

---

## Phase 2: Bayesianisches Updating (WM-Form)

**Ziel:** WM-Ergebnisse fließen automatisch in die Torerwartung ein.

**Startet:** ab 11.06.2026, sobald erste Spiele gespielt sind.

Tasks:

1. `data/wm_results.json` nach jedem Spieltag manuell oder per Skript befüllen
2. `model/bayesian_update.py` — α-gewichtete Kombination aus Elo-Prior und WM-Form
3. WM-Form-Score aus bisherigen Toren, Gegentoren, Punkten berechnen
4. α-Tabelle implementieren (0 Spiele → 0.0, 1 → 0.40, 2 → 0.65, 3+ → 0.85)
5. Poisson-Modell nutzt automatisch aktualisierte Stärke-Schätzung
6. KO-Modus: Unentschieden-Masse auf Sieger umverteilen

**Erfolgskriterium:** Nach Spieltag 1 liefert das Modell für Spieltag-2-Spiele angepasste Prognosen.

---

## Phase 3: LLM-Erklärung

**Ziel:** Das LLM erklärt den Tipp nachvollziehbar, ohne ihn zu überschreiben.

Tasks:

1. OpenAI/Anthropic-Service konfigurieren (API-Key in `.env`)
2. Prompt-Template: Modell-Output als strukturierter JSON-Input ans LLM
3. LLM gibt Erklärung zurück (keine freie Tippänderung)
4. Fallback: Wenn LLM nicht erreichbar, wird Erklärung weggelassen (Tipp bleibt)
5. Ausgabe enthält: Tipp, E[pts], P(A/X/B), LLM-Erklärung, genutzte Datenquellen

**Erfolgskriterium:** Die App zeigt eine verständliche Analyse. LLM ändert den Tipp nicht.

---

## Phase 4: Web-App (React + Express)

**Ziel:** Bedienbare UI für den täglichen Einsatz während der WM.

Tasks:

1. Express-Backend mit `/api/predict` und `/api/special-questions`
2. React-Frontend mit Team-Eingabe, Tipp-Ausgabe, Wahrscheinlichkeitsanzeige
3. Sonderfragen-Ansicht (alle 15 Fragen mit Empfehlungen)
4. WM-Ergebnisse-Eingabemaske (für Bayesianisches Updating)
5. Ladezustand während Berechnung
6. Fehlerbehandlung bei Backend-Ausfall

**Erfolgskriterium:** Nutzer kann Teams eingeben und erhält Tipp mit Erklärung im Browser.

---

## Phase 5: Live-Daten-Anbindung

**Ziel:** WM-Ergebnisse und Elo-Ratings automatisch aktuell halten.

Tasks:

1. Fußball-API auswählen (z.B. football-data.org, API-Football)
2. Data-Service implementiert automatischen Abruf nach Spielende
3. Cache: Matchdaten 15 Min, Elo/Ranking 24h
4. `wm_results.json` wird automatisch befüllt
5. Datenqualitätsanzeige im Frontend (Quelle, Zeitstempel)

**Erfolgskriterium:** Das System aktualisiert sich nach jedem WM-Spieltag automatisch.

---

## Phase 6: Backtesting

**Ziel:** Modellqualität historisch validieren.

Tasks:

1. Historische WM-Daten 2014, 2018, 2022 laden
2. Backtest-Service: simuliere Tipps + berechne echte Kicktipp-Punkte
3. Primärmetrik: `avg_kicktipp_pts` pro Spiel (2–4 Punkte Turnier-Regel)
4. Sekundärmetriken: 1X2-Accuracy, Brier Score, Log Loss
5. Modellvergleich: Poisson-Elo vs. naive Baseline vs. Elo-only

**Erfolgskriterium:** Das Poisson-Modell übertrifft die naive Baseline in `avg_kicktipp_pts`.

---

## Phase 7: MCP-ready Refactoring

**Ziel:** Tool-Schnittstellen so strukturieren, dass später MCP-Tools ergänzt werden können.

Tasks:

1. Interne Tool-Interfaces für Daten, Modell, Simulation definieren
2. Datenabrufe kapseln (austauschbar: JSON → API → MCP)
3. Prediction-Tools kapseln
4. MCP-Server optional ergänzen
5. Finale Policy (Expected-Points-Optimizer) bleibt immer im Code, nicht im LLM

**Erfolgskriterium:** Das System läuft ohne MCP, kann aber später MCP-Tools bereitstellen.
