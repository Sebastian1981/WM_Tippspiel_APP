"""
Bayesianisches Updating der Teamstärke mit WM-Form.
Je mehr WM-Spiele ein Team gespielt hat, desto stärker gewichtet die WM-Form.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# α-Gewichtung: WM-Form vs. historischer Elo-Prior
ALPHA_TABLE = {0: 0.0, 1: 0.40, 2: 0.65}
ALPHA_DEFAULT = 0.85  # ab 3 Spielen


def load_wm_results() -> list[dict]:
    path = DATA_DIR / "wm_results.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_alpha(games_played: int) -> float:
    return ALPHA_TABLE.get(games_played, ALPHA_DEFAULT)


def compute_wm_form_score(team: str, results: list[dict]) -> tuple[float, int]:
    """
    Berechnet WM-Form-Score und Anzahl gespielter WM-Spiele für ein Team.
    Score basiert auf Punkte/Spiel, Tordifferenz/Spiel, Tore/Spiel.
    Gibt (form_score, games_played) zurück.
    """
    team_results = [r for r in results if r["team_a"] == team or r["team_b"] == team]
    games = len(team_results)
    if games == 0:
        return 0.0, 0

    points = 0
    goals_for = 0
    goals_against = 0

    for r in team_results:
        if r["team_a"] == team:
            gf, ga = r["score_a"], r["score_b"]
        else:
            gf, ga = r["score_b"], r["score_a"]

        goals_for += gf
        goals_against += ga
        if gf > ga:
            points += 3
        elif gf == ga:
            points += 1

    ppg = points / games
    gf_pg = goals_for / games
    ga_pg = goals_against / games
    gd_pg = (goals_for - goals_against) / games

    # Gleiche Gewichtung wie Elo-Modell (normalisiert auf Elo-Skala)
    form_score = (
        0.35 * ppg
        + 0.25 * gd_pg
        + 0.20 * gf_pg
        - 0.20 * ga_pg
    )
    return form_score, games


def get_effective_elo(team: str, elo: float, results: list[dict]) -> float:
    """
    Kombiniert historischen Elo-Prior mit WM-Form.
    Gibt effektive Teamstärke in Elo-Skala zurück.
    """
    form_score, games = compute_wm_form_score(team, results)
    alpha = get_alpha(games)
    if alpha == 0.0:
        return elo

    # WM-Form auf Elo-Skala mappen (empirisch: 1 Pkt/Spiel ≈ 100 Elo)
    form_elo = 1500 + form_score * 200
    effective = (1 - alpha) * elo + alpha * form_elo
    return effective
