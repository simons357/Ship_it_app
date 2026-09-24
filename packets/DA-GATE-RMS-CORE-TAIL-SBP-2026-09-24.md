# DA-GATE — RMS core / tail summation-by-parts

24 September 2026.
**Identity only. Moves the tail.
Does not remove it. Not DA-NS-2.
NS not solved.**

Desk page:
[`docs/CORE-TAIL-SBP.md`](../docs/CORE-TAIL-SBP.md).
Residual parent:
[`docs/NARROW-HET-RESIDUAL.md`](../docs/NARROW-HET-RESIDUAL.md).
Ledger:
[`docs/CENTERED-MASTER-LEDGER.md`](../docs/CENTERED-MASTER-LEDGER.md).

Every identity below was checked
in sympy (`scripts/ns_attacks/core_tail_sbp.py`).
Unaugmented NS. No \(Q_1\). No
\(\Phi\)-cancel. No SND. No
Theorem H. Unrestricted \(\star\)
**KILLED**. Charge-only **KILLED**.
Static SAG depletion **KILLED**.

Pick **one** \(\Lambda\) convention.
This gate is the **frozen epoch**
\(\lambda_e=\kappa_e^2\). Do not
mix it with live \(\kappa(t)=\sqrt\Lambda\).

---

## Steps (1)–(4)

Chebyshev tail bound and the
core-radius bound (2) are
**PROVED**. The factor of two
is exact: at the shell,
\(\mathrm{d}(m^2)/\mathrm{d}m=2\kappa\).

For (3), the gradient of \(R\)
at the core \(i=j=o=\kappa\),
\(\Lambda=\kappa^2\), is

\[
\boxed{
\nabla_{(i,j,o)}R=(5\kappa^2,5\kappa^2,0),
\qquad
\partial_\Lambda R=-2\kappa.
}
\]

Hence, with the core centered
on the **same** \(\kappa\) that
appears in \(2\kappa^3\),

\[
\boxed{
\lvert R-2\kappa^3\rvert
\le 5\kappa^3 L r+O((Lr)^2).
}
\]

Convention flag on (3). Written
with the **live** \(\Lambda\)
there is no moving term, but
\(2\kappa(t)^3 Q_a\) no longer
telescopes. Written with the
**frozen** \(\lambda_e\), the
core is at \(\kappa_e\) and
picks up an extra

\[
\boxed{
R(\kappa_e,\kappa_e,\kappa_e;\Lambda)-2\kappa_e^3
=-2\kappa_e(\Lambda-\lambda_e).
}
\]

Do not quote the \(5\kappa^3 Lr\)
bound from the live core and
the SBP from the frozen core
in the same line.

Diagnosis of (4): **PROVED** as
the forbidden replacement of a
signed sum by a sum of absolute
values. That step stays dead.

On the tail: small \(X\)-mass and
small \(Y\)-mass can still hold
essentially all of \(\mathcal D_s\).
Tail leakage competes with
\(\nu\mathcal D_s\) restricted to
the tail. That is the BROAD
missing estimate again.

---

## Two existing identities — PROVED

Weight \(\lvert m\rvert\) has flux
\(2o(i-j)\) on heterochiral triads
and \(0\) on homochiral ones
(Heavy normalization). Raw
Waleffe \(\dot I=2g(s_p\lvert p\rvert-s_q\lvert q\rvert)\)
gives \(4go(i-j)\) on \((++-)\);
Heavy absorbs the \(2g\).

\[
\boxed{
Q_{a,\Gamma}
=\tfrac12\Bigl(\frac{d}{dt}\Bigr)_{\mathrm{NL}}
\lVert u\rVert_{\dot H^{1/2}}^2.
}
\]

Charge is the flux of the
critical \(\dot H^{1/2}\) norm.
This is the same shape as the
dossier cross-radius helicity
primitive (ledger §13), read
on the weight \(\lvert k\rvert\).
Not re-identified with
\(\Psi_\lambda^\varepsilon\) here.

\[
\boxed{
M^{\mathrm{het}}=\sum AHQ,
\qquad
N^{\mathrm{het}}=\sum AQ.
}
\]

---

## Summation-by-parts — EXACT

\[
\boxed{
\phi_e(m)
=\tfrac12(m-\kappa_e)^2
(m^2+2\kappa_e m+2\kappa_e^2)\ge 0.
}
\]

\(\phi_e(\kappa_e)=\phi_e'(\kappa_e)=0\),
\(\phi_e(0)=\kappa_e^4\),
\(\phi_e(m)\sim m^4/2\) at large \(m\).

Capacity \(\Phi_e=\sum_k\phi_e(\lvert k\rvert)\lvert a_k\rvert^2\).
Normalize as in the clock:

\[
\mathfrak T_c=\tfrac12\sum_m(m^4-\Lambda m^2)\dot I_m,
\quad
N=\tfrac12\sum_m m^2\dot I_m,
\quad
Q_a=\tfrac12\sum_m m\,\dot I_m.
\]

Then, exactly, over **all**
triads (only energy
\(\sum\dot I_m=0\) is used),

\[
\boxed{
\mathfrak T_c
=
\Bigl(\frac{d}{dt}\Bigr)_{\mathrm{NL}}\Phi_e
+2\kappa_e^3 Q_a
-(\Lambda-\lambda_e)N.
}
\]

The modal weight residual is
\(-\kappa_e^4\), killed by
energy conservation.

Narrow-homochiral and
heterochiral-radial variation
land on \(\Phi_e'\), not on
\(\sum\lvert Q\rvert\). That is
the bridge, **stamped as an
identity only**. It is not a
solution of
\(\mathsf B^{\mathrm{prim}}w=A\).
Loop-primitive holonomy stays
**NO**. This \(\phi_e\) is a
different object.

\(N\) in the identity is the
full nonlinear pairing
\(\tfrac12 X'_{\mathrm{NL}}\).
\(N^{\mathrm{het}}=\sum AQ\) is
its heterochiral part.

---

## What it costs — all OPEN

- \(\phi_e(0)=\kappa_e^4\).
  \(\phi_e\) grows like \(m^4/2\).
  \(\Phi_e/Y\) is **not**
  controlled by \(r^2\).
  Low-mode energy enters as
  \(\kappa_e^4 E\). That piece
  is a \(Y\)-scale obstruction,
  not an \(r^2\) remainder.
- Integrating \(\Phi_e'/Y\) by
  parts returns
  \(\Phi_e Y'/Y^2\), absorbable
  only if \(\Phi_e/Y\) is small.
  Tail leakage reappears as
  the weight of \(\phi_e\) away
  from the shell.
- Viscous part of \(\Phi_e\) has
  the good sign. Epoch resets
  add a jump ledger for
  \(\kappa_e\mapsto\kappa_{e+1}\).
- The residual is still the
  charge (\(\dot H^{1/2}\) flux)
  and \(-(\Lambda-\lambda_e)N\).

Lemma A PROVED
([`docs/LEMMA-A-SBP.md`](../docs/LEMMA-A-SBP.md)).
\(C_\kappa\le 1\) on \(m\ge 1\).
\(\Phi_e\le D_e^{\mathrm{frozen}}
=D_s+X(\Lambda-\lambda_e)^2\).
Low tail absorbed. Last mile
= charge + epoch motion.

---

## Lock

SBP EXACT, frozen epoch.
\(\nabla R=(5\kappa^2,5\kappa^2,0)\),
\(\partial_\Lambda R=-2\kappa\)
PROVED. Live vs frozen: do
not mix. Factor two in the
core-radius comparison EXACT.
(4) stays the forbidden
absolute-sum step.
Tail can hold \(\mathcal D_s\).
Lemma A PROVED. Low tail
absorbed. Sharp L3/L4.
Lemma B OPEN.
Not DA-NS-2. NS not solved.
