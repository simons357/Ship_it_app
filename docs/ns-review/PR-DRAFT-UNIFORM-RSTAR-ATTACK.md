# Draft PR — uniform R_★ attack (PRODUCT-BLOCK still OPEN)

**Branch:** `cursor/uniform-rstar-attack-0cc5` → `main`  
**Status:** Draft. Scientific / honesty only.

## Summary

Locks Jonathan's research policy and focuses the live PRODUCT-BLOCK node: uniform \(\sup_v\mathcal{R}_\star(v)<\infty\).

- **Policy:** analytic structure / efficient math expression of truth — **not** an HPC/supercomputer arms race; light probes only as sanity checks
- Λ-relative HH/HL/LL split of \(T_c\) on the self-contained `ns_lemma_star_core` Field
- Lead route: \(T_c\) structure + Λ-relative HH channel reduction — **HH still open**
- Scientific status docs updated; **no Clay / NS closure claim**

## Honesty locks

- Lemma★ / DA-NS-1 = **HYPOTHESIS**
- PRODUCT-BLOCK / uniform R_★ = **still OPEN**
- Kill lane = **LIVE** unless a diverging family is found in the probe
- Do **not** revive false universal \(|T_c|\le C\|v\|_2 X^{3/2}\) (\(a^3\) vs \(a^4\))
- Numerics ≠ proof; probes subordinate to analysis

## Key paths

- `docs/ns-review/RESEARCH-POLICY.md`
- `docs/ns-review/UNIFORM-RSTAR-ATTACK.md`
- `scripts/ns_attacks/uniform_rstar_attack.py`
- `scripts/ns_attacks/ns_lemma_star_core.py`
- `docs/ns-review/SCIENTIFIC-REPORT.md` (§4.3)

## Reproduce

```bash
python3 scripts/ns_attacks/uniform_rstar_attack.py
python3 scripts/ns_attacks/uniform_rstar_attack.py --quick
```
