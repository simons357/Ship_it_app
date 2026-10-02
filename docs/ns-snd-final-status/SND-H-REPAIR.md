# Repaired SND nonlinear-term estimate — addendum

15 September 2026.
**Addendum to the 15 September audit
[`SND-H-REVIEW.md`](SND-H-REVIEW.md).
Distribute alongside that audit and the
original extract, not in place of them.**

Theorem H stays withdrawn as stated.
\(A.2\) (the \(M\)-dependent bound on
\(F_j\)) already sits in the audit.
This page assembles that bound with the
exact shell budget and a Dini treatment
of peak-shell crossings.

It does **not** prove SND propagation.
It does **not** prove a floor on \(\rho\).
Catalog B open stays 1 (`B_regularity`).
Not leftover 1. Not leftover 4. Not \(\star\).
Do not start H1 from this page.
Do not weld \(\star\).
Do not merge PR 48.
Ring stays **REPAIR**.
\(\Phi\)-cancel stays dropped on Track B.
This desk does not send mail to a panel.

Plain: [`SND-H-PLAIN.md`](SND-H-PLAIN.md).
Implication: [`SND-TO-REGULARITY.md`](SND-TO-REGULARITY.md).
Living extract (object under review):
[`UNAUGMENTED-R4-VORTICITY-PLAN.md`](UNAUGMENTED-R4-VORTICITY-PLAN.md)
§8.1.
Arithmetic: `python3 scripts/snd_h_repair.py`.

---

## Cover-sheet erratum (circulation)

Supersedes the 15 September cover-sheet
wording **as a circulation paragraph**.
The audit page stays the audit.

> In the previously circulated extract,
> Theorem H was not established, even
> under \(X\le M\): its proof conflated
> the flux quantity \(\Pi_j\) with the
> nonlinear term \(F_j\) alone, dropping
> a non-negative viscous tail; it relied
> on two three-dimensional Sobolev
> embeddings that do not hold in general
> — \(H^1\) does not control \(L^\infty\);
> \(H^2\) does not control \(\nabla u\) in
> \(L^\infty\) — and it did not supply a
> complete Bony decomposition. The
> displayed absolute-flux estimate fails
> explicitly on smooth, fixed-enstrophy
> shear fields with a fixed spread ratio
> — see Part 2 of the 15 September audit.
>
> A corrected, fully proved conditional
> bound for \(F_j\) (\(M\)-dependent,
> uniform in \(j\)) sits in the audit
> (Part 3 / \(A.2\) below). It is derived
> from Hölder and Poincaré, not from
> \(\Pi_j\). Assembling it with the exact
> per-shell enstrophy budget gives a
> proposed one-sided differential
> inequality for the peak fraction
> \(\rho\) (\(A.3\)). That assembly is an
> **upper** bound on the upper Dini
> derivative \(D^+\rho\). It is a
> comparison ceiling, not a floor. It
> has been checked against the shear,
> amplitude, and equal-shell families
> that falsified the prior version, in
> the sense of Part B below. It does not
> establish forward-in-time SND
> propagation or an initial-time spectral
> floor. Those remain open and require a
> separate comparison argument in the
> **lower** Dini direction, Bernstein
> constants frozen on a fixed partition,
> and an initial-data-dependent (not
> universal) hypothesis, consistent with
> Part 6 of the audit.
>
> The spectral shell toolkit is retained
> as research tools. \(\Phi\)-cancel stays
> dropped on unaugmented Track B. Ring
> stays REPAIR, not a theorem. Theorem H
> is withdrawn as stated. The SND
> propagation claim is open, with a
> validated bound on \(F_j\) in hand and
> the \(\rho\)-evolution argument still
> unwritten. The original manuscript
> extract is preserved as the object
> under review, unmodified.

---

## A.1 Exact shell budget

Do not start from packet \(\Pi_j=F_j-S_j\).
For smooth unforced NS, fixed \(j\), and
\(X_j=2^{2j}\lvert\Delta_j u\rvert_2^2\),

\[
\frac12\dot X_j
+\nu\,2^{2j}\lvert\nabla\Delta_j u\rvert_2^2
=-2^{2j}F_j,
\]

with \(F_j=\langle\Delta_j[(u\cdot\nabla)u],\Delta_j u\rangle\).
Write \(\widetilde D_j:=\nu 2^{2j}\lvert\nabla\Delta_j u\rvert_2^2\).
Then

\[
\dot X_j=-2\widetilde D_j-2\cdot 4^j F_j.
\]

On a frozen dyadic partition, Bernstein
gives comparability \(\widetilde D_j\asymp\nu 4^j X_j\),
not automatic equality. Any coefficient
\(\lambda_j\) in what follows is a
partition-dependent constant of order
\(4^j\), with a lower constant
\(\kappa\in(0,1]\) in
\(\widetilde D_j\ge\kappa\nu 4^j X_j\).
Exact Fourier-weighted shells make
\(\kappa=1\) on the shear family of the
audit.

---

## A.2 Sitting bound on \(F_j\)

Already proved in the audit, for smooth
mean-zero divergence-free \(u\) with
\(X\le M\):

\[
\lvert F_j\rvert
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{1/2}\mathcal D^{1/2},
\]

uniformly in \(j\). Hölder \((6,2,3)\),
mean-zero Sobolev / Poincaré, and
\(\mathcal D\ge\nu\lambda_1 X\).
Needs neither spread nor a dominant
shell. This is the only nonlinear-term
estimate from the original packet that
survives the counterexamples.

Legitimate packet consequences, already
recorded:

\[
\Pi_j^{\mathrm{packet}}\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,X^{1/2}\mathcal D^{1/2},
\qquad
\bigl\lvert\Pi_j^{\mathrm{packet}}\bigr\rvert
\le
S_j
+
C\sqrt{\frac{M}{\nu\lambda_1}}\,X^{1/2}\mathcal D^{1/2}.
\]

Neither is Theorem H. Neither is
propagation.

---

## A.3 Peak fraction: Dini assembly

Let \(j_*(t)\in\mathrm{argmax}_j X_j(t)\)
and \(J(t)=X_{j_*(t)}\), \(\rho=J/X\).
\(J\) is a maximum of finitely many
smooth functions, hence Lipschitz, not
everywhere differentiable. Envelope /
Danskin:

\[
D^+J(t)\le\max_{j\in\mathrm{argmax}(t)}\dot X_j(t).
\]

On a smooth unforced trajectory, \(X\) is
\(C^1\) wherever \(X>0\), so the quotient
rule holds with Dini on the numerator:

\[
D^+\rho
=\frac{D^+J}{X}-\rho\frac{\dot X}{X}.
\]

On an active peak shell, using \(A.2\)
and the Bernstein lower bound on
\(\widetilde D_{j_*}\),

\[
\dot X_{j_*}
\le
-2\kappa\nu 4^{j_*}J
+
2\cdot 4^{j_*}
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{1/2}\mathcal D^{1/2}.
\]

Hence the proposed assembly

\[
D^+\rho
\le
-2\kappa\nu 4^{j_*}\rho
+
2\cdot 4^{j_*}
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{-1/2}\mathcal D^{1/2}
-\rho\frac{\dot X}{X}.
\]

**Direction lock.** This is an **upper**
bound on \(D^+\rho\). Comparison against
an ODE \(\dot r=f(r)\) with this \(f\)
gives a **ceiling** \(\rho(t)\le r(t)\).
It does not by itself stop \(\rho\) from
falling. A floor, or the original G idea
that spread forces \(\dot\rho>0\), needs
a **lower** bound on a Dini derivative
of \(\rho\) in the spread regime. That
argument is not written here.

**Last term, without Bony.** The full
enstrophy identity is

\[
\frac12\dot X
=-\mathcal D-\langle(u\cdot\nabla)u,\Delta u\rangle,
\]

and the same Hölder bound gives
\(\lvert\langle(u\cdot\nabla)u,\Delta u\rangle\rvert\le C X^{3/2}\).
So

\[
\dot X\ge -2\mathcal D-2C X^{3/2}.
\]

For an **upper** bound on
\(-\rho\dot X/X\) one uses this lower
bound on \(\dot X\). That step does not
need a Bony split. Summing shell
equations to rebuild \(X\) would
re-introduce LP equivalence and the
incompletely indexed Bony gap from the
audit table. Do not take that route
for this term.

The remaining named gaps in any
propagation theorem on top of \(A.3\)
are therefore: (1) the missing lower
Dini bound / comparison barrier;
(2) frozen Bernstein \(\kappa\);
(3) handling of \(j_*\) jumps already
allowed by Danskin, but not yet turned
into a reference trajectory.

---

## A.4 What this does and does not establish

Does: a legitimate \(M\)-dependent
upper bound on \(D^+\rho\), free of the
\(\Pi_j\) defect and the false
\(L^\infty\) embeddings, once \(X\le M\)
and a frozen partition are assumed.

Does not: a floor \(\rho(t)\ge\rho_0\);
SND-C; Theorem H; Theorem G; a bound
on \(X\); Ring; leftover 1.

The gap is relocated correctly from
“the proof of Theorem H is wrong” to
“the input estimate on \(F_j\) sits;
the propagation argument is still
unwritten.”

---

## Part B — three families

### B.1 High-tail shears (audit §2)

On \(u_K\), \((u_K\cdot\nabla)u_K\equiv 0\),
so every \(F_j=0\). The original Theorem H
failed because it tracked \(\Pi_j=F_j-S_j\)
and dropped \(S_j\ne 0\). \(A.2\) is
vacuous on this family (\(0\le\) a positive
right-hand side).

\(A.3\) is **not** \(0\le 0\). The
dissipative and quotient terms remain.
On exact Fourier-weighted shells
(\(\kappa=1\)) with unique peak \(j_*=0\),

\[
\dot\rho
=-2\nu\rho-\rho\frac{\dot X}{X},
\]

which **equals** the \(F_j=0\) right-hand
side of \(A.3\). Locked at the audit
weights by `scripts/snd_h_repair.py`.
High shells die faster, so \(\rho\)
rises toward 1. The \(K\to\infty\) table
does not recur, because the quantity
being estimated is \(F_j\), not
\(\lvert F_j-S_j\rvert\).

Result: \(A.2\) and the \(F_j=0\) case of
\(A.3\) hold. They no longer answer the
question that broke.

### B.2 Amplitude (audit §5)

Under \(u=Aw\): \(X\to A^2 X\),
\(\mathcal D\to A^2\mathcal D\),
\(F_j\to A^3 F_j\). The \(A.2\)
right-hand side at **fixed** \(M\) is
quadratic in \(A\). That is compatible
only while \(A^2 X(w)\le M\). Sending
\(A\to\infty\) leaves the hypothesis,
which is the audit §5 obstruction to
an \(M\)-free quadratic bound.

If the ceiling is scaled,
\(M=A^2 M(w)\), then \(\sqrt{M}\)
supplies the missing factor of \(A\)
and the bound is cubic, matching
\(F_j\). Locked in the script.

Result: \(A.2\) passes by not claiming
the \(M\)-free estimate §5 killed.

### B.3 Equal shells / floor at \(t=0\) (audit §6)

For \(v_L\), \(\rho(0)=1/L\to 0\) at
fixed \(X=q\). No universal
\(c_*(\nu,\delta_*,M,C_S)\) from time
zero. \(A.3\) bounds a Dini derivative.
It makes no claim about \(\rho(0)\).
A small initial peak fraction is
outside what a forward-rate inequality
can repair. Any later SND theorem must
be conditioned on \(\rho(0)\), not
asserted uniformly over all data.

Result: consistent with §6. Not a
counterexample to \(A.2\) or \(A.3\).

---

## Part C — verdict

| Claim | Status |
|---|---|
| Displayed Theorem H, even with \(X\le M\) | **Withdrawn.** Audit stands. |
| \(A.2\) bound on \(F_j\) | **Sits.** |
| Packet \(\lvert\Pi_j\rvert\) estimate | **Fails** (shear table). |
| \(A.3\) as upper bound on \(D^+\rho\) | **Proposed assembly.** Holds with equality on exact-mode shears when \(F_j=0\) and \(j_*\) is unique. Not a floor. |
| SND propagation \(\rho(t)\ge\rho_0\) | **OPEN.** Needs a lower Dini / barrier argument. |
| Universal floor from \(t=0\) | **NO.** Audit §6. |
| Remove \(M\) from the same quadratic bound | **NO.** Audit §5. |
| Ring / \(\Phi\)-cancel / leftover 1 | Unchanged. REPAIR / dropped / open. |

---

## Standing corrections (carried)

| Location | Correction |
|---|---|
| August \(X\ge c_* J\) | \(J/X\ge c_*\) means \(J\ge c_* X\), i.e. \(X\le J/c_*\). |
| “\(H^1\) is supercritical” | Velocity \(\dot H^{1/2}\) is critical. \(H^1\) is subcritical. Energy control is supercritical. |
| “Energy class” | Leray–Hopf is \(L^\infty_t L^2_x\cap L^2_t H^1_x\), not a uniform-in-time \(H^1\) ceiling. |
| LP shell identities | \(\asymp\), not equality, unless exact Fourier weights are used. |
| Bony split | Still not fully indexed. Not used for the last term of \(A.3\) if the global enstrophy identity is used. |
| \(M=M(\lvert u_0\rvert_{H^1})\) | Carry \(\nu\) and the domain; \(T\)-dependence can suffice for continuation. |
| Official Statement (B) | Smooth periodic divergence-free data. An \(H^1\) route is not the literal wording. |
| “Naming fraud” | definition/claim mismatch. |

---

## What this does not do

It does not restore Theorem H.
It does not close leftover 1.
It does not restore unrestricted \(\star\).
It does not make Ring a theorem.
It does not put \(\Phi\)-cancel back on B.
It does not give a bound on \(X\).
Closing \(F_j\) still would not close
ordinary NS: [`SND-H-PLAIN.md`](SND-H-PLAIN.md).

NS not solved.

---

## Lock

Theorem H withdrawn.
A.2 sits: |F_j| ≤ C √(M/νλ_1) X^{1/2} D^{1/2}.
A.3 is D+ρ ≤ −2κν 4^{j*} ρ + driving − ρ Ẋ/X.
D+ is a ceiling, not a floor.
Last term from the global enstrophy
identity, not from Bony.
Shears: F_j=0, A.3 holds with equality
on exact modes, not 0≤0.
Amplitude: M caps A; scaled M is cubic.
Equal shells: no universal floor from t=0.
Propagation unwritten.
definition/claim mismatch.
NS not solved.
