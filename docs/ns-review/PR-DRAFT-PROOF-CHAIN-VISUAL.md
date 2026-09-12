# PR draft — NS proof-chain visual journey

**Branch:** `cursor/ns-proof-chain-visual-0cc5`  
**Base:** `main`

## Summary

Public face for the Navier–Stokes packaging: a visual proof-chain journey with clean math. Experts read the chain; node colors carry status. Campaign materials do **not** stamp solved / unsolved.

## Deliverables

- `docs/ns-review/PROOF-CHAIN-CLEAN.md` — superior exposition (\(T_c,\Lambda,X,Y,Z,E\), Lemma★, product needs)
- `docs/ns-review/visual-journey/` — Mermaid + PNG/SVG chain map, chain-status card, captions, reused barycenter/shell figures
- `docs/campaign/visual-journey/` — campaign pointer
- Optional one-pager PDF: `docs/ns-review/visual-journey/proof-chain-onepager.pdf`
- Generator + tests: `scripts/visual_journey/generate_proof_chain_figures.py`, `tests/test_proof_chain_visual.py`

## Math cleaned

- Notation aligned across Lemma★ / Φ-renorm / SND texture
- \(\dot H^{1.3}\) relabel visible on the Φ branch
- Open nodes labeled **open estimate** (not FAILED / ERRATA)
- Theater / biography framing kept out of this pack

## Monday visual

Post first: `docs/ns-review/visual-journey/figures/proof-chain.png`

## Test plan

```bash
python3 scripts/visual_journey/generate_proof_chain_figures.py
python3 -m pytest -q tests/test_proof_chain_visual.py
```
