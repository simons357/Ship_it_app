# Turbulence intensity vs a no-actuation control

**Status:** a Domain Architect lab cycle, August 2026  
**Not 3D Navier–Stokes. Not a coating. Clay is NOT CLAIMED.**

The slogan “decrease turbulence” is **not** a recognized setpoint. A13
refuses it. This cycle writes the desired state the way inverse design
is allowed to: a concrete \(x\to x^\star\), compared against a
**control arm** with \(u=0\).

## Definition

- **State** \(x(t)\): lumped intensity analog. Not enstrophy of a field.
- **Plant:** \(\ddot x + 2\zeta\omega\dot x + \omega^2 x = \omega^2 x_{\mathrm{eq}} + u\)
- **Control arm:** \(u=0\). Equilibrium \(x_{\mathrm{eq}}\) (baseline).
- **Treated arm:** recognized setpoint \(x\to x^\star\) with
  \(x^\star=(1-r)x_{\mathrm{eq}}\), default \(r=1/2\). Saturated PD plus
  the feedforward \(\omega^2(x^\star-x_{\mathrm{eq}})\). Constraint \(|u|\le u_{\max}\).
- **Decreased vs control:** terminal treated \(x\) is below \(0.9\) of
  terminal control \(x\), treated arm settled, constraint held.

Computational gate is **on this analog only**.

## Run it

```
python -m domain_architect cycle turbulence-intensity
python -m domain_architect synthesize --target "decrease turbulence"
python -m domain_architect synthesize --target "x → 0.5" --constraint "|u| ≤ 6"
```

Desktop Cycle tab: **Intensity vs control**.

## What this does not do

- It does not decrease turbulence in a DNS or a tank.
- It does not validate a coating.
- It does not close NS-open.
- It does not make the slogan “decrease turbulence” a legal inverse-design target.
