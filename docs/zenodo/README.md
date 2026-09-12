# Zenodo deposit remediation (September 2026)

Closes presentation and file mistakes on Jonathan R. Simons Zenodo deposits.

## Presentation rule

1. **Title** — scholarly title only (never ERRATA / WITHDRAWN / Superseded banners).
2. **Description top** — honest abstract / scope.
3. **Description bottom** — correction notice + pointer to status index `10.5281/zenodo.22050978`.

KEEP stays KEEP. PARK stays PARK. History is not deleted.

## Live audit (2026-09-12)

| Issue | Count | Status |
| --- | ---: | --- |
| Title banners still live | **0** | Already cleared on Zenodo (8 historical scarlet-letter titles cleaned) |
| PARK/REVIEW missing description errata | **23** | Pack + manual instructions ready; apply blocked without token |
| Title typo (trailing `"` on 20518388) | **1** | Clean title in pack |
| File fix 21071991 (`\dot H^{2.6}` → `\dot H^{1.3}`) | **1** | Corrected TeX+PDF packaged |

## Quick commands

```bash
# Refresh live inventory
python3 scripts/zenodo_inventory_live_fetch.py

# Live remediation audit
python3 scripts/zenodo_metadata_remediation.py audit

# Ensure PhiRenorm upload pack matches swirl SoT
python3 scripts/zenodo_metadata_remediation.py package-files

# Copy-paste instructions
python3 scripts/zenodo_metadata_remediation.py manual-instructions
# → also writes docs/zenodo/MANUAL-INSTRUCTIONS.md

# Regenerate per-deposit markdown
python3 scripts/zenodo_metadata_remediation.py write-docs
```

## Apply live (needs Jonathan's token)

```bash
export ZENODO_ACCESS_TOKEN='...'   # zenodo.org → Applications → Personal access tokens
                                   # scopes: deposit:write, deposit:actions
python3 scripts/zenodo_metadata_remediation.py apply
# or just the file fix:
python3 scripts/zenodo_metadata_remediation.py apply --record-id 21071991
```

Without a token, nothing is published to Zenodo from CI/agents. Use `MANUAL-INSTRUCTIONS.md`.

## Files

| Path | Role |
| --- | --- |
| `data/zenodo/deposit_metadata.json` | Canonical KEEP / PARK / REVIEW + live audit flags |
| `data/zenodo/upload_packs/21071991/` | Corrected PhiRenorm TeX+PDF |
| `deposits/*.md` | Per-record clean title + description HTML |
| `MANUAL-INSTRUCTIONS.md` | Exact copy-paste for remaining live fixes |
| `CORRECTION-INDEX-2026.md` | Public status index text |
| `../scripts/zenodo_metadata_remediation.py` | Audit / package / optional API apply |

## Honesty

- `21071991` remains **conditional** (`op:gronwall` / `||u^r/r||_∞` open).
- No Clay / RH proofs invented.
- No SFE→NS glue.
- Domain Architect FRA stays software KEEP (repo-only unless deposited later).
