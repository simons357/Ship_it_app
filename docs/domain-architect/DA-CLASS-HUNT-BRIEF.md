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

**Scope lock (Jonathan, 2026-10-01).** This class hunt concerns the **same-scale route**. It does **not** supply **WRITE (6)/H1**. See § What this is not.

Cross-link only to five-lane / Lemma★ (`cursor/ns-five-lane-lemma-star-1390`, PR #48). **Do not merge stacks.**

---

## What this is not

**Locked near-verbatim from Jonathan (2026-10-01).** Artifact: `/opt/cursor/artifacts/theta_lab_honesty/LOCK.md`.

The sharpest survivor (`enforced_alignment_theta`) has **three unresolved parts**:

1. **Wrong quantities for the desired bridge.** The disk template uses shell energy \(Z\) and \(D=\sum\lvert k\rvert^2\lvert\hat u_k\rvert^2\). That \(D\) is **not** palinstrophy.
2. **Assumed cancellation.** \(\theta=\lvert\sum c_\triangle\rvert/\sum\lvert c_\triangle\rvert\) measures cancellation in the tested transfers. Defining a class by small \(\theta\) does **not** prove NSE keeps solutions in that class.
3. **Unproved template constant.** `conditional_theta_bound()` calculates the proposed RHS; it does **not** establish a cutoff-uniform constant for the transfer bound.

So this is useful **conditional laboratory material**. The missing mathematics remains: an **enstrophy transfer** estimate, a **dynamical mechanism** that maintains its depletion, and **cross-scale assembly**.

For **WRITE (6)**, we still need the separate **bad-pair cylinder estimate**. Neither this template nor its passing tests proves that estimate. Cross-link: [`SND-AND-SIX.md`](SND-AND-SIX.md) (WRITE (6)/H1 = Bad-pair / \(A_{\mathrm{bad}}\) on \(Q_r\); **PARK / not proved**; SoT on `origin/cursor/tjj-estimate-chain-e5c5` `docs/WRITE_6.md`). Estimate Step 6 ≠ WRITE (6).

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

## Required structure (method lock)

**Standing rule (Jonathan):** *What doesn’t work is almost as important as what actually does work.*

This brief’s deliverable order is fixed:

1. **Dead ends first** (KILL map) — first-class, not an afterthought.
2. **Survivors next** (KEEP inventory, then ranked TRY/KEEP routes).

Do not invent math. Do not reopen a KILL as if it seats (A).

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

## Why axisymmetry alone failed on mixed fields

Axisymmetry-with-swirl is a **real geometry class**: it removes free helical HHH on fully 3-D wavevector configurations incompatible with rotation about \(z\), and restricts exact-disk probes to meridional \(k=(k_x,0,k_z)\) with swirl polarization \(\hat e_y\).

What it does **not** remove:

1. **Meridional self-stretch \(T^{\mathrm{mm}}\)** — on compact mixed swirl+meridional samples, \(T^{\mathrm{mm}}\) is the bulk of local \(T_{j\leftarrow j}\) (§7–§8 of the estimate note). Pure swirl (\(u^r=u^z=0\)) kills the pairing; mixed fields do not inherit that zero.
2. **Near-scale (\(b\ge 1\)) feeders** — sharp \(b=0\) energy telescope is an identity on a closed annulus; Door-1 with soft LP / \(b\ge 1\) leaks. Disk probe: \(\max\lvert T_{\mathrm{near}}\rvert/Z^{3/2}\) stays \(O(1)\) on axisym-restricted disks.
3. **Enstrophy same-scale** — does not inherit the energy triad telescope.

So “class (C) = axisymmetric-with-swirl” is the right *plant*, not a seated bound of the remainder. Route (C) alone ≠ (A).

---

## Survivors — KEEP inventory (already earned)

- Door-1 exact budget; remainder named \(T_{j\leftarrow j}\).
- Sharp \(b=0\) energy identity as **hygiene** (separates near-scale from false depleters).
- Signed \(\mathrm{Im}\) triad form; HH→L separated from same-scale.
- Far-shell Young templates (IR/UV); summability still open.
- Conditions (A)–(C) as **candidate** routes; Step 6 proposed IF (A).
- Conditional Gronwall \(\nu^1\) template under explicit [A\(_\varepsilon\)], [Poincaré-shell], [far], [no-cycle].
- Pure-swirl zero; mixed \(T^{\mathrm{mm}}\) bulk on compact samples.
- Harness + tests: `scripts/axisym_same_scale_tjj.py`, `domain_architect.axisym_same_scale_tjj`.

---

## Ranked routes to a usable CLASS for Door-1 / (A)

Marks: **KEEP** (in the program), **TRY** (next experiment / proof move), **KILL** (do not spend cycles as if they seat (A)).

### Rank 1 — Conditional \(\theta\)-class  ·  **KEEP-CONDITIONAL** (lab only) · **KILL** as bridge to (A)

**Class card.** \(\mathcal C_\theta=\{\)axisym-with-swirl fields with near-scale geometric factor \(\theta=\lvert\mathrm{signed}\rvert/\sum\lvert\mathrm{contrib}\rvert\le\theta_\ast\}\).

**What already sits.** Disk template (estimate § Same-scale): if \(\theta\le\theta_\ast\) then \(\lvert T_{\mathrm{near}}\rvert\le\theta_\ast C_{\mathrm{young}}\sqrt{D}\,Z\). **Not (A).** Letters are energy \(Z\) and \(D=\sum\lvert k\rvert^2\lvert\hat u\rvert^2\) — **\(D\) is not palinstrophy** (§ What this is not §1).

**Lab status** (`scripts/axisym_theta_bridge.py` · estimate § What this is not / § θ lab diagnostics).

1. Quantity mismatch stops any honest claim of a bridge to (A) — **PARTIAL/KILL as bridge**.
2. Lab probes under pretend Poincaré letters still need \(\theta_\ast=O(\nu)\) or \(O(\sqrt{\nu})\) — **KILL** as large-data geometry.
3. Natural proxy hunt: \(E_{\mathrm{mer}}/E\), unrestricted \(\theta\) — neither stays small on nonempty mixed class (**KILL**).
4. Defining \(\mathcal C_\theta\) by small \(\theta\) does **not** prove NSE invariance (§2). `conditional_theta_bound()` does **not** prove cutoff-uniform \(C\) (§3).

**Seating criterion.** Class control of \(\theta_\ast\) **plus** \(\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu P_j+R\) with named \(\varepsilon,R\) on **palinstrophy** letters. **Not met.** Wrong quantities alone already fail the criterion.

**KEEP.** The \(\theta\)-template as *conditional laboratory material* under enforced \([\theta]\).  
**KILL.** Treating \(\theta C\sqrt{D}\,Z\) as (A) or as a bridge to (A).  
**KILL.** Claiming this hunt supplies WRITE (6)/H1.

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
| **θ-bound conditional** (Rank 1) | Conditional lab class | KEEP-CONDITIONAL lab only; **not** (A); \(D\neq\) palinstrophy; WRITE (6) untouched |
| **Full axisym-with-swirl (no extra)** | Removes free HHH; leaves \(T^{\mathrm{mm}}\) + near-scale | **KEEP** as the plant. **KILL** as “already seats (A).” |

**Small-data honesty.** Small data can make \(\lvert T_{j\leftarrow j}\rvert\) absorbable because everything is small — that is **not** a depletion lemma and must not be sold as (B)⇒(A) on large data.

**Extra-symmetry honesty.** Compact-sample \(\overline\alpha\sim 0\) on mixed blobs did **not** kill \(T_{j\leftarrow j}\) (ratios \(O(10^{-3})\)). Alignment alone is insufficient; need a symmetry that removes meridional self-stretch or near-scale feeders.

---

## DA-VC / route card — Rank 1 θ lab (not a bridge; WRITE (6) untouched)

| Field | Value |
|---|---|
| **ID** | `DA-VC-ROUTE-θ-lab` |
| **Parent** | DA-VC-01 (unaugmented NS) — status **FAIL** |
| **Class** | Axisym-with-swirl ∩ \([\theta\le\theta_\ast]\) (brackets mandatory) |
| **Quantity** | Energy-disk near-scale diagnostic (\(Z\), non-palinstrophy \(D\)) — **not** (A) letters |
| **Remainder** | Still \(T_{j\leftarrow j}\) — (A) **not** seated; WRITE (6)/H1 **still open** |
| **Experiment** | Lab only: quantity mismatch filed; scaling probes under pretend letters; \(E_{\mathrm{mer}}/E\) proxy |
| **Pass for route** | Would need enstrophy transfer + dynamical depletion + cross-scale assembly — **not** disk \(\theta C\sqrt{D}Z\) |
| **Fail (recorded)** | Wrong quantities (\(D\neq\) palinstrophy); assumed cancellation; unproved template \(C\); pretend-letter absorption still \(O(\nu)\)/\(O(\sqrt{\nu})\) |
| **DA-VC-01** | Remains **FAIL** |
| **NS / Clay** | **NOT CLAIMED** |

**Status of this route card:** **PARTIAL/KILL as bridge to (A).** Template KEEP-CONDITIONAL as **lab material only**. Do not reopen as large-data (A). Does **not** touch WRITE (6).

**Next:** Missing math is enstrophy transfer, dynamical depletion mechanism, cross-scale assembly — **or** the separate bad-pair cylinder for WRITE (6). Do not recycle \(\dot e_j/\dot Z/\Lambda'\).

---

## Coordination note

Sibling class-hunt / same-scale work lives on this branch tip (`72913ae` and later). Prefer structural analysis and **one** harness extension over thrashing estimate prose. Pull before edit; if dirty, wait. Cross-link Lemma★ only; do not merge five-lane stacks into Door-1.

---

## Sign-off

| Field | Value |
|---|---|
| Dream-team verdict | Rank 1 θ = **lab only** (not (A); \(D\neq\) palinstrophy); Rank 2 sparse evolutionary **KILL** as mixed close; Rank 3 pure-swirl / small-data / extra symmetry **conditional** only |
| Executed KEEP/KILL | Estimate § Class hunt + § What this is not; `scripts/axisym_class_hunt.py`; `scripts/axisym_theta_bridge.py` (lab) |
| OOE / extra reflection | **KILL** as general seat (live parity keeps \(O(1)\) near-scale); empty-triad parities → sparse |
| Spectral gap | **KEEP-CONDITIONAL** energy Door-1 under hard gap; evolutionary **KILL**; enstrophy open |
| θ status | Conditional laboratory material; three unresolved parts; **not** a bridge to (A) |
| WRITE (6)/H1 | **Still open** (bad-pair cylinder); class hunt does **not** supply it |
| (A) seated? | **No** (only on trivial/conditional subclasses: pure-swirl identity, small data, fixed \(K_{\max}\)) |
| DA-VC-01 | **FAIL** |
| Clay | **NOT CLAIMED** |
| Fake close | **Refused** |
