# Exact 25 August 2026 chat paste (reconstructed from the arrived kernel).
# Snapshot only. Do not treat comments as physics. Headless runner:
#   sfe_field_headless.py
#
# Original hygiene notes (kept out of the kernel):
# - mutable default primes=[2, 3, 5, 7]
# - plt.show() at module bottom (hangs headless)
# - slogan comments were not promoted to theorems

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def sfe_field(x, y, t, primes=[2, 3, 5, 7], A=1.0, phi_mod=1.0, delta=0.0, epsilon=0.5):
    Phi = np.zeros_like(x)
    for p in primes:
        f_p = p
        Phi += A * np.sin(2 * np.pi * f_p * t / phi_mod + delta)
    r = np.sqrt(x**2 + y**2)
    Gamma = np.abs(Phi) / (r + 1e-5)  # Coherence pressure Γ (mimics black hole attractor)
    mask = Gamma >= epsilon
    Phi[mask] = 0  # Simulate phase collapse
    return Phi


x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)
fig, ax = plt.subplots()
im = ax.imshow(sfe_field(X, Y, 0), cmap="viridis", extent=(-10, 10, -10, 10))
ax.set_title("SFE Black Hole Simulator: Coherence Collapse")


def update(frame):
    im.set_array(sfe_field(X, Y, frame / 10))
    return [im]


ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.colorbar(im, label="Field Amplitude Phi")
plt.show()
