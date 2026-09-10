"""Unit checks for Stokes-moment / Lemma★ probe library (exact formula lock)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ns_attacks.stokes_moments import (
    Ds_double_sum,
    Ds_operator_norm,
    Ds_two_shell,
    Ds_variance_sum,
    Lambda_prime_from_XY,
    Lambda_prime_rhs,
    Tc_from_B_field,
    Tc_from_operator_inner,
    Tc_from_triads,
    dilate_field,
    enforce_reality,
    high_triad_field,
    make_divfree_amp,
    moments,
    nonlinear_B,
    nonlinear_B_fft_dealiased,
    probe,
    scale_field,
    shell_energies,
    sum_Tk,
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
    assert abs(m["Ds"] - Ds_operator_norm(f)) < 1e-9


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


def test_Tc_equals_operator_inner_product():
    """Tc = −⟨B, A(A−Λ)v⟩ matches triad / M−ΛN forms."""
    f = high_triad_field(amp=1.4, phases=(0.2, -0.5, 0.7))
    r = probe(f)
    inner = Tc_from_operator_inner(f)
    tri = Tc_from_triads(f)
    assert abs(inner - r.Tc) < 1e-8 * max(1.0, abs(r.Tc))
    assert abs(inner - tri) < 1e-8 * max(1.0, abs(tri))


def test_Tc_odd_Ds_E_Y_even_under_reversal():
    """Tc(-v)=-Tc(v); Ds,E,Y even. Universal (Tc_+)^2 bound ≡ Tc^2 bound."""
    f = high_triad_field(amp=1.1, phases=(0.3, -0.2, 0.6))
    r = probe(f)
    rm = probe(scale_field(f, -1.0))
    assert abs(rm.Tc + r.Tc) < 1e-8 * max(1.0, abs(r.Tc))
    assert abs(rm.Ds - r.Ds) < 1e-8 * max(1.0, abs(r.Ds))
    assert abs(rm.E - r.E) < 1e-12
    assert abs(rm.Y - r.Y) < 1e-8 * max(1.0, abs(r.Y))
    # (Tc_+)^2(v) and (Tc_+)^2(-v) cover Tc(v)^2 between them
    pos = max(r.Tc, 0.0) ** 2
    pos_m = max(rm.Tc, 0.0) ** 2
    assert abs(max(pos, pos_m) - r.Tc ** 2) < 1e-8 * max(1.0, r.Tc ** 2)


def test_false_u2_X32_product_fails_as_a_to_zero():
    """|Tc| <= C ||u||_2 X^{3/2} cannot hold uniformly: ratio ~ 1/a as a→0."""
    f = high_triad_field(amp=1.0)
    r = probe(f)
    assert abs(r.Tc) > 1e-8
    ratios = []
    for a in (1.0, 0.1, 0.01, 1e-3):
        ra = probe(scale_field(f, a))
        denom = math.sqrt(ra.E) * (ra.X ** 1.5)
        ratios.append(abs(ra.Tc) / denom)
    assert ratios[-1] / ratios[0] > 50.0


def test_single_shell_Ds_zero_implies_Tc_zero():
    """Ds=0 ⇒ one shell and Tc=0. Not a kill."""
    from ns_attacks.attack9b_exact_shell_K import (
        build_exact_shell_field,
        normalize_field,
        shells_up_to,
    )

    modes = shells_up_to(4)[5]
    rng = np.random.default_rng(1390)
    n = len(modes)
    w = normalize_field(
        build_exact_shell_field(
            modes,
            rng.uniform(0.4, 1.2, size=n),
            rng.uniform(0, 2 * np.pi, size=n),
            rng.uniform(0, 2 * np.pi, size=n),
        )
    )
    r = probe(w)
    assert abs(r.Ds) < 1e-10
    assert abs(r.Tc) < 1e-10
    assert abs(Tc_from_operator_inner(w)) < 1e-10


def test_R_star_invariant_under_amplitude_scaling():
    """R_★(a v) = R_★(v) for a ≠ 0."""
    base = high_triad_field(amp=1.0)
    r1 = probe(base)
    for a in (0.2, 3.0, 11.0, 1e-2):
        r2 = probe(scale_field(base, a))
        assert math.isfinite(r1.ratio_R_star)
        assert abs(r1.ratio_R_star - r2.ratio_R_star) < 1e-9
        assert abs(r1.ratio_R_star_shape - r2.ratio_R_star_shape) < 1e-9


def test_R_star_invariant_under_uniform_Fourier_dilation():
    """R_★(v(n·)) = R_★(v) — exact; amplitude/frequency do NOT shrink R_★."""
    base = high_triad_field(amp=1.0)
    r1 = probe(base)
    for n in (2, 3):
        r2 = probe(dilate_field(base, n))
        assert math.isfinite(r1.ratio_R_star)
        assert abs(r1.ratio_R_star - r2.ratio_R_star) < 1e-8


def test_amplitude_homogeneity_legacy_ratios():
    base = high_triad_field(amp=1.0)
    r1 = probe(base)
    r2 = probe(scale_field(base, 7.0))
    assert abs(r2.ratio_star / r1.ratio_star - 1.0 / 7.0) < 1e-6
    assert abs(r1.ratio_preyoung - r2.ratio_preyoung) < 1e-9
    assert abs(r1.ratio_cstar - r2.ratio_cstar) < 1e-9
    assert abs(r2.ratio_k0 / r1.ratio_k0 - 7.0) < 1e-6


def test_shape_ratio_matches_Tc_plus_definition():
    """R_★ = (Tc)_+^2 / (Ds E Y); when Tc≥0 this equals Tc^2/(Ds E Y)."""
    r = probe(high_triad_field(amp=1.2))
    Tc_plus = max(r.Tc, 0.0)
    expect = (Tc_plus ** 2) / (r.Ds * r.E * r.Y)
    assert abs(r.ratio_R_star_shape - expect) < 1e-9
    assert abs(r.ratio_R_star - expect) < 1e-9
    assert abs(r.Tc_plus - Tc_plus) < 1e-15
    if r.Tc >= 0:
        assert abs(r.ratio_R_star - (r.Tc ** 2) / (r.Ds * r.E * r.Y)) < 1e-9


def test_Tc_from_signed_triads_matches_M_minus_Lambda_N():
    f = high_triad_field(amp=1.1, phases=(0.2, 0.5, -0.7))
    r = probe(f)
    tc_tri = Tc_from_triads(f)
    assert abs(tc_tri - r.Tc) < 1e-8 * max(1.0, abs(r.Tc))
    assert math.isfinite(tc_tri)


def test_sum_Tk_vanishes():
    f = high_triad_field(amp=1.4, phases=(0.3, -0.2, 0.7))
    assert abs(sum_Tk(f)) < 1e-10


def test_triad_agrees_with_dealiased_FFT_Tc():
    f = high_triad_field(amp=1.0, phases=(0.1, 0.4, -0.5))
    Buu = nonlinear_B(f)
    Buu_fft = nonlinear_B_fft_dealiased(f)
    tc_tri = Tc_from_triads(f)
    tc_fft = Tc_from_B_field(f, Buu_fft)
    tc_B = Tc_from_B_field(f, Buu)
    assert abs(tc_tri - tc_B) < 1e-8 * max(1.0, abs(tc_tri))
    assert abs(tc_tri - tc_fft) < 1e-6 * max(1.0, abs(tc_tri))


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


def test_attack9_controls_on_small_packet():
    """Attack 9 required controls on m=1 packet."""
    from ns_attacks.attack9_packet_fan import field_from_params, random_packet_params

    rng = np.random.default_rng(42)
    params = random_packet_params(1, rng)
    f = field_from_params(1, params)
    r0 = probe(f)
    assert math.isfinite(r0.ratio_R_star) or r0.Ds < 1e-30
    if math.isfinite(r0.ratio_R_star):
        for a in (0.5, 4.0):
            assert abs(probe(scale_field(f, a)).ratio_R_star - r0.ratio_R_star) < 1e-8
        for n in (2, 3):
            assert abs(probe(dilate_field(f, n)).ratio_R_star - r0.ratio_R_star) < 1e-7
    assert abs(sum_Tk(f)) < 1e-9
    tc_tri = Tc_from_triads(f)
    tc_fft = Tc_from_B_field(f, nonlinear_B_fft_dealiased(f))
    assert abs(tc_tri - tc_fft) < 1e-6 * max(1.0, abs(tc_tri))


def test_attack9b_exact_shell_K_eps_limit_and_controls():
    """9B: exact-shell Ds≈0; K amp-invariant; R_★(w+εz)→K as ε→0."""
    from ns_attacks.attack9b_exact_shell_K import (
        K_of_w,
        build_exact_shell_field,
        closing_packet_from_PiB,
        combine_eps,
        choose_closing_sign,
        eps_limit_check,
        normalize_field,
        project_B_to_shell,
        shells_up_to,
    )

    shells = shells_up_to(5)
    modes = shells[5][:6]
    assert len(modes) >= 2
    rng = np.random.default_rng(1390)
    amps = rng.uniform(0.4, 1.2, size=len(modes))
    thetas = rng.uniform(0, 2 * np.pi, size=len(modes))
    phis = rng.uniform(0, 2 * np.pi, size=len(modes))
    w = normalize_field(build_exact_shell_field(modes, amps, thetas, phis))
    m = moments(w)
    assert abs(m["Ds"]) < 1e-10
    alpha, beta = 5.0, 10.0
    info = K_of_w(w, alpha, beta)
    assert math.isfinite(info["K"])
    for a in (0.3, 5.0):
        assert abs(K_of_w(scale_field(w, a), alpha, beta)["K"] - info["K"]) < 1e-9
    if info["PiB_L2"] > 1e-12:
        chk = eps_limit_check(w, alpha, beta, eps_list=(1e-2, 1e-3))
        assert chk["limit_ok"]
        assert chk["rel_err_at_smallest_eps"] < 0.15
        Buu = nonlinear_B(w)
        PiB = project_B_to_shell(Buu, beta)
        z = closing_packet_from_PiB(PiB, sign=choose_closing_sign(w, PiB))
        r = probe(combine_eps(w, z, 1e-3))
        assert math.isfinite(r.ratio_R_star)
        assert abs(r.ratio_R_star - info["K"]) / max(info["K"], 1e-30) < 0.15


def _field_inner(a, b) -> float:
    keys = set(a) | set(b)
    s = 0.0
    zero = np.zeros(3, dtype=np.complex128)
    for k in keys:
        s += float(np.vdot(a.get(k, zero), b.get(k, zero)).real)
    return s


def test_near_shell_limit_needs_aligned_sign_selected_zbeta():
    """lim R_★(w+ε z_β)=K only for aligned, stretch-oriented z_β ∥ Π_β B.

    Arbitrary z_β: the limit tracks the squared projection against B(w,w).
    The compressing sign makes (Tc)_+=0, so R_★→0, not K.
    """
    from ns_attacks.attack9b_exact_shell_K import (
        K_of_w,
        build_exact_shell_field,
        closing_packet_from_PiB,
        combine_eps,
        choose_closing_sign,
        field_l2,
        normalize_field,
        project_B_to_shell,
        shells_up_to,
    )

    shells = shells_up_to(5)
    modes_a, modes_b = shells[5], shells[10]
    rng = np.random.default_rng(1390)
    w = normalize_field(
        build_exact_shell_field(
            modes_a,
            rng.uniform(0.4, 1.2, size=len(modes_a)),
            rng.uniform(0, 2 * np.pi, size=len(modes_a)),
            rng.uniform(0, 2 * np.pi, size=len(modes_a)),
        )
    )
    alpha, beta = 5.0, 10.0
    info = K_of_w(w, alpha, beta)
    assert info["PiB_L2"] > 1e-8
    PiB = project_B_to_shell(nonlinear_B(w), beta)
    stretch = choose_closing_sign(w, PiB)
    z_align = closing_packet_from_PiB(PiB, sign=stretch)
    z_compress = closing_packet_from_PiB(PiB, sign=-stretch)
    r_align = probe(combine_eps(w, z_align, 1e-3))
    r_comp = probe(combine_eps(w, z_compress, 1e-3))
    assert abs(r_align.ratio_R_star - info["K"]) / info["K"] < 0.15
    assert r_comp.Tc < 0
    assert r_comp.ratio_R_star == 0.0 or r_comp.ratio_R_star < 1e-12

    z_rand = normalize_field(
        build_exact_shell_field(
            modes_b,
            rng.uniform(0.3, 1.5, size=len(modes_b)),
            rng.uniform(0, 2 * np.pi, size=len(modes_b)),
            rng.uniform(0, 2 * np.pi, size=len(modes_b)),
        )
    )
    n_pib = field_l2(PiB)
    cos2 = (_field_inner(z_rand, PiB) / max(n_pib, 1e-30)) ** 2
    r_rand = probe(combine_eps(w, z_rand, 1e-3))
    expected = info["K"] * cos2
    if r_rand.Tc <= 0:
        assert r_rand.ratio_R_star < 0.15 * info["K"]
    else:
        assert abs(r_rand.ratio_R_star - expected) / max(expected, 1e-12) < 0.25
        # misaligned: not the full K unless the random field happened to align
        if cos2 < 0.7:
            assert r_rand.ratio_R_star < 0.85 * info["K"]


def test_fixed_output_counting_at_most_m_pairs():
    """Each output k has at most m ordered partners q=k-p."""
    from ns_attacks.counting_cs import max_ordered_pairs_per_output, ordered_pairs_onto_k

    support = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    m = len(support)
    k = (1, 1, 0)
    n = ordered_pairs_onto_k(support, k)
    assert 0 <= n <= m
    assert max_ordered_pairs_per_output(support, support) <= m


def test_cs_and_K_le_16s_on_exact_shell():
    """|B̂_k| ≤ |k| E and K ≤ s (β/α)² ≤ 16s, all phases/pols."""
    from ns_attacks.attack9b_exact_shell_K import (
        K_of_w,
        build_exact_shell_field,
        field_l2,
        normalize_field,
        project_B_to_shell,
        shells_up_to,
    )
    from ns_attacks.counting_cs import (
        K_cs_fixed_s,
        beta_from_two_alpha_inputs_max,
        check_cs_pointwise,
        occupied_shell_keys,
    )

    shells = shells_up_to(5)
    alpha, beta = 5, 10
    assert beta <= beta_from_two_alpha_inputs_max(alpha)
    modes = shells[alpha]
    rng = np.random.default_rng(1390)
    for _ in range(8):
        n = len(modes)
        w = normalize_field(
            build_exact_shell_field(
                modes,
                rng.uniform(0.3, 1.5, size=n),
                rng.uniform(0, 2 * np.pi, size=n),
                rng.uniform(0, 2 * np.pi, size=n),
            )
        )
        Buu = nonlinear_B(w)
        assert check_cs_pointwise(w, Buu)
        PiB = project_B_to_shell(Buu, float(beta))
        s = len(occupied_shell_keys(PiB, float(beta)))
        info = K_of_w(w, float(alpha), float(beta))
        cap = K_cs_fixed_s(max(s, 1), float(alpha), float(beta))
        if s == 0:
            assert info["K"] < 1e-12
        else:
            assert info["K"] <= cap + 1e-8
            assert info["K"] <= 16.0 * s + 1e-8
        assert abs(field_l2(w) ** 2 - 1.0) < 1e-12
