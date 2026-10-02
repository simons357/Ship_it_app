# Square-root candidate — small-case attack

**Candidate (UNPROVED):**

\[
|T_c|
\le
C\,\|\nabla u\|_3\sqrt{Y\,D_s}.
\]

**Honesty lock.** The exact near-shell obstruction motivates the square-root
in \(D_s\). It does **not** establish the estimate. A successful script run
verifies the tested Fourier identities. The uniform inequality and its
required time budget remain **separate proof obligations**. Lemma★ /
PRODUCT-BLOCK / Navier–Stokes regularity are **not** closed here.

Code: `scripts/ns_attacks/exact_fourier.py`, `scripts/ns_attacks/sqrt_estimate_attack.py`.  
Tests: `tests/test_sqrt_estimate_attack.py`.

---

## What is certified, and what is not

| Object | How | Status after a green run |
| --- | --- | --- |
| \(Y=\sum\lambda_k^2\|v_k\|^2\) | exact \(Q\)-arithmetic on finite support | **identity** |
| \(D_s=Z-Y^2/X\) and the two equivalent sums | exact, cross-checked | **identity** |
| \(T_c=M-\Lambda N=\sum\lambda_k(\lambda_k-\Lambda)T_k\) | complete signed triad sum, never \(|\mathrm{Im}|\) | **identity** |
| \(\sum_k T_k=0\) | energy conservation on mean-zero fields | **identity** |
| \(\widehat{|\nabla u|^2}(0)=X\) | exact convolution | **identity** |
| \(\|\nabla u\|_3\) | certified \(L^2\) lower / Riesz–Thorin \(L^4\) upper | **bounds**, not a value |
| Quotient \(Q=\|T_c\|/(\|\nabla u\|_3\sqrt{YD_s})\) | \(Q_{\mathrm{lb}}\) from the \(L^3\) upper bound; \(Q_{\mathrm{ub}}\) from \(\|\nabla u\|_3\ge\sqrt{X}\) | **interval** |
| \(\exists C<\infty\) for every field | — | **OPEN** |
| Time budget / occupation integral | — | **OPEN** |

Sampled physical-space quadrature **cannot** certify a counterexample:
an uncertified \(\|\nabla u\|_3\) in the denominator does not produce a
rigorous \(Q_{\mathrm{lb}}\). This board never uses a grid sample for
\(\|\nabla u\|_3\).

---

## Near-shell obstruction (motivation only)

On a main shell plus satellite amplitude \(\varepsilon\),

\[
T_c\sim\varepsilon,\qquad D_s\sim\varepsilon^2,
\]

so \(T_c/D_s\) blows up while \(T_c/\sqrt{D_s}\) stays ordered. That kills a
linear-in-\(D_s\) same-time bound and is why the square-root is the candidate.
It is not a proof of any \(L^3\) estimate.

---

## Small-case priorities

1. **Nearly single-shell states with several interacting triads.**
   Shell 5 parents with three independent closings onto shell 10.
2. **Widely separated frequencies with varied amplitudes.**
   Shells \(1\)–\(2\) versus \(36\)–\(72\), plus occupied HL cross outputs.
3. **Dense packets with coordinated phases.**
   Phase-locked box packet, and a P/Q affine packet with occupied cross
   outputs (contributions added, not overwritten).

Finite certified \(Q_{\mathrm{lb}}\) on this board is **not** a kill.
A kill requires \(Q_{\mathrm{lb}}\to\infty\) along a family.

---

## Runtime

```bash
python3 scripts/ns_attacks/sqrt_estimate_attack.py
python3 -m unittest tests.test_sqrt_estimate_attack -v
```

Display columns \(Q_{\mathrm{lb}}\sim\) / \(Q_{\mathrm{ub}}\sim\) are
floating-point renderings of exact sixth / square powers. Comparisons
in the tests stay in \(\mathbb{Q}\).

---

## Do not glue

- Φ-renorm swirl algebra is a different book.
- Lemma★ shape form \(\mathcal{R}_\star=(T_c)_+^2/(D_s\,E\,Y)\) is a
  different quotient. This note does not green ★.
- Clay Statement B remains open.
