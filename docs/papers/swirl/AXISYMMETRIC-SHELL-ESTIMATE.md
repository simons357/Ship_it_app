# Axisymmetric-with-swirl shell estimate

**Filter:** [`docs/domain-architect/AXISYMMETRIC-SHELL-AUDIT.md`](../../domain-architect/AXISYMMETRIC-SHELL-AUDIT.md)  
**Date:** 2026-09-12  
**Status:** OPEN. Remainder \(T_{j\leftarrow j}\) is not computed here and is not shown small. Clay is **NOT CLAIMED**. Unconditional 3-D regularity is **NOT CLAIMED**. DA-VC-01 stays **FAIL**.

Class: unaugmented axisymmetric Navier–Stokes with swirl. Quantity: dyadic shell block \(Z_j\). Remainder after the Door-1 budget: intra-shell transfer \(T_{j\leftarrow j}\). Assumed, in brackets: [smooth compactly supported divergence-free axisymmetric-with-swirl solutions of classical NS; no added field; unaugmented normalization; pairing identity closed only when the stepper and the diagnostic agree to \(10^{-16}\)].

This note uses **only** KEEP objects from the audit. Discard items do not appear in the identity, the Young step, or the claim. Parked stacks stay parked.

Swirl \(\Phi=u_\theta/r\) is not FRA/DA \(\Phi\), not Newtonian \(\Phi_g\), and not Paper2 \(\Phi_j\). This remainder is **not** leftover-split strain \(\int\|u^r/r\|_\infty\,dt\) and **not** Paper2 simplex \(\|a-\mu\|_{\ell^1}\).

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
(The enstrophy shell \(\tfrac12\|P_j\omega\|_{L^2}^2\), \(\omega=\nabla\times u\), has the same Door-1 *shape*; using it changes the global sum, which then equals stretching, not zero. This note takes the energy shell as the quantity so that the telescope below is the energy pairing.)
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

## 3. Closed-triad rewrite and lattice shift

On a closed triad, the interaction is rewritten
\[
\tau=(\omega(p)-\omega(r))J_p+(\omega(q)-\omega(r))J_q.
\]

Frequencies are shifted by a lattice constant \(\omega_*\), **not** by \(\Lambda\). Unaugmented normalization: do not add a field to help the estimate.

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
| random-phase \(O(10^{-2})\); HHH occupancy 1 on the orbits that were run; \(\alpha\approx 0.5\) | **3-D**, recorded, not re-run | stay 3-D; occupancy 1 is not CFM |
| \(\mathrm{sign}(\Lambda')\) | — | **NOT QUOTED** (no closed time series) |
| \(T_{j\leftarrow j}/Z_j\) | axisymmetric-with-swirl | **NOT COMPUTED** |

Door 3: vorticity-direction alignment \(\alpha\) is a **criterion to test**, kept **separate** from triad-phase occupancy. The 3-D number \(\alpha\approx 0.5\) is a recorded 3-D fact, not a close.

Swirl geometry is the **class** that removes free helical HHH. That is a class statement, not a measured 3-D CFM close.

Refuse “visibility of cancellation = uniform smallness.”

---

## 5. Extra hypotheses in brackets

A conditional theorem is a theorem. A hidden hypothesis is not.

- [axisymmetric with swirl] — real geometry; preferred over a modified PDE that is no longer classical NS.
- [pairing closed] — stepper and diagnostic agree to \(10^{-16}\); otherwise do not quote \(\mathrm{sign}(\Lambda')\). This environment has no stepper, so the algebraic residual is not a time-series close.
- [measured \(\rho_j=T_{j\leftarrow j}/Z_j\)] — not printed here.

[SND] in its **large** form (“assume the dangerous interactions are not dangerous”) is **not** used as measured smallness. Ring \(\inf J/X\ge c_*\) remains a leftover-split **CONDITIONAL** hypothesis on a different book; it is not a measured bound of \(T_{j\leftarrow j}\) here.

---

## 6. Gap (send the work with the gap visible)

The leftover is still \(T_{j\leftarrow j}\) and still **OPEN**. There is no Young step. There is no printed \(\rho_j\). Clay is **NOT CLAIMED**. Unconditional 3-D regularity is **NOT CLAIMED**.

Modified / hyperviscous / Q1-augmented equations stay **separate** from classical NS. A close of another PDE is not a close of NS.

---

## 7. What this note refuses

Discard list objects do not enter the identity, the Young step, or the claim: SFE / coherence viscosity / Q1–Q6 as constitutive classical NS; bounding the bad term by \(\Lambda'\) or \(\dot Z_j\); large-form [SND] as measured smallness; GCD spectral attractor / E8 cathedral / prime-harmonic lock / Borromean coherence as mechanisms that force \(T_{j\leftarrow j}\) small; Base 44 / gematria as estimates; Q6-Kabbalah / Lightning Flash inside the proof; 2-D \(\rho=0.02\) imported to 3-D; occupancy 1 imported to CFM; FFT-aliased orbits treated as \(\dot\Lambda=2(T_c-\nu D_s)\); “Clay is solved”; Tao certification; coherence-floor / extra memory / prime gates added to NS and called the Millennium problem.

Parked elsewhere (not deleted): Harmonic Blueprint / SFE archive; apps; Base 44 partition experiment until \(\rho_j\) is tested; defense stacks; RH / Goldbach; turbulence-reduction (ships ACTIVE; other slots QUEUED); leftover-split strain; Ring / Paper2 / Route J.

---

## 8. DA lab

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
