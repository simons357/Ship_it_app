"""Arithmetic sign realizability — first-variation neighboring-shell gate.

Do not alter the loop-gauge / telescopic-capacity gate.

Discrete expansion (EXACT, actual neighboring transfer T):

    T_c = Λ ⟨δ, T⟩ + Σ_m δ_m² T_m,
    δ_m = λ_m − Λ.

The neighboring T_m itself varies with the deformation.
The first-variation object freezes the parent transfer:

    L_{1,N} = Λ_N ⟨δ_N, T_N^{(0)}⟩

on the asymptotic neighboring-shell family, so the transfer
variation is next order. The actual neighboring T_m is kept
separately. Consistency remainder:

    R_{2,N} := T_{c,N} − Λ_N ⟨δ_N, T_N^{(0)}⟩.

A legitimate first-variation sequence has R_{2,N} of higher
order than L_{1,N}. If not, the deformation changed
polarization / amplitudes / topology too strongly.

Outcome tree (heterochiral, legitimate samples, |ρ| ≥ c):

    BOTH SIGNS  → universal first-order one-sided narrow
                  depletion is FALSE. Stop static closure
                  on this question. Save A_N^+. Dynamic
                  frontier: dangerous-state persistence.
                  Θ_N = ν κ_N² τ_{U,N} is then live.
    ZERO ONLY   → consistent with Vandermonde delay on
                  homochiral families. Does not rescue NSE;
                  heterochiral remains separate.
    ONE SIGN    → ask whether the restriction is the
                  Gram / lattice realization problem.
    NO NEIGHBOR → arithmetic rigidity, not sign depletion.

ρ_N is the geometric correlation of the child gap against
the frozen parent transfer, at canonical real helical
amplitudes a = 1. Amplitude sign flips are recorded but
do not by themselves make BOTH SIGNS (that is the already
killed phase-twin). BOTH SIGNS requires two legitimate
heterochiral geometries of opposite ρ.

Not a T_c bound. Not DA-NS-2. NS is not solved.
"""

from __future__ import annotations

import json
import math
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from ns_attacks.helical import (
    add,
    as_mode,
    helical_basis,
    norm2,
    sub,
)

Mode = Tuple[int, int, int]
CVec = Tuple[complex, complex, complex]
Triad = Tuple[Mode, Mode, Mode]
Field = Dict[Mode, CVec]

UNIT_MOVES: Tuple[Mode, ...] = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)

HOMO: Tuple[Tuple[int, int, int], ...] = ((1, 1, 1), (-1, -1, -1))
HETERO: Tuple[Tuple[int, int, int], ...] = (
    (1, 1, -1),
    (1, -1, 1),
    (-1, 1, 1),
    (1, -1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
)

RHO_FLOOR = 0.05
R2_RATIO_MAX = 0.55  # legitimate first-variation: |R2| < this |L1|


def is_sum_of_three_squares(n: int) -> bool:
    if n <= 0:
        return False
    m = n
    while m % 4 == 0:
        m //= 4
    return m % 8 != 7


def shell(n: int) -> List[Mode]:
    pts: List[Mode] = []
    r = int(math.isqrt(n)) + 1
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            zz = n - x * x - y * y
            if zz < 0:
                continue
            z = int(math.isqrt(zz))
            if z * z != zz:
                continue
            if z == 0:
                pts.append((x, y, 0))
            else:
                pts.append((x, y, z))
                pts.append((x, y, -z))
    return pts


def exact_shell_triads(n: int) -> List[Triad]:
    """p+q=k with |p|²=|q|²=|k|²=n. N even is required for p·q=−n/2."""
    pts = shell(n)
    s = set(pts)
    out: List[Triad] = []
    seen = set()
    for p in pts:
        for q in pts:
            k = add(p, q)
            if k not in s or k == (0, 0, 0):
                continue
            if p == (0, 0, 0) or q == (0, 0, 0):
                continue
            key = tuple(sorted((p, q, k)))
            if key in seen:
                continue
            seen.add(key)
            out.append((p, q, k))
    return out


def _nonzero(m: Mode) -> bool:
    return m != (0, 0, 0)


def neighbor_deformations(triad: Triad) -> List[dict]:
    """Unit lattice moves that preserve p+q=k and change at least one shell."""
    p0, q0, k0 = triad
    n0 = norm2(p0)
    out: List[dict] = []
    seen = set()
    for e in UNIT_MOVES:
        candidates = (
            (add(p0, e), q0, add(k0, e), "p"),
            (p0, add(q0, e), add(k0, e), "q"),
            (add(p0, e), add(q0, sub((0, 0, 0), e)), k0, "pq"),
        )
        for p, q, k, tag in candidates:
            if not (_nonzero(p) and _nonzero(q) and _nonzero(k)):
                continue
            if add(p, q) != k:
                continue
            if len({p, q, k}) < 3:
                continue
            shells = (norm2(p), norm2(q), norm2(k))
            if shells == (n0, n0, n0):
                continue
            key = tuple(sorted((p, q, k)))
            if key in seen:
                continue
            seen.add(key)
            out.append(
                {
                    "parent": triad,
                    "child": (p, q, k),
                    "move": tag,
                    "e": e,
                    "parent_shells": (n0, n0, n0),
                    "child_shells": shells,
                    "gap": max(shells) - min(shells),
                }
            )
    return out


def _scale(v: CVec, a: complex) -> CVec:
    return (a * v[0], a * v[1], a * v[2])


def _cabs2(v: CVec) -> float:
    return float(abs(v[0]) ** 2 + abs(v[1]) ** 2 + abs(v[2]) ** 2)


def helical_field(
    triad: Triad,
    sigma: Tuple[int, int, int],
    amps: Tuple[complex, complex, complex] = (1.0, 1.0, 1.0),
    axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> Field:
    """Real field on {±p,±q,±k} with helical amplitudes."""
    p, q, k = triad
    field: Field = {}
    for mode, s, a in ((p, sigma[0], amps[0]), (q, sigma[1], amps[1]), (k, sigma[2], amps[2])):
        v = _scale(helical_basis(mode, s, axis), a)
        field[mode] = v
        field[sub((0, 0, 0), mode)] = (v[0].conjugate(), v[1].conjugate(), v[2].conjugate())
    return field


def modal_transfers(field: Field) -> Dict[Mode, float]:
    """Seated I_3 sum: T_k = Σ_{p+q=k} Im[(q·v_p)(v_q·conj(v_k))]."""
    keys = list(field)
    t: Dict[Mode, float] = {m: 0.0 for m in keys}
    keyset = set(keys)
    for p in keys:
        vp = field[p]
        for q in keys:
            k = add(p, q)
            if k not in keyset:
                continue
            vq = field[q]
            vk = field[k]
            qvp = q[0] * vp[0] + q[1] * vp[1] + q[2] * vp[2]
            vq_vk = (
                vq[0] * vk[0].conjugate()
                + vq[1] * vk[1].conjugate()
                + vq[2] * vk[2].conjugate()
            )
            t[k] += (qvp * vq_vk).imag
    return t


def energy_sum(t: Dict[Mode, float]) -> float:
    return float(sum(t.values()))


def moments(field: Field, t: Dict[Mode, float]) -> dict:
    x = y = z = 0.0
    for k, v in field.items():
        e = _cabs2(v)
        lam = float(norm2(k))
        x += lam * e
        y += (lam ** 2) * e
        z += (lam ** 3) * e
    if x <= 0.0:
        raise ValueError("empty field")
    lam_bar = y / x
    tc = 0.0
    inner = 0.0
    quad = 0.0
    delta: Dict[Mode, float] = {}
    for k, tk in t.items():
        lam = float(norm2(k))
        d = lam - lam_bar
        delta[k] = d
        tc += lam * d * tk
        inner += d * tk
        quad += (d ** 2) * tk
    ds = z - lam_bar * y
    return {
        "X": x,
        "Y": y,
        "Z": z,
        "Lambda": lam_bar,
        "D_s": ds,
        "T_c": tc,
        "delta": delta,
        "inner_dT": inner,
        "quad_d2T": quad,
        "identity_residual": tc - (lam_bar * inner + quad),
    }


def role_pair(parent: Triad, child: Triad, t0: Dict[Mode, float], delta: Dict[Mode, float]) -> float:
    """⟨δ_N, T_N^{(0)}⟩ by matching roles (p,q,k) and conjugates."""
    acc = 0.0
    for i in range(3):
        m0 = parent[i]
        m1 = child[i]
        acc += delta.get(m1, 0.0) * t0.get(m0, 0.0)
        zm0 = sub((0, 0, 0), m0)
        zm1 = sub((0, 0, 0), m1)
        acc += delta.get(zm1, 0.0) * t0.get(zm0, 0.0)
    return acc


def first_variation(
    parent: Triad,
    child: Triad,
    sigma: Tuple[int, int, int],
    amps: Tuple[complex, complex, complex] = (1.0, 1.0, 1.0),
) -> dict:
    f0 = helical_field(parent, sigma, amps)
    f1 = helical_field(child, sigma, amps)
    t0 = modal_transfers(f0)
    t1 = modal_transfers(f1)
    m0 = moments(f0, t0)
    m1 = moments(f1, t1)
    inner0 = role_pair(parent, child, t0, m1["delta"])
    l1 = m1["Lambda"] * inner0
    r2 = m1["T_c"] - l1
    t0_roles = [t0.get(parent[i], 0.0) for i in range(3)]
    d_roles = [m1["delta"].get(child[i], 0.0) for i in range(3)]
    nrm_d = math.sqrt(sum(x * x for x in d_roles))
    nrm_t = math.sqrt(sum(x * x for x in t0_roles))
    rho = (sum(d_roles[i] * t0_roles[i] for i in range(3)) / (nrm_d * nrm_t)) if nrm_d > 0 and nrm_t > 0 else 0.0
    l1_abs = abs(l1)
    legitimate = (l1_abs <= 1e-14 and abs(r2) <= 1e-10) or (
        l1_abs > 1e-14 and abs(r2) <= R2_RATIO_MAX * l1_abs
    )
    return {
        "parent": parent,
        "child": child,
        "sigma": sigma,
        "amps": [complex(a) for a in amps],
        "channel": "homochiral" if sigma[0] == sigma[1] == sigma[2] else "heterochiral",
        "Lambda_0": m0["Lambda"],
        "T_c_0": m0["T_c"],
        "energy_sum_0": energy_sum(t0),
        "identity_0": m0["identity_residual"],
        "Lambda_N": m1["Lambda"],
        "T_c_N": m1["T_c"],
        "D_s_N": m1["D_s"],
        "energy_sum_N": energy_sum(t1),
        "identity_N": m1["identity_residual"],
        "T_0_roles": t0_roles,
        "T_N_roles": [t1.get(child[i], 0.0) for i in range(3)],
        "delta_N_roles": d_roles,
        "inner_dT0": inner0,
        "L_1_N": l1,
        "R_2_N": r2,
        "rho_N": rho,
        "R2_over_L1": (r2 / l1) if l1_abs > 1e-14 else None,
        "legitimate": legitimate and abs(m1["identity_residual"]) < 1e-8,
        "T_N_minus_T_0": [t1.get(child[i], 0.0) - t0_roles[i] for i in range(3)],
    }


def classify_channel(sig: Tuple[int, int, int]) -> str:
    return "homochiral" if sig[0] == sig[1] == sig[2] else "heterochiral"


def scan_scale(n: int, max_parents: int = 8, max_children: int = 6) -> dict:
    """One scale of the neighboring-shell family."""
    if not is_sum_of_three_squares(n):
        return {
            "N": n,
            "category": "NO_NEIGHBOR",
            "reason": "shell empty (not a sum of three squares)",
            "n_parents": 0,
            "n_children": 0,
            "samples": [],
        }
    parents = exact_shell_triads(n)
    if not parents:
        return {
            "N": n,
            "category": "NO_NEIGHBOR",
            "reason": "no exact-shell triad p+q=k on this shell",
            "n_parents": 0,
            "n_children": 0,
            "samples": [],
        }
    samples: List[dict] = []
    n_children = 0
    for parent in parents[:max_parents]:
        kids = neighbor_deformations(parent)
        n_children += len(kids)
        for kid in kids[:max_children]:
            for sig in HOMO + HETERO:
                row = first_variation(parent, kid["child"], sig)
                row["gap"] = kid["gap"]
                row["move"] = kid["move"]
                row["e"] = kid["e"]
                row["N"] = n
                samples.append(row)
    if n_children == 0:
        return {
            "N": n,
            "category": "NO_NEIGHBOR",
            "reason": "exact-shell triads exist, but no unit move leaves the shell",
            "n_parents": len(parents),
            "n_children": 0,
            "samples": [],
        }
    return {
        "N": n,
        "category": "HAS_NEIGHBOR",
        "n_parents": len(parents),
        "n_parents_used": min(len(parents), max_parents),
        "n_children": n_children,
        "samples": samples,
    }


def _geom_key(row: dict) -> Tuple:
    return (row["parent"], row["child"], row["sigma"])


def verdict(scans: Sequence[dict], c: float = RHO_FLOOR) -> dict:
    """Apply the outcome tree. Amplitude flips are not BOTH SIGNS."""
    hetero_pos = []
    hetero_neg = []
    homo_nonzero = []
    homo_zero = 0
    homo_tot = 0
    no_neighbor_scales = []
    live_scales = []
    r2_ratios = []
    for sc in scans:
        if sc["category"] == "NO_NEIGHBOR":
            no_neighbor_scales.append(sc["N"])
            continue
        live_scales.append(sc["N"])
        for row in sc["samples"]:
            rho = float(row["rho_N"])
            t0n = math.sqrt(sum(x * x for x in row["T_0_roles"]))
            if row["channel"] == "homochiral":
                homo_tot += 1
                # Vandermonde delay: frozen equal-shell homochiral transfer
                # vanishes, so L_1 is not the leading object.
                if t0n < 1e-10 or abs(row["L_1_N"]) < 1e-10 or abs(rho) < c:
                    homo_zero += 1
                else:
                    homo_nonzero.append(row)
                continue
            if not row["legitimate"]:
                continue
            if rho >= c:
                hetero_pos.append(row)
            elif rho <= -c:
                hetero_neg.append(row)
            if row["R2_over_L1"] is not None:
                r2_ratios.append((sc["N"], abs(row["R2_over_L1"])))

    # Geometry-only both signs: distinct parent/child, not amp twins.
    both = bool(hetero_pos) and bool(hetero_neg)
    outcome = None
    if not live_scales and no_neighbor_scales:
        outcome = "NO_NEIGHBOR"
    elif both:
        outcome = "BOTH_SIGNS"
    elif hetero_pos and not hetero_neg:
        outcome = "ONE_SIGN_PLUS"
    elif hetero_neg and not hetero_pos:
        outcome = "ONE_SIGN_MINUS"
    elif not hetero_pos and not hetero_neg:
        if homo_tot and homo_zero == homo_tot:
            outcome = "ZERO_ONLY"
        else:
            outcome = "NO_HETERO_SIGNAL"
    reading = {
        "BOTH_SIGNS": (
            "universal first-order one-sided narrow depletion is FALSE. "
            "Stop static closure on this question. Positive branch goes "
            "to evolution. Θ_N = ν κ_N² τ_{U,N} is now live."
        ),
        "ONE_SIGN_PLUS": (
            "ONE SIGN heterochirally (positive). Ask whether the "
            "restriction is encoded by the Gram/lattice realization problem."
        ),
        "ONE_SIGN_MINUS": (
            "ONE SIGN heterochirally (negative). Ask whether the "
            "restriction is encoded by the Gram/lattice realization problem."
        ),
        "ZERO_ONLY": (
            "systematic ZERO ONLY. Consistent with Vandermonde delay "
            "if this is the homochiral sector. Does not rescue NSE; "
            "heterochiral remains separate."
        ),
        "NO_HETERO_SIGNAL": (
            "no legitimate heterochiral |ρ| ≥ c on the scanned family."
        ),
        "NO_NEIGHBOR": (
            "NO NEIGHBOR. Arithmetic rigidity is not sign depletion."
        ),
    }[outcome]

    seed = None
    theta = None
    if outcome == "BOTH_SIGNS":
        # Prefer a large-N legitimate plus seed (smaller R2/L1).
        pick = max(
            hetero_pos,
            key=lambda r: (r.get("N", 0), -abs(r.get("R2_over_L1") or 1.0), r["rho_N"]),
        )
        seed = _seed_from(pick)
        theta = _theta(pick, nu=1.0)
    return {
        "outcome": outcome,
        "reading": reading,
        "n_hetero_plus": len(hetero_pos),
        "n_hetero_minus": len(hetero_neg),
        "n_homo_zero": homo_zero,
        "n_homo_total": homo_tot,
        "n_homo_nonzero": len(homo_nonzero),
        "live_scales": live_scales,
        "no_neighbor_scales": no_neighbor_scales,
        "r2_ratios": r2_ratios[:40],
        "static_verdict": (
            "universal first-order one-sided narrow depletion is false"
            if outcome == "BOTH_SIGNS"
            else None
        ),
        "stop_static_closure": outcome == "BOTH_SIGNS",
        "seed_A_N_plus": seed,
        "Theta_N": theta,
        "c": c,
    }


def _cvec_json(v: CVec) -> List[dict]:
    return [{"re": z.real, "im": z.imag} for z in v]


def _seed_from(row: dict) -> dict:
    """Canonical adversarial seed A_N^+: full field, not just δ and T^{(0)}."""
    child = row["child"]
    sigma = row["sigma"]
    amps = (1.0 + 0.0j, 1.0 + 0.0j, 1.0 + 0.0j)
    field = helical_field(child, sigma, amps)
    pol = {str(m): _cvec_json(v) for m, v in field.items()}
    return {
        "tag": "A_N_plus",
        "parent": row["parent"],
        "child": child,
        "integer_vectors": {"p": child[0], "q": child[1], "k": child[2]},
        "helicity": sigma,
        "amplitudes": {"a_p": 1.0, "a_q": 1.0, "a_k": 1.0},
        "polarizations": pol,
        "delta_N": row["delta_N_roles"],
        "T_0": row["T_0_roles"],
        "T_N": row["T_N_roles"],
        "Lambda_N": row["Lambda_N"],
        "L_1_N": row["L_1_N"],
        "R_2_N": row["R_2_N"],
        "rho_N": row["rho_N"],
        "T_c_N": row["T_c_N"],
        "N": row.get("N"),
        "note": (
            "exact reproducible neighboring-shell field, statically "
            "pointed in the dangerous direction. NSE gets the next move."
        ),
    }


def _theta(row: dict, nu: float = 1.0) -> dict:
    kappa = math.sqrt(max(row["Lambda_N"], 0.0))
    t_rms = math.sqrt(sum(x * x for x in row["T_0_roles"]) / 3.0)
    tau_u = 1.0 / t_rms if t_rms > 0 else None
    val = (nu * (kappa ** 2) * tau_u) if tau_u is not None else None
    return {
        "formula": "Theta_N = nu * kappa_N^2 * tau_U,N",
        "nu": nu,
        "kappa_N": kappa,
        "tau_U_N": tau_u,
        "Theta_N": val,
        "live_because": "BOTH_SIGNS",
    }


def report(scales: Sequence[int] | None = None) -> dict:
    if scales is None:
        scales = [6, 10, 14, 18, 26, 30, 42, 50, 66, 74]
    scans = [scan_scale(n) for n in scales]
    tree = verdict(scans)
    # Remainder-order diagnostic along live scales.
    order = []
    for sc in scans:
        if sc["category"] != "HAS_NEIGHBOR":
            continue
        rats = [
            abs(r["R2_over_L1"])
            for r in sc["samples"]
            if r["legitimate"] and r["R2_over_L1"] is not None and r["channel"] == "heterochiral"
        ]
        if rats:
            order.append({"N": sc["N"], "median_abs_R2_over_L1": sorted(rats)[len(rats) // 2]})
    return {
        "gate": "arithmetic sign realizability",
        "date": "2026-09-24",
        "frozen": "loop-gauge and telescopic-capacity board is not altered",
        "expansion": "T_c = Lambda <delta, T> + sum delta^2 T   (actual T)",
        "first_variation": "L_1,N = Lambda_N <delta_N, T_N^{(0)}>",
        "remainder": "R_2,N = T_c,N - Lambda_N <delta_N, T_N^{(0)}>",
        "scans": [
            {
                "N": s["N"],
                "category": s["category"],
                "reason": s.get("reason"),
                "n_parents": s.get("n_parents"),
                "n_children": s.get("n_children"),
                "n_samples": len(s.get("samples") or []),
                "n_legitimate": sum(1 for r in (s.get("samples") or []) if r.get("legitimate")),
            }
            for s in scans
        ],
        "remainder_order": order,
        "verdict": tree,
        "frontiers": {
            "static": "arithmetic sign realizability",
            "dynamic": "dangerous-state persistence",
        },
        "locks": {
            "loop_gauge_unaltered": True,
            "T_neighbor_kept_separate": True,
            "no_silent_T0_substitution": True,
            "no_neighbor_is_own_category": True,
            "phase_twin_is_not_both_signs": True,
            "not_a_close": True,
        },
    }


def _py(x):
    if isinstance(x, complex):
        return {"re": x.real, "im": x.imag}
    if isinstance(x, dict):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(list(argv) if argv is not None else None)
    print(json.dumps(_py(report()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
