# NS review notes

Working notes for the axisymmetric-with-swirl / Φ-renorm book and adjacent NS packaging.

## Scientific face (preferred)

Strictly scientific package (no campaign / outreach framing):

- [`SCIENTIFIC-REPORT.md`](./SCIENTIFIC-REPORT.md) — problem statement, objects, Lemma★ / PRODUCT-BLOCK status, proved vs hypothesized vs parked
- [`RESEARCH-POLICY.md`](./RESEARCH-POLICY.md) — locked policy: analytic main path; no HPC arms race; live target \(\sup\mathcal{R}_\star<\infty\) (**OPEN**; no Clay)
- [`UNIFORM-RSTAR-ATTACK.md`](./UNIFORM-RSTAR-ATTACK.md) — Λ-relative HH/HL/LL reduction map + light numeric maximizer / kill-lane status (**uniform \(\mathcal{R}_\star\) still OPEN**)
- [`UNIFORM-RSTAR-PROGRESS.md`](./UNIFORM-RSTAR-PROGRESS.md) — close-attempt lemmas (Cauchy / channels / two-shell \(D_s\)); HL/LL **not** classical; no kill
- [`DA-AUDIT.md`](./DA-AUDIT.md) — Domain Architect check + language sanitize (CONDITIONAL PASS)
- [`METHOD-PANEL-REVIEW.md`](./METHOD-PANEL-REVIEW.md) — simulated method-seat review (not peer review; not real mathematicians)
- [`PROOF-CHAIN-CLEAN.md`](./PROOF-CHAIN-CLEAN.md) — definitions of \(T_c,\Lambda,X,Y,Z,E\); Lemma★; open estimate (prefer SCIENTIFIC-REPORT §4 for live PRODUCT-BLOCK = uniform \(\mathcal{R}_\star\))

Reproducibility: [`scripts/ns_attacks/`](../../scripts/ns_attacks/) — start with `uniform_rstar_attack.py` + `ns_lemma_star_core.py`.

## Proof chain (visual + clean math)

- [`PROOF-CHAIN-CLEAN.md`](./PROOF-CHAIN-CLEAN.md) — math companion
- [`visual-journey/`](./visual-journey/) — Mermaid + PNG/SVG chain map, captions

Campaign / outreach materials (if present under `docs/campaign/`) are **not** part of the scientific face.

## Φ-renorm (KEEP; conditional)

- [`PHI-RENORM-WHAT-IS-KEPT.md`](./PHI-RENORM-WHAT-IS-KEPT.md) — field-first KEEP / PARK card; separate from Lemma★.
- [`PHI-RENORM-AUDIT-2026-08-22.md`](./PHI-RENORM-AUDIT-2026-08-22.md) — independent 22 Aug 2026 audit of the June 30 swirl paper (\(\dot H^{2.6}\to\dot H^{1.3}\) relabel; barrier left open).
- TeX faces: [`docs/papers/swirl/`](../papers/swirl/).

**Open barrier (unchanged):** \(\|u^r/r\|_{L^\infty}\) uniform in \(\eps\) — equivalent in difficulty to axisymmetric-with-swirl global regularity. Paper remains a conditional reduction.

**Do not conflate** with Lemma★ PRODUCT-BLOCK packaging.
