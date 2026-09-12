# Draft PR — Zenodo deposit fixes

**Branch:** `cursor/zenodo-deposit-fixes-0cc5`  
**Base:** `main`  
**Compare:** https://github.com/simons357/Ship_it_app/compare/main...cursor/zenodo-deposit-fixes-0cc5

## Title

Fix Zenodo deposit presentation + PhiRenorm file pack (21071991)

## Body

### Summary
- Live audit of all Jonathan-owned Zenodo records vs corrected inventory.
- Title banners already cleared live (0 remaining); refresh metadata so we stop claiming banners are still present.
- Package description errata HTML for 23 PARK/REVIEW deposits + trailing-quote title fix for `20518388`.
- Rebuild PhiRenorm June 30 PDF with `\dot H^{1.3}` and ship upload pack for `21071991` (conditional KEEP; barrier open).

### Live apply
Blocked in this environment (no Zenodo token). Jonathan:

```bash
export ZENODO_ACCESS_TOKEN='...'
python3 scripts/zenodo_metadata_remediation.py apply
```

### Test plan
- [x] `python3 -m unittest tests.test_zenodo_metadata_remediation tests.test_phi_renorm_audit -v`
- [x] `python3 scripts/zenodo_metadata_remediation.py audit`
- [x] `python3 scripts/zenodo_metadata_remediation.py package-files`
