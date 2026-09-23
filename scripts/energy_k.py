"""Energy-class remainder ladder after K~sqrt(E). Not a close.

Homogeneity: only p = 1/2 is amplitude-legal for
    |T_c| <= C E^p X
and only q = 1/2 is amplitude-legal for
    |T_c| <= C E^q Y.
The mid door |T_c| <= C sqrt(E X Y) is the unique
amplitude-matched interpolation. All three would be
useful Route B remainders if a uniform C sat.
v_n already killed the X-door. This file scores the
other two and the illegal p.

Do not overwrite stokes_moments.py.
Do not restore ★.
Do not seat B★.
Do not cash Attack-2 C_* as this death.
Do not start leftover 1.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from stokes_moments import scale_field  # noqa: E402
from bstar_attack import score, separated_triad  # noqa: E402
from bstar_symmetrize import fft_probe, power_law_field  # noqa: E402
from fourier_triangle import isosceles_hh_l  # noqa: E402
from ns_lemma_star_core import Field  # noqa: E402
from verify_pr24_closure_review import growing_layer_field  # noqa: E402

OUT = ROOT / "results" / "energy_k.json"


def E_n(n: int) -> float:
    return 4.0 * (2 * n + 1)


def X_n(n: int) -> float:
    """Growing-layer enstrophy. Locked: n(2n+1)(49n+4)/3."""
    return n * (2 * n + 1) * (49 * n + 4) / 3.0


def Y_n(n: int) -> float:
    """Growing-layer palinstrophy. Locked: n(2n+1)(1167n³+174n²+8n-4)/15."""
    return n * (2 * n + 1) * (1167 * n**3 + 174 * n**2 + 8 * n - 4) / 15.0


def T_c_n(n: int) -> float:
    return 3.0 * (n**5) * (3 * n * n + 3 * n + 1)


def R_Y_closed(n: int) -> float:
    return T_c_n(n) / (math.sqrt(E_n(n)) * Y_n(n))


def R_mid_closed(n: int) -> float:
    return T_c_n(n) / math.sqrt(E_n(n) * X_n(n) * Y_n(n))


def _ratios(e: float, x: float, y: float, tc: float) -> dict:
    tc = abs(tc)
    r_e = tc / (math.sqrt(e) * x) if e > 0 and x > 0 else float("nan")
    r_y = tc / (math.sqrt(e) * y) if e > 0 and y > 0 else float("nan")
    r_mid = (
        tc / math.sqrt(e * x * y) if e > 0 and x > 0 and y > 0 else float("nan")
    )
    lam = y / x if x > 0 else float("nan")
    return {
        "E": e,
        "X": x,
        "Y": y,
        "Lambda": lam,
        "Tc_abs": tc,
        "R_E": r_e,
        "R_Y": r_y,
        "R_mid": r_mid,
    }


def from_score(row: dict) -> dict:
    out = _ratios(row["E"], row["X"], row["Y"], row["Tc"])
    out["label"] = row["label"]
    out["R_B"] = row.get("R_B")
    out["R_star"] = row.get("R_star")
    return out


def field_to_stokes_dict(field: Field) -> dict:
    return {k: v.copy() for k, v in field.modes.items()}


def amplitude_scan() -> dict:
    """Scale a live two-shell triangle. Only p = 1/2 stays flat."""
    base = field_to_stokes_dict(isosceles_hh_l())
    scales = (0.05, 0.2, 1.0, 4.0)
    rows = []
    for a in scales:
        pr = score(scale_field(base, a), f"amp{a}")
        ratios = from_score(pr)
        # Illegal doors: p = 1 (small A) and p = 0 (large A).
        e, x, tc = ratios["E"], ratios["X"], ratios["Tc_abs"]
        ratios["R_p1"] = tc / (e * x) if e > 0 and x > 0 else float("nan")
        ratios["R_p0"] = tc / x if x > 0 else float("nan")
        ratios["amp"] = a
        rows.append(ratios)
    r_e = [r["R_E"] for r in rows]
    r_y = [r["R_Y"] for r in rows]
    r_mid = [r["R_mid"] for r in rows]
    r_p1 = [r["R_p1"] for r in rows]
    r_p0 = [r["R_p0"] for r in rows]
    return {
        "rows": rows,
        "R_E_flat": max(r_e) / min(r_e) < 1.01,
        "R_Y_flat": max(r_y) / min(r_y) < 1.01,
        "R_mid_flat": max(r_mid) / min(r_mid) < 1.01,
        "R_p1_grows_as_A_shrinks": r_p1[0] > 5.0 * r_p1[-1],
        "R_p0_grows_as_A_grows": r_p0[-1] > 5.0 * r_p0[0],
        "unique_amp_legal_p": 0.5,
    }


def family_rows() -> list:
    families = []
    for n in (1, 4, 8):
        families.append(from_score(score(growing_layer_field(n), f"vn{n}")))
    for m in (1, 8):
        families.append(from_score(score(separated_triad(m), f"sep{m}")))
    for K, ngrid in ((4, 32), (6, 32), (8, 48)):
        pr = fft_probe(power_law_field(K, 2.0, "imag"), n=ngrid)
        row = _ratios(pr["E"], pr["X"], pr["Y"], pr["Tc"])
        row["label"] = f"imagK{K}"
        row["R_B"] = pr["R_B"]
        families.append(row)
    return families


def record() -> dict:
    amp = amplitude_scan()
    families = family_rows()
    vn = [r for r in families if r["label"].startswith("vn")]
    imag = [r for r in families if r["label"].startswith("imag")]
    sep = [r for r in families if r["label"].startswith("sep")]
    closed = []
    for n in (1, 4, 8):
        row = next(r for r in vn if r["label"] == f"vn{n}")
        closed.append(
            {
                "n": n,
                "X_match": abs(row["X"] - X_n(n)) < 1e-8,
                "Y_match": abs(row["Y"] - Y_n(n)) < 1e-6,
                "R_Y_match": abs(row["R_Y"] - R_Y_closed(n)) < 1e-10,
                "R_mid_match": abs(row["R_mid"] - R_mid_closed(n)) < 1e-10,
                "R_Y_closed": R_Y_closed(n),
                "R_mid_closed": R_mid_closed(n),
            }
        )
    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "not_attack2_Cstar": True,
        "homogeneity": {
            "T_c_degree": 3,
            "EXY_degree": 2,
            "unique_p_for_E_p_X": 0.5,
            "unique_q_for_E_q_Y": 0.5,
            "mid_door": "|T_c| <= C sqrt(E X Y)",
            "X_door": "|T_c| <= C sqrt(E) X  =>  K ~ sqrt(E)",
            "Y_door": "|T_c| <= C sqrt(E) Y  =>  K_Y ~ sqrt(E)",
            "if_X_sits": "Lambda' <= 2 C sqrt(E)",
            "if_Y_sits": "(log Lambda)' <= 2 C sqrt(E)",
            "if_mid_sits": "(sqrt(Lambda))' <= C sqrt(E)",
        },
        "amplitude": amp,
        "families": families,
        "vn_R_E_grows": vn[-1]["R_E"] > vn[0]["R_E"],
        "vn_R_Y_grows": vn[-1]["R_Y"] > vn[0]["R_Y"],
        "vn_R_mid_grows": vn[-1]["R_mid"] > vn[0]["R_mid"],
        "imag_R_Y_grows": imag[-1]["R_Y"] > imag[0]["R_Y"],
        "imag_R_mid_grows": imag[-1]["R_mid"] > imag[0]["R_mid"],
        "sep_not_the_kill": sep[-1]["R_Y"] < sep[0]["R_Y"],
        "sits_as_universal_C": False,
        "energy_class_ladder_dead": True,
        "g4_stays_open": True,
        "closed_forms": {
            "E_n": "4(2n+1)",
            "X_n": "n(2n+1)(49n+4)/3",
            "Y_n": "n(2n+1)(1167 n^3+174 n^2+8n-4)/15",
            "T_c": "3 n^5 (3n^2+3n+1)",
            "R_Y_asymp": "c n^{3/2}",
            "R_mid_asymp": "c n^{5/2}",
            "rows": closed,
            "all_match": all(
                r["X_match"] and r["Y_match"] and r["R_Y_match"] and r["R_mid_match"]
                for r in closed
            ),
        },
        "vn_table": [
            {
                "label": r["label"],
                "R_E": r["R_E"],
                "R_mid": r["R_mid"],
                "R_Y": r["R_Y"],
                "Lambda": r["Lambda"],
            }
            for r in vn
        ],
        "imag_table": [
            {
                "label": r["label"],
                "R_E": r["R_E"],
                "R_mid": r["R_mid"],
                "R_Y": r["R_Y"],
                "Lambda": r["Lambda"],
            }
            for r in imag
        ],
        "sep_table": [
            {"label": r["label"], "R_Y": r["R_Y"], "R_mid": r["R_mid"]}
            for r in sep
        ],
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
