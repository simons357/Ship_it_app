#!/usr/bin/env python3
"""Three-lane certified uppers for the small-case attack. Not a proof."""

from pathlib import Path

import json
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
LANE_ORDER = ("near_single_shell", "separated_varied", "dense_packet")
LANE_LABEL = {
    "near_single_shell": "near-single-shell",
    "separated_varied": "separated, varied amp",
    "dense_packet": "dense coordinated packet",
}
LANE_COLOR = {
    "near_single_shell": "#0b5cab",
    "separated_varied": "#2a7f4f",
    "dense_packet": "#8a4b08",
}


def main(out_path: Path | None = None) -> Path:
    data = json.loads((ROOT / "results" / "da_gate_tc_l3_sqrt_yds.json").read_text())
    rows = [r for r in data["small_case"] if r.get("ratio_cert_upper") is not None]
    rows.sort(key=lambda r: -float(r["ratio_cert_upper"]))
    names = [r["name"] for r in rows]
    ups = [float(r["ratio_cert_upper"]) for r in rows]
    colors = [LANE_COLOR[r["lane"]] for r in rows]
    note_u = float(data["note_triad"]["ratio_cert_upper"])

    fig, ax = plt.subplots(figsize=(10.6, 5.2), facecolor="white")
    ax.barh(range(len(names)), ups, color=colors, edgecolor="none")
    ax.axvline(note_u, color="#b00020", ls="--", lw=1.2, label="note triad cert upper")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("certified upper |T_c| / (sqrt(X) sqrt(Y D_s))")
    ax.set_title(
        "Small-case attack: no certified counterexample. OPEN, not proved. NS not solved."
    )
    handles = [
        plt.Line2D([0], [0], color=LANE_COLOR[k], lw=6, label=LANE_LABEL[k]) for k in LANE_ORDER
    ]
    handles.append(plt.Line2D([0], [0], color="#b00020", ls="--", label="note triad cert upper"))
    ax.legend(handles=handles, frameon=False, fontsize=8, loc="lower right")
    ax.grid(True, axis="x", alpha=0.3)
    fig.tight_layout()
    if out_path is None:
        out_path = ROOT / "results" / "da_gate_tc_l3_small_case.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    print(main())
