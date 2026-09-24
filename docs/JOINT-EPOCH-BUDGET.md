# Joint Gap–Charge Epoch Budget — next Gate

24 September 2026.
**Static shared-output SAG does not
rescue charge-only coercivity.
The next Gate is dynamic.
Not SAG-6. Not a close.
NS not solved.**

Archive:
`DA-NS-SPRINT-02-EXACT-TWO-TRIAD-STRIKE-AND-JOINT-EPOCH-BUDGET-2026-09-07.md`,
`MASTER_DA_SHOWDOWN_DOSSIER_2026-09-07.md`,
[`DA-NS-2.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/DA-NS-2.md)
on PR #104.

SAG parent:
[`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md).
Equal-input stack (different object):
[`SAG-6-LATTICE-CIRCLE.md`](SAG-6-LATTICE-CIRCLE.md).
Centered master ledger:
[`CENTERED-MASTER-LEDGER.md`](CENTERED-MASTER-LEDGER.md).

Unaugmented NS on \(\mathbb{T}^3\).
No \(Q_1\). No \(\Phi\). No SND. No
Theorem H. No Route A weld.
Unrestricted \(\star\) stays
**KILLED**. Claimed \(K\le 16/9\)
stays CLAIMED. Charge-only close
stays **KILLED** (later tape,
7 Sep). No occupancy envelope.

---

## The witness is not an equal-input circle

That is the first correction.

Two geometric triads, archive
convention \(k+p+q=0\):

\[
\gamma_1=(k,p,q),\qquad
\gamma_2=(k,r,s),
\]

\[
k=(1,0,0),\;
p=(0,1,1),\;
q=(-1,-1,-1),
\]

\[
r=(0,1,0),\;
s=(-1,-1,0).
\]

They share the mode \(k\), and

\[
\det(k,p,r)=-1,
\]

so the span is genuinely rank
three, not a planar escape.

Lengths:

\[
\lvert k\rvert=1,\;
\lvert p\rvert=\sqrt 2,\;
\lvert q\rvert=\sqrt 3,
\]

\[
\lvert k\rvert=1,\;
\lvert r\rvert=1,\;
\lvert s\rvert=\sqrt 2.
\]

This lives in the
**unequal-length / scalene**
territory. The SAG-6 identity
that collapsed an equal-input
pair to one tangent vector
**does not apply**.

SAG sign-flip: \(p+q=r+s=-k\).
The shared mode is the SAG
output after that flip. Both
descriptions are the same
field.

---

## Exact adversarial data

Helicity
\(\sigma_1=(+,+,-)\),
\(\sigma_2=(+,-,+)\).
With \(\iota=1+\sqrt 2-\sqrt 3\),

\[
a_k^+=1,\quad
a_p^+=\sqrt 2/\iota,\quad
a_q^-=e^{-i\pi/4},
\]

\[
a_r^-=\sqrt 2,\quad
a_s^+=i.
\]

Reality supplies the conjugates.
One globally compatible real
Fourier field. One common
\(a_k^+=1\).

\[
\boxed{\Lambda=2}
\]

\[
\boxed{
Q_{a,1}=2(\sqrt 2-1),\qquad
Q_{a,2}=-2(\sqrt 2-1)
}
\]

\[
\boxed{Q_{a,\Gamma}=0}
\]

Geometric multipliers differ:

\[
R_1
=\frac{3+3\sqrt 2+5\sqrt 3+\sqrt 6}{6},
\qquad
R_2=1+\sqrt 2.
\]

Centered contributions:

\[
\boxed{
\mathfrak T_{c,1}
=1-\sqrt 3+\frac{4\sqrt 6}{3}
}
\qquad
\boxed{\mathfrak T_{c,2}=-2}
\]

\[
\boxed{
\mathfrak T^{\mathrm{het}}_{c,\Gamma}
=\frac{4\sqrt 6-3\sqrt 3-3}{3}>0
}
\]

Mechanism:

\[
Q_1=-Q_2
\quad\not\Rightarrow\quad
R_1 Q_1+R_2 Q_2=0,
\]

because \(R_1\neq R_2\).
That is the covariance.
Exact split on the later tape:

\[
T_c^{\mathrm{het}}=2\kappa^3 Q_a+\rho.
\]

Charge-only coercivity is
already dead. \(\rho\) is
needed.

Code:
`scripts/ns_attacks/sag_two_triad_witness.py`.

---

## SAG eyes on the same field

Both triangles are tested
against the same \(v_k\):

\[
\mathcal T_1
=\mathrm{Im}\bigl[(q\cdot v_p)
(v_q\cdot\overline{v_k})+\cdots\bigr],
\]

\[
\mathcal T_2
=\mathrm{Im}\bigl[(s\cdot v_r)
(v_s\cdot\overline{v_k})+\cdots\bigr].
\]

SAG therefore sees a
**shared-output** compatibility
constraint (SAG-5B, two scalene
triangles, one \(v_k\)).

The helical amplitudes already
satisfy that constraint. They
are one legal real field with
one \(a_k^+\). Nevertheless

\[
\boxed{\mathfrak T_{c,\Gamma}>0.}
\]

The old counterexample **passes**
the first SAG test.

\[
\boxed{
\text{static shared-output compatibility does NOT eliminate }\rho_\Gamma.
}
\]

\[
\boxed{\text{SAG static shared-output rescue of charge-only coercivity: KILLED}}
\]

Do not spend weeks trying to
prove that it does. The
directional frustration that
exists is too weak to force
cancellation of the weighted
sum once \(R_1\neq R_2\).

This is complementary, not
contradictory:

- SAG: two scalene triangles
  share \(v_k\); polarizations
  must coexist.
- Helical book: signed charges
  cancel; radial multipliers
  do not.

Same configuration.

---

## A stronger archive adversary

A second checkpoint has

\[
R_1=R_2\approx -60.7616659871,
\qquad
Q_{a,\Gamma}\approx -21.9024889809,
\]

and still

\[
\mathfrak T^{\mathrm{het}}_{c,\Gamma}
\approx 1330.83171974>0.
\]

Both raw phase rates vanish
there. NUMERICAL archive
sample, not re-derived here.

So the obstruction is not
always multiplier *variation*.
A common negative \(R\) times
a negative \(Q_{a,\Gamma}\)
already gives positive
centered drift. “Make the
multipliers more coherent”
does not close the problem
either.

---

## The scaled family

For every integer \(L\ge 2\),

\[
k=(L+1,L,0),
\]

\[
p=(-L,0,L),\;
q=(-1,-L,-L),
\]

\[
r=(0,-L,L),\;
s=(-L-1,0,-L),
\]

with \(k+p+q=k+r+s=0\) and

\[
\boxed{\det(k,p,r)=L^2(2L+1)\neq 0.}
\]

The construction stays
three-dimensional as scale
grows. Relative radial width
shrinks (\(\sim 0.237\) at
\(L=2\) to \(\sim 0.0091\) at
\(L=55\)) while positive
centered drift persists in
the finite computations.

The normalized diagnostic

\[
\frac{\lvert\rho_\Gamma\rvert}
{\kappa^3(\lvert Q_{a,1}\rvert+\lvert Q_{a,2}\rvert)}
\]

decreases across those
samples (\(\sim 1.19\times 10^{-2}\)
to \(\sim 9.30\times 10^{-7}\)).
The source **warns** that this
is not a time-integrated
budget. NUMERICAL. Not
\(\int K\). Not DA-NS-2.

---

## Verdict of the experiment

Question: does SAG expose a
static directional
incompatibility that defeats
the old \(Q_a\) counterexample?

\[
\boxed{\textbf{NO — not at the static two-triad level.}}
\]

The known counterexample is
already a globally compatible
rank-three Fourier field
sharing a mode across two
scalene triangles, and
positive centered drift
survives.

Static compatibility has been
adversarially exhausted at
this level. SAG-6 (equal-input
stack, \(\rho_k(N)=1\)) is a
**different** object and stays
on its own page. This witness
never lived there.

---

## The next Gate

What survives is not a static
constant coherence defect. It
is the **scale dependence and
time occupation** of the
covariance remainder.

\[
\boxed{\textbf{Joint Gap–Charge Epoch Budget}}
\]

That is the September leftover,
already named on
[`DA-NS-2.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/DA-NS-2.md):

\[
K=\frac{(T_c-\theta\nu\mathcal D_s)_+}{Y},
\qquad
\sup_n\int_0^T K\,dt\le F(\nu,T,u_0)<\infty.
\]

The archive’s last line:

\[
\boxed{
\begin{aligned}
&\text{exact full-flow split}\\
&+\ \text{joint gap-charge control}\\
&+\ \text{one-use dissipation}\\
&+\ \text{summable resets}\\
&\quad\Longrightarrow?\quad\text{DA-NS-2}.
\end{aligned}
}
\]

Charge, radial covariance,
moving-barycenter error,
homochiral drift, cross-band
flux, phase/far terms, one-use
dissipation, summable resets.
All together, cutoff-uniform.
If the last line is
\(\int\mathcal D_s/Y\),
\(\sup\Lambda\), \(\int Y\), or a
continuation norm, **stop**.

This is **not** another version
of SAG-6. It is Loss B plus
the covariance remainder,
written as one budget.

A write of this Gate is either

1. a cutoff-uniform epoch
   budget that integrates the
   shrinking near-shell
   diagnostic, including
   barycenter motion and
   resets, and implies DA-NS-2,
   **or**
2. a named death that every
   such integral reintroduces
   \(\|\nabla u\|_\infty\),
   occupancy \(s\), or a
   tautological \(K\).

Do not reopen charge-only.
Do not reopen static
shared-output rescue.
Do not weld this Gate to
leftover 1 or leftover 5.
Do not restore unrestricted
\(\star\).

---

## Lock

Witness scalene, rank three,
shares \(k\), \(\Lambda=2\),
\(Q_{a,\Gamma}=0\),
\(\mathfrak T_{c,\Gamma}^{\mathrm{het}}>0\)
EXACT.
Not an equal-input circle.
SAG static shared-output rescue
of charge-only coercivity
**KILLED**.
Common-multiplier coherence
does not close.
\(L\)-family stays 3-D; finite
diagnostic decay is not
\(\int K\).
Next Gate = Joint Gap–Charge
Epoch Budget \(\to\) DA-NS-2.
Not SAG-6.
Reset \(\Delta W
=X\bigl[(\Lambda-K_{e+1})^2-(\Lambda-K_e)^2\bigr]\)
EXACT from \(W_K\). Residual
\((\Lambda-\lambda_e)\dot S_\Gamma\)
is Stieltjes.
Master ledger:
[`CENTERED-MASTER-LEDGER.md`](CENTERED-MASTER-LEDGER.md).
NS not solved.
