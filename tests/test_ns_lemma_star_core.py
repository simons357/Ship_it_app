"""Lock ns_lemma_star_core.py against the Stokes-moment identities.

The core module is self-contained (no stokes_moments import). These tests
compare the two implementations on the same finite-support fields.
NS is not solved. Lemma★ is OPEN.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ns_lemma_star_core as core  # noqa: E402
from ns_attacks.stokes_moments import (  # noqa: E402
    high_triad_field,
    moments as sm_moments,
    probe,
    scale_field,
    two_shell_field,
)


def _from_stokes(d) -> core.Field:
    f = core.Field()
    seen = set()
    for k, v in d.items():
        if k in seen or k == (0, 0, 0):
            continue
        nk = (-k[0], -k[1], -k[2])
        f.set_mode(k, v)
        seen.add(k)
        seen.add(nk)
    return f


def test_shell_wavevectors_n5_has_24_points_12_canonical():
    all_pts = core.shell_wavevectors(5, canonical_only=False)
    can = core.shell_wavevectors(5, canonical_only=True)
    assert len(all_pts) == 24
    assert len(can) == 12
    assert all(core.lam(k) == 5.0 for k in all_pts)
    # every point or its negative is represented
    can_set = set(can)
    for p in all_pts:
        neg = tuple(-x for x in p)
        assert p in can_set or neg in can_set


def test_Ds_formulas_agree_on_triad():
    f = _from_stokes(high_triad_field(amp=1.4, phases=(0.2, -0.5, 0.7)))
    rec = core.R_star(f, verify=True, tol=1e-9)
    assert rec["D_s"] > 0
    assert math.isfinite(rec["R_star"])


def test_core_matches_stokes_moments_on_high_triad():
    d = high_triad_field(amp=1.4, phases=(0.2, -0.5, 0.7))
    f = _from_stokes(d)
    rec = core.R_star(f)
    r = probe(d)
    assert abs(rec["E"] - r.E) < 1e-10
    assert abs(rec["X"] - r.X) < 1e-10
    assert abs(rec["Y"] - r.Y) < 1e-10
    assert abs(rec["Z"] - r.Z) < 1e-10
    assert abs(rec["Lambda"] - r.Lambda) < 1e-10
    assert abs(rec["D_s"] - r.Ds) < 1e-8
    assert abs(rec["T_c"] - r.Tc) < 1e-8 * max(1.0, abs(r.Tc))
    if r.Tc >= 0:
        assert abs(rec["R_star"] - r.ratio_R_star_shape) < 1e-8 * max(1.0, rec["R_star"])


def test_core_matches_two_shell_Ds():
    d = two_shell_field(amp_low=1.2, amp_high=0.7, k_low=(1, 0, 0), k_high=(5, 2, 1))
    f = _from_stokes(d)
    rec = core.R_star(f)
    m = sm_moments(d)
    assert abs(rec["D_s"] - m["Ds"]) < 1e-10
    assert abs(rec["T_c"] - probe(d).Tc) < 1e-8 * max(1.0, abs(probe(d).Tc))


def test_R_star_amplitude_invariant_in_core():
    f = _from_stokes(high_triad_field(amp=1.0))
    r1 = core.R_star(f)["R_star"]
    for a in (0.2, 3.0, 11.0):
        r2 = core.R_star(f.scale(a))["R_star"]
        assert abs(r1 - r2) < 1e-9


def test_Tc_odd_under_reversal_in_core():
    f = _from_stokes(high_triad_field(amp=1.1, phases=(0.3, -0.2, 0.6)))
    rec = core.R_star(f)
    recm = core.R_star(f.scale(-1.0))
    assert abs(recm["T_c"] + rec["T_c"]) < 1e-8 * max(1.0, abs(rec["T_c"]))
    assert abs(recm["D_s"] - rec["D_s"]) < 1e-8 * max(1.0, abs(rec["D_s"]))
    assert abs(recm["E"] - rec["E"]) < 1e-12
    assert abs(recm["Y"] - rec["Y"]) < 1e-8 * max(1.0, abs(rec["Y"]))


def test_single_shell_is_vacuous():
    rng = np.random.default_rng(1390)
    w = core.random_shell_field(5, rng, target_E=1.0)
    rec = core.R_star(w)
    assert rec["vacuous_single_shell"]
    assert abs(rec["D_s"]) < 1e-10
    assert abs(rec["T_c"]) < 1e-10
    assert rec["R_star"] == 0.0


def test_false_u2_X32_product_fails_in_core():
    f = _from_stokes(high_triad_field(amp=1.0))
    rec = core.R_star(f)
    assert abs(rec["T_c"]) > 1e-8
    ratios = []
    for a in (1.0, 0.1, 0.01, 1e-3):
        ra = core.R_star(f.scale(a))
        denom = math.sqrt(ra["E"]) * (ra["X"] ** 1.5)
        ratios.append(abs(ra["T_c"]) / denom)
    assert ratios[-1] / ratios[0] > 50.0


def test_aligned_closing_packet_R_star_tends_to_K():
    rng = np.random.default_rng(1390)
    alpha, beta = 5, 10
    K = 0.0
    w = z = None
    for _ in range(24):
        w = core.random_shell_field(alpha, rng, target_E=1.0)
        z, raw = core.build_closing_direction(w, beta)
        K = core.K_alpha_beta(w, alpha, beta)
        if raw > 1e-8 and K > 1e-8:
            break
    else:
        raise AssertionError("no stretching closing packet on (5,10) in 24 draws")
    s = core.choose_closing_sign(w, z)
    rec = core.R_star(core.combine_eps(w, z, s * 1e-3))
    assert rec["T_c"] > 0
    assert abs(rec["R_star"] - K) / max(K, 1e-30) < 0.15
    rec_comp = core.R_star(core.combine_eps(w, z, -s * 1e-3))
    assert rec_comp["T_c"] < 0
    assert rec_comp["R_star"] == 0.0 or rec_comp["R_star"] < 1e-12
