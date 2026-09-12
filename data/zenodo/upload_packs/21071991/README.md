# Upload pack — Zenodo record 21071991

**Disposition:** KEEP conditional (open `||u^r/r||_∞` / `op:gronwall`).

## Fix

Relabel energy / dual norms `\dot H^{2.6}` → `\dot H^{1.3}` (22 Aug 2026 audit).
Do **not** claim global regularity or Clay Statement (B).

## Files

| File | Role |
| --- | --- |
| `Simons_PhiRenorm_Swirl_2026-06-30.tex` | Corrected SoT TeX |
| `Simons_PhiRenorm_Swirl_2026-06-30.pdf` | Recompiled PDF with `\dot H^{1.3}` |

## Apply

```bash
export ZENODO_ACCESS_TOKEN=...
python3 scripts/zenodo_metadata_remediation.py apply --record-id 21071991
```

Or manually: New version on https://doi.org/10.5281/zenodo.21071991 →
replace both files → append description file-correction notice → publish.
