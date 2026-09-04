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
    return rec(
        "B5b_tube_vs_viscosity",
        "angular 1/r² viscosity dominates I_tube at δ ~ 2^{-j*}",
        "open",
        "This is the reason to keep 1/r^4. Not shown. Do not cancel to Φ to escape it.",
    )


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
            "B5 swirl (Δu)_θ identity (pass); viscosity vs I_tube still open",
            "B6 ∫X dt < ∞ does not bound X (fail of that close)",
            "Φ is not the estimate variable (fail)",
            "B7 Bony split + T2 self (pass); energy-class low T (pass); uniform ρ^{1/2} fail",
            "B8 occupation clock (pass); high j* short (pass); Leray⇒short CONC fail; glue to X open",
            "B9 glue bookkeeping (pass); high-j CONC sits (pass); switching high-j sits (pass)",
            "B9b low-j CONC cubic is live (fail); B9d sketch is not an NS a priori (open)",
            "classical regularity remains open",
        ],
        "next_da_move": (
            "Low-j_* CONC is the remaining cubic (B9b). Either coarse packets "
            "cannot stay CONC, or the cubic is bounded when j_* is small. "
            "Tesla: that is the paragraph."
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
