#!/usr/bin/env python3
"""Two-panel certificate: near-shell sqrt(D_s) saturation vs v_n (star grows, new slot falls)."""

from pathlib import Path

import json
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main(out_path: Path | None = None) -> Path:
    data = json.loads((ROOT / "results" / "da_gate_tc_l3_sqrt_yds.json").read_text())
    ns = [r for r in data["near_shell"] if not r.get("empty_closer")]
    vn = data["growing_layer"]

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.4), facecolor="white")

    ax = axes[0]
    eps = [r["eps"] for r in ns]
    ax.plot(eps, [r["T_c_over_Ds"] for r in ns], "o-", color="#b00020", label="T_c / D_s")
    ax.plot(
        eps,
        [r["ratio_l3"] for r in ns],
        "s-",
        color="#0b5cab",
        label="|T_c| / (||grad u||_3 sqrt(Y D_s))",
    )
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel("near-shell eps (left = closer to the shell)")
    ax.set_ylabel("ratio")
    ax.set_title("exact obstruction: linear in D_s blows")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    n = [r["n"] for r in vn]
    ax.plot(n, [r["ratio_star"] for r in vn], "o-", color="#b00020", label="sqrt(R_star)")
    ax.plot(
        n,
        [r["ratio_l3"] for r in vn],
        "s-",
        color="#0b5cab",
        label="|T_c| / (||grad u||_3 sqrt(Y D_s))",
    )
    ax.set_xlabel("growing layer v_n")
    ax.set_ylabel("ratio")
    ax.set_title("v_n kills unrestricted star; new slot falls")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(True, alpha=0.3)

    fig.suptitle(
        "Candidate |T_c| <= C ||grad u||_3 sqrt(Y D_s)  —  OPEN, not proved.  NS not solved.",
        fontsize=11,
    )
    fig.tight_layout()
    if out_path is None:
        out_path = ROOT / "results" / "da_gate_tc_l3_sqrt_yds.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    print(main())
