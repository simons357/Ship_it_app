"""Unit checks for Stokes-moment / Lemma★ probe library (exact formula lock)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ns_attacks.stokes_moments import (
    Ds_double_sum,
    Ds_two_shell,
    Ds_variance_sum,
    Lambda_prime_from_XY,
    Lambda_prime_rhs,
    Tc_from_triads,
    enforce_reality,
    high_triad_field,
    make_divfree_amp,
    moments,
    probe,
    scale_field,
    shell_energies,
    two_shell_field,
)


def test_Ds_nonnegative_and_equivalent_forms():
    f = high_triad_field(amp=1.3)
    m = moments(f)
    assert m["Ds"] >= -1e-10
    expect = m["Z"] - (m["Y"] ** 2) / m["X"]
    assert abs(m["Ds"] - expect) < 1e-9
    assert abs(m["Ds"] - Ds_variance_sum(f)) < 1e-9
    assert abs(m["Ds"] - Ds_double_sum(f)) < 1e-8


def test_Ds_two_shell_closed_form():
    f = two_shell_field(amp_low=1.2, amp_high=0.7, k_low=(1, 0, 0), k_high=(5, 2, 1))
    shells = shell_energies(f)
    assert len(shells) == 2
    (a, ea), (b, eb) = list(shells.items())
    closed = Ds_two_shell(a, b, ea, eb)
    m = moments(f)
    assert m["Ds"] >= -1e-12
    assert abs(closed - m["Ds"]) < 1e-10


def test_Lambda_prime_sign_convention_identity():
    """Λ' = 2/X (Tc − ν Ds) matches X'=-2νY+2N, Y'=-2νZ+2M on a sample."""
    f = high_triad_field(amp=1.7, phases=(0.1, -0.4, 0.8))
    r = probe(f)
    for nu in (0.0, 0.01, 1.0, 7.5):
        lhs = Lambda_prime_from_XY(r.N, r.M, r.X, r.Y, r.Z, nu)
        rhs = Lambda_prime_rhs(r.Tc, r.Ds, r.X, nu)
        assert math.isfinite(lhs) and math.isfinite(rhs)
        assert abs(lhs - rhs) < 1e-10 * max(1.0, abs(rhs))


def test_R_star_invariant_under_amplitude_scaling():
    """R_★(a v) = R_★(v) for a ≠ 0."""
    base = high_triad_field(amp=1.0)
    r1 = probe(base)
    for a in (0.2, 3.0, 11.0, 1e-2):
        r2 = probe(scale_field(base, a))
        assert math.isfinite(r1.ratio_R_star)
        assert abs(r1.ratio_R_star - r2.ratio_R_star) < 1e-9
        assert abs(r1.ratio_R_star_shape - r2.ratio_R_star_shape) < 1e-9


def test_amplitude_homogeneity_legacy_ratios():
    base = high_triad_field(amp=1.0)
    r1 = probe(base)
    r2 = probe(scale_field(base, 7.0))
    assert abs(r2.ratio_star / r1.ratio_star - 1.0 / 7.0) < 1e-6
    assert abs(r1.ratio_preyoung - r2.ratio_preyoung) < 1e-9
    assert abs(r1.ratio_cstar - r2.ratio_cstar) < 1e-9
    assert abs(r2.ratio_k0 / r1.ratio_k0 - 7.0) < 1e-6


def test_shape_ratio_matches_definition():
    r = probe(high_triad_field(amp=1.2))
    expect = (r.Tc ** 2) / (r.Ds * r.E * r.Y)
    assert abs(r.ratio_R_star_shape - expect) < 1e-9
    assert abs(r.ratio_R_star - expect) < 1e-9


def test_Tc_from_signed_triads_matches_M_minus_Lambda_N():
    f = high_triad_field(amp=1.1, phases=(0.2, 0.5, -0.7))
    r = probe(f)
    tc_tri = Tc_from_triads(f)
    assert abs(tc_tri - r.Tc) < 1e-8 * max(1.0, abs(r.Tc))
    # Signed — flipping global phase of one triad parent changes Im continuously;
    # absolute-value rearrangement would not match M−ΛN.
    assert math.isfinite(tc_tri)


def test_pure_single_shell_vacuous():
    """Pure one-mode: Ds=0 and Tc=0 — vacuous, not a kill of ★."""
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
