#!/usr/bin/env python3
"""Audit the two PR-24 analytic conclusions against the live evaluators.

Does not overwrite stokes_moments.py.
Does not stamp ordinary NS as solved.
Unrestricted Lemma★ is the boxed sup R_star < ∞.
A diverging admissible family is the named kill of that box.
The exact-shell 9D bound is a different statement.

Checks the symbolic growing-layer identity and compares
those calculations with the evaluator. Reads the saved
grow-s sweep summary. Computes the exact three-shear K.
Does not perform the weighted-incidence / shell-count
experiments on the exact-shell page.

Independent specialist review is still pending.
This script is not a proof assistant.
"""

from __future__ import annotations

import argparse
import hashlib
import json
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
from attack9b_exact_shell_K import K_of_w  # noqa: E402

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


def three_shear_field() -> dict:
    """w = (sin y, sin z, sin x) on the normalized torus."""
    field = {
        (0, 1, 0): np.array([1.0 / (2.0j), 0.0, 0.0], dtype=np.complex128),
        (0, 0, 1): np.array([0.0, 1.0 / (2.0j), 0.0], dtype=np.complex128),
        (1, 0, 0): np.array([0.0, 0.0, 1.0 / (2.0j)], dtype=np.complex128),
    }
    return enforce_reality(field)


def k_form(x: float) -> float:
    return 0.75 * (x**2) * (1.0 - x / 4.0)


def check_exact_shell_symbolic() -> dict:
    """Exact three-shear K and the elementary K-form maximum.

    Does not run weighted-incidence / shell-count experiments.
    """
    rec = K_of_w(three_shear_field(), 1.0, 2.0)
    shear_ok = (
        abs(rec["K"] - (2.0 / 3.0)) < 1e-12
        and abs(rec["E_w"] - 1.5) < 1e-12
        and abs(rec["PiB_L2_sq"] - 0.75) < 1e-12
    )
    xs = [i / 64.0 for i in range(1, 4 * 64 + 1)]
    vals = [k_form(x) for x in xs]
    sampled_max = max(vals)
    at_eight_thirds = k_form(8.0 / 3.0)
    form_ok = (
        abs(at_eight_thirds - K_BOUND) < 1e-12
        and sampled_max <= K_BOUND + 1e-12
        and k_form(4.0) <= 1e-12
    )
    return {
        "K_bound": K_BOUND,
        "C": 4.0 / 3.0,
        "conventions": {
            "torus_measure": "normalized",
            "K_requires_alpha_positive_and_w_nonzero": True,
        },
        "three_shear": {
            "field": "w=(sin y, sin z, sin x)",
            "alpha": 1.0,
            "beta": 2.0,
            "K": rec["K"],
            "K_exact": 2.0 / 3.0,
            "E_w": rec["E_w"],
            "PiB_L2_sq": rec["PiB_L2_sq"],
            "ok": bool(shear_ok),
        },
        "k_form": {
            "value_at_8_over_3": at_eight_thirds,
            "sampled_max_on_64ths": sampled_max,
            "ok": bool(form_ok),
        },
        "performs_shell_count_experiments": False,
        "reads_saved_sweep_summary": True,
        "ok": bool(shear_ok and form_ok),
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
    shell = check_exact_shell_symbolic()
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
    print("three-shear K:", payload["exact_shell"]["three_shear"]["K"])
    print("NS solved:", payload["ns_solved"])
    ok = (
        payload["family"]["all_ok"]
        and payload["seed"]["ok"]
        and payload["exact_shell"]["ok"]
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
