"""Headless runner for the SFE black-hole matplotlib toy.

Same kernel as sfe_field_paste.py. Does not call plt.show().
Writes mp4 and/or gif (and a still PNG) under --outdir.

This is a toy 2D animation. It is not GR, not a black hole, not
Navier-Stokes, and not a proof. Phi in the loop does not depend on
(x, y) — only t and the prime list. Spatial structure is only
Gamma = |Phi| / (r + 1e-5) then zeroing inside a disk.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np

# Import-safe: paste.py calls plt.show() at import time.
DEFAULT_PRIMES = [2, 3, 5, 7]


def sfe_field(x, y, t, primes=None, A=1.0, phi_mod=1.0, delta=0.0, epsilon=0.5):
    """Spatially constant sine sum of primes, then a radial disk mask.

    Phi is independent of (x, y). The mask zeros the constant inside
    r <= |Phi(t)| / epsilon (approximately; +1e-5 in the denominator).
    """
    if primes is None:
        primes = list(DEFAULT_PRIMES)
    Phi = np.zeros_like(x, dtype=float)
    for p in primes:
        f_p = p
        Phi += A * np.sin(2 * np.pi * f_p * t / phi_mod + delta)
    r = np.sqrt(x**2 + y**2)
    gamma = np.abs(Phi) / (r + 1e-5)
    Phi[gamma >= epsilon] = 0
    return Phi


def phi_scalar(t, primes=None, A=1.0, phi_mod=1.0, delta=0.0):
    """The actual field: a single number from t and the prime list."""
    if primes is None:
        primes = list(DEFAULT_PRIMES)
    total = 0.0
    for p in primes:
        total += A * np.sin(2 * np.pi * p * t / phi_mod + delta)
    return float(total)


def build_grid(n=100, span=10.0):
    x = np.linspace(-span, span, n)
    y = np.linspace(-span, span, n)
    return np.meshgrid(x, y)


def render_frame(t, n=100, span=10.0, epsilon=0.5):
    X, Y = build_grid(n=n, span=span)
    return sfe_field(X, Y, t, epsilon=epsilon)


def _save_animation(frames, interval_ms, out_path, writer_name, fps=None):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter

    fig, ax = plt.subplots()
    im = ax.imshow(frames[0], cmap="viridis", extent=(-10, 10, -10, 10), origin="upper")
    ax.set_title("SFE Black Hole Simulator: Coherence Collapse (toy)")
    fig.colorbar(im, ax=ax, label="Field Amplitude Phi")

    def update(i):
        im.set_array(frames[i])
        return [im]

    anim = FuncAnimation(fig, update, frames=len(frames), interval=interval_ms, blit=True)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if writer_name == "pillow":
        anim.save(out_path, writer=PillowWriter(fps=fps or max(1, int(1000 / interval_ms))))
    else:
        anim.save(out_path, writer=writer_name, fps=fps or max(1, int(1000 / interval_ms)))
    plt.close(fig)
    return out_path


def save_still(frame, out_path):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    im = ax.imshow(frame, cmap="viridis", extent=(-10, 10, -10, 10), origin="upper")
    ax.set_title("SFE Black Hole Simulator: Coherence Collapse (toy still)")
    fig.colorbar(im, ax=ax, label="Field Amplitude Phi")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return Path(out_path)


def default_outdir():
    artifacts = Path("/opt/cursor/artifacts")
    if artifacts.is_dir() or os.access(artifacts.parent, os.W_OK):
        return artifacts
    return Path.cwd() / "out"


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Headless SFE toy field animation (not a black hole).")
    p.add_argument("--frames", type=int, default=80, help="Frame count (paste used 200).")
    p.add_argument("--interval-ms", type=int, default=50, help="Frame interval in ms (paste used 50).")
    p.add_argument("--n", type=int, default=100, help="Grid points per axis.")
    p.add_argument("--outdir", type=Path, default=None)
    p.add_argument("--mp4", action="store_true", default=True)
    p.add_argument("--no-mp4", action="store_false", dest="mp4")
    p.add_argument("--gif", action="store_true", default=True)
    p.add_argument("--no-gif", action="store_false", dest="gif")
    p.add_argument("--still-only", action="store_true")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    outdir = args.outdir or default_outdir()
    outdir.mkdir(parents=True, exist_ok=True)

    times = [i / 10.0 for i in range(args.frames)]
    frames = [render_frame(t, n=args.n) for t in times]
    still = save_still(frames[0], outdir / "sfe_bh_sim_still.png")
    print(f"wrote {still}")

    if args.still_only:
        return 0

    fps = max(1, int(round(1000 / args.interval_ms)))
    written = []
    if args.mp4:
        mp4 = outdir / "sfe_bh_sim_coherence_collapse.mp4"
        try:
            _save_animation(frames, args.interval_ms, mp4, writer_name="ffmpeg", fps=fps)
            written.append(mp4)
            print(f"wrote {mp4}")
        except Exception as exc:
            print(f"mp4 failed ({exc!r}); will try gif", file=sys.stderr)

    if args.gif:
        gif = outdir / "sfe_bh_sim_coherence_collapse.gif"
        try:
            _save_animation(frames, args.interval_ms, gif, writer_name="pillow", fps=fps)
            written.append(gif)
            print(f"wrote {gif}")
        except Exception as extra:
            print(f"gif failed ({extra!r})", file=sys.stderr)

    if not written and not args.still_only:
        print("no animation writer succeeded; still PNG only", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
