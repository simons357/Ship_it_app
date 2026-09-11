# NS / SND review docs

| Doc | Role |
| --- | --- |
| [`ARCHON-PANEL-ADVERSARIAL-VERDICT.md`](./ARCHON-PANEL-ADVERSARIAL-VERDICT.md) | Adversarial audit: Theorem H ≠ unconditional SND; Clay (B) not resolved |
| [`SND-TWEET-EQUATIONS.md`](./SND-TWEET-EQUATIONS.md) | Transcription of SND equations from Jonathan's June 2026 tweet one-pager |
| [`SND-TWEET-DA-AUDIT.md`](./SND-TWEET-DA-AUDIT.md) | Domain Architect exhaustive audit of tweet equations (Clay NOT closed) |
| [`DA-GAP-CLOSURE-PLAYBOOK.md`](./DA-GAP-CLOSURE-PLAYBOOK.md) | **Closer playbook:** Broken at X → close by Y; DA runtime refuse path |
| [`LEMMA-STAR-DA-NS-1.md`](./LEMMA-STAR-DA-NS-1.md) | **Lemma★ / DA-NS-1:** energy-budget Clay packaging; broken at PRODUCT-BLOCK |
| [`LEMMA-STAR-CAMPAIGN-PAPER.md`](./LEMMA-STAR-CAMPAIGN-PAPER.md) | **Paper/post-ready:** Lemma★ campaign writeup (★ not proved; door locked) |
| [`LEMMA-STAR-X-THREAD.md`](./LEMMA-STAR-X-THREAD.md) | Paste-ready X thread (classy, honest) |
| [`LEMMA-STAR-FOR-X.md`](./LEMMA-STAR-FOR-X.md) | Short outline for posts |
| [`LEMMA-STAR-IN-ENGLISH.md`](./LEMMA-STAR-IN-ENGLISH.md) | Plain-English barycenter narrative |
| [`assets/lemma-campaign/`](./assets/lemma-campaign/) | Campaign figures + image inventory |
| [`THEOREM-H-ATTACK-PLAN.md`](./THEOREM-H-ATTACK-PLAN.md) | Analytic attack routes on the \(X\le M\) gap (bootstrap first) |
| [`COMPETITIVE-POSITION-2026.md`](./COMPETITIVE-POSITION-2026.md) | One-page honest race card |
| [`PR-DRAFT-COMPETITIVE-PACKAGE.md`](./PR-DRAFT-COMPETITIVE-PACKAGE.md) | Pasteable draft PR body (token cannot open PRs) |

**Inventory / tooling:** `data/domain_architect/snd_claim_inventory.json`, `domain_architect/snd_claims.py`, `domain_architect/gap_closure.py`

**Probe (not a proof):** `scripts/ns_snd_honest_probe.py` — see `scripts/README-ns-snd-probe.md`

**Runtime:**

```bash
python3 -m domain_architect --gap-closure '…claim…'
python3 -m domain_architect --snd-dual
python3 scripts/da_ns_gap_closure_demo.py
python3 scripts/ns_snd_honest_probe.py --out /tmp/ns_snd_probe.json
```
