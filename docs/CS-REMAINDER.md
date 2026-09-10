# Localized ABC — evaluator, not a proof. ★ still OPEN.

10 September 2026. **NS not solved.** Exact core ≠ proof.
H1 is a different integral and was **not** run on ABC_λ.
Augmented / Q-stack is out of this book.

Score vs SuperGrok and DA:
`docs/ns-recovery/CS-REMAINDER-VS-DA-REJECT.md`
(PR 45 comparison: https://github.com/simons357/Ship_it_app/pull/45).

This book’s kill rule: \(\mathcal R_\star\to\infty\) kills ★.
One large finite value only raises \(C_{\mathrm{geom}}\).
Largest FFT number on the gate table is **0.327 at λ=8**
(after reverse). That is not a falsifier. Do not stamp
Target A / CS / ★-as-closer. Do not stop patching Lemma★.

## Same \(\mathcal R_\star\) (Claude 1)

Write-up: \(\mathcal R_\star=(T_c)_+^2/(\mathcal D_s E Y)\).
JSON `R_star` is that object and is **0** here (\(T_c<0\)).
The published climb is `R_star_signed` \(=T_c^2/(\mathcal D_s E Y)\)
= canonical \(\mathcal R_\star(-v)\). Not an ABC-only variant.

## H1 on ABC_λ (Claude 2)

**Untested.** Named only. Do not start H1 from this page.

## Exact script — four jobs, already ran

`scripts/ns_attacks/cs_remainder_exact_check.py`

1. 3-mode triad vs `probe` (on that field \(T_c=0\); \(\mathcal D_s\) matches).
2. Export 99% energy modes and sum the triad — **λ=2, 3, 4 only**.
3. Same truncated field on a grid: FFT \(T_c\) = triad to \(10^{-13}\).
4. \(v(n\cdot)\) leaves \(\mathcal R_\star\) flat.

It never ran λ=8 or 16. More finite rows would not close a kill.

## FFT table (full field; different from the cutoff)

| λ | CS \(\|A^{1/2}B\|_2/\sqrt{EY}\) | \(\mathcal R_\star(-v)\) |
|---|---|---|
| 2 | 2.492 | 0.00517 |
| 3 | 4.607 | 0.0173 |
| 4 | 7.104 | 0.0409 |
| 5 | 9.934 | 0.0798 |
| 6 | 13.062 | 0.138 |
| 8 | 20.114 | **0.327** |

Fit on six grids: CS \(\sim 0.88\lambda^{3/2}\),
\(\mathcal R_\star\sim 6.47\times 10^{-4}\lambda^3\).
A fit is not \(\mathcal R_\star\to\infty\).

## Exact-core table (99% cutoff — a different field)

| λ | modes | \(\mathcal R_\star(-v)\) | \(T_c\) rel vs full FFT |
|---|---|---|---|
| 2 | 836 | 0.001748 | 0.535 |
| 3 | 2820 | 0.005181 | 0.565 |
| 4 | 6672 | 0.013669 | 0.542 |

N-shell max saturates. This family does not on the grids
they ran. That is a live kill-lane clue. It is not a
logged reject of ★.

Stay in this chat.
