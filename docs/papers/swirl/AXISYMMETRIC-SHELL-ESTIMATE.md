# Axisymmetric-with-swirl shell estimate

**Filter:** [`docs/domain-architect/AXISYMMETRIC-SHELL-AUDIT.md`](../../domain-architect/AXISYMMETRIC-SHELL-AUDIT.md)  
**Date:** 2026-09-12  
**Status:** OPEN. Remainder \(T_{j\leftarrow j}\) is not shown small. Clay is **NOT CLAIMED**. Unconditional 3-D regularity is **NOT CLAIMED**. DA-VC-01 stays **FAIL**.

Class: unaugmented axisymmetric Navier–Stokes with swirl. Quantity: dyadic shell block \(Z_j\). Remainder after the Door-1 budget: intra-shell transfer \(T_{j\leftarrow j}\). Assumed, in brackets: [smooth compactly supported divergence-free axisymmetric-with-swirl solutions of classical NS; no added field; unaugmented normalization; pairing identity closed only when the stepper and the diagnostic agree to \(10^{-16}\)].

This note uses **only** KEEP objects from the audit. Discard items do not appear in the identity, the Young step, or the claim. Parked stacks stay parked.

Swirl \(\Phi=u_\theta/r\) is not FRA/DA \(\Phi\), not Newtonian \(\Phi_g\), and not Paper2 \(\Phi_j\). This remainder is **not** leftover-split strain \(\int\|u^r/r\|_\infty\,dt\) and **not** Paper2 simplex \(\|a-\mu\|_{\ell^1}\).

---

## 1. Identity first

Write the exact identity before any bound. For a Littlewood–Paley / dyadic shell projector \(P_j\) and a non-negative shell block \(Z_j\) built from \(P_j u\) (enstrophy form is allowed; the letter is bookkeeping), the Door-1 shell budget is

\[
\dot Z_j
=
T_{j\leftarrow\neq j}
+
T_{j\leftarrow j}
-
\nu D_j.
\]

Cross-shell flux \(T_{j\leftarrow\neq j}\) is moved by the budget. Dissipation \(\nu D_j\) cannot grow \(Z_j\). **The one term that can grow the quantity is \(T_{j\leftarrow j}\).**

Never bound \(T_{j\leftarrow j}\) by a copy of the time derivative being estimated: not by \(\dot Z_j\), not by \(\Lambda'\), not by a new symbol of the same size.

Door 1: after the budget, **the only remainder is \(T_{j\leftarrow j}\)** (axisymmetric if that is the class).

---

## 2. Bookkeeping that is not the final left-hand side

\[
\Lambda'=\frac{2(T_c-\nu D_s)}{X}
\]

is bookkeeping for signed production versus dissipation. It is **not** the final left-hand side of this estimate. If the pairing identity is not closed in the time series, **do not quote the sign of \(\Lambda'\)**.

Energy conservation of the pairing is a check: residual \(10^{-16}\). If the stepper and the diagnostic disagree, the identity is not closed.

---

## 3. Closed-triad rewrite and lattice shift

On a closed triad, the interaction is rewritten

\[
\tau=(\omega(p)-\omega(r))J_p+(\omega(q)-\omega(r))J_q.
\]

Frequencies are shifted by a lattice constant \(\omega_*\), **not** by \(\Lambda\).

Unaugmented normalization: do not add a field to help the estimate.

---

## 4. Door 3 is a criterion to test, not a close

Door 3: vorticity-direction alignment \(\alpha\) is a **criterion to test**. Keep \(\alpha\) **separate** from triad-phase occupancy.

Refuse “visibility of cancellation = uniform smallness.”

---

## 5. Measured facts, labeled by class

These numbers are **facts in the class that produced them**. They are allowed in because a number can come out the other way. They are **not** imported across dimension or into CFM.

| Class | Fact | Not allowed |
|---|---|---|
| **2-D** | adversary \(\lvert T_c\rvert/D_s\sim 0.017\); occupancy \(\sim 0.15\) | do not import 2-D \(\rho=0.02\) into 3-D |
| **3-D** | random-phase ratio still \(O(10^{-2})\); HHH occupancy 1 on the orbits that were run; \(\alpha\approx 0.5\) | do not import occupancy 1 into CFM |

Swirl geometry is the **class** that removes free helical HHH. That is a class statement, not a measured 3-D CFM close.

---

## 6. Extra hypotheses in brackets

A conditional theorem is a theorem. A hidden hypothesis is not.

- [axisymmetric with swirl] — real geometry; preferred over a modified PDE that is no longer Clay NS.
- [pairing closed] — stepper and diagnostic agree to \(10^{-16}\); otherwise do not quote \(\mathrm{sign}(\Lambda')\).
- [measured \(\rho_j=T_{j\leftarrow j}/Z_j\)] — smallness is this printed ratio, or an explicit integral of \(\|\omega\|_\infty\), not a story.

[SND] in its **large** form (“assume the dangerous interactions are not dangerous”) is **not** used as measured smallness. Ring \(\inf J/X\ge c_*\) remains a leftover-split **CONDITIONAL** hypothesis on a different book; it is not a measured bound of \(T_{j\leftarrow j}\) here.

---

## 7. Gap (send the work with the gap visible)

\(T_{j\leftarrow j}\) is **not** shown small uniformly. There is no Young step that closes the remainder. There is no claim that Clay is solved. There is no unconditional 3-D regularity.

A Tao-positive reply is **not** certification of a proof.

Modified / hyperviscous / Q1-augmented equations stay **separate** from classical NS. A close of another PDE is not a close of NS.

---

## 8. What this note refuses

Discard list objects do not enter the identity, the Young step, or the claim: SFE / coherence viscosity / Q1–Q6 as constitutive Clay NS; bounding the bad term by \(\Lambda'\) or \(\dot Z_j\); large-form [SND] as measured smallness; GCD spectral attractor / E8 cathedral / prime-harmonic lock / Borromean coherence as mechanisms that force \(T_{j\leftarrow j}\) small; Base 44 / gematria as estimates; Q6-Kabbalah / Lightning Flash inside the proof; 2-D \(\rho=0.02\) imported to 3-D; occupancy 1 imported to CFM; FFT-aliased orbits treated as \(\dot\Lambda=2(T_c-\nu D_s)\); “Clay is solved”; Tao certification; coherence-floor / extra memory / prime gates added to NS and called the Millennium problem.

Parked elsewhere (not deleted): Harmonic Blueprint / SFE archive; apps; Base 44 partition experiment until \(\rho_j\) is tested; defense stacks; RH / Goldbach; turbulence-reduction (ships ACTIVE; other slots QUEUED); leftover-split strain; Ring / Paper2 / Route J.

---

## 9. DA lab

```
python -m domain_architect cycle axisymmetric-shell
python -m domain_architect cycle open-board
```

Lab string (parser-safe remainder ratio, not a close):

```
Tjj / Zj
```

Decompose returns `unclassified` plus a book warning. That is expected. Synthesize of unaugmented smoothness stays `inverse_design[refused]`. A13 still refuses slogans. Analog 15% turbulence intensity is a **separate** lumped setpoint, not this remainder.
