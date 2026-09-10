# Independent Lemma★ core

10 September 2026. Phone lock. **Not a proof. NS not solved.**

Paste: `ns_lemma_star_core.py`. Self-contained
writing of the boxed shape quantities. Direct
triad sum. Two \(\mathcal D_s\) formulas
cross-checked on every \(\mathcal R_\star\)
call. Live `stokes_moments.py` was **not overwritten**.

Code: `scripts/ns_attacks/ns_lemma_star_core.py`
Tests: `tests/test_ns_lemma_star_core.py`

\[
\mathcal R_\star
=
\frac{(T_c)_+^2}{\mathcal D_s\,E\,Y}
\]

Same objects as
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

Remaining job: uniform \(\mathcal R_\star\), or a
family that diverges. One large finite value is
not a kill. Stay in this chat.
