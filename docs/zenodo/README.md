# Zenodo metadata remediation (August 2026)

Urgent fix for **ERRATA / WITHDRAWN / SUPERSEDED banners in deposit titles**. Those notices belong in the **description** (under the honest abstract), not in the title field.

## Quick commands

```bash
# Live audit against Zenodo API
python3 scripts/zenodo_metadata_remediation.py audit

# Copy-paste instructions for records that still need fixes
python3 scripts/zenodo_metadata_remediation.py manual-instructions

# Regenerate per-deposit markdown from data/zenodo/deposit_metadata.json
python3 scripts/zenodo_metadata_remediation.py write-docs
```

## API apply (optional)

```bash
export ZENODO_ACCESS_TOKEN=...   # Zenodo account → Applications → Personal access tokens
python3 scripts/zenodo_metadata_remediation.py dry-run --record-id 20405526
python3 scripts/zenodo_metadata_remediation.py apply --record-id 20405526
```

Without a token, use `manual-instructions` output or the per-deposit files in `deposits/`.

## Files

| Path | Role |
| --- | --- |
| `CORRECTION-INDEX-2026.md` | Single public index page content |
| `data/zenodo/deposit_metadata.json` | Canonical inventory (KEEP vs PARK/ARCHIVE) |
| `deposits/*.md` | Per-record clean title + description errata block |
| `../scripts/zenodo_metadata_remediation.py` | Audit + optional API remediation |

## Presentation rule

1. **Title** — scholarly title only (what the deposit is).
2. **Description top** — honest abstract or scope for corrected KEEP records.
3. **Description bottom** — correction notice explaining withdrawals and pointing to the status index `10.5281/zenodo.22050978`.

## Related repo docs

Domain Architect audited baseline (software KEEP, no Clay): `docs/domain-architect/00-AUDITED-BASELINE.md`

Historical submit pack (on branch `cursor/tao-snd-h-panel-a0eb`): `docs/papers/submit/`
