# 08_ui_spec.md

## Ziel
Das Frontend soll einfach, lokal und verständlich sein.

## Hauptscreen

Elemente:

- Titel: WM-Tippspiel-Assistent
- Eingabe Team A
- Eingabe Team B
- Auswahl Tippstrategie
- Checkbox: Metadaten verwenden
- Checkbox: Quoten verwenden
- Button: Tipp berechnen

## Ergebnisanzeige

Die Ergebnisanzeige enthält:

1. Empfohlener Tipp
2. Wahrscheinlichkeiten
3. Basismodell-Tipp
4. Ensemble-Tipp
5. Erklärung
6. Unsicherheiten
7. Datenqualität

## Beispielanzeige

```
Empfohlener Tipp:
Deutschland 2:1 Brasilien

Wahrscheinlichkeiten:
Deutschland-Sieg: 45 %
Unentschieden: 29 %
Brasilien-Sieg: 26 %

Warum?
Deutschland hat bisher mehr Punkte pro Spiel, die bessere Tordifferenz und weniger Gegentore.

Unsicherheit:
Die Datenlage ist dünn, da erst drei Turnierspiele vorliegen.
```

## UI-Zustände

Die UI MUSS folgende Zustände unterstützen:

- leer
- lädt
- Ergebnis vorhanden
- Fehler
- keine Daten
- LLM nicht verfügbar

## MVP-Design

Schlichtes Card-Layout.

Keine komplexen Charts im MVP.

Später möglich:

- Balkendiagramm für Wahrscheinlichkeiten
- Feature-Vergleich Team A vs Team B
- Backtest-Dashboard
- Tipp-Historie
