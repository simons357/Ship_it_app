#!/usr/bin/env python3
"""
Snapshot tests of A_bad with Lambda = Lambda0 fixed.

Classical NS. No Q1. No K(t). No GCD matrix.
Not leftover 1. Not WRITE (6) as a theorem. Not a start from ABC_λ.

If Lambda scales with ||ω||_∞, the high set of a fixed-shape field
is amplitude-invariant and the sweep does not test the threshold.
This probe freezes Lambda0 from amplitude 1, then scales only the
field. C_needed_raw is the raw constant that would absorb A_bad
into r^{-2}∬|ω|² (no ν/8 dissipation subtracted).
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from track_b_lemmas import curl, fft, make_grid


VOL_T3 = (2.0 * math.pi) ** 3
TWOPI = 2.0 * math.pi
EC_FRAC = 0.35
C_STAR = 0.25
R_CYL = math.pi
AMP0 = 1.0
AMPS = (0.5, 1.0, 2.0, 4.0)
SNAPSHOT_LABEL = "snapshot test"


@dataclass(frozen=True)
class FieldReport:
    field: str
    amplitude: float
    lambda_fixed: float
    a_bad: float
    c_needed_raw: float
    x_loc: float
    r: float
    n: int
    n_high: int
    n_bad_pairs: int
    omega_inf: float
    c_star: float
    label: str = SNAPSHOT_LABEL
    leftover_1_closed: bool = False
    started_from_abc: bool = False
    note: str = (
        "Snapshot test. Lambda = Lambda0 fixed. "
        "Not leftover 1. Do not start H1 from ABC_λ."
    )


def c_needed_raw(a_bad: float, x_loc: float, r: float) -> float:
    """Raw C such that A_bad ≤ C r^{-2} ∫|ω|². Dissipation not subtracted."""
    denom = x_loc / (r * r)
    if denom <= 0.0:
        return float("nan")
    return float(a_bad / denom)


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


def bad_pair_integral(
    ox: np.ndarray,
    oy: np.ndarray,
    oz: np.ndarray,
    high: np.ndarray,
    dx: float,
    c_star: float,
    chunk: int = 256,
) -> tuple[float, int]:
    """Majorant ∭_Bad |ω(x)|²|ω(y)|/|x-y|³ on T³. Self-pairs dropped."""
    idx = np.flatnonzero(high.ravel())
    n_high = int(idx.size)
    if n_high == 0:
        return 0.0, 0
    n = ox.shape[0]
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
    acc = 0.0
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
        sinphi = np.sqrt(cx * cx + cy * cy + cz * cz)
        bad = valid & (sinphi > c_star * np.sqrt(dist))
        contrib = (mag[i0:i1, None] ** 2) * mag[None, :] / np.maximum(dist**3, 1e-30)
        acc += float(np.sum(contrib[bad]))
        n_bad += int(np.sum(bad))
        del dpx, dpy, dpz, dist2, dist, valid, cx, cy, cz, sinphi, bad, contrib
    _ = n
    return acc * (dx**6), n_bad


def run_one(
    field: str,
    amp: float,
    lambda0: float,
    n: int = 16,
    r: float = R_CYL,
    c_star: float = C_STAR,
) -> FieldReport:
    u, v, w = _field(field, n, amp)
    ox, oy, oz = vorticity(u, v, w)
    mag = np.sqrt(ox * ox + oy * oy + oz * oz)
    high = mag >= lambda0
    dx = TWOPI / n
    a_bad, n_bad = bad_pair_integral(ox, oy, oz, high, dx, c_star)
    x_loc = float(np.sum(mag * mag)) * dx**3
    c_raw = c_needed_raw(a_bad, x_loc, r)
    name = "ABC" if field.lower() == "abc" else "Taylor–Green"
    return FieldReport(
        field=name,
        amplitude=float(amp),
        lambda_fixed=float(lambda0),
        a_bad=float(a_bad),
        c_needed_raw=float(c_raw),
        x_loc=float(x_loc),
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
) -> tuple[float, list[FieldReport]]:
    lambda0 = reference_lambda0(field, n)
    rows = [run_one(field, amp, lambda0, n=n, r=r, c_star=c_star) for amp in amps]
    return lambda0, rows


def sweep(n: int = 16, amps: tuple[float, ...] = AMPS) -> dict:
    out_rows = []
    tables = {}
    for field in ("abc", "taylor-green"):
        lambda0, rows = sweep_field(field, n=n, amps=amps)
        tables[rows[0].field] = {
            "lambda0": lambda0,
            "rows": [asdict(row) for row in rows],
        }
        out_rows.extend(rows)
    return {
        "label": SNAPSHOT_LABEL,
        "leftover_1_closed": False,
        "started_from_abc": False,
        "lambda_policy": "Lambda = Lambda0 fixed; Lambda0 = 0.35 ||ω||_∞ at amplitude 1",
        "c_star": C_STAR,
        "r": R_CYL,
        "n": n,
        "amps": list(amps),
        "fields": tables,
        "meta": {
            "slot": "B",
            "write": "snapshot A_bad with fixed Lambda0",
            "h1_proved": False,
            "write_6_is_theorem": False,
            "tuning_the_pde": False,
            "tesla": "estimates, not names. A finite C_needed_raw is not C0.",
        },
        "printed": format_table(out_rows),
    }


def format_table(rows: list[FieldReport]) -> str:
    header = (
        "SNAPSHOT TESTS — Lambda = Lambda0 fixed. Not leftover 1.\n"
        f"{'field':<14} {'amplitude':>10} {'fixed threshold':>16} "
        f"{'bad-pair integral':>20} {'C_needed_raw':>14}"
    )
    lines = [header]
    for row in rows:
        lines.append(
            f"{row.field:<14} {row.amplitude:10.4g} {row.lambda_fixed:16.6g} "
            f"{row.a_bad:20.6g} {row.c_needed_raw:14.6g}"
        )
    return "\n".join(lines)


def run(n: int = 16, amps: tuple[float, ...] = AMPS, out: Path | None = None) -> dict:
    payload = sweep(n=n, amps=amps)
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        slim = {k: v for k, v in payload.items() if k != "printed"}
        out.write_text(json.dumps(slim, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=16)
    p.add_argument("--quick", action="store_true")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    amps = (0.5, 1.0, 2.0) if args.quick else AMPS
    payload = run(n=args.n, amps=amps, out=args.out)
    print(payload["printed"])
    print()
    print("label: snapshot tests")
    print("leftover 1 closed:", payload["leftover_1_closed"])
    print("started from ABC_λ:", payload["started_from_abc"])


if __name__ == "__main__":
    main()
