#!/usr/bin/env python3
"""Small-case attack on the unproved square-root candidate

    |T_c|  ≤  C  ||∇u||_3  √(Y D_s).

What a successful run certifies
-------------------------------
* Exact Fourier identities for T_c, Y, D_s (and the |∇u|^2 zero-mode).
* Certified Q bounds that do not use sampled quadrature for ||∇u||_3.

What a successful run does *not* certify
----------------------------------------
* The uniform inequality (existence of a finite C for all fields).
* Any time-budget / occupation integral that would feed a Gronwall close.
* Lemma★ / PRODUCT-BLOCK / Navier–Stokes regularity.

The exact near-shell obstruction (T_c / D_s blows while T_c / √D_s stays
finite) motivates the square-root, and does not establish it.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, asdict
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ns_attacks.exact_fourier import (  # noqa: E402
    Field,
    GQ,
    I,
    IdentityReport,
    KVec,
    ONE,
    Vec3,
    cascade,
    certified_grad_l3,
    gq_vec,
    iterate_phase_locks,
    project_perp,
    lam,
    moments,
    shell_energy,
    two_shell_D_s,
    verify_identities,
    vscale,
)

CANDIDATE = "|T_c| <= C ||∇u||_3 sqrt(Y D_s)"
STATUS = "UNPROVED CANDIDATE"


def _int_vec(k: KVec) -> Vec3:
    """Generic rational polarization in the Leray plane (not a coordinate-axis trap).

    Pure e_3 on an xy-shell makes q·v_p vanish for in-plane partners, so the
    triad is dead.  Projecting (1,1,1) (or (1,0,-1) if k ∥ (1,1,1)) keeps
    the coefficient in Q and typically leaves several live closings.
    """
    seed = gq_vec((1, 1, 1))
    polar = project_perp(k, seed)
    if polar[0].abs2() + polar[1].abs2() + polar[2].abs2() == 0:
        polar = project_perp(k, gq_vec((1, 0, -1)))
    return polar


def _put(field: Field, k: KVec, amp, phase: GQ = ONE, polar: Optional[Vec3] = None) -> None:
    if polar is None:
        polar = _int_vec(k)
    field.set_mode(k, vscale(GQ(amp) * phase, polar))


def near_shell_several_triads(eps: Fraction, phase: GQ = ONE) -> Field:
    """Main shell 5, several closings onto shell 10, satellite amplitude eps.

    Occupied main parents (all |k|^2 = 5):
        (1,2,0), (2,-1,0), (2,1,0), (1,-2,0), (1,0,2), (2,0,-1)
    Occupied outputs (all |k|^2 = 10):
        (3,1,0), (3,-1,0), (3,0,1)
    """
    f = Field()
    mains: Sequence[KVec] = (
        (1, 2, 0),
        (2, -1, 0),
        (2, 1, 0),
        (1, -2, 0),
        (1, 0, 2),
        (2, 0, -1),
    )
    sats: Sequence[KVec] = (
        (3, 1, 0),
        (3, -1, 0),
        (3, 0, 1),
    )
    for k in mains:
        _put(f, k, Fraction(1), phase)
    for k in sats:
        _put(f, k, eps, phase * I)
    return f


def separated_varied_amplitudes(high_amp: Fraction, phase: GQ = ONE) -> Field:
    """Widely separated frequencies, explicit LL / HH / HL closings.

    Low triad on shells 1 and 2; high triad on shells 36 and 72;
    cross outputs (7,0,0), (1,6,0), (6,1,0) so HL lands on the support.
    """
    f = Field()
    lows: Sequence[Tuple[KVec, Fraction]] = (
        ((1, 0, 0), Fraction(1)),
        ((0, 1, 0), Fraction(1)),
        ((1, 1, 0), Fraction(1)),
    )
    highs: Sequence[Tuple[KVec, Fraction]] = (
        ((6, 0, 0), high_amp),
        ((0, 6, 0), high_amp),
        ((6, 6, 0), high_amp),
    )
    cross: Sequence[Tuple[KVec, Fraction]] = (
        ((7, 0, 0), high_amp),
        ((1, 6, 0), high_amp),
        ((6, 1, 0), high_amp),
    )
    for k, amp in lows:
        _put(f, k, amp, phase)
    for k, amp in highs:
        _put(f, k, amp, phase * I)
    for k, amp in cross:
        _put(f, k, amp, phase)
    return f


def dense_coordinated_packet(width: int, phase: GQ = ONE) -> Field:
    """Dense box packet |k_i| ≤ width with phase lock i^{k1+k2+k3}.

    Coordinated phases; many interacting triads on a small lattice block.
    """
    if width < 1:
        raise ValueError("width must be >= 1")
    f = Field()
    rng = range(-width, width + 1)
    for a in rng:
        for b in rng:
            for c in rng:
                k = (a, b, c)
                if k == (0, 0, 0):
                    continue
                # set only one of {k,-k}; set_mode writes the conjugate
                first_nz = next(x for x in k if x != 0)
                if first_nz < 0:
                    continue
                s = (a + b + c) % 4
                lock = (ONE, I, -ONE, -I)[s]
                _put(f, k, Fraction(1), phase * lock)
    return f


def coherent_affine_packet(n: int, sat: Fraction, phase: GQ = ONE) -> Field:
    """P/Q affine packet plus occupied cross outputs (coordinated).

    P_i = (i,1,0) with e_3, Q_j = (j,0,1) with e_2,
    R_{i,j} = (i+j,1,1) with satellite amplitude `sat`.
    """
    if n < 2:
        raise ValueError("need at least two P and two Q nodes")
    f = Field()
    e3 = gq_vec((0, 0, 1))
    e2 = gq_vec((0, 1, 0))
    for i in range(1, n + 1):
        _put(f, (i, 1, 0), Fraction(1), phase, polar=e3)
        _put(f, (i, 0, 1), Fraction(1), phase * I, polar=e2)
    sat_polar = gq_vec((0, 1, 1))
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # add, so two parent pairs that share an output stay coordinated
            f.add_mode((i + j, 1, 1), vscale(GQ(sat) * phase, sat_polar))
    return f


@dataclass
class CaseRow:
    family: str
    name: str
    identities_ok: bool
    vacuous: bool
    E: str
    X: str
    Y: str
    D_s: str
    T_c: str
    Q_ub_sq: Optional[str]
    Q_lb_sixth: Optional[str]
    Q_ub_display: Optional[float]
    Q_lb_display: Optional[float]
    note: str


def _row(family: str, name: str, field: Field, note: str = "") -> Tuple[CaseRow, IdentityReport]:
    report = verify_identities(field)
    mom = moments(field)
    cas = cascade(field, mom.Lambda)
    cert = certified_grad_l3(field, mom, cas)
    Q_ub = None
    Q_lb = None
    if cert.Q_ub_sq is not None:
        Q_ub = math.sqrt(float(cert.Q_ub_sq))
    if cert.Q_lb_sixth is not None:
        Q_lb = float(cert.Q_lb_sixth) ** (1.0 / 6.0)
    row = CaseRow(
        family=family,
        name=name,
        identities_ok=report.ok,
        vacuous=cert.vacuous,
        E=str(mom.E),
        X=str(mom.X),
        Y=str(mom.Y),
        D_s=str(mom.D_s),
        T_c=str(cas.T_c),
        Q_ub_sq=None if cert.Q_ub_sq is None else str(cert.Q_ub_sq),
        Q_lb_sixth=None if cert.Q_lb_sixth is None else str(cert.Q_lb_sixth),
        Q_ub_display=Q_ub,
        Q_lb_display=Q_lb,
        note=note,
    )
    return row, report


def near_shell_obstruction_rows() -> List[Tuple[CaseRow, IdentityReport, Dict[str, str]]]:
    """Exact near-shell scaling: T_c/D_s blows, T_c^2/D_s stays ordered.

    This motivates √D_s and does not prove the L^3 estimate.
    """
    out = []
    for exp in (0, 1, 2, 3, 4):
        eps = Fraction(1, 2 ** exp)
        field = near_shell_several_triads(eps, phase=ONE)
        row, report = _row(
            "near_shell_obstruction",
            f"eps=1/{2 ** exp}",
            field,
            note="motivates sqrt(D_s); does not prove the candidate",
        )
        mom = moments(field)
        cas = cascade(field, mom.Lambda)
        extra = {
            "eps": str(eps),
            "T_c_sq_over_D_s": (
                None if mom.D_s == 0 else str((cas.T_c * cas.T_c) / mom.D_s)
            ),
            "T_c_sq_over_D_s_sq": (
                None if mom.D_s == 0 else str((cas.T_c * cas.T_c) / (mom.D_s * mom.D_s))
            ),
            "two_shell_D_s_check": str(
                two_shell_D_s(
                    5,
                    10,
                    shell_energy(field, 5),
                    shell_energy(field, 10),
                )
            ),
        }
        out.append((row, report, extra))
    return out


def build_cases() -> List[Tuple[CaseRow, IdentityReport]]:
    cases: List[Tuple[CaseRow, IdentityReport]] = []

    # Family 1: nearly single-shell, several interacting triads.
    for exp in (0, 1, 2, 3):
        eps = Fraction(1, 2 ** exp)
        for i, phase in enumerate(iterate_phase_locks()):
            field = near_shell_several_triads(eps, phase=phase)
            cases.append(
                _row(
                    "near_shell_triads",
                    f"eps=1/{2 ** exp}/phase{i}",
                    field,
                    note="several shell-5 triads closing onto shell 10",
                )
            )
            break  # one phase per eps in the default board; tests sweep phases

    # Family 2: widely separated frequencies, varied amplitudes.
    for high in (Fraction(1), Fraction(1, 4), Fraction(4), Fraction(1, 16)):
        field = separated_varied_amplitudes(high, phase=ONE)
        cases.append(
            _row(
                "separated_amplitudes",
                f"high_amp={high}",
                field,
                note="shells 1–2 vs 36–72 plus HL cross outputs",
            )
        )

    # Family 3: dense packets with coordinated phases.
    for width in (1,):
        field = dense_coordinated_packet(width, phase=ONE)
        cases.append(
            _row(
                "dense_box_packet",
                f"width={width}",
                field,
                note="3×3×3 minus origin, phase i^{k1+k2+k3}",
            )
        )
    for n, sat in ((2, Fraction(1)), (2, Fraction(1, 4)), (3, Fraction(1, 2))):
        field = coherent_affine_packet(n, sat, phase=ONE)
        cases.append(
            _row(
                "dense_affine_packet",
                f"n={n}/sat={sat}",
                field,
                note="coordinated P/Q packet with occupied cross outputs",
            )
        )
    return cases


def run_board() -> Dict:
    identity_failures: List[str] = []
    rows: List[dict] = []
    max_Q_lb = None
    max_Q_ub = None

    for row, report in build_cases():
        if not report.ok:
            identity_failures.extend(f"{row.name}: {msg}" for msg in report.failures)
        rec = asdict(row)
        rows.append(rec)
        if row.Q_lb_display is not None:
            max_Q_lb = row.Q_lb_display if max_Q_lb is None else max(max_Q_lb, row.Q_lb_display)
        if row.Q_ub_display is not None:
            max_Q_ub = row.Q_ub_display if max_Q_ub is None else max(max_Q_ub, row.Q_ub_display)

    obstruction = []
    for row, report, extra in near_shell_obstruction_rows():
        if not report.ok:
            identity_failures.extend(f"{row.name}: {msg}" for msg in report.failures)
        obstruction.append({**asdict(row), **extra})

    identities_ok = not identity_failures
    payload = {
        "candidate": CANDIDATE,
        "status": STATUS,
        "identities_verified": identities_ok,
        "identity_failures": identity_failures,
        "uniform_inequality": "SEPARATE PROOF OBLIGATION",
        "time_budget": "SEPARATE PROOF OBLIGATION",
        "nabla_u_3": (
            "certified L2 lower / Riesz–Thorin L4 interpolation upper; "
            "sampled quadrature is not used and cannot certify a counterexample"
        ),
        "max_Q_lb_display": max_Q_lb,
        "max_Q_ub_display": max_Q_ub,
        "kill_claim": (
            "none — finite certified Q_lb on a finite board does not kill "
            "the candidate; a kill requires Q_lb → ∞ along a family"
        ),
        "cases": rows,
        "near_shell_obstruction": obstruction,
    }
    return payload


def _print_table(payload: Dict) -> None:
    print(f"Candidate: {payload['candidate']}")
    print(f"Status:    {payload['status']}")
    print(f"Identities verified: {payload['identities_verified']}")
    print(f"Uniform inequality:  {payload['uniform_inequality']}")
    print(f"Time budget:         {payload['time_budget']}")
    print(f"||∇u||_3:            {payload['nabla_u_3']}")
    print()
    hdr = f"{'family':<24} {'name':<22} {'ok':<5} {'T_c':>16} {'Q_lb~':>10} {'Q_ub~':>10}"
    print(hdr)
    print("-" * len(hdr))
    for rec in payload["cases"]:
        qlb = "vacuous" if rec["vacuous"] else f"{rec['Q_lb_display']:.4g}" if rec["Q_lb_display"] is not None else "—"
        qub = "vacuous" if rec["vacuous"] else f"{rec['Q_ub_display']:.4g}" if rec["Q_ub_display"] is not None else "—"
        print(
            f"{rec['family']:<24} {rec['name']:<22} "
            f"{'yes' if rec['identities_ok'] else 'NO':<5} "
            f"{rec['T_c']:>16} {qlb:>10} {qub:>10}"
        )
    print()
    print("Near-shell obstruction (motivates √D_s; does not prove the candidate):")
    for rec in payload["near_shell_obstruction"]:
        print(
            f"  {rec['name']}: T_c^2/D_s={rec['T_c_sq_over_D_s']}  "
            f"T_c^2/D_s^2={rec['T_c_sq_over_D_s_sq']}"
        )
    print()
    print(f"max certified Q_lb (display): {payload['max_Q_lb_display']}")
    print(f"max certified Q_ub (display): {payload['max_Q_ub_display']}")
    print(f"Kill claim: {payload['kill_claim']}")
    if payload["identity_failures"]:
        print("IDENTITY FAILURES:")
        for msg in payload["identity_failures"]:
            print("  ", msg)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=None, help="write the board as JSON")
    args = parser.parse_args(argv)
    payload = run_board()
    _print_table(payload)
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"wrote {args.json}")
    return 0 if payload["identities_verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
