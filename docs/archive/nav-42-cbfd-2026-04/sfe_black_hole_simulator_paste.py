"""Historical toy only (queued 25 August 2026 with the NAV-42 dump).

Not live Domain Architect. Do not import into domain_architect/.
Do not add an Equation Explorer tab. Not Track A A_3. Not Clay.
This Phi is not swirl Phi=u_theta/r, not DA Phi, not Paper2 Phi_j.

SFE / UHF / DHFA stay archive. Sibling toy:
docs/archive/sfe-hb/equation_explorer_simons_field.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def sfe_field(x, y, t, primes=None, A=1.0, phi_mod=1.0, delta=0.0, epsilon=0.5):
    if primes is None:
        primes = [2, 3, 5, 7]
    Phi = np.zeros_like(x)
    for p in primes:
        f_p = p
        Phi += A * np.sin(2 * np.pi * f_p * t / phi_mod + delta)
    r = np.sqrt(x**2 + y**2)
    Gamma = np.abs(Phi) / (r + 1e-5)
    mask = Gamma >= epsilon
    Phi[mask] = 0
    return Phi


if __name__ == "__main__":
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    fig, ax = plt.subplots()
    im = ax.imshow(sfe_field(X, Y, 0), cmap="viridis", extent=(-10, 10, -10, 10))
    ax.set_title("SFE Black Hole Simulator: Coherence Collapse (archive toy)")

    def update(frame):
        im.set_array(sfe_field(X, Y, frame / 10))
        return [im]

    FuncAnimation(fig, update, frames=200, interval=50, blit=True)
    plt.colorbar(im, label="Field Amplitude Phi")
    plt.show()
