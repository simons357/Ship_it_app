# Centered master ledger — SAG / JGC consolidation

**24 September 2026.** Current centered ledger as handed over,
through today’s SAG / JGC work. Filing only.
Compressed rally: [`CENTERED-RESIDUAL-BOARD.md`](CENTERED-RESIDUAL-BOARD.md)
(low-tail capacity + charge + epoch motion).
**Not a closure theorem.** Ordinary NS is not solved. Soft X silent.
Do not put \(K(t)\) in the PDE.

Source of the consolidation: the paste on this turn, citing
`MASTER_DA_SHOWDOWN_DOSSIER_2026-09-07.md`. That dossier file is
**not on this tree.** Earlier useful extract on another branch:
`origin/cursor/unaug-ns-unified-status-a7a2:docs/DA-NS-2.md`.

How to read the tags:

| Tag | Meaning |
|---|---|
| **EXACT** | Algebra on this book, or recorded as exact in the paste |
| **REPORTED** | Numerical / SAG result in the paste; not recomputed here |
| **KILLED** | Named mechanism is dead |
| **OPEN** | Named target, not obtained |
| **TRUNCATED** | Paste broke; completed only if it is a unique corollary of a boxed identity |

Live instruments on this PR stay:
[`CENTERED-EQUATION.md`](CENTERED-EQUATION.md),
[`CENTERED-SPECTRAL-BARYCENTER.md`](CENTERED-SPECTRAL-BARYCENTER.md),
[`CENTERED-DRIFT-K-CANDIDATES.md`](CENTERED-DRIFT-K-CANDIDATES.md).
The superseded Gate-5–7 roadmap stays lineage only:
[`GATE-ROADMAP-LINEAGE.md`](GATE-ROADMAP-LINEAGE.md).
**REOPEN = recompute only.**

Notation on this book: \(T_c=\mathfrak T_c=M-\Lambda N\).
The two \(D_s\) writings \(\|(A-\Lambda)A^{1/2}u\|_2^2\) and
\(\|A^{1/2}(A-\Lambda)u\|_2^2\) agree on eigenmodes of \(A\).

---

## Status board

| # | Object | Tag |
|---|---|---|
| 1 | Centered core / \(\Lambda'\) | **EXACT** |
| 2 | DA-NS-2, \(\int K_{\min,\theta}^{(n)}\) | **OPEN** |
| 3 | Signed \(T_k\), Leray, \(\lvert k_\perp\rvert^2\) | **EXACT** |
| 4 | Two-shell product, three zeros | **EXACT** |
| 5 | Unequal-length defect | **EXACT** |
| 6 | Equal-input circle, \(w=2\sigma(\rho\times\hat k)\) | **EXACT**; \(10^{-14}\) **REPORTED** |
| 7 | Static Signed Assembly (triangle / circle / star / tree) | **KILLED** as the missing power; \(\Gamma_{\mathrm{star}}=1\) **REPORTED** |
| 8 | Loop gate / helical holonomy / \(\Gamma_{\mathrm{cyc}}(N)\lesssim N^{-\delta}\) | **OPEN** |
| 9 | Helical network reconstruction | **EXACT** finite algebra; 176 / 4272 match **REPORTED** |
| 10 | Phase twins | **KILLED** (orientation-only payment) |
| 11 | Heterochiral \(T_c=R_{\Lambda}Q_a\) and \(\rho_\Gamma\) | **EXACT** |
| 12 | Charge-only coercivity | **KILLED** |
| 13 | Cross-radius signed-helicity ledger / \(\Psi_\lambda^\varepsilon\) | **EXACT** |
| 14 | Moving-center covariance, \(S_\Gamma\) | **EXACT** |
| 15 | \(\dot T_c^{\mathrm{het}}\) residual \((\Lambda-\lambda_e)\dot S_\Gamma\) | **EXACT**; latest algebraic frontier |
| 16 | Joint Gap–Charge Epoch Budget | **OPEN** |
| 17 | Frozen \(W_K=D_s+X(\Lambda-K)^2\) | **EXACT** |
| 17 | Reset jump \(\Delta W\) at fixed state | **EXACT** (unique corollary of \(W_K\)) |
| 17 | Cutoff-uniform reset ledger | **OPEN** |
| 18 | \(\phi_\kappa/d_\kappa\) (A)(B)(C); shell limit \(5/(8\kappa^2)\) | **EXACT** |
| 18 | Low-tail capacity \(L_e=\kappa_e^4 E_{\mathrm{low}}/Y\) | **OPEN** |
| 18 | \(\phi_\kappa=\kappa^4-\kappa^3 m-\tfrac12\kappa^2 m^2+\tfrac12 m^4\) | **EXACT** |
| 18 | Snapshot \(L_e\) on \(v_n\) / near-shell / separated triad | **REPORTED**; TG not run |
| 19 | \(T_c=\Lambda\langle\delta,T\rangle+\sum\delta^2 T\) | **EXACT** |
| 19 | \(L_{1,N}=\Lambda_N\langle\delta_N,T_N^{(0)}\rangle\), \(R_{2,N}\) | **EXACT** protocol; \(T^{(0)}\) not live \(T\) |
| 19 | Heterochiral sign tree / \(\mathcal A_N^{+}\) | **ARMED**; family not on this tree |

Every new mechanism must eventually pay DA-NS-2. That integral is
not sitting. The sharpened last mile is
[`CENTERED-RESIDUAL-BOARD.md`](CENTERED-RESIDUAL-BOARD.md).

---

## 1. Centered core — EXACT

Classical unforced incompressible NSE, \(A=-P\Delta\):

\[
X=\|A^{1/2}u\|_2^2,\qquad
Y=\|Au\|_2^2,\qquad
Z=\|A^{3/2}u\|_2^2,
\qquad
\Lambda=\frac{Y}{X}.
\]

\[
\tfrac12 X'+\nu Y=\mathcal N,
\qquad
\tfrac12 Y'+\nu Z=\mathcal M.
\]

This book’s evaluator writing is the same pair:
\(X'=-2\nu Y+2N\), \(Y'=-2\nu Z+2M\).

\[
T_c=\mathfrak T_c=\mathcal M-\Lambda\mathcal N,
\qquad
D_s=Z-\Lambda Y
=\|A^{1/2}(A-\Lambda)u\|_2^2\ge 0.
\]

\[
\Lambda'=\frac{2}{X}(T_c-\nu D_s),
\qquad
(\log\Lambda)'=\frac{2}{Y}(T_c-\nu D_s).
\]

Page: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).

Picture (names, not estimates):

\[
\Lambda=\text{spectral barycenter},\qquad
T_c=\text{nonlinear barycenter velocity},\qquad
D_s=\text{viscous spectral variance}.
\]

The mass-only half of that picture is already locked on this PR:
\(D_s=X\mathrm{Var}_p(\lambda)\). Pairing with signed stretch:
\(T_c=X\mathrm{Cov}_p(\lambda,t)\).
[`CENTERED-SPECTRAL-BARYCENTER.md`](CENTERED-SPECTRAL-BARYCENTER.md).

---

## 2. Frozen endpoint — OPEN (the actual close)

For fixed \(0\le\theta<1\), Galerkin index \(n\),

\[
K_{\min,\theta}^{(n)}
=
\frac{\bigl[T_c^{(n)}-\theta\nu D_s^{(n)}\bigr]_+}{Y^{(n)}}.
\]

That is the tautological \(K_Y\) already named on the inventory.
Content is the integral.

**DA-NS-2 (live theorem target, not obtained):**

\[
\sup_n\int_0^T K_{\min,\theta}^{(n)}(t)\,dt
\le F(\nu,T,u_0)<\infty.
\]

If obtained noncircularly and uniformly in the cutoff, the
centered continuation chain closes. Status: **OPEN**.

Do not add this \(K\) to the PDE. Unrestricted uniform
\(C_0\) / Lemma★ remains **dead** on \(v_n\). A pathwise
integrable remainder is a different sentence.

---

## 3. Fourier triangle — EXACT

\(p+q=k\),

\[
T_k
=
\sum_{p+q=k}
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Keep \(\mathrm{Im}\). Leray: \(q\cdot v_p=k\cdot v_p\).
Equal input \(\lvert p\rvert^2=\lvert q\rvert^2=\alpha\),
\(\lvert k\rvert^2=\beta\):

\[
\lvert k_\perp\rvert^2
=\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr).
\]

Flat configuration \(\beta=4\alpha\) kills the pair. No division
by \(1-\beta/(4\alpha)\).
[`FOURIER-TRIANGLE-GEOMETRY.md`](FOURIER-TRIANGLE-GEOMETRY.md).

---

## 4. Two-shell centered cancellation — EXACT

Closed equal-input triad, \(\tau_p+\tau_q+\tau_k=0\),
\(f(\lambda)=\lambda(\lambda-\Lambda)\). Then

\[
T_{c,\triangle}
=[f(\beta)-f(\alpha)]\tau_k
=
(\beta-\alpha)(\alpha+\beta-\Lambda)\tau_k.
\]

This book’s six-mode evaluator writes a factor \(2\) because it
sums both conjugate modes. Do not “correct” one convention into
the other.

Recorded structural form after transverse geometry:

\[
T_{c,\triangle}
=
(\beta-\alpha)(\alpha+\beta-\Lambda)
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}
\,\mathcal S_{\alpha,\beta}^{\triangle}.
\]

Three exact zeros:

| Zero | Name |
|---|---|
| \(\beta=\alpha\) | gap cancellation |
| \(\beta=4\alpha\) | flat / transverse cancellation |
| \(\alpha+\beta=\Lambda\) | centered cancellation |

\(\mathcal S_{\alpha,\beta}^{\triangle}\) is not Need★ and is not
a bound on occupancy.

---

## 5. Unequal-length defect — EXACT

\(\lvert p\rvert^2=a\), \(\lvert q\rvert^2=b\), \(\lvert k\rvert^2=c\),
\(a\neq b\):

\[
T_{c,\triangle}
=[f(a)-f(c)]\tau_p+[f(b)-f(c)]\tau_q
=
(a-c)(a+c-\Lambda)\tau_p
+(b-c)(b+c-\Lambda)\tau_q.
\]

The common equal-input coefficient is gone. Same gap factor
already used in
[`CENTERED-DRIFT-TRIAD-SPLIT.md`](CENTERED-DRIFT-TRIAD-SPLIT.md).

---

## 6. Equal-input circle — EXACT; match REPORTED

Fixed output \(k\), \(p=k/2+\rho\), \(q=k/2-\rho\), \(\rho\perp k\).
Horizontal polarizations \(x=P_{k^\perp}v_p\), \(y=P_{k^\perp}v_q\):

\[
w_{p,q;k}=2\rho\times(x\times y)=2\sigma(\rho\times\hat k),
\qquad
\sigma=\det_{k^\perp}(x,y).
\]

The vector is tangent to the equal-input circle.
DA match \(\sim 10^{-14}\) relative: **REPORTED**, not recomputed here.

---

## 7. Static Signed Assembly — KILLED as the missing power

Reported hierarchy on the SAG attack (not this PR’s evaluator
families):

- triangle \(\to\) no gain
- circle \(\to\) no scale gain
- isolated multi-output star \(\to\) \(\Gamma_{\mathrm{star}}=1\) (SAG-6′)
- tree \(\to\) baseline \(1\)

Mode reuse alone does **not** create depletion. A single circle
cannot supply scale decay: determinant phases undo angular
dispersion. The \(2/\pi\) sign adversary survives on the
appropriate real/sign restriction.

All four are **dead as sources of the missing power**.
The remaining static candidate is closed-loop
polarization / helical incompatibility.

\(\Gamma_{\mathrm{star}}=1\) is **REPORTED**. Not recomputed here.

---

## 8. Loop gate — OPEN

A global phase \(\phi_k=\xi\cdot k\) satisfies
\(\phi_p+\phi_q-\phi_k=0\) on every triad. Loops do not
automatically force phase frustration.

Incidence: \(B\phi=b\pmod{2\pi}\). For \(c^TB=0\), true
frustration needs nonzero holonomy \(\Omega_c=c^Tb\not\equiv 0
\pmod{2\pi}\). After the gauge quotient, the candidate is
polarization / helical holonomy.

Optimization trends are lower bounds only. Until

\[
L_N\le M_N\le U_N
\]

is certified, there is no proved defect.
Even \(\Gamma_{\mathrm{cyc}}\le 0.7\) would not be enough.
The prize is scale decay \(\Gamma_{\mathrm{cyc}}(N)\lesssim N^{-\delta}\).

Status: **OPEN** / certification pending.

---

## 9. Phase-resolved helical network — EXACT finite algebra

Helical basis \(ik\times h_s(k)=s\lvert k\rvert h_s(k)\),
\(\widehat u_k=\sum_{s=\pm}a_k^s h_s(k)\). Signed channel:

\[
W_{\Delta,\sigma}
=
g_{\Delta,\sigma}
\overline{a_k^{s_k}a_p^{s_p}a_q^{s_q}},
\qquad
T_{c,\Delta,\sigma}
=
2C_{\Delta,\sigma}(\Lambda)\,\mathrm{Re}\,W_{\Delta,\sigma}.
\]

\[
T_c=\sum_{\Delta,\sigma}\mathcal A_{\Delta,\sigma}\cos\Psi_{\Delta,\sigma}.
\]

Finite match to direct Galerkin sums on 176- and 4,272-channel
networks: **REPORTED** (dossier). Not recomputed here.

---

## 10. Phase twins — KILLED

One \((++-)\) triad: a \(\pi\) shift of one modal phase leaves
\(X,Y,Z,\Lambda,D_s,\|\nabla u\|_3\) fixed and flips

\[
T_c(u)=-0.79707557316,
\qquad
T_c(\widetilde u)=+0.79707557316.
\]

Those two numbers are **REPORTED** from the dossier. The kill is
the existence of a sign flip at fixed quadratic data, not the
digits.

The same map preserves every quadratic helicity-weighted
intensity \(H^\varepsilon=\sum_{k,s}\varepsilon s\,\lambda_k\lvert a_k^s\rvert^2\).
Hence

\[
(X,Y,Z,\Lambda,D_s,H^\varepsilon)\text{ fixed}
\not\Rightarrow
\mathrm{sign}\,T_c.
\]

Orientation-only payment: **KILLED**. Cubic phase cannot be
discarded. \(T_c\) is odd; this is the same honesty already on
the evaluator.

---

## 11. Heterochiral charge factorization — EXACT

Channel \(\gamma\):

\[
T_{c,\gamma}^{\mathrm{het}}=R_{\Lambda,\gamma}Q_{a,\gamma},
\qquad
R_{\Lambda,\gamma}
=
\frac{(i+o)(j+o)}{2o}(H_{ij\mid o}-\Lambda),
\]

\[
H_{ij\mid o}=i^2+j^2+o^2+ij-o(i+j).
\]

Near \(i,j,o\approx\kappa=\sqrt{\Lambda}\),
\(R_{\Lambda,\gamma}=2\kappa^3+O(\kappa^2\delta)\).

Connected network:

\[
T_{c,\Gamma}^{\mathrm{het}}=2\kappa^3 Q_{a,\Gamma}+\rho_\Gamma,
\qquad
\rho_\Gamma=\sum_\gamma(R_{\Lambda,\gamma}-2\kappa^3)Q_{a,\gamma}.
\]

The covariance term is structurally necessary.

---

## 12. Charge-only coercivity — KILLED

Rank-three two-triad witness: \(Q_{a,1}+Q_{a,2}=0\) while
\(T_{c,1}^{\mathrm{het}}+T_{c,2}^{\mathrm{het}}>0\).
Net charge cancellation does not control positive centered
drift. The same field is already one globally compatible
rank-three Fourier field, so it also kills a static SAG
shared-output rescue.

Finite check on the other branch:
`origin/cursor/unaug-ns-unified-status-a7a2:scripts/centered_barycenter.py`
(`two_triad_strike`). Do not rebuild it as a new close.

---

## 13. Cross-radius signed-helicity ledger — EXACT

Conservative oriented transfers \(\sum_m\eta_{\gamma,m}=0\),
\(f_\lambda(r)=r(r^2-\lambda)\):

\[
T_\gamma
=f_\lambda(o)Q_\gamma+\sum_m f_\lambda(r_m)\eta_{\gamma,m},
\qquad
\sum_m f_\lambda(r_m)\eta_{\gamma,m}
=\int_0^\infty(3\varrho^2-\lambda)\Pi_\gamma^H(\varrho)\,d\varrho,
\]

with \(\Pi_\gamma^H(\varrho)=\sum_{r_m>\varrho}\eta_{\gamma,m}\).

For frozen \(\lambda\), that is the nonlinear derivative of

\[
\Psi_\lambda^\varepsilon(u)
=
\frac12\sum_{k,s}\varepsilon s\,\lvert k\rvert^2
(\lvert k\rvert^2-\lambda)\lvert a_k^s\rvert^2.
\]

Surviving exact potential. Not a remainder theorem.

---

## 14. Moving-center covariance — EXACT

Epoch \(e\), freeze \(\lambda_e=\kappa_e^2\):

\[
T_{c,\Gamma}^{\mathrm{het}}
=
2\kappa_e^3 Q_{a,\Gamma}
+\rho_{\Gamma,e}^{\mathrm{rad}}
+\rho_{\Gamma,e}^{\mathrm{mov}},
\]

\[
\rho_{\Gamma,e}^{\mathrm{rad}}
=\sum_\gamma(R_{\lambda_e,\gamma}-2\kappa_e^3)Q_{a,\gamma},
\qquad
S_\Gamma=\sum_\gamma A_\gamma Q_{a,\gamma},
\qquad
\rho_{\Gamma,e}^{\mathrm{mov}}=-(\Lambda-\lambda_e)S_\Gamma.
\]

---

## 15. Latest derivative identity — EXACT

\(\partial_\Lambda R_{\Lambda,\gamma}=-A_\gamma\), so

\[
\dot T_{c,\Gamma}^{\mathrm{het}}
=-\Lambda'S_\Gamma+\sum_\gamma R_{\Lambda,\gamma}\dot Q_{a,\gamma},
\qquad
-\Lambda'S_\Gamma
=\frac{d}{dt}\rho_{\Gamma,e}^{\mathrm{mov}}
+(\Lambda-\lambda_e)\dot S_\Gamma.
\]

The residual is exactly \((\Lambda-\lambda_e)\dot S_\Gamma\).
Do not pointwise-estimate \(\dot S_\Gamma\) (derivative
escalation). It is a variation / Stieltjes problem.
Latest algebraic frontier. Not DA-NS-2.

---

## 16. Joint Gap–Charge Epoch Budget — OPEN

Required shape (target, not a theorem):

\[
K_{\theta,n}
\le
-\frac{d}{dt}\mathscr Q_{n,e}
+g^{\mathrm{rad}}+g^{\mathrm{mov}}+g^{\mathrm{hom}}
+g^{\mathrm{cross}}+g^{\mathrm{rot/far}}.
\]

Dissipation may be spent only once:
\(\sum_\alpha d_{\alpha,n}\le\theta\nu D_{s,n}\).
Reset jumps need a cutoff-uniform ledger.
A bounded charge on each epoch is insufficient.

If the last line of a write is \(\int D_s/Y\), \(\sup\Lambda\),
\(\int Y\), or a continuation norm, stop.

---

## 17. Frozen variance and reset jump — EXACT; ledger OPEN

Recorded complete identity:

\[
W_K=D_s+X(\Lambda-K)^2
=\|A^{1/2}(A-K)u\|_2^2.
\]

The paste broke at the chart reset \(K_e\to K_{e+1}\) with the
physical state fixed. **REOPEN = recompute only.** The unique
corollary of the boxed \(W_K\) at fixed \(X,\Lambda,D_s\) is

\[
\Delta W
=
W_{K_{e+1}}-W_{K_e}
=
X\Bigl[(\Lambda-K_{e+1})^2-(\Lambda-K_e)^2\Bigr].
\]

That matches the cut fragment
\(\Delta W\ldots X[(\Lambda-K_{e+1})^2\ldots\)
and nothing else. It is not a bound and not a summable ledger.

Algebra lock: `scripts/centered_wk_identity.py`,
`results/centered_wk_identity.json`.

Cutoff-uniform control of the reset jumps in DA-NS-2 remains
**OPEN**.

---

## What this does not do

It does not obtain DA-NS-2.
It does not restore unrestricted ★.
It does not certify the loop gate.
It does not reopen Gate 5.
It does not splice SND, Theorem H, Soft X, or five fingers.
It does not turn \(\Delta W\) into a cutoff-uniform ledger.

No new estimate is claimed. No continuation criterion.
**NS not solved.**
