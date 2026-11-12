# NS review notes

Working notes for the axisymmetric-with-swirl / Φ-renorm book and adjacent NS packaging.

## Φ-renorm (KEEP; conditional)

- [`PHI-RENORM-WHAT-IS-KEPT.md`](./PHI-RENORM-WHAT-IS-KEPT.md) — field-first KEEP / PARK card; separate from Lemma★.
- [`PHI-RENORM-AUDIT-2026-08-22.md`](./PHI-RENORM-AUDIT-2026-08-22.md) — independent 22 Aug 2026 audit of the June 30 swirl paper (\(\dot H^{2.6}\to\dot H^{1.3}\) relabel; barrier left open).
- TeX faces: [`docs/papers/swirl/`](../papers/swirl/).

**Open barrier (unchanged):** \(\|u^r/r\|_{L^\infty}\) uniform in \(\eps\) — equivalent to axisymmetric-with-swirl global regularity. Paper remains a conditional reduction. Clay is not closed.

**Do not conflate** with Lemma★ PRODUCT-BLOCK packaging.

## DA-NS-2 (Y-cousin occupation; integral OPEN)

- [`DA-NS-2.md`](./DA-NS-2.md) — \(K_{\min,\theta}=[T_c-\theta\nu D_s]_+/Y\); Galerkin-uniform integral is the hole; tautological \(K\) refused; JGC budget not seated.
- Packet: [`packets/DA-NS-2-2026-11-12.md`](../../packets/DA-NS-2-2026-11-12.md).
- Machine: `PYTHONPATH=scripts python3 scripts/ns_attacks/da_ns_2.py`.
- DA card: `python3 -m domain_architect --da-ns-2`.

`ns_solved` is false. Do not glue to Φ-renorm.
