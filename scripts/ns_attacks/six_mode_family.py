"""DA six-mode family and F_X budget ingredients.

Family (integer j >= 3)
    p = (1,0,0),  u_p = e_2
    q = (j,j,0),  u_q = j^{-1/2} e_3
    k = p+q,      u_k = i j^{-1/2} e_3
    plus reality conjugates.

j a perfect square keeps every amplitude in Q(i), so T_c, N, Y, D_s are
exact.  Linear moments (E,X,Y,Z,D_s) are in Q for every integer j,
because they depend only on |u|^2.

Claimed identities (checked on square j, moments on all j):
    N = -2(2j+1)
    Ds / (Lambda Y) ~ 1/(4j)

F_X = 2 (Cs g sqrt(Lambda) - nu Lambda)_+
is a proved implication from the finite-C estimate plus energy, not a
paid time budget.  This module only records the exact ingredients
(Lambda, X, Y, certified g bounds) so Atlas can display F_X(Cs, nu).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional

from ns_attacks.exact_fourier import (
    Field,
    GQ,
    I,
    cascade,
    certified_grad_l3,
    gq_vec,
    moments,
    vscale,
    verify_identities,
)


def _is_square(j: int) -> bool:
    if j <= 0:
        return False
    s = int(math.isqrt(j))
    return s * s == j


def six_mode_lambdas(j: int) -> Dict[str, int]:
    if j < 3:
        raise ValueError("family is stated for integer j >= 3")
    return {
        "p": 1,
        "q": 2 * j * j,
        "k": (1 + j) * (1 + j) + j * j,
    }


def six_mode_energies(j: int) -> Dict[str, Fraction]:
    """Pair energies |u_r|^2 + |u_{-r}|^2."""
    invj = Fraction(1, j)
    return {
        "p": Fraction(2),
        "q": 2 * invj,
        "k": 2 * invj,
    }


def six_mode_moments(j: int):
    """Linear moments from |u|^2.  Exact for every integer j >= 3."""
    lam = six_mode_lambdas(j)
    eng = six_mode_energies(j)
    E = X = Y = Z = Fraction(0)
    for name in ("p", "q", "k"):
        e = eng[name]
        lmb = lam[name]
        E += e
        X += lmb * e
        Y += lmb * lmb * e
        Z += lmb * lmb * lmb * e
    Lambda = Y / X
    Ds = Z - (Y * Y) / X
    return {
        "j": j,
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lambda,
        "D_s": Ds,
        "Ds_over_Lambda_Y": Ds / (Lambda * Y),
        "claimed_Ds_over_Lambda_Y_lead": Fraction(1, 4 * j),
    }


def claimed_N(j: int) -> Fraction:
    return Fraction(-2 * (2 * j + 1))


def six_mode_field(j: int) -> Field:
    """Exact Q(i) realization.  j must be a perfect square (j^{-1/2} in Q)."""
    if not _is_square(j):
        raise ValueError(f"six_mode_field requires a perfect square j; got {j}")
    s = int(math.isqrt(j))
    inv = Fraction(1, s)
    f = Field()
    f.set_mode((1, 0, 0), gq_vec((0, 1, 0)))
    f.set_mode((j, j, 0), gq_vec((0, 0, inv)))
    f.set_mode((1 + j, j, 0), vscale(I * GQ(inv), gq_vec((0, 0, 1))))
    return f


@dataclass(frozen=True)
class SixModeRow:
    j: int
    identities_ok: bool
    N: str
    claimed_N: str
    N_matches_claim: bool
    T_c: str
    Lambda: str
    D_s: str
    Ds_over_Lambda_Y: str
    claimed_lead: str
    Lambda_N_over_sqrt_YDs: str
    Q_lb_display: Optional[float]
    Q_ub_display: Optional[float]


def evaluate_square_j(j: int) -> SixModeRow:
    field = six_mode_field(j)
    report = verify_identities(field)
    mom = moments(field)
    cas = cascade(field, mom.Lambda)
    cert = certified_grad_l3(field, mom, cas)
    closed = six_mode_moments(j)
    if mom.E != closed["E"] or mom.X != closed["X"] or mom.Y != closed["Y"] or mom.D_s != closed["D_s"]:
        raise RuntimeError(f"moment mismatch at j={j}")
    claimed = claimed_N(j)
    if mom.D_s == 0 or mom.Y == 0:
        lamN_ratio = None
    else:
        # |Lambda N| / sqrt(Y Ds)  — exact square, display after sqrt
        ratio_sq = (mom.Lambda * cas.N) ** 2 / (mom.Y * mom.D_s)
        lamN_ratio = str(ratio_sq)
    Q_lb = Q_ub = None
    if cert.Q_ub_sq is not None:
        Q_ub = float(cert.Q_ub_sq) ** 0.5
    if cert.Q_lb_sixth is not None:
        Q_lb = float(cert.Q_lb_sixth) ** (1.0 / 6.0)
    return SixModeRow(
        j=j,
        identities_ok=report.ok,
        N=str(cas.N),
        claimed_N=str(claimed),
        N_matches_claim=cas.N == claimed,
        T_c=str(cas.T_c),
        Lambda=str(mom.Lambda),
        D_s=str(mom.D_s),
        Ds_over_Lambda_Y=str(closed["Ds_over_Lambda_Y"]),
        claimed_lead=str(closed["claimed_Ds_over_Lambda_Y_lead"]),
        Lambda_N_over_sqrt_YDs=lamN_ratio if lamN_ratio is not None else "vacuous",
        Q_lb_display=Q_lb,
        Q_ub_display=Q_ub,
    )


def square_j_values(max_j: int = 36) -> List[int]:
    out = []
    s = 2
    while s * s < 3:
        s += 1
    while s * s <= max_j:
        if s * s >= 3:
            out.append(s * s)
        s += 1
    return out


def fx_ingredients(j: int) -> Dict:
    """Exact (Lambda, X, Y) plus certified g^2 interval for F_X(Cs, nu).

    F_X = 2 (Cs g sqrt(Lambda) - nu Lambda)_+
    Active when g > nu sqrt(Lambda) / Cs.

    Certified:
      g^2 >= X
      g^6 <= X * ||∇u||_4^4   (square j only; moments-only j omits g_ub)
    """
    closed = six_mode_moments(j)
    out = {
        "j": j,
        "Lambda": str(closed["Lambda"]),
        "X": str(closed["X"]),
        "Y": str(closed["Y"]),
        "D_s": str(closed["D_s"]),
        "g_lb_sq": str(closed["X"]),
        "note": (
            "F_X=2(Cs g sqrt(Lambda)-nu Lambda)_+ is a proved implication, "
            "not a paid budget. Atlas can plot F_X(Cs,nu) from these ingredients."
        ),
    }
    if _is_square(j):
        field = six_mode_field(j)
        mom = moments(field)
        cas = cascade(field, mom.Lambda)
        cert = certified_grad_l3(field, mom, cas)
        out["g_ub_sixth"] = str(cert.L3_ub_sixth)
        out["L4_fourth"] = str(cert.L4_fourth)
    return out


def run_family(max_j: int = 36) -> Dict:
    squares = square_j_values(max_j)
    rows = [evaluate_square_j(j) for j in squares]
    moment_rows = [six_mode_moments(j) for j in range(3, max_j + 1)]
    # Ds/(Lambda Y) * 4j -> 1
    lead_errors = []
    for rec in moment_rows:
        j = rec["j"]
        ratio = rec["Ds_over_Lambda_Y"] / rec["claimed_Ds_over_Lambda_Y_lead"]
        lead_errors.append({"j": j, "4j_Ds_over_Lambda_Y": str(ratio)})
    return {
        "family": "p=(1,0,0), q=(j,j,0), k=p+q; u_p=e2, u_q=j^{-1/2}e3, u_k=i j^{-1/2}e3",
        "claimed_N": "N=-2(2j+1)",
        "square_j_rows": [r.__dict__ for r in rows],
        "all_N_match_claim": all(r.N_matches_claim and r.identities_ok for r in rows),
        "Ds_lead_check": lead_errors,
        "fx_ingredients": [fx_ingredients(j) for j in squares],
        "status": (
            "six-mode identities only; finite C is the smooth-split theorem, "
            "not this family. Time budget remains OPEN."
        ),
    }
