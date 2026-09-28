# MIN-CYCLE verifier v2 — DA working page

**Status frozen:** `MIN-CYCLE v2: BUILT → SELF-TESTED → DISARMED → AWAITING DA REVIEW`

This page records DA's independent reproduction of the v2 repair.
It is not an arming. It is not a P2 run. It is not a stamp of an
unseen builder binary.

Packet: [`packets/DA-AUDIT-MIN-CYCLE-VERIFIER-V2-2026-09-28.md`](../packets/DA-AUDIT-MIN-CYCLE-VERIFIER-V2-2026-09-28.md)
Machine: [`results/min_cycle_v2_da_audit.json`](../results/min_cycle_v2_da_audit.json)

```bash
PYTHONPATH=scripts python3 -m unittest tests.test_min_cycle_verifier_v2 -q
PYTHONPATH=scripts python3 scripts/run_min_cycle_v2_da_audit.py
```

## Repair

Search is over the **saturated integer kernel**

\[
\ker_{\mathbb Z}(M)=\{x\in\mathbb Z^n:Mx=0\},
\]

computed as the trailing columns of the unimodular factor \(U\) in
the column Hermite form \(H=MU\). This is not the lattice obtained
by taking a \(\mathbb Q\)-nullspace and clearing denominators. That
old lattice can sit at finite index inside the true kernel.

## \((2,1,1)^T\) regression

For \(M=[2\ 1\ 1]\) (equivalently the column \((2,1,1)^T\)):

| object | result |
|---|---|
| saturated basis (builder report) | \((0,-1,1),\ (1,-1,-1)\) — DA recovers the same lattice |
| missing primitive cycle | \((0,1,-1)\) **is** in the saturated lattice |
| old Q-cleared lattice | index **2**; does **not** contain \((0,1,-1)\) |
| gcd of maximal minors (saturated) | **1** |
| relative index old ⊂ saturated | **2** |

## Unimodular operations

Column HNF uses only:

- swap two columns (det −1)
- negate a column (det −1)
- add an integer multiple of one column to another (det +1)

`det U = ±1` is maintained as a running sign and checked by an
independent determinant.

## Two index computations

1. **Saturation index:** gcd of the maximal minors of a generator
   matrix. Equals 1 iff the lattice is saturated in its Q-span ∩ Z^n.
2. **Relative index:** saturation-index(sub) / saturation-index(sat),
   after checking containment. For the old Q-cleared lattice of
   `[2 1 1]` this is 2.

## coeff_max is not \(\lVert c\rVert_\infty\)

`coeff_max` bounds coordinates **in the chosen saturated basis**.
A short cycle can require large basis coefficients after a unimodular
skew, and a long cycle can have small basis coefficients. A minimum
reported from that enumeration is not a global minimum over integer
cycles. Use **entry-bounded** enumeration (`||c||_∞ ≤ B`) when a
minimum-support certificate depends on a coordinate bound.

This sentence is attached to every enumerator result.

## Firewall / disarm

- No canonical \(M,b,\gamma\)-labels in the computational core.
- No P2 data.
- `ARMED = False`. P2 stays disarmed.
- First real MIN-CYCLE run is not permitted on this packet.

## Next gate

\[
\gamma=(\Delta,\sigma)\ \text{channel identity}
\]

then canonical \(M,b,\) labels, then Jonathan GO, then the first
real MIN-CYCLE run. Not before.
