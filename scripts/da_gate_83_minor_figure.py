#!/usr/bin/env python3
from pathlib import Path
import json
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main(out_path: Path | None = None) -> Path:
    data = json.loads((ROOT / "results" / "da_gate_83_minor_factor.json").read_text())
    fig, ax = plt.subplots(figsize=(10.4, 5.8), facecolor="white")
    ax.axis("off")
    p = data["pivot"]
    lines = [
        "Gate 83  specimen-1  8x8 minor",
        "",
        "M  ≢  0",
        "",
        f"specimen 1: t={data['specimen_1']['t']}  r={data['specimen_1']['r']}  "
        f"b={data['specimen_1']['b']}  d={data['specimen_1']['d']}",
        f"exact rank J_L = {data['specimen_1_exact_rank']}",
        f"rows {p['rows']}",
        f"drop column {p['drop_var']}",
        f"M = {p['exact_det']}",
        f"nonzero 9x9 minors: {data['n_nonzero_9x9_minors']} / 220",
        "",
        "factorization over Q[t,r1,r2,r3,b1,b2,d1,d2]: did not land",
        "NS not solved.",
    ]
    ax.text(0.04, 0.96, "\n".join(lines), va="top", family="monospace", fontsize=11)
    fig.tight_layout()
    if out_path is None:
        out_path = ROOT / "results" / "da_gate_83_minor.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    print(main())
