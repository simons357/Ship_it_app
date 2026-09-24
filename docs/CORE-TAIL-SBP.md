# Core / tail SBP

24 September 2026.
**The summation-by-parts identity
exists and is elementary.
It moves the tail. It does not
remove it. Not a close.
NS not solved.**

Filed gate:
[`packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md`](../packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md).
Residual:
[`NARROW-HET-RESIDUAL.md`](NARROW-HET-RESIDUAL.md).
Ledger:
[`CENTERED-MASTER-LEDGER.md`](CENTERED-MASTER-LEDGER.md).

Sympy checks:
`scripts/ns_attacks/core_tail_sbp.py`.

Frozen epoch only:
\(\lambda_e=\kappa_e^2\).
Live \(\kappa(t)=\sqrt\Lambda\)
is a different convention.
Do not mix them.

---

## What (1)–(4) became

Chebyshev tail and core-radius
(2): **PROVED**. Factor of two
exact at the shell,
\(\mathrm d(m^2)/\mathrm dm=2\kappa\).

(3) at the core:

\[
\boxed{
\nabla_{(i,j,o)}R=(5\kappa^2,5\kappa^2,0),
\quad
\partial_\Lambda R=-2\kappa.
}
\]

\[
\lvert R-2\kappa^3\rvert
\le 5\kappa^3 Lr+O((Lr)^2)
\]

when the core is the **same**
\(\kappa\) used in \(2\kappa^3\).
If the core is frozen at
\(\kappa_e\) and \(\Lambda\neq\lambda_e\),
add

\[
\boxed{
R(\kappa_e,\kappa_e,\kappa_e;\Lambda)-2\kappa_e^3
=-2\kappa_e(\Lambda-\lambda_e).
}
\]

Live \(\Lambda\): no moving term,
but \(2\kappa(t)^3 Q_a\) does not
telescope. Frozen: telescopes,
and the extra \(2\kappa_e\lvert\Lambda-\lambda_e\rvert\)
is mandatory.

(4) is the forbidden
\(\lvert\sum\rvert\to\sum\lvert\,\rvert\).
Stays dead.

Tail fact: small \(X\)-mass and
small \(Y\)-mass can carry
essentially all of
\(\mathcal D_s\). Leakage
competes with \(\nu\mathcal D_s\)
on the tail. BROAD again.

---

## Charge as \(\dot H^{1/2}\) flux — PROVED

Weight \(\lvert m\rvert\): flux
\(2o(i-j)\) on het, \(0\) on homo
(Heavy). Then

\[
\boxed{
Q_{a,\Gamma}
=\tfrac12\Bigl(\frac{d}{dt}\Bigr)_{\mathrm{NL}}
\lVert u\rVert_{\dot H^{1/2}}^2.
}
\]

\[
M^{\mathrm{het}}=\sum AHQ,
\qquad
N^{\mathrm{het}}=\sum AQ.
\]

---

## The identity — EXACT

\[
\boxed{
\phi_e(m)
=\tfrac12(m-\kappa_e)^2
(m^2+2\kappa_e m+2\kappa_e^2)\ge 0
}
\]

\[
\Phi_e=\sum_k\phi_e(\lvert k\rvert)\lvert a_k\rvert^2
\]

\[
\boxed{
\mathfrak T_c
=
\Bigl(\frac{d}{dt}\Bigr)_{\mathrm{NL}}\Phi_e
+2\kappa_e^3 Q_a
-(\Lambda-\lambda_e)N.
}
\]

All triads. Only
\(\sum\dot I=0\). Modal remainder
\(-\kappa_e^4\).

Narrow homo and het-radial
land on \(\Phi_e'\), not on
\(\sum\lvert Q\rvert\). Identity
only. Not
\(\mathsf B^{\mathrm{prim}}w=A\).
That primitive stays **NO**
on lattice loops.

---

## Cost — OPEN

\(\phi_e(0)=\kappa_e^4\),
\(\phi_e\sim m^4/2\).
\(\Phi_e/Y\) is not \(O(r^2)\).
\(\int\Phi_e'/Y\) returns
\(\Phi_e Y'/Y^2\), which needs
\(\Phi_e/Y\) small. Tail
leakage is exactly the mass
of \(\phi_e\) off the shell.

Viscous sign is good. Resets
need a jump ledger.

Residual still

\[
\boxed{
2\kappa_e^3 Q_a
-(\Lambda-\lambda_e)N.
}
\]

Charge is the
\(\dot H^{1/2}\) flux. \(N\) is
the full pairing
\(\tfrac12 X'_{\mathrm{NL}}\).

Taylor–Green \(\Phi_e/Y\) split
(core / low / high) is the
next measurement. No \(N=64\)
or \(N=96\) data in this
checkout. The splitter is
ready.

---

## Lock

SBP EXACT, frozen epoch.
\(\nabla R\) and
\(\partial_\Lambda R\) PROVED.
Do not mix live and frozen.
(4) remains forbidden.
Tail can hold \(\mathcal D_s\).
\(\Phi_e/Y\) OPEN.
Charge and moving \(N\) OPEN.
Not DA-NS-2. NS not solved.
