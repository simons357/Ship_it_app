#!/usr/bin/env python3
"""Sprint 01 finite-Galerkin certification. Not DA-NS-2. NS is not solved."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.fourier import cube_modes
from ns_attacks.frozen_charge import R_nu1_bound, charge_split
from ns_attacks.galerkin import flux_stats, random_cube
from ns_attacks.icosahedral import finite_difference_check, icosa_geometry, one_shell_field, quadratic_output_modes, rational_shell
from ns_attacks.fourier import nrm2
from ns_attacks.phase_network import network_sum
from ns_attacks.reset_safe import charge_covariance
from ns_attacks.symmetry_2d3c import N_VEC, locked_seed


def _py(x):
    if isinstance(x, dict):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return float(x)
    if isinstance(x, complex):
        return {"re": x.real, "im": x.imag}
    return x


def main() -> int:
    rng = np.random.default_rng(0)
    f1 = random_cube(1, rng)
    rec1 = network_sum(f1, cube_modes(1))
    f2 = random_cube(2, np.random.default_rng(0))
    rec2 = network_sum(f2, cube_modes(2))
    lock = locked_seed()
    rec_lock = network_sum(lock, lock.modes(), planar_n=N_VEC)
    st = flux_stats(f1, cube_modes(1))
    split = charge_split(st, nu=0.3, theta=0.5, kappa_e=math.sqrt(st["Lambda"]))
    n_ok = 0
    for i in range(10000):
        a = 0.5 + rng.random()
        b = a + 0.05 + 0.5 * rng.random()
        radii = a + (b - a) * rng.random(8)
        masses = rng.random(8)
        if R_nu1_bound(radii, masses)["ok"]:
            n_ok += 1
    shell = rational_shell(3, 2)
    K = nrm2(shell[0])
    ico_field = one_shell_field(shell, rng=np.random.default_rng(3))
    taylor = finite_difference_check(ico_field, quadratic_output_modes(shell), K, dt=1e-5, nu=0.0)
    g = icosa_geometry()
    payload = {
        "not_DA_NS_2": True,
        "ns_not_solved": True,
        "radius_one": rec1,
        "radius_two": rec2,
        "locked_seed": rec_lock,
        "frozen_charge_recon_err": split["recon_err"],
        "narrow_band_ok": n_ok,
        "icosa": {
            "sum_zero": g["sum_zero"],
            "radius_ok": g["radius_ok"],
            "isotropic": g["second_moment_isotropic"],
            "leaves_shell": g["pair_sums_leave_shell"],
        },
        "rational_shell_taylor": taylor,
        "two_triad": charge_covariance(),
    }
    out = ROOT / "results" / "sprint01_phase_charge.json"
    out.write_text(json.dumps(_py(payload), indent=2) + "\n")
    print(out)
    print("R=1 signed", rec1["n_signed"], "err", rec1["recon_err"])
    print("R=2 signed", rec2["n_signed"], "err", rec2["recon_err"])
    print("lock err", rec_lock["recon_err"], "align", rec_lock["alignment"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
