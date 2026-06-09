# 11_epics_and_stories.md

## Rollen
- **Nutzer** — will den punkteoptimalen Kicktipp-Tipp mit Erklärung sehen
- **Product Owner** — will Qualität, Transparenz und Punktemaximierung sicherstellen
- **Entwickler** — will sauberen, testbaren, robusten Code

---

## Sprint 0 — Sofort-Tipp-Skript ⚡ (Deadline: 10.06.2026)

- **US-00** `[Phase 0]` Als **Nutzer** möchte ich ein lauffähiges Python-Skript haben, das alle Kicktipp-Tipps (Spieltag 1 + alle 15 Sonderfragen) auf einmal berechnet und ausgibt, damit ich sie morgen vor Deadline eintragen kann.

- **US-01** `[Phase 0]` Als **Entwickler** möchte ich die Kicktipp-Punktefunktion `pts(a,b,i,j)` korrekt implementiert haben (2–4 Punkte, Turnier-Regel, inkl. Unentschieden-Sonderfall), damit der Optimierer die richtigen Werte berechnet.

- **US-02** `[Phase 0]` Als **Nutzer** möchte ich für jedes Spiel nicht nur den wahrscheinlichsten, sondern den **punkteoptimalen Tipp** sehen (`argmax E[pts]`), damit ich mehr Kicktipp-Punkte erhalte als mit einer naiven Vorhersage.

- **US-03** `[Phase 0]` Als **Nutzer** möchte ich für alle 12 Gruppensieger-Fragen (A–L) eine datenbasierte Empfehlung mit Wahrscheinlichkeit sehen, damit ich alle 48 Punkte dieser Sonderfragen optimal abgreifen kann.

- **US-04** `[Phase 0]` Als **Nutzer** möchte ich 4 Halbfinalisten-Empfehlungen und 1 Weltmeister-Empfehlung auf Basis einer Monte-Carlo-Simulation sehen, damit ich diese Sonderfragen datenbasiert beantworten kann.

- **US-05** `[Phase 0]` Als **Nutzer** möchte ich eine Torschützenkönig-Team-Empfehlung sehen (Proxy: Angriffsstärke × erwartete Spiele), damit ich auch diese Sonderfrage nicht raten muss.

---

## Sprint 1 — Modulares Python-Kern-MVP

- **US-06** `[Phase 1]` Als **Entwickler** möchte ich das Skript in Module aufgeteilt haben (`poisson.py`, `expected_points.py`, `tournament.py`, `data/`), damit der Code testbar und erweiterbar ist.

- **US-07** `[Phase 1]` Als **Entwickler** möchte ich Elo-Ratings und Gruppen als JSON-Datendateien haben (nicht hardcoded im Code), damit Daten einfach aktualisiert werden können.

- **US-08** `[Phase 1]` Als **Nutzer** möchte ich das Skript mit einem CLI-Argument aufrufen können (`python main.py --match "Deutschland Ecuador"`), damit ich jederzeit einen einzelnen Tipp berechnen kann.

- **US-09** `[Phase 1]` Als **Entwickler** möchte ich Unit-Tests für die Punktefunktion haben (alle Grenzfälle: exaktes Ergebnis, Tordifferenz, Tendenz, Unentschieden, KO-Modus), damit Berechnungsfehler sofort auffallen.

- **US-10** `[Phase 1]` Als **Entwickler** möchte ich eine leere `wm_results.json` als Platzhalter haben, damit Phase 2 (Bayesianisches Updating) nahtlos andocken kann.

---

## Sprint 2 — Bayesianisches Updating

- **US-11** `[Phase 2]` Als **Nutzer** möchte ich dass das Modell nach jedem WM-Spieltag automatisch aktualisierte Stärke-Schätzungen verwendet, damit Spieltag-2-Tipps die tatsächliche WM-Form berücksichtigen.

- **US-12** `[Phase 2]` Als **Entwickler** möchte ich die α-Gewichtung (`0 Spiele → 0.0, 1 → 0.40, 2 → 0.65, 3+ → 0.85`) als konfigurierbare Konstante implementiert haben, damit sie per Backtesting später optimiert werden kann.

- **US-13** `[Phase 2]` Als **Entwickler** möchte ich den KO-Modus implementiert haben (Unentschieden-Masse wird proportional zur Elo-Siegwahrscheinlichkeit auf Sieger-Tipps umverteilt), damit Elfmeterschießen-Spiele korrekt behandelt werden.

- **US-14** `[Phase 2]` Als **Nutzer** möchte ich im Output sehen, ob ein Tipp auf historischen Daten oder auf WM-Form basiert und wie viele WM-Spiele ein Team bereits gespielt hat, damit ich die Datengrundlage einschätzen kann.

---

## Sprint 3 — LLM-Erklärung

- **US-15** `[Phase 3]` Als **Nutzer** möchte ich auch ohne LLM einen Tipp bekommen (Fallback auf Poisson-Modell allein), damit die App immer funktioniert.

- **US-16** `[Phase 3]` Als **Nutzer** möchte ich eine verständliche Erklärung lesen, die klar unterscheidet zwischen: Modelldaten (Elo, WM-Form) und interpretativer Einschätzung (LLM), damit ich der Analyse vertrauen kann.

- **US-17** `[Phase 3]` Als **Product Owner** möchte ich dass das LLM den berechneten Tipp niemals überschreibt — es erklärt nur, damit der Expected-Points-Optimizer immer die finale Entscheidung trifft.

- **US-18** `[Phase 3]` Als **Product Owner** möchte ich optionale LLM-Metadaten (Verletzungen, Rotation, Motivation) als leichten kontrollierten Adjustment-Faktor (max. ±5%) einbauen können, damit qualitative Infos das Modell sinnvoll ergänzen.

---

## Sprint 4 — Web-App Frontend & Backend

- **US-19** `[Phase 4]` Als **Nutzer** möchte ich ein schlichtes Web-Formular haben (Team A, Team B, Spielphase), damit ich Tipps ohne Kommandozeile berechnen kann.

- **US-20** `[Phase 4]` Als **Nutzer** möchte ich den optimalen Tipp, E[pts], P(A/X/B), Top-3-Alternativen und die LLM-Erklärung übersichtlich dargestellt sehen.

- **US-21** `[Phase 4]` Als **Nutzer** möchte ich eine Sonderfragen-Übersicht sehen (alle 15 Fragen mit aktuellen Empfehlungen und Wahrscheinlichkeiten), damit ich die Sondertipps jederzeit abrufen kann.

- **US-22** `[Phase 4]` Als **Nutzer** möchte ich WM-Ergebnisse manuell eintragen können (einfaches Formular), damit das Bayesianische Updating ausgelöst wird ohne JSON-Dateien zu bearbeiten.

- **US-23** `[Phase 4]` Als **Nutzer** möchte ich einen Ladezustand sehen während die Simulation läuft, und eine sinnvolle Fehlermeldung wenn das Backend nicht erreichbar ist.

---

## Sprint 5 — Live-Daten-Anbindung

- **US-24** `[Phase 5]` Als **Entwickler** möchte ich einen Data-Service haben, der WM-Ergebnisse automatisch von einer Fußball-API abruft (nach Spielende), damit `wm_results.json` sich selbst aktuell hält.

- **US-25** `[Phase 5]` Als **Entwickler** möchte ich Caching implementiert haben (Matchdaten 15 Min, Elo/Ranking 24h), damit API-Limits geschont werden.

- **US-26** `[Phase 5]` Als **Nutzer** möchte ich im Frontend sehen welche Daten automatisch abgerufen wurden (Quelle, Zeitstempel), damit ich die Datenqualität einschätzen kann.

---

## Sprint 6 — Backtesting

- **US-27** `[Phase 6]` Als **Entwickler** möchte ich historische WM-Daten (2014, 2018, 2022) als Testdatensatz haben und den Backtest-Service implementieren, der simulierte Kicktipp-Punkte berechnet.

- **US-28** `[Phase 6]` Als **Product Owner** möchte ich `avg_kicktipp_pts` als Primärmetrik sehen (nicht nur 1X2-Accuracy), damit Modellverbesserungen am echten Spielziel gemessen werden.

- **US-29** `[Phase 6]` Als **Product Owner** möchte ich ein neues Modell nur dann zum Standard machen, wenn es im Backtest einen höheren `avg_kicktipp_pts` erzielt als das aktuelle, damit Änderungen datenbasiert entschieden werden.

---

## Sprint 7 — MCP-ready Refactoring *(Post-WM)*

- **US-30** `[Phase 7]` Als **Entwickler** möchte ich interne Tool-Interfaces definieren (Daten, Modell, Simulation), die austauschbar sind (JSON → API → MCP), damit das System langfristig erweiterbar bleibt.

- **US-31** `[Phase 7]` Als **Product Owner** möchte ich dass der Expected-Points-Optimizer immer im Code bleibt (nie im LLM/MCP), damit die Zielfunktion deterministisch und prüfbar ist.

- **US-00** `[E0/F-00]` Als **Entwickler** möchte ich ein laufendes React-Frontend und Express-Backend haben, die miteinander kommunizieren (hardcoded Response), damit der technische Stack bestätigt ist.

---

## Sprint 1 — Mockdaten & Datenmodell

- **US-01** `[E5/F-08]` Als **Entwickler** möchte ich lokale JSON-Mockdaten für Teams nutzen, damit die App ohne Live-API läuft.
- **US-02** `[E2/F-02]` Als **Entwickler** möchte ich aus Matchdaten Kennzahlen berechnen (Punkte/Spiel, Tore/Spiel, Form etc.), damit das Prognosemodell eine strukturierte Eingabe hat.
- **US-03** `[E2/F-02]` Als **Product Owner** möchte ich dass fehlende Daten als "dünn" markiert werden statt die App zum Absturz zu bringen, damit der Nutzer transparent informiert wird.

---

## Sprint 2 — Basismodell

- **US-04** `[E2/F-03]` Als **Product Owner** möchte ich dass der Basistipp bei gleichen Eingabedaten immer dasselbe Ergebnis liefert, damit die Vorhersage reproduzierbar und testbar ist.
- **US-05** `[E2/F-03]` Als **Nutzer** möchte ich Sieg/Unentschieden/Niederlage-Wahrscheinlichkeiten sehen, damit ich die Sicherheit der Prognose einschätzen kann.

---

## Sprint 3 — Eingabe & Validierung

- **US-06** `[E1/F-01]` Als **Nutzer** möchte ich Team A und Team B eingeben, damit ich eine Vorhersage für dieses Spiel bekomme.
- **US-07** `[E1/F-01]` Als **Nutzer** möchte ich eine Fehlermeldung sehen bei leerer oder identischer Eingabe, damit ich meinen Fehler korrigieren kann.
- **US-08** `[E1/F-01]` Als **Nutzer** möchte ich eine Tippstrategie wählen (konservativ/ausgewogen/mutig), damit ich den Tipp an meine Risikobereitschaft anpassen kann.

---

## Sprint 4 — Frontend UI

- **US-09** `[E6/F-10]` Als **Nutzer** möchte ich ein schlichtes Formular sehen mit Team-Eingabe, Strategie-Auswahl und Berechnen-Button.
- **US-10** `[E6/F-11]` Als **Nutzer** möchte ich Tipp, Wahrscheinlichkeiten, Erklärung und Unsicherheiten klar dargestellt sehen.
- **US-11** `[E6/F-11]` Als **Nutzer** möchte ich den Ladezustand sehen während die Berechnung läuft, damit ich weiß dass die App arbeitet.
- **US-12** `[E6/F-11]` Als **Nutzer** möchte ich eine sinnvolle Fehlermeldung sehen wenn das Backend nicht erreichbar ist.

---

## Sprint 5 — LLM-Erklärung

- **US-13** `[E4/F-06]` Als **Nutzer** möchte ich auch ohne LLM einen Tipp bekommen (Fallback auf deterministisches Modell), damit die App immer funktioniert.
- **US-14** `[E4/F-06]` Als **Nutzer** möchte ich eine verständliche Erklärung lesen die klar zwischen Datenfakten und Interpretation unterscheidet.

---

## Sprint 6 — Ensemble & Policy Engine

- **US-15** `[E3/F-04]` Als **Product Owner** möchte ich dass Basismodell (60%), Elo (30%) und LLM-Adjustment (10%) kombiniert werden, damit die Prognose mehrere Datenquellen berücksichtigt.
- **US-16** `[E3/F-04]` Als **Entwickler** möchte ich fehlende Modelle automatisch herausrechnen und Gewichte normalisieren, damit der Ensemble-Tipp auch bei unvollständigen Daten korrekt bleibt.
- **US-17** `[E3/F-05]` Als **Product Owner** möchte ich LLM-Anpassungen auf maximal ±0.05 pro Wahrscheinlichkeit begrenzen, damit das LLM den deterministischen Tipp nicht unkontrolliert überschreibt.
- **US-18** `[E3/F-05]` Als **Product Owner** möchte ich jede LLM-Anpassung validieren lassen bevor sie in den finalen Tipp einfließt, damit die Policy Engine die Kontrolle behält.

---

## Sprint 7 — Live-Daten

- **US-19** `[E5/F-09]` Als **Entwickler** möchte ich eine Fußball-API anbinden und Matchdaten normalisieren, damit das Modell echte Daten statt Mockdaten nutzt.
- **US-20** `[E5/F-09]` Als **Entwickler** möchte ich Daten cachen (Matchdaten 15 Min, Quoten 5 Min, Ranking 24h), damit API-Limits geschont und Antwortzeiten verbessert werden.

---

## Sprint 8 — LLM-Metadaten *(optional)*

- **US-21** `[E4/F-07]` Als **Product Owner** möchte ich dass das LLM Metadaten (Rotation, Verletzungen, Motivation) aus Texten extrahiert, damit diese kontrolliert in die Prognose einfließen können.
- **US-22** `[E4/F-07]` Als **Product Owner** möchte ich dass das LLM keine unbelegten Fakten als sicher darstellt, damit die Erklärung vertrauenswürdig bleibt.

---

## Sprint 9 — Backtesting *(Post-MVP)*

- **US-23** `[E7/F-12]` Als **Entwickler** möchte ich Modelle auf WM-Daten 2014–2022 testen und Metriken (1X2-Accuracy, Brier Score, Log Loss) vergleichen.
- **US-24** `[E7/F-12]` Als **Product Owner** möchte ich ein neues Modell nur dann zum Standard machen wenn es im Backtest besser abschneidet, damit Modellverbesserungen datenbasiert entschieden werden.
