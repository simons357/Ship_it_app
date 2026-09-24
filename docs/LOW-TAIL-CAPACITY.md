# Low-tail capacity

24 September 2026.
**Compare \(\phi_\kappa\) to frozen
variance before reading 64/96.
The enemy is the low-frequency
tail, not tails generically.
Not a close. NS not solved.**

SBP parent:
[`CORE-TAIL-SBP.md`](CORE-TAIL-SBP.md).
Packet:
[`packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md`](../packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md).
Residual:
[`NARROW-HET-RESIDUAL.md`](NARROW-HET-RESIDUAL.md).

Sympy checks:
`scripts/ns_attacks/core_tail_sbp.py`.
Frozen epoch only.

Do not interpret Taylor–Green
until this comparison is seated.
No \(N=64/96\) data is in this
checkout.

---

## Exact ratio

\(m=\lvert k\rvert\),
\(\kappa=\kappa_e\),
\(\lambda_e=\kappa^2\).

\[
\phi_\kappa(m)
=\tfrac12(m-\kappa)^2
(m^2+2\kappa m+2\kappa^2)
\]

\[
d_\kappa(m)
=m^2(m^2-\kappa^2)^2
=m^2(m-\kappa)^2(m+\kappa)^2
\]

For \(m\neq\kappa\),

\[
\boxed{
\frac{\phi_\kappa(m)}{d_\kappa(m)}
=
\frac{m^2+2\kappa m+2\kappa^2}
{2m^2(m+\kappa)^2}.
}
\tag{A}
\]

\(x=m/\kappa\):

\[
\boxed{
\frac{\phi_\kappa}{d_\kappa}
=
\frac1{2\kappa^2}
\frac{x^2+2x+2}{x^2(x+1)^2}.
}
\tag{B}
\]

Shell limit \(x\to 1\):

\[
\boxed{\frac{5}{8\kappa^2}.}
\]

The scaled factor
\((x^2+2x+2)/(x^2(x+1)^2)\)
is decreasing on \((0,\infty)\)
(numerator of the derivative
\(-2(x^3+3x^2+5x+2)<0\)).
On any annulus
\(a\kappa\le m\le b\kappa\),
\(a>0\),

\[
\boxed{
\Phi_e^{\mathrm{core}}
\le
\frac{C(a,b)}{\kappa_e^2}
D_e^{\mathrm{frozen,core}},
}
\tag{C}
\]

\[
C(a,b)
=\frac{a^2+2a+2}{2a^2(a+1)^2}.
\]

Both weights vanish
quadratically at the shell.
(C) is a uniform comparison,
not just that shared zero.

---

## Asymmetry

As \(m/\kappa\to\infty\),

\[
\frac{\phi_\kappa}{d_\kappa}\sim\frac1{2m^2}.
\]

High tail is **favorable**
against frozen variance.

As \(m/\kappa\to 0\),

\[
\frac{\phi_\kappa}{d_\kappa}\sim\frac1{m^2}.
\]

That blows up.
\(\phi_e(0)=\kappa_e^4\) is
exactly this.

\[
\boxed{\textbf{LOW-FREQUENCY TAIL}}
\]

is the enemy. Not tails
generically.

---

## What the solver must return

Not merely \(\Phi^{\mathrm{low}}\),
\(\Phi^{\mathrm{high}}\).
On dangerous epochs:

\[
\boxed{
L_e
=
\frac{\kappa_e^4 E_{\mathrm{low}}}{Y}
}
\]

or the exact low-tail piece
of \(\phi_e\). If the route
fails numerically, this is
where it should fail.

A two-mode sample
(core at \(\kappa=20\),
\(E_{\mathrm{low}}/E\approx 0.02\))
puts **all** of \(\Phi_e\) in
the low tail, with
\(L_e\approx 0.02\) and
\(Y\) still core-dominated.
That is the old
high-frequency core + small
low-frequency population,
now with a reason.

---

## Energy does not pay it

For \(m\le a\kappa\), \(a<1\),
nonzero torus modes have
\(m\ge 1\), so
\(E_{\mathrm{low}}\le Y_{\mathrm{low}}\).
Then
\(\kappa^4 E_{\mathrm{low}}\le\kappa^4 Y_{\mathrm{low}}\)
is useless at high \(\kappa\).
Global energy
\(E_{\mathrm{low}}\le E_0\)
makes
\(\kappa^4 E_0/Y\)
uncontrolled.
Ordinary energy is not the
low-tail estimate.

---

## Sharpened last mile

\[
\boxed{\mathrm{CORE}\to\text{controlled by frozen variance}}
\]

\[
\boxed{\mathrm{HIGH\ TAIL}\to\text{even stronger variance weight}}
\]

\[
\boxed{\textbf{LOW TAIL}\to\textbf{OPEN}}
\]

plus charge and epoch motion.

\[
\boxed{
\textbf{NARROW HETEROCHIRAL LAST MILE}
=
\textbf{LOW-TAIL CAPACITY}
+
\textbf{CHARGE}
+
\textbf{EPOCH MOTION}.
}
\]

The 64/96 question is no
longer generic LH bounds.
It is:

\[
\boxed{
\text{can an NSE trajectory keep enough low-mode mass
under a high }\kappa_e
\text{ that }
\kappa_e^4 E_{\mathrm{low}}/Y
\text{ is large on dangerous time?}
}
\]

If \(\Phi/Y\) spikes, say
whether the spike is
low-tail dominated. If not,
this diagnosis is wrong.

---

## Lock

(A), (B), shell \(5/(8\kappa^2)\)
EXACT. (C) EXACT on a
comparable annulus.
High tail favorable.
Low tail OPEN.
\(L_e=\kappa_e^4 E_{\mathrm{low}}/Y\)
is the diagnostic.
Energy does not pay it.
Last mile = low tail +
charge + epoch motion.
Not DA-NS-2. NS not solved.
