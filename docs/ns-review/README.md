# NS review notes

Working notes for the axisymmetric-with-swirl / Φ-renorm book and adjacent NS packaging.

## Scientific face (preferred)

Strictly scientific package (no campaign / outreach framing):

- [`UNAUG-PROOF-CHAIN.md`](./UNAUG-PROOF-CHAIN.md) — locked unaugmented-face honesty / terminology (spectral-shift ≠ ★; \(T_{j\leftarrow j}\) **OPEN**; numerics ≠ depletion)
- [`TJ-SAME-SCALE-CANDIDATES.md`](./TJ-SAME-SCALE-CANDIDATES.md) — narrow-first attack shortlist for \(T_{j\leftarrow j}\) / (A); DEAD vs TRY; hard-run (§5) + harder-run (§6); NS / Clay B not solved, \(T_{j\leftarrow j}\) **OPEN**
- [`HH-SPECTRAL-CONCENTRATION-AUDIT.md`](./HH-SPECTRAL-CONCENTRATION-AUDIT.md) — screenshot audit (IPR / \(N_{\mathrm{eff}}\) / HH triad heuristics / \(N=32\) Lemma 5.3 probes); ChatGPT “closes Leray gap” **OVERCLAIM refuse**; maps to C7/C10/C12
- [`PR-DRAFT-TJ-SAME-SCALE-CANDIDATES.md`](./PR-DRAFT-TJ-SAME-SCALE-CANDIDATES.md) — paste-ready title/body for [PR #102](https://github.com/simons357/Ship_it_app/pull/102) (branch `cursor/tj-candidates-9083`)
- [`PR-DRAFT-HH-SPECTRAL-CONCENTRATION-AUDIT.md`](./PR-DRAFT-HH-SPECTRAL-CONCENTRATION-AUDIT.md) — paste-ready draft for `cursor/hh-concentration-audit-4792`
- [`SCIENTIFIC-REPORT.md`](./SCIENTIFIC-REPORT.md) — problem statement, objects, Lemma★ / PRODUCT-BLOCK status, proved vs hypothesized vs parked
- [`CREDIT-BODY-OF-WORK.md`](./CREDIT-BODY-OF-WORK.md) — KEEP shelf vs named open doors (no Clay claim)
- [`DA-AUDIT.md`](./DA-AUDIT.md) — Domain Architect check + language sanitize (CONDITIONAL PASS)
- [`METHOD-PANEL-REVIEW.md`](./METHOD-PANEL-REVIEW.md) — simulated method-seat review (not peer review; not real mathematicians)
- [`PROOF-CHAIN-CLEAN.md`](./PROOF-CHAIN-CLEAN.md) — definitions of \(T_c,\Lambda,X,Y,Z,E\); spectral-shift identity; Lemma★; open estimate (prefer SCIENTIFIC-REPORT §4 for live PRODUCT-BLOCK = uniform \(\mathcal{R}_\star\))

Reproducibility: [`scripts/ns_attacks/`](../../scripts/ns_attacks/). Same-scale probes: `python3 scripts/ns_attacks/tj_same_scale_candidate_probes.py` · hard run: `python3 scripts/ns_attacks/tj_survivors_hard_run.py` · harder run: `python3 scripts/ns_attacks/tj_survivors_harder_run.py`.

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

## Claim ledger governance

- [`CLAIM-LEDGER-AUDIT-2026-10.md`](./CLAIM-LEDGER-AUDIT-2026-10.md) — July 23 numbered CLAIM LEDGER vs Oct 2026 honesty locks (KEEP / RELABEL / CONFLICT).
- [`CLAIM-LEDGER-DRAFT-NS-RH-Q6-2026-10.md`](./CLAIM-LEDGER-DRAFT-NS-RH-Q6-2026-10.md) — optional draft excerpt (NS + RH + Q6 only).
- [`PR-DRAFT-CLAIM-LEDGER-AUDIT.md`](./PR-DRAFT-CLAIM-LEDGER-AUDIT.md) — paste-ready draft PR.
- [`RING-LEMMA-RECONCILIATION-2026-10.md`](./RING-LEMMA-RECONCILIATION-2026-10.md) — Oct 2 Ring uploads vs July NS-6/7/8/10; June 19 geometry superseded; RL-G1…G3 spatial SoT.
- [`ring-lemma/`](./ring-lemma/) — ingested TeX + ledger reconciliation text.
- [`PR-DRAFT-RING-LEMMA-RECONCILIATION.md`](./PR-DRAFT-RING-LEMMA-RECONCILIATION.md) — paste-ready draft PR.

**Dangerous July PROVED rows:** NS-4 (Aug↔SND equivalence), unscopeed NS-9 (augmented \(C^\infty\)). **KEEP:** NS-10 OPEN, NS-11 NOT CLAIMED. **NS-6 Ring:** scoped spatial PROVED (RL-G1…G3) only — not Clay; June linear Ring withdrawn.
