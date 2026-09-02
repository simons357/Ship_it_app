"""Historical toy only (filed 25 August 2026). Not live Domain Architect.

Not a proof of NS / RH / YM / BSD / Hodge. Clay is NOT CLAIMED.
Not June Paper2 FIXED. Not Ring SND (inf J/X >= c_*). Not Q6 H_N.
This slider phi is not swirl Phi = u_theta/r, not DA output Phi, not
Newtonian Phi_g, not Paper2 Phi_j.

The sine sum does not depend on x:
    phi += A * sin(2*pi*f*t/spatial_mod + delta)
so this is not a spatial field plot. Toy UI only.

Live product stays DECOMPOSE -> CROSS-DOMAIN TRANSLATE -> SYNTHESIZE
(docs/DOMAIN-ARCHITECT.md). SFE / UHF / DHFA / Harmonic Blueprint /
QStack are not canonical. Do not import into `domain_architect/`.
Do not add an Equation Explorer tab to the desktop app.
prime_field_coherence.py is also archive-only
(docs/archive/prime-field-2026-08-25/). UHSA dump already at
docs/archive/sfe-hb/.

Bytes below are Jon's 25 August 2026 chat paste. Archive only.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
# Define the Simons Field Equation function from the book
def simons_field(x, t, primes, amplitudes, frequencies, phases, spatial_mod):
    phi = np.zeros_like(x)
    for A, f, delta in zip(amplitudes, frequencies, phases):
        phi += A * np.sin(2 * np.pi * f * t / spatial_mod + delta)
    return phi
# Initial parameters inspired by SFE: primes for modes, golden ratio mod, etc.
init_primes = [2, 3, 5, 7, 11]  # Prime-indexed modes
x = np.linspace(0, 10, 1000)  # Space grid
init_t = 0.0  # Time
init_spatial_mod = 1.618  # ϕ(x) ~ golden ratio
init_amplitudes = [1 / np.sqrt(p) for p in init_primes]  # Normalized A_p
init_frequencies = init_primes  # f_p ∝ p
init_phases = np.zeros(len(init_primes))  # δ_p starts at 0
# Figure setup, styled like your dark cosmic visuals
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0a0a2a')  # Dark background
ax.set_facecolor('#0a0a2a')
plt.subplots_adjust(left=0.1, bottom=0.35)
line, = ax.plot(x, simons_field(x, init_t, init_primes, init_amplitudes, init_frequencies, init_phases, init_spatial_mod), color='cyan')
ax.set_title('Equation Explorer: Simons Field Φ(x,t)', color='white')
ax.set_xlabel('Space (x)', color='white')
ax.set_ylabel('Field Φ', color='white')
ax.tick_params(colors='white')
ax.grid(True, color='gray')
# Sliders for key variables (like your knobs/sliders: time t, spatial ϕ, phase δ0 for first mode—expand as needed)
ax_t = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor='lightgray')
slider_t = Slider(ax_t, 'Time t', 0.0, 10.0, valinit=init_t)
ax_phi = plt.axes([0.1, 0.20, 0.65, 0.03], facecolor='lightgray')
slider_phi = Slider(ax_phi, 'Spatial Mod ϕ', 0.1, 5.0, valinit=init_spatial_mod)
ax_delta0 = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor='lightgray')
slider_delta0 = Slider(ax_delta0, 'Phase δ (Mode 1)', 0.0, 2*np.pi, valinit=init_phases[0])
# Update func: Recalculates Φ on slider change, shows field evolution
def update(val):
    t = slider_t.val
    spatial_mod = slider_phi.val
    phases = list(init_phases)
    phases[0] = slider_delta0.val  # Tweak first phase; add more sliders for others
    y = simons_field(x, t, init_primes, init_amplitudes, init_frequencies, phases, spatial_mod)
    line.set_ydata(y)
    ax.set_ylim(y.min() - 1, y.max() + 1)  # Auto-scale for visibility
    fig.canvas.draw_idle()
slider_t.on_changed(update)
slider_phi.on_changed(update)
slider_delta0.on_changed(update)
# Apply/Reset button like your "APPLY"
reset_ax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(reset_ax, 'Apply/Reset', color='navy', hovercolor='cyan')
def reset(event):
    slider_t.reset()
    slider_phi.reset()
    slider_delta0.reset()
    update(None)  # Force apply
button.on_clicked(reset)
plt.show()
