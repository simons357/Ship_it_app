# CS remainder is false. Target A is false.

10 September 2026. **NS not solved.** Lemma★ does not close unaugmented NSE.

Checked against the exact triad core before the stamp.
`scripts/ns_attacks/cs_remainder_exact_check.py`
JSON: `results/cs_remainder_bump/exact_core_check.json`

## Locks (sit)

- Fast triad \(T_c\) matches `stokes_moments.probe` on a three-mode field.
- Same truncated ABC field: FFT \(T_c\) equals the triad sum to \(10^{-13}\).
- Fourier dilation \(v(n\cdot)\) leaves that \(\mathcal R_\star\) invariant (rel \(=0\)).

The first table compared a **full** FFT field to a **99% energy cutoff**.
Those are different fields. \(T_c\) lives in the tail. That gap is not
a convention bug.

## Exact-core table (99% energy cutoff)

Direct pair sum on the exported modes. Reverse so \(T_c>0\).

| \(\lambda\) | modes | \(\mathcal R_\star\) | \(\mathcal R_\star/\lambda^3\) |
|---|---|---|---|
| 2 | 836 | 0.001748 | \(2.19\times 10^{-4}\) |
| 3 | 2820 | 0.005181 | \(1.92\times 10^{-4}\) |
| 4 | 6672 | 0.013669 | \(2.14\times 10^{-4}\) |

Climbs. Same power as the full-field FFT table.

## Full-field FFT (Galerkin, all modes)

| \(\lambda\) | \(\|A^{1/2}B\|_2/\sqrt{EY}\) | \(\mathcal R_\star\) |
|---|---|---|
| 2 | 2.492 | 0.00517 |
| 3 | 4.607 | 0.0173 |
| 4 | 7.104 | 0.0409 |
| 5 | 9.934 | 0.0798 |
| 6 | 13.062 | 0.138 |
| 8 | 20.114 | 0.327 |

\(\|A^{1/2}B\|_2/\sqrt{EY}\sim 0.88\,\lambda^{3/2}\).
\(\mathcal R_\star\sim 6.47\times 10^{-4}\,\lambda^3\).

## Field

\[
v_\lambda
=
-
\frac{P(\gamma_\lambda\,\mathrm{ABC}_\lambda)}
{\|P(\gamma_\lambda\,\mathrm{ABC}_\lambda)\|_2},
\qquad
\widehat{\gamma}_\lambda(k)=\exp(-|k|^2/(2\lambda^2)).
\]

N-shell samples saturate. \(v(n\cdot)\) is flat. This family is
spatial concentration on a fixed torus. Target A is false.
The CS remainder is false. H1 is a different integral.

Stay in this chat.
