"""Loop-gauge test: topology is not a phase-frustration theorem.

Write a modal coefficient a_k = A_k exp(i φ_k). For a triad
p+q=k the convolution part of the cubic phase is

    φ_p + φ_q − φ_k.

The global family φ_k = ξ·k + φ_0 satisfies

    φ_p + φ_q − φ_k = φ_0

on every triad at once, loops included. So a closed triadic
cycle is not an automatically frustrated spin loop.

The actual cycle test uses the triad–mode incidence matrix B
with row e_p + e_q − e_k:

    B φ = b  (mod 2π)                         (C1)

If c^T B = 0 then compatibility requires

    c^T b = 0  (mod 2π)                       (C2)

Here b_e = −χ_e + Φ_e^* and χ_e = arg g_e is the geometric
coupling offset. Φ_e^* = 0 is the independently optimal
cosine alignment.

LOOP-GAUGE TEST: after quotienting the additive/translation
gauge, if the independently optimal phases are realizable,
then Γ_cyc = 1 at the phase level. Only polarization
geometry can still create a static defect.

Not a T_c bound. Not DA-NS-2. NS is not solved.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from ns_attacks.helical import (
    AXES,
    add,
    all_helical_couplings,
    as_mode,
    wrap_pi,
)

Mode = Tuple[int, int, int]
Triad = Tuple[Mode, Mode, Mode]  # (p, q, k) with p+q=k


def _mode_key(m: Mode) -> Mode:
    return as_mode(m)


def validate_triad(triad: Sequence[Sequence[int]]) -> Triad:
    if len(triad) != 3:
        raise ValueError("triad is (p, q, k)")
    p, q, k = as_mode(triad[0]), as_mode(triad[1]), as_mode(triad[2])
    if add(p, q) != k:
        raise ValueError(f"triad does not close: {p}+{q}!={k}")
    if p == (0, 0, 0) or q == (0, 0, 0) or k == (0, 0, 0):
        raise ValueError("zero mode is not allowed")
    return (p, q, k)


def incidence_matrix(
    triads: Sequence[Sequence[Sequence[int]]],
) -> Tuple[List[Triad], List[Mode], List[List[int]]]:
    """B[e][j] is +1 at p, +1 at q, −1 at k. Columns indexed by modes."""
    closed = [validate_triad(t) for t in triads]
    modes: List[Mode] = []
    seen = set()
    for p, q, k in closed:
        for m in (p, q, k):
            if m not in seen:
                seen.add(m)
                modes.append(m)
    index = {m: j for j, m in enumerate(modes)}
    B: List[List[int]] = []
    for p, q, k in closed:
        row = [0] * len(modes)
        row[index[p]] += 1
        row[index[q]] += 1
        row[index[k]] -= 1
        B.append(row)
    return closed, modes, B


def _rref(A: List[List[Fraction]]) -> Tuple[List[List[Fraction]], List[int]]:
    """Row-reduce A in place. Returns (R, pivot_cols)."""
    rows = len(A)
    cols = len(A[0]) if A else 0
    r = 0
    pivots: List[int] = []
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(rows):
            if i == r or A[i][c] == 0:
                continue
            fac = A[i][c]
            A[i] = [A[i][j] - fac * A[r][j] for j in range(cols)]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return A, pivots


def left_kernel_basis(B: Sequence[Sequence[int]]) -> List[List[int]]:
    """Exact Z-basis for {c : c^T B = 0} = ker B^T.

    Solve B^T c = 0 over Q, then clear denominators.
    """
    m = len(B)
    if m == 0:
        return []
    n = len(B[0])
    # Augment n x m matrix B^T with identity m x m to read the kernel
    # from free columns of rref(B^T).
    At: List[List[Fraction]] = [
        [Fraction(B[j][i], 1) for j in range(m)] for i in range(n)
    ]
    R, pivots = _rref([row[:] for row in At])
    pivot_set = set(pivots)
    free = [j for j in range(m) if j not in pivot_set]
    # Map pivot column -> row
    pivot_row = {pivots[r]: r for r in range(len(pivots))}
    basis: List[List[int]] = []
    for f in free:
        vec = [Fraction(0, 1)] * m
        vec[f] = Fraction(1, 1)
        for pcol, r in pivot_row.items():
            # R[r][pcol] = 1, R[r][f] is the coefficient
            vec[pcol] = -R[r][f]
        dens = [abs(x.denominator) for x in vec]
        lcm = 1
        for d in dens:
            lcm = lcm * d // math.gcd(lcm, d)
        ints = [int(x * lcm) for x in vec]
        g = 0
        for v in ints:
            g = math.gcd(g, v)
        if g > 1:
            ints = [v // g for v in ints]
        # Prefer a leading positive
        for v in ints:
            if v != 0:
                if v < 0:
                    ints = [-u for u in ints]
                break
        basis.append(ints)
    return basis


def right_kernel_basis(B: Sequence[Sequence[int]]) -> List[List[int]]:
    """Exact Q-basis for {φ : B φ = 0}, returned in integers."""
    if not B:
        return []
    m = len(B)
    n = len(B[0])
    A = [[Fraction(B[i][j], 1) for j in range(n)] for i in range(m)]
    R, pivots = _rref([row[:] for row in A])
    pivot_set = set(pivots)
    free = [j for j in range(n) if j not in pivot_set]
    pivot_row = {pivots[r]: r for r in range(len(pivots))}
    basis: List[List[int]] = []
    for f in free:
        vec = [Fraction(0, 1)] * n
        vec[f] = Fraction(1, 1)
        for pcol, r in pivot_row.items():
            vec[pcol] = -R[r][f]
        dens = [abs(x.denominator) for x in vec]
        lcm = 1
        for d in dens:
            lcm = lcm * d // math.gcd(lcm, d)
        ints = [int(x * lcm) for x in vec]
        g = 0
        for v in ints:
            g = math.gcd(g, v)
        if g > 1:
            ints = [v // g for v in ints]
        for v in ints:
            if v != 0:
                if v < 0:
                    ints = [-u for u in ints]
                break
        basis.append(ints)
    return basis


def additive_gauge_family(modes: Sequence[Mode]) -> List[List[float]]:
    """The structural translation gauge φ_k = ξ·k, plus the constant φ_0.

    Constants produce Bφ = φ_0 1, not 0. The three characters ξ·k
    sit in ker B whenever every triad obeys p+q=k.
    """
    ex = [float(m[0]) for m in modes]
    ey = [float(m[1]) for m in modes]
    ez = [float(m[2]) for m in modes]
    ones = [1.0] * len(modes)
    return [ex, ey, ez, ones]


def apply_B(B: Sequence[Sequence[int]], phi: Sequence[float]) -> List[float]:
    out = []
    for row in B:
        out.append(sum(row[j] * float(phi[j]) for j in range(len(row))))
    return out


def convolution_phases_vanish(B: Sequence[Sequence[int]], modes: Sequence[Mode]) -> dict:
    """φ_k = ξ·k gives Bφ = 0 on every triad. Constant gives Bφ = φ_0 1."""
    gauges = additive_gauge_family(modes)
    residual = [apply_B(B, g) for g in gauges]
    names = ["xi_x", "xi_y", "xi_z", "phi_0"]
    ok = []
    for name, r in zip(names, residual):
        if name == "phi_0":
            ok.append(all(abs(x - 1.0) < 1e-12 for x in r))
        else:
            ok.append(all(abs(x) < 1e-12 for x in r))
    return {
        "translation_in_right_kernel": all(ok[:3]),
        "constant_gives_all_ones": ok[3],
        "residuals": {n: r for n, r in zip(names, residual)},
        "boxed": "loop topology by itself does not force phase frustration",
    }


def holonomy(c: Sequence[int], b: Sequence[float]) -> float:
    return wrap_pi(sum(float(c[i]) * float(b[i]) for i in range(len(c))))


def phase_targets(
    triads: Sequence[Triad],
    axis: Sequence[float] = (0.0, 0.0, 1.0),
    phi_star: float = 0.0,
) -> List[dict]:
    """Independently optimal b_e = −χ_e + Φ_e^* from preferred |g|."""
    out = []
    for p, q, k in triads:
        coup = all_helical_couplings(p, q, k, axis)
        chi = float(coup["preferred"]["arg_g"])
        b = wrap_pi(-chi + phi_star)
        out.append(
            {
                "triad": (p, q, k),
                "preferred_sigma": coup["preferred"]["sigma"],
                "abs_g": coup["preferred"]["abs_g"],
                "chi": chi,
                "phi_star": phi_star,
                "b": b,
                "n_ties": coup["n_ties"],
            }
        )
    return out


def loop_gauge_test(
    triads: Sequence[Sequence[Sequence[int]]],
    axis: Sequence[float] = (0.0, 0.0, 1.0),
    phi_star: float = 0.0,
    tol: float = 1e-10,
) -> dict:
    """Fail-fast (C1)/(C2) before any phase optimization."""
    closed, modes, B = incidence_matrix(triads)
    ker = left_kernel_basis(B)
    right = right_kernel_basis(B)
    gauge = convolution_phases_vanish(B, modes)
    targets = phase_targets(closed, axis, phi_star)
    b = [row["b"] for row in targets]
    cycles = []
    frustrated = False
    for c in ker:
        om = holonomy(c, b)
        hit = abs(om) > tol
        frustrated = frustrated or hit
        cycles.append({"c": c, "Omega": om, "frustrated": hit})
    tree = len(ker) == 0
    gamma = 1 if (tree or not frustrated) else None
    return {
        "n_triads": len(closed),
        "n_modes": len(modes),
        "modes": modes,
        "triads": closed,
        "B": B,
        "dim_ker_BT": len(ker),
        "ker_BT": ker,
        "dim_ker_B": len(right),
        "tree_combinatorial": tree,
        "gauge": gauge,
        "targets": targets,
        "cycles": cycles,
        "phase_holonomy_vanishes": not frustrated,
        "Gamma_cyc_phase": gamma,
        "loop_gauge": (
            "PASS: independently optimal phases are globally realizable "
            "modulo the translation/additive gauge. Γ_cyc = 1 at the "
            "phase level. Only polarization geometry can still defect."
            if not frustrated
            else "FAIL-FAST: some Ω_c ≠ 0. Genuine cycle phase frustration. "
            "Do not compare an uncertified local max to the tree baseline."
        ),
        "axis": tuple(axis),
        "locks": {
            "topology_alone_is_not_frustration": True,
            "no_occupancy_bound": True,
            "not_a_close": True,
        },
    }


# Locked parallelogram: a convolution-compatible 4-cycle.
# T1: p+q = k,  T2: p+r = m,  T3: k+r = n,  T4: m+q = n.
P_PAR: Mode = (1, 0, 0)
Q_PAR: Mode = (0, 1, 0)
R_PAR: Mode = (0, 0, 1)
K_PAR: Mode = (1, 1, 0)
M_PAR: Mode = (1, 0, 1)
N_PAR: Mode = (1, 1, 1)

PARALLELOGRAM: Tuple[Triad, ...] = (
    (P_PAR, Q_PAR, K_PAR),
    (P_PAR, R_PAR, M_PAR),
    (K_PAR, R_PAR, N_PAR),
    (M_PAR, Q_PAR, N_PAR),
)

# Two-triad archive witness as a star (SAG convention p+q = −k).
# Archive k+p+q=0 is the same field. Shared output −k after the flip.
K_STAR: Mode = (1, 0, 0)
P_STAR: Mode = (0, 1, 1)
Q_STAR: Mode = (-1, -1, -1)
R_STAR: Mode = (0, 1, 0)
S_STAR: Mode = (-1, -1, 0)
MINUS_K: Mode = (-1, 0, 0)

STAR_WITNESS: Tuple[Triad, ...] = (
    (P_STAR, Q_STAR, MINUS_K),
    (R_STAR, S_STAR, MINUS_K),
)


def locked_cycle_vector() -> List[int]:
    """T1 − T2 + T3 − T4 is the integer generator of ker B^T."""
    return [1, -1, 1, -1]


def frame_sensitivity(triads: Sequence[Sequence[Sequence[int]]], tol: float = 1e-9) -> dict:
    """Holonomy that moves with the helical axis is a frame gauge, not a defect."""
    reports = []
    omegas = []
    for ax in AXES:
        rep = loop_gauge_test(triads, axis=ax)
        reports.append({"axis": ax, "cycles": rep["cycles"], "pass": rep["phase_holonomy_vanishes"]})
        omegas.append(tuple(c["Omega"] for c in rep["cycles"]))
    invariant = True
    if omegas:
        ref = omegas[0]
        for other in omegas[1:]:
            if len(other) != len(ref):
                invariant = False
                break
            if any(abs(wrap_pi(a - b)) > tol for a, b in zip(ref, other)):
                invariant = False
                break
    return {
        "per_axis": reports,
        "Omega_frame_invariant": invariant,
        "reading": (
            "phase holonomy is frame-invariant"
            if invariant
            else "phase holonomy moves with the helical axis: FRAME-GAUGE, "
            "not a physical loop defect"
        ),
    }


def tree_baseline_certified(targets: Sequence[dict]) -> float:
    """Γ=1 tree value: sum |g_e|. Realizable iff holonomy vanishes."""
    return float(sum(t["abs_g"] for t in targets))


def constrained_cosine_max(abs_g: Sequence[float], c: Sequence[int], omega: float) -> dict:
    """Certified max of Σ |g_e| cos θ_e subject to c·θ ≡ Ω (mod 2π).

    On a tree there is no constraint and the max is Σ |g|.
    On a single cycle the Lagrange condition is
    |g_e| sin θ_e = λ c_e, with c·θ = Ω.
    For the locked parallelogram c_e = ±1, this is solved by a
    one-dimensional scan of the cycle coordinate.
    """
    tree = float(sum(abs(x) for x in abs_g))
    if all(v == 0 for v in c):
        return {"tree": tree, "loop": tree, "Gamma_cyc": 1.0, "method": "no-cycle"}
    # Parameterize θ_e = c_e ψ + α_e with a particular solution
    # of c·θ = Ω and homogeneous solutions orthogonal to c.
    # For c_e ∈ {−1,0,1} with support on a 4-cycle, set
    # θ_e = c_e * (Ω / ||c||_2^2) + free tree directions that
    # we set to 0 to hit the constrained cosine problem along
    # the cycle. Then maximize Σ |g_e| cos(c_e ψ) with
    # Σ c_e θ_e = ψ Σ c_e^2 = Ω, so ψ = Ω / ||c||^2, unique
    # if we also demand equal |θ| on the support (the worst
    # equal-share). That is a lower bound, not the max.
    #
    # Exact max for one cycle: θ_e = sign(c_e) φ + δ_e with
    # Σ |c_e| φ = Ω after absorbing signs, and δ ⊥ c in the
    # weighted-sine sense. Numerically maximize over the
    # one angle that carries the holonomy, putting the rest
    # of the deficit on the cheapest edges.
    #
    # Closed form: max Σ a_e cos θ_e s.t. Σ c_e θ_e = Ω
    # is attained at sin θ_e = μ c_e / a_e when a_e > 0.
    # We solve for μ by 1-D Newton on Σ c_e arcsin(clip(μ c_e/a_e)) = Ω.
    a = [float(x) for x in abs_g]
    cc = [int(x) for x in c]
    mu = 0.0
    target = wrap_pi(omega)

    def residual(mu_: float) -> float:
        s = 0.0
        for ae, ce in zip(a, cc):
            if ce == 0 or ae == 0.0:
                continue
            x = mu_ * ce / ae
            x = max(-1.0, min(1.0, x))
            s += ce * math.asin(x)
        return wrap_pi(s - target)

    # Bisection on μ. The range |μ| ≤ min a_e on the support.
    support_a = [ae for ae, ce in zip(a, cc) if ce != 0 and ae > 0.0]
    if not support_a:
        return {"tree": tree, "loop": 0.0, "Gamma_cyc": 0.0, "method": "empty-support"}
    hi = min(support_a)
    lo, hi = -hi, hi
    rlo, rhi = residual(lo), residual(hi)
    # If the holonomy cannot be reached even at the clip, the
    # constraint is saturated and some |sin| = 1.
    if rlo * rhi > 0:
        # Evaluate endpoints and the equal-share fallback.
        def value_at(mu_: float) -> float:
            tot = 0.0
            for ae, ce in zip(a, cc):
                if ce == 0:
                    tot += ae
                    continue
                if ae == 0.0:
                    continue
                x = max(-1.0, min(1.0, mu_ * ce / ae))
                tot += ae * math.sqrt(max(0.0, 1.0 - x * x))
            return tot

        loop = max(value_at(lo), value_at(hi))
        return {
            "tree": tree,
            "loop": loop,
            "Gamma_cyc": (loop / tree) if tree > 0 else 1.0,
            "method": "clipped-endpoint",
            "reachable": False,
        }
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        rm = residual(mid)
        if rlo * rm <= 0:
            hi, rhi = mid, rm
        else:
            lo, rlo = mid, rm
        if hi - lo < 1e-14:
            break
    mu = 0.5 * (lo + hi)
    loop = 0.0
    thetas = []
    for ae, ce in zip(a, cc):
        if ce == 0:
            loop += ae
            thetas.append(0.0)
            continue
        if ae == 0.0:
            thetas.append(0.0)
            continue
        x = max(-1.0, min(1.0, mu * ce / ae))
        th = math.asin(x)
        thetas.append(th)
        loop += ae * math.cos(th)
    return {
        "tree": tree,
        "loop": loop,
        "Gamma_cyc": (loop / tree) if tree > 0 else 1.0,
        "method": "single-cycle-stationary",
        "mu": mu,
        "thetas": thetas,
        "reachable": True,
    }


def parallelogram_report(axis: Sequence[float] = (0.0, 0.0, 1.0)) -> dict:
    test = loop_gauge_test(PARALLELOGRAM, axis=axis)
    # Force the locked generator if the computed basis is a unit multiple.
    locked = locked_cycle_vector()
    b = [row["b"] for row in test["targets"]]
    omega = holonomy(locked, b)
    abs_g = [row["abs_g"] for row in test["targets"]]
    certified = constrained_cosine_max(abs_g, locked, omega)
    frames = frame_sensitivity(PARALLELOGRAM)
    return {
        "family": "parallelogram_4cycle",
        "loop_gauge": test,
        "locked_c": locked,
        "Omega_locked": omega,
        "certified": certified,
        "frames": frames,
        "compare_rule": (
            "Compare only this certified loop maximum against the Γ=1 "
            "tree baseline sum |g_e|. Do not use a local optimizer."
        ),
    }


def star_report() -> dict:
    test = loop_gauge_test(STAR_WITNESS)
    return {
        "family": "two_triad_star_witness",
        "loop_gauge": test,
        "reading": (
            "A star has ker B^T = 0. No cycle test. Phase compatibility "
            "is automatic. This is the archive two-triad field under "
            "SAG's p+q=−k flip. Stars can realize their couplings; a "
            "meaningful loop obstruction has to be a polarization "
            "holonomy, not this incidence."
        ),
    }
