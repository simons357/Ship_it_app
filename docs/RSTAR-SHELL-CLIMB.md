# R★ maximizer — N shells vs |k|_max

10 September 2026. **Not a proof. NS not solved.**

Target A: \(|T_c|\le C\sqrt{\mathcal D_s\,E\,Y}\),
i.e. \(\sup\mathcal R_\star<\infty\) independent of
\(|k|_{\max}\). Growing output occupancy \(s\) stays
the live hole in the phase-free bound \(K\le 16s\).

## Table

One \(B(w,w)\) per sample on shell \(\alpha\); every
output \(\beta\) scored. \(N=3,4,5\) perturb the
best two-shell field at that \(|k|_{\max}\).

| \(N\) | \(\lvert k\rvert_{\max}\) | \(\max\mathcal R_\star\) | \(\max K\) | \(\max s\) | maximizer shells |
|---|---|---|---|---|---|
| 2 | 2 | 0.393 | 0.396 | 48 | 1, 2 |
| 2 | 3 | 0.572 | 0.577 | 72 | 1, 2 |
| 2 | 4 | 0.585 | 0.590 | 96 | 1, 2 |
| 2 | 5 | 0.498 | 0.502 | 120 | 16, 32 |
| 2 | 6 | 0.610 | 0.615 | 144 | 1, 2 |
| 2 | 8 | 0.433 | 0.437 | 192 | 64, 128 |
| 3 | 2 | 0.005 | — | — | 1, 2, 5 |
| 3 | 5 | 0.436 | — | — | 16, 32, 11 |
| 3 | 8 | 0.407 | — | — | 64, 128, 70 |
| 4 | 5 | 0.409 | — | — | 16, 32, 4, 14 |
| 4 | 8 | 0.394 | — | — | 64, 128, 35, 12 |
| 5 | 5 | 0.439 | — | — | 16, 32, 18, 48, 12 |
| 5 | 8 | 0.425 | — | — | 64, 128, 62, 51, 61 |

Best on this run: \(\mathcal R_\star=0.610\) at
\(N=2\), \(|k|_{\max}=6\), shells \((1,2)\), \(s=12\).
9B peak \(K\approx 0.641\) at \((4,8)\) is the same
order. Dilations of \((1,2)\) stay in that band.

\(\max s\) grows \(48\to 192\). The maximizer stays
on \(s=12\) (the \((1,2)\) family). Extra shells did
not beat two.

## Verdict

Does not climb **on this family**. Extra shells do
not beat two. Fourier dilation \(v(n\cdot)\) stays
flat.

ABC_λ is a different family: write-up \(\mathcal R_\star\sim\lambda^3\)
at \(\lambda=2,4,8,16\). See `docs/CS-REMAINDER.md`.
This N-shell table saturates. That one does not.

JSON: `results/rstar_shell_climb/maximizer.json`
Script: `scripts/ns_attacks/maximize_rstar_shells.py`

Stay in this chat.
