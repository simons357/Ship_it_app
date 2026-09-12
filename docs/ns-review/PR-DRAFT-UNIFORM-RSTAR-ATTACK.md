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
python3 -m pytest -q tests/test_uniform_rstar_attack.py
```

## Probe snapshot (not a proof)

- max R_★ ≈ 4.5e-2 (quick) / 1.9e-2 (full) on triad/near-shell samples
- kill_found = False; kill lane LIVE
- channel-sum error ≲ 1e-14
- false X^{3/2} product scales as 1/a (ratio max/min = 32 on a∈[1/4,8]); R_★ flat
- **PRODUCT-BLOCK still OPEN**
