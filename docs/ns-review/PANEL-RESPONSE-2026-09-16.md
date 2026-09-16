# Response to the reviewer panel — displayed Theorem H

**From:** Jonathan R. Simons  
**To:** the specialist reviewing the SND packet  
**Date:** 16 September 2026

This letter withdraws the displayed Theorem H. It is **not** a repaired Theorem H.

Shared target: [`SND-CLARIFICATION.md`](./SND-CLARIFICATION.md).  
Test of (P): [`SND-PERSISTENCE.md`](./SND-PERSISTENCE.md).  
Identities: [`SND-WHAT-IS-KEPT.md`](./SND-WHAT-IS-KEPT.md).

---

Displayed Theorem H is not established, even with \(X\le M\). The proof identifies \(\Pi_j=F_j-S_j\) with \(F_j\) and drops the viscous tail \(S_j\ge 0\). The claimed absolute-value bound then fails on an explicit smooth shear family with fixed enstrophy and fixed spread (ratio \(\sim 2^K\); about \(9\times 10^8\) at \(K=32\)). Those fields are genuine unforced solutions after the heat factor.

What is kept:

\[
\tfrac12\dot X_j+\nu\,2^{2j}\|\nabla\Delta_j u\|_2^2=-2^{2j}F_j,
\]

and, for mean-zero \(H^2\) fields with \(X\le M\),

\[
|F_j|
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{1/2}\mathcal{D}^{1/2}.
\]

The lemma is A.2. It is not a dominant-shell persistence result. \(F_j\) is cubic in amplitude, so no \(M\)-free quadratic bound holds. Equal-shell shears \(v_L\) make \(\rho(0)\) arbitrarily small at fixed \(X\), so [SND] is a per-solution hypothesis, not a uniform theorem from time zero. In 3D, \(H^1\) controls \(L^6\), not \(L^\infty\).

The remaining question was local persistence of \(\rho=J/X\) on a time \(T(M,\nu,\rho_*)\) only. That statement is **false**. High-peak unforced shears kill the peak on the viscous timescale \(1/(\nu 4^K)\) while \(X\le M\). Using A.2 for a lower comparison leaves an unbounded \(4^{j_*}\). Do not insert \(\|\nabla u\|_\infty\) to repair this, and do not write a new Theorem H.

Not claimed: Theorem H, Theorem G, [SND] for all data, [SND] \(\Leftrightarrow\) Clay (B), unforced Statement (B), conditional local SND-persistence under only \((M,\nu,\rho_*)\).

Spectral research can still *measure* \(\rho\). It does not get a floor on \(\rho\) from \((M,\nu,\rho_*)\) alone.

Jonathan R. Simons
