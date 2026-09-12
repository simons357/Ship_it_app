#!/usr/bin/env python3
"""Audit the two PR-24 analytic conclusions against the live evaluators.

Does not overwrite stokes_moments.py.
Does not stamp ordinary NS as solved.
Unrestricted Lemma★ is the boxed sup R_star < ∞.
A diverging admissible family is the named kill of that box.
The exact-shell 9D bound is a different statement.

Specialist review of the all-n T_c identity and the weighted
sphere count is still pending. This script records hashes and
finite checks. It is not a proof assistant.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from stokes_moments import (  # noqa: E402
    N_and_M,
    enforce_reality,
    k_norm2,
    probe,
    triad_Im_transfer,
)
from attack9b_exact_shell_K import (  # noqa: E402
    K_of_w,
    build_exact_shell_field,
    random_shell_params,
    shells_up_to,
)

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "ns_lemma_star_core_standalone",
    ROOT / "scripts" / "ns_lemma_star_core.py",
)
_core = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_core)

SEED_R = ((1, 0), (1, 1), (2, 1), (-1, 0), (-1, -1), (-2, -1))
CLAIMED_TABLE = {
    1: {"modes": 18, "N": 0.0, "Tc": 21.0, "R_star": 0.001398359660043},
    2: {"modes": 30, "N": 0.0, "Tc": 1824.0, "R_star": 0.002574888688615},
    3: {"modes": 42, "N": 0.0, "Tc": 26973.0, "R_star": 0.003771825398057},
    4: {"modes": 54, "N": 0.0, "Tc": 187392.0, "R_star": 0.004972851263004},
}
ASYMP = 496125 / 411555776
K_BOUND = 16.0 / 9.0
GROW_S_JSON = ROOT / "results" / "attack9b_grow_s" / "grow_s.json"
SOURCES = (
    ROOT / "docs" / "ATTACK-9D-GROW-S.md",
    ROOT / "docs" / "LEMMA-STAR-REASON.md",
    ROOT / "docs" / "math" / "ns_attacks" / "LEMMA_STAR_CANONICAL.md",
    ROOT / "docs" / "math" / "ns_attacks" / "LEMMA_STAR_EXACT_FORMULAS.md",
    ROOT / "scripts" / "ns_attacks" / "stokes_moments.py",
    ROOT / "scripts" / "ns_lemma_star_core.py",
    GROW_S_JSON,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def growing_layer_field(n: int) -> dict:
    field = {}
    for r1, r2 in SEED_R:
        amp = 0.5j * np.array([-r2, r1, 0.0], dtype=np.complex128)
        for j in range(-n, n + 1):
            field[(n * r1, n * r2, j)] = amp.copy()
    return field


def tc_closed_form(n: int) -> float:
    return 3.0 * (n**5) * (3 * n * n + 3 * n + 1)


def cubic_count(n: int) -> int:
    return sum(
        1
        for a in range(-n, n + 1)
        for b in range(-n, n + 1)
        if abs(a + b) <= n
    )


def check_seed() -> dict:
    field = {}
    for r1, r2 in SEED_R:
        amp = 0.5j * np.array([-r2, r1, 0.0], dtype=np.complex128)
        field[(r1, r2, 0)] = amp
    field = enforce_reality(field)
    Tk = triad_Im_transfer(field)
    shells: dict[float, float] = {}
    for k, t in Tk.items():
        shells[k_norm2(k)] = shells.get(k_norm2(k), 0.0) + t
    N, M, _ = N_and_M(field)
    claimed = {1.0: 0.75, 2.0: -1.0, 5.0: 0.25}
    ok = (
        abs(N) < 1e-12
        and abs(M - 3.0) < 1e-12
        and abs(sum(Tk.values())) < 1e-12
        and all(abs(shells.get(lam, 0.0) - val) < 1e-12 for lam, val in claimed.items())
    )
    cubics = {n: cubic_count(n) for n in range(1, 6)}
    cubic_ok = all(cubics[n] == 3 * n * n + 3 * n + 1 for n in cubics)
    return {
        "shell_T": {str(int(k)): v for k, v in sorted(shells.items())},
        "N": N,
        "M": M,
        "claimed_shell_T": {"1": 0.75, "2": -1.0, "5": 0.25},
        "cubic_counts": cubics,
        "ok": bool(ok and cubic_ok),
    }


def check_family(ns: list[int]) -> dict:
    rows = []
    all_ok = True
    prev = None
    for n in ns:
        raw = growing_layer_field(n)
        field = enforce_reality(raw)
        pr = probe(field, label=f"v_{n}")
        core_r = _core.R_star(_core.from_mode_dict(field))
        claimed = CLAIMED_TABLE.get(n)
        tc_form = tc_closed_form(n)
        row = {
            "n": n,
            "modes": len(field),
            "E": pr.E,
            "N": pr.N,
            "Tc": pr.Tc,
            "Ds": pr.Ds,
            "R_star": pr.ratio_box,
            "core_R_star": core_r["R_star"],
            "tc_closed_form": tc_form,
            "R_over_n": pr.ratio_box / n,
            "elementary_lb": n / 165888.0,
            "E_formula": 4 * (2 * n + 1),
        }
        ok = (
            abs(pr.N) < 1e-8
            and abs(pr.Tc - tc_form) < 1e-6 * max(1.0, abs(tc_form))
            and abs(pr.E - row["E_formula"]) < 1e-9
            and pr.Ds > 0
            and pr.ratio_box > row["elementary_lb"]
            and abs(pr.ratio_box - core_r["R_star"]) < 1e-12
            and (prev is None or pr.ratio_box > prev)
        )
        if claimed:
            ok = ok and row["modes"] == claimed["modes"]
            ok = ok and abs(pr.Tc - claimed["Tc"]) < 1e-6
            ok = ok and abs(pr.ratio_box - claimed["R_star"]) < 1e-12
        row["ok"] = bool(ok)
        all_ok = all_ok and ok
        prev = pr.ratio_box
        rows.append(row)
    return {
        "rows": rows,
        "all_ok": all_ok,
        "asymptotic_R_over_n": ASYMP,
        "last_R_over_n": rows[-1]["R_over_n"] if rows else None,
        "diverges_on_checked_n": bool(all_ok and rows[-1]["R_star"] > rows[0]["R_star"]),
    }


def weighted_count(alpha: int, beta: int, kmax: int, rng: np.random.Generator) -> dict:
    pos = []
    for i in range(-kmax, kmax + 1):
        for j in range(-kmax, kmax + 1):
            for k in range(-kmax, kmax + 1):
                if i * i + j * j + k * k == alpha and (i, j, k) != (0, 0, 0):
                    pos.append((i, j, k))
    if not pos:
        return {"alpha": alpha, "beta": beta, "vacuous": True, "ok": True}
    a = {p: float(rng.uniform(0.1, 1.5)) for p in pos}
    mass2 = sum(x * x for x in a.values())
    c2 = 0.0
    outputs = []
    for i in range(-2 * kmax, 2 * kmax + 1):
        for j in range(-2 * kmax, 2 * kmax + 1):
            for k in range(-2 * kmax, 2 * kmax + 1):
                if i * i + j * j + k * k != beta:
                    continue
                kk = (i, j, k)
                s = 0.0
                for p in pos:
                    q = (kk[0] - p[0], kk[1] - p[1], kk[2] - p[2])
                    if q in a:
                        s += a[p] * a[q]
                c2 += s * s
                if s:
                    outputs.append(kk)
    ratio = c2 / (mass2 * mass2) if mass2 > 0 else 0.0
    return {
        "alpha": alpha,
        "beta": beta,
        "n_input": len(pos),
        "n_output_used": len(outputs),
        "ratio": ratio,
        "bound": 3.0,
        "ok": ratio <= 3.0 + 1e-9,
        "vacuous": False,
    }


def check_exact_shell_K(seed: int = 1390) -> dict:
    rng = np.random.default_rng(seed)
    shells = shells_up_to(8)
    pairs = [(4, 8), (5, 4), (9, 4), (16, 32), (1, 2)]
    rows = []
    max_K = 0.0
    for alpha, beta in pairs:
        modes = shells.get(int(alpha), [])
        if not modes:
            continue
        params = random_shell_params(len(modes), rng)
        w = build_exact_shell_field(modes, params["amps"], params["thetas"], params["phis"])
        rec = K_of_w(w, float(alpha), float(beta))
        rec["ok"] = rec["K"] <= K_BOUND + 1e-12
        max_K = max(max_K, rec["K"])
        rows.append(rec)
    counts = []
    for alpha, beta in ((4, 8), (5, 4), (1, 2)):
        counts.append(weighted_count(alpha, beta, 8, rng))
    return {
        "K_bound": K_BOUND,
        "C": 4.0 / 3.0,
        "max_K_on_samples": max_K,
        "rows": rows,
        "weighted_counts": counts,
        "all_K_under_bound": all(r["ok"] for r in rows),
        "all_counts_under_3": all(c["ok"] for c in counts),
    }


def check_grow_s_record() -> dict:
    data = json.loads(GROW_S_JSON.read_text())
    g = data["growing"]
    return {
        "n_input_fields": g["n_input_fields"],
        "n_occupied_rows": g["n_fields"],
        "max_K": g["max_K"],
        "max_s": g["max_s"],
        "worst": g["worst"],
        "historical_only": True,
        "used_as_C0": False,
    }


def run() -> dict:
    family = check_family([1, 2, 3, 4, 5, 6, 8, 10])
    seed = check_seed()
    shell = check_exact_shell_K()
    grow = check_grow_s_record()
    hashes = {str(p.relative_to(ROOT)): sha256(p) for p in SOURCES if p.exists()}
    return {
        "review": "pr24-closure-review",
        "ns_solved": False,
        "accepted_as_ns_close": False,
        "soft_x": "silent",
        "unrestricted_lemma_star": "KILLED_BY_EXPLICIT_FAMILY",
        "exact_shell_9d_bound": "CLAIMED_C_4_OVER_3",
        "need_star_repairs_unrestricted": False,
        "specialist_review": "pending",
        "proof_assistant": False,
        "seed": seed,
        "family": family,
        "exact_shell": shell,
        "grow_s_historical": grow,
        "source_sha256": hashes,
        "stokes_moments_overwritten": False,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="", help="write JSON audit")
    args = p.parse_args()
    payload = run()
    text = json.dumps(payload, indent=2)
    if args.out:
        out = Path(args.out)
        if not out.is_absolute():
            out = ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n")
        print("wrote", out.relative_to(ROOT))
    print("unrestricted Lemma★:", payload["unrestricted_lemma_star"])
    print("exact-shell 9D:", payload["exact_shell_9d_bound"])
    print("family all_ok:", payload["family"]["all_ok"])
    print("last R_star:", payload["family"]["rows"][-1]["R_star"])
    print("max sample K:", payload["exact_shell"]["max_K_on_samples"])
    print("NS solved:", payload["ns_solved"])
    return 0 if payload["family"]["all_ok"] and payload["seed"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
