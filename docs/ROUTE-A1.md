# Route A1 — dynamical \(a_+\): write or kill

18 September 2026.
**Literature-mined Arrow 2. Not a
theorem. Not leftover 1. Not Route B.
NS not solved.**

Class: classical, unforced, unaugmented
3-D Navier–Stokes. Smooth
divergence-free finite-energy data on
\(\mathbb{T}^3\) or \(\mathbb{R}^3\).
Keep \(1/r^4\). No \(Q_1\). No
\(\Phi\)-cancel. No modified viscosity.

Seated exact inequality, preserved:

\[
\mathrm{stretch}_j
:=\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2
\le a_+(t)\,Z_j.
\]

This page asks one question:

\[
\boxed{\text{What does NS itself force }a_+(t)\text{ to do?}}
\]

Target, if a noncircular mechanism
exists:

\[
\boxed{\int_0^T a_+(t)\,dt<\infty}
\]

from quantities independently
available before \(H^1\) continuation
is known.

No new 9D sweep. No SND persistence.
No Theorem H. No \(C_\tau\). No H1.
No centered-drift weld. No A2
staircase.

Definitions as on
[`C10-CHAIN.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/C10-CHAIN.md)
(PR #104):

\[
u_{\mathrm{loc}}=(\Delta_{j-1}+\Delta_j+\Delta_{j+1})u,
\qquad
Z_j=\|\Delta_j\omega\|_2^2,
\]

\[
\xi_j=\frac{\Delta_j\omega}{\lvert\Delta_j\omega\rvert}
\quad\text{on }\ \{\Delta_j\omega\neq 0\},
\]

\[
\alpha_{\mathrm{loc},j}
=\xi_j\cdot S(u_{\mathrm{loc}})\,\xi_j,
\qquad
a_+
:=\bigl\|(\alpha_{\mathrm{loc},j})_+\bigr\|_\infty.
\]

\(S=\tfrac12(\nabla u+(\nabla u)^{\mathsf T})\).
This \(a_+\) is an \(L^\infty\) of
**frequency-localized positive
stretching** along the local vorticity
direction. It is not \(A_{\mathrm{bad}}\),
not \(P_+\), not \(\lambda_2^+\) of the
full field, and not \(\|\nabla u\|_\infty\).
It is bounded by those objects.

Circularity test, applied to every
proposed bound:

> \(H^1\), \(L^\infty\),
> \(\|\nabla u\|_\infty\), BKM,
> Prodi–Serrin, or an equivalent
> continuation criterion
> \(\Rightarrow\) reject as closure.

The mining question for every outside
theorem is not “can we cite this
regularity criterion?” It is:

> Does its **proof** contain an
> intermediate inequality that bounds
> **our** \(a_+\) without assuming
> that theorem’s regularity
> hypothesis?

---

## Verdict

\[
\boxed{\text{UNRESOLVED}}
\]

No new exact NS mechanism was found
that puts \(a_+\) in \(L^1_t\) from
energy-class data. Every mined
depletion theorem is a **criterion**:
it assumes extra geometric smallness
and concludes regularity. The one
unconditional geometric output of NS
(Constantin–Fefferman’s averaged
direction bound) does not control
\(a_+\).

Per the close-plan stopping rule:
**park Route A. No A2 staircase.
Move to Route B.**

This is not

\[
\boxed{\text{NONCIRCULAR }a_+\text{ CONTROL}}
\]

and it is not a proof that no
mechanism can exist (that would be
Clay-adjacent). It is a named death
of every **existing estimate shape**
that was supposed to feed Arrow 2.

| Shape tried | Circularity test |
|---|---|
| Bound \(a_+\) by \(\|\nabla u\|_\infty\) or Sobolev of the unknown field | **REJECT.** BKM. |
| Bound \(a_+\) by energy / \(\mathcal E\) / \(X\) | **REJECT.** Same \(\lambda^{1/2}\) wall as C1. |
| Bernstein \(a_+\lesssim 2^{3j/2}\|S(u_{\mathrm{loc}})\|_2\) | **REJECT.** Cubic wall; Gronwall wants the \(H^1\) ceiling. |
| Cite Constantin–Fefferman / Beirão da Veiga–Berselli / Grujić as a bound on \(a_+\) | **REJECT.** Those papers assume the geometric smallness C10 is trying to prove. |
| Upgrade the CF averaged \(\int\lvert\omega\rvert\lvert\nabla\xi\rvert^2\) to Lipschitz of \(\xi\) or to \(L^\infty\) of \(\xi\cdot S\xi\) | **Unwritten in the literature, and the papers themselves treat that upgrade as the open step.** |
| Miller / Neustupa–Penel \(\lambda_2^+\) in a critical space | **REJECT as closure.** Characterization of blowup, not an a priori. |
| Frequency-localized LPS / BKM (Cheskidov–Dai, Bradshaw–Kukavica–Rusin, \ldots) | **REJECT.** Still a criterion on a window of shells. |

If a later write produces a genuinely
new exact identity that bounds \(a_+\)
without those inputs, reopen Arrow 2
under that identity. Do not reopen it
by citing a criterion harder.

---

## What NS itself forces

These are the seated, noncircular
outputs. None of them is
\(\int a_+<\infty\).

### 1. Constantin stretching identity (EXACT)

On \(\{\omega\neq 0\}\),
\(\alpha=\xi\cdot S\xi\) admits the
singular-integral representation
(Constantin, *SIAM Rev.* **36** (1994);
also the Euler form in Constantin–
Fefferman–Majda):

\[
\alpha(x)
=
\frac{3}{4\pi}\,
\mathrm{P.V.}
\int_{\mathbb{R}^3}
D\bigl(\hat y,\,\xi(x+y),\,\xi(x)\bigr)
\frac{\lvert\omega(x+y)\rvert}{\lvert y\rvert^3}\,dy,
\]

\[
D(e_1,e_2,e_3)
=(e_1\cdot e_3)\,\det(e_1,e_2,e_3).
\]

\(D\) vanishes when any two arguments
are parallel or anti-parallel, and

\[
\lvert D(\hat y,\xi(x+y),\xi(x))\rvert
\le
\lvert P_{\xi(x)}^\perp\xi(x+y)\rvert
\sim
\lvert\sin\theta(x,x+y)\rvert.
\]

**KEEP as algebra.** This is the
geometric kernel C10 wanted. It does
**not** bound \(\alpha\) or \(a_+\).
To pass from the identity to an
estimate one must control \(D\), i.e.
assume coherence of \(\xi\). That is
the Constantin–Fefferman **hypothesis**,
not a conclusion.

A frequency-localized cousin with
\(\xi_j\) and \(S(u_{\mathrm{loc}})\)
is the same identity on a band-limited
pair. Localization does not cancel
\(D\).

### 2. Strain / enstrophy identities (EXACT)

Standard:

\[
\frac12\frac{d}{dt}\|\omega\|_2^2
=
\langle S,\omega\otimes\omega\rangle
-\nu\|\nabla\omega\|_2^2.
\]

Miller, *Arch. Ration. Mech. Anal.*
**235** (2020) (arXiv:1710.05569),
and Chae for Euler:

\[
\frac{d}{dt}\|S\|_2^2
=
-2\|S\|_{\dot H^1}^2
-4\int\det(S)
\]

(up to a force inner product in the
mild-solution form), and

\[
\langle S,\omega\otimes\omega\rangle
=-4\int\det(S)
=-\frac43\int\mathrm{tr}(S^3).
\]

Because \(S\) is trace-free,
\(\lambda_1+\lambda_2+\lambda_3=0\),
and Miller’s algebraic bound

\[
-\det(S)\le\tfrac12\lvert S\rvert^2\lambda_2^+
\]

shows that **enstrophy production is
controlled by \(\lambda_2^+\)**.

**KEEP as algebra.** This is what NS
forces \(a_+\)’s cousin to *do to
enstrophy*: if \(\lambda_2^+\) (or
\(\alpha_+\)) is large, \(X\) can
grow cubically. It is the **converse**
of Arrow 2. NS does not force
\(\lambda_2^+\) or \(a_+\) small. It
forces that you need them small to
stop growth.

On the local block,
\(\alpha_{\mathrm{loc},j}
=\sum_i\lambda_i(u_{\mathrm{loc}})
(\xi_j\cdot e_i)^2\), so

\[
a_+
\le
\bigl\|(\lambda_{\max}(S(u_{\mathrm{loc}})))_+\bigr\|_\infty.
\]

If \(\xi_j\) aligns with the middle
eigenvector — the numerically observed
tendency Miller cites, not a theorem —
then \(a_+\) tracks \(\|\lambda_2^+(u_{\mathrm{loc}})\|_\infty\).
That heuristic makes Miller’s
criterion the closest cousin of
\(\int a_+<\infty\). It remains a
criterion: blowup if and only if
\(\lambda_2^+\) fails a scale-critical
integrability condition (BKM at the
endpoint \(L^1_t L^\infty_x\)).

### 3. Constantin–Fefferman averaged direction bound (CONDITIONAL A PRIORI)

CF 1993, eq. (20), as quoted by
Beirão da Veiga–Berselli
(*Diff. Int. Eq.* **15** (2002)):
if \(\omega_0\in L^1\), then

\[
\|\omega(t)\|_1
+\nu\int_0^t
\int_{\{\lvert\omega\rvert>0\}}
\lvert\omega\rvert\,\lvert\nabla\xi\rvert^2\,dx\,d\sigma
\le
\|\omega_0\|_1
+\frac2\nu\|u_0\|_2^2.
\]

**This is the only intermediate
inequality in the depletion
literature that is not secretly a
regularity hypothesis.** It says NS
produces *averaged* coherence:
weighted \(L^2\) control of \(\nabla\xi\)
on the support of \(\omega\).

It does **not** bound \(a_+\).

- Lipschitz / \(\tfrac12\)-Hölder of
  \(\xi\) is a pointwise condition.
  \(\lvert\omega\rvert^{1/2}\nabla\xi\in L^2_{t,x}\)
  does not embed to that.
- \(a_+\) is \(L^\infty\) of a CZ
  image of a band-limited vorticity.
  Pointwise control of \(\xi\cdot S\xi\)
  is the step CF *assume* as Lipschitz
  of \(\xi\) in high-vorticity regions.
- The \(L^1\) vorticity bound needs
  \(\omega_0\in L^1\). Energy-class
  data on \(\mathbb{R}^3\) need not
  have that. On \(\mathbb{T}^3\),
  \(\|\omega\|_1\le C\|\omega\|_2\),
  which uses enstrophy — circular if
  used to continue \(H^1\).

BdV–Berselli explicitly note that
their Hölder-criterion proof **does
not use** (3.2), and that (3.2) is
how CF got Lipschitz from an extra
assumption plus an \(L^1\) bound.
The upgrade from the average to
\(a_+\) is exactly the open step.

### 4. Scaling (what energy cannot force)

Energy-class concentrating family
\(u^\lambda(x)=\lambda^{3/2}\varphi(\lambda x)\)
(the same family that killed C1):

\[
a_+
\sim
\|\nabla u^\lambda\|_\infty
\sim\lambda^{5/2},
\qquad
\text{viscous time }\sim\lambda^{-2}.
\]

\[
\int a_+\,dt
\sim\lambda^{1/2}\to\infty.
\]

Any majorant of \(a_+\) by
energy-class quantities that would
put \(\int a_+\) in \(L^1\) on this
family **fails with the same
\(\lambda^{1/2}\) as TJJ-E-false.**
Amplitude \(u=Aw\): \(a_+\to A a_+\),
cubic in the stretch, quadratic in
energy. C10 already recorded this:
the \(a_+ Z_j\) majorant matches the
cubic only if \(a_+\) is **kept**,
not replaced by energy.

NS can still force \(\int a_+<\infty\)
along *actual trajectories* by a
dynamical cancellation that these
instantaneous fields do not see.
No such cancellation was found.

### 5. Two-dimensional and shear vacuity

On a 2-D flow, \(\xi\) is constant
and \(\alpha=0\). On high-tail shears
\(u=f(y)e_1\), \(\xi\cdot S\xi=0\) on
the support of \(\omega\), so
\(a_+=0\) and \(T_{j\leftarrow j}=0\).
NS forces \(a_+=0\) on those fields.
That is \(0\le 0\). It does not test
depletion on a genuinely stretching
local block. Locked already on the
C10 chain.

---

## Outside theorems, mined for intermediate inequalities

For each paper: the theorem’s
hypothesis, the intermediate
estimate actually used in the proof,
and whether that estimate bounds
**our** \(a_+\) without the hypothesis.

### Constantin–Fefferman 1993

*Indiana Univ. Math. J.* **42**, 775–789.

**Theorem.** If \(\lvert\sin\theta(x,x+y,t)\rvert\le C\lvert y\rvert\)
in high-vorticity regions, the
solution stays regular.

**Intermediate in the proof.** The
stretching integral is estimated by
the geometric kernel \(D\); Lipschitz
of \(\xi\) makes \(D=O(\lvert y\rvert)\),
which turns the singular integral
into something absorbable. Separately,
the averaged bound of §3 above.

**Our \(a_+\) without the hypothesis?**
**No.** The Lipschitz input *is* the
bound on \(D\), hence on \(\alpha\).
Removing it leaves the identity, not
an estimate. The averaged \(\nabla\xi\)
bound is unconditional (given
\(\omega_0\in L^1\)) and too weak for
\(L^\infty\) of \(\xi\cdot S\xi\).

**Direction relative to C10.**
Converse. *If* alignment is depleted,
stretching is weaker.

### Beirão da Veiga–Berselli 2002

*Diff. Int. Eq.* **15**, 345–356.
PDF: https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-89.pdf
(later boundary variants: Navier slip
OK, no-slip still open).

**Theorem.** \(\tfrac12\)-Hölder of
\(\xi\), or \(\xi\in L^a_t W^{1,b}_x\)
with \(2/a+3/b=1/2\), implies
regularity. Relaxes CF Lipschitz.

**Intermediate.** Stretching estimated
by \(\lvert\nabla\xi\rvert\) (or the
Hölder modulus) times vorticity
factors; then Sobolev / interpolation
closes under the hypothesis. They do
**not** need CF’s \(L^1\) bound.

**Our \(a_+\) without the hypothesis?**
**No.** \(\nabla\xi\) (or the Hölder
modulus) is the input. That is a bound
of stretching *by* directional
regularity, which is the object
Arrow 2 would have to produce.

Later variants (Berselli; Beirão da
Veiga 2006–2013; the 2018 *q*-norm
self-improvement arXiv:1712.00551)
change the exponent on \(\omega\) or
the Hölder exponent \(\beta(q)\). All
remain: *assume directional coherence,
conclude a bound on \(\|\omega\|_q\)*.
None derives coherence.

### Grujić — localization and sparseness

- Ruzmaikina–Grujić, *Comm. Math. Phys.*
  **247** (2004): extra cancellation in
  the stretching term \(\Rightarrow\)
  new geometric **criteria**.
- Grujić, *Comm. Math. Phys.* **290**
  (2009): vortex stretching localized
  to an arbitrarily small space-time
  cylinder; complete localization of
  the geometric condition. Independent
  of domain / boundary type.
- Grujić–Zhang 2006; Chae–Kang–Lee
  2007: other localizations of
  \(\tfrac12\)-Hölder.
- Grujić, *Nonlinearity* **26** (2013),
  arXiv:1111.0217: local 1-D sparseness
  of intense-vorticity superlevel sets,
  at the scale of the analyticity
  radius, prevents blowup.
  “Intermittency implies regularity.”

**Our \(a_+\) without the hypothesis?**
**No.** Localization moves the *same*
geometric hypothesis onto a cylinder.
Sparseness is a hypothesis on
superlevel sets of \(\lvert\omega\rvert\)
or \(\lvert u\rvert\), compared to the
analyticity radius, which itself is
estimated from \(\|u\|_\infty\) or
\(\|\omega\|_\infty\). Using the
analyticity radius as an input is a
continuation-scale quantity. The
proof’s engine is a harmonic-measure
maximum principle under that
sparseness, not a bound on
\(\xi\cdot S\xi\).

NS does not prove sparseness a priori.
Filament scenarios that are *not*
sparse on the analyticity scale are
exactly what remains.

### Miller 2020 / Neustupa–Penel \(\lambda_2^+\)

Miller, ARMA **235**; Neustupa–Penel
earlier \(\lambda_2\) criteria.

**Theorem.** Scale-critical control of
\(\lambda_2^+=\max(\lambda_2,0)\) is
necessary and sufficient for
continuation (BKM at the
\(L^1_t L^\infty_x\) endpoint).

**Intermediate.** The strain-only
enstrophy identity, plus
\(-\det(S)\le\tfrac12\lvert S\rvert^2\lambda_2^+\),
plus Gronwall in critical spaces.

**Our \(a_+\) without the hypothesis?**
**No.** The identity is KEEP. The
theorem is “blowup iff \(\lambda_2^+\)
is not integrable in a critical
norm.” That restates the problem in
strain eigenvalues. It does not put
\(\lambda_2^+\) or \(a_+\) in \(L^1_t\).

Miller’s cubic a priori
\(dX/dt\le C X^3\) with a better
constant (factor \(\sim 4920\) on the
existence time) is still cubic. A
better constant is not Arrow 2.

### Frequency-localized criteria

Cheskidov–Dai, *Arch. Ration. Mech.
Anal.* (2017), arXiv:1501.01043:
only a finite LP window whose lower
edge \(\to\infty\) as \(t\) approaches
a first singular time needs to be
well behaved.

Bradshaw–Kukavica–Rusin-type BKM with
frequency and time localization
(arXiv:1803.05569): control modes
below an explicit critical frequency.

**Our \(a_+\) without the hypothesis?**
**No.** These say *which shells matter*.
They still require a BKM / LPS bound
on that window. Our \(a_+\) *is* an
\(L^\infty\) strain on a three-shell
packet. Putting \(\int a_+<\infty\)
by citing “only those shells matter”
assumes the bound on those shells.

### Numerical / phenomenological depletion

Ashurst–Kerstein–Kerr–Gibson alignment
of \(\omega\) with \(e_2\); Tsinober;
Buaria–Lawson, *Sci. Adv.* (2024),
“twisting vortex lines regularize
turbulence.”

**Not a theorem.** Alignment is
observed, not proved. Twisting is a
measured depletion, not an
\(L^1_t L^\infty_x\) bound on \(a_+\).

---

## Adversarial families

No new 9D sweeps. Same families as
C10.

| Family | What it does to \(a_+\) | Verdict for Arrow 2 |
|---|---|---|
| High-tail shears | \(a_+=0\), \(T_{j\leftarrow j}=0\) | Vacuous pass. Does not test stretching. |
| Amplitude \(u=Aw\) | \(a_+\to A a_+\), stretch cubic | Energy majorant fails. Must keep \(a_+\) in the majorant. |
| Equal-enstrophy \(v_L\) | \(\rho(0)=1/L\) | A rate bound on \(a_+\) does not create a \(t=0\) floor. |
| Growing-layer \(v_n\) | Instantaneous class; \(\mathcal R_\star\to\infty\) | Does not resurrect unrestricted \(\star\). If \(a_+(v_n)\) stayed bounded while \(T_c/\mathcal D_s\) blew, that would *forbid* a C10\(\to T_c\) weld. Do not weld. |
| Compact mixed swirl | \(T^{\mathrm{mm}}\) bulk; occupancy \(55/56\) not \([\rho]\) | Not a class bound on \(a_+\). |
| Energy-class concentrating \(u^\lambda\) | \(\int a_+\sim\lambda^{1/2}\) | Kills energy / Bernstein majorants of \(a_+\). |

---

## Direct answer

**What does NS itself force \(a_+(t)\) to do?**

1. Admit Constantin’s geometric
   singular-integral formula, so that
   *if* \(\xi_j\) is coherent then
   stretching is depleted. NS does
   not force that coherence in a
   norm that controls \(a_+\).
2. Drive enstrophy through
   \(\langle S,\omega\otimes\omega\rangle=-4\int\det(S)\),
   hence through \(\lambda_2^+\) and
   through \(\alpha_+\). Large \(a_+\)
   is how blowup would happen, not
   something NS forbids.
3. Produce *averaged* directional
   smoothness \(\int\lvert\omega\rvert\lvert\nabla\xi\rvert^2<\infty\)
   when \(\omega_0\in L^1\). That
   average does not upgrade to
   \(\int a_+\,dt<\infty\).
4. Vanish \(a_+\) on 2-D and on
   non-stretching shears. Irrelevant
   to the stretching local block.
5. Nothing in the depletion canon
   puts \(\|(\xi_j\cdot S(u_{\mathrm{loc}})\xi_j)_+\|_\infty\)
   in \(L^1_t\) from energy-class
   data.

\(\int a_+<\infty\) is a **strictly
weaker continuation criterion than
BKM** (\(a_+\le C\|\nabla u_{\mathrm{loc}}\|_\infty\)),
still supercritical, still not
implied by the energy inequality.
Treating it as a consequence rather
than a hypothesis is the C10
confusion.

The enemy stays localized where the
close plan put it:

\[
\boxed{\textbf{near-scale positive high-frequency stretching}}
\]

Localizing the enemy is defensible.
Deriving \(\int a_+<\infty\) from NS
is not available from this literature
or from the estimate shapes already
killed on the desk.

---

## Park, and the Route B handoff

Route A is **parked**. Do not write
an A2 staircase (geometric tail,
Kato–Ponce remainder, “almost BKM,”
Pólya \(\rho\)-floor, SND persistence,
or a CF citation as if it were
Arrow 2).

Leftover 5 stays OPEN. (A) stays
unseated. The exact stretch
\(\le a_+ Z_j\) stays.

Next write is Route B, independently,
as already ordered:

\[
\boxed{\text{Route B: find an integrable centered nonlinear remainder}}
\]

Operator shape (do not tautologize):

\[
T_c
=-\langle B,\,A(A-\Lambda)u\rangle,
\qquad
\mathcal D_s
=\|(A-\Lambda)A^{1/2}u\|_2^2.
\]

Cauchy–Schwarz against the spread
produces some interaction norm
\(\mathcal I_\Lambda\) with

\[
\lvert T_c\rvert
\stackrel{?}{\le}
\sqrt{\mathcal D_s\,\mathcal I_\Lambda}.
\]

AM-GM would then give

\[
T_c
\le
\theta\nu\mathcal D_s
+\frac{\mathcal I_\Lambda}{4\theta\nu},
\]

so the useful-\(K\) question is
exactly whether \(\mathcal I_\Lambda/X\)
has an independently integrable
majorant — energy-class or dynamical,
not \(\|\nabla u\|_\infty\), not
\((T_c-\theta\nu\mathcal D_s)_+/X\),
and not a uniform \(\star\)-scaling
remainder (\(v_n\) kills that).

That audit is the next page. It is
not started by welding \(a_+\) to
\(T_c\).

If Route B also dies, the leftover
is a **new estimate shape**, not a
hybrid of A and B wreckage.

---

## Lock

Stretch \(\le a_+ Z_j\) EXACT.
Constantin kernel EXACT, not a bound.
Miller / Chae det-\(S\) identity EXACT,
converse of Arrow 2.
CF averaged \(\lvert\omega\rvert\lvert\nabla\xi\rvert^2\)
sits and does not control \(a_+\).
Every mined depletion theorem is a
criterion.
Energy / Bernstein majorants of \(a_+\)
die on \(u^\lambda\).
No new exact mechanism found.

\[
\boxed{\text{UNRESOLVED}}
\]

Park Route A. No A2. Move to Route B.
NS not solved.
