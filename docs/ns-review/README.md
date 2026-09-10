# NS / SND review docs

| Doc | Role |
| --- | --- |
| [`ARCHON-PANEL-ADVERSARIAL-VERDICT.md`](./ARCHON-PANEL-ADVERSARIAL-VERDICT.md) | Adversarial audit: Theorem H ≠ unconditional SND; Clay (B) not resolved |
| [`SND-TWEET-EQUATIONS.md`](./SND-TWEET-EQUATIONS.md) | Transcription of SND equations from Jonathan's June 2026 tweet one-pager |
| [`SND-TWEET-DA-AUDIT.md`](./SND-TWEET-DA-AUDIT.md) | Domain Architect exhaustive audit of tweet equations (Clay NOT closed) |
| [`DA-GAP-CLOSURE-PLAYBOOK.md`](./DA-GAP-CLOSURE-PLAYBOOK.md) | **Closer playbook:** Broken at X → close by Y; DA runtime refuse path |
| [`LEMMA-STAR-DA-NS-1.md`](./LEMMA-STAR-DA-NS-1.md) | **Lemma★ / DA-NS-1:** energy-budget Clay packaging; broken at PRODUCT-BLOCK |
| [`LEMMA-STAR-EXACT-FORMULAS.md`](./LEMMA-STAR-EXACT-FORMULAS.md) | Exact Fourier / \(\mathcal R_\star\) formulas (shape lock-in) |
| [`GROK-RETIRED-CONCLUSIONS.md`](./GROK-RETIRED-CONCLUSIONS.md) | **RETIRED:** “kill lane closed”; “amplitude/frequency shrinks the ratio” |
| [`ATTACK-8-RECORD.md`](./ATTACK-8-RECORD.md) | Revised Attack 8 = correct record; kill lane LIVE |
| [`ATTACK-9-COHERENT-PACKET-FAN.md`](./ATTACK-9-COHERENT-PACKET-FAN.md) | **Attack 9A** negative for kill; protocol + controls |
| [`ATTACK-9B-EXACT-SHELL-CLOSING.md`](./ATTACK-9B-EXACT-SHELL-CLOSING.md) | **Attack 9B** exact-shell + closing → \(K_{\alpha,\beta}\); runtime \(\max K\approx0.641\) **not** a kill; lane **LIVE** |
| [`ATTACK-9C-FIXED-GAP-SPHERES.md`](./ATTACK-9C-FIXED-GAP-SPHERES.md) | **Attack 9C** fixed-gap spheres: natural same-shell **not a kill** (\(0.11\to0.031\)) |
| [`ATTACK-9D-THETA-M2-LOCKED-PHASE.md`](./ATTACK-9D-THETA-M2-LOCKED-PHASE.md) | **Attack 9D** designed \(\Theta(m^2)\)-closure locked phases — remaining falsifier |
| [`ATTACK-9-FIXED-GAP-SPHERES.md`](./ATTACK-9-FIXED-GAP-SPHERES.md) | Legacy alias → **9C** fixed-gap (Θ(m²) was mislabeled 9C; now **9D**) |
| [`../math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md`](../math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md) | Five-lane canonical Attack 9B SoT twin |
| [`LEMMA-STAR-SIDE-ARCHIVE.md`](./LEMMA-STAR-SIDE-ARCHIVE.md) | LP-shell / Route N / Q6 / \(M=256\) floor — **not** ★ evidence |
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
