#!/usr/bin/env python3
"""
Coherent CONC: a named field with net P ≈ (ω·Sω)_+.

Classical NS. No Q1. No ε. Random-phase packets cancelled
(B16d). A Stokes eigenfunction has ∫ω·Sω = 0. A
z-independent tube in periodic strain does too: ∫ cos z dz
= 0. Sit a blob where S_zz keeps a sign. The cubic goes
one-sided. One-sided is not large versus D at this box.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from track_b_balance import VOL, production_dissipation
from track_b_evolve import ifrk2_step, packet_stats, shell_masses
from track_b_lemmas import curl, fft, make_grid, project, rec

N = 32
AMP_S = 0.02
DELTA = 0.35
X_TARGET = 2.5
NU = 0.1
DT_IDENT = 5e-5
CANCEL_MIN = 0.5
PD_MAX = 0.05
TUBE_CANCEL_MAX = 0.05
IDENT_MAX = 1e-2
SIGMA_MIN = 0.5

_BLOB: dict | None = None
_TUBE: dict | None = None
_IDENT: dict | None = None


def _coords(n: int):
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    return np.meshgrid(x, x, x, indexing="ij")


def _project_scaled(u, x_target: float):
    n = u.shape[1]
    kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
    uh, vh, wh = project(
        fft(u[0]) * dealias,
        fft(u[1]) * dealias,
        fft(u[2]) * dealias,
        kx,
        ky,
        kz,
        k2_safe,
    )
    ox, oy, oz, *_ = curl(uh, vh, wh, kx, ky, kz)
    xtot = float(np.mean(ox * ox + oy * oy + oz * oz)) * VOL
    scale = math.sqrt(x_target / max(xtot, 1e-30))
    uh, vh, wh = project(
        uh * scale * dealias,
        vh * scale * dealias,
        wh * scale * dealias,
        kx,
        ky,
        kz,
        k2_safe,
    )
    return uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias


def blob_strain_velocity(n: int = N, amp_s: float = AMP_S, delta: float = DELTA):
    """Gaussian blob at (π,π,0), where S_zz of the strain equals +1."""
    X, Y, Z = _coords(n)
    dx = X - math.pi
    dy = Y - math.pi
    dz = np.minimum(np.abs(Z), 2.0 * math.pi - np.abs(Z))
    env = np.exp(-(dx * dx + dy * dy + dz * dz) / (2.0 * delta * delta))
    u = np.zeros((3, n, n, n))
    u[0] = -env * dy
    u[1] = env * dx
    u[0] += amp_s * np.sin(X) * np.cos(Z)
    u[2] += -amp_s * np.cos(X) * np.sin(Z)
    return u


def tube_strain_velocity(n: int = N, amp_s: float = AMP_S, delta: float = DELTA):
    """Same swirl, z-independent. Periodic S_zz averages to 0 along the tube."""
    X, Y, Z = _coords(n)
    dx = X - math.pi
    dy = Y - math.pi
    env = np.exp(-(dx * dx + dy * dy) / (2.0 * delta * delta))
    u = np.zeros((3, n, n, n))
    u[0] = -env * dy
    u[1] = env * dx
    u[0] += amp_s * np.sin(X) * np.cos(Z)
    u[2] += -amp_s * np.cos(X) * np.sin(Z)
    return u


def _pack(u, nu: float = NU, x_target: float = X_TARGET) -> dict:
    uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias = _project_scaled(u, x_target)
    pd = production_dissipation(uh, vh, wh, kx, ky, kz, nu)
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
    st = packet_stats(shell_masses(oxh, oyh, ozh, k2, VOL), 3)
    return {
        "uh": uh,
        "vh": vh,
        "wh": wh,
        "kx": kx,
        "ky": ky,
        "kz": kz,
        "k2": k2,
        "k2_safe": k2_safe,
        "dealias": dealias,
        "pd": pd,
        "stats": st,
        "nu": nu,
    }


def blob_packet() -> dict:
    global _BLOB
    if _BLOB is None:
        _BLOB = _pack(blob_strain_velocity())
    return _BLOB


def tube_packet() -> dict:
    global _TUBE
    if _TUBE is None:
        _TUBE = _pack(tube_strain_velocity())
    return _TUBE


def identity_check() -> dict:
    global _IDENT
    if _IDENT is None:
        pack = blob_packet()
        before = pack["pd"]
        uh, vh, wh = ifrk2_step(
            pack["uh"],
            pack["vh"],
            pack["wh"],
            pack["kx"],
            pack["ky"],
            pack["kz"],
            pack["k2"],
            pack["k2_safe"],
            pack["dealias"],
            pack["nu"],
            DT_IDENT,
        )
        after = production_dissipation(
            uh, vh, wh, pack["kx"], pack["ky"], pack["kz"], pack["nu"]
        )
        pred = before["Xdot"]
        got = (after["X"] - before["X"]) / DT_IDENT
        _IDENT = {
            "pred": pred,
            "got": got,
            "rel": abs(got - pred) / max(abs(pred), 1e-30),
            "dt": DT_IDENT,
        }
    return _IDENT


def lemma_coherent_field() -> dict:
    pack = blob_packet()
    ident = identity_check()
    pd, st = pack["pd"], pack["stats"]
    ok = (
        ident["rel"] < IDENT_MAX
        and st["sigma"] >= SIGMA_MIN
        and abs(pd["X"] - X_TARGET) < 1e-9
    )
    return rec(
        "B17_coherent_field",
        "a named two-scale blob + signed strain is a readable classical CONC field",
        "pass" if ok else "fail",
        "Gaussian blob at (π,π,0) in u=(sin x cos z, 0, −cos x sin z). S_zz=+1 on the blob. Not a Stokes eigenfunction.",
        rel=ident["rel"],
        sigma=st["sigma"],
        jbar=st["jbar"],
        jstar=st["jstar"],
        X=pd["X"],
    )


def lemma_net_is_plus() -> dict:
    pd = blob_packet()["pd"]
    ok = pd["cancel"] >= CANCEL_MIN and pd["P"] > 0.0
    return rec(
        "B17a_net_is_plus",
        "this coherent CONC field has |∫ω·Sω| / ((ω·Sω)_+ + (ω·Sω)_−) ≥ 1/2",
        "pass" if ok else "fail",
        "Net sits on the plus pile. Random-phase packets cancelled at ~10^{-3}. This field does not.",
        cancel=pd["cancel"],
        P=pd["P"],
        Pplus=pd["Pplus"],
        Pminus=pd["Pminus"],
    )


def lemma_cubic_not_live() -> dict:
    pd = blob_packet()["pd"]
    live = abs(pd["P_over_D"]) >= PD_MAX or pd["Xdot"] >= 0.0
    return rec(
        "B17b_cubic_not_live",
        "the one-sided cubic owns Ẋ at the B13 working box (ν=0.1, X=2.5)",
        "fail" if not live else "open",
        "Coherence killed cancellation. It did not make P large versus D. Viscosity still owns the net.",
        P_over_D=pd["P_over_D"],
        Pplus_over_D=pd["Pplus_over_D"],
        Xdot=pd["Xdot"],
        D=pd["D"],
    )


def lemma_tube_still_cancels() -> dict:
    pd = tube_packet()["pd"]
    nets = pd["cancel"] >= CANCEL_MIN
    return rec(
        "B17c_tube_still_cancels",
        "a z-independent swirl in the same strain also has net P ≈ (ω·Sω)_+",
        "fail" if not nets else "open",
        "∫ cos z dz = 0 along the tube. Coherence of swirl is not the cubic. The blob had to sit where S_zz keeps a sign.",
        cancel=pd["cancel"],
        P=pd["P"],
        Pplus=pd["Pplus"],
    )


def lemma_blob_not_bkm() -> dict:
    pd = blob_packet()["pd"]
    return rec(
        "B17d_blob_is_not_bkm",
        "an L² bound on this blob is the Beale–Kato–Majda criterion",
        "fail",
        "The blob is more peaked than a fat packet. The criterion still asks for ∫‖ω‖_∞. Do not improve it into L².",
        bkm_gap=pd["bkm_gap"],
        winf=pd["winf"],
        wl2=pd["wl2"],
    )


def lemma_coherent_not_close() -> dict:
    return rec(
        "B17e_coherent_not_X_a_priori",
        "a signed-strain blob closes a bound for classical X",
        "fail",
        "Scored as B28. One-sided cubic at this box is still a leftover versus D. A leftover that no longer cancels is not continuation.",
    )


def lemma_coherent_not_a_retune() -> dict:
    return rec(
        "B17f_not_a_pde_retune",
        "reading a signed-strain blob, or turning ν down until Ẋ>0, is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. Localization in z is a knob on the check. Turning ν down is the same knob. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_coherent_field(),
        lemma_net_is_plus(),
        lemma_cubic_not_live(),
        lemma_tube_still_cancels(),
        lemma_blob_not_bkm(),
        lemma_coherent_not_close(),
        lemma_coherent_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "coherent CONC; signed-strain blob versus z-independent tube",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. A Stokes eigenfunction is not a cubic. "
                "Sit the blob where S_zz keeps a sign. One-sided is not large versus D."
            ),
            "domain_verdict": "open",
            "n": N,
            "amp_s": AMP_S,
            "delta": DELTA,
            "X": X_TARGET,
            "nu": NU,
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). DNS leftover is B23e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_coherent.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Coherent CONC. Signed-strain blob versus the tube that cancels.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
