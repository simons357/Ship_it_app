# Captions — visual journey

Accessible captions with expert-accurate math. No solved / unsolved stamps.

---

## 01 — Proof chain map

**File:** `figures/proof-chain.png` (also `.svg`, `.mmd`)

The main trunk runs classical Navier–Stokes on \(\mathbb{T}^3\) through spectral moments \(E,X,Y,Z\) and scale \(\Lambda=Y/X\), through the identities for spread \(D_s\) and centered cascade \(T_c\), into Lemma★ packaging and five-lane diagnostics, then through a product bound on \(T_c\) into continuation.

Dashed warm nodes are **open estimates** named as math objects (product bound on \(T_c\); \(\|u^r/r\|_\infty\) integrability on the Φ-renorm branch). The muted side node is optional SND / Ring Lemma texture — conditional shell bookkeeping, not a substitute for the product step.

---

## 02 — Chain status card

**File:** `figures/chain-status-card.png`

Same information as a status strip: colors mark whether a node is classical, an identity, packaging, an open estimate, or optional texture. Not a report card of grades. Not a verdict board.

---

## 03 — Barycenter map

**File:** `assets/lemma-star-barycenter.png` (alias `00-barycenter-map.png`)

Frequency-space picture of the shape packaging: spectral scale \(\Lambda\), spread \(D_s\), and the centered stretch \(T_c\) that feeds \(\mathcal{R}_\star=(T_c)_+^2/(D_s E Y)\). Neighborhood probes sit as orbits around that center; the center claim is the uniform shape bound.

---

## 04 — Stretch versus spread

**File:** `assets/03-tug-of-war-stretch-vs-spread.png`

Intuition for the shape quotient: upward cascade \((T_c)_+\) pulls against spectral spread \(D_s\). Lemma★ packaging says the dimensionless score stays geometrically controlled for all smooth shapes.

---

## 05 — Shape is not size

**File:** `assets/02-shape-ne-size.png`

Under \(v\mapsto a v\), numerator and denominator of \(\mathcal{R}_\star\) scale the same way — amplitude cancels. Uniform Fourier dilation likewise leaves the quotient unchanged. What remains is relative geometry among shells and triads.

---

## 06 — Viscosity wrapper

**File:** `assets/06-viscosity-melts-wrapper.png`

Energy-budget form places \(\nu\) in an outer Young wrapper:

\[
T_c\le\theta\nu D_s+C_0(\theta)\nu^{-1} E Y.
\]

After size optimization, the hard geometric content is the shape bound on \(\mathcal{R}_\star\).

---

## 07 — Nested shells

**File:** `assets/fig_three_spheres.png`

Shell nesting → triad transfer → vorticity geometry. Visual vocabulary for the spectral moments and for Ring Lemma / shell texture notes.

---

## 08 — Triad ring

**File:** `assets/fig_star_david_ring_lemma.png`

Finite triad geometry from the Ring Lemma spectral line. Useful atmosphere for the optional SND texture branch; not a claim that SND closes the product estimate.

---

## 09 — Torus atmosphere

**File:** `assets/t3_torus_shape_render.png`

The domain of the main trunk: divergence-free fields on \(\mathbb{T}^3\).

---

## 10 — Triad amplitude diagnostic

**File:** `assets/amp_ratios_triad.png`

Amplitude ratios on an explicit triad. Documents that pure viscous absorption \(T_c\le\theta\nu D_s\) cannot hold uniformly (ratio grows with amplitude). Separate from the open product estimate on the main chain.

---

## Φ-renorm callout (text figure)

Keep visible in any slide that shows the side branch:

- Identity: \(r^{-4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) — KEEP algebra.
- Dissipation label: \(\dot H^{1.3}\) (relabeled from the incorrect \(\dot H^{2.6}\) energy-norm reading).
- Open estimate: uniform \(\|u^r/r\|_{L^\infty}\) control.
