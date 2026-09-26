# Small-lattice ABC vs locked \(D_s\), \(T_c\), \(\mathcal R_\star\)

**Date:** 10 September 2026  
**Evaluator:** [`scripts/abc_small_lattice_rstar.py`](../../scripts/abc_small_lattice_rstar.py)  
**Core:** [`scripts/ns_lemma_star_core.py`](../../scripts/ns_lemma_star_core.py)  
**JSON:** [`results/abc_small_lattice_rstar.json`](../../results/abc_small_lattice_rstar.json)

**NS not solved. Lemma★ OPEN.** Unrestricted lemma is **not** killed.

---

## Proof files first (locked)

Canonical: [`docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md`](../math/ns_attacks/LEMMA_STAR_CANONICAL.md)  
Formulas: [`docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md)

\[
D_s=Z-Y^2/X=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2,
\quad
T_c=\sum_k\lambda_k(\lambda_k-\Lambda)T_k,
\quad
\mathcal R_\star=\frac{(T_c_+)^2}{D_s E Y}.
\]

If \(D_s=0\), one shell and \(T_c=0\). Not a kill. One finite \(\mathcal R_\star\) only raises \(C_{\mathrm{geom}}\).

---

## Family (well-posed on paper)

\[
\mathrm{ABC}_\lambda(x)=(\sin\lambda z+\cos\lambda y,\;\sin\lambda x+\cos\lambda z,\;\sin\lambda y+\cos\lambda x),
\quad
\widehat\gamma_\lambda(k)=\exp(-|k|^2/(2\lambda^2)),
\]
\[
v_\lambda=-\frac{P(\gamma_\lambda\,\mathrm{ABC}_\lambda)}{\|P(\gamma_\lambda\,\mathrm{ABC}_\lambda)\|_2}.
\]

Spatial product = convolution of the six ABC spikes with \(\widehat\gamma\). This run keeps \(\widehat\gamma\) on the box \(|k|_\infty\le R\). That is the **truncated envelope**, exact for finite Fourier support. It is **not** PR #24’s FFT Galerkin table.

`set_mode` enforces \(k\cdot v_k=0\) and \(v_{-k}=\overline{v_k}\). Hygiene: every row `div_free` and `real_valued` (residuals \(<10^{-12}\)).

---

## Small-lattice table (locked shape form)

`R_star` is \((T_c)_+\). `R_signed` \(=T_c^2/(D_s E Y)=\mathcal R_\star(-v)\) when \(T_c<0\).

| λ | R | modes | \(D_s\) | \(T_c\) | \(\mathcal R_\star\) | \(\mathcal R_\star(-v)\) | vacuous |
|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 0 | 6 | 0 | 0 | 0 | 0 | yes |
| 1 | 1 | 80 | 6.66 | −0.155 | 0 | 0.000415 | no |
| 1 | 2 | 274 | 13.88 | −0.251 | 0 | 0.000420 | no |
| 2 | 0 | 6 | 0 | 0 | 0 | 0 | yes |
| 2 | 1 | 134 | 53.0 | −0.00283 | 0 | \(3.2\times10^{-9}\) | no |
| 2 | 2 | 424 | 257 | −3.25 | 0 | 0.000397 | no |
| 3 | 0 | 6 | 0 | 0 | 0 | 0 | yes |
| 3 | 1 | 162 | 232 | \(\approx0\) | 0 | 0 | no |
| 3 | 2 | 574 | 929 | −1.35 | 0 | 0.000007 | no |

Dilation \(v(n\cdot)\) on (λ=1, R=1): \(\mathcal R_\star(-v)\) unchanged (rel \(2.6\times10^{-16}\)).

On the R=2 slice, signed \(\mathcal R_\star\) is **0.000420, 0.000397, 0.000007**. It does **not** climb.

---

## Unrestricted lemma

**Not killed.** Pure ABC is one shell. The truncated envelope is div-free and real. Locked \(\mathcal R_\star\) after reverse stays \(<5\times10^{-4}\) on these lattices. That is not \(\mathcal R_\star\to\infty\).

Do not import PR #24’s FFT λ³ fit as this run. SuperGrok falsifier stamp stays refused: [`SUPERGROK-ABC-LOCK.md`](SUPERGROK-ABC-LOCK.md).
