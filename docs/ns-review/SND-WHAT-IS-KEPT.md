# SND — what is kept

**Send this.** Everything else in `docs/ns-review/` is archive.

**Date:** 16 September 2026  
**Class:** smooth, mean-zero, divergence-free, **unforced** Navier–Stokes on a fixed torus \((\mathbb{R}/2\pi\mathbb{Z})^3\).

Displayed Theorem H is **false**. Spectral notation is **kept**. Unforced Clay Statement (B) is **not claimed**.

---

## Keep

### 1. Names

\[
F_j=\bigl\langle(u\cdot\nabla)u,\,\Delta_j^2 u\bigr\rangle
=\bigl\langle\Delta_j[(u\cdot\nabla)u],\,\Delta_j u\bigr\rangle
\quad\text{(real self-adjoint \(\Delta_j\))}.
\]

\[
X_j:=2^{2j}\|\Delta_j u\|_2^2,\qquad
X:=\sum_j X_j,\qquad
J:=\max_j X_j,\qquad
\rho:=J/X.
\]

On a frozen exact-block partition, \(X=\|\nabla u\|_2^2\). For a general Littlewood–Paley partition, \(X\asymp\|\nabla u\|_2^2\).

\[
\mathcal{D}:=\nu\|\Delta u\|_2^2,\qquad
S_j:=\nu\sum_{k>j}2^{2k}\|\Delta_k\nabla u\|_2^2\ge 0.
\]

Manuscript flux \(\Pi_j=F_j-S_j\) is **not** the nonlinear term in the \(X_j\) equation. Do not estimate \(|\Pi_j|\) in order to close \(\dot X_j\).

**[SND]** means \(J/X\ge c_*\), i.e. \(J\ge c_*X\). It is a **per-solution hypothesis**, not a theorem.

### 2. Exact shell equation

Unforced NS, \(\operatorname{div}u=0\). Apply \(\Delta_j\), test against \(\Delta_j u\), multiply by \(2^{2j}\):

\[
\boxed{
\frac12\dot X_j
+
\nu\,2^{2j}\|\nabla\Delta_j u\|_2^2
=
-2^{2j} F_j.
}
\]

If \(F_j>0\), the nonlinear term drives that shell’s \(X_j\) **down**. The viscous term on the left is not \(S_j\).

Theorem G in the old TeX used a different ODE in \(\Pi_{j_*}\). That equation is **parked**.

### 3. Valid lemma (needs \(X\le M\))

Mean-zero, divergence-free, \(H^2\) (or smooth). Hölder \(6,2,3\), Sobolev/Poincaré, \(\mathcal{D}\ge\nu\lambda_1 X\):

\[
\boxed{
|F_j|
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{1/2}\mathcal{D}^{1/2}.
}
\]

No spread hypothesis. Independent of \(j\). Amplitude degree is cubic once \(M\) tracks \(X\).

Immediate, and weaker: \(\Pi_j\le F_j\). Also \(|\Pi_j|\le S_j+C\sqrt{M/(\nu\lambda_1)}\,X^{1/2}\mathcal{D}^{1/2}\).

**This lemma is not a propagation theorem.** The factor \(2^{2j}\) is still on the right of the boxed equation, so it does not compare transfer to viscosity uniformly in \(j\).

### 4. Three tests any later claim must survive

| Test | Family | Kills | Survives |
| --- | --- | --- | --- |
| **A** | High-tail shear: \((u\cdot\nabla)u=0\), one shell at \(2^K\), fixed \(X,\rho,M\) | displayed \(\lvert\Pi_{j_*}\rvert\) (ratio \(\sim 2^K\); at \(K=32\) about \(9.16\times 10^8\)) | \(F_j=0\), so the lemma is trivial. High shells heat-decay faster; this family does not by itself kill \(\rho\) increase. |
| **B** | Amplitude \(u=Aw\) | any \(M\)-free quadratic bound on \(F_j\) (\(F_j\sim A^3\), \(X^{1/2}\mathcal{D}^{1/2}\sim A^2\)) | the lemma, if \(M\) is allowed to track amplitude |
| **C** | Equal-enstrophy shears \(v_L\), \(\rho(0)=1/L\) | a uniform floor \(c_*(\nu,\delta_*,M,C_S)\) from \(t=0\) | nothing about \(\rho(0)\). A later \(\dot\rho\) barrier can only involve \(\min\{\rho(0),\text{threshold}\}\) |

### 5. Scaling (one line)

In 3D, velocity \(\dot H^{1/2}\) is critical. \(H^1\) is **subcritical**. Energy control is **supercritical**. Mean-zero \(H^1\) embeds in \(L^6\), not \(L^\infty\). Leray–Hopf is \(L^\infty_t L^2\cap L^2_t H^1\), not a uniform \(H^1\) ceiling.

A legitimate interpolation, if an \(L^\infty\) bound is needed, is \(\|u\|_\infty\le C\nu^{-1/4}X^{1/4}\mathcal{D}^{1/4}\). It does not restore \(S_j\).

---

## Park (do not send, do not claim)

- Displayed Theorem H / (SND-C) absolute-flux bound, even under \(X\le M\).
- Theorem G as a uniform SND law.
- The manuscript extract of the false proof, except as an archive of what was withdrawn.
- Incomplete Bony splitting of the wrong quantity.
- [SND] for all data, or [SND] \(\Leftrightarrow\) Clay (B).
- Unforced Statement (B). Official (B) is smooth periodic \(u_0\), \(f\equiv 0\).
- Forced C/D announcements as a decision on unforced (B).
- ARCHON / 10-expert roleplay as evidence.
- KEEP labels, Ring \(E_c\) vs \(E_c^\infty\), Φ-renorm, Lemma★ as substitutes for this estimate.
- “Naming fraud.” The error is a definition/claim mismatch.

Archive of the withdrawal (not part of the send): [`SND-MATH-CORRECTIONS-2026-09-15.md`](./SND-MATH-CORRECTIONS-2026-09-15.md), [`THEOREM-H-STATEMENT-AND-PROOF.md`](./THEOREM-H-STATEMENT-AND-PROOF.md).

---

## Lock

**Identity for \(\dot X_j\) in terms of \(F_j\): yes. Absolute-value Theorem H: no. Fallback \(F_j\) lemma: yes, and not a propagation theorem. Spectral research continues from the boxed equation. No new Theorem H until a candidate estimate passes Tests A–C.**
