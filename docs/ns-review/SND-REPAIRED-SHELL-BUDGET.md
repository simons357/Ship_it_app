# Repaired shell budget — identities and tests, not a new Theorem H

**Date:** 16 September 2026  
**Status:** **NOT a proof of Theorem H, [SND], or unforced Statement (B).** Archive: the sendable card is [`SND-WHAT-IS-KEPT.md`](./SND-WHAT-IS-KEPT.md).  
**After:** panel response [`PANEL-RESPONSE-2026-09-16.md`](./PANEL-RESPONSE-2026-09-16.md) and audit [`SND-MATH-CORRECTIONS-2026-09-15.md`](./SND-MATH-CORRECTIONS-2026-09-15.md) §8.  
**Class:** smooth, mean-zero, divergence-free solutions of **unforced** NS on a fixed torus \((\mathbb{R}/2\pi\mathbb{Z})^3\) (period changes constants, not the tests). Real self-adjoint dyadic multipliers with uniformly bounded symbols.

This note does four things only:

1. Derive the boxed shell equation and name \(F_j\) before estimating.
2. Record the valid \(M\)-conditional bound on \(F_j\) and the one-sided consequence for \(\Pi_j\).
3. Write the formal \(\rho\) evolution when a unique maximizer exists, so it is clear what a later propagation argument would have to control.
4. Run the three required tests against the **failed** displayed bound and against the **valid** \(F_j\) lemma, without promoting either to dominant-shell persistence.

No Bony reconstruction is attempted here. An incomplete indexed decomposition was part of the defect.

---

## 1. Names

\[
F_j=\bigl\langle(u\cdot\nabla)u,\,\Delta_j^2 u\bigr\rangle
=\bigl\langle\Delta_j[(u\cdot\nabla)u],\,\Delta_j u\bigr\rangle
\quad\text{(real self-adjoint \(\Delta_j\))}.
\]

\[
X_j:=2^{2j}\|\Delta_j u\|_2^2,\qquad
X:=\sum_j X_j.
\]

On a frozen exact-block partition as in the shear family, \(X=\|\nabla u\|_2^2\). For a general Littlewood–Paley partition, \(X\asymp\|\nabla u\|_2^2\); use equivalence constants or define \(X_j\) as the Fourier-weighted shell energy actually used. This note uses the displayed \(X_j\) so the boxed equation is exact.

\[
\mathcal{D}:=\nu\|\Delta u\|_2^2,\qquad
S_j:=\nu\sum_{k>j}2^{2k}\|\Delta_k\nabla u\|_2^2\ge 0.
\]

The **manuscript** flux was \(\Pi_j=F_j-S_j\). That combination is **not** the left-hand nonlinear term in the \(X_j\) equation below. Do not estimate \(|\Pi_j|\) in order to close \(\dot X_j\).

---

## 2. Derivation of the boxed equation

Unforced NS, \(\operatorname{div}u=0\):

\[
\partial_t u+\mathbb{P}(u\cdot\nabla)u=\nu\Delta u.
\]

Apply \(\Delta_j\) (Fourier multiplier, commutes with \(\partial_t\), \(\nabla\), \(\mathbb{P}\)):

\[
\partial_t\Delta_j u+\Delta_j\mathbb{P}((u\cdot\nabla)u)=\nu\Delta\Delta_j u.
\]

Test against \(\Delta_j u\). The pressure/Leray projector drops. The viscous pairing is
\(\nu\langle\Delta\Delta_j u,\Delta_j u\rangle=-\nu\|\nabla\Delta_j u\|_2^2\).
The nonlinear pairing is
\(\langle\Delta_j((u\cdot\nabla)u),\Delta_j u\rangle=F_j\).

Thus

\[
\tfrac12\frac{d}{dt}\|\Delta_j u\|_2^2
+\nu\|\nabla\Delta_j u\|_2^2
=-F_j.
\]

Multiply by \(2^{2j}\):

\[
\boxed{
\frac12\dot X_j
+
\nu\,2^{2j}\|\nabla\Delta_j u\|_2^2
=
-2^{2j} F_j.
}
\]

Equivalently

\[
\dot X_j
=
-2\cdot 2^{2j} F_j
-2\nu\,2^{2j}\|\nabla\Delta_j u\|_2^2.
\]

The viscous term on the left is **not** \(S_j\). Sign: if \(F_j>0\), that shell’s \(X_j\) is driven **down** by the nonlinear term.

This is the quantity a repaired program estimates. The displayed Theorem H estimated something else.

---

## 3. Valid conditional lemma for \(F_j\) (accepted)

Assume \(u\) mean-zero, divergence-free, and in \(H^2\) (or smooth), with \(X\le M\). Let \(\lambda_1>0\) be the first nonzero eigenvalue of \(-\Delta\).

Hölder with exponents \(6,2,3\):

\[
|F_j|
\le
\|u\|_6\,\|\nabla u\|_2\,\|\Delta_j^2 u\|_3.
\]

Mean-zero Sobolev/Poincaré and a uniform \(H^1\) multiplier bound on \(\Delta_j^2\) give \(\|u\|_6\lesssim\|\nabla u\|_2\) and \(\|\Delta_j^2 u\|_3\lesssim\|\nabla u\|_2\), hence \(|F_j|\le C X^{3/2}\) with \(C\) independent of \(j\).

Poincaré on \(\mathcal{D}\): \(\mathcal{D}=\nu\|\Delta u\|_2^2\ge\nu\lambda_1 X\), so
\(X/\mathcal{D}^{1/2}\le\sqrt{M/(\nu\lambda_1)}\). Therefore

\[
\boxed{
|F_j|
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{1/2}\mathcal{D}^{1/2}.
}
\]

No spread hypothesis. No dominant-shell choice. Independent of \(j\).

**One-sided manuscript flux (if that combination is still wanted):**
\[
\Pi_j=F_j-S_j\le F_j
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,X^{1/2}\mathcal{D}^{1/2},
\]
and
\[
|\Pi_j|\le S_j+C\sqrt{\frac{M}{\nu\lambda_1}}\,X^{1/2}\mathcal{D}^{1/2}.
\]

Neither is the displayed Theorem H. Neither is a propagation theorem.

**Into the boxed equation:**
\[
\bigl|\tfrac12\dot X_j+\nu\,2^{2j}\|\nabla\Delta_j u\|_2^2\bigr|
=
2^{2j}|F_j|
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,2^{2j}X^{1/2}\mathcal{D}^{1/2}.
\]

The factor \(2^{2j}\) is still on the right. This bound does **not** by itself compare nonlinear transfer to the viscous term \(\nu 2^{2j}\|\nabla\Delta_j u\|_2^2\) uniformly in \(j\). High shells make the right-hand side large in \(j\) while the lemma’s right-hand side for \(|F_j|\) does not see \(j\). That is compatible with the high-tail test: when \(F_j=0\) the lemma is trivial; when \(F_j\ne 0\) at high \(j\), extra structure is required.

---

## 4. Formal peak-fraction evolution (no estimate)

Let \(J(t)=\max_j X_j(t)\) and \(\rho=J/X\). On any open interval where a **unique** maximizer \(j_*\) persists,

\[
\dot\rho
=
\frac{\dot X_{j_*}}{X}
-
\rho\frac{\dot X}{X}.
\]

Substitute the boxed equation for \(j_*\). Write \(\dot X=\sum_\ell\dot X_\ell\) from the same family of identities. Switches of \(j_*\) require a comparison argument (e.g. \(\tfrac{d}{dt}\max_j X_j\) in the viscosity sense, or a gap \(X_{j_*}-\max_{j\ne j_*}X_j\)). **None of that is carried out here.**

An argument that \(\dot\rho>0\) below a threshold, even if proved, yields a barrier involving \(\min\{\rho(0),\text{threshold}\}\). It cannot force an initially smaller ratio above that threshold at time zero (audit §6).

---

## 5. The three required tests

Any candidate bound, including the lemma in §3, must be checked against these families **before** a persistence claim.

### Test A — high-tail shear (audit §2)

\[
(u\cdot\nabla)u=0\qquad\Rightarrow\qquad F_j=0\text{ for all }j.
\]

The boxed equation collapses to heat decay of each block. \(\Pi_{j_*}=-S_{j_*}\) can be arbitrarily negative as the high shell \(K\to\infty\) at fixed \(X,\rho,M\). **Displayed \(|\Pi_{j_*}|\) bound: FAIL.**  
**\(F_j\) lemma: PASS trivially** (\(0\le\text{RHS}\)).  
**Propagation:** high shells die faster than the low dominant block, so \(\rho(t)\) of this family need not be the obstruction. The test kills the **wrong quantity** \(|\Pi_j|\), not the boxed \(F_j\) identity.

### Test B — amplitude (audit §5)

\(X(Aw)=A^2 X(w)\), \(\mathcal{D}(Aw)=A^2\mathcal{D}(w)\), \(F_j(Aw)=A^3 F_j(w)\).

A right-hand side \(C X^{1/2}\mathcal{D}^{1/2}\) is \(O(A^2)\). The lemma’s factor \(\sqrt{M}\) with \(M\sim A^2 X(w)\) restores \(O(A^3)\) and is **compatible** with this test **as long as \(M\) is allowed to track amplitude**. An \(M\)-free quadratic bound on \(F_j\) **FAILS**.

### Test C — equal shells (audit §6)

\(v_L\) has \(X=q\), \(\rho=1/L\). **Uniform** \(c_*(\nu,\delta_*,M,C_S)\) from \(t=0\): **FAIL.**  
The \(F_j\) lemma does not claim a floor on \(\rho\). For this family again \(F_j=0\).

---

## 6. What is proved in this note

| Item | Status |
| --- | --- |
| Boxed shell equation for smooth unforced NS | **Identity** |
| Distinction \(F_j\) vs \(\Pi_j=F_j-S_j\) vs viscous term in \(\dot X_j\) | **Locked** |
| \(\lvert F_j\rvert\le C\sqrt{M/(\nu\lambda_1)}\,X^{1/2}\mathcal{D}^{1/2}\) on mean-zero \(H^2\), \(X\le M\) | **Lemma** (audit §3) |
| \(\Pi_j\le F_j\) | **Immediate** (\(S_j\ge 0\)) |
| Displayed Theorem H / \(\lvert\Pi_{j_*}\rvert\) bound | **False** (Test A) |
| Dominant-shell persistence / Theorem G | **Not proved** |
| [SND] uniform or per-solution as a theorem | **Not proved** |
| Unforced Statement (B) | **Not claimed** |

---

## 7. What a later persistence proof would still have to do

1. State the exact class (smooth / \(H^2\); freeze LP constants).
2. Control \(\dot\rho\) from the boxed equation, including maximizer switches.
3. Use an estimate of \(F_j\) whose amplitude degree is cubic, or a time-integrated / dynamical restriction that the three tests do not kill.
4. Not claim a uniform floor at \(t=0\).
5. Not treat KEEP labels, Q1 limits, or Φ-renorm as substitutes.

Until those are written and pass Tests A–C, there is **no** repaired Theorem H.

---

## 8. One-line lock

**Identity for \(\dot X_j\) in terms of \(F_j\): yes. Absolute-value Theorem H: no. Fallback \(F_j\) lemma: yes, and not a propagation theorem. Spectral research continues from this equation, not from the displayed \(\Pi_j\) bound.**
