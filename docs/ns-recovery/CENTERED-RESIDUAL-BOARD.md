# Centered residual board

**24 September 2026.** Compressed program. One residual region.
**Not a closure theorem.** Ordinary NS is not solved. Soft X silent.
Do not put \(K(t)\) in the PDE.

Rally point (the only live close-adjacent job):

\[
\textbf{NARROW HETEROCHIRAL RESIDUAL}
\qquad
2\kappa^3 Q_a-(\Lambda-\kappa_e^2)S_\Gamma,
\qquad
S_\Gamma=\sum_\gamma A_\gamma Q_{a,\gamma}.
\]

First question: does \(S_\Gamma\) admit a uniformly conditioned
translation-invariant quadratic primitive on the actual loop
networks? That test is \(\mathsf B^{\mathrm{prim}}w=b\).
The matrix and the loop/tree families are **not on this tree**.
They are not invented here.

Ledger: [`CENTERED-MASTER-LEDGER.md`](CENTERED-MASTER-LEDGER.md).
Width arithmetic: `scripts/centered_width_crossover.py`,
`results/centered_width_crossover.json`.
Clock: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).

Do not spend compute on single-circle searches, isolated stars,
constant coherence defects, generic phase-rotation experiments,
homochiral optimization, or more exact-shell counting unless it
feeds this residual.

---

## Endpoint (stable, OPEN)

\[
\exists\,\theta<1:\quad
\sup_n\int_0^T
\frac{\bigl[T_c^{(n)}-\theta\nu D_s^{(n)}\bigr]_+}{Y^{(n)}}\,dt
<\infty.
\tag{DA-NS-2}
\]

Clock:

\[
(\log\Lambda)'=\frac{2}{Y}(T_c-\nu D_s).
\]

Every mechanism must pay that integral. It is not sitting.

---

## Width split — arithmetic EXACT; threshold not stamped

Recorded relative spectral width

\[
r^2=\frac{D_s}{\Lambda Y}.
\]

On this book that is the barycenter relative width, not an
absolute radial width and not a single-mode \(\lvert k\rvert^2\):

\[
r=\frac{\sigma_\lambda}{\Lambda}=\frac{\sqrt{X D_s}}{Y},
\qquad
\frac{D_s}{Y}=\Lambda r^2,
\qquad
\kappa=\sqrt{\Lambda}.
\]

\(\Lambda=Y/X\) is the enstrophy barycenter (an eigenvalue).
\(\kappa=\sqrt{\Lambda}\) is its wavenumber. Do not set \(\Lambda=\lvert k\rvert^2\)
for one mode and reuse the same letter.

The unique exponent that makes \(D_s/Y\) have the scale of
\(\kappa\) is \(r\sim\kappa^{-1/2}\):

\[
r=\kappa^{-1/2}
\quad\Rightarrow\quad
\frac{D_s}{Y}=\Lambda\cdot\kappa^{-1}=\kappa.
\]

That is the recorded “missing-half-derivative” scale. It is
**arithmetic of the definitions**. It is not a derived decision
theorem. Do not stamp the crossover.

Schematic (architecture, not a proof):

\[
\text{DANGEROUS}
\to
\begin{cases}
\text{BROAD }(r\gtrsim\kappa^{-1/2}) & \to D_s/\text{viscosity},\\
\text{NARROW HOMO} & \to\text{cubic radial gap }(x-y)(y-z)(z-x),\\
\text{NARROW HET RADIAL} & \to\text{linear gap }R_\Lambda-2\kappa^3=O(\kappa^3 r),\\
\textbf{NARROW HET CHARGE + MOVING CENTER} & \to\textbf{CURRENT RESIDUAL}.
\end{cases}
\]

On the evaluator families already on this PR (not a stamp):

| Field | \(r\) | \(\kappa^{-1/2}\) | region |
|---|---:|---:|---|
| §4 note triad | \(0.350\) | \(0.919\) | NARROW |
| separated \(L=8\) | \(0.071\) | \(0.354\) | NARROW |
| \(v_1\) | \(0.268\) | \(0.667\) | NARROW |
| \(v_8\) | \(0.270\) | \(0.239\) | BROAD |
| near-shell \(\varepsilon=0.025\) | \(0.00447\) | \(\approx 0.67\) | NARROW |

\(v_n\) freezes \(r\approx 0.270\) while \(\kappa^{-1/2}\) shrinks, so
the family crosses into BROAD. That matches absorption at
\(\theta=1/2\) on \(v_n\). Near-shell stays NARROW. Convention
check: \(r=\sigma_\lambda/\Lambda\) on every row.

---

## Residual (EXACT factorization; payment OPEN)

Frozen epoch \(\kappa_e^2=\lambda_e\):

\[
T_{c,\Gamma}^{\mathrm{het}}
=2\kappa_e^3 Q_{a,\Gamma}
+\rho_{\Gamma,e}^{\mathrm{rad}}
+\rho_{\Gamma,e}^{\mathrm{mov}},
\qquad
\rho_{\Gamma,e}^{\mathrm{mov}}=-(\Lambda-\kappa_e^2)S_\Gamma.
\]

Radial \(\rho^{\mathrm{rad}}\) has a plausible narrow-width
payment (linear gap). The two hard pieces are

\[
2\kappa^3 Q_a
\qquad\text{and}\qquad
-(\Lambda-\kappa_e^2)S_\Gamma.
\]

Quadratic primitive test for \(S_\Gamma\): a modal capacity
\(\mathcal H_w=\sum_m w_m\lvert a_m\rvert^2\) whose nonlinear
derivative produces \(S_\Gamma\) iff

\[
\mathsf B^{\mathrm{prim}}w=b.
\]

Equivalently, every left-null vector satisfies \(c^Tb=0\),
\(c\in\ker[(\mathsf B^{\mathrm{prim}})^T]\). A failure is an exact
primitive-holonomy obstruction. No optimizer.

**Heavy on this tree:** \(\mathsf B^{\mathrm{prim}}\) and the
loop/tree families are missing. Rank, left-nullspace, \(c^Tb\),
and minimum-norm \(w\) versus \(N\) are **not computed**.
Do not invent the matrix. Do not substitute a coherence
optimization.

---

## Bullpen (this book)

| Seat | Job | Status here |
|---|---|---|
| Heavy | \(\mathsf B^{\mathrm{prim}}w=b\) on existing loop/tree families | **Blocked.** Families not on this tree. |
| Independent algebra | \(r\sim\kappa^{-1/2}\) conventions | **Arithmetic sits.** Threshold not stamped. |
| DA | Classify BROAD/NARROW; find an existing primitive for \(S_\Gamma\); no invented bridge | Not this agent |
| Solver | Adversarial \(J_{\theta,n}(T)\) and \(\alpha_{c,\kappa}^2\chi_\kappa^2\kappa\) | Not this tree |
| Narrow residual | Charge and moving covariance share a primitive, or prove they cannot | **OPEN** |

---

## Board

**CLOSED-INTERNAL / exact.** Centered clock, \(D_s\ge 0\), helical
reconstruction (dossier), phase twins, heterochiral factorization,
cross-radius signed-helicity primitive, Fourier-triangle identities,
\(W_K\) and fixed-state \(\Delta W\).

**KILLED / PARKED as closure mechanisms.** Unrestricted Lemma★,
charge-only coercivity, quadratic-data sign prediction, isolated
circle/star depletion, constant coherence gain, automatic
dephasing, naive higher-moment potential, naive soft atlas,
uniform energy-class \(K\) slots.

**NUMERICAL.** Corrected solver evidence, including Taylor–Green,
remains evidence only. Not on this tree.

**UNRESOLVED.** Certified loop defect, corrected per-field
\(\beta\), primitive conditioning, global patching / reset
control.

**OPEN primary.** DA-NS-2, and immediately upstream the narrow
heterochiral charge + moving-center payment.

No new estimate is claimed. No continuation criterion.
**NS not solved.**
