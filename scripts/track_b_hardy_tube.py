#!/usr/bin/env python3
"""
Hardy → I_tube probes.

Packet class at δ ~ 2^{-j*}: dissipation can budget the tube source.
All-data domination: a slow fat swirl makes the ratio arbitrarily large.
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


def rz_grid(nr: int = 160, nz: int = 128, r1: float = 1.6):
    r = np.linspace(1e-4, r1, nr)
    z = np.linspace(0.0, 2.0 * math.pi, nz, endpoint=False)
    R, Z = np.meshgrid(r, z, indexing="ij")
    return r, z, R, Z


def integrate(field: np.ndarray, r: np.ndarray, z: np.ndarray) -> float:
    """∫ f r dr dz  (2π from θ dropped)."""
    weight = r[:, None]
    return float(np.trapezoid(np.trapezoid(field * weight, z, axis=1), r))


def swirl_fields(h: np.ndarray, r: np.ndarray, z: np.ndarray) -> dict:
    """Derivatives on the full field. Localize only when integrating."""
    dr = r[1] - r[0]
    dz = z[1] - z[0]
    hr = np.gradient(h, dr, axis=0)
    hz = np.gradient(h, dz, axis=1)
    wr = -hz
    wz = hr + h / r[:, None]
    wrr = np.gradient(wr, dr, axis=0)
    wrz = np.gradient(wr, dz, axis=1)
    wzr = np.gradient(wz, dr, axis=0)
    wzz = np.gradient(wz, dz, axis=1)
    source = 2.0 * h * hz / (r[:, None] ** 2)
    return {"source": source, "diss_density": wrr**2 + wrz**2 + wzr**2 + wzz**2}


def integrate_mask(
    field: np.ndarray, r: np.ndarray, z: np.ndarray, mask: np.ndarray | None
) -> float:
    if mask is not None:
        field = np.where(mask, field, 0.0)
    return integrate(field, r, z)


def masked_budget(h: np.ndarray, r: np.ndarray, z: np.ndarray, delta: float) -> dict:
    R, _Z = np.meshgrid(r, z, indexing="ij")
    fields = swirl_fields(h, r, z)
    tube = R < delta
    off = ~tube
    tube_i = integrate_mask(np.abs(fields["source"]), r, z, tube)
    tube_diss = integrate_mask(fields["diss_density"], r, z, tube)
    off_i = integrate_mask(np.abs(fields["source"]), r, z, off)
    full_i = integrate(np.abs(fields["source"]), r, z)
    full_diss = integrate(fields["diss_density"], r, z)
    idx = int(np.argmin(np.abs(r - delta)))
    wall_delta = 2.0 * float(np.trapezoid(h[idx] ** 2, z))
    return {
        "tube_i": tube_i,
        "tube_diss": tube_diss,
        "off_i": off_i,
        "wall_delta": wall_delta,
        "ratio_tube": tube_i / max(tube_diss, 1e-30),
        "full_ratio": full_i / max(full_diss, 1e-30),
    }


def packet_field(R: np.ndarray, Z: np.ndarray, ell: float, kappa: float) -> np.ndarray:
    """h = u_θ, Γ = r h. Smooth on the axis: h ∼ r."""
    return R * np.exp(-((R / ell) ** 2)) * np.sin(kappa * Z)


def killer_field(R: np.ndarray, Z: np.ndarray, eps: float) -> np.ndarray:
    """Slow fat swirl: solid-body radial profile, long z-wave."""
    return R * np.sin(eps * Z)


def scan_packets(jstars: tuple[int, ...] = (2, 3, 4, 5)) -> dict:
    r, z, R, Z = rz_grid()
    rows = []
    for j in jstars:
        ell = 2.0 ** (-j)
        kappa = 2.0**j
        h = packet_field(R, Z, ell, kappa)
        bud = masked_budget(h, r, z, delta=2.0 * ell)
        rows.append(
            {
                "jstar": j,
                "ell": ell,
                "kappa": kappa,
                "delta": 2.0 * ell,
                **bud,
            }
        )
    ratios = [row["ratio_tube"] for row in rows]
    # High-frequency packets should stay budgeted: ratio not exploding with j.
    decreasing = ratios[-1] <= ratios[0] * 1.05
    bounded = max(ratios) < 2.5
    return {
        "rows": rows,
        "ratios": ratios,
        "decreasing": decreasing,
        "bounded": bounded,
        "ok": decreasing and bounded,
    }


def scan_killers(epss: tuple[float, ...] = (1.0, 0.5, 0.25, 0.125, 0.0625)) -> dict:
    rows = []
    for eps in epss:
        # One full period, so the slow wave is periodic and np.gradient stays honest.
        r = np.linspace(1e-4, 1.6, 160)
        z = np.linspace(0.0, 2.0 * math.pi / eps, 192, endpoint=False)
        R, Z = np.meshgrid(r, z, indexing="ij")
        h = killer_field(R, Z, eps)
        bud = masked_budget(h, r, z, delta=1.0)
        rows.append({"eps": eps, **bud})
    ratios = [row["ratio_tube"] for row in rows]
    # Analytic target: |I|/diss ∼ 1/ε. Doubles when ε halves.
    blows = ratios[-1] > 3.0 * ratios[0] and ratios[-1] > 2.5
    return {"rows": rows, "ratios": ratios, "blows": blows, "ok_as_kill": blows}


def wall_match_packet(jstar: int = 3) -> dict:
    r, z, R, Z = rz_grid()
    ell = 2.0 ** (-jstar)
    h = packet_field(R, Z, ell, 2.0**jstar)
    delta = 2.0 * ell
    bud = masked_budget(h, r, z, delta)
    # Wall is the off-axis match: it should be a real, finite charge, not the whole I.
    wall = bud["wall_delta"]
    tube = bud["tube_i"]
    frac = wall / max(tube + wall, 1e-30)
    return {
        "jstar": jstar,
        "wall": wall,
        "tube_i": tube,
        "wall_over_tube_plus_wall": frac,
        "ok": 0.0 < wall and frac < 0.95,
    }


def lemma_packet_absorbed() -> dict:
    scan = scan_packets()
    return rec(
        "B4c_packet_hardy_tube",
        "3-shell / packet class at δ ∼ 2^{-j*}: |I_tube| is budgeted by tube vorticity dissipation",
        "pass" if scan["ok"] else "fail",
        "Same weight, both sides, at the packet scale. Ratio stays bounded and does not grow with j*.",
        scan=scan,
    )


def lemma_wall_match() -> dict:
    wall = wall_match_packet()
    return rec(
        "B4d_wall_matches_off_axis",
        "Hardy wall 2h(δ)² is a finite off-axis charge, not the whole tube integral",
        "pass" if wall["ok"] else "fail",
        "Spend the wall on r ∼ δ. That is the match I_off asked for.",
        wall=wall,
    )


def lemma_all_data_killed() -> dict:
    kill = scan_killers()
    return rec(
        "B4b_hardy_not_I_tube",
        "tube Hardy ⇒ |I_tube| absorbed in ν||∇ω||_2² for all data",
        "fail" if kill["ok_as_kill"] else "open",
        "Slow fat swirl: h = r sin(εz). Ratio |I_tube|/diss ∼ 1/ε blows as ε → 0. All-data domination is dead. Packet class still lives as B4c.",
        killer=kill,
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_packet_absorbed(),
        lemma_wall_match(),
        lemma_all_data_killed(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "Hardy → I_tube",
            "focused_problem": "B4b all-data vs B4c packet",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Use B4c inside 3-CONC. Then energy-class low Bony T on SPREAD. "
            "Do not revive all-data Hardy absorption."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_hardy_tube.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Hardy → I_tube. Packet class vs all-data.")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
