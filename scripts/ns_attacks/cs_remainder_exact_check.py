#!/usr/bin/env python3
"""Check the localized-ABC table against the exact Lemma★ core.

FFT Galerkin is not the core. DA rejected the ABC_λ recon
as a kill. This checker does not stamp Target A.

NS not solved. Lemma★ still open. Not a plate.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.cs_remainder_bump import (  # noqa: E402
    _wave_numbers,
    localized_abc,
    probe_hat,
)
from ns_attacks.ns_lemma_star_core import Field, dilate  # noqa: E402
from ns_attacks.stokes_moments import probe  # noqa: E402

OUT = ROOT / "results" / "cs_remainder_bump"


def hat_to_core(vx, vy, vz, energy_keep: float = 0.9995) -> Field:
    """Export an FFT field, keeping enough modes to hold energy_keep of E."""
    n = vx.shape[0]
    k1d = _wave_numbers(n)
    amp2 = (np.abs(vx) ** 2 + np.abs(vy) ** 2 + np.abs(vz) ** 2).real
    E = float(amp2.sum())
    flat = amp2.ravel()
    order = np.argsort(flat)[::-1]
    kept = 0.0
    take = []
    for idx in order:
        e = float(flat[idx])
        if e <= 0:
            break
        take.append(idx)
        kept += e
        if kept >= energy_keep * E:
            break
    f = Field()
    seen = set()
    for idx in take:
        i, j, l = np.unravel_index(idx, amp2.shape)
        k = (int(k1d[i]), int(k1d[j]), int(k1d[l]))
        if k == (0, 0, 0) or k in seen:
            continue
        w = np.array([vx[i, j, l], vy[i, j, l], vz[i, j, l]], dtype=complex)
        f.set_mode(k, w)
        seen.add(k)
        seen.add((-k[0], -k[1], -k[2]))
    return f.normalize(1.0)


def exact_moments_and_Tc(field: Field) -> dict:
    """Direct triad T_c / moments. One O(m²) pass, only when p+q is in support."""
    keys = list(field.modes.keys())
    vecs = [np.asarray(field.modes[k], dtype=np.complex128) for k in keys]
    lams = np.array([float(k[0] * k[0] + k[1] * k[1] + k[2] * k[2]) for k in keys])
    amps = np.array([float(np.vdot(v, v).real) for v in vecs])
    E = float(amps.sum())
    X = float((lams * amps).sum())
    Y = float((lams * lams * amps).sum())
    Z = float((lams ** 3 * amps).sum())
    Lambda = Y / X if X > 0 else 0.0
    Ds = Z - Lambda * Y
    index = {k: i for i, k in enumerate(keys)}
    # Plain tuples in the inner loop; numpy.dot is too slow at O(m²).
    vr = [(complex(v[0]), complex(v[1]), complex(v[2])) for v in vecs]
    Tc = 0.0
    m = len(keys)
    for i in range(m):
        p0, p1, p2 = keys[i]
        vp0, vp1, vp2 = vr[i]
        for j in range(m):
            q = keys[j]
            t = index.get((p0 + q[0], p1 + q[1], p2 + q[2]))
            if t is None:
                continue
            vq0, vq1, vq2 = vr[j]
            vk0, vk1, vk2 = vr[t]
            qdot = q[0] * vp0 + q[1] * vp1 + q[2] * vp2
            vqvk = vq0 * vk0.conjugate() + vq1 * vk1.conjugate() + vq2 * vk2.conjugate()
            lk = lams[t]
            Tc += lk * (lk - Lambda) * (qdot * vqvk).imag
    R = (Tc ** 2) / (Ds * E * Y) if Ds > 0 and E > 0 and Y > 0 else 0.0
    return {"E": E, "X": X, "Y": Y, "Z": Z, "Lambda": Lambda, "Ds": Ds, "Tc": Tc, "R_signed": R, "n_modes": m}


def check_one(lam: int, n: int, energy_keep: float = 0.99) -> dict:
    vx, vy, vz = localized_abc(n, width=float(lam), k0=lam)
    fft = probe_hat(vx, vy, vz)
    core_f = hat_to_core(vx, vy, vz, energy_keep=energy_keep)
    core = exact_moments_and_Tc(core_f)
    probe_R = None
    if core["n_modes"] <= 400:
        d = {k: np.array(v, copy=True) for k, v in core_f.modes.items()}
        pr = probe(d)
        probe_R = (pr.Tc ** 2) / (pr.Ds * pr.E * pr.Y) if pr.Ds > 0 else 0.0
    return {
        "lambda": lam,
        "n_grid": n,
        "n_modes": core["n_modes"],
        "energy_keep": energy_keep,
        "fft_Y": fft["Y"],
        "core_Y": core["Y"],
        "fft_Ds": fft["Ds"],
        "core_Ds": core["Ds"],
        "fft_Tc": fft["T_c"],
        "core_Tc": core["Tc"],
        "fft_R_signed": fft["R_star_signed"],
        "core_R_signed": core["R_signed"],
        "probe_R_signed": probe_R,
        "fft_cs": fft["cs_ratio"],
        "Tc_rel": abs(fft["T_c"] - core["Tc"]) / max(abs(fft["T_c"]), 1e-30),
        "Ds_rel": abs(fft["Ds"] - core["Ds"]) / max(abs(fft["Ds"]), 1e-30),
        "R_rel": abs(fft["R_star_signed"] - core["R_signed"])
        / max(fft["R_star_signed"], 1e-30),
    }


def dilation_invariance(lam: int = 2, n: int = 32) -> dict:
    vx, vy, vz = localized_abc(n, width=float(lam), k0=lam)
    f = hat_to_core(vx, vy, vz, energy_keep=0.99)
    r1 = exact_moments_and_Tc(f)
    r2 = exact_moments_and_Tc(dilate(f, 2))
    R1 = r1["R_signed"]
    R2 = r2["R_signed"]
    return {
        "R_base": R1,
        "R_dilated": R2,
        "rel": abs(R1 - R2) / max(abs(R1), 1e-30),
        "n_modes": len(f.modes),
    }


def _probe_formula_lock() -> dict:
    """The fast triad sum must match stokes_moments.probe on a tiny field."""
    from ns_attacks.stokes_moments import enforce_reality, make_divfree_amp

    field = {}
    field[(1, 0, 0)] = make_divfree_amp((1, 0, 0), (0.0, 1.0, 0.3))
    field[(0, 1, 0)] = 0.4 * make_divfree_amp((0, 1, 0), (1.0, 0.0, 0.2))
    field[(1, 1, 0)] = 0.25 * make_divfree_amp((1, 1, 0), (0.2, 0.5, 1.0))
    field = enforce_reality(field)
    f = Field()
    seen = set()
    for k, w in field.items():
        if k in seen or k == (0, 0, 0):
            continue
        f.set_mode(k, w)
        seen.add(k)
        seen.add((-k[0], -k[1], -k[2]))
    pr = probe(field)
    ex = exact_moments_and_Tc(f)
    return {
        "probe_Tc": pr.Tc,
        "exact_Tc": ex["Tc"],
        "probe_Ds": pr.Ds,
        "exact_Ds": ex["Ds"],
        "Tc_err": abs(pr.Tc - ex["Tc"]),
        "Ds_err": abs(pr.Ds - ex["Ds"]),
    }


def same_field_fft_vs_exact(lam: int = 2, n: int = 64, energy_keep: float = 0.99) -> dict:
    """Place the truncated field on a large grid; FFT B must match the triad sum."""
    vx, vy, vz = localized_abc(32, width=float(lam), k0=lam)
    f = hat_to_core(vx, vy, vz, energy_keep=energy_keep)
    ex = exact_moments_and_Tc(f)
    hx = np.zeros((n, n, n), dtype=np.complex128)
    hy = np.zeros_like(hx)
    hz = np.zeros_like(hx)
    for k, v in f.modes.items():
        idx = (k[0] % n, k[1] % n, k[2] % n)
        hx[idx] += v[0]
        hy[idx] += v[1]
        hz[idx] += v[2]
    fft = probe_hat(hx, hy, hz)
    return {
        "n_modes": ex["n_modes"],
        "exact_Tc": ex["Tc"],
        "fft_Tc": fft["T_c"],
        "exact_R": ex["R_signed"],
        "fft_R": fft["R_star_signed"],
        "Tc_rel": abs(ex["Tc"] - fft["T_c"]) / max(abs(ex["Tc"]), 1e-30),
        "R_rel": abs(ex["R_signed"] - fft["R_star_signed"]) / max(ex["R_signed"], 1e-30),
    }


def main():
    lock = _probe_formula_lock()
    print("formula_lock", json.dumps(lock), flush=True)
    if lock["Tc_err"] > 1e-8 or lock["Ds_err"] > 1e-8:
        raise RuntimeError(f"exact triad sum disagrees with probe: {lock}")
    rows = []
    for lam, n in ((2, 32), (3, 36), (4, 48)):
        print(f"checking λ={lam} n={n}", flush=True)
        rec = check_one(lam, n)
        rows.append(rec)
        print(json.dumps({k: rec[k] for k in rec}, indent=2), flush=True)
    inv = dilation_invariance()
    print("dilation", json.dumps(inv), flush=True)
    same = same_field_fft_vs_exact()
    print("same_field", json.dumps(same), flush=True)
    Rs = [r["core_R_signed"] for r in rows]
    climb = bool(len(Rs) >= 3 and Rs[-1] > 1.35 * max(Rs[0], 1e-12))
    same_ok = same["R_rel"] < 1e-6 and same["Tc_rel"] < 1e-6
    dil_ok = inv["rel"] < 1e-12
    payload = {
        "ns_solved": False,
        "formula_lock": lock,
        "rows": rows,
        "dilation": inv,
        "same_field": same,
        "same_field_matches": bool(same_ok),
        "dilation_invariant": bool(dil_ok),
        "core_R_climbs": bool(climb),
        "core_R": Rs,
        "verdict": (
            "Exact core confirms the climb. Same truncated field: FFT=triad. "
            "v(n·) leaves R★ invariant. Spatial ABC family still climbs."
            if same_ok and dil_ok and climb
            else "Exact-core check failed. Target A stamp withdrawn."
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "exact_core_check.json").write_text(json.dumps(payload, indent=2))
    print("verdict", payload["verdict"])


if __name__ == "__main__":
    main()
