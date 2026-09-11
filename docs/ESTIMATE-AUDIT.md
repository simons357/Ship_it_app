# Estimate audit — axisymmetric shell filter

11 September 2026. This is the filter.
**Not a proof. NS not solved.
Class is axisymmetric with swirl.
Remainder is \(T_{j\leftarrow j}\).
Do not start H1. Do not stamp ★.
Do not add a field to the PDE.**

Anything written next uses this page.
KEEP may enter the estimate.
DISCARD does not enter the identity,
the Young step, or the claim sentence.
PARK lives in another stack.

Probe: `python3 scripts/estimate_audit.py`

The estimate this filter wrote:
[`AXISYM-SHELL.md`](AXISYM-SHELL.md).
Identity and far-shell Young sit.
Remainder \(T_{j\leftarrow j}\) is open.

---

## The estimate this filter is for

First sentence, every time:

Axisymmetric-with-swirl Navier–Stokes,
unaugmented, one named manifold;
quantity is the shell budget (named
\(Z_j\) or the exact stand-in in the
first line); remainder is
\(T_{j\leftarrow j}\); extra hypotheses
in brackets, in the open.

That is a restricted class. It is not
unrestricted 3-D regularity. It is not
Lemma★. It is not H1 / WRITE (6).
Do not glue those three.

Pick \(\mathbb{T}^3\) or \(\mathbb{R}^3\)
in that first sentence and stay there.

---

## KEEP — method

These may enter.

- Write the exact identity first. Name
  the one term that can grow the
  quantity. Never bound that term by a
  copy of the time derivative you are
  estimating.
- State extra hypotheses in brackets,
  in the open, the way [SND] was
  stated. A conditional theorem is a
  theorem. A hidden hypothesis is not.
- Prefer a restricted class with real
  geometry (axisymmetric with swirl)
  over a modified PDE that is no
  longer classical NS.
- Measure before closing: signed
  triads, cancellation \(C\),
  \(\lvert T_c\rvert/\mathcal D_s\),
  shell block \(T_{j\leftarrow j}/Z_j\),
  occupancy, alignment \(\alpha\).
  If a number can come out the other
  way, it is allowed in.
- Unaugmented normalization. Do not
  add a field to help the estimate.
- Galerkin / truncation theorems with
  every constant named, scope in the
  first sentence.
- Energy conservation of the pairing
  as a check (\(10^{-16}\) residual).
  If the stepper and the diagnostic
  disagree, the identity is not closed.

---

## KEEP — objects that may enter

Bookkeeping that already sits:

\[
\Lambda'=\frac{2}{X}(T_c-\nu\mathcal D_s).
\]

Identity check. Not the final
left-hand side. Already on disk:
[`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
If the identity is not closed in the
time series, do not quote the sign
of \(\Lambda'\).

Seated as identities in
[`AXISYM-SHELL.md`](AXISYM-SHELL.md)
(not as bounds):

- Closed-triad rewrite
  \(\tau=(\omega(p)-\omega(r))J_p+(\omega(q)-\omega(r))J_q\).
- Shift by a lattice constant
  \(\omega_*\), not by \(\Lambda\).

Still named, not closed:

- Audit Door 1: shell budget. The
  only remainder is \(T_{j\leftarrow j}\).
  This is **not** Attack-6 “Door 1”
  (uniform pre-Young \(C\)), which is
  off.
- Door 3 as a **criterion to test**:
  vorticity-direction alignment
  \(\alpha\), kept separate from
  triad-phase occupancy.
- Swirl geometry as the class that
  removes free helical HHH. Class,
  not a close. Map:
  [`SWIRL-PAPER.md`](SWIRL-PAPER.md).

Samples named in the audit, **2-D
stays 2-D, 3-D stays 3-D**:

- 2-D: adversary
  \(\lvert T_c\rvert/\mathcal D_s\sim 0.017\),
  occupancy \(\sim 0.15\).
- 3-D: random-phase ratio still
  \(O(10^{-2})\), HHH occupancy 1 on
  the orbits that were run,
  \(\alpha\approx 0.5\).

Those numbers are allowed in as
printed measurements of those orbits.
They are not regenerated here.
Do not import the 2-D pair into 3-D.
Do not import occupancy 1 into
Constantin–Fefferman.

---

## KEEP — habits

- Send work with the gap visible.
- Refuse “visibility of cancellation
  \(=\) uniform smallness.”
- Separate modified equations from
  classical NS. Theorem A is a
  different PDE. It stays there.

---

## DISCARD — not in this program

If a paragraph needs one of these to
move, the paragraph is out. Not as
motivation inside the proof either.

- SFE, coherence viscosity, \(Q_1\)–\(Q_6\)
  as constitutive laws of classical NS.
  Other PDEs. A close of another PDE
  is not a close of NS.
- Any bound of the bad term by
  \(\Lambda'\), \(\dot Z_j\), or a new
  symbol of the same size.
- [SND] in its large form (“assume the
  dangerous interactions are not
  dangerous”) as if it were a
  smallness you measured.
- GCD spectral attractor, E8 cathedral,
  prime-harmonic lock, Borromean
  coherence as mechanisms that force
  \(T_{j\leftarrow j}\) small.
- Base 44 / gematria / letter-number
  maps as estimates. They do not
  bound a flux.
- Q6-Kabbalah, Lightning Flash,
  syncretic narrative inside the
  proof. Opinion stack only.
- Importing 2-D \(\rho=0.02\) into 3-D,
  or occupancy 1 into CFM.
- FFT-aliased orbits used as if
  \(\dot\Lambda=2(T_c-\nu\mathcal D_s)\)
  held.
- “Clay is solved,” “unconditional
  3-D regularity,” or any sentence
  that drops the class and the
  measured \(\rho_j\).
- Treating a Tao-positive reply as
  certification of a proof.
- Coherence-floor / extra memory /
  prime gates added to NS and then
  described as the Millennium
  problem.

Already off the live desk for the
same reason: [`SHELF.md`](SHELF.md).
SND is a named hole, not this
remainder: [`SND-H-PLAIN.md`](SND-H-PLAIN.md).

---

## PARK — other stacks

Not this estimate.

- Harmonic Blueprint / SFE as a
  standalone field model.
- Apps (Prime Breath, GCD Shells viz,
  Swirl publishing, FIELD MAPPER).
  Engineering and exposition. Not
  lemmas. The swirl *map* may be
  cited; the apps may not close a
  flux.
- Base 44 as an optional partition
  experiment: relabel existing
  triads; keep the label only if
  \(\rho_j\) drops. Until that test
  is run, parked.
- Defense / TITAN-X / HarborSafe.
- RH / Goldbach / “Three in One.”

---

## Standing orders

1. First sentence: class, quantity,
   remainder, what is assumed.
2. Remainder is \(T_{j\leftarrow j}\)
   (axisymmetric if that is the class).
3. Smallness is a printed ratio or an
   explicit integral of
   \(\|\omega\|_\infty\), not a story.
4. No object from the discard list
   appears in the identity, the Young
   step, or the claim.
5. If the identity is not closed in
   the time series, do not quote the
   sign of \(\Lambda'\).

---

## Score against this book

| id | Verdict | What it is |
|---|---|---|
| EAud_filter_seated | **pass** | KEEP / DISCARD / PARK is the writing rule |
| EAud_class_named | **pass** | axisymmetric with swirl, not all data |
| EAud_lambda_bookkeeping | **pass** | \(\Lambda'\) sits as an identity, not the LHS |
| EAud_remainder_named | **pass** | \(T_{j\leftarrow j}\) is the named hole |
| EAud_tau_seated | **pass** | Proposition AS-τ: rewrite, not a bound |
| EAud_omega_star_seated | **pass** | Proposition AS-ω\*: constant shift, not \(\Lambda\) |
| EAud_door1_closed | **fail** | shell budget remainder is open |
| EAud_door3_closed | **fail** | \(\alpha\) is a criterion to test, not a bound |
| EAud_discard_in_claim | **fail** | discard list does not enter the claim |
| EAud_ns_solved | **fail** | class and \(\rho_j\) stay in the sentence |

The axisymmetric shell estimate is
**OPEN**. Filter: this page.
Estimate: [`AXISYM-SHELL.md`](AXISYM-SHELL.md).
Identity and far-shell Young sit.
The remainder does not.

Do not start H1 from this page.
Do not cash a cube family or
ABC_λ table as \(T_{j\leftarrow j}\).
Do not weld ★ to this door.

NS not solved.
