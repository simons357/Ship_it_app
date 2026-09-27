#!/usr/bin/env python3
"""Desk figure for the Gate 83 lock and reduced-slice evidence."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

import da_gate_83_radical_trapping as g

ROOT = Path(__file__).resolve().parents[1]


def main(out_path: Path | None = None) -> Path:
    payload = g.run(n_starts=8)
    fig, ax = plt.subplots(figsize=(10.6, 6.2), facecolor="white")
    ax.axis("off")
    d = payload["decision"]
    sl = payload["frozen_z_exact"]
    cot = payload["first_order_cotangent"]
    sr = payload["local_search"]
    lines = [
        "Gate 83  —  radical / divisibility lock",
        "",
        "After gauge:  V = b2 * λ",
        "Question 83.34:  λ ∈ rad(I_act) at p_71E ?",
        "Certificate 83.35:  h λ^N = A·C + B·F,  h(p_71E) ≠ 0",
        "",
        f"83.34  {d['question_83_34']}",
        f"free-z (83.35) constructed: {d['explicit_certificate']}",
        f"frozen-z gcd: {sl['gcd']}   F1 ≡ 0: {sl['F1_identically_zero']}",
        f"no C1 volumetric branch: {cot['no_C1_volumetric_branch']}"
        f"  (A·dλ = {cot['left_null_dot_dlambda']:.3f})",
        f"nearby search: {sr['n_planar_active']} planar / "
        f"{sr['n_volumetric_active']} volumetric  (of {sr['n_active_hits']} hits)",
        "",
        "Gate 81 census: REPORTED, not recomputed.",
        "NS not solved.  DA-NS-2 open.",
    ]
    ax.text(0.04, 0.96, "\n".join(lines), va="top", ha="left", family="monospace", fontsize=11)
    fig.tight_layout()
    if out_path is None:
        out_path = ROOT / "results" / "da_gate_83_certificate.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    print(main())
