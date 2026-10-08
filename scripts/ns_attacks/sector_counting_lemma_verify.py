#!/usr/bin/env python3
"""Verify the sector-counting lower bound M_N >= c N log N on square shells.

Implements the explicit injective family from
docs/ns-review/SECTOR-COUNTING-LEMMA-2026-10-08.md.

Not a proof of SND-U / (17) / Clay. Combinatorial kill-test ingredient only.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "results" / "shared_budget"
OUT.mkdir(parents=True, exist_ok=True)


def is_collinear(a: int, b: int, c: int) -> bool:
    for x, y, z in ((a, b, c), (b, a, c), (c, a, b)):
        if (x - y - z) ** 2 == 4 * y * z:
            return True
    return False


def family_shapes(n: int) -> tuple[set[tuple[int, int]], dict]:
    """Return shapes from the explicit injective family at N=n^2."""
    L = max(1, int(math.log2(n)))
    Y0 = L * L + 1
    shapes: set[tuple[int, int]] = set()
    meta = {
        "n": n,
        "N": n * n,
        "L": L,
        "Y0": Y0,
        "collisions": 0,
        "collinear": 0,
        "skipped_pmax": 0,
        "range_empty": Y0 > n // 2,
    }
    if meta["range_empty"]:
        return shapes, meta

    seen_index: dict[tuple[int, int], tuple[int, int, int]] = {}
    for s in range(1, L + 1):
        for y in range(Y0, n // 2 + 1):
            for x in range(1, n // 2 + 1):
                A = x * x + y * y + s * s
                if A > n * n:
                    meta["skipped_pmax"] += 1
                    continue
                B = (n - x) * (n - x) + y * y + s * s
                key = (min(A, B), max(A, B))
                if key in seen_index:
                    meta["collisions"] += 1
                else:
                    seen_index[key] = (x, y, s)
                    if is_collinear(key[0], key[1], n * n):
                        meta["collinear"] += 1
                    shapes.add(key)
    meta["n_shapes"] = len(shapes)
    meta["theoretical_cap"] = L * max(0, n // 2 - Y0 + 1) * (n // 2)
    return shapes, meta


def main() -> None:
    rows = []
    all_ok = True
    # Choose c small enough that the asymptotic (1/8 in log2 units) clears it.
    c_target = 0.02  # against N * ln(N)

    for n in (128, 256, 512, 1024, 2048):
        shapes, meta = family_shapes(n)
        N = meta["N"]
        nlogn = N * math.log(N)
        ratio = meta["n_shapes"] / nlogn if nlogn else 0.0
        ok = (
            not meta["range_empty"]
            and meta["collisions"] == 0
            and meta["collinear"] == 0
            and meta["n_shapes"] >= c_target * nlogn
        )
        all_ok = all_ok and ok
        row = {
            **meta,
            "N_ln_N": nlogn,
            "ratio_shapes_over_N_ln_N": ratio,
            "c_target": c_target,
            "passes_lower_bound": ok,
        }
        rows.append(row)
        print(
            f"n={n} N={N} shapes={meta['n_shapes']} "
            f"col={meta['collisions']} collinear={meta['collinear']} "
            f"ratio={ratio:.4f} ok={ok}",
            flush=True,
        )

    # Spot-check injectivity rebuild at n=128
    n_spot = 128
    _, meta_spot = family_shapes(n_spot)
    N_spot = n_spot * n_spot
    decode_ok = True
    rebuild: dict[tuple[int, int], tuple[int, int, int]] = {}
    for s in range(1, meta_spot["L"] + 1):
        for y in range(meta_spot["Y0"], n_spot // 2 + 1):
            for x in range(1, n_spot // 2 + 1):
                A = x * x + y * y + s * s
                if A > N_spot:
                    continue
                B = (n_spot - x) ** 2 + y * y + s * s
                key = (min(A, B), max(A, B))
                if key in rebuild and rebuild[key] != (x, y, s):
                    decode_ok = False
                rebuild[key] = (x, y, s)

    payload = {
        "status": "PASS" if all_ok and decode_ok else "FAIL",
        "lemma": "M_N >= c N log N for large square shells N=n^2",
        "c_target_against_N_ln_N": c_target,
        "proof_ref": "docs/ns-review/SECTOR-COUNTING-LEMMA-2026-10-08.md",
        "rows": rows,
        "injectivity_spot_n": n_spot,
        "injectivity_spot_ok": decode_ok,
        "not_claimed": ["SND-U", "criterion (17)", "Clay Statement B", "weighted rho kill"],
        "ns_regularity": "open",
    }
    out = OUT / "sector_counting_lemma_verify.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"status": payload["status"], "out": str(out)}, indent=2))
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
