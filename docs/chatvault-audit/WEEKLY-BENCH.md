# ChatVault weekly search bench

**At:** 2026-11-09T14:00:32.724Z (Monday 9 Nov 2026, 9:00 AM Eastern)
**Engine:** chatvault-hybrid-0.2.0
**Result:** PASS — nDCG 1.000 (was 1.000) · MRR 1.000 (was 1.000) · 12.3 ms (was 11.6)
**Vs 6 Nov 2026:** Quality unchanged. All six gated cases still hit. Mean latency +0.7 ms is machine noise, not a ranker change. Engine version did not move. Display-only atlas HUD / ledger spectrum / latency-sim UI are not in this number.

| Case | Query | Top hit | nDCG@5 | MRR | ms | Hit |
| --- | --- | --- | --- | --- | --- | --- |
| euler-and | `euler identity` | Euler identity as a definitional fact | 1.00 | 1.00 | 21.9 | yes |
| phrase-blowup | `"finite-time blow-up"` | Spectral regularity for Navier–Stokes — status of the claim | 1.00 | 1.00 | 16.0 | yes |
| claim-field | `claim:definitional` | Euler identity as a definitional fact | 1.00 | 1.00 | 8.0 | yes |
| gap-field | `gap:blow-up` | Spectral regularity for Navier–Stokes — status of the claim | 1.00 | 1.00 | 7.3 | yes |
| ai-claude | `ai:Claude` | Spectral regularity for Navier–Stokes — status of the claim | 1.00 | 1.00 | 12.6 | yes |
| or-query | `euler OR navier-stokes` | Euler identity as a definitional fact | 1.00 | 1.00 | 8.0 | yes |

Fixture corpus only. A pass here is not a pass on Jonathan’s live chats.
Memory/context boost is not in this number. Ranker regressions cannot hide behind memory.
