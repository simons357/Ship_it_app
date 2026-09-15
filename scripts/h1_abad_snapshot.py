#!/usr/bin/env python3
"""
Periodic snapshot diagnostics of A_bad with Lambda = Lambda0 fixed.

Classical NS. No Q1. No K(t). No GCD matrix.
Not leftover 1. Not WRITE (6) as a theorem. Not a start from ABC_λ.

Two integrals on the same grid and the same Bad pairs:

  A_angle    = ∭_Bad δ |ω(x)|² |ω(y)| / |x-y|³     δ = |ξ(x)×ξ(y)|
  A_no_angle = ∭_Bad     |ω(x)|² |ω(y)| / |x-y|³

The Bad cut does not replace δ in the integrand. A_no_angle is a
larger majorant (0 ≤ δ ≤ 1). It is not the original quantity.

C_needed_raw = max(0, (r²/E) [A_angle − (ν/8) D_φ])
with E = ∫|ω|² and D_φ = ∫|∇ω|² φ. φ ≡ 1 on T³. One time.

ABC as an exact smooth Beltrami field already defeats unrestricted
local (6). These snapshots neither establish nor undo that. Correcting
the record does not rescue that estimate.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from track_b_lemmas import curl, fft, ifft, make_grid


VOL_T3 = (2.0 * math.pi) ** 3
TWOPI = 2.0 * math.pi
EC_FRAC = 0.35
C_STAR = 0.25
R_CYL = math.pi
NU = 1.0
AMP0 = 1.0
AMPS = (0.5, 1.0, 2.0, 4.0)
SNAPSHOT_LABEL = "periodic snapshot diagnostic"


@dataclass(frozen=True)
class FieldReport:
    field: str
    amplitude: float
    lambda_fixed: float
    a_angle: float
    a_no_angle: float
    c_needed_raw: float
    c_no_angle_diag: float
    e: float
    d_phi: float
    nu: float
    r: float
    n: int
    n_high: int
    n_bad_pairs: int
    omega_inf: float
    c_star: float
    label: str = SNAPSHOT_LABEL
    leftover_1_closed: bool = False
    started_from_abc: bool = False
    unrestricted_local_6_rescued: bool = False
    note: str = (
        "Periodic snapshot diagnostic. Lambda = Lambda0 fixed. "
        "A_angle keeps δ=|ξ×ξ|. A_no_angle is a larger majorant. "
        "Not leftover 1. Does not rescue unrestricted local (6). "
        "Do not start H1 from ABC_λ."
    )


def c_needed_raw(
    a_angle: float,
    e: float,
    d_phi: float,
    r: float,
    nu: float = NU,
) -> float:
    """Requested snapshot constant. Dissipation subtracted. Floor at 0."""
    if e <= 0.0:
        return float("nan")
    return float(max(0.0, (r * r / e) * (a_angle - (nu / 8.0) * d_phi)))


def c_no_angle_diag(a_no_angle: float, e: float, r: float) -> float:
    """Angle-free diagnostic r² A_no_angle / E. Not C_needed_raw."""
    if e <= 0.0:
        return float("nan")
    return float((r * r / e) * a_no_angle)


def abc_field(n: int, amp: float):
    x = np.linspace(0.0, TWOPI, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    u = amp * (np.sin(Z) + np.cos(Y))
    v = amp * (np.sin(X) + np.cos(Z))
    w = amp * (np.sin(Y) + np.cos(X))
    return u, v, w


def taylor_green_field(n: int, amp: float):
    x = np.linspace(0.0, TWOPI, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    u = amp * np.sin(X) * np.cos(Y) * np.cos(Z)
    v = -amp * np.cos(X) * np.sin(Y) * np.cos(Z)
    w = np.zeros_like(u)
    return u, v, w


def vorticity(u, v, w):
    n = u.shape[0]
    kx, ky, kz, _k2, _k2_safe, _dealias = make_grid(n)
    uh, vh, wh = fft(u), fft(v), fft(w)
    ox, oy, oz, _oxh, _oyh, _ozh = curl(uh, vh, wh, kx, ky, kz)
    return ox, oy, oz


def omega_inf(ox, oy, oz) -> float:
    return float(np.max(np.sqrt(ox * ox + oy * oy + oz * oz)))


def dissipation_phi(ox, oy, oz, dx: float, phi: np.ndarray | None = None) -> float:
    """D_φ = ∫ |∇ω|² φ. φ ≡ 1 on T³ if phi is None."""
    n = ox.shape[0]
    kx, ky, kz, _k2, _k2_safe, _dealias = make_grid(n)
    acc = np.zeros_like(ox)
    for comp in (ox, oy, oz):
        ch = fft(comp)
        acc = acc + ifft(1j * kx * ch) ** 2
        acc = acc + ifft(1j * ky * ch) ** 2
        acc = acc + ifft(1j * kz * ch) ** 2
    if phi is not None:
        acc = acc * phi
    return float(np.sum(acc)) * dx**3


def reference_lambda0(field: str, n: int, amp0: float = AMP0, frac: float = EC_FRAC) -> float:
    ox, oy, oz = vorticity(*_field(field, n, amp0))
    return frac * omega_inf(ox, oy, oz)


def _field(name: str, n: int, amp: float):
    key = name.lower().replace("–", "-").replace("—", "-")
    key = key.replace("taylor-green", "tg").replace("taylorgreen", "tg")
    if key in ("abc",):
        return abc_field(n, amp)
    if key in ("tg", "taylor green", "taylor-green"):
        return taylor_green_field(n, amp)
    raise ValueError(name)


def _torus_delta(delta: np.ndarray) -> np.ndarray:
    return delta - TWOPI * np.round(delta / TWOPI)


def bad_pair_integrals(
    ox: np.ndarray,
    oy: np.ndarray,
    oz: np.ndarray,
    high: np.ndarray,
    dx: float,
    c_star: float,
    chunk: int = 256,
) -> tuple[float, float, int]:
    """A_angle and A_no_angle on the same Bad pairs. Self-pairs dropped."""
    idx = np.flatnonzero(high.ravel())
    n_high = int(idx.size)
    if n_high == 0:
        return 0.0, 0.0, 0
    ii, jj, kk = np.unravel_index(idx, ox.shape)
    px = ii.astype(np.float64) * dx
    py = jj.astype(np.float64) * dx
    pz = kk.astype(np.float64) * dx
    wx = ox.ravel()[idx]
    wy = oy.ravel()[idx]
    wz = oz.ravel()[idx]
    mag = np.sqrt(wx * wx + wy * wy + wz * wz)
    safe = np.maximum(mag, 1e-30)
    sx, sy, sz = wx / safe, wy / safe, wz / safe
    acc_angle = 0.0
    acc_no = 0.0
    n_bad = 0
    for i0 in range(0, n_high, chunk):
        i1 = min(n_high, i0 + chunk)
        dpx = _torus_delta(px[i0:i1, None] - px[None, :])
        dpy = _torus_delta(py[i0:i1, None] - py[None, :])
        dpz = _torus_delta(pz[i0:i1, None] - pz[None, :])
        dist2 = dpx * dpx + dpy * dpy + dpz * dpz
        dist = np.sqrt(np.maximum(dist2, 0.0))
        valid = dist > 0.5 * dx
        cx = sy[i0:i1, None] * sz[None, :] - sz[i0:i1, None] * sy[None, :]
        cy = sz[i0:i1, None] * sx[None, :] - sx[i0:i1, None] * sz[None, :]
        cz = sx[i0:i1, None] * sy[None, :] - sy[i0:i1, None] * sx[None, :]
        delta = np.sqrt(cx * cx + cy * cy + cz * cz)
        bad = valid & (delta > c_star * np.sqrt(dist))
        kernel = (mag[i0:i1, None] ** 2) * mag[None, :] / np.maximum(dist**3, 1e-30)
        acc_no += float(np.sum(kernel[bad]))
        acc_angle += float(np.sum((delta * kernel)[bad]))
        n_bad += int(np.sum(bad))
        del dpx, dpy, dpz, dist2, dist, valid, cx, cy, cz, delta, bad, kernel
    vol6 = dx**6
    return acc_angle * vol6, acc_no * vol6, n_bad


def run_one(
    field: str,
    amp: float,
    lambda0: float,
    n: int = 16,
    r: float = R_CYL,
    c_star: float = C_STAR,
    nu: float = NU,
) -> FieldReport:
    u, v, w = _field(field, n, amp)
    ox, oy, oz = vorticity(u, v, w)
    mag = np.sqrt(ox * ox + oy * oy + oz * oz)
    high = mag >= lambda0
    dx = TWOPI / n
    a_angle, a_no_angle, n_bad = bad_pair_integrals(ox, oy, oz, high, dx, c_star)
    e = float(np.sum(mag * mag)) * dx**3
    d_phi = dissipation_phi(ox, oy, oz, dx)
    c_raw = c_needed_raw(a_angle, e, d_phi, r, nu=nu)
    c_diag = c_no_angle_diag(a_no_angle, e, r)
    name = "ABC" if field.lower() == "abc" else "Taylor–Green"
    return FieldReport(
        field=name,
        amplitude=float(amp),
        lambda_fixed=float(lambda0),
        a_angle=float(a_angle),
        a_no_angle=float(a_no_angle),
        c_needed_raw=float(c_raw),
        c_no_angle_diag=float(c_diag),
        e=float(e),
        d_phi=float(d_phi),
        nu=float(nu),
        r=float(r),
        n=int(n),
        n_high=int(np.sum(high)),
        n_bad_pairs=int(n_bad),
        omega_inf=omega_inf(ox, oy, oz),
        c_star=float(c_star),
    )


def sweep_field(
    field: str,
    n: int = 16,
    amps: tuple[float, ...] = AMPS,
    r: float = R_CYL,
    c_star: float = C_STAR,
    nu: float = NU,
) -> tuple[float, list[FieldReport]]:
    lambda0 = reference_lambda0(field, n)
    rows = [
        run_one(field, amp, lambda0, n=n, r=r, c_star=c_star, nu=nu) for amp in amps
    ]
    return lambda0, rows


def sweep(
    n: int = 16,
    amps: tuple[float, ...] = AMPS,
    nu: float = NU,
) -> dict:
    out_rows = []
    tables = {}
    for field in ("abc", "taylor-green"):
        lambda0, rows = sweep_field(field, n=n, amps=amps, nu=nu)
        tables[rows[0].field] = {
            "lambda0": lambda0,
            "rows": [asdict(row) for row in rows],
        }
        out_rows.extend(rows)
    return {
        "label": SNAPSHOT_LABEL,
        "leftover_1_closed": False,
        "started_from_abc": False,
        "unrestricted_local_6_rescued": False,
        "lambda_policy": "Lambda = Lambda0 fixed; Lambda0 = 0.35 ||ω||_∞ at amplitude 1",
        "c_star": C_STAR,
        "r": R_CYL,
        "nu": nu,
        "n": n,
        "amps": list(amps),
        "fields": tables,
        "meta": {
            "slot": "B",
            "write": "periodic snapshot diagnostic; A_angle keeps δ",
            "h1_proved": False,
            "write_6_is_theorem": False,
            "tuning_the_pde": False,
            "unrestricted_local_6_defeated_by_abc": True,
            "tesla": "estimates, not names. A finite C_needed_raw is not C0.",
        },
        "printed": format_table(out_rows),
    }


def format_table(rows: list[FieldReport]) -> str:
    header = (
        "PERIODIC SNAPSHOT DIAGNOSTICS — Lambda = Lambda0 fixed.\n"
        "A_angle keeps δ=|ξ×ξ|. A_no_angle is a larger majorant, not the original.\n"
        "C_needed_raw = max(0, (r²/E)[A_angle − (ν/8) D_φ]). Not leftover 1.\n"
        "Does not rescue unrestricted local (6).\n"
        f"{'field':<14} {'amplitude':>10} {'fixed threshold':>16} "
        f"{'A_angle':>14} {'A_no_angle':>14} {'C_needed_raw':>14}"
    )
    lines = [header]
    for row in rows:
        lines.append(
            f"{row.field:<14} {row.amplitude:10.4g} {row.lambda_fixed:16.6g} "
            f"{row.a_angle:14.6g} {row.a_no_angle:14.6g} {row.c_needed_raw:14.6g}"
        )
    return "\n".join(lines)


def run(
    n: int = 16,
    amps: tuple[float, ...] = AMPS,
    nu: float = NU,
    out: Path | None = None,
) -> dict:
    payload = sweep(n=n, amps=amps, nu=nu)
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        slim = {k: v for k, v in payload.items() if k != "printed"}
        out.write_text(json.dumps(slim, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=16)
    p.add_argument("--quick", action="store_true")
    p.add_argument("--nu", type=float, default=NU)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    amps = (0.5, 1.0, 2.0) if args.quick else AMPS
    payload = run(n=args.n, amps=amps, nu=args.nu, out=args.out)
    print(payload["printed"])
    print()
    print("label:", payload["label"])
    print("leftover 1 closed:", payload["leftover_1_closed"])
    print("started from ABC_λ:", payload["started_from_abc"])
    print("unrestricted local (6) rescued:", payload["unrestricted_local_6_rescued"])


if __name__ == "__main__":
    main()
