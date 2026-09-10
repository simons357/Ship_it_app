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
    # Post-Young R★ scales as 1/B; pre-Young and C* are invariant
    assert abs(r2.ratio_star / r1.ratio_star - 1.0 / 7.0) < 1e-6
    assert abs(r1.ratio_preyoung - r2.ratio_preyoung) < 1e-9
    assert abs(r1.ratio_cstar - r2.ratio_cstar) < 1e-9
    # K=0 ratio scales ~ B
    assert abs(r2.ratio_k0 / r1.ratio_k0 - 7.0) < 1e-6


def test_reality_pairs():
    f = high_triad_field(amp=1.0)
    for k, v in f.items():
        mk = (-k[0], -k[1], -k[2])
        assert mk in f
        assert np.allclose(f[mk], np.conjugate(v))
