# WM-Tippspiel-Assistent

A data-driven assistant that helps you maximise your score in a **Kicktipp** World Cup prediction game (2–4 point tournament rules).

---

## Project Goal

Most prediction-game participants simply tip the most *likely* scoreline. This app goes one step further: it calculates the scoreline that **maximises your expected Kicktipp points** — which is not always the same as the most probable result.

Given two competing teams, the app:

1. Computes a full probability distribution over all possible scorelines using a Poisson model driven by Elo ratings.
2. Applies Bayesian updating so that actual World Cup results progressively override the historical Elo prior.
3. Evaluates every possible tip (0:0 – 5:5, i.e. 36 candidate scorelines) against the Kicktipp scoring function and selects the tip with the highest **Expected Points (E[pts])**.
4. Runs a Monte Carlo tournament simulation to recommend answers to the special questions (group winners, semi-finalists, World Champion, top-scorer team).
5. Uses an LLM to structure contextual metadata (injuries, suspensions, motivation, etc.) and generate a human-readable explanation — without ever allowing the LLM to override the deterministic model output.

---

## Business Logic

### Kicktipp Scoring Rules (2–4 Points, Tournament Mode)

| Situation | Points |
|---|---|
| Exact scoreline correct | **4** |
| Correct goal difference (non-draw) | **3** |
| Correct tendency (win/draw/loss) | **2** |
| Wrong tendency | **0** |

> For draws, the goal-difference tier is skipped (goal difference is always 0).  
> All World Cup matches are played on neutral ground, so there is no home/away distinction.  
> Knockout-round tips must reflect the result *after penalties* if applicable.

### Expected-Points Optimiser

The optimal tip is computed as:

```
E[pts(a,b)] = Σ_{i,j} P(i,j) · pts(a,b,i,j)

Optimal tip = argmax_{(a,b)} E[pts(a,b)]   with a,b ∈ {0…5}
```

Because the scoring function is non-linear, the argmax of E[pts] frequently differs from the mode of P(i,j).

### Poisson Model

Goal expectations are derived from Elo ratings:

```
BASE  = 1.35   # average international goals per team per game
SCALE = 600    # Elo scaling factor

lambda_A = max(0.25,  BASE + (elo_A - elo_B) / SCALE)
lambda_B = max(0.25,  BASE - (elo_A - elo_B) / SCALE)

P(i,j) = Poisson(i; lambda_A) · Poisson(j; lambda_B)   [normalised to 0:0 – 7:7]
```

### Bayesian Updating (World Cup Form)

Once matches are played, the historical Elo prior is progressively replaced by observed World Cup form:

```
effective_strength = α · wm_form_score + (1 − α) · elo_prior

α schedule:
  0 WC matches played  →  α = 0.00
  1 WC match played    →  α = 0.40
  2 WC matches played  →  α = 0.65
  3+ WC matches played →  α = 0.85
```

### Knockout Mode

In knockout rounds, draw probability mass is redistributed proportionally onto win tips using the Elo-based win probability:

```
P_elo(A wins) = 1 / (1 + 10^((elo_B − elo_A) / 400))
```

### Tournament Simulation (Monte Carlo)

For special questions (group winners, semi-finalists, World Champion, top-scorer team), a Monte Carlo simulation runs **30,000–50,000 iterations** of the entire tournament. This range balances convergence accuracy (standard error < 0.5 % for typical win probabilities) with acceptable runtime on a local machine. The Poisson model is used for group-stage games and Elo win probabilities for knockout games.

### Ensemble & Policy Engine

The final recommendation is built from a weighted ensemble:

| Model component | Default weight |
|---|---|
| Base model / WC form | 60 % |
| Elo / ranking model | 30 % |
| LLM metadata adjustment | 10 % |

The **Policy Engine** enforces guardrails: the LLM may only suggest minor adjustments and may never freely override the deterministic tip.

---

## Architecture

### MVP Data Flow

```
React Frontend
      │
      ▼
Express API  (/api/predict, /api/special-questions)
      │
      ▼
Prediction Orchestrator
      │
      ├─► Data Service          (Elo ratings + WC results, optional betting odds)
      │
      ├─► Feature Engineering   (goals, points, form sequence per team)
      │
      ├─► Poisson Model         (lambda_A, lambda_B → P(i,j))
      │
      ├─► Expected-Points Optimizer   (argmax over 36 tips)
      │
      ├─► Tournament Simulator  (Monte Carlo for special questions)
      │
      ├─► LLM Explanation Service     (structured prompt → explanation JSON)
      │
      └─► Policy / Ensemble Engine    (validates LLM adjustments, combines models)
            │
            ▼
      Structured JSON Response → Frontend
```

### Future MCP-Ready Architecture

The internal tool interfaces (data fetch, model, simulation) are designed to be replaceable. A future version will expose them as **MCP (Model Context Protocol) tools**, allowing external agents or search tools to be plugged in without changing the core prediction logic.

```
React Frontend
      │
      ▼
Express API
      │
      ▼
Prediction Orchestrator
      │
      ▼
MCP Tool Layer  (data sources, local tools, search tools)
      │
      ▼
Prediction Engine  →  Policy Engine  →  LLM Explanation
```

### Key Architectural Decision

> **The objective function is always: maximise E[Kicktipp points] — not P(most likely scoreline).**

The LLM is strictly an *explanation and metadata-extraction* layer. It receives structured model output and returns a human-readable summary. It does **not** determine or override the final tip.

### Component Responsibilities

| Component | Responsibility |
|---|---|
| **Frontend** (React) | Team input, strategy selection, tip display, LLM explanation, uncertainty indicator |
| **Backend** (Node/Express) | Input validation, data fetching, prediction orchestration, structured JSON response |
| **Data Service** | Match data, team data, optional betting odds and news; in-memory/file cache fallback |
| **Prediction Engine** | Poisson model, Bayesian update, score distribution, Expected-Points optimiser, KO mode, Monte Carlo simulation |
| **Policy / Ensemble Engine** | Combine model outputs, enforce LLM guardrails, validate tip adjustments |
| **LLM Service** | Extract metadata from text (injuries, suspensions, motivation, weather …), generate explanation |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Backend API | Node.js / Express |
| Core Prediction | Python (`numpy`, `scipy`) |
| LLM Integration | OpenAI / Anthropic API |
| Simulation | Monte Carlo (Python) |

---

## Implementation Phases

| Phase | Title | Goal |
|---|---|---|
| 0 | Quick-Tip Script | Single Python script with hardcoded Elo ratings for all 48 teams (2026 expanded format), all tips for matchday 1 |
| 1 | Python Core MVP | Modular package: `model/`, `optimizer/`, `simulation/`, `data/` |
| 2 | Bayesian Updating | WC results feed into the model after each matchday |
| 3 | LLM Explanation | Explainable tips via LLM, without overriding the model |
| 4 | Web App | React + Express UI for daily use during the tournament |
| 5 | Live Data | Automatic result and Elo-rating ingestion via football API |
| 6 | Backtesting | Validate model on WC 2014, 2018, 2022 data |
| 7 | MCP Refactoring | Replace internal adapters with MCP tool interfaces |

---

## MVP Success Criteria

The MVP is considered successful when:

1. A user can enter two team names.
2. The backend processes Elo ratings and WC match results.
3. The Poisson model produces a complete score distribution P(i,j).
4. The Expected-Points optimiser selects the point-optimal tip under the Kicktipp rules.
5. A Monte Carlo tournament simulation provides recommendations for all special questions.
6. The LLM generates a coherent, verifiable explanation.
7. The final recommendation is presented transparently (tip, E[pts], win/draw/loss probabilities, explanation, confidence, risk note).
8. The system supports post-tournament backtesting.

---

## Project Structure (Target — Phase 1+)

```
WM_Tippspiel_APP/
├── src/
│   ├── model/
│   │   ├── poisson.py            # Poisson model (Elo input)
│   │   └── bayesian_update.py    # α-weighted WC form update
│   ├── optimizer/
│   │   └── expected_points.py    # Expected-Points optimiser + scoring function
│   ├── simulation/
│   │   └── tournament.py         # Monte Carlo tournament simulation
│   └── data/
│       ├── elo_ratings.json      # Elo ratings for all 48 teams (FIFA 2026 expanded format)
│       ├── groups.json           # Group assignments
│       └── wm_results.json       # Live WC results (updated each matchday)
├── main.py                       # CLI entry point
├── specs/                        # Detailed specification documents
└── README.md
```

---

## Disclaimer

This app is designed for private use in a Kicktipp prediction game. It does not constitute professional betting software, and it provides no guarantee of results. All tips should be manually reviewed before submission.
