# Lemma★: Mapping the Shape Center of Clay B

**Honest status (one line):** Lemma★ is **not proved**. Navier–Stokes on \(\mathbb{T}^3\) is **not solved**. The campaign mapped the right packaging — shape / \(\mathcal{R}_\star\) — and the door is still locked.

![Lemma★ barycenter — we mapped to the center; door still locked](./assets/lemma-campaign/lemma-star-barycenter.png)

---

## 1. What it is

Lemma★ is a **shape statement** about 3D incompressible Navier–Stokes on the torus, packaged so that a single geometric claim sits at the center of Clay Millennium Problem B (global regularity) **under this book**.

Read a fluid not only as “how large,” but as a **shape in frequency space**: how hard it stretches versus how much its energy is spread across shells. Viscosity packaging is an outer wrapper. After optimizing size, what remains is pure geometry on the shape.

**Packaging right ≠ prize won.** Proving Lemma★ would close Clay B *in this packaging*. That proof does not exist.

---

## 2. What it does

Define spectral moments on divergence-free Fourier fields, spectral scale \(\Lambda\), centered dissipation (spectral spread) \(\mathcal{D}_s\), and centered stretching \(T_c\). The canonical quotient is

\[
\mathcal{R}_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}
\qquad(\mathcal{D}_s>0).
\]

Lemma★ asserts a **finite geometric constant** \(C_{\mathrm{geom}}\) such that \(\mathcal{R}_\star\) stays bounded for **all** smooth shapes — equivalently

\[
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
\mathcal{D}_s(v)\,
\|v\|_2^2\,
Y(v).
\]

In words: stretching cannot outrun spectral spread by more than a universal shape constant. The equivalent viscosity form (energy-budget packaging) recovers after Young in \(\nu\); it is derived, not primary.

**Invariants that make this cool:** \(\mathcal{R}_\star\) is unchanged under amplitude rescaling and under uniform Fourier dilation. Size and viscosity cancel. What is left is geometry.

---

## 3. Where it lives

- **Domain:** 3D Navier–Stokes on \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\), divergence-free, frequency-space moments and triad transfers.
- **This repository:** Domain Architect (`DA-NS-1` / Lemma★ tooling), five-lane `ns_attacks` scripts and status locks, self-contained shape core (`ns_lemma_star_core`), unit tests that refuse greening language.
- **Related public trail (light touch):** earlier Ring Lemma / spectral geometry figures from the Zenodo spectral line sit behind the same research thread — triad rings, shell nesting, torus imagery — without claiming those archives close ★.

---

## 4. How the campaign worked

The work was organized as a **kill-or-prove** campaign, not a victory lap.

### Five-lane discipline

Simultaneous lanes with locked definitions, kill criteria, and status documents. Headline from the recovered five-lane run: K=0 absorption **dead**; Lemma★ \(C_{\mathrm{geom}}\) **not killed** by the search; HH→L **live bottleneck**; global regularity **not solved**.

![Attack 2 — K=0 blows; geometric ratios amp-invariant](./assets/lemma-campaign/amp_ratios_triad.png)

### Domain Architect (DA)

Books and welds record Lemma★ as **hypothesis**, Clay implication **conditional / withheld**, PRODUCT-BLOCK / HH→L **open**. DA refuses “almost proved,” “numeric survival ⇒ proved,” and greening language. That refusal is part of the scientific product.

### Attacks 9A–9D (neighborhood probes)

| Attack | Probe | Outcome |
| --- | --- | --- |
| **9A** | AP / coherent packet fan | Did **not** kill ★ — \(\mathcal{D}_s\) grew faster than stretching |
| **9B** | Exact / near-shell \(K_{\alpha,\beta}\) | Sample \(\max K\approx 0.641\) at \((4,8)\); restricted family ≠ full ★ |
| **9C** | Fixed-gap spheres | \(\mathcal{R}_\star\) fell \(0.11\to 0.031\); natural same-shell is **not** a kill |
| **9D** | Designed \(\Theta(m^2)\) locked-phase falsifier | Stub / **LIVE** kill attempt — not closed |

These are orbits around the barycenter, not the barycenter itself.

### Core numerics

![Attack 5 kill drill — survives numeric; kill threshold far above](./assets/lemma-campaign/attack5_bounds.png)

Attack 5 stress tests (hundreds of samples) kept ratios far below a kill threshold. Shape★ maxes on tested families were small. **A finite list of small \(\mathcal{R}_\star\) fields is not a supremum.** Failure to find a counterexample is not a proof. Kill lane remains **LIVE**.

---

## 5. Why it’s cool (without fake glory)

1. **Clear reduction.** One number, \(\mathcal{R}_\star\), carries the geometric claim. Amplitude and viscosity cancel → pure shape.
2. **Honest packaging of Clay B.** In this book, ★ is not a side lemma; it *is* the Millennium problem under the energy-budget / shape weld — and that weld is marked withheld until the product gap closes.
3. **Kill-or-prove clarity.** Live kill criteria are written: \(\mathcal{R}_\star\to\infty\) on a smooth family, or \(\mathcal{D}_s=0\) with \(T_c>0\), would kill ★. Surviving probes does not close the kill lane.
4. **Discipline.** Five-lane + DA status locks make it hard to quietly green a numeric sample into a theorem.
5. **Geometry you can see.** Triad rings, shell structure, and the barycenter map turn an abstract estimate into a picture of where the door sits.

![Finite triad ring — geometric core of the Ring Lemma line](./assets/lemma-campaign/fig_star_david_ring_lemma.png)

---

## 6. What we learned / what we do not claim

### Learned

- The **right center** is the shape statement: finite \(C_{\mathrm{geom}}\) / bounded \(\mathcal{R}_\star\) for **all** shapes.
- Naive K=0 “stretching ≤ viscous spread alone” is **dead**.
- Ordinary product / Agmon from energy alone does **not** close the gap; **HH→L** remains the analytic bottleneck.
- Several natural near-shell and packet families **failed to kill** ★ — interesting, not decisive.
- Tooling and status language matter: refuse greening; keep kill lane live until mathematics (or a true kill) decides.

### Do not claim

| Claim | Truth |
| --- | --- |
| Lemma★ proved | **No** |
| Navier–Stokes / Clay B solved | **No** |
| Millennium prize | **Not claimed; not won** |
| Kill lane closed | **No — still LIVE** |
| Uniform \(\mathcal{R}_\star\) / HH→L closed | **Still open** |
| Numeric survival = proof | **Refused** |

> We mapped to the center; door still locked.

---

## 7. Caption-ready figure list

Paths relative to this document; mirrors also under `/opt/cursor/artifacts/lemma-star-paper/`.

| # | File | Caption |
| --- | --- | --- |
| 1 | `assets/lemma-campaign/lemma-star-barycenter.png` | **Map to the barycenter.** Lemma★ center = finite \(C_{\mathrm{geom}}\) / bounded \(\mathcal{R}_\star\) for all shapes. Attacks 9A–9D are neighborhood probes. Door still locked. ★ not proved · NS not solved · kill lane LIVE. |
| 2 | `assets/lemma-campaign/amp_ratios_triad.png` | **Attack 2 hard hit.** K=0 ratio blows with amplitude; pre-Young and \(C_*\) ratios stay amplitude-invariant — geometry, not size. |
| 3 | `assets/lemma-campaign/attack5_bounds.png` | **Attack 5 kill drill.** Max ratios far below kill threshold on the sample. Survives numeric ≠ proved. |
| 4 | `assets/lemma-campaign/fig_star_david_ring_lemma.png` | **Finite triad ring** on a Littlewood–Paley shell — geometric core of the Ring Lemma / spectral line behind this campaign. |
| 5 | `assets/lemma-campaign/fig_three_spheres.png` | **Nested picture:** shell distribution → nonlinear transfer → vorticity / triad-ring geometry. |
| 6 | `assets/lemma-campaign/t3_torus_shape_render.png` | **Conceptual \(\mathbb{T}^3\) / shape atmosphere** (render, not a proof artifact). Optional cover visual. |

Full inventory: [`assets/lemma-campaign/IMAGE-INVENTORY.md`](./assets/lemma-campaign/IMAGE-INVENTORY.md).

---

## 8. Soft credit

Independent research by **Jonathan R. Simons**.

Tools and AI assistants were used for drafting, code, numerics harnesses, and status discipline. They did not invent the claim, and they do not green proofs.

No dunking on labs, models, or institutions. The standard here is the mathematics: clear packaging, honest status, live kill lane.

---

## Companion posts

- Paste-ready X thread: [`LEMMA-STAR-X-THREAD.md`](./LEMMA-STAR-X-THREAD.md)
- Short outline: [`LEMMA-STAR-FOR-X.md`](./LEMMA-STAR-FOR-X.md)
- Plain-English companion: [`LEMMA-STAR-IN-ENGLISH.md`](./LEMMA-STAR-IN-ENGLISH.md)
- DA packaging / blocker card: [`LEMMA-STAR-DA-NS-1.md`](./LEMMA-STAR-DA-NS-1.md)

**NS not solved. Lemma★ open. Recognition for the map — not for a prize that was not won.**
