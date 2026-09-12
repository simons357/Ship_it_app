# Draft PR — uniform R_★ attack (PRODUCT-BLOCK still OPEN)

**Branch:** `cursor/uniform-rstar-attack-0cc5` → `main`  
**Related push:** `cursor/uniform-rstar-dilation-00ef` (dilation ledger + credit pack)  
**Status:** Scientific / honesty only. **No Clay claim.**

## Summary

Analytic attack on Lemma★ / PRODUCT-BLOCK (uniform \(\mathcal{R}_\star\)), plus a credit / body-of-work face for Jonathan R. Simons.

### Verdict

**STILL OPEN** — not closed, not killed. No Clay / Statement B claim. Publisher/X “clean proof” **not** offered.

### What is proved (algebra / packaging)

- Cauchy form: \(|T_c|\le\sqrt{D_s}\,\|A^{1/2}B\|_2\) ⇒ sufficient target \(\|A^{1/2}B\|_2^2\le C\,E\,Y\)
- Exact Λ-relative split \(T_c=T_c^{\mathrm{HH}}+T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}}\)
- Two-shell formula for \(D_s\); amplitude / lattice-dilation invariance of \(\mathcal{R}_\star\) and of \(Q=\|A^{1/2}B\|_2^2/(EY)\)
- Dilation ledger + two-shell channel dichotomy + signed Stokes weights (Lemmas G–J)
- Elementary unmatched-Λ HL/LL route **killed** (dilation obstruction)
- False universal \(|T_c|\le C\|v\|_2 X^{3/2}\) discarded

### What remains open

Geometric HL/LL and HH bounds (geometry-only constants). Conditional close only if both hold.

### Credit / show-work

- `docs/ns-review/CREDIT-BODY-OF-WORK.md` — KEEP shelf vs open door
- `docs/campaign/TWO-YEARS-MAP.md` — campaign-safe map of two years’ work

## Honesty locks

- Lemma★ / DA-NS-1 = **HYPOTHESIS**
- PRODUCT-BLOCK / uniform R_★ = **still OPEN**
- Kill lane = **LIVE** unless a diverging family is found
- Do **not** revive false universal \(|T_c|\le C\|v\|_2 X^{3/2}\)
- Numerics ≠ proof; probes subordinate to analysis
- Zero lab shade; credit for mapped work

## Key paths

- `docs/ns-review/RESEARCH-POLICY.md`
- `docs/ns-review/UNIFORM-RSTAR-ATTACK.md`
- `docs/ns-review/UNIFORM-RSTAR-PROGRESS.md`
- `docs/ns-review/CREDIT-BODY-OF-WORK.md`
- `scripts/ns_attacks/uniform_rstar_dilation.py`
- `scripts/ns_attacks/uniform_rstar_attack.py`
- `scripts/ns_attacks/ns_lemma_star_core.py`

## Reproduce

```bash
python3 scripts/ns_attacks/uniform_rstar_identities.py
python3 scripts/ns_attacks/uniform_rstar_dilation.py
python3 scripts/ns_attacks/uniform_rstar_attack.py --quick
python3 -m pytest -q tests/test_uniform_rstar_attack.py tests/test_uniform_rstar_dilation.py
```

## Probe snapshot (not a proof)

- Dilation: R_★ and Q invariant to ~1e-15; naive ρ=Λ^{1/2}X/Y scales as 1/n
- Two-shell dichotomy + signed weights: ok
- max R_★ on prior maximizer samples ≲ 4.5e-2; kill_found = False
- **PRODUCT-BLOCK still OPEN**
