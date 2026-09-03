#!/usr/bin/env python3
"""
Cooperative game on the reconstructed knobs.

Game R: v(S) = lock_R(S) − baseline. Shapley says who is pivotal for the score.
Game U: u(S) = 1 iff every must-hit is in S. Shapley is 1/|must| on those, 0 else.

Neither game writes F. Additive. Does not change slots A, B, Q.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_fingers import CANDIDATE_META, SIXTEEN  # noqa: E402
from unifier_combo import INPUTS, lock_score, r_batch, sample_matrix  # noqa: E402


MUST_HIT = [
    name
    for name in SIXTEEN
    if name != "R" and CANDIDATE_META[name][1].startswith("must_hit")
]
FLUSHED = ["log_cc_ratio", "log_hierarchy", "S_coh", "delta_spread"]


def shapley_monte_carlo(
    players: list[str],
    value_fn,
    rng: np.random.Generator,
    n_perm: int,
) -> dict[str, float]:
    phi = {name: 0.0 for name in players}
    n = len(players)
    order = np.arange(n)
    for _ in range(n_perm):
        rng.shuffle(order)
        prev = 0.0
        chosen: list[str] = []
        for idx in order:
            name = players[idx]
            chosen.append(name)
            now = value_fn(tuple(chosen))
            phi[name] += now - prev
            prev = now
    return {name: val / n_perm for name, val in phi.items()}


def run(n: int = 80, n_perm: int = 240, seed: int = 1, out: Path | None = None) -> dict:
    rng = np.random.default_rng(seed)
    base = sample_matrix(n, rng)
    baseline = float(np.mean(r_batch(base)))
    players = [name for name in SIXTEEN if name != "R" and name in INPUTS]
    cache: dict[tuple[str, ...], float] = {}

    def v_r(chosen: tuple[str, ...]) -> float:
        key = tuple(sorted(chosen))
        if key not in cache:
            cache[key] = lock_score(base, key) - baseline
        return cache[key]

    phi_r = shapley_monte_carlo(players, v_r, rng, n_perm)
    ranked = sorted(phi_r.items(), key=lambda kv: kv[1], reverse=True)
    top4 = [name for name, _ in ranked[:4]]
    same_as_flush = set(top4) == set(FLUSHED)

    grand = v_r(tuple(players))
    phi_sum = sum(phi_r.values())

    phi_u = {name: (1.0 / len(MUST_HIT) if name in MUST_HIT else 0.0) for name in SIXTEEN if name != "R"}

    payload = {
        "meta": {
            "games": ["R (score)", "U (unifier claim)"],
            "not_a_unifier": True,
            "n": n,
            "n_perm": n_perm,
            "seed": seed,
        },
        "game_R": {
            "v": "lock_R(S) − baseline",
            "baseline": baseline,
            "v_grand_coalition": grand,
            "shapley": {k: v for k, v in ranked},
            "shapley_sum": phi_sum,
            "efficiency_err": abs(phi_sum - grand),
            "top4": top4,
            "flush_top4": FLUSHED,
            "same_four_as_flush": same_as_flush,
            "narrows_past_flush": (not same_as_flush),
        },
        "game_U": {
            "u": "1 iff every must-hit is in S, else 0",
            "must_hit": MUST_HIT,
            "shapley": phi_u,
            "note": "This ranking is by definition, not by data. It protects nature leftovers.",
        },
        "what_it_cannot_do": [
            "write F",
            "collapse the waveform",
            "decide the vacuum topological fork",
            "replace Cosmo names",
        ],
        "how_far": [
            "Game R Shapley recovers the same four as the Hilbert flush"
            if same_as_flush
            else "Game R Shapley disagrees with the flush; that would be a real re-rank",
            "Game U puts equal weight on must-hits and zero on the rest (definition, not data)",
            "two games, two answers; do not glue them",
            "game theory did not write F and did not collapse the wave",
        ],
        "next_da_move": "Keep Game R and Game U separate. Do not treat Shapley as emergence.",
    }
    dest = Path(out) if out is not None else Path("results/da_game.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA game theory. Two games. Neither is F.")
    print("Game R Shapley (score):")
    for name, val in payload["game_R"]["shapley"].items():
        print(f"  {name:<18} {val:+.4f}")
    print("top4:", payload["game_R"]["top4"], "same as flush:", payload["game_R"]["same_four_as_flush"])
    print("narrows past flush:", payload["game_R"]["narrows_past_flush"])
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
