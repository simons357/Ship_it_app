#!/usr/bin/env python3
"""Maximize R★ on N=2,3,4,5 shells while raising |k|_∞.

One B(w,w) per sample on shell α; every output β is scored.
That is the fair test of growing s = #keys on the output shell.

Target A: |T_c| ≤ C √(D_s E Y)  (sup R★ < ∞, independent of |k|_max).
If max R★ climbs with |k|_max or with s, Target A is false.
If it saturates, Target A is not killed by this family.

NS not solved. Not a plate.
"""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.stokes_moments import (  # noqa: E402
    Field,
    ModeKey,
    enforce_reality,
    k_norm2,
    l2_normalize,
    leray_project,
    make_divfree_amp,
    nonlinear_B,
    probe,
    scale_field,
)

OUT = ROOT / "results" / "rstar_shell_climb"


def shells_up_to(kmax: int) -> Dict[int, List[ModeKey]]:
    buckets: Dict[int, List[ModeKey]] = defaultdict(list)
    for i in range(-kmax, kmax + 1):
        for j in range(-kmax, kmax + 1):
            for k in range(-kmax, kmax + 1):
                if (i, j, k) == (0, 0, 0):
                    continue
                buckets[i * i + j * j + k * k].append((i, j, k))
    return dict(buckets)


def pos_half(modes: Sequence[ModeKey]) -> List[ModeKey]:
    out = []
    for i, j, k in modes:
        if i > 0 or (i == 0 and j > 0) or (i == 0 and j == 0 and k > 0):
            out.append((i, j, k))
    return out


def random_shell(modes: Sequence[ModeKey], rng: np.random.Generator) -> Field:
    half = pos_half(modes)
    field: Field = {}
    for k in half:
        seed = rng.normal(size=3)
        v = make_divfree_amp(k, seed)
        n = float(np.linalg.norm(v))
        if n < 1e-15:
            continue
        phase = rng.uniform(0, 2 * np.pi)
        amp = float(rng.uniform(0.25, 1.6))
        field[k] = (amp * np.exp(1j * phase) / n) * v
    field = enforce_reality(field)
    return l2_normalize(field) if field else {}


def rstar_of(field: Field) -> Optional[float]:
    r = probe(field)
    if r.Ds <= 1e-14 or r.E <= 0 or r.Y <= 0:
        return None
    tc = r.Tc
    val = (tc ** 2) / (r.Ds * r.E * r.Y)
    return float(val) if math.isfinite(val) else None


def mix_eps(w: Field, z: Field, eps: float) -> Field:
    out: Field = {k: math.sqrt(max(1.0 - eps * eps, 0.0)) * v for k, v in w.items()}
    for k, v in z.items():
        out[k] = out.get(k, np.zeros(3, dtype=np.complex128)) + eps * v
    return enforce_reality(out)


def field_dump(field: Field) -> dict:
    return {
        str(list(k)): [[float(z.real), float(z.imag)] for z in v] for k, v in field.items()
    }


def bucket_B(Buu: Field) -> Dict[int, Field]:
    buckets: Dict[int, Field] = defaultdict(dict)
    for k, v in Buu.items():
        n = int(k_norm2(k))
        buckets[n][k] = v
    return dict(buckets)


def maximize(kmax_list: Sequence[int], seed: int = 11) -> dict:
    rng = np.random.default_rng(seed)
    rows = []
    k_records = []
    best = {"R": 0.0, "field": None, "meta": None}
    best2_field: Dict[int, Tuple[float, Field, List[int]]] = {}

    def consider(val: Optional[float], field: Field, meta: dict) -> None:
        if val is None:
            return
        rec = {**meta, "R_star": val}
        rows.append(rec)
        if val > best["R"]:
            best["R"] = val
            best["meta"] = rec
            best["field"] = field_dump(field)
        if meta.get("N") == 2:
            km = meta["kmax"]
            prev = best2_field.get(km)
            if prev is None or val > prev[0]:
                best2_field[km] = (
                    val,
                    {k: v.copy() for k, v in field.items()},
                    list(meta.get("shells") or []),
                )

    for kmax in kmax_list:
        shells = shells_up_to(kmax)
        ns = sorted(n for n, m in shells.items() if len(pos_half(m)) >= 1)
        n_trial = 6 if kmax <= 6 else 4
        print(f"kmax={kmax} n_shells={len(ns)} trials/α={n_trial}", flush=True)
        for a in ns:
            for _ in range(n_trial):
                w = random_shell(shells[a], rng)
                if not w:
                    continue
                E = 1.0
                Buu = nonlinear_B(w)
                by = bucket_B(Buu)
                scored = []
                for b, PiB in by.items():
                    if int(b) == int(a):
                        continue
                    n2 = sum(float(np.vdot(v, v).real) for v in PiB.values())
                    if n2 <= 1e-30:
                        continue
                    s = len(PiB)
                    K = (b * n2) / ((a ** 2) * (E ** 2))
                    scored.append((K, int(b), s, n2, PiB))
                    k_records.append(
                        {"kmax": kmax, "alpha": int(a), "beta": int(b), "s": s, "K": float(K)}
                    )
                scored.sort(reverse=True)
                for K, b, s, n2, PiB in scored[:2]:
                    n = math.sqrt(n2)
                    z = enforce_reality({k: v / n for k, v in PiB.items()})
                    for sign in (1.0, -1.0):
                        v = mix_eps(w, scale_field(z, sign), 0.04)
                        consider(
                            rstar_of(v),
                            v,
                            {
                                "N": 2,
                                "kmax": kmax,
                                "shells": [int(a), int(b)],
                                "s": s,
                                "K": float(K),
                                "kind": "aligned",
                                "eps": 0.04,
                            },
                        )

        base = best2_field.get(kmax)
        for N in (3, 4, 5):
            if base is None or len(ns) < N:
                continue
            _R0, f2, sh2 = base
            rest = [n for n in ns if n not in sh2]
            if len(rest) < N - 2:
                continue
            for _ in range(12):
                extra = [int(x) for x in rng.choice(rest, size=N - 2, replace=False)]
                eps_ex = float(rng.uniform(0.05, 0.22))
                parts = [scale_field(f2, math.sqrt(1.0 - eps_ex * eps_ex))]
                wts = rng.dirichlet(np.ones(len(extra)))
                for lam, wt in zip(extra, wts):
                    extra_f = random_shell(shells[int(lam)], rng)
                    parts.append(scale_field(extra_f, eps_ex * math.sqrt(float(wt))))
                v = {}
                for p in parts:
                    for k, vec in p.items():
                        v[k] = v.get(k, np.zeros(3, dtype=np.complex128)) + vec
                v = enforce_reality(v)
                consider(
                    rstar_of(v),
                    v,
                    {
                        "N": N,
                        "kmax": kmax,
                        "shells": sh2 + extra,
                        "kind": "two_plus",
                    },
                )

    table = []
    for kmax in kmax_list:
        for N in (2, 3, 4, 5):
            block = [r for r in rows if r["kmax"] == kmax and r["N"] == N]
            if not block:
                table.append({"N": N, "kmax": kmax, "n": 0, "max_R": None})
                continue
            mx = max(block, key=lambda r: r["R_star"])
            kblock = [r for r in k_records if r["kmax"] == kmax]
            table.append(
                {
                    "N": N,
                    "kmax": kmax,
                    "n": len(block),
                    "max_R": mx["R_star"],
                    "max_K": max((r["K"] for r in kblock), default=None) if N == 2 else None,
                    "max_s": max((r["s"] for r in kblock), default=None) if N == 2 else None,
                    "shells": mx.get("shells"),
                    "kind": mx.get("kind"),
                    "s": mx.get("s"),
                    "K": mx.get("K"),
                }
            )

    by_N = {}
    for N in (2, 3, 4, 5):
        seq = [t for t in table if t["N"] == N and t["max_R"] is not None]
        vals = [t["max_R"] for t in seq]
        climb = bool(len(vals) >= 3 and vals[-1] > 1.35 * max(vals[0], 1e-12) and vals[-1] >= 0.98 * max(vals))
        by_N[str(N)] = {"vals": vals, "climb": climb}

    climbs = any(v["climb"] for v in by_N.values())
    return {
        "ns_solved": False,
        "lemma_star": "OPEN",
        "target_A": "|T_c| <= C sqrt(Ds E Y), i.e. sup R_star < infinity independent of |k|_max",
        "kmax_list": list(kmax_list),
        "table": table,
        "by_N": by_N,
        "climbs": climbs,
        "best": {"R_star": best["R"], "meta": best["meta"]},
        "maximizer_field": best["field"] if climbs else None,
        "verdict": (
            "Target A false on this sample: max R_star climbs with |k|_max."
            if climbs
            else "Target A not killed: max R_star saturates on this sample. Not a proof."
        ),
    }


def main():
    payload = maximize([2, 3, 4, 5, 6, 8], seed=11)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "maximizer.json").write_text(json.dumps(payload, indent=2))
    print("N  kmax   max_R     max_K     s     shells")
    for t in payload["table"]:
        print(
            f"{t['N']}  {t['kmax']:<4}  {(t['max_R'] or float('nan')):8.5f}  "
            f"{(t['max_K'] if t['max_K'] is not None else float('nan')):8.5f}  "
            f"{str(t.get('s')):<5} {t.get('shells')}"
        )
    print("climbs", payload["climbs"])
    print("best", json.dumps(payload["best"], indent=2))


if __name__ == "__main__":
    main()
