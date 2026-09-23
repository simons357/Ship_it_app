# Master plan — unaugmented 3-D Navier–Stokes

16 September 2026.
**How this desk moves. Not a proof.
Ordinary NS is not solved.
Catalog B open stays 1.**

Adjudication of the incoming
reports: [`REPORT-AUDIT.md`](REPORT-AUDIT.md).
Score: [`NS-STATUS.md`](NS-STATUS.md).
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).
Operator report after every peer
note: [`NS-CLOSE-REPORT.md`](NS-CLOSE-REPORT.md).
Path to a close (G1 then G4):
[`PATH-TO-CLOSE.md`](PATH-TO-CLOSE.md).
Route A write (pairing, not
\(L^\infty\)):
[`ROUTE-A-WRITE.md`](ROUTE-A-WRITE.md).
B★ (no universal \(C\); imag cutoff
grows \(R_B\); not a useful \(K\)):
[`BSTAR.md`](BSTAR.md),
[`BSTAR-PROOF.md`](BSTAR-PROOF.md).
Fourier-triangle geometry
(identities sit; first missing
arrow to Route B; not a close):
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).
First lift (\(K\sim\sqrt{E}\)
dead; G4 still OPEN):
[`TRIANGLE-LIFT.md`](TRIANGLE-LIFT.md).
Energy-class ladder (dead;
pathwise \(K\) still the G4
target):
[`ENERGY-K.md`](ENERGY-K.md).
Pairing CS doors:
[`L-DOOR.md`](L-DOOR.md).
Instantaneous \(MN\):
[`MN-CANCEL.md`](MN-CANCEL.md).
First jet:
[`PATHWISE.md`](PATHWISE.md).
Short interval:
[`INTERVAL.md`](INTERVAL.md).

This page answers the operator’s
question: how do we beat unforced
3-D Navier–Stokes with the
machinery that survived?

**Enough information?** Yes for
this plan. No for a close.
Incoming reports plus the tape
are enough to name the leftover
and order the next writes. They
are not enough to seat (A) or a
useful \(K\).

This desk is **unaugmented**.
Track A / \(Q_1\) / Theorem A is
a different PDE. A is not B.
Do not switch.

Honest first sentence: **we do
not have a seated close.** A
successful route has to produce
an a priori mechanism that keeps
smooth admissible data smooth.
Two target shapes on this desk
could still do that. Both are
OPEN. Both can die. If both die,
the leftover is a **new estimate
shape**, not a repair of a dead
box.

Do not start leftover 1 from this
page. Do not weld \(\star\).
Do not add \(K(t)\) to the PDE.
Do not mail a panel.

---

## What “beat it” means here

Official Statement (B), unforced,
smooth divergence-free finite-energy
data on \(\mathbb{T}^3\) or
\(\mathbb{R}^3\). Track B. Keep
\(1/r^4\). No \(Q_1\). No
\(\Phi\)-cancel. No modified
viscosity.

A close is one of:

1. an a priori bound that prevents
   finite-time loss of regularity,
   or
2. a named smooth field in the
   class that blows up.

This desk has been aimed at (1).
OpenAI’s forced construction is
(C)/(D) if it holds. It is not
(1) and not (2) for unforced data.
A blowup hunt (Córdoba–Martínez-Zoroa
/ self-similar profiles) is a
different program. Do not switch
the living line to it unless the
operator names that switch.
Rocks’ cut-off line “prove that
viscosity always pre[vents …]”
is this desk **only** as an
a priori from unforced data.
It is not “drop the OpenAI force
and watch the same profile.”

---

## What is already decided

**Do not spend primary effort on**

- repairing displayed Theorem H,
- a universal \(\rho\)-floor,
- more exact-shell sweeps,
- BKM from an assumed tail,
- SFE / Q / HB / \(K(t)\) in the PDE,
- restoring unrestricted \(\star\),
- starting H1 from ABC_λ,
- welding C10 to \(T_c\) without
  an inequality,
- the Endgame covering of dead
  triads / \(Q_6\) spectral gap /
  restoring \(\Phi\) or Ring.

**Keep as tools, not theorems**

- spectral bookkeeping
  \(X,Y,Z,\Lambda,T_c,\mathcal D_s\),
- SND instrument
  \(X_j,J,\rho,j_*,\gamma,F_j\),
- \(A.2\) on \(F_j\) under \(X\le M\),
- TJJ-Trans, TJJ-α, stretch
  \(\le a_+ Z_j\).

**CLAIMED, frozen**

Exact-shell \(C=4/3\), \(K\le 16/9\).
Independent reproduction only.
Designed 9D is **NO.**

---

## The two routes that can still carry (1)

They are independent. They have
explicit death conditions.

### Route A — C10 / near-scale depletion

Class: local block
\(T_{j\leftarrow j}\)
(axisymmetric-with-swirl leftover 5;
same local piece in unrestricted 3-D).

Need the whole chain, every arrow
marked:

\[
\text{NS}
\Rightarrow
a_+\text{ from the dynamics}
\Rightarrow
\int a_+<\infty
\Rightarrow
(A)
\Rightarrow
\text{control of the local block}.
\]

What already sits: stretch
\(\le a_+ Z_j\) (EXACT).
TJJ-template (STANDARD; \(L^\infty\)
remainder).

What failed to seat: depletion of
\(a_+\); remainder of (A).

**How this beats NS if it works.**
If (A) sits with \(\int a_+<\infty\)
and the remainder is energy-class,
the local block no longer feeds a
finite-time enstrophy blowup by
near-scale stretching. Combined
with the far-shell Young that
already sits, leftover 5 moves.
That is **not** leftover 1 and
**not** unrestricted 3-D by itself.
A later write would still have to
pass from the local block to
global \(X\). Do not pretend that
arrow exists today.

**Death condition.** Any of:

- \(a_+\) controlled only by
  \(\|\nabla u\|_\infty\) or a
  Sobolev embedding of the unknown
  field (BKM / circular);
- remainder of (A) estimated by
  Bernstein so Gronwall wants the
  \(H^1\) ceiling;
- an adversarial family with
  \(a_+\) large and the local
  block uncontrolled;
- a silent strengthening that
  assumes the conclusion.

If Route A dies, record the
failed arrow and stop patching.
Leftover 5 stays OPEN.

**Next write (only this).**
A-pair: control
\(\int(\alpha)_+\lvert\Delta_j\omega\rvert^2\)
plus the commutator, not
\(\|(\alpha)_+\|_\infty\).
[`ROUTE-A-WRITE.md`](ROUTE-A-WRITE.md).
Bounding \(a_+\) by
\(\|\nabla u\|_\infty\) is BKM.
If A-pair cannot be written
without \(H^1\), \(L^\infty\),
or BKM, Route A is dead as an
a priori. Do not invent
depletion.

### Route B — centered spectral drift

Class: unrestricted smooth
divergence-free fields on
\(\mathbb{T}^3\).

Target:

\[
T_c
\le
\theta\nu\mathcal D_s
+K(t)X,
\qquad
\theta<1,
\]

with \(K\) **useful** and
\(K\in L^1_{\mathrm{loc}}\).

Useful means: \(K\) is controlled
by the energy inequality or by a
named cancellation in
\(T_c=M-\Lambda N\), not by
defining \(K=(T_c-\theta\nu\mathcal D_s)_+/X\).

What already sits: the identities,
including
\((\log\Lambda)'=2(T_c-\nu\mathcal D_s)/Y\)
and the formal implication
“estimate \(\Rightarrow\Lambda'\le 2K\)
\(\Rightarrow X\) bound.”

What is OPEN: the estimate.

What is DEAD: unrestricted ★
(uniform \(C_0\nu^{-1}EY\) remainder),
killed by \(v_n\).

**How this beats NS if it works.**
A useful integrable \(K\) keeps
\(\Lambda\) finite, hence
\(X\le\|u\|_2^2\Lambda\) finite,
hence no finite-time enstrophy
blowup on the torus, **in this
packaging**. One direction only.
No converse.

**Death condition.** Any of:

- every proposed \(K\) is
  tautological;
- \(K\) is a uniform function of
  energy-class norms of ★ scaling
  (\(v_n\) already kills that);
- \(K\) is \(\|\nabla u\|_\infty\)
  (BKM);
- \(M\) and \(\Lambda N\) are split
  so the centering is lost and the
  remainder is worse than ★.

**Next write (only this).**
Keep \(T_c-\theta\nu\mathcal D_s\)
as one pairing. Hunt cancellation
from the moving center. Test the
remainder on \(v_n\), amplitude,
shears, and single shells. Do not
restore \(\sup\mathcal R_\star<\infty\).

### Crossover

Only if Route A seats (A).
Then ask for an actual inequality
from \(a_+\) to \(T_c\).
None sits. Do not draw a
conceptual arrow.

---

## If both routes die

Then the energy-budget path needs
a **different leftover-4 estimate**
that \(v_n\) does not kill.
Need★ cannot repair the dead box.

The geometric path (leftover 1 =
H1 = WRITE (6) on the cylinder)
is a different integral. It is
OPEN. It is **not** started from
this plan. Shapes 1–3 remain the
named missing estimates there.

Axisymmetric leftover 5 stays
OPEN until Route A seats or a
field with \(\int\rho_j=\infty\)
is written.

That is the honest remaining
map. It is not a third fake
bridge.

---

## Execution order (this desk)

1. **Freeze.** Theorem H.
   Exact-shell sweeps. Designed 9D.
   Blowup-search as the living
   line. Leftover 1.
2. **Route A write or kill.**
   One page: dynamical \(a_+\)
   or a named death of that
   arrow. Adversarial families
   already on the desk. No new
   9D sweeps.
3. **Route B write or kill.**
   Independent. Centered pairing
   only. Useful \(K\) or a named
   death.
4. **Crossover** only after (A)
   sits.
5. **SND** stays an instrument.
   Print \(\rho\), \(j_*\), tail,
   \(F_j\), \(\Delta j_*\). Do
   not assert persistence.
6. **Score** every write in
   four buckets. If a later
   sentence contradicts
   [`YES-NO-OPEN.md`](YES-NO-OPEN.md),
   the tape wins.

No parallel resurrection of H.
No Pólya \(\rho\)-floor document
as primary. A \(D^+\) comparison
cannot produce a \(\rho\) floor.
No “9D is claimed.”
No Kato–Ponce stall of Route A.
No switch to Track A.

---

## Peer recommendations, accepted or not

From the long 16 Sep “Global
Regularity Program” write.
Full score: [`REPORT-AUDIT.md`](REPORT-AUDIT.md)
§8.

**Accept now**

- Route A: next depletion write
  under the C10 discipline
  (dynamical \(a_+\), or name
  the death).
- Route B already chosen:
  centered pairing, useful \(K\).
- \(\Gamma\)-conditional as a
  publication fallback, not
  the living attack.
- Exact-shell bound stays
  CLAIMED. No more sweeps.

**Reject as primary**

- Lower-Dini \(\rho\)-floor /
  “synchronize the corrected
  peak-fraction floor.”
- “C10 died — generate a
  different mechanism” as if
  the candidate program is
  already dead. The failed
  seating of (A) is the reason
  Route A is a write-or-kill,
  not a burial.
- “Decide whether” centered
  drift is worth it. It is
  Route B.
- Kato–Ponce citation as the
  load-bearing next step.
  \(A.2\) is Hölder \(6,2,3\).
- Close 9D on this desk.
- Switch the living line to
  augmented NS or to a
  blowup hunt.

---

## What would count as winning

A seated inequality, with every
arrow marked, that

- does not assume \(H^1\),
  \(L^\infty\), BKM, or the
  desired conclusion,
- survives the named families
  (\(v_n\), shears, amplitude,
  \(v_L\), mixed swirl),
- and implies an a priori bound
  on \(X\) (Route B) or on the
  local block with a written
  passage to \(X\) (Route A plus
  a later global step).

Until that page exists, the
answer to “how do we beat it”
is: **attack those two
inequalities and accept a
named death if they fail.**
Talking is not the close.

---

## Lock

Unrestricted ★ is KILLED, not
OPEN. C10 is a candidate, not a
theorem. Centered drift is a
target, not an estimate.
A.3 is a ceiling, not a floor.
Blowup-search is not this line.
Do not repair H.
This desk is unaugmented.
Enough for this plan. Not a close.
Two routes, independent, both
OPEN, both killable.
NS not solved.
