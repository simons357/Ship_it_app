#!/usr/bin/env python3
"""Direct arithmetic test of the boxed SND persistence statement (P).

(P)  X(t) ≤ M and ρ(0) ≥ ρ_*  ⇒?  ρ(t) ≥ ρ_*/2
     for 0 ≤ t ≤ T(M, ν, ρ_*), with T independent of j_*(0).

Do not repair Theorem H. A.2 is retained. A.3 is the wrong Dini side.

This script checks three things:

1. Indexed LH / HL / HH ranges exhaust the shell index set.
2. Closing a lower comparison with A.2 leaves an unbounded 4^{j_*} factor.
3. Family H (unforced shears, F_j ≡ 0, high peak) falsifies (P) for every
   ρ_* ∈ (0, 1): for any candidate T(M, ν, ρ_*), a high enough peak makes
   ρ dip below ρ_*/2 while X stays ≤ M. The dip is the intermediate
   plateau 1/(L−1) after the high mode dies and before the lower block
   differentiates. As t → ∞, ρ recovers toward 1 (lowest shell); (P)
   already failed at the dip.

Family H does not kill (P) at the endpoint ρ_* = 1 (single occupied shell,
heat preserves ρ = 1). That is a different statement. Do not relabel it as (P).

High-tail shears (low peak + one high shell) do not kill (P): the high
shell dies first and ρ increases.

Run:  python3 scripts/snd_persistence_test.py
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from typing import Iterable


# ---------------------------------------------------------------------------
# Indexed paraproduct
# ---------------------------------------------------------------------------

def paraproduct_buckets(
    j: int, n: int, k_min: int, k_max: int
) -> tuple[list[int], list[int], list[int]]:
    """Low-high / high-low / high-high in the inner factor Δ_k u, overlap N."""
    if n < 2:
        raise ValueError("overlap N must be ≥ 2")
    ks = range(k_min, k_max + 1)
    lh = [k for k in ks if k <= j - n]
    hl = [k for k in ks if k >= j + n]
    hh = [k for k in ks if abs(k - j) < n]
    return lh, hl, hh


def assert_paraproduct_exhausts() -> None:
    """The three k-ranges partition {k_min, …, k_max} for every tested (j, N)."""
    for n in (2, 4):
        for k_min, k_max in ((-8, 8), (0, 16), (-3, 21)):
            universe = list(range(k_min, k_max + 1))
            for j in universe:
                lh, hl, hh = paraproduct_buckets(j, n, k_min, k_max)
                union = sorted(lh + hl + hh)
                if union != universe:
                    raise AssertionError(
                        f"LH/HL/HH miss or overlap at j={j}, N={n}: {union}"
                    )
                if len(lh) + len(hl) + len(hh) != len(universe):
                    raise AssertionError(f"duplicate k at j={j}, N={n}")
                if set(lh) & set(hl) or set(lh) & set(hh) or set(hl) & set(hh):
                    raise AssertionError(f"range overlap at j={j}, N={n}")


# ---------------------------------------------------------------------------
# A.2 leftover
# ---------------------------------------------------------------------------

def a2_drain_over_peak_viscosity(
    j_star: int, *, m: float, nu: float, rho: float, x: float, kappa: float = 1.0
) -> float:
    """Ratio of the A.2 drain 4^{j}|F_j| to peak viscosity, using Bernstein on D.

    A.2: |F_j| ≤ C √(M/(ν λ_1)) X^{1/2} D^{1/2}, uniform in j (C, λ_1 absorbed
    as 1). On a high peak, D ≳ ν κ 4^{j_*} J, so

        4^{j_*} |F_j| / (ν 4^{j_*} J)  ≳  4^{j_*/2} · (√(M X) √κ) / (ν √(ρ) X)

    which grows without bound in j_* at fixed (M, ν, ρ, X).
    """
    # Lower-bound the A.2 size by inserting the peak's own dissipation.
    d_peak = nu * kappa * (4**j_star) * (rho * x)
    f_size = math.sqrt(m / nu) * math.sqrt(x * d_peak)
    drain = (4**j_star) * f_size
    visc = nu * kappa * (4**j_star) * (rho * x)
    return drain / visc


def assert_a2_leftover_unbounded() -> None:
    m, nu, rho, x = 1.0, 1.0, 0.5, 1.0
    ratios = [
        a2_drain_over_peak_viscosity(j, m=m, nu=nu, rho=rho, x=x)
        for j in (4, 8, 12, 16)
    ]
    for earlier, later in zip(ratios, ratios[1:]):
        if later <= earlier * 3:
            raise AssertionError(
                f"A.2 leftover did not grow like 4^{{j_*/2}}: {ratios}"
            )
    # Explicit 4^{j_*} prefactor on a j-independent |F_j| bound.
    leftover = [4**j for j in (4, 8, 12, 16)]
    if not leftover[0] < leftover[1] < leftover[2] < leftover[3]:
        raise AssertionError("4^{j_*} leftover is not strictly increasing")


# ---------------------------------------------------------------------------
# Heat shears (F ≡ 0)
# ---------------------------------------------------------------------------

def choose_L(rho_star: float) -> int:
    """L ≥ 3 with unique high max at t = 0 and plateau 1/(L−1) < ρ_*/2."""
    if not 0.0 < rho_star < 1.0:
        raise ValueError("Family H needs ρ_* ∈ (0, 1)")
    l = 3
    while l < 10_000:
        plateau = 1.0 / (l - 1)
        unique_max = rho_star > 1.0 / l
        if plateau < 0.5 * rho_star and unique_max:
            return l
        l += 1
    raise RuntimeError("no L found")


def family_h(rho_star: float, q: float, k: int, l: int | None = None) -> dict[int, float]:
    """Enstrophy by shell. Peak at K, equal remainder on 1…L−1."""
    l = choose_L(rho_star) if l is None else l
    if k <= l - 1:
        raise ValueError("K must sit above the lower block")
    a = rho_star * q
    b = (1.0 - rho_star) * q / (l - 1)
    shells = {k: a}
    for ell in range(1, l):
        shells[ell] = b
    return shells


def family_high_tail(rho_star: float, q: float, k: int) -> dict[int, float]:
    """Low peak at shell 1 plus one high tail at K. Does not kill (P)."""
    return {1: rho_star * q, k: (1.0 - rho_star) * q}


def heat(shells: dict[int, float], nu: float, t: float) -> dict[int, float]:
    out: dict[int, float] = {}
    for j, x0 in shells.items():
        expo = -2.0 * nu * float(4**j) * t
        out[j] = 0.0 if expo < -745.0 else x0 * math.exp(expo)
    return out


def rho_of(shells: dict[int, float]) -> tuple[float, float, float, int]:
    x = sum(shells.values())
    if x <= 0.0:
        raise ValueError("X = 0")
    j_star = max(shells, key=lambda j: shells[j])
    jval = shells[j_star]
    return jval / x, x, jval, j_star


def sample_times(t_max: float, n: int = 800) -> list[float]:
    if t_max <= 0.0:
        return [0.0]
    log_min = math.log(t_max / 1.0e12)
    log_max = math.log(t_max)
    ts = [0.0]
    ts.extend(
        math.exp(log_min + (log_max - log_min) * i / (n - 1)) for i in range(n)
    )
    ts.append(t_max)
    return ts


@dataclass(frozen=True)
class Trajectory:
    t: list[float]
    rho: list[float]
    x: list[float]
    j_star: list[int]


def trajectory(shells0: dict[int, float], nu: float, t_max: float) -> Trajectory:
    ts = sample_times(t_max)
    rhos: list[float] = []
    xs: list[float] = []
    js: list[int] = []
    kept_t: list[float] = []
    for t in ts:
        heated = heat(shells0, nu, t)
        if sum(heated.values()) <= 0.0:
            # Total dissipation: ρ is undefined. A single decaying shell
            # keeps ρ = 1 until this underflow.
            if not rhos:
                r0, x0, _, j0 = rho_of(shells0)
                kept_t, rhos, xs, js = [0.0], [r0], [x0], [j0]
            break
        r, x, _, j = rho_of(heated)
        kept_t.append(t)
        rhos.append(r)
        xs.append(x)
        js.append(j)
    return Trajectory(t=kept_t, rho=rhos, x=xs, j_star=js)


def min_rho_on(traj: Trajectory, t_hi: float) -> tuple[float, float]:
    best = (traj.rho[0], traj.t[0])
    for t, r in zip(traj.t, traj.rho):
        if t <= t_hi and r < best[0]:
            best = (r, t)
    return best


def dminus_rho_floor_f0(
    shells: dict[int, float], nu: float
) -> tuple[float, float]:
    """Correctly oriented lower Dini bound at a unique peak, F_j ≡ 0.

    D_- J ≥ min_{argmax} Ẋ_j = −2ν 4^{j_*} J,
    Ẋ = −2ν ∑ 4^j X_j ≤ 0, so −ρ D^+ X / X ≥ 0, and

        D_- ρ  ≥  D_-J / X − ρ D^+X / X
               = −2ν 4^{j_*} ρ − ρ Ẋ / X.

    The floor is correctly sided and ~ −2ν 4^{j_*} ρ(1−ρ) when the rest of
    the mass is at much lower frequency. Unbounded in j_* at fixed (M, ν, ρ).
    """
    r, x, jval, j_star = rho_of(shells)
    xdot = -2.0 * nu * sum(float(4**j) * xj for j, xj in shells.items())
    dminus_j = -2.0 * nu * float(4**j_star) * jval
    floor = dminus_j / x - r * xdot / x
    # Exact ρ̇ while the argmax is unique.
    rdot = (dminus_j * x - jval * xdot) / (x * x)
    return floor, rdot


# ---------------------------------------------------------------------------
# Tests of (P)
# ---------------------------------------------------------------------------

def assert_family_h_kills_p(
    *,
    m: float = 1.0,
    nu: float = 1.0,
    rho_star: float = 0.5,
    candidate_times: Iterable[float] = (1.0, 1.0e-2, 1.0e-4, 1.0e-8),
) -> list[str]:
    """For every candidate T, some K makes min_{t≤T} ρ < ρ_*/2 with X≤M."""
    lines: list[str] = []
    l = choose_L(rho_star)
    plateau = 1.0 / (l - 1)
    q = m
    half = 0.5 * rho_star
    if not plateau < half:
        raise AssertionError("L choice failed the plateau test")
    lines.append(
        f"Family H  ρ_*={rho_star}  L={l}  plateau=1/(L-1)={plateau:.6f}  "
        f"ρ_*/2={half:.6f}  M={m}  ν={nu}"
    )
    for t_cand in candidate_times:
        # K large enough that the high mode is dead by T/2 and the lower
        # block has not yet split: 4^{L-1} / 4^K ≪ 1, and t_cross ≪ T.
        k = l + 4
        while True:
            t_cross = math.log(rho_star * (l - 1) / (1.0 - rho_star)) / (
                2.0 * nu * float(4**k)
            )
            if t_cross < 0.5 * t_cand and k >= l + 6:
                break
            k += 1
            if k > l + 80:
                raise RuntimeError("could not place K")
        shells0 = family_h(rho_star, q, k, l)
        r0, x0, _, j0 = rho_of(shells0)
        if abs(r0 - rho_star) > 1.0e-12:
            raise AssertionError(f"ρ(0)={r0} ≠ ρ_*")
        if j0 != k:
            raise AssertionError(f"j_*(0)={j0} ≠ K={k}")
        traj = trajectory(shells0, nu, t_cand)
        if max(traj.x) > m + 1.0e-12:
            raise AssertionError("X exceeded M")
        r_min, t_min = min_rho_on(traj, t_cand)
        if r_min >= half:
            raise AssertionError(
                f"(P) survived Family H at T={t_cand}, K={k}: min ρ={r_min}"
            )
        # Floor at t=0 is correctly oriented and blows in K.
        floor0, rdot0 = dminus_rho_floor_f0(shells0, nu)
        if floor0 > rdot0 + 1.0e-9:
            raise AssertionError("Dini floor exceeded the exact derivative")
        if floor0 >= 0.0:
            raise AssertionError("expected a negative floor at a high unique peak")
        lines.append(
            f"  T={t_cand:.3e}  K={k}  t_cross={t_cross:.3e}  "
            f"min_ρ={r_min:.6f} at t={t_min:.3e}  "
            f"D_-ρ floor(0)={floor0:.3e}  ρ̇(0)={rdot0:.3e}  FAIL (P)"
        )
    return lines


def assert_high_tail_does_not_kill_p(
    *, m: float = 1.0, nu: float = 1.0, rho_star: float = 0.5, k: int = 12
) -> str:
    shells0 = family_high_tail(rho_star, m, k)
    r0, _, _, j0 = rho_of(shells0)
    if j0 != 1:
        raise AssertionError("high-tail peak should be the low shell")
    traj = trajectory(shells0, nu, 1.0)
    if min(traj.rho) < r0 - 1.0e-12:
        raise AssertionError("high-tail ρ decreased; expected increase toward 1")
    if max(traj.x) > m + 1.0e-12:
        raise AssertionError("X exceeded M")
    return (
        f"High-tail  ρ(0)={r0:.6f}  min ρ={min(traj.rho):.6f}  "
        f"max ρ={max(traj.rho):.6f}  does not kill (P)"
    )


def assert_rho_star_one_survives_heat() -> str:
    """ρ_*=1 is a single shell; heat keeps ρ=1. Not a Family-H kill of (P)."""
    shells0 = {8: 1.0}
    traj = trajectory(shells0, 1.0, 1.0)
    if any(abs(r - 1.0) > 1.0e-12 for r in traj.rho):
        raise AssertionError("single-shell heat must keep ρ=1")
    return "ρ_*=1 heat: ρ≡1 (Family H does not address this endpoint)"


def write_svg(path: str, traj: Trajectory, rho_star: float, title: str) -> None:
    """Tiny SVG of ρ(t). No matplotlib required."""
    w, h, pad = 720, 280, 48
    inner_w, inner_h = w - 2 * pad, h - 2 * pad
    t_max = max(traj.t) if traj.t[-1] > 0 else 1.0
    # Linear time axis would hide the dip; use a log axis for t>0.
    pts: list[tuple[float, float]] = []
    log_t0 = math.log(min(t for t in traj.t if t > 0.0))
    log_t1 = math.log(t_max)

    def x_of(t: float) -> float:
        if t <= 0.0:
            return float(pad)
        return pad + inner_w * (math.log(t) - log_t0) / (log_t1 - log_t0)

    def y_of(r: float) -> float:
        return pad + inner_h * (1.0 - r)

    for t, r in zip(traj.t, traj.rho):
        pts.append((x_of(t), y_of(r)))
    d = "M " + " ".join(f"{x:.2f},{y:.2f}" for x, y in pts[1:])
    half = 0.5 * rho_star
    y_half = y_of(half)
    y_plat = y_of(min(traj.rho))
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="#fff"/>
  <text x="{pad}" y="22" font-family="ui-sans-serif,sans-serif" font-size="14">{title}</text>
  <line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h-pad}" stroke="#333"/>
  <line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="#333"/>
  <line x1="{pad}" y1="{y_of(rho_star)}" x2="{w-pad}" y2="{y_of(rho_star)}" stroke="#888" stroke-dasharray="4 3"/>
  <line x1="{pad}" y1="{y_half}" x2="{w-pad}" y2="{y_half}" stroke="#c00" stroke-dasharray="4 3"/>
  <path d="{d}" fill="none" stroke="#0b57d0" stroke-width="2"/>
  <text x="{w-pad-4}" y="{y_of(rho_star)-6}" text-anchor="end" font-size="11" fill="#555">ρ_*</text>
  <text x="{w-pad-4}" y="{y_half-6}" text-anchor="end" font-size="11" fill="#c00">ρ_*/2</text>
  <text x="{pad+4}" y="{y_plat-6}" font-size="11" fill="#0b57d0">min ρ={min(traj.rho):.3f}</text>
  <text x="{w/2}" y="{h-12}" text-anchor="middle" font-size="11" fill="#333">t (log)</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--svg",
        default="",
        help="optional path to write a Family-H ρ(t) SVG",
    )
    args = p.parse_args(argv)

    assert_paraproduct_exhausts()
    print("indexed LH/HL/HH: partitions every tested (j, N, k-range)")

    assert_a2_leftover_unbounded()
    demo = [
        (
            j,
            a2_drain_over_peak_viscosity(j, m=1.0, nu=1.0, rho=0.5, x=1.0),
            4**j,
        )
        for j in (4, 8, 12, 16)
    ]
    print("A.2 obstruction (M=ν=1, ρ=1/2):")
    for j, ratio, pref in demo:
        print(f"  j_*={j:2d}  drain/visc ≳ {ratio:.3e}  4^{{j_*}}={pref:.3e}")

    print(assert_high_tail_does_not_kill_p())
    print(assert_rho_star_one_survives_heat())

    lines = assert_family_h_kills_p()
    for line in lines:
        print(line)

    # One plotted trajectory at a moderate T, large K.
    rho_star = 0.5
    l = choose_L(rho_star)
    k = l + 10
    shells0 = family_h(rho_star, 1.0, k, l)
    t_max = 10.0 / (2.0 * float(4 ** (l - 1)))  # lower block still alive
    traj = trajectory(shells0, 1.0, t_max)
    r_min, t_min = min_rho_on(traj, t_max)
    print(
        f"plot sample  K={k}  T={t_max:.3e}  min ρ={r_min:.6f} at t={t_min:.3e}"
    )
    if args.svg:
        write_svg(
            args.svg,
            traj,
            rho_star,
            f"Family H  ρ(t)  K={k}  (P) fails: min ρ={r_min:.3f} &lt; ρ_*/2=0.25",
        )
        print(f"wrote {args.svg}")

    print()
    print("VERDICT")
    print("  Theorem H: withdrawn. Do not repair.")
    print("  A.2: retained. Closing (P) with A.2 leaves 4^{j_*}.")
    print("  A.3: wrong Dini side.")
    print("  Indexed LH/HL/HH: written; k-ranges exhaust Z.")
    print("  (P): FALSE for ρ_* ∈ (0,1), Family H, F_j≡0.")
    print("  Conditional local SND-persistence under only (M,ν,ρ_*): no.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
