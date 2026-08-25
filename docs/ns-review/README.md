# NS / SND review docs

| Doc | Role |
| --- | --- |
| [`ARCHON-PANEL-ADVERSARIAL-VERDICT.md`](./ARCHON-PANEL-ADVERSARIAL-VERDICT.md) | Adversarial audit: Theorem H ≠ unconditional SND; Clay (B) not resolved |
| [`DA-GAP-CLOSURE-PLAYBOOK.md`](./DA-GAP-CLOSURE-PLAYBOOK.md) | **Closer playbook:** Broken at X → close by Y; DA runtime refuse path |
| [`THEOREM-H-ATTACK-PLAN.md`](./THEOREM-H-ATTACK-PLAN.md) | Analytic attack routes on the \(X\le M\) gap (bootstrap first) |
| [`COMPETITIVE-POSITION-2026.md`](./COMPETITIVE-POSITION-2026.md) | One-page honest race card |

**Runtime:**

```bash
python3 -m domain_architect --gap-closure '…claim…'
python3 -m domain_architect --snd-dual
python3 scripts/da_ns_gap_closure_demo.py
```
