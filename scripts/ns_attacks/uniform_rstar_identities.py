#!/usr/bin/env python3
"""Minimal identity / sanity probes for uniform R_★ close attempt.

Verifies (not proves PRODUCT-BLOCK):
  A. |T_c| <= sqrt(D_s) * ||A^{1/2} B||_2
  B. T_c = T_c_HH + T_c_HL + T_c_LL  (Λ-relative input split)
  C. Two-shell D_s = α β (α-β)^2 E_α E_β / X
  D. Amplitude invariance of R_★; false X^{3/2} product not invariant
  E. Light kill sanity: near-shell / two-shell / ball samples (finite)

Honesty: does NOT prove sup R_★ < ∞. Numerics ≠ proof.
Policy: docs/ns-review/RESEARCH-POLICY.md
Progress: docs/ns-review/UNIFORM-RSTAR-PROGRESS.md
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ns_lemma_star_core import (  # noqa: E402
    B_hat_at,
    Field,
    R_star,
    lam,
    moments,
    project_perp,
    shell_wavevectors,
    T_c_direct,
)
from uniform_rstar_attack import (  # noqa: E402
    T_c_lambda_channels,
    near_shell_field,
    triad_packet_field,
    two_shell_field,
)

ARTIFACT_DIR = Path("/opt/cursor/artifacts/uniform-rstar-close")


def _rand_perp(k, rng: np.random.Generator) -> np.ndarray:
    w = rng.normal(size=3) + 1j * rng.normal(size=3)
    return project_perp(k, w)


def Ahalf_B_norm2(field: Field) -> float:
    keys = list(field.modes.keys())
    ks = {
        (p[0] + q[0], p[1] + q[1], p[2] + q[2]) for p in keys for q in keys
    }
    ks.discard((0, 0, 0))
    total = 0.0
    for k in ks:
        Bk = B_hat_at(field, k)
        total += lam(k) * float(np.vdot(Bk, Bk).real)
    return total


def shell_energies(field: Field, n1: int, n2: int) -> tuple[float, float]:
    e1 = e2 = 0.0
    for k, vk in field.modes.items():
        e = float(np.vdot(vk, vk).real)
        lk = int(round(lam(k)))
        if lk == n1:
            e1 += e
        elif lk == n2:
            e2 += e
    return e1, e2


def check_cauchy(field: Field) -> dict:
    E, X, Y, Z, Lam = moments(field)
    Ds = Z - (Y * Y) / X if X > 0 else 0.0
    Tc = T_c_direct(field, Lam)
    AhB2 = Ahalf_B_norm2(field)
    bound = math.sqrt(max(Ds, 0.0)) * math.sqrt(max(AhB2, 0.0))
    return {
        "T_c": Tc,
        "D_s": Ds,
        "AhalfB2": AhB2,
        "cauchy_bound": bound,
        "cauchy_ok": bool(abs(Tc) <= bound + 1e-7 * max(1.0, bound)),
        "R_star_cauchy_upper": (AhB2 / (E * Y)) if E * Y > 0 else None,
    }


def check_two_shell_Ds(n1: int, n2: int, rng: np.random.Generator) -> dict:
    f = two_shell_field(n1, n2, rng, amp2=float(rng.uniform(0.2, 2.0)), per_shell=3)
    E, X, Y, Z, Lam = moments(f)
    Ds = Z - (Y * Y) / X
    Ea, Eb = shell_energies(f, n1, n2)
    formula = (n1 * n2 * ((n1 - n2) ** 2) * Ea * Eb) / X if X > 0 else 0.0
    rel = abs(Ds - formula) / max(abs(Ds), abs(formula), 1e-300)
    return {
        "n1": n1,
        "n2": n2,
        "D_s": Ds,
        "D_s_formula": formula,
        "rel_err": rel,
        "ok": bool(rel < 1e-10),
        "E_a": Ea,
        "E_b": Eb,
    }


def check_amplitude_invariance(rng: np.random.Generator) -> dict:
    f0 = None
    for _ in range(40):
        cand = triad_packet_field((1, 0, 0), (2, 1, 0), rng, amp_r=0.5)
        rec = R_star(cand, verify=True)
        if abs(float(rec["T_c"])) > 1e-12 and not rec.get("vacuous_single_shell"):
            f0 = cand
            break
    if f0 is None:
        return {"ok": False, "error": "no_nonzero_Tc_seed"}
    rows = []
    for a in (0.25, 1.0, 4.0):
        rec = R_star(f0.scale(a), verify=True)
        E, X = float(rec["E"]), float(rec["X"])
        Tc = float(rec["T_c"])
        v2 = math.sqrt(max(E, 0.0))
        prod = v2 * (X ** 1.5) if X > 0 else float("nan")
        rows.append(
            {
                "a": a,
                "R_star": None if rec["R_star"] == float("inf") else float(rec["R_star"]),
                "false_X32_ratio": (abs(Tc) / prod) if prod > 0 else None,
            }
        )
    rs = [r["R_star"] for r in rows if r["R_star"] is not None]
    fp = [r["false_X32_ratio"] for r in rows if r["false_X32_ratio"]]
    rs_spread = (max(rs) - min(rs)) / max(max(rs), 1e-300) if rs else None
    return {
        "rows": rows,
        "R_star_rel_spread": rs_spread,
        "false_product_max_over_min": (max(fp) / max(min(fp), 1e-300)) if fp else None,
        "ok": bool(rs_spread is not None and rs_spread < 1e-9),
        "note": "R_★ flat in a; false X^{3/2} ratio tracks ~1/a",
    }


def light_kill_sanity(rng: np.random.Generator) -> dict:
    samples = []
    # near-shell eps sweep
    for eps in (0.5, 0.1, 0.02):
        for _ in range(4):
            f = near_shell_field(5, 8, eps, rng)
            rec = R_star(f, verify=True)
            if not rec.get("vacuous_single_shell") and rec["R_star"] != float("inf"):
                samples.append(
                    {
                        "family": f"near_5_8_eps{eps}",
                        "R_star": float(rec["R_star"]),
                        "T_c": float(rec["T_c"]),
                    }
                )
    # two-shell
    for n1, n2 in ((1, 2), (5, 8), (2, 10)):
        for _ in range(6):
            f = two_shell_field(n1, n2, rng, amp2=1.0, per_shell=4)
            rec = R_star(f, verify=True)
            if not rec.get("vacuous_single_shell") and rec["R_star"] != float("inf"):
                samples.append(
                    {
                        "family": f"two_shell_{n1}_{n2}",
                        "R_star": float(rec["R_star"]),
                        "T_c": float(rec["T_c"]),
                    }
                )
    # triad
    for _ in range(12):
        f = triad_packet_field((1, 0, 0), (2, 1, 0), rng, amp_r=float(rng.uniform(0.2, 1.5)))
        rec = R_star(f, verify=True)
        if not rec.get("vacuous_single_shell") and rec["R_star"] != float("inf"):
            samples.append(
                {
                    "family": "triad_1_210",
                    "R_star": float(rec["R_star"]),
                    "T_c": float(rec["T_c"]),
                }
            )

    finite = [s["R_star"] for s in samples]
    max_rs = max(finite) if finite else None
    # Heuristic only: no claim that max is near the sup.
    kill_triggered = bool(max_rs is not None and max_rs > 1e3)
    return {
        "n_samples": len(samples),
        "max_R_star": max_rs,
        "kill_triggered_heuristic": kill_triggered,
        "kill_lane": "TRIGGERED_INVESTIGATE" if kill_triggered else "LIVE_no_family_found",
        "top": sorted(samples, key=lambda s: s["R_star"], reverse=True)[:8],
    }


def run(seed: int = 20260912) -> dict:
    rng = np.random.default_rng(seed)
    cauchy_rows = []
    channel_rows = []
    for label, builder in [
        ("triad", lambda: triad_packet_field((1, 0, 0), (2, 1, 0), rng, amp_r=0.7)),
        ("two_shell_1_2", lambda: two_shell_field(1, 2, rng, amp2=1.0, per_shell=4)),
        ("near_5_8", lambda: near_shell_field(5, 8, 0.15, rng)),
    ]:
        for j in range(4):
            f = builder()
            c = check_cauchy(f)
            c["family"] = f"{label}_{j}"
            cauchy_rows.append(c)
            ch = T_c_lambda_channels(f, theta=1.0)
            channel_rows.append(
                {
                    "family": f"{label}_{j}",
                    "channel_sum_err": ch["channel_sum_err"],
                    "ok": bool(ch["channel_sum_err"] < 1e-8 * max(1.0, abs(ch["T_c_full"]))),
                    "T_c_full": ch["T_c_full"],
                    "HH": ch["T_c_HH"],
                    "HL": ch["T_c_HL"],
                    "LL": ch["T_c_LL"],
                }
            )

    two_shell_rows = [
        check_two_shell_Ds(n1, n2, rng)
        for n1, n2 in ((1, 2), (1, 5), (5, 13), (2, 10))
    ]
    amp = check_amplitude_invariance(rng)
    kill = light_kill_sanity(rng)

    summary = {
        "attack": "uniform_rstar_identities_close_attempt",
        "seed": seed,
        "lemma_A_cauchy_all_ok": all(r["cauchy_ok"] for r in cauchy_rows),
        "lemma_B_channel_all_ok": all(r["ok"] for r in channel_rows),
        "lemma_C_two_shell_Ds_all_ok": all(r["ok"] for r in two_shell_rows),
        "lemma_D_amplitude_ok": amp.get("ok"),
        "max_channel_sum_err": max(r["channel_sum_err"] for r in channel_rows),
        "max_two_shell_Ds_rel_err": max(r["rel_err"] for r in two_shell_rows),
        "kill_sanity": kill,
        "status": {
            "PRODUCT_BLOCK": "OPEN",
            "uniform_R_star": "OPEN",
            "Lemma_star": "HYPOTHESIS",
            "Clay_Statement_B": "NOT_SOLVED",
            "HL_LL_classical": "OPEN_not_filed",
            "HH_bound": "OPEN",
            "kill_lane": kill["kill_lane"],
            "numerics_are_proof": False,
        },
        "progress_doc": "docs/ns-review/UNIFORM-RSTAR-PROGRESS.md",
        "note": (
            "Identity checks only. Does not prove PRODUCT-BLOCK. "
            "HL/LL not claimed classical. No Clay claim."
        ),
    }
    return {
        "summary": summary,
        "cauchy_rows": cauchy_rows,
        "channel_rows": channel_rows,
        "two_shell_Ds_rows": two_shell_rows,
        "amplitude_check": amp,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=20260912)
    ap.add_argument("--out-dir", type=str, default=str(ARTIFACT_DIR))
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = run(seed=args.seed)
    s = payload["summary"]

    (out_dir / "uniform_rstar_identities.json").write_text(
        json.dumps(payload, indent=2, default=str)
    )

    lines = [
        "uniform_rstar_identities — close-attempt sanity",
        s["note"],
        f"A cauchy_ok={s['lemma_A_cauchy_all_ok']}  "
        f"B channel_ok={s['lemma_B_channel_all_ok']}  "
        f"C two_shell_Ds_ok={s['lemma_C_two_shell_Ds_all_ok']}  "
        f"D amp_ok={s['lemma_D_amplitude_ok']}",
        f"max_channel_sum_err={s['max_channel_sum_err']!r}  "
        f"max_Ds_rel_err={s['max_two_shell_Ds_rel_err']!r}",
        f"kill: {s['kill_sanity']['kill_lane']}  "
        f"max_R*={s['kill_sanity']['max_R_star']!r}",
        f"status PRODUCT-BLOCK={s['status']['PRODUCT_BLOCK']}  "
        f"HL/LL={s['status']['HL_LL_classical']}  "
        f"HH={s['status']['HH_bound']}  "
        f"Clay={s['status']['Clay_Statement_B']}",
    ]
    text = "\n".join(lines) + "\n"
    (out_dir / "uniform_rstar_identities.txt").write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
