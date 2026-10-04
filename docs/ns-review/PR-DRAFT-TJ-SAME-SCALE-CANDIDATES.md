# Draft PR — \(T_{j\leftarrow j}\) same-scale attack candidates

**Branch:** `cursor/tj-candidates-9083`  
**Base:** `main`  
**PR:** https://github.com/simons357/Ship_it_app/pull/102  
**Compare:** https://github.com/simons357/Ship_it_app/compare/main...cursor/tj-candidates-9083  
**Tip (verify):** `ea66bd05` (includes hard-run `3fbf3b0` + harder-run)

> **PR title/body update status:** `gh` integration returns 403 on `updatePullRequest`; ManagePullRequest tool is **not** available in this agent run. Paste the Title + Body below into the GitHub PR UI if the dashboard sync does not apply them.

## Title

Same-scale Tj←j attack candidates — narrow + hard-run survivors

## Body (paste below this line)

### Summary

Narrow-first candidate filter for same-scale \(T_{j\leftarrow j}\) / path to (A), then hard-run (2026-09-16) and harder second pass (2026-10-01) of the **alive set only** (C1–C5 not revived).

**Claim line:** NS / Clay B **not** solved. \(T_{j\leftarrow j}\) still **OPEN**.

### Files

- `docs/ns-review/TJ-SAME-SCALE-CANDIDATES.md` (§5 hard-run, §6 harder-run)
- `scripts/ns_attacks/tj_same_scale_candidate_probes.py`
- `scripts/ns_attacks/tj_survivors_hard_run.py`
- `scripts/ns_attacks/tj_survivors_harder_run.py`
- `results/tj-survivors-hard-run/` · `results/tj-survivors-harder-run/`
- Artifacts: `/opt/cursor/artifacts/tj-survivors-hard-run/` · `/opt/cursor/artifacts/tj-survivors-harder-run/`

### Hard-run blunt ranking (2026-09-16; alive only)

| Rank | ID | Verdict | Note |
| --- | --- | --- | --- |
| 1 | **C10** | **SURVIVES** | Principal door empty; sketches collapse onto C6 / C11 / C8 |
| 2 | **C7** | **SURVIVES** | HH bottleneck live; naive energy-only HH product killed (\(\sim\lambda^{3/2}\)) |
| 3 | **C8** | **SURVIVES** *(lab)* | Near-shell + light 9B finite; not a depletion theorem |
| 4 | **C6** | **WEAKENED** | \(\alpha_+ Z\) sharp for stretch; escapes energy \(R\) and Bernstein wall → Door-3 criterion only |
| 5 | **C11** | **WEAKENED** | \(T^{\mathrm{mm}}\) bulk named; energy-\(R\) / 2D-transfer myths dead |
| 6 | **C9** | **WEAKENED** | \(\omega_*\) invariance → rewrite only; standalone bound dead |

### Harder-run ranking (2026-10-01; C1–C5 not revived)

| Verdict | IDs |
| --- | --- |
| **SURVIVES** | **C10** principal (false shortcuts killed); **C7** HH bottleneck |
| **SURVIVES lab / WEAKENED feeder** | **C8** ★ lab only; category gap vs shell (A) |
| **WEAKENED** | C6 further (\(\alpha\) escapes \(\nu P\)); C11 (\(\Phi\neq T^{\mathrm{mm}}\)); C9 non-feeder |
| **DEAD / BLOCKED** | C1–C5 (unchanged; not revived) |

**NEW kills/weakens (harder pass):** Sobolev-\(\alpha\) vs \(P_j\); CZ/Biot–Savart pointwise; \(\Phi\)-as-depletion; BKM-as-shortcut (refuse); Agmon HH; Bernstein no absorption margin; C8 as C10 feeder (category gap).

### Best next theorem-shaped target

Prove **depletion ⇒ (A)** by controlling \((\alpha_{\mathrm{loc},j})_+\) (or an integrable substitute) so stretch enters \(\theta\nu P_j + R_{\mathrm{allowed}}\), without \(\dot e_j/\dot Z/\Lambda'\) and without the Bernstein cubic wall. That is **C10 through the honest C6 hinge**. Absolute Sobolev control by \(P_j\) is false (\(\lambda^{1/2}\)). No BKM / near-shell-sample shortcuts.

### Honesty

- NS / Clay B **not** claimed — \(T_{j\leftarrow j}\) still **OPEN**
- Spectral-shift ≠ Lemma★
- No recycling \(\dot e_j / \dot Z / \Lambda'\)
- Numerics ≠ depletion / ≠ theorem

### Probe

    python3 scripts/ns_attacks/tj_same_scale_candidate_probes.py
    python3 scripts/ns_attacks/tj_survivors_hard_run.py
    python3 scripts/ns_attacks/tj_survivors_harder_run.py
