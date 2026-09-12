# Uniform \(\mathcal{R}_\star\) — close attempt progress

**Date:** 2026-09-12  
**Branch:** `cursor/uniform-rstar-hh-push-3c58` → `cursor/uniform-rstar-attack-0cc5` (PR #73)  
**Policy:** [`RESEARCH-POLICY.md`](./RESEARCH-POLICY.md) — analytic-first; light probes only.  
**Honesty lock:** Lemma★ / DA-NS-1 remains a **HYPOTHESIS**. Clay Statement B is **not solved**. Numerics ≠ proof. Do **not** revive \(|T_c|\le C\|v\|_2 X^{3/2}\).  
**Credit face:** [`CREDIT-BODY-OF-WORK.md`](./CREDIT-BODY-OF-WORK.md) · campaign map [`../campaign/TWO-YEARS-MAP.md`](../campaign/TWO-YEARS-MAP.md).  
**Publisher/X gate:** [`GATED-PUBLISH-CHECKLIST.md`](./GATED-PUBLISH-CHECKLIST.md) — **INACTIVE** until real proof.

**One-line status:** **STILL OPEN** — no proof of \(\sup_v\mathcal{R}_\star<\infty\), no \(\mathcal{R}_\star\to\infty\) kill. Dilation ledger + HH mass proved; elementary Λ-power HL/LL **killed**; Cauchy-sufficient \(\sup Q<\infty\) **strategically blocked** (face family); geometric HL/LL and HH still **OPEN**.

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

### Lemma G — Lattice-dilation scaling ledger (algebra)

Transport coefficients along rays under \(k\mapsto n k\) (\(n\in\mathbb{N}_{\ge 1}\)). Then

\[
E\mapsto E,\quad
X\mapsto n^2 X,\quad
Y\mapsto n^4 Y,\quad
Z\mapsto n^6 Z,\quad
\Lambda\mapsto n^2\Lambda,\quad
D_s\mapsto n^6 D_s.
\]

Both shape functionals

\[
\mathcal{R}_\star(v)
\qquad\text{and}\qquad
Q(v)=\frac{\|A^{1/2}B(v,v)\|_2^2}{E\,Y}
\]

are invariant. Cross-checked to \(\sim 10^{-15}\) relative error in `uniform_rstar_dilation.py`.  

**Consequence:** PRODUCT-BLOCK (and the sufficient Cauchy target) are pure **shape** problems — equivalent to a bound on a fundamental domain modulo amplitude and lattice dilation. Any estimate that inserts unmatched powers of \(\Lambda\) (or of absolute Sobolev norms that scale the same way) cannot be geometry-only.

### Lemma H — Two-shell channel dichotomy (\(\theta=1\))

Let \(v\) be supported on exact Stokes shells \(\alpha<\beta\) with \(E_\alpha,E_\beta>0\). Then \(\Lambda\in(\alpha,\beta)\). Declaring high iff \(\lambda\ge\Lambda\):

- every mode on shell \(\alpha\) is **Low**,
- every mode on shell \(\beta\) is **High**.

Hence parent pairs classify exactly as: LL = both on \(\alpha\), HL = mixed, HH = both on \(\beta\). No other channels exist on two-shell support.

### Lemma I — Elementary unmatched-\(\Lambda\) HL/LL route is killed

After low-mode absorption \(D_s\ge(1-\theta)^2\Lambda^2 X_L\), elementary Sobolev / paraproduct remainders leave dimensionless leftovers with unmatched \(\Lambda\) powers (prototype \(\rho=\Lambda^{1/2} X/Y\)). Under lattice dilation, \(\rho\mapsto\rho/n\) while \(\mathcal{R}_\star\) is flat. Therefore **no** close that requires a uniform bound on such a leftover is dilation-invariant / geometry-only.

**This kills filing HL/LL as “classical for free.”** It does **not** kill PRODUCT-BLOCK: a different, genuinely geometric HL/LL bound may still exist.

### Lemma J — Signed Stokes weights on two-shell (feeds \((T_c)_+\))

On the same two-shell class, the centered weight on a child mode is \(\lambda(\lambda-\Lambda)\):

\[
\alpha(\alpha-\Lambda)<0<\beta(\beta-\Lambda).
\]

Only triad output landing on the **high** shell can contribute positively to \(T_c\). Low-shell children feed \(T_c\le 0\) for that term. Combined with Lemma H: the \((T_c)_+\) budget on two-shell is carried by HH→β, HL→β, and LL→β only.

### Lemma K — HH mass control (\(\theta>1\))

Declare high iff \(\lambda_k\ge\theta\Lambda\) with \(\theta>1\). Then

\[
X_H
:=\sum_{\lambda_k\ge\theta\Lambda}\lambda_k|v_k|^2
\le
\frac{D_s}{(\theta-1)^2\Lambda^2}.
\]

**Proof.** On the high set, \(|\lambda-\Lambda|\ge(\theta-1)\Lambda\), so
\(D_s=\sum\lambda(\lambda-\Lambda)^2|v_k|^2\ge(\theta-1)^2\Lambda^2 X_H\).  

**Corollary.** \(E_H\le X_H/(\theta\Lambda)\le D_s/(\theta(\theta-1)^2\Lambda^3)\).  
Useful bookkeeping for HH estimates; **does not** by itself bound \(T_c^{\mathrm{HH}}\) against \(\sqrt{D_s E Y}\) (Agmon / \(\|\nabla v_H\|_\infty\) still lose geometry-only control).

### Lemma L — Cauchy-sufficient route strategically blocked (face family)

Write

\[
Q(v)=\frac{\|A^{1/2}B(v,v)\|_2^2}{E\,Y}.
\]

Lemma A gives \(\mathcal{R}_\star(v)\le Q(v)\) whenever \(T_c>0\). So \(\sup Q<\infty\) would close PRODUCT-BLOCK.  

**Face family.** For \(K\in\mathbb{N}\), let \(v^{(K)}\) be \(L^2\)-normalized with Fourier support on the face
\(\{k_1=K:\ |k_2|,|k_3|\le K\}\setminus\{0\}\) and \(\widehat v_k\parallel P_k e_2\). Then (exact finite-support computation in `uniform_rstar_hh_push.py`):

| \(K\) | 2 | 4 | 6 | 8 | 10 | 12 | 16 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| \(Q(v^{(K)})\) | 0.30 | 0.73 | 1.38 | 2.25 | 3.33 | 4.62 | 7.83 |
| \(Q/K^2\) | 0.074 | 0.046 | 0.038 | 0.035 | 0.033 | 0.032 | 0.031 |
| \(T_c\) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

So \(Q\) is **monotone through \(K\le 16\)** with \(Q/K^2\searrow c_\star\approx 0.03\), while \(\mathcal{R}_\star\) is vacuous/zero on the same fields (\(T_c=0\)).

**What this kills.** Closing PRODUCT-BLOCK by proving a geometry-only \(\sup Q<\infty\) with an \(O(1)\) constant suggested by sparse-mode samples is **dead**: face shapes already force \(Q\gtrsim 7\), and the coherent face×face scaling heuristic (\(Q\sim c K^2\)) predicts \(Q\to\infty\).

**What this does *not* kill.** PRODUCT-BLOCK / \(\sup\mathcal{R}_\star<\infty\) — on these fields \(\mathcal{R}_\star\) does not blow. Cancellations between \(B\) and \(A(A-\Lambda)v\) are **mandatory**, not optional.  

**Conjecture L (not a theorem).** \(Q(v^{(K)})\to\infty\) as \(K\to\infty\). Empirically \(Q\sim c_\star K^2\). Full discrete convolution lower bound not closed in this pass — do **not** file unboundedness of \(Q\) as proved.

### Lemma M — True same-shell HH→L is lattice-sparse (diagnostic)

Pairs of parents on shell \(\beta\) summing to a child on shell \(\alpha<\beta\) are often **empty** on \(\mathbb{Z}^3\) (e.g. \((\alpha,\beta)\in\{(1,5),(1,13),(5,25)\}\)). When triples exist (e.g. \((2,10),(2,50)\)), light phase/amplitude samples give \(\mathcal{R}_\star\lesssim 10^{-2}\) with no divergence. Not a kill; not a bound.

---

## 2. What failed / what is not proved

### 2.1 HL/LL is **not** classical (correction + route kill)

The prior attack map called HL/LL “classical-ish bookkeeping.” **That oversells the state of the estimate.**

Elementary Sobolev / paraproduct bounds on \(B^{\mathrm{HL}}\) and \(B^{\mathrm{LL}}\) produce **field-dependent powers of \(\Lambda\)** (lose dilation invariance). Absorbing low-mode mass via

\[
D_s\ge(1-\theta)^2\Lambda^2 X_L
\qquad(\lambda<\theta\Lambda)
\]

still leaves ratios that are not controlled by \(E Y\) alone without further structure. Lemma I makes the dilation obstruction explicit: unmatched-\(\Lambda\) leftovers scale as negative powers of \(n\) under \(k\mapsto nk\).

**Status:** HL/LL bound of the form \((T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}})_+^2\le C_{\mathrm{HL/LL}} D_s E Y\) with geometry-only \(C\) is **OPEN**, not filed. The elementary route is **dead**; a geometric route is still required.

### 2.2 HH remains open

Same for \((T_c^{\mathrm{HH}})_+^2\le C_{\mathrm{HH}} D_s E Y\). Ordinary energy-only Agmon products do not close it. Lemma K controls \(X_H\) for \(\theta>1\) but does not upgrade to a geometric HH product. Face-family blowup of \(Q\) shows why crude \(\|A^{1/2}B\|_2\) control cannot be the whole story for \(\mathcal{R}_\star\).

### 2.3 Sufficient Cauchy form \(\sup Q<\infty\) — strategically blocked

See Lemma L. Do not attempt to green PRODUCT-BLOCK solely by bounding \(Q\) with sparse-mode intuition. Either prove a sharp inequality that uses the signed weight \(A(A-\Lambda)v\), or produce a true \(\mathcal{R}_\star\to\infty\) family.

### 2.4 Kill lane — no \(\mathcal{R}_\star\to\infty\) counterexample found

Analytic constructions checked (not an HPC sweep):

| Family | Outcome |
| --- | --- |
| Near-shell \(\varepsilon\to 0\) | \(\mathcal{R}_\star\to K_{\alpha,\beta}<\infty\) (no kill) |
| Two-shell amplitude / ratio sweeps | Finite sample \(\mathcal{R}_\star\lesssim 10^{-2}\); no divergence in ratio |
| Filled Fourier balls (\(|k|\le K\)) | \(\mathcal{R}_\star\) stays small; often \(T_c\le 0\) |
| Face fields \(v^{(K)}\) (Lemma L) | \(Q\) grows; \(\mathcal{R}_\star=0\) (no PRODUCT-BLOCK kill) |
| True same-shell HH→L triples (Lemma M) | Sparse; sampled \(\mathcal{R}_\star\) small |
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

**Former sufficient target (now strategically blocked as a solo close):**

\[
\|A^{1/2}B(v,v)\|_2^2\le C\,E\,Y
\qquad\text{(geometry-only \(C\))}.
\]

Lemma L: do not expect an \(O(1)\) \(C\) from sparse-mode intuition; face shapes inflate \(Q\) while \(\mathcal{R}_\star\) stays zero. A close must use the signed weight against \(A(A-\Lambda)v\), or bound channels in a cancellation-aware way.

Isolated HH obstruction form (still live):

\[
\bigl(T_c^{\mathrm{HH}}\bigr)_+^2\le C_{\mathrm{HH}}\,D_s\,E\,Y,
\]

with geometric HL+LL still required (not free).

---

## 4. Code (minimal)

| Path | Role |
| --- | --- |
| `scripts/ns_attacks/uniform_rstar_identities.py` | Verify Lemmas A–D residuals; light kill/sanity probe |
| `scripts/ns_attacks/uniform_rstar_dilation.py` | Lemmas G–J: dilation ledger, two-shell dichotomy, naive-Λ route kill |
| `scripts/ns_attacks/uniform_rstar_hh_push.py` | Lemmas K–M: HH mass, face \(Q\)-block, HH→L sparsity |
| `scripts/ns_attacks/uniform_rstar_attack.py` | Existing Λ-channel maximizer (subordinate) |
| `scripts/ns_attacks/ns_lemma_star_core.py` | Exact finite-support \(T_c\), \(D_s\), \(\mathcal{R}_\star\) |
| `tests/test_uniform_rstar_dilation.py` | Smoke tests for G–J |
| `tests/test_uniform_rstar_hh_push.py` | Smoke tests for K–M |

```bash
python3 scripts/ns_attacks/uniform_rstar_identities.py
python3 scripts/ns_attacks/uniform_rstar_dilation.py
python3 scripts/ns_attacks/uniform_rstar_hh_push.py
python3 scripts/ns_attacks/uniform_rstar_attack.py --quick
python3 -m pytest tests/test_uniform_rstar_attack.py tests/test_uniform_rstar_dilation.py tests/test_uniform_rstar_hh_push.py -q
```

---

## 5. Honesty table

| Item | Status |
| --- | --- |
| PRODUCT-BLOCK / \(\sup\mathcal{R}_\star<\infty\) | **OPEN** |
| Lemma★ / DA-NS-1 | **HYPOTHESIS** |
| Lemma A–F | **Proved** (as stated) |
| Lemma G–J (dilation / dichotomy / route kill / signs) | **Proved** (as stated) |
| Lemma K (HH mass \(\theta>1\)) | **Proved** |
| Lemma L (face \(Q\) block) | **Strategic block recorded**; \(Q\to\infty\) = **CONJECTURE** |
| Lemma M (HH→L sparsity) | **Diagnostic** (proved as stated) |
| Elementary unmatched-Λ HL/LL route | **KILLED** |
| Cauchy-sufficient \(\sup Q<\infty\) as solo close | **STRATEGICALLY BLOCKED** |
| HL/LL geometric bound | **OPEN** (not classical) |
| HH geometric bound | **OPEN** |
| Kill family \(\mathcal{R}_\star\to\infty\) | **Not found** (lane LIVE) |
| Clay Statement B | **NOT SOLVED** |
| Publisher / X “clean proof” offer | **Gate CLOSED** — [`GATED-PUBLISH-CHECKLIST.md`](./GATED-PUBLISH-CHECKLIST.md) |
| Numerics = proof? | **No** |

---

## 6. One-line status

**Still OPEN. Proved: Cauchy/channels/\(D_s\)/dilation/HH-mass; elementary Λ-HL/LL killed; Cauchy-only \(\sup Q\) strategically blocked by face family. Remainder: geometric \(T_c^{\mathrm{HH}}\) and \(T_c^{\mathrm{HL/LL}}\) with cancellations. No \(\mathcal{R}_\star\) kill. NS / Clay B not solved.**
