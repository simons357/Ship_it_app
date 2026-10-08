# Gate D — height × duration on normalized blocks

8 October 2026.
**ACTIVE shot. Not (17).**

Parent deficit:
[`GATE-C-HALF-DERIVATIVE-2026-10-08.md`](GATE-C-HALF-DERIVATIVE-2026-10-08.md).

Program: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

---

## Deficit (from Gate C)

\[
\boxed{\text{We need a dynamical mechanism worth one half derivative.}}
\]

Schematic residual after shared energy:
\[
\mathcal T_{\mathrm{bad}}
\lesssim
\nu Y\times\Lambda^{1/2}
\quad\text{(an \(H^{1/2}\) deficit).}
\]

---

## The shot

Control the missing budget by summing normalized block costs:
\[
\boxed{
\sum_I B_I
\le
C(u_0,\nu,K,T)
}
\]
uniformly in the Galerkin cutoff \(N\).

That bound would directly control
\[
\mathcal S_{K,N}(T)
=
\int_0^T
\frac{\bigl[\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4\bigr]_+}{X_N}\,dt
\]
and close the path to the high-pass criterion at the level of (17)’s
budget object — still **not** a Clay claim, still scoped.

---

## Promising clue (onset law)

The onset law already shows a dangerous-looking **positive crossing**
can carry only
\[
O(\rho^{-2})
\]
normalized cost on its **first shrinking window**.

So:

- amplitude growth ≠ budget cost;
- dynamics is compressing the time window.

That is the seed of a mechanism, not yet a theorem.

---

## Mechanism to prove or kill

Ask whether the onset clue upgrades to a **general** law:
\[
\boxed{
\text{height}\times\text{duration}
}
\]
with enough decay (in the normalized block variables) to recover the
missing half derivative.

| Object | Role |
|---|---|
| **Height** | Size of the positive / dangerous crossing in the normalized block |
| **Duration** | Length of the shrinking time window supporting that crossing |
| **Product** | Normalized block cost \(B_I\) (onset clue: first window \(O(\rho^{-2})\)) |
| **Sum** | \(\sum_I B_I\) — must stay \(\le C(u_0,\nu,K,T)\) uniformly in \(N\) |

This is the dynamical content of the quartic forcing / normalized
block-evolution identity: time integration sees height×duration;
damping and structural cancellation are the levers that may force
the product to decay hard enough for \(H^{1/2}\).

---

## Not the next target

| Non-target | Why |
|---|---|
| Shell-count / multiplicity upgrades | Does not buy height×duration decay |
| Young / equal-allocation reshuffles | Instantaneous budget face, not window compression |
| Generic instantaneous phase cancellation | Not a dynamical duration mechanism |
| Finite family extensions (52/70/100) | Parked at Gate A |
| Random-phase fishing | Parked |
| Ring / swirl-as-substitute / B41→NSE | Parked as before |

Older fixed-block \(\mathcal Q\)-identity for \((5,8,25)\): laboratory
precedent only — do not silently promote to all-shape (17).

---

## Immediate work

1. Define \(B_I\) precisely from the normalized block-evolution /
   quartic forcing identity (onset-law normalization).
2. Prove or refute: first-window cost \(O(\rho^{-2})\) extends to a
   general height×duration bound with summable / uniform control.
3. Check whether that decay is enough to erase the \(H^{1/2}\) deficit
   in \(\mathcal S_{K,N}(T)\).

---

## STATUS

GATE D: ACTIVE — THE SHOT IS \(\sum B_I\le C\) VIA HEIGHT×DURATION.
CLUE: ONSET LAW, FIRST WINDOW \(O(\rho^{-2})\); AMPLITUDE ≠ BUDGET COST.
TARGET: RECOVER \(H^{1/2}\) IN \(\mathcal S_{K,N}(T)\).
SHELL-COUNT / YOUNG / GENERIC PHASE: NOT THE NEXT TARGET.
(17) NOT CLAIMED.
NS NOT SOLVED.
