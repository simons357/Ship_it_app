# Centered spectral drift — current-files inventory

**16 September 2026.** Direct centered route after unrestricted ★
(\(B^\star\)) is dead. Identities only. **No new proof.**
Ordinary NS is not solved. Soft X silent.

Do not redo: Theorem H, SND persistence, 9D/\(K_{\alpha,\beta}\) sweeps,
augmented NS, SFE/HB, or `CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md`
(that search said the identities were lost; they are not).

---

## 1. Exact identities (proved / evaluator-checked)

On mean-zero divergence-free \(u\) on \(\mathbb T^3\), \(A=-P\Delta\),
\(\lambda_k=|k|^2\):

\[
X=\|A^{1/2}u\|_2^2,\quad
Y=\|Au\|_2^2,\quad
Z=\|A^{3/2}u\|_2^2,\quad
\Lambda=Y/X,
\]
\[
T_c=M-\Lambda N=-\langle B(u,u),A(A-\Lambda)u\rangle
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k,
\]
\[
\mathcal D_s=Z-\Lambda Y=Z-Y^2/X
=\|(A-\Lambda)A^{1/2}u\|_2^2
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|u_k|^2\ge 0.
\]

Also exact: two-point form
\(\mathcal D_s=\frac1{2X}\sum_{k,\ell}\lambda_k\lambda_\ell(\lambda_k-\lambda_\ell)^2|u_k|^2|u_\ell|^2\);
two-shell
\(\mathcal D_s=\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta/X\);
signed triads
\(T_k=\sum_{p+q=k}\mathrm{Im}[(q\cdot u_p)(u_q\cdot\overline{u_k})]\)
(never abs); \(N=\sum\lambda_k T_k\), \(M=\sum\lambda_k^2 T_k\);
spectral Cauchy \(X^2\le E Y\Rightarrow X\le E\Lambda\).
**The centered equation** (exact, not an estimate):
\(\Lambda'=-(2\nu/X)D_s+(2/X)T_c=2(T_c-\nu D_s)/X\),
equivalently \((\log\Lambda)'=2(T_c-\nu D_s)/Y\).
Page: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
homogeneity \(T_c(au)=a^3 T_c(u)\), \(\mathcal D_s(au)=a^2\mathcal D_s(u)\);
one shell \(\Rightarrow T_c=\mathcal D_s=0\).

Two-shell gap-cancel (identity): \(T_\alpha+T_\beta=0\) and
\(T_c=(\alpha-\beta)(\alpha\beta E/X)T_\alpha\). The gap drops out of
\(\mathcal R_\star\). That is **not** a bound on \(T_\beta\).

Algebra after a remainder (not the remainder): if
\(T_c\le\theta\nu\mathcal D_s+K X\) with \(\theta<1\), then
\(\Lambda'\le 2K\). Y-cousin: \((\log\Lambda)'\le 2K_Y\).
One direction only.

Near-scale LP identities that sit **beside** this (not a \(T_c\) bound):
TJJ-Trans (local transport integral vanishes), TJJ-α (stretch
\(=\int\alpha_{\mathrm{loc},j}|\Delta_j\omega|^2\)). First new C10
arrow (template \(\to a_+\)) is empty. No seated
\(T_c\le C\sum a_+ Z_j\).

NoCancellation reconstruction: **never written.** Palinstrophy is
not a named lemma here; \(\mathcal D_s\) is the spectral-variance
object.

---

## 2. Strongest direct bound on \(T_c\)

**None that is useful and proved.**

| Attempt | Status |
|---|---|
| \(T_c\le\theta\nu\mathcal D_s\) (K=0) | **Dead.** \(\lvert T_c\rvert/\mathcal D_s\) scales with amplitude. |
| \(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\) | **Dead by algebra** (\(a^3\) vs \(a^4\)). |
| \(T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1} E Y\) | Uniform \(C_0\) **dead** (same as unrestricted ★ / \(B^\star\)). |
| \(\lvert T_c\rvert\le C_* X^{3/2}\Lambda\) | Right degree. **Not a theorem.** Uniform \(C_*\) also fails on \(v_n\). |
| Target \(T_c\le\theta\nu\mathcal D_s+K(t)X\) (or \(K_Y Y\)) | **Open.** Named. Not derived. |

Pairing from the inner product (not isolated as a numbered lemma):
\(\lvert T_c\rvert\le\|A^{1/2}B\|_2\,\sqrt{\mathcal D_s}\). Closing that
by \(\|A^{1/2}B\|_2\le C\sqrt{EY}\) is Target A / CS remainder, which
is the killed shape bound in other units.

Tautology: \(K=(T_c-\theta\nu\mathcal D_s)_+/X\) makes the estimate an
identity. Content collapses to \(\int K<\infty\).

---

## 3. Remaining term / obstruction in that bound

- Cubic stretching vs quadratic spread: remainder must scale like
  amplitude\(^3\). Energy-linear \(K\) fails.
- Splitting \(M\) and \(\Lambda N\) by coarse Sobolev **loses the
  centering.** Work \(T_c-\theta\nu\mathcal D_s\) as one object.
- HH / Bony / paraproduct: HH is the live channel on a high triad;
  random HH fraction is not a bound. No paraproduct estimate of
  \(T_c\). Need★ (signed dual on HH→L after gap-cancel) is **missing**.
  Unsigned CS \(\lvert T_\beta\rvert\le\sqrt{\beta}\,E\sqrt{s\,e_\beta}\)
  hides occupancy \(s\).
- \(K\) from \(\|\nabla u\|_\infty\) or a spectral tail is BKM, not
  an attack. \(K\) from \(\|u\|_{H^1}\) assumes the unknown.
- Extra-factor diagnostic on \(v_n\) only:
  \(\mathcal R_\star\big/\sqrt{X/E}\) looks flat. **Not proved** on
  other fields. Not a remainder theorem.

---

## 4. Was \(K(t)\) shown integrable?

**No.** Never derived for classical unaugmented NS. Pathwise
\(K\in L^1_{\mathrm{loc}}\) is the whole claim. Do not put \(K(t)\)
in the PDE.

---

## 5. Small \(\mathcal D_s\) at high frequency

- Exact one shell: \(\mathcal D_s=T_c=0\). Vacuous. Does not test
  the estimate.
- Almost-single-shell probes: stretching did not stay alive as
  \(\mathcal D_s\to 0^+\). Not a theorem.
- Two-shell: \(\mathcal D_s\sim(\alpha-\beta)^2\). Small gap \(\Rightarrow\)
  small spread; gap-cancel already used; signed \(T_\beta\) still open.
- Growing layer \(v_n\): **not** small \(\mathcal D_s\).
  \(\mathcal D_s(v_n)>0\) (eigenvalues \(n^2,2n^2,5n^2\) at \(j=0\)).
  Aspect exactly 6. \(N=0\), so \(T_c=M=3n^5(3n^2+3n+1)\) on the
  evaluator \(n=1\ldots 8\). High-frequency **concentration**, many
  modes, \(\mathcal R_\star\gtrsim n/165888\to\infty\). This kills
  every uniform remainder of ★ scaling. It does not, by itself, kill
  a pathwise \(K(t)\) allowed to grow with the snapshot.

---

## 6. Thin high-frequency many-mode packets

- \(v_n=D_n(z)\,(U_1(nx,ny),U_2(nx,ny),0)\): \(\Theta(n)\) occupied
  eigenvalues, 18–102 modes for \(n=1\ldots 8\). Strongest negative
  result for a uniform \(T_c\) remainder.
- Natural same-shell / fixed-gap spheres: \(\mathcal D_s\) from the
  **gap**, not the width; mixed closures \(O(m)\); natural ensemble
  did **not** make \(\mathcal R_\star\) blow. Analytic fact. Do not
  re-sweep.
- Exact-shell \(K_{\alpha,\beta}\) / occupancy \(s\): **different
  object** from \(K(t)\). Designed \(\Theta(m^2)\) is excluded
  (\(K\le 16s\)). Claimed \(16/9\) is frozen, not this estimate.

---

## 7. Where the surviving work sits

| What | Path |
|---|---|
| Identity lock | `docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md` |
| Canonical defs / dead uniform box | `docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md` |
| Evaluator (signed triads, two \(\mathcal D_s\) forms) | `scripts/ns_lemma_star_core.py`, `scripts/ns_attacks/stokes_moments.py` |
| Direct-route target + circularity test | `docs/ns-snd-final-status/CENTERED-DRIFT.md` |
| Algebra-only script (PR #104 branch, not this tree) | `origin/cursor/unaug-ns-unified-status-a7a2:scripts/centered_drift.py` |
| \(v_n\) kill of uniform \(C_0\) | `docs/ns-recovery/GROWING-LAYER-SCORE.md`, `scripts/growing_layer_counterexample.py` |
| Replacement job (no theorem) | `docs/ns-recovery/REPLACEMENT-CLOSURE.md` |
| Two-shell gap-cancel; Need★ missing | `origin/cursor/unaug-ns-unified-status-a7a2:docs/NEED-STAR-HH-L-DUAL.md` |
| Bony HH diagnostic | `docs/math/ns_attacks/ATTACK_3_BONY_HH_L.md` |
| K=0 dead (do not rebuild) | `docs/math/ns_attacks/ATTACK_2_TRIAD_K0_CSTAR.md` |
| Stokes identity check | `docs/math/ns_attacks/ATTACK_4_STOKES.md` |
| CS pairing / Target A | `docs/ns-recovery/CS-REMAINDER-VS-DA-REJECT.md` |
| C10 identities, empty first arrow | `docs/ns-snd-final-status/C10-CHAIN.md` |

**Next write (not done):** a non-tautological \(K\) or \(K_Y\) from
cancellation inside \(T_c=M-\Lambda N\), true on \(v_n\) if that
field is in the class, without \(H^1/L^\infty/\)BKM.
