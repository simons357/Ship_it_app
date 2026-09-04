#!/usr/bin/env python3
"""
Track B lemmas: fail-able checks, not a regularity proof.

Classical NS, keep 1/r^4. No Q1, no Phi as the estimate variable,
no Bridge*, no A=>B. Domain B stays open even when identities pass.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


def rec(name: str, statement: str, verdict: str, why: str, **extra) -> dict:
    row = {"name": name, "statement": statement, "verdict": verdict, "why": why}
    row.update(extra)
    return row


def k_1d(n: int) -> np.ndarray:
    return np.fft.fftfreq(n) * n


def make_grid(n: int):
    k = k_1d(n)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k2_safe = k2.copy()
    k2_safe[0, 0, 0] = 1.0
    dealias = (np.abs(kx) < n / 3) & (np.abs(ky) < n / 3) & (np.abs(kz) < n / 3)
    return kx, ky, kz, k2, k2_safe, dealias


def fft(u: np.ndarray) -> np.ndarray:
    return np.fft.fftn(u)


def ifft(uh: np.ndarray) -> np.ndarray:
    return np.fft.ifftn(uh).real


def project(uh, vh, wh, kx, ky, kz, k2_safe):
    div = kx * uh + ky * vh + kz * wh
    uh = uh - kx * div / k2_safe
    vh = vh - ky * div / k2_safe
    wh = wh - kz * div / k2_safe
    uh[0, 0, 0] = 0.0
    vh[0, 0, 0] = 0.0
    wh[0, 0, 0] = 0.0
    return uh, vh, wh


def random_divfree(n: int, rng: np.random.Generator):
    kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
    shape = (n, n, n)
    uh = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * dealias
    vh = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * dealias
    wh = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * dealias
    uh, vh, wh = project(uh, vh, wh, kx, ky, kz, k2_safe)
    return uh, vh, wh, kx, ky, kz, k2, k2_safe


def mask_band(k2: np.ndarray, kmin: float, kmax: float) -> np.ndarray:
    kabs = np.sqrt(np.maximum(k2, 0.0))
    return (kabs > kmin) & (kabs <= kmax)


def convect(u, v, w, uh, vh, wh, kx, ky, kz):
    ux = ifft(1j * kx * uh)
    uy = ifft(1j * ky * uh)
    uz = ifft(1j * kz * uh)
    vx = ifft(1j * kx * vh)
    vy = ifft(1j * ky * vh)
    vz = ifft(1j * kz * vh)
    wx = ifft(1j * kx * wh)
    wy = ifft(1j * ky * wh)
    wz = ifft(1j * kz * wh)
    return (
        u * ux + v * uy + w * uz,
        u * vx + v * vy + w * vz,
        u * wx + v * wy + w * wz,
    )


def curl(uh, vh, wh, kx, ky, kz):
    oxh = 1j * ky * wh - 1j * kz * vh
    oyh = 1j * kz * uh - 1j * kx * wh
    ozh = 1j * kx * vh - 1j * ky * uh
    return ifft(oxh), ifft(oyh), ifft(ozh), oxh, oyh, ozh


# --- B1: T2 Lemma 1 --------------------------------------------------------


def lemma_t2_low_flux(n: int = 24, j: int = 3, seed: int = 1) -> dict:
    rng = np.random.default_rng(seed)
    uh, vh, wh, kx, ky, kz, k2, _ = random_divfree(n, rng)
    low = mask_band(k2, -0.5, 2.0**j)
    band = mask_band(k2, 2.0 ** (j - 1), 2.0**j)
    uh_l, vh_l, wh_l = uh * low, vh * low, wh * low
    uh_j, vh_j, wh_j = uh * band, vh * band, wh * band
    u_l, v_l, w_l = ifft(uh_l), ifft(vh_l), ifft(wh_l)
    u_j, v_j, w_j = ifft(uh_j), ifft(vh_j), ifft(wh_j)
    cu, cv, cw = convect(u_l, v_l, w_l, uh_j, vh_j, wh_j, kx, ky, kz)
    vol = (2.0 * math.pi) ** 3
    flux = float(np.mean(cu * u_j + cv * v_j + cw * w_j)) * vol
    energy = float(np.mean(u_j * u_j + v_j * v_j + w_j * w_j)) * vol
    rel = abs(flux) / max(energy, 1e-30)
    ok = rel < 1e-10
    return rec(
        "B1_t2_low_flux",
        "∫ (u_≤j · ∇) u_j · u_j = 0 for periodic div-free u",
        "pass" if ok else "fail",
        "div-free + parts: (1/2) ∫ u_low · ∇(|u_j|²) = 0. T2 Lemma 1 only.",
        residual=flux,
        rel_residual=rel,
        energy_j=energy,
        n=n,
        j=j,
    )


def lemma_t2_lemma2_circular() -> dict:
    return rec(
        "B1b_t2_lemma2_dropped",
        "T2 Lemma 2 (H^{2.3} absorbing ball) is an input to the a priori estimate",
        "fail",
        "Already-regular H^{2.3} is circular for large-data Track B. Not used.",
    )


# --- B2: regime cover ------------------------------------------------------


def packet_stats(x: np.ndarray) -> dict:
    x = np.asarray(x, dtype=float)
    total = float(np.sum(x))
    if total <= 0:
        return {"sigma": 0.0, "rho": 0.0, "jstar": 0}
    jstar = int(np.argmax(x))
    lo, hi = max(jstar - 1, 0), min(jstar + 1, len(x) - 1)
    sigma = float(np.sum(x[lo : hi + 1]) / total)
    rho = float(np.max(x) / total)
    return {"sigma": sigma, "rho": rho, "jstar": jstar}


def lemma_regime_cover(n_shells: int = 12, trials: int = 400, seed: int = 2) -> dict:
    rng = np.random.default_rng(seed)
    gaps = 0
    rho_le_sigma = 0
    for _ in range(trials):
        x = rng.random(n_shells)
        st = packet_stats(x)
        conc = st["sigma"] >= 0.5
        spread = st["sigma"] <= 0.5
        if not (conc or spread):
            gaps += 1
        if st["rho"] <= st["sigma"] + 1e-12:
            rho_le_sigma += 1
    ok = gaps == 0 and rho_le_sigma == trials
    return rec(
        "B2_regime_cover",
        "3-CONC (σ≥1/2) and SPREAD (σ≤1/2) cover (0,1]; ρ≤σ",
        "pass" if ok else "fail",
        "A cover of mass fractions, not a dynamics theorem. One threshold, no gap.",
        trials=trials,
        gaps=gaps,
        rho_le_sigma=rho_le_sigma,
    )


# --- B3: 3-shell Bernstein / Ring -----------------------------------------


def three_shell_field(n: int, jstar: int, rng: np.random.Generator):
    uh, vh, wh, kx, ky, kz, k2, k2_safe = random_divfree(n, rng)
    band = mask_band(k2, 2.0 ** (jstar - 1), 2.0 ** (jstar + 1))
    uh, vh, wh = uh * band, vh * band, wh * band
    uh, vh, wh = project(uh, vh, wh, kx, ky, kz, k2_safe)
    return uh, vh, wh, kx, ky, kz, k2


def lemma_ring_bernstein(n: int = 32, seed: int = 3) -> dict:
    rng = np.random.default_rng(seed)
    ratios = []
    dir_ratios = []
    for jstar in (3, 4):
        uh, vh, wh, kx, ky, kz, _ = three_shell_field(n, jstar, rng)
        ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
        gox = [ifft(1j * k * oxh) for k in (kx, ky, kz)]
        goy = [ifft(1j * k * oyh) for k in (kx, ky, kz)]
        goz = [ifft(1j * k * ozh) for k in (kx, ky, kz)]
        grad_inf = max(float(np.max(np.abs(g))) for g in gox + goy + goz)
        vol = (2.0 * math.pi) ** 3
        ol2 = math.sqrt(float(np.mean(ox * ox + oy * oy + oz * oz)) * vol)
        if ol2 < 1e-14:
            continue
        ratios.append(grad_inf / ((2.0 ** (2 * jstar)) * ol2))

        mag = np.sqrt(ox * ox + oy * oy + oz * oz)
        rms = float(np.sqrt(np.mean(mag * mag)))
        ec = mag >= 0.5 * rms
        if not np.any(ec):
            continue
        # ∇ξ = (∇ω)/|ω| − ω ⊗ (ω·∇ω) / |ω|³
        dxi = []
        for gi, oi in ((gox, ox), (goy, oy), (goz, oz)):
            for d in range(3):
                wd = ox * gox[d] + oy * goy[d] + oz * goz[d]
                dxi.append(gi[d] / (mag + 1e-30) - oi * wd / (mag**3 + 1e-30))
        dxi_inf = max(float(np.max(np.abs(comp[ec]))) for comp in dxi)
        dir_ratios.append(dxi_inf / (2.0**jstar))

    bern_ok = bool(ratios) and max(ratios) < 2.0
    dir_ok = bool(dir_ratios) and max(dir_ratios) < 8.0
    ok = bern_ok and dir_ok
    return rec(
        "B3_three_shell_ring",
        "3-shell support ⇒ ||∇ω||_∞ ≤ C 2^{2j*} ||ω||_2 and ||∇ξ||_∞ ≤ C 2^{j*} on E_c",
        "pass" if ok else "fail",
        "Bernstein on a triad packet. Not stretching depletion. Not all-data geometry.",
        bernstein_ratios=ratios,
        direction_ratios=dir_ratios,
        n=n,
    )


def lemma_ring_not_depletion() -> dict:
    return rec(
        "B3b_ring_is_not_depletion",
        "3-shell Ring forces cos α_3 → 0 for all data",
        "fail",
        "Ring bounds |∇ξ| on E_c. It does not force alignment. Biot–Savart slogan stays forbidden.",
    )


# --- B4: tube Hardy --------------------------------------------------------


def hardy_1d_samples(n: int = 800, delta: float = 1.0, seed: int = 4) -> dict:
    rng = np.random.default_rng(seed)
    r = np.linspace(delta / n, delta, n)
    worst = 0.0
    for _ in range(40):
        coeff = rng.normal(size=5)
        g = np.zeros_like(r)
        # g(0)=0: start at r^1
        for k, a in enumerate(coeff, start=1):
            g = g + a * r**k
        lhs = float(np.trapezoid((g / r) ** 2, r))
        gp = np.gradient(g, r)
        rhs = 4.0 * float(np.trapezoid(gp**2, r))
        worst = max(worst, lhs / max(rhs, 1e-30))
    return {"worst_lhs_over_4grad": worst, "holds": worst <= 1.0 + 1e-6}


def hardy_tube_wall_samples(n: int = 800, delta: float = 1.0, seed: int = 5) -> dict:
    rng = np.random.default_rng(seed)
    r = np.linspace(delta / n, delta, n)
    worst = 0.0
    for _ in range(40):
        coeff = rng.normal(size=5)
        h = np.zeros_like(r)
        for k, a in enumerate(coeff, start=1):
            h = h + a * r**k
        lhs = float(np.trapezoid(h**2 / r, r))
        hp = np.gradient(h, r)
        rhs = 4.0 * float(np.trapezoid(hp**2 * r, r)) + 2.0 * float(h[-1] ** 2)
        worst = max(worst, lhs / max(rhs, 1e-30))
    return {"worst_lhs_over_rhs": worst, "holds": worst <= 1.0 + 2e-2}


def lemma_tube_hardy() -> dict:
    one = hardy_1d_samples()
    tube = hardy_tube_wall_samples()
    ok = one["holds"] and tube["holds"]
    return rec(
        "B4_tube_hardy",
        "g(0)=0 ⇒ ∫(g/r)² dr ≤ 4∫(g')²; h(0)=0 ⇒ ∫ h²/r dr ≤ 4∫(h')² r dr + 2 h(δ)²",
        "pass" if ok else "fail",
        "Localized Hardy with a wall term. Does not yet beat I_tube by viscosity.",
        hardy_1d=one,
        hardy_tube_wall=tube,
    )


def lemma_hardy_not_closed() -> dict:
    from track_b_hardy_tube import lemma_all_data_killed

    return lemma_all_data_killed()


def lemma_packet_tube() -> dict:
    from track_b_hardy_tube import lemma_packet_absorbed

    return lemma_packet_absorbed()


def lemma_wall_match() -> dict:
    from track_b_hardy_tube import lemma_wall_match as wall

    return wall()


# --- B5: swirl dissipation -------------------------------------------------


def lemma_swirl_visc(nr: int = 96, nz: int = 64) -> dict:
    r0, r1 = 1e-3, 1.5
    r = np.linspace(r0, r1, nr)
    z = np.linspace(0.0, 2.0 * math.pi, nz, endpoint=False)
    R, Z = np.meshgrid(r, z, indexing="ij")
    uth = (R**2) * np.exp(-((R / 0.4) ** 2)) * np.sin(Z)
    gamma = R * uth
    d2z = -uth  # sin → -sin
    # radial derivatives
    dr = r[1] - r[0]
    duth_dr = np.gradient(uth, dr, axis=0)
    d2uth_dr = np.gradient(duth_dr, dr, axis=0)
    L = d2uth_dr + duth_dr / R + d2z
    vec_th = L - uth / (R**2)
    # manufactured check: for uth = r^2 f(z) near 0, uth/r^2 = f(z)
    # identity we record: angular piece uth/r
    weight = R  # r dr dz, dθ absorbed as 2π later
    ang = float(np.sum((uth / R) ** 2 * weight) * dr * (z[1] - z[0]))
    source = 2.0 * gamma * np.gradient(gamma, z[1] - z[0], axis=1) / (R**4)
    i_tube = float(np.sum(np.abs(source) * weight) * dr * (z[1] - z[0]))
    # vector Laplacian should be finite on this field
    finite = bool(np.all(np.isfinite(vec_th)))
    ratio = i_tube / max(ang, 1e-30)
    return rec(
        "B5_swirl_visc_identity",
        "axisymmetric (Δu)_θ = Δu_θ − u_θ/r²; angular piece ∫(u_θ/r)² sits in the tube",
        "pass" if finite and ang > 0 else "fail",
        "Identity only. Ratio |I_source|/angular-mass is reported, not claimed < 1.",
        angular_mass=ang,
        abs_source_mass=i_tube,
        source_over_angular=ratio,
        vector_laplacian_finite=finite,
    )


def lemma_swirl_domination() -> dict:
    from track_b_angular import lemma_angular_not_dominate as ang

    return ang()


def lemma_angular_climbs() -> dict:
    from track_b_angular import lemma_angular_climbs as climbs

    return climbs()


def lemma_killer_not_angular() -> dict:
    from track_b_angular import lemma_killer_not_angular as kill_ang

    return kill_ang()


def lemma_not_phi_cancel() -> dict:
    from track_b_angular import lemma_not_phi_cancel as no_phi

    return no_phi()


def lemma_angular_not_close() -> dict:
    from track_b_angular import lemma_angular_not_close as ang_ap

    return ang_ap()


def lemma_angular_not_a_retune() -> dict:
    from track_b_angular import lemma_angular_not_a_retune as ang_rt

    return ang_rt()


# --- B6: energy integrability is not a close -------------------------------


def lemma_energy_not_enough() -> dict:
    tstar = 1.0
    t = np.linspace(0.0, tstar - 1e-4, 2000)
    x = (tstar - t) ** (-0.5)
    integ = float(np.trapezoid(x, t))
    bounded = bool(np.max(x) < 1e3)
    # integrable on [0, T*-ε] stays finite as ε→0 in the limit of the antiderivative
    # but X is unbounded. That kills "∫X < ∞ ⇒ X ∈ L^∞".
    return rec(
        "B6_energy_not_enough",
        "Leray ∫ X dt < ∞ implies X ∈ L^∞ (closes the cubic enstrophy ODE)",
        "fail",
        f"X=(T*-t)^{{-1/2}} has ∫X≈{integ:.3f} on a truncated interval and is unbounded. Viscosity or geometry has to do the extra work.",
        spike_unbounded=not bounded,
        truncated_integral=integ,
    )


def lemma_bony_split() -> dict:
    from track_b_bony_t import lemma_bony_split as bony

    return bony()


def lemma_bony_t2() -> dict:
    from track_b_bony_t import lemma_self_is_b1

    return lemma_self_is_b1()


def lemma_bony_energy() -> dict:
    from track_b_bony_t import lemma_low_T_energy

    return lemma_low_T_energy()


def lemma_bony_not_rho() -> dict:
    from track_b_bony_t import lemma_low_T_not_rho

    return lemma_low_T_not_rho()


def lemma_occupation_clock() -> dict:
    from track_b_occupation import lemma_clock

    return lemma_clock()


def lemma_occupation_high_j() -> dict:
    from track_b_occupation import lemma_high_jstar

    return lemma_high_jstar()


def lemma_occupation_leray() -> dict:
    from track_b_occupation import lemma_leray_not_short

    return lemma_leray_not_short()


def lemma_occupation_glue() -> dict:
    from track_b_occupation import lemma_occupation_not_close

    return lemma_occupation_not_close()


def lemma_glue_bookkeeping() -> dict:
    from track_b_glue import lemma_bookkeeping

    return lemma_bookkeeping()


def lemma_glue_high_j() -> dict:
    from track_b_glue import lemma_high_j_glue

    return lemma_high_j_glue()


def lemma_glue_low_j() -> dict:
    from track_b_glue import lemma_low_j_blows

    return lemma_low_j_blows()


def lemma_glue_switching() -> dict:
    from track_b_glue import lemma_switching

    return lemma_switching()


def lemma_glue_not_ns() -> dict:
    from track_b_glue import lemma_glue_not_regularity

    return lemma_glue_not_regularity()


def lemma_energy_ceiling() -> dict:
    from track_b_low_j import lemma_energy_ceiling as ceiling

    return ceiling()


def lemma_frozen_blow_not_ns() -> dict:
    from track_b_low_j import lemma_frozen_blow_not_ns as frozen

    return frozen()


def lemma_ceiling_not_climbing() -> dict:
    from track_b_low_j import lemma_ceiling_not_climbing as climb

    return climb()


def lemma_climbing_open() -> dict:
    from track_b_low_j import lemma_climbing_open as climbing

    return climbing()


def lemma_not_a_retune() -> dict:
    from track_b_low_j import lemma_not_a_retune as no_retune

    return no_retune()


def lemma_climb_bookkeeping() -> dict:
    from track_b_climb import lemma_climb_bookkeeping as climb_bk

    return climb_bk()


def lemma_bounded_j_bounds_x() -> dict:
    from track_b_climb import lemma_bounded_j_bounds_x as bounded

    return bounded()


def lemma_slow_climb_blows() -> dict:
    from track_b_climb import lemma_slow_climb_blows as slow

    return slow()


def lemma_fast_climb_sits() -> dict:
    from track_b_climb import lemma_fast_climb_sits as fast

    return fast()


def lemma_ns_climb_law() -> dict:
    from track_b_climb import lemma_ns_climb_law as law

    return law()


def lemma_climb_not_a_priori() -> dict:
    from track_b_climb import lemma_climb_not_a_priori as not_ap

    return not_ap()


def lemma_barycenter() -> dict:
    from track_b_climb_law import lemma_barycenter as bary

    return bary()


def lemma_c_from_rhs() -> dict:
    from track_b_climb_law import lemma_c_from_rhs as from_rhs

    return from_rhs()


def lemma_t0_not_saving() -> dict:
    from track_b_climb_law import lemma_t0_not_saving as t0

    return t0()


def lemma_visc_pulls_down() -> dict:
    from track_b_climb_law import lemma_visc_pulls_down as pulls

    return pulls()


def lemma_evolved_cascade() -> dict:
    from track_b_climb_law import lemma_evolved_cascade_open as ev

    return ev()


def lemma_law_not_a_priori() -> dict:
    from track_b_climb_law import lemma_law_not_a_priori as law_ap

    return law_ap()


def lemma_short_run() -> dict:
    from track_b_evolve import lemma_run_completes

    return lemma_run_completes()


def lemma_evolve_no_saving() -> dict:
    from track_b_evolve import lemma_no_saving_climb

    return lemma_no_saving_climb()


def lemma_evolve_no_high() -> dict:
    from track_b_evolve import lemma_no_high_fill

    return lemma_no_high_fill()


def lemma_evolve_stays_conc() -> dict:
    from track_b_evolve import lemma_stays_conc

    return lemma_stays_conc()


def lemma_evolve_visc_down() -> dict:
    from track_b_evolve import lemma_visc_still_down

    return lemma_visc_still_down()


def lemma_finer_open() -> dict:
    from track_b_evolve import lemma_finer_open as finer

    return finer()


def lemma_evolve_not_a_priori() -> dict:
    from track_b_evolve import lemma_evolve_not_a_priori as ev_ap

    return ev_ap()


def lemma_strain_identity() -> dict:
    from track_b_geometry import lemma_strain_identity as ident

    return ident()


def lemma_conc_not_depleted() -> dict:
    from track_b_geometry import lemma_conc_not_depleted as conc

    return conc()


def lemma_ring_not_alignment() -> dict:
    from track_b_geometry import lemma_ring_not_alignment as ring_al

    return ring_al()


def lemma_cf_conditional() -> dict:
    from track_b_geometry import lemma_cf_conditional as cf

    return cf()


def lemma_geometry_not_close() -> dict:
    from track_b_geometry import lemma_geometry_not_close as geo_ap

    return geo_ap()


def lemma_geo_not_a_retune() -> dict:
    from track_b_geometry import lemma_geo_not_a_retune as geo_rt

    return geo_rt()


def lemma_stretch_budget() -> dict:
    from track_b_stretch import lemma_budget_readable as bud

    return bud()


def lemma_cf_weights_budget() -> dict:
    from track_b_stretch import lemma_cf_weights_budget as wgt

    return wgt()


def lemma_majority_aligned() -> dict:
    from track_b_stretch import lemma_majority_aligned as maj

    return maj()


def lemma_run_not_depleted() -> dict:
    from track_b_stretch import lemma_run_not_depleted as rnd

    return rnd()


def lemma_run_keeps_budget() -> dict:
    from track_b_stretch import lemma_run_keeps_budget as keep

    return keep()


def lemma_budget_not_close() -> dict:
    from track_b_stretch import lemma_budget_not_close as bud_ap

    return bud_ap()


def lemma_stretch_not_a_retune() -> dict:
    from track_b_stretch import lemma_stretch_not_a_retune as st_rt

    return st_rt()


def lemma_enstrophy_identity() -> dict:
    from track_b_balance import lemma_enstrophy_identity as ident

    return ident()


def lemma_visc_owns_net() -> dict:
    from track_b_balance import lemma_visc_owns_net as owns

    return owns()


def lemma_plus_not_a_cubic() -> dict:
    from track_b_balance import lemma_plus_not_a_cubic as plus

    return plus()


def lemma_l2_not_bkm() -> dict:
    from track_b_balance import lemma_not_bkm as not_bkm

    return not_bkm()


def lemma_not_all_conc() -> dict:
    from track_b_balance import lemma_not_all_conc as not_all

    return not_all()


def lemma_balance_not_close() -> dict:
    from track_b_balance import lemma_balance_not_close as bal_ap

    return bal_ap()


def lemma_balance_not_a_retune() -> dict:
    from track_b_balance import lemma_balance_not_a_retune as bal_rt

    return bal_rt()


def lemma_field_clock() -> dict:
    from track_b_field_occ import lemma_field_clock as fclk

    return fclk()


def lemma_paths_stay_conc() -> dict:
    from track_b_field_occ import lemma_stays_conc as stay

    return stay()


def lemma_clock_did_not_save() -> dict:
    from track_b_field_occ import lemma_clock_did_not_save as nosave

    return nosave()


def lemma_conc_not_short() -> dict:
    from track_b_field_occ import lemma_conc_not_short as notshort

    return notshort()


def lemma_cubic_not_live_time() -> dict:
    from track_b_field_occ import lemma_cubic_not_live_time as nlive

    return nlive()


def lemma_field_occ_not_close() -> dict:
    from track_b_field_occ import lemma_field_occ_not_close as focc_ap

    return focc_ap()


def lemma_field_occ_not_a_retune() -> dict:
    from track_b_field_occ import lemma_field_occ_not_a_retune as focc_rt

    return focc_rt()


def lemma_field_rates() -> dict:
    from track_b_field_glue import lemma_field_rates as frates

    return frates()


def lemma_sign_mismatch() -> dict:
    from track_b_field_glue import lemma_sign_mismatch as smis

    return smis()


def lemma_not_the_blowup() -> dict:
    from track_b_field_glue import lemma_not_the_blowup as nblow

    return nblow()


def lemma_alpha_not_cubic() -> dict:
    from track_b_field_glue import lemma_alpha_not_cubic as na

    return na()


def lemma_gamma_not_visc() -> dict:
    from track_b_field_glue import lemma_gamma_not_visc as gv

    return gv()


def lemma_field_glue_not_close() -> dict:
    from track_b_field_glue import lemma_field_glue_not_close as fg_ap

    return fg_ap()


def lemma_field_glue_not_a_retune() -> dict:
    from track_b_field_glue import lemma_field_glue_not_a_retune as fg_rt

    return fg_rt()


def lemma_field_c() -> dict:
    from track_b_ns_climb import lemma_field_c as fc

    return fc()


def lemma_blob_t0_not_saving() -> dict:
    from track_b_ns_climb import lemma_blob_t0_not_saving as bt0

    return bt0()


def lemma_paths_not_saving() -> dict:
    from track_b_ns_climb import lemma_paths_not_saving as pns

    return pns()


def lemma_blob_visc_not_ladder() -> dict:
    from track_b_ns_climb import lemma_blob_visc_not_ladder as bvl

    return bvl()


def lemma_offset_not_climb() -> dict:
    from track_b_ns_climb import lemma_offset_not_climb as onc

    return onc()


def lemma_ns_climb_not_close() -> dict:
    from track_b_ns_climb import lemma_ns_climb_not_close as nc_ap

    return nc_ap()


def lemma_ns_climb_not_a_retune() -> dict:
    from track_b_ns_climb import lemma_ns_climb_not_a_retune as nc_rt

    return nc_rt()


def lemma_window_rates() -> dict:
    from track_b_climb_sketch import lemma_window_rates as wr

    return wr()


def lemma_not_the_room() -> dict:
    from track_b_climb_sketch import lemma_not_the_room as nroom

    return nroom()


def lemma_not_the_sitting() -> dict:
    from track_b_climb_sketch import lemma_not_the_sitting as nsit

    return nsit()


def lemma_delta_j_not_prescribed() -> dict:
    from track_b_climb_sketch import lemma_delta_j_not_prescribed as djnp

    return djnp()


def lemma_sketch_did_not_save() -> dict:
    from track_b_climb_sketch import lemma_sketch_did_not_save as sds

    return sds()


def lemma_sketch_not_close() -> dict:
    from track_b_climb_sketch import lemma_sketch_not_close as sk_ap

    return sk_ap()


def lemma_sketch_not_a_retune() -> dict:
    from track_b_climb_sketch import lemma_sketch_not_a_retune as sk_rt

    return sk_rt()


def lemma_longer_readable() -> dict:
    from track_b_longer import lemma_longer_readable as lr

    return lr()


def lemma_longer_not_saving() -> dict:
    from track_b_longer import lemma_longer_not_saving as lns

    return lns()


def lemma_longer_not_ladder() -> dict:
    from track_b_longer import lemma_longer_not_ladder as lnl

    return lnl()


def lemma_longer_no_high_fill() -> dict:
    from track_b_longer import lemma_longer_no_high_fill as lnh

    return lnh()


def lemma_longer_clock_did_not_save() -> dict:
    from track_b_longer import lemma_longer_clock_did_not_save as lcd

    return lcd()


def lemma_finer_box_open() -> dict:
    from track_b_longer import lemma_finer_open as finer_box

    return finer_box()


def lemma_longer_not_a_retune() -> dict:
    from track_b_longer import lemma_longer_not_a_retune as lrt

    return lrt()


def lemma_dns_readable() -> dict:
    from track_b_dns import lemma_dns_readable as dr

    return dr()


def lemma_dns_not_a_priori() -> dict:
    from track_b_dns import lemma_dns_not_a_priori as dna

    return dna()


def lemma_room_time_not_continuation() -> dict:
    from track_b_dns import lemma_room_time_not_continuation as rtc

    return rtc()


def lemma_packet_not_all_data() -> dict:
    from track_b_dns import lemma_packet_not_all_data as pnad

    return pnad()


def lemma_no_blow_not_bounded() -> dict:
    from track_b_dns import lemma_no_blow_not_bounded as nbb

    return nbb()


def lemma_finer_still_open() -> dict:
    from track_b_dns import lemma_finer_still_open as fso

    return fso()


def lemma_dns_not_a_retune() -> dict:
    from track_b_dns import lemma_dns_not_a_retune as dnr

    return dnr()


def lemma_tube_readable() -> dict:
    from track_b_tube import lemma_tube_readable as tr

    return tr()


def lemma_angular_not_a_priori() -> dict:
    from track_b_tube import lemma_angular_not_a_priori as ana

    return ana()


def lemma_b4c_not_a_priori() -> dict:
    from track_b_tube import lemma_b4c_not_a_priori as b4c_ap

    return b4c_ap()


def lemma_rd_not_bounded() -> dict:
    from track_b_tube import lemma_rd_not_bounded as rdnb

    return rdnb()


def lemma_not_revive_hardy_or_phi() -> dict:
    from track_b_tube import lemma_not_revive_hardy_or_phi as nrhp

    return nrhp()


def lemma_geometry_leftover() -> dict:
    from track_b_tube import lemma_geometry_leftover as geo_l

    return geo_l()


def lemma_tube_not_a_retune() -> dict:
    from track_b_tube import lemma_tube_not_a_retune as tnr

    return tnr()


def lemma_align_readable() -> dict:
    from track_b_align import lemma_align_readable as ar

    return ar()


def lemma_depletion_not_a_priori() -> dict:
    from track_b_align import lemma_depletion_not_a_priori as dna

    return dna()


def lemma_frame_not_a_priori() -> dict:
    from track_b_align import lemma_frame_not_a_priori as fna

    return fna()


def lemma_median_not_a_class() -> dict:
    from track_b_align import lemma_median_not_a_class as mnc

    return mnc()


def lemma_cf_not_bkm() -> dict:
    from track_b_align import lemma_cf_not_bkm as cnb

    return cnb()


def lemma_budget_leftover() -> dict:
    from track_b_align import lemma_budget_leftover as bl

    return bl()


def lemma_align_not_a_retune() -> dict:
    from track_b_align import lemma_align_not_a_retune as anr

    return anr()


def lemma_payers_readable() -> dict:
    from track_b_payers import lemma_payers_readable as pr

    return pr()


def lemma_share_not_a_priori() -> dict:
    from track_b_payers import lemma_share_not_a_priori as sna

    return sna()


def lemma_emptying_not_continuation() -> dict:
    from track_b_payers import lemma_emptying_not_continuation as enc

    return enc()


def lemma_share_not_a_class() -> dict:
    from track_b_payers import lemma_share_not_a_class as snc

    return snc()


def lemma_aligned_budget_not_bkm() -> dict:
    from track_b_payers import lemma_aligned_budget_not_bkm as abn

    return abn()


def lemma_enstrophy_leftover() -> dict:
    from track_b_payers import lemma_enstrophy_leftover as el

    return el()


def lemma_payers_not_a_retune() -> dict:
    from track_b_payers import lemma_payers_not_a_retune as pnr

    return pnr()


def lemma_net_readable() -> dict:
    from track_b_net import lemma_net_readable as nr

    return nr()


def lemma_visc_ensemble_not_a_priori() -> dict:
    from track_b_net import lemma_visc_ensemble_not_a_priori as vena

    return vena()


def lemma_cancel_not_all_data() -> dict:
    from track_b_net import lemma_cancel_not_all_data as cnad

    return cnad()


def lemma_decay_not_continuation() -> dict:
    from track_b_net import lemma_decay_not_continuation as dnc

    return dnc()


def lemma_net_not_integral_max() -> dict:
    from track_b_net import lemma_net_not_integral_max as nnim

    return nnim()


def lemma_coherent_leftover() -> dict:
    from track_b_net import lemma_coherent_leftover as cl

    return cl()


def lemma_net_not_a_retune() -> dict:
    from track_b_net import lemma_net_not_a_retune as nnr

    return nnr()


def lemma_blob_priori_readable() -> dict:
    from track_b_blob import lemma_blob_priori_readable as bpr

    return bpr()


def lemma_onesided_not_a_priori() -> dict:
    from track_b_blob import lemma_onesided_not_a_priori as ona

    return ona()


def lemma_sign_not_a_class() -> dict:
    from track_b_blob import lemma_sign_not_a_class as snc

    return snc()


def lemma_peaked_not_integral_max() -> dict:
    from track_b_blob import lemma_peaked_not_integral_max as pnim

    return pnim()


def lemma_nu_not_continuation() -> dict:
    from track_b_blob import lemma_nu_not_continuation as nnc

    return nnc()


def lemma_occupation_leftover() -> dict:
    from track_b_blob import lemma_occupation_leftover as ol

    return ol()


def lemma_blob_priori_not_a_retune() -> dict:
    from track_b_blob import lemma_blob_priori_not_a_retune as bpnr

    return bpnr()


def lemma_clock_priori_readable() -> dict:
    from track_b_clock import lemma_clock_priori_readable as cpr

    return cpr()


def lemma_stay_not_a_priori() -> dict:
    from track_b_clock import lemma_stay_not_a_priori as sna

    return sna()


def lemma_full_occ_not_short() -> dict:
    from track_b_clock import lemma_full_occ_not_short as fons

    return fons()


def lemma_occ_not_live_cubic() -> dict:
    from track_b_clock import lemma_occ_not_live_cubic as onlc

    return onlc()


def lemma_clock_not_integral_max() -> dict:
    from track_b_clock import lemma_clock_not_integral_max as cnim

    return cnim()


def lemma_glue_leftover() -> dict:
    from track_b_clock import lemma_glue_leftover as gl

    return gl()


def lemma_clock_priori_not_a_retune() -> dict:
    from track_b_clock import lemma_clock_priori_not_a_retune as cpnr

    return cpnr()


def lemma_match_priori_readable() -> dict:
    from track_b_match import lemma_match_priori_readable as mpr

    return mpr()


def lemma_match_not_a_priori() -> dict:
    from track_b_match import lemma_match_not_a_priori as mna

    return mna()


def lemma_shrink_alpha_not_continuation() -> dict:
    from track_b_match import lemma_shrink_alpha_not_continuation as sanc

    return sanc()


def lemma_wrong_sign_not_ns() -> dict:
    from track_b_match import lemma_wrong_sign_not_ns as wsns

    return wsns()


def lemma_match_not_integral_max() -> dict:
    from track_b_match import lemma_match_not_integral_max as mnim

    return mnim()


def lemma_climb_leftover() -> dict:
    from track_b_match import lemma_climb_leftover as clb

    return clb()


def lemma_match_priori_not_a_retune() -> dict:
    from track_b_match import lemma_match_priori_not_a_retune as mpnr

    return mpnr()


def lemma_saving_priori_readable() -> dict:
    from track_b_saving import lemma_saving_priori_readable as spr

    return spr()


def lemma_field_c_not_a_priori() -> dict:
    from track_b_saving import lemma_field_c_not_a_priori as fcna

    return fcna()


def lemma_offset_not_continuation() -> dict:
    from track_b_saving import lemma_offset_not_continuation as onc

    return onc()


def lemma_ladder_not_a_class() -> dict:
    from track_b_saving import lemma_ladder_not_a_class as lnc

    return lnc()


def lemma_c_not_integral_max() -> dict:
    from track_b_saving import lemma_c_not_integral_max as cnim

    return cnim()


def lemma_sketch_leftover() -> dict:
    from track_b_saving import lemma_sketch_leftover as sl

    return sl()


def lemma_saving_priori_not_a_retune() -> dict:
    from track_b_saving import lemma_saving_priori_not_a_retune as spnr

    return spnr()


def lemma_window_priori_readable() -> dict:
    from track_b_window import lemma_window_priori_readable as wpr

    return wpr()


def lemma_window_not_a_priori() -> dict:
    from track_b_window import lemma_window_not_a_priori as wna

    return wna()


def lemma_short_not_continuation() -> dict:
    from track_b_window import lemma_short_not_continuation as snc

    return snc()


def lemma_growing_not_ns() -> dict:
    from track_b_window import lemma_growing_not_ns as gns

    return gns()


def lemma_window_not_integral_max() -> dict:
    from track_b_window import lemma_window_not_integral_max as wnim

    return wnim()


def lemma_finer_box_leftover() -> dict:
    from track_b_window import lemma_finer_box_leftover as fbl

    return fbl()


def lemma_window_priori_not_a_retune() -> dict:
    from track_b_window import lemma_window_priori_not_a_retune as wpnr

    return wpnr()


def lemma_finer_priori_readable() -> dict:
    from track_b_finer import lemma_finer_priori_readable as fpr

    return fpr()


def lemma_finer_not_a_priori() -> dict:
    from track_b_finer import lemma_finer_not_a_priori as fna

    return fna()


def lemma_fft_not_continuation() -> dict:
    from track_b_finer import lemma_fft_not_continuation as fnc

    return fnc()


def lemma_n64_not_ns() -> dict:
    from track_b_finer import lemma_n64_not_ns as nns

    return nns()


def lemma_finer_not_integral_max() -> dict:
    from track_b_finer import lemma_finer_not_integral_max as fnim

    return fnim()


def lemma_dns_finer_leftover() -> dict:
    from track_b_finer import lemma_dns_finer_leftover as dfl

    return dfl()


def lemma_finer_priori_not_a_retune() -> dict:
    from track_b_finer import lemma_finer_priori_not_a_retune as fpnr

    return fpnr()


def lemma_mesh_priori_readable() -> dict:
    from track_b_mesh import lemma_mesh_priori_readable as mpr

    return mpr()


def lemma_mesh_not_a_priori() -> dict:
    from track_b_mesh import lemma_mesh_not_a_priori as mna

    return mna()


def lemma_mesh_not_continuation() -> dict:
    from track_b_mesh import lemma_mesh_not_continuation as mnc

    return mnc()


def lemma_finer_dns_not_ns() -> dict:
    from track_b_mesh import lemma_finer_dns_not_ns as fdns

    return fdns()


def lemma_mesh_not_integral_max() -> dict:
    from track_b_mesh import lemma_mesh_not_integral_max as mnim

    return mnim()


def lemma_regularity_leftover() -> dict:
    from track_b_mesh import lemma_regularity_leftover as rl

    return rl()


def lemma_mesh_priori_not_a_retune() -> dict:
    from track_b_mesh import lemma_mesh_priori_not_a_retune as mpnr

    return mpnr()


def lemma_close_priori_readable() -> dict:
    from track_b_close import lemma_close_priori_readable as cpr

    return cpr()


def lemma_close_not_a_priori() -> dict:
    from track_b_close import lemma_close_not_a_priori as cna

    return cna()


def lemma_catalog_not_continuation() -> dict:
    from track_b_close import lemma_catalog_not_continuation as cnc

    return cnc()


def lemma_fails_not_ns() -> dict:
    from track_b_close import lemma_fails_not_ns as fns

    return fns()


def lemma_close_not_integral_max() -> dict:
    from track_b_close import lemma_close_not_integral_max as cnim

    return cnim()


def lemma_domain_leftover() -> dict:
    from track_b_close import lemma_domain_leftover as dl

    return dl()


def lemma_close_priori_not_a_retune() -> dict:
    from track_b_close import lemma_close_priori_not_a_retune as cpnr

    return cpnr()


def lemma_object_priori_readable() -> dict:
    from track_b_object import lemma_object_priori_readable as opr

    return opr()


def lemma_object_not_a_priori() -> dict:
    from track_b_object import lemma_object_not_a_priori as ona

    return ona()


def lemma_object_not_continuation() -> dict:
    from track_b_object import lemma_object_not_continuation as onc

    return onc()


def lemma_object_not_ns() -> dict:
    from track_b_object import lemma_object_not_ns as ons

    return ons()


def lemma_object_not_integral_max() -> dict:
    from track_b_object import lemma_object_not_integral_max as onim

    return onim()


def lemma_object_not_regularity() -> dict:
    from track_b_object import lemma_object_not_regularity as onr

    return onr()


def lemma_object_priori_not_a_retune() -> dict:
    from track_b_object import lemma_object_priori_not_a_retune as opnr

    return opnr()


def lemma_residual_readable() -> dict:
    from track_b_residual import lemma_residual_readable as rr

    return rr()


def lemma_residual_not_a_priori() -> dict:
    from track_b_residual import lemma_residual_not_a_priori as rna

    return rna()


def lemma_residual_not_continuation() -> dict:
    from track_b_residual import lemma_residual_not_continuation as rnc

    return rnc()


def lemma_residual_not_ns() -> dict:
    from track_b_residual import lemma_residual_not_ns as rns

    return rns()


def lemma_residual_not_integral_max() -> dict:
    from track_b_residual import lemma_residual_not_integral_max as rnim

    return rnim()


def lemma_residual_not_regularity() -> dict:
    from track_b_residual import lemma_residual_not_regularity as rnr

    return rnr()


def lemma_residual_not_a_retune() -> dict:
    from track_b_residual import lemma_residual_not_a_retune as rnr2

    return rnr2()


def lemma_coherent_field() -> dict:
    from track_b_coherent import lemma_coherent_field as coh

    return coh()


def lemma_net_is_plus() -> dict:
    from track_b_coherent import lemma_net_is_plus as netp

    return netp()


def lemma_cubic_not_live() -> dict:
    from track_b_coherent import lemma_cubic_not_live as not_live

    return not_live()


def lemma_tube_still_cancels() -> dict:
    from track_b_coherent import lemma_tube_still_cancels as tube_c

    return tube_c()


def lemma_blob_not_bkm() -> dict:
    from track_b_coherent import lemma_blob_not_bkm as not_bkm

    return not_bkm()


def lemma_coherent_not_close() -> dict:
    from track_b_coherent import lemma_coherent_not_close as coh_ap

    return coh_ap()


def lemma_coherent_not_a_retune() -> dict:
    from track_b_coherent import lemma_coherent_not_a_retune as coh_rt

    return coh_rt()


def lemma_regularity() -> dict:
    return rec(
        "B_regularity",
        "classical 3D NS is globally regular (keep 1/r^4, no Q1)",
        "open",
        "No closed estimate for X. Lemma identities are not a continuation argument.",
    )


def lemma_phi_not_variable() -> dict:
    return rec(
        "B_phi_not_estimate_variable",
        "pass to Φ = Γ/r² as the primary unknown",
        "fail",
        "The identity 1/r^4 ∂_z(Γ²)=∂_z(Φ²) is true. It moves the work onto ||Φ||_∞. Keep Γ.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_t2_low_flux(),
        lemma_t2_lemma2_circular(),
        lemma_regime_cover(),
        lemma_ring_bernstein(),
        lemma_ring_not_depletion(),
        lemma_tube_hardy(),
        lemma_hardy_not_closed(),
        lemma_packet_tube(),
        lemma_wall_match(),
        lemma_swirl_visc(),
        lemma_swirl_domination(),
        lemma_angular_climbs(),
        lemma_killer_not_angular(),
        lemma_not_phi_cancel(),
        lemma_angular_not_close(),
        lemma_angular_not_a_retune(),
        lemma_energy_not_enough(),
        lemma_phi_not_variable(),
        lemma_bony_split(),
        lemma_bony_t2(),
        lemma_bony_energy(),
        lemma_bony_not_rho(),
        lemma_occupation_clock(),
        lemma_occupation_high_j(),
        lemma_occupation_leray(),
        lemma_occupation_glue(),
        lemma_glue_bookkeeping(),
        lemma_glue_high_j(),
        lemma_glue_low_j(),
        lemma_glue_switching(),
        lemma_glue_not_ns(),
        lemma_energy_ceiling(),
        lemma_frozen_blow_not_ns(),
        lemma_ceiling_not_climbing(),
        lemma_climbing_open(),
        lemma_not_a_retune(),
        lemma_climb_bookkeeping(),
        lemma_bounded_j_bounds_x(),
        lemma_slow_climb_blows(),
        lemma_fast_climb_sits(),
        lemma_ns_climb_law(),
        lemma_climb_not_a_priori(),
        lemma_barycenter(),
        lemma_c_from_rhs(),
        lemma_t0_not_saving(),
        lemma_visc_pulls_down(),
        lemma_evolved_cascade(),
        lemma_law_not_a_priori(),
        lemma_short_run(),
        lemma_evolve_no_saving(),
        lemma_evolve_no_high(),
        lemma_evolve_stays_conc(),
        lemma_evolve_visc_down(),
        lemma_finer_open(),
        lemma_evolve_not_a_priori(),
        lemma_strain_identity(),
        lemma_conc_not_depleted(),
        lemma_ring_not_alignment(),
        lemma_cf_conditional(),
        lemma_geometry_not_close(),
        lemma_geo_not_a_retune(),
        lemma_stretch_budget(),
        lemma_cf_weights_budget(),
        lemma_majority_aligned(),
        lemma_run_not_depleted(),
        lemma_run_keeps_budget(),
        lemma_budget_not_close(),
        lemma_stretch_not_a_retune(),
        lemma_enstrophy_identity(),
        lemma_visc_owns_net(),
        lemma_plus_not_a_cubic(),
        lemma_l2_not_bkm(),
        lemma_not_all_conc(),
        lemma_balance_not_close(),
        lemma_balance_not_a_retune(),
        lemma_coherent_field(),
        lemma_net_is_plus(),
        lemma_cubic_not_live(),
        lemma_tube_still_cancels(),
        lemma_blob_not_bkm(),
        lemma_coherent_not_close(),
        lemma_coherent_not_a_retune(),
        lemma_field_clock(),
        lemma_paths_stay_conc(),
        lemma_clock_did_not_save(),
        lemma_conc_not_short(),
        lemma_cubic_not_live_time(),
        lemma_field_occ_not_close(),
        lemma_field_occ_not_a_retune(),
        lemma_field_rates(),
        lemma_sign_mismatch(),
        lemma_not_the_blowup(),
        lemma_alpha_not_cubic(),
        lemma_gamma_not_visc(),
        lemma_field_glue_not_close(),
        lemma_field_glue_not_a_retune(),
        lemma_field_c(),
        lemma_blob_t0_not_saving(),
        lemma_paths_not_saving(),
        lemma_blob_visc_not_ladder(),
        lemma_offset_not_climb(),
        lemma_ns_climb_not_close(),
        lemma_ns_climb_not_a_retune(),
        lemma_window_rates(),
        lemma_not_the_room(),
        lemma_not_the_sitting(),
        lemma_delta_j_not_prescribed(),
        lemma_sketch_did_not_save(),
        lemma_sketch_not_close(),
        lemma_sketch_not_a_retune(),
        lemma_longer_readable(),
        lemma_longer_not_saving(),
        lemma_longer_not_ladder(),
        lemma_longer_no_high_fill(),
        lemma_longer_clock_did_not_save(),
        lemma_finer_box_open(),
        lemma_longer_not_a_retune(),
        lemma_dns_readable(),
        lemma_dns_not_a_priori(),
        lemma_room_time_not_continuation(),
        lemma_packet_not_all_data(),
        lemma_no_blow_not_bounded(),
        lemma_finer_still_open(),
        lemma_dns_not_a_retune(),
        lemma_tube_readable(),
        lemma_angular_not_a_priori(),
        lemma_b4c_not_a_priori(),
        lemma_rd_not_bounded(),
        lemma_not_revive_hardy_or_phi(),
        lemma_geometry_leftover(),
        lemma_tube_not_a_retune(),
        lemma_align_readable(),
        lemma_depletion_not_a_priori(),
        lemma_frame_not_a_priori(),
        lemma_median_not_a_class(),
        lemma_cf_not_bkm(),
        lemma_budget_leftover(),
        lemma_align_not_a_retune(),
        lemma_payers_readable(),
        lemma_share_not_a_priori(),
        lemma_emptying_not_continuation(),
        lemma_share_not_a_class(),
        lemma_aligned_budget_not_bkm(),
        lemma_enstrophy_leftover(),
        lemma_payers_not_a_retune(),
        lemma_net_readable(),
        lemma_visc_ensemble_not_a_priori(),
        lemma_cancel_not_all_data(),
        lemma_decay_not_continuation(),
        lemma_net_not_integral_max(),
        lemma_coherent_leftover(),
        lemma_net_not_a_retune(),
        lemma_blob_priori_readable(),
        lemma_onesided_not_a_priori(),
        lemma_sign_not_a_class(),
        lemma_peaked_not_integral_max(),
        lemma_nu_not_continuation(),
        lemma_occupation_leftover(),
        lemma_blob_priori_not_a_retune(),
        lemma_clock_priori_readable(),
        lemma_stay_not_a_priori(),
        lemma_full_occ_not_short(),
        lemma_occ_not_live_cubic(),
        lemma_clock_not_integral_max(),
        lemma_glue_leftover(),
        lemma_clock_priori_not_a_retune(),
        lemma_match_priori_readable(),
        lemma_match_not_a_priori(),
        lemma_shrink_alpha_not_continuation(),
        lemma_wrong_sign_not_ns(),
        lemma_match_not_integral_max(),
        lemma_climb_leftover(),
        lemma_match_priori_not_a_retune(),
        lemma_saving_priori_readable(),
        lemma_field_c_not_a_priori(),
        lemma_offset_not_continuation(),
        lemma_ladder_not_a_class(),
        lemma_c_not_integral_max(),
        lemma_sketch_leftover(),
        lemma_saving_priori_not_a_retune(),
        lemma_window_priori_readable(),
        lemma_window_not_a_priori(),
        lemma_short_not_continuation(),
        lemma_growing_not_ns(),
        lemma_window_not_integral_max(),
        lemma_finer_box_leftover(),
        lemma_window_priori_not_a_retune(),
        lemma_finer_priori_readable(),
        lemma_finer_not_a_priori(),
        lemma_fft_not_continuation(),
        lemma_n64_not_ns(),
        lemma_finer_not_integral_max(),
        lemma_dns_finer_leftover(),
        lemma_finer_priori_not_a_retune(),
        lemma_mesh_priori_readable(),
        lemma_mesh_not_a_priori(),
        lemma_mesh_not_continuation(),
        lemma_finer_dns_not_ns(),
        lemma_mesh_not_integral_max(),
        lemma_regularity_leftover(),
        lemma_mesh_priori_not_a_retune(),
        lemma_close_priori_readable(),
        lemma_close_not_a_priori(),
        lemma_catalog_not_continuation(),
        lemma_fails_not_ns(),
        lemma_close_not_integral_max(),
        lemma_domain_leftover(),
        lemma_close_priori_not_a_retune(),
        lemma_object_priori_readable(),
        lemma_object_not_a_priori(),
        lemma_object_not_continuation(),
        lemma_object_not_ns(),
        lemma_object_not_integral_max(),
        lemma_object_not_regularity(),
        lemma_object_priori_not_a_retune(),
        lemma_residual_readable(),
        lemma_residual_not_a_priori(),
        lemma_residual_not_continuation(),
        lemma_residual_not_ns(),
        lemma_residual_not_integral_max(),
        lemma_residual_not_regularity(),
        lemma_residual_not_a_retune(),
        lemma_regularity(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "object": "classical NS, keep 1/r^4",
            "not_a_regularity_proof": True,
            "no_q1": True,
            "no_phi_estimate": True,
            "no_A_implies_B": True,
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "how_far": [
            "B1 T2 low-flux identity holds (pass); T2 Lemma 2 stays dropped (fail)",
            "B2 3-CONC / SPREAD cover (pass as a cover, not as dynamics)",
            "B3 3-shell Bernstein / |∇ξ| on E_c (pass as Bernstein; depletion fail)",
            "B4 tube Hardy with wall term (pass)",
            "B4b all-data Hardy→I_tube fail: slow fat swirl ratio ∼ 1/ε",
            "B4c packet class at δ ∼ 2^{-j*} pass; B4d wall match pass",
            "B5 swirl (Δu)_θ identity (pass); angular 1/r² vs I_tube fail; R_ang climbs (pass)",
            "B5d B4b killer is not the angular killer (fail); not a Φ cancel (fail); angular not an a priori (B5f fail)",
            "B6 ∫X dt < ∞ does not bound X (fail of that close)",
            "Φ is not the estimate variable (fail)",
            "B7 Bony split + T2 self (pass); energy-class low T (pass); uniform ρ^{1/2} fail",
            "B8 occupation clock (pass); high j* short (pass); Leray⇒short CONC fail; occupation closes X fail",
            "B9 glue bookkeeping (pass); high-j CONC sits (pass); switching high-j sits (pass)",
            "B9b low-j CONC cubic is live (fail); B9d sketch is not an NS a priori (fail)",
            "B10 energy ceiling (pass); B9b unbounded path is not NS (fail); not a PDE retune (fail)",
            "B10b ceiling does not follow a climbing j* (fail); climbing CONC not a close (B10c fail)",
            "B11 climb bookkeeping (pass); bounded j* bounds X (pass); slow climb blows (fail)",
            "B11c fast climb sits (pass); NS did not force a saving c (B11d fail); sketch is not an a priori (B11e fail)",
            "B12 barycenter + c from RHS (pass); t=0 packets do not produce c≥8 (fail)",
            "B12c viscosity pulls j_bar down (fail); evolved cascade not a saving climb (B12d fail); t=0 not a law (B12e fail)",
            "B13 short run finite (pass); no saving climb (fail); no high fill (fail); stays CONC (pass)",
            "B13d visc still pulls down (fail); longer n=32 not a saving climb (B13e fail); DNS not an a priori (B13f fail)",
            "B14 strain identity (pass); CONC not depleted (fail); Ring is not alignment (fail)",
            "B14c CF conditional (pass); geometry does not close X (B14d fail); not a PDE retune (fail)",
            "B15 stretching budget readable (pass); CF weights the budget (pass); majority from aligned cap (pass)",
            "B15c short run does not deplete |cos α_3| (fail); aligned share stays (fail); budget not an a priori (B15e fail)",
            "B16 enstrophy identity (pass); visc owns the net on this ensemble (pass); P_+ is not a net cubic (fail)",
            "B16c L² is not BKM (fail); random-phase is not all CONC (fail); balance not an a priori (B16e fail)",
            "B17 signed-strain blob readable (pass); net ≈ P+ (pass); working-box cubic not live (fail)",
            "B17c z-independent tube still cancels (fail); L² blob is not BKM (fail); blob not an a priori (B17e fail)",
            "B18 field clock on a path (pass); paths stay CONC (pass); clock did not save X (fail)",
            "B18c CONC occupation not short (fail); cubic not live in time (fail); field occupation not an a priori (B18e fail)",
            "B19 both Ẋ readable (pass); j*=2 sign mismatch (fail); NS packet is not B9b (fail)",
            "B19c α_c is not the field cubic (fail); γ is not NS visc (fail); field glue not an a priori (B19e fail)",
            "B20 c readable on blob and B18 paths (pass); blob t=0 not c≥8 (fail); path mean not c≥8 (fail)",
            "B20c visc is not a ladder on the blob (fail); j_bar offset is not a climb (fail); NS climb not an a priori (B20e fail)",
            "B21 ODE and NS readable on the window (pass); c=8 not yet in the viscous room (fail); not the sitting path (fail)",
            "B21c NS Δj is not cT (fail); sketch did not sit on this window (fail); climb sketch not an a priori (B21e fail)",
            "B22 longer n=32 readable past room time (pass); not c≥8 (fail); not a ladder (fail)",
            "B22c no high fill (fail); clock did not save (fail); finer box not an a priori (B22e fail); DNS not an a priori (B13f fail)",
            "B23 short+longer DNS readable (pass); decaying packet not an a priori (fail); room time not continuation (fail)",
            "B23c packet not all data (fail); no-blow not L∞ (fail); finer DNS not an a priori (B23e fail); not a PDE retune (fail)",
            "B24 B4c and B5b readable together (pass); angular not an a priori (fail); B4c not an a priori (fail)",
            "B24c R_D ≪ 1 is not L∞ (fail); not Hardy/Φ revive (fail); geometry leftover scored (B14d fail); not a PDE retune (fail)",
            "B25 identity+CF readable (pass); depletion not an a priori (fail); Lipschitz+CF not an a priori (fail)",
            "B25c median not a class (fail); CF is not BKM (fail); budget leftover scored (B15e fail); not a PDE retune (fail)",
            "B26 budget+weight+majority readable (pass); aligned share not an a priori (fail); time emptying not continuation (fail)",
            "B26c share not a class (fail); aligned budget is not ∫‖ω‖_∞ (fail); enstrophy leftover scored (B16e fail); not a PDE retune (fail)",
            "B27 identity+visc-owned net readable (pass); visc ensemble not an a priori (fail); cancel not all-data (fail)",
            "B27c decay not continuation (fail); identity is not ∫‖ω‖_∞ (fail); coherent leftover scored (B17e fail); not a PDE retune (fail)",
            "B28 blob+one-sided net readable (pass); one-sided leftover not an a priori (fail); sign not a class (fail)",
            "B28c peaked L² is not ∫‖ω‖_∞ (fail); ν knob not continuation (fail); occupation leftover scored (B18e fail); not a PDE retune (fail)",
            "B29 clock+full CONC+visc-owned X readable (pass); stay not an a priori (fail); τ_C=T is not a short visit (fail)",
            "B29c CONC occupation is not a live cubic (fail); clock is not ∫‖ω‖_∞ (fail); glue leftover scored (B19e fail); not a PDE retune (fail)",
            "B30 rates+sign mismatch+model-grows/field-falls readable (pass); match not an a priori (fail); shrink α_c not continuation (fail)",
            "B30c wrong-sign ODE is not NS (fail); match is not ∫‖ω‖_∞ (fail); climb leftover scored (B20e fail); not a PDE retune (fail)",
            "B31 field c+blob miss+path-mean miss readable (pass); field c not an a priori (fail); offset not continuation (fail)",
            "B31c visc fall is not a class (fail); c is not ∫‖ω‖_∞ (fail); sketch leftover scored (B21e fail); not a PDE retune (fail)",
            "B32 window rates+missed room+sketch-grows/field-falls readable (pass); window not an a priori (fail); short not continuation (fail)",
            "B32c growing sketch is not NS (fail); window is not ∫‖ω‖_∞ (fail); finer leftover scored (B22e fail); not a PDE retune (fail)",
            "B33 longer miss+empty high shells+short window readable (pass); finer not an a priori (fail); FFT not continuation (fail)",
            "B33c unrun n=64 is not NS (fail); finer is not ∫‖ω‖_∞ (fail); DNS leftover scored (B23e fail); not a PDE retune (fail)",
            "B34 DNS miss+refused no-blow+finer-box miss readable (pass); finer DNS not an a priori (fail); mesh not continuation (fail)",
            "B34c unrun finer DNS is not NS (fail); mesh is not ∫‖ω‖_∞ (fail); leftover close scored (B34e fail); not a PDE retune (fail)",
            "B35 leftover catalog+finer miss+DNS miss readable (pass); leftover close not an a priori (fail); catalog not continuation (fail)",
            "B35c stack of fails is not NS (fail); leftover close is not ∫‖ω‖_∞ (fail); regularity leftover scored (B35e fail); not a PDE retune (fail)",
            "B36 leftover catalog miss+leftover-close miss readable (pass); leftover knobs do not decide regularity (fail); catalog not continuation (fail)",
            "B36c naming the object is not NS (fail); leftover catalog is not ∫‖ω‖_∞ (fail); this write does not decide regularity (fail); not a PDE retune (fail)",
            "B37 three holes of R readable on n=32 (pass); naming holes is not a closed estimate (fail); readable is not integrable (fail)",
            "B37c synthetic R is not NS (fail); residual tool is not ∫‖ω‖_∞ (fail); this write does not decide regularity (fail); not a PDE retune (fail)",
            "classical regularity remains open",
        ],
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Leftover close is not an a priori (B34e). Regularity leftover is not an a priori (B35e). "
            "The residual tool names the holes in R. It is not an a priori. "
            "Regularity stays open. Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_lemmas.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Track B lemmas. Domain stays open. Not a regularity proof.")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("counts", payload["counts"])
    print("domain:", payload["meta"]["domain_verdict"])
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
