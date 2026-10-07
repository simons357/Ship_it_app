# Navier–Stokes research update and cross-device handoff

**Prepared for Jonathan Simons — 7 October 2026, America/New_York**  
**Coverage:** October 5–7, with emphasis on October 6 and the early-morning October 7 session.  
**Purpose:** A self-contained update to upload into other phone conversations. This report does not automatically update those conversations or the live research apps.

**Repo filing note (Cursor cloud, same date):** Archived under `docs/ns-review/`. Companion Grok paste file: `NS-Research-Update-2026-10-07.md`. Shared-budget branch: `cursor/shared-budget-32-shape-c3ed` (PR #166).

---

## 1. Executive update

The strongest concrete progress is in exact-shell geometry and shared viscous budgets. The research has moved from individual interactions to a controlled union of **32 nonzero shape ratios** and all their positive integer dilations. The central bookkeeping question is how often the same dissipation is charged when these interactions overlap.

An important October 7 development: the previously missing `Shared-Budget-17-Family-Audit-and-9-25-Extension.zip` was found, downloaded, and inspected. Its verification script was rerun successfully. **Other conversations should stop treating retrieval of that ZIP as the current blocker.**

The rerun confirms the finite enumerations, determinant checks, overlap witnesses, and displayed constants encoded in the supplied script. It is **not** a new independent proof of every analytic inequality in the accompanying audit.

### Main results to carry forward

- The original **17-shape** family has a scoped shared-budget argument, recorded as **proved** in the recovered audit.
- Adding **15 nonzero** shapes from anchors \((9,25)\) gives the controlled **32-shape** union.
- Combined charge multiplicity is **6** before removing zero-transfer shapes, **4** afterward. Both numbers refer to specific accounting definitions; they are not contradictory.
- The sharper weighted coefficient is \(\rho + 3\rho' \approx 3.1077752814793693\).
- The combined family has a stated high-pass cutoff that makes its restricted positive excess vanish. This does **not** cover the full all-scalene transfer.
- Exact regeneration calculations show that new high-frequency interactions are genuinely produced. Positive transfer alone has **not** demonstrated an excess over viscosity.
- The phase experiments do **not** justify closing every phase-aware route. Coherent signs and saturation of a geometric bound are different questions.
- A separate swirl note supplies a detailed compression-versus-viscosity target and identifies several shortcuts that fail. Its proposed closure remains **open**.

Classical unaugmented Navier–Stokes regularity, the all-shape criterion **(17)**, and the swirl compression closure remain **unproved** by this work.

---

## 2. Evidence labels used here

| Label | Meaning |
|---|---|
| **Rerun here** | The supplied computation was executed successfully during preparation of this report. |
| **Source-backed analytic result** | The source text was read and supplies an argument; this report does not claim a fresh specialist certification of every step. |
| **Reported result** | Present in the conversation or source report, but its underlying calculation was not rerun here. |
| **Conditional** | A stated conclusion follows if an additional estimate is supplied. |
| **Open** | The needed estimate or bridge has not been established. |

The recovered audit labels its restricted-family theorem “Proved at stated scope.” That label is preserved as the audit’s verdict. Today’s independent action was retrieval, source inspection, and a rerun of the bundled finite checks.

---

## 3. Chronology: what changed

### October 5 background

The recent work clarified the distinction between corrected spatial Ring estimates and a dynamical regularity argument. Work on \(L^3\)/C10 focused on controlling nonlinear production over time rather than inferring regularity from a snapshot. Exact two-shell regeneration was being developed, and the need to count shared dissipation across many blocks became central.

These are background developments from the recent record, not new proofs certified in this report.

### October 6: substantive source results

1. The datum-selected cutoff and complete two-shell signed assembly were written explicitly.
2. The regeneration example separated a full-field scalene derivative from the later all-high scalene jet.
3. The 17-family shared-energy audit and \((9,25)\) extension supplied exact overlap counts and a common high-pass cutoff.
4. The swirl bench note developed conditional source absorption, concentration tests, a coupled local NSE initial-layer argument, and the signed compression target.

### October 7: corrections and verified handoff progress

1. The conclusion “phase cancellation is a dead end” was narrowed: the experiments only establish the behavior of their tested configurations.
2. It was clarified that a phase-to-transfer map is nonlinear, although phase combinations themselves are linear modulo \(2\pi\).
3. The Ring explanation was corrected to emphasize **spatial** variation, not a time-speed limit or a force acting on fluid.
4. The working focus was stated as geometry plus viscous smoothing, while keeping the spectral and axisymmetric branches distinct.
5. The complete supplied swirl note was read in this conversation.
6. The supposedly missing shared-budget ZIP was recovered, and `verify_families.py` passed.

---

## 4. Exact 17/32-shape family: now available

Shell labels below are **squared radii**, so shell \(a\) means \(|k|^2=a\). These are exact spheres, not broad dyadic annuli.

### Original family

Anchor squared radii are \((5,25)\). The 17 third-shell labels are:

\[
8,\;10,\;14,\;18,\;20,\;22,\;24,\;26,\;30,\;
34,\;36,\;38,\;40,\;42,\;46,\;50,\;52
\]

The corresponding shapes are \((5,b,25)\), and the covered dilations are \((5n^2,bn^2,25n^2)\) for positive integers \(n\).

### Added family

Anchor squared radii are \((9,25)\). Enumeration gives 17 third-shell labels, but **4** and **64** are collinear, identically zero-transfer endpoints. After removing those two, the **15 active** labels are:

\[
6,\;10,\;12,\;14,\;16,\;24,\;30,\;34,\;
38,\;44,\;52,\;54,\;56,\;58,\;62
\]

The added shapes are \((9,b,25)\) and their integer dilations. Together the two lists define the **32-shape** union. A passing reference to a “37-shape” family in the phase discussion is **not** a definition of this recovered package and should not be substituted for it.

### Constants and overlap

| Quantity | Value | Evidence |
|---|---|---|
| Original \(\rho\) | \(0.6318550823987903\) | Recomputed by bundled script |
| Added \(\rho'\) | \(0.8253067330268596\) | Recomputed by bundled script |
| Original individual multiplicity | \(3\) | Exact enumeration/grouping check |
| Added active individual multiplicity | \(3\) | Exact enumeration/grouping check |
| Combined literal multiplicity | \(6\) | Exact witness at squared radius \(14400\) |
| Combined zero-pruned multiplicity | \(4\) | Exact witnesses at squared radii \(216\) and \(3600\) |
| Weighted combined charge \(\rho+3\rho'\) | \(3.1077752814793693\) | Recomputed from the charge groups |

At physical squared radius \(216\), the four charges are:

| Family anchor | Label | Dilation \(n\) | Physical squared radius |
|---|---|---|---|
| \(5\) | \(24\) | \(3\) | \(216\) |
| \(9\) | \(6\) | \(6\) | \(216\) |
| \(9\) | \(24\) | \(3\) | \(216\) |
| \(9\) | \(54\) | \(2\) | \(216\) |

This explains the practical gain: we can bound how often these families spend the same dissipation. The repeated label \(25\) must still be counted separately when charged by both families.

### High-pass result and its exact scope

The audit supplies a tail estimate of the form

\[
\sum_{n\ge M}(H_{\mathrm{old},n}+H_{\mathrm{new},n})
\le \frac{(\rho+3\rho')\sqrt{E_0}}{M}\,Y.
\]

For \(0<\eta<1\), take

\[
M=\max\left\{1,\left\lceil
\frac{(\rho+3\rho')\sqrt{E_0}}{\eta\nu}
\right\rceil\right\},
\qquad K=\max\{2,3(M-1)\}.
\]

The stated restricted-family conclusion is

\[
\bigl[\mathcal T_{\mathrm{combined}}(P_{>K}u_N)-\eta\nu Y_N\bigr]_+=0.
\]

This is a **pointwise-in-time** statement for that selected family, with arbitrary other modes allowed in the underlying solution. It does **not** require the solution to remain supported on those shapes. It also does **not** control omitted shapes.

The original family’s smaller cutoff was \(\max\{2,\sqrt5\,(M-1)\}\) — a product, not \(\sqrt{5(M-1)}\). Do **not** reuse that smaller cutoff for the extension without proof.

**Why this matters:** a finite list of shape ratios can cover infinitely many scales with controlled charges.  
**What remains:** enlarging the coverage without losing summability of the aggregate charges, or obtaining a stronger signed estimate for the omitted interactions.

---

## 5. Geometric constants: preserve the normalization

The recovered audit retains the original fixed-output-shell convolution-square bound with constant **3**. Its mechanism is a diagonal contribution at most \(1\) and an off-diagonal contribution at most \(2\). Two independent planes intersect an output sphere in at most two points; nonzero plane constants exclude the antipodal exception.

A largest-output convention safely supplies the nonzero plane constants. The actual hypotheses, not the convention alone, matter when relabeling.

After taking a square root and pairing with the third shell, the corresponding scalar triple-product factor is \(\sqrt3\). A distinct-input sharpening to a convolution-square constant \(2\) would give \(\sqrt2\) at that same step.

**Correction for cross-device summaries:** do not call the triple-product factors “3 and 2” unless a different squared normalization is explicitly being used. The recovered package’s shape constants use \(\sqrt{3\Delta}\). Its displayed \(\rho\) values were not silently recomputed using the sharper constant-2 lemma.

---

## 6. Datum cutoff and signed two-shell assembly

The October 6 source defines the cutoff from the **initial datum**, before estimating the future solution. With

\[
\sigma_K(u_0)^2=\sum_{|k|>K}|k|\,|\widehat u_0(k)|^2,
\]

choose a finite \(K\) making \(C_0\sigma_K(u_0)\le c\nu/2\). A sufficient integer cutoff follows from \(\sigma_K^2\le X(u_0)/K\). No unknown future maximum of \(X\) is used.

The exact Duhamel formula splits the high-frequency tail into a heat-evolved initial tail and a nonlinear regeneration term. Heat contraction controls the first. The unresolved accumulation sits in the second. A small initial tail does **not** establish persistence of smallness.

For a snapshot \(u=v+w\) with \(Av=av\), \(Aw=bw\), and \(0<a<b\), define

\[
j_{b\leftarrow aa}=-\langle B(v,v),w\rangle,
\quad j_{a\leftarrow bb}=-\langle B(w,w),v\rangle,
\quad J=j_{b\leftarrow aa}-j_{a\leftarrow bb}.
\]

The complete signed enstrophy transfer is

\[
\mathcal T(u)=(b-a)J.
\]

Mixed-input contributions are included through the signed identity; they are not an extra omitted block. The source also gives the centered identity

\[
\mathcal T_c=(b-a)(a+b-\Lambda)J,
\qquad \Lambda=Y/X.
\]

These are spatial identities, not a replacement for the all-high time budget. A single exact sphere has zero instantaneous total enstrophy transfer, even though its nonlinearity can generate other spheres.

---

## 7. Regeneration: what the exact example shows

The read source reports a divergence-free two-sphere datum with

\[
E=14,\quad X=20,\quad Y=32,\quad J=4,\quad\mathcal T=4.
\]

It generates the initially absent mode \((2,1,0)\), of squared radius \(5\), immediately. The two distinct transfer statements are:

| Object | Reported leading term | Meaning |
|---|---|---|
| Full-field scalene transfer | \(28t+O(t^2)\) | Three-radius transfer appears in the full field |
| All-high scalene transfer with \(K=2\) | \((15084/1625)t^6+O(t^7)\) | Genuine transfer among regenerated high modes appears later in the local expansion |

The all-high leading contribution comes from squared-radius blocks \((5,8,25)\) and \((5,10,25)\). The source reports viscosity independence of the leading coefficient. The earlier handoff also reports agreement for Galerkin cutoffs \(N\ge5\); the jet computation was not rerun for this report, and a uniform remainder estimate is not being asserted.

**Essential distinction:** positive nonlinear transfer does **not** mean transfer exceeds the viscous allowance. The supplied account says the positive excess is zero sufficiently near the initial time for the filed example. Neither leading coefficient disproves criterion **(17)**.

The separate fixed-block forcing audit reports an identity with damping \(38\nu\) for the \((5,8,25)\) transfer and an integrable forcing majorant. The rerun confirms its finite census: **24 triads** and maximum mode incidences \((1,2,1)\). Its lifted-incidence scope must not be promoted to arbitrary newly populated full shells at larger dilation.

---

## 8. Phase cancellation: today’s corrected conclusion

The pasted phase report describes strong cancellation for random independent triads and a ratio of \(1\) for some coherent shared-mode examples. Its synthetic 32-shape experiment was performed **before** the exact list was available to that test.

Two reported random ratios, approximately \(0.0012\) and \(0.04\), appear in different passages. They cannot be treated as one reproducible benchmark without the seeds, amplitudes, normalization, and code. No reconciliation or rerun was performed here.

For nonzero denominator,

\[
R=\frac{\lvert\sum_\sigma T_\sigma\rvert}{\sum_\sigma\lvert T_\sigma\rvert}=1
\]

means the nonzero real contributions have a **common sign**. It does **not** mean they simultaneously saturate the individual geometric upper bounds. It therefore does **not** establish optimality of the shared-budget coefficient.

Other corrections to retain:

- Phase alignment maximizes a fixed complex contribution’s real projection; it does not by itself prove sharpness of all geometric and polarization inequalities.
- Triad phase combinations are linear modulo \(2\pi\); transfers involve trigonometric functions and are **not** a linear map of phases.
- Random cancellation is diagnostic evidence, not a worst-case theorem input.
- A coherent witness rules out a strict cancellation discount only at its demonstrated scope.
- The reported assembly obstruction \(2M^2\) versus \(2M\) warns against replacing a square of a sum by a sum of squares; its underlying construction was not rerun here.

**Current verdict:** a blanket cancellation discount is unjustified, but “all phase-aware estimates are dead” is also unjustified. An exact-family optimization should compare signed transfer against the actual proposed budget, preserving one consistent divergence-free real Fourier field.

---

## 9. Separate axisymmetric swirl branch

The supplied swirl note is titled “DA swirl: first probe of four open mechanisms,” dated October 6. It concerns smooth axisymmetric fields on \(\mathbb{R}^3\), with physical measure \(dx=2\pi r\,dr\,dz\). This is a **different setting** from the periodic exact-shell family.

Its variables are

\[
F=u^\theta/r,\quad G=\omega^\theta/r,\quad
\Gamma=ru^\theta,\quad U=u^r/r.
\]

### Conditional source absorption

The \(G\) energy identity has a source \(-\int G_z F^2\,dx\). Young’s inequality gives

\[
\left|\int G_zF^2\,dx\right|
\le\eta\nu\int|G_z|^2\,dx
+\frac1{4\eta\nu}\int|F|^4\,dx.
\]

Thus a supplied spacetime \(L^4\) bound for \(F\) pays this source. It does **not** prove that NSE supplies that bound. Local cutoffs introduce additional source and transport/diffusion terms, all of which must be retained.

### Concentration tests

The note uses smooth pure-swirl Gaussian initial data

\[
u_\varepsilon=a_\varepsilon e^{-|x|^2/\varepsilon^2}(-y,x,0),
\qquad a_\varepsilon=\varepsilon^{-3/2}.
\]

Its stated exact formulas give energy of order \(\varepsilon^2\), bounded initial gradient energy, circulation maximum of order \(\varepsilon^{1/2}\), but instantaneous \(\int F^4\) of order \(\varepsilon^{-3}\).

The passive heat model has an integrated cost of order \(1/(\nu\varepsilon)\). More significantly, Section 7 supplies a local coupled NSE perturbation argument retaining a lower bound \(c_0/(\nu\varepsilon)\) on a shrinking initial interval, with \(c_0\approx3.53926394\times10^{-5}\).

This is a source-backed analytic proposition. Its conclusion concerns lack of a uniform initial-layer bound across changing data under the listed low-order upper bounds. It does **not** show infinite cost for one smooth datum, a late-time singularity, or failure of a delayed estimate.

### First coupled response has both signs

The source derives \(\partial_t U(0,0,0)=a^2/5>0\), so the initial central response is radial expansion, favorable to reducing \(F\). Farther along the axis the response changes sign. The reported first zero is at \(|z|/\varepsilon\approx0.6067752158654651\). These are initial derivatives, not a global favorable-sign theorem.

### The actual open target

The global quartic identity in the note is

\[
\frac14 Q'+\nu D_F=C_F,
\quad Q=\int F^4\,dx,
\]

\[
D_F=3\int F^2|\nabla F|^2\,dx+\pi\int F(0,z)^4\,dz,
\qquad C_F=-2\int U F^4\,dx.
\]

The proposed sufficient estimate is

\[
C_F\le\eta\nu D_F+B(t)Q,\qquad 0\le\eta<1,
\]

with an independently controlled integral of \(B\) over a delayed interval \([t_0,T]\). Assuming it, one obtains

\[
Q(t)\le Q(t_0)\exp\left(4\int_{t_0}^t B(s)\,ds\right).
\]

The needed bound on \(B\) remains **open**. Defining it from the uncontrolled excess itself would be circular. Pure instantaneous absorption for all data fails the note’s amplitude-scaling test: compression scales as \(M^5\), while this dissipation scales as \(M^4\).

The note excludes none of its four receiving/recession endpoints. It also says the original swirl-note localization conventions still need recovery. External papers cited there were not independently checked for this handoff; their claims should not be described as audited here.

*(Cursor cloud spot-check, separate session: Gaussian \(E,Q\), axis zero, \(m_0/c_0\), amplitude kill — see `DA-SWIRL-FOUR-DOORS-2026-10-06.md`.)*

---

## 10. Ring geometry and the meaning of “heat”

The displayed Ring discussion concerns a **band-limited spatial snapshot**. Under its fixed-domain normalization, a frequency cutoff \(L\) gives a gradient estimate of order \(L^{5/2}\|\omega\|_2\). Where \(|\omega|\ge c\|\omega\|_2\), division by \(|\omega|\) gives a direction-gradient ceiling of order \(L^{5/2}/c\).

This limits how sharply rotation directions change across **space**. It does **not** itself control future evolution, preserve the strong set, or supply the missing transfer budget. The stronger peak-relative hypothesis belongs to a different, linear-in-\(L\) estimate.

“Geometry and heat” means geometric restrictions on nonlinear interactions plus viscosity’s heat-like smoothing. It does **not** mean a new thermal forcing term. The Ring estimate remains a potential supporting tool until a specific bridge into the required budget is proved. No new novelty or publication-readiness verdict was established today.

---

## 11. Current task list

| Priority | Task | Completion criterion |
|---|---|---|
| 1 | Finish independent analytic review of recovered 32-family package | Check constants, overlap, and common cutoff against the primary manuscript; preserve exact scope |
| 2 | Test exact-family signed efficiency | Optimize signed transfer relative to the proposed budget with reality and divergence-free constraints; label finite searches numerical |
| 3 | Address extension beyond selected families | Supply a summable all-family charge rule or an alternative signed bound |
| 4 | Continue all-high regeneration budget work | Bound accumulated excess, including repeated events, uniformly in Galerkin cutoff |
| 5 | Audit the swirl note’s coupled lower-bound argument | Check normalization, local existence/closeness, and allowed dependence of constants |
| 6 | Attack delayed swirl compression | Control \(B\) from already controlled data of the same solution, with localization costs paid |

The exact spectral target recorded in the read source remains

\[
\sup_N\int_0^T
\frac{[\mathcal T_{\mathrm{sc}}(P_{>K}u_N)-\nu Y_N/4]_+}{X_N}\,dt,
\]

with a fixed datum-selected cutoff and the source’s zero-solution convention. A bound for the 32-family sub-sum does **not** establish this full expression.

---

## 12. Source and reproducibility record

### Read directly for this update

1. Pasted swirl note — complete October 6 swirl note, including Sections 6–9. Library ID: `libfile_d0d9719f8ed48191a06c0517d4ac167e`.
2. Pasted text — October 6 datum-cutoff/two-shell source, including all-high follow-up. Library ID: `libfile_7bef94b714f881918da026a857c7fb8b`.
3. Pasted markdown — earlier version of the datum-cutoff/two-shell note. Library ID: `libfile_35b71c6e78a88191b8cb5d7f76b2d733`.
4. `Shared-Budget-17-Family-Audit-and-9-25-Extension.zip` — recovered October 7. Library ID: `libfile_e69ca0f14ab4819186900a547b61df20`.
5. The user’s pasted phase exploration and reported PR #166 / commit `888c3343`. The PR was not independently opened or rerun for that Library report.

### Recovered archive contents

- `AUDIT-AND-HANDOFF.txt`
- `family-results.json`
- `shape-constants.csv`
- `verify_families.py`

**Execution:** `python3 verify_families.py` completed successfully on October 7. Integer/Fraction checks cover enumerations, determinants, overlap witnesses, and the fixed-block incidence census. Radical expressions define the mathematical constants; floating-point evaluations provide the displayed decimals.

The archive’s audit cites `Shared-Energy-Time-Bound.pdf` and `Block-5825-Review.pdf` as its primary source papers. Those PDFs were not independently re-audited in full for this handoff. The earlier claim that the package could not be found is **superseded** by its successful recovery.

**Cursor-cloud workspace note:** as of filing this markdown into the git branch, the ZIP binary itself may still need to be committed into the repo for agents without Library access. PR #166 currently holds the cover note / extension desk / constants face-check; treat Library recovery as authoritative for phone Grok until the binary is mirrored in-repo.

---

## 13. Compact handoff to paste into another conversation

As of early October 7, 2026, our active focus is exact-shell geometry plus viscous smoothing, with a separate axisymmetric signed-compression branch. The 17/32 shared-budget ZIP has now been recovered and its bundled verification script passes. The active families are \((5,b,25)\) for 17 listed \(b\) values and \((9,b,25)\) for 15 nonzero \(b\) values, with all integer dilations. Combined charge multiplicity is exactly 4 after removing the zero-transfer endpoints 4 and 64; the weighted coefficient is \(\rho+3\rho'\approx 3.1077752814793693\). The recovered audit states restricted high-pass absorption with \(K=\max\{2,3(M-1)\}\). This does not prove all-scalene criterion (17). Regeneration is real: the full-field scalene term begins at \(28t\), while the \(K=2\) all-high term begins at \((15084/1625)t^6\); neither establishes an above-viscosity episode. Phase ratio 1 means common signs, not geometric-bound saturation, so do not label all signed/phase-aware routes dead. The swirl note’s remaining target is delayed same-solution compression control \(C_F\le\eta\nu D_F+BQ\) with independently integrable \(B\) and paid localization terms. The Ring result is spatial only. Preserve reported-versus-rerun labels; no full regularity or novelty claim has been established.

---

*End of cross-device handoff.*
