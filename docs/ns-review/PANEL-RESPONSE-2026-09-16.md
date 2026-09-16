# Response to the reviewer panel — displayed Theorem H

**From:** Jonathan R. Simons  
**To:** the specialist reviewing the SND / unaugmented NS packet  
**Date:** 16 September 2026  
**Re:** audit of the displayed Theorem H (dropped viscous tail, shear counterexample, embeddings, amplitude, uniform floor)

This letter is the erratum / response. It accepts the audit. It does **not** re-assert Theorem H, dominant-shell propagation, [SND] as a uniform theorem, or unforced Clay Statement (B).

A companion note, [`SND-REPAIRED-SHELL-BUDGET.md`](./SND-REPAIRED-SHELL-BUDGET.md), starts from the exact shell equation and records what can be written now. It is **not** a repaired Theorem H.

---

## Position (adopted)

> In the supplied extract, Theorem H is not established even with \(X\le M\). Its proof drops a viscous tail, uses invalid Sobolev embeddings and does not provide a complete Bony decomposition. The displayed absolute-flux estimate fails on smooth fixed-enstrophy shear fields. A valid \(M\)-dependent bound for the nonlinear shell term can be proved separately, but its usefulness for SND propagation remains to be shown. Any SND floor asserted from time zero must respect the initial spectral distribution. Retain the spectral toolkit and rebuild the required estimate from the exact shell evolution.

I adopt that wording as the public and panel status of the displayed estimate.

---

## Findings accepted, point by point

**1. Dropped term.** With \(\Pi_j=F_j-S_j\) and \(S_j\ge 0\), identifying \(\Pi_j\) with \(F_j\) in the first line of the proof changes the quantity. A Bony decomposition of \(F_j\) cannot bound \(|F_j-S_j|\). An upper bound on \(F_j\) yields only \(\Pi_j\le F_j\), not the claimed absolute-value bound.

**2. Explicit counterexample.** The high-tail shear family (low block + \(N-1\) middle shells + one shell at frequency \(2^K\)), with \((u\cdot\nabla)u=0\), fixed \(X\le M\) and fixed spread \(\rho\), makes the required ratio diverge as \(K\to\infty\). The tabulated values at \(K=24,28,32\) are accepted. These are initial data of explicit global unforced solutions (heat factors \(e^{-\nu 4^j t}\)). The example is not excluded by asking for genuine NS states.

**3. Invalid embeddings.** In three dimensions, mean-zero \(H^1\) controls \(L^6\), not \(L^\infty\); \(H^2\) does not control \(\nabla u\) in \(L^\infty\). The packet Step 2 claims \(\|u\|_\infty\lesssim M^{1/2}\) and \(\|\nabla u\|_\infty\lesssim\|\Delta u\|_2\) are withdrawn. The interpolation
\(\|u\|_\infty\le C\nu^{-1/4}X^{1/4}\mathcal{D}^{1/4}\)
is a legitimate substitute for that line; carrying it through does not restore the missing tail \(S_j\).

**4. Amplitude scaling.** \(F_j(Aw)=A^3 F_j(w)\) while a right-hand side built from \(X^{1/2}\mathcal{D}^{1/2}\) is quadratic in \(A\). No amplitude-independent quadratic bound on \(F_j\) can hold for a spread field with \(F_{j_*}(w)\ne 0\). Removing \(M\) from the *same* displayed estimate is not an open target.

**5. No universal SND floor at \(t=0\).** The equal-shell shears \(v_L\) give \(X(0)=q\) and \(\rho(0)=1/L\) arbitrarily small. No common \(c_*(\nu,\delta_*,M,C_S)\) holds from time zero for every such datum. [SND] remains a **solution-by-solution** extra hypothesis, not a uniform theorem across all data of given size. Small-data existence does not supply a universal initial \(\rho\), because amplitude scaling leaves \(\rho\) unchanged. A \(\dot\rho>0\) barrier can involve \(\min\{\rho(0),\text{threshold}\}\) and cannot lift an initially smaller ratio at \(t=0\).

**6. Valid fallback.** I accept
\[
|F_j|
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{1/2}\mathcal{D}^{1/2}
\]
for mean-zero smooth (or \(H^2\)) divergence-free fields with \(X\le M\), by Hölder \(6,2,3\), mean-zero Sobolev/Poincaré, and \(\mathcal{D}\ge\nu\lambda_1 X\). Consequences \(\Pi_j\le F_j\) and \(|\Pi_j|\le S_j+C\sqrt{M/(\nu\lambda_1)}\,X^{1/2}\mathcal{D}^{1/2}\) are different estimates from Theorem H. They do **not** establish dominant-shell propagation.

**7. Wording and definition fixes** in the audit table are accepted, including:

| Item | Adopted correction |
| --- | --- |
| [SND] | \(J/X\ge c_*\) means \(J\ge c_*X\), not \(X\ge c_*J\) |
| Scaling | Velocity \(\dot H^{1/2}\) is critical; \(H^1\) is subcritical; **energy** control is supercritical |
| Leray–Hopf | \(L^\infty_t L^2_x\cap L^2_t H^1_x\), not a uniform-in-time \(H^1\) ceiling |
| LP sums | \(\asymp\) unless the partition is frozen |
| Domain of estimates | Smooth or \(H^2\) first; \(\mathcal{D}\) need not be finite on \(H^1\) |
| Displayed Bony split | Incomplete (unquantified \(j'\); high–low uses whole \(u\)) |
| KEEP / Ring | A KEEP label is not verification; \(E_c^\infty\) Bernstein changes the threshold |
| Official (B) | Smooth periodic \(u_0\), \(f\equiv 0\) |
| “Naming fraud” | **Definition/claim mismatch** / mislabeling |

---

## What I am not claiming

- Displayed Theorem H, even under \(X\le M\).
- Dominant-shell persistence / Theorem G as a uniform law.
- [SND] for all data, or [SND] \(\Leftrightarrow\) Clay Statement (B).
- Unforced Statement (B).
- That the fallback \(|F_j|\) lemma closes any SND program.
- That OpenAI’s 8 September forced C/D announcement, or Clay’s 11 September evaluation note, decides unforced (B).

---

## What happens next (spectral research retained)

1. This letter and the 15 September mathematical corrections remain the status of the **old** statement.
2. Any new estimate starts from
   \[
   \tfrac12\dot X_j+\nu\,2^{2j}\|\nabla\Delta_j u\|_2^2=-2^{2j}F_j
   \]
   for smooth unforced NS, with \(F_j\) named before any bound is attempted.
3. Before any propagation claim is re-asserted, the candidate must be tested against:
   - the high-tail shear family;
   - amplitude rescaling \(u=Aw\);
   - many equal-enstrophy shells \(v_L\).
4. The first repaired note ([`SND-REPAIRED-SHELL-BUDGET.md`](./SND-REPAIRED-SHELL-BUDGET.md)) records identities, the fallback lemma, the one-sided consequence for \(\Pi_j\), and those three tests. It **does not** claim a new Theorem H.

I am grateful for a line-by-line audit. The gaps are real. The spectral dictionary stays; the displayed close does not.

Jonathan R. Simons
