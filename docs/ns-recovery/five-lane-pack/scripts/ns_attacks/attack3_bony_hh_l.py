#!/usr/bin/env python3
"""Attack 3 — Bony HH→L channel bottleneck.

Decompose the nonlinear transfer into HH / HL / LL parent-wavevector channels
and measure which channel dominates the centered remainder Tc.

Prior note: HH→L is the live analytic bottleneck for closing product estimates
toward |Tc| ≤ C ||u||_2 X^{3/2} (or equiv). Numerics here only diagnose channel
size — they do not prove a Bony estimate.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ns_attacks.stokes_moments import (  # noqa: E402
    bony_channel_split,
    format_probe,
    high_triad_field,
    k_norm2,
    moments,
    nonlinear_B,
    probe,
    random_field,
    scale_field,
    two_shell_field,
)


def Tc_by_channel(field, k_cut: float) -> dict:
    """Recompute N,M,Tc with B restricted to each Bony channel."""
    from ns_attacks.stokes_moments import Field, leray_project

    keys = list(field.keys())
    B_chan = {"HH": {}, "HL": {}, "LL": {}}

    def add(ch, k, vec):
        B_chan[ch][k] = B_chan[ch].get(k, np.zeros(3, dtype=np.complex128)) + vec

    for p in keys:
        up = field[p]
        pn = np.sqrt(k_norm2(p))
        for q in keys:
            uq = field[q]
            qn = np.sqrt(k_norm2(q))
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            coeff = 1j * np.dot(np.array(q, dtype=np.float64), up)
            contrib = leray_project(k, coeff * uq)
            if pn >= k_cut and qn >= k_cut:
                ch = "HH"
            elif pn >= k_cut or qn >= k_cut:
                ch = "HL"
            else:
                ch = "LL"
            add(ch, k, contrib)

    m = moments(field)
    Lam = m["Lambda"]
    out = {}
    for ch, Bf in B_chan.items():
        N = 0.0 + 0.0j
        M = 0.0 + 0.0j
        for k, bk in Bf.items():
            kn2 = k_norm2(k)
            if kn2 == 0:
                continue
            uk = field.get(k, np.zeros(3, dtype=np.complex128))
            Tk = -np.dot(bk, np.conjugate(uk))
            N += kn2 * Tk
            M += (kn2 * kn2) * Tk
        N = float(N.real)
        M = float(M.real)
        out[ch] = {"N": N, "M": M, "Tc": M - Lam * N}
    out["cut"] = k_cut
    out["Lambda"] = Lam
    return out


def run(seed: int = 3) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    cases = []

    # Pure high triad: all modes high ⇒ HH dominates by construction if cut below min |k|
    triad = high_triad_field(amp=1.0)
    kns = [np.sqrt(k_norm2(k)) for k in triad]
    cut = 0.5 * min(kns)
    ch = Tc_by_channel(triad, cut)
    r = probe(triad, label="high_triad")
    print(format_probe(r), flush=True)
    print(f"  channels@{cut:.2f}: {ch}", flush=True)
    cases.append({"name": "high_triad", "probe": r.ratio_star, "channels": ch})

    # Two-shell: low + high — HH should feed low via k_high + (-k_high + k_low) etc.
    for ah in [1.0, 5.0, 20.0]:
        f = two_shell_field(amp_low=1.0, amp_high=ah)
        # Need enough modes for HH→L: add conjugate partners already via enforce_reality
        # Add a second high mode so high+high can hit low
        from ns_attacks.stokes_moments import enforce_reality, make_divfree_amp

        f2 = dict(f)
        k_h2 = (8, -3, 2)
        v = make_divfree_amp(k_h2, (0.2, 1.0, -0.3))
        f2[k_h2] = (ah / np.linalg.norm(v)) * v
        f2 = enforce_reality(f2)
        cut = 3.0
        ch = Tc_by_channel(f2, cut)
        r = probe(f2, label=f"two_shell_ah={ah}")
        print(format_probe(r), flush=True)
        print(f"  channels@{cut}: HH={ch['HH']['Tc']:.4e} HL={ch['HL']['Tc']:.4e} LL={ch['LL']['Tc']:.4e}", flush=True)
        cases.append(
            {
                "name": f"two_shell_ah={ah}",
                "ratio_star": r.ratio_star,
                "Tc": r.Tc,
                "HH_Tc": ch["HH"]["Tc"],
                "HL_Tc": ch["HL"]["Tc"],
                "LL_Tc": ch["LL"]["Tc"],
                "HH_frac": abs(ch["HH"]["Tc"])
                / max(abs(ch["HH"]["Tc"]) + abs(ch["HL"]["Tc"]) + abs(ch["LL"]["Tc"]), 1e-30),
            }
        )

    # Random broadband
    hh_fracs = []
    for i in range(40):
        f = random_field(rng, kmax=6, n_modes=16, amp=1.0)
        kns = sorted(np.sqrt(k_norm2(k)) for k in f)
        cut = kns[len(kns) // 2] if kns else 2.0
        ch = Tc_by_channel(f, cut)
        tot = abs(ch["HH"]["Tc"]) + abs(ch["HL"]["Tc"]) + abs(ch["LL"]["Tc"])
        frac = abs(ch["HH"]["Tc"]) / max(tot, 1e-30)
        hh_fracs.append(frac)

    summary = {
        "attack": 3,
        "name": "bony_HH_to_L",
        "cases": cases,
        "random_HH_frac_mean": float(np.mean(hh_fracs)) if hh_fracs else None,
        "random_HH_frac_p90": float(np.percentile(hh_fracs, 90)) if hh_fracs else None,
        "bottleneck_note": (
            "HH channel often carries a large fraction of |Tc|; analytic close of "
            "|Tc|≲||u||_2 X^{3/2} needs HH→L product control beyond Agmon/standard 3D."
        ),
        "verdict": "HH_CHANNEL_LIVE_BOTTLENECK_no_closure",
        "ns_solved": False,
    }
    print("\n=== ATTACK 3 SUMMARY ===", flush=True)
    print(json.dumps({k: v for k, v in summary.items() if k != "cases"}, indent=2), flush=True)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--seed", type=int, default=3)
    args = ap.parse_args()
    summary = run(seed=args.seed)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
