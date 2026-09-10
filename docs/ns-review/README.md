# NS / SND review docs

| Doc | Role |
| --- | --- |
| [`ARCHON-PANEL-ADVERSARIAL-VERDICT.md`](./ARCHON-PANEL-ADVERSARIAL-VERDICT.md) | Adversarial audit: Theorem H ≠ unconditional SND; Clay (B) not resolved |
| [`SND-TWEET-EQUATIONS.md`](./SND-TWEET-EQUATIONS.md) | Transcription of SND equations from Jonathan's June 2026 tweet one-pager |
| [`SND-TWEET-DA-AUDIT.md`](./SND-TWEET-DA-AUDIT.md) | Domain Architect exhaustive audit of tweet equations (Clay NOT closed) |
| [`DA-GAP-CLOSURE-PLAYBOOK.md`](./DA-GAP-CLOSURE-PLAYBOOK.md) | **Closer playbook:** Broken at X → close by Y; DA runtime refuse path |
| [`LEMMA-STAR-ACTUAL-SHAPE.md`](./LEMMA-STAR-ACTUAL-SHAPE.md) | **Canonical shape ★** / \(\mathcal{R}_\star\) claim box — **OPEN**; NS not solved |
| [`PROOF_LemmaStar_LIVE_LOCK.md`](./PROOF_LemmaStar_LIVE_LOCK.md) | **LIVE** kill/proof-lane lock (Attack 8 / 9A–9D) |
| [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md) | Annotated **archive** of older proof attempt — does **not** green ★ |
| [`LEMMA-STAR-DA-NS-1.md`](./LEMMA-STAR-DA-NS-1.md) | **Lemma★ / DA-NS-1:** energy-budget Clay packaging; live gap is uniform \(\mathcal{R}_\star\) / HH→L (discarded \(X^{3/2}\) route) |
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
