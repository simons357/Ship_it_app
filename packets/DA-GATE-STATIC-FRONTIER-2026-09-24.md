# DA-GATE — static frontier: arithmetic sign realizability

**24 September 2026.** Board frozen. This is a protocol lock, not a close.

**Do not alter**
[`packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md`](DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md)
(separate PR). That gate stays as filed.

**Classical unaugmented 3-D Navier–Stokes stays open.**
DA-NS-2 stays **OPEN**. No more potentials. No more
reinterpretation of the same clock. Run this gate.

Machine: [`scripts/da_gate_static_frontier.py`](../scripts/da_gate_static_frontier.py).
Lock: [`data/da_gate_static_frontier_2026-09-24.json`](../data/da_gate_static_frontier_2026-09-24.json).

Notation collision: the pair \(\rho_N^\pm\) below is the first-variation
sign pair of this gate. It is **not** the ledger remainder
\(\rho_\Gamma\). Do not mix those symbols.

---

## Status

| Item | Bucket |
|---|---|
| First-variation object \(L_{1,N}\) | **LOCKED** (definition) |
| Remainder check \(R_{2,N}\) | **LOCKED** (definition) |
| Silent \(T^{(0)}\) substitution into the finite-gap identity | **FORBIDDEN** |
| Four-outcome tree | **LOCKED** |
| \(\mathcal A_N^{+}\) seed schema | **LOCKED** |
| Predicted higher-order behaviour of \(R_{2,N}\) | **OPEN** (to be measured) |
| Sign-realizability search | **OPEN** — this is the gate |
| Gram / lattice encoding of a one-sign restriction | **OPEN**, only if ONE SIGN appears |
| \(I_3\) arithmetic as a seated NS remainder | **NOT SEATED** here |
| \(\Theta_N=\nu\kappa_N^2\tau_{U,N}\) | **NAMED**, live only after BOTH SIGNS |
| DA-NS-2 | **OPEN** |

---

## Notation safeguard

In the discrete expansion

\[
T_c
=
\Lambda\langle\delta,T\rangle
+
\sum_m\delta_m^2 T_m,
\]

the \(T_m\) in the exact neighboring state itself also varies with
the deformation. Do not treat that \(T\) as frozen.

For the first variation the object is

\[
\boxed{
L_{1,N}
=
\Lambda_N
\langle
\delta_N,
T_N^{(0)}
\rangle,
}
\]

provided the family is the **asymptotic neighboring-shell** family,
so the transfer variation contributes only at the next order.

Heavy must retain the actual neighboring \(T_m\) separately as a
remainder check. Silently substituting \(T^{(0)}\) into the full
finite-gap identity is **FORBIDDEN**.

That gives the numerical consistency test

\[
\boxed{
R_{2,N}
:=
T_{c,N}
-
\Lambda_N
\langle
\delta_N,
T_N^{(0)}
\rangle.
}
\]

For a legitimate first-variation sequence, \(R_{2,N}\) must show the
predicted higher-order behaviour. If it does not, the deformation
changed polarization, amplitudes, or topology too strongly to
represent the intended gate. The predicted order is **not invented
here**; it is a measurement on the sequence Heavy actually runs.

This packet does **not** complete a finite-gap identity, and it does
not expand the neighboring \(T_m\). Those stay with Heavy as a
remainder check.

---

## Outcome tree — LOCKED

If Heavy gets a persistent **BOTH SIGNS** heterochiral family with

\[
\lvert\rho_N^\pm\rvert\ge c>0,
\]

then the static verdict is explicit:

\[
\boxed{
\text{universal first-order one-sided narrow depletion is false}.
}
\]

At that point **stop static closure work on this question**. The
positive branch goes directly into evolution, and

\[
\Theta_N=\nu\kappa_N^2\tau_{U,N}
\]

becomes one of the most important numbers in the project. This
packet names \(\Theta_N\). It does not evaluate it.

If Heavy instead gets systematic **ZERO ONLY** in homochiral
families, that is consistent with the Vandermonde delay. It does
**not** rescue the full NSE: heterochiral remains separate.

If Heavy gets **ONE SIGN** heterochirally, determine whether the
restriction is encoded by the Gram / lattice realization problem.
That would be the first serious bridge from the \(I_3\) arithmetic
work into the centered dynamics rather than merely into occupancy.
This packet does **not** seat \(I_3\) and does not reconstruct it.

**NO NEIGHBOR** remains its own category. Arithmetic rigidity is
not sign depletion.

| Outcome | Verdict |
|---|---|
| BOTH SIGNS, \(\lvert\rho_N^\pm\rvert\ge c>0\) | one-sided narrow depletion is false; stop static closure; go to evolution; keep \(\Theta_N\) |
| ZERO ONLY, homochiral | consistent with Vandermonde delay; NSE not rescued |
| ONE SIGN, heterochiral | test Gram / lattice realization; prospective \(I_3\) bridge |
| NO NEIGHBOR | own category; arithmetic rigidity \(\neq\) sign depletion |

---

## Adversarial seed — LOCKED

If BOTH SIGNS appears, save the actual integer vectors, helicity
labels, polarizations, and amplitudes — **not** merely \(\delta\)
and \(T^{(0)}\). That object is the canonical adversarial seed

\[
\boxed{\mathcal A_N^{+}}
\]

for the dynamic phase: an exact, reproducible, increasingly narrow
field that is statically pointed in the dangerous direction. Then
the NSE itself gets the next move.

Required fields of \(\mathcal A_N^{+}\):

- integer wavevectors
- helicity labels
- polarizations
- amplitudes

Insufficient by themselves: \(\delta\), \(T^{(0)}\).

---

## Frozen board

\[
\boxed{\textbf{STATIC FRONTIER: arithmetic sign realizability}}
\]

\[
\Downarrow
\]

\[
\boxed{\textbf{DYNAMIC FRONTIER: dangerous-state persistence}}
\]

No more potentials. No more reinterpretation of the same clock.
Run the gate.

**NS not solved.**
