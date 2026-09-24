# Centered master ledger

24 September 2026.
**Exact algebra, numerical evidence,
and killed routes. Not a close.
NS not solved.**

Consolidated through today’s
SAG / JGC work against the
7 September showdown dossier
and PR #104
([`DA-NS-2.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/DA-NS-2.md)).

Four buckets only: **EXACT** /
**NUMERICAL** / **OPEN** /
**KILLED**. CLAIMED stays a
fifth word, not a proof.

Unaugmented NS. No \(Q_1\).
No \(\Phi\). No SND persistence.
No Theorem H. No Route A weld.
Unrestricted \(\star\) stays
**KILLED**. Claimed \(K\le 16/9\)
stays CLAIMED.

Pointers:
[`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md),
[`SAG-5-COMPATIBILITY.md`](SAG-5-COMPATIBILITY.md),
[`SAG-6-LATTICE-CIRCLE.md`](SAG-6-LATTICE-CIRCLE.md),
[`JOINT-EPOCH-BUDGET.md`](JOINT-EPOCH-BUDGET.md),
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md),
[`NARROW-HET-RESIDUAL.md`](NARROW-HET-RESIDUAL.md),
[`CORE-TAIL-SBP.md`](CORE-TAIL-SBP.md),
[`LOW-TAIL-CAPACITY.md`](LOW-TAIL-CAPACITY.md).

---

## Scoreboard

| # | Object | Bucket |
|---|---|---|
| 1 | Centered core \(\Lambda,\mathfrak T_c,\mathcal D_s,\Lambda'\) | **EXACT** |
| 2 | DA-NS-2 / \(K_{\min,\theta}\) | **OPEN** |
| 3 | Fourier \(T_k\), \(k_\perp\), flat \(\beta=4\alpha\) | **EXACT** |
| 4 | Two-shell \(T_{c,\triangle}=(\beta-\alpha)(\alpha+\beta-\Lambda)\tau_k\) | **EXACT** |
| 5 | Unequal-length defect | **EXACT** |
| 6 | Equal-input \(w=2\sigma(\rho\times\hat k)\) | **EXACT** |
| 7 | Static SAG: triangle / circle / star / tree | **KILLED** as missing power |
| 8 | Loop / helical holonomy \(\Gamma_{\mathrm{cyc}}(N)\) | **OPEN** |
| 9 | Phase-resolved helical network | **EXACT** finite algebra |
| 10 | Phase twins | **EXACT**; orientation-only **KILLED** |
| 11 | Heterochiral \(T_c^{\mathrm{het}}=RQ\), \(\rho_\Gamma\) | **EXACT** |
| 12 | Charge-only coercivity; static SAG rescue | **KILLED** |
| 13 | Cross-radius \(\Psi_\lambda^\varepsilon\) | **EXACT** |
| 14 | Moving-center \(\rho^{\mathrm{rad}}+\rho^{\mathrm{mov}}\) | **EXACT** |
| 15 | \(\dot{\mathfrak T}_{c,\Gamma}^{\mathrm{het}}\); residual \((\Lambda-\lambda_e)\dot S_\Gamma\) | **EXACT** |
| 16 | Joint Gap–Charge Epoch Budget | **OPEN** |
| 17 | Frozen \(W_K\); reset \(\Delta W\) | **EXACT** |
| 18 | \(r\sim\kappa^{-1/2}\) crossover; BROAD / NARROW map | **EXACT** equivalence; torus units |
| 19 | Narrow het residual \(2\kappa^3 Q_a-(\Lambda-\kappa_e^2)S_\Gamma\) | **OPEN** |
| 20 | \(S_\Gamma\) quadratic primitive on lattice loops | **NO** (holonomy); \(L\)-trees yes |
| 21 | Core / tail SBP \(\mathfrak T_c=\Phi_e'+2\kappa_e^3 Q_a-(\Lambda-\lambda_e)N\) | **EXACT** (frozen epoch) |
| 22 | \(\Phi_e/Y\); charge and moving \(N\) after SBP | **OPEN** |
| 23 | \(\phi_\kappa/d_\kappa\); core (C), high tail favorable | **EXACT** |
| 24 | Low-tail capacity \(L_e=\kappa_e^4 E_{\mathrm{low}}/Y\) | **OPEN** |

Every new mechanism must eventually
pay §2. Talking is not that integral.

---

## 1. Centered core — EXACT

\(A=-P\Delta\).

\[
X=\|A^{1/2}u\|_2^2,\qquad
Y=\|Au\|_2^2,\qquad
Z=\|A^{3/2}u\|_2^2,
\qquad
\boxed{\Lambda=Y/X}.
\]

\[
\tfrac12 X'+\nu Y=\mathcal N,
\qquad
\tfrac12 Y'+\nu Z=\mathcal M.
\]

\[
\boxed{\mathfrak T_c=\mathcal M-\Lambda\mathcal N},
\qquad
\boxed{\mathcal D_s=Z-\Lambda Y}.
\]

\[
\boxed{\Lambda'=\frac2X(\mathfrak T_c-\nu\mathcal D_s)},
\qquad
\boxed{(\log\Lambda)'=\frac2Y(\mathfrak T_c-\nu\mathcal D_s)}.
\]

\[
\boxed{\mathcal D_s=\|A^{1/2}(A-\Lambda)u\|_2^2\ge 0}.
\]

\(\Lambda\) is the spectral
barycenter. \(\mathfrak T_c\) is
nonlinear barycenter velocity.
\(\mathcal D_s\) is viscous
spectral variance. Foundation.
Do not redo.

---

## 2. Frozen endpoint — still the close — OPEN

Fixed \(0\le\theta<1\), Galerkin \(n\):

\[
\boxed{
K_{\min,\theta}^{(n)}
=
\frac{[\mathfrak T_c^{(n)}-\theta\nu\mathcal D_s^{(n)}]_+}{Y^{(n)}}.
}
\]

\[
\boxed{
\sup_n\int_0^T K_{\min,\theta}^{(n)}(t)\,dt
\le F(\nu,T,u_0)<\infty.
}
\tag{DA-NS-2}
\]

If obtained noncircularly and
uniformly in the cutoff, the
centered continuation chain
closes in this packaging.
Status: **OPEN**. This is the
quantity every new mechanism
must pay.

Tautological
\(K=(\mathfrak T_c-\theta\nu\mathcal D_s)_+/Y\)
is not content. \(\|\nabla u\|_\infty\)
is BKM. Lemma★ is the same
leftover in energy units,
**not proved**.

---

## 3. Fourier-triangle structure — EXACT

Triad \(p+q=k\).

\[
\boxed{
T_k
=\sum_{p+q=k}
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
}
\]

\(p\cdot v_p=0\) \(\Rightarrow\)
\(q\cdot v_p=k\cdot v_p\).
Equal input
\(\lvert p\rvert^2=\lvert q\rvert^2=\alpha\),
\(\lvert k\rvert^2=\beta\):

\[
\boxed{
\lvert k_\perp\rvert^2
=\beta\bigl(1-\beta/(4\alpha)\bigr).
}
\]

\(\beta=4\alpha\) kills the
channel geometrically.

---

## 4. Two-shell centered cancellation — EXACT

Closed equal-input triad,
\(\tau_p+\tau_q+\tau_k=0\),
\(f(\lambda)=\lambda(\lambda-\Lambda)\).

\[
\boxed{T_{c,\triangle}=[f(\beta)-f(\alpha)]\tau_k}
=\boxed{(\beta-\alpha)(\alpha+\beta-\Lambda)\tau_k}.
\]

With transverse geometry:

\[
\boxed{
T_{c,\triangle}
=
(\beta-\alpha)(\alpha+\beta-\Lambda)
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}
\,\mathcal S_{\alpha,\beta}^{\triangle}.
}
\]

Three zeros:

\[
\boxed{\beta=\alpha}
\text{ gap},\quad
\boxed{\beta=4\alpha}
\text{ flat},\quad
\boxed{\alpha+\beta=\Lambda}
\text{ centered}.
\]

---

## 5. Unequal-length defect — EXACT

\(\lvert p\rvert^2=a\),
\(\lvert q\rvert^2=b\),
\(\lvert k\rvert^2=c\), \(a\neq b\):

\[
\boxed{
T_{c,\triangle}
=[f(a)-f(c)]\tau_p+[f(b)-f(c)]\tau_q
}
\]

\[
=(a-c)(a+c-\Lambda)\tau_p
+(b-c)(b+c-\Lambda)\tau_q.
\]

The common equal-input
coefficient is gone.

---

## 6. Equal-input circle identity — EXACT

Fixed output \(k\),
\(p=k/2+\rho\), \(q=k/2-\rho\),
\(\rho\perp k\).
\(x=P_{k^\perp}v_p\),
\(y=P_{k^\perp}v_q\):

\[
\boxed{w_{p,q;k}=2\rho\times(x\times y)}.
\]

\(x,y\in k^\perp\) \(\Rightarrow\)
\(x\times y=\sigma\hat k\), so

\[
\boxed{w_{p,q;k}=2\sigma(\rho\times\hat k),
\quad\sigma=\det_{k^\perp}(x,y).}
\]

The vector is tangent to the
circle. DA reproduction to
relative error \(O(10^{-14})\):
**NUMERICAL** check of an
**EXACT** identity.

---

## 7. Static Signed Assembly — KILLED as missing power

Attacked hard. Dead as a source
of the missing power:

| Object | Result |
|---|---|
| one triangle | no gain |
| one circle | no scale gain; \(N^{1/2}\) obstructed |
| isolated multi-output star | \(\Gamma_{\mathrm{star}}=1\) |
| tree | baseline \(1\) |

A circular polarization of a
reused \(v_p\) saturates every
triangle at once.

\[
\boxed{\text{mode reuse alone does NOT create depletion}.}
\]

SAG-5 \(\rho_2=1/\sqrt{2}\) is
**EXACT** finite constant
depletion, not \(N^{-\delta}\).
SAG-6 \(\rho_k(N)=1\) on a
legal coherent family.
The \(2/\pi\) sign adversary
survives on the appropriate
real restriction; complex-phase
freedom is the constant
obstruction.

Only remaining **static**
candidate: closed-loop
polarization / helical
incompatibility (§8).

---

## 8. Loop gate — OPEN

Ordinary modal phases are not
enough. \(\phi_k=\xi\cdot k\)
satisfies
\(\phi_p+\phi_q-\phi_k=0\)
on every triad.

\[
\boxed{\text{loops do not automatically force phase frustration}.}
\]

Incidence: \(B\phi=b\pmod{2\pi}\).
For \(c^TB=0\), true frustration
needs holonomy

\[
\boxed{\Omega_c=c^Tb\not\equiv 0\pmod{2\pi}.}
\]

After the gauge quotient, the
candidate is polarization /
helical holonomy.

Optimization trends are
**NUMERICAL lower bounds
only**. Until

\[
L_N\le M_N\le U_N
\]

is certified, there is no
proved defect.
\(\Gamma_{\mathrm{cyc}}\le 0.7\)
would not pay the close.
The prize is

\[
\boxed{\Gamma_{\mathrm{cyc}}(N)\lesssim N^{-\delta}.}
\]

Status: **OPEN** / certification
pending. Not a write of DA-NS-2.

---

## 9. Phase-resolved helical network — EXACT finite algebra

\(ik\times h_s(k)=s\lvert k\rvert h_s(k)\),
\(\widehat u_k=\sum_{s=\pm}a_k^s h_s(k)\).

\[
\boxed{W_{\Delta,\sigma}
=g_{\Delta,\sigma}
\overline{a_k^{s_k}a_p^{s_p}a_q^{s_q}}.}
\]

\[
\boxed{\mathfrak T_{c,\Delta,\sigma}
=2C_{\Delta,\sigma}(\Lambda)\,\mathrm{Re}\,W_{\Delta,\sigma}.}
\]

\[
\boxed{\mathfrak T_c
=\sum_{\Delta,\sigma}
\mathcal A_{\Delta,\sigma}\cos\Psi_{\Delta,\sigma}.}
\]

Finite implementation matched
direct Galerkin sums on tested
176- and 4272-channel networks:
**NUMERICAL** match of **EXACT**
algebra. Not a bound.

---

## 10. Phase twins — EXACT; orientation-only KILLED

One \((++-)\) triad. Shift one
modal phase by \(\pi\):
\(X,Y,Z,\Lambda,\mathcal D_s,
\|\nabla u\|_3\) fixed, and

\[
\mathfrak T_c(u)=-0.79707557316,
\qquad
\mathfrak T_c(\widetilde u)=+0.79707557316.
\]

NUMERICAL values of an EXACT
sign flip. Every quadratic
helicity-weighted intensity
\(H^\varepsilon\) is likewise
fixed.

\[
\boxed{
(X,Y,Z,\Lambda,\mathcal D_s,H^\varepsilon)
\text{ fixed}
\not\Rightarrow
\operatorname{sign}\mathfrak T_c.
}
\]

Orientation-only payment:
**KILLED**. Keep the cubic
phase.

---

## 11. Heterochiral charge factorization — EXACT

\[
\boxed{\mathfrak T_{c,\gamma}^{\mathrm{het}}=R_{\Lambda,\gamma}Q_{a,\gamma}},
\]

\[
R_{\Lambda,\gamma}
=\frac{(i+o)(j+o)}{2o}(H_{ij\mid o}-\Lambda),
\quad
H_{ij\mid o}
=i^2+j^2+o^2+ij-o(i+j).
\]

Near \(i,j,o\approx\kappa=\sqrt\Lambda\),
\(R=2\kappa^3+O(\kappa^2\delta)\).

\[
\boxed{\mathfrak T_{c,\Gamma}^{\mathrm{het}}=2\kappa^3 Q_{a,\Gamma}+\rho_\Gamma},
\quad
\rho_\Gamma
=\sum_\gamma(R_{\Lambda,\gamma}-2\kappa^3)Q_{a,\gamma}.
\]

Covariance is structurally
necessary.

---

## 12. Charge-only coercivity — KILLED

Exact rank-three two-triad
witness (`JOINT-EPOCH-BUDGET.md`):
\(Q_{a,1}+Q_{a,2}=0\) and
\(\mathfrak T_{c,1}^{\mathrm{het}}+\mathfrak T_{c,2}^{\mathrm{het}}>0\).

Net charge cancellation does
not control positive centered
drift. The same field is
already globally compatible
and shares \(v_k\). Static SAG
shared-output rescue:
**KILLED**.

---

## 13. Cross-radius signed-helicity ledger — EXACT

Conservative oriented transfers
\(\eta_{\gamma,m}\),
\(\sum_m\eta_{\gamma,m}=0\),
\(f_\lambda(r)=r(r^2-\lambda)\):

\[
\boxed{T_\gamma=f_\lambda(o)Q_\gamma+\sum_m f_\lambda(r_m)\eta_{\gamma,m}.}
\]

\(\Pi_\gamma^H(\varrho)=\sum_{r_m>\varrho}\eta_{\gamma,m}\),

\[
\boxed{
\sum_m f_\lambda(r_m)\eta_{\gamma,m}
=\int_0^\infty(3\varrho^2-\lambda)\Pi_\gamma^H(\varrho)\,d\varrho.
}
\]

Frozen \(\lambda\): this is the
nonlinear derivative of

\[
\boxed{
\Psi_\lambda^\varepsilon(u)
=\tfrac12\sum_{k,s}\varepsilon s\,\lvert k\rvert^2
(\lvert k\rvert^2-\lambda)\lvert a_k^s\rvert^2.
}
\]

Surviving exact potential.

---

## 14. Moving-center covariance — EXACT

Epoch \(e\), freeze
\(\lambda_e=\kappa_e^2\).

\[
\boxed{
\mathfrak T_{c,\Gamma}^{\mathrm{het}}
=2\kappa_e^3 Q_{a,\Gamma}
+\rho_{\Gamma,e}^{\mathrm{rad}}
+\rho_{\Gamma,e}^{\mathrm{mov}}
}
\]

\[
\rho_{\Gamma,e}^{\mathrm{rad}}
=\sum_\gamma(R_{\lambda_e,\gamma}-2\kappa_e^3)Q_{a,\gamma},
\quad
\rho_{\Gamma,e}^{\mathrm{mov}}
=-(\Lambda-\lambda_e)S_\Gamma,
\]

\[
\boxed{S_\Gamma=\sum_\gamma A_\gamma Q_{a,\gamma}.}
\]

---

## 15. Latest derivative identity — EXACT

\(\partial_\Lambda R_{\Lambda,\gamma}=-A_\gamma\), so

\[
\boxed{
\dot{\mathfrak T}_{c,\Gamma}^{\mathrm{het}}
=-\Lambda'S_\Gamma
+\sum_\gamma R_{\Lambda,\gamma}\dot Q_{a,\gamma}.
}
\]

\[
\boxed{
-\Lambda'S_\Gamma
=\frac{d}{dt}\rho_{\Gamma,e}^{\mathrm{mov}}
+(\Lambda-\lambda_e)\dot S_\Gamma.
}
\]

The residual is exactly
\((\Lambda-\lambda_e)\dot S_\Gamma\).
Do **not** pointwise-estimate
\(\dot S_\Gamma\) (derivative
escalation). It is a
variation / Stieltjes problem.
This is the latest algebraic
frontier.

---

## 16. Joint Gap–Charge Epoch Budget — OPEN

\[
\boxed{
K_{\theta,n}
\le
-\frac{d}{dt}\mathscr Q_{n,e}
+g^{\mathrm{rad}}
+g^{\mathrm{mov}}
+g^{\mathrm{hom}}
+g^{\mathrm{cross}}
+g^{\mathrm{rot/far}}.
}
\]

Dissipation once:

\[
\boxed{\sum_\alpha d_{\alpha,n}\le\theta\nu\mathcal D_{s,n}.}
\]

Reset jumps: cutoff-uniform
ledger. A bounded charge on
each epoch is **not** enough.

If the last line is
\(\int\mathcal D_s/Y\),
\(\sup\Lambda\), \(\int Y\), or a
continuation norm, **stop**.
This is the next Gate
(`JOINT-EPOCH-BUDGET.md`).
Not another SAG-6.

---

## 17. Reset — EXACT

Frozen variance (any chart
center \(K\)):

\[
\boxed{W_K=\mathcal D_s+X(\Lambda-K)^2.}
\]

The incoming note cut off at
the jump. The identity already
gives it. At a reset
\(K_e\to K_{e+1}\) the
**physical** state
\((X,Y,Z,\Lambda,\mathcal D_s)\)
is fixed, so

\[
\boxed{
\Delta W
=X\bigl[(\Lambda-K_{e+1})^2-(\Lambda-K_e)^2\bigr]
=X(K_e-K_{e+1})(2\Lambda-K_e-K_{e+1}).
}
\]

That is the exact reset
ledger-line. It is not a bound
on \(\int K\). Summable resets
in §16 must use this jump,
not a new remainder.

---

## 18–20. Narrow residual and the primitive — see `NARROW-HET-RESIDUAL.md`

\(r^2=\mathcal D_s/(\Lambda Y)\)
makes
\(r\gtrsim\kappa^{-1/2}
\Leftrightarrow\mathcal D_s/Y\gtrsim\kappa\)
an identity in torus units.
\(R-2\kappa^3=O(\kappa^3 r)\)
linear; Vandermonde cubic.
The residual is
\(2\kappa^3 Q_a-(\Lambda-\kappa_e^2)S_\Gamma\).
On actual lattice het loops,
\(\mathsf B^{\mathrm{prim}}w=A\)
has a holonomy obstruction
(relative residual \(\approx 1\)).
\(L\)-family trees solve it
with \(\mathrm{cond}\sim 1.7\)
and \(\lVert w\rVert=O(1)\).
Isotropic
\(w(\lvert k\rvert,s)\) already
fails on the lattice tree.
Not a bound on \(\int K\).

---

## What every later write must respect

- Pay §2, or name a death.
- Keep \(\mathrm{Im}\) / helical
  phase. Phase twins killed
  orientation-only payment.
- Do not revive charge-only,
  static SAG rescue, star /
  circle / tree depletion, or
  unrestricted \(\star\).
- Do not estimate \(\dot S_\Gamma\)
  pointwise.
- Do not mix live
  \(\kappa(t)=\sqrt\Lambda\) with
  frozen \(\kappa_e\). The SBP
  is frozen-epoch only.
- Do not spend \(\nu\mathcal D_s\)
  twice.
- Loop \(\Gamma_{\mathrm{cyc}}\)
  needs a certified sandwich
  and then scale decay; a
  constant \(<1\) is not the
  close.
- Do not treat \(S_\Gamma\) as
  the derivative of a
  quadratic Fourier
  multiplier on lattice
  loops. That primitive is
  obstructed.

---

## Lock

Centered core EXACT.
DA-NS-2 OPEN.
Two-shell product EXACT.
Unequal-length defect EXACT.
Circle tangent identity EXACT.
Static SAG triangle / circle /
star / tree **KILLED** as
missing power.
Charge-only and static
shared-output rescue **KILLED**.
Phase twins: orientation-only
**KILLED**.
Loop gate OPEN, no certified
defect yet.
Epoch budget OPEN: next Gate.
\(W_K\) and \(\Delta W\) EXACT.
Narrow het residual OPEN:
[`NARROW-HET-RESIDUAL.md`](NARROW-HET-RESIDUAL.md).
\(r\gtrsim\kappa^{-1/2}
\Leftrightarrow\mathcal D_s/Y\gtrsim\kappa\)
EXACT, torus units.
Lattice-loop primitive for
\(S_\Gamma\): **NO**.
\(L\)-family trees: cond
\(\sim 1.7\), \(\lVert w\rVert=O(1)\).
Isotropic \(w(\lvert k\rvert,s)\)
fails on the lattice tree.
Core / tail SBP EXACT,
frozen epoch
([`CORE-TAIL-SBP.md`](CORE-TAIL-SBP.md)):
moves the tail, does not
remove it. Do not mix live
\(\kappa(t)\) with frozen
\(\kappa_e\). \(\Phi_e/Y\) OPEN.
Low tail OPEN; high tail
favorable
([`LOW-TAIL-CAPACITY.md`](LOW-TAIL-CAPACITY.md)).
Last mile = low-tail capacity
+ charge + epoch motion.
NS not solved.
