#!/usr/bin/env python3
"""Need★ — signed dual on HH→L after gap-cancel.

Gap-cancel is an identity. The signed dual bound is MISSING.
The machine checks the identity and refuses a fake close.
9D is secondary. Soft X silent. NS not solved. Lemma★ OPEN.
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
from ns_attacks.attack9b_exact_shell_K import (  # noqa: E402
    build_exact_shell_field,
    choose_closing_sign,
    closing_packet_from_PiB,
    combine_eps,
    normalize_field,
    project_B_to_shell,
    random_shell_params,
    shells_up_to,
)
from ns_attacks.stokes_moments import (  # noqa: E402
    Ds_two_shell,
    k_norm2,
    moments,
    nonlinear_B,
    probe,
    shell_energies,
    triad_Im_transfer,
)

ROOT = Path(__file__).resolve().parents[1]
WRITE = ROOT / "docs" / "NEED-STAR-HH-L-DUAL.md"

REFUSE_MARKERS = (
    "need★ is proved",
    "need star is a theorem",
    "signed dual sits as a bound",
    "gap-cancel is need★",
    "attack 12 is need★",
    "0.71 is need★",
    "ns is solved",
    "lemma★ is proved",
    "soft x closes",
    "five fingers close",
)


def classify_need_star_claim(text: str) -> dict:
    low = text.lower()
    hits = [m for m in REFUSE_MARKERS if m in low]
    audit = classify_paragraph(text)
    return {
        "refuse_hits": hits,
        "accepted_as_close": False,
        "allowed_as_write": len(hits) == 0 and audit["allowed_in_estimate"],
        "discard_hits": audit["discard_hits"],
        "signed_dual": "MISSING",
        "lemma_star": "KILLED",
    }


def shell_Tk(field) -> dict:
    out: dict[float, float] = {}
    for k, t in triad_Im_transfer(field).items():
        lam = float(k_norm2(k))
        out[lam] = out.get(lam, 0.0) + float(t)
    return out


def occupied_s(field, beta: float, tol: float = 1e-14) -> int:
    return sum(
        1
        for k, v in field.items()
        if abs(k_norm2(k) - beta) <= 1e-9 and float(np.linalg.norm(v)) > tol
    )


def score_field(field, alpha: float, beta: float, label: str) -> dict:
    m = moments(field)
    shells = shell_energies(field)
    tk = shell_Tk(field)
    e_a = float(shells.get(alpha, 0.0))
    e_b = float(shells.get(beta, 0.0))
    t_a = float(tk.get(alpha, 0.0))
    t_b = float(tk.get(beta, 0.0))
    e, x, y, ds = m["E"], m["X"], m["Y"], m["Ds"]
    gap = alpha - beta
    pred = -(gap * alpha * beta * e / x) * t_b if x > 0 else float("nan")
    r = probe(field, label=label)
    tc = float(r.Tc)
    ds2 = Ds_two_shell(alpha, beta, e_a, e_b)
    s = occupied_s(field, beta)
    cs = math.sqrt(beta) * e * math.sqrt(max(s, 0) * max(e_b, 0.0))
    denom = (alpha / math.sqrt(beta)) * e_a * math.sqrt(max(e_b, 0.0)) if beta > 0 else float("nan")
    n_star = abs(t_b) / denom if denom and denom > 0 else float("nan")
    reduced = (
        (alpha * beta * e * t_b * t_b) / (x * e_a * e_b * y)
        if x > 0 and e_a > 0 and e_b > 0 and y > 0
        else float("nan")
    )
    return {
        "label": label,
        "alpha": alpha,
        "beta": beta,
        "E": e,
        "X": x,
        "Y": y,
        "Ds": ds,
        "Ds_two_shell": ds2,
        "T_alpha": t_a,
        "T_beta": t_b,
        "T_alpha_plus_T_beta": t_a + t_b,
        "Tc": tc,
        "Tc_from_gap_cancel": pred,
        "gap_cancel_abs": abs(tc - pred),
        "R_star": float(r.ratio_box) if np.isfinite(r.ratio_box) else None,
        "R_star_after_gap_cancel": reduced,
        "s": s,
        "unsigned_CS": cs,
        "signed_over_CS": abs(t_b) / cs if cs > 0 else None,
        "N_star": n_star,
        "signed_dual": "MISSING",
    }


def aligned_hh_l_closer(alpha: int, beta: int, rng: np.random.Generator, eps: float = 0.05):
    """9B aligned closer on a lower output: the gap-cancel family."""
    shells = shells_up_to(max(int(alpha ** 0.5) + 3, 4))
    modes = shells.get(int(alpha), [])
    if len(modes) < 2:
        return {}
    params = random_shell_params(len(modes), rng)
    w = normalize_field(
        build_exact_shell_field(modes, params["amps"], params["thetas"], params["phis"])
    )
    PiB = project_B_to_shell(nonlinear_B(w), float(beta))
    if not PiB:
        return {}
    sign = choose_closing_sign(w, PiB)
    z = closing_packet_from_PiB(PiB, sign=sign)
    if not z:
        return {}
    return normalize_field(combine_eps(w, z, eps))


def run(seed: int = 1390) -> dict:
    rng = np.random.default_rng(seed)
    rows = []
    for alpha, beta in ((5, 4), (8, 4), (9, 4)):
        field = aligned_hh_l_closer(alpha, beta, rng)
        if not field:
            continue
        rec = score_field(field, float(alpha), float(beta), f"closer_{alpha}_{beta}")
        rec["family"] = "aligned_HH_to_L_closer"
        rows.append(rec)
    page = WRITE.read_text() if WRITE.exists() else ""
    claim = classify_need_star_claim(page)
    gap_ok = all(r["gap_cancel_abs"] < 1e-9 for r in rows) if rows else False
    energy_ok = all(abs(r["T_alpha_plus_T_beta"]) < 1e-9 for r in rows) if rows else False
    return {
        "need_star": "SIGNED_DUAL_MISSING",
        "gap_cancel_identity": bool(gap_ok and energy_ok),
        "n_fields": len(rows),
        "rows": rows,
        "max_N_star": max((r["N_star"] for r in rows if r["N_star"] == r["N_star"]), default=None),
        "max_signed_over_CS": max(
            (r["signed_over_CS"] for r in rows if r["signed_over_CS"] is not None),
            default=None,
        ),
        "claim": claim,
        "accepted_as_close": False,
        "ns_solved": False,
        "lemma_star": "KILLED",
        "kill_lane": "CLOSED_BY_V_N",
        "nine_d": "historical",
        "soft_x": "silent",
        "note": (
            "Gap-cancel sits. Unsigned CS hides s. "
            "Signed dual Need★ is MISSING. Cannot repair dead unrestricted ★. "
            "NS not solved."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--seed", type=int, default=1390)
    args = ap.parse_args()
    summary = run(seed=args.seed)
    print(json.dumps(summary, indent=2), flush=True)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(summary, indent=2))
        print(f"wrote {args.out}", flush=True)
    return 0 if summary["gap_cancel_identity"] and not summary["accepted_as_close"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
