# B★ — identity, symmetrization, stall

16 September 2026.
**The pairing identity sits.
The uniform \(C\) does not.
Not a close. ★ stays killed.**

Living verdict: [`BSTAR.md`](BSTAR.md).
Triangle reconstruction:
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).
Pairing CS doors (tight is
★; LE dead; LX not seated):
[`L-DOOR.md`](L-DOOR.md).
Instantaneous \(MN\):
[`MN-CANCEL.md`](MN-CANCEL.md).
Machine: `python3 scripts/bstar_symmetrize.py`.
Do not overwrite `stokes_moments.py`.
Do not start leftover 1.
Do not weld \(\star\).

---

## Exact pairing (one object)

On mean-zero divergence-free
fields, \(\omega=\nabla\times u\),
\(Au=\nabla\times\omega\), and

\[
\mathcal D_s=\|(A-\Lambda)\omega\|_2^2.
\]

The centered transfer is one
pairing, not \(M\) and \(\Lambda N\)
split:

\[
T_c
=
\bigl\langle
(\omega\cdot\nabla)u-(u\cdot\nabla)\omega,\;
(A-\Lambda)\omega
\bigr\rangle.
\]

Locked on a resonant triad and
on a power-law field against
`probe().Tc`. Sign flip
\(u\mapsto -u\) is odd in \(T_c\).

Cauchy–Schwarz on that pairing:

\[
\lvert T_c\rvert
\le
\|L\|_2\,\mathcal D_s^{1/2},
\qquad
L=(\omega\cdot\nabla)u-(u\cdot\nabla)\omega.
\]

Hence
\(R_B\le R_L\) with
\(R_L=\|L\|_2/\sqrt{XY}\).
B★ would follow from a uniform
bound on \(R_L\). That bound is
the wrong door.

---

## Why CS-through-\(L\) cannot prove B★

Hölder \(3,6\) and Sobolev
\(H^1(\mathbb{T}^3)\subset L^6\),
\(H^{1/2}\subset L^3\):

\[
\|(\omega\cdot\nabla)u\|_2
\le
C\,\|\omega\|_3\|\nabla u\|_6
\le
C\,\Lambda^{1/4}\sqrt{XY}.
\]

So \(R_L\lesssim \Lambda^{1/4}\) is
the crude ceiling, not \(O(1)\).
Kato–Ponce on \(\|A^{1/2}B\|_2\)
wants \(\|\nabla u\|_\infty\) and
does not close in \(H^2(\mathbb{T}^3)\).

On the imag \(|k|^{-2}\) cutoff
family the live FFT records
\(R_L/\Lambda^{1/4}\) climbing
through \(0.30\to 0.35\) as
\(K=3\to 16\). The stall is
saturated, not an artifact of
Bernstein.

The same family has
\(R_B/\Lambda^{1/4}\) saturating
near \(0.056\). The pairing with
\((A-\Lambda)\omega\) removes a
constant, not the
\(\Lambda^{1/4}\). Helical
polarization of the *same*
spectrum makes \(T_c\approx 0\).
Imag does not. Incompressibility
and centering are used. They do
not produce a uniform \(C\).

---

## What was tried and kept

Full triad sum for \(T_c\) is
already exact in
[`LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md):

\[
T_c=\sum_{p+q=k}\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Symmetrizing the three vertices
uses energy conservation on each
triad, \(t_p+t_q+t_k=0\), and
rewrites the multiplier as a
difference of \((\lambda-\Lambda)\).
That identity is the pairing
above. Estimating the two legs
of \(L\) separately is how the
\(\Lambda^{1/4}\) re-enters.
Do not split \(M\) and \(\Lambda N\).
The split is not needed: the
combined pairing still tracks
\(\Lambda^{1/4}\) on imag
power-law.

Widely separated triads shrink
\(R_B\). Amplitude matches cubic.
\(v_n\) kills ★, not this box.
Many-mode random stays small.
Ascent on four modes reached
\(R_B\approx 0.45\), a local
finite max, not the cutoff
family.

---

## What this is not

Not a closed-form \(T_c(K)\)
for the cutoff family. Specialist
may ask for that page. The live
evaluator through \(K=16\) is
the record.

Not a useful Route B \(K\).
AM-GM of a false B★ is void.
Even the formal remainder was
\(Y/\nu\).

Not a restoration of ★.
\(v_n\) still kills
\(\sup\mathcal R_\star<\infty\).

Catalog B open stays 1.
NS not solved.
