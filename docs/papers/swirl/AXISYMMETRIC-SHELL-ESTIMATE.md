# Axisymmetric-with-swirl shell estimate

**Filter:** [`docs/domain-architect/AXISYMMETRIC-SHELL-AUDIT.md`](../../domain-architect/AXISYMMETRIC-SHELL-AUDIT.md)  
**Predecessor (11 Sept, not this HEAD):** `origin/cursor/tjj-estimate-chain-e5c5` — `docs/ESTIMATE-AUDIT.md`, `docs/AXISYM-SHELL.md`, `docs/TJJ-ESTIMATE.md`, `docs/AXISYM-SWIRL-PROBE.md`.  
**Date:** 2026-09-12 (same-scale attack §14: 2026-09-16)  
**Status:** OPEN. Remainder \(T_{j\leftarrow j}\) is still open. Far-shell Young sits. The requested local Young is **REFUSED**. Compact-sample ratios are not a class \(\rho_j\). Same-scale attack: conditional \(\theta\)-template only; (A) **not** seated. Clay is **NOT CLAIMED**. Unconditional 3-D regularity is **NOT CLAIMED**. DA-VC-01 stays **FAIL**.

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

**Remaining closure.** Conditions (A)–(C) describe candidate routes for completing this particular proof chain. The principal unresolved term is the same-scale transfer \(T_{j\leftarrow j}\). Estimate Step 6 is a **proposed** closure mechanism: it requires (A), or a depletion estimate implying (A), without using \(\dot e_j\), \(\dot Z\) or \(\Lambda'\) to reintroduce the quantity being bounded. **Not claimed.** It is not WRITE (6)/H1, not leftover-split item #6, not Q6, not Ring/Paper2 SND leftover, and not Statement-B table Step 6.

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

Filed from the unaugmented proof-chain standing text (11–12 Sept 2026). **Not invented here. Not claimed for the class.**

- **(A)** — enstrophy–palinstrophy bound
  \[
  \lvert T_{j\leftarrow j}\rvert
  \le
  \varepsilon\nu P_j
  +
  R(X,Z)
  \]
  with \(0\le\varepsilon<1\) and \(R\) controlled by energy and known quantities. Here \(P_j\) is **palinstrophy**, not the LP projector. Palinstrophy-normalized \(\rho_j=\lvert T_{j\leftarrow j}\rvert/P_j\) and the comparison \(\rho_j<\nu\) live on this route. **Not** absorption on the displayed energy budget (viscous slot \(\nu D_j\) or \(\nu Z_j\)).

- **(B)** — depletion implying (A): a factor \(\sin\phi\) or \(1-\alpha\) from vorticity-direction mismatch on HHH that makes (A) true. Occupancy \(1\) on small orbits means phase rotation is **not** supplying this by itself. Recorded occupancy \(1\) with \(\alpha\approx 1/2\) does **not** establish depletion.

- **(C)** — restriction of the data (axisymmetry-with-swirl, etc.). That is a **different** theorem path (this swirl/Door-1 note), not a generic 3-D close.

- **Estimate Step 6** — proposed closure shape: assume (A) with \(\varepsilon<1\) (or (B)\(\Rightarrow\)(A)); sum on shells; absorb into palinstrophy dissipation; use energy from Step 0 and standard Sobolev interpolation; then enstrophy stays finite on a finite interval and BKM applies. **Not claimed.** Must not use \(\dot e_j\), \(\dot Z\), or \(\Lambda'\) to reintroduce the leftover. Not WRITE (6)/H1. Not Q6. Not the Statement-B table row “Step 6” (conditional \(H^1\) IF [SND]). Not leftover-split item #6.

The principal unresolved term is still \(T_{j\leftarrow j}\). None of (A)–(C) or estimate Step 6 is seated here. Proofs stay parked.

Harness (diagnostic only): `python -m domain_architect.axisym_ac_tests` and `python scripts/axisym_ac_gronwall_occupancy.py`.
Same-scale attack harness: `python scripts/axisym_same_scale_tjj.py` (module `domain_architect.axisym_same_scale_tjj`).

---

## 10a. Conditional Gronwall under (A) — repaired template, not a close

Class: unaugmented axisymmetric-with-swirl. Quantity: enstrophy shell \(Z_j=\|\Delta_j\omega\|_{L^2}^2\) with palinstrophy \(P_j\) (letters as in (A); **not** the displayed energy \(Z_j\) of §1). Remainder: \(T_{j\leftarrow j}\). Assumed: explicit hypotheses below. **NS not solved. Not claimed for the class.**

**Broken / sloppy pattern refused.** A rate that inserts \(\nu^2\) where the viscous Poincaré / absorption chain supplies a single factor of \(\nu\) is refused here. Cross-link only: the Paper2 T2 shell-flux note’s \(\alpha_F=2\nu^2\cdot 4^{1/\rho_0}\rho_0\) conflicts with its own proof line \(\mathcal D\ge\nu\cdot 4^{1/\rho_0}\rho_0\,X\) (see [`docs/papers/ns-snd/03_t2_shell_flux_gronwall.MISSING.md`](../ns-snd/03_t2_shell_flux_gronwall.MISSING.md) errata). Do not import that \(\nu^2\) rate into this Door-1 chain. Do not bound \(T_{j\leftarrow j}\) by \(\dot e_j\), \(\dot Z\), or \(\Lambda'\).

**Hypotheses (all required; none hidden).**

1. **[A\(_\varepsilon\)]** Condition (A) with \(0\le\varepsilon<1\): \(\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu P_j+R\), and \(R\) is controlled by energy / known quantities (not by \(\dot e_j\), \(\dot Z\), or \(\Lambda'\)).
2. **[Poincaré-shell]** \(P_j\ge c\,4^{j} Z_j\) for a named \(c=c[\varphi]>0\).
3. **[far]** Infrared / ultraviolet remainders are majorized by an integrable function \(M(t)\) on \([0,T]\). Precise bounds and summability are **not** established by this note (gap).
4. **[no-cycle]** The spectral-shift identity is bookkeeping only; it is not used as a bound of \(T_{j\leftarrow j}\).

**Conditional estimate (template).** Under 1–4, the enstrophy shell satisfies
\[
\dot Z_j
+
2\nu(1-\varepsilon)\,c\,4^{j}\,Z_j
\le
2M(t).
\]
Let \(\alpha:=2\nu(1-\varepsilon)\,c\,4^{j}\) (**one** power of \(\nu\)). Gronwall gives
\[
Z_j(t)
\le
Z_j(0)\,e^{-\alpha t}
+
\int_0^t e^{-\alpha(t-s)}\,2M(s)\,ds.
\]
If \(M\le M_\ast\) on \([0,T]\), then \(Z_j\) stays finite on \([0,T]\). This is the shape of estimate Step 6 under (A). **Not claimed:** [A\(_\varepsilon\)] and [far] are missing for the class; the requested local Young stays **REFUSED**.

**What would make a true repair need a missing lemma.** Seating [A\(_\varepsilon\)] without recycling \(\dot e_j/\dot Z/\Lambda'\), or seating [far] summability, or a depletion lemma that implies (A) without treating occupancy \(1\) as depletion. Until one of those arrives, the leftover stays \(T_{j\leftarrow j}\).

---

## Same-scale transfer attack

Class: unaugmented axisymmetric-with-swirl. Quantity: Door-1 same-scale block \(T_{j\leftarrow j}\). Remainder: \(T_{j\leftarrow j}\). Assumed: [small exact disks / restricted classes; signed \(\mathrm{Im}\) triad form; no absolute-value Young that destroys the problem; no \(\dot e_j/\dot Z/\Lambda'\) recycling; spectral-shift identity ≠ Lemma★ ratio bound]. **NS not solved. Invent no proofs.** Overall status: **OPEN**.

Harness: `python scripts/axisym_same_scale_tjj.py` · module `domain_architect.axisym_same_scale_tjj` · tests `tests/test_axisym_same_scale_tjj.py`. Artifact: `/opt/cursor/artifacts/axisym_same_scale_Tjj/`.

### A. Structure of the object

**LP / Door-1 definition (as in §1).** With Littlewood–Paley projectors \(P_j\) and named locality width \(b\),
\[
T_{j\leftarrow\ell m}
:=
-\bigl\langle P_j\bigl((P_\ell u)\cdot\nabla(P_m u)\bigr),\,P_j u\bigr\rangle,
\qquad
T_{j\leftarrow j}
:=
\sum_{\lvert\ell-j\rvert\le b,\;\lvert m-j\rvert\le b}
T_{j\leftarrow\ell m}.
\]
Cross-scale / HH→L sit in \(T_{j\leftarrow\neq j}\) and are **not** this remainder; their precise bounds and summability remain **not** established by this note.

**Fourier signed form (exact-disk diagnostic).** On a closed triad \(p+q=k\) with divergence-free amplitudes \(\hat u_p,\hat u_q,\hat u_k\),
\[
\tau(p,q;k)
=
\mathrm{Im}\Bigl[(\hat u_p\cdot q)\,(\hat u_q\cdot\hat u_k^*)\Bigr].
\]
Same-scale disk transfer is the signed sum of \(\tau\) over triads with \(\lvert p\rvert,\lvert q\rvert,\lvert k\rvert\) all in the shell band. Absolute-value Young is **REFUSED** for this attack (it replaces the cancellation problem by a larger one).

**Hygiene / sharp \(b=0\) energy identity.** For the **energy** shell with a **sharp** spectral cutoff and locality width \(b=0\) (all triad legs in an annulus closed under \(k\leftrightarrow-k\)), the internal transfer vanishes: each closed triad obeys \(J_p+J_q+J_r=0\), so sharp \(b=0\) energy \(T_{j\leftarrow j}\equiv 0\). That zero is the **triad energy identity**, not geometric depletion. Door-1 “same-scale” with \(b\ge 1\) is **near-scale** leakage (and soft LP bumps differ from sharp cutoffs). The **enstrophy** same-scale term does **not** inherit this telescope. The numeric probe records the \(b=0\) identity and attacks near-scale (\(b\ge 1\)) separately.

**Known / moved vs remainder.**

| Piece | Status |
|---|---|
| Pressure in the energy pairing | drops |
| \(-\nu D_j\) | cannot grow \(Z_j\) |
| \(T_{j\leftarrow\neq j}\) (incl. HH→L) | moved by Door-1 budget; bounds/summability **not** seated here |
| Spectral-shift identity on a listed triad | bookkeeping only; ≠ Lemma★; does **not** control transfer |
| Main local transport (enstrophy write) | vanishes; commutator remains |
| Pure swirl \(u^r=u^z=0\) | \(T_{j\leftarrow j}=0\) on that field |
| Sharp \(b=0\) ENERGY internal transfer | \(\equiv 0\) by triad pairing (not depletion) |
| **Door-1 \(T_{j\leftarrow j}\) at \(b\ge 1\) (near-scale energy) / enstrophy same-scale** | **OPEN remainder** |

**What axisymmetry-with-swirl kills or reduces.** Free helical HHH supported on fully 3-D wavevector configurations incompatible with axisymmetry about \(z\) are removed as a **class** statement. On exact disks the probe restricts to meridional wavevectors \(k=(k_x,0,k_z)\) with swirl polarization \(\hat e_y\) allowed. That restriction does **not** kill meridional self-stretch \(T^{\mathrm{mm}}\) on mixed fields, nor same-scale triads inside the restricted disk.

### B. Attack avenues (status)

| # | Avenue | Status | Finding |
|---|---|---|---|
| 1 | Axisymmetric cancellation / structure constants (signed \(\mathrm{Im}\)) | **PARTIAL** | Axisym slice removes free 3-D HHH support and many triads. Sharp \(b=0\) energy internal \(\equiv 0\) (identity). Near-scale \(b\ge 1\) signed transfer is **nonzero** on disks; **not** uniformly small. Absolute-value Young refused. **No uniform bound.** |
| 2 | Depletion \(\Rightarrow\) (A) without \(\dot e_j/\dot Z/\Lambda'\) | **PARTIAL** (false candidates **KILLED**) | Killed: occupancy \(1\Rightarrow\) depletion; \((1-\lvert\alpha\rvert)\approx\tfrac12\) seats (A); recycling \(\dot Z/\Lambda'\) as (A); reading sharp \(b=0\) energy zero as depletion. Open candidate: class control of a geometric factor \(\theta\) plus a named template — **not seated**. |
| 3 | Conditional bound under geometric factor \(\theta\) | **PARTIAL** | Template: if \(\theta\le\theta_\ast\) then \(\lvert T_{\mathrm{near}}\rvert\le\theta\,C_{\mathrm{young}}\sqrt{D}\,Z\) on the disk diagnostic. **Not** (A) (wrong normalization; no class \(\theta_\ast\)). |
| 4 | Numeric kill/search on small exact disks | **PARTIAL** | Records sharp \(b=0\) energy identity; maximizes \(\lvert T_{\mathrm{near}}\rvert/Z^{3/2}\) for \(b\ge 1\); HH→L separate. “\(b=0\) zero \(\Rightarrow\) depletion” **KILLED**. “Axisymmetry alone forces Door-1 \(T_{j\leftarrow j}\approx 0\) on mixed fields” **KILLED** by nonzero near-scale maxima. Scope: finite disks / trials only — no \(K_{\max}\to\infty\). |

**Conditional bound obtained (disk template only).** Under hypothesis \([\theta]\) (geometric factor \(\theta=\lvert\mathrm{signed}\rvert/\sum\lvert\mathrm{contrib}\rvert\le\theta_\ast\) on near-scale feeders),
\[
\lvert T_{\mathrm{near}}\rvert
\le
\theta_\ast\,C_{\mathrm{young}}\,\sqrt{D}\,Z.
\]
This is **not** condition (A). Bridging to (A) needs palinstrophy normalization, \(\varepsilon\nu\) absorption, and class control of \(\theta_\ast\) — none seated here. Does not use \(\dot e_j\), \(\dot Z\), or \(\Lambda'\).

**What failed / dead ends.** Occupancy \(1\) with \(\alpha\approx 1/2\) as depletion; treating spectral-shift as transfer control; absolute-value Young as the same-scale attack; claiming axisym mixed fields have Door-1 \(T_{j\leftarrow j}\equiv 0\); recycling \(\dot Z/\Lambda'\) into (A); reading sharp \(b=0\) energy internal zero as depletion.

**What is left for (A).** A depletion or geometric lemma that yields \(\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu P_j+R\) on the **near-scale / enstrophy** remainder (not the sharp \(b=0\) energy identity), with \(R\) controlled by energy / known quantities, without \(\dot e_j/\dot Z/\Lambda'\), and without treating occupancy as depletion. Cross-scale summability remains a separate gap.

### C. Honesty locks (unchanged)

Spectral-shift ≠ Lemma★. \(\rho_j<\nu\) is enstrophy–palinstrophy (A), not shell-energy absorption. Cross-scale bounds not established here. Principal open term remains same-scale \(T_{j\leftarrow j}\). Clay / unconditional 3-D regularity **NOT CLAIMED**.

---

## 11. Gap (send the work with the gap visible)

The leftover is still \(T_{j\leftarrow j}\) and still **OPEN**. Far-shell Young templates sit; precise cross-scale bounds and summability are not established by this note. The requested local Young is **REFUSED**. There is no class leftover ratio. Palinstrophy \(\rho_j<\nu\) is not energy-budget absorption. Occupancy 1 with \(\alpha\approx 1/2\) is not depletion. Same-scale attack (§ Same-scale transfer attack): conditional \(\theta\)-template only; (A) not seated; axisym slice does not kill mixed same-scale transfer on exact disks.

Modified / hyperviscous / Q1-augmented equations stay **separate** from classical NS. A close of another PDE is not a close of NS.

---

## 12. What this note refuses

Discard list objects do not enter the identity, the Young step, or the claim: SFE / coherence viscosity / Q1–Q6 as constitutive classical NS; bounding the bad term by \(\Lambda'\) or \(\dot Z_j\); large-form [SND] as measured smallness; GCD spectral attractor / E8 cathedral / prime-harmonic lock / Borromean coherence as mechanisms that force \(T_{j\leftarrow j}\) small; Base 44 / gematria as estimates; Q6-Kabbalah / Lightning Flash inside the proof; 2-D \(\rho=0.02\) imported to 3-D; occupancy 1 imported to CFM; FFT-aliased orbits treated as \(\dot\Lambda=2(T_c-\nu D_s)\); “Clay is solved”; Tao certification; coherence-floor / extra memory / prime gates added to NS and called the Millennium problem.

This note also refuses: treating the spectral-shift identity as the Lemma★ ratio bound or as control of nonlinear transfer; treating \(\rho_j<\nu\) as absorption on the displayed energy budget; treating occupancy 1 with \(\alpha\approx 1/2\) as the depletion required for closure; using \(\dot e_j\), \(\dot Z\), or \(\Lambda'\) in Step 6 to reintroduce the leftover.

Parked elsewhere (not deleted): Harmonic Blueprint / SFE archive; apps; Base 44 partition experiment until \(\rho_j\) is tested; defense stacks; RH / Goldbach; turbulence-reduction (ships ACTIVE; other slots QUEUED); leftover-split strain; Ring / Paper2 / Route J.

Left on the Sept 11 branch, not welded here: Lemma★ / attack notes, H1 / WRITE (6), `SWIRL-PAPER.md` Hardy as a repair of \(R\), lattice random / 4-fold / Taylor–Green interpolant ratios (not this class), the FFT probe scripts themselves.

**WRITE (6) / H1** is a named geometric leftover (Bad-pair / \(A_{\mathrm{bad}}\) on \(Q_r\)). It is **not proved** and **not** this Door-1 remainder. Status **PARK**. Do not set WRITE (6) = estimate Step 6 = \(T_{j\leftarrow j}\) = SND leftover = Q6.

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
