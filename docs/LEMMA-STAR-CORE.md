# Independent Lemma★ core

10 September 2026. Phone lock. **Exact evaluator, not a proof.**
**Lemma★ is still open. NS not solved.**
ABC_λ table: `docs/CS-REMAINDER.md`. Not a falsifier.

Standalone: `scripts/ns_lemma_star_core.py`.
Does not import the Stokes library.
\(v_{-k}=\overline{v_k}\) is enforced in `set_mode`.
\(T_c\) is a direct triad sum. Two \(\mathcal D_s\)
formulas are checked on every \(\mathcal R_\star\) call.
Live `stokes_moments.py` was **not overwritten**.
Shim only: `scripts/ns_attacks/ns_lemma_star_core.py`.
Tests: `tests/test_ns_lemma_star_core.py`

\[
\mathcal R_\star
=
\frac{(T_c)_+^2}{\mathcal D_s\,E\,Y}
\]

Same objects as
[`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md),
[`math/ns_attacks/LEMMA_STAR_CANONICAL.md`](math/ns_attacks/LEMMA_STAR_CANONICAL.md)
and
[`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Not a second claim. A match against `probe()`
is a code check, not a bound.

Engineering only (same math):
- `scale(a)` requires real \(a\) (reality).
- Shell points use integer `isqrt`.
- \(T_c\) is also checked against \(M-\Lambda N\).
  Near-zero uses an absolute floor so
  single-shell cancellation is not a false fail.
- Aligned \(z_\beta\parallel\Pi_\beta B\) recovers
  \(K_{\alpha,\beta}\). A misaligned closer does not.

This file is an exact evaluator, not a proof.
Lemma★ is still open. Stay in this chat.
