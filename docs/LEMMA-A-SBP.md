# Lemma A — SBP capacity comparison

24 September 2026.
**Lemma A PROVED. Low tail
absorbed. Sharp L3. Lemma B
OPEN. Not a close.
NS not solved.**

SBP:
[`CORE-TAIL-SBP.md`](CORE-TAIL-SBP.md).
Ratio page (now updated):
[`LOW-TAIL-CAPACITY.md`](LOW-TAIL-CAPACITY.md).
Packet:
[`packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md`](../packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md).

Center:

\[
\mathfrak T_c
=
\Bigl(\frac{d}{dt}\Bigr)_{\mathrm{NL}}\Phi_e
+2\kappa_e^3 Q_a
-(\Lambda-\lambda_e)N.
\]

Three bills: low tail, charge,
epoch motion. Homochiral loops
stay on their own desk.

---

## Lemma A — PROVED

On \(\mathbb T^3\), nonzero
modes have \(m=\lvert k\rvert\ge 1\).
Need \(\kappa\ge 1\) only for
the narrative high-center
regime; the comparison holds
for every \(\kappa>0\).

After cancelling
\((m-\kappa)^2\) (\(m\neq\kappa\)):

\[
\boxed{
m^2+2\kappa m+2\kappa^2
\le
2m^2(m+\kappa)^2.
}
\tag{A}
\]

The ratio
\((x^2+2x+2)/(x^2(x+1)^2)\)
decreases on \((0,\infty)\).
So for \(m\ge 1\),

\[
C_\kappa
=
\sup_{m\ge 1}
\frac{\phi_\kappa(m)}{d_\kappa(m)}
=
\frac{2\kappa^2+2\kappa+1}{2(\kappa+1)^2}.
\]

\[
1-C_\kappa
=
\frac{\kappa+\tfrac12}{(\kappa+1)^2}>0,
\qquad
\lim_{\kappa\to\infty}C_\kappa=1.
\]

\[
\boxed{C_\kappa\le 1.}
\]

Equality is not attained at
finite \(\kappa\). The closest
approach is the fundamental
mode \(m=1\) as
\(\kappa\to\infty\).
At the shell,
\(5/(8\kappa^2)\). At
infinity, \(0\).

Therefore, globally
(core + low + high),

\[
\boxed{\Phi_e\le D_e^{\mathrm{frozen}}.}
\tag{L1}
\]

The torus gap \(m\ge 1\)
stops the \(1/m^2\) blow-up.
The independent low-tail
occupancy bill is
**absorbed**. No occupancy
theorem.

---

## Frozen vs live \(D_s\) — sharper than Young

\[
\lambda-\lambda_e
=(\lambda-\Lambda)+(\Lambda-\lambda_e).
\]

Young gives (L2) for any
\(\eta>0\). It is true and
**strictly weaker**.

The cross term is
\(2(\Lambda-\lambda_e)\sum\lambda(\lambda-\Lambda)\lvert a\rvert^2\).
The sum is \(Y-\Lambda X=0\).
So

\[
\boxed{
D_e^{\mathrm{frozen}}
=
D_s+X(\Lambda-\lambda_e)^2
=W_{\lambda_e}.
}
\]

With (L1),

\[
\boxed{
\Phi_e
\le
D_s+X(\Lambda-\lambda_e)^2.
}
\tag{L3 sharp}
\]

The pair \((1+\eta,1+\eta^{-1})\)
is not needed.

---

## Center displacement — scalar chart

\[
\frac{X(\Lambda-\lambda_e)^2}{Y}
=
\frac{(\Lambda-\lambda_e)^2}{\Lambda}
=\zeta_e^2,
\qquad
\zeta_e
=
\frac{\Lambda-\lambda_e}{\sqrt\Lambda}.
\]

\[
\boxed{
\frac{\Phi_e}{Y}
\le
\frac{D_s}{Y}+\zeta_e^2.
}
\tag{L4 sharp}
\]

Reset when

\[
\boxed{\lvert\Lambda-\lambda_e\rvert=c\sqrt\Lambda.}
\tag{RESET}
\]

Then \(\zeta_e^2=c^2\),
scale-covariant. This is the
natural dimensionless chart
scale. It does **not** prove
summability of resets.

---

## Charge — still a different bill

\[
\tfrac12 H_a'+\nu D_a=Q_a,
\qquad
2\kappa_e^3 Q_a
=\kappa_e^3 H_a'+2\nu\kappa_e^3 D_a.
\]

Near the shell
\(D_a\sim\kappa X\), while
\(D_s\) can be tiny. \(D_s\)
does not pay \(D_a\). The
old failure was positive
variation / reset, not
instantaneous size.
Charge and epoch must be
budgeted together.

\[
\boxed{
\text{Lemma B — charge/epoch joint budget: OPEN.}
}
\]

Need
\(\sum_e\bigl([\Delta\mathcal C_e]_+
+\int_{I_e}\text{charge remainder}\bigr)
<\infty\)
cutoff-uniform. Hard.
Do not write it as
\(\int D_s/Y\) or
\(\sup\Lambda\).

---

## Board after A

\[
\boxed{\mathrm{CORE}+\mathrm{TAILS}\to D_s+\zeta_e^2}
\]

\[
\boxed{\textbf{CHARGE}+\textbf{EPOCH MOTION}\to\textbf{OPEN}}
\]

Last mile is no longer three
independent bills. Radial /
tail apparatus sits inside
live variance plus center
displacement.

Do not mix scalene
homochiral loops into this
heterochiral charge ledger.
Solver: still measure
\(\Phi_e/Y\) to test the
identity and to split
\(\zeta_e^2\) vs charge on
dangerous time. No 64/96
data here.

---

## Lock

(A) PROVED. \(C_\kappa\le 1\)
PROVED. (L1) PROVED.
\(D_e^{\mathrm{frozen}}=W_{\lambda_e}\)
EXACT. (L3), (L4) sharp.
RESET scale-covariant,
summability OPEN.
Low-tail occupancy bill
**absorbed**.
Lemma B OPEN.
This page is frozen. Do not
alter it. Sign realizability
is a different gate:
[`STATIC-SIGN-REALIZABILITY.md`](STATIC-SIGN-REALIZABILITY.md).
Not DA-NS-2. NS not solved.
