#!/usr/bin/env python3
"""
Angular 1/r² viscosity vs I_tube.

Classical NS. No Q1. No ε. No Φ cancel.
B4c: full tube dissipation budgets the packet source.
B5b: the extra 1/r² piece, alone, does not.
Turn j* up; R_ang climbs. Tesla: that is a knob.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from track_b_hardy_tube import (
    integrate_mask,
    killer_field,
    packet_field,
    rec,
    swirl_fields,
)

_PACKETS: dict | None = None
_KILLERS: dict | None = None

JSTARS = (2, 3, 4, 5)


def rz_grid_fine(nr: int = 320, nz: int = 256, r1: float = 1.0):
    r = np.linspace(1e-5, r1, nr)
    z = np.linspace(0.0, 2.0 * np.pi, nz, endpoint=False)
    R, Z = np.meshgrid(r, z, indexing="ij")
    return r, z, R, Z


def angular_budget(h: np.ndarray, r: np.ndarray, z: np.ndarray, delta: float) -> dict:
    R, _Z = np.meshgrid(r, z, indexing="ij")
    fields = swirl_fields(h, r, z)
    tube = R < delta
    tube_i = integrate_mask(np.abs(fields["source"]), r, z, tube)
    ang = integrate_mask((h / np.maximum(R, 1e-30)) ** 2, r, z, tube)
    diss = integrate_mask(fields["diss_density"], r, z, tube)
    return {
        "tube_i": tube_i,
        "ang": ang,
        "diss": diss,
        "R_ang": tube_i / max(ang, 1e-30),
        "R_D": tube_i / max(diss, 1e-30),
        "n_r_tube": int(np.sum(r < delta)),
    }


def scan_packets() -> dict:
    global _PACKETS
    if _PACKETS is None:
        r, z, R, Z = rz_grid_fine()
        rows = []
        for j in JSTARS:
            ell = 2.0 ** (-j)
            h = packet_field(R, Z, ell, 2.0**j)
            bud = angular_budget(h, r, z, delta=2.0 * ell)
            rows.append(
                {
                    "jstar": j,
                    "ell": ell,
                    "delta": 2.0 * ell,
                    **bud,
                }
            )
        angs = [row["R_ang"] for row in rows]
        ds = [row["R_D"] for row in rows]
        _PACKETS = {
            "rows": rows,
            "R_ang": angs,
            "R_D": ds,
            "dominates": bool(angs) and max(angs) < 1.0,
            "climbs": angs[-1] > 2.0 * angs[0],
            "D_falls": ds[-1] < ds[0],
        }
    return _PACKETS


def scan_killers() -> dict:
    global _KILLERS
    if _KILLERS is None:
        rows = []
        for eps in (1.0, 0.5, 0.25, 0.125, 0.0625):
            r = np.linspace(1e-4, 1.6, 160)
            z = np.linspace(0.0, 2.0 * np.pi / eps, 192, endpoint=False)
            R, Z = np.meshgrid(r, z, indexing="ij")
            h = killer_field(R, Z, eps)
            bud = angular_budget(h, r, z, delta=1.0)
            rows.append({"eps": eps, **bud})
        angs = [row["R_ang"] for row in rows]
        _KILLERS = {
            "rows": rows,
            "R_ang": angs,
            "blows": angs[-1] > 3.0 * angs[0],
            "falls": angs[-1] < 0.5 * angs[0],
        }
    return _KILLERS


def lemma_angular_not_dominate() -> dict:
    scan = scan_packets()
    return rec(
        "B5b_tube_vs_viscosity",
        "angular 1/r² viscosity dominates I_tube at δ ∼ 2^{-j*} on the packet class",
        "fail" if not scan["dominates"] else "pass",
        "R_ang sits above 1 and climbs with j*. The extra 1/r² piece, alone, does not beat the source. Full D_tube still does (B4c).",
        R_ang=scan["R_ang"],
        R_D=scan["R_D"],
        rows=scan["rows"],
    )


def lemma_angular_climbs() -> dict:
    scan = scan_packets()
    ok = scan["climbs"] and scan["D_falls"]
    return rec(
        "B5c_angular_climbs",
        "on resolved packets, R_ang = |I_tube|/∫(u_θ/r)² climbs with j* while R_D falls",
        "pass" if ok else "fail",
        "Tesla’s knob on this write: turn j* up. Angular loses. Full dissipation wins. The two ratios disagree.",
        R_ang=scan["R_ang"],
        R_D=scan["R_D"],
    )


def lemma_killer_not_angular() -> dict:
    kill = scan_killers()
    return rec(
        "B5d_killer_not_angular_kill",
        "the slow fat swirl that killed B4b also kills angular domination",
        "fail" if not kill["blows"] else "open",
        "Turn ε down: R_ang falls. The B4b killer is not the B5b killer. Source slowed; (u_θ/r)² did not care.",
        R_ang=kill["R_ang"],
        falls=kill["falls"],
    )


def lemma_not_phi_cancel() -> dict:
    return rec(
        "B5e_not_a_phi_cancel",
        "angular 1/r² failing means cancel to Φ = Γ/r²",
        "fail",
        "B4c already budgets the packet with full ∇ω. Keep Γ. Keep 1/r^4. The extra angular term was not the absorption.",
    )


def lemma_angular_not_close() -> dict:
    return rec(
        "B5f_angular_not_X_a_priori",
        "the angular 1/r² piece closes a bound for classical X",
        "open",
        "A failed Poincaré is not continuation. Packet dissipation (B4c) is still a tube budget, not an a priori for X.",
    )


def lemma_angular_not_a_retune() -> dict:
    return rec(
        "B5g_not_a_pde_retune",
        "reading angular viscosity vs I_tube is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. No ε. No Φ. The ratio is a knob on the estimate.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_angular_not_dominate(),
        lemma_angular_climbs(),
        lemma_killer_not_angular(),
        lemma_not_phi_cancel(),
        lemma_angular_not_close(),
        lemma_angular_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "angular 1/r² viscosity vs I_tube",
            "tuning_the_pde": False,
            "tesla": "exacting, not a jerk. Turn j* up. Angular loses. Full dissipation does not.",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Coherent CONC (B16d): a packet with net P ≈ (ω·Sω)_+. "
            "B4c stands. Angular 1/r² does not. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_angular.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Angular 1/r² vs I_tube. The extra piece, alone, does not dominate.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
