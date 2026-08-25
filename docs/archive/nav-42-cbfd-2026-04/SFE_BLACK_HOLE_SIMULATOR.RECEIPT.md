> **Archive receipt (25 August 2026).** Chat paste titled *SFE Black Hole
> Simulator: Coherence Collapse*. **Track C only.** Not Domain Architect.
> Not Track A \(A_3\). Clay **NOT CLAIMED**. Do **not** add an Equation
> Explorer tab. Do **not** import into `domain_architect/`. This \(\Phi\)
> is **not** swirl \(\Phi=u_\theta/r\).

# SFE black-hole matplotlib paste — arrived

## What arrived

This chat is the numpy / matplotlib `FuncAnimation` snippet:

- `sfe_field(x, y, t, primes=[2,3,5,7], …)`
- title *SFE Black Hole Simulator: Coherence Collapse*
- `Gamma = abs(Phi) / (r + 1e-5)`; `Phi[Gamma >= epsilon] = 0`

Those bytes were already queued and filed as
[`sfe_black_hole_simulator_paste.py`](sfe_black_hole_simulator_paste.py).
This message is the **same kernel**. It is now marked **arrived**, like
`qc_coherence` paste 3 matching paste 1.

Archive hygiene already applied (keep it):

- mutable default `primes=[2,3,5,7]` sanitized to `primes=None`
- comments calling the mask a black-hole attractor were **not** promoted
  to a theorem
- `__main__` only; importing the module does not call `plt.show()`

Sibling toy (same sine-sum bug, slider UI):
[`docs/archive/sfe-hb/equation_explorer_simons_field.py`](../sfe-hb/equation_explorer_simons_field.py).

## What the kernel actually does

The harmonic sum is **independent of \(x\) and \(y\)**:

```
Phi += A * sin(2 * pi * f_p * t / phi_mod + delta)
```

So \(\Phi(\cdot,t)\) is spatially constant before the mask. The only spatial
structure is a **disk**: \(\Gamma\ge\varepsilon\) iff \(r\le|\Phi(t)|/\varepsilon\).
Inside the disk the constant is zeroed. That is a radial threshold on a
flat field, **not** a PDE, **not** GR, **not** an event horizon.

Comments in the chat paste (`# Coherence pressure Γ (mimics black hole
attractor)`, `# Simulate phase collapse`) are slogans. They do **not**
make a Schwarzschild spacetime or an NS collapse criterion.

## What this is not

- **Not** live Domain Architect. Do not add a simulator tab.
- **Not** Track A: \(A_{\omega S}\), \(A_3\), \(D_\xi\), \(H_{NS}\).
- **Not** swirl \(\Phi=u_\theta/r\). **Not** DA output \(\Phi\).
  **Not** Newtonian \(\Phi_g\). **Not** Paper2 \(\Phi_j\).
- **Not** Paper2 operator SND. **Not** Ring \(\inf J/X\). **Not** Q6 \(H_N\).
- **Not** the NS PDE. **Not** Clay. Clay is **NOT CLAIMED**.
- **Not** June Paper2 FIXED. **Not** a rewrite of `docs/DOMAIN-ARCHITECT.md`.

Live product stays DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE
([`docs/DOMAIN-ARCHITECT.md`](../../DOMAIN-ARCHITECT.md)).
SFE / UHF / DHFA stay archive.
