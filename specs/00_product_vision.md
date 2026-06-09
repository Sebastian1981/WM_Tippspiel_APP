# 00_product_vision.md

## Produktname
WM-Tippspiel-Assistent

## Ziel
Die App soll einem Nutzer helfen, in einem WM-Tippspiel (Kicktipp, 2–4 Punkte Turnier-Regel) die **maximale Punktzahl** zu erzielen. Der Nutzer gibt zwei Länder ein, die gegeneinander spielen. Die App berechnet eine Wahrscheinlichkeitsverteilung über alle möglichen Spielergebnisse und wählt den Tipp mit dem **höchsten erwarteten Punkteertrag (Expected Points)** gemäß dem konkreten Kicktipp-Regelwerk.

## Kernidee
Die App kombiniert:

1. probabilistische Fußballmodelle (Poisson-Modell auf Basis von Elo-Ratings),
2. aktuelle WM-interne Ergebnisdaten (Bayesianisches Updating: WM-Form überschreibt historischen Prior),
3. optional Buchmacherquoten,
4. LLM-basierte Metadatenanalyse,
5. eine Expected-Points-Optimierungslogik (nicht einfache Wahrscheinlichkeitsmaximierung),
6. eine Monte-Carlo-Turniersimulation für Sonderfragen.

Das LLM darf Informationen strukturieren und erklären, aber nicht unkontrolliert den finalen Tipp überschreiben.

## Zielnutzer
Ein privater Nutzer, der an einem WM-Tippspiel teilnimmt und bessere, datenbasierte Tipps abgeben möchte.

## Primärer Use Case
Der Nutzer gibt ein:

- Team A
- Team B
- optional Spielphase
- optional Tippstrategie: konservativ, ausgewogen, mutig

Die App gibt zurück:

- Basismodell-Tipp
- Ensemble-Tipp
- empfohlener Tippspiel-Tipp
- Sieg-/Unentschieden-/Niederlage-Wahrscheinlichkeiten
- Erklärung der wichtigsten Gründe
- Unsicherheitsbewertung

## Nicht-Ziele im MVP
Die App ist im MVP keine professionelle Wettsoftware.

Die App gibt keine Garantie für Ergebnisse.

Die App optimiert **nicht** auf Wettquoten oder Wett-Expected-Value, sondern auf **Kicktipp-Punktemaximierung**.

Die App soll im MVP lokal laufen.

Die App ersetzt im MVP keine manuelle Prüfung der Tipps durch den Nutzer.

## Erfolgsdefinition
Der MVP ist erfolgreich, wenn:

1. der Nutzer zwei Teams eingeben kann,
2. das Backend Elo-Ratings und WM-Ergebnisse verarbeitet,
3. ein Poisson-Modell eine vollständige Score-Wahrscheinlichkeitsverteilung P(i:j) berechnet,
4. ein Expected-Points-Optimierer den punkteoptimalen Tipp gemäß Kicktipp-Regelwerk auswählt,
5. eine Monte-Carlo-Turniersimulation Gruppensieger, Halbfinalisten und Weltmeister-Tipps liefert,
6. ein LLM eine Erklärung erzeugt,
7. die finale Empfehlung nachvollziehbar dargestellt wird,
8. spätere Backtests möglich sind.
