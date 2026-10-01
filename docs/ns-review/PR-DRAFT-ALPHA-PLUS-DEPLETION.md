# Draft PR — \(\alpha_+\) depletion ⇒ (A) (C10 / C6 hinge)

**Branch:** `cursor/alpha-plus-depletion-0cc5`  
**Base:** `main` (tip ancestry: `cursor/tj-candidates-9083` / [PR #102](https://github.com/simons357/Ship_it_app/pull/102))  
**Compare:** https://github.com/simons357/Ship_it_app/compare/main...cursor/alpha-plus-depletion-0cc5  

> **PR create/update status:** `gh` integration returns 403; ManagePullRequest tool is **not** available in this agent run. Paste Title + Body below into GitHub if dashboard sync does not open/update a PR. Prefer updating PR #102 or opening a new PR from this branch.

## Title

α₊ depletion ⇒ (A): C10 through C6 hinge (conditional packaging)

## Body (paste below this line)

### Summary

Analytic attack on the hard-run target from [PR #102](https://github.com/simons357/Ship_it_app/pull/102): prove depletion ⇒ (A) by controlling \((\alpha_{\mathrm{loc},j})_+\) (or an integrable substitute) so stretch enters \(\theta\nu D_j+R_{\mathrm{allowed}}\), without \(\dot e_j/\dot Z/\Lambda'\) and without Bernstein cubic wall.

**Blunt verdict:** **OPEN** (absolute). **CONDITIONAL** best seated statement under explicit \([\alpha_\theta]\). NS / Clay B **not** solved. \(T_{j\leftarrow j}\) still **OPEN**.

### Files

- `docs/ns-review/ALPHA-PLUS-DEPLETION.md` — proved vs open; axisym labels
- `docs/ns-review/TJ-SAME-SCALE-CANDIDATES.md` (§7 α₊ attack)
- `scripts/ns_attacks/alpha_plus_depletion_probes.py`
- `results/alpha-plus-depletion/`

### What sits / what dies

| Item | Status |
| --- | --- |
| TJJ-Trans / TJJ-α / template identities | **PROVED** (already seated) |
| CZ–Sobolev substitute \(\lesssim Z^{3/4}D^{3/4}\le\varepsilon D+C_\varepsilon Z^3\) | **STANDARD sketch**; **KILLED as absolute (A)** (cubic + \(\lambda^{1/2}\)) |
| \([\alpha_\theta]\) ⇒ main stretch enters (A) | **CONDITIONAL PROVED** (packaging) |
| Dynamics ⇒ \([\alpha_\theta]\); geometric CF \([G_\delta]\) | **OPEN / ABSENT** |
| Axisym mixed \(\alpha^{\mathrm{mm}}\) | **OPEN** *(axisym-conditional)* |
| Commutators → \(R_{\mathrm{allowed}}\) | **OPEN** |

**Not revived:** C1–C5; Sobolev-\(\alpha\) vs \(P_j\); CZ pointwise; Φ-as-depletion; BKM shortcut; naive energy HH.

### Best statement achieved

Under explicit hypothesis \([\alpha_\theta]\) (positive local stretch \(\le\theta\nu D_j+R_{\mathrm{allowed}}\)), the main-stretch piece of \(T_{j\leftarrow j}\) enters (A). The CZ integrable substitute removes \(\|a_+\|_\infty\) but hits the classical cubic wall and the same \(\lambda^{1/2}\) concentration escape — not an unaugmented close.

### Honesty

- NS / Clay B **not** claimed
- Spectral-shift ≠ Lemma★
- No recycling \(\dot e_j/\dot Z/\Lambda'\)
- Numerics / ledgers ≠ theorems
- Axisym-conditional results labeled

### Probe

```bash
python3 scripts/ns_attacks/alpha_plus_depletion_probes.py
```
