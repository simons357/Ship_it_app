# DA gate — RMS core / tail / summation-by-parts

**24 September 2026.** Filing of the RMS core–tail SBP gate
on this book. The source name is
`packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md`.
The original sympy notebook is **not on this tree**.
Elementary facts are rechecked here in
`scripts/da_gate_rms_core_tail_sbp.py`.
The full triad identity is **filed as stated**, not rebuilt.

**Not a closure theorem.** Ordinary NS is not solved. Soft X silent.
Do not put \(K(t)\) in the PDE.
Convention: **FROZEN epoch** \((\kappa_e,\lambda_e=\kappa_e^2)\).
Do not mix with the live-\(\Lambda\) writing.

Rally: [`docs/ns-recovery/CENTERED-RESIDUAL-BOARD.md`](../docs/ns-recovery/CENTERED-RESIDUAL-BOARD.md).

---

## What is PROVED / elementary (rechecked)

### Weight \(\phi_e\)

\[
\phi_e(m)
=\tfrac12(m-\kappa_e)^2(m^2+2\kappa_e m+2\kappa_e^2)\ge 0.
\]

Shift \(u=m-\kappa_e\):

\[
\phi_e(\kappa_e+u)
=\tfrac12 u^2\bigl(u^2+4\kappa_e u+5\kappa_e^2\bigr),
\qquad
u^2+4\kappa_e u+5\kappa_e^2=(u+2\kappa_e)^2+\kappa_e^2\ge\kappa_e^2.
\]

So \(\phi_e\) is nonnegative, vanishes to **second order** at the
shell, \(\phi_e(0)=\kappa_e^4\), and \(\phi_e\sim m^4/2\) at large
\(m\).

Capacity \(\Phi_e=\sum_k\phi_e(\lvert k\rvert)\lvert a_k\rvert^2\).

### Heterochiral \(R\) at the core

Recorded

\[
R_{\Lambda}(i,j,o)
=\frac{(i+o)(j+o)}{2o}\bigl(H_{ij\mid o}-\Lambda\bigr),
\qquad
H_{ij\mid o}=i^2+j^2+o^2+ij-o(i+j).
\]

At \((i,j,o)=(\kappa,\kappa,\kappa)\):

\[
\partial_\Lambda R=-2\kappa,
\qquad
\nabla_{i,j,o}R=(5\kappa^2,5\kappa^2,0)
\quad(\Lambda=\kappa^2).
\]

Frozen core: \(R(\kappa_e,\kappa_e,\kappa_e;\lambda_e)=2\kappa_e^3\),
and

\[
R(\kappa_e,\kappa_e,\kappa_e;\Lambda)-2\kappa_e^3
=-2\kappa_e(\Lambda-\lambda_e).
\]

That is the extra \(2\kappa_e\lvert\Lambda-\lambda_e\rvert\) in
the frozen convention. Live convention \(\kappa=\sqrt{\Lambda}\)
has \(R=2\kappa^3\) exactly on the core and **no** moving term,
but \(2\kappa(t)^3 Q_a\) does not telescope. Pick one.
This filing uses **frozen**.

Chebyshev tail bound and core-radius bound with exact factor
two: **PROVED** in the source gate, not rebuilt here.

---

## Two existing identities (PROVED in the source gate)

Weight \(\lvert m\rvert\) has flux \(2o(i-j)\) on heterochiral
triads and zero on homochiral ones. With Heavy’s normalization,

\[
Q_{a,\Gamma}
=\tfrac12\Bigl(\frac{d}{dt}\Bigr)_{\mathrm{NL}}
\|u\|^2_{\dot H^{1/2}}.
\]

Charge is the flux of the critical \(\dot H^{1/2}\) norm.
Whether this is the dossier’s cross-radius helicity primitive
is **not confirmed** here (dossier not on this tree).

\[
M^{\mathrm{het}}=\sum AHQ,
\qquad
N^{\mathrm{het}}=\sum AQ.
\]

---

## Summation-by-parts — EXACT as filed (not rebuilt)

Over all triads, frozen epoch:

\[
T_c
=
\Bigl(\frac{d}{dt}\Bigr)_{\mathrm{NL}}\Phi_e
+2\kappa_e^3 Q_a
-(\Lambda-\lambda_e)N.
\]

Narrow-homochiral and heterochiral-radial pieces together are
the nonlinear time derivative of one nonnegative capacity that
vanishes to second order at the shell. The order-\(r\) multiplier
variation lands on \(\Phi_e'\), not on \(\sum\lvert Q\rvert\).
That is the described bridge, **stamped as an identity only**.
It moves the tail problem. It does not remove it.

Replacing a signed sum by a sum of absolute values stays
**forbidden**.

---

## What it costs (all OPEN)

- \(\phi_e(0)=\kappa_e^4\) and \(\phi_e\sim m^4/2\) at high \(k\),
  so \(\Phi_e/Y\) is **not** controlled by \(r^2\). Low-mode
  energy enters as \(\kappa^4 E\), which is always at least \(Y\).
- Integrating \(\Phi_e'/Y\) by parts returns \(\Phi_e Y'/Y^2\),
  absorbable only if \(\Phi_e/Y\) is small. Tail leakage
  reappears as the weight of \(\phi_e\) away from the shell.
- The tail can hold essentially all of \(D_s\) while carrying
  small \(X\)-mass and small \(Y\)-mass. Tail leakage competes
  with \(\nu D_s\) restricted to the tail: the BROAD missing
  estimate again.
- Viscous part has the good sign. Epoch resets add a jump
  ledger.
- Residual after the identity:

\[
2\kappa_e^3 Q_a
\qquad\text{and}\qquad
-(\Lambda-\lambda_e)N.
\]

Charge is the \(\dot H^{1/2}\) flux.

---

## Taylor–Green \(\Phi_e/Y\) split

A useful next measurement is \(\Phi_e/Y\) split into core, low
tail, and high tail on the existing \(N=64\) and \(N=96\)
Taylor–Green runs. **Those data are not on this tree.** The
split is not run here. Evidence only if and when it is run.

---

## What this does not do

It does not obtain DA-NS-2.
It does not control \(\Phi_e/Y\) by \(r^2\).
It does not rebuild the source sympy notebook.
It does not mix live \(\Lambda\) with frozen \(\lambda_e\).
It does not stamp a remainder from \(\sum\lvert Q\rvert\).

No new estimate is claimed. No continuation criterion.
**NS not solved.**
