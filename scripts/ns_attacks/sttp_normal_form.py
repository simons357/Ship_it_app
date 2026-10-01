#!/usr/bin/env python3
"""Stokes-type test potential (STTP) normal-form diagnostic.

Fixed-λ identity, quartic remainder, amplitude scaling, and the moving-λ
term that a print-only ChatGPT script omitted.

This is a diagnostic. It does not close centered drift.
Classical 3D Navier–Stokes is not solved.

Primitive (declared, not recovered from an external canvas):

    Φ_λ(u) = ⟨B(u,u), (A+λ)^{-1} u⟩,
    B(u,w)_k = i P_k Σ_{p+q=k} (û(p)·q) ŵ(q),
    g(κ) = 1/(κ+λ),  λ > 0 frozen when taking DΦ.

Then, writing ⟨ , ⟩ for the real Plancherel pairing,

    DΦ[v] = ⟨B(v,u)+B(u,v), G_λ u⟩ + ⟨B(u,u), G_λ v⟩,
    C_λ   = DΦ[-ν A u],
    R_4   = DΦ[-B(u,u)],
    ∂_λ Φ = ⟨B(u,u), -G_λ² u⟩.

Along NS, u_t = -B(u,u) - ν A u, so at frozen λ

    d/dt Φ_λ(u(t)) = C_λ + R_4.

If the parameter is slaved to the live barycenter λ(t)=Λ(u(t))=Y/X,

    Λ̇ = 2(T_c - ν D_s)/X,   T_c = M - Λ N,   D_s = Z - Λ Y,

and the omitted term is Λ̇ ∂_λ Φ. ChatGPT wrote L for that dissipation;
the Stokes-moment identity forces L = D_s.

Cubelet: integer modes with coordinates in {-1,0,1}, not the origin.
Every frequency length lies in [1, √3], so a comparable-triad ratio-2
filter is vacuous — every triad on this support passes.

Evaluator convention matches the five-lane Stokes-moment scripts
(Plancherel Σ |û(k)|²). Those scripts are not required at runtime.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

Mode = Tuple[int, int, int]
Field = Dict[Mode, np.ndarray]

CUBELET: Tuple[Mode, ...] = tuple(
    (i, j, k)
    for i in (-1, 0, 1)
    for j in (-1, 0, 1)
    for k in (-1, 0, 1)
    if (i, j, k) != (0, 0, 0)
)
MAX_LENGTH_RATIO = math.sqrt(3.0)  # √3 < 2
IDENTITY_TOL = 1e-10
SCALING_SLOPE_TOL = 0.15


def k_norm2(k: Mode) -> float:
    return float(k[0] * k[0] + k[1] * k[1] + k[2] * k[2])


def leray_project(k: Mode, v: np.ndarray) -> np.ndarray:
    kn2 = k_norm2(k)
    if kn2 == 0.0:
        return np.zeros(3, dtype=np.complex128)
    kk = np.array(k, dtype=np.float64)
    return v - (np.dot(kk, v) / kn2) * kk


def zeros() -> np.ndarray:
    return np.zeros(3, dtype=np.complex128)


def enforce_reality(field: Field) -> Field:
    out: Field = {}
    for k, v in field.items():
        if k == (0, 0, 0):
            continue
        mk = (-k[0], -k[1], -k[2])
        proj = leray_project(k, np.asarray(v, dtype=np.complex128))
        if k in out:
            continue
        out[k] = proj
        out[mk] = np.conjugate(proj)
    return out


def scale_field(field: Field, amp: float) -> Field:
    return {k: amp * v for k, v in field.items()}


def add_field(f: Field, g: Field, a: float = 1.0, b: float = 1.0) -> Field:
    keys = set(f) | set(g)
    return {k: a * f.get(k, zeros()) + b * g.get(k, zeros()) for k in keys}


def apply_A(field: Field) -> Field:
    return {k: k_norm2(k) * v for k, v in field.items() if k_norm2(k) > 0}


def apply_G(field: Field, lam: float) -> Field:
    if lam <= 0:
        raise ValueError("λ must be positive")
    return {k: v / (k_norm2(k) + lam) for k, v in field.items() if k_norm2(k) > 0}


def apply_G2(field: Field, lam: float) -> Field:
    if lam <= 0:
        raise ValueError("λ must be positive")
    return {
        k: v / (k_norm2(k) + lam) ** 2 for k, v in field.items() if k_norm2(k) > 0
    }


def inner(f: Field, g: Field) -> float:
    acc = 0.0
    for k in set(f) | set(g):
        acc += float(np.vdot(f.get(k, zeros()), g.get(k, zeros())).real)
    return acc


def bilinear_B(u: Field, w: Field) -> Field:
    raw: Field = {}
    for p, up in u.items():
        for q, wq in w.items():
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            coeff = 1j * np.dot(up, np.array(q, dtype=np.float64))
            raw[k] = raw.get(k, zeros()) + coeff * wq
    return {k: leray_project(k, v) for k, v in raw.items()}


def nonlinear_B(u: Field) -> Field:
    return bilinear_B(u, u)


def moments(field: Field) -> Dict[str, float]:
    E = X = Y = Z = 0.0
    for k, v in field.items():
        amp2 = float(np.vdot(v, v).real)
        kn2 = k_norm2(k)
        if kn2 == 0:
            continue
        E += amp2
        X += kn2 * amp2
        Y += kn2 * kn2 * amp2
        Z += kn2**3 * amp2
    Lam = Y / X if X > 0 else float("nan")
    Ds = Z - Lam * Y if X > 0 else float("nan")
    return {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lam,
        "Ds": Ds,
    }


def N_M_Tc(field: Field) -> Dict[str, float]:
    Buu = nonlinear_B(field)
    N = 0.0 + 0.0j
    M = 0.0 + 0.0j
    for k in set(field) | set(Buu):
        kn2 = k_norm2(k)
        if kn2 == 0:
            continue
        uk = field.get(k, zeros())
        bk = Buu.get(k, zeros())
        ip = np.vdot(bk, uk)
        N -= kn2 * ip
        M -= (kn2 * kn2) * ip
    N_r = float(N.real)
    M_r = float(M.real)
    Lam = moments(field)["Lambda"]
    return {"N": N_r, "M": M_r, "Tc": M_r - Lam * N_r}


def phi_lambda(field: Field, lam: float) -> float:
    return inner(nonlinear_B(field), apply_G(field, lam))


def Dphi(field: Field, direction: Field, lam: float) -> float:
    Buu = nonlinear_B(field)
    Bvu = bilinear_B(direction, field)
    Buv = bilinear_B(field, direction)
    Gu = apply_G(field, lam)
    Gv = apply_G(direction, lam)
    return inner(add_field(Bvu, Buv), Gu) + inner(Buu, Gv)


def C_lambda(field: Field, lam: float, nu: float = 1.0) -> float:
    return Dphi(field, scale_field(apply_A(field), -nu), lam)


def R4(field: Field, lam: float) -> float:
    return Dphi(field, scale_field(nonlinear_B(field), -1.0), lam)


def dphi_dlam(field: Field, lam: float) -> float:
    return inner(nonlinear_B(field), scale_field(apply_G2(field, lam), -1.0))


def lambda_dot(field: Field, nu: float = 1.0) -> float:
    """Λ̇ = 2(T_c − ν D_s)/X along NS. ChatGPT's L is this D_s."""
    m = moments(field)
    tc = N_M_Tc(field)["Tc"]
    if m["X"] <= 0:
        return float("nan")
    return 2.0 * (tc - nu * m["Ds"]) / m["X"]


def moving_lambda_term(field: Field, lam: float, nu: float = 1.0) -> float:
    return lambda_dot(field, nu=nu) * dphi_dlam(field, lam)


def Dphi_polarization(field: Field, direction: Field, lam: float) -> float:
    """Exact cubic polarization: DΦ[v] = (Φ(u+v) − Φ(u−v))/2 − Φ(v)."""
    plus = add_field(field, direction, 1.0, 1.0)
    minus = add_field(field, direction, 1.0, -1.0)
    return 0.5 * (phi_lambda(plus, lam) - phi_lambda(minus, lam)) - phi_lambda(
        direction, lam
    )


def C_lambda_polarization(field: Field, lam: float, nu: float = 1.0) -> float:
    """Independent analytic checkout of C_λ along −ν A u."""
    return Dphi_polarization(field, scale_field(apply_A(field), -nu), lam)


def C_lambda_finite_difference(
    field: Field, lam: float, nu: float = 1.0, eps: float = 1e-6
) -> float:
    """Secondary central-difference checkout. Prefer C_lambda_polarization."""
    direction = scale_field(apply_A(field), -nu)
    plus = add_field(field, direction, 1.0, eps)
    minus = add_field(field, direction, 1.0, -eps)
    return (phi_lambda(plus, lam) - phi_lambda(minus, lam)) / (2.0 * eps)


def euler_identity_error(field: Field, lam: float) -> float:
    """|DΦ[u] − 3 Φ| for a cubic primitive."""
    return abs(Dphi(field, field, lam) - 3.0 * phi_lambda(field, lam))


def cubelet_frequency_lengths(modes: Sequence[Mode] = CUBELET) -> List[float]:
    return sorted({math.sqrt(k_norm2(k)) for k in modes if k_norm2(k) > 0})


def cubelet_max_length_ratio(modes: Sequence[Mode] = CUBELET) -> float:
    lengths = cubelet_frequency_lengths(modes)
    return lengths[-1] / lengths[0]


def comparable_triad_filter_vacuous(modes: Sequence[Mode] = CUBELET) -> bool:
    """Ratio-2 comparable-triad filter does not restrict this cubelet."""
    return cubelet_max_length_ratio(modes) < 2.0


def random_cubelet_field(rng: np.random.Generator, amp: float = 1.0) -> Field:
    raw: Field = {}
    seen = set()
    for k in CUBELET:
        mk = (-k[0], -k[1], -k[2])
        if k in seen or mk in seen:
            continue
        vec = amp * (rng.normal(size=3) + 1j * rng.normal(size=3))
        raw[k] = vec
        seen.add(k)
        seen.add(mk)
    return enforce_reality(raw)


def exhibit_c_field() -> Field:
    """Deterministic cubelet used for the moving-λ independent check.

    Near-scale triad of the centered-drift note, plus a (1,1,1) mode so
    the support meets every cubelet length {1, √2, √3}.
    """
    raw: Field = {
        (1, 0, 0): np.array([0.0, 1.0, 0.0], dtype=np.complex128),
        (0, 1, 0): np.array([1.0, 0.0, 1.0], dtype=np.complex128),
        (1, 1, 0): np.array([0.0, 0.0, -1j], dtype=np.complex128),
        (1, 1, 1): np.array([1.0, -1.0, 0.0], dtype=np.complex128),
    }
    return enforce_reality(raw)


def loglog_slope(amps: Sequence[float], values: Sequence[float]) -> float:
    xs = np.log(np.asarray(amps, dtype=float))
    ys = np.log(np.abs(np.asarray(values, dtype=float)))
    if np.any(~np.isfinite(ys)):
        return float("nan")
    A = np.vstack([xs, np.ones_like(xs)]).T
    slope, _ = np.linalg.lstsq(A, ys, rcond=None)[0]
    return float(slope)


@dataclass
class DiagnosticReport:
    identity_max_abs_error: float
    identity_pass: bool
    r4_positive: int
    r4_negative: int
    r4_nonfinite: int
    n_random: int
    C_lambda_amp_slope: float
    R4_amp_slope: float
    scaling_pass: bool
    exhibit_c_moving_term: float
    exhibit_c_lambda_dot: float
    exhibit_c_dphi_dlam: float
    cubelet_min_length: float
    cubelet_max_length: float
    cubelet_max_ratio: float
    comparable_triad_filter_vacuous: bool
    centered_drift_closed: bool
    ns_solved: bool
    moving_lambda_included: bool
    fail_fast: bool


def run_diagnostic(
    seed: int = 7,
    n_random: int = 100,
    nu: float = 1.0,
    fail_fast: bool = True,
) -> DiagnosticReport:
    rng = np.random.default_rng(seed)
    identity_errors: List[float] = []
    r4_pos = r4_neg = r4_bad = 0

    for _ in range(n_random):
        field = random_cubelet_field(rng)
        lam = moments(field)["Lambda"]
        if not np.isfinite(lam) or lam <= 0:
            r4_bad += 1
            continue
        c_closed = C_lambda(field, lam, nu=nu)
        c_pol = C_lambda_polarization(field, lam, nu=nu)
        identity_errors.append(
            max(abs(c_closed - c_pol), euler_identity_error(field, lam))
        )
        rem = R4(field, lam)
        if not np.isfinite(rem):
            r4_bad += 1
        elif rem > 0:
            r4_pos += 1
        elif rem < 0:
            r4_neg += 1

    identity_max = max(identity_errors) if identity_errors else float("inf")
    identity_pass = identity_max < IDENTITY_TOL

    shape = exhibit_c_field()
    amps = (0.5, 1.0, 2.0)
    c_vals = []
    r_vals = []
    for a in amps:
        f = scale_field(shape, a)
        lam = moments(f)["Lambda"]
        c_vals.append(C_lambda(f, lam, nu=nu))
        r_vals.append(R4(f, lam))
    c_slope = loglog_slope(amps, c_vals)
    r_slope = loglog_slope(amps, r_vals)
    scaling_pass = (
        abs(c_slope - 3.0) < SCALING_SLOPE_TOL
        and abs(r_slope - 4.0) < SCALING_SLOPE_TOL
    )

    ex = exhibit_c_field()
    lam_ex = moments(ex)["Lambda"]
    moving = moving_lambda_term(ex, lam_ex, nu=nu)
    ldot = lambda_dot(ex, nu=nu)
    dlam = dphi_dlam(ex, lam_ex)
    lengths = cubelet_frequency_lengths()

    report = DiagnosticReport(
        identity_max_abs_error=identity_max,
        identity_pass=identity_pass,
        r4_positive=r4_pos,
        r4_negative=r4_neg,
        r4_nonfinite=r4_bad,
        n_random=n_random,
        C_lambda_amp_slope=c_slope,
        R4_amp_slope=r_slope,
        scaling_pass=scaling_pass,
        exhibit_c_moving_term=moving,
        exhibit_c_lambda_dot=ldot,
        exhibit_c_dphi_dlam=dlam,
        cubelet_min_length=lengths[0],
        cubelet_max_length=lengths[-1],
        cubelet_max_ratio=cubelet_max_length_ratio(),
        comparable_triad_filter_vacuous=comparable_triad_filter_vacuous(),
        centered_drift_closed=False,
        ns_solved=False,
        moving_lambda_included=True,
        fail_fast=fail_fast,
    )
    if fail_fast:
        _assert_report(report)
    return report


def _assert_report(report: DiagnosticReport) -> None:
    """Fail-fast thresholds. Print-only diagnostics are not enough."""
    if not report.identity_pass:
        raise AssertionError(
            f"fixed-λ identity failed: max |C_closed − C_fd| = "
            f"{report.identity_max_abs_error} (tol {IDENTITY_TOL})"
        )
    if not report.scaling_pass:
        raise AssertionError(
            f"amplitude scaling failed: C_λ slope {report.C_lambda_amp_slope}, "
            f"R_4 slope {report.R4_amp_slope}"
        )
    if report.r4_positive + report.r4_negative == 0:
        raise AssertionError("R_4 was never finite-and-nonzero on the ensemble")
    if report.r4_nonfinite > 0:
        raise AssertionError(f"R_4 nonfinite on {report.r4_nonfinite} fields")
    if not report.comparable_triad_filter_vacuous:
        raise AssertionError("cubelet length ratio unexpectedly ≥ 2")
    if abs(report.exhibit_c_moving_term) < 1e-18:
        raise AssertionError(
            "moving-λ term vanished on Exhibit C; the omitted term must be computed"
        )
    if report.centered_drift_closed or report.ns_solved:
        raise AssertionError("honesty lock violated")
    if not report.moving_lambda_included:
        raise AssertionError("moving-λ term was omitted")


def report_dict(report: DiagnosticReport) -> dict:
    return asdict(report)


def main(argv: Iterable[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--n-random", type=int, default=100)
    p.add_argument("--nu", type=float, default=1.0)
    p.add_argument(
        "--no-fail-fast",
        action="store_true",
        help="print the report even if a threshold fails (tests must not do this)",
    )
    p.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="optional JSON path for the diagnostic report",
    )
    args = p.parse_args(list(argv) if argv is not None else None)
    try:
        report = run_diagnostic(
            seed=args.seed,
            n_random=args.n_random,
            nu=args.nu,
            fail_fast=not args.no_fail_fast,
        )
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    payload = report_dict(report)
    print(json.dumps(payload, indent=2))
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
