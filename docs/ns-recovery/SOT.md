# SoT — centered drift / same-shell packet

**Locked:** 10 September 2026  
**This file is the source of truth** for the packet line. Longer notes do not override it.

Navier–Stokes is **not solved**. The uniform triadic bound is **open**.

**Full lemma (OPEN):** [`docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md`](../math/ns_attacks/LEMMA_STAR_CANONICAL.md). Formulas: [`docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md). \(K_{\alpha,\beta}\) is a restricted near-shell test, not the lemma.

---

## Locked

Fixed-gap spheres \(S_n\cup S_{n+d}\). This is a **packet**, not an AP.

- \(D_s\) comes from the **gap** \(d\), not from a width.
- Mixed closures of type \((n,n,n+d)\) are only \(O(m)\), not \(O(m^2)\). Checked: 48 closures at \(n=9\) (\(m=54\)); 288 at \(n=89\) (144+120 keys).
- \(\mathcal R_\star\) falls with \(n\) (0.11 → 0.031). It does **not** track \(m^{1/2}\).
- The **natural same-shell ensemble is not a kill**.

The \(O(1)\) gap is available in this model, and that still does not produce \(\mathcal R_\star\sim m\).

---

## Remaining packet falsifier

**Fixed-output \(\Theta(m^2)\) 9D is excluded.** For each output \(k\), \(q=k-p\), so at most \(m\) ordered pairs land on that mode. Occupied output count \(s\) on shell \(\beta\) gives \(K_{\alpha,\beta}\le 16s\). A fixed number of outputs cannot produce unbounded \(K\). Note: [`docs/math/ns_attacks/ATTACK_9B_COUNTING_CS_EXCLUSION.md`](../math/ns_attacks/ATTACK_9B_COUNTING_CS_EXCLUSION.md).

Board lock: [`WHAT-ELSE.md`](WHAT-ELSE.md). Two live writes only (9D + ★ reason).

**Still live:** growing **input and output** supports, full complex polarizations, frequency factors retained. Uniform 9B target:
\[
\|\Pi_\beta B(w,w)\|_2\le C\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2.
\]
A bound \(C\alpha\|w\|_2^2\) is insufficient. Spec: [`docs/math/ns_attacks/ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](../math/ns_attacks/ATTACK_9D_THETA_M2_LOCKED_PHASE.md).

Isolated triangles, wide APs, narrow APs, full adjacent spheres, and fixed-\(s\) designed packets: **no kill**.

---

## Do not write

- Do not treat full lattice spheres as an additive basis of density \(\Theta(m^2)\).
- Do not claim \(\Theta(m^2)\) pairs onto one output, or onto a fixed number of outputs.
- Do not restore an AP-width \(D_s\) for this construction.
- Do not claim a uniform triadic bound or Clay regularity from this ensemble.
- Canonical lock: `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`,
  \[
  \mathcal R_\star(v)=\frac{(T_c(v)_+)^2}{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)}.
  \]
  The values \(0.11\to 0.031\) are locked as **user-reported** on the natural ensemble; they have **not** been recomputed here with that formula.

---

## Other live writing

H1 on the cylinder is the other live track if the packet line is shelved. It is **not** started by this lock.

PR #24 localized ABC / CS remainder is **not** this packet line. Finite Galerkin climb, not a ★ kill. Lock: [`SUPERGROK-ABC-LOCK.md`](SUPERGROK-ABC-LOCK.md). Detail: [`CS-REMAINDER-VS-DA-REJECT.md`](CS-REMAINDER-VS-DA-REJECT.md).

Dream team = papers and measurements, not another model. Vote cannot close. [`DREAM-TEAM-SUMMARY.md`](DREAM-TEAM-SUMMARY.md).

---

## Pointers (do not override)

| File | Role |
|---|---|
| `scripts/ns_lemma_star_core.py` | Standalone exact \(T_c\) / \(D_s\) / \(\mathcal R_\star\) (direct triad sum; \(D_s\) cross-check) |
| `tests/test_same_shell_packet.py` | Locks 48 / 288 / \(d=2\) zeros / \(O(m)\) not \(O(m^2)\) |
| `docs/ns-recovery/SAME-SHELL-PACKET-NOTE.md` | Expanded packet note |
| `docs/ns-recovery/CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md` | 7 Sep search; Stokes-moment paste was missing until PR #48 |
| `docs/ns-recovery/GROK_HEAVY.md` | **Grok Heavy entry** — formulas, five-lane JSON, live work |
| `docs/ns-recovery/FIVE_LANE_PACK_LOCATOR.md` | Absolute script paths + box drop for 9B / \(R_★\) |
| `docs/ns-recovery/CS-REMAINDER-VS-DA-REJECT.md` | PR #24 ABC / λ vs DA reject; do not import “★ false” |
| `docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md` | Working foundation: uniform \(\mathcal R_\star\) |
| `docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md` | Operator / triad identities |
| `docs/math/ns_attacks/ARCHIVE_OLDER_LEMMA_STAR_PROOF.md` | Older Section 4 is **not** a theorem |
| `docs/math/ns_attacks/ATTACK_9D_THETA_M2_LOCKED_PHASE.md` | Live 9D: growing I/O, complex pols |
| `docs/ns-recovery/five-lane-pack/` | PR #48 five-lane / Lemma★ pack. Index: `five-lane-pack/HIT.md`. Live: https://github.com/simons357/Ship_it_app/pull/48 |
