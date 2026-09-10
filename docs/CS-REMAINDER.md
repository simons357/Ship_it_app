# ABC_λ exact printout — λ=2,4,8,16

10 September 2026. **NS not solved.** Evaluator ≠ proof.

Normalization is the write-up, not an ABC-only variant:

\[
\mathcal R_\star
=
\frac{(T_c)_+^2}{\mathcal D_s\,E\,Y}
\qquad\text{from }\texttt{scripts/ns\_lemma\_star\_core.py}.
\]

\(T_c(-v)=-T_c(v)\). On this family \(T_c<0\), so boxed \(\mathcal R_\star=0\).
The column below is boxed \(\mathcal R_\star(-v)=T_c^2/(\mathcal D_s E Y)\).
Same object. Formula lock vs `stokes_moments.probe` sits
(\(T_c,D_s,\mathcal R_\star\) err \(<10^{-15}\)).

H1 is a different integral. **H1 was not run on ABC_λ.**
The H1-TUBE ABC is exact Beltrami, not this field.

## What this package does on this field

On this family, with this normalization:

- Target A fails (\(\mathcal R_\star\) does not stay \(O(1)\)).
- The CS remainder \(\|A^{1/2}B\|_2\le C\sqrt{EY}\) fails.
- Lemma★ fails as a closer for unaugmented NSE.

Stop patching Lemma★. Do not send this as a solve.
N-shell samples still saturate. That is a different family.

## Exact-check table

`scripts/ns_attacks/cs_remainder_exact_check.py`
JSON: `results/cs_remainder_bump/exact_core_check.json`
Grids \(n=16\lambda\) (same as the FFT local_abc table).

Full-field FFT (Galerkin; convention locked on a sparse triad).
Flip column = write-up \(\mathcal R_\star(-v)\).

| \(\lambda\) | \(n\) | \(\|A^{1/2}B\|_2/\sqrt{EY}\) | \(\mathrm{CS}/\lambda^{3/2}\) | \(\mathcal R_\star(-v)\) | \(\mathcal R_\star/\lambda^3\) |
|---|---|---|---|---|---|
| 2 | 48 | 2.492 | 0.881 | 0.005170 | \(6.46\times 10^{-4}\) |
| 4 | 64 | 7.104 | 0.888 | 0.04086 | \(6.38\times 10^{-4}\) |
| 8 | 128 | 20.114 | 0.889 | 0.3266 | \(6.38\times 10^{-4}\) |
| 16 | 256 | 56.899 | 0.889 | 2.612 | \(6.38\times 10^{-4}\) |

Standalone / embed on a high-energy export (λ=2: `R_star`; λ≥4: embed FFT = triad on that support):

| \(\lambda\) | modes | keep | \(\mathcal R_\star(-v)\) | \(\mathcal R_\star/\lambda^3\) |
|---|---|---|---|---|
| 2 | 1902 | 0.9999 | 0.004542 | \(5.68\times 10^{-4}\) |
| 4 | 15284 | 0.9999 | 0.03586 | \(5.60\times 10^{-4}\) |
| 8 | 86318 | 0.999 | 0.2212 | \(4.32\times 10^{-4}\) |
| 16 | 690576 | 0.999 | 1.767 | \(4.31\times 10^{-4}\) |

Both columns climb. FFT is \(\sim\lambda^3\) to three digits from λ=4 to 16.
Export 8→16 exponent \(\log_2(1.767/0.221)=2.997\).
Same truncated field: embed \(T_c\) equals the exact triad sum to \(10^{-13}\) at λ=2.
\(v(n\cdot)\) leaves boxed \(\mathcal R_\star\) invariant.

The 99% cutoff in the older printout was a different field.
This printout uses the write-up objects on \(n=16\lambda\).

Stay in this chat.
