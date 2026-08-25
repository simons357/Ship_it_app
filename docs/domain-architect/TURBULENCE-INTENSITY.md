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
- **Industry standard** on this analog: no-actuation equilibrium
  \(x_{\mathrm{eq}}=1\). That is the control arm, \(u=0\).
- **Treated arm:** recognized setpoint \(x\to x^\star\) with
  \(x^\star=0.85\,x_{\mathrm{eq}}\) (**15% below** that industry baseline).
  Saturated PD plus the feedforward \(\omega^2(x^\star-x_{\mathrm{eq}})\).
  Constraint \(|u|\le u_{\max}\).
- **Decreased vs control:** terminal treated \(x\) is below \(0.9\) of
  terminal control \(x\), treated arm settled, constraint held.

Computational gate is **on this analog only**.

For a **hardware catalog** (riblets + discrete suction) with the same
analog 15% as a **desired** state, run `available-turbulence`
([`AVAILABLE-TURBULENCE.md`](AVAILABLE-TURBULENCE.md)).

## Run it

```
python -m domain_architect cycle turbulence-intensity
python -m domain_architect synthesize --target "decrease turbulence"
python -m domain_architect synthesize --target "x → 0.85" --constraint "|u| ≤ 6"
```

Desktop Cycle tab: **Intensity vs control**.

## What this does not do

- It does not decrease turbulence in a DNS or a tank.
- It does not validate a coating.
- It does not close NS-open.
- It does not make the slogan “decrease turbulence” a legal inverse-design target.
