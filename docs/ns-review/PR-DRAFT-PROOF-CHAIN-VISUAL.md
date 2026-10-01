# PR draft — NS proof journey (visual + campaign)

**Branch:** `cursor/ns-proof-chain-visual-0cc5`  
**Base:** `main`

## Summary

Click-through proof journey for the whole body of work: campaign landing, reputation lock, notation glossary, expanded chain diagram (five-lane on the trunk; open nodes named as math objects), and clean math face. Experts read status from the chain. Campaign materials do **not** stamp solved / unsolved, and do not claim Clay closure.

## Deliverables

- `docs/campaign/PROOF-JOURNEY.md` — landing + chapters (PhiRenorm, Lemma★, five-lane, Q6, SND, DA, Zenodo KEEP, archive shelf)
- `docs/campaign/REPUTATION-LOCK.md` — mistakes OK if corrected under content; rep = full evidence + clean chain; barycenter = locus
- `docs/campaign/NOTATION-GLOSSARY.md` — symbol card + cleanup pointers
- `docs/campaign/journey-chain.mmd` — body-of-work Mermaid
- `docs/ns-review/PROOF-CHAIN-CLEAN.md` + `docs/ns-review/visual-journey/` — clean math + PNG/SVG chain
- Generator + tests: `scripts/visual_journey/generate_proof_chain_figures.py`, `tests/test_proof_chain_visual.py`

## Monday first click

`docs/ns-review/visual-journey/figures/proof-chain.png` — then barycenter `assets/lemma-star-barycenter.png`.

## Test plan

```bash
python3 scripts/visual_journey/generate_proof_chain_figures.py
python3 -m pytest -q tests/test_proof_chain_visual.py
```
