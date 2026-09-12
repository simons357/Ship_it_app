# Need★ — signed dual on HH→L after gap-cancel

12 September 2026.
Unaugmented Navier–Stokes on \(\mathbb{T}^3\),
two-shell / HH→L supported;
quantity is the signed dual
\(\mathcal S_\star=T_\beta^{\mathrm{HH}\to\mathrm{L}}\)
after the gap-cancel reduction;
remainder is unsigned CS / occupancy \(s\);
no extra field; the signed bound is
**MISSING.** Leftover 4 stays **OPEN.**

**This is the primary math target.
It is a write of the missing estimate.
It is not a theorem. NS is not solved.**

9D / grow \(s\) is secondary kill-lane
pressure on the same leftover.
Soft X silent. Cosmo five fingers,
Q-stack, SND, Theorem H, augmented
NSE: out of this book. The B-hand
map ([`DA-NS-FIVE-FINGER.md`](DA-NS-FIVE-FINGER.md))
is a different object. MAP, not a close.

Identities: [`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Map: [`LEMMA-STAR-REASON.md`](LEMMA-STAR-REASON.md).
HH→L fan (scored, not a kill):
[`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).
Machine: `scripts/need_star_hh_l_dual.py`.

---

## Gap-cancel (identity; sits)

On exactly two eigenvalue shells
\(\alpha>\beta>0\), with shell energies
\(e_\alpha,e_\beta\), \(E=e_\alpha+e_\beta\),
\(X=\alpha e_\alpha+\beta e_\beta\),
\(Y=\alpha^2 e_\alpha+\beta^2 e_\beta\):

\[
\mathcal D_s
=
\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{X}.
\]

Energy: \(T_\alpha+T_\beta=0\). Centered
drift:

\[
T_c
=
(\alpha-\beta)\frac{\alpha\beta E}{X}\,T_\alpha
=
-(\alpha-\beta)\frac{\alpha\beta E}{X}\,T_\beta.
\]

The gap \((\alpha-\beta)\) cancels in
\(\mathcal R_\star\). When \(T_c>0\):

\[
\mathcal R_\star
=
\frac{\alpha\beta E\,T_\beta^2}{X\,e_\alpha e_\beta Y}.
\]

Near-shell \(e_\beta\to 0\) recovers the
aligned 9B limit
\(K=\beta\|\Pi_\beta B\|_2^2/(\alpha^2\|w\|_2^4)\).
That reduction sits. It is not Need★.

---

## What is still MISSING

HH→L: two high inputs on \(\alpha\),
output on the lower shell \(\beta\).
The signed dual is the complete Im-sum
on that output:

\[
\mathcal S_\star
=
T_\beta^{\mathrm{HH}\to\mathrm{L}}
=
\sum_{\substack{p+q=k\\|p|^2=|q|^2=\alpha\\|k|^2=\beta}}
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Keep \(\mathrm{Im}\). Do not replace it
by an absolute value. Only this signed
sum enters \(\mathcal R_\star\) after
gap-cancel.

Unsigned CS already sits:

\[
\lvert T_\beta\rvert
\le
\sqrt{\beta}\,E\sqrt{s\,e_\beta}.
\]

That hides occupancy \(s\). Same hole
as \(K\le 16s\). Cheap CS is not Need★.

Need★ is a geometry-only bound that
kills \(s\) or proves it bounded:

\[
\lvert\mathcal S_\star\rvert
\le
C\frac{\alpha}{\sqrt{\beta}}\,e_\alpha\sqrt{e_\beta},
\]

or the equivalent two-shell form
\(\lvert T_\beta\rvert\le C\sqrt{X e_\alpha e_\beta Y/(\alpha\beta E)}\).
Either one is \(\sup\mathcal R_\star<\infty\)
on this channel. Neither is written.

The vertex in Attack 12 carries
\(\sqrt{\beta}\), not \(\sqrt{\alpha}\).
That is why HH→L looks able to stretch.
It is why the signed dual, not the
unsigned size, is the leftover.

---

## What this write is not

- A theorem. The reason map named the
  hole. This page names the estimate.
  The estimate is still MISSING.
- Attack 12’s table. Finite
  \(\mathcal R_\star\sim\beta/\alpha\)
  (largest \(\approx 0.71\)) is a sample.
  Do not turn it into Need★.
- Designed \(\Theta(m^2)\) 9D. Dead.
- Grow \(s\) as a close. Secondary
  pressure. Finite \(K\approx 0.456\)
  is not \(C_0\).
- H1. Soft X. Cosmo five fingers.
  The B-hand map is not this estimate.

---

## Locked ratio (not a bound)

\[
\mathcal N_\star
=
\frac{\lvert\mathcal S_\star\rvert}{(\alpha/\sqrt{\beta})\,e_\alpha\sqrt{e_\beta}}.
\]

A uniform \(\sup\mathcal N_\star<\infty\)
is Need★. A finite sample is not.
\(\mathcal N_\star\to\infty\) on a family
kills ★ on this channel. The machine
refuses a fake close.

On aligned HH→L closers (seed 1390,
\((\alpha,\beta)=(5,4)\) and \((9,4)\))
gap-cancel residual is \(10^{-16}\).
Printed \(\mathcal N_\star\approx 0.099\)
is a sample. It is not Need★.

---

## Status

| Item | Verdict |
|---|---|
| Two-shell gap-cancel | **YES** as an identity |
| Unsigned CS / \(K\le 16s\) | **YES** as a bound. Hides \(s\). |
| Signed dual Need★ | **MISSING.** **OPEN.** |
| Attack 12 table as Need★ | **NO.** Sample. |
| Lemma★ | **OPEN** |

Kill lane LIVE. Bounded samples are
not a proof. NS not solved.
