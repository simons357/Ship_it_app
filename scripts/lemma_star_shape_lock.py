#!/usr/bin/env python3
"""Lemma★ shape-form lock — identities only. Does not prove ★.

NS is NOT solved. Lemma★ is OPEN. Kill lane LIVE.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ns_attacks.stokes_moments import (  # noqa: E402
    Ds_double_sum,
    Ds_two_shell,
    Ds_variance_sum,
    dilate_field,
    enforce_reality,
    high_triad_field,
    moments,
    probe,
    scale_field,
    shell_energies,
)


def _two_shell_field():
    field = {
        (1, 0, 0): np.array([0.0, 1.0, 0.2], dtype=np.complex128),
        (2, 1, 0): np.array([0.3, -0.1, 0.5j], dtype=np.complex128),
    }
    return enforce_reality(field)


def _single_shell_field():
    field = {
        (1, 0, 0): np.array([0.0, 1.0, 0.0], dtype=np.complex128),
        (0, 1, 0): np.array([1.0, 0.0, 0.0], dtype=np.complex128),
    }
    return enforce_reality(field)


def prove_Ds_equivalences() -> dict:
    field = _two_shell_field()
    m = moments(field)
    var = Ds_variance_sum(field, m["Lambda"])
    dbl = Ds_double_sum(field)
    shells = shell_energies(field)
    assert len(shells) == 2
    (a, ea), (b, eb) = list(shells.items())
    two = Ds_two_shell(a, b, ea, eb)
    return {
        "moment_vs_variance": bool(abs(m["Ds"] - var) < 1e-12),
        "moment_vs_double": bool(abs(m["Ds"] - dbl) < 1e-12),
        "moment_vs_two_shell": bool(abs(m["Ds"] - two) < 1e-12),
        "nonnegative": bool(m["Ds"] >= -1e-15),
    }


def prove_homogeneity() -> dict:
    field = high_triad_field(amp=1.0)
    p1 = probe(field, "base")
    p2 = probe(scale_field(field, 2.0), "x2")
    p_n = probe(dilate_field(field, 2), "dilate2")
    return {
        "Tc_scales_a3": bool(abs(p2.Tc - (8.0 * p1.Tc)) < 1e-10),
        "Ds_scales_a2": bool(abs(p2.Ds - (4.0 * p1.Ds)) < 1e-10),
        "E_scales_a2": bool(abs(p2.E - (4.0 * p1.E)) < 1e-10),
        "Y_scales_a2": bool(abs(p2.Y - (4.0 * p1.Y)) < 1e-10),
        "Lambda_invariant": bool(abs(p2.Lambda - p1.Lambda) < 1e-12),
        "R_star_scale_invariant": bool(
            abs(p2.ratio_R_star_shape - p1.ratio_R_star_shape) < 1e-10
        ),
        "R_star_dilation_invariant": bool(
            abs(p_n.ratio_R_star_shape - p1.ratio_R_star_shape) < 1e-10
        ),
        "legacy_ratio_star_is_not_invariant": bool(
            abs(p2.ratio_star - p1.ratio_star) > 1e-8
        ),
    }


def prove_single_shell_vacuous() -> dict:
    p = probe(_single_shell_field(), "single")
    return {
        "Ds_zero": bool(abs(p.Ds) <= 1e-14),
        "Tc_plus_zero": bool(max(p.Tc, 0.0) == 0.0),
        "not_a_kill": True,
    }


def prove_all() -> dict:
    return {
        "Ds": prove_Ds_equivalences(),
        "homogeneity": prove_homogeneity(),
        "single_shell": prove_single_shell_vacuous(),
        "lemma_star": "OPEN",
        "ns_solved": False,
        "kill_lane": "LIVE",
        "K_alpha_beta_is_full_lemma": False,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Lemma-star shape-form lock")
    p.add_argument("--out", default=None)
    args = p.parse_args()
    payload = prove_all()
    text = json.dumps(payload, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
