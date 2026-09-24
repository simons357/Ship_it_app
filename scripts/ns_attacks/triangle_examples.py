"""Locked finite Fourier-triangle examples and the remaining estimate.

Exact finite computations (not a close):
  - phase twins T ∈ {0, +24, −24} on the same quadratic moments
  - generated mode (3,−2,0) with B coefficient 3i e_3
  - shear field w = (sin y, sin z, sin x): E=3/2, |Π_2 B|^2=3/4, ratio 2/3
  - odd Hermitian triad: X=52A^2, Y=532A^2, T=24A^3, X'=50688 at ν=1,A=24
  - even-output polynomial and 16/9 gap
  - identity (18) on the seated moments

The missing theorem (17) is recorded as OPEN. It is not proved here.
NS is not solved.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, Iterable, List, Sequence, Tuple

from ns_attacks.fourier_triangle_geom import (
    S_pq_direct,
    S_pq_equal_formula,
    S_pq_formula,
    T_aab,
    T_abc,
    check_incompressibility,
    even_output_sum,
    polarizations,
    sixteen_ninths_gap,
    triangle_frame,
    triangle_invariants,
    unequal_defect,
)
from ns_attacks.helical import add, norm2, sub
from ns_attacks.i3_primes import report as i3_report
from ns_attacks.sign_realizability import Field, Mode, energy_sum, modal_transfers, moments

CVec = Tuple[complex, complex, complex]


def _energy(field: Field) -> float:
    return float(sum(abs(v[0]) ** 2 + abs(v[1]) ** 2 + abs(v[2]) ** 2 for v in field.values()))


def _B_hat(field: Field, k: Mode) -> CVec:
    """B̂(u,u)(k) = i P_k Σ_{p+q=k} (q·u_p) u_q. Full ordered sum."""
    acc = [0j, 0j, 0j]
    keys = list(field)
    ck = float(norm2(k))
    for p in keys:
        q = sub(k, p)
        if q not in field:
            continue
        vp = field[p]
        vq = field[q]
        qvp = q[0] * vp[0] + q[1] * vp[1] + q[2] * vp[2]
        acc[0] += qvp * vq[0]
        acc[1] += qvp * vq[1]
        acc[2] += qvp * vq[2]
    if ck == 0:
        return (0j, 0j, 0j)
    kv = k[0] * acc[0] + k[1] * acc[1] + k[2] * acc[2]
    t = kv / ck
    proj = (acc[0] - t * k[0], acc[1] - t * k[1], acc[2] - t * k[2])
    return (1j * proj[0], 1j * proj[1], 1j * proj[2])


def phase_twin_field(kind: str) -> Field:
    """u = (2 cos 2y, 0, 2 cos 3x + f(3x+2y))."""
    field: Field = {
        (0, 2, 0): (1 + 0j, 0j, 0j),
        (0, -2, 0): (1 + 0j, 0j, 0j),
        (3, 0, 0): (0j, 0j, 1 + 0j),
        (-3, 0, 0): (0j, 0j, 1 + 0j),
    }
    if kind == "cos":
        field[(3, 2, 0)] = (0j, 0j, 1 + 0j)
        field[(-3, -2, 0)] = (0j, 0j, 1 + 0j)
    elif kind == "sin":
        field[(3, 2, 0)] = (0j, 0j, -1j)
        field[(-3, -2, 0)] = (0j, 0j, 1j)
    elif kind == "msin":
        field[(3, 2, 0)] = (0j, 0j, 1j)
        field[(-3, -2, 0)] = (0j, 0j, -1j)
    else:
        raise ValueError(kind)
    return field


def phase_twin_report() -> dict:
    rows = []
    for kind, expected_T in (("cos", 0.0), ("sin", 24.0), ("msin", -24.0)):
        field = phase_twin_field(kind)
        t = modal_transfers(field)
        m = moments(field, t)
        T = sum(float(norm2(k)) * tk for k, tk in t.items())
        rows.append(
            {
                "f": kind,
                "E": _energy(field),
                "X": m["X"],
                "Y": m["Y"],
                "Z": m["Z"] if "Z" in m else None,
                "I3": energy_sum(t),
                "T": T,
                "expected_T": expected_T,
                "T_err": abs(T - expected_T),
            }
        )
    # generated mode on the cosine (zero-transfer) field
    cos = phase_twin_field("cos")
    k_gen = (3, -2, 0)
    Bgen = _B_hat(cos, k_gen)
    return {
        "rows": rows,
        "quadratic_lock": all(
            abs(r["E"] - 6) < 1e-12
            and abs(r["X"] - 52) < 1e-12
            and abs(r["Y"] - 532) < 1e-12
            and abs((r["Z"] or 0.0) - 5980) < 1e-8
            for r in rows
        ),
        "sign_lock": all(r["T_err"] < 1e-9 for r in rows),
        "energy_sum_zero": all(abs(r["I3"]) < 1e-12 for r in rows),
        "generated_mode": {
            "k": k_gen,
            "B": [complex(z) for z in Bgen],
            "matches_3i_e3": abs(Bgen[0]) < 1e-12
            and abs(Bgen[1]) < 1e-12
            and abs(Bgen[2] - 3j) < 1e-12,
        },
    }


def odd_field(A: float) -> Field:
    """Purely imaginary Hermitian triad. Invariant real-odd subspace."""
    iA = 1j * A
    return {
        (2, 0, 0): (0j, iA, 0j),
        (-2, 0, 0): (0j, -iA, 0j),
        (0, 3, 0): (0j, 0j, iA),
        (0, -3, 0): (0j, 0j, -iA),
        (2, 3, 0): (0j, 0j, iA),
        (-2, -3, 0): (0j, 0j, -iA),
    }


def odd_field_report(A: float = 24.0, nu: float = 1.0) -> dict:
    field = odd_field(A)
    t = modal_transfers(field)
    m = moments(field, t)
    T = sum(float(norm2(k)) * tk for k, tk in t.items())
    Xp = 2.0 * T - 2.0 * nu * m["Y"]
    return {
        "A": A,
        "nu": nu,
        "X": m["X"],
        "Y": m["Y"],
        "T": T,
        "X_dot": Xp,
        "X_expected": 52.0 * A * A,
        "Y_expected": 532.0 * A * A,
        "T_expected": 24.0 * A ** 3,
        "X_dot_expected": 50688.0 if abs(A - 24.0) < 1e-15 and abs(nu - 1.0) < 1e-15 else None,
        "positive_X_dot": Xp > 0,
        "phase_need_not_rotate": Xp > 0,
    }


def shear_field() -> Field:
    """w = (sin y, sin z, sin x)."""
    h = -0.5j
    hc = 0.5j
    return {
        (0, 1, 0): (h, 0j, 0j),
        (0, -1, 0): (hc, 0j, 0j),
        (0, 0, 1): (0j, h, 0j),
        (0, 0, -1): (0j, hc, 0j),
        (1, 0, 0): (0j, 0j, h),
        (-1, 0, 0): (0j, 0j, hc),
    }


def _shell(n: int) -> List[Mode]:
    out: List[Mode] = []
    r = int(math.sqrt(n)) + 2
    for i in range(-r, r + 1):
        for j in range(-r, r + 1):
            for k in range(-r, r + 1):
                if i * i + j * j + k * k == n:
                    out.append((i, j, k))
    return out


def shear_report() -> dict:
    field = shear_field()
    E = _energy(field)
    beta = 2
    coeffs = {}
    acc = 0.0
    for k in _shell(beta):
        Bk = _B_hat(field, k)
        n2 = abs(Bk[0]) ** 2 + abs(Bk[1]) ** 2 + abs(Bk[2]) ** 2
        if n2 > 1e-18:
            coeffs[str(k)] = [complex(z) for z in Bk]
            acc += n2
    # |A^{1/2} Π_β B|_2^2 / |w|_2^4
    ratio = (beta * acc) / (E ** 2) if E else 0.0
    return {
        "E": E,
        "n_nonzero_output": len(coeffs),
        "output_norm_sq": acc,
        "normalized_ratio": ratio,
        "coeffs": coeffs,
        "locks": {
            "E_3_over_2": abs(E - 1.5) < 1e-12,
            "output_3_over_4": abs(acc - 0.75) < 1e-12,
            "twelve_outputs": len(coeffs) == 12,
            "ratio_2_over_3": abs(ratio - (2.0 / 3.0)) < 1e-12,
        },
    }


def identity_1_check() -> dict:
    samples = (
        ((2, 0, 0), (0, 3, 0), 1 + 0.3j, -0.4 + 0.2j, 0.7j, 1.1),
        ((1, 1, 0), (1, -1, 1), 0.5, 0.5j, -0.2, 0.8 - 0.1j),
        ((3, 1, 1), (-1, 2, 0), 1, 0, 0, 1),  # mixed in-plane / normal
        ((1, 2, 2), (2, 1, -2), 0.2 - 0.3j, 0.4, 0.5j, -0.7),
    )
    rows = []
    for p, q, A1, A2, B1, B2 in samples:
        fr = triangle_frame(p, q)
        up, uq = polarizations(fr, A1, A2, B1, B2)
        inc = check_incompressibility(p, q, up, uq)
        Sd = S_pq_direct(p, q, up, uq)
        Sf = S_pq_formula(fr, A1, A2, B1, B2)
        err = max(abs(Sd[i] - Sf[i]) for i in range(3))
        defc = unequal_defect(p, q, up, uq)
        rows.append(
            {
                "p": p,
                "q": q,
                "S_err": err,
                "defect_err": defc["err"],
                "p_up": abs(inc["p_up"]),
                "q_uq": abs(inc["q_uq"]),
                "q_up_is_k_up": abs(inc["q_up_minus_k_up"]),
                "p_uq_is_k_uq": abs(inc["p_uq_minus_k_uq"]),
            }
        )
    return {
        "rows": rows,
        "S_identity": all(r["S_err"] < 1e-10 for r in rows),
        "defect_identity": all(r["defect_err"] < 1e-10 for r in rows),
        "div_free": all(r["p_up"] < 1e-10 and r["q_uq"] < 1e-10 for r in rows),
        "slot_identities": all(
            r["q_up_is_k_up"] < 1e-10 and r["p_uq_is_k_uq"] < 1e-10 for r in rows
        ),
    }


def identity_3_check() -> dict:
    """Equal-length: a=b=5, c=10, p=(2,1,0), q=(-1,2,0), k=(1,3,0)."""
    p, q = (2, 1, 0), (-1, 2, 0)
    fr = triangle_frame(p, q)
    assert abs(fr["a"] - fr["b"]) < 1e-12
    A1, A2, B1, B2 = 0.4 + 0.1j, 0.7, -0.2j, 0.5 - 0.3j
    up, uq = polarizations(fr, A1, A2, B1, B2)
    Sd = S_pq_direct(p, q, up, uq)
    Se = S_pq_equal_formula(fr["a"], fr["c"], A1, A2, B1, B2, fr["e2"])
    # in-plane component must vanish
    e1 = fr["e1"]
    in_plane = Sd[0] * e1[0] + Sd[1] * e1[1] + Sd[2] * e1[2]
    # purely in-plane inputs kill the normal component
    up0, uq0 = polarizations(fr, A1, 0, B1, 0)
    S0 = S_pq_direct(p, q, up0, uq0)
    return {
        "a": fr["a"],
        "c": fr["c"],
        "equal_formula_err": max(abs(Sd[i] - Se[i]) for i in range(3)),
        "in_plane_component": abs(in_plane),
        "in_plane_inputs_kill_normal": max(abs(z) for z in S0),
    }


def exact_sphere_incidence(alpha: int = 1, beta: int = 2) -> dict:
    """Small check of (8): Σ_{|k|^2=β} L_k^2 ≤ 3 F^2, r_p = 1 on the α-shell."""
    shell_a = _shell(alpha)
    r = {p: 1.0 for p in shell_a}
    F = sum(v * v for v in r.values())
    L2 = 0.0
    for k in _shell(beta):
        L = 0.0
        for p in shell_a:
            q = sub(k, p)
            if q in r:
                L += r[p] * r[q]
        L2 += L * L
    return {
        "alpha": alpha,
        "beta": beta,
        "F2": F * F,
        "sum_L2": L2,
        "bound": 3 * F * F,
        "holds": L2 <= 3 * F * F + 1e-12,
    }


def polynomial_checks() -> dict:
    even = [even_output_sum(a) for a in (1, 2, 3, 5, 8, 13)]
    # exact rational 16/9 identity on a grid
    gaps = []
    for num, den in ((0, 1), (1, 2), (1, 1), (3, 2), (2, 1), (8, 3), (4, 1)):
        r = Fraction(num, den)
        left = Fraction(16, 9) - Fraction(3, 4) * r * r * (1 - r / 4)
        right = (3 * r + 4) * (3 * r - 8) ** 2 / 144
        gaps.append({"r": f"{num}/{den}", "left": str(left), "right": str(right), "eq": left == right})
    # also float probe including non-rational
    float_ok = all(abs(sixteen_ninths_gap(x)) < 1e-12 for x in (0.0, 0.25, 0.7, 1.3, 2.0, 3.1, 4.0))
    return {
        "even_output": even,
        "even_output_exact": all(e["err"] < 1e-10 for e in even),
        "sixteen_ninths_rational": gaps,
        "sixteen_ninths_rational_exact": all(g["eq"] for g in gaps),
        "sixteen_ninths_float": float_ok,
    }


def T_grouping_checks() -> dict:
    # (6) and (7) are algebraic in the I / tau slots
    return {
        "T_aab": T_aab(5, 9, 2.0),
        "T_aab_expected": 8.0,
        "T_abc": T_abc(2, 5, 9, 1.0, -0.5, 0.25),
        "T_abc_expected": (9 - 5) * 1.0 + (2 - 9) * (-0.5) + (5 - 2) * 0.25,
    }


def centered_drift_check() -> dict:
    """Identity (18) on the sin twin: Λ' = 2/X (T_c − ν D_s)."""
    field = phase_twin_field("sin")
    t = modal_transfers(field)
    m = moments(field, t)
    nu = 1.5
    lam_dot = (2.0 / m["X"]) * (m["T_c"] - nu * m["D_s"])
    # reconstruct T_c from modal transfers
    T = sum(float(norm2(k)) * tk for k, tk in t.items())
    return {
        "X": m["X"],
        "Y": m["Y"],
        "Lambda": m["Lambda"],
        "T_c": m["T_c"],
        "D_s": m["D_s"],
        "identity_residual": m["identity_residual"],
        "T": T,
        "Lambda_dot": lam_dot,
        "D_s_nonneg": m["D_s"] >= -1e-12,
    }


def missing_theorem() -> dict:
    return {
        "label": "(17)",
        "statement": (
            "For every smooth divergence-free u0 and every nu>0 there exists "
            "finite K=K(u0,nu) such that for every finite T, "
            "sup_N S_{K,N}(T) < infinity."
        ),
        "S_definition": (
            "S_{K,N}(T) = ∫_0^T [T_sc(h_{K,N}) − nu Y_N/4]_+ / X_N dt, "
            "h = P_{|k|>K} u_N, T_sc = all-high scalene complete triads."
        ),
        "conditional_H1": (
            "X_N(t) <= X_N(0) exp[ 6 C_K sqrt(E0)/nu (1-e^{-nu T}) "
            "+ E0/(4 nu^2) + 2 S_{K,N}(T) ]."
        ),
        "status": "OPEN",
        "not_proved_here": True,
        "does_not_follow_from_I3_primes": True,
        "does_not_follow_from_one_episode": True,
        "fixed_data_S1_reported_not_rerun": {
            "nu": 1.5,
            "K": 1,
            "N2": [6, 12, 20],
            "S1": [0.001337845, 0.046918627, 0.072599898],
            "status": "NUMERICAL-reported-not-rerun",
            "three_cutoffs_do_not_prove_uniformity": True,
        },
    }


def report() -> dict:
    geom = identity_1_check()
    eq = identity_3_check()
    twins = phase_twin_report()
    odd = odd_field_report()
    shear = shear_report()
    poly = polynomial_checks()
    grp = T_grouping_checks()
    drift = centered_drift_check()
    i3 = i3_report()
    sphere = exact_sphere_incidence()
    miss = missing_theorem()
    return {
        "geometry": geom,
        "equal_length": eq,
        "phase_twins": twins,
        "odd_field": odd,
        "shear": shear,
        "polynomials": poly,
        "grouping": grp,
        "centered_drift": drift,
        "I3_primes": i3,
        "exact_sphere": sphere,
        "missing_theorem": miss,
        "board": {
            "STATIC_FRONTIER": "arithmetic sign realizability (already run; not reopened)",
            "DYNAMIC_FRONTIER": "dangerous-state persistence / scalene budget (17)",
            "I3": "lattice Gram / Hilbert local-to-global; not energy conservation alone",
            "NS_solved": False,
        },
        "locks": {
            "identity_1": geom["S_identity"],
            "identity_4": geom["defect_identity"],
            "identity_3": eq["equal_formula_err"] < 1e-10 and eq["in_plane_component"] < 1e-10,
            "phase_twins": twins["sign_lock"] and twins["quadratic_lock"],
            "generated_mode": twins["generated_mode"]["matches_3i_e3"],
            "shear": all(shear["locks"].values()),
            "odd_field": odd["positive_X_dot"],
            "even_output": poly["even_output_exact"],
            "sixteen_ninths": poly["sixteen_ninths_rational_exact"],
            "I3_regressions": i3["all_match"],
            "sphere_8": sphere["holds"],
            "theorem_17_open": miss["status"] == "OPEN",
        },
    }
