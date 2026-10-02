#!/usr/bin/env python3
"""L3 budget gates: scaling, Young, Bernstein, locks.

(L3-1) is classical Hölder+Sobolev. (L3-5) is not proved.
NS is not solved.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import isqrt


def holder_exponents() -> dict:
    """1/2 = 1/3 + 1/6."""
    return {
        "l2_inv": Fraction(1, 2),
        "l3_inv": Fraction(1, 3),
        "l6_inv": Fraction(1, 6),
        "sum": Fraction(1, 3) + Fraction(1, 6),
        "ok": Fraction(1, 3) + Fraction(1, 6) == Fraction(1, 2),
    }


def serrin_endpoint_p(q: int) -> Fraction | None:
    """2/p + 3/q = 1. At q=3 this forces p=∞ (no finite p)."""
    # 2/p = 1 - 3/q = (q-3)/q  ⇒ p = 2q/(q-3) for q>3
    if q <= 3:
        return None
    return Fraction(2 * q, q - 3)


def young_rep_split(X: Fraction, Y: Fraction, nu: Fraction) -> bool:
    """(√3/2) X √Y ≤ (ν/8) Y + (3/(2ν)) X²."""
    # Avoid the outer square root: compare after the ε=ν/4 Young form.
    # (√3/2) X √Y ≤ (ν/8) Y + (3/(2ν)) X²
    # ⇔ 3 X² Y ≤ 4 ( (ν/8) Y + 3X²/(2ν) )²
    left = 3 * X * X * Y
    right_half = nu * Y / 8 + (3 * X * X) / (2 * nu)
    return left <= 4 * right_half * right_half


def bernstein_H12(eigs: list[int], mass: list[Fraction], K: int) -> dict:
    """On |k| > K, ||h||_{Ḣ^{1/2}}^2 = ∑ |k| m ≤ X_h / min|k|."""
    min_r = None
    H12 = Fraction(0)
    Xh = Fraction(0)
    for lam, m in zip(eigs, mass):
        r = isqrt(lam)
        if r * r != lam:
            raise ValueError("need perfect-square shells for exact |k|")
        if r <= K:
            continue
        Xh += lam * m
        H12 += r * m
        min_r = r if min_r is None else min(min_r, r)
    bound = Fraction(0) if Xh == 0 else Xh / min_r
    return {
        "Xh": Xh,
        "H12": H12,
        "bound": bound,
        "ok": H12 <= bound,
        "min_r": min_r,
    }


def gn_ratio_fourier(eigs: list[int], mass: list[Fraction]) -> Fraction:
    """Critical interpolation proxy: (∑ |k| m)^2 / (E X) ≤ 1 by CS.

    ||u||_{Ḣ^{1/2}}^2 = ∑ |k| m, E=∑ m, X=∑ |k|² m.
    Cauchy–Schwarz: (∑ |k| m)^2 ≤ (∑ m)(∑ |k|² m) = E X.
    The Sobolev map ||u||_3 ≤ C ||u||_{Ḣ^{1/2}} then yields ||u||_3^4 ≤ C' E X.
    """
    E = sum(mass)
    X = sum(lam * m for lam, m in zip(eigs, mass))
    H12 = sum(isqrt(lam) * m for lam, m in zip(eigs, mass))
    return (H12 * H12) / (E * X)


def l3_5_not_serrin() -> dict:
    """(L3-5) weights L^3 excess by Λ. That is not L^p_t L^3_x."""
    return {
        "serrin_q3_finite_p": serrin_endpoint_p(3) is None,
        "l3_5_carries_Lambda": True,
        "equivalent_to_17": True,
    }


def report() -> dict:
    h = holder_exponents()
    p4 = serrin_endpoint_p(4)
    p6 = serrin_endpoint_p(6)
    p3 = serrin_endpoint_p(3)
    # two-shell high field: radii 2 and 3, K=1
    eigs = [4, 9]
    mass = [Fraction(1, 2), Fraction(1, 3)]
    bern = bernstein_H12(eigs, mass, K=1)
    gn = gn_ratio_fourier([1, 4, 9], [Fraction(1), Fraction(1, 2), Fraction(1, 4)])
    young_ok = young_rep_split(Fraction(52), Fraction(532), Fraction(3, 2))
    return {
        "holder": {k: str(v) if isinstance(v, Fraction) else v for k, v in h.items()},
        "serrin": {
            "q3_finite_p": p3,
            "q4": str(p4),
            "q6": str(p6),
            "q4_is_8": p4 == 8,
            "q6_is_4": p6 == 4,
        },
        "bernstein": {
            "Xh": str(bern["Xh"]),
            "H12": str(bern["H12"]),
            "bound": str(bern["bound"]),
            "ok": bern["ok"],
        },
        "gn_cs": str(gn),
        "gn_cs_le_1": gn <= 1,
        "young_ok": young_ok,
        "l3_5": l3_5_not_serrin(),
        "locks": {
            "not_a_close": True,
            "l3_1_classical": True,
            "l3_5_proved": False,
            "theorem_17_proved": False,
            "not_beyond_ESS": True,
            "no_novelty": True,
            "lemma_A_unaltered": True,
            "sign_gate_unaltered": True,
        },
    }


def main(argv=None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    print(json.dumps(report(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
