# 09_non_functional_requirements.md

## Lokal lauffähig
Die App MUSS lokal laufen.

```
Frontend: localhost:5173
Backend:  localhost:3001
```

## API-Key-Sicherheit
API-Keys DÜRFEN NICHT im Frontend liegen.

Alle API-Keys liegen im Backend in `.env`.

## Robustheit
Die App MUSS auch dann funktionieren, wenn:

- LLM nicht erreichbar ist
- externe Fußball-API nicht erreichbar ist
- keine Quoten verfügbar sind
- keine News verfügbar sind

In solchen Fällen muss das System auf verfügbare Daten zurückfallen.

## Reproduzierbarkeit
Der deterministische Basistipp MUSS bei gleichen Daten identisch bleiben.

LLM-Ausgaben können variieren, dürfen aber den finalen Tipp nicht unkontrolliert überschreiben.

## Testbarkeit
Jeder Service SOLL isoliert testbar sein.

Mindesttests:

- Feature-Berechnung
- Basismodell
- Tipp-Regeln
- Policy-Validierung
- API-Response-Format

## Transparenz
Die App MUSS anzeigen:

- welche Daten genutzt wurden
- welche Modelle genutzt wurden
- ob Metadaten genutzt wurden
- ob Quoten genutzt wurden
- wie sicher die Prognose ist

## Datenschutz
Im MVP werden keine personenbezogenen Daten gespeichert.

## Performance
Eine Vorhersage SOLL im Normalfall unter 10 Sekunden zurückkommen.

Bei LLM- oder News-Nutzung darf es länger dauern, aber die UI muss einen Ladezustand anzeigen.
