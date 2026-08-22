# Q1-augmented Navier–Stokes: proof chain (Track A)

Draft. Augmented system only. This is a different PDE from the classical (unaugmented) equations.

Does **not** close Track B. No inverse-GCD, no Bridge, no Route C.

The extra dissipation is the Ladyzhenskaya / \(p\)-Laplacian term already known to give global regularity in three dimensions when the power is large enough. The chain below records that fact in your \(Q_1\) notation and lists numerical checks.

---

## Status dashboard

| Claim | Status |
|---|---|
| Energy identity for \(Q_1\) | Proved below |
| Global weak solutions, \(\beta\ge 1/2\) | Standard (Ladyzhenskaya class) |
| Uniqueness / strong solutions, \(\beta\ge 1/2\) | Standard in that class |
| \(C^\infty\) bootstrap for \(\varepsilon>0\) | Standard once \(H^1\) is uniform |
| \(\Phi\) identity \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) | Algebra only; **not used** here |
| Uniform \(H^1\) as \(\varepsilon\to 0\) | Open (old C/I; do not reuse) |
| Classical unaugmented regularity | Not claimed |

---

## 0. The system

On \(\mathbb{T}^3\times[0,T]\), \(\nu>0\), \(\varepsilon>0\), \(\alpha>0\), \(\beta\ge 1/2\):

\[
\partial_t u+(u\cdot\nabla)u
=-\nabla p+\nu\Delta u
+\varepsilon^\alpha\,\mathbb{P}\,\mathrm{div}\bigl(|\nabla u|^\beta\nabla u\bigr),
\qquad
\nabla\cdot u=0.
\]

\(\mathbb{P}\) is the Leray projector. Initial data \(u_0\in H^1(\mathbb{T}^3)\), \(\nabla\cdot u_0=0\).

Write \(p=\beta+2\), so \(\beta\ge 1/2\) is \(p\ge 5/2\). The extra term is the variational derivative of \(\frac1p\int|\nabla u|^p\). This is the Ladyzhenskaya modification (Ladyzhenskaya 1968; Málek–Nečas–Růžička). It is **not** the scalar \(-\varepsilon^\alpha|\nabla u|^\beta\Delta u\) from an older draft. Use the divergence form so the energy identity is exact.

Effective viscosity in the stress is at least \(\nu\). The system is uniformly parabolic for each fixed \(\varepsilon>0\).

---

## 1. Energy identity

Test the equation against \(u\). The convective term and the pressure vanish.

**Lemma 1.** For a smooth solution,

\[
\frac12\frac{d}{dt}\|u\|_2^2
+\nu\|\nabla u\|_2^2
+\varepsilon^\alpha\|\nabla u\|_{L^{\beta+2}}^{\beta+2}
=0.
\]

Hence for every \(T>0\),

\[
\frac12\|u(T)\|_2^2
+\nu\int_0^T\|\nabla u\|_2^2\,dt
+\varepsilon^\alpha\int_0^T\|\nabla u\|_{L^{\beta+2}}^{\beta+2}\,dt
=\frac12\|u_0\|_2^2.
\]

**Proof.** \(\int(u\cdot\nabla)u\cdot u=\frac12\int u\cdot\nabla(|u|^2)=0\).  
\(\int\mathbb{P}\mathrm{div}(|\nabla u|^\beta\nabla u)\cdot u=-\int|\nabla u|^{\beta+2}\).  
The Stokes term is \(-\nu\|\nabla u\|_2^2\).

This is the only energy law used below. No Gronwall, no \(\Phi\).

---

## 2. Galerkin existence

Let \(P_n\) be the projection onto the first \(n\) Stokes eigenfunctions.

**Lemma 2.** The Galerkin system has a global-in-time solution \(u_n\). The bounds of Lemma 1 are uniform in \(n\).

**Proof.** Finite-dimensional ODE. The same energy identity holds for \(u_n\). The right-hand side is independent of \(n\) and of \(T\). No finite-time blowup of \(\|u_n\|_2\).

**Lemma 3.** There is a subsequence \(u_n\rightharpoonup u\) with

\[
u\in L^\infty(0,\infty;L^2)\cap L^2(0,\infty;H^1),
\qquad
\nabla u\in L^{\beta+2}(0,\infty;L^{\beta+2}),
\]

and \(u\) is a weak solution of the \(Q_1\) system.

**Proof.** Banach–Alaoglu on the bounds of Lemma 1. Aubin–Lions for strong \(L^2\) compactness of the convective term (the extra dissipation only helps). Monotonicity of \(v\mapsto\mathrm{div}(|\nabla v|^\beta\nabla v)\) passes to the limit (Minty–Browder). Details: Málek–Nečas–Růžička, *Weak and Measure-valued Solutions to Evolutionary PDEs*, Ch. 5.

---

## 3. Why \(\beta\ge 1/2\) closes in 3D

The obstruction in the classical system is the stretching integral \(\int(\omega\cdot S\omega)\). After one derivative, you need something like \(u\in L^s_t L^r_x\) with \(2/s+3/r=1\), \(r>3\).

Here \(\nabla u\in L^{\beta+2}_t L^{\beta+2}_x\). Sobolev on \(\mathbb{T}^3\) gives

\[
\|u\|_{L^{3(\beta+2)/(\beta+1)}}\lesssim \|\nabla u\|_{L^{\beta+2}}
\]

(up to the mean-zero / Poincaré convention). For \(\beta\ge 1/2\) one has \(\beta+2\ge 5/2\) and the pair \((s,r)\) built from these integrabilities meets the Ladyzhenskaya–Prodi–Serrin line (or the Ladyzhenskaya \(p\ge 5/2\) criterion for the modified stress). That is the whole gain: **extra integrability of \(\nabla u\)**, not a geometric cancel.

**Lemma 4.** For \(\beta\ge 1/2\) and \(\varepsilon>0\), the weak solution of Lemma 3 is unique and lies in \(L^\infty(0,\infty;H^1)\cap L^2(0,\infty;H^2)\).

**Proof.** Standard difference-of-two-solutions estimate in this class: the extra term produces a monotone remainder that absorbs the convective difference. See Ladyzhenskaya (1968) and Málek–Nečas–Růžička. The constant depends on \(\varepsilon,\alpha,\beta,\nu,\|u_0\|_{H^1}\). It **blows up** as \(\varepsilon\to 0\). That is why this lemma does not pass to Track B.

---

## 4. Smoothness bootstrap

**Lemma 5.** The unique strong solution of Lemma 4 is \(C^\infty(\mathbb{T}^3\times(0,\infty))\).

**Proof.** Frozen \(\varepsilon>0\), the linearized operator is a uniformly elliptic Stokes operator with continuous coefficients (after Lemma 4). Difference quotients give \(H^k\) bounds for all \(k\). Sobolev embedding: \(C^\infty\) in space. Time regularity from the equation. No new idea.

---

## 5. Theorem (Track A)

**Theorem A.** Let \(\nu>0\), \(\varepsilon>0\), \(\alpha>0\), \(\beta\ge 1/2\), and let \(u_0\in H^1(\mathbb{T}^3)\) be divergence-free. The \(Q_1\) system has a unique solution

\[
u\in C^\infty(\mathbb{T}^3\times(0,\infty))\cap L^\infty(0,\infty;H^1).
\]

No finite-time singularity occurs **for this PDE**.

**Proof.** Lemma 2 \(\to\) Lemma 3 \(\to\) Lemma 4 \(\to\) Lemma 5.

Data need not be axisymmetric. The \(\Phi\) identity is not used.

---

## 6. What this chain does not do

- It does not send \(\varepsilon\to 0\). The \(H^1\) bound of Lemma 4 depends on \(\varepsilon^{-\,c(\beta)}\).
- It does not prove anything about \(\frac1{r^4}\partial_z(\Gamma^2)\) in the classical swirl equations.
- It does not prove SND-C, 3-CONC, or Ring.
- It does not use \(Q_N\) or Bridge\(^*\).

Track B stays the other note.

---

## 7. Numerical checks (verification, not a proof)

The script `scripts/augmented_ns_verify.py` runs a Fourier–Galerkin Taylor–Green flow on \(\mathbb{T}^3\).

| Check | What would support the chain |
|---|---|
| **E1** energy residual | \(\bigl|\frac12\|u(T)\|_2^2+\nu\int\|\nabla u\|_2^2+\varepsilon^\alpha\int|\nabla u|^{\beta+2}-\frac12\|u_0\|_2^2\bigr|\) small |
| **E2** extra dissipation positive | \(\int|\nabla u|^{\beta+2}>0\) whenever \(\varepsilon>0\) and \(\nabla u\not\equiv 0\) |
| **E3** enstrophy bounded for \(\varepsilon>0\) | \(X(t)=\|\omega(t)\|_2^2\) stays finite on a fixed window where the \(\varepsilon=0\) run is already straining the grid |
| **E4** \(\varepsilon\)-dependence | peak \(X\) grows as \(\varepsilon\) decreases (consistent with Lemma 4 not being uniform) |
| **E5** divergence | \(\|\nabla\cdot u\|_\infty\) at roundoff after projection |

Failure of E1 means the discretization is wrong, not that Theorem A is wrong. Success of E3 is consistency, not a proof.

Suggested first run: \(N=24\) modes, \(\nu=0.01\), \(\beta=1/2\), \(\alpha=1\), \(\varepsilon\in\{0,0.05,0.2\}\), \(T=2\), Taylor–Green amplitude 1.

### First verification run

Fourier–Galerkin Taylor–Green, \(N=16\), \(\nu=0.02\), \(\beta=1/2\), \(\alpha=1\), \(T=0.4\), \(\Delta t=0.01\), 2/3 dealias, RK2, trapezoidal dissipation integral. Output: `results/augmented_ns_verify.json`.

| \(\varepsilon\) | \(E(0)\) | \(E(T)\) | \(\nu\int\|\nabla u\|_2^2\) | \(\varepsilon^\alpha\int|\nabla u|^{5/2}\) | residual | \(X(0)\) | \(X(T)\) | \(\|\nabla\cdot u\|_\infty\) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 31.0063 | 29.5456 | 1.4607 | 0 | \(4.6\times10^{-6}\) | 93.02 | 90.04 | \(1.9\times10^{-15}\) |
| 0.05 | 31.0063 | 26.3776 | 1.3804 | 3.2483 | \(4.4\times10^{-6}\) | 93.02 | 80.22 | \(1.6\times10^{-15}\) |
| 0.20 | 31.0063 | 19.1359 | 1.1802 | 10.6898 | \(3.4\times10^{-4}\) | 93.02 | 57.99 | \(1.7\times10^{-15}\) |

Reading against the checklist:

- **E1** holds. Residual is \(10^{-6}\) at \(\varepsilon=0\) and \(3\times10^{-4}\) at \(\varepsilon=0.2\) (RK2 + trapezoid, not a conserved discrete energy).
- **E2** holds. The \(Q_1\) integral is strictly positive for \(\varepsilon>0\).
- **E3** holds on this window. Enstrophy stays finite; larger \(\varepsilon\) damps it faster.
- **E4** is consistent with Lemma 4 not being uniform: \(X(T)\) grows as \(\varepsilon\) decreases (\(58\to80\to90\)).
- **E5** holds at roundoff after Leray projection.

This is a consistency check of Lemma 1 on a smooth periodic field. It is not a proof of Theorem A and says nothing about Track B.

Reproduce:

```
python3 scripts/augmented_ns_verify.py --n 16 --t 0.4 --dt 0.01 --nu 0.02 --eps 0.0 0.05 0.2 --out results/augmented_ns_verify.json
python3 -m unittest tests/test_augmented_ns_verify.py
```
