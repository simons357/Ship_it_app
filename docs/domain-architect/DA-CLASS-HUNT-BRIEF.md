# DA dream-team brief — usable CLASS for Door-1 / (A)

**Voice:** Domain Architect (DA), dream-team consult  
**Date:** 2026-09-16  
**Branch:** `cursor/axisymmetric-shell-audit-9d6b`  
**Filter:** [`AXISYMMETRIC-SHELL-AUDIT.md`](AXISYMMETRIC-SHELL-AUDIT.md)  
**Estimate:** [`docs/papers/swirl/AXISYMMETRIC-SHELL-ESTIMATE.md`](../papers/swirl/AXISYMMETRIC-SHELL-ESTIMATE.md)  
**Faces:** [`docs/papers/swirl/FACES.md`](../papers/swirl/FACES.md)  
**Decisions:** [`DECISIONS.md`](DECISIONS.md)  
**Artifact mirror:** `/opt/cursor/artifacts/da_dream_team_class/BRIEF.md`

**First sentence.** Class: unaugmented axisymmetric-with-swirl (and named subclasses below). Quantity: Door-1 shell block \(Z_j\) / near-scale \(T_{j\leftarrow j}\) at \(b\ge 1\) (energy) or enstrophy same-scale. Remainder after Door-1: \(T_{j\leftarrow j}\). Assumed: [no recycling \(\dot e_j/\dot Z/\Lambda'\); spectral-shift ≠ Lemma★; occupancy \(1+\alpha\approx\tfrac12\) not depletion; sharp \(b=0\) energy identity ≡ 0 is triad pairing, not depletion; NS not solved; Clay NOT CLAIMED].

**This is not a close.** DA-VC-01 stays **FAIL** until (A) seats (and even then NS-open / Clay stay separate scoreboards).

Cross-link only to five-lane / Lemma★ (`cursor/ns-five-lane-lemma-star-1390`, PR #48). **Do not merge stacks.**

---

## Locked honesty (do not reopen)

| Lock | Status |
|---|---|
| Sharp \(b=0\) ENERGY internal \(T_{j\leftarrow j}\) | \(\equiv 0\) by triad pairing — **not** depletion |
| Door-1 remainder | Near-scale \(b\ge 1\) (energy) and/or enstrophy same-scale |
| Occupancy \(1\) + \(\alpha\approx\tfrac12\) | **KILLED** as depletion \(\Rightarrow\) (A) |
| Spectral-shift identity | Bookkeeping only; ≠ Lemma★; ≠ transfer control |
| Conditional Gronwall under (A) | \(\nu^1\) template; needs (A); **not claimed** |
| Axisym alone on mixed fields | Does **not** force Door-1 \(T_{j\leftarrow j}\approx 0\) (disk maxima \(O(1)\)) |
| DA-VC-01 | **FAIL** |
| Clay / unconditional 3-D | **NOT CLAIMED** |

**What “seating (A)” means (acceptance).** A named class \(\mathcal C\) and an explicit lemma:

\[
\lvert T_{j\leftarrow j}\rvert
\le
\varepsilon\nu P_j + R
\quad\text{on }\mathcal C,\quad
0\le\varepsilon<1,
\]

with \(P_j\) = **palinstrophy**, \(R\) controlled by energy / known quantities, **without** \(\dot e_j\), \(\dot Z\), or \(\Lambda'\), and without reading occupancy or the sharp \(b=0\) energy zero as the smallness. Wrong-normalization templates (\(C\sqrt{D}\,Z\), energy-budget \(\rho_j<\nu\)) do **not** count as seated (A).

---

## Why axisymmetry alone failed on mixed fields

Axisymmetry-with-swirl is a **real geometry class**: it removes free helical HHH on fully 3-D wavevector configurations incompatible with rotation about \(z\), and restricts exact-disk probes to meridional \(k=(k_x,0,k_z)\) with swirl polarization \(\hat e_y\).

What it does **not** remove:

1. **Meridional self-stretch \(T^{\mathrm{mm}}\)** — on compact mixed swirl+meridional samples, \(T^{\mathrm{mm}}\) is the bulk of local \(T_{j\leftarrow j}\) (§7–§8 of the estimate note). Pure swirl (\(u^r=u^z=0\)) kills the pairing; mixed fields do not inherit that zero.
2. **Near-scale (\(b\ge 1\)) feeders** — sharp \(b=0\) energy telescope is an identity on a closed annulus; Door-1 with soft LP / \(b\ge 1\) leaks. Disk probe: \(\max\lvert T_{\mathrm{near}}\rvert/Z^{3/2}\) stays \(O(1)\) on axisym-restricted disks.
3. **Enstrophy same-scale** — does not inherit the energy triad telescope.

So “class (C) = axisymmetric-with-swirl” is the right *plant*, not a seated bound of the remainder. Route (C) alone ≠ (A).

---

## Ranked routes to a usable CLASS for Door-1 / (A)

Marks: **KEEP** (in the program), **TRY** (next experiment / proof move), **KILL** (do not spend cycles as if they seat (A)).

### Rank 1 — Conditional \(\theta\)-class → bridge to (A)  ·  **TRY** (best next)

**Class card.** \(\mathcal C_\theta=\{\)axisym-with-swirl fields with near-scale geometric factor \(\theta=\lvert\mathrm{signed}\rvert/\sum\lvert\mathrm{contrib}\rvert\le\theta_\ast\}\).

**What already sits.** Disk template (estimate § Same-scale): if \(\theta\le\theta_\ast\) then \(\lvert T_{\mathrm{near}}\rvert\le\theta_\ast C_{\mathrm{young}}\sqrt{D}\,Z\). Not (A).

**Next move (one experiment).**

1. On the existing harness `scripts/axisym_same_scale_tjj.py`, print \(\theta\) vs \(\lvert T_{\mathrm{near}}\rvert/P_j\) (palinstrophy-normalized) on axisym disks — same signed Im object, **new normalization**.
2. Search for a **named** geometric proxy for \(\theta\) that is *not* occupancy and *not* \(1-\lvert\alpha\rvert\) (both killed / insufficient): e.g. meridional/swirl energy ratio \(E_{\mathrm{mer}}/E\), near-scale feeder count density, or a structure-constant cancellation score \(C=\lvert\sum\tau\rvert/\sum\lvert\tau\rvert\) restricted to \(b\ge 1\) legs.
3. Attempt the absorption rewrite: Young \(\sqrt{D}\,Z\) against palinstrophy via Poincaré-shell \(P_j\ge c\,4^j Z_j\) — only if \(\theta_\ast\) is small enough that \(\varepsilon=\theta_\ast C'/\nu\) (or the correct scaling) stays \(<1\). If the \(\nu\)-scaling fails, **record the failure mode** (likely: \(\theta\) must be \(O(\nu)\) — too strong for a class, becomes small-data).

**Seating criterion.** Class control of \(\theta_\ast\) **plus** \(\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu P_j+R\) with named \(\varepsilon,R\). Disk-only \(\theta\) prints are not seating.

**Failure modes.**

- \(\theta\sim O(1)\) on every mixed axisym disk ⇒ \(\mathcal C_\theta\) empty of interesting mixed data; route collapses to small-data / extra symmetry.
- Bridge needs \(\theta=O(\nu)\) ⇒ not a geometric class; rename as smallness hypothesis.
- Absolute-value Young sneaks back ⇒ **OUT** (audit DISCARD).

**KEEP.** The \(\theta\)-template as a *conditional* object.  
**KILL.** Treating the present \(\theta C\sqrt{D}\,Z\) line as (A).

---

### Rank 2 — Sparse / near-scale-free Fourier support  ·  **TRY**

**Class card.** \(\mathcal C_{\mathrm{sparse}}=\{\)axisym-with-swirl fields whose active Fourier support has **no** (or \(o(1)\) density of) near-scale closed triads at width \(b\) for shells that carry energy\(\}\).

**Why it might seat (A).** If near-scale feeders are absent, Door-1 \(T_{j\leftarrow j}\) at that \(b\) vanishes by support, not by depletion storytelling. Remainder moves to \(T_{j\leftarrow\neq j}\) (already budgeted; summability still a gap) or forces a thinner \(b\).

**Next move.**

1. Exact-disk census: enumerate axisym-allowed triads with \(\lvert\ell-j\rvert,\lvert m-j\rvert\le b\) vs support cardinality; print fraction of near-scale feeders vs \(\lvert T_{\mathrm{near}}\rvert\).
2. Construct **one** named sparse family (e.g. single meridional shell + swirl polarization with no resonant \(b\ge 1\) closing) and verify \(T_{j\leftarrow j}=0\) at that \(b\) to \(10^{-16}\).
3. Ask whether sparsity is **preserved** by NS evolution (almost certainly **no** in general). If not preserved, the class is **initial-data only** — still a theorem path, but not a dynamical close.

**Seating criterion.** For fields in \(\mathcal C_{\mathrm{sparse}}\), \(T_{j\leftarrow j}=0\) (or \(\le\varepsilon\nu P_j\)) by support counting, with the preservation hypothesis written in brackets.

**Failure modes.**

- Nonlinear cascade immediately fills near-scale bands ⇒ class not invariant.
- Soft LP bumps create effective near-scale even on sparse sharp support.
- Confusing “few modes on a small disk” with class sparsity as \(K_{\max}\to\infty\).

**KEEP.** Support-census diagnostic on the harness.  
**KILL.** Claiming generic axisym data are near-scale-free.

---

### Rank 3 — Pure swirl / small data / extra symmetry  ·  **KEEP** as conditional subclasses, **KILL** as mixed-class close

| Subclass | What it does | Usable for Door-1 / (A)? |
|---|---|---|
| **Pure swirl** \(u^r=u^z=0\) | \(T_{j\leftarrow j}=0\) exactly on that field | **KEEP** as a class statement / unit check. **KILL** as a bound on mixed fields (estimate §7). |
| **Small data** | Classical regularity by smallness in critical/subcritical norms | **TRY** as a *different* theorem path: seats smoothness without seating geometric (A). Does not unlock mixed large-data Door-1. Write [small data] in brackets. |
| **Extra symmetry** (e.g. reflection \(z\mapsto -z\), odd/even swirl, Beltrami-like alignment forced) | May kill \(T^{\mathrm{mm}}\) or force \(\theta\) small | **TRY** only with a **named** symmetry and a printed kill of the bulk term. Do not invent a symmetry that is not in the plant. |
| **θ-bound conditional** (Rank 1) | Conditional geometric class | Best bridge toward (A) if \(\theta_\ast\) is class-controlled. |
| **Full axisym-with-swirl (no extra)** | Removes free HHH; leaves \(T^{\mathrm{mm}}\) + near-scale | **KEEP** as the plant. **KILL** as “already seats (A).” |

**Small-data honesty.** Small data can make \(\lvert T_{j\leftarrow j}\rvert\) absorbable because everything is small — that is **not** a depletion lemma and must not be sold as (B)⇒(A) on large data.

**Extra-symmetry honesty.** Compact-sample \(\overline\alpha\sim 0\) on mixed blobs did **not** kill \(T_{j\leftarrow j}\) (ratios \(O(10^{-3})\)). Alignment alone is insufficient; need a symmetry that removes meridional self-stretch or near-scale feeders.

---

## Dead ends (KILL list for this hunt)

Do not re-open as if they seat (A):

1. Occupancy \(1\) ⇒ depletion; occupancy \(1\) + \(\alpha\approx\tfrac12\) ⇒ (A).
2. Sharp \(b=0\) energy internal \(\equiv 0\) as geometric depletion.
3. Bounding \(T_{j\leftarrow j}\) by \(\dot e_j\), \(\dot Z\), or \(\Lambda'\).
4. Absolute-value Young as the same-scale attack.
5. Spectral-shift identity as Lemma★ or as transfer control.
6. \(\rho_j<\nu\) as absorption on the **energy** budget (\(\nu Z_j\) / \(\nu D_j\)).
7. “Axisymmetry alone ⇒ Door-1 \(T_{j\leftarrow j}\approx 0\) on mixed fields.”
8. Importing 2-D \(\rho\sim 0.02\) / occupancy into 3-D CFM.
9. Merging leftover-split strain, Ring/Paper2 SND, WRITE (6)/H1, Q6, or Lemma★ into this remainder.
10. Fake close / DA-VC-01 PASS / Clay claimed.

---

## KEEP inventory (already earned)

- Door-1 exact budget; remainder named \(T_{j\leftarrow j}\).
- Sharp \(b=0\) energy identity as **hygiene** (separates near-scale from false depleters).
- Signed \(\mathrm{Im}\) triad form; HH→L separated from same-scale.
- Far-shell Young templates (IR/UV); summability still open.
- Conditions (A)–(C) as **candidate** routes; Step 6 proposed IF (A).
- Conditional Gronwall \(\nu^1\) template under explicit [A\(_\varepsilon\)], [Poincaré-shell], [far], [no-cycle].
- Pure-swirl zero; mixed \(T^{\mathrm{mm}}\) bulk on compact samples.
- Harness + tests: `scripts/axisym_same_scale_tjj.py`, `domain_architect.axisym_same_scale_tjj`.

---

## DA-VC / route card — best next move

| Field | Value |
|---|---|
| **ID** | `DA-VC-ROUTE-θ→(A)` |
| **Parent** | DA-VC-01 (unaugmented NS) — status **FAIL** |
| **Class** | Axisym-with-swirl ∩ \([\theta\le\theta_\ast]\) (brackets mandatory) |
| **Quantity** | Near-scale / enstrophy \(T_{j\leftarrow j}\) (not sharp \(b=0\) energy zero) |
| **Remainder** | Still \(T_{j\leftarrow j}\) until (A) seats |
| **Experiment** | Palinstrophy-normalize the existing \(\theta\)-diagnostic; hunt a named proxy for \(\theta\) ≠ occupancy / \(\alpha\); attempt \(\varepsilon\nu P_j\) absorption with one \(\nu\) |
| **Pass for route** | Printed lemma-shaped (A) on \(\mathcal C_\theta\) with named \(\varepsilon,R\), no recycling |
| **Fail (expected default)** | \(\theta\) stays \(O(1)\) on mixed disks, or absorption demands \(\theta=O(\nu)\) |
| **DA-VC-01** | Remains **FAIL** until seating (A) *and* the lab gates (A5 \(T\), etc.) — seating (A) alone does not pass DA-VC-01 |
| **NS / Clay** | **NOT CLAIMED** even if the route passes |

**Status of this route card:** **OPEN / not seated.** Likely remains FAIL until (A) seats.

**Parallel TRY (do not block Rank 1):** sparse-support census (Rank 2) as a kill/search — either produces a thin invariant class or documents that near-scale fill-in is immediate.

---

## Coordination note

Sibling class-hunt / same-scale work lives on this branch tip (`72913ae` and later). Prefer structural analysis and **one** harness extension over thrashing estimate prose. Pull before edit; if dirty, wait. Cross-link Lemma★ only; do not merge five-lane stacks into Door-1.

---

## Sign-off

| Field | Value |
|---|---|
| Dream-team verdict | Rank 1 = \(\theta\)-class bridge to (A); Rank 2 = sparse support; Rank 3 = pure-swirl / small-data / extra symmetry as **conditional** only |
| (A) seated? | **No** |
| DA-VC-01 | **FAIL** |
| Clay | **NOT CLAIMED** |
| Fake close | **Refused** |
