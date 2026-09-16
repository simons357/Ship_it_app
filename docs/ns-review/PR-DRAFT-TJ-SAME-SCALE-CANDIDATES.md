# Draft PR — \(T_{j\leftarrow j}\) same-scale attack candidates

**Branch:** `cursor/tj-candidates-9083`  
**Base:** `main`  
**PR:** https://github.com/simons357/Ship_it_app/pull/102  
**Compare:** https://github.com/simons357/Ship_it_app/compare/main...cursor/tj-candidates-9083  

## Title

Same-scale Tj←j attack candidates — narrow + hard-run survivors

## Body

### Summary

Narrow-first candidate filter for same-scale \(T_{j\leftarrow j}\) / path to (A), then a **hard run** of the alive set only.

- `docs/ns-review/TJ-SAME-SCALE-CANDIDATES.md` (incl. §5 hard-run results)
- `scripts/ns_attacks/tj_same_scale_candidate_probes.py`
- `scripts/ns_attacks/tj_survivors_hard_run.py`
- `results/tj-survivors-hard-run/`

### Hard-run ranking (alive only; C1–C5 not revived)

| Verdict | IDs |
| --- | --- |
| **SURVIVES** | **C10** principal empty door; **C7** HH bottleneck; **C8** lab only |
| **WEAKENED** | C6 Door-3/α criterion; C11 \(T^{\mathrm{mm}}\) bulk target (axisym); C9 identity-only rewrite |
| **DEAD / BLOCKED** | C1–C5 (unchanged; not revived) |

**Best next theorem-shaped target:** non-circular \((\alpha_{\mathrm{loc},j})_+\) (or integrable) control feeding depletion ⇒ (A), without \(\dot e_j/\dot Z/\Lambda'\) and without Bernstein cubic wall.

### Honesty

- NS / Clay B **not** claimed — \(T_{j\leftarrow j}\) still **OPEN**
- Spectral-shift ≠ Lemma★
- No recycling \(\dot e_j / \dot Z / \Lambda'\)
- Numerics ≠ depletion / ≠ theorem

### Probe

```bash
python3 scripts/ns_attacks/tj_same_scale_candidate_probes.py
python3 scripts/ns_attacks/tj_survivors_hard_run.py
```
