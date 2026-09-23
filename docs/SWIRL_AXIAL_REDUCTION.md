# Swirl axial reduction — subclass only

Jonathan Simons  
Companion to the 11 September 2026 generic 3-D chain.

**This is not Step 7 of generic unaugmented 3-D Navier–Stokes.**  
**This is not a proof of global regularity, even on the subclass.**

The generic chain stops at \(T_{j\leftarrow j}\). Axisymmetric-with-swirl is a restriction of the data — route (C) on that chain — and is written here so it cannot be spliced back as a later generic step.

Generic face: [`docs/ns-review/UNAUG-GENERIC-3D-PROOF-CHAIN.md`](ns-review/UNAUG-GENERIC-3D-PROOF-CHAIN.md).

---

## Class

Axisymmetric with swirl, unaugmented:

\[
\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u,
\qquad
\nabla\cdot u=0,
\]

on \(\mathbb{R}^3\), velocity independent of the azimuthal angle, swirl component present. No extra field. No force. No \(Q\)-operator.

Bulk pairing is the same organization as Steps 2–4 of the generic chain (closed triads; shell budget; same-scale remainder named). The extra object is the axis.

---

## Axial remainder

Standing dictionary on this face: \(F=u^\theta/r\), \(G=\omega^\theta/r\). \(F\) is the intensive swirl \(\Phi\) of the Φ-renorm book. Do not reuse \(\Phi\) as any other symbol.

Near the axis the leftover is written

\[
T_{\mathrm{ax}}=\int_{r<\delta}G\,\partial_z(F^2)\,dm.
\]

This is the swirl-source term on a tube of radius \(\delta\). It is not \(T_{j\leftarrow j}\) of the generic chain, and it is not controlled by Lemma Star.

---

## Young condition (conditional)

\[
\int_0^T\|F\|_{L^4(B_\delta)}^4\,dt<\infty
\]

prevents blow-up from the swirl source. That is a condition, not a theorem that the integral stays finite.

The existing Φ-renorm book keeps the algebra \(\Gamma=r u_\theta\), \(\Phi=\Gamma/r^2=u_\theta/r\), and leaves the barrier \(\|u^r/r\|_{L^\infty}\) open. That barrier is equivalent to axisymmetric-with-swirl global regularity. This page does not close it.

Faces: [`docs/papers/swirl/`](papers/swirl/) · [`docs/ns-review/PHI-RENORM-WHAT-IS-KEPT.md`](ns-review/PHI-RENORM-WHAT-IS-KEPT.md).

---

## What this page refuses

- Inserting this note as “Step 7 of generic 3-D.”
- Using the axial Young condition as a generic (A) or (B).
- Claiming Clay Statement B, or even swirl global regularity, from the reduction.
- Gluing Φ-renorm, \(Q\), or an extra field into the generic chain.

**Subclass. Conditional. Not the generic remainder.**
