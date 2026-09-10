# Latest chains — 10 September 2026

Phone pack. Same GitHub login as PR 24.
Branch: cursor/unaugmented-r4-vorticity-f80e

https://github.com/simons357/Ship_it_app/pull/24

---

## The three you asked for

**Aug NS (Track A) — closed for this PDE**
docs/A-CHAIN.md
https://github.com/simons357/Ship_it_app/blob/cursor/unaugmented-r4-vorticity-f80e/docs/A-CHAIN.md

Theorem A sits. Extra-stress NS, eps > 0,
beta >= 1/2. Known class (Ladyzhenskaya /
Malek–Necas–Ruzicka). Your note. Not
ordinary NS. Uniform H1 as eps → 0 still
open. Paper: docs/THEOREM-A-Q1.pdf

**Unaug NS (ordinary) — open**
docs/UNAUGMENTED-NS-CHAIN.md
https://github.com/simons357/Ship_it_app/blob/cursor/unaugmented-r4-vorticity-f80e/docs/UNAUGMENTED-NS-CHAIN.md

10 September packet. H-system:
docs/H-SYSTEM.md
Do not merge letters. H = global parent,
open. Lemma C is an if, not an H.
H1 = WRITE (6) = Lemma I on the ball.
H2, H3 labeled. Cylinder needs C+R_φ,
H1, H2-a priori (or CKN-small), and H3.
Local Serrin then, not CKN. Object:
docs/H1-OBJECT.md. Tube SoT (opened):
docs/H1-SOT.md. First tube numbers:
docs/H1-TUBE.md
(ABC stretch ~ A, not C(ρ,L); Burgers
J=0 by imposed strain; pair thinness
O(1) from Biot–Savart).
Estimate package OPEN, not a GR close:
docs/DOOR-B-H1-ESTIMATE-PLAN.md
L∞ sketch (MISSING marks):
docs/DOOR-B-H1-B5-LINFTY-SKETCH.md
Outside-E identity blocked. Enumerator
still on the star lane.
Gaps: §11. Literature:
docs/LITERATURE-H.md (H1 not under another
name). Lookups: all miss. docs/LOOKUP-H1.md.
Shapes as estimates, not proved:
docs/H1-SHAPES.md. CS-thinness is still
E^{3/2}, not H1.
WRITE (6): docs/WRITE_6.md
(supported: docs/WRITE_6_SUPPORTED.md).
Score of the write: aimed leftover yes;
theorem no. Dream-team read:
docs/DREAM-TEAM-H.md
(they would sign the map, not (6)).
Swirl paper (map, not a proof):
docs/SWIRL-PAPER.pdf
Magazine cut: docs/SWIRL-MAGAZINE.md
This week: docs/SWIRL-DEPOSIT.md
OpenAI forced blowup is C/D, not (6):
docs/OPENAI-NS-CLAIM.md
Lemma★ (energy-budget leftover, locked
as hypothesis, not proved):
docs/LEMMA-STAR.md
Working claim:
docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md
docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md
Four corrections:
docs/LEMMA-STAR-CORRECTIONS.md
Independent core (direct triad sum;
live stokes_moments.py not overwritten):
docs/LEMMA-STAR-CORE.md
scripts/ns_lemma_star_core.py
Object app (pictures; bound still open):
docs/THE-OBJECT-APP.md
apps/the-object/
R★ maximizer (N shells vs |k|_max; does not climb):
docs/RSTAR-SHELL-CLIMB.md
The \(a^4\) missing inequality is dead.
★ implies GR in this packaging; not equivalent.
Test both signs of \(T_c\). Section 4 is not proved.
Exact form: scale-invariant trilinear
shape estimate on R★. Live fork: sup R★
finite proves ★; a near-shell or HH→L
sequence with R★ → ∞ kills it. Samples
are evidence only.
File: docs/LEMMA-STAR-R.md
Three-key (Attack 8): two Fourier keys
Tc=0; two shells can be live. Isolated
triad did not kill ★.
docs/LEMMA-STAR-E.md
Packets (Attack 9): wide AP made Tc grow,
but Ds grew faster, so the O(1)
denominator failed. Adjacent spheres
(Attack 11): d=1 landings O(m), not
O(m^2); R★ falls. HH→L fan (Attack 12):
R★ ~ β/α, no blow. Designed Θ(m^2)
subset is Freiman-AP, already dead.
The m^{1/2} heuristic has no lattice
home. Route A incidence (conditional):
docs/LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md
kills Θ(m^2) in the continuum model if
I ≪ m^{4/3}. Lattice transfer X1–X4/X6
MISSING. Next: Hyp-Lat★. Not a theorem.
H1 on one cylinder is the other
live writing (docs/H1-SOT.md). Bound open.
docs/LEMMA-STAR-PACKET.md
Attack 6: uniform pre-Young C dead
(|R_pre| ~ s). That is not ★ dying.
docs/LEMMA-STAR-NEXT.md
K=0 dead. Lattice HH→L did not kill.
Numeric kill-survive is not a proof.
Drill: GitHub PR 48.
Original five lanes (not 9A–9D):
docs/FIVE-LANE-DISCUSSION.md
docs/five-lane-export/FIVE_LANES.md
Pack (ffe858c folder plus tests):
docs/FIVE-LANE-PACK.md
Five-lane export (defs + HH→L):
docs/five-lane-export/INDEX.md
Original computation (JSON, not a re-proof):
docs/five-lane-export/COMPUTE.md
results/ns_five_lane_2026-09-10/
Attack 9B exact-shell \(K_{\alpha,\beta}\)
(max \(K\approx 0.641\) at \((4,8)\); not a kill):
docs/five-lane-export/ATTACK_9B.md
Fixed-output \(\Theta(m^2)\): counting error,
\(K\le 16s\). docs/LEMMA-STAR-9B-COUNTING.md
No \(K(t)\). No Q1.

**RH — open**
docs/RH-CHAIN.md
https://github.com/simons357/Ship_it_app/blob/cursor/unaugmented-r4-vorticity-f80e/docs/RH-CHAIN.md

HAVE (1)–(5) literature. WRITE (6) still
missing. Q is not this leftover.

---

## The others (progress, not closes)

**Q (inverse-GCD) — some facts sit**
docs/Q6-FLOOR-CHAIN.md
Theorem P, H_N >= −1, Bridge*, nonnegative
form. Full Q floor and H_N >= −3/14 stay
false. Not RH.

**Goldbach-shaped — corollary sits**
docs/GOLDBACH-CHAIN.md
If that prime-difference vector is nonzero,
R >= −2/9. Not Goldbach’s conjecture.

**Poincaré — literature sits**
docs/POINCARE-PROOF-CHAIN.md
Perelman. You reprinted the map. You did
not prove it here.

**Yang–Mills mass gap — open**
docs/YM-PROOF-CHAIN.md
HAVE: gauge field / SM kinetic term.
WRITE: the mass gap. Not sitting.

**BSD — open**
docs/BSD-PROOF-CHAIN.md
HAVE (1)–(5) including low-rank literature.
WRITE (6): every E/Q. Zenodo 20552682 is Q
as a prototype, not BSD.

**Hodge — open**
docs/HODGE-PROOF-CHAIN.md
HAVE: Hodge decomposition, Lefschetz (1,1),
some special cases. WRITE (6): every
rational Hodge class. No Hodge paper here.

**P vs NP — open**
docs/PNP-PROOF-CHAIN.md
HAVE: P, NP, Cook–Levin. SFE is not the
model. WRITE: a TM proof either way.

---

Nothing else on this desk closed a leftover
overnight. Maps moved. Leftovers did not.
