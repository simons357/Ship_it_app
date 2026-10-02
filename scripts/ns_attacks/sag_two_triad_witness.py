#!/usr/bin/env python3
"""SAG eyes on the exact two-triad charge/covariance witness.

Not DA-NS-2. Not a T_c bound. NS is not solved.

Archive convention: k+p+q = 0 (helical triad).
SAG convention: p+q = −k, so the shared mode k is the
output after the sign flip (inputs −p, −q).
The witness is scalene. It is not an equal-input circle.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Dict, List, Sequence, Tuple

Mode = Tuple[int, int, int]


def add(a: Mode, b: Mode) -> Mode:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Mode, b: Mode) -> Mode:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Mode, b: Mode) -> int:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm2(a: Mode) -> int:
    return dot(a, a)


def det3(a: Mode, b: Mode, c: Mode) -> int:
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


# Exact witness, DA-NS-SPRINT-02 / showdown dossier 7 Sep 2026.
K: Mode = (1, 0, 0)
P: Mode = (0, 1, 1)
Q: Mode = (-1, -1, -1)
R: Mode = (0, 1, 0)
S: Mode = (-1, -1, 0)


def geometry() -> dict:
    g1 = add(K, add(P, Q))
    g2 = add(K, add(R, S))
    sag_out_1 = add(P, Q)  # = −k
    sag_out_2 = add(R, S)
    return {
        "k": K,
        "p": P,
        "q": Q,
        "r": R,
        "s": S,
        "triad_sum_1": g1,
        "triad_sum_2": g2,
        "closes": g1 == (0, 0, 0) and g2 == (0, 0, 0),
        "share_mode_k": True,
        "det_kpr": det3(K, P, R),
        "rank_three": det3(K, P, R) != 0,
        "lengths": {
            "k": math.sqrt(norm2(K)),
            "p": math.sqrt(norm2(P)),
            "q": math.sqrt(norm2(Q)),
            "r": math.sqrt(norm2(R)),
            "s": math.sqrt(norm2(S)),
        },
        "equal_input_circle": False,
        "why_not_equal_input": (
            "|p|≠|q| on γ1 (√2 vs √3); |r|≠|s| on γ2 (1 vs √2). "
            "SAG-6 collapse to one tangent vector does not apply."
        ),
        "sag_outputs": {"p+q": sag_out_1, "r+s": sag_out_2, "minus_k": sub((0, 0, 0), K)},
        "shared_output_after_sign_flip": sag_out_1 == sag_out_2 == sub((0, 0, 0), K),
    }


def charge_covariance() -> dict:
    """Dossier §12 arithmetic. Exact. Charge-only close is already dead."""
    sqrt2 = math.sqrt(2.0)
    sqrt3 = math.sqrt(3.0)
    sqrt6 = math.sqrt(6.0)
    q1 = 2.0 * (sqrt2 - 1.0)
    q2 = -2.0 * (sqrt2 - 1.0)
    r1 = (3.0 + 3.0 * sqrt2 + 5.0 * sqrt3 + sqrt6) / 6.0
    r2 = 1.0 + sqrt2
    t1 = 1.0 - sqrt3 + 4.0 * sqrt6 / 3.0
    t2 = -2.0
    boxed = (4.0 * sqrt6 - 3.0 * sqrt3 - 3.0) / 3.0
    lam = 2.0
    kappa = math.sqrt(lam)
    two_k3 = 2.0 * kappa**3
    rho = (r1 - two_k3) * q1 + (r2 - two_k3) * q2
    return {
        "Lambda": lam,
        "Q_a_1": q1,
        "Q_a_2": q2,
        "Q_a_Gamma": q1 + q2,
        "R_1": r1,
        "R_2": r2,
        "T_c_1": t1,
        "T_c_2": t2,
        "T_c_het_Gamma": t1 + t2,
        "T_from_RQ": r1 * q1 + r2 * q2,
        "boxed": boxed,
        "rho_split": rho,
        "two_kappa_cubed": two_k3,
        "R_1_equals_R_2": abs(r1 - r2) < 1e-15,
        "helicity": {"sigma_1": "(+,+,-)", "sigma_2": "(+,-,+)"},
        "iota": 1.0 + sqrt2 - sqrt3,
        "amplitudes": {
            "a_k_plus": 1.0,
            "a_p_plus": math.sqrt(2.0) / (1.0 + sqrt2 - sqrt3),
            "a_q_minus": complex(math.cos(-math.pi / 4.0), math.sin(-math.pi / 4.0)),
            "a_r_minus": math.sqrt(2.0),
            "a_s_plus": 1j,
        },
    }


def L_family(L: int) -> dict:
    """Integer family, L ≥ 2. Stays rank three. Archive scale probe."""
    if L < 2:
        raise ValueError("L >= 2")
    k = (L + 1, L, 0)
    p = (-L, 0, L)
    q = (-1, -L, -L)
    r = (0, -L, L)
    s = (-L - 1, 0, -L)
    d = det3(k, p, r)
    return {
        "L": L,
        "k": k,
        "p": p,
        "q": q,
        "r": r,
        "s": s,
        "sum_1": add(k, add(p, q)),
        "sum_2": add(k, add(r, s)),
        "det": d,
        "det_formula": L * L * (2 * L + 1),
        "rank_three": d != 0,
        "equal_input": norm2(p) == norm2(q) or norm2(r) == norm2(s),
    }


def archive_second_witness() -> dict:
    """Same-multiplier archive sample. NUMERICAL. Not re-derived here."""
    return {
        "tag": "NUMERICAL archive checkpoint, not this page's derivation",
        "R_1": -60.7616659871,
        "R_2": -60.7616659871,
        "Q_a_Gamma": -21.9024889809,
        "T_c_het_Gamma": 1330.83171974,
        "note": (
            "R_1=R_2<0 and Q_{a,Γ}<0 still give T_c^het>0. "
            "A common-multiplier coherence strategy does not close. "
            "Both raw phase rates vanish at the checkpoint."
        ),
    }


def archive_scale_diagnostic() -> dict:
    """Finite instantaneous decay. Explicitly not a time budget."""
    return {
        "tag": "NUMERICAL archive samples, not ∫K",
        "L2_width": 0.237,
        "L55_width": 0.0091,
        "L2_norm_cov": 1.19e-2,
        "L55_norm_cov": 9.30e-7,
        "diagnostic": "|ρ_Γ| / (κ^3 (|Q_a,1|+|Q_a,2|))",
        "warning": "finite instantaneous decay is not a time-integrated budget",
    }


def sag_eyes() -> dict:
    geo = geometry()
    cov = charge_covariance()
    return {
        "shared_output": geo["shared_output_after_sign_flip"],
        "one_a_k_plus": cov["amplitudes"]["a_k_plus"],
        "globally_compatible_real_field": True,
        "static_shared_output_forces_Tc_cancel": False,
        "Q_cancel": abs(cov["Q_a_Gamma"]) < 1e-15,
        "Tc_het_positive": cov["T_c_het_Gamma"] > 0.0,
        "verdict": (
            "SAG static shared-output rescue of charge-only coercivity: KILLED"
        ),
    }


def report() -> dict:
    return {
        "geometry": geometry(),
        "charge_covariance": charge_covariance(),
        "sag_eyes": sag_eyes(),
        "L_family_2": L_family(2),
        "L_family_55": L_family(55),
        "second_witness": archive_second_witness(),
        "scale_diagnostic": archive_scale_diagnostic(),
        "next_gate": "Joint Gap–Charge Epoch Budget → DA-NS-2. Not SAG-6.",
        "locks": {
            "not_equal_input_circle": True,
            "no_occupancy_bound": True,
            "no_static_shared_output_rescue": True,
            "not_a_time_budget": True,
            "not_a_close": True,
        },
    }


def _py(x):
    if isinstance(x, complex):
        return {"re": x.real, "im": x.imag}
    if isinstance(x, dict):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(list(argv) if argv is not None else None)
    print(json.dumps(_py(report()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
