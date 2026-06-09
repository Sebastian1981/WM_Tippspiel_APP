"""
Monte-Carlo Turniersimulation für WM 2026.
Simuliert Gruppenphase und KO-Runden für Sonderfragen-Empfehlungen.
"""
import json
import random
import numpy as np
from collections import defaultdict
from pathlib import Path

from src.model.poisson import compute_lambdas

DATA_DIR = Path(__file__).parent.parent / "data"


def load_groups() -> dict[str, list[str]]:
    with open(DATA_DIR / "groups.json", encoding="utf-8") as f:
        return json.load(f)


def load_elo() -> dict[str, float]:
    with open(DATA_DIR / "elo_ratings.json", encoding="utf-8") as f:
        return json.load(f)


def sim_match_goals(elo_a: float, elo_b: float) -> tuple[int, int]:
    """Simuliert ein Spiel mit Poisson-Modell, gibt Tore zurück."""
    la, lb = compute_lambdas(elo_a, elo_b)
    return int(np.random.poisson(la)), int(np.random.poisson(lb))


def ko_winner(team_a: str, team_b: str, elo: dict[str, float]) -> str:
    """KO-Spiel: Sieger via Elo-Wahrscheinlichkeit (inkl. Elfmeter)."""
    p_a = 1 / (1 + 10 ** ((elo[team_b] - elo[team_a]) / 400))
    return team_a if random.random() < p_a else team_b


def simulate_group(
    teams: list[str], elo: dict[str, float]
) -> list[tuple[str, int, int, int]]:
    """
    Simuliert alle Gruppenspiele, gibt Rankings zurück.
    Rückgabe: Liste (team, punkte, tordiff, tore) absteigend sortiert.
    """
    points = defaultdict(int)
    gd = defaultdict(int)
    gf = defaultdict(int)

    for i, a in enumerate(teams):
        for b in teams[i + 1:]:
            ga, gb = sim_match_goals(elo[a], elo[b])
            gf[a] += ga
            gf[b] += gb
            gd[a] += ga - gb
            gd[b] += gb - ga
            if ga > gb:
                points[a] += 3
            elif ga == gb:
                points[a] += 1
                points[b] += 1
            else:
                points[b] += 3

    ranked = sorted(
        teams,
        key=lambda t: (points[t], gd[t], gf[t]),
        reverse=True,
    )
    return [(t, points[t], gd[t], gf[t]) for t in ranked]


def simulate_tournament(
    elo: dict[str, float],
    groups: dict[str, list[str]],
    n_simulations: int = 30000,
    seed: int | None = None,
) -> dict:
    """
    Führt n_simulations Monte-Carlo-Simulationen durch.
    Gibt Wahrscheinlichkeiten für Gruppensieger, Halbfinale, Weltmeister zurück.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    group_winner_count: dict[str, dict[str, int]] = {g: defaultdict(int) for g in groups}
    semifinal_count: dict[str, int] = defaultdict(int)
    winner_count: dict[str, int] = defaultdict(int)

    for _ in range(n_simulations):
        group_ranked: dict[str, list[str]] = {}
        third_place_teams: list[tuple[int, int, int, str]] = []

        # Gruppenphase simulieren
        for grp, teams in groups.items():
            ranked = simulate_group(teams, elo)
            group_ranked[grp] = [t for t, _, _, _ in ranked]
            group_winner_count[grp][group_ranked[grp][0]] += 1
            # Drittplatzierte sammeln für Best-of-8
            _, pts, gd_val, gf_val = ranked[2]
            third_place_teams.append((pts, gd_val, gf_val, group_ranked[grp][2]))

        # Beste 8 Drittplatzierten ermitteln
        third_place_teams.sort(reverse=True)
        best_third = [t for _, _, _, t in third_place_teams[:8]]

        # KO-Feld aufbauen: 2 Erste + 2 Zweite pro Gruppe + 8 Dritte = 32 Teams
        ko_field = []
        for grp in groups:
            ko_field.append(group_ranked[grp][0])
            ko_field.append(group_ranked[grp][1])
        ko_field.extend(best_third)

        # KO-Runden
        random.shuffle(ko_field)
        current_round = ko_field
        round_num = 0

        while len(current_round) > 1:
            next_round = []
            for i in range(0, len(current_round), 2):
                winner = ko_winner(current_round[i], current_round[i + 1], elo)
                next_round.append(winner)

            round_num += 1
            # Halbfinalisten = Teams die ins Halbfinale kommen (4 Teams übrig → QF-Sieger)
            if len(next_round) == 4:
                for t in next_round:
                    semifinal_count[t] += 1

            current_round = next_round

        winner_count[current_round[0]] += 1

    # Wahrscheinlichkeiten berechnen
    group_probs = {
        grp: {
            team: round(count / n_simulations, 4)
            for team, count in counts.items()
        }
        for grp, counts in group_winner_count.items()
    }

    # Gruppensieger-Empfehlung: höchste Wahrscheinlichkeit pro Gruppe
    group_recommendations = {
        grp: max(probs, key=probs.get)
        for grp, probs in group_probs.items()
    }

    semifinal_probs = {
        t: round(semifinal_count[t] / n_simulations, 4)
        for t in elo
    }
    winner_probs = {
        t: round(winner_count[t] / n_simulations, 4)
        for t in elo
    }

    # Top-4 Halbfinalisten
    top_sf = sorted(semifinal_probs, key=semifinal_probs.get, reverse=True)[:4]
    world_champion = max(winner_probs, key=winner_probs.get)

    return {
        "group_winner_probabilities": group_probs,
        "group_recommendations": group_recommendations,
        "semifinal_probabilities": {t: semifinal_probs[t] for t in sorted(semifinal_probs, key=semifinal_probs.get, reverse=True)[:10]},
        "semifinal_recommendations": top_sf,
        "world_champion_probabilities": {t: winner_probs[t] for t in sorted(winner_probs, key=winner_probs.get, reverse=True)[:10]},
        "world_champion_recommendation": world_champion,
    }


def compute_top_scorer_team(
    elo: dict[str, float],
    semifinal_probs: dict[str, float],
    winner_probs: dict[str, float],
) -> dict:
    """
    Proxy für Torschützenkönig-Team:
    Angriffsstärke (lambda_avg) × erwartete Spiele im Turnier.
    """
    scores = {}
    for team in elo.keys():
        # Durchschnittliche Torerwartung gegen alle anderen Teams
        lambdas = [compute_lambdas(elo[team], elo[opp])[0] for opp in elo if opp != team]
        avg_lambda = sum(lambdas) / len(lambdas)

        # Erwartete Spiele: Gruppenphase(3) + KO-Anteil
        p_sf = semifinal_probs.get(team, 0)
        p_wc = winner_probs.get(team, 0)
        expected_games = 3 + p_sf * 2 + p_wc * 1  # vereinfacht

        scores[team] = round(avg_lambda * expected_games, 4)

    ranked = sorted(scores, key=scores.get, reverse=True)
    return {
        "recommendation": ranked[0],
        "top_5": [{"team": t, "score": scores[t]} for t in ranked[:5]],
    }
