# Draft PR — Phi-renorm 22 Aug 2026 audit fix

**Branch:** `cursor/phi-renorm-audit-fix-0cc5`  
**Base:** `main`  
**Compare:** https://github.com/simons357/Ship_it_app/compare/main...cursor/phi-renorm-audit-fix-0cc5

> Note: `gh pr create` returned 403 (integration cannot create PRs). Open the compare link above as a draft PR, or let the Cloud Agent PR automation pick up the branch.

## Title

Apply 22 Aug 2026 Phi-renorm audit (Hdot relabel; barrier open)

## Body

### Summary

- Deposit June 30 Phi-renorm swirl SoT TeX with independent 22 Aug 2026 audit applied: \(\dot H^{2.6}\to\dot H^{1.3}\) at audited energy/duality sites.
- `lem:Phieq`, Lions \(\beta=0.6\), and `op:gronwall` left intact. Conditional reduction only — not Clay.
- Optional \(r^3\) rewrite deferred on June 30; Aug 22 companion included.
- Audit summary + DA NS-Φ KEEP wiring + regression tests.

### Honesty lock

★ NOT proved · NS NOT solved · open condition = \(\|u^r/r\|_\infty\) uniform in \(\eps\).

### Test plan

- [x] `python3 -m unittest tests.test_phi_renorm_audit -v`
- [x] Audit line sites verified \(\dot H^{1.3}\)
- [x] `op:gronwall` / `lem:Phieq` present
