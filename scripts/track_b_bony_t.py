#!/usr/bin/env python3
"""
Energy-class low Bony T on T^3.

T2 Lemma 1 kills (u_low · ∇) u_j · u_j. What remains is low
velocity feeding neighboring shells into Π_j. Spread does not
give a uniform ρ^{1/2} L^∞ bound on the low sum as ρ → 0.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from track_b_lemmas import convect, ifft, make_grid, mask_band, project, rec


def random_shell(n: int, j: int, rng: np.random.Generator, amplitude: float = 1.0):
    kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
    shape = (n, n, n)
    band = mask_band(k2, 2.0 ** (j - 1), 2.0**j) & dealias
    uh = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * band
    vh = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * band
    wh = (rng.normal(size=shape) + 1j * rng.normal(size=shape)) * band
    uh, vh, wh = project(uh, vh, wh, kx, ky, kz, k2_safe)
    # normalize X_j = 2^{2j} ||u_j||_2^2 ~ amplitude
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    vol = (2.0 * math.pi) ** 3
    l2 = math.sqrt(float(np.mean(u * u + v * v + w * w)) * vol)
    target = math.sqrt(max(amplitude, 1e-30)) / max(2.0**j, 1.0)
    scale = target / max(l2, 1e-30)
    return uh * scale, vh * scale, wh * scale, kx, ky, kz, k2, k2_safe


def add_shells(pieces):
    uh = vh = wh = None
    kx = ky = kz = k2 = k2_safe = None
    for piece in pieces:
        pu, pv, pw, kx, ky, kz, k2, k2_safe = piece
        uh = pu if uh is None else uh + pu
        vh = pv if vh is None else vh + pv
        wh = pw if wh is None else wh + pw
    return uh, vh, wh, kx, ky, kz, k2, k2_safe


def flux(u, v, w, uh, vh, wh, u_j, v_j, w_j, kx, ky, kz) -> float:
    cu, cv, cw = convect(u, v, w, uh, vh, wh, kx, ky, kz)
    vol = (2.0 * math.pi) ** 3
    return float(np.mean(cu * u_j + cv * v_j + cw * w_j)) * vol


def linf(u, v, w) -> float:
    return float(np.max(np.sqrt(u * u + v * v + w * w)))


def enstrophy_of(uh, vh, wh, kx, ky, kz, k2) -> float:
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    vol = (2.0 * math.pi) ** 3
    # X ≈ ||∇u||_2^2 via Fourier
    ux = ifft(1j * kx * uh)
    uy = ifft(1j * ky * uh)
    uz = ifft(1j * kz * uh)
    vx = ifft(1j * kx * vh)
    vy = ifft(1j * ky * vh)
    vz = ifft(1j * kz * vh)
    wx = ifft(1j * kx * wh)
    wy = ifft(1j * ky * wh)
    wz = ifft(1j * kz * wh)
    return float(
        np.mean(
            ux * ux
            + uy * uy
            + uz * uz
            + vx * vx
            + vy * vy
            + vz * vz
            + wx * wx
            + wy * wy
            + wz * wz
        )
        * vol
    )


def split_flux(n: int = 32, j: int = 4, nsep: int = 3, seed: int = 7) -> dict:
    rng = np.random.default_rng(seed)
    pieces = [random_shell(n, k, rng, amplitude=1.0) for k in range(1, j + 3)]
    uh, vh, wh, kx, ky, kz, k2, k2_safe = add_shells(pieces)
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    band_j = mask_band(k2, 2.0 ** (j - 1), 2.0**j)
    low = mask_band(k2, -0.5, 2.0 ** (j - nsep))
    near = mask_band(k2, 2.0 ** (j - nsep), 2.0 ** (j + nsep)) & (~band_j)
    high = ~(low | near | band_j)
    u_j, v_j, w_j = ifft(uh * band_j), ifft(vh * band_j), ifft(wh * band_j)
    parts = {}
    for name, mask in (("full", None), ("T", low), ("R_near", near), ("self", band_j), ("Tstar", high)):
        if mask is None:
            pu, pv, pw = uh, vh, wh
        else:
            pu, pv, pw = uh * mask, vh * mask, wh * mask
        p_u, p_v, p_w = ifft(pu), ifft(pv), ifft(pw)
        parts[name] = flux(p_u, p_v, p_w, uh, vh, wh, u_j, v_j, w_j, kx, ky, kz)
    # T2 Lemma 1: low-or-equal velocity advecting the peak, paired with the peak.
    u_leq, v_leq, w_leq = ifft(uh * (low | band_j)), ifft(vh * (low | band_j)), ifft(wh * (low | band_j))
    parts["t2_self"] = flux(
        u_leq, v_leq, w_leq, uh * band_j, vh * band_j, wh * band_j, u_j, v_j, w_j, kx, ky, kz
    )
    residual = parts["full"] - (parts["T"] + parts["R_near"] + parts["self"] + parts["Tstar"])
    energy_j = float(np.mean(u_j * u_j + v_j * v_j + w_j * w_j)) * (2.0 * math.pi) ** 3
    return {
        "parts": parts,
        "residual": residual,
        "rel_residual": abs(residual) / max(abs(parts["full"]), energy_j, 1e-30),
        "t2_over_energy": abs(parts["t2_self"]) / max(energy_j, 1e-30),
        "n": n,
        "j": j,
        "nsep": nsep,
    }


def plane_wave(n: int, kvec, amplitude: float):
    """Div-free plane wave, aligned so L^∞ adds at the origin."""
    kx, ky, kz, k2, k2_safe, _ = make_grid(n)
    uh = np.zeros((n, n, n), dtype=complex)
    vh = np.zeros_like(uh)
    wh = np.zeros_like(uh)
    kx0, ky0, kz0 = (int(x) for x in kvec)
    # polarization ⟂ k
    if abs(kz0) + abs(ky0) == 0:
        pol = (0.0, 1.0, 0.0)
    else:
        pol = (0.0, -float(kz0), float(ky0))
    pn = math.sqrt(pol[0] ** 2 + pol[1] ** 2 + pol[2] ** 2) or 1.0
    uh[kx0, ky0, kz0] = (pol[0] / pn) * n**3 * 0.5
    vh[kx0, ky0, kz0] = (pol[1] / pn) * n**3 * 0.5
    wh[kx0, ky0, kz0] = (pol[2] / pn) * n**3 * 0.5
    uh[-kx0, -ky0, -kz0] = np.conj(uh[kx0, ky0, kz0])
    vh[-kx0, -ky0, -kz0] = np.conj(vh[kx0, ky0, kz0])
    wh[-kx0, -ky0, -kz0] = np.conj(wh[kx0, ky0, kz0])
    uh, vh, wh = project(uh, vh, wh, kx, ky, kz, k2_safe)
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    vol = (2.0 * math.pi) ** 3
    l2 = math.sqrt(float(np.mean(u * u + v * v + w * w)) * vol)
    scale = math.sqrt(max(amplitude, 1e-30)) / max(l2, 1e-30)
    return uh * scale, vh * scale, wh * scale, kx, ky, kz, k2, k2_safe


def spread_stack(n: int, j: int, nsep: int, n_low: int, rng: np.random.Generator):
    """n_low aligned low plane waves plus a random peak shell."""
    kmax = max(int(2.0 ** (j - nsep)) - 1, 1)
    ks = []
    m = 1
    while len(ks) < n_low and m <= kmax:
        ks.append((m, 0, 0))
        m += 1
    if not ks:
        ks = [(1, 0, 0)]
    amp = 1.0
    pieces = [plane_wave(n, kv, amp) for kv in ks]
    pieces.append(random_shell(n, j, rng, amplitude=amp))
    if j >= 2:
        pieces.append(random_shell(n, j - 1, rng, amplitude=amp))
    uh, vh, wh, kx, ky, kz, k2, _ = add_shells(pieces)
    return uh, vh, wh, kx, ky, kz, k2, ks


def low_T_scan(n: int = 48, j: int = 4, nsep: int = 1, seed: int = 8) -> dict:
    rng = np.random.default_rng(seed)
    rows = []
    for n_low in (1, 2, 4, 6):
        uh, vh, wh, kx, ky, kz, k2, lows = spread_stack(n, j, nsep, n_low, rng)
        u, v, w = ifft(uh), ifft(vh), ifft(wh)
        band_j = mask_band(k2, 2.0 ** (j - 1), 2.0**j)
        low = mask_band(k2, -0.5, 2.0 ** (j - nsep))
        u_j, v_j, w_j = ifft(uh * band_j), ifft(vh * band_j), ifft(wh * band_j)
        u_l, v_l, w_l = ifft(uh * low), ifft(vh * low), ifft(wh * low)
        t_full = flux(u_l, v_l, w_l, uh, vh, wh, u_j, v_j, w_j, kx, ky, kz)
        t_self = flux(u_l, v_l, w_l, uh * band_j, vh * band_j, wh * band_j, u_j, v_j, w_j, kx, ky, kz)
        x = enstrophy_of(uh, vh, wh, kx, ky, kz, k2)
        xj = enstrophy_of(uh * band_j, vh * band_j, wh * band_j, kx, ky, kz, k2)
        rho = xj / max(x, 1e-30)
        # J is max shell; here shells are equal so ρ ≈ 1/(n_low+1)
        sl_inf = linf(u_l, v_l, w_l)
        energy_bound = (2.0 ** ((j - nsep) / 2.0)) * math.sqrt(max(x, 1e-30))
        rho_hope = math.sqrt(max(rho, 1e-30)) * math.sqrt(max(x, 1e-30))
        rows.append(
            {
                "n_low": n_low,
                "n_shells": n_low + 1,
                "rho": rho,
                "T": t_full,
                "T_self": t_self,
                "X": x,
                "Xj": xj,
                "S_low_inf": sl_inf,
                "energy_bound": energy_bound,
                "rho_hope": rho_hope,
                "inf_over_energy": sl_inf / max(energy_bound, 1e-30),
                "inf_over_rho_hope": sl_inf / max(rho_hope, 1e-30),
                "T_over_energy": abs(t_full) / max(energy_bound * math.sqrt(max(xj, 1e-30)), 1e-30),
            }
        )
    inf_ratios = [r["inf_over_rho_hope"] for r in rows]
    energy_ratios = [r["inf_over_energy"] for r in rows]
    return {
        "rows": rows,
        "inf_over_rho_hope": inf_ratios,
        "inf_over_energy": energy_ratios,
        "rho_hope_grows": inf_ratios[-1] > 1.3 * inf_ratios[0],
        "energy_stays": max(energy_ratios) < 8.0,
    }


def lemma_bony_split() -> dict:
    split = split_flux()
    ok = split["rel_residual"] < 1e-8
    return rec(
        "B7_bony_split",
        "Π_j = T + T* + R_near + self for a Bony cut at j−N",
        "pass" if ok else "fail",
        "Bookkeeping identity on T^3. T2 Lemma 1 is the self piece.",
        split=split,
    )


def lemma_self_is_b1() -> dict:
    split = split_flux()
    ok = split["t2_over_energy"] < 1e-8
    return rec(
        "B7a_self_is_t2",
        "∫ (u_≤j · ∇) u_j · u_j = 0 (T2 Lemma 1). That is not the surviving low T.",
        "pass" if ok else "fail",
        "Self-flux of the peak dies. Low T is u_low feeding neighbors into Π_j.",
        t2_over_energy=split["t2_over_energy"],
    )


def lemma_low_T_energy() -> dict:
    scan = low_T_scan()
    return rec(
        "B7b_low_T_energy_class",
        "||u_{≤j−N}||_∞ ≲ 2^{(j−N)/2} X^{1/2} in energy class",
        "pass" if scan["energy_stays"] else "fail",
        "Bernstein + Cauchy–Schwarz on the low sum. No ρ improvement claimed.",
        scan=scan,
    )


def lemma_low_T_not_rho() -> dict:
    scan = low_T_scan()
    return rec(
        "B7c_low_T_not_rho_uniform",
        "spread ⇒ ||u_{≤j−N}||_∞ ≲ ρ^{1/2} X^{1/2} uniformly as ρ → 0",
        "fail" if scan["rho_hope_grows"] else "open",
        "Each low shell is ≤ ρ X. The sum in L^∞ is not. CCFS does not give G its ρ^{1/2}.",
        scan=scan,
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_bony_split(),
        lemma_self_is_b1(),
        lemma_low_T_energy(),
        lemma_low_T_not_rho(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "energy-class low Bony T",
            "regime": "SPREAD",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "H at frozen ρ ≤ 1/4 may still be written with the energy-class T. "
            "G (push out of deep SPREAD) is dead. Occupation time is next."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_bony_t.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Low Bony T. Energy class vs uniform ρ^{1/2}.")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
