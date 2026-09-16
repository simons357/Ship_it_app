# SND-to-regularity implication

15 September 2026.
**The implication is not a bound on X.
SND sitting is not a bound on X.
Theorem G is dead. Ring is REPAIR.
Displayed Theorem H is not established
even with X<=M.
Ordinary NS is not solved.**

Not leftover 1. Not leftover 4. Not \(\star\).
Catalog B open stays 1 (`B_regularity`).
Do not merge PR 48 SND / Q6 / SFE pile.
Do not start H1 from this page.
Do not weld \(\star\).
No more numerical sweeps on this write.

Specialist H review (viscous tail,
shear kill, valid \(F_j\) bound):
[`SND-H-REVIEW.md`](SND-H-REVIEW.md).
Repaired \(F_j\) assembly (Dini ceiling,
not a floor; Theorem H withdrawn):
[`SND-H-REPAIR.md`](SND-H-REPAIR.md).
SND sits **beside** leftover 5, not in
front of it. C10 is the named local-block
candidate, not this implication:
[`C10-CHAIN.md`](C10-CHAIN.md).
Do not work Theorem H from this page.

Plain page (closing SND does not close NS):
[`SND-H-PLAIN.md`](SND-H-PLAIN.md).
Dictionary: [`UNAUGMENTED-R4-VORTICITY-PLAN.md`](UNAUGMENTED-R4-VORTICITY-PLAN.md)
§8–§10. Low Bony \(T\):
[`TRACK-B-BONY-T.md`](TRACK-B-BONY-T.md).
Climb from the field:
[`TRACK-B-CLIMB-LAW.md`](TRACK-B-CLIMB-LAW.md).
Tape: [`YES-NO-OPEN.md`](YES-NO-OPEN.md).

---

## What was asked

Write down exactly:

1. what the shell condition controls,
2. what additional information about
   frequency drift is needed,
3. whether the proof assumes the desired
   bound anywhere.

Three answers. In that order.

The claimed May-note chain, after the
\(\Phi\) / \(Q_1\) glue is cut, is

\[
\text{SND-C in SPREAD}
\xrightarrow{\ H\ }
\text{Bony }T+T^*+R
\xrightarrow{\ G\ }
\inf J/X\ge c_*
\xrightarrow{\ \mathrm{Ring}\ }
\|\nabla\xi\|_{L^\infty(E_c)}\le C\,2^{j_*}
\xrightarrow{\ \mathrm{CF}\ }
\text{stretching control}.
\]

The last arrow is not regularity.
Occupation is not a bound on \(X\).
The three answers below say why the
arrow from the shell condition to
ordinary NS does not sit.

---

## 1. What the shell condition controls

The living objects are Littlewood–Paley
enstrophy shells on \(\mathbb{T}^3\):

\[
X_j=2^{2j}\|\Delta_j u\|_2^2,\qquad
X=\sum_j X_j=\|\omega\|_2^2,\qquad
J=\max_j X_j,\qquad
\rho=J/X,
\]

\[
j_*=\mathrm{argmax}_j X_j,\qquad
P_{j_*}=X_{j_*-1}+X_{j_*}+X_{j_*+1},\qquad
\sigma=\frac{P_{j_*}}{X}\in(0,1].
\]

The **shell condition** is an instantaneous
occupation cut on those masses. One
threshold, no gap (B2, pass as a cover
of fractions, not as dynamics):

- **3-CONC:** \(\sigma\ge 1/2\). Some triad
  around the peak holds at least half the
  enstrophy. Licenses 3-shell Ring /
  Bernstein on the packet
  \(u_{\mathrm{pkt}}=\sum_{|k-j_*|\le 1}\Delta_k u\),
  with remainder size \((1-\sigma)^{1/2}X^{1/2}\).
- **SPREAD:** \(\sigma\le 1/2\). No three
  consecutive shells hold half the
  enstrophy. Licenses T2 Lemma 1 (the
  self-flux
  \(\int(u_{\le j}\cdot\nabla)\Delta_j u\cdot\Delta_j u=0\))
  and the attempted packaging of the
  peak-shell flux
  \[
  \Pi_{j_*}=\int\Delta_{j_*}\bigl[(u\cdot\nabla)u\bigr]\cdot\Delta_{j_*}u
  \]
  as SND-C:
  \[
  |\Pi_{j_*}|\le C_*\bigl(\nu\,2^{2j_*}X_{j_*}+X^{1/2}\mathcal D^{1/2}\bigr)
  \]
  in the class \(X\ge\delta_*/4\), \(\rho\le\rho_0\).
- **EQ3:** 3-CONC plus comparable neighbors
  \(\kappa\le 2\). Helps **only the diagonal
  Bony remainder \(R\)** (Bernstein constants
  of the same order on \(j_*-1,j_*,j_*+1\)).
  Does **not** help the low paraproduct
  \(T\) (\(k\le j_*-4\)). Those shells sit
  outside the triad by definition.

August one-shell “SND” is the special case
\(X_{j_*}\approx P_{j_*}\). June “no shell
above \(\rho_0\)” is implied by SPREAD if
\(\rho_0\ge 1/2\). Do not call both SND.
Concentration and spread are opposite
cuts. They are two jobs.

What the cut does control:

- which Bony pieces are “near” the peak
  (diagonal \(R\) versus far infrared \(T\));
- which estimate is licensed this instant
  (Ring on a packet, or T2 Lemma 1 plus
  attempted SND-C);
- the packet scale \(\delta\sim 2^{-j_*}\)
  used as a tube radius on the swirl
  column — a scale, not an absorption.

What the cut does not control:

- \(\|\omega\|_\infty\);
- \(\int X\,dt\) (Leray already has that);
- a bound on \(X\) itself;
- alignment \(\omega\cdot S\omega\), or
  \(\lvert\cos\alpha_3\rvert\) on \(E_c\)
  (B14a: 3-CONC does not deplete the
  median; frequency occupation is not
  strain-axis equidistribution);
- the \(1/r^4\) tube remainder
  \(I_{\mathrm{tube}}\) for all data
  (B4b fail; B4c is a packet class);
- leakage of mass to \(j_*\pm 1\) as a
  dynamical law, or to the far infrared.

A cover of hats is not a continuation
criterion. B8 partitions time
(\(\tau_{\mathrm{C}}+\tau_{\mathrm{S}}=T\)).
B8c fails as a bound on \(X\).

---

## 2. Frequency drift still needed

The shell condition is a photograph of
the mass. Regularity needs a law for
where the photograph goes.

The missing object is a climb law for
the peak scale **from the field**, not a
prescribed rate written into the estimate:

\[
c=\frac{\mathrm{d}j_*}{\mathrm{d}t}
\quad\text{or}\quad
c=\frac{\mathrm{d}j_{\mathrm{bar}}}{\mathrm{d}t},\qquad
j_{\mathrm{bar}}=\frac{\sum_j j\,X_j}{X}.
\]

What is already scored, and what is
still absent:

- **Prescribed climb is not NS.** On the
  glue ODE, slow climb \(c=1\) dies in
  the fat room; fast climb \(c=8\) sits
  (B11b fail / B11c pass on the model).
  Classical NS did not hand \(c=8\)
  (B11d, B11e fail). Writing \(c=8\)
  into the estimate assumes the saving
  rate.
- **Instantaneous drift is not a law.**
  The vorticity RHS makes \(c\) readable
  (B12, B12a pass). Random CONC packets
  at \(t=0\) do not produce \(c\ge 8\):
  Euler drift \(\sim 10^{-4}\) even at
  \(X=40\); viscous drift \(\sim-1.4\)
  (B12b). Viscosity is not a ladder:
  high shells damp first, so
  \(j_{\mathrm{bar}}\) falls (B12c).
  A short evolution does not write a
  saving climb (B12d). The \(t=0\)
  reading is not an a priori (B12e).
- **Frozen support is the case still
  left.** Packet support \(|k|\le K\)
  gives \(X\le K^2 E\) (B10 pass). Frozen
  \(j_*\) freezes \(K\). If \(j_*\)
  climbs, \(K\) climbs, the ceiling
  lifts (B10b fail). The implication
  must still handle a moving peak.
  DNS of a window is not that law
  (B13f).
- **Occupation time is a clock, not a
  bound.** Leray \(\int X<\infty\) does
  not shorten CONC: the spike
  \(X\sim(T_*-t)^{-1/2}\) stays CONC
  the whole interval and \(X\) is
  unbounded (B8b fail; same as B6).
- **Leakage is the open H piece.** Mass
  outside the triad is exactly the low
  paraproduct \(T\). EQ3 says nothing
  about it. Energy-class
  \(\|u_{\le j-N}\|_\infty\lesssim
  2^{(j-N)/2}X^{1/2}\) sits (B7b). The
  uniform hope
  \(\|u_{\mathrm{low}}\|_\infty\lesssim
  \rho^{1/2}X^{1/2}\) as \(\rho\to 0\)
  fails on stacked low modes (B7c).
- **Glue is a sketch.** CONC cubic versus
  SPREAD quadratic, switched by the
  clock, adds increments (B9 pass as
  bookkeeping). Low \(j_*=2\) CONC grows
  on the model; high \(j_*\) viscosity
  owns the cubic. B9d fails as an
  a priori for classical \(X\).

Needed, and not supplied by \(\sigma\ge 1/2\)
or by \(\sigma\le 1/2\):

1. a field-derived bound on \(c\), or a
   proof that \(j_*\) cannot run to
   infinity on a smooth interval while
   \(X\) stays large;
2. a quantitative leakage estimate from
   the triad into \(j_*\pm 1\) and into
   \(k\le j_*-4\), in energy class, without
   a \(\rho^{1/2}\) upgrade as \(\rho\to 0\);
3. control of the moving-support ceiling
   \(X\le K(t)^2 E\) when \(K(t)=2^{j_*(t)+1}\)
   is allowed to climb.

Until those three sit, the shell condition
does not run in time.

---

## 3. Whether the proof assumes the desired bound

Yes. Several load-bearing steps assume
the bound they are supposed to produce,
or a stronger cousin of it.

| Step | What it assumes | Why that is circular |
|---|---|---|
| **Theorem E** (“SND on smooth intervals”) | \(u\) is already smooth | True for a smooth field. Does not start the a priori. Continuation is the leftover. |
| **Theorem F** \(\mathcal D\ge\nu\cdot 4^{N-1}\cdot\rho\cdot X\), \(N=\lceil X/J\rceil\) | “\(N\) active shells” sit at exponentially higher frequency | Consecutive low shells kill that. Super-exponential dissipation as \(\rho\to 0\) is not a theorem. The diagonal step \(2^{j_*}\le(\mathcal D/(\nu X_{j_*}))^{1/2}\) inherits F. |
| **Theorem G** (SND-C \(\Rightarrow\) \(\inf J/X\ge c_*\)) | uniform \(C_*\) as \(\rho\to 0\), via F exploding \(\mathcal D\) | H assumes \(\rho\le\rho_0\). If \(C_*\) blows as \(\rho_0\to 0\), the contradiction fails. The \(\rho^{1/2}\) hope for \(\|u_{\mathrm{low}}\|_\infty\) fails (B7c). **G is dead.** |
| **H at frozen \(\rho\le 1/4\)** | a smaller class, like \(\varepsilon>0\) | Legal energy-class \(T\) there is not the limit G uses. Ladyzhenskaya: frozen spread is not the limit. |
| **Ring** \(\|\nabla\xi\|_{L^\infty(E_c)}\le C\,2^{j_*}\) | the direction bound it wants | Status **REPAIR**. Not quoted as proved. H1 is that claim restricted to one cylinder; still not a theorem. |
| **Prescribed \(c=8\)** | the saving climb | Sits on the model ODE. NS did not pick it (B11d/e). |
| **Frozen-support ceiling \(X\le K^2 E\)** | \(j_*\) does not move | The case the implication must still handle is the moving peak (B10b). |
| **T2 Lemma 2 / \(H^{2.3}\) ball** | a subcritical a priori | Circular for large-data continuation (B1b fail). Dropped. |
| **Constantin–Fefferman after Ring** | small \(\lvert\cos\alpha_3\rvert\) | Conditional. 3-CONC does not force depletion (B14a). Ring Lipschitz is not alignment (B14b). |

The diagonal / high Bony pieces can be
attempted from Bernstein plus T2 Lemma 1
without F. The low term \(T\) cannot.
G needed the low term uniformly as
\(\rho\to 0\). That uniformity assumed
the dissipation Theorem F was written
to supply. F assumed a spectral gap the
spread class does not have. E assumed
smoothness. Ring assumes the Lipschitz
bound on \(\xi\). Climb assumes \(c=8\).
The ceiling assumes frozen \(j_*\).

Each of those is the desired bound, or
a bound that implies it, used as an
input. The implication is not an
a priori.

---

## Even if SND-C sat

A two-regime estimate that controls
\(\Pi_{j_*}\) in SPREAD and licenses Ring
in 3-CONC is still not:

- integrable leftover stretching
  \(\int\mathcal R\);
- all-data alignment (A1);
- all-data middle-strain integral (A2);
- a field that kills the stretch;
- leftover 1 (\(A_{\mathrm{bad}}\) on
  \(Q_r\));
- leftover 4 (replacement energy-budget
  after \(v_n\) killed unrestricted
  \(\sup\mathcal R_\star\)).

SND sitting is not a bound on X.
Closing SND does not close ordinary NS.
Catalog B open remains 1.
Do not retitle this page as leftover 1
or as \(\star\).

T2 Lemma 1 sits (B1). The occupation
cover sits (B2). Energy-class low
\(L^\infty\) sits (B7b). The clock
partitions (B8). Those are identities
and covers. They are not regularity.

---

## Lock

Shell condition: occupation sigma
and rho. Not ||omega||_infty.
Not a bound on X.

Frequency drift: a law for
dj*/dt from the field is still needed.
Prescribed c=8 is not that law.

Circularity: Theorem E, Theorem F,
Theorem G, Ring REPAIR, prescribed
climb, frozen-support ceiling.
Theorem E does not start the a priori.

G is dead. Ring is REPAIR.
SND sitting is not a bound on X.
NS not solved.
