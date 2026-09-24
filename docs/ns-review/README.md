# NS review notes

Working notes for the axisymmetric-with-swirl / Φ-renorm book and adjacent NS packaging.

## Φ-renorm (KEEP; conditional)

- [`PHI-RENORM-WHAT-IS-KEPT.md`](./PHI-RENORM-WHAT-IS-KEPT.md) — field-first KEEP / PARK card; separate from Lemma★.
- [`PHI-RENORM-AUDIT-2026-08-22.md`](./PHI-RENORM-AUDIT-2026-08-22.md) — independent 22 Aug 2026 audit of the June 30 swirl paper (\(\dot H^{2.6}\to\dot H^{1.3}\) relabel; barrier left open).
- TeX faces: [`docs/papers/swirl/`](../papers/swirl/).

**Open barrier (unchanged):** \(\|u^r/r\|_{L^\infty}\) uniform in \(\eps\) — equivalent to axisymmetric-with-swirl global regularity. Paper remains a conditional reduction. Clay is not closed.

**Do not conflate** with Lemma★ packaging. Static uniform \(\sup\mathcal{R}_\star<\infty\) is **dead** (Attack 10). That does not close Φ-renorm, and it does not close Clay B.

## Lemma★ / \(\mathcal{R}_\star\) (static bound killed)

- [`../math/ns_attacks/ATTACK_10_LOCALIZED_BUMP.md`](../math/ns_attacks/ATTACK_10_LOCALIZED_BUMP.md) — localized bump, \(\mathcal{R}_\star\sim\ell^{-3}\). A single universal \(C_{\mathrm{geom}}\) cannot close the energy budget.
- Packet: [`../../packets/ATTACK-10-LOCALIZED-BUMP-2026-09-24.md`](../../packets/ATTACK-10-LOCALIZED-BUMP-2026-09-24.md).
- Probe: `scripts/ns_attacks/attack10_localized_bump.py`.

The centered identities (\(\Lambda'\), \(D_s\), two-shell, homogeneity) stand. What is dead is using \(\sup\mathcal{R}_\star<\infty\) as a static closure. The remaining question is dynamical: can NS hold a concentrating bump with coherent positive \(T_c\)? **NS not solved.**
