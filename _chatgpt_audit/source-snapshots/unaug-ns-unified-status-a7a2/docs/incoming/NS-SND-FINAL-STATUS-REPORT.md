# NS/SND Final Status Report — Markdown

**Download this file.**
Same body as the 16 Sep Global
Regularity Program paste, with the
tape on each section.
Not the tape itself. Not a close.

GitHub:
https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/incoming/NS-SND-FINAL-STATUS-REPORT.md

Raw (Save As):
https://raw.githubusercontent.com/simons357/Ship_it_app/cursor/unaug-ns-unified-status-a7a2/docs/incoming/NS-SND-FINAL-STATUS-REPORT.md

Living desk score (different file):
[`../UNAUG-NS-UNIFIED.md`](../UNAUG-NS-UNIFIED.md)

---

# Incoming — Navier–Stokes Global Regularity Program

**Incoming paste. 16 September 2026.
Not the tape. Not a theorem.
Ordinary NS is not solved.**

This is the ChatGPT-shaped write-up,
pasted in full into this agent chat.
Phone paste flattened superscripts
(`22j` means \(2^{2j}\);
`X1/2` means \(X^{1/2}\)).
Do not treat this file as
[`YES-NO-OPEN.md`](../YES-NO-OPEN.md).

Scored: [`REPORT-AUDIT.md`](../REPORT-AUDIT.md) §8.
Who said what:
[`INCOMING-WRITEUPS.md`](../INCOMING-WRITEUPS.md).

**C10 “died” in §4 is NO as a program
death.** (A) not seated. Leftover 5
stays OPEN. Route A is write-or-kill.

---

# Navier–Stokes Global Regularity Program

Status Report — Classical (Unaugmented)
Incompressible Equation, \(\mathbb{R}^3/\mathbb{T}^3\)

Prepared: 16 September 2026

Prepared for: Jonathan R. Simons,
CRNA, MBS — Founder & CEO, Prime Field
Technologies LLC / Primary Fields Research

Scope: the classical, unaugmented 3D
incompressible Navier–Stokes equations.
No modified operator, no auxiliary field,
no augmented system — this report covers
only the original Clay-Statement-B
**object**. It does not claim Statement B
sits.

## 1. Executive Summary

Global regularity for the classical 3D
incompressible Navier–Stokes equations
remains open. Nothing in this report
closes it, and nothing claims to. What
this cycle produced instead is a
materially cleaner, more honestly scoped
research program: one previously-claimed
theorem was correctly identified as false
and withdrawn; a real conditional result
was derived and proven correct as far as
it goes; one candidate mechanism for
closing the remaining gap was tested
against a rigorous circularity standard
and died cheaply, for a stated reason; a
second track remains a claimed-but-unverified
identity, correctly labeled as such; and
the single obstruction standing between
the current partial results and a full
proof has been isolated and named
precisely, rather than left diffuse.

The honest one-line summary: we know
exactly what is missing, we know it is
hard, and we have ruled out one
plausible shortcut around it.

## 2. What Is Actually Proven (unconditional, rigorous)

These hold for smooth, mean-zero,
divergence-free \(u\) on a fixed torus,
with no unproven hypothesis:

- Exact shell energy budget. With
  \(X_j := 2^{2j}\|\Delta_j u\|_2^2\) and
  \(\widetilde D_j := \nu 2^{2j}\|\nabla\Delta_j u\|_2^2\)
  taken as exact definitions (no Bernstein
  “\(\approx\)”), the identity
  \(\tfrac12\dot X_j + \widetilde D_j = -2^{2j}F_j\)
  is exact, and the peak shell
  \(J(t)=\max_j X_j(t)\) satisfies the
  exact one-sided envelope bounds
  \(D^-J \ge \min_{j\in\mathrm{argmax}} \dot X_j\)
  and
  \(D^+J \le \max_{j\in\mathrm{argmax}} \dot X_j\)
  for a max of \(C^1\) functions.

- Commutator identity.
  \(F_j = \langle[\Delta_j, u\cdot\nabla]u, \Delta_j u\rangle\)
  exactly. This follows because
  \(\langle(u\cdot\nabla)w,w\rangle = 0\)
  for any divergence-free \(u\)
  (integration by parts, \(\nabla\cdot u=0\)),
  which kills the self-transport term after
  subtracting and re-adding
  \((u\cdot\nabla)\Delta_j u\). This is a
  genuine simplification: the standard
  three-way Bony decomposition is not
  structurally necessary for this term — a
  single commutator captures all three
  interactions at once.

- Conditional nonlinear bound (A.2).
  For \(X \le M\):
  \(\lvert F_j\rvert \le C\sqrt{M/(\nu\lambda_1)}\cdot X^{1/2}\mathcal{D}^{1/2}\),
  uniform in \(j\), proved via Hölder
  \((6,2,3)\) + mean-zero Sobolev/Poincaré
  + the eigenvalue bound
  \(\mathcal{D} \ge \nu\lambda_1 X\).
  This is the one piece of the original
  packet's nonlinear-term work that
  survives every adversarial test run
  against it.

- Corrected peak-fraction floor. Using
  the commutator bound above (which is
  shell-local, cubic in amplitude, and
  carries no spurious cross-term), the
  lower Dini derivative of the peak
  fraction \(\rho=J/X\) satisfies
  \(D^-\rho \ge -A(t)\rho\) with
  \(A(t) := 2\nu\lambda_{j_*} + 2C_1\Gamma + C^2\Gamma^2/\nu\),
  giving directly
  \(\rho(t) \ge \rho(0)\cdot\exp(-\int_0^t A)\).
  This is conditional on two hypotheses
  (\(\Gamma := \|\nabla u\|_\infty\) bounded,
  and \(\Lambda := \sup \lambda_{j_*}(t)\)
  bounded) but is otherwise a complete,
  checkable derivation with no gaps.

**Tape on §2.** Shell identity and
commutator **KEEP**. \(A.2\) **sits**
(Hölder \(6,2,3\), not Kato–Ponce).
Peak-fraction floor is **not**
unconditional. It assumes
\(\|\nabla u\|_\infty\) and a bound on
\(j_*\). That is BKM-adjacent. On this
desk \(A.3\) is a ceiling, not a floor.
The displayed \(D^-\rho\) write is not
seated as primary.

## 3. Claimed, Pending Independent Verification

- Exact-shell 9D: \(K \le 16/9\). A
  separate track, via a projected
  complex-polarization estimate →
  ordered/symmetrized factor \(1/2\) →
  squared → \(1/4\) → weighted-incidence
  factor \(3\) → \(K \le 16/9\). Status is
  explicitly CLAIMED, not proved: a
  written derivation exists and internal
  checks (including a three-shear
  numerical example giving \(K_{1,2}=2/3\))
  are consistent with it, but two
  specific pieces — the projected
  complex-polarization identity, and the
  weighted-incidence count including
  multiplicities and normalization
  convention — have not yet been
  independently reproduced from the
  definitions. The correct firewall is
  being maintained: exact-shell 9D
  \(\neq\) an unrestricted estimate
  \(\neq\) regularity closure. This
  result, even if fully verified, is a
  restricted-shell identity, not a route
  to global regularity by itself.

- Kato–Ponce self-commutator citation.
  Used in the corrected \(F_j\) bound
  above. The form used is standard and
  well-known in this literature, but has
  been used from recollection rather than
  checked against a primary source
  (Kato–Ponce 1988, or Majda–Bertozzi).
  This is a fifteen-minute verification,
  not an open research question, and
  should be closed before any of the
  above is presented externally as
  settled.

**Tape on §3.** Exact-shell \(K\le 16/9\)
**CLAIMED**. Freeze sweeps. Designed
\(\Theta(m^2)\) 9D is **NO**. Do not
write “9D is claimed.” Kato–Ponce is
cheap, **not** the foundation of \(A.2\),
**not** step 1 of the living attack.

## 4. What Has Died, and Why

| Claim | Reason it failed | Tape |
|---|---|---|
| Theorem H (original) | Conflated \(\Pi_j\) with \(F_j\), dropped viscous tail; false 3-D Sobolev embeddings; shear ratio \(\to\infty\) (to \(\sim 9\times 10^8\)). | **DEAD.** Agree. |
| Universal (\(M\)-free) nonlinear bound | \(F_j\sim A^3\) vs quadratic capped by \(X\le M\). | **DEAD.** Agree. |
| Universal initial-time SND floor | Equal-enstrophy \(L\) shells, \(\rho(0)=1/L\). | **DEAD.** Agree. |
| C10 (Cursor track) | First new arrow in depletion \(\Rightarrow\) (A) is already the conclusion, or smuggles \(\|\nabla u\|_\infty\) via Kato–Ponce remainders. Not an independent mechanism. | **NO as a program death.** (A) not seated. Leftover 5 stays OPEN. Write-or-kill. |
| Geometric-tail / BKM as primary | Not false — demoted. Downstream of BKM. | **Demoted as primary.** Agree. |

## 5. The Central Obstruction — Stated Once

Every currently active lane — the
peak-fraction floor, the C10 depletion
mechanism, the centered spectral drift
criterion \(T_c = M - \Lambda N\) —
reduces, at some point in its chain, to
the same unresolved question: does an a
priori bound on \(\|\nabla u\|_\infty\)
(or an equivalent Beale–Kato–Majda-type
control) follow from \(X \le M\) alone,
or from the Navier–Stokes dynamics
without assuming it? Nobody currently
has that proof. This is not a
bookkeeping gap or a missing citation —
it is a form of the open 3D
Navier–Stokes regularity question
itself.

This means the three lanes are not
independent attacks of decreasing
importance — they are three different
bets on the same unresolved dynamical
question, wearing different notation.
None currently has a proof that the
dynamics themselves cooperate; all three
are structured hopes that some quantity
(peak fraction, depletion rate, centered
drift) turns out to decay or concentrate
favorably. Treating C10 or 9D as
“closer to done” than the SND
conditional theorem, merely because
their framing sounds more dynamical,
would be a mistake — none of the three
has cleared the actual gate yet.

**Tape on §5.** Same difficulty class:
yes. Same estimate shape: **no**.
Centered \(T_c\) and local \(a_+\) have
different death conditions. Treating
them as notation variants is how you
stop attacking cancellation. None is a
close. C10 is not closer to done as a
theorem. It is still the first
write-or-kill on leftover 5.

## 6. Recommended Pathway Forward

In order of cost and dependency —
cheapest and most load-bearing first:

1. Verify the Kato–Ponce citation
   against a primary source.
2. Synchronize the corrected
   (lower-direction) Gronwall derivation
   into the canonical repository
   document. Re-run the shear-family
   test against corrected \(D^-\rho\).
3. Close out 9D: independently
   reproduce the two flagged pieces, or
   find the break. No more \(K\) sweeps.
4. Generate the next depletion-mechanism
   candidate under the same discipline
   that killed C10.
5. Decide whether centered spectral
   drift is worth independent pursuit.
   Do not merge with C10 unless an
   explicit inequality connects them.
6. Maintain the conditional theorem as
   a publishable fallback.
7. Exploratory: a different quantity
   than \(\rho=J/X\).

**Tape on §6.** This desk does **not**
take that order as primary.
[`MASTER-PLAN.md`](../MASTER-PLAN.md):

1. Freeze H, \(\rho\)-floor as primary,
   9D sweeps.
2. Route A: dynamical \(a_+\) without
   \(H^1/L^\infty/\)BKM, or name the
   death.
3. Route B: useful \(K\) for \(T_c\),
   already decided, independent.
4. SND instrument. Exact-shell stays
   CLAIMED. Kato–Ponce cheap, not
   load-bearing for \(A.2\).

## 7. Honest Ceiling

Closing this equation unconditionally —
proving that \(X \le M\) forces
\(\|\nabla u\|_\infty\) to stay finite,
with no further hypothesis — is not
something that follows from more careful
bookkeeping on any of the three current
lanes. It is a form of a major open
problem in the field. Nobody has that
proof.

The realistic best outcomes: (a) a
verified conditional theorem, honestly
labeled; (b) a catalog of falsified
candidates; (c) a new mechanism that
survives the same standard — a discovery
to hope for, not a deliverable to
schedule.

Cover sheets should say: active research
program, with a validated conditional
partial result and a catalog of
rigorously falsified candidate
mechanisms — not “near proof.”

**Tape on §7.** Agree as a public
sentence. Not near proof. NS not solved.

---

End of incoming status report.
NS not solved.
