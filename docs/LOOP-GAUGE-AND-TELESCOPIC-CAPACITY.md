# Loop gauge and telescopic capacity

24 September 2026.
**Two strikes. Neither target
is closed. A layer of wishful
thinking is gone.
NS not solved.**

Parent Gate:
[`JOINT-EPOCH-BUDGET.md`](JOINT-EPOCH-BUDGET.md).
SAG parent:
[`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md).
Archive:
`MASTER_DA_SHOWDOWN_DOSSIER_2026-09-07.md`,
`DA-NS-SPRINT-02-EXACT-TWO-TRIAD-STRIKE-AND-JOINT-EPOCH-BUDGET-2026-09-07.md`.

Unaugmented NS on \(\mathbb{T}^3\).
No \(Q_1\). No \(\Phi\). No SND.
No Theorem H. No Route A weld.
Unrestricted \(\star\) stays
**KILLED**. Charge-only close
stays **KILLED**. Static
shared-output rescue stays
**KILLED**. Claimed \(K\le 16/9\)
stays CLAIMED.

Code:
`scripts/ns_attacks/loop_gauge.py`,
`scripts/ns_attacks/polarization_holonomy.py`,
`scripts/ns_attacks/telescopic_capacity.py`,
`scripts/ns_attacks/helical.py`.

```bash
PYTHONPATH=scripts python3 -m unittest \
  tests.test_loop_gauge \
  tests.test_polarization_holonomy \
  tests.test_telescopic_capacity \
  tests.test_sag_two_triad_witness -q
PYTHONPATH=scripts python3 scripts/ns_attacks/run_holonomy_capacity.py
```

---

## Strike 1 — loops: topology is not the theorem

Write a modal coefficient

\[
a_k=A_k e^{i\phi_k}.
\]

For a triad \(p+q=k\), the phase
entering a cubic interaction is

\[
\Phi_{pqk}
=
\phi_p+\phi_q-\phi_k+\arg g_{pqk},
\]

where \(g_{pqk}\) is the
geometric / helical coupling.

Ignore \(\arg g\) for one moment.
The part created solely by
sharing modes is
\(\phi_p+\phi_q-\phi_k\).

There is a global family

\[
\boxed{\phi_k=\xi\cdot k+\phi_0}
\]

for which, because \(p+q=k\),

\[
\phi_p+\phi_q-\phi_k
=
\phi_0
\]

on every triad in the entire
network, regardless of how many
loops it contains. In particular,
with \(\phi_0=0\),

\[
\boxed{\phi_p+\phi_q-\phi_k=0}
\]

simultaneously on every triad.

That family is not an accident.
\(\widehat u_k\mapsto e^{i\xi\cdot k}\widehat u_k\)
is a spatial translation of the
underlying Fourier field.
Navier–Stokes is translation
invariant, so this phase freedom
is structural.

\[
\boxed{
\text{LOOP TOPOLOGY BY ITSELF
DOES NOT FORCE PHASE FRUSTRATION.}
}
\]

A closed triadic cycle is not
analogous to an automatically
frustrated spin loop. The
convolution relation \(p+q=k\)
carries a global additive phase
character that satisfies every
edge at once.

If Heavy finds genuine loop
depletion, it must come from
something finer:

\[
\boxed{
\text{geometric / helical coupling
phases}
+
\text{polarization constraints}
}

\]

— not from the fact that the
incidence hypergraph contains
cycles.

Do not classify “tree versus
loop” merely combinatorially
anymore.

---

## The correct cycle invariant

For each interaction let
\(\chi_e:=\arg g_e\). The
compatibility equations are

\[
\phi_{p_e}+\phi_{q_e}-\phi_{k_e}
\equiv
-\chi_e+\Phi_e^\star
\pmod{2\pi},
\]

where \(\Phi_e^\star\) is the
phase that maximizes the signed
contribution. This page locks
\(\Phi_e^\star=0\) as independent
cosine alignment.

Let \(B\) be the triad–mode
incidence matrix with row
\(e_p+e_q-e_k\). Then

\[
\boxed{B\phi=b\pmod{2\pi}.}
\tag{C1}
\]

Loops matter only through the
left nullspace of \(B\). If
\(c^TB=0\), compatibility
requires

\[
\boxed{c^Tb=0\pmod{2\pi}.}
\tag{C2}
\]

That is the actual
cycle-frustration test.

For every loop family compute
\(\ker B^T\) and the phase
holonomy

\[
\boxed{\Omega_c=c^Tb\pmod{2\pi}.}
\]

If every \(\Omega_c=0\), the
loop is phase-unfrustrated
despite being topologically
closed. If some \(\Omega_c\neq 0\),
there is genuine cycle
frustration.

\[
\boxed{\textbf{LOOP-GAUGE TEST}}
\]

Before any expensive
optimization, solve (C1). If
the independently optimal
interaction phases are globally
realizable modulo the
translation / additive gauge,
then

\[
\Gamma_{\mathrm{cyc}}=1
\]

at the phase level and only
polarization geometry can still
create a defect.

Compare only a **certified**
global maximum against the
\(\Gamma=1\) tree baseline
\(\sum_e\lvert g_e\rvert\). A
local optimizer is not a
certificate. A holonomy that
moves when the helical reference
axis moves is a **frame gauge**,
not a physical loop defect.

---

## Locked families

### Star — the archive two-triad witness

SAG convention \(p+q=-k\):

\[
(0,1,1)+(-1,-1,-1)=(-1,0,0),
\]
\[
(0,1,0)+(-1,-1,0)=(-1,0,0).
\]

Same field as
[`JOINT-EPOCH-BUDGET.md`](JOINT-EPOCH-BUDGET.md).
Two hyperedges, one shared
output. Combinatorial star.

\[
\ker B^T=\{0\}.
\]

No cycle test. Phase
compatibility is automatic.
\(\Gamma_{\mathrm{cyc}}=1\) at
the phase level. This is why
static shared-output
compatibility did not kill
\(\rho_\Gamma\): there was
never a phase loop to
frustrate.

### Parallelogram — a convolution-compatible 4-cycle

\[
\begin{aligned}
T_1&: (1,0,0)+(0,1,0)=(1,1,0),\\
T_2&: (1,0,0)+(0,0,1)=(1,0,1),\\
T_3&: (1,1,0)+(0,0,1)=(1,1,1),\\
T_4&: (1,0,1)+(0,1,0)=(1,1,1).
\end{aligned}
\]

Locked generator

\[
c=(1,-1,1,-1)\in\ker B^T.
\]

The translation gauge still
gives \(B\phi=0\) for
\(\phi_k=\xi\cdot k\). Topology
alone does **not** frustrate
this loop.

The helical coupling offsets
do. On the locked Waleffe-style
\(g\), with \(\Phi_e^\star=0\),

\[
\boxed{\Omega_c=\frac{2\pi}{3}}
\]

exactly (to machine precision),
and the same holonomy is
returned for helical frames
built from \(\hat x\), \(\hat y\),
and \(\hat z\).

\[
\boxed{
\text{genuine cycle phase
frustration from }\arg g,
\text{ not from topology.}
}
\]

Certified cosine comparison
against the \(\Gamma=1\) tree
baseline \(\sum_e\lvert g_e\rvert\):

\[
\sum_e\lvert g_e\rvert
\approx 1.76478,
\qquad
\max_{c\cdot\theta=\Omega}\sum_e\lvert g_e\rvert\cos\theta_e
\approx 1.53837,
\]

\[
\boxed{\Gamma_{\mathrm{cyc}}\approx 0.8717
\quad\text{(this family, this }g\text{).}}
\]

One parallelogram is not a
theorem for every lattice
family. It is a certificate
that the cycle test can fire
for geometric phases after
the additive gauge is
quotiented, and that the
comparison is a constrained
maximum, not a local search.

---

## Strike 3 — polarization is the static remainder

After phase compatibility is
removed, each mode still has
to satisfy \(k\cdot v_k=0\).
One \(v_k\) participates in
several interaction planes.

The residual static question
is whether one collection of
transverse vectors \(\{v_k\}\)
can realize the required
geometric couplings
simultaneously.

Stars can. The archive witness
is already one globally
compatible real field.

A further loop obstruction,
after phase compatibility is
settled, would have to be a
**polarization holonomy**.
In helical coordinates each
mode has only \(a_k^+\),
\(a_k^-\). Transport the
preferred helicity state
around the cycle.

On the locked parallelogram
the preferred helicity triples
**are** simultaneously
realizable on all three
reference axes. No transported
flip. So this family has a
phase holonomy and **no**
extra polarization holonomy.

\[
\boxed{
\text{no static polarization
defect on the locked
parallelogram.}
}
\]

The archive star is the same:
preferred triples realize, and
there is no cycle.

A preferred-triple conflict
on a star would be a **local
hub conflict**, not a loop
holonomy. SAG-5A already
named that rank fact. Do not
relabel it.

The remaining static target
is therefore narrower than
“loops might cancel,” and on
this first loop family it is
already located: \(\arg g\),
not topology, not helicity
assignment.

---

## Strike 4 — reset summability takes a hit

Nearest-center does kill one
artificial reset cost. For

\[
W_K=D_s+X(\Lambda-K)^2
=\sum_k\lambda_k(\lambda_k-K)^2\lvert v_k\rvert^2,
\]

a chart change at fixed
physical state costs

\[
\Delta W
=
X\bigl[
(\Lambda-K_{e+1})^2-(\Lambda-K_e)^2
\bigr].
\]

Choosing \(K_{e+1}\) closer
to \(\Lambda\) guarantees

\[
\boxed{\Delta W\le 0.}
\]

\[
\boxed{
\text{center-selection reset
cost can be killed by design.}
}
\]

That does not solve reset
summability. A nearest-shell
rule can switch every time
\(\Lambda\) crosses another
midpoint. The number of those
switches is governed by how
far \(\Lambda(t)\) travels,
and

\[
(\log\Lambda)'
=
\frac{2}{Y}(T_c-\nu D_s)
\]

is the Gate quantity.

\[
\boxed{
\text{“few resets because
}\Lambda\text{ cannot move much”}
}

\]

is circular unless it is
derived from an independent
budget.

---

## Strike 5 — do not count resets; make them telescopic

Do not try to prove
\(\#\{\text{epochs}\}<\infty\).
Do not even necessarily prove
\(\sum_e\lvert\Delta K_e\rvert<\infty\).

Design the capacity so that
adjacent charts satisfy

\[
\boxed{
\mathscr Q_{e+1}(u)
\le
\mathscr Q_e(u)
+
\text{an already-paid physical quantity.}
}
\]

Best case:

\[
\boxed{\mathscr Q_{e+1}(u)\le\mathscr Q_e(u)}
\]

at every reset. Then
infinitely many resets are
harmless.

\(W_K\) with nearest-center
does the jump. The
intra-epoch derivative, \(K\)
frozen, is a different
sentence:

\[
W_K'
=
-2\nu\sum\lambda_k^2(\lambda_k-K)^2 e_k
+
2\sum\lambda_k(\lambda_k-K)^2\tau_k.
\]

The nonlinear piece is not
\(T_c\) and is not absorbed.
That is still open. It is
**not** DA-NS-2.

Any proposed reset estimate
that requires prior control
of \(\Lambda\)'s total motion
is **rejected as circular**.

The old dossier warning
matches: the design
requirement is stronger than
“bounded charge per epoch.”

---

## What this does not do

- It does not close loops.
- It does not close the Joint
  Gap–Charge Epoch Budget.
- It does not restore
  unrestricted \(\star\).
- It does not produce an
  occupancy envelope.
- It does not bound \(T_c\).
- It does not imply
  \(\int K<\infty\).
- A finite helical sample on
  one parallelogram is not a
  theorem for every lattice
  family.
- Frame-dependent holonomy is
  not a physical defect.

---

## Lock

Ordinary modal phases possess
a global additive gauge that
satisfies arbitrary convolution
loops. Topology is not a
frustration theorem.

On the locked parallelogram
the geometric offsets
**do** create inconsistency:

\[
\Omega_c=2\pi/3,
\qquad
\Gamma_{\mathrm{cyc}}\approx 0.8717,
\]

frame-invariant, certified
against the tree baseline.
Preferred helicities on that
same family realize. So the
static defect found here is
phase holonomy of \(\arg g\),
not polarization holonomy.

A different family could still
produce a polarization
holonomy after \(\Omega_c=0\).
That remains the residual
static target when the
LOOP-GAUGE TEST passes.

\[
\boxed{\textbf{TELESCOPIC CAPACITY}}
\]

is the remaining JGC reset
question, rather than bounding
the number of epochs.
\(W_K\) nearest-center does
the jump. Intra-epoch \(W_K'\)
is open. DA-NS-2 is not seated.

LOOP: build \(B\), quotient
the translation / additive
gauge, compute \(\ker B^T\)
and exact cycle phase
holonomies **before**
optimization. If phase
holonomy vanishes, test
polarization / helical
holonomy. Compare only
certified global maxima
against the \(\Gamma=1\) tree
baseline.

JGC: stop trying to control
epoch count. Search for a
capacity whose chart change
is nonpositive or telescopes
at every center / projector /
component reset. Any proposed
reset estimate that requires
prior control of \(\Lambda\)'s
total motion is rejected as
circular.

Those are things we can
actually kill or certify.
Neither is certified as a
regularity close.

The Fourier-triangle audit
[`FOURIER-TRIANGLE-AUDIT.md`](FOURIER-TRIANGLE-AUDIT.md)
does not reopen these two
instructions.

NS not solved.
