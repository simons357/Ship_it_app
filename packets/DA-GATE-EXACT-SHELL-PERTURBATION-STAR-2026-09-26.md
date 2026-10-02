# DA gate — exact-shell perturbation ★ (local)

**26 September 2026.** Restricted statement only.
Unrestricted \(\sup\mathcal R_\star<\infty\) stays **KILLED**.
DA-NS-2 stays **OPEN**. Ordinary NS is not solved.

Proof:
[`../docs/ns-recovery/EXACT-SHELL-PERTURBATION-STAR.md`](../docs/ns-recovery/EXACT-SHELL-PERTURBATION-STAR.md).
Machine: `scripts/da_gate_exact_shell_perturbation_star.py`.

Does **not** alter the locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) packets. Does **not** stamp \(r\sim\kappa^{-1/2}\).

---

## Proved

For \(Aw=\alpha w\), \(\beta>0\), \(r=\beta/\alpha\),

\[
\bigl\|\Pi_\beta B(w,w)\bigr\|_2^2
\le
\tfrac34\beta\bigl(1-\beta/(4\alpha)\bigr)\,\|w\|_2^4,
\]

\[
K_{\alpha,\beta}(w)
\le
\tfrac34 r^2\bigl(1-r/4\bigr)
\le
16/9,
\]

\[
\bigl\|\Pi_\beta B(w,w)\bigr\|_2
\le
\tfrac43\,\alpha\,\beta^{-1/2}\,\|w\|_2^2.
\]

The constant \(4/3\) is sharp for this argument (maximum of the
polynomial at \(r=8/3\)). Not asserted as a field maximizer.

On the aligned 9B family, \(\lim\varepsilon\to 0\,\mathcal R_\star=K_{\alpha,\beta}(w)\le 16/9\).

Extreme satellites \(r\to 0\) and \(r\to 4\) make the bound
vanish. Conservation geometry is locally neutralized there, not
refuted.

---

## Still dead / still open

| Item | Status |
|---|---|
| Unrestricted \(\sup\mathcal R_\star<\infty\) | **KILLED** (\(v_n\), localized bump) |
| Comparable / multi-shell remainder | **OPEN** |
| DA-NS-2 | **OPEN** |
| \(r\sim\kappa^{-1/2}\) as a decision | **not stamped** |
| Q4-0 | **plan only, not run** |

**NS not solved.**
