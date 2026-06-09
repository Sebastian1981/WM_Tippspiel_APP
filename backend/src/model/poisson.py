"""
Poisson-Modell für WM-Tippspiel
Berechnet Torerwartungen und Score-Wahrscheinlichkeitsverteilung P(i,j)
"""
import numpy as np
from scipy.stats import poisson

# Modellparameter
BASE_GOALS = 1.35   # Ø Tore pro Team pro internationalem Spiel
ELO_SCALE = 600     # Elo-Differenz-Skalierung für Torerwartung
MAX_GOALS = 7       # Maximale Tore pro Team für Verteilung


def compute_lambdas(elo_a: float, elo_b: float) -> tuple[float, float]:
    """Berechnet Torerwartungen lambda_A und lambda_B aus Elo-Differenz."""
    elo_diff = elo_a - elo_b
    lambda_a = max(0.25, BASE_GOALS + elo_diff / ELO_SCALE)
    lambda_b = max(0.25, BASE_GOALS - elo_diff / ELO_SCALE)
    return lambda_a, lambda_b


def score_distribution(lambda_a: float, lambda_b: float) -> dict[tuple[int, int], float]:
    """
    Berechnet P(i,j) für alle Scorelines (0:0) bis (MAX_GOALS:MAX_GOALS).
    Normiert auf Summe = 1.
    """
    dist = {}
    for i in range(MAX_GOALS + 1):
        for j in range(MAX_GOALS + 1):
            dist[(i, j)] = poisson.pmf(i, lambda_a) * poisson.pmf(j, lambda_b)

    total = sum(dist.values())
    return {k: v / total for k, v in dist.items()}


def outcome_probabilities(dist: dict[tuple[int, int], float]) -> dict[str, float]:
    """Berechnet P(Sieg A), P(Unentschieden), P(Sieg B) aus Score-Verteilung."""
    p_a = sum(p for (i, j), p in dist.items() if i > j)
    p_x = sum(p for (i, j), p in dist.items() if i == j)
    p_b = sum(p for (i, j), p in dist.items() if i < j)
    return {"team_a_win": p_a, "draw": p_x, "team_b_win": p_b}


def adjust_for_ko(
    dist: dict[tuple[int, int], float], elo_a: float, elo_b: float
) -> dict[tuple[int, int], float]:
    """
    KO-Modus: Verteilt die Unentschieden-Masse auf Sieger-Tipps,
    da im Elfmeterschießen ein Sieger ermittelt wird.
    Elo-Siegwahrscheinlichkeit bestimmt die Aufteilung.
    """
    p_elo_a = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
    adjusted = {}
    for (i, j), p in dist.items():
        if i == j:
            # Unentschieden-Masse aufteilen: A gewinnt nach Elfmeter
            adjusted[(i + 1, j)] = adjusted.get((i + 1, j), 0) + p * p_elo_a
            adjusted[(i, j + 1)] = adjusted.get((i, j + 1), 0) + p * (1 - p_elo_a)
        else:
            adjusted[(i, j)] = adjusted.get((i, j), 0) + p
    return adjusted
