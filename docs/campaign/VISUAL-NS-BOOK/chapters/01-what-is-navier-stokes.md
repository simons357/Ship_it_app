# 01 — What is Navier–Stokes?

**Hero:** [`../../../ns-review/assets/lemma-campaign/t3_torus_shape_render.png`](../../../ns-review/assets/lemma-campaign/t3_torus_shape_render.png)

## Plain language

Imagine arrows filling a wrap-around box: at every point, “which way is the fluid going?” Navier–Stokes is the standard continuum model for a sticky, incompressible fluid — Newton’s laws written as PDEs. Our math question lives on that ideal model (here a 3-torus), not on a photograph of water.

## What the equation means (optional)

\[
\partial_t u+\mathbb{P}\bigl((u\cdot\nabla)u\bigr)=\nu\Delta u,\qquad
\nabla\cdot u=0.
\]

- \(\partial_t u\) — how the velocity field changes in time.  
- \((u\cdot\nabla)u\) — flow pushing flow (the nonlinear engine).  
- \(\mathbb{P}\) — Leray projector: pressure’s job of keeping the fluid incompressible, packaged cleanly.  
- \(\nu\Delta u\) — viscosity; the sticky smoothing.  
- \(\nabla\cdot u=0\) — no compression.

## Honesty

This book is a **map of a question**, not a claim that the question is answered. NS / Clay B is not solved here.
