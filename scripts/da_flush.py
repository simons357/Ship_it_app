#!/usr/bin/env python3
"""
Flush which of the 16 are live, using Hilbert / Born weights on combinations.

This is quantum *math* on the reconstructed score, not a quantum computer
and not the shelved Quantum Lens. 2^15 is small; every subset is classical.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_fingers import CANDIDATE_META, SIXTEEN  # noqa: E402
from unifier_combo import INPUTS, lock_score, r_batch, sample_matrix  # noqa: E402


KMAX = 4
N_DRAW = 200


def run(n: int = N_DRAW, seed: int = 1, out: Path | None = None) -> dict:
    rng = np.random.default_rng(seed)
    base = sample_matrix(n, rng)
    baseline = float(np.mean(r_batch(base)))

    knobs = [name for name in SIXTEEN if name != "R" and name in INPUTS]
    deltas = {name: max(lock_score(base, (name,)) - baseline, 0.0) for name in knobs}
    # leftover reconstructed slots with no lock (theta_qcd): amplitude 0
    for name in SIXTEEN:
        if name not in deltas and name != "R":
            deltas[name] = 0.0

    names = [name for name in SIXTEEN if name != "R"]
    amp = np.array([np.sqrt(deltas[name]) for name in names], dtype=float)
    norm = float(np.linalg.norm(amp))
    if norm == 0.0:
        psi = np.zeros_like(amp)
    else:
        psi = amp / norm
    born = psi ** 2

    by_type: dict[str, float] = {}
    for name, p in zip(names, born):
        cat = CANDIDATE_META[name][0]
        by_type[cat] = by_type.get(cat, 0.0) + float(p)

    marked = [name for name, d in deltas.items() if d > 0.02]
    n_marked = len(marked)
    n_dim = len(names)
    grover_iters = float(0.25 * np.pi * np.sqrt(n_dim / max(n_marked, 1)))

    combo_top = []
    for k in range(1, KMAX + 1):
        best = None
        best_mass = -1.0
        idx = {name: i for i, name in enumerate(names)}
        for subset in itertools.combinations(names, k):
            mass = float(sum(born[idx[name]] for name in subset))
            if mass > best_mass:
                best_mass = mass
                best = list(subset)
        combo_top.append({"k": k, "set": best, "born_mass": best_mass})

    payload = {
        "meta": {
            "method": "Hilbert flush: amplitude = sqrt(max(Δ lock_R, 0)), Born = |a|²",
            "not_quantum_lens": True,
            "not_a_unifier": True,
            "n": n,
            "seed": seed,
        },
        "state": {
            "names": names,
            "delta_lock_R": deltas,
            "born": {name: float(p) for name, p in zip(names, born)},
            "born_by_type": by_type,
        },
        "marked_score_movers": marked,
        "grover_oracle_size": {
            "N": n_dim,
            "M": n_marked,
            "approx_iterations": grover_iters,
            "note": "Illustration only. 2^15 subsets are cheaper classically.",
        },
        "best_combination_by_born_mass": combo_top,
        "flushed": marked,
        "how_far": [
            "every singleton and every k≤4 subset was scored (classical)",
            f"Born mass sits on {marked}",
            "same four the lock-R singleton test already found",
            "category mass is gravity-gauge then teleological then harmonic",
            "this is a rewrite of the score, not a new producing-map",
        ],
        "next_da_move": (
            "Replace deltas with Cosmo type-tags or a real F-residual. "
            "Do not stand up a quantum device for 15 knobs."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_flush.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA Hilbert flush. Not Quantum Lens. Not a quantum computer.")
    born = payload["state"]["born"]
    ranked = sorted(born.items(), key=lambda kv: kv[1], reverse=True)
    print("Born weights:")
    for name, p in ranked:
        print(f"  {name:<18} {p:6.3f}")
    print("by type:", json.dumps(payload["state"]["born_by_type"], indent=2))
    print("flushed (score-movers):", payload["flushed"])
    for row in payload["best_combination_by_born_mass"]:
        print(f"k={row['k']}  mass={row['born_mass']:.3f}  {row['set']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
