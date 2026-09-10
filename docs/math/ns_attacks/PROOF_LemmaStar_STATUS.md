# PROOF status — Lemma★ (energy remainder)

**Date:** 2026-09-10  
**Lock:** **NS is NOT solved.** Lemma★ is **OPEN**. Numerics are not a proof.

## Statement (working)

On divergence-free fields on \(\mathbb{T}^3\), with Stokes operator \(A\) and
\[
X=\|A^{1/2}u\|_2^2,\quad Y=\|Au\|_2^2,\quad Z=\|A^{3/2}u\|_2^2,\quad\Lambda=\frac{Y}{X},
\]
\[
\mathcal N=-\langle B(u,u),Au\rangle,\quad
\mathcal M=-\langle B(u,u),A^2u\rangle,\quad
\mathfrak T_c=\mathcal M-\Lambda\mathcal N,\quad
\mathcal D_s=Z-\Lambda Y\ge0,
\]
**Lemma★** asserts: for every \(\theta\in(0,1)\) there is a geometric constant \(C_0\) (independent of \(u,\nu\)) such that
\[
\mathfrak T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}\|u\|_2^2 X\Lambda.
\]

## What is proved / killed / open

| Claim | Status | Evidence |
|-------|--------|----------|
| Lemma★ \(\Rightarrow\) no finite-time blowup of \(\Lambda\) in this packaging \(\Rightarrow\) GR on \(\mathbb{T}^3\) **in this packaging** | **Conditional implication** (sketch / packaging only) | Energy/enstrophy differential inequalities + absorption; not a Clay submission |
| K=0 form \(\mathfrak T_c\le\theta\nu\mathcal D_s\) | **KILLED** (numeric; scaling) | Attack 2: \(\mathfrak T_c/\mathcal D_s\) grows with amplitude (\(\sim B\)) |
| Young reduction of \(\mathfrak T_c\) toward a norm of \(B(u,u)\) | **Partial** | Formal polarization; does not close 3D product gap |
| \(|\mathfrak T_c|\le C\|u\|_2 X^{3/2}\) (or equiv) by Agmon/product | **GAP — does not close** | Standard 3D estimates insufficient for HH→L |
| Uniform geometric \(C_0\) for Lemma★ | **OPEN** | Attack 1+5 numeric survival ≠ proof; live door: prove **or** kill with blowing family |
| Amplitude-invariant \(C_*\) for \(X^{3/2}\Lambda\) remainder | **OPEN (numeric support)** | Attack 2 |

## Live door

1. **Prove** Lemma★ with uniform geometric \(C_0\), or the weaker \(C_* X^{3/2}\Lambda\) bound; **or**
2. **Kill** by exhibiting a smooth family with \(R_\star=\mathfrak T_c/(\|u\|_2^2 X\Lambda)\to\infty\); **or**
3. Upgrade centering cancellation beyond \(\mathfrak T_c=\mathcal M-\Lambda\mathcal N\) to remove the dangerous HH→L piece.

Until one of these lands as mathematics (not numerics), **do not claim global regularity**.

## Related files

- `docs/math/ns_attacks/ATTACK_SYNTHESIS_SIMULTANEOUS.md`
- `docs/ns-recovery/CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md`
- `scripts/ns_attacks/`
