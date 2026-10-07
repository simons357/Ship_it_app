#!/usr/bin/env python3
"""Second Gate B test: signed Q_x, cancellation preserved.

The nonnegative majorant cannot supply the desired gain by
regrouping. This probe keeps the exact signed receiver form

    T_abc = (c-b) Im I_p + (a-c) Im I_q + (b-a) Im I_r

on one globally compatible divergence-free field, groups
Q_x^{sgn} on the low vertex, and asks whether ||Q^{sgn}||_2 / Ω
can beat Λ^{1/2}.

Not a theorem. Not (17). NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_attacks.qx_kernel import (  # noqa: E402
    C_abc,
    df_mode,
    df_residual,
    energy_enstrophy,
    equal_energy_amplitudes,
    l2,
    nonnegative_Q,
    occupied_shells,
    similar_seed_triad,
    subnet_triads,
    theta_hat,
    triad_T_signed,
)


TWO_PI = 2.0 * math.pi


def _unit_field(triads, f, phases, pols):
    """û on every vertex, amplitude = shell amplitude, DF polarizations."""
    u = {}
    for p, q, r, a, b, c in triads:
        for k, shell in ((p, a), (q, b), (r, c)):
            if k in u:
                continue
            amp = f.get(shell, 0.0)
            ph = phases.get(k, 0.0)
            pol = pols.get(k, 0.0)
            u[k] = df_mode(k, amp, ph, pol)
    return u


def signed_Q_and_T(triads, f, phases, pols) -> tuple[dict[int, float], float, float]:
    field = _unit_field(triads, f, phases, pols)
    Q: dict[int, float] = {x: 0.0 for x in f}
    T = 0.0
    abs_sum = 0.0
    for p, q, r, a, b, c in triads:
        t = triad_T_signed(p, q, r, field[p], field[q], field[r])
        T += t
        abs_sum += abs(t)
        fa = f.get(a, 0.0)
        if fa > 0:
            Q[a] = Q.get(a, 0.0) + t / fa
    return Q, T, abs_sum


def majorant_ok(triads, f, T_abs_sum, atol=1e-8) -> bool:
    """Σ |T_abc| ≤ Σ C_abc f_a f_b f_c  (signed terms vs nonnegative envelope)."""
    envelope = 0.0
    for _p, _q, _r, a, b, c in triads:
        envelope += C_abc(a, b, c) * f.get(a, 0.0) * f.get(b, 0.0) * f.get(c, 0.0)
    return T_abs_sum <= envelope + atol * max(1.0, envelope)


def random_angles(keys, rng):
    return {k: rng.uniform(0.0, TWO_PI) for k in keys}


def keys_of(triads):
    seen = set()
    out = []
    for p, q, r, *_rest in triads:
        for k in (p, q, r):
            if k not in seen:
                seen.add(k)
                out.append(k)
    return out


def coordinate_ascent(
    triads,
    f,
    rng,
    n_restarts: int = 4,
    n_passes: int = 3,
    grid: int = 8,
    maximize: str = "Q2",
) -> dict:
    """Maximize ||Q^{sgn}||_2 or |T| over phases/polarizations. Shared û_w."""
    ks = keys_of(triads)
    grid_angles = [TWO_PI * i / grid for i in range(grid)]
    best = {
        "Q2": -1.0,
        "T": 0.0,
        "abs_sum": 0.0,
        "coherence": 0.0,
        "phases": {},
        "pols": {},
    }

    def score(phases, pols):
        Q, T, abs_sum = signed_Q_and_T(triads, f, phases, pols)
        Q2 = l2(Q.values())
        coh = abs(T) / abs_sum if abs_sum > 0 else 0.0
        target = Q2 if maximize == "Q2" else abs(T)
        return target, Q2, T, abs_sum, coh, Q

    for _restart in range(n_restarts):
        phases = random_angles(ks, rng)
        pols = random_angles(ks, rng)
        # Shared w is one key in `ks`; updating it once per pass is the
        # shared-mode constraint. Per-triad u,v stay independent DF modes.
        target, Q2, T, abs_sum, coh, _Q = score(phases, pols)
        for _pass in range(n_passes):
            for k in ks:
                best_local = target
                best_ph, best_pol = phases[k], pols[k]
                for ph in grid_angles:
                    for pol in grid_angles:
                        phases[k] = ph
                        pols[k] = pol
                        tgt, q2, t, ab, c, _ = score(phases, pols)
                        if tgt > best_local:
                            best_local = tgt
                            best_ph, best_pol = ph, pol
                            target, Q2, T, abs_sum, coh = tgt, q2, t, ab, c
                phases[k] = best_ph
                pols[k] = best_pol
        if Q2 > best["Q2"]:
            best = {
                "Q2": Q2,
                "T": T,
                "abs_sum": abs_sum,
                "coherence": coh,
                "phases": dict(phases),
                "pols": dict(pols),
            }
    Q, T, abs_sum = signed_Q_and_T(triads, f, best["phases"], best["pols"])
    best["Q"] = Q
    best["T"] = T
    best["abs_sum"] = abs_sum
    best["coherence"] = abs(T) / abs_sum if abs_sum else 0.0
    best["Q2"] = l2(Q.values())
    return best


def random_baseline(triads, f, rng, n_samples: int = 40) -> dict:
    ks = keys_of(triads)
    Q2s, cohs, Ts = [], [], []
    for _ in range(n_samples):
        phases = random_angles(ks, rng)
        pols = random_angles(ks, rng)
        Q, T, abs_sum = signed_Q_and_T(triads, f, phases, pols)
        Q2s.append(l2(Q.values()))
        Ts.append(abs(T))
        cohs.append(abs(T) / abs_sum if abs_sum else 0.0)
    Q2s.sort()
    return {
        "n_samples": n_samples,
        "Q2_mean": sum(Q2s) / n_samples,
        "Q2_max": Q2s[-1],
        "Q2_median": Q2s[n_samples // 2],
        "coherence_mean": sum(cohs) / n_samples,
        "coherence_max": max(cohs),
        "abs_T_mean": sum(Ts) / n_samples,
        "abs_T_max": max(Ts),
    }


def single_triad_signed(n: int, rng) -> dict:
    triads = [similar_seed_triad(n)]
    u, v, w, a, b, c = triads[0]
    f = equal_energy_amplitudes([a, b, c])
    Qplus = nonnegative_Q(triads, f)
    E, Omega, Lam = energy_enstrophy(f)
    adv = coordinate_ascent(
        triads, f, rng, n_restarts=3, n_passes=2, grid=6, maximize="Q2"
    )
    field_res = max(
        df_residual(k, df_mode(k, 1.0, adv["phases"][k], adv["pols"][k]))
        for k in (u, v, w)
    )
    envelope = C_abc(a, b, c) * f[a] * f[b] * f[c]
    return {
        "n": n,
        "Lambda": Lam,
        "E": E,
        "Omega": Omega,
        "Qplus2": l2(Qplus.values()),
        "Qplus2_over_Omega": l2(Qplus.values()) / Omega,
        "Qsgn2": adv["Q2"],
        "Qsgn2_over_Omega": adv["Q2"] / Omega,
        "T": adv["T"],
        "abs_T": abs(adv["T"]),
        "envelope_Cfff": envelope,
        "signed_le_majorant": abs(adv["T"]) <= envelope + 1e-8 * max(1.0, envelope),
        "coherence": adv["coherence"],
        "df_residual_max": field_res,
        "ratio_Qsgn_to_Qplus": adv["Q2"] / l2(Qplus.values()) if Qplus else float("nan"),
    }


def subnet_signed(n: int, rng) -> dict:
    triads = subnet_triads(n)
    shells = occupied_shells(triads)
    f = equal_energy_amplitudes(shells)
    Qplus = nonnegative_Q(triads, f)
    E, Omega, Lam = energy_enstrophy(f)
    Qplus2 = l2(Qplus.values())
    adv = coordinate_ascent(
        triads, f, rng, n_restarts=2, n_passes=2, grid=6, maximize="Q2"
    )
    base = random_baseline(triads, f, rng, n_samples=24)
    T_plus = sum(f[x] * Qplus[x] for x in f)
    T_sgn = sum(f[x] * adv["Q"][x] for x in f)
    return {
        "n": n,
        "c": 2 * n * n,
        "Lambda": Lam,
        "n_triads": len(triads),
        "M_shells": len(shells),
        "n_modes": len(keys_of(triads)),
        "E": E,
        "Omega": Omega,
        "Qplus2": Qplus2,
        "Qplus2_over_Omega": Qplus2 / Omega,
        "Qsgn2_adversary": adv["Q2"],
        "Qsgn2_over_Omega_adversary": adv["Q2"] / Omega,
        "coherence_adversary": adv["coherence"],
        "T_adversary": adv["T"],
        "abs_sum_adversary": adv["abs_sum"],
        "majorant_holds": majorant_ok(triads, f, adv["abs_sum"]),
        "T_plus": T_plus,
        "T_signed_reassembled": T_sgn,
        "reassembly_identity": abs(T_sgn - adv["T"]) <= 1e-8 * max(1.0, abs(adv["T"])),
        "random_baseline": base,
        "signed_gain_vs_nonneg": (adv["Q2"] / Qplus2) if Qplus2 else float("nan"),
        "random_Q2_over_Omega": base["Q2_mean"] / Omega,
    }


def report(seed: int = 0) -> dict:
    rng = random.Random(seed)
    single_ns = (4, 8)
    single_rows = [single_triad_signed(n, rng) for n in single_ns]
    single_theta_plus = theta_hat(
        single_rows[0]["Qplus2_over_Omega"],
        single_rows[1]["Qplus2_over_Omega"],
        single_rows[0]["Lambda"],
        single_rows[1]["Lambda"],
    )
    single_theta_sgn = theta_hat(
        single_rows[0]["Qsgn2_over_Omega"],
        single_rows[1]["Qsgn2_over_Omega"],
        single_rows[0]["Lambda"],
        single_rows[1]["Lambda"],
    )

    subnet_ns = (4, 6, 8)
    subnet_rows = [subnet_signed(n, rng) for n in subnet_ns]
    subnet_theta_plus = [
        {
            "from_n": subnet_rows[i]["n"],
            "to_n": subnet_rows[i + 1]["n"],
            "theta_hat_nonneg": theta_hat(
                subnet_rows[i]["Qplus2_over_Omega"],
                subnet_rows[i + 1]["Qplus2_over_Omega"],
                subnet_rows[i]["Lambda"],
                subnet_rows[i + 1]["Lambda"],
            ),
            "theta_hat_signed_adversary": theta_hat(
                subnet_rows[i]["Qsgn2_over_Omega_adversary"],
                subnet_rows[i + 1]["Qsgn2_over_Omega_adversary"],
                subnet_rows[i]["Lambda"],
                subnet_rows[i + 1]["Lambda"],
            ),
            "theta_hat_signed_random": theta_hat(
                subnet_rows[i]["random_Q2_over_Omega"],
                subnet_rows[i + 1]["random_Q2_over_Omega"],
                subnet_rows[i]["Lambda"],
                subnet_rows[i + 1]["Lambda"],
            ),
        }
        for i in range(len(subnet_rows) - 1)
    ]

    adv_thetas = [row["theta_hat_signed_adversary"] for row in subnet_theta_plus]
    mean_adv = sum(adv_thetas) / len(adv_thetas)
    rand_thetas = [row["theta_hat_signed_random"] for row in subnet_theta_plus]
    mean_rand = sum(rand_thetas) / len(rand_thetas)
    factors = [row["signed_gain_vs_nonneg"] for row in subnet_rows]
    mean_factor = sum(factors) / len(factors)
    factor_spread = max(factors) - min(factors)
    # A power gain would need a stable hat clearly below 1/2.
    # n=4,6,8 hats jump (e.g. 0.16 then 0.64); do not read that as beating 1/2.
    hats_stable_below_half = mean_adv < 0.40 and max(adv_thetas) < 0.45
    factor_only = factor_spread < 0.05 and 0.05 < mean_factor < 0.9
    beats_half = hats_stable_below_half and not factor_only
    random_looks_smaller = mean_rand < mean_adv - 0.05

    return {
        "object": "signed Q_x from exact T_abc, one DF Hermitian-capable field",
        "definition": {
            "T_abc": "(c-b) Im I_p + (a-c) Im I_q + (b-a) Im I_r",
            "Q_x_signed": "sum_{triads with low vertex x} T_abc / f_x",
            "identity": "sum_x f_x Q_x^{sgn} = sum T_abc",
            "constraint": "one globally compatible DF field; shared w on the subnet",
            "forbidden": "no |sum S| -> sum |S| before grouping",
        },
        "single_triad": {
            "rows": [
                {k: v for k, v in row.items() if k not in ("phases", "pols", "Q")}
                for row in single_rows
            ],
            "theta_hat_nonneg": single_theta_plus,
            "theta_hat_signed_adversary": single_theta_sgn,
            "note": (
                "A single triad has nothing to cancel against. "
                "Signed |T| stays under the C-majorant; theta stays 1/2."
            ),
        },
        "subnet_shared_w": {
            "rows": subnet_rows,
            "theta_hats": subnet_theta_plus,
            "mean_theta_signed_adversary": mean_adv,
            "mean_theta_signed_random": mean_rand,
            "mean_Qsgn_over_Qplus": mean_factor,
            "Qsgn_over_Qplus_spread": factor_spread,
            "constant_factor_only_on_sample": factor_only,
            "coherent_adversary_beats_half_on_sample": beats_half,
            "random_phases_smaller_than_adversary": random_looks_smaller,
        },
        "reading": {
            "nonnegative_regrouping": "ruled out as a source of gain (theta >= 1/2, optimal open)",
            "single_triad_signed": "cannot beat the majorant; no cancellation available",
            "shared_w_adversary": (
                "finite DF search on the diagnostic subnet. A stable Q^{sgn}/Q^+ "
                "ratio is a constant geometric factor, not a drop of theta below 1/2. "
                "Unstable hats at n=4,6,8 are not a power. Random-phase means are "
                "optimistic and not a bound."
            ),
            "not_a_theorem": True,
        },
        "locks": {
            "preserves_signed_cancellation": True,
            "uses_exact_T_abc": True,
            "one_df_field": True,
            "no_abs_before_assembly": True,
            "theta_signed_proved": False,
            "theorem_17_proved": False,
            "not_a_close": True,
            "gate_A": "UNRESOLVED / DIAGNOSTIC ONLY",
            "gate_B_active": True,
            "seed": seed,
        },
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args(argv)
    payload = report(seed=args.seed)
    out = Path(__file__).with_name("SIGNED-CANCELLATION-TEST.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
