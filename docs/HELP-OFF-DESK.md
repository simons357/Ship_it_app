# Help needed to get this off the desk

12 September 2026.
**Not a close. Ordinary Navier–Stokes is not
solved. The Riemann hypothesis is not
solved. This is a request for estimates.**

To everyone who worked on this project.

One-page send sheet (every leftover, rows 1–12):
[`ISSUES-SHEET.md`](ISSUES-SHEET.md).
This page is the math for rows 1–5. A person who was
not in the chat can work the leftovers
from either page. It does not ask anyone
to certify a proof that is not there. It
does not ask OpenAI, Tao, or Albritton
to finish the leftover by attention.

Operator: Jonathan Robert Simons
(Prime Field Technologies). Living line:
GitHub PR 24, branch
`cursor/unaugmented-r4-vorticity-f80e`.
Filter for anything written next:
[`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).

---

## 0. Glossary (desk words, once)

| Word | Meaning here |
|---|---|
| Desk | This project’s notes and checks. Not furniture. |
| Scored | Checked (sits / wrong / still missing). The check is not the proof. |
| DA | Domain Architect: a checker and a map. Not a closer. |
| Track A | Extra-stress / \(Q_1\)-augmented NS. Different PDE. |
| Track B | Classical unaugmented NS. Keep \(1/r^4\). No extra field. |
| WRITE (6) | The named missing estimate on that track. |
| H1 | WRITE (6) = Lemma I on the ball. Same leftover. |
| Lemma★ | Energy-budget writing of leftover (6) on \(\mathbb{T}^3\). Different integral. |
| [ρ] | Extra hypothesis on the axisymmetric local remainder. An *if*. |
| Occupancy | Printed share of modes in a shell. Not Constantin–Fefferman. Not the withdrawn wall detector. |

Do not merge: fluids **H**, matrix \(H_N\), stretching H-system, leftover H1, Theorem A’s Sobolev \(H^1\), GCD \(H_M[a]\).

---

## 1. Official split — do not mix slots

Fefferman’s four statements cut on force.

- **(A)/(B).** Unforced. Smooth data stay
  smooth on \(\mathbb{R}^3\) or on the torus.
  That is Track B. **Open here.**
- **(C)/(D).** A smooth force is allowed.
  Ask for breakdown. The 8 September 2026
  announcement sits in that slot *if* the
  write-up holds. [`OPENAI-NS-CLAIM.md`](OPENAI-NS-CLAIM.md).

A forced finite-time construction is not
unforced regularity. A vortex picture is
not WRITE (6). Theorem A is not (A)/(B).

Constantin–Fefferman 1993 and Beirão da
Veiga–Berselli 2002 already own the
geometric *if*: alignment of vorticity
direction at Lipschitz, then at Hölder
\(1/2\). Good pairs are their theorem.
Bad pairs are the pairs they refused.
That cut is not a 2026 invention.

---

## 2. What is already off this desk

Do not redo these. Send them with honest
titles, or leave them taped.

**Theorem A (Track A).** Extra-stress NS,
\(\varepsilon>0\), \(\beta\ge 1/2\), on
\(\mathbb{T}^3\): globally regular. Known
class (Ladyzhenskaya / \(p\)-Laplacian /
Málek–Nečas–Růžička). The note is ours.
The class was already known. Uniform
\(H^1\) as \(\varepsilon\to 0\) is still
open and is **not** required for A to stay
finished. A is not B.
Files: `docs/THEOREM-A-Q1.pdf`,
[`A-CHAIN.md`](A-CHAIN.md).

**Inverse-GCD / Q.** Bridge*; Theorem P;
\(H_N\ge -1\); nonnegative form;
Goldbach-shaped corollary (not Goldbach).
Zenodo 22045478. Not RH. Full Q floor
\(>-1/2\) and \(H_N\ge -3/14\) were taken
back. [`DA-Q.md`](DA-Q.md).

**Taken back, stay back.** \(\Phi\)-cancel
as the ordinary-NS path. HB as a unifier.
SFE / UHF / DHFA as constitutive NS.
Occupation decay from the swirl-wall
detector. [`SWIRL-WALL-CORRECTION.md`](SWIRL-WALL-CORRECTION.md).

Those items are off the B desk. Help on
B is not help on A, and not help on Q.

---

## 3. Three writings on Track B — three integrals

Do not glue. A number on one is not a
bound on the others.

### 3.1 Geometric leftover — H1 = WRITE (6)

Class: unaugmented NS on \(\mathbb{R}^3\)
or a cylinder \(Q_r\). Quantity: Bad-pair
stretching. Remainder: \(A_{\mathrm{bad}}\).
No extra field.

On \(\{\omega\neq 0\}\), \(\xi=\omega/|\omega|\),
\(\varphi(x,y)\) the angle between
\(\xi(x)\) and \(\xi(y)\). Stretching is
\[
\alpha(x)=\mathrm{P.V.}\int
D(\hat z,\xi(x),\xi(y))
\frac{|\omega(y)|}{|x-y|^3}\,dy,
\qquad
|D|\le C|\sin\varphi|.
\]

**Good.** \(|\sin\varphi|\le C_*|x-y|^{1/2}\)
whenever both \(|\omega|\ge\Lambda\).
Lemma C. Their theorem as an *if*.
Localization to \(Q_r\) leaves a cutoff
error \(R_\phi\). Not free.

**Bad.** \(|\omega|\ge\Lambda\) and
\(|\sin\varphi|>C_*|x-y|^{1/2}\). Kernel
still \(|z|^{-3}\). HLS returns local
\(E^3\). The Hölder cut changes the set,
not the exponent.

**The request (stated, not proved).**
On \(Q_r\), Bad pairs only, both ends in
the ball,
\[
A_{\mathrm{bad}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]
Equivalent majorant (\(|D|\le C|\sin\varphi|\)):
\[
\iint\!\!\int_{\mathrm{Bad}}
\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}\,\phi
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]
\(\nu/8\) is a conventional slice, not a
sharp constant. Parabolic scaling of the
three terms agrees. There is no dimensional
obstruction. There is also no proof.

Near-Bad (\(|x-y|<\rho\)) is the core.
Mid-Bad is a named remainder. It is not
H1. Tube stretching on one cylinder is
the same leftover class, a different
integral. Do not merge the two.
[`WRITE_6.md`](WRITE_6.md),
[`H1-OBJECT.md`](H1-OBJECT.md),
[`WHERE-H1.md`](WHERE-H1.md),
[`H-SYSTEM.md`](H-SYSTEM.md).

**Letters on the same cylinder, not H1.**

| Letter | What it is | Status |
|---|---|---|
| C | Good pairs | Theorem as an *if*. Not an H. |
| H1 | Bad pairs, WRITE (6) | **Open. This is the request.** |
| H2 | Flux \(r^{-1}\iint|u||\omega|^2\) | CKN-smallness sits. From energy alone: open. |
| H3 | Exterior Biot–Savart | Written. Not absorbed as \(r\to 0\). |
| H | Global parent stretching | Open. A cylinder is not this parent. |

A cylinder closes only if
\(\mathrm{C}+R_\phi\), H1, H2-a priori
(or CKN-small), and H3 all sit. Then
local Serrin gives smoothness on
\(Q_{\theta r}\). If H1 sits and
H2-from-energy does not, the cylinder
still does not close.

**Cousins that sit and are not H1.**

- P1-lowpass: on
  \(\widehat{\omega}(k)=0\) for
  \(|k|>K\le C/\rho\),
  \(\rho^2\int|\omega|^2\le C^2\int|u|^2\).
  NSE membership open.
  [`H1-P1.md`](H1-P1.md).
- P1-loc: cutoff form, \(\nabla u\) kept.
  Dropping \(\nabla u\) fails.
  [`H1-P1-LOC.md`](H1-P1-LOC.md).
- PC: on a \(C^1\) path,
  \(\int_\gamma|\nabla\xi|\ge\varphi\ge|\sin\varphi|\).
  One-dimensional. A sheet or a gap
  removes the path. [`H1-PC.md`](H1-PC.md).

Literature lookup: all miss. H1 is not
under another name.
[`LOOKUP-H1.md`](LOOKUP-H1.md),
[`LITERATURE-H.md`](LITERATURE-H.md).
Ring Lemma direction bound is **REPAIR**.
Do not quote it as proved. Do not start
H1 from ABC_λ. Do not add \(K(t)\) to
the PDE.

**The only shapes that still look like H1.**
Prove one, and you have H1. None sits.

1. **Thinness.** Bad-pair measure in each
   \(B_r\) small enough that HLS turns
   \(E^3\) into \(E^2\) or into dissipation.
   CS-summable volume thinness is still
   \(E^{3/2}\). That is not H1.
2. **\(J\) on folds only.** Persistent-bad
   pairs live in folds, not sheets or gaps,
   so \(\int_{B_{2\rho}}|\nabla\omega|^2
   \gtrsim\Lambda^2\rho^2\) and a Vitali
   sum closes. Not Lemma J on generic
   fields.
3. **Dynamics.** NSE forbids the
   alternatives to (2) on the time scale
   \(r^2/\nu\). Not an imposed wait.

Outside-\(\mathcal{E}\) identity: blocked.
No candidate. Do not invent one.

### 3.2 Energy-budget leftover — Lemma★

Class: divergence-free fields on
\(\mathbb{T}^3\). Quantity:
\[
\mathcal R_\star(v)
=
\frac{(T_c(v)_+)^2}{\mathcal D_s(v)\,E(v)\,Y(v)}.
\]
Remainder: the uniform bound
\(\sup_v\mathcal R_\star<\infty\).
No extra field.

\(A=-P\Delta\), \(B(v,v)=P[(v\cdot\nabla)v]\),
\(E=\|v\|_2^2\), \(Y=\|Av\|_2^2\),
\(\mathcal D_s=Z-\Lambda Y\),
\(T_c=M-\Lambda N
=-\langle B(v,v),A(A-\Lambda)v\rangle\).

**Boxed claim (hypothesis, not a theorem).**
\[
(T_c)_+^2
\le
C_{\mathrm{geom}}\,\mathcal D_s\,E\,Y.
\]
Young packaging:
\[
T_c
\le
\theta\nu\mathcal D_s
+C_0\nu^{-1}E\,Y,
\qquad
C_0=C_{\mathrm{geom}}/(4\theta).
\]
Equivalent trilinear form
(\(C_{\star}^2=4\theta C_0\)):
\[
\bigl[-\langle B(v,v),A(A-\Lambda)v\rangle\bigr]_+
\le
C_{\star}\|v\|_2\|Av\|_2
\bigl\|(A-\Lambda)A^{1/2}v\bigr\|_2.
\]
This \(C_{\star}\) is ★. It is not
Attack-2 \(C_*\).

★ \(\Rightarrow\) GR in this packaging,
one direction. No converse is written.
A sequence with \(\mathcal R_\star\to\infty\)
kills ★. A finite sample only raises
\(C_{\mathrm{geom}}\).

**Already dead, do not rebuild.**

- \(K=0\) (\(T_c\le\theta\nu\mathcal D_s\)
  as a universal bound). Amplitude kills it.
- \(|T_c|\le C\|u\|_2 X^{3/2}\). Scaling:
  left \(a^3\), right \(a^4\).
- Uniform pre-Young \(C\).
- Fixed-output \(\Theta(m^2)\)
  (\(K\le 16s\); growing \(s\) stays live).
- Freiman-AP 9D.

**Already scored, not a kill.** Isolated
triad; wide/narrow AP (\(\mathcal D_s\)
wins); adjacent spheres; HH→L fan
(\(\mathcal R_\star\sim\beta/\alpha\));
N-shell climb \(\mathcal R_\star=0.610\)
on \((1,2)\); 9B exact-shell
\(\max K\approx 0.641\) at \((4,8)\);
ABC_λ gate \(0.327\). None is \(C_0\).
None is \(\mathcal R_\star\to\infty\).

**Still missing for the incidence route.**
Continuum \(I\ll m^{4/3}\) would give
\(C(S)=O(m^{4/3})\) in the continuum
model. Lattice transfer X1–X4/X6 is
MISSING. Next name: Hyp-Lat★. That file
is not written. Do not emit it as a
theorem. [`LEMMA-STAR.md`](LEMMA-STAR.md),
[`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md),
[`LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md`](LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md).

### 3.3 Axisymmetric shell — remainder \(T_{j\leftarrow j}\)

Class: axisymmetric with swirl,
unaugmented, on \(\mathbb{R}^3\).
Quantity \(Z_j=\|\Delta_j\omega\|_2^2\).
Remainder \(T_{j\leftarrow j}\).
No extra field. Keep \(1/r^4\).

**Identity (sits).**
\[
\tfrac12\dot Z_j+\nu D_j=T_j,
\qquad
T_j
=
\langle\Delta_j(\omega\cdot\nabla u-u\cdot\nabla\omega),\Delta_j\omega\rangle.
\]
Door 1 split (sits):
\(T_j=T_{j\leftarrow\mathrm{IR}}
+T_{j\leftarrow j}
+T_{j\leftarrow\mathrm{UV}}\).

**Far-shell Young (sits).** Named
constants \(C_{\mathrm{IR}}[\varphi]\),
\(C_{\mathrm{UV}}[\varphi]\) only.
Infrared *transport* may absorb into
\(\nu D_j\). That absorption is not an
estimate of \(T_{j\leftarrow j}\).

\(\tau\) and \(\omega_*\) are identities,
not bounds. The sign of \(\Lambda'\) is
not quoted (no closed time series).

**[ρ] (not measured for the class).**
On \(\{Z_j>0\}\),
\[
\rho_j(t)=\frac{(T_{j\leftarrow j})_+(t)}{Z_j(t)},
\qquad
\int_0^T\rho_j(t)\,dt<\infty.
\]
Under [ρ] plus the far Young lemmas,
\(Z_j\) stays finite on \([0,T]\). A
conditional theorem is a theorem. [ρ]
is not a smallness that was measured.

**Printed, not a class bound.** Compact
swirl on a ball \(R=2.4<\pi\), dealiased
Leray interpolant. Pairing residual
\(10^{-18}\). Pure swirl: \(\rho_j\sim 0\).
Swirl plus meridional:
\(\max|T_{j\leftarrow j}/X_j|\) from
\(6\times 10^{-4}\) to \(1.4\times 10^{-3}\)
on \(n=32,48\), and it moved with \(n\).
Local-remainder cancellation
\(C\sim 0.22\). Support occupancy of the
peak shell \(j=1\): \(55/56\). That share
did **not** fall with \(n\). \(\rho_j\)
did. \(\alpha\) stays separate.
[`AXISYM-SHELL.md`](AXISYM-SHELL.md),
[`AXISYM-SWIRL-PROBE.md`](AXISYM-SWIRL-PROBE.md).

**Dictionary, corrected.**
\(F=u^\theta/r\), \(G=\omega^\theta/r\),
\(\Gamma=ru^\theta=r^2F\), \(U=u^r/r\).
Integrating-factor exponent
\(p(1-d)\int\overline U_{d,p}\).
The source wall is a time-window *if*:
\[
\int_{\sigma-h}^{\sigma}
\|(u^r)_-(t)\|_\infty\,dt
\le
2\sqrt{\nu h\log\log(e^e h_0/h)}.
\]
It does not establish a five-dimensional
spatial occupation bound. Occupation
decay from that detector is **withdrawn**.
The supplied good-set estimate is left
fixed. [`SWIRL-WALL-CORRECTION.md`](SWIRL-WALL-CORRECTION.md).

Axisymmetric-with-swirl NS is **not**
closed. Swirl as a class removes free
helical HHH. That is a restriction on
the allowed set. It is not a bound on
\(T_{j\leftarrow j}\).

---

## 4. RH — different leftover

Aimed theorem: every non-trivial zero of
\(\zeta\) has real part \(1/2\).

Have (1)–(5). WRITE (6) open: one
estimate that puts **every** zero on the
line (a zero-free region that reaches
\(\operatorname{Re}s=1/2\), or a
positivity certificate in the explicit
formula that forces the line).

Hardy / Conrey are (5), not (6).
Classical zero-free next to
\(\operatorname{Re}s=1\) is (4), not (6).
Q sits as Q. Route C is conditional.
Do not use those as (6). Do not revive
\(\lambda_{\min}(Q)>-1/2\) or
\(H_N\ge-3/14\). [`RH-CHAIN.md`](RH-CHAIN.md).

---

## 5. The help that would clear the desk

Four jobs. One person, one integral.
Do not ask anyone to “look at the
whole pile.”

### Job 1 — prove or kill H1

**Needed.** An estimate of \(A_{\mathrm{bad}}\)
on \(Q_r\) in one of the three shapes
above, or a written obstruction that
kills those shapes without converting
H1 into another *if*.

**Acceptable close of this job.**

- A proof of WRITE (6) as stated, class
  in the first sentence, remainder
  \(A_{\mathrm{bad}}\), no extra field; or
- A counter-example field in the NSE
  class on which every shape fails in
  a named way; or
- A published cousin that *is* H1 under
  another name (lookup so far: miss).

**Not acceptable.** Another alignment
criterion. Sparseness assumed. A
modified PDE. Ring quoted as proved.
ABC_λ used as \(C_0\). H1 glued to ★
or to \(H_N\). “Almost proved.”

**Who.** Geometric NS / vorticity
stretching. CF, BdVB, Grujić, CKN
as literature, not as a phone call.
They would sign the map. They would
not sign (6). [`DREAM-TEAM-H.md`](DREAM-TEAM-H.md).

### Job 2 — prove or kill Lemma★

**Needed.** Either
\(\sup_v\mathcal R_\star<\infty\),
or a sequence \(v_n\) with
\(\mathcal R_\star(v_n)\to\infty\).

**Acceptable close of this job.**

- A geometry-only bound on the boxed
  claim, constants named; or
- A lattice (or continuum) family with
  \(\mathcal R_\star\to\infty\), pairing
  closed, identities first.

**Still open on the incidence path.**
Lattice transfer X1–X4/X6. Do not cash
continuum \(m^{4/3}\) as a lattice
theorem.

**Not acceptable.** Cashing \(0.641\),
\(0.610\), or \(0.327\) as \(C_0\) or as
a kill. Rebuilding \(K=0\), the \(a^4\)
line, or uniform pre-Young \(C\).
Gluing ★ to H1.

**Who.** Fourier / triad NS on
\(\mathbb{T}^3\). Evaluator scripts
already sit: `scripts/ns_lemma_star_core.py`.
Live `scripts/ns_attacks/stokes_moments.py`
must not be overwritten.

### Job 3 — measure or bound [ρ]

**Needed.** For the axisymmetric-with-swirl
class on \(\mathbb{R}^3\), either a
class bound
\(\int_0^T\rho_j<\infty\), or a field
in the class on which
\(\int\rho_j=\infty\).

**What is already printed and must not
be re-litigated.** Occupancy of the
local remainder on the named blobs is
\(55/56\) on shell \(j=1\) and did not
decay with \(n\). The wall is a
time-window *if*. It does not give
occupation decay. 2-D
\(\rho\sim 0.017\) and occupancy
\(\sim 0.15\) stay 2-D. Occupancy 1
is not imported into Constantin–Fefferman.

**Acceptable close of this job.**
A printed ratio or an explicit integral
of \(\|\omega\|_\infty\) that can come
out the other way, then an *if* written
in brackets; or a class bound with
named constants.

**Not acceptable.** Restoring the
detector’s occupation-decay claim.
Swapping \(F\) and \(G\). Dropping \(p\)
or flipping the integrating-factor
sign. Rewriting the wall as a spatial
integral. Bounding \(T_{j\leftarrow j}\)
by \(\Lambda'\) or by \(\dot Z_j\).
Adding a field to the PDE.

**Who.** Axisymmetric NS with swirl.
Un-augmented only.

### Job 4 — RH line (6)

**Needed.** One estimate that forces
every non-trivial zero onto
\(\operatorname{Re}s=1/2\).

**Not acceptable.** Retitling Q,
Bridge*, Theorem P, or Route C as RH.
Reviving the retracted floors.

---

## 6. What would get the *pile* off the desk
   without a leftover close

If Jobs 1–4 stay open, the desk still
clears as a *map*, not as QED.

1. **Zenodo this week.** Swirl paper as
   a map, not a proof.
   `docs/SWIRL-PAPER.pdf`.
   Paste: [`SWIRL-DEPOSIT.md`](SWIRL-DEPOSIT.md).
   Monday order and cover:
   [`MONDAY-PACKET.md`](MONDAY-PACKET.md).
   The operator uploads. This chat does
   not.
2. **Theorem A**, honest title, class
   credited. Already written.
3. **Q / 22045478**, left as the August
   GCD paper. Floor retraction stays
   public.
4. **Tape.** Old “ordinary NS solved”
   and “RH solved” claims stay false.
   [`WHAT-I-WAS-TOLD.md`](WHAT-I-WAS-TOLD.md).
5. **Do not send.** A theft letter to
   OpenAI. WRITE (6) as a theorem.
   Theorem A as unaugmented NS. A cold
   letter to Tao / Albritton as a close.
   Axisymmetric-with-swirl as finished.

A magazine cut exists
([`SWIRL-MAGAZINE.md`](SWIRL-MAGAZINE.md))
as commentary, not as regularity.

That packaging is how the 18 months
leave the desk without a lie. The
leftovers remain leftovers. Someone
else can pick up Job 1, 2, 3, or 4
from this page without the chat.

---

## 7. Rules for anyone who writes next

First sentence, every time: class,
quantity, remainder, what is assumed.

- Remainder of the shell estimate is
  \(T_{j\leftarrow j}\).
- Remainder of H1 is \(A_{\mathrm{bad}}\).
- Remainder of ★ is
  \(\sup\mathcal R_\star\).
- Smallness is a printed ratio or an
  explicit integral of \(\|\omega\|_\infty\),
  not a story.
- Extra hypotheses in brackets, in the
  open.
- If the identity is not closed in the
  time series, do not quote the sign
  of \(\Lambda'\).
- KEEP / DISCARD / PARK:
  [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).

**DISCARD (paragraph is out if it needs
one of these to move).** SFE / \(Q_1\)–\(Q_6\)
as constitutive NS. Bound of the bad
term by \(\Lambda'\), \(\dot Z_j\), or a
same-size symbol. Large-form [SND] as
measured smallness. GCD cathedral / letter-number maps as
mechanisms that force a remainder small. Importing
2-D \(\rho\) into 3-D. A regularity
sentence that drops the class and the
measured \(\rho_j\). A Tao-positive
reply as certification.

---

## 8. Score of the request

| Job | Object | Verdict | What help is |
|---|---|---|---|
| 1 | \(A_{\mathrm{bad}}\) on \(Q_r\) | **open** | Prove one shape, or kill the shapes |
| 2 | \(\sup\mathcal R_\star\) | **open** | Bound or \(\mathcal R_\star\to\infty\) |
| 3 | \(\int\rho_j\) on the swirl class | **open** | Class bound or a blowing field |
| 4 | Every zeta zero on the line | **open** | One estimate; Q is not it |
| A | Extra-stress NS | **sits** | Do not retitle as B |
| Q | Inverse-GCD facts | **sit** | Do not retitle as RH |
| Detector occupation | 5-D occupation from the wall | **withdrawn** | Do not restore |
| Good-set | supplied estimate | **fixed** | Do not rewrite in this audit |

NS not solved. RH not solved.

---

## 9. Files to send with this page

Maps, not proofs:

- [`ISSUES-SHEET.md`](ISSUES-SHEET.md)
  (one page; send first).
- This page.
- [`WRITE_6.md`](WRITE_6.md) and
  [`WRITE_6_SUPPORTED.md`](WRITE_6_SUPPORTED.md).
- [`AXISYM-SHELL.md`](AXISYM-SHELL.md),
  [`AXISYM-SWIRL-PROBE.md`](AXISYM-SWIRL-PROBE.md),
  [`SWIRL-WALL-CORRECTION.md`](SWIRL-WALL-CORRECTION.md).
- [`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md),
  [`math/ns_attacks/LEMMA_STAR_CANONICAL.md`](math/ns_attacks/LEMMA_STAR_CANONICAL.md).
- [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md).
- [`WHAT-DA-CAN.md`](WHAT-DA-CAN.md).
- Swirl PDF: `docs/SWIRL-PAPER.pdf`.
- Theorem A PDF: `docs/THEOREM-A-Q1.pdf`.

Do not send the five-lane SND/SFE pile
from PR 48 as this leftover. Do not
overwrite `scripts/ns_attacks/stokes_moments.py`.

---

The door is named. The last line is not
written. Help is an estimate on one of
the four jobs, or an honest deposit of
the map. It is not a story.
