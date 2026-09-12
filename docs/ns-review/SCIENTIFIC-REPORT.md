# Scientific report — Navier–Stokes packaging (Lemma★ / DA-NS-1)

**Audience:** technical readers (Jonathan R. Simons and method reviewers)  
**Scope:** Clay Millennium Problem, Navier–Stokes regularity (mild / Statement B packaging on \(\mathbb{T}^3\))  
**Honesty lock:** Lemma★ / DA-NS-1 is a **HYPOTHESIS**, not a theorem. Clay Statement B is **not solved**. Numerics are **not** proofs.  
**Contamination rule:** this file is scientific only — no campaign, outreach, or metaphor framing.

**Primary companions in this folder:**

- [`PROOF-CHAIN-CLEAN.md`](./PROOF-CHAIN-CLEAN.md) — definitions, identities, open product / shape node  
- [`PHI-RENORM-WHAT-IS-KEPT.md`](./PHI-RENORM-WHAT-IS-KEPT.md) — separate Φ-renorm KEEP card (do not glue)  
- [`PHI-RENORM-AUDIT-2026-08-22.md`](./PHI-RENORM-AUDIT-2026-08-22.md) — independent swirl-paper audit  
- Attack / probe code: [`scripts/ns_attacks/`](../../scripts/ns_attacks/)

Science content formerly mixed into campaign-titled notes (e.g. `MONDAY-DOOR-SPRINT.md`) is restated here without that framing. Prefer this report + `PROOF-CHAIN-CLEAN.md` as the scientific face.

---

## 1. Problem statement (Clay NS regularity, mild form)

Clay Millennium Problem Statement B (Navier–Stokes, smooth / mild data, periodic setting used here): show that smooth, divergence-free, mean-zero initial data on the 3-torus

\[
\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3
\]

produce a unique smooth solution for all positive times (global regularity), or exhibit a smooth blowup. Classical NSE:

\[
\partial_t u+\mathbb{P}\bigl((u\cdot\nabla)u\bigr)=\nu\Delta u,\qquad
\nabla\cdot u=0,\qquad \nu>0.
\]

This repository packages one **conditional** route to Statement B via a uniform shape / energy-budget inequality (Lemma★ / DA-NS-1). Packaging a prize problem is not solving it.

---

## 2. Objects

Let \(P\) be the Leray projector, \(A=-P\Delta\), \(B(v,v)=P[(v\cdot\nabla)v]\). For a smooth mean-zero divergence-free field \(v\) (shape), or a strong solution \(u(t)\) (energy-budget wrapper):

\[
\begin{aligned}
E&=\|v\|_2^2,\\
X&=\|A^{1/2}v\|_2^2,\\
Y&=\|Av\|_2^2,\\
Z&=\|A^{3/2}v\|_2^2,\\
\Lambda&=\frac{Y}{X}\quad(X>0).
\end{aligned}
\]

| Symbol | Role |
| --- | --- |
| \(E\) | kinetic energy |
| \(X\) | enstrophy scale (\(\|\nabla v\|_{L^2}^2\) up to constants) |
| \(Y,Z\) | higher Stokes moments |
| \(\Lambda\) | spectral scale (enstrophy-weighted mean eigenvalue) |

On \(\mathbb{T}^3\) with mean zero, \(\Lambda\ge 1\). Plancherel / Cauchy–Schwarz: \(X\le E\Lambda\).

**Spectral spread**

\[
D_s=Z-\Lambda Y=Z-\frac{Y^2}{X}
=\bigl\|(A-\Lambda)A^{1/2}v\bigr\|_2^2\ge 0.
\]

**Centered cascade / stretching**

\[
N=-\langle B(v,v),Av\rangle,\quad
M=-\langle AB(v,v),Av\rangle,\quad
T_c=M-\Lambda N=-\langle B(v,v),A(A-\Lambda)v\rangle.
\]

Write \((T_c)_+=\max(T_c,0)\). Only upward stretch enters the shape quotient.

**Identity (algebra; proved along strong solutions)**

\[
\Lambda'=\frac{2}{X}\bigl(T_c-\nu D_s\bigr).
\]

Single-shell fields: \(D_s=0\) and \(T_c=0\) (vacuous for the shape quotient).

**Shape quotient**

\[
\mathcal{R}_\star(v)=\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,E\,Y}
\quad(D_s E Y>0).
\]

\(\mathcal{R}_\star\) is invariant under amplitude \(v\mapsto a v\) and under uniform Fourier dilation.

Executable finite-support Fourier formulas: `scripts/ns_attacks/ns_lemma_star_core.py`.

---

## 3. Lemma★ / DA-NS-1 — statement and status

### 3.1 Shape form (primary hypothesis)

**Claim (OPEN):** there exists a geometric constant \(C_{\mathrm{geom}}<\infty\) such that for every smooth nonzero divergence-free \(v\),

\[
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
D_s(v)\,
E\,
Y.
\]

Equivalently: \(\sup_v\mathcal{R}_\star(v)<\infty\).

### 3.2 Energy-budget form (Young wrapper)

For \(0<\theta<1\),

\[
T_c(u)
\le
\theta\nu\,D_s(u)
+C_0(\theta)\,\nu^{-1}\,E\,Y,
\qquad
C_{\mathrm{geom}}=4\theta\,C_0(\theta).
\]

(Equivalent bookkeeping with remainder \(C_0\nu^{-1} E X\Lambda\) appears in some notes; after \(X\le E\Lambda\) the wrappers are interchangeable up to constants.)

Registry ASCII (conceptual):  
`T_c <= theta*nu*(Z - Lambda*Y) + C_0*nu^{-1}*||u||_2^2*X*Lambda`

**Status:** **HYPOTHESIS**. Domain Architect label for this packaging: **DA-NS-1**. Do not green as PROVED.

### 3.3 Conditional implication (one direction — proved as an implication)

**If** the energy-budget form holds with geometric \(C_0\), then along any strong-solution interval with \(E(t)\le E(0)\),

\[
\Lambda(t)\le\Lambda(0)\exp\bigl(C\,\nu^{-1} E(0)\,t\bigr),
\]

hence \(X(t)\) stays finite and smooth solutions continue. Thus **Lemma★ ⇒ global regularity** in this packaging.

**Not proved:** converse (global regularity ⇒ uniform \(\mathcal{R}_\star\) over every smooth field). Do not write “★ ≡ GR.”

---

## 4. Open node: PRODUCT-BLOCK (the last door on this trunk)

**Where it sits in the chain.** After spectral moments → \(D_s\), \(T_c\), \(\Lambda'\) identity → Lemma★ packaging, the **last open analytic node** on the main trunk is PRODUCT-BLOCK. Closing it is what would turn the energy-budget form into a usable Gronwall ceiling on \(\Lambda(t)\). Everything after that arrow (continuation / Statement B packaging) is conditional on this node.

**Break ID:** PRODUCT-BLOCK (legacy name retained).  
**Live mathematical target:** uniform control of the shape quotient,

\[
\sup_v\mathcal{R}_\star(v)<\infty
\quad\text{(equivalently finite geometric \(C_{\mathrm{geom}}\) / \(C_0\))}.
\]

**Analytic bottleneck:** Bony high×high input channel control for the signed triad sum defining \(T_c\) (historical diagnostic label “HH→L” / HH input channel). Ordinary 3D Sobolev / Agmon estimates from energy alone do **not** close the bound for all \(v\).

### 4.0 Legal directions (analytic routes only)

These are the legitimate ways to attack the node — estimates, structure, and honest conditionals. No slogan closes it.

1. **Primary target:** prove \(\sup_v\mathcal{R}_\star(v)<\infty\) with a geometry-only constant (shape form), **or** an equivalent Young energy-budget form with geometric \(C_0(\theta)\).
2. **Structure on \(T_c\):** rewrite the triad \(T_c=M-\Lambda N\) to expose cancellations; remove or dominate the worst high×high input piece.
3. **HH-channel budget:** bound only the HH contribution to \(T_c\); treat HL/LL by classical products if available.
4. **Conditional paper (honest):** Lemma★ under an explicit HH / shell / SND hypothesis — labeled conditional, not Clay.
5. **Negative control:** search for smooth families with \(\mathcal{R}_\star\to\infty\); if found, packaging dies and must be recorded.
6. **Do not:** revive false universal products (see §4.1), glue SFE↔NS, or treat numeric survival as a theorem.

### 4.1 Discarded false product target (do not revive)

A once-proposed universal estimate

\[
|T_c|\le C\|v\|_2\,X^{3/2}
\]

is **algebraically false** as a scale-invariant universal bound: under \(v\mapsto a v\), LHS scales as \(a^3\) while RHS scales as \(a^4\). Archive only. Schematic “product-class” language in older notes must be read as pointing at structure that feeds Young in \(\nu\), **not** as endorsing that false inequality.

Related schematic forms such as \(|T_c|\lesssim\|v\|_2 X\Lambda\) are post-Young / amplitude-sensitive objects; they are **not** substitutes for \(\sup\mathcal{R}_\star<\infty\).

### 4.2 What five-lane / probes say (stress tests, not proofs)

| Lane / claim | Status |
| --- | --- |
| Pure viscous absorption \(T_c\le\theta\nu D_s\) (K=0) | **DEAD** (amplitude scaling) |
| Uniform \(\mathcal{R}_\star\) / geometric \(C_{\mathrm{geom}}\) | **OPEN** (survives numeric kill on tested families ≠ proved) |
| HH-channel product structure | **GAP (live)** |
| Near-shell \(K_{\alpha,\beta}\) (Attack 9B) | Restricted family probe only ≠ full ★ |
| Clay Statement B / global regularity | **NOT SOLVED** |

Reproducible probes (no campaign framing required):

```bash
python3 scripts/ns_attacks/uniform_rstar_attack.py   # Λ-relative HH/HL/LL + maximizers
python3 scripts/ns_attacks/product_bound_probe.py
python3 scripts/ns_attacks/run_all_five.py   # if dependencies resolve
python3 -m pytest -q tests/test_proof_chain_visual.py
```

Core module: `scripts/ns_attacks/ns_lemma_star_core.py`. Focused uniform-\(\mathcal{R}_\star\) attack note: [`UNIFORM-RSTAR-ATTACK.md`](./UNIFORM-RSTAR-ATTACK.md). Locked research policy (analytic main path; no HPC arms race): [`RESEARCH-POLICY.md`](./RESEARCH-POLICY.md). Individual attack scripts live under `scripts/ns_attacks/` (`attack1_…` through `attack9b_…`, plus `uniform_rstar_attack.py`).

### 4.3 Analytic reduction (attack map — not a theorem)

Λ-relative input split \(T_c=T_c^{\mathrm{HH}}+T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}}\) (mode high iff \(\lambda_k\ge\theta\Lambda\)). **If** both HL/LL and HH admit geometric bounds against \(D_s E Y\), then \(\sup\mathcal{R}_\star<\infty\). Close-attempt progress: Cauchy / channel / dilation / HH-mass lemmas proved; elementary unmatched-Λ HL/LL route **killed**; Cauchy-only \(\sup Q<\infty\) **strategically blocked** by face family (large \(Q\), \(T_c=0\)); geometric HL/LL and HH still unbound; no \(\mathcal{R}_\star\to\infty\) kill. Publisher/X gate **CLOSED**. Details: [`UNIFORM-RSTAR-PROGRESS.md`](./UNIFORM-RSTAR-PROGRESS.md), [`GATED-PUBLISH-CHECKLIST.md`](./GATED-PUBLISH-CHECKLIST.md).

---

## 5. Proved vs hypothesized vs parked

| Item | Classification |
| --- | --- |
| Spectral-moment definitions; \(D_s\ge 0\); \(T_c=-\langle B,A(A-\Lambda)v\rangle\); \(\Lambda'=2(T_c-\nu D_s)/X\) | **Proved algebra** (along strong solutions where stated) |
| Pure viscous absorption false (amplitude blowup of \(T_c/D_s\)) | **Proved** (explicit triad families) |
| Young reduction of \(|T_c|\) into \(\varepsilon D_s + C_\varepsilon\|A^{1/2}B\|_2^2\) | **Proved** (Plancherel + pointwise Young) |
| Lemma★ ⇒ GR (conditional implication) | **Proved as implication**; hypothesis open |
| Uniform \(\sup\mathcal{R}_\star<\infty\) / finite \(C_{\mathrm{geom}}\) | **HYPOTHESIS** (PRODUCT-BLOCK) |
| Five-lane / packet / near-shell numeric ceilings | **Evidence only** — not theorems |
| Φ-renorm identity \(\partial_z(\Gamma^2)/r^4=\partial_z(\Phi^2)\) | **KEEP algebra**; barrier \(\int\|u^r/r\|_\infty\,dt\) **open** |
| Φ-renorm ⇔ Lemma★ glue | **INCOMPATIBLE / refuse** |
| SFE ↔ NS glue | **INCOMPATIBLE / refuse** |
| SND / Ring Lemma unconditional Statement B | **PARK** (conditional texture only) |
| RH / ARCHON Statement B greening | **PARK** (RH not proved; ARCHON parked) |
| Clay B “proved” deposits | **PARK / withdrawn** where so marked in Zenodo remediation |

---

## 6. Numerics ≠ proof

Finite-support Fourier probes, two-shell \(K_{\alpha,\beta}\) tables, and bounded \(\mathcal{R}_\star\) on sampled families:

- can **fail to kill** ★ on those samples;
- cannot establish \(\sup_v\mathcal{R}_\star<\infty\);
- cannot close PRODUCT-BLOCK;
- cannot claim Clay Statement B.

A smooth family with \(\mathcal{R}_\star(v_n)\to\infty\) would **kill** the packaging. Absence of such a family in tests leaves the kill lane **LIVE** and the proof lane **OPEN**.

---

## 7. Adjacent books (kept separate)

**Φ-renorm (axisymmetric-with-swirl).** Extensive / intensive swirl \(\Gamma=r u_\theta\), \(\Phi=\Gamma/r^2\). KEEP algebraic identity; open barrier equivalent in difficulty to axisymmetric-with-swirl global regularity. See [`PHI-RENORM-WHAT-IS-KEPT.md`](./PHI-RENORM-WHAT-IS-KEPT.md). **Do not glue** to Lemma★ PRODUCT-BLOCK.

**SND texture.** Conditional shell-concentration bookkeeping. Optional side texture; not a substitute for uniform \(\mathcal{R}_\star\); not a glue from arithmetic programs into classical NS.

**Domain Architect (DA).** Software / Functional Role Analysis for equation audits. “DA REJECT” means the **tool / method** refuses greening a claim — not a person. On the present mainline CLI, NS packaging symbols typically reach only **Level 0** coherent classification (parser limits); see [`DA-AUDIT.md`](./DA-AUDIT.md).

---

## 8. Reading order

1. This report (status + honesty locks).  
2. [`PROOF-CHAIN-CLEAN.md`](./PROOF-CHAIN-CLEAN.md) (full definitions and chain).  
3. `scripts/ns_attacks/ns_lemma_star_core.py` + `product_bound_probe.py` (reproducibility).  
4. Φ-renorm KEEP / audit cards if working the swirl branch (separate).  
5. Method-seat review: [`METHOD-PANEL-REVIEW.md`](./METHOD-PANEL-REVIEW.md).

---

## 9. One-line status

**Lemma★ / DA-NS-1 = HYPOTHESIS, blocked at PRODUCT-BLOCK (uniform \(\mathcal{R}_\star\)). HL/LL and HH both OPEN geometrically; Cauchy-only \(\sup Q\) strategically blocked. NS / Clay B not solved. SFE incompatible. RH / ARCHON parked. Publisher gate CLOSED. Numerics ≠ proof.**
