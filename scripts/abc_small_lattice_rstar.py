#!/usr/bin/env python3
"""Small-lattice ABC envelope against the locked Lemma★ core.

Paper family (well-posed on T^3):

    ABC_λ(x) = (sin λz + cos λy, sin λx + cos λz, sin λy + cos λx)
    γ̂_λ(k)  = exp(-|k|^2 / (2 λ^2))
    v_λ      = - P(γ_λ ABC_λ) / ||P(γ_λ ABC_λ)||_2

Spatial product = convolution of the six ABC spikes with γ̂.
This script keeps γ̂ on the box |k|_∞ ≤ R (a finite-support field).
That is exact for the truncated envelope, not PR #24's FFT Galerkin bump.

Uses scripts/ns_lemma_star_core.py only:
    R★ = (T_c)_+^2 / (D_s E Y)
    D_s cross-checked on every call.

NS not solved. Lemma★ OPEN. Evaluator, not a kill.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import ns_lemma_star_core as core  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "abc_small_lattice_rstar.json"


def _abc_spikes(k0: int) -> dict[tuple[int, int, int], np.ndarray]:
    """Standard ABC spectrum at frequency k0 (A=B=C=1), before the envelope."""
    spikes: dict[tuple[int, int, int], np.ndarray] = {}

    def add(k, amp, axis: int):
        k = tuple(int(x) for x in k)
        if k == (0, 0, 0):
            return
        w = spikes.get(k, np.zeros(3, dtype=complex))
        w[axis] += amp
        spikes[k] = w

    add((0, 0, k0), 1.0 / (2j), 0)
    add((0, 0, -k0), -1.0 / (2j), 0)
    add((0, k0, 0), 0.5, 0)
    add((0, -k0, 0), 0.5, 0)
    add((k0, 0, 0), 1.0 / (2j), 1)
    add((-k0, 0, 0), -1.0 / (2j), 1)
    add((0, 0, k0), 0.5, 1)
    add((0, 0, -k0), 0.5, 1)
    add((0, k0, 0), 1.0 / (2j), 2)
    add((0, -k0, 0), -1.0 / (2j), 2)
    add((k0, 0, 0), 0.5, 2)
    add((-k0, 0, 0), 0.5, 2)
    return spikes


def _box(R: int):
    for a in range(-R, R + 1):
        for b in range(-R, R + 1):
            for c in range(-R, R + 1):
                yield (a, b, c)


def localized_abc_truncated(lam: int, R: int) -> core.Field:
    """Convolution of ABC_λ with γ̂_λ truncated to |k|_∞ ≤ R, then Leray + unit energy."""
    if lam <= 0 or R < 0:
        raise ValueError("lam >= 1 and R >= 0 required")
    spikes = _abc_spikes(lam)
    acc: dict[tuple[int, int, int], np.ndarray] = {}
    for q in _box(R):
        g = math.exp(-core.lam(q) / (2.0 * lam * lam))
        if g == 0.0:
            continue
        for p, amp in spikes.items():
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            acc[k] = acc.get(k, np.zeros(3, dtype=complex)) + g * amp
    f = core.Field()
    seen = set()
    for k, w in acc.items():
        if k in seen:
            continue
        f.set_mode(k, w)
        seen.add(k)
        seen.add((-k[0], -k[1], -k[2]))
    return f.normalize(1.0)


def hygiene(field: core.Field) -> dict:
    """Divergence-free / reality residuals after set_mode."""
    max_div = 0.0
    max_real = 0.0
    for k, vk in field.modes.items():
        max_div = max(max_div, abs(complex(np.dot(np.array(k, dtype=float), vk))))
        nk = (-k[0], -k[1], -k[2])
        vn = field.modes[nk]
        max_real = max(max_real, float(np.linalg.norm(vn - np.conj(vk))))
    return {
        "n_modes": len(field.modes),
        "max_k_dot_v": max_div,
        "max_reality": max_real,
        "div_free": max_div < 1e-12,
        "real_valued": max_real < 1e-12,
    }


def dilate(field: core.Field, n: int) -> core.Field:
    """Fourier dilation v(n · ): mode k maps to mode n k."""
    if n <= 0:
        raise ValueError("dilation factor must be a positive integer")
    out = core.Field()
    seen = set()
    for k, vk in field.modes.items():
        nk = (n * k[0], n * k[1], n * k[2])
        if nk in seen:
            continue
        out.set_mode(nk, vk)
        seen.add(nk)
        seen.add((-nk[0], -nk[1], -nk[2]))
    return out.normalize(1.0)


def record(field: core.Field) -> dict:
    rec = core.R_star(field, verify=True, tol=1e-9)
    recm = core.R_star(field.scale(-1.0), verify=True, tol=1e-9)
    Ds, E, Y, Tc = rec["D_s"], rec["E"], rec["Y"], rec["T_c"]
    R_signed = (Tc ** 2) / (Ds * E * Y) if Ds > 1e-14 and E > 0 and Y > 0 else 0.0
    return {
        **hygiene(field),
        "E": rec["E"],
        "X": rec["X"],
        "Y": rec["Y"],
        "Z": rec["Z"],
        "Lambda": rec["Lambda"],
        "D_s": rec["D_s"],
        "T_c": rec["T_c"],
        "T_c_reversed": recm["T_c"],
        "R_star": rec["R_star"],
        "R_star_reversed": recm["R_star"],
        "R_signed": R_signed,
        "vacuous_single_shell": rec["vacuous_single_shell"],
        "odd_Tc": abs(recm["T_c"] + rec["T_c"]) < 1e-10 * max(1.0, abs(rec["T_c"])),
    }


def run() -> dict:
    rows = []
    for lam in (1, 2, 3):
        for R in (0, 1, 2):
            f = localized_abc_truncated(lam, R)
            rec = record(f)
            rec["lambda"] = lam
            rec["R_box"] = R
            rec["family"] = "truncated_envelope_ABC"
            rows.append(rec)

    base = localized_abc_truncated(1, 1)
    dil = record(dilate(base, 2))
    dil["lambda"] = 1
    dil["R_box"] = 1
    dil["family"] = "dilate_v(n·)_n=2"
    base_rec = [r for r in rows if r["lambda"] == 1 and r["R_box"] == 1][0]
    dilation = {
        "R_signed_base": base_rec["R_signed"],
        "R_signed_dilated": dil["R_signed"],
        "rel": abs(base_rec["R_signed"] - dil["R_signed"])
        / max(abs(base_rec["R_signed"]), 1e-30),
        "invariant": True,
    }
    dilation["invariant"] = dilation["rel"] < 1e-12

    Rs = [r["R_signed"] for r in rows if r["R_box"] == 2]
    climb = bool(len(Rs) >= 3 and Rs[-1] > 1.35 * max(Rs[0], 1e-30))
    payload = {
        "ns_solved": False,
        "lemma_star": "OPEN",
        "evaluator_not_proof": True,
        "definitions": {
            "D_s": "Z - Y^2/X = sum λ_k (λ_k-Λ)^2 |v_k|^2",
            "T_c": "sum λ_k (λ_k-Λ) T_k, signed triad, never abs",
            "R_star": "(T_c)_+^2 / (D_s E Y)",
            "R_signed": "T_c^2 / (D_s E Y) = R_star(-v) when T_c<0",
        },
        "note": (
            "R=0 is pure ABC (one shell). R≥1 is the paper envelope truncated "
            "to |k|_∞≤R. Not PR #24's FFT table. Finite values only raise C_geom."
        ),
        "rows": rows,
        "dilation": dilation,
        "signed_R_climbs_on_Rbox2": climb,
        "verdict": (
            "Small-lattice envelope is well-posed (div-free, real). "
            "Locked R★ computed. Not a kill of unrestricted Lemma★."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    return payload


def main():
    payload = run()
    print(json.dumps({k: payload[k] for k in payload if k != "rows"}, indent=2))
    for r in payload["rows"]:
        print(
            f"λ={r['lambda']} R={r['R_box']} modes={r['n_modes']} "
            f"Ds={r['D_s']:.4e} Tc={r['T_c']:+.4e} "
            f"R★={r['R_star']:.6f} R_signed={r['R_signed']:.6f} "
            f"vacuous={r['vacuous_single_shell']}"
        )
    print("wrote", OUT)


if __name__ == "__main__":
    main()
