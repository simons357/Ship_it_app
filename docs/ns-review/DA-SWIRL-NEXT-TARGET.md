# DA swirl — locked next target

**Date:** 7 October 2026  
**Branch focus:** axisymmetric swirl (Shahmurov record geometry), **not** the 17/32 shared-budget package

---

## Desk assessment (accepted)

The 6 Oct four-doors bench is a **useful research note**: it kills failed shortcuts and states a precise remaining target. It is **not** regularity closure.

Feedback loop in plain English:

1. Swirl generates radial/vertical (meridional) motion  
2. That motion can squeeze swirl inward  
3. Inward squeeze can strengthen swirl  
4. Viscosity works against that concentration  

**Question that matters:** can inward squeezing be controlled over time on the **same evolving solution**?

### Two distinctions to keep

- Small energy + bounded initial gradients **do not** automatically make the swirl budget uniformly small (Gaussian family).  
- Viscosity **cannot** absorb every instantaneous compression by itself (amplitude scaling). An extra controlled term is required.

---

## The inequality to work

\[
\underbrace{C_F(t)}_{\text{signed compression}}
\;\le\;
\eta\,\nu\,D_F(t)
\;+\;
B(t)\,Q(t),
\qquad 0\le\eta<1,
\]

with

\[
Q=\int F^4\,dx,\qquad
\int_{t_0}^{T} B(t)\,dt
\text{ bounded from already controlled same-solution data.}
\]

If proved: controls \(Q\) from a chosen start time and pays \(\int Q\) on a finite interval.

**Unresolved part:** the independently bounded accumulation \(B\).  
Defining \(B\) from the same uncontrolled compression accomplishes nothing.

---

## Where to work on this branch

**Signed compression** — how much inward squeezing survives after accounting for outward motion and viscosity, along the same evolving solution.

Retain every localization / boundary-layer cost from the \(\chi\)-weighted \(G\) identity when localizing.

### Reject immediately

- Assuming the gate to prove the gate  
- Dropping a localization flux  
- Universal pure absorption \(C_F\le\eta\nu D_F\) for all data  
- Pretending frozen drift is full NSE  
- Claiming any Shahmurov door is closed  

---

## Status stamps

| Stamp | Value |
|---|---|
| NS / Clay | not solved |
| \(L^4\) gate from NSE | not proved |
| Four Shahmurov doors | all still open |
| This target | **OPEN — work here** |
| Shared-Budget 17/32 | separate track; ZIP recovered 7 Oct (`verify_families.py` passed); Priority 1 analytic review |

Full bench: `DA-SWIRL-FOUR-DOORS-2026-10-06.md`  
Phone sync: `PHONE-HANDOFF-2026-10-07.md`
