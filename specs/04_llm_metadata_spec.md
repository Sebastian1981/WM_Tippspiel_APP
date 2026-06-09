# 04_llm_metadata_spec.md

## Ziel
Das LLM soll keine freie Prognosemaschine sein. Es soll unstrukturierte Informationen interpretieren und daraus kontrollierte Metadaten ableiten.

## Aufgaben des LLM

Das LLM darf:

- aktuelle Spielberichte zusammenfassen
- Metadaten extrahieren
- Risiken benennen
- Prognosen erklären
- leichte Anpassungen vorschlagen

Das LLM darf nicht:

- finale Tipps unkontrolliert überschreiben
- erfundene Verletzungen nennen
- nicht belegte Nachrichten als Fakt darstellen
- Buchmacherquoten ignorieren, wenn sie verfügbar sind
- extreme Tipps ohne starke Evidenz erzeugen

## Input für Metadatenextraktion

```json
{
  "teamA": "Germany",
  "teamB": "Brazil",
  "articles": [
    {
      "source": "example",
      "title": "Germany may rotate squad",
      "text": "..."
    }
  ]
}
```

## LLM-Output für Metadaten

```json
{
  "metadataSignals": [
    {
      "type": "rotation",
      "team": "Germany",
      "direction": "negative",
      "strength": "medium",
      "evidence": "Article suggests several starters may be rested.",
      "confidence": "medium"
    }
  ],
  "overallAdjustmentSuggestion": {
    "teamAWinDelta": -0.03,
    "drawDelta": 0.02,
    "teamBWinDelta": 0.01,
    "reason": "Possible rotation reduces Team A advantage slightly."
  },
  "riskNotes": [
    "The rotation information is not confirmed."
  ]
}
```

## Maximal erlaubte Adjustments

Im MVP darf das LLM Wahrscheinlichkeiten nur gering verändern:

```
max absolute delta per outcome = 0.05
```

Beispiel erlaubt:

```json
{
  "teamAWinDelta": -0.03,
  "drawDelta": 0.02,
  "teamBWinDelta": 0.01
}
```

Nicht erlaubt:

```json
{
  "teamAWinDelta": -0.20,
  "drawDelta": 0.05,
  "teamBWinDelta": 0.15
}
```

## Erklärungsprompt

Das LLM erhält vom Backend:

```json
{
  "match": "Germany vs Brazil",
  "baselinePrediction": {},
  "ensemblePrediction": {},
  "metadataSignals": [],
  "dataQuality": {}
}
```

Das LLM soll ausgeben:

```json
{
  "shortSummary": "...",
  "mainReasons": ["...", "..."],
  "mainUncertainties": ["...", "..."],
  "conservativeTip": "1:1",
  "balancedTip": "2:1",
  "boldTip": "3:1",
  "recommendedTip": "2:1",
  "explanation": "..."
}
```

## Prompt-Regeln

Der Prompt MUSS enthalten:

```
Du bist ein nüchterner Fußballanalyst für ein Tippspiel.

Nutze ausschließlich die gelieferten strukturierten Daten und klar gekennzeichnete Metadaten.

Erfinde keine Verletzungen, keine Aufstellungen und keine aktuellen Nachrichten.

Wenn die Datenlage dünn ist, sage das ausdrücklich.

Unterscheide zwischen:
- Datenfakten
- Modellinterpretation
- Unsicherheit

Antworte ausschließlich als valides JSON.
```
