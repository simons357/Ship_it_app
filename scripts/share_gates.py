"""Share-Gate A / Share-Gate B. Lattice triad identities sit. Kill not stamped.

Share-Gate A: named kill target L_{z_j}→∞ for positive family-level Young.
Share-Gate B: global energy sharing; first target is a frequency exponent, not regularity.
Not Track A. Not Track B. Not Lemma A/B. Not Catalog B.
Do not stamp W_N ≳ log N. Do not revive K~√E. Do not start leftover 1.

Does not overwrite stokes_moments.py.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "share_gates.json"


def triad(N: int, j: int, v: int) -> dict:
    r = (N, 0, 0)
    q = (-j, v, 0)
    p = (j - N, -v, 0)
    s2 = j * j + v * v
    x = N * N + s2 - 2 * N * j
    y = s2
    z = N * N
    cross = (
        q[1] * r[2] - q[2] * r[1],
        q[2] * r[0] - q[0] * r[2],
        q[0] * r[1] - q[1] * r[0],
    )
    # p × q in the xy-plane
    pxq_z = p[0] * q[1] - p[1] * q[0]
    pxq_abs = abs(pxq_z)
    return {
        "N": N,
        "j": j,
        "v": v,
        "s": int(math.isqrt(s2)) if math.isqrt(s2) ** 2 == s2 else math.sqrt(s2),
        "p": p,
        "q": q,
        "r": r,
        "sum": (p[0] + q[0] + r[0], p[1] + q[1] + r[1], p[2] + q[2] + r[2]),
        "x": x,
        "y": y,
        "z": z,
        "p_norm2": p[0] * p[0] + p[1] * p[1] + p[2] * p[2],
        "q_norm2": q[0] * q[0] + q[1] * q[1] + q[2] * q[2],
        "r_norm2": r[0] * r[0] + r[1] * r[1] + r[2] * r[2],
        "pxq_abs": pxq_abs,
        "N_abs_v": N * abs(v),
        "Delta": N * N * v * v,
        "x_le_y_le_z": x <= y <= z,
        "j_ge_half_N": j * 2 >= N,
        "s2_le_N2": y <= z,
        "cross_qr": cross,
    }


def pythagorean_samples() -> list[tuple[int, int, int, int]]:
    """(N, j, v, s) with j^2 + v^2 = s^2 and s <= N."""
    return [
        (5, 4, 3, 5),
        (13, 12, 5, 13),
        (17, 15, 8, 17),
        (25, 24, 7, 25),
        (10, 8, 6, 10),
    ]


def record() -> dict:
    rows = []
    all_ok = True
    for N, j, v, s in pythagorean_samples():
        t = triad(N, j, v)
        ok = (
            t["sum"] == (0, 0, 0)
            and t["p_norm2"] == t["x"]
            and t["q_norm2"] == t["y"]
            and t["r_norm2"] == t["z"]
            and t["y"] == s * s
            and t["z"] == N * N
            and t["pxq_abs"] == t["N_abs_v"]
            and t["Delta"] == t["pxq_abs"] * t["pxq_abs"]
            and t["x_le_y_le_z"]
            and t["j_ge_half_N"]
        )
        t["ok"] = ok
        rows.append(t)
        all_ok = all_ok and ok

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "catalog_b_open_stays_1": True,
        "not_track_A": True,
        "not_track_B": True,
        "not_lemma_A": True,
        "not_lemma_B": True,
        "not_catalog_B": True,
        "do_not_merge_letters": True,
        "lattice_triad_identities_sit": all_ok,
        "samples": [
            {
                "N": r["N"],
                "j": r["j"],
                "v": r["v"],
                "x": r["x"],
                "y": r["y"],
                "z": r["z"],
                "ok": r["ok"],
            }
            for r in rows
        ],
        "share_gate_A_question": (
            "Can positive dissipation sharing alone survive infinitely many shapes?"
        ),
        "share_gate_B_question": (
            "What happens when the low-frequency factors must share energy globally?"
        ),
        "share_gate_A_kill_target": "construct z_j→∞ and prove L_{z_j}→∞",
        "share_gate_A_kill_stamped": False,
        "frozen_rule_from_original_shell_estimate": False,
        "restricted_pythagorean_count_seated": False,
        "W_N_log_divergence_seated": False,
        "finite_shells_are_not_the_kill": True,
        "kill_would_not_prove_every_shared_budget": True,
        "kill_would_not_prove_signed_cancellation": True,
        "kill_would_not_prove_shared_energy_accounting": True,
        "kill_would_not_prove_criterion_17": True,
        "kill_would_not_prove_regularity": True,
        "share_gate_B_open": True,
        "share_gate_B_waits_for_A": False,
        "share_gate_B_is_not_prove_regularity": True,
        "share_gate_B_first_target": "sharp frequency exponent after global energy sharing",
        "share_gate_B_schematic_derived": False,
        "per_family_sqrt_E_repeatedly_spends_same_energy": True,
        "do_not_revive_K_sqrt_E": True,
        "do_not_revive_uniform_preYoung_C": True,
        "do_not_start_leftover_1": True,
        "c10_not_a_theorem": True,
        "sign_gate_unaltered": True,
        "lemma_A_unaltered": True,
        "lemma_B_open": True,
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "sits_as_beyond_ess": False,
        "g4_stays_open": True,
        "do_not_invent_a_bridge": True,
        "do_not_run_taylor_green": True,
        "not_a_thirteenth_leftover": True,
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
