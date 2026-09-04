#!/usr/bin/env python3
"""
Occupation time of 3-CONC vs SPREAD.

One threshold. The clock covers. High j* dies fast on a packet
budget. Leray ∫X dt < ∞ does not make CONC short.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from track_b_lemmas import packet_stats, rec


def occupation(sigma: np.ndarray, dt: float, thresh: float = 0.5) -> dict:
    # Partition: threshold sits on CONC. A cover that double-counts is not a clock.
    conc = sigma >= thresh
    spread = ~conc
    return {
        "tau_conc": float(np.sum(conc) * dt),
        "tau_spread": float(np.sum(spread) * dt),
        "T": float(len(sigma) * dt),
        "switches": int(np.sum(conc[1:] != conc[:-1])) if len(sigma) > 1 else 0,
    }


def clock_paths(n: int = 800, seed: int = 11) -> dict:
    rng = np.random.default_rng(seed)
    dt = 1.0 / n
    rows = []
    # stay CONC, stay SPREAD, switch, random walk on σ
    sigmas = [
        np.full(n, 0.8),
        np.full(n, 0.2),
        np.where(np.arange(n) % 40 < 20, 0.7, 0.3),
        np.clip(0.5 + 0.4 * np.sin(np.linspace(0, 8 * math.pi, n)), 0.0, 1.0),
    ]
    for i in range(6):
        x = rng.random((n, 8))
        sigmas.append(np.array([packet_stats(row)["sigma"] for row in x]))
    gaps = 0
    for sig in sigmas:
        occ = occupation(sig, dt)
        if abs(occ["tau_conc"] + occ["tau_spread"] - occ["T"]) > 1e-9:
            gaps += 1
        rows.append(occ)
    return {"rows": rows, "gaps": gaps, "ok": gaps == 0}


def high_jstar_decay(nu: float = 0.1, x0: float = 1.2) -> dict:
    """Ẋ = X³ − ν 2^{2j*} X. Time while X stays above 1, vs j*."""
    rows = []
    for jstar in (2, 3, 4, 5, 6):
        gamma = nu * (2.0 ** (2 * jstar))
        # explicit Euler on a short window
        dt = min(1e-4, 0.05 / max(gamma, 1.0))
        t = 0.0
        x = x0
        taut = 0.0
        steps = 0
        while t < 2.0 and x > 1e-6 and steps < 200000:
            if x >= 1.0:
                taut += dt
            x = x + dt * (x**3 - gamma * x)
            x = max(x, 0.0)
            t += dt
            steps += 1
            if x > 50.0:
                break
        rows.append(
            {
                "jstar": jstar,
                "gamma": gamma,
                "tau_hot": taut,
                "scale": 1.0 / gamma,
            }
        )
    hot = [r["tau_hot"] for r in rows]
    # High j* should occupy less hot time than low j*.
    shorter = hot[-1] < hot[0] * 0.5
    return {"rows": rows, "hot": hot, "ok": shorter}


def leray_spike_in_conc(tstar: float = 1.0, n: int = 4000) -> dict:
    """CONC the whole time, X = (T*−t)^{-1/2}. ∫X finite, X unbounded."""
    t = np.linspace(0.0, tstar - 1e-4, n)
    dt = float(t[1] - t[0])
    x = (tstar - t) ** (-0.5)
    sigma = np.full_like(t, 0.8)
    occ = occupation(sigma, dt)
    integ = float(np.trapezoid(x, t))
    return {
        "tau_conc": occ["tau_conc"],
        "T": occ["T"],
        "integral_X": integ,
        "X_max": float(np.max(x)),
        "occupies_almost_all": occ["tau_conc"] > 0.9 * occ["T"],
        "X_unbounded": float(np.max(x)) > 50.0,
    }


def lemma_clock() -> dict:
    paths = clock_paths()
    return rec(
        "B8_occupation_clock",
        "τ_CONC + τ_SPREAD = T at threshold σ = 1/2. Switching allowed.",
        "pass" if paths["ok"] else "fail",
        "One threshold, no gap. A clock, not a bound on X.",
        paths=paths,
    )


def lemma_high_jstar() -> dict:
    dec = high_jstar_decay()
    return rec(
        "B8a_high_jstar_short",
        "packet budget Ẋ = X³ − ν 2^{2j*} X: hot occupation falls as j* rises",
        "pass" if dec["ok"] else "fail",
        "B4c’s scale. High packets cannot sit hot for long on that ODE.",
        decay=dec,
    )


def lemma_leray_not_short() -> dict:
    spike = leray_spike_in_conc()
    killed = spike["occupies_almost_all"] and spike["X_unbounded"]
    return rec(
        "B8b_leray_not_occupation",
        "Leray ∫X dt < ∞ ⇒ occupation of 3-CONC is short",
        "fail" if killed else "open",
        "Sit in CONC with X = (T*−t)^{-1/2}. The integral is finite. The clock runs the whole interval.",
        spike=spike,
    )


def lemma_occupation_not_close() -> dict:
    return rec(
        "B8c_occupation_not_X_bound",
        "occupation-time bookkeeping closes a bound for X",
        "fail",
        "B8b sits in CONC the whole interval with unbounded X. Short NS paths occupy CONC fully; the bound, when it sits, is viscosity. The clock did not write X∈L∞.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_clock(),
        lemma_high_jstar(),
        lemma_leray_not_short(),
        lemma_occupation_not_close(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "occupation time",
            "threshold": "sigma = 1/2",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Climb and DNS knobs at n=32 are scored. DNS is not an a priori (B13f). "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not write c=8 into the PDE."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_occupation.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Occupation time. Two-regime clock.")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
