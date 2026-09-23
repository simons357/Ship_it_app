"""First lift of Fourier-triangle identities. Not a close.

What still sits after two triangles are added, and the first
arrow that does not. B of a closed triad leaks off-support.
Do not overwrite stokes_moments.py.
Do not restore ★.
Do not seat B★.
Do not start leftover 1.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from fourier_triangle import (  # noqa: E402
    closed_triad,
    isosceles_hh_l,
    three_shell_unequal,
    two_shell_reduction,
)
from ns_lemma_star_core import (  # noqa: E402
    B_hat_at,
    Field,
    T_c_direct,
    lam,
    moments,
)
from bstar_attack import score, separated_triad  # noqa: E402
from bstar_symmetrize import fft_probe, power_law_field  # noqa: E402
from verify_pr24_closure_review import growing_layer_field  # noqa: E402

OUT = ROOT / "results" / "triangle_lift.json"


def iso_yz(amp=1.0, phase_q=0.5) -> Field:
    """Second 2+2=4 triangle, yz-plane. Same two shells, disjoint keys."""
    return closed_triad(
        (0, 1, 1),
        (0, -1, 1),
        (amp, amp, amp),
        (0.0, phase_q, -0.3),
        ((1.0, -1.0, 1.0), (1.0, 1.0, -1.0), (1.0, 0.0, 0.0)),
    )


def iso_five_eighteen(amp=1.0, phase_q=0.4) -> Field:
    """Two-shell packet on 5 and 18. Disjoint from the 2+2=4 triangle."""
    return closed_triad(
        (2, 1, 0),
        (1, 2, 0),
        (amp, amp, amp),
        (0.0, phase_q, -0.2),
        ((1.0, -2.0, 0.5), (-2.0, 1.0, 0.5), (0.0, 0.0, 1.0)),
    )


def add_fields(a: Field, b: Field) -> Field:
    return a.add(b)


def shells_of(field: Field) -> list:
    return sorted({lam(k) for k in field.support()})


def leak_B(field: Field) -> dict:
    """||B||^2 on support vs on every pairwise sum (the leak)."""
    keys = list(field.support())
    landing = set()
    for p in keys:
        for q in keys:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k != (0, 0, 0):
                landing.add(k)
    on = off = 0.0
    n_off = 0
    for k in landing:
        bk = B_hat_at(field, k)
        e = float(np.vdot(bk, bk).real)
        if k in field.modes:
            on += e
        else:
            off += e
            if e > 1e-14:
                n_off += 1
    tot = on + off
    return {
        "n_support": len(keys),
        "n_landings": len(landing),
        "n_off_live": n_off,
        "B2_on": on,
        "B2_off": off,
        "leak_frac": (off / tot) if tot > 0 else 0.0,
        "closed_under_B": n_off == 0,
    }


def tc_of(field: Field) -> float:
    _E, _X, _Y, _Z, Lam = moments(field)
    return float(T_c_direct(field, Lam))


def R_E_row(pr: dict) -> float:
    e, x, tc = pr["E"], pr["X"], abs(pr["Tc"])
    denom = math.sqrt(e) * x if e > 0 and x > 0 else float("nan")
    return tc / denom if denom == denom and denom > 0 else float("nan")


def record() -> dict:
    a = isosceles_hh_l()
    b = iso_yz()
    b_unbal = closed_triad(
        (0, 1, 1),
        (0, -1, 1),
        (1.0, 1.0, 0.2),
        (0.0, 0.5, -0.3),
        ((1.0, -1.0, 1.0), (1.0, 1.0, -1.0), (1.0, 0.0, 0.0)),
    )
    c = iso_five_eighteen()
    uneq = three_shell_unequal()
    same = add_fields(a, b)
    same_unbal = add_fields(a, b_unbal)
    four = add_fields(a, c)

    red_a = two_shell_reduction(a)
    red_b = two_shell_reduction(b)
    red_same = two_shell_reduction(same)
    red_four = two_shell_reduction(four)
    red_uneq = two_shell_reduction(uneq)

    tc_a, tc_b, tc_c = tc_of(a), tc_of(b), tc_of(c)
    tc_same, tc_four = tc_of(same), tc_of(four)

    leak_a = leak_B(a)
    leak_same = leak_B(same)
    leak_four = leak_B(four)
    leak_uneq = leak_B(uneq)

    families = []
    for n in (1, 4, 8):
        row = score(growing_layer_field(n), f"vn{n}")
        row["R_E"] = R_E_row(row)
        families.append(
            {
                "label": row["label"],
                "R_E": row["R_E"],
                "R_B": row["R_B"],
                "R_star": row["R_star"],
            }
        )
    for m in (1, 8):
        row = score(separated_triad(m), f"sep{m}")
        row["R_E"] = R_E_row(row)
        families.append(
            {"label": row["label"], "R_E": row["R_E"], "R_B": row["R_B"]}
        )
    for K, ngrid in ((4, 32), (6, 32), (8, 48)):
        pr = fft_probe(power_law_field(K, 2.0, "imag"), n=ngrid)
        re = abs(pr["Tc"]) / (math.sqrt(pr["E"]) * pr["X"])
        families.append(
            {
                "label": f"imagK{K}",
                "R_E": re,
                "R_B": pr["R_B"],
                "Lambda": pr["Lambda"],
            }
        )

    vn_re = [r["R_E"] for r in families if r["label"].startswith("vn")]
    imag_re = [r["R_E"] for r in families if r["label"].startswith("imag")]

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "lifts_that_sit": {
            "two_shell_a": red_a["two_shell"] and abs(red_a["Tc"] - red_a["pred_from_Ta"]) < 1e-10,
            "two_shell_b": red_b["two_shell"] and abs(red_b["Tc"] - red_b["pred_from_Ta"]) < 1e-10,
            "same_two_shells_still_gap": red_same["two_shell"]
            and abs(red_same["Tc"] - red_same["pred_from_Ta"]) < 1e-9,
            "same_two_shells_n": len(shells_of(same)),
        },
        "first_failed_sum": {
            "four_shell_n": len(shells_of(four)),
            "four_shell_gap_formula": bool(red_four.get("two_shell")),
            "unequal_gap_formula": bool(red_uneq.get("two_shell")),
            "tc_a": tc_a,
            "tc_c": tc_c,
            "tc_a_plus_c": tc_a + tc_c,
            "tc_four": tc_four,
            "nonadditive": abs(tc_four - (tc_a + tc_c)) > 0.1,
            "same_tc_a_plus_b": tc_a + tc_b,
            "same_tc_sum": tc_same,
            "same_nonadditive": abs(tc_same - (tc_a + tc_b)) > 0.1,
            "unbal_still_two_shell": two_shell_reduction(same_unbal)["two_shell"],
            "unbal_tc_a_plus_b": tc_a + tc_of(b_unbal),
            "unbal_tc_sum": tc_of(same_unbal),
            "unbal_residual": abs(tc_of(same_unbal) - (tc_a + tc_of(b_unbal))),
        },
        "first_failed_evolve": {
            "isolated_closed_under_B": leak_a["closed_under_B"],
            "leak_a": leak_a,
            "leak_same": leak_same,
            "leak_four": leak_four,
            "leak_uneq": leak_uneq,
        },
        "attempted_energy_K": {
            "shape": "|T_c| <= C sqrt(E) X  =>  K ~ sqrt(E)",
            "families": families,
            "vn_R_E_grows": vn_re[-1] > vn_re[0],
            "imag_R_E_grows": imag_re[-1] > imag_re[0],
            "sits_as_universal_C": False,
        },
        "first_missing": (
            "two-shell gap-cancel does not lift to a useful K after "
            "a third eigenvalue or after B leaks off the triangle"
        ),
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
