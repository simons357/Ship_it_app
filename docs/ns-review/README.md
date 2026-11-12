# NS review notes

Working notes for the axisymmetric-with-swirl / Φ-renorm book and adjacent NS packaging.

## Φ-renorm (KEEP; conditional)

- [`PHI-RENORM-WHAT-IS-KEPT.md`](./PHI-RENORM-WHAT-IS-KEPT.md) — field-first KEEP / PARK card; separate from Lemma★.
- [`PHI-RENORM-AUDIT-2026-08-22.md`](./PHI-RENORM-AUDIT-2026-08-22.md) — independent 22 Aug 2026 audit of the June 30 swirl paper (\(\dot H^{2.6}\to\dot H^{1.3}\) relabel; barrier left open).
- TeX faces: [`docs/papers/swirl/`](../papers/swirl/).

**Open barrier (unchanged):** \(\|u^r/r\|_{L^\infty}\) uniform in \(\eps\) — equivalent to axisymmetric-with-swirl global regularity. Paper remains a conditional reduction. Clay is not closed.

**Do not conflate** with Lemma★ PRODUCT-BLOCK packaging.

## Centered drift (identities KEEP; remainder OPEN)

- [`CENTERED-DRIFT.md`](./CENTERED-DRIFT.md) — spectral centering \(T_c\) vs spread \(D_s\); note triad \(T_c=16/5\); uniform absorption killed; pathwise \(K(t)\) open.
- [`CENTERED-EQUATION.md`](./CENTERED-EQUATION.md) — \(\Lambda'=2(T_c-\nu D_s)/X\), exact, not an estimate.

Machine: `PYTHONPATH=scripts python3 scripts/ns_attacks/centered_drift.py`.
`ns_solved` is false. Do not glue to Φ-renorm.
