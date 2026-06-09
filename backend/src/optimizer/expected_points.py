"""
Expected-Points-Optimizer für Kicktipp (2-4 Punkte, Turnier-Regel).
Berechnet für jeden möglichen Tipp den erwarteten Punkteertrag
und gibt den optimalen Tipp zurück.
"""

MAX_TIP = 5  # Tipps von 0:0 bis 5:5


def kicktipp_points(tip_a: int, tip_b: int, result_a: int, result_b: int) -> int:
    """
    Berechnet Kicktipp-Punkte gemäß 2-4 Punkte Turnier-Regel.

    Punktetabelle:
      Exaktes Ergebnis:           4 Punkte
      Tordifferenz korrekt (Sieg): 3 Punkte
      Nur Tendenz korrekt:         2 Punkte
      Falsche Tendenz:             0 Punkte

    Sonderfall Unentschieden:
      Tordifferenz-Stufe (3 Pkt) entfällt → nur 2 oder 4.
    """
    # Tendenzen: +1 = A gewinnt, 0 = Unentschieden, -1 = B gewinnt
    tip_tendency = (tip_a > tip_b) - (tip_a < tip_b)
    result_tendency = (result_a > result_b) - (result_a < result_b)

    if tip_tendency != result_tendency:
        return 0  # Falsche Tendenz

    if tip_a == result_a and tip_b == result_b:
        return 4  # Exaktes Ergebnis

    if tip_tendency == 0:
        # Unentschieden korrekt getippt, aber nicht exakt → 2 Punkte
        return 2

    if (tip_a - tip_b) == (result_a - result_b):
        return 3  # Tordifferenz korrekt

    return 2  # Nur Tendenz korrekt


def expected_points(
    tip_a: int, tip_b: int, dist: dict[tuple[int, int], float]
) -> float:
    """Berechnet E[pts(tip_a, tip_b)] über alle Scorelines."""
    return sum(
        p * kicktipp_points(tip_a, tip_b, i, j)
        for (i, j), p in dist.items()
    )


def find_optimal_tip(
    dist: dict[tuple[int, int], float]
) -> dict:
    """
    Findet den Tipp mit maximalem E[pts] über alle (tip_a, tip_b) mit 0 ≤ a,b ≤ MAX_TIP.
    Gibt optimalen Tipp, E[pts] und Top-3-Alternativen zurück.
    """
    results = []
    for ta in range(MAX_TIP + 1):
        for tb in range(MAX_TIP + 1):
            ep = expected_points(ta, tb, dist)
            results.append({"tip_a": ta, "tip_b": tb, "expected_points": round(ep, 4)})

    results.sort(key=lambda x: x["expected_points"], reverse=True)

    return {
        "optimal_tip": f"{results[0]['tip_a']}:{results[0]['tip_b']}",
        "optimal_tip_a": results[0]["tip_a"],
        "optimal_tip_b": results[0]["tip_b"],
        "expected_points": results[0]["expected_points"],
        "top_alternatives": [
            {"tip": f"{r['tip_a']}:{r['tip_b']}", "expected_points": r["expected_points"]}
            for r in results[1:4]
        ],
    }
