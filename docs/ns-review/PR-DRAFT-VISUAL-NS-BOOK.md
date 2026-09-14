# PR draft — Visual NS Book + scientific work-list

**Branch:** `cursor/visual-ns-book-0cc5`  
**Base:** `main`  
**Compare:** https://github.com/simons357/Ship_it_app/compare/main...cursor/visual-ns-book-0cc5

## Title

Visual NS Book (Skool+Substack) + scientific work-list honesty

## Body

### Summary

Two deliverables on one branch for Jonathan Simons:

**Part A — Scientific report.** `docs/ns-review/SCIENTIFIC-REPORT.md` gains §9 “What can still be worked on”: PRODUCT-BLOCK / uniform \(\mathcal{R}_\star\) still OPEN with remaining routes (HH, HL/LL dilation-invariant, kill search); settled items (identities, false \(X^{3/2}\), spectral-shift ≠ ★); will-not-resolve-soon (Clay-by-Monday); NS not solved.

**Part B — Visual book.** New curriculum at `docs/campaign/VISUAL-NS-BOOK/`: README (Skool short vs Substack long), lesson sequence, image inventory reusing lemma-campaign + proof-chain figures, Week-1 posting pack, ten chapter cards. Tone: host/guide, house-as-map, no break-in / shade / trophy.

**Explicit:** the visual book is **education / map, not a proof**.

### Test plan

```bash
test -f docs/campaign/VISUAL-NS-BOOK/README.md
test -f docs/ns-review/assets/lemma-campaign/lemma-star-barycenter.png
test -f docs/ns-review/visual-journey/figures/proof-chain.png
rg -n 'not solved|OPEN|HYPOTHESIS|education / map' docs/campaign/VISUAL-NS-BOOK/README.md docs/ns-review/SCIENTIFIC-REPORT.md
rg -n 'Clay closed|we broke in|trophy|OpenAI' docs/campaign/VISUAL-NS-BOOK/ || true
```
