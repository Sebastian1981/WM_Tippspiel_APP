# 06_data_sources.md

## Ziel
Die App soll Online-Daten verwenden können, aber auch mit Cache oder Mockdaten lauffähig bleiben.

---

## WM 2026 – Turnierdaten (hardcoded, Stand 09.06.2026)

### Gruppen und Teams

| Gruppe | Teams |
|---|---|
| A | Mexiko, Südkorea, Tschechien, Südafrika |
| B | Schweiz, Kanada, Bosnien, Katar |
| C | Brasilien, Marokko, Schottland, Haiti |
| D | Türkei, Paraguay, Australien, USA |
| E | Ecuador, Deutschland, Elfenbeinküste, Curaçao |
| F | Niederlande, Japan, Schweden, Tunesien |
| G | Belgien, Iran, Ägypten, Neuseeland |
| H | Spanien, Uruguay, Kap Verde, Saudi-Arabien |
| I | Frankreich, Norwegen, Senegal, Irak |
| J | Argentinien, Österreich, Algerien, Jordanien |
| K | Portugal, Kolumbien, Usbekistan, DR Kongo |
| L | England, Kroatien, Panama, Ghana |

### Elo-Ratings (World Football Elo, Stand 09.06.2026)

```json
{
  "Mexiko": 1875, "Südkorea": 1758, "Tschechien": 1740, "Südafrika": 1518,
  "Schweiz": 1891, "Kanada": 1788, "Bosnien": 1595, "Katar": 1423,
  "Brasilien": 1991, "Marokko": 1827, "Schottland": 1782, "Haiti": 1554,
  "Türkei": 1911, "Paraguay": 1833, "Australien": 1777, "USA": 1726,
  "Ecuador": 1938, "Deutschland": 1932, "Elfenbeinküste": 1695, "Curaçao": 1433,
  "Niederlande": 1948, "Japan": 1906, "Schweden": 1712, "Tunesien": 1628,
  "Belgien": 1893, "Iran": 1772, "Ägypten": 1696, "Neuseeland": 1563,
  "Spanien": 2157, "Uruguay": 1892, "Kap Verde": 1576, "Saudi-Arabien": 1566,
  "Frankreich": 2063, "Norwegen": 1914, "Senegal": 1867, "Irak": 1618,
  "Argentinien": 2114, "Österreich": 1830, "Algerien": 1760, "Jordanien": 1680,
  "Portugal": 1986, "Kolumbien": 1982, "Usbekistan": 1714, "DR Kongo": 1661,
  "England": 2021, "Kroatien": 1911, "Panama": 1730, "Ghana": 1510
}
```

### Spielplan Spieltag 1

| Datum | Team A | Team B |
|---|---|---|
| 11.06.2026 21:00 | Mexiko | Südafrika |
| 12.06.2026 04:00 | Südkorea | Tschechien |
| 12.06.2026 21:00 | Kanada | Bosnien |
| 13.06.2026 03:00 | USA | Paraguay |
| 13.06.2026 21:00 | Katar | Schweiz |
| 14.06.2026 00:00 | Brasilien | Marokko |
| 14.06.2026 03:00 | Haiti | Schottland |
| 14.06.2026 06:00 | Australien | Türkei |

### Spielplan Spieltag 2

| Datum | Team A | Team B | Gruppe |
|---|---|---|---|
| 14.06.2026 19:00 | Deutschland | Curaçao | E |
| 14.06.2026 22:00 | Niederlande | Japan | F |
| 15.06.2026 01:00 | Elfenbeinküste | Ecuador | E |
| 15.06.2026 04:00 | Schweden | Tunesien | F |
| 15.06.2026 18:00 | Spanien | Kap Verde | H |
| 15.06.2026 21:00 | Belgien | Ägypten | G |
| 16.06.2026 00:00 | Saudi-Arabien | Uruguay | H |
| 16.06.2026 03:00 | Iran | Neuseeland | G |

### Spielplan Spieltag 3

| Datum | Team A | Team B | Gruppe |
|---|---|---|---|
| 16.06.2026 21:00 | Frankreich | Senegal | I |
| 17.06.2026 00:00 | Irak | Norwegen | I |
| 17.06.2026 03:00 | Argentinien | Algerien | J |
| 17.06.2026 06:00 | Österreich | Jordanien | J |
| 17.06.2026 19:00 | Portugal | DR Kongo | K |
| 17.06.2026 22:00 | England | Kroatien | L |
| 18.06.2026 01:00 | Ghana | Panama | L |
| 18.06.2026 04:00 | Usbekistan | Kolumbien | K |

---

## Datenquellen-Typen

### Matchdaten

Benötigt:

- bisherige WM-Spiele
- Tore
- Gegentore
- Datum
- Turnierphase
- Teamnamen

### Ranking-/Elo-Daten

Optional:

- FIFA-Ranking
- Elo-Rating
- historische Teamstärke

### Quoten

Optional:

- Sieg Team A
- Unentschieden
- Sieg Team B
- Zeitpunkt der Quote
- Anbieter

### News/Metadaten

Optional:

- Verletzungen
- Sperren
- Rotation
- Motivation
- bereits qualifiziert
- Trainer-Aussagen

## MVP-Datenstrategie

**Phase 1:**

- Lokale Mockdaten
- Manuelle JSON-Daten
- Keine Pflicht zur Live-API

**Phase 2:**

- Fußball-API anbinden

**Phase 3:**

- Quoten-API anbinden

**Phase 4:**

- News-/Metadaten-Recherche ergänzen

## Cache-Regeln

Das Backend SOLL Daten cachen.

Empfehlung:

| Datentyp   | Cache-Dauer |
|------------|-------------|
| Matchdaten | 15 Minuten  |
| Quoten     | 5 Minuten   |
| News       | 30 Minuten  |
| Ranking    | 24 Stunden  |

## Datenqualitätsbewertung

Jede Vorhersage MUSS eine Datenqualitätsbewertung enthalten:

```json
{
  "matchDataAvailable": true,
  "oddsAvailable": false,
  "metadataAvailable": false,
  "sampleSize": "low",
  "warnings": [
    "Only two tournament matches available."
  ]
}
```
