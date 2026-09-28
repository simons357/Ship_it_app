"""Sprint 02 two-triad charge/covariance strike.

Connected heterochiral component with Q_{a,Γ}=0 and T_c^{het}>0.
Charge-only coercivity is false; the gap/covariance remainder is
structurally necessary. Not DA-NS-2. NS is not solved.
"""

from __future__ import annotations

import math
from typing import Dict

from ns_attacks.fourier import Mode, nrm2


K: Mode = (1, 0, 0)
P: Mode = (0, 1, 1)
Q: Mode = (-1, -1, -1)
R: Mode = (0, 1, 0)
S: Mode = (-1, -1, 0)


def det3(a: Mode, b: Mode, c: Mode) -> int:
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def charge_covariance() -> Dict[str, float]:
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
    two_k3 = 2.0 * kappa ** 3
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
        "rho": rho,
        "two_kappa_cubed": two_k3,
        "det_kpr": float(det3(K, P, R)),
        "rank_three": float(det3(K, P, R) != 0),
        "sum1": float(sum(K[i] + P[i] + Q[i] for i in range(3))),
        "sum2": float(sum(K[i] + R[i] + S[i] for i in range(3))),
        "len_k": math.sqrt(nrm2(K)),
        "len_p": math.sqrt(nrm2(P)),
        "len_q": math.sqrt(nrm2(Q)),
        "len_r": math.sqrt(nrm2(R)),
        "len_s": math.sqrt(nrm2(S)),
    }


def second_witness() -> Dict[str, float]:
    """Archive numerical checkpoint: negative net charge, negative common
    multiplier, positive centered drift. Not re-derived here."""
    return {
        "R_1": -60.7616659871,
        "R_2": -60.7616659871,
        "Q_a_Gamma": -21.9024889809,
        "T_c_het_Gamma": 1330.83171974,
        "common_multiplier_negative": 1.0,
        "net_charge_negative": 1.0,
        "centered_positive": 1.0,
    }
