# SND reviewer packet — mathematical corrections

15 September 2026.
**Addendum to the historical August verdict
and to the current Theorem H commentary.
The original extract stays an extract.
It is the object under review.**

Displayed Theorem H is not established
even with \(X\le M\).
The absolute-flux estimate fails on
smooth shear fields with fixed enstrophy
and a fixed spread ratio.
A valid \(M\)-dependent bound for the
nonlinear shell term sits separately.
It does not give dominant-shell
propagation.
SND sitting is not a bound on \(X\).
Ordinary NS is not solved.

Not leftover 1. Not leftover 4. Not \(\star\).
Catalog B open stays 1 (`B_regularity`).
Do not merge PR 48 SND / Q6 / SFE pile.
Do not start H1 from this page.
Do not weld \(\star\).
Do not write “naming fraud.”
The formulas establish an error. They
do not establish intent. Say
definition/claim mismatch.

Implication (what \(\sigma\) controls;
frequency drift; circularity):
[`SND-TO-REGULARITY.md`](SND-TO-REGULARITY.md).
Plain: [`SND-H-PLAIN.md`](SND-H-PLAIN.md).
Living extract (object under review):
[`UNAUGMENTED-R4-VORTICITY-PLAN.md`](UNAUGMENTED-R4-VORTICITY-PLAN.md)
§8.1. Arithmetic lock:
`python3 scripts/snd_h_review.py`.
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).

Underlying GitHub / Zenodo KEEP files
were not re-fetched for this addendum.
The calculations address the formulas
as supplied in the specialist packet.

---

## Replacement wording

> In the supplied extract, Theorem H is
> not established even with \(X\le M\).
> Its proof drops a viscous tail, uses
> invalid Sobolev embeddings and does
> not provide a complete Bony
> decomposition. The displayed
> absolute-flux estimate fails on
> smooth fixed-enstrophy shear fields.
> A valid \(M\)-dependent bound for the
> nonlinear shell term can be proved
> separately, but its usefulness for
> SND propagation remains to be shown.
> Any SND floor asserted from time zero
> must respect the initial spectral
> distribution. Retain the spectral
> toolkit and rebuild the required
> estimate from the exact shell
> evolution.

Use this as the cover-sheet correction.
Preserve the original manuscript extract
as an extract, clearly marked.

---

## Two names for two quantities

The packet under review and the living
dictionary on this branch used the same
letter \(\Pi_j\) for different objects.
Freeze the names.

\[
F_j=\bigl\langle(u\cdot\nabla)u,\Delta_j^2 u\bigr\rangle,\qquad
S_j=\nu\sum_{k>j}2^{2k}\|\Delta_k\nabla u\|_2^2.
\]

For real self-adjoint Fourier multipliers,

\[
F_j=\bigl\langle\Delta_j[(u\cdot\nabla)u],\Delta_j u\bigr\rangle.
\]

**Packet \(\Pi_j\).** \(\Pi_j=F_j-S_j\).

**Living extract \(\Pi_j\).** Plan §8.1 wrote
only the nonlinear pairing
\(\int\Delta_j[(u\cdot\nabla)u]\cdot\Delta_j u\).
That is \(F_j\). It is not \(F_j-S_j\).

The first line of the purported proof
identifies packet \(\Pi_j\) with \(F_j\).
That drops \(S_j\). A Bony split of \(F_j\)
cannot by itself bound \(\lvert F_j-S_j\rvert\).

The sign matters. \(S_j\ge 0\), so an
upper bound on \(F_j\) gives an upper
bound on packet \(\Pi_j\). It does not
give the displayed absolute-value bound.

---

## Displayed estimate fails with \(X\le M\)

Work on \((\mathbb{R}/2\pi\mathbb{Z})^3\) with
normalized volume, so
\(\lvert\sin(ny)\rvert_2^2=1/2\). Smooth
radial cutoffs that isolate frequency
\(2^j\) in block \(j\). Mean-zero fields.

Fix \(q>0\), \(\nu>0\), \(0<\rho_0<1\). Choose
an integer \(N\) large enough that
\(2/(N+2)\le\rho_0\). Set

\[
a=\frac{2q}{N+2},\qquad b=\frac{q}{N+2}.
\]

For an integer \(K>N\), the shear

\[
u_K=\Biggl(
\sqrt{2a}\,\sin y
+\sqrt{2b}\sum_{j=1}^{N-1}2^{-j}\sin(2^j y)
+\sqrt{2b}\,2^{-K}\sin(2^K y),\;
0,\;0
\Biggr)
\]

is smooth, periodic, mean zero and
divergence free. Velocity points in
\(x\) and depends only on \(y\), so
\((u_K\cdot\nabla)u_K=0\). Shells:

\[
X_0=a,\qquad
X_1=\cdots=X_{N-1}=X_K=b,\qquad
X=a+Nb=q,\qquad
J=a,\qquad j_*=0,\qquad
\rho=\frac{2}{N+2}.
\]

Independent of \(K\). Taking
\(\delta_*=M=q\) meets the stated
enstrophy cuts. Write

\[
S_K=\nu b\Bigl(\sum_{j=1}^{N-1}4^j+4^K\Bigr).
\]

Then \(\mathcal D=\nu a+S_K\) and
packet \(\Pi_{j_*}(u_K)=-S_K\). The
displayed estimate would need a finite
\(C_*(\nu,\delta_*,M,\rho_0,C_S)\) with

\[
S_K\le C_*\bigl(\nu a+\sqrt{q(\nu a+S_K)}\bigr).
\]

The ratio tends to infinity:

\[
\frac{S_K}{\nu a+\sqrt{q(\nu a+S_K)}}
\sim\sqrt{\frac{\nu b}{q}}\,2^K
\longrightarrow\infty.
\]

Every allowed argument of \(C_*\) is
fixed. No such finite constant exists
for the displayed estimate on these
standard blocks. Overlapping dyadic
partitions do not stop the
quadratic-versus-linear frequency
growth.

Packet table, \(\nu=q=M=\delta_*=1\),
\(N=20\), \(\rho_0=0.1\), so \(J=\rho=1/11\):

| \(K\) | \(\lvert\Pi_{j_*}\rvert/(\nu 4^{j_*}J+\sqrt{X\mathcal D})\) |
|---:|---:|
| 24 | \(3.57924234\times 10^6\) |
| 28 | \(5.72307770\times 10^7\) |
| 32 | \(9.15690113\times 10^8\) |

Locked by `scripts/snd_h_review.py`.
The asymptotic proves unboundedness.
The table checks the arithmetic.

These are also initial states of
explicit global unforced NS solutions:
multiply each sine coefficient by
\(e^{-\nu 4^j t}\). The example is not
excluded by asking for genuine NS
states. For small positive times the
failure persists whenever the initial
ratio sits beyond a proposed bound.

“Proved under X<=M” must be replaced. These are defects **before**
the proposed removal of \(M\).

---

## Valid conditional bound for \(F_j\) only

Let \(u\) be mean-zero, divergence-free
and smooth on a fixed torus. Real
self-adjoint dyadic multipliers with
uniformly bounded symbols.
\(X=\lvert\nabla u\rvert_2^2\).

Hölder with exponents \(6,2,3\):

\[
\lvert F_j\rvert
\le\lvert u\rvert_6\,\lvert\nabla u\rvert_2\,\lvert\Delta_j^2 u\rvert_3
\le C X^{3/2}.
\]

Mean-zero Sobolev / Poincaré and the
uniform \(H^1\) multiplier bound. The
constant is independent of \(j\).
\(H^1\) controls \(L^6\), not \(L^\infty\).

Let \(\lambda_1>0\) be the first nonzero
eigenvalue of \(-\Delta\). For \(u\in H^2\),

\[
\mathcal D=\nu\lvert\Delta u\rvert_2^2\ge\nu\lambda_1 X.
\]

If \(X\le M\),

\[
\lvert F_j\rvert
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{1/2}\mathcal D^{1/2}.
\]

Needs neither spread nor a dominant
shell. Extends to the Sobolev class by
approximation. Legitimate consequences:

\[
\Pi_j^{\mathrm{packet}}\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,X^{1/2}\mathcal D^{1/2},
\]

\[
\bigl\lvert\Pi_j^{\mathrm{packet}}\bigr\rvert
\le
S_j
+
C\sqrt{\frac{M}{\nu\lambda_1}}\,X^{1/2}\mathcal D^{1/2}.
\]

These are different estimates from
Theorem H. They do not supply a new
propagation theorem. Usefulness for
SND still requires the actual
evolution inequality in Theorem G.

---

## Invalid embeddings in the supplied proof

The supplied proof asserts

\[
\lvert u\rvert_\infty\lesssim M^{1/2},\qquad
\lvert\nabla u\rvert_\infty\lesssim\lvert\Delta u\rvert_2.
\]

Neither is a general three-dimensional
Sobolev inequality. Mean-zero \(H^1\)
controls \(L^6\), not \(L^\infty\). \(H^2\)
does not control \(\nabla u\) in \(L^\infty\).
The peak-fraction condition supplies
no demonstrated replacement. Without
mean-zero, a constant velocity already
disproves the first assertion while
leaving \(X\) and \(\rho\) unchanged.

A legitimate mean-zero interpolation is

\[
\lvert u\rvert_\infty
\le C\lvert\nabla u\rvert_2^{1/2}\lvert\Delta u\rvert_2^{1/2}
=C\nu^{-1/4}X^{1/4}\mathcal D^{1/4}.
\]

Using it changes subsequent powers.
It does not repair the missing viscous
tail.

---

## Removing \(M\) fails an amplitude check

Even after replacing packet \(\Pi_j\) by
\(F_j\), the proposed right-hand side is
quadratic in amplitude while \(F_j\) is
cubic. For \(u=Aw\), \(A>0\):

\[
X(Aw)=A^2 X(w),\quad
\mathcal D(Aw)=A^2\mathcal D(w),\quad
\rho(Aw)=\rho(w),\quad
F_j(Aw)=A^3 F_j(w).
\]

For any admissible spread field with
\(F_{j_*}(w)\ne 0\), an
amplitude-independent quadratic bound
fails as \(A\to\infty\). A lower
enstrophy threshold does not stop the
rescaling.

Explicit spread fields exist. Embed
the 2-D stream function
\(\psi=\alpha\cos x+\beta\cos(2y)+\gamma\cos(x+2y)\)
as \(w=(\partial_y\psi,-\partial_x\psi,0)\).
The low block of frequency \((1,0,0)\)
has \(F_0=\alpha\beta\gamma/2\). Choose
\(\alpha=2\) and \(\beta=\gamma\) small.
Add modes \(c_m\sin(2^m y)\,e_1\),
\(m\ge 3\), one unit of enstrophy per
block. The original low block stays
dominant while its fraction becomes
arbitrarily small. The added modes do
not change \(F_0\).

So “remove \(M\) from this same estimate
for every spread field” is not an
appropriate open target. A revised
estimate needs compatible amplitude
powers, another justified restriction,
or a dynamical / time-integrated
formulation.

---

## No universal SND floor from \(t=0\)

For any fixed \(q>0\) and integer \(L\ge 1\),

\[
v_L(y)=\sqrt{\frac{2q}{L}}
\sum_{j=0}^{L-1}2^{-j}\sin(2^j y)\,e_1
\]

has \(X(0)=q\), \(X_j(0)=q/L\),
\(\rho(0)=1/L\). Smooth shear data.
Exact unforced NS evolutions are
global and satisfy \(X(t)\le q\). The
initial peak fraction can be
arbitrarily small while \(\nu\),
\(M=q\), a lower enstrophy threshold
and the dyadic convention stay fixed.

No common positive bound
\(c_*(\nu,\delta_*,M,C_S)\) can hold from
\(t=0\) for every such datum. The same
obstruction applies if the infimum
excludes \(0\) but includes arbitrarily
small positive times, by continuity.

This rules out a uniform conclusion
with those quantifiers. It does not
rule out a positive lower bound that
depends on the particular initial
spectrum. Solution-by-solution SND
is not a uniform theorem across all
data.

Making a field arbitrarily small in
amplitude leaves \(\rho\) unchanged.
Small-data existence cannot supply a
universal initial spectral fraction.

An argument showing \(\dot\rho>0\) below
a threshold produces a barrier
involving \(\min\{\rho(0),\text{threshold}\}\).
It cannot force an initially smaller
ratio above that threshold at time
zero.

---

## Additional corrections before circulation

| Packet location | Correction |
|---|---|
| August verdict \(X\ge c_* J\) | \(J/X\ge c_*\) means \(J\ge c_* X\), equivalently \(X\le J/c_*\). Printed \(X\ge c_* J\) is not equivalent. For \(0<c_*\le 1\) it already follows from \(J\le X\). If the August text is preserved, attach an erratum. |
| “\(H^1\) is supercritical” / “a derivative short” | Under \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2 t)\), \(\lvert u_\lambda\rvert_{\dot H^s}=\lambda^{s-1/2}\lvert u\rvert_{\dot H^s}\) in 3-D. Velocity \(\dot H^{1/2}\) is critical. \(H^1\) is **subcritical**. The available energy control is supercritical. |
| “Energy class” | Leray–Hopf is \(L^\infty_t L^2_x\cap L^2_t H^1_x\). It is not a uniform-in-time \(H^1\) ceiling. |
| Exact LP equalities | Usually \(\sum_j 2^{2j}\lvert\Delta_j u\rvert_2^2\asymp\lvert\nabla u\rvert_2^2\), not equality. Freeze the partition and use equivalence constants, or define exact Fourier-weighted shells. |
| Theorem H for every \(H^1\) field | \(\mathcal D\) need not be finite. Prove any finite estimate for smooth or \(H^2\) fields first, then state the limit. |
| Displayed Bony split | \(j'\) unquantified; neighboring output blocks not fully specified; supposed high–low term uses the whole \(u\). High–high-to-low must be assigned. Not a complete indexed decomposition. |
| Ring Lemma labeled KEEP | A KEEP label is not verification. Ring is **REPAIR** on this desk. An elementary band-limited bound on \(E_c^\infty=\{\lvert\omega\rvert\ge c\lvert\omega\rvert_\infty\}\) gives \(\lvert\nabla\xi\rvert_{L^\infty(E_c^\infty)}\le C\lambda/c\). That changes the threshold and must not silently replace the manuscript set. |
| Requested \(M=M(\lvert u_0\rvert_{H^1})\) | Include viscosity and fixed-domain dependence. A bound finite on each finite interval, allowed to depend on its endpoint \(T\), can suffice for continuation; an all-time constant is stronger. |
| Official Statement (B) | Fefferman: smooth periodic divergence-free initial data. An \(H^1\) theory may be a route. It is not the literal official initial-data assumption. |
| “Naming fraud” | Replace with definition/claim mismatch or mislabeling. |

---

## First equation to write

For smooth unforced NS, fixed \(j\), and
\(X_j=2^{2j}\lvert\Delta_j u\rvert_2^2\),

\[
\frac12\dot X_j
+\nu\,2^{2j}\lvert\nabla\Delta_j u\rvert_2^2
=-2^{2j}F_j.
\]

Apply \(\Delta_j\), test against
\(\Delta_j u\), multiply by \(2^{2j}\).
Incompressibility removes pressure.
This specifies the nonlinear quantity,
the sign, the derivative weight and
the viscous term **before** any
estimate.

Derive the desired \(J/X\) evolution
from this equation. Handle switches of
the maximizing shell by comparison.
Only then select the estimate the
propagation proof actually needs.
Test it against:

1. the high-tail shear family above;
2. amplitude rescaling;
3. many equal-enstrophy shells.

Retain the spectral toolkit. Replace
the failed statement.

---

## Public-status (packet §9)

OpenAI’s 8 September announcement is
Fefferman (C)/(D) if it holds: a forced
finite-time singularity. It is not
unforced Statement (B). Record:
[`OPENAI-NS-CLAIM.md`](OPENAI-NS-CLAIM.md).
Clay’s 11 September note describes an
evaluation process. It is not an award
notice. This addendum does not examine
the announced proof or a Lean
formalization. Track B stays unforced.

---

## What this does not do

It does not close leftover 1.
It does not restore unrestricted \(\star\).
It does not make Ring a theorem.
It does not give a bound on \(X\).
Closing a correct \(F_j\) estimate
still would not close ordinary NS:
[`SND-H-PLAIN.md`](SND-H-PLAIN.md).

NS not solved.

---

## Lock

Displayed Theorem H is not established
even with X<=M. Packet Pi_j drops S_j.
Shear family: (u_K·∇)u_K=0 and the
ratio grows like 2^K. Valid
M-dependent bound for F_j only.
H^1 controls L^6, not L^infty.
H^1 is subcritical. Velocity
Ḣ^{1/2} is critical. Printed
X>= c_* J is not equivalent.
Remove M from this same estimate
is not the open target. No universal
SND floor from t=0. First equation:
(1/2)Ẋ_j + ν 2^{2j}|∇Δ_j u|_2^2
= -2^{2j} F_j.
definition/claim mismatch.
NS not solved.
