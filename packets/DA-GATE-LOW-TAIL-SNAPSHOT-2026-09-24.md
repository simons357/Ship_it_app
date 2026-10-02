# DA gate — low-tail snapshot on existing families

**24 September 2026.** After the \(\phi_\kappa/d_\kappa\) comparison, the
solver ask was \(L_e=\kappa_e^4 E_{\mathrm{low}}/Y\) and the exact
\(\phi_e\) low-tail share. Taylor–Green \(N=64/96\) is **not on this
tree**. This filing does the same diagnostic on the evaluator
families that are. It is a snapshot, not a trajectory, not a theorem.

Lock: `scripts/da_gate_low_tail_snapshot.py`.
Comparison: [`DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md`](DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md).
Rally: [`../docs/ns-recovery/CENTERED-RESIDUAL-BOARD.md`](../docs/ns-recovery/CENTERED-RESIDUAL-BOARD.md).

**Not a closure theorem.** Ordinary NS is not solved. Soft X silent.
Do not put \(K(t)\) in the PDE.
Do not mix this snapshot freeze into the SBP identity.

---

## Exact rewrite of \(\phi_\kappa\) — EXACT

The boxed weight expands uniquely as

\[
\phi_\kappa(m)
=
\kappa^4
-\kappa^3 m
-\tfrac12\kappa^2 m^2
+\tfrac12 m^4.
\]

Hence, with \(H=\|u\|_{\dot H^{1/2}}^2=\sum_k\lvert k\rvert\lvert a_k\rvert^2\),

\[
\Phi_e
=
\kappa^4 E
-\kappa^3 H
-\tfrac12\kappa^2 X
+\tfrac12 Y.
\]

Charge \(Q_a\) is the nonlinear flux of the same \(H\). The low-tail
capacity and the charge residual share a primitive moment. That is
an identity, not a bound.

---

## Snapshot convention (not the SBP freeze)

On a static field the only available epoch is

\[
\kappa_e=\sqrt{\Lambda},\qquad \lambda_e=\Lambda.
\]

That makes the moving term \(-(\Lambda-\lambda_e)N\) vanish by
construction. It is a **diagnostic**, labeled
`SNAPSHOT_kappa_eq_sqrt_Lambda`. It is not substituted into

\[
T_c=(d/dt)_{\mathrm{NL}}\Phi_e+2\kappa_e^3 Q_a-(\Lambda-\lambda_e)N.
\]

Low / core / high use the same comparable cut as (C):
\(m<\tfrac12\kappa\), \(\tfrac12\kappa\le m\le 2\kappa\), \(m>2\kappa\).

---

## What the on-tree families say — REPORTED

| Field | \(\kappa\) | \(\min m/\kappa\) | \(L_e\) | \(\Phi_e/Y\) | low-tail share of \(\Phi_e\) |
|---|---:|---:|---:|---:|---:|
| §4 note triad | \(1.18\) | \(0.845\) | \(0\) | \(0.075\) | \(0\) |
| near-shell \(\varepsilon=0.025\) | \(2.24\) | \(0.895\) | \(0\) | \(1.6\cdot10^{-5}\) | \(0\) |
| \(v_1\) | \(2.25\) | \(0.444\) | \(0.048\) | \(0.102\) | \(0.22\) |
| \(v_8\) | \(17.5\) | \(0.456\) | \(0.060\) | \(0.113\) | \(0.23\) |
| separated \(L=2\) | \(2.04\) | \(0.491\) | \(0.296\) | \(0.132\) | \(0.94\) |
| separated \(L=8\) | \(8.00\) | \(0.125\) | \(0.330\) | \(0.286\) | \(1.00\) |
| separated \(L=16\) | \(16.0\) | \(0.0625\) | \(0.332\) | \(0.311\) | \(1.00\) |

Core band obeys (C) on every row. TG not run.

### Growing layer is not the low-tail enemy

\(v_n\) has \(\min m=n\), scaling with \(\kappa=\Theta(n)\).
\(\min m/\kappa\) freezes near \(0.45\). The \(a=\tfrac12\) cut
nicks the inner edge of a fat annulus; at \(a=0.4\) there is
**no** low tail and \(L_e=0\). \(\Phi_e/Y\) stays \(\approx 0.11\).
This is a comparable annulus. It is the family that killed
unrestricted ★. It is **not** a high core plus an \(O(1)\) reservoir.

### Separated triad is the on-tree adversary

Section 5 field: one pair at \(m=1\) (\(E_{\mathrm{low}}=2\)) and
closing modes at \(m\sim L\). Snapshot \(\kappa\sim L\),
\(\min m/\kappa=1/L\to 0\). \(\Phi_e\) is low-tail dominated
already at \(L=2\), and entirely so by \(L=8\).

On that field, \(Y\sim 6L^4\) and

\[
L_e\to\frac13,\qquad \frac{\Phi_e}{Y}\to\frac13.
\]

That is arithmetic of the amplitudes, not a PDE statement and not
Taylor–Green. It shows the diagnosis is not vacuous: a field
already on this book makes \(\Phi_e/Y\) an order-one low-tail
tax while the barycenter runs to infinity.

Energy still does not pay it. \(E_{\mathrm{low}}=2\) is fixed;
\(\kappa^4 E_0/Y\) stays order one.

---

## What this changes about the last mile

The testable question stays

\[
\text{Can an NSE trajectory keep enough }m=O(1)\text{ mass under a high }
\kappa_e\text{ to make }L_e\text{ large on dangerous time?}
\]

On-tree static evidence:

- comparable / near-shell / \(v_n\) do **not** produce a large \(L_e\);
- the old separated triad **does**, and the spike is low-tail dominated.

If \(N=64/96\) later shows a \(\Phi/Y\) spike that is **not**
low-tail dominated, this diagnosis is wrong. If it is, the
theorem target remains: persistence of a low-frequency reservoir
underneath an upward-moving high-frequency barycenter.

Those TG data remain **not on this tree**.

---

## What this does not do

It does not obtain DA-NS-2.
It does not turn a static triad into an NSE trajectory.
It does not mix snapshot \(\kappa=\sqrt{\Lambda}\) into the frozen
SBP identity.
It does not invent \(\mathsf B^{\mathrm{prim}}\).
It does not stamp \(r\sim\kappa^{-1/2}\).

No new estimate is claimed. No continuation criterion.
**NS not solved.**
