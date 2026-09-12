# Draft PR — Zenodo inventory correction

**Branch:** `cursor/zenodo-inventory-correction-0cc5`  
**Open:** https://github.com/simons357/Ship_it_app/pull/new/cursor/zenodo-inventory-correction-0cc5

## Title
Correct Zenodo inventory from live API (Aug 14 dump was stale/misaligned)

## Body
See commit message and `docs/zenodo/INVENTORY-CORRECTION-2026.md`.

- Aug 14 is **not** newest; file columns were shifted.
- Corrected CSV: `data/zenodo/ZENODO_INVENTORY_CORRECTED_LIVE_numbers.csv`
- KEEP 8 / PARK 17 / REVIEW 6 / NEEDS_TITLE_CLEAN 0 / NEEDS_AUDIT_FIX 1
