# Axisymmetric-with-swirl shell estimate

**Filter:** [`docs/domain-architect/AXISYMMETRIC-SHELL-AUDIT.md`](../../domain-architect/AXISYMMETRIC-SHELL-AUDIT.md)  
**Predecessor (11 Sept, not this HEAD):** `origin/cursor/tjj-estimate-chain-e5c5` — `docs/ESTIMATE-AUDIT.md`, `docs/AXISYM-SHELL.md`, `docs/TJJ-ESTIMATE.md`, `docs/AXISYM-SWIRL-PROBE.md`.  
**Date:** 2026-09-12  
**Status:** OPEN. Remainder \(T_{j\leftarrow j}\) is still open. Far-shell Young sits. The requested local Young is **REFUSED**. Compact-sample ratios are not a class \(\rho_j\). Clay is **NOT CLAIMED**. Unconditional 3-D regularity is **NOT CLAIMED**. DA-VC-01 stays **FAIL**.

Class: unaugmented axisymmetric Navier–Stokes with swirl. Quantity: dyadic shell block \(Z_j\). Remainder after the Door-1 budget: intra-shell transfer \(T_{j\leftarrow j}\). Assumed, in brackets: [smooth compactly supported divergence-free axisymmetric-with-swirl solutions of classical NS; no added field; unaugmented normalization; pairing identity closed only when the stepper and the diagnostic agree to \(10^{-16}\)].

This note uses **only** KEEP objects from the audit. Discard items do not appear in the identity, the Young step, or the claim. Parked stacks stay parked.

Swirl \(\Phi=u_\theta/r\) is not FRA/DA \(\Phi\), not Newtonian \(\Phi_g\), and not Paper2 \(\Phi_j\). This remainder is **not** leftover-split strain \(\int\|u^r/r\|_\infty\,dt\) and **not** Paper2 simplex \(\|a-\mu\|_{\ell^1}\).

Two shells stay labeled and are not glued. **Energy** \(Z_j=\tfrac12\|P_j u\|_{L^2}^2\) is the displayed §1 quantity (\(P_j\) here is the Littlewood–Paley projector). **Enstrophy** \(Z_j=\|\Delta_j\omega\|_{L^2}^2\) is the Sept 11 write. Palinstrophy \(P_j\) in Status / Terminology / Scope below is **not** the LP projector. The leftover print \(T_{j\leftarrow j}/Z_j\) is **not** the palinstrophy-normalized \(\rho_j\) of route (A).

---

## Status / Terminology / Scope

**Locked / filed 13 September 2026.** Standing honesty language for this shell-budget chain. **NS not solved.** No proofs are invented here.

Class: unaugmented axisymmetric-with-swirl. Quantity: the labeled shell in use. Remainder: \(T_{j\leftarrow j}\). Assumed: [these five blocks are standing language for this program; they do not close the leftover].

**Terminology.** We call the exact bookkeeping relation the **spectral-shift identity**. It is distinct from the **Lemma★ ratio bound** discussed in earlier attack notes. Establishing the identity does not establish that bound or control nonlinear transfer.

*(Cross-link only: Lemma★ SoT lives on branch `cursor/ns-five-lane-lemma-star-1390` / PR https://github.com/simons357/Ship_it_app/pull/48 (`docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`). Do not conflate.)*

**Dissipation threshold.** Because \(\rho_j\) is normalized by palinstrophy \(P_j\), the comparison \(\rho_j<\nu\) belongs to the enstrophy–palinstrophy estimate in (A). It is not an absorption criterion for the displayed shell-energy budget, whose viscous term is \(\nu Z_j\).

**Cross-scale terms.** This program proposes to handle cross-scale interactions using standard estimates. Their precise bounds and summability remain to be supplied within this chain; they are not established by this note.

**Remaining closure.** Conditions (A)–(C) describe candidate routes for completing this particular proof chain. The principal unresolved term is the same-scale transfer \(T_{j\leftarrow j}\). Step 6 describes a proposed closure mechanism: it requires (A), or a depletion estimate implying (A), without using \(\dot e_j\), \(\dot Z\) or \(\Lambda'\) to reintroduce the quantity being bounded.

**Scope of computations.** The reported measurements concern small exact disks and the stated restricted classes. They establish no uniform conclusion as \(K_{\max}\to\infty\) or for generic data. Observed occupancy \(1\) alongside alignment approximately \(1/2\) does not establish the depletion required for closure.

Letters, so they do not glue: LP projector \(P_j\) in §1 \(\neq\) palinstrophy \(P_j\) in (A). Energy \(Z_j=\tfrac12\|P_j u\|_{L^2}^2\) \(\neq\) enstrophy \(Z_j=\|\Delta_j\omega\|_{L^2}^2\). The §1 pairing writes dissipation as \(\nu D_j=\nu\|\nabla P_j u\|_{L^2}^2\). Whether one writes that slot as \(\nu D_j\) or as \(\nu Z_j\), \(\rho_j<\nu\) is still not absorption on the energy budget.

---

## 1. Identity first

Class: unaugmented axisymmetric Navier–Stokes with swirl,
\(u=u^r(r,z)\,e_r+u^\theta(r,z)\,e_\theta+u^z(r,z)\,e_z\).
Quantity: the energy shell
\[
Z_j(t)
:=
\tfrac12\|P_j u(t)\|_{L^2}^2,
\]
with \(P_j\) the Littlewood–Paley projector onto frequencies \(\sim 2^j\).
(The Sept 11 enstrophy shell \(Z_j=\|\Delta_j\omega\|_{L^2}^2\), \(\omega=\nabla\times u\), is a different quantity. Using it changes the global sum, which then equals stretching, not zero. This note takes the energy shell as the displayed quantity so that the telescope below is the energy pairing. Do not glue the two \(Z_j\)’s.)
Remainder: \(T_{j\leftarrow j}\).
Assumed: [smooth compactly supported divergence-free axisymmetric-with-swirl classical NS; \(P_j\) a Fourier multiplier, self-adjoint, commuting with derivatives, and preserving divergence-free fields; no added field].

The momentum equation paired with \(P_j u\) drops pressure
(\(\langle P_j\nabla p,\,P_j u\rangle=0\)) and gives
\[
\dot Z_j
=
-\bigl\langle P_j(u\cdot\nabla u),\,P_j u\bigr\rangle
-
\nu\|\nabla P_j u\|_{L^2}^2.
\]

Insert the LP partition of unity \(I=\sum_\ell P_\ell\)
(coarse mass \(P_{<j_0}\) is a finite set of low shells, not the remainder)
and name the bilinear pieces
\[
T_{j\leftarrow \ell m}
:=
-\bigl\langle P_j\bigl((P_\ell u)\cdot\nabla(P_m u)\bigr),\,P_j u\bigr\rangle,
\qquad
D_j
:=
\|\nabla P_j u\|_{L^2}^2\ge 0.
\]

Let \(b\in\mathbb{N}\cup\{0\}\) be a **named locality width**. It is a grouping cutoff, not a smallness, and this note does not assign it a value that bounds the remainder. The Door-1 split is
\[
T_{j\leftarrow j}
:=
\sum_{\lvert\ell-j\rvert\le b,\;\lvert m-j\rvert\le b}
T_{j\leftarrow \ell m},
\qquad
T_{j\leftarrow\neq j}
:=
\sum_{\lvert\ell-j\rvert>b\text{ or }\lvert m-j\rvert>b}
T_{j\leftarrow \ell m}.
\]

Then the exact Door-1 shell budget is the partition
\[
\dot Z_j
=
T_{j\leftarrow\neq j}
+
T_{j\leftarrow j}
-
\nu D_j.
\]

\(-\nu D_j\) cannot grow \(Z_j\). \(T_{j\leftarrow\neq j}\) is moved by the budget: it is flux among shells, and the nonlinear pairing sums to zero on the energy (the telescope). **The one term that can grow the quantity is \(T_{j\leftarrow j}\).**

It is not bounded here. It is not bounded by \(\dot Z_j\), by \(\Lambda'\), or by a new symbol of the same size.

Door 1: after the budget, **the only remainder is \(T_{j\leftarrow j}\)**.

---

## 2. Bookkeeping that is not the final left-hand side

\[
\Lambda'=\frac{2(T_c-\nu D_s)}{X}
\]

is bookkeeping for signed production versus dissipation. It is **not** the final left-hand side of this estimate. If the pairing identity is not closed in the time series, **do not quote the sign of \(\Lambda'\)**. This environment has no closed time-series stepper, so the sign is **not quoted**.

---

## 3. Spectral-shift identity (bookkeeping, not Lemma★)

On a closed triad, the interaction is rewritten
\[
\tau=(\omega(p)-\omega(r))J_p+(\omega(q)-\omega(r))J_q.
\]

Frequencies are shifted by a lattice constant \(\omega_*\), **not** by \(\Lambda\). This pair — the rewrite and the constant shift — is the **spectral-shift identity**. It is exact bookkeeping. It is distinct from the Lemma★ ratio bound. Establishing the identity does not establish that bound and does not control nonlinear transfer.

Unaugmented normalization: do not add a field to help the estimate.

**Proposition (listed triad; not a bound of \(T_{j\leftarrow j}\)).**
Class: one closed Fourier triad \((p,q,r)\) of a divergence-free periodic velocity. Quantity: \(S=J_p+J_q+J_r\). Remainder of this proposition: none (\(S=0\) is the identity). Assumed: [standard incompressible triad pairing; no added field]. Then \(S=0\). Constants: none besides the floating-point gate \(10^{-16}\) used to *check* the identity. Scope: the listed triad. This is not a time series and does not bound \(T_{j\leftarrow j}\).

---

## 4. What this environment can print

Class: unaugmented axisymmetric-with-swirl, **algebraic pairing check only**. Quantity: \(Z_j\). Remainder: \(T_{j\leftarrow j}\). Assumed: [no DNS; no closed NS stepper; recorded 2-D / 3-D facts stay in the class that produced them].

This environment has **no DNS** and **no closed time-series stepper**. The shell ratio \(\rho_j=T_{j\leftarrow j}/Z_j\) is **NOT COMPUTED**. Smallness is that printed ratio, or an explicit integral of \(\|\omega\|_\infty\). Neither is produced here.

What *is* printed (see `python -m domain_architect.axisymmetric_shell`):

| Print | Class / dimension | Status |
|---|---|---|
| pairing residual \(\lvert J_p+J_q+J_r\rvert\) on a listed triad | algebraic / any dimension of the triad pairing | unit check; closed only at \(\le 10^{-16}\) |
| same residual on a broken triad \((1,1,1)\) | algebraic | gate demonstration; not closed |
| \(\lvert T_c\rvert/D_s\sim 0.017\); occupancy \(\sim 0.15\) | **2-D**, recorded, not re-run | stay 2-D; do not import 2-D \(\rho=0.02\) into 3-D |
| random-phase \(O(10^{-2})\); HHH occupancy 1 on the orbits that were run; \(\alpha\approx 0.5\) | **3-D**, recorded, not re-run; small exact disks / restricted class | stay 3-D; occupancy 1 is not CFM; occupancy 1 with \(\alpha\approx 1/2\) does not establish depletion |
| \(\mathrm{sign}(\Lambda')\) | — | **NOT QUOTED** (no closed time series) |
| \(T_{j\leftarrow j}/Z_j\) | axisymmetric-with-swirl | **NOT COMPUTED** |

Door 3: vorticity-direction alignment \(\alpha\) is a **criterion to test**, kept **separate** from triad-phase occupancy. The 3-D number \(\alpha\approx 0.5\) is a recorded 3-D fact on the orbits that were run. Observed occupancy 1 alongside alignment approximately \(1/2\) does not establish the depletion required for closure.

Swirl geometry is the **class** that removes free helical HHH. That is a class statement, not a measured 3-D CFM close.

Refuse “visibility of cancellation = uniform smallness.”

---

## 5. Sept 11 enstrophy Door-1 and far-shell Young

Class: unaugmented axisymmetric-with-swirl NS on \(\mathbb{R}^3\). Quantity on that write: the enstrophy shell \(Z_j=\|\Delta_j\omega\|_{L^2}^2\) (this is **not** the energy \(Z_j=\tfrac12\|P_j u\|_{L^2}^2\) of §1; same remainder letter, different shell). Remainder: \(T_{j\leftarrow j}\). Assumed: [smooth rapidly decreasing axisymmetric-with-swirl; no added field; radial LP bump \(\varphi\)].

Source: `docs/AXISYM-SHELL.md` on `origin/cursor/tjj-estimate-chain-e5c5`. Not re-derived here.

Write \(B(\omega,u)=\omega\cdot\nabla u-u\cdot\nabla\omega\), and
\[
T_j=\langle\Delta_j B(\omega,u),\Delta_j\omega\rangle,
\qquad
\tfrac12\dot Z_j+\nu D_j=T_j,
\qquad
D_j=\|\nabla\Delta_j\omega\|_2^2.
\]
Infrared / local / ultraviolet split of the field:
\(u_{\mathrm{IR}}=S_{j-2}u\),
\(u_{\mathrm{loc}}=(\Delta_{j-1}+\Delta_j+\Delta_{j+1})u\)
(this local block is the \(b=1\) grouping),
\(u_{\mathrm{UV}}=u-u_{\mathrm{IR}}-u_{\mathrm{loc}}\). Then
\[
T_j=T_{j\leftarrow\mathrm{IR}}+T_{j\leftarrow j}+T_{j\leftarrow\mathrm{UV}}.
\]
The only remainder after the next two lemmas is still \(T_{j\leftarrow j}\).

**Lemma AS-IR.** There is a finite \(C_{\mathrm{IR}}=C_{\mathrm{IR}}[\varphi]\) such that
\[
\lvert T_{j\leftarrow\mathrm{IR}}\rvert
\le
C_{\mathrm{IR}}\Bigl(\sum_{k\le j-2}2^{3k/2}Z_k^{1/2}\Bigr)Z_j
+
C_{\mathrm{IR}}\Bigl(\sum_{k\le j-2}2^{k/2}Z_k^{1/2}\Bigr)D_j^{1/2}Z_j^{1/2}.
\]
Infrared *transport* absorbs as
\(\lvert T_{j\leftarrow\mathrm{IR}}^{\mathrm{trans}}\rvert\le\frac\nu4 D_j+C_{\mathrm{IR}}^2\nu^{-1}\|u_{\mathrm{IR}}\|_\infty^2 Z_j\).
That absorption is not an estimate of \(T_{j\leftarrow j}\).

**Lemma AS-UV.** There is a finite \(C_{\mathrm{UV}}=C_{\mathrm{UV}}[\varphi]\) such that
\[
\lvert T_{j\leftarrow\mathrm{UV}}\rvert
\le
C_{\mathrm{UV}}\sum_{\ell\ge j+2}2^{j-\ell/2}Z_\ell\,Z_j^{1/2}.
\]

Constants named: \(C_{\mathrm{IR}}[\varphi]\), \(C_{\mathrm{UV}}[\varphi]\). Scope: far shells only. The local block is not in these two lemmas. Precise bounds and summability of the cross-scale terms remain to be supplied; they are not established by this note.

---

## 6. Requested local Young — REFUSED

Class: same unaugmented axisymmetric-with-swirl class. Quantity: the §5 enstrophy shell. Remainder: \(T_{j\leftarrow j}\). Assumed: [no extra field; \(R\) only from energy, \(Z\), maybe a direction factor; not \(\dot Z_j\); not \(\Lambda'\)].

Source: `docs/TJJ-ESTIMATE.md` on `origin/cursor/tjj-estimate-chain-e5c5`.

The requested line
\[
\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu D_j+R
\]
with that allowed \(R\) is **REFUSED**. It is not seated.

What was figured out and is **not** the request:

- Main transport vanishes: \(\int(u_{\mathrm{loc}}\cdot\nabla)\Delta_j\omega\cdot\Delta_j\omega=0\). Only the commutator remains from transport.
- Main stretch is \(\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2\), an identity, not a bound.
- A template with \(\|u_{\mathrm{loc}}\|_\infty\) and \(\|\nabla u_{\mathrm{loc}}\|_\infty\) sits. Those norms are not energy, not \(Z\), and not a direction factor. Bernstein puts \(2^{3j}\) back in.

Energy-linear \(R\) is **false** as a uniform bound: on \(u^\lambda(x)=\lambda^{3/2}\varphi(\lambda x)\),
\(\lvert T_{j\leftarrow j}\rvert/(\varepsilon\nu D_j+C\,\mathcal E\,Z_j)\sim\lambda^{1/2}\to\infty\).
That scaling is why the line stays refused.

\(\dot Z_j\) and \(\Lambda'\) stay out as bounds.

---

## 7. Transport / \(\alpha\) / swirl bilinear split

Class: unaugmented axisymmetric-with-swirl. Quantity: local enstrophy pairing. Remainder: \(T_{j\leftarrow j}\). Assumed: [local block as in §5; no added field].

On the local block
\[
T_{j\leftarrow j}
=
\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2
+
T_{j\leftarrow j}^{\mathrm{comm}}.
\]
Door 3: a printed \(\alpha\) is a criterion. \(\|(\alpha)_+\|_\infty\) is not controlled by energy.

Write \(u=u_{\mathrm{mer}}+u_{\mathrm{swirl}}\). The pairing is bilinear:
\[
T_{j\leftarrow j}=T^{\mathrm{mm}}+T^{\mathrm{ss}}+T^{\mathrm{cross}}.
\]
\(T^{\mathrm{ss}}\) is the centrifugal source. \(T^{\mathrm{mm}}\) is meridional self-stretch.

If \(u^r=u^z=0\), then \(T_j=T_{j\leftarrow j}=0\). That is why the compact *pure-swirl* samples printed \(\sim 0\). It is not a bound on a mixed field.

A tempting sentence — “no-swirl is regular, so only \(T^{\mathrm{ss}}\) remains” — is **false** as a measurement on this class. On the mixed compact samples, \(T^{\mathrm{mm}}\) is the bulk. Do not set \(T^{\mathrm{ss}}\) equal to leftover-split strain \(\int\|u^r/r\|_\infty\,dt\).

---

## 8. Compact swirl samples (not DNS)

Class: named compact axisymmetric-with-swirl blobs on \(\mathbb{R}^3\), support in a ball of radius \(R=2.4<\pi\), scored on a 2/3-dealiased Leray interpolant. Quantity: printed \(\max\lvert T_{j\leftarrow j}/X_j\rvert\) on that interpolant. Remainder: \(T_{j\leftarrow j}\). Assumed: [these named fields only; pairing closed on the samples; no time series].

Source: `docs/AXISYM-SWIRL-PROBE.md` and the mixed-split table in `docs/TJJ-ESTIMATE.md` on `origin/cursor/tjj-estimate-chain-e5c5`. **Not re-run here. Not DNS.**

**Scope of these numbers.** They concern small exact disks and the stated restricted classes. They establish no uniform conclusion as \(K_{\max}\to\infty\) or for generic data. They are not a class leftover ratio and not palinstrophy-normalized \(\rho_j\). Occupancy was not scored on this table.

Pairing residual on those samples \(\le 3\times 10^{-18}\) relative. Rotation residual \(\le 4\times 10^{-15}\). Occupancy was not scored. \(\alpha\) stayed separate. The sign of \(\Lambda'\) was not quoted.

| field | \(n\) | \(\max\lvert T_{j\leftarrow j}/X_j\rvert\) | \(\overline{\alpha}\) |
|---|---|---|---|
| pure swirl | 32 | \(3.2\times 10^{-19}\) | \(0\) |
| swirl+meridional \(m=1\) | 32 | \(0.00112\) | \(-1.3\times 10^{-4}\) |
| swirl+meridional \(m=3\) | 32 | \(0.00141\) | \(-1.0\times 10^{-4}\) |
| swirl+meridional \(m=1\) | 48 | \(0.000583\) | \(-9.2\times 10^{-5}\) |
| swirl+meridional \(m=3\) | 48 | \(0.000726\) | \(-4.5\times 10^{-5}\) |

Pure swirl printed as zero to residual on these two grids. Mixed ratios sit at \(O(10^{-3})\) on \(n=32\) and **moved with \(n\) and with \(m\)**. The continuum value of these blobs is not locked.

Mixed split, compact swirl+meridional, \(n=24\), energy-carrying shells (rounded print; not a \(10^{-16}\) sum check):

| \(j\) | \(T^{\mathrm{mm}}\) | \(T^{\mathrm{ss}}\) | \(T^{\mathrm{cross}}\) | \(T_{j\leftarrow j}\) |
|---|---|---|---|---|
| 1 | \(8.15\times 10^3\) | \(-62\) | \(217\) | \(8.30\times 10^3\) |
| 2 | \(-1.08\times 10^4\) | \(4.03\times 10^3\) | \(-142\) | \(-6.89\times 10^3\) |
| 3 | \(-1.32\times 10^4\) | \(622\) | \(88\) | \(-1.25\times 10^4\) |

\(T^{\mathrm{mm}}\) is the bulk. 2-D \(\lvert T_c\rvert/D_s\sim 0.017\) is not used here.

---

## 9. Extra hypotheses in brackets

A conditional theorem is a theorem. A hidden hypothesis is not.

- [axisymmetric with swirl] — real geometry; preferred over a modified PDE that is no longer classical NS.
- [pairing closed] — stepper and diagnostic agree to \(10^{-16}\); otherwise do not quote \(\mathrm{sign}(\Lambda')\). This environment has no stepper, so the algebraic residual is not a time-series close.
- [measured \(\rho_j=T_{j\leftarrow j}/Z_j\)] — not a class print. Compact-sample ratios in §8 are not this hypothesis.
- [ρ] (Sept 11, extra, not measured): \(\int_0^T(T_{j\leftarrow j})_+/Z_j\,dt<\infty\) and the infrared sum of Lemma AS-IR finite. Under [ρ] the far-shell lemmas keep that enstrophy shell finite on \([0,T]\). [ρ] is not shown for the class.

[SND] in its **large** form (“assume the dangerous interactions are not dangerous”) is **not** used as measured smallness. Ring \(\inf J/X\ge c_*\) remains a leftover-split **CONDITIONAL** hypothesis on a different book; it is not a measured bound of \(T_{j\leftarrow j}\) here.

---

## 10. Candidate routes (A)–(C) and Step 6

Class: unaugmented axisymmetric-with-swirl. Quantity: the labeled shell in use. Remainder: \(T_{j\leftarrow j}\). Assumed: [(A)–(C) and Step 6 are candidate routes, not theorems; no extra field].

- **(A)** — enstrophy–palinstrophy route. Palinstrophy-normalized \(\rho_j<\nu\) lives here. It is not absorption on the displayed energy budget.
- **(B)**, **(C)** — named candidate routes. Their statements are not supplied on this page. This note does not invent them.
- **Step 6** — a proposed closure mechanism. It requires (A), or a depletion estimate implying (A), without using \(\dot e_j\), \(\dot Z\), or \(\Lambda'\) to reintroduce the quantity being bounded.

The principal unresolved term is still \(T_{j\leftarrow j}\). None of (A)–(C) or Step 6 is seated here.

---

## 11. Gap (send the work with the gap visible)

The leftover is still \(T_{j\leftarrow j}\) and still **OPEN**. Far-shell Young templates sit; precise cross-scale bounds and summability are not established by this note. The requested local Young is **REFUSED**. There is no class leftover ratio. Palinstrophy \(\rho_j<\nu\) is not energy-budget absorption. Occupancy 1 with \(\alpha\approx 1/2\) is not depletion.

Modified / hyperviscous / Q1-augmented equations stay **separate** from classical NS. A close of another PDE is not a close of NS.

---

## 12. What this note refuses

Discard list objects do not enter the identity, the Young step, or the claim: SFE / coherence viscosity / Q1–Q6 as constitutive classical NS; bounding the bad term by \(\Lambda'\) or \(\dot Z_j\); large-form [SND] as measured smallness; GCD spectral attractor / E8 cathedral / prime-harmonic lock / Borromean coherence as mechanisms that force \(T_{j\leftarrow j}\) small; Base 44 / gematria as estimates; Q6-Kabbalah / Lightning Flash inside the proof; 2-D \(\rho=0.02\) imported to 3-D; occupancy 1 imported to CFM; FFT-aliased orbits treated as \(\dot\Lambda=2(T_c-\nu D_s)\); “Clay is solved”; Tao certification; coherence-floor / extra memory / prime gates added to NS and called the Millennium problem.

This note also refuses: treating the spectral-shift identity as the Lemma★ ratio bound or as control of nonlinear transfer; treating \(\rho_j<\nu\) as absorption on the displayed energy budget; treating occupancy 1 with \(\alpha\approx 1/2\) as the depletion required for closure; using \(\dot e_j\), \(\dot Z\), or \(\Lambda'\) in Step 6 to reintroduce the leftover.

Parked elsewhere (not deleted): Harmonic Blueprint / SFE archive; apps; Base 44 partition experiment until \(\rho_j\) is tested; defense stacks; RH / Goldbach; turbulence-reduction (ships ACTIVE; other slots QUEUED); leftover-split strain; Ring / Paper2 / Route J.

Left on the Sept 11 branch, not welded here: Lemma★ / attack notes, H1 / WRITE (6), `SWIRL-PAPER.md` Hardy as a repair of \(R\), lattice random / 4-fold / Taylor–Green interpolant ratios (not this class), the FFT probe scripts themselves.

---

## 13. DA lab

```
python -m domain_architect cycle axisymmetric-shell
python -m domain_architect.axisymmetric_shell
python -m domain_architect cycle open-board
```

Lab string (parser-safe remainder ratio, not a close):

```
Tjj / Zj
```

Decompose returns `unclassified` plus a book warning. That is expected. Synthesize of unaugmented smoothness stays `inverse_design[refused]`. A13 still refuses slogans. Analog 15% turbulence intensity is a **separate** lumped setpoint, not this remainder.
