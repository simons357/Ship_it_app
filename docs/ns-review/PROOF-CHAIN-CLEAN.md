# Proof chain — clean exposition

A single visual and notational face for the Navier–Stokes regularity packaging used in this repository. Figures and captions live in [`visual-journey/`](./visual-journey/). This note is the math companion: definitions first, then the chain, then what the product estimate needs.

Notation is aligned with the Lemma★ shape lock, the Φ-renorm swirl book, and the conditional SND texture. Branches are kept separate.

---

## 1. Setting

On the torus \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\), take a smooth, mean-zero, divergence-free velocity \(v\):

\[
\nabla\cdot v=0,\qquad
\int_{\mathbb{T}^3}v=0.
\]

Let \(P\) be the Leray projector and

\[
A=-P\Delta,\qquad
B(v,v)=P\bigl[(v\cdot\nabla)v\bigr].
\]

In Fourier space, \(\lambda_k=|k|^2\) and \((Av)_k=\lambda_k v_k\).

Classical Navier–Stokes on \(\mathbb{T}^3\) reads

\[
\partial_t u+\mathbb{P}\bigl((u\cdot\nabla)u\bigr)=\nu\Delta u,\qquad
\nabla\cdot u=0,
\]

with viscosity \(\nu>0\). The objects below are spectral moments of a fixed field \(v\) (shape), or of a time-dependent strong solution \(u(t)\) (energy-budget wrapper).

---

## 2. Spectral moments

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
| \(\Lambda\) | spectral scale — mean eigenvalue weighted by enstrophy |

On \(\mathbb{T}^3\) with mean zero, \(\Lambda\ge 1\). Cauchy–Schwarz / Plancherel gives \(X\le E\Lambda\).

---

## 3. Spread and centered cascade

Spectral spread (all forms identical):

\[
\begin{aligned}
D_s
=\mathcal{D}_s
&=Z-\Lambda Y
=Z-\frac{Y^2}{X}
=\bigl\|(A-\Lambda)A^{1/2}v\bigr\|_2^2
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
\ge 0.
\end{aligned}
\]

Centered cascade / stretching:

\[
\begin{aligned}
N&=-\langle B(v,v),Av\rangle,\\
M&=-\langle AB(v,v),Av\rangle,\\
T_c
=\mathcal{T}_c
&=M-\Lambda N
=-\langle B(v,v),A(A-\Lambda)v\rangle.
\end{aligned}
\]

Write \(T_c{}_+=\max(T_c,0)\). Only upward stretch enters the shape quotient.

**Identity (algebra).** Along a strong solution,

\[
\Lambda'
=\frac{2}{X}\bigl(T_c-\nu D_s\bigr).
\]

Single-shell fields have \(D_s=0\) and \(T_c=0\) (vacuous for the shape quotient).

---

## 4. Lemma★ — shape form and energy-budget form

**Shape form.** There exists a geometric constant \(C_{\mathrm{geom}}<\infty\) such that for every smooth nonzero divergence-free \(v\),

\[
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
D_s(v)\,
E\,
Y.
\]

Equivalently, whenever \(D_s E Y>0\),

\[
\mathcal{R}_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,E\,Y},
\qquad
\sup_v\mathcal{R}_\star(v)<\infty.
\]

\(\mathcal{R}_\star\) is invariant under amplitude \(v\mapsto a v\) and under uniform Fourier dilation.

**Energy-budget form (Young wrapper).** For \(0<\theta<1\),

\[
T_c(u)
\le
\theta\nu\,D_s(u)
+C_0(\theta)\,\nu^{-1}\,E\,Y,
\qquad
C_{\mathrm{geom}}=4\theta\,C_0(\theta).
\]

(Equivalent bookkeeping with remainder \(C_0\nu^{-1} E X\Lambda\) is used in some energy-budget notes; after \(X\le E\Lambda\) the two wrappers are interchangeable up to constants.)

If the shape (or energy-budget) bound holds with geometric constants, the identity for \(\Lambda'\) yields a Gronwall ceiling on \(\Lambda(t)\) on any strong-solution interval, hence finite enstrophy and continuation. The packaging is the chain from moments to that estimate; the remaining analytic step is the product control in §5.

---

## 5. Product / shape estimate — open node (PRODUCT-BLOCK)

The live target that closes the energy-budget form is **uniform shape control**

\[
\sup_v\mathcal{R}_\star(v)<\infty
\]

(equivalently a geometric \(C_{\mathrm{geom}}\) or Young \(C_0\)). That is the hinge between Lemma★ packaging and the regularity-continuation arrow.

**Schematic product language** in older notes pointed at structure that feeds Young in \(\nu\). A once-proposed universal bound \(|T_c|\le C\|v\|_2 X^{3/2}\) is **algebraically false** as a scale-invariant estimate (LHS \(\sim a^3\), RHS \(\sim a^4\) under \(v\mapsto a v\)) and must not be revived; see [`SCIENTIFIC-REPORT.md`](./SCIENTIFIC-REPORT.md) §4.

Ordinary 3D Sobolev / Agmon product estimates from energy alone do not deliver uniform \(\mathcal{R}_\star\). In the Bony channel diagnostic, the high×high input channel is the live bottleneck (historical label “HH→L”; input-channel split, not a proved high→low output map).

**Attack map (not a theorem):** Λ-relative split \(T_c=T_c^{\mathrm{HH}}+T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}}\). If HL/LL are controlled classically and HH admits a geometric bound against \(D_s E Y\), uniform \(\mathcal{R}_\star\) closes. HH unbound ⇒ PRODUCT-BLOCK **open**. See [`UNIFORM-RSTAR-ATTACK.md`](./UNIFORM-RSTAR-ATTACK.md) and `scripts/ns_attacks/uniform_rstar_attack.py`.

In the chain diagram this node is marked **open estimate**.

---

## 6. Φ-renorm branch (separate book)

Axisymmetric-with-swirl, cylindrical coordinates. Extensive and intensive swirl scalars:

\[
\Gamma=r\,u_\theta,\qquad
\Phi=\frac{\Gamma}{r^2}=\frac{u_\theta}{r}.
\]

**Algebraic identity (KEEP):**

\[
\frac{1}{r^4}\partial_z(\Gamma^2)
=
\partial_z(\Phi^2).
\]

June 30 conditional reduction: after the \(\dot H^{1.3}\) dissipation relabel (operator composition \(2.6\) is not the energy norm), Aubin–Lions compactness and the Φ-equation remain as written. Open barrier:

\[
\sup_{\eps}\int_0^T\Bigl\|\frac{u^r_\eps}{r}\Bigr\|_{L^\infty}\,\mathrm{d}t<\infty,
\]

equivalent in difficulty to axisymmetric-with-swirl global regularity. This branch does not glue to Lemma★ PRODUCT-BLOCK.

---

## 7. SND texture (optional)

Spectral Non-Dispersal / Ring Lemma notes supply a **conditional** shell-concentration texture: under an SND-type hypothesis, shell flux / Gronwall estimates can be written cleanly. Treat as optional side texture on the chain map — not a substitute for the product estimate on the main trunk, and not a glue from arithmetic programs into classical NS.

---

## 8. Notation alignment card

| Object | Lemma★ / \(\mathbb{T}^3\) | Φ-renorm | SND texture |
| --- | --- | --- | --- |
| Primary field | \(v\) or \(u\) on \(\mathbb{T}^3\) | axisymmetric \(u=(u^r,u^\theta,u^z)\) | band-limited vorticity / shells |
| Scale | \(\Lambda=Y/X\) | cylindrical \(r\), intensive \(\Phi\) | shell index / flux |
| Danger object | \((T_c)_+\) vs \(D_s\) | \(\|u^r/r\|_\infty\) | shell dispersal |
| Dissipation label | \(\nu D_s\) | \(\dot H^{1.3}\) (relabeled) | viscous shell damping |
| Open estimate | product / HH-channel bound | strain / \(\|u^r/r\|_\infty\) | SND hypothesis itself |

Do not reuse FRA output symbol \(\Phi\) for swirl \(\Phi\). Do not identify \(T_c\) with shell flux \(J\).

---

## 9. Chain summary (reading order)

1. Classical NSE on \(\mathbb{T}^3\).
2. Moments \(E,X,Y,Z\) and scale \(\Lambda\).
3. Identities for \(D_s\) and \(T_c\); \(\Lambda'=2(T_c-\nu D_s)/X\).
4. Lemma★ shape / energy-budget packaging.
5. Five-lane diagnostics (Bony / shell / packet probes) — stress tests, not a substitute bound.
6. Product bound on \(T_c\) (open estimate).
7. Continuation / regularity arrow (feeds on 4+6).
8. Side: Φ-renorm identity + open \(\|u^r/r\|_\infty\) integrability.
9. Optional: SND conditional texture.

Campaign landing with all adjacent books: [`../campaign/PROOF-JOURNEY.md`](../campaign/PROOF-JOURNEY.md).

Diagram sources: [`visual-journey/proof-chain.mmd`](./visual-journey/proof-chain.mmd), rendered SVG/PNG under [`visual-journey/figures/`](./visual-journey/figures/).
