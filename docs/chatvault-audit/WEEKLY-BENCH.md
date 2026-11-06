# ChatVault weekly search bench

**At:** 2026-11-06T10:12:52.033Z
**Engine:** chatvault-hybrid-0.2.0
**Result:** PASS — nDCG 1.000 · MRR 1.000 · 11.6 ms mean

| Case | Query | Top hit | nDCG@5 | MRR | ms | Hit |
| --- | --- | --- | --- | --- | --- | --- |
| euler-and | `euler identity` | Euler identity as a definitional fact | 1.00 | 1.00 | 20.4 | yes |
| phrase-blowup | `"finite-time blow-up"` | Spectral regularity for Navier–Stokes — status of the claim | 1.00 | 1.00 | 14.4 | yes |
| claim-field | `claim:definitional` | Euler identity as a definitional fact | 1.00 | 1.00 | 8.2 | yes |
| gap-field | `gap:blow-up` | Spectral regularity for Navier–Stokes — status of the claim | 1.00 | 1.00 | 7.2 | yes |
| ai-claude | `ai:Claude` | Spectral regularity for Navier–Stokes — status of the claim | 1.00 | 1.00 | 12.1 | yes |
| or-query | `euler OR navier-stokes` | Euler identity as a definitional fact | 1.00 | 1.00 | 7.4 | yes |

Fixture corpus only. A pass here is not a pass on Jonathan’s live chats.
Memory/context boost is not in this number. Ranker regressions cannot hide behind memory.
