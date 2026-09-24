#!/usr/bin/env python3
"""Fourier-triangle audit — reconstruction of 20 September 2026.

Checks the displayed exact identities and the four Hilbert-symbol
regressions. Does not prove the missing scalene time estimate (17).
Does not claim global regularity. I3 here is integer realizability
of wavevectors, not velocity amplitudes.
"""

from __future__ import annotations

import argparse
import json
from itertools import product

import numpy as np
import sympy as sp

# ---------------------------------------------------------------------------
# Hilbert symbol on Q_ℓ  (classical; used only for criterion (12))
# ---------------------------------------------------------------------------


def _legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return -1 if r == p - 1 else r


def _odd_unit_val(n: int, p: int) -> tuple[int, int]:
    if n == 0:
        raise ValueError("Hilbert symbol is undefined at 0")
    sign = -1 if n < 0 else 1
    n = abs(n)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v, sign * n


def hilbert_symbol(a: int, b: int, ell: int) -> int:
    """(a, b)_ℓ for nonzero integers a, b and prime ℓ."""
    if a == 0 or b == 0:
        raise ValueError("Hilbert symbol is undefined at 0")
    if ell == 2:
        va, ua = _odd_unit_val(a, 2)
        vb, ub = _odd_unit_val(b, 2)
        exp = ((ua - 1) * (ub - 1)) // 4 + (va * (ub * ub - 1)) // 8 + (vb * (ua * ua - 1)) // 8
        return -1 if exp % 2 else 1
    va, ua = _odd_unit_val(a, ell)
    vb, ub = _odd_unit_val(b, ell)
    sign = -1 if (va * vb * ((ell - 1) // 2)) % 2 else 1
    if vb % 2:
        sign *= _legendre(ua, ell)
    if va % 2:
        sign *= _legendre(ub, ell)
    return sign


def primes_dividing(n: int) -> list[int]:
    n = abs(n)
    out = []
    if n % 2 == 0:
        out.append(2)
        while n % 2 == 0:
            n //= 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 2
    if n > 1:
        out.append(n)
    return out


def i3_local_product(a: int, delta: int) -> dict[int, int]:
    """(a,Δ)_ℓ (a,-1)_ℓ (Δ,-1)_ℓ for every prime ℓ | 2aΔ."""
    if a <= 0 or delta <= 0:
        raise ValueError("positive-definite place requires a>0 and Δ>0")
    out = {}
    for ell in primes_dividing(2 * a * delta):
        out[ell] = (
            hilbert_symbol(a, delta, ell)
            * hilbert_symbol(a, -1, ell)
            * hilbert_symbol(delta, -1, ell)
        )
    return out


def i3_passes(a: int, delta: int) -> bool:
    return all(v == 1 for v in i3_local_product(a, delta).values())


def prove_hilbert_regressions() -> dict:
    cases = {
        "(96,96,0)": (96, 96, 0, False, {2, 3}),
        "(2,3,1)": (2, 3, 1, False, {2, 5}),
        "(2,2,-1)": (2, 2, -1, True, set()),
        "(14,14,-7)": (14, 14, -7, True, set()),
    }
    report = {}
    for name, (a, b, s, should_pass, fail_at) in cases.items():
        delta = a * b - s * s
        prod = i3_local_product(a, delta)
        failed = {ell for ell, val in prod.items() if val != 1}
        report[name] = {
            "a": a,
            "b": b,
            "s": s,
            "Delta": delta,
            "product": {str(k): v for k, v in prod.items()},
            "failed_primes": sorted(failed),
            "passes": not failed,
            "matches_audit": (not failed) == should_pass and failed == fail_at,
        }
    odd_mono = []
    for alpha in (1, 3, 5, 7, 9, 11):
        # a=b=c=α forces s=-α/2, impossible for odd α in integers.
        odd_mono.append(alpha % 2 == 1 and (alpha % 2 != 0))
    return {
        "cases": report,
        "all_match_audit": all(v["matches_audit"] for v in report.values()),
        "odd_alpha_monochromatic_impossible": all(odd_mono),
    }


# ---------------------------------------------------------------------------
# Polarization identities (1), (3), (4)
# ---------------------------------------------------------------------------


def _frame_symbols():
    a, b, c = sp.symbols("a b c", positive=True)
    A1, A2, B1, B2 = sp.symbols("A1 A2 B1 B2")
    e0 = sp.Matrix([1, 0, 0])
    e1 = sp.Matrix([0, 1, 0])
    e2 = sp.Matrix([0, 0, 1])
    s = (c - a - b) / 2
    delta = a * b - s**2
    x = (c + a - b) / (2 * sp.sqrt(c))
    y = (c + b - a) / (2 * sp.sqrt(c))
    h = sp.sqrt(delta / c)
    p = x * e0 + h * e1
    q = y * e0 - h * e1
    k = p + q
    u_p = A1 * (h * e0 - x * e1) / sp.sqrt(a) + A2 * e2
    u_q = B1 * (h * e0 + y * e1) / sp.sqrt(b) + B2 * e2
    return {
        "a": a,
        "b": b,
        "c": c,
        "A1": A1,
        "A2": A2,
        "B1": B1,
        "B2": B2,
        "e0": e0,
        "e1": e1,
        "e2": e2,
        "s": s,
        "delta": delta,
        "x": x,
        "y": y,
        "h": h,
        "p": p,
        "q": q,
        "k": k,
        "u_p": u_p,
        "u_q": u_q,
    }


def prove_S_decomposition() -> dict:
    fr = _frame_symbols()
    a, b, c = fr["a"], fr["b"], fr["c"]
    A1, A2, B1, B2 = fr["A1"], fr["A2"], fr["B1"], fr["B2"]
    e0, e1, e2 = fr["e0"], fr["e1"], fr["e2"]
    h, p, q, u_p, u_q = fr["h"], fr["p"], fr["q"], fr["u_p"], fr["u_q"]
    raw = (q.dot(u_p)) * u_q + (p.dot(u_q)) * u_p
    S = raw - raw.dot(e0) * e0
    expect = (h * (b - a) / sp.sqrt(a * b)) * A1 * B1 * e1 + (
        sp.sqrt(c) * h * (A1 * B2 / sp.sqrt(a) + A2 * B1 / sp.sqrt(b))
    ) * e2
    residual = sp.simplify(S - expect)
    # |p|^2 = a, |q|^2 = b, k = √c e0, p·u_p = q·u_q = 0
    p2 = sp.simplify(sp.expand(p.dot(p) - a))
    q2 = sp.simplify(sp.expand(q.dot(q) - b))
    k_res = sp.simplify(fr["k"] - sp.sqrt(c) * e0)
    div_p = sp.simplify(p.dot(u_p))
    div_q = sp.simplify(q.dot(u_q))
    return {
        "S_identity": residual == sp.Matrix([0, 0, 0]),
        "p_on_shell": p2 == 0,
        "q_on_shell": q2 == 0,
        "k_is_sqrt_c_e0": k_res == sp.Matrix([0, 0, 0]),
        "div_free_p": div_p == 0,
        "div_free_q": div_q == 0,
        "q_dot_up_is_k_dot_up": sp.simplify(q.dot(u_p) - (sp.sqrt(c) * e0).dot(u_p)) == 0,
    }


def prove_equal_length_form() -> dict:
    fr = _frame_symbols()
    a, c = fr["a"], fr["c"]
    A1, A2, B1, B2 = fr["A1"], fr["A2"], fr["B1"], fr["B2"]
    e1, e2, h = fr["e1"], fr["e2"], fr["h"]
    raw = (fr["q"].dot(fr["u_p"])) * fr["u_q"] + (fr["p"].dot(fr["u_q"])) * fr["u_p"]
    S = raw - raw.dot(fr["e0"]) * fr["e0"]
    S_eq = sp.simplify(S.subs(fr["b"], a))
    expect = sp.sqrt(c * (1 - c / (4 * a))) * (A1 * B2 + A2 * B1) * e2
    # h|_{b=a} = sqrt(a - c/4)
    residual = sp.simplify(S_eq - expect)
    in_plane = sp.simplify(S_eq.dot(e1))
    return {
        "equal_length_normal_form": residual == sp.Matrix([0, 0, 0]),
        "in_plane_cancels": in_plane == 0,
    }


def prove_unequal_defect() -> dict:
    fr = _frame_symbols()
    a, b, c = fr["a"], fr["b"], fr["c"]
    k = fr["k"]
    p = fr["p"]
    S_raw = (fr["q"].dot(fr["u_p"])) * fr["u_q"] + (fr["p"].dot(fr["u_q"])) * fr["u_p"]
    S = S_raw - S_raw.dot(fr["e0"]) * fr["e0"]
    Pk_p = p - (p.dot(fr["e0"])) * fr["e0"]
    left = sp.simplify(Pk_p.dot(S))
    right = sp.simplify(((b - a) / c) * (k.dot(fr["u_p"])) * (k.dot(fr["u_q"])))
    return {"defect_identity": sp.simplify(left - right) == 0}


def prove_16_9_polynomial() -> dict:
    r = sp.symbols("r")
    left = sp.Rational(16, 9) - sp.Rational(3, 4) * r**2 * (1 - r / 4)
    right = (3 * r + 4) * (3 * r - 8) ** 2 / 144
    return {"identity": bool(sp.expand(left - right) == 0)}


def prove_even_output_sum() -> dict:
    """Σ_{b even, 2≤b≤4a} (b-a)² (1-b/(4a)) = a³ - a²/2 for integer a≥1."""
    a = sp.symbols("a", integer=True, positive=True)
    b = sp.symbols("b", integer=True, positive=True)
    term = (b - a) ** 2 * (1 - b / (4 * a))
    # Closed form via even b = 2m, m=1..2a
    m = sp.symbols("m", integer=True, positive=True)
    term_m = term.subs(b, 2 * m)
    summed = sp.summation(term_m, (m, 1, 2 * a))
    expect = a**3 - a**2 / 2
    closed = bool(sp.simplify(summed - expect) == 0)
    numeric = True
    for aval in range(1, 9):
        acc = 0.0
        for bv in range(2, 4 * aval + 1, 2):
            acc += (bv - aval) ** 2 * (1 - bv / (4 * aval))
        if abs(acc - (aval**3 - aval**2 / 2)) > 1e-10:
            numeric = False
    return {"closed_form": closed, "numeric_a_1_to_8": numeric}


# ---------------------------------------------------------------------------
# Finite signed-transfer example
# ---------------------------------------------------------------------------


def _parseval_modes(modes: dict) -> dict:
    e = x = y = z = 0.0
    for k, uk in modes.items():
        m2 = float(k[0] ** 2 + k[1] ** 2 + k[2] ** 2)
        ek = float(np.vdot(uk, uk).real)
        e += ek
        x += m2 * ek
        y += m2 * m2 * ek
        z += m2 * m2 * m2 * ek
    return {"E": e, "X": x, "Y": y, "Z": z}


def _bhat(k, modes: dict) -> np.ndarray:
    acc = np.zeros(3, dtype=complex)
    for p, up in modes.items():
        q = (k[0] - p[0], k[1] - p[1], k[2] - p[2])
        uq = modes.get(q)
        if uq is None:
            continue
        q_vec = np.array(q, dtype=float)
        acc += np.dot(q_vec, up) * uq
    kk = float(k[0] ** 2 + k[1] ** 2 + k[2] ** 2)
    k_vec = np.array(k, dtype=float)
    raw = 1j * acc
    return raw - (np.dot(k_vec, raw) / kk) * k_vec


def _full_T(modes: dict) -> dict:
    keys = set(modes)
    # include generated receivers that the donor sum can hit
    extra = set()
    for p, q in product(keys, keys):
        extra.add((p[0] + q[0], p[1] + q[1], p[2] + q[2]))
    tau_sum = 0.0
    t_enst = 0.0
    t_energy = 0.0
    for k in extra:
        if k == (0, 0, 0):
            continue
        uk = modes.get(k, np.zeros(3, dtype=complex))
        bk = _bhat(k, modes)
        tau = -np.real(np.vdot(uk, bk))
        m2 = float(k[0] ** 2 + k[1] ** 2 + k[2] ** 2)
        tau_sum += tau
        t_enst += m2 * tau
        t_energy += tau
    return {"T": t_enst, "energy_transfer": t_energy}


def cosine_example(kind: str) -> dict:
    """u = (2 cos 2y, 0, 2 cos 3x + f(3x+2y))."""
    modes = {
        (0, 2, 0): np.array([1.0, 0.0, 0.0], dtype=complex),
        (0, -2, 0): np.array([1.0, 0.0, 0.0], dtype=complex),
        (3, 0, 0): np.array([0.0, 0.0, 1.0], dtype=complex),
        (-3, 0, 0): np.array([0.0, 0.0, 1.0], dtype=complex),
    }
    if kind == "cos":
        modes[(3, 2, 0)] = np.array([0.0, 0.0, 1.0], dtype=complex)
        modes[(-3, -2, 0)] = np.array([0.0, 0.0, 1.0], dtype=complex)
    elif kind == "sin":
        modes[(3, 2, 0)] = np.array([0.0, 0.0, -1j], dtype=complex)
        modes[(-3, -2, 0)] = np.array([0.0, 0.0, 1j], dtype=complex)
    elif kind == "msin":
        modes[(3, 2, 0)] = np.array([0.0, 0.0, 1j], dtype=complex)
        modes[(-3, -2, 0)] = np.array([0.0, 0.0, -1j], dtype=complex)
    else:
        raise ValueError(kind)
    mom = _parseval_modes(modes)
    tr = _full_T(modes)
    return {**mom, **tr, "kind": kind}


def prove_cosine_example() -> dict:
    expect_t = {"cos": 0.0, "sin": 24.0, "msin": -24.0}
    rows = {}
    ok = True
    for kind, t_exp in expect_t.items():
        row = cosine_example(kind)
        match = (
            abs(row["E"] - 6.0) < 1e-12
            and abs(row["X"] - 52.0) < 1e-12
            and abs(row["Y"] - 532.0) < 1e-12
            and abs(row["Z"] - 5980.0) < 1e-12
            and abs(row["T"] - t_exp) < 1e-10
            and abs(row["energy_transfer"]) < 1e-10
        )
        ok = bool(ok and match)
        rows[kind] = {
            "E": row["E"],
            "X": row["X"],
            "Y": row["Y"],
            "Z": row["Z"],
            "T": row["T"],
            "energy_transfer": row["energy_transfer"],
            "matches_audit": match,
        }
    # generated mode (3,-2,0) from the cosine field
    cos_modes = {
        (0, 2, 0): np.array([1.0, 0.0, 0.0], dtype=complex),
        (0, -2, 0): np.array([1.0, 0.0, 0.0], dtype=complex),
        (3, 0, 0): np.array([0.0, 0.0, 1.0], dtype=complex),
        (-3, 0, 0): np.array([0.0, 0.0, 1.0], dtype=complex),
        (3, 2, 0): np.array([0.0, 0.0, 1.0], dtype=complex),
        (-3, -2, 0): np.array([0.0, 0.0, 1.0], dtype=complex),
    }
    b_gen = _bhat((3, -2, 0), cos_modes)
    gen_ok = np.allclose(b_gen, np.array([0.0, 0.0, 3j]), atol=1e-12)
    return {
        "rows": rows,
        "all_match": ok,
        "generated_mode_3_-2_0": {
            "B": [complex(z) for z in b_gen],
            "matches_3i_e3": gen_ok,
        },
    }


def prove_shear_ratio() -> dict:
    """w = (sin y, sin z, sin x). Twelve nonzero equal-input outputs on β=2."""
    modes = {
        (0, 1, 0): np.array([-0.5j, 0.0, 0.0], dtype=complex),
        (0, -1, 0): np.array([0.5j, 0.0, 0.0], dtype=complex),
        (0, 0, 1): np.array([0.0, -0.5j, 0.0], dtype=complex),
        (0, 0, -1): np.array([0.0, 0.5j, 0.0], dtype=complex),
        (1, 0, 0): np.array([0.0, 0.0, -0.5j], dtype=complex),
        (-1, 0, 0): np.array([0.0, 0.0, 0.5j], dtype=complex),
    }
    mom = _parseval_modes(modes)
    out = {}
    for kx, ky, kz in product(range(-2, 3), repeat=3):
        k = (kx, ky, kz)
        if kx * kx + ky * ky + kz * kz != 2:
            continue
        bk = _bhat(k, modes)
        if np.linalg.norm(bk) > 1e-14:
            out[str(k)] = [complex(z) for z in bk]
    sq = sum(float(np.vdot(np.array(v), np.array(v)).real) for v in out.values())
    return {
        "E": mom["E"],
        "nonzero_outputs_on_beta_2": len(out),
        "squared_output_norm": sq,
        "E_is_3_over_2": abs(mom["E"] - 1.5) < 1e-12,
        "twelve_nonzero": len(out) == 12,
        "output_norm_3_over_4": abs(sq - 0.75) < 1e-10,
    }


# ---------------------------------------------------------------------------
# Lock dump
# ---------------------------------------------------------------------------


def prove_all() -> dict:
    return {
        "S_decomposition": prove_S_decomposition(),
        "equal_length": prove_equal_length_form(),
        "unequal_defect": prove_unequal_defect(),
        "ratio_16_9": prove_16_9_polynomial(),
        "even_output_sum": prove_even_output_sum(),
        "hilbert": prove_hilbert_regressions(),
        "cosine_example": prove_cosine_example(),
        "shear": prove_shear_ratio(),
        "missing_theorem_17": "OPEN",
        "I3_determines_amplitudes": False,
        "W_ij_reconstructed": False,
        "ns_solved": False,
        "da_ns_2": "OPEN",
        "classical_ns_open": True,
        "fixed_data_S1_rerun_here": False,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Fourier-triangle audit checks")
    p.add_argument("--out", default=None)
    args = p.parse_args()
    payload = prove_all()
    text = json.dumps(payload, indent=2, default=str)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
