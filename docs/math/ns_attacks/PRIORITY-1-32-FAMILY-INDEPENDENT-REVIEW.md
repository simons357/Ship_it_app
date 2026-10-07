# Priority 1 — Independent analytic review of the 32-family package

**Date:** 7 October 2026  
**Reviewer role:** autonomous desk review against Oct 7 handoff SoT +
in-repo filing (not a fresh specialist certification of every PDF line).  
**Primary SoT:** [`NS-HANDOFF-2026-10-07.md`](NS-HANDOFF-2026-10-07.md)  
**Finite checks:** `scripts/ns_attacks/verify_families.py` →
`VERIFY-FAMILIES.json` (**Rerun here**)

---

## Explicit non-claims (locked)

- No classical unaugmented Navier–Stokes regularity / Clay claim.
- No all-scalene criterion **(17)**.
- No swirl compression closure.
- No substitution of a “37-shape” package for this **32-shape** union.

---

## 1. Package inventory vs handoff

| Item | Status | Evidence |
|---|---|---|
| ZIP name `Shared-Budget-17-Family-Audit-and-9-25-Extension.zip` | Recovered in source conversation Oct 7 | **Reported** (handoff); library ID `libfile_e69ca0f14ab4819186900a547b61df20` |
| Bundled `verify_families.py` passed in source conversation | Recorded | **Reported** |
| Binary ZIP in *this* workspace | Absent | Missing bytes; **not** a research blocker |
| Contents expected: `AUDIT-AND-HANDOFF.txt`, `family-results.json`, `shape-constants.csv`, `verify_families.py` | Named in handoff | **Reported**; fixtures re-filed under `fixtures/shared_budget_32/` from handoff locks |
| In-repo reimplementation of finite checks | Present | **Rerun here** |

**Verdict on ZIP:** retrieval is no longer the blocker. Analytic inequalities
inside the audit PDFs remain **Source-backed analytic result** until a
specialist re-certifies every step against the primary manuscript PDF.

---

## 2. Shape lists and overlap

### Original 17-family — anchors \((5,25)\)

Third-shell labels \(b\):

\[
8,10,14,18,20,22,24,26,30,34,36,38,40,42,46,50,52.
\]

Finite lattice existence of triangles \((5,b,25)\): **PASS**
(`verify_families.py`).

### Added family — anchors \((9,25)\)

Collinear zero-transfer endpoints \(b\in\{4,64\}\) removed by
exact identity \((b-a-c)^2=4ac\). Active 15:

\[
6,10,12,14,16,24,30,34,38,44,52,54,56,58,62.
\]

Union with original = **32** nonzero shapes. **Rerun here.**

### Multiplicity / overlap

| Accounting | Value | Evidence |
|---|---|---|
| Original individual multiplicity | 3 | **Rerun here** (dilation scan) |
| Added active individual multiplicity | 3 | **Rerun here** |
| Combined zero-pruned at \(R=216\) | 4 | **Rerun here** — charges \((5,24,n{=}3)\), \((9,6,n{=}6)\), \((9,24,n{=}3)\), \((9,54,n{=}2)\) |
| Combined literal multiplicity | 6 | **Reported** (witness \(|k|^2=14400\); ZIP charge-group definition) |

**Important scope note (desk):** a third-shell-only scan at
\(R=14400\) does **not** reproduce literal multiplicity 6
(`VERIFY-FAMILIES.json` records count 4 on that narrow scan). Keep the
ZIP charge-group definition (literal 6) distinct from the zero-pruned
witness table (4 at 216). No contradiction claimed; different
accountings.

---

## 3. Constants and geometric normalization

| Quantity | Face | Desk check |
|---|---|---|
| \(\rho\) | \(0.6318550823987903\) | Stored face (**Reported** from bundled script) |
| \(\rho'\) | \(0.8253067330268596\) | Stored face (**Reported**) |
| \(\rho+3\rho'\) | \(3.1077752814793693\) | Arithmetic **PASS** (**Rerun here**) |

Normalization hygiene (handoff §4 vs Oct 6 cover note):

| Statement | Desk verdict |
|---|---|
| Convolution-square constant **3** remains valid under its hypotheses | Preserve (**Source-backed**) |
| Distinct-donor sharpening → convolution-square **2** | Preserve under distinct hypotheses (**Source-backed**) |
| Triple-product factors \(\sqrt3\), \(\sqrt2\) | Correct product-face language |
| Calling triple-product factors “3 and 2” without squared-normalization caveat | **Reject** — handoff forbids |
| Shape constants use \(\sqrt{3\Delta}\); displayed \(\rho\) not silently recomputed with constant-2 | Preserve |

Oct 6 cover note / extension desk language that mentions \(\sqrt3\) and
\(\sqrt2\) is consistent **if** read as product faces. Any phrasing that
equates the triple-product factors with bare 3 and 2 is out of scope for
this package.

---

## 4. Common high-pass cutoff vs primary filing

Combined family (handoff):

\[
M=\max\Bigl\{1,\Bigl\lceil
\frac{(\rho+3\rho')\sqrt{E_0}}{\eta\nu}
\Bigr\rceil\Bigr\},
\qquad
K=\max\{2,\ 3(M-1)\}.
\]

Restricted conclusion:

\[
\bigl[\mathcal T_{\mathrm{combined}}(P_{>K}u_N)-\eta\nu Y_N\bigr]_+=0
\]

scoped to the selected 32-family only.

| Check | Verdict |
|---|---|
| Combined cutoff \(K=\max\{2,3(M-1)\}\) matches cover note + extension desk | Consistent |
| Original smaller cutoff \(\max\{2,\sqrt5\,(M-1)\}\) is a **product**, not \(\sqrt{5(M-1)}\) | Consistent with handoff; do not reuse for extension without proof |
| Restricted excess-zero conclusion ⇒ criterion (17) | **False** — scope forbids |
| “Proved at stated scope” for original 17-family high-pass | Preserve as **audit verdict** (**Source-backed**), not re-proved here |

Manuscript binary (`AUDIT-AND-HANDOFF.txt` / paper PDF) was not
available as bytes in this workspace. Desk comparison is against the
handoff locks + Oct 6 in-repo filing. Full line-by-line PDF audit remains
**Open** as specialist certification, not as ZIP retrieval.

---

## 5. Consistency with in-repo Oct 6 filing

| Filing | Alignment with Oct 7 SoT |
|---|---|
| `docs/SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md` | Aligned on 32-shape union, \(\rho+3\rho'\), \(K=\max\{2,3(M-1)\}\), non-claims; updated for ZIP-not-blocker |
| `docs/COVER-NOTE-17-FAMILY-32-SHAPE-REVIEW-2026-10-06.md` | Aligned; decimals truncated in places — use handoff full faces for arithmetic |
| `docs/PHASE-CANCELLATION-EXPLORATION-2026-10-06.md` | Narrowed: \(R=1\) = common signs, not geometric-bound saturation |
| Earlier “ZIP missing” notes | Superseded |

---

## 6. Priority-1 completion criterion

Handoff §11 item 1: *constants, overlap, common cutoff against primary
manuscript; preserve exact scope.*

| Subcriterion | Status |
|---|---|
| Constants faces + weighted arithmetic | **Done** (Rerun / Reported faces) |
| Overlap witnesses (esp. \(R=216\) ×4) | **Done** (Rerun) |
| Common cutoff formula + scope | **Done** (consistent across filing) |
| Literal multiplicity-6 charge-group definition vs third-shell scan | Documented gap; keep **Reported** for literal 6 |
| Line-by-line certification of every inequality in audit PDF | **Open** — binary manuscript not in workspace; audit verdict preserved as source-backed |

**Desk verdict:** package is internally consistent at the handoff’s
stated scope for the controlled 32-shape extension. Restricted-family
theorem remains **Proved at stated scope** per audit label. Extension
beyond that family, (17), Clay, and swirl closure are **not**
established.

---

## STATUS

PRIORITY 1 DESK REVIEW: COMPLETE AT FILING SCOPE.
FINITE CHECKS: PASS (verify_families.py).
AUDIT PDF SPECIALIST RE-CERTIFICATION: OPEN (bytes not required for ZIP-blocker narrative).
(17) / CLAY / SWIRL CLOSURE: NOT CLAIMED.
NS NOT SOLVED.
