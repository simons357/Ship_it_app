#!/usr/bin/env python3
"""Build stills + JSON for the Lemma★ object gallery.

Not a proof. NS is not solved. Samples are not C0.
Live stokes_moments.py is not imported.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.ns_lemma_star_core import (  # noqa: E402
    Field,
    K_of_w,
    R_star,
    build_closing_direction,
    random_shell_field,
    shell_wavevectors,
)

OUT = ROOT / "results" / "the_object"
APP_DATA = ROOT / "apps" / "the-object" / "data"
NINEB = ROOT / "results" / "ns_five_lane_2026-09-10" / "attack9b_exact_shell" / "attack9b.json"

ALPHA = 4
BETA = 8
SEED = 21


def _inner(a: Field, b: Field) -> complex:
    acc = 0j
    for k, vk in a.modes.items():
        acc += np.vdot(vk, b.get(k))
    return acc


def _orthogonalize(z: Field, other: Field) -> Field:
    ip = _inner(z, other)
    mis = Field()
    keys = set(z.support()) | set(other.support())
    for k in keys:
        mis.modes[k] = other.get(k) - ip * z.get(k)
    return mis.normalize(1.0)


def _pts(n: int):
    return [list(k) for k in shell_wavevectors(n, canonical_only=False)]


def _scan_eps(w: Field, z: Field, epss):
    rows = []
    for eps in epss:
        r = R_star(w.add(z.scale(float(eps))))
        rows.append(
            {
                "eps": float(eps),
                "R_star": float(r["R_star"]),
                "T_c": float(r["T_c"]),
                "D_s": float(r["D_s"]),
                "E": float(r["E"]),
                "Y": float(r["Y"]),
            }
        )
    return rows


def compute():
    rng = np.random.default_rng(SEED)
    w = random_shell_field(ALPHA, rng)
    z, raw = build_closing_direction(w, BETA)
    if z is None:
        raise RuntimeError("no closing direction on this seed")
    info = K_of_w(w, float(ALPHA), float(BETA))
    K = float(info["K"])
    rp = R_star(w.add(z.scale(1e-4)))
    rm = R_star(w.add(z.scale(-1e-4)))
    sign = 1.0 if rp["R_star"] >= rm["R_star"] else -1.0
    z = z.scale(sign)
    z_rand = random_shell_field(BETA, rng)
    z_mis = _orthogonalize(z, z_rand)

    epss = [0.2, 0.12, 0.08, 0.05, 0.03, 0.02, 0.01, 0.005, 0.002]
    aligned = _scan_eps(w, z, epss)
    misaligned = _scan_eps(w, z_mis, epss)

    samples = []
    s_rng = np.random.default_rng(1390)
    for i in range(36):
        wi = random_shell_field(ALPHA, s_rng)
        zi, raw_i = build_closing_direction(wi, BETA)
        if zi is None or raw_i <= 0:
            continue
        ki = K_of_w(wi, float(ALPHA), float(BETA))
        ri = R_star(wi.add(zi.scale(0.03)))
        rn = R_star(wi.add(zi.scale(-0.03)))
        use = ri if ri["R_star"] >= rn["R_star"] else rn
        samples.append(
            {
                "i": i,
                "K": float(ki["K"]),
                "R_star_eps": float(use["R_star"]),
                "T_c": float(use["T_c"]),
                "D_s": float(use["D_s"]),
            }
        )

    nineb = json.loads(NINEB.read_text())
    pairs = [
        {"alpha": p["alpha"], "beta": p["beta"], "K": p["K"]}
        for p in nineb["per_pair"]
        if p.get("K") is not None
    ]

    payload = {
        "ns_solved": False,
        "lemma_star": "OPEN",
        "kill_lane": "LIVE",
        "object": "Lemma-star shape quotient",
        "formula": "(T_c)_+^2 / (D_s E Y)",
        "caption": "A finite sample is not a bound. The uniform constant is open.",
        "featured": {
            "alpha": ALPHA,
            "beta": BETA,
            "seed": SEED,
            "K": K,
            "PiB_L2": float(info["PiB_L2"]),
            "E_w": float(info["E_w"]),
            "nineb_peak_K": nineb["max_K"]["K"],
            "nineb_peak_pair": [nineb["max_K"]["alpha"], nineb["max_K"]["beta"]],
        },
        "shells": {"alpha": _pts(ALPHA), "beta": _pts(BETA)},
        "aligned": aligned,
        "misaligned": misaligned,
        "samples": samples,
        "nineb_pairs": pairs,
        "sample_max_K": max((s["K"] for s in samples), default=float("nan")),
        "sample_max_R": max((s["R_star_eps"] for s in samples), default=float("nan")),
    }
    return payload


def _style():
    plt.rcParams.update(
        {
            "figure.facecolor": "#0b0d10",
            "axes.facecolor": "#0b0d10",
            "axes.edgecolor": "#3a4048",
            "axes.labelcolor": "#d7d2c8",
            "text.color": "#d7d2c8",
            "xtick.color": "#9a9488",
            "ytick.color": "#9a9488",
            "savefig.facecolor": "#0b0d10",
            "font.family": "serif",
        }
    )


def draw_shells(payload, path: Path):
    fig = plt.figure(figsize=(8.2, 8.2))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0b0d10")
    fig.patch.set_facecolor("#0b0d10")
    a = np.array(payload["shells"]["alpha"], dtype=float)
    b = np.array(payload["shells"]["beta"], dtype=float)
    ax.scatter(a[:, 0], a[:, 1], a[:, 2], c="#e2a35a", s=70, depthshade=True, label=r"shell $\alpha=4$")
    ax.scatter(b[:, 0], b[:, 1], b[:, 2], c="#7eb8c9", s=46, depthshade=True, label=r"shell $\beta=8$")
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.fill = False
        axis.pane.set_edgecolor("#2a3038")
    ax.grid(True, color="#2a3038")
    # a few chords from a point on α toward a sum on β
    if len(a) and len(b):
        p = a[0]
        for q in a[1:3]:
            s = p + q
            ax.plot(
                [p[0], s[0]],
                [p[1], s[1]],
                [p[2], s[2]],
                color="#c45c26",
                lw=1.1,
                alpha=0.85,
            )
    ax.set_title("The object in Fourier space", pad=12)
    ax.legend(loc="upper left", facecolor="#0b0d10", edgecolor="#3a4048")
    ax.set_xlabel(r"$k_1$")
    ax.set_ylabel(r"$k_2$")
    ax.set_zlabel(r"$k_3$")
    ax.view_init(elev=18, azim=38)
    ax.set_box_aspect((1, 1, 1))
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def draw_eps(payload, path: Path):
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ea = [r["eps"] for r in payload["aligned"]]
    ra = [r["R_star"] for r in payload["aligned"]]
    em = [r["eps"] for r in payload["misaligned"]]
    rm = [r["R_star"] for r in payload["misaligned"]]
    ax.semilogx(ea, ra, "o-", color="#e2a35a", lw=2, label="aligned closer")
    ax.semilogx(em, rm, "s--", color="#7eb8c9", lw=1.6, label="orthogonal closer")
    ax.axhline(payload["featured"]["K"], color="#c45c26", ls=":", lw=1.2, label=r"$K_{\alpha,\beta}$")
    ax.set_xlabel(r"$\varepsilon$")
    ax.set_ylabel(r"$\mathcal{R}_\star$")
    ax.set_title(r"Aligned closer recovers $K$. Orthogonal closer does not.")
    ax.legend(facecolor="#0b0d10", edgecolor="#3a4048")
    ax.grid(True, color="#2a3038", alpha=0.7)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def draw_machine(payload, path: Path):
    row = payload["aligned"][4]  # eps ~ 0.03
    parts = [
        (r"$(T_c)_+^2$", max(row["T_c"], 0.0) ** 2, "#e2a35a"),
        (r"$\mathcal{D}_s$", row["D_s"], "#7eb8c9"),
        (r"$E$", row["E"], "#c8c3b4"),
        (r"$Y$", row["Y"], "#9aa7b2"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 3.6))
    for ax, (lab, val, col) in zip(axes, parts):
        ax.bar([0], [val], color=col, width=0.55)
        ax.set_xticks([])
        ax.set_title(lab, fontsize=12)
        ax.set_xlim(-0.8, 0.8)
        ax.tick_params(axis="y", labelsize=8)
    fig.suptitle(
        r"$\mathcal{R}_\star=(T_c)_+^2/(\mathcal{D}_s\,E\,Y)$"
        + f"  =  {row['R_star']:.3f}   at  ε={row['eps']}",
        color="#d7d2c8",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def draw_samples(payload, path: Path):
    ks = [s["K"] for s in payload["samples"]]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.hist(ks, bins=10, color="#e2a35a", edgecolor="#0b0d10")
    ax.axvline(payload["featured"]["nineb_peak_K"], color="#c45c26", ls="--", label="9B peak (seed 1390)")
    ax.set_xlabel(r"$K_{4,8}(w)$ on random exact-shell $w$")
    ax.set_ylabel("count")
    ax.set_title("Samples raise a constant. They do not prove one exists.")
    ax.legend(facecolor="#0b0d10", edgecolor="#3a4048")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main():
    _style()
    OUT.mkdir(parents=True, exist_ok=True)
    APP_DATA.mkdir(parents=True, exist_ok=True)
    payload = compute()
    (OUT / "object.json").write_text(json.dumps(payload, indent=2))
    (APP_DATA / "object.json").write_text(json.dumps(payload, indent=2))
    (APP_DATA.parent / "data.js").write_text(
        "window.OBJECT_DATA = " + json.dumps(payload) + ";\n"
    )
    draw_shells(payload, OUT / "object_shells.png")
    draw_eps(payload, OUT / "object_aligned.png")
    draw_machine(payload, OUT / "object_quotient.png")
    draw_samples(payload, OUT / "object_samples.png")
    for name in (
        "object_shells.png",
        "object_aligned.png",
        "object_quotient.png",
        "object_samples.png",
    ):
        dest = APP_DATA.parent / "stills" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((OUT / name).read_bytes())
    print(
        json.dumps(
            {
                "featured_K": payload["featured"]["K"],
                "sample_max_K": payload["sample_max_K"],
                "n_samples": len(payload["samples"]),
                "ns_solved": payload["ns_solved"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
