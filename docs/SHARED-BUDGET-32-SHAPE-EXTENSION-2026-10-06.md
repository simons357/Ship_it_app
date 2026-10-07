# Shared-budget 32-shape extension — independent review filing

6 October 2026.
**Concrete enlargement for independent review. Not (17).
NS not solved. PR #165 unchanged.**

Author package (handoff name):
`Shared-Budget-17-Family-Audit-and-9-25-Extension.zip`

**Cover note for reviewers:**
[`COVER-NOTE-17-FAMILY-32-SHAPE-REVIEW.md`](COVER-NOTE-17-FAMILY-32-SHAPE-REVIEW.md).

**Phase-cancellation exploration** (does not alter proved
scopes; worst-case coherent ratio can hit 1):
[`PHASE-CANCELLATION-EXPLORATION.md`](PHASE-CANCELLATION-EXPLORATION.md).

Parents / scope separation:
- Original **17-family** shared-budget argument (high-pass
  conclusion at its stated scope).
- Older fixed-block \(\mathcal Q\)-identity and integrable
  majorant (separate scope).
- This page: **17 + 15** nonzero shapes from the
  \((9,25)\) family → **32** shapes, one controlled
  combined charge.

---

## RESULT

| Item | Verdict |
|---|---|
| Original 17-family argument, including its high-pass conclusion | **Proved** at stated scope |
| Older \(\mathcal Q\)-identity and integrable majorant | **Proved** at its separate fixed-block scope |
| Combined charge multiplicity, excluding zero-transfer shapes | **Exactly 4** |
| Enlargement | Original 17 shapes **plus** 15 nonzero shapes from \((9,25)\) → **32** shapes |
| Control of arbitrary families | **Not claimed** — one controlled extension only |

Exact third-shell lists and overlap witnesses:
[`NS-HANDOFF-2026-10-07.md`](NS-HANDOFF-2026-10-07.md).
Finite checks: `scripts/ns_attacks/verify_families.py`.

Using the paper’s existing constants, the sharper weighted
combined charge is

\[
\boxed{
\rho+3\rho'\approx 3.1077752814793693,
\qquad
\rho\approx 0.6318550823987903,
\qquad
\rho'\approx 0.8253067330268596.
}
\]

(\(\rho\) = original 17-family constant; \(\rho'\) = new
\((9,25)\)-family constant.) Combined multiplicity: **6**
literal / **4** zero-pruned (different accountings).
Common high-pass cutoff:

\[
\boxed{
K=\max\bigl\{2,\ 3(M-1)\bigr\}.
}
\]

Original family used \(\max\{2,\sqrt5\,(M-1)\}\) — product,
not \(\sqrt{5(M-1)}\); do not reuse without proof.

**ZIP retrieval is no longer the research blocker** (recovered
in the Oct 7 source conversation). This workspace may still
lack the binary; content is filed from the handoff.

Adding families does **not** necessarily increase the
maximum charge every time; that depends on their overlap.
This calculation establishes one controlled extension —
not control of arbitrary families.

---

## 1. Corrections (constants)

| Statement | Status |
|---|---|
| Older **constant-3** fixed-shell lemma | Remains **valid under its hypotheses** |
| **Constant 2** | Sharpens the **distinct-donor** case |
| Resulting triple-product factors | \(\sqrt 3\) (fixed-shell / equal-donor line) and \(\sqrt 2\) (distinct-donor sharpening) |

Do not withdraw the constant-3 lemma when citing the
distinct-donor sharpening. The two constants apply under
different hypotheses; the product faces are \(\sqrt 3\)
and \(\sqrt 2\).

---

## 2. What the 32-shape extension is

- **Base:** the audited 17-shape shared-budget family.
- **Add:** 15 nonzero-transfer shapes from the
  \((9,25)\) family (zero-transfer shapes excluded from
  the charge count).
- **Total:** 32 shapes under one combined charge
  bookkeeping.
- **Combined multiplicity** (nonzero-transfer only):
  exactly **4**.
- **Weighted charge** (paper constants):
  \(\rho+3\rho'\approx 3.1077752815\) with
  \(\rho'\approx 0.8253067330\).
- **Cutoff:** raise the common high-pass gate to
  \(K=\max\{2,3(M-1)\}\) so the enlarged family shares
  one cutoff.

---

## 3. Independent-review checklist (package)

The author ZIP is named to contain:

1. Full checklist for the 17-family audit and the
   \((9,25)\) extension.
2. Constants (\(\rho,\rho'\), multiplicity 4, product
   factors \(\sqrt 3,\sqrt 2\)).
3. Exact overlap witnesses (why multiplicity is 4; why
   zero-transfer shapes drop out).
4. Reproducible script.
5. Handoff note for reviewers.

**Environment note (this filing):** the ZIP
`Shared-Budget-17-Family-Audit-and-9-25-Extension.zip`
was **not present** in the agent workspace at commit
time. This page records the author-stated audit results
for PR submission. Drop or authorize attachment of the
ZIP to complete the binary handoff.

---

## 4. Explicit non-claims

- Does **not** establish criterion (17).
- Does **not** establish global regularity / Clay.
- Does **not** claim control of arbitrary shape families.
- Does **not** modify PR #165 (signed-scalene / (Q⋆)
  chain). That PR could not be updated (write access
  denied); this filing is the independent-review
  submission instead.

Overlap of shells across families can keep the max
charge from rising when a new family is added; the
present calculation is one extension where the combined
multiplicity is controlled at 4.

---

## STATUS

17-FAMILY (STATED SCOPE): PROVED (AUTHOR AUDIT).
FIXED-BLOCK Q-IDENTITY / INTEGRABLE MAJORANT: PROVED (SEPARATE SCOPE).
32-SHAPE EXTENSION (17 + 15 FROM (9,25)): FILED FOR INDEPENDENT REVIEW.
COMBINED CHARGE MULTIPLICITY (NONZERO-TRANSFER): EXACTLY 4.
WEIGHTED CHARGE ρ+3ρ′ ≈ 3.1077752815 (ρ′ ≈ 0.8253067330).
COMMON HIGH-PASS: K = max{2, 3(M−1)}.
CONSTANT-3 LEMMA: VALID UNDER HYPOTHESES; DISTINCT-DONOR SHARPENING → 2; FACTORS √3, √2.
ZIP BINARY: NOT IN WORKSPACE AT THIS FILING — ATTACH WHEN AVAILABLE.
(17) / GLOBAL REGULARITY: NOT CLAIMED.
PR #165: NOT UPDATED (WRITE ACCESS DENIED).
INDEPENDENT-REVIEW COVER NOTE: FILED.
NS NOT SOLVED.
