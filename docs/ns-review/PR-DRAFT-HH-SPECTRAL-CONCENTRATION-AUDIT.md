# Draft PR — HH / spectral-concentration screenshot audit

**Branch:** `cursor/hh-concentration-audit-4792` (from `cursor/tj-candidates-9083`)  
**Base:** `main` (or stack on #102 if preferred)  
**Related:** [PR #102](https://github.com/simons357/Ship_it_app/pull/102) (Tj←j candidates; honesty locks this audit uses)

---

## Suggested title

HH / spectral-concentration screenshot audit — C7/C12 diagnostics; refuse “closes Leray gap”

## Suggested body

### Summary

Audit of ~9 SuperGrok / ChatGPT / Base44 screenshots on spectral concentration, IPR / \(N_{\mathrm{eff},j}\), HH triad amplitude heuristics, and \(N=32\) “Lemma 5.3” numerics.

**Claim line:** NS / Clay B **not** solved. \(T_{j\leftarrow j}\) still **OPEN**. \(N=32\) probes ≠ proof.

### Files

- `docs/ns-review/HH-SPECTRAL-CONCENTRATION-AUDIT.md`
- `docs/ns-review/README.md` (index link)
- `docs/ns-review/PR-DRAFT-HH-SPECTRAL-CONCENTRATION-AUDIT.md`

### Verdict map (blunt)

| Item | Status |
| --- | --- |
| IPR / \(N_{\mathrm{eff}}\) / shell defs | **KEEP** diagnostic (C12 vocabulary) |
| \(A_\tau\sim(E/N_{\mathrm{eff}})^{3/2}\) as intuition | **KEEP** diagnostic (C7) |
| Same as absolute energy-only HH bound | **DEAD** (already killed \(\sim\lambda^{3/2}\)) |
| Cond. 1–3 / \(a_j\) as proved gate | **OVERCLAIM** |
| \(|I_{\mathrm{HH}}|\le C\sum 2^j E_j\) sketch | **TRY** target (C7); not proved here |
| ChatGPT “closes Leray gap / That’s the bridge” | **OVERCLAIM — REFUSE** |
| Base44 \(N=32\) \(\delta_{\mathrm{eff}}\gtrsim 2/3\), \(P_j\ge 139\) | **KEEP** probe only; cannot close Clay |
| Ring Lemma corrected TeX (2026-10-02) | **Not found** in this environment; existing SND/Ring stance unchanged (conditional C12) |

### What would still be needed (not supplied)

1. Prove SND / Lemma-5.3-type participation lower bound for the solution class (not one \(N=32\) run).  
2. Or prove geometric HH product into \(\theta\nu P_j+R_{\mathrm{allowed}}\) (C7→C10).  
3. Close \(T_{j\leftarrow j}\) / (A) without \(\dot e_j/\dot Z/\Lambda'\) (C10 still empty).

### Honesty

- Numerics ≠ depletion / ≠ theorem  
- C10 principal empty; C7 HH survives as bottleneck  
- C1–C5 / Sobolev-\(\alpha\) vs \(P_j\) / naive energy HH **not revived**

### Note on PR create

If GitHub `gh pr create` returns 403 in this environment, paste this title/body manually (same pattern as α₊ depletion draft).
