#!/usr/bin/env python3
"""
Axisymmetric shell estimate — identities and measurements.

Class of the theorem: axisymmetric with swirl, unaugmented, on R^3.
This probe checks pairing algebra on Z^3 (normalized T^3).
That is not the theorem's manifold.

Remainder T_{j<-j} is not bounded here.
Do not quote the sign of Lambda'.
NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from estimate_audit import classify_paragraph  # noqa: E402
from track_b_lemmas import rec  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "AXISYM-SHELL.md"
PAIRING_TOL = 1e-15


def tau(omega_xi: float, omega_eta: float, omega_zeta: float, j_xi: float, j_eta: float) -> float:
    return (omega_xi - omega_zeta) * j_xi + (omega_eta - omega_zeta) * j_eta


def tau_shift_identity(omega_star: float = 3.0) -> dict:
    xi, eta, zeta = 5.0, -1.0, 2.0
    j_xi, j_eta = 7.0, -4.0
    left = tau(xi, eta, zeta, j_xi, j_eta)
    right = tau(xi - omega_star, eta - omega_star, zeta - omega_star, j_xi, j_eta)
    return {
        "tau": left,
        "tau_shifted": right,
        "abs_err": abs(left - right),
        "omega_star": omega_star,
        "closed": abs(left - right) == 0.0,
    }


def wave_numbers(n: int) -> np.ndarray:
    return np.fft.fftfreq(n) * n


def mesh(n: int):
    k = wave_numbers(n)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k2_safe = k2.copy()
    k2_safe[0, 0, 0] = 1.0
    dealias = (np.abs(kx) < n / 3) & (np.abs(ky) < n / 3) & (np.abs(kz) < n / 3)
    dealias[0, 0, 0] = False
    return kx, ky, kz, k2, k2_safe, dealias


def project_div_free(uh, kx, ky, kz, k2_safe):
    div = kx * uh[0] + ky * uh[1] + kz * uh[2]
    out = uh - np.stack([kx, ky, kz], axis=0) * (div / k2_safe)
    out[:, 0, 0, 0] = 0.0
    return out


def from_physical(u: np.ndarray) -> np.ndarray:
    n = u.shape[1]
    kx, ky, kz, _k2, k2_safe, dealias = mesh(n)
    uh = np.stack([np.fft.fftn(u[c]) for c in range(3)], axis=0)
    uh *= dealias
    return project_div_free(uh, kx, ky, kz, k2_safe)


def random_field(n: int, rng: np.random.Generator) -> np.ndarray:
    return from_physical(rng.normal(size=(3, n, n, n)))


def rotate_z90_phys(u: np.ndarray) -> np.ndarray:
    """u'(x) = R u(R^{-1} x) with R(x,y,z)=(-y,x,z)."""
    src = np.rot90(u, -1, axes=(1, 2))
    out = np.empty_like(src)
    out[0] = -src[1]
    out[1] = src[0]
    out[2] = src[2]
    return out


def fourfold(uh: np.ndarray) -> np.ndarray:
    u = physical(uh)
    acc = u.copy()
    cur = u
    for _ in range(3):
        cur = rotate_z90_phys(cur)
        acc = acc + cur
    return from_physical(acc * 0.25)


def taylor_green_like(n: int) -> np.ndarray:
    """Trigonometric sample. Not the R^3 axisymmetric class."""
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    u0 = np.sin(X) * np.cos(Y) * np.cos(Z)
    u1 = -np.cos(X) * np.sin(Y) * np.cos(Z)
    u2 = np.zeros_like(u0)
    return from_physical(np.stack([u0, u1, u2], axis=0))


def physical(uh: np.ndarray) -> np.ndarray:
    return np.stack([np.fft.ifftn(uh[c]).real for c in range(3)], axis=0)


def bilinear(uh: np.ndarray, kx, ky, kz) -> np.ndarray:
    u = physical(uh)
    du = []
    for kk in (kx, ky, kz):
        du.append(np.stack([np.fft.ifftn(1j * kk * uh[c]).real for c in range(3)], axis=0))
    conv = u[0] * du[0] + u[1] * du[1] + u[2] * du[2]
    return np.stack([np.fft.fftn(conv[c]) for c in range(3)], axis=0)


def curl(uh: np.ndarray, kx, ky, kz) -> np.ndarray:
    wx = 1j * ky * uh[2] - 1j * kz * uh[1]
    wy = 1j * kz * uh[0] - 1j * kx * uh[2]
    wz = 1j * kx * uh[1] - 1j * ky * uh[0]
    return np.stack([wx, wy, wz], axis=0)


def energy(uh: np.ndarray) -> float:
    n = uh.shape[1]
    return float(np.vdot(uh, uh).real) / (n**3)


def pairing_energy(uh: np.ndarray, kx, ky, kz) -> float:
    b = bilinear(uh, kx, ky, kz)
    n = uh.shape[1]
    return float(np.vdot(b, uh).real) / (n**3)


def shell_id(k2: np.ndarray) -> np.ndarray:
    out = np.full(k2.shape, -100, dtype=int)
    mask = k2 > 0
    out[mask] = np.floor(0.5 * np.log2(k2[mask])).astype(int)
    return out


def split_field(uh: np.ndarray, shells: np.ndarray, j: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ir = uh * (shells <= j - 2)
    loc = uh * (np.abs(shells - j) <= 1)
    uv = uh - ir - loc
    return ir, loc, uv


def transfer_into(uh_src_pair: np.ndarray, uh_test: np.ndarray, kx, ky, kz, mask) -> float:
    b = bilinear(uh_src_pair, kx, ky, kz)
    n = uh_test.shape[1]
    tes = uh_test * mask
    return -float(np.vdot(b, tes).real) / (n**3)


OCC_REL = 1e-3


def modewise_pairing(b: np.ndarray, tes: np.ndarray, n: int) -> np.ndarray:
    """Per-mode energy pairing. Sum over a mask equals -Re(vdot(b, tes))/n³."""
    raw = np.zeros(tes.shape[1:], dtype=np.float64)
    for c in range(3):
        raw += (np.conj(b[c]) * tes[c]).real
    return -raw / (n**3)


def remainder_occupancy(contrib: np.ndarray, mask: np.ndarray, xj: float) -> dict:
    """Occupancy and cancellation of the local remainder on one shell.

    C = |sum contrib| / sum |contrib|. 1 = no cancel. None if vacuous.
    occ_support = share of shell modes above OCC_REL of max |contrib|.
    occ_part = participation ratio of |contrib|.
    Not 5-D spatial occupation. Not Constantin–Fefferman.
    """
    c = contrib[mask]
    n_modes = int(c.size)
    signed = float(c.sum()) if n_modes else 0.0
    l1 = float(np.abs(c).sum()) if n_modes else 0.0
    scale = max(abs(xj) ** 1.5, 1e-30)
    # Live remainder, not cancelled noise: |T| must sit above pairing residual.
    vacuous = n_modes == 0 or abs(signed) <= 1e-14 * scale
    if vacuous:
        return {
            "n_modes": n_modes,
            "C": None,
            "occ_support": 0.0,
            "occ_part": 0.0,
            "l1": l1,
            "signed": signed,
            "vacuous": True,
        }
    ac = np.abs(c)
    mx = float(ac.max())
    occ_support = float(np.mean(ac >= OCC_REL * mx))
    occ_part = float((ac.sum() ** 2) / (n_modes * float(np.dot(ac, ac)) + 1e-30))
    return {
        "n_modes": n_modes,
        "C": abs(signed) / l1,
        "occ_support": occ_support,
        "occ_part": occ_part,
        "l1": l1,
        "signed": signed,
        "vacuous": False,
    }


def enstrophy_transfer(uh: np.ndarray, kx, ky, kz, mask) -> float:
    wh = curl(uh, kx, ky, kz)
    # B(ω,u) = ω·∇u - u·∇ω
    u = physical(uh)
    w = physical(wh)
    du = [np.stack([np.fft.ifftn(1j * kk * uh[c]).real for c in range(3)], axis=0) for kk in (kx, ky, kz)]
    dw = [np.stack([np.fft.ifftn(1j * kk * wh[c]).real for c in range(3)], axis=0) for kk in (kx, ky, kz)]
    stretch = w[0] * du[0] + w[1] * du[1] + w[2] * du[2]
    trans = u[0] * dw[0] + u[1] * dw[1] + u[2] * dw[2]
    bh = np.stack([np.fft.fftn(stretch[c] - trans[c]) for c in range(3)], axis=0)
    n = uh.shape[1]
    tes = wh * mask
    return float(np.vdot(bh, tes).real) / (n**3)


def strain_alignment(uh: np.ndarray, kx, ky, kz, thresh: float) -> dict:
    u = physical(uh)
    grads = []
    for kk in (kx, ky, kz):
        grads.append(np.stack([np.fft.ifftn(1j * kk * uh[c]).real for c in range(3)], axis=0))
    # grads[j][i] = ∂_j u_i
    S = np.zeros((3, 3) + u.shape[1:])
    for i in range(3):
        for j in range(3):
            S[i, j] = 0.5 * (grads[j][i] + grads[i][j])
    w = physical(curl(uh, kx, ky, kz))
    w2 = np.sum(w * w, axis=0)
    live = w2 > thresh
    if not np.any(live):
        return {"alpha_mean": None, "n_live": 0}
    xi = w / np.sqrt(w2 + 1e-30)
    alpha = np.zeros(w2.shape)
    for i in range(3):
        for j in range(3):
            alpha += xi[i] * S[i, j] * xi[j]
    return {
        "alpha_mean": float(alpha[live].mean()),
        "n_live": int(live.sum()),
        "thresh": thresh,
    }


def score_field(uh: np.ndarray, name: str) -> dict:
    n = uh.shape[1]
    kx, ky, kz, k2, _k2_safe, dealias = mesh(n)
    uh = uh * dealias
    shells = shell_id(k2)
    e = energy(uh)
    pair = pairing_energy(uh, kx, ky, kz)
    pair_scale = max(e ** 1.5, 1e-30)
    pair_rel = abs(pair) / pair_scale

    js = sorted(int(j) for j in np.unique(shells) if j >= 0)
    rows = []
    sum_t = 0.0
    for j in js:
        mask = shells == j
        xj = energy(uh * mask)
        if xj <= 0:
            continue
        ir, loc, _uv = split_field(uh, shells, j)
        t_full = transfer_into(uh, uh, kx, ky, kz, mask)
        t_no_ir = transfer_into(uh - ir, uh, kx, ky, kz, mask)
        b_loc = bilinear(loc, kx, ky, kz)
        tes = uh * mask
        t_loc = -float(np.vdot(b_loc, tes).real) / (n**3)
        contrib = modewise_pairing(b_loc, tes, n)
        occ = remainder_occupancy(contrib, mask, xj)
        t_ir = t_full - t_no_ir
        t_uv = t_no_ir - t_loc
        split_err = abs(t_full - (t_ir + t_loc + t_uv))
        wh = curl(uh, kx, ky, kz)
        zj = energy(wh * mask)
        z_full = enstrophy_transfer(uh, kx, ky, kz, mask)
        z_no_ir = enstrophy_transfer(uh - ir, kx, ky, kz, mask)
        z_loc = enstrophy_transfer(loc, kx, ky, kz, mask)
        z_ir = z_full - z_no_ir
        z_uv = z_no_ir - z_loc
        rows.append(
            {
                "j": j,
                "X_j": xj,
                "Z_j": zj,
                "T_j": t_full,
                "T_IR": t_ir,
                "T_loc": t_loc,
                "T_UV": t_uv,
                "split_err": split_err,
                "rho_E": t_loc / xj if xj else None,
                "rho_Z": z_loc / zj if zj else None,
                "Z_IR": z_ir,
                "Z_loc": z_loc,
                "Z_UV": z_uv,
                "C": occ["C"],
                "occ_support": occ["occ_support"],
                "occ_part": occ["occ_part"],
                "vacuous": occ["vacuous"],
                "n_modes": occ["n_modes"],
            }
        )
        sum_t += t_full

    live = [r for r in rows if r["X_j"] > 1e-14]
    rho_e = [r["rho_E"] for r in live if r["rho_E"] is not None]
    rho_z = [r["rho_Z"] for r in live if r["rho_Z"] is not None and r["Z_j"] > 1e-14]
    align = strain_alignment(uh, kx, ky, kz, thresh=1e-8 * (energy(curl(uh, kx, ky, kz)) + 1e-30))
    peak = max(live, key=lambda r: abs(r["rho_E"] or 0.0), default=None)
    measured = [r for r in live if not r["vacuous"] and r["C"] is not None]
    wsum = sum(r["X_j"] for r in measured)
    rem = {
        "peak_j": None if peak is None else peak["j"],
        "C_peak": None if peak is None else peak["C"],
        "occ_support_peak": None if peak is None else peak["occ_support"],
        "occ_part_peak": None if peak is None else peak["occ_part"],
        "peak_vacuous": True if peak is None else bool(peak["vacuous"]),
        "C_mean": (
            None
            if wsum <= 0
            else float(sum(r["C"] * r["X_j"] for r in measured) / wsum)
        ),
        "occ_support_mean": (
            None
            if wsum <= 0
            else float(sum(r["occ_support"] * r["X_j"] for r in measured) / wsum)
        ),
        "occ_part_mean": (
            None
            if wsum <= 0
            else float(sum(r["occ_part"] * r["X_j"] for r in measured) / wsum)
        ),
        "n_live": len(live),
        "n_measured": len(measured),
    }
    return {
        "name": name,
        "n": n,
        "E": e,
        "pairing": pair,
        "pairing_rel": pair_rel,
        "pairing_closed": pair_rel < PAIRING_TOL,
        "sum_T": sum_t,
        "sum_T_rel": abs(sum_t) / max(pair_scale, 1e-30),
        "max_split_err": max((r["split_err"] for r in rows), default=0.0),
        "rho_E": rho_e,
        "rho_Z": rho_z,
        "max_abs_rho_E": max((abs(x) for x in rho_e), default=0.0),
        "max_abs_rho_Z": max((abs(x) for x in rho_z), default=0.0),
        "alignment": align,
        "remainder": rem,
        "shells": rows,
    }


def lemmas(payload_fields: list[dict], tau_row: dict, page_ok: bool) -> list[dict]:
    pairing_ok = all(f["pairing_closed"] for f in payload_fields)
    split_ok = all(f["max_split_err"] < 1e-12 for f in payload_fields)
    return [
        rec(
            "AS_identity",
            "shell enstrophy identity on axisymmetric-with-swirl NS on R^3",
            "pass",
            "Proposition AS-Id. T_j is named. Not bounded by Z-dot or Lambda'.",
        ),
        rec(
            "AS_split",
            "T_j = T_IR + T_{j<-j} + T_UV",
            "pass" if split_ok else "fail",
            "Door 1 partition. Lattice check max_split_err on samples.",
        ),
        rec(
            "AS_young_IR",
            "infrared Young with C_IR[φ] only",
            "pass",
            "Named constant. Transport piece may absorb into nu D_j. Not the local block.",
        ),
        rec(
            "AS_young_UV",
            "ultraviolet Young with C_UV[φ] only",
            "pass",
            "Named constant. Exponent may move by a fixed shift. Local block stays.",
        ),
        rec(
            "AS_tau",
            "closed-triad rewrite τ is an identity",
            "pass" if tau_row["closed"] else "fail",
            "Algebra. Not a bound.",
        ),
        rec(
            "AS_omega_star",
            "τ(ω-ω_*)=τ(ω) for a constant ω_*",
            "pass" if tau_row["closed"] else "fail",
            "Shift by a constant, not by Lambda.",
        ),
        rec(
            "AS_pairing_check",
            "energy pairing residual < 10^{-15} relative",
            "pass" if pairing_ok else "fail",
            "Lattice diagnostic. Not the R^3 time series. Sign of Lambda' is not quoted.",
        ),
        rec(
            "AS_remainder",
            "T_{j<-j} is bounded for the class",
            "fail",
            "Named remainder. Samples print a ratio; that is not [ρ].",
        ),
        rec(
            "AS_rho",
            "[ρ] holds for axisymmetric-with-swirl NS",
            "fail",
            "Conditional theorem only. Not measured for the class.",
        ),
        rec(
            "AS_door3",
            "alignment α bounds T_{j<-j}",
            "fail",
            "Criterion to test. Separate from occupancy.",
        ),
        rec(
            "AS_page_clean",
            "estimate page has no discard-list object in the claim",
            "pass" if page_ok else "fail",
            "Filter: estimate_audit.classify_paragraph.",
        ),
        rec(
            "AS_ns_solved",
            "this estimate solves NS",
            "fail",
            "Class and ρ_j stay in the sentence.",
        ),
    ]


def run(n: int = 24, seed: int = 1390, out: Path | None = None) -> dict:
    rng = np.random.default_rng(seed)
    raw = random_field(n, rng)
    fields = [
        score_field(raw, "random_divfree"),
        score_field(fourfold(raw), "fourfold_z"),
        score_field(taylor_green_like(n), "taylor_green_like"),
    ]
    tau_row = tau_shift_identity()
    page_text = PAGE.read_text() if PAGE.exists() else ""
    page_cls = classify_paragraph(page_text)
    page_ok = page_cls["allowed_in_estimate"] and "unrestricted three-dimensional" in page_text.lower()
    rows = lemmas(fields, tau_row, page_ok)
    counts = {"pass": 0, "fail": 0, "open": 0}
    for item in rows:
        counts[item["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "axisymmetric shell estimate",
            "class": "axisymmetric with swirl",
            "manifold_theorem": "R^3",
            "manifold_probe": "T^3 lattice algebra",
            "remainder": "T_{j<-j}",
            "tuning_the_pde": False,
            "lemma_star_open": True,
            "h1_started": False,
            "estimate_open": True,
            "kill": False,
            "lambda_prime_sign_quoted": False,
            "n": n,
            "seed": seed,
        },
        "tau": tau_row,
        "fields": [
            {
                "name": f["name"],
                "E": f["E"],
                "pairing_rel": f["pairing_rel"],
                "pairing_closed": f["pairing_closed"],
                "sum_T_rel": f["sum_T_rel"],
                "max_split_err": f["max_split_err"],
                "max_abs_rho_E": f["max_abs_rho_E"],
                "max_abs_rho_Z": f["max_abs_rho_Z"],
                "alignment": f["alignment"],
            }
            for f in fields
        ],
        "page_filter": page_cls,
        "lemmas": rows,
        "counts": counts,
        "domain_verdict": "open",
        "claim": (
            "Axisymmetric-with-swirl unaugmented NS on R^3; "
            "Z_j shell budget; remainder T_{j<-j}; [ρ] not assumed as measured."
        ),
    }
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=24)
    p.add_argument("--seed", type=int, default=1390)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    print(json.dumps(run(n=args.n, seed=args.seed, out=args.out), indent=2))


if __name__ == "__main__":
    main()
