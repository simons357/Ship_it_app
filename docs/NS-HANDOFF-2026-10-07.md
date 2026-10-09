# Navier–Stokes research update and cross-device handoff

**Prepared for Jonathan Simons — 7 October 2026**
(America/New_York coverage: Oct 5–7; emphasis Oct 6 and early Oct 7.)

**Purpose:** Self-contained update for other device conversations.
Does **not** auto-update those conversations or live research apps.

Vault filing of the user’s Oct 7 handoff text, with local
rerun tags where this agent re-executed finite checks.
PR #166 carries the independent-review package; PR #165
unchanged (write access denied on that chain).

---

## 1. Executive update

Strongest concrete progress: exact-shell geometry and shared
viscous budgets — from individual interactions to a controlled
union of **32** nonzero shape ratios and all positive integer
dilations. Central bookkeeping: how often the same dissipation
is charged when interactions overlap.

**ZIP status (corrected).** The package
`Shared-Budget-17-Family-Audit-and-9-25-Extension.zip` was
recovered and inspected in the source conversation (Oct 7);
`verify_families.py` passed there. **Other conversations should
stop treating retrieval of that ZIP as the current blocker.**

This agent workspace still lacks the binary bytes; finite
checks below were reimplemented from the handoff lists/faces
and rerun here (`scripts/ns_attacks/verify_families.py`).
That rerun confirms enumerations, overlap witness \(R=216\),
and weighted-face arithmetic. It is **not** a new independent
proof of every analytic inequality in the audit PDFs.

**Carry forward:**

- Original 17-shape family: scoped shared-budget argument,
  recorded **Proved at stated scope** in the recovered audit.
- +15 nonzero from anchors \((9,25)\) → controlled 32-shape union.
- Combined charge multiplicity: **6** before removing
  zero-transfer shapes, **4** afterward — different accountings,
  not contradictory.
- Sharper weighted coefficient:
  \(\rho+3\rho'\approx 3.1077752814793693\).
- Combined family has a stated high-pass cutoff making its
  **restricted** positive excess vanish — not full all-scalene.
- Exact regeneration: new high-frequency interactions are
  genuinely produced; positive transfer alone has not shown
  excess over viscosity.
- Phase experiments do **not** justify closing every
  phase-aware route. Coherent signs ≠ geometric-bound
  saturation.
- Separate swirl note: compression-vs-viscosity target open.
- Classical unaugmented regularity, criterion **(17)**, and
  swirl compression closure remain **unproved**.

---

## 2. Evidence labels

| Label | Meaning |
|---|---|
| **Rerun here** | Computation executed successfully in this agent filing |
| **Source-backed analytic result** | Source text supplies an argument; not fresh specialist certification of every step |
| **Reported result** | In conversation/source; not rerun here |
| **Conditional** | Follows if an additional estimate is supplied |
| **Open** | Needed estimate/bridge not established |

Audit label “Proved at stated scope” for the restricted-family
theorem is **preserved as the audit’s verdict**.

---

## 3. Exact 17/32-shape family

Shell label \(a\) means \(\lvert k\rvert^2=a\) — exact spheres,
not thick dyadic annuli.

### Original family — anchors \((5,25)\)

17 third-shell labels \(b\):

\[
8,10,14,18,20,22,24,26,30,34,36,38,40,42,46,50,52.
\]

Shapes \((5,b,25)\) and dilations \((5n^2,bn^2,25n^2)\),
\(n\in\mathbb N\).

### Added family — anchors \((9,25)\)

17 third-shell labels enumerated; **4** and **64** are
collinear zero-transfer endpoints. After removal, **15** active:

\[
6,10,12,14,16,24,30,34,38,44,52,54,56,58,62.
\]

Shapes \((9,b,25)\) and dilations. Union with the original
list = **32** nonzero shapes. A casual “37-shape” phrase in
phase discussion is **not** this package’s definition.

### Constants and overlap

| Quantity | Value | Evidence |
|---|---|---|
| Original \(\rho\) | \(0.6318550823987903\) | Reported (bundled script); face stored |
| Added \(\rho'\) | \(0.8253067330268596\) | Reported (bundled script); face stored |
| \(\rho+3\rho'\) | \(3.1077752814793693\) | **Rerun here** (face arithmetic) |
| Original individual multiplicity | 3 | **Rerun here** (scan) |
| Added active individual multiplicity | 3 | **Rerun here** (scan) |
| Combined literal multiplicity | 6 | **Reported** (witness \(R=14400\); charge-group definition in ZIP) |
| Combined zero-pruned multiplicity | 4 | **Rerun here** at \(R=216\) (exact four charges below) |

At physical squared radius **216**, the four charges
(**Rerun here**):

| Family anchor | Label | Dilation \(n\) | Physical \(R\) |
|---|---|---|---|
| 5 | 24 | 3 | 216 |
| 9 | 6 | 6 | 216 |
| 9 | 24 | 3 | 216 |
| 9 | 54 | 2 | 216 |

Repeated label **25** must still be counted separately when
charged by both families.

### High-pass (stated scope)

\[
\sum_{n\ge M}(H_{\mathrm{old},n}+H_{\mathrm{new},n})
\le
\frac{(\rho+3\rho')\sqrt{E_0}}{M}\,Y.
\]

For \(0<\eta<1\),

\[
M=\max\Bigl\{1,\Bigl\lceil
\frac{(\rho+3\rho')\sqrt{E_0}}{\eta\nu}
\Bigr\rceil\Bigr\},
\qquad
K=\max\{2,\ 3(M-1)\}.
\]

Restricted-family conclusion:

\[
\bigl[\mathcal T_{\mathrm{combined}}(P_{>K}u_N)-\eta\nu Y_N\bigr]_+=0.
\]

Pointwise-in-time for that selected family; other modes
allowed; **does not** control omitted shapes; **does not**
prove (17).

Original family’s smaller cutoff was
\(\max\{2,\sqrt5\,(M-1)\}\) — a **product**, not
\(\sqrt{5(M-1)}\). Do not reuse for the extension without proof.

---

## 4. Geometric constants — preserve normalization

- Fixed-output-shell convolution-square bound with **constant 3**
  remains valid under its hypotheses (diagonal ≤1, off-diagonal ≤2).
- Distinct-input sharpening → convolution-square **constant 2**.
- Triple-product factors after square root: \(\sqrt3\) and \(\sqrt2\).
- **Do not** call the triple-product factors “3 and 2” unless a
  different squared normalization is explicit.
- Package shape constants use \(\sqrt{3\Delta}\); displayed \(\rho\)
  were **not** silently recomputed with constant-2.

---

## 5. Phase cancellation — corrected conclusion

Narrowed from “dead end”:

- Experiments establish behavior of **tested configurations** only.
- \(R=\lvert\sum T_\sigma\rvert/\sum\lvert T_\sigma\rvert=1\) means
  common signs among nonzero contributions — **not** saturation of
  individual geometric bounds, hence **not** optimality of the
  shared-budget coefficient.
- Phase combinations are linear mod \(2\pi\); transfers are
  trigonometric / nonlinear in phases.
- Random cancellation: diagnostic, not worst-case theorem input.
- A coherent witness rules out a strict cancellation discount
  only at its demonstrated scope.
- Assembly obstruction \(2M^2\) vs \(2M\): warn against replacing
  square-of-sum by sum-of-squares (**Reported**; construction not
  rerun here).

**Current verdict:** blanket cancellation discount unjustified;
“all phase-aware estimates are dead” **also** unjustified.
Next signed test: exact-family optimization of signed transfer
against the **proposed budget**, one consistent divergence-free
real Fourier field.

---

## 6. Regeneration / two-shell / swirl (compact)

- Datum cutoff from \(\sigma_K(u_0)\) before evolution; Duhamel
  regeneration term remains the accumulation (**Source-backed** /
  prior filing).
- Two-shell signed \(\mathcal T=(b-a)J\) (**Source-backed**).
- Regeneration example \(E=14,X=20,Y=32\): full-field scalene
  \(28t+O(t^2)\); all-high \(K=2\) jet
  \((15084/1625)t^6+O(t^7)\) (**Reported**). Positive transfer ≠
  above-viscosity episode.
- Fixed-block \((5,8,25)\): damping \(38\nu\); integrable majorant
  at fixed-block scope — **not required** by 17/32 arguments.
- Swirl branch (axisymmetric \(\mathbb R^3\)): open target
  \(C_F\le\eta\nu D_F+BQ\) with independently integrable \(B\)
  (**Open**). Separate from periodic exact-shell family.

---

## 7. Current task list (Gates A–D)

**Program lock (7 Oct):**
[`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).
**Do not add further finite families.**

| Priority | Task | Status |
|---|---|---|
| **A** | As named by the sharp-band source | **Diagnostic and unresolved.** The \(L_{z_n}\) note is a separate load bound, not this closure ([`sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt`](sources/Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt)) |
| **B** | Shared-energy accounting | Not the band exponent ([`GATE-B-SHARED-ENERGY.md`](GATE-B-SHARED-ENERGY.md)) |
| **C** | Sharp instantaneous signed band | **CLOSED — optimal wavenumber exponent \(1/2\)**. Gate A is not a premise. (17) not established ([`GATE-C-HALF-DERIVATIVE.md`](GATE-C-HALF-DERIVATIVE.md)) |
| **D** | Episode control and recurrence funding | **OPEN** ([`GATE-D-REVIEW.md`](GATE-D-REVIEW.md)): both \(B_I\le C\mathcal R_I\) and \(\sum\mathcal R_I\le C_{\mathrm{data},\nu,T}\). A completed finite episode can support this and cannot establish cutoff-uniform control or summable recurrence |
| Parked | 52/70/100 family extensions; random-phase fishing; Ring without bridge | — |

Spectral target remains (15)–(17) on all-high scalene; a
32-family sub-sum does **not** establish that full expression.

---

## 8. Compact paste for other conversations

As of early October 7, 2026, active focus is exact-shell
geometry plus viscous smoothing, with a separate axisymmetric
signed-compression branch. The 17/32 shared-budget ZIP has been
recovered (source conversation) and its bundled verification
passed there; this vault reimplements finite checks from the
handoff lists. Active families: \((5,b,25)\) for 17 listed \(b\),
and \((9,b,25)\) for 15 nonzero \(b\), with all integer dilations.
Combined charge multiplicity exactly 4 after removing
zero-transfer endpoints 4 and 64; weighted coefficient
\(\rho+3\rho'\approx 3.1077752814793693\). Restricted high-pass
absorption with \(K=\max\{2,3(M-1)\}\). Does **not** prove
all-scalene criterion (17). Regeneration is real; neither jet
establishes an above-viscosity episode. Phase ratio 1 means
common signs, not geometric-bound saturation — do not label all
signed/phase-aware routes dead. Swirl open target: delayed
same-solution compression control. Ring is spatial only. No full
regularity or novelty claim.

---

## STATUS

ZIP RETRIEVAL: NO LONGER THE RESEARCH BLOCKER (RECOVERED IN SOURCE CONVERSATION).
17/32 FINITE CHECKS: RERUN HERE (lists, R=216×4, ρ+3ρ′, individual mult 3).
GATE A: DIAGNOSTIC AND UNRESOLVED IN THE SHARP-BAND SOURCE.
GATE C: CLOSED FOR THE SHARP INSTANTANEOUS SIGNED BAND — OPTIMAL WAVENUMBER EXPONENT \(1/2\).
GATE A: UNRESOLVED — NOT A PREMISE.
GATE D: OPEN ON EPISODE CONTROL AND RECURRENCE FUNDING.
(17) NOT ESTABLISHED.
RESTRICTED-FAMILY THEOREM: PROVED AT STATED SCOPE (AUDIT VERDICT).
(17) / CLAY / SWIRL CLOSURE: OPEN.
PHASE: NARROWED — NOT A BLANKET DEAD END.
PR #165: UNCHANGED.
NS NOT SOLVED.
