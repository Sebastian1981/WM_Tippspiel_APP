# 00_product_vision.md

## Produktname
WM-Tippspiel-Assistent

## Ziel
Die App soll einem Nutzer helfen, für ein WM-Tippspiel bessere und nachvollziehbare Tipps abzugeben. Der Nutzer gibt zwei Länder ein, die gegeneinander spielen. Die App recherchiert beziehungsweise lädt aktuelle Fußball-Daten, berechnet eine datenbasierte Prognose und erzeugt daraus einen empfohlenen Ergebnistipp mit Erklärung.

## Kernidee
Die App kombiniert:

1. deterministische Fußballmodelle,
2. aktuelle Online-Daten,
3. optional Buchmacherquoten,
4. LLM-basierte Metadatenanalyse,
5. eine kontrollierte Ensemble-Logik.

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

Die App optimiert zunächst nicht auf Wettquoten oder Expected Value, sondern auf Tippspiel-Trefferwahrscheinlichkeit.

Die App soll im MVP lokal laufen.

## Erfolgsdefinition
Der MVP ist erfolgreich, wenn:

1. der Nutzer zwei Teams eingeben kann,
2. das Backend aktuelle oder gespeicherte Matchdaten verarbeitet,
3. ein deterministisches Modell einen Tipp berechnet,
4. ein LLM eine Erklärung erzeugt,
5. die finale Empfehlung nachvollziehbar dargestellt wird,
6. spätere Backtests möglich sind.
