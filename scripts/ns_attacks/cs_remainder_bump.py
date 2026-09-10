#!/usr/bin/env python3
"""CS remainder ||A^{1/2} B||_2 / √(E Y) on 3D concentrated bumps.

N-shell R★ saturated. Target A stays plausible on that family.
This script tests the leftover door: whether
    ||A^{1/2} B(v,v)||_2 ≤ C √(E Y)
holds, which would close ★ via |T_c| ≤ √D_s ||A^{1/2} B||.

FFT Galerkin on T³. Not a plate. NS not solved.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "cs_remainder_bump"


def _wave_numbers(n: int) -> np.ndarray:
    """Integer frequencies for an n-point periodic FFT (fftshifted)."""
    return np.fft.fftfreq(n, d=1.0 / n).astype(np.int64)


def spectral_curl(psi: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """v = curl ψ on the FFT grid. psi shape (3, n, n, n), complex spectral."""
    n = psi.shape[-1]
    k1d = _wave_numbers(n)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing="ij")
    kx = kx.astype(np.float64)
    ky = ky.astype(np.float64)
    kz = kz.astype(np.float64)
    vx = 1j * (ky * psi[2] - kz * psi[1])
    vy = 1j * (kz * psi[0] - kx * psi[2])
    vz = 1j * (kx * psi[1] - ky * psi[0])
    # kill k=0
    vx[0, 0, 0] = 0.0
    vy[0, 0, 0] = 0.0
    vz[0, 0, 0] = 0.0
    return vx, vy, vz


def leray_hat(vx, vy, vz):
    n = vx.shape[0]
    k1d = _wave_numbers(n).astype(np.float64)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k2[0, 0, 0] = 1.0
    div = kx * vx + ky * vy + kz * vz
    vx = vx - kx * div / k2
    vy = vy - ky * div / k2
    vz = vz - kz * div / k2
    vx[0, 0, 0] = 0.0
    vy[0, 0, 0] = 0.0
    vz[0, 0, 0] = 0.0
    return vx, vy, vz


def moments_hat(vx, vy, vz) -> Dict[str, float]:
    n = vx.shape[0]
    k1d = _wave_numbers(n).astype(np.float64)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing="ij")
    lam = kx * kx + ky * ky + kz * kz
    amp2 = (np.abs(vx) ** 2 + np.abs(vy) ** 2 + np.abs(vz) ** 2).real
    E = float(amp2.sum())
    X = float((lam * amp2).sum())
    Y = float((lam * lam * amp2).sum())
    Z = float((lam ** 3 * amp2).sum())
    Lam = Y / X if X > 0 else float("nan")
    Ds = Z - Lam * Y if X > 0 else float("nan")
    return {"E": E, "X": X, "Y": Y, "Z": Z, "Lambda": Lam, "Ds": Ds}


def bilinear_B(vx, vy, vz):
    """B = P((v·∇)v) from spectral v. Spectral derivatives, real-space product."""
    n = vx.shape[0]
    k1d = _wave_numbers(n).astype(np.float64)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing="ij")
    # physical fields (orthonormal Fourier: Parseval = sum |hat|^2)
    ux = np.fft.ifftn(vx).real
    uy = np.fft.ifftn(vy).real
    uz = np.fft.ifftn(vz).real
    # ∇u via spectral; ifft of i k û
    dux_dx = np.fft.ifftn(1j * kx * vx).real
    dux_dy = np.fft.ifftn(1j * ky * vx).real
    dux_dz = np.fft.ifftn(1j * kz * vx).real
    duy_dx = np.fft.ifftn(1j * kx * vy).real
    duy_dy = np.fft.ifftn(1j * ky * vy).real
    duy_dz = np.fft.ifftn(1j * kz * vy).real
    duz_dx = np.fft.ifftn(1j * kx * vz).real
    duz_dy = np.fft.ifftn(1j * ky * vz).real
    duz_dz = np.fft.ifftn(1j * kz * vz).real
    # (u·∇)u. Math convention u = Σ û_k e^{ik·x}:
    # ifft(û) = u/n³, so the product of iffts is short by n⁶,
    # and fftn of a physical field is n³ times the math coefficient.
    # Net: (u·∇)u_hat = n³ fftn(ifft(û) * ifft(ik û)).
    n3 = float(n) ** 3
    advx = n3 * (ux * dux_dx + uy * dux_dy + uz * dux_dz)
    advy = n3 * (ux * duy_dx + uy * duy_dy + uz * duy_dz)
    advz = n3 * (ux * duz_dx + uy * duz_dy + uz * duz_dz)
    bx = np.fft.fftn(advx)
    by = np.fft.fftn(advy)
    bz = np.fft.fftn(advz)
    return leray_hat(bx, by, bz)


def probe_hat(vx, vy, vz) -> Dict[str, float]:
    m = moments_hat(vx, vy, vz)
    bx, by, bz = bilinear_B(vx, vy, vz)
    n = vx.shape[0]
    k1d = _wave_numbers(n).astype(np.float64)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing="ij")
    lam = kx * kx + ky * ky + kz * kz
    b2 = (np.abs(bx) ** 2 + np.abs(by) ** 2 + np.abs(bz) ** 2).real
    AhalfB2 = float((lam * b2).sum())
    AhalfB = math.sqrt(max(AhalfB2, 0.0))
    # T_k = -Re(B_k · conj(v_k)); N = sum λ T, M = sum λ² T
    ip = (bx * np.conjugate(vx) + by * np.conjugate(vy) + bz * np.conjugate(vz)).real
    Tk = -ip
    N = float((lam * Tk).sum())
    M = float((lam * lam * Tk).sum())
    Tc = M - m["Lambda"] * N
    E, Y, Ds = m["E"], m["Y"], m["Ds"]
    cs = AhalfB / math.sqrt(E * Y) if E > 0 and Y > 0 else float("nan")
    tc_plus = max(Tc, 0.0)
    R = (tc_plus ** 2) / (Ds * E * Y) if Ds > 1e-14 and E > 0 and Y > 0 else 0.0
    R_abs = (Tc ** 2) / (Ds * E * Y) if Ds > 1e-14 and E > 0 and Y > 0 else 0.0
    return {
        **m,
        "AhalfB": AhalfB,
        "cs_ratio": cs,
        "T_c": Tc,
        "R_star": R,
        "R_star_signed": R_abs,
        "kmax": int(k1d.max()),
        "n_grid": n,
    }


def normalize(vx, vy, vz):
    E = float((np.abs(vx) ** 2 + np.abs(vy) ** 2 + np.abs(vz) ** 2).real.sum())
    s = 1.0 / math.sqrt(E)
    return vx * s, vy * s, vz * s


def curl_gaussian(n: int, width: float, axis: Tuple[float, float, float] = (0.0, 0.0, 1.0)):
    """v = curl( G_width(x) e ). Spatial Gaussian width ~ 1/width in frequency."""
    k1d = _wave_numbers(n).astype(np.float64)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    g = np.exp(-k2 / (2.0 * width * width))
    psi = np.stack([g * axis[0], g * axis[1], g * axis[2]], axis=0)
    vx, vy, vz = spectral_curl(psi)
    return normalize(vx, vy, vz)


def modulated_curl_packet(n: int, lam: int, width: float):
    """Frequency blob of width `width` centered at (lam, 0, 0): LP bump.
    v = curl( e^{i λ x_1} G(x) e_3 ).
    """
    k1d = _wave_numbers(n).astype(np.float64)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing="ij")
    k2c = (kx - lam) ** 2 + ky * ky + kz * kz
    g = np.exp(-k2c / (2.0 * width * width))
    # also the conjugate blob at -λ so the field is real
    k2cn = (kx + lam) ** 2 + ky * ky + kz * kz
    gn = np.exp(-k2cn / (2.0 * width * width))
    psi = np.zeros((3, n, n, n), dtype=np.complex128)
    psi[2] = g + gn
    vx, vy, vz = spectral_curl(psi)
    return normalize(vx, vy, vz)


def aligned_ball(n: int, radius: float, seed: Tuple[float, float, float] = (0.2, 0.7, 1.0)):
    """Every mode with |k| ≤ radius, polarization P_k(e). Focuses at the origin."""
    k1d = _wave_numbers(n).astype(np.float64)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing="ij")
    rad = np.sqrt(kx * kx + ky * ky + kz * kz)
    mask = (rad <= radius) & (rad > 0)
    e = np.array(seed, dtype=np.float64)
    vx = np.where(mask, e[0], 0.0).astype(np.complex128)
    vy = np.where(mask, e[1], 0.0).astype(np.complex128)
    vz = np.where(mask, e[2], 0.0).astype(np.complex128)
    vx, vy, vz = leray_hat(vx, vy, vz)
    return normalize(vx, vy, vz)


def localized_abc(n: int, width: float, k0: int):
    """ABC truncated by a spatial Gaussian of frequency-width `width`."""
    k1d = _wave_numbers(n).astype(np.float64)
    kx, ky, kz = np.meshgrid(k1d, k1d, k1d, indexing="ij")
    g = np.exp(-(kx * kx + ky * ky + kz * kz) / (2.0 * width * width))
    # ABC modes at ±k0 along each axis, then multiply by Gaussian in space
    # = convolve ABC spectrum with g. ABC spectrum is six points; we
    # just window a fat ABC in frequency by taking those six and
    # spreading them with g (product in space = convolution in k).
    vx = np.zeros((n, n, n), dtype=np.complex128)
    vy = np.zeros_like(vx)
    vz = np.zeros_like(vx)
    # A sin(k0 z) + C cos(k0 y)  etc. Use complex exponentials.
    # Standard ABC: (A sin z + C cos y, B sin x + A cos z, C sin y + B cos x)
    # Put A=B=C=1, frequency k0.
    def add(dest, k, amp):
        i, j, l = (int(k[0]) % n, int(k[1]) % n, int(k[2]) % n)
        dest[i, j, l] += amp

    # sin(k0 z) = (e^{ik0 z} - e^{-ik0 z}) / (2i)
    add(vx, (0, 0, k0), 1.0 / (2j))
    add(vx, (0, 0, -k0), -1.0 / (2j))
    add(vx, (0, k0, 0), 0.5)
    add(vx, (0, -k0, 0), 0.5)
    add(vy, (k0, 0, 0), 1.0 / (2j))
    add(vy, (-k0, 0, 0), -1.0 / (2j))
    add(vy, (0, 0, k0), 0.5)
    add(vy, (0, 0, -k0), 0.5)
    add(vz, (0, k0, 0), 1.0 / (2j))
    add(vz, (0, -k0, 0), -1.0 / (2j))
    add(vz, (k0, 0, 0), 0.5)
    add(vz, (-k0, 0, 0), 0.5)
    # spatial Gaussian window = convolve spectrum with g
    vx = np.fft.fftn(np.fft.ifftn(vx).real * np.fft.ifftn(g).real)
    vy = np.fft.fftn(np.fft.ifftn(vy).real * np.fft.ifftn(g).real)
    vz = np.fft.fftn(np.fft.ifftn(vz).real * np.fft.ifftn(g).real)
    vx, vy, vz = leray_hat(vx, vy, vz)
    return normalize(vx, vy, vz)


def _triad_crosscheck() -> dict:
    """Match stokes_moments.probe on a two-mode field placed on an FFT grid."""
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from ns_attacks.stokes_moments import (  # noqa: WPS433
        enforce_reality,
        make_divfree_amp,
        probe,
    )

    field = {}
    k0 = (1, 0, 0)
    k1 = (0, 1, 0)
    field[k0] = make_divfree_amp(k0, (0.0, 1.0, 0.3))
    field[k1] = 0.4 * make_divfree_amp(k1, (1.0, 0.0, 0.2))
    field = enforce_reality(field)
    exact = probe(field)
    n = 32
    vx = np.zeros((n, n, n), dtype=np.complex128)
    vy = np.zeros_like(vx)
    vz = np.zeros_like(vx)
    for k, vec in field.items():
        idx = (k[0] % n, k[1] % n, k[2] % n)
        vx[idx] += vec[0]
        vy[idx] += vec[1]
        vz[idx] += vec[2]
    fft = probe_hat(vx, vy, vz)
    return {
        "E_err": abs(fft["E"] - exact.E),
        "Y_err": abs(fft["Y"] - exact.Y),
        "Tc_err": abs(fft["T_c"] - exact.Tc),
        "Ds_err": abs(fft["Ds"] - exact.Ds),
        "exact_R": exact.ratio_box,
        "fft_R": fft["R_star"],
    }


def run() -> dict:
    check = _triad_crosscheck()
    print("crosscheck", json.dumps(check), flush=True)
    if check["Tc_err"] > 1e-8 or check["E_err"] > 1e-10:
        raise RuntimeError(f"FFT convention failed triad cross-check: {check}")
    rows: List[dict] = []

    def record(name: str, scale: int, vx, vy, vz):
        p = probe_hat(vx, vy, vz)
        rec = {"family": name, "scale": scale, **p}
        rows.append(rec)
        print(
            f"{name:18} λ={scale:<3} n={p['n_grid']:<3}  "
            f"CS={p['cs_ratio']:.4f}  R★={p['R_star']:.4f}  "
            f"R_signed={p['R_star_signed']:.4f}  "
            f"T_c={p['T_c']:+.4e}  Ds={p['Ds']:.4e}",
            flush=True,
        )
        return rec

    # Curl-Gaussian spatial bumps. Frequency width = scale.
    # Products reach ~6λ; keep n > 12λ to avoid wrap.
    for lam in (2, 3, 4, 5, 6, 8):
        n = max(32, 12 * lam)
        if n % 2:
            n += 1
        vx, vy, vz = curl_gaussian(n, width=float(lam), axis=(0.2, 0.5, 1.0))
        record("curl_gaussian", lam, vx, vy, vz)

    # LP packets: blob width ~ lam/3 centered at frequency lam.
    for lam in (3, 4, 5, 6, 8):
        n = max(32, 12 * lam)
        if n % 2:
            n += 1
        w = max(lam / 3.0, 1.0)
        vx, vy, vz = modulated_curl_packet(n, lam=lam, width=w)
        record("lp_packet", lam, vx, vy, vz)

    # Localized ABC: carrier k0=scale, envelope width = scale.
    # 16λ matched 24λ on λ≤5; keep that grid.
    for lam in (2, 3, 4, 5, 6, 8):
        n = max(48, 16 * lam)
        if n % 2:
            n += 1
        vx, vy, vz = localized_abc(n, width=float(lam), k0=lam)
        record("local_abc", lam, vx, vy, vz)

    # Phase-aligned Fourier ball (spatial focus at 0).
    for lam in (2, 3, 4, 5, 6, 8):
        n = max(32, 12 * lam)
        if n % 2:
            n += 1
        vx, vy, vz = aligned_ball(n, radius=float(lam), seed=(0.2, 0.7, 1.0))
        record("aligned_ball", lam, vx, vy, vz)

    def family_climb(name: str) -> dict:
        block = [r for r in rows if r["family"] == name]
        cs = [r["cs_ratio"] for r in block]
        Rs = [r["R_star_signed"] for r in block]
        climb_cs = bool(len(cs) >= 3 and cs[-1] > 1.35 * max(cs[0], 1e-12) and cs[-1] >= 0.9 * max(cs))
        climb_R = bool(len(Rs) >= 3 and Rs[-1] > 1.35 * max(Rs[0], 1e-12) and Rs[-1] >= 0.9 * max(Rs))
        return {
            "cs": cs,
            "R_signed": Rs,
            "climb_cs": climb_cs,
            "climb_R": climb_R,
            "max_cs": max(cs) if cs else None,
            "max_R": max(Rs) if Rs else None,
        }

    by = {
        name: family_climb(name)
        for name in ("curl_gaussian", "lp_packet", "local_abc", "aligned_ball")
    }
    climbs_cs = any(v["climb_cs"] for v in by.values())
    climbs_R = any(v["climb_R"] for v in by.values())
    best_cs = max(rows, key=lambda r: r["cs_ratio"])
    return {
        "ns_solved": False,
        "lemma_star": "OPEN",
        "target": "||A^{1/2} B||_2 <= C sqrt(E Y)",
        "rows": rows,
        "by_family": by,
        "climbs_cs": climbs_cs,
        "climbs_R_star": climbs_R,
        "best_cs": {
            "family": best_cs["family"],
            "scale": best_cs["scale"],
            "cs_ratio": best_cs["cs_ratio"],
            "R_star_signed": best_cs["R_star_signed"],
        },
        "counterexample_field": (
            "v_λ = −P(γ_λ ABC_λ) / ||P(γ_λ ABC_λ)||_2, "
            "ABC_λ the ABC flow at frequency λ, "
            "γ_λ the periodic Gaussian with γ̂_λ(k)=exp(−|k|²/(2λ²)). "
            "Sign so T_c>0 (the computed field has T_c<0)."
        ),
        "verdict": (
            "Target A false: R★ ~ c λ³ on reversed localized ABC. "
            "CS remainder also false: ||A^{1/2}B||/√(EY) ~ c' λ^{3/2}."
            if climbs_R
            else (
                "CS remainder false: ||A^{1/2}B||/√(EY) climbs on a 3D bump. "
                "R★ not killed on these bumps."
                if climbs_cs
                else "CS remainder not killed on these bumps. Not a proof."
            )
        ),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    payload = run()
    (OUT / "cs_remainder.json").write_text(json.dumps(payload, indent=2))
    print("climbs_cs", payload["climbs_cs"], "climbs_R", payload["climbs_R_star"])
    print("verdict", payload["verdict"])


if __name__ == "__main__":
    main()
