#!/usr/bin/env python3
"""Attack 9 — coherent triad packets. Live falsification target. Not a proof.

Heuristic: packets P, Q, R=P+Q, ~m modes each. Coeffs ~ m^{-1/2}.
O(m^2) aligned triads × O(m^{-3/2}) each ⇒ Tc ~ m^{1/2}, R★ ~ m
if incompressibility / phases / conservation do not cancel.

If R★ grows like m, Lemma★ is in trouble. If it stays bounded, a
proof needs the matching square-summation / orthogonality.

Isolated triangles (Attack 8) are not this. Frozen fans are not this.
NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ns_attacks.stokes_moments import (  # noqa: E402
    coherent_packet_field,
    hh_l_fan_field,
    probe,
    two_eigenvalue_closed_triad,
    two_shell_shift_field,
)


def _py(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def _rec(r, **extra) -> dict:
    row = {
        "ratio_box": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
        "Tc": float(r.Tc),
        "Ds": float(r.Ds),
        "E": float(r.E),
        "Y": float(r.Y),
        "Lambda": float(r.Lambda),
        "denom": float(r.Ds * r.E * r.Y) if r.Ds > 0 and r.E > 0 and r.Y > 0 else None,
    }
    row.update(extra)
    return row


def two_key_control() -> dict:
    f = two_shell_shift_field((6, 0, 0), (0, 1, 0))
    r = probe(f)
    return _rec(r, name="two_keys")


def two_shell_live(rng: np.random.Generator, n_phase: int = 12) -> dict:
    """Three keys, two eigenvalues. Can be live."""
    best = None
    for i in range(n_phase):
        if i == 0:
            ph = (0.0, 0.3, -0.2)
            seeds = ((0.0, 1.0, 0.2), (1.0, 0.0, 0.3), (0.2, 0.5, 1.0))
        else:
            ph = tuple(float(x) for x in rng.uniform(0, 2 * np.pi, size=3))
            seeds = tuple(tuple(float(x) for x in rng.normal(size=3)) for _ in range(3))
        r = probe(two_eigenvalue_closed_triad(phases=ph, pol_seeds=seeds))
        rec = _rec(r, name="two_shell_three_keys")
        if best is None or abs(rec["Tc"]) > abs(best["Tc"]):
            best = rec
    return best


def best_coherent_packet(
    m: int,
    rng: np.random.Generator,
    n_try: int = 8,
    p0: Tuple[int, int, int] = (5, 2, 1),
    q0: Tuple[int, int, int] = (-3, 1, 1),
    step: Tuple[int, int, int] = (0, 1, 0),
    family: str = "coherent",
) -> dict:
    best = None
    shifts = (0.0, 0.5 * np.pi, np.pi, -0.5 * np.pi)
    for i in range(n_try):
        seed = (0.2, 1.0, -0.3) if i == 0 else tuple(float(x) for x in rng.normal(size=3))
        for sh in shifts:
            f = coherent_packet_field(
                m,
                p0=p0,
                q0=q0,
                step=step,
                pol_seed=seed,
                phase_r_shift=float(sh),
                random_phases=False,
                random_pol=False,
            )
            r = probe(f, label=f"pkt_{m}")
            rec = _rec(r, m=m, family=family, p0=list(p0), q0=list(q0))
            if rec["ratio_box"] is None:
                continue
            if best is None or rec["ratio_box"] > best["ratio_box"]:
                best = rec
    return best


def random_packet(m: int, rng: np.random.Generator) -> dict:
    f = coherent_packet_field(
        m, random_phases=True, random_pol=True, rng=rng, phase_r_shift=0.0
    )
    r = probe(f, label=f"rand_{m}")
    return _rec(r, m=m, family="random")


def best_fan(n_pairs: int, rng: np.random.Generator, n_try: int = 8) -> dict:
    best = None
    for _ in range(n_try):
        f = hh_l_fan_field(n_pairs, rng=rng, randomize=True)
        r = probe(f, label=f"fan_{n_pairs}")
        rec = _rec(r, n_pairs=n_pairs, family="fan")
        if rec["ratio_box"] is None:
            continue
        if best is None or rec["ratio_box"] > best["ratio_box"]:
            best = rec
    return best


def log_exponents(rows: List[dict], xkey: str, ykey: str = "ratio_box") -> List[dict]:
    usable = [r for r in rows if r and r.get(ykey) and r[ykey] > 0 and r.get(xkey, 0) > 0]
    usable = sorted(usable, key=lambda r: r[xkey])
    out = []
    for a, b in zip(usable, usable[1:]):
        lx = math.log(b[xkey] / a[xkey])
        ly = math.log(b[ykey] / a[ykey])
        out.append(
            {
                "from": a[xkey],
                "to": b[xkey],
                "exponent": float(ly / lx) if abs(lx) > 1e-12 else None,
                "R_from": a[ykey],
                "R_to": b[ykey],
            }
        )
    return out


def run(seed: int = 9, n_try: int = 8) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    two_keys = two_key_control()
    two_shells = two_shell_live(rng, n_phase=12)
    print(
        f"two keys:     Tc={two_keys['Tc']:.3e}  R★={two_keys['ratio_box']}",
        flush=True,
    )
    print(
        f"two shells:   Tc={two_shells['Tc']:.3e}  R★={two_shells['ratio_box']}",
        flush=True,
    )

    ms = (2, 3, 4, 6, 8, 12, 16)
    coherent = []
    random_rows = []
    for m in ms:
        c = best_coherent_packet(m, rng, n_try=n_try)
        rnd = random_packet(m, rng)
        if c:
            coherent.append(c)
            print(
                f"packet m={m:2d} coherent R★={c['ratio_box']:.4e}  "
                f"Tc={c['Tc']:.3e} Ds={c['Ds']:.3e} Y={c['Y']:.3e}",
                flush=True,
            )
        if rnd:
            random_rows.append(rnd)
            print(
                f"packet m={m:2d} random    R★={rnd['ratio_box']}  Tc={rnd['Tc']:.3e}",
                flush=True,
            )

    narrow = []
    for m in (2, 4, 6, 8, 12, 16, 20, 24):
        n_here = n_try if m <= 12 else max(4, n_try // 2)
        c = best_coherent_packet(
            m,
            rng,
            n_try=n_here,
            p0=(32, 2, 1),
            q0=(-24, 1, 1),
            family="narrow",
        )
        if c:
            narrow.append(c)
            print(
                f"narrow m={m:2d} R★={c['ratio_box']:.4e}  "
                f"Tc={c['Tc']:.3e} Ds={c['Ds']:.3e} Y={c['Y']:.3e}",
                flush=True,
            )

    fans = []
    for n in (2, 4, 8, 12, 16):
        row = best_fan(n, rng, n_try=n_try)
        if row:
            fans.append(row)
            print(
                f"fan N={n:2d}  R★={row['ratio_box']}  Tc={row['Tc']:.3e}",
                flush=True,
            )

    coh_exp = log_exponents(coherent, "m")
    narrow_exp = log_exponents(narrow, "m")
    fan_exp = log_exponents(fans, "n_pairs")

    rmax = 0.0
    for block in (coherent, random_rows, fans, [two_shells], narrow):
        for row in block:
            val = row.get("ratio_box")
            if val:
                rmax = max(rmax, val)

    def _grows(rows: list) -> bool:
        if len(rows) < 3 or not rows[0].get("ratio_box") or not rows[-1].get("ratio_box"):
            return False
        ratio = rows[-1]["ratio_box"] / rows[0]["ratio_box"]
        mratio = rows[-1]["m"] / rows[0]["m"]
        return bool(ratio > 0.5 * mratio and rows[-1]["ratio_box"] > 2 * rows[0]["ratio_box"])

    grows = _grows(coherent) or _grows(narrow)
    # Finite-m growth is not a kill. A kill is R★ → ∞, not a peak of 0.2.
    killed = bool(rmax > 1e3)

    return _py(
        {
            "attack": 9,
            "name": "coherent_triad_packets",
            "ns_solved": False,
            "LemmaStar_killed": bool(killed),
            "two_keys": two_keys,
            "two_shell_three_keys": two_shells,
            "coherent_packets": coherent,
            "narrow_packets": narrow,
            "random_packets": random_rows,
            "hh_l_fans": fans,
            "coherent_exponents_in_m": coh_exp,
            "narrow_exponents_in_m": narrow_exp,
            "fan_exponents": fan_exp,
            "Rbox_max": rmax,
            "heuristic_grows_with_m": bool(grows),
            "verdict": "KILL_LemmaStar" if killed else "PACKET_OPEN_bound_open",
            "note": (
                "Live target is a growing coherent packet or HH→L fan. "
                "Isolated triangles are not this. Samples are evidence only. "
                "NS not solved."
            ),
        }
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--n-try", type=int, default=8)
    args = ap.parse_args()
    summary = run(n_try=args.n_try)
    print("\n=== ATTACK 9 SUMMARY ===", flush=True)
    slim = {
        k: v
        for k, v in summary.items()
        if k not in ("coherent_packets", "random_packets", "hh_l_fans", "narrow_packets")
    }
    print(json.dumps(slim, indent=2), flush=True)
    if args.out:
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()
