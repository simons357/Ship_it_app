# NS review notes

Working notes for the axisymmetric-with-swirl / Φ-renorm book and adjacent NS packaging.

## Scientific face (preferred)

Strictly scientific package (no campaign / outreach framing):

- [`UNAUG-PROOF-CHAIN.md`](./UNAUG-PROOF-CHAIN.md) — locked unaugmented-face honesty / terminology (spectral-shift ≠ ★; \(T_{j\leftarrow j}\) **OPEN**; numerics ≠ depletion)
- [`TJ-SAME-SCALE-CANDIDATES.md`](./TJ-SAME-SCALE-CANDIDATES.md) — narrow-first attack shortlist for \(T_{j\leftarrow j}\) / (A); DEAD vs TRY; hard-run (§5) + harder-run (§6) + α₊ hinge (§7); NS / Clay B not solved, \(T_{j\leftarrow j}\) **OPEN**
- [`ALPHA-PLUS-DEPLETION.md`](./ALPHA-PLUS-DEPLETION.md) — C10 through C6: geometric/conditional \((\alpha_{\mathrm{loc},j})_+\) attack; CZ substitute killed as absolute; \([\alpha_\theta]\) conditional packaging
- [`PR-DRAFT-TJ-SAME-SCALE-CANDIDATES.md`](./PR-DRAFT-TJ-SAME-SCALE-CANDIDATES.md) — paste-ready title/body for [PR #102](https://github.com/simons357/Ship_it_app/pull/102) (branch `cursor/tj-candidates-9083`)
- [`PR-DRAFT-ALPHA-PLUS-DEPLETION.md`](./PR-DRAFT-ALPHA-PLUS-DEPLETION.md) — paste-ready draft for `cursor/alpha-plus-depletion-0cc5`
- [`SCIENTIFIC-REPORT.md`](./SCIENTIFIC-REPORT.md) — problem statement, objects, Lemma★ / PRODUCT-BLOCK status, proved vs hypothesized vs parked
- [`CREDIT-BODY-OF-WORK.md`](./CREDIT-BODY-OF-WORK.md) — KEEP shelf vs named open doors (no Clay claim)
- [`DA-AUDIT.md`](./DA-AUDIT.md) — Domain Architect check + language sanitize (CONDITIONAL PASS)
- [`METHOD-PANEL-REVIEW.md`](./METHOD-PANEL-REVIEW.md) — simulated method-seat review (not peer review; not real mathematicians)
- [`PROOF-CHAIN-CLEAN.md`](./PROOF-CHAIN-CLEAN.md) — definitions of \(T_c,\Lambda,X,Y,Z,E\); spectral-shift identity; Lemma★; open estimate (prefer SCIENTIFIC-REPORT §4 for live PRODUCT-BLOCK = uniform \(\mathcal{R}_\star\))

Reproducibility: [`scripts/ns_attacks/`](../../scripts/ns_attacks/). Same-scale probes: `python3 scripts/ns_attacks/tj_same_scale_candidate_probes.py` · hard run: `python3 scripts/ns_attacks/tj_survivors_hard_run.py` · harder run: `python3 scripts/ns_attacks/tj_survivors_harder_run.py` · α₊ hinge: `python3 scripts/ns_attacks/alpha_plus_depletion_probes.py`.

## Proof chain (visual + clean math)

- [`UNAUG-PROOF-CHAIN.md`](./UNAUG-PROOF-CHAIN.md) — honesty card for this face
- [`PROOF-CHAIN-CLEAN.md`](./PROOF-CHAIN-CLEAN.md) — math companion
- [`visual-journey/`](./visual-journey/) — Mermaid + PNG/SVG chain map, captions

**One-line:** OPEN at \(T_{j\leftarrow j}\) / PRODUCT-BLOCK. NS not claimed.

Campaign / outreach materials (if present under `docs/campaign/`) are **not** part of the scientific face.

## Φ-renorm (KEEP; conditional)

- [`PHI-RENORM-WHAT-IS-KEPT.md`](./PHI-RENORM-WHAT-IS-KEPT.md) — field-first KEEP / PARK card; separate from Lemma★.
- [`PHI-RENORM-AUDIT-2026-08-22.md`](./PHI-RENORM-AUDIT-2026-08-22.md) — independent 22 Aug 2026 audit of the June 30 swirl paper (\(\dot H^{2.6}\to\dot H^{1.3}\) relabel; barrier left open).
- TeX faces: [`docs/papers/swirl/`](../papers/swirl/).

**Open barrier (unchanged):** \(\|u^r/r\|_{L^\infty}\) uniform in \(\eps\) — equivalent in difficulty to axisymmetric-with-swirl global regularity. Paper remains a conditional reduction.

**Do not conflate** with Lemma★ PRODUCT-BLOCK packaging.
