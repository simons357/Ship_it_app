# Draft PR — \(T_{j\leftarrow j}\) same-scale attack candidates

**Branch:** `cursor/tj-candidates-9083`  
**Base:** `main`  
**PR:** https://github.com/simons357/Ship_it_app/pull/102  
**Compare:** https://github.com/simons357/Ship_it_app/compare/main...cursor/tj-candidates-9083  

## Title

Same-scale Tj←j attack candidates — narrow + hard-run survivors

## Body

### Summary

Narrow-first candidate filter for same-scale \(T_{j\leftarrow j}\) / path to (A), then hard-run (2026-09-16) and **harder second pass** (2026-10-01) of the alive set only.

- `docs/ns-review/TJ-SAME-SCALE-CANDIDATES.md` (§5 hard-run, §6 harder-run)
- `scripts/ns_attacks/tj_same_scale_candidate_probes.py`
- `scripts/ns_attacks/tj_survivors_hard_run.py`
- `scripts/ns_attacks/tj_survivors_harder_run.py`
- `results/tj-survivors-hard-run/` · `results/tj-survivors-harder-run/`

### Harder-run ranking (2026-10-01; C1–C5 not revived)

| Verdict | IDs |
| --- | --- |
| **SURVIVES** | **C10** principal (false shortcuts killed); **C7** HH bottleneck |
| **SURVIVES lab / WEAKENED feeder** | **C8** ★ lab only; category gap vs shell (A) |
| **WEAKENED** | C6 further (α escapes νP); C11 (Φ≠T^mm); C9 non-feeder |
| **DEAD / BLOCKED** | C1–C5 (unchanged; not revived) |

**NEW kills/weakens:** Sobolev-α vs \(P_j\); CZ/Biot–Savart pointwise; Φ-as-depletion; BKM-as-shortcut (refuse); Agmon HH; Bernstein no absorption margin; C8 as C10 feeder (category gap).

**Best next theorem-shaped target:** geometric or explicitly conditional \((\alpha_{\mathrm{loc},j})_+\) bound feeding depletion ⇒ (A), without \(\dot e_j/\dot Z/\Lambda'\), without Bernstein cubic wall, without BKM/\★-sample shortcuts. Absolute Sobolev control by \(P_j\) is false (\(\lambda^{1/2}\)).

### Honesty

- NS / Clay B **not** claimed — \(T_{j\leftarrow j}\) still **OPEN**
- Spectral-shift ≠ Lemma★
- No recycling \(\dot e_j / \dot Z / \Lambda'\)
- Numerics ≠ depletion / ≠ theorem

### Probe

```bash
python3 scripts/ns_attacks/tj_same_scale_candidate_probes.py
python3 scripts/ns_attacks/tj_survivors_hard_run.py
python3 scripts/ns_attacks/tj_survivors_harder_run.py
```
