# 11_epics_and_stories.md

## Rollen
- **Nutzer** — will einen guten, nachvollziehbaren Tipp sehen
- **Product Owner** — will Qualität, Determinismus und Transparenz sicherstellen
- **Entwickler** — will sauberen, testbaren, robusten Code

---

## Sprint 0 — Walking Skeleton

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
