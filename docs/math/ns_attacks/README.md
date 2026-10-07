# NS attacks — exact-shell / shared-budget desk

**Active focus (Oct 7 2026 handoff):** exact-shell geometry + viscous
smoothing; separate axisymmetric signed-compression swirl branch.

**Not claimed:** classical unaugmented NS regularity; all-shape
criterion **(17)**; swirl compression closure.

## Durable source of truth

| Doc | Role |
|---|---|
| [`NS-HANDOFF-2026-10-07.md`](NS-HANDOFF-2026-10-07.md) | Cross-device handoff SoT (evidence labels, 17/32 tables, constants, open list) |
| [`PRIORITY-1-32-FAMILY-INDEPENDENT-REVIEW.md`](PRIORITY-1-32-FAMILY-INDEPENDENT-REVIEW.md) | Independent analytic review of recovered 32-family package vs filing |
| [`PRIORITY-2-SIGNED-EFFICIENCY.md`](PRIORITY-2-SIGNED-EFFICIENCY.md) | Exact-family signed-efficiency numerical probe (finite search) |
| [`OPEN-ITEMS-3-6.md`](OPEN-ITEMS-3-6.md) | Priorities 3–6 left Open with precise scope |

Vault mirrors (same content roots):

- [`docs/NS-HANDOFF-2026-10-07.md`](../../NS-HANDOFF-2026-10-07.md)
- [`docs/SHARED-BUDGET-32-SHAPE-EXTENSION.md`](../../SHARED-BUDGET-32-SHAPE-EXTENSION.md)
- [`packets/Shared-Budget-17-Family-Audit-and-9-25-Extension/`](../../../packets/Shared-Budget-17-Family-Audit-and-9-25-Extension/)

## Fixtures and scripts

| Path | Role |
|---|---|
| `fixtures/shared_budget_32/family-lists.json` | Exact 17 + 15 lists |
| `fixtures/shared_budget_32/constants.json` | ρ, ρ′, multiplicities, high-pass formulas |
| `scripts/ns_attacks/verify_families.py` | Finite enumeration / overlap / face checks |
| `scripts/ns_attacks/signed_efficiency_probe.py` | Priority-2 numerical probe |

## ZIP status

Package name: `Shared-Budget-17-Family-Audit-and-9-25-Extension.zip`  
Library ID (reported): `libfile_e69ca0f14ab4819186900a547b61df20`  
**ZIP retrieval is no longer the research blocker** (recovered Oct 7 in
source conversation; bundled `verify_families.py` passed there).  
This workspace may still lack binary bytes; finite checks are
reimplemented from the handoff lists and rerun here.

## Related PR / branch context

- Independent-review package also lives on
  `cursor/shared-budget-32-shape-c3ed` (PR #166).
- This desk branch continues Priority 1–2 work without mixing into
  Lemma★ / axisymmetric lock branches.
