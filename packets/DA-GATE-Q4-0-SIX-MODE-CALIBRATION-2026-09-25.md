# DA gate — Q4-0 six-mode calibration **plan**

**25 September 2026.** Plan only. **Do not run.**
DA must approve this page before any evolution, sweep, or
diagnostic execute.

Working record:
[`../docs/ns-recovery/WORKING-RECORD-2026-09-25.md`](../docs/ns-recovery/WORKING-RECORD-2026-09-25.md).
Lock: `scripts/da_gate_q4_0_six_mode_plan.py`
(contract only; `executed=false`).

Does **not** alter the locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) / shape-form packets.

**Not a closure theorem.** Ordinary NS is not solved. Soft X silent.
Do not put \(K(t)\) in the PDE.

---

## Purpose

Measure how fast the nonlinear force rotates against viscosity,
on a six-mode real triad, looking **only** at states with

\[
\alpha_c\approx 1\qquad\text{and}\qquad T_c>0.
\]

This is a calibration of an alignment diagnostic. It is not
DA-NS-2, not a remainder bound, and not a solver campaign.

---

## Objects already on this book (do not reinvent)

Six-mode real field: a closed triad \(\{p,q,r\}\) together with
the three conjugate modes. Evaluator:
`scripts/centered_drift_triad_test.py` on
`scripts/ns_lemma_star_core.py`.
Convention note: this book’s evaluator writes a factor \(2\)
because it sums both conjugate modes
([`../docs/ns-recovery/CENTERED-MASTER-LEDGER.md`](../docs/ns-recovery/CENTERED-MASTER-LEDGER.md)).
Do not “correct” one convention into the other.

Nonlinear force \(F=B(u,u)\). Alignment identity already
inventoried:

\[
T_c
=
-\langle F,\,g\rangle,
\qquad
g=A(A-\Lambda)u.
\]

Sign of \(T_c\) is an alignment question. Phase-only reversal
already sits on the aligned closer
(\(\max T_c=16/5\), \(\min T_c=-16/5\)).

Viscous clock on the same field is \(\nu D_s\), or the modal
rate \(\nu\kappa^2\) with \(\kappa=\sqrt{\Lambda}\).
The comparison Q4-0 asks for is the **rotation** of \(F\)
relative to that viscous clock, not another packaging of
\(T_c/(\nu D_s)\).

A quartic term is to be **reused** as a rotation diagnostic,
not invented. The named 54/46 quartic test is **not on this
tree**. DA must name the exact quartic already in the record
before a run. Do not write a new one here.

---

## Admission filter

A state is eligible only if both hold:

1. \(T_c>0\) (dangerous alignment).
2. \(\alpha_c\approx 1\) (near-maximal coherence of the local
   envelope already named on the occupation line).

This plan does **not** invent a six-mode definition of
\(\alpha_c\). DA must approve the proxy before execution.
A natural candidate, not stamped here, is the normalized
alignment of \(F\) against \(g\) in the stated envelope units
\(\kappa^{3/2}X D_s^{1/2}\). If DA rejects that proxy, stop;
do not substitute a different \(\alpha_c\) silently.

Rejected (do not admit):

- \(T_c\le 0\).
- \(\alpha_c\) bounded away from 1.
- Fields that are not six-mode real triads.
- Taylor–Green, Galerkin \(N=64/96\), or any family not already
  on this tree, unless DA adds it in writing.
- States used to reopen a killed route (unrestricted ★,
  charge-only, uniform energy-class \(K\)).

Existing on-tree snapshots that already have \(T_c>0\)
(note triad; aligned closer; some separated \(L\)) are
**candidate seeds only**. They are not a completed Q4-0 table.
\(\alpha_c\) is not stamped on them here.

---

## What the approved run would measure

Once DA names \(\alpha_c\) and the quartic, and only then,
the calibration records, on admitted states:

| Symbol | Meaning |
|---|---|
| \(\tau_\nu\sim 1/(\nu\kappa^2)\) | viscous time |
| \(\tau_{\mathrm{rot}}\) | time for \(F\) to rotate off \(g\) |
| \(\Theta_{\mathrm{rot}}=\tau_{\mathrm{rot}}/\tau_\nu\) | rotation versus viscosity |
| \(T_c\), \(\nu D_s\), \(T_c/(\nu D_s)\) | alignment versus dissipation (already named) |
| the DA-named quartic | rotation diagnostic, reused not invented |

Output is a table on a handful of six-mode seeds, plus the
admission flags. No parameter sweep. No closure sentence.

If \(\Theta_{\mathrm{rot}}\ll 1\) on \(\alpha_c\approx 1\), \(T_c>0\)
states, the force rotates off the dangerous direction faster
than viscosity can act. That would be a **calibration fact**,
not a proof that occupation holds and not a proof of DA-NS-2.

If \(\Theta_{\mathrm{rot}}\gtrsim 1\), rotation is not a free
gain on those states. Same caveat.

---

## Hard stops

- **Do not run** until DA approves this page in writing,
  including the \(\alpha_c\) proxy and the quartic.
- Do not drop \(\nu\).
- Do not treat a six-mode table as a bound on general data.
- Do not import I3 weighted, \(K,K,L\) regrouping, A8-R
  construction, cube-field, or 54/46 as if they were on disk.
- Do not move the separated-scale fiber verdict off NEUTRAL
  from this plan.
- Do not silently substitute live \(T\) for \(T^{(0)}\).
- Do not spend compute on circle/star/coherence/exact-shell
  searches.

---

## Approval checklist (DA)

- [ ] \(\alpha_c\) six-mode proxy named.
- [ ] Admission window (\(\lvert\alpha_c-1\rvert\le ?\)) named.
- [ ] Quartic rotation diagnostic named from an existing file.
- [ ] \(\nu\) convention named (keep the symbol, or set \(\nu=1\)
      explicitly as a scoring unit).
- [ ] Seed list restricted to six-mode real triads already
      on this tree, unless DA adds a seed in writing.
- [ ] Written approval to execute.

Until every box is ticked, `executed` stays false.

No new estimate is claimed. No continuation criterion.
**NS not solved.**
