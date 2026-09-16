"""B★ second pass: keep T_c as one pairing; triad identity; harder families.

Prove or disprove
  [T_c]_+ ≤ C X Λ^{1/2} D_s^{1/2}
by (1) writing the centered identity, (2) attacking with spectra the
first hunt never reached (power-law, lacunary, tube, ascent).
Not a close. ★ stays killed. Do not overwrite stokes_moments.py.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from stokes_moments import (  # noqa: E402
    enforce_reality,
    high_triad_field,
    k_norm2,
    leray_project,
    make_divfree_amp,
    nonlinear_B,
    probe,
)

from bstar_attack import score, separated_triad  # noqa: E402


def finite(x: float) -> bool:
    return x == x and abs(x) < 1e300


def omega_hat(k, uk: np.ndarray) -> np.ndarray:
    """ω̂_k = i k × û_k."""
    return 1j * np.cross(np.array(k, dtype=np.float64), uk)


def lamb_stretch_pairing(field: dict) -> dict:
    """T_c as one pairing: ⟨(u·∇)ω − (ω·∇)u, (A−Λ)ω⟩.

    Exact Fourier: L̂_k = i Σ_{p+q=k} [(û_p·q) ω̂_q − (ω̂_p·q) û_q].
    Then ⟨L,(A−Λ)ω⟩ = Σ_k L̂_k · conj((λ_k−Λ) ω̂_k).
    Sign is locked by matching probe().Tc on a triad.
    """
    field = enforce_reality(field)
    pr = probe(field)
    keys = list(field.keys())
    L: dict = {}
    for p in keys:
        up = field[p]
        wp = omega_hat(p, up)
        for q in keys:
            uq = field[q]
            wq = omega_hat(q, uq)
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            qv = np.array(q, dtype=np.float64)
            contrib = 1j * (np.dot(up, qv) * wq - np.dot(wp, qv) * uq)
            L[k] = L.get(k, np.zeros(3, dtype=np.complex128)) + contrib
    lam = pr.Lambda
    pairing = 0.0 + 0.0j
    l2 = 0.0
    ds_from_omega = 0.0
    for k, lk in L.items():
        kn2 = k_norm2(k)
        if kn2 == 0:
            continue
        uk = field.get(k, np.zeros(3, dtype=np.complex128))
        wk = omega_hat(k, uk)
        pairing += np.vdot((kn2 - lam) * wk, lk)
        l2 += float(np.vdot(lk, lk).real)
        ds_from_omega += ((kn2 - lam) ** 2) * float(np.vdot(wk, wk).real)
    pairing = -float(pairing.real)
    # Modes in the field with no L still contribute to D_s.
    ds_om = 0.0
    for k, uk in field.items():
        kn2 = k_norm2(k)
        wk = omega_hat(k, uk)
        ds_om += ((kn2 - lam) ** 2) * float(np.vdot(wk, wk).real)
    return {
        "Tc_probe": pr.Tc,
        "pairing": pairing,
        "L2": math.sqrt(max(l2, 0.0)),
        "Ds": pr.Ds,
        "Ds_omega": ds_om,
        "X": pr.X,
        "Y": pr.Y,
        "Lambda": pr.Lambda,
        "R_L": math.sqrt(max(l2, 0.0)) / math.sqrt(pr.X * pr.Y) if pr.X > 0 and pr.Y > 0 else float("nan"),
    }


def perp_basis(k) -> tuple[np.ndarray, np.ndarray]:
    kf = np.array(k, dtype=np.float64)
    nrm = np.linalg.norm(kf)
    if nrm < 1e-15:
        raise ValueError("k=0")
    kh = kf / nrm
    tmp = np.array([1.0, 0.0, 0.0]) if abs(kh[0]) < 0.7 else np.array([0.0, 1.0, 0.0])
    e1 = tmp - np.dot(tmp, kh) * kh
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(kh, e1)
    return e1, e2


def power_law_field(kmax: int, alpha: float, phase: str = "imag") -> dict:
    """û(k) = |k|^{-α} e_⊥(k), reality-safe.

    phase='imag': û = i |k|^{-α} e1, a sine series.
    phase='helix': û = |k|^{-α} (e1 + i e2)/√2.
    """
    field = {}
    for i in range(-kmax, kmax + 1):
        for j in range(-kmax, kmax + 1):
            for k in range(-kmax, kmax + 1):
                kk = (i, j, k)
                if kk == (0, 0, 0):
                    continue
                if kk in field:
                    continue
                kn = math.sqrt(k_norm2(kk))
                amp = kn ** (-alpha)
                e1, e2 = perp_basis(kk)
                if phase == "helix":
                    v = (amp / math.sqrt(2.0)) * (e1 + 1j * e2)
                else:
                    v = 1j * amp * e1
                field[kk] = v.astype(np.complex128)
    return enforce_reality(field)


def lacunary_field(jmax: int, alpha: float = 1.5) -> dict:
    """Dyadic shells |k| ~ 2^j with a closing triad on each scale."""
    field = {}
    for j in range(jmax + 1):
        m = 1 << j
        keys = ((m, 0, 0), (0, m, 0), (m, m, 0))
        seeds = ((0.0, 1.0, 0.2), (1.0, 0.0, 0.3), (0.2, 0.5, 1.0))
        phases = (0.0, 0.5 * math.pi, -0.35)
        amp = float(m) ** (-alpha)
        for k, seed, ph in zip(keys, seeds, phases):
            v = make_divfree_amp(k, seed)
            nrm = np.linalg.norm(v)
            if nrm < 1e-15:
                continue
            field[k] = (amp * np.exp(1j * ph) / nrm) * v
    return enforce_reality(field)


def tube_field(kperp: int, kz_max: int = 2, alpha: float = 1.0) -> dict:
    """Energy on a frequency tube: |k_z|≤kz_max, k_perp up to kperp."""
    field = {}
    for i in range(-kperp, kperp + 1):
        for j in range(-kperp, kperp + 1):
            for kz in range(-kz_max, kz_max + 1):
                k = (i, j, kz)
                if k == (0, 0, 0):
                    continue
                rp = math.sqrt(i * i + j * j)
                if rp < 1e-15:
                    continue
                amp = (rp ** (-alpha)) * math.exp(-0.15 * kz * kz)
                e1, e2 = perp_basis(k)
                # axial vorticity bias
                field[k] = (1j * amp * e1).astype(np.complex128)
    return enforce_reality(field)


def random_power_subset(rng: np.random.Generator, kmax: int, n_modes: int, alpha: float) -> dict:
    candidates = []
    for i in range(-kmax, kmax + 1):
        for j in range(-kmax, kmax + 1):
            for k in range(-kmax, kmax + 1):
                if (i, j, k) != (0, 0, 0) and i >= 0:
                    candidates.append((i, j, k))
    rng.shuffle(candidates)
    field = {}
    for k in candidates[:n_modes]:
        kn = math.sqrt(k_norm2(k))
        amp = kn ** (-alpha)
        e1, e2 = perp_basis(k)
        th = float(rng.uniform(0.0, 2.0 * math.pi))
        ph = float(rng.uniform(0.0, 2.0 * math.pi))
        v = amp * (math.cos(th) * e1 + math.sin(th) * e2) * np.exp(1j * ph)
        field[k] = v.astype(np.complex128)
    return enforce_reality(field)


def fft_probe(field: dict, n: int) -> dict:
    """Dealiased spectral (u·∇)u on an n³ grid. n even, n/2 > 2 kmax."""
    field = enforce_reality(field)
    uhat = np.zeros((3, n, n, n), dtype=np.complex128)
    kmax = 0
    for k, v in field.items():
        kmax = max(kmax, abs(k[0]), abs(k[1]), abs(k[2]))
        ix = tuple(ki % n for ki in k)
        uhat[0][ix] += v[0]
        uhat[1][ix] += v[1]
        uhat[2][ix] += v[2]
    if 2 * kmax >= n // 2:
        raise ValueError(f"grid n={n} too small for kmax={kmax}")
    # physical fields via ifft (û stored as FFT coefficients: u = ifft * n³)
    u = np.fft.ifftn(uhat, axes=(1, 2, 3)) * (n**3)
    # Mode k=(kx,ky,kz) lives at index (kx%n, ky%n, kz%n) on axes (1,2,3).
    kx_g = np.fft.fftfreq(n, d=1.0 / n).astype(np.float64)
    KX, KY, KZ = np.meshgrid(kx_g, kx_g, kx_g, indexing="ij")
    du = []
    for comp in range(3):
        dux = np.fft.ifftn(1j * KX * uhat[comp], axes=(0, 1, 2)) * (n**3)
        duy = np.fft.ifftn(1j * KY * uhat[comp], axes=(0, 1, 2)) * (n**3)
        duz = np.fft.ifftn(1j * KZ * uhat[comp], axes=(0, 1, 2)) * (n**3)
        du.append((dux, duy, duz))
    conv = np.zeros_like(u)
    for i in range(3):
        conv[i] = u[0] * du[i][0] + u[1] * du[i][1] + u[2] * du[i][2]
    Bhat = np.fft.fftn(conv, axes=(1, 2, 3)) / (n**3)
    kn2 = KX * KX + KY * KY + KZ * KZ
    with np.errstate(invalid="ignore", divide="ignore"):
        kdotB = KX * Bhat[0] + KY * Bhat[1] + KZ * Bhat[2]
        proj = np.where(kn2 > 0, kdotB / kn2, 0.0)
    Bhat[0] = Bhat[0] - proj * KX
    Bhat[1] = Bhat[1] - proj * KY
    Bhat[2] = Bhat[2] - proj * KZ
    # pairings from original support only (exact for the cubic if dealiased)
    E = X = Y = Z = N = M = 0.0
    ahalfB2 = 0.0
    for k, v in field.items():
        kn = k_norm2(k)
        amp2 = float(np.vdot(v, v).real)
        E += amp2
        X += kn * amp2
        Y += kn * kn * amp2
        Z += kn * kn * kn * amp2
        ix = tuple(ki % n for ki in k)
        bk = np.array([Bhat[0][ix], Bhat[1][ix], Bhat[2][ix]])
        ip = float(np.vdot(bk, v).real)
        N -= kn * ip
        M -= (kn * kn) * ip
    # L = (ω·∇)u − (u·∇)ω in physical space; R_L = ||L||_2 / √(XY).
    what = np.stack(
        [
            1j * (KY * uhat[2] - KZ * uhat[1]),
            1j * (KZ * uhat[0] - KX * uhat[2]),
            1j * (KX * uhat[1] - KY * uhat[0]),
        ],
        axis=0,
    )
    w = np.fft.ifftn(what, axes=(1, 2, 3)) * (n**3)
    dw = []
    for comp in range(3):
        dwx = np.fft.ifftn(1j * KX * what[comp], axes=(0, 1, 2)) * (n**3)
        dwy = np.fft.ifftn(1j * KY * what[comp], axes=(0, 1, 2)) * (n**3)
        dwz = np.fft.ifftn(1j * KZ * what[comp], axes=(0, 1, 2)) * (n**3)
        dw.append((dwx, dwy, dwz))
    Lphys = np.zeros_like(u)
    for i in range(3):
        Lphys[i] = (
            w[0] * du[i][0]
            + w[1] * du[i][1]
            + w[2] * du[i][2]
            - (u[0] * dw[i][0] + u[1] * dw[i][1] + u[2] * dw[i][2])
        )
    # Parseval: Σ_k |L̂_k|² = (1/n³) Σ_j |L_j|² if L̂ = fft(L)/n³ and L = ifft(n³ L̂)
    L2 = math.sqrt(max(float(np.mean(np.sum(np.abs(Lphys) ** 2, axis=0)).real), 0.0))
    ahalfB2 = float(np.sum(kn2 * np.sum(np.abs(Bhat) ** 2, axis=0)).real)
    Lam = Y / X if X > 0 else float("nan")
    Ds = Z - Lam * Y if X > 0 else float("nan")
    Tc = M - Lam * N
    denom = X * math.sqrt(Lam) * math.sqrt(Ds) if X > 0 and Lam > 0 and Ds > 0 else float("nan")
    RL = L2 / math.sqrt(X * Y) if X > 0 and Y > 0 else float("nan")
    Lam_fourth = (Lam ** 0.25) if Lam == Lam and Lam > 0 else float("nan")
    return {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lam,
        "Ds": Ds,
        "N": N,
        "M": M,
        "Tc": Tc,
        "R_B": abs(Tc) / denom if denom == denom and denom > 0 else float("nan"),
        "AhalfB": math.sqrt(max(ahalfB2, 0.0)),
        "AhalfB_over_sqrtXY": (
            math.sqrt(max(ahalfB2, 0.0)) / math.sqrt(X * Y) if X > 0 and Y > 0 else float("nan")
        ),
        "L2": L2,
        "R_L": RL,
        "Lambda_fourth": Lam_fourth,
        "kmax": kmax,
        "grid": n,
    }


def ascent_rb(seed: dict, steps: int = 40, lr: float = 0.08, rng=None) -> dict:
    """Projected gradient ascent on R_B. Finite-difference, div-free + reality."""
    rng = rng or np.random.default_rng(0)
    field = enforce_reality({k: np.array(v, dtype=np.complex128) for k, v in seed.items()})
    keys = [k for k in field if k < (-k[0], -k[1], -k[2]) or k[0] > 0 or (k[0] == 0 and (k[1] > 0 or (k[1] == 0 and k[2] > 0)))]
    best = score(field, "ascent0")
    cur = best
    eps = 1e-4
    for step in range(steps):
        grad = {}
        base = cur["R_B"]
        if not finite(base):
            break
        for k in keys:
            if k_norm2(k) == 0:
                continue
            e1, e2 = perp_basis(k)
            for vec, tag in ((e1, "1"), (e2, "2")):
                for comp, fac in (("re", 1.0), ("im", 1j)):
                    trial = {kk: vv.copy() for kk, vv in field.items()}
                    trial[k] = trial.get(k, np.zeros(3, dtype=np.complex128)) + eps * fac * vec
                    trial = enforce_reality(trial)
                    row = score(trial, "fd")
                    if finite(row["R_B"]):
                        grad[(k, tag, comp)] = (row["R_B"] - base) / eps
                    else:
                        grad[(k, tag, comp)] = 0.0
        # step
        trial = {kk: vv.copy() for kk, vv in field.items()}
        for (k, tag, comp), g in grad.items():
            e1, e2 = perp_basis(k)
            vec = e1 if tag == "1" else e2
            fac = 1.0 if comp == "re" else 1j
            trial[k] = trial.get(k, np.zeros(3, dtype=np.complex128)) + lr * g * fac * vec
        trial = enforce_reality(trial)
        row = score(trial, f"ascent{step+1}")
        if finite(row["R_B"]) and row["R_B"] > cur["R_B"]:
            field = trial
            cur = row
            if row["R_B"] > best["R_B"]:
                best = row
        else:
            lr *= 0.6
            if lr < 1e-4:
                break
    best["ascent_steps"] = step + 1
    return best


def max_rb(group):
    vals = [r["R_B"] for r in group if finite(r.get("R_B", float("nan")))]
    return max(vals) if vals else float("nan")


def rb_vs_kmax(group, key="kmax"):
    out = {}
    for r in group:
        if key not in r or not finite(r.get("R_B", float("nan"))):
            continue
        k = r[key]
        out[str(k)] = max(out.get(str(k), 0.0), r["R_B"])
    return out


def run() -> dict:
    rows: list[dict] = []
    identities = []

    # --- Identity: triad + vorticity pairing ---
    triad = high_triad_field(amp=1.0)
    ident = lamb_stretch_pairing(triad)
    ident["label"] = "triad_identity"
    identities.append(ident)
    pl = power_law_field(2, 2.5, "helix")
    ident2 = lamb_stretch_pairing(pl)
    ident2["label"] = "power_identity"
    identities.append(ident2)

    # FFT vs exact on the triad
    fft_triad = fft_probe(triad, n=32)
    fft_triad["label"] = "fft_vs_exact_triad"
    exact_triad = score(triad, "exact_triad")
    fft_match = abs(fft_triad["Tc"] - exact_triad["Tc"]) < 1e-8 * max(1.0, abs(exact_triad["Tc"]))

    ident_ok = all(
        abs(r["pairing"] - r["Tc_probe"]) < 1e-8 * max(1.0, abs(r["Tc_probe"]))
        and abs(r["Ds_omega"] - r["Ds"]) < 1e-8 * max(1.0, r["Ds"])
        for r in identities
    )
    print("identities done", ident_ok, "fft_match", fft_match, flush=True)
    power_rows = []
    for alpha in (1.5, 2.0, 2.5, 3.0, 3.5):
        for kmax in (2, 3):
            for phase in ("imag", "helix"):
                field = power_law_field(kmax, alpha, phase)
                row = score(field, f"power_a{alpha}_k{kmax}_{phase}")
                row["alpha"] = alpha
                row["kmax"] = kmax
                rows.append(row)
                power_rows.append(row)

    print("power exact", max_rb(power_rows), flush=True)
    lac_rows = []
    for jmax in (1, 2, 3, 4):
        row = score(lacunary_field(jmax, 1.5), f"lac_j{jmax}")
        rows.append(row)
        lac_rows.append(row)
        row2 = score(lacunary_field(jmax, 0.5), f"lac_flat_j{jmax}")
        rows.append(row2)
        lac_rows.append(row2)

    # --- Vortex-tube spectra ---
    tube_rows = []
    for kp, kz, al in ((3, 1, 1.0), (4, 1, 1.0), (5, 1, 1.2)):
        field = tube_field(kp, kz, al)
        row = score(field, f"tube_kp{kp}_kz{kz}_a{al}")
        rows.append(row)
        tube_rows.append(row)

    # --- Random power-law subsets, larger boxes ---
    rng = np.random.default_rng(20260916)
    rnd_rows = []
    for kmax, n_modes, alpha in (
        (6, 20, 2.5),
        (8, 24, 2.5),
        (8, 24, 3.0),
        (10, 28, 2.5),
        (12, 30, 3.0),
    ):
        field = random_power_subset(rng, kmax, n_modes, alpha)
        row = score(field, f"rpow_k{kmax}_n{n_modes}_a{alpha}")
        rows.append(row)
        rnd_rows.append(row)

    # --- FFT power-law at kmax the O(M²) probe can still do via grid ---
    fft_rows = []
    for alpha in (2.0, 2.5, 3.0, 3.5):
        for kmax in (3, 4, 6, 8):
            for phase in ("imag", "helix"):
                field = power_law_field(kmax, alpha, phase)
                n = 1
                while n < 4 * kmax + 4:
                    n *= 2
                row = fft_probe(field, n=n)
                row["label"] = f"fft_power_a{alpha}_k{kmax}_{phase}"
                row["alpha"] = alpha
                fft_rows.append(row)
                rows.append({**row, "modes": len(field)})
    print(
        "fft power R_B",
        max_rb(fft_rows),
        "R_L_by_k",
        {
            k: max(
                (r["R_L"] for r in fft_rows if str(r.get("kmax")) == k and finite(r.get("R_L", float("nan")))),
                default=float("nan"),
            )
            for k in rb_vs_kmax(fft_rows)
        },
        flush=True,
    )

    # High-kmax imag power-law: the only family whose R_B still rose.
    hi_rows = []
    for kmax in (8, 10, 12, 16):
        field = power_law_field(kmax, 2.0, "imag")
        n = 1
        while n <= 4 * kmax:
            n *= 2
        row = fft_probe(field, n=n)
        row["label"] = f"hi_power_a2_k{kmax}_imag"
        row["alpha"] = 2.0
        hi_rows.append(row)
        rows.append({**row, "modes": len(field)})
        print("hi", row["label"], "R_B", row["R_B"], "R_L", row["R_L"], "Lam", row["Lambda"], flush=True)
    fft_rows.extend(hi_rows)

    # --- Ascent on the local m=1 triad (previous max ~0.095) and a 4-mode seed ---
    ascent_rows = []
    a1 = ascent_rb(high_triad_field(amp=1.0), steps=25, lr=0.12, rng=rng)
    a1["label"] = "ascent_triad"
    ascent_rows.append(a1)
    rows.append(a1)

    seed4 = {}
    for k, seed, ph, amp in (
        ((1, 0, 0), (0.0, 1.0, 0.2), 0.0, 1.0),
        ((0, 1, 0), (1.0, 0.0, 0.3), 0.7, 0.8),
        ((1, 1, 0), (0.2, 0.5, 1.0), -0.4, 0.6),
        ((0, 0, 1), (1.0, 0.4, 0.0), 0.3, 0.5),
    ):
        v = make_divfree_amp(k, seed)
        nrm = np.linalg.norm(v)
        if nrm > 0:
            seed4[k] = (amp * np.exp(1j * ph) / nrm) * v
    a2 = ascent_rb(seed4, steps=20, lr=0.1, rng=rng)
    a2["label"] = "ascent_four_mode"
    ascent_rows.append(a2)
    rows.append(a2)
    a3 = ascent_rb(separated_triad(1), steps=20, lr=0.1, rng=rng)
    a3["label"] = "ascent_sep_m1"
    ascent_rows.append(a3)
    rows.append(a3)
    print("ascent", max_rb(ascent_rows), flush=True)

    ident_ok = all(
        abs(r["pairing"] - r["Tc_probe"]) < 1e-8 * max(1.0, abs(r["Tc_probe"]))
        and abs(r["Ds_omega"] - r["Ds"]) < 1e-8 * max(1.0, r["Ds"])
        for r in identities
    )

    finite_rb = [r["R_B"] for r in rows if finite(r.get("R_B", float("nan")))]
    verdict = {
        "identity_ok": ident_ok,
        "fft_match_triad": fft_match,
        "fft_triad_Tc": fft_triad["Tc"],
        "exact_triad_Tc": exact_triad["Tc"],
        "max_R_B": max(finite_rb) if finite_rb else None,
        "power_max_R_B": max_rb(power_rows),
        "power_rb_by_kmax": rb_vs_kmax(power_rows),
        "lac_max_R_B": max_rb(lac_rows),
        "tube_max_R_B": max_rb(tube_rows),
        "rnd_max_R_B": max_rb(rnd_rows),
        "fft_max_R_B": max_rb(fft_rows),
        "fft_rb_by_kmax": rb_vs_kmax(fft_rows),
        "fft_max_R_L": max(
            (r["R_L"] for r in fft_rows if finite(r.get("R_L", float("nan")))),
            default=float("nan"),
        ),
        "fft_RL_by_kmax": {
            str(r["kmax"]): max(
                (
                    s["R_L"]
                    for s in fft_rows
                    if s.get("kmax") == r["kmax"] and finite(s.get("R_L", float("nan")))
                ),
                default=float("nan"),
            )
            for r in fft_rows
        },
        "hi_rb_by_kmax": rb_vs_kmax(hi_rows),
        "hi_max_R_B": max_rb(hi_rows),
        "ascent_max_R_B": max_rb(ascent_rows),
        "killed": False,
        "survived_second_pass": True,
    }
    p_by_k = rb_vs_kmax(fft_rows)
    if p_by_k:
        ks = sorted(p_by_k, key=lambda x: int(x))
        if (
            len(ks) >= 3
            and p_by_k[ks[-1]] > 2.0 * max(p_by_k[ks[0]], 1e-16)
            and p_by_k[ks[-1]] > 1.0
        ):
            verdict["killed"] = True
            verdict["survived_second_pass"] = False
            verdict["kill_note"] = "FFT power-law R_B grew with kmax on this range"
    return {
        "verdict": verdict,
        "identities": identities,
        "rows": rows,
        "fft_rows": fft_rows,
        "ascent_rows": ascent_rows,
    }


def main() -> None:
    out = run()
    dest = ROOT / "results" / "bstar_attack"
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "bstar_symmetrize.json"
    path.write_text(json.dumps(out, indent=2, default=str))
    v = out["verdict"]
    print("identity_ok", v["identity_ok"])
    print("fft_match", v["fft_match_triad"], "fft_Tc", v["fft_triad_Tc"], "exact", v["exact_triad_Tc"])
    print("max_R_B", v["max_R_B"])
    print("power_max", v["power_max_R_B"], "by_kmax", v["power_rb_by_kmax"])
    print("lac_max", v["lac_max_R_B"], "tube_max", v["tube_max_R_B"])
    print("rnd_max", v["rnd_max_R_B"], "fft_max", v["fft_max_R_B"])
    print("ascent_max", v["ascent_max_R_B"], "fft_max_R_L", v.get("fft_max_R_L"), v.get("fft_RL_by_kmax"))
    print("hi_max", v.get("hi_max_R_B"), "by_kmax", v.get("hi_rb_by_kmax"))
    print("wrote", path)


if __name__ == "__main__":
    main()
