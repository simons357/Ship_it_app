# DA audit — MIN-CYCLE verifier v2

**Date:** 28 September 2026
**Gate:** MIN-CYCLE v2 (saturated integer kernel)
**Status frozen:**

\[
\text{MIN-CYCLE v2: BUILT} \to \text{SELF-TESTED} \to \text{DISARMED} \to \text{AWAITING DA REVIEW}
\]

This packet **closes the builder stage, not the gate**. It does **not**
arm the verifier. It does **not** run P2. It does **not** stamp an
unseen builder binary.

Working page: [`docs/MIN-CYCLE-VERIFIER-V2.md`](../docs/MIN-CYCLE-VERIFIER-V2.md)
Machine: [`results/min_cycle_v2_da_audit.json`](../results/min_cycle_v2_da_audit.json)

```bash
PYTHONPATH=scripts python3 -m unittest tests.test_min_cycle_verifier_v2 -q
PYTHONPATH=scripts python3 scripts/run_min_cycle_v2_da_audit.py
```

## What DA inspected

The cited file `SPEC-MIN-CYCLE-VERIFIER-V2-2026-09-28.txt` is **not in
this repository**, and the builder's code / self-test / hashes were
**not deposited here**. DA therefore did not rubber-stamp a report.
DA independently implemented and inspected:

1. The **column-HNF** transform \(H = M U\), \(U \in \mathrm{GL}(n,\mathbb Z)\).
2. The operation log: every step is `swap_cols` (det −1), `neg_col`
   (det −1), or `add_col` (det +1). No other column operations exist.
3. **Both index computations:** gcd of maximal minors (saturation
   index), and relative index of the old Q-cleared lattice inside the
   saturated kernel.
4. Independent reproduction of the \((2,1,1)^T\) regression.
5. Independent reproduction of one malformed-input refusal
   (`[[2, 1, 1.0]]`).

## Independent \((2,1,1)^T\) reproduction

Constraint: the row \([2\ 1\ 1]\), equivalently the column
\((2,1,1)^T\).

- Saturated HNF basis is unimodular-equivalent to the reported
  \((0,-1,1),\ (1,-1,-1)\). Same lattice.
- That lattice **contains** the missing primitive cycle \((0,1,-1)\).
- The old lattice (Q-nullspace, denominators cleared) is generated
  (up to signs) by \((-1,2,0),\ (-1,0,2)\). Saturation index **2**.
- \((0,1,-1)\) is **not** in the old lattice: last two coordinates of
  every old vector are even.
- Relative index of old inside saturated: **2**.
- Independent index-1 check: gcd of \(2\times 2\) minors of the
  saturated basis is **1**.

This is the repair the spec required: search over a saturated integer
kernel, not a possibly finite-index lattice obtained by clearing
denominators from a rational nullspace.

## Unimodular log (column HNF)

Every recorded operation is elementary in \(\mathrm{GL}(n,\mathbb Z)\).
The running determinant sign equals \(\det U = \pm 1\). Replaying the
log on \(I_n\) recovers \(U\). \(MU = H\).

## coeff_max caveat (attached to every future MIN-CYCLE result)

\[
\texttt{coeff\_max}\ \text{bounds coordinates in the chosen saturated basis, not }\lVert c\rVert_\infty.
\]

A reported minimum from that enumeration is **not** automatically a
global minimum over integer cycles. The spec anticipated this and
suggested **entry-bounded enumeration** if exhaustive minimum-support
certification depends on it. Every enumerator result in this package
carries that sentence.

## Firewall

- No canonical \(M, b, \gamma\)-labels are baked into the
  computational core.
- No P2 data are imported or used.
- The package does not import `ns_attacks`, `torus_p2`, or
  `one_cycle_loss`.
- `ARMED = False`, `P2_ARMED = False`,
  `FIRST_REAL_MIN_CYCLE_RUN_PERMITTED = False`.

## DA conclusion

\[
\text{DA-AUDITED (independent reproduction)} \to \text{STILL DISARMED} \to \text{NEXT: }\gamma=(\Delta,\sigma)\ \text{channel identity}
\]

- Builder-stage: **closed** (per the freeze).
- Builder binary: **not stamped** (artifacts not in this repo).
- Independent reproduction of the required tests: **pass**.
- Verifier: **DISARMED**.
- P2: **DISARMED**.

## Research chain (unchanged)

\[
\text{DA audit v2}
\ \longrightarrow\
\gamma=(\Delta,\sigma)\ \text{channel identity}
\ \longrightarrow\
\text{canonical }M,b,\text{ labels}
\ \longrightarrow\
\text{Jonathan GO}
\ \longrightarrow\
\text{first real MIN-CYCLE run}.
\]

Until those gates clear, P2 remains disarmed.

## Hashes (SHA-256) returned for review

Bundle: `6382b5edb28430c6017e1849c030abc04a5401a9d06da3b4016af358afc9d696`

| file | sha256 |
|---|---|
| `scripts/min_cycle_verifier_v2/__init__.py` | `9be149440d24a6c4948e182c85f54ebc53ee0c74e4fa412fc27a8e1ee72e9ff8` |
| `scripts/min_cycle_verifier_v2/enumerate.py` | `b23df23daf3ec7c41a9d2e6075fea1a2046e48ed1f8a565c7660e9834f1ad4c8` |
| `scripts/min_cycle_verifier_v2/exceptions.py` | `772ebb40221df2bbe9fe186c1bb5fbec112072490c2b248b2cc9767579d31ab2` |
| `scripts/min_cycle_verifier_v2/hnf.py` | `cba3f6f6f75b2483bdb30121a871272702fca75ab1b253f5f396fbe713be6b3b` |
| `scripts/min_cycle_verifier_v2/index.py` | `3305131e886a9a5bb6f48cecd57850175f1d824e55d86ea267f5fe128399a72b` |
| `scripts/min_cycle_verifier_v2/kernel.py` | `9d4c3383edd9764811e93c75e1a843185d0e35e056e8c864c85317f7df38d59b` |
| `scripts/min_cycle_verifier_v2/rational_sublattice.py` | `81154975dde42753b1e100b126eaa5269b16d4e16ad9519dbc2441caa09ca50c` |
| `scripts/min_cycle_verifier_v2/status.py` | `5c7ec06018373cbd83adaa58e29f7987f595cdf98793e4c93fbef881562dd897` |
| `scripts/min_cycle_verifier_v2/validate.py` | `0af479d1298860227a2aee7ac88d14bf4daf37dc90b29a00a39ddddcb0570fa1` |

Machine record: [`results/min_cycle_v2_da_audit.json`](../results/min_cycle_v2_da_audit.json). 66/66 tests. Column-HNF ops on `[2 1 1]`: swap 0↔1, col1 += −2 col0, col2 += −1 col0. All unimodular, \(\det U=-1\).

## Explicitly not claimed

- Verifier armed
- P2 evaluated
- NS solved
- Global \(\lVert c\rVert_\infty\)-minimum from `coeff_max`
- Stamp of a builder binary that was not deposited here
