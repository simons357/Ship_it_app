#!/usr/bin/env python3
"""
Score SuperGrok's 11 September analytic review of the cube family.

Recomputes the continuum quadratic moments of F on [-1,1]^3
with exact fractions. Does not import a missing hexagon file.
Does not stamp a kill. NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from track_b_lemmas import rec  # noqa: E402

# |F(ξ)|² = ξ1^8 + ξ1^6 ξ2² + ξ1^4 ξ2² + ξ1² ξ2^4
# F(ξ) = ξ1(-ξ1² + i ξ2)(-ξ2, ξ1, 0),  ξ ∈ [-1,1]³.


def _I(p: int) -> Fraction:
    if p % 2 == 1:
        return Fraction(0)
    return Fraction(2, p + 1)


def _mom_F2(a: int, b: int) -> Fraction:
    terms = ((8, 0), (6, 2), (4, 2), (2, 4))
    return sum((_I(p + a) * _I(q + b) for p, q in terms), Fraction(0))


def _int_xi2m_F2(m: int) -> Fraction:
    total = Fraction(0)
    for i in range(m + 1):
        for j in range(m - i + 1):
            k = m - i - j
            coef = math.comb(m, i) * math.comb(m - i, j)
            total += coef * _I(2 * k) * _mom_F2(2 * i, 2 * j)
    return total


E0 = 2 * _mom_F2(0, 0)
X0 = _int_xi2m_F2(1)
Y0 = _int_xi2m_F2(2)
Z0 = _int_xi2m_F2(3)
LAM0 = Y0 / X0
D0 = Z0 - Y0 * Y0 / X0

M0_CLAIMED = Fraction(89567, 134534400)
C_BOX_FROM_M0 = (M0_CLAIMED * M0_CLAIMED) / (D0 * E0 * Y0)

# Previous dump OCR.
L0_REPORTED = Fraction(7360, 315)
LAM0_REPORTED = Fraction(2854451, 1653661)
D0_REPORTED = Fraction(87136986657536, 1173133320108875)
C_BOX_FRACTION_OCR = Fraction(
    1523085778924828999575, 3839130303817223093956294737922
)
C_BOX_FLOAT_REVIEW = 3.967267736160021e-8

# Locked discrete samples already computed with ns_lemma_star_core.
LOCKED_TC_OVER_N2 = {
    2: 0.037834167480468736,
    3: 0.015218074276339533,
    4: 0.007750106349703872,
    5: 0.004973097437587313,
    6: 0.003649299113331108,
    7: 0.002906970015410098,
}
LOCKED_R_OVER_N3 = {
    2: 1.0078040091368528e-07,
    3: 1.0585106020575111e-07,
    4: 8.21135406702495e-08,
    5: 6.940234200780329e-08,
    6: 6.212319070051957e-08,
    7: 5.753905697355065e-08,
}


def continuum() -> dict:
    return {
        "E0": str(E0),
        "X0": str(X0),
        "Y0": str(Y0),
        "Z0": str(Z0),
        "Lambda0": str(LAM0),
        "D0": str(D0),
        "E0_float": float(E0),
        "X0_float": float(X0),
        "Y0_float": float(Y0),
        "Z0_float": float(Z0),
        "Lambda0_float": float(LAM0),
        "D0_float": float(D0),
        "M0_claimed": str(M0_CLAIMED),
        "M0_claimed_float": float(M0_CLAIMED),
        "c_box_from_M0": str(C_BOX_FROM_M0),
        "c_box_from_M0_float": float(C_BOX_FROM_M0),
        "L0_reported": str(L0_REPORTED),
        "L0_is_10_E0": L0_REPORTED == 10 * E0,
        "L1_matches_X0": X0 == Fraction(21536, 5775),
        "L2_matches_Y0": Y0 == Fraction(91342432, 14189175),
        "L3_matches_Z0": Z0 == Fraction(280364512, 23648625),
        "Lambda0_reported_typo": LAM0_REPORTED != LAM0,
        "D0_reported_near_tenth": abs(float(D0) / float(D0_REPORTED) - 10.0) < 1e-8,
        "ocr_fraction_times_100": abs(float(100 * C_BOX_FRACTION_OCR) - float(C_BOX_FROM_M0))
        < 1e-20,
        "review_float_matches_corrected": abs(float(C_BOX_FROM_M0) - C_BOX_FLOAT_REVIEW)
        < 1e-20,
    }


def lemmas(cont: dict) -> list[dict]:
    n7 = LOCKED_TC_OVER_N2[7]
    m0 = float(M0_CLAIMED)
    return [
        rec(
            "LSrev_files_on_branch",
            "Lemma_Star_Analytic_Review_2026-09-11.md and verify_box_integrals.py are on this branch",
            "fail",
            "Attachment marks only. Same class as the missing Finite_Lattice file.",
        ),
        rec(
            "LSrev_quad_moments",
            "continuum E0,X0,Y0,Z0,D0 of |F|^2 on [-1,1]^3",
            "pass" if cont["L1_matches_X0"] and cont["L2_matches_Y0"] and cont["L3_matches_Z0"] else "fail",
            "Exact fractions. L1=X0, L2=Y0, L3=Z0. L0 reported 10 E0.",
            E0=cont["E0"],
            D0=cont["D0"],
        ),
        rec(
            "LSrev_reported_constants_clean",
            "every reported constant matches with no digit defects",
            "fail",
            "L0 extra zero. Lambda0 denom 1653661 vs 1653561. D0 denom 10x. Old c_box fraction /100.",
        ),
        rec(
            "LSrev_N0_discrete",
            "N=0 on the locked cube samples",
            "pass",
            "Even n exact 0. Odd n at 1e-17. Not a continuum hexagon expansion.",
        ),
        rec(
            "LSrev_M0_from_lock",
            "locked Tc/n^2 has settled at 89567/134534400",
            "fail",
            "n=7 gives 0.00291 vs M0=0.000666 (4.4x). Linear intercept of Tc/n^2 is negative.",
            Tc_over_n2_n7=n7,
            M0=m0,
            ratio=n7 / m0,
        ),
        rec(
            "LSrev_no_defect_35",
            "no defect in §§3–5 of a manuscript on this branch",
            "fail",
            "Those sections are not here. Polyhedral O(1/n) for |F|^2 is not a triad theorem.",
        ),
        rec(
            "LSrev_samples_unnecessary",
            "larger locked samples are unnecessary for the inference",
            "fail",
            "Through n=7 the T_c leading term is not dominant. R★/n³ is 1.45x the claimed c_box.",
            R_over_n3_n7=LOCKED_R_OVER_N3[7],
            c_box=float(C_BOX_FROM_M0),
        ),
        rec(
            "LSrev_unrestricted_killed",
            "unrestricted Lemma★ is killed",
            "fail",
            "Asymptotic implication is as strong as M0 plus a remainder theorem. Neither is locked. ★ OPEN.",
        ),
        rec(
            "LSrev_ns_h1",
            "review solves NS or starts H1",
            "fail",
            "Not a trajectory. Not WRITE (6). ★ ⇒ GR still one way.",
        ),
    ]


def run(out: Path | None = None) -> dict:
    cont = continuum()
    rows = lemmas(cont)
    counts = {"pass": 0, "fail": 0, "open": 0}
    for item in rows:
        counts[item["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "Lemma★ cube analytic review against the lock",
            "tuning_the_pde": False,
            "lemma_star_open": True,
            "h1_started": False,
            "files_on_branch": False,
            "kill": False,
        },
        "continuum": cont,
        "locked_Tc_over_n2": LOCKED_TC_OVER_N2,
        "locked_R_over_n3": LOCKED_R_OVER_N3,
        "lemmas": rows,
        "counts": counts,
        "domain_verdict": "open",
    }
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    print(json.dumps(run(out=args.out), indent=2))


if __name__ == "__main__":
    main()
