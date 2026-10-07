"""Priority 2 — exact-family signed efficiency probe (NUMERICAL).

Optimizes signed transfer on the exact 32-shape list under
reality + divergence-free constraints (finite search).

Not a proof. Not criterion (17). Not Clay. Not swirl closure.
"""
from __future__ import annotations

from math import isqrt, sqrt
from pathlib import Path
import json
import numpy as np

# Exact lists (Oct 7 handoff)
FAMILY_5_25_THIRDS = [
    8, 10, 14, 18, 20, 22, 24, 26, 30,
    34, 36, 38, 40, 42, 46, 50, 52,
]
FAMILY_9_25_ACTIVE = [
    6, 10, 12, 14, 16, 24, 30, 34,
    38, 44, 52, 54, 56, 58, 62,
]
RHO = 0.6318550823987903
RHO_PRIME = 0.8253067330268596
RHO_PLUS_3_RHO_PRIME = RHO + 3 * RHO_PRIME


def radius(k):
    return int(k[0] * k[0] + k[1] * k[1] + k[2] * k[2])


def lattice_shell(r2: int):
    R = isqrt(r2) + 1
    return [
        (x, y, z)
        for x in range(-R, R + 1)
        for y in range(-R, R + 1)
        for z in range(-R, R + 1)
        if x * x + y * y + z * z == r2
    ]


def first_witness_triad(a: int, b: int, c: int, shells):
    for p in shells[a]:
        for q in shells[b]:
            r = (-(p[0] + q[0]), -(p[1] + q[1]), -(p[2] + q[2]))
            if radius(r) == c:
                return p, q, r
    return None


def orthonormal_perp(k):
    kx, ky, kz = (float(t) for t in k)
    if abs(kx) + abs(ky) < 1e-15:
        a = np.array([1.0, 0.0, 0.0])
    else:
        a = np.array([-ky, kx, 0.0])
    e1 = a / np.linalg.norm(a)
    e2 = np.cross(np.array([kx, ky, kz], float), e1)
    e2 /= np.linalg.norm(e2)
    return e1, e2


def make_field(modes, phases, amps, pols):
    u = {}
    for p, ph, amp, pol in zip(modes, phases, amps, pols):
        mp = (-p[0], -p[1], -p[2])
        uk = 1j * amp * np.exp(1j * ph) * pol
        u[p] = (complex(uk[0]), complex(uk[1]), complex(uk[2]))
        if mp != p:
            u[mp] = (uk[0].conjugate(), uk[1].conjugate(), uk[2].conjugate())
    return u


def T_on_triad(u, p, q, r, a, b, c):
    """Polarized transfer contribution of one representative triad."""
    up, uq, ur = u.get(p), u.get(q), u.get(r)
    if up is None or uq is None or ur is None:
        return 0.0
    Ip = (q[0] * up[0] + q[1] * up[1] + q[2] * up[2]) * (
        uq[0] * ur[0] + uq[1] * ur[1] + uq[2] * ur[2]
    )
    Iq = (r[0] * uq[0] + r[1] * uq[1] + r[2] * uq[2]) * (
        ur[0] * up[0] + ur[1] * up[1] + ur[2] * up[2]
    )
    Ir = (p[0] * ur[0] + p[1] * ur[1] + p[2] * ur[2]) * (
        up[0] * uq[0] + up[1] * uq[1] + up[2] * uq[2]
    )
    return float(((c - b) * Ip + (a - c) * Iq + (b - a) * Ir).imag)


def energy_dissipation(modes, amps):
    """Energy / dissipation proxy on independent Hermitian mode amplitudes."""
    E = float(np.sum(amps * amps))
    Y = float(sum(radius(k) * (a * a) for k, a in zip(modes, amps)))
    return E, Y


def shell_phase_probe(shapes, rng, n_restarts=40, n_passes=10, grid=24):
    labels = sorted({s for sh in shapes for s in sh})
    idx = {lab: i for i, lab in enumerate(labels)}
    S = len(labels)

    def score(phases):
        ts = np.array(
            [np.cos(phases[idx[a]] + phases[idx[b]] + phases[idx[c]]) for a, b, c in shapes]
        )
        abs_sum = float(np.sum(np.abs(ts)))
        signed = float(np.sum(ts))
        ratio = abs(signed) / abs_sum if abs_sum > 1e-30 else 0.0
        return signed, abs_sum, ratio, ts

    best = {"ratio": -1.0}
    for restart in range(n_restarts):
        ph = rng.uniform(0, 2 * np.pi, size=S)
        signed, abs_sum, ratio, ts = score(ph)
        for _ in range(n_passes):
            improved = False
            for i in rng.permutation(S):
                best_abs, best_ph = abs(signed), ph[i]
                best_pack = (signed, abs_sum, ratio, ts)
                for trial in np.linspace(0, 2 * np.pi, grid, endpoint=False):
                    ph[i] = trial
                    s2, a2, r2, t2 = score(ph)
                    if abs(s2) > best_abs + 1e-14:
                        best_abs, best_ph = abs(s2), trial
                        best_pack = (s2, a2, r2, t2)
                        improved = True
                ph[i] = best_ph
                signed, abs_sum, ratio, ts = best_pack
            if not improved:
                break
        if ratio > best["ratio"]:
            best = {
                "ratio": float(ratio),
                "sum_signed": float(signed),
                "sum_abs": float(abs_sum),
                "n_nonzero": int(np.sum(np.abs(ts) > 1e-12)),
                "restart": int(restart),
            }
    rand = [score(rng.uniform(0, 2 * np.pi, size=S))[2] for _ in range(80)]
    return {
        "n_shapes": len(shapes),
        "n_shell_labels": S,
        "shell_labels": labels,
        "worst_case_coherent": best,
        "random_phase_baseline": {
            "ratio_mean": float(np.mean(rand)),
            "ratio_max": float(np.max(rand)),
            "ratio_median": float(np.median(rand)),
            "n_samples": len(rand),
        },
        "reading": (
            "ratio=1 means common signs among nonzero cos contributions "
            "on the exact 32 list — not geometric-bound saturation"
        ),
    }


def representative_df_probe(shapes, shells, rng, n_restarts=12, n_passes=5, grid=12):
    triads = []
    for a, b, c in shapes:
        w = first_witness_triad(a, b, c, shells)
        if w is None:
            raise RuntimeError(f"missing witness for {(a, b, c)}")
        triads.append((a, b, c, w[0], w[1], w[2]))

    # Unique modes up to Hermitian pair
    modes, seen = [], set()
    for _, _, _, p, q, r in triads:
        for k in (p, q, r):
            key = tuple(sorted((k, (-k[0], -k[1], -k[2]))))
            if key in seen:
                continue
            seen.add(key)
            modes.append(k)
    n = len(modes)
    amps = np.ones(n) / sqrt(n)

    def random_pols():
        pols = []
        for p in modes:
            e1, e2 = orthonormal_perp(p)
            th = float(rng.uniform(0, 2 * np.pi))
            pols.append(np.cos(th) * e1 + np.sin(th) * e2)
        return pols

    def score(phases, pols):
        u = make_field(modes, phases, amps, pols)
        ts = np.array(
            [T_on_triad(u, p, q, r, a, b, c) for a, b, c, p, q, r in triads], float
        )
        abs_sum = float(np.sum(np.abs(ts)))
        signed = float(np.sum(ts))
        ratio = abs(signed) / abs_sum if abs_sum > 1e-30 else 0.0
        E, Y = energy_dissipation(modes, amps)
        budget = RHO_PLUS_3_RHO_PRIME * sqrt(max(E, 0.0)) * Y
        eta = abs(signed) / budget if budget > 1e-30 else None
        return {
            "sum_signed": signed,
            "sum_abs": abs_sum,
            "coherence_ratio": ratio,
            "E": float(E),
            "Y": float(Y),
            "budget_proxy": float(budget),
            "eta_eff": float(eta) if eta is not None else None,
            "ts": ts,
        }

    best = {"coherence_ratio": -1.0, "abs_signed": -1.0}
    for restart in range(n_restarts):
        phases = rng.uniform(0, 2 * np.pi, size=n)
        pols = random_pols()
        pack = score(phases, pols)
        for _ in range(n_passes):
            improved = False
            for i in rng.permutation(n):
                best_abs, best_ph = abs(pack["sum_signed"]), phases[i]
                best_pack = pack
                for trial in np.linspace(0, 2 * np.pi, grid, endpoint=False):
                    phases[i] = trial
                    p2 = score(phases, pols)
                    if abs(p2["sum_signed"]) > best_abs + 1e-14:
                        best_abs, best_ph = abs(p2["sum_signed"]), trial
                        best_pack = p2
                        improved = True
                phases[i] = best_ph
                pack = best_pack
            # light polarization refresh on a few modes
            for i in rng.choice(n, size=min(6, n), replace=False):
                e1, e2 = orthonormal_perp(modes[i])
                base = pols[i].copy()
                best_abs = abs(pack["sum_signed"])
                best_pol = base
                for th in np.linspace(0, 2 * np.pi, 8, endpoint=False):
                    pols[i] = np.cos(th) * e1 + np.sin(th) * e2
                    p2 = score(phases, pols)
                    if abs(p2["sum_signed"]) > best_abs + 1e-14:
                        best_abs = abs(p2["sum_signed"])
                        best_pol = pols[i].copy()
                        pack = p2
                        improved = True
                pols[i] = best_pol
            if not improved:
                break
        key = (abs(pack["sum_signed"]), pack["coherence_ratio"])
        if key > (best.get("abs_signed", -1.0), best.get("coherence_ratio", -1.0)):
            best = {
                "abs_signed": abs(pack["sum_signed"]),
                "sum_signed": float(pack["sum_signed"]),
                "sum_abs": float(pack["sum_abs"]),
                "coherence_ratio": float(pack["coherence_ratio"]),
                "E": pack["E"],
                "Y": pack["Y"],
                "budget_proxy": pack["budget_proxy"],
                "eta_eff": pack["eta_eff"],
                "restart": int(restart),
                "n_modes": n,
                "n_shapes": len(shapes),
                "max_abs_shape": float(np.max(np.abs(pack["ts"]))) if len(pack["ts"]) else 0.0,
            }

    rand_eta, rand_coh = [], []
    for _ in range(40):
        phases = rng.uniform(0, 2 * np.pi, size=n)
        pack = score(phases, random_pols())
        if pack["eta_eff"] is not None:
            rand_eta.append(pack["eta_eff"])
        rand_coh.append(pack["coherence_ratio"])

    return {
        "note": (
            "One lattice witness triad per exact shape; shared DF modes across "
            "overlapping witnesses. Finite coordinate ascent. Not a full-shell sum."
        ),
        "worst_case_search": best,
        "random_baseline": {
            "coherence_ratio_mean": float(np.mean(rand_coh)),
            "coherence_ratio_max": float(np.max(rand_coh)),
            "eta_eff_mean": float(np.mean(rand_eta)) if rand_eta else None,
            "eta_eff_max": float(np.max(rand_eta)) if rand_eta else None,
            "n_samples": len(rand_coh),
        },
        "budget_proxy_definition": (
            "B_proxy = (ρ+3ρ') √E Y with E=∑|û_k|², Y=∑|k|²|û_k|² "
            "on the representative-mode field; numerical face only"
        ),
        "rho_plus_3_rho_prime": RHO_PLUS_3_RHO_PRIME,
    }


def main():
    rng = np.random.default_rng(20261007)
    shapes = [(5, b, 25) for b in FAMILY_5_25_THIRDS] + [
        (9, b, 25) for b in FAMILY_9_25_ACTIVE
    ]
    assert len(shapes) == 32

    shells_needed = sorted({5, 9, 25} | set(FAMILY_5_25_THIRDS) | set(FAMILY_9_25_ACTIVE))
    shells = {r: lattice_shell(r) for r in shells_needed}

    shell_phase = shell_phase_probe(shapes, rng)
    rep_df = representative_df_probe(shapes, shells, rng)

    out = {
        "status": "NUMERICAL",
        "family": {
            "n_shapes": 32,
            "original_17": [(5, b, 25) for b in FAMILY_5_25_THIRDS],
            "added_15": [(9, b, 25) for b in FAMILY_9_25_ACTIVE],
            "dilation": "n=1 only in this probe",
        },
        "shell_phase_exact_32": shell_phase,
        "representative_triad_df": rep_df,
        "reading": {
            "shell_phase": (
                "If worst_case_coherent.ratio hits 1 on the exact list, common "
                "signs are attainable; that does not saturate geometric C_b bounds."
            ),
            "representative_df": (
                "Compare coherence_ratio and eta_eff under DF+reality. "
                "eta_eff uses a proxy budget, not the paper high-pass lemma."
            ),
            "next_analytic": (
                "Signed multi-shape lemma still Open; this search only constrains "
                "optimistic cancellation hopes on the exact family."
            ),
        },
        "not_claimed": [
            "criterion (17)",
            "global regularity",
            "swirl closure",
            "optimality of rho+3rho'",
            "full-lattice shell sums",
        ],
    }
    path = Path(__file__).with_name("SIGNED-EFFICIENCY-PROBE.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
