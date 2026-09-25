# Erratum — withdrawn Taylor–Green fraction

**Date:** 25 September 2026
**Schema:** v5
**Status of old value:** WITHDRAWN — historical provenance only

## Live scientific value

Replace every live citation of the withdrawn Taylor–Green fraction
with

\[
r^2=2.2291,\qquad \frac{T_c}{\nu D_s}=1.2259.
\]

These are the values Process Console and Atlas export. They are
numerical / diagnostic constants on this desk, not a regularity proof.

## Withdrawn value

| Field | Value |
|---|---|
| Old fraction | \(3915/663\) |
| Diagnostic imbalance | 3,915 broad-spectral counts vs 663 pointwise viscous counts |
| Status | **WITHDRAWN** |
| Cite as evidence? | No |

Leave the old numbers only where a historical run must be readable
(Q4-1 v1). Those records are marked WITHDRAWN / defective /
INCONCLUSIVE.

## Sweep

```bash
python scripts/sweep_withdrawn_taylor_green.py
```

Any live ledger, paper, or reviewer artifact that still treats
\(3915/663\) as a scientific value is a regression.

## What the error became

1. This erratum.
2. Regression tests in `tests/test_atlas_and_errata.py`.
3. Process rule: a failed consistency check is INCONCLUSIVE and cannot
   be promoted.
4. Atlas closed shortcut: a broad spectral state does not imply
   pointwise viscous payment of the dangerous term.
