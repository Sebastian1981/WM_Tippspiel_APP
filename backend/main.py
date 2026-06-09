"""
WM-Tippspiel FastAPI Backend
Endpunkte:
  GET  /api/health                    - Health-Check
  POST /api/predict                   - Einzelspiel-Tipp
  GET  /api/special-questions         - Alle Sonderfragen-Empfehlungen
  POST /api/results                   - WM-Ergebnis eintragen
  GET  /api/matchday/{day}            - Alle Tipps für einen Spieltag
"""
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.model.poisson import compute_lambdas, score_distribution, outcome_probabilities, adjust_for_ko
from src.model.bayesian_update import load_wm_results, get_effective_elo
from src.optimizer.expected_points import find_optimal_tip
from src.simulation.tournament import (
    simulate_tournament,
    compute_top_scorer_team,
    load_groups,
    load_elo,
)

app = FastAPI(title="WM-Tippspiel-Assistent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).parent / "src" / "data"


# ── Pydantic-Modelle ─────────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    team_a: str
    team_b: str
    match_phase: str = "group"  # "group" oder "ko"


class MatchResult(BaseModel):
    team_a: str
    team_b: str
    score_a: int
    score_b: int
    match_date: str = ""
    group: str = ""


# ── Hilfsfunktionen ──────────────────────────────────────────────────────────

def load_elo_ratings() -> dict[str, float]:
    with open(DATA_DIR / "elo_ratings.json", encoding="utf-8") as f:
        return json.load(f)


def load_schedule() -> dict:
    with open(DATA_DIR / "schedule.json", encoding="utf-8") as f:
        return json.load(f)


def save_wm_results(results: list[dict]) -> None:
    with open(DATA_DIR / "wm_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


# ── Endpunkte ────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "WM-Tippspiel-Assistent"}


@app.post("/api/predict")
def predict(req: PredictRequest):
    elo_ratings = load_elo_ratings()
    wm_results = load_wm_results()

    if req.team_a not in elo_ratings:
        raise HTTPException(status_code=404, detail=f"Team '{req.team_a}' nicht gefunden.")
    if req.team_b not in elo_ratings:
        raise HTTPException(status_code=404, detail=f"Team '{req.team_b}' nicht gefunden.")
    if req.team_a == req.team_b:
        raise HTTPException(status_code=400, detail="Team A und Team B dürfen nicht identisch sein.")

    # Effektive Stärke (mit WM-Form wenn vorhanden)
    elo_a = get_effective_elo(req.team_a, elo_ratings[req.team_a], wm_results)
    elo_b = get_effective_elo(req.team_b, elo_ratings[req.team_b], wm_results)

    lambda_a, lambda_b = compute_lambdas(elo_a, elo_b)
    dist = score_distribution(lambda_a, lambda_b)

    # KO-Modus: Unentschieden-Masse umverteilen
    if req.match_phase == "ko":
        dist = adjust_for_ko(dist, elo_a, elo_b)

    outcomes = outcome_probabilities(dist)
    tip = find_optimal_tip(dist)

    return {
        "team_a": req.team_a,
        "team_b": req.team_b,
        "match_phase": req.match_phase,
        "elo_a": round(elo_a, 1),
        "elo_b": round(elo_b, 1),
        "lambda_a": round(lambda_a, 3),
        "lambda_b": round(lambda_b, 3),
        "probabilities": {
            "team_a_win": round(outcomes["team_a_win"], 3),
            "draw": round(outcomes["draw"], 3),
            "team_b_win": round(outcomes["team_b_win"], 3),
        },
        "optimal_tip": tip["optimal_tip"],
        "expected_points": tip["expected_points"],
        "top_alternatives": tip["top_alternatives"],
        "data_sources": {
            "elo_prior": elo_ratings[req.team_a],
            "wm_games_a": len([r for r in wm_results if r["team_a"] == req.team_a or r["team_b"] == req.team_a]),
            "wm_games_b": len([r for r in wm_results if r["team_a"] == req.team_b or r["team_b"] == req.team_b]),
        },
    }


@app.get("/api/special-questions")
def special_questions(simulations: int = 30000):
    elo = load_elo()
    groups = load_groups()

    sim_result = simulate_tournament(elo, groups, n_simulations=simulations, seed=42)

    sf_probs = {t: sim_result["semifinal_probabilities"].get(t, 0) for t in elo}
    wc_probs = {t: sim_result["world_champion_probabilities"].get(t, 0) for t in elo}
    top_scorer = compute_top_scorer_team(elo, sf_probs, wc_probs)

    return {
        "simulations": simulations,
        "group_winners": {
            grp: {
                "recommendation": sim_result["group_recommendations"][grp],
                "probabilities": sorted(
                    [{"team": t, "probability": p} for t, p in probs.items()],
                    key=lambda x: x["probability"],
                    reverse=True,
                ),
            }
            for grp, probs in sim_result["group_winner_probabilities"].items()
        },
        "semifinalists": {
            "recommendations": sim_result["semifinal_recommendations"],
            "probabilities": [
                {"team": t, "probability": p}
                for t, p in sim_result["semifinal_probabilities"].items()
            ],
        },
        "world_champion": {
            "recommendation": sim_result["world_champion_recommendation"],
            "probabilities": [
                {"team": t, "probability": p}
                for t, p in sim_result["world_champion_probabilities"].items()
            ],
        },
        "top_scorer_team": top_scorer,
    }


@app.get("/api/matchday/{day}")
def matchday_tips(day: int):
    if day not in (1, 2, 3):
        raise HTTPException(status_code=400, detail="Spieltag muss 1, 2 oder 3 sein.")

    schedule = load_schedule()
    key = f"matchday_{day}"
    matches = schedule.get(key, [])

    if not matches:
        return {"matchday": day, "tips": [], "message": "Noch keine Spiele eingetragen."}

    elo_ratings = load_elo_ratings()
    wm_results = load_wm_results()
    tips = []

    for match in matches:
        team_a = match["team_a"]
        team_b = match["team_b"]

        elo_a = get_effective_elo(team_a, elo_ratings[team_a], wm_results)
        elo_b = get_effective_elo(team_b, elo_ratings[team_b], wm_results)
        lambda_a, lambda_b = compute_lambdas(elo_a, elo_b)
        dist = score_distribution(lambda_a, lambda_b)
        outcomes = outcome_probabilities(dist)
        tip = find_optimal_tip(dist)

        tips.append({
            "date": match["date"],
            "team_a": team_a,
            "team_b": team_b,
            "group": match.get("group", ""),
            "optimal_tip": tip["optimal_tip"],
            "expected_points": tip["expected_points"],
            "probabilities": {
                "team_a_win": round(outcomes["team_a_win"], 3),
                "draw": round(outcomes["draw"], 3),
                "team_b_win": round(outcomes["team_b_win"], 3),
            },
        })

    return {"matchday": day, "tips": tips}


@app.post("/api/results")
def add_result(result: MatchResult):
    results = load_wm_results()
    results.append(result.model_dump())
    save_wm_results(results)
    return {"status": "ok", "total_results": len(results)}


@app.get("/api/results")
def get_results():
    return load_wm_results()
