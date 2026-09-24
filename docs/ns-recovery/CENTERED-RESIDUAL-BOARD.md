# Centered residual board

**24 September 2026.** Compressed program. One residual region.
**Not a closure theorem.** Ordinary NS is not solved. Soft X silent.
Do not put \(K(t)\) in the PDE.

Rally point (the only live close-adjacent job):

\[
\textbf{NARROW HETEROCHIRAL LAST MILE}
=
\textbf{LOW-TAIL CAPACITY}
+
\textbf{CHARGE}
+
\textbf{EPOCH MOTION}.
\]

Charge + motion remain

\[
2\kappa_e^3 Q_a-(\Lambda-\lambda_e)N,
\]

with \(Q_a\) the \(\dot H^{1/2}\) flux. Frozen convention only.
The capacity leftover after comparing \(\phi_\kappa\) to frozen
\(d_\kappa\) is **not** a generic tail: it is the

\[
\textbf{LOW-FREQUENCY TAIL}.
\]

SBP identity:
[`../../packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md`](../../packets/DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md).
Weight comparison (A)(B)(C):
[`../../packets/DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md`](../../packets/DA-GATE-PHI-VS-FROZEN-VARIANCE-2026-09-24.md).

\[
T_c
=
\Bigl(\frac{d}{dt}\Bigr)_{\mathrm{NL}}\Phi_e
+2\kappa_e^3 Q_a
-(\Lambda-\lambda_e)N.
\]

Narrow homo + het radial sit in \(\Phi_e'\). Core and high tail
of \(\Phi_e\) are controlled by frozen variance. Low tail is
**OPEN**. \(\mathsf B^{\mathrm{prim}}\) on loop families is still
**not on this tree** and is not invented.

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
\text{NARROW HOMO} & \to\text{cubic radial gap, now in }\Phi_e,\\
\text{NARROW HET RADIAL / CORE} & \to\text{controlled by frozen }d_\kappa,\\
\text{HIGH TAIL} & \to\text{even stronger variance weight},\\
\textbf{LOW TAIL} & \to\textbf{OPEN},\\
\textbf{CHARGE + MOVING EPOCH} & \to\textbf{OPEN}.
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

Snapshot \(L_e\) on the same fields (freeze \(\kappa_e=\sqrt{\Lambda}\);
not mixed into the SBP identity; not Taylor–Green):
[`../../packets/DA-GATE-LOW-TAIL-SNAPSHOT-2026-09-24.md`](../../packets/DA-GATE-LOW-TAIL-SNAPSHOT-2026-09-24.md).

| Field | \(\min m/\kappa\) | \(L_e\) | \(\Phi_e/Y\) | low-tail share |
|---|---:|---:|---:|---:|
| note triad | \(0.845\) | \(0\) | \(0.075\) | \(0\) |
| near-shell \(\varepsilon=0.025\) | \(0.895\) | \(0\) | \(\sim10^{-5}\) | \(0\) |
| \(v_8\) | \(0.456\) | \(0.060\) | \(0.113\) | \(0.23\) |
| separated \(L=16\) | \(0.0625\) | \(0.332\) | \(0.311\) | \(1\) |

\(v_n\) is a comparable annulus (\(\min m=n\)). The \(a=\tfrac12\)
cut nicks its inner edge; at \(a=0.4\), \(L_e=0\). Separated
triad is the on-tree high-core + \(m=1\) reservoir:
\(L_e\to 1/3\) and \(\Phi_e\) is low-tail dominated. Static
arithmetic, not a trajectory.

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

The SBP identity (frozen) puts narrow homo + het radial into
one nonnegative capacity \(\Phi_e\) that vanishes to second
order at the shell. That is an identity, not a bound.

Comparing \(\phi_\kappa\) to the frozen variance weight
\(d_\kappa(m)=m^2(m^2-\kappa^2)^2\) splits that capacity:

\[
\frac{\phi_\kappa}{d_\kappa}
=
\frac{m^2+2\kappa m+2\kappa^2}{2m^2(m+\kappa)^2}
=
\frac1{2\kappa^2}\frac{x^2+2x+2}{x^2(x+1)^2},
\qquad
x=\frac m\kappa.
\]

Shell limit \(5/(8\kappa^2)\). On a comparable annulus
\(a\kappa\le m\le b\kappa\), \(a>0\),

\[
\Phi_e^{\mathrm{core}}
\le
\frac{C(a,b)}{\kappa_e^2}
D_e^{\mathrm{frozen,core}},
\qquad
C(a,b)=\tfrac12 f(a).
\]

High tail \(\phi/d\sim 1/(2m^2)\) is favorable. Low tail
\(\phi/d\sim 1/m^2\) blows, in agreement with
\(\phi_e(0)=\kappa_e^4\). Energy and \(Y_{\mathrm{low}}\) do
not pay \(L_e=\kappa_e^4 E_{\mathrm{low}}/Y\).

The remaining hard pieces are therefore

\[
\textbf{low-tail }\Phi_e/Y,
\qquad
2\kappa_e^3 Q_a,
\qquad
-(\Lambda-\lambda_e)N.
\]

\(Q_a\) is the flux of \(\|u\|_{\dot H^{1/2}}^2\). Whether that
is the dossier’s cross-radius helicity primitive is not
confirmed here.

\(\mathsf B^{\mathrm{prim}}\) on loop/tree families remains
missing on this tree. Do not invent it. Do not replace a
signed sum by a sum of absolute values.

---

## Bullpen (this book)

| Seat | Job | Status here |
|---|---|---|
| Heavy | \(\mathsf B^{\mathrm{prim}}w=b\) on existing loop/tree families | **Blocked.** Families not on this tree. SBP \(\Phi_e\) identity filed; core/high tail vs \(d_\kappa\) sit; low tail **OPEN**. |
| Independent algebra | \(r\sim\kappa^{-1/2}\) conventions; \(\phi/d\) comparison | **Arithmetic sits.** Threshold not stamped. (A)(B)(C) sit. |
| DA | Classify BROAD/NARROW; find an existing primitive for \(S_\Gamma\); no invented bridge | Not this agent |
| Solver | On dangerous epochs: \(L_e=\kappa_e^4 E_{\mathrm{low}}/Y\) (or exact \(\phi_e\) low-tail). If \(\Phi/Y\) spikes, is it low-tail dominated? | **Named. TG 64/96 not on this tree.** On-tree snapshot: separated triad is low-tail dominated (\(L_e\to 1/3\)); \(v_n\) is not. |
| Narrow residual | Low-tail persistence under high \(\kappa_e\); charge; epoch motion | **OPEN** |

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

**OPEN primary.** DA-NS-2, and immediately upstream
**low-tail capacity** \(+\) \(2\kappa_e^3 Q_a-(\Lambda-\lambda_e)N\).
Core/high-tail \(\Phi_e\) vs frozen \(D_s\) sit as (C). The
BROAD tail-\(D_s\) estimate remains open. Taylor–Green must
report whether a \(\Phi/Y\) spike is low-tail dominated via
\(L_e\); data are not on this tree and are not run.

No new estimate is claimed. No continuation criterion.
**NS not solved.**
