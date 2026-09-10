"""Unit checks for Stokes-moment / Lemma★ probe library."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ns_attacks.stokes_moments import high_triad_field, moments, probe, scale_field


def test_Ds_nonnegative_and_identity():
    f = high_triad_field(amp=1.3)
    m = moments(f)
    assert m["Ds"] >= -1e-10
    expect = m["Z"] - (m["Y"] ** 2) / m["X"]
    assert abs(m["Ds"] - expect) < 1e-9


def test_amplitude_homogeneity_LemmaStar_ratio():
    base = high_triad_field(amp=1.0)
    r1 = probe(base)
    r2 = probe(scale_field(base, 7.0))
    assert math.isfinite(r1.ratio_preyoung)
    assert math.isfinite(r1.ratio_R_star_shape)
    # Post-Young R_post scales as 1/B; pre-Young, C*, and shape★ are invariant
    assert abs(r2.ratio_star / r1.ratio_star - 1.0 / 7.0) < 1e-6
    assert abs(r1.ratio_preyoung - r2.ratio_preyoung) < 1e-9
    assert abs(r1.ratio_cstar - r2.ratio_cstar) < 1e-9
    assert abs(r1.ratio_R_star_shape - r2.ratio_R_star_shape) < 1e-9
    # K=0 ratio scales ~ B
    assert abs(r2.ratio_k0 / r1.ratio_k0 - 7.0) < 1e-6


def test_shape_ratio_matches_definition():
    r = probe(high_triad_field(amp=1.2))
    expect = (r.Tc ** 2) / (r.Ds * r.E * r.Y)
    assert abs(r.ratio_R_star_shape - expect) < 1e-9


def test_pure_single_shell_vacuous():
    """Pure one-mode: Ds=0 and Tc=0 — vacuous, not a kill of ★."""
    from ns_attacks.stokes_moments import enforce_reality, make_divfree_amp

    k = (2, 1, 0)
    f = {k: make_divfree_amp(k, (1.0, 0.0, 0.0))}
    f[k] = f[k] / np.linalg.norm(f[k])
    r = probe(enforce_reality(f))
    assert r.Ds < 1e-12
    assert abs(r.Tc) < 1e-12
    assert not math.isfinite(r.ratio_R_star_shape) or r.Ds <= 1e-30


def test_reality_pairs():
    f = high_triad_field(amp=1.0)
    for k, v in f.items():
        mk = (-k[0], -k[1], -k[2])
        assert mk in f
        assert np.allclose(f[mk], np.conjugate(v))
