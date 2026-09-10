#!/usr/bin/env python3
"""
Family check against the locked Lemma★ shape form.

Not a proof. Not a kill. No new SuperGrok family was sent.
Runs the announced checks on the locked two-shell closer.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ns_attacks.ns_lemma_star_core import (  # noqa: E402
    D_s_direct_form,
    D_s_moment_form,
    Field,
    R_star,
    build_closing_direction,
    dilate,
    moments,
    random_shell_field,
)
from track_b_lemmas import rec  # noqa: E402


def _divfree_reality(field: Field, tol: float = 1e-10) -> dict:
    max_div = 0.0
    max_real = 0.0
    missing = 0
    for k, vk in field.modes.items():
        max_div = max(max_div, abs(complex(np.dot(np.array(k, dtype=float), vk))))
        nk = tuple(-x for x in k)
        if nk not in field.modes:
            missing += 1
            continue
        max_real = max(
            max_real, float(np.linalg.norm(field.modes[nk] - np.conj(vk)))
        )
    return {
        "n_modes": len(field.modes),
        "max_kdot_v": max_div,
        "max_reality_err": max_real,
        "missing_conjugates": missing,
        "ok": max_div <= tol and max_real <= tol and missing == 0,
    }


def _two_shell(alpha: int, beta: int, seed: int, eps: float) -> Field:
    rng = np.random.default_rng(seed)
    w = random_shell_field(alpha, rng, target_E=1.0)
    z, raw = build_closing_direction(w, beta)
    if z is None or raw <= 0.0:
        raise RuntimeError(f"no closer on shells ({alpha},{beta})")
    return w.add(z.scale(eps))


def _row(alpha: int, beta: int, seed: int) -> dict:
    v = _two_shell(alpha, beta, seed, eps=0.15)
    setup = _divfree_reality(v)
    r = R_star(v)
    E, X, Y, Z, Lam = moments(v)
    ds_m = D_s_moment_form(X, Y, Z)
    ds_d = D_s_direct_form(v, Lam)
    amp = R_star(v.scale(3.0))
    dil2 = R_star(dilate(v, 2))
    dil3 = R_star(dilate(v, 3))
    rev = R_star(v.scale(-1.0))
    return {
        "alpha": alpha,
        "beta": beta,
        "seed": seed,
        "setup": setup,
        "Ds_moment": ds_m,
        "Ds_direct": ds_d,
        "Ds_match": abs(ds_m - ds_d) <= 1e-9 * max(abs(ds_m), abs(ds_d), 1.0),
        "T_c": r["T_c"],
        "R_star": r["R_star"],
        "R_star_unsigned": float((r["T_c"] ** 2) / (r["D_s"] * r["E"] * r["Y"])),
        "R_star_amp": amp["R_star"],
        "R_star_dilate_2": dil2["R_star"],
        "R_star_dilate_3": dil3["R_star"],
        "T_c_reverse": rev["T_c"],
        "R_star_reverse": rev["R_star"],
        "amp_flat": abs(r["R_star"] - amp["R_star"]) <= 1e-8,
        "dilate_flat": (
            abs(r["R_star"] - dil2["R_star"]) <= 1e-8
            and abs(r["R_star"] - dil3["R_star"]) <= 1e-8
        ),
        "Tc_odd": abs(rev["T_c"] + r["T_c"]) <= 1e-8,
    }


def sweep(seed: int = 7) -> dict:
    rows = [_row(1, 2, seed), _row(4, 8, seed + 1)]
    return {
        "meta": {
            "slot": "B",
            "write": "Lemma★ family check against the lock",
            "tuning_the_pde": False,
            "lemma_star_open": True,
            "h1_started": False,
            "new_family_arrived": False,
            "kill": False,
        },
        "families": rows,
    }


def lemmas(payload: dict) -> list[dict]:
    rows = payload["families"]
    setup_ok = all(r["setup"]["ok"] and r["Ds_match"] for r in rows)
    dilate_ok = all(r["dilate_flat"] and r["amp_flat"] and r["Tc_odd"] for r in rows)
    finite = all(np.isfinite(r["R_star"]) and r["R_star"] < 10.0 for r in rows)
    return [
        rec(
            "LSfam_lock_first",
            "check locked Ds, Tc, R★ before a kill stamp",
            "pass",
            "Desk rule. Identities, not a reconstructed claim.",
        ),
        rec(
            "LSfam_div_real",
            "div-free and v_{-k}=conj(v_k) on the locked families",
            "pass" if setup_ok else "fail",
            "Setup of the boxed claim. Not well-posedness of NSE.",
            families=[{"a": r["alpha"], "b": r["beta"], "ok": r["setup"]["ok"]} for r in rows],
        ),
        rec(
            "LSfam_dilation_flat",
            "R★(av)=R★(v(n·))=R★(v); Tc odd",
            "pass" if dilate_ok else "fail",
            "Fourier dilation is not a kill lane. Already on disk.",
        ),
        rec(
            "LSfam_wellposed_kills",
            "well-posed on paper kills the unrestricted lemma",
            "fail",
            "Admissible ≠ Hadamard ≠ sup R★ < ∞.",
        ),
        rec(
            "LSfam_small_lattice_kills",
            "finite R★ on small n kills ★",
            "fail" if finite else "open",
            "Kill is R★(v_n)→∞. A finite climb raises C_geom.",
            R_star=[r["R_star"] for r in rows],
        ),
        rec(
            "LSfam_unrestricted_killed",
            "unrestricted Lemma★ is killed",
            "fail",
            "No new family. Locked samples stay finite. ★ OPEN.",
        ),
    ]


def run(seed: int = 7, out: Path | None = None) -> dict:
    payload = sweep(seed=seed)
    rows = lemmas(payload)
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in rows:
        counts[row["verdict"]] += 1
    payload["lemmas"] = rows
    payload["counts"] = counts
    payload["domain_verdict"] = "open"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    payload = run(seed=args.seed, out=args.out)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
