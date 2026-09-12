# Uniform \(\mathcal{R}_\star\) — close attempt progress

**Date:** 2026-09-12  
**Branch:** `cursor/uniform-rstar-close-0cc5` (from `cursor/uniform-rstar-attack-0cc5`)  
**Policy:** [`RESEARCH-POLICY.md`](./RESEARCH-POLICY.md) — analytic-first; light probes only.  
**Honesty lock:** Lemma★ / DA-NS-1 remains a **HYPOTHESIS**. Clay Statement B is **not solved**. Numerics ≠ proof. Do **not** revive \(|T_c|\le C\|v\|_2 X^{3/2}\).

**One-line status:** **STILL OPEN** — no proof of \(\sup_v\mathcal{R}_\star<\infty\), no analytic kill family. Sharpest remainder is the Cauchy / channel form below; HL/LL is **not** filed as classical.

---

## 0. Target

\[
\mathcal{R}_\star(v)=\frac{(T_c)_+^2}{D_s\,E\,Y}\qquad(D_s E Y>0),
\qquad
\text{PRODUCT-BLOCK}\iff\sup_v\mathcal{R}_\star(v)<\infty.
\]

---

## 1. Proved lemmas (this pass)

### Lemma A — Plancherel / Cauchy form of \(T_c\)

\[
T_c=-\langle B(v,v),A(A-\Lambda)v\rangle,
\qquad
|T_c|\le\sqrt{D_s}\,\|A^{1/2}B(v,v)\|_2.
\]

**Proof.** \(D_s=\|A^{1/2}(A-\Lambda)v\|_2^2\); Cauchy–Schwarz in \(L^2\).  

**Corollary.** Whenever \(T_c>0\) and \(D_s E Y>0\),

\[
\mathcal{R}_\star(v)\le\frac{\|A^{1/2}B(v,v)\|_2^2}{E\,Y}.
\]

So a **sufficient** geometric close of PRODUCT-BLOCK is

\[
\sup_v\frac{\|A^{1/2}B(v,v)\|_2^2}{E\,Y}<\infty.
\]

This sufficient form may be strictly stronger than PRODUCT-BLOCK (Cauchy need not be sharp). Cancellations between \(B\) and \(A(A-\Lambda)v\) are visible in probes: \(\|A^{1/2}B\|_2^2/(EY)\) can sit \(O(10^{-1})\) while \(\mathcal{R}_\star\) is \(O(10^{-2})\) or zero when \(T_c\le 0\).

### Lemma B — Λ-relative input channel split (exact)

Fix \(\theta>0\). Declare mode \(k\) high iff \(\lambda_k\ge\theta\Lambda\). Partition every parent pair \((p,q)\) in the triad sum for \(\widehat B_k\) as HH / HL / LL. Then

\[
T_c=T_c^{\mathrm{HH}}+T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}}
\]

exactly (finite support: verified by channel-sum residual \(\approx 0\) in code). Same Cauchy form applies channelwise:

\[
|T_c^{\mathrm{ch}}|\le\sqrt{D_s}\,\|A^{1/2}B^{\mathrm{ch}}\|_2,
\qquad\mathrm{ch}\in\{\mathrm{HH},\mathrm{HL},\mathrm{LL}\}.
\]

### Lemma C — Exact two-shell spectral spread

If \(v\) is supported on Stokes shells \(\alpha\neq\beta\) with shell energies \(E_\alpha,E_\beta>0\) and \(X=\alpha E_\alpha+\beta E_\beta\), then

\[
D_s=\frac{\alpha\beta\,(\alpha-\beta)^2\,E_\alpha E_\beta}{X}.
\]

(Algebra from \(Z-\Lambda Y\); cross-checked numerically to \(\sim 10^{-15}\) relative error.)

### Lemma D — Invariances (algebra)

\(\mathcal{R}_\star\) is invariant under \(v\mapsto a v\) (\(a\neq 0\)) and under lattice-compatible Fourier dilations \(k\mapsto nk\) (\(n\in\mathbb{N}\)) with coefficients transported along rays.  

**Discarded:** \(|T_c|\le C\|v\|_2 X^{3/2}\) fails amplitude scaling (\(a^3\) vs \(a^4\)).

### Lemma E — Single-shell vacuity

If \(v\) is an exact Stokes eigenfield (\(Av=\Lambda v\)), then \(D_s=0\) and \(T_c=0\). The shape quotient is vacuous.

### Lemma F — Near-shell limit structure (Attack 9B bookkeeping)

For \(v_\varepsilon=w_\alpha+\varepsilon z_\beta\) with \(z_\beta\parallel\Pi_\beta B(w_\alpha,w_\alpha)\) and \(\varepsilon\to 0\), \(\mathcal{R}_\star(v_\varepsilon)\) tends to a finite shell functional \(K_{\alpha,\beta}(w)\) (when the closing packet is nontrivial). This limit is a **number for each fixed \((\alpha,\beta,w)\)**, not a proof of uniformity over all shells, and not a kill (\(\not\to\infty\) along \(\varepsilon\to 0\)).

---

## 2. What failed / what is not proved

### 2.1 HL/LL is **not** classical (correction to the attack sketch)

The prior attack map called HL/LL “classical-ish bookkeeping.” **That oversells the state of the estimate.**

Elementary Sobolev / paraproduct bounds on \(B^{\mathrm{HL}}\) and \(B^{\mathrm{LL}}\) produce **field-dependent powers of \(\Lambda\)** (lose dilation invariance). Absorbing low-mode mass via

\[
D_s\ge(1-\theta)^2\Lambda^2 X_L
\qquad(\lambda<\theta\Lambda)
\]

still leaves ratios that are not controlled by \(E Y\) alone without further structure.  

**Status:** HL/LL bound of the form \((T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}})_+^2\le C_{\mathrm{HL/LL}} D_s E Y\) with geometry-only \(C\) is **OPEN**, not filed.

### 2.2 HH remains open

Same for \((T_c^{\mathrm{HH}})_+^2\le C_{\mathrm{HH}} D_s E Y\). Ordinary energy-only Agmon products do not close it.

### 2.3 Kill lane — no counterexample found

Analytic constructions checked (not an HPC sweep):

| Family | Outcome |
| --- | --- |
| Near-shell \(\varepsilon\to 0\) | \(\mathcal{R}_\star\to K_{\alpha,\beta}<\infty\) (no kill) |
| Two-shell amplitude / ratio sweeps | Finite sample \(\mathcal{R}_\star\lesssim 10^{-2}\); no divergence in ratio |
| Filled Fourier balls (\(|k|\le K\)) | \(\mathcal{R}_\star\) stays small; often \(T_c\le 0\) |
| Coherent circular shell pairs / ABC-style | Typically \(T_c\approx 0\) |
| Naive continuum “blob” scaling \(\mathcal{R}_\star\sim\lambda^3\) | **Invalid** as a kill: ignores triad cancellations / near-shell structure; contradicted by lattice-dilation invariance on ray-supported fields and by ball probes |

**Kill lane:** still **LIVE** (absence of a family ≠ proof of uniformity).

---

## 3. Sharpest partial / conditional statement

**Theorem-shaped conditional (honest):**

Assume there exist geometry-only constants \(C_{\mathrm{HL/LL}},C_{\mathrm{HH}}<\infty\) such that for every smooth mean-zero divergence-free \(v\) on \(\mathbb{T}^3\),

\begin{align}
\bigl(T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}}\bigr)_+^2
&\le C_{\mathrm{HL/LL}}\,D_s\,E\,Y,\\
\bigl(T_c^{\mathrm{HH}}\bigr)_+^2
&\le C_{\mathrm{HH}}\,D_s\,E\,Y.
\end{align}

Then \(\sup_v\mathcal{R}_\star(v)<\infty\) (e.g. \(C_{\mathrm{geom}}\le 2C_{\mathrm{HL/LL}}+2C_{\mathrm{HH}}\) after \((a+b)_+^2\le 2a_+^2+2b_+^2\)), the energy-budget form of Lemma★ closes, and the \(\Lambda'\) Gronwall packaging yields continuation on this trunk.

**Neither hypothesis is proved.**  

**Equivalent sufficient target (cleaner inequality):**

\[
\|A^{1/2}B(v,v)\|_2^2\le C\,E\,Y
\qquad\text{(geometry-only \(C\))}.
\]

Isolated HH obstruction form:

\[
\|A^{1/2}B^{\mathrm{HH}}(v,v)\|_2^2\le C_{\mathrm{HH}}\,E\,Y,
\]

with the analogous HL+LL inequality still required (not free).

---

## 4. Code (minimal)

| Path | Role |
| --- | --- |
| `scripts/ns_attacks/uniform_rstar_identities.py` | Verify Lemmas A–D residuals; light kill/sanity probe |
| `scripts/ns_attacks/uniform_rstar_attack.py` | Existing Λ-channel maximizer (subordinate) |
| `scripts/ns_attacks/ns_lemma_star_core.py` | Exact finite-support \(T_c\), \(D_s\), \(\mathcal{R}_\star\) |

```bash
python3 scripts/ns_attacks/uniform_rstar_identities.py
python3 scripts/ns_attacks/uniform_rstar_attack.py --quick
```

---

## 5. Honesty table

| Item | Status |
| --- | --- |
| PRODUCT-BLOCK / \(\sup\mathcal{R}_\star<\infty\) | **OPEN** |
| Lemma★ / DA-NS-1 | **HYPOTHESIS** |
| Lemma A–F above | **Proved** (as stated) |
| HL/LL geometric bound | **OPEN** (not classical) |
| HH geometric bound | **OPEN** |
| Kill family \(\mathcal{R}_\star\to\infty\) | **Not found** (lane LIVE) |
| Clay Statement B | **NOT SOLVED** |
| Numerics = proof? | **No** |

---

## 6. One-line status

**Still OPEN. Proved: Cauchy + channel split + two-shell \(D_s\) + invariances. Remainder: geometric control of \(T_c^{\mathrm{HH}}\) and \(T_c^{\mathrm{HL/LL}}\) (equivalently of \(\|A^{1/2}B\|_2^2/(EY)\)). No kill. NS / Clay B not solved.**
