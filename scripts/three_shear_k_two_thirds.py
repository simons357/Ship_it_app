#!/usr/bin/env python3
"""Three-shear write-up example: w = (sin y, sin z, sin x).

K_{1,2}(w) = 2/3 by hand. This is a floor: sup K >= 2/3.
It is not the 16/9 ceiling and not C_0.

NS not solved. Unrestricted ★ stays dead on v_n.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import ns_lemma_star_core as core  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "three_shear_k_two_thirds.json"

TWO_THIRDS = 2.0 / 3.0
HAND_E = 1.5
HAND_PIB2 = 0.75  # 12 * (1/16)
SHELL2 = (
    (1, 1, 0),
    (1, -1, 0),
    (-1, 1, 0),
    (-1, -1, 0),
    (1, 0, 1),
    (1, 0, -1),
    (-1, 0, 1),
    (-1, 0, -1),
    (0, 1, 1),
    (0, 1, -1),
    (0, -1, 1),
    (0, -1, -1),
)


def three_shear() -> core.Field:
    """w = (sin y, sin z, sin x) on shell α=1."""
    f = core.Field()
    f.set_mode((0, 1, 0), np.array([-0.5j, 0.0, 0.0]))
    f.set_mode((0, 0, 1), np.array([0.0, -0.5j, 0.0]))
    f.set_mode((1, 0, 0), np.array([0.0, 0.0, -0.5j]))
    return f


def hygiene(field: core.Field) -> dict:
    max_div = 0.0
    max_real = 0.0
    lambdas = set()
    for k, vk in field.modes.items():
        lambdas.add(core.lam(k))
        max_div = max(max_div, abs(complex(np.dot(np.array(k, dtype=float), vk))))
        nk = (-k[0], -k[1], -k[2])
        max_real = max(max_real, float(np.linalg.norm(field.modes[nk] - np.conj(vk))))
    return {
        "n_modes": len(field.modes),
        "lambdas": sorted(lambdas),
        "exact_shell_alpha_1": lambdas == {1.0},
        "max_k_dot_v": max_div,
        "max_reality": max_real,
        "div_free": max_div < 1e-12,
        "real_valued": max_real < 1e-12,
    }


def output_sizes(field: core.Field) -> list[dict]:
    rows = []
    for k in SHELL2:
        Bk = core.B_hat_at(field, k)
        size = float(np.vdot(Bk, Bk).real)
        rows.append({"k": list(k), "B_abs2": size})
    return rows


def record() -> dict:
    f = three_shear()
    h = hygiene(f)
    E = f.energy()
    outs = output_sizes(f)
    pib2 = sum(r["B_abs2"] for r in outs)
    K = core.K_alpha_beta(f, 1, 2)
    hand_K = (2.0 * HAND_PIB2) / (1.0 * HAND_E**2)
    return {
        "ns_solved": False,
        "singular_nse": False,
        "field": "w = (sin y, sin z, sin x)",
        "role": "write_up_example_floor_not_bound",
        "K_is_C0": False,
        "exact_shell_16_over_9": "CLAIMED_not_stamped",
        **h,
        "E": E,
        "E_hand": HAND_E,
        "PiB_L2_sq": pib2,
        "PiB_L2_sq_hand": HAND_PIB2,
        "n_outputs": len(outs),
        "each_output_B_abs2": [r["B_abs2"] for r in outs],
        "all_outputs_one_sixteenth": all(abs(r["B_abs2"] - 0.0625) < 1e-12 for r in outs),
        "K_1_2": K,
        "K_hand": TWO_THIRDS,
        "K_matches_two_thirds": abs(K - TWO_THIRDS) < 1e-12,
        "hand_arithmetic": hand_K,
        "unrestricted_lemma_star": "still_dead_on_v_n",
        "note": (
            "sup K >= 2/3. 2/3 is not C_0 and not 16/9. "
            "A random-search maximum is a weaker object than this floor."
        ),
    }


def main() -> None:
    payload = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
