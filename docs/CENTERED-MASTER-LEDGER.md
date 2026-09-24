# Centered master ledger

**24 September 2026.** Consolidated through today’s SAG / JGC work.

Exact algebra, numerical evidence, and killed items are kept in
separate buckets. This page is a ledger, not a close.

**Classical unaugmented 3-D Navier–Stokes stays open.**
DA-NS-2 stays **OPEN**. NS not solved.

Source: the centered master ledger sent 24 September 2026.
Cited dossier: `MASTER_DA_SHOWDOWN_DOSSIER_2026-09-07.md`
(not in this tree; not reconstructed here).

Machine lock: [`data/centered_master_ledger_2026-09-24.json`](../data/centered_master_ledger_2026-09-24.json).

§17 arrived **truncated**. The reset increment was cut mid-formula.
It is not completed on this page. Send the rest to reopen that line.

---

## Status board

| # | Item | Bucket |
|---|---|---|
| 1 | Centered core | **EXACT** |
| 2 | Frozen endpoint / DA-NS-2 | **OPEN** — the actual close |
| 3 | Fourier-triangle structure | **EXACT** |
| 4 | Two-shell centered cancellation | **EXACT** |
| 5 | Unequal-length defect | **EXACT** |
| 6 | Equal-input circle identity | **EXACT** (DA check \(\sim 10^{-14}\)) |
| 7 | Static Signed Assembly | **KILLED** as a power source |
| 8 | Loop gate | **OPEN** / certification pending |
| 9 | Phase-resolved helical network | **EXACT** finite algebra |
| 10 | Phase twins | **EXACT** counterexample; orientation-only **KILLED** |
| 11 | Heterochiral charge factorization | **EXACT** |
| 12 | Charge-only coercivity | **KILLED** |
| 13 | Cross-radius signed-helicity ledger | **EXACT** |
| 14 | Moving-center covariance | **EXACT** |
| 15 | Latest derivative identity | **EXACT** — algebraic frontier |
| 16 | Joint Gap–Charge Epoch Budget | **OPEN** |
| 17 | Reset / frozen variance | **EXACT** identity sits; increment **TRUNCATED** |

Numerical evidence (helical-network match, loop lower bounds, S
measurement) is not a substitute for DA-NS-2.

---

## 1. Centered core — EXACT

For classical unforced incompressible NSE, with \(A=-P\Delta\),

\[
X=\|A^{1/2}u\|_2^2,\qquad
Y=\|Au\|_2^2,\qquad
Z=\|A^{3/2}u\|_2^2,
\]

and

\[
\boxed{\Lambda=\frac{Y}{X}}.
\]

The derivative-level balances are

\[
\frac12 X'+\nu Y=\mathcal N,
\qquad
\frac12 Y'+\nu Z=\mathcal M.
\]

Define

\[
\boxed{\mathfrak T_c=\mathcal M-\Lambda\mathcal N}
\]

and

\[
\boxed{\mathcal D_s=Z-\Lambda Y}.
\]

Then

\[
\boxed{
\Lambda'
=
\frac{2}{X}
(\mathfrak T_c-\nu\mathcal D_s)
}
\]

and equivalently

\[
\boxed{
(\log\Lambda)'
=
\frac{2}{Y}
(\mathfrak T_c-\nu\mathcal D_s).
}
\]

The viscous term is an exact variance:

\[
\boxed{
\mathcal D_s
=
\|A^{1/2}(A-\Lambda)u\|_2^2\ge0.
}

\]

So the picture remains:

\[
\boxed{
\Lambda=\text{spectral barycenter},\qquad
\mathfrak T_c=\text{nonlinear barycenter velocity},\qquad
\mathcal D_s=\text{viscous spectral variance}.
}
\]

These are the foundation.

---

## 2. Frozen endpoint — still the actual close

For fixed \(0\le\theta<1\), define

\[
\boxed{
K_{\min,\theta}^{(n)}
=
\frac{
[\mathfrak T_c^{(n)}
-\theta\nu\mathcal D_s^{(n)}]_+
}{
Y^{(n)}
}.
}
\]

The live theorem remains

\[
\boxed{
\sup_n
\int_0^T
K_{\min,\theta}^{(n)}(t)\,dt
\le
F(\nu,T,u_0)<\infty.
}
\tag{DA-NS-2}
\]

If obtained noncircularly and uniformly in the Galerkin cutoff, the
centered continuation chain closes.

**Status: OPEN.** This is the quantity every new mechanism must
eventually pay.

---

## 3. Exact Fourier-triangle structure

For a Fourier triad \(p+q=k\), the signed modal transfer retains the
imaginary cubic product

\[
\boxed{
T_k
=
\sum_{p+q=k}
\operatorname{Im}
\left[
(q\cdot v_p)
(v_q\cdot\overline{v_k})
\right].
}
\]

Divergence freedom gives \(p\cdot v_p=0\) and therefore
\(q\cdot v_p=k\cdot v_p\).

When \(|p|^2=|q|^2=\alpha\) and \(|k|^2=\beta\),

\[
\boxed{
|k_\perp|^2
=
\beta\left(1-\frac{\beta}{4\alpha}\right).
}
\]

Thus the flat configuration

\[
\boxed{\beta=4\alpha}
\]

kills the interaction geometrically.

---

## 4. Two-shell centered cancellation — EXACT

For a closed equal-input triad, let \(\tau_p+\tau_q+\tau_k=0\).
With \(f(\lambda)=\lambda(\lambda-\Lambda)\), the centered triadic
contribution is

\[
f(\alpha)\tau_p+f(\alpha)\tau_q+f(\beta)\tau_k.
\]

Energy conservation gives

\[
\boxed{
T_{c,\triangle}
=
[f(\beta)-f(\alpha)]\tau_k
}
\]

and therefore

\[
\boxed{
T_{c,\triangle}
=
(\beta-\alpha)(\alpha+\beta-\Lambda)\tau_k.
}
\]

Combining this with transverse geometry gives the exact structural form

\[
\boxed{
T_{c,\triangle}
=
(\beta-\alpha)
(\alpha+\beta-\Lambda)
\sqrt{
\beta\left(1-\frac{\beta}{4\alpha}\right)
}
\,\mathcal S_{\alpha,\beta}^{\triangle}.
}
\]

Three distinct zero mechanisms are visible:

\[
\boxed{\beta=\alpha}
\quad\text{gap cancellation},\qquad
\boxed{\beta=4\alpha}
\quad\text{flat/transverse cancellation},\qquad
\boxed{\alpha+\beta=\Lambda}
\quad\text{centered cancellation}.
\]

---

## 5. Unequal-length defect — EXACT

For \(|p|^2=a\), \(|q|^2=b\), \(|k|^2=c\) with \(a\neq b\),

\[
\boxed{
T_{c,\triangle}
=
[f(a)-f(c)]\tau_p
+
[f(b)-f(c)]\tau_q
}
\]

or

\[
\boxed{
T_{c,\triangle}
=
(a-c)(a+c-\Lambda)\tau_p
+
(b-c)(b+c-\Lambda)\tau_q.
}
\]

The common equal-input coefficient disappears. That is the precise
algebraic version of the unequal-length defect.

---

## 6. Equal-input circle identity — EXACT

For fixed output \(k\),

\[
p=\frac{k}{2}+\rho,\qquad
q=\frac{k}{2}-\rho,\qquad
\rho\perp k.
\]

With horizontal polarizations \(x=P_{k^\perp}v_p\), \(y=P_{k^\perp}v_q\),
the symmetrized pair contribution satisfies

\[
\boxed{
w_{p,q;k}
=
2\rho\times(x\times y).
}
\]

Since \(x,y\in k^\perp\), \(x\times y=\sigma\hat k\), so

\[
\boxed{
w_{p,q;k}
=
2\sigma(\rho\times\hat k),
\qquad
\sigma=\det_{k^\perp}(x,y).
}
\]

DA independently reproduced this to about \(10^{-14}\) relative error.
The vector is tangent to the equal-input circle.

---

## 7. Static Signed Assembly — KILLED as a power source

This branch has been attacked hard.

A single circle cannot provide scale decay: determinant phases can undo
angular dispersion.

The \(2/\pi\) sign adversary survives for the appropriate real/sign
restriction, while complex-phase freedom gives the corresponding
constant obstruction.

More strongly, the corrected SAG-6′ result is

\[
\boxed{\Gamma_{\mathrm{star}}=1}
\]

for an isolated multi-output star. A circular polarization of the
reused \(v_p\) permits full per-triangle saturation simultaneously.

So

\[
\boxed{
\text{mode reuse alone does NOT create depletion}.
}
\]

Current hierarchy:

- triangle \(\to\) no gain
- circle \(\to\) no scale gain
- star \(\to\) \(\Gamma=1\)
- tree \(\to\) baseline \(1\)

All are dead as sources of the missing power.

The only remaining static candidate is closed-loop
polarization / helical incompatibility.

---

## 8. Loop gate — OPEN

Ordinary modal phase topology is not enough.

For \(p+q=k\), the global phase assignment \(\phi_k=\xi\cdot k\)
satisfies

\[
\phi_p+\phi_q-\phi_k=0
\]

on every triad simultaneously. Therefore

\[
\boxed{\text{loops do not automatically force phase frustration}.}
\]

The correct incidence equation is \(B\phi=b\pmod{2\pi}\).
For \(c^TB=0\), true phase frustration requires nonzero holonomy

\[
\boxed{\Omega_c=c^Tb\not\equiv0\pmod{2\pi}.}
\]

After quotienting this gauge freedom, the remaining candidate is
polarization / helical holonomy.

Heavy currently has a loop trend from optimization. Those are
**lower bounds only**.

Until there is a certified upper bound

\[
L_N\le M_N\le U_N,
\]

there is no proved defect.

Even \(\Gamma_{\mathrm{cyc}}\le 0.7\) would not be enough. The prize
is scale decay

\[
\boxed{\Gamma_{\mathrm{cyc}}(N)\lesssim N^{-\delta}.}
\]

**Status: OPEN / certification pending.**

---

## 9. Phase-resolved helical network — EXACT finite algebra

Choose

\[
ik\times h_s(k)=s|k|h_s(k),
\qquad
\widehat u_k=\sum_{s=\pm}a_k^s h_s(k).
\]

For a signed triad channel,

\[
\boxed{
W_{\Delta,\sigma}
=
g_{\Delta,\sigma}
\overline{
a_k^{s_k}a_p^{s_p}a_q^{s_q}
}.
}
\]

The centered contribution is

\[
\boxed{
\mathfrak T_{c,\Delta,\sigma}
=
2C_{\Delta,\sigma}(\Lambda)
\operatorname{Re}W_{\Delta,\sigma}.
}
\]

The full network reconstructs

\[
\boxed{
\mathfrak T_c
=
\sum_{\Delta,\sigma}
\mathcal A_{\Delta,\sigma}
\cos\Psi_{\Delta,\sigma}.
}
\]

The finite implementation matched direct Galerkin sums in tested
176- and 4,272-channel networks. That match is numerical evidence
for the finite algebra, not DA-NS-2.

---

## 10. Phase twins — EXACT counterexample

For one \((++-)\) triad, shifting one modal phase by \(\pi\) leaves

\[
X,Y,Z,\Lambda,\mathcal D_s,\|\nabla u\|_3
\]

unchanged while producing

\[
\boxed{\mathfrak T_c(u)=-0.79707557316},
\qquad
\boxed{\mathfrak T_c(\widetilde u)=+0.79707557316}.
\]

Because the transformation preserves \(|a_k|^2\), it also preserves
every quadratic helicity-weighted intensity of the form

\[
H^\varepsilon
=
\sum_{k,s}
\varepsilon s\,\lambda_k|a_k^s|^2.
\]

Therefore

\[
\boxed{
(X,Y,Z,\Lambda,D_s,H^\varepsilon)
\text{ fixed}
\not\Rightarrow
\operatorname{sign}\mathfrak T_c.
}
\]

Orientation-only payment: **KILLED**. The cubic phase information
cannot be discarded.

---

## 11. Heterochiral charge factorization — EXACT

For heterochiral channel \(\gamma\),

\[
\boxed{\mathfrak T^{\mathrm{het}}_{c,\gamma}=R_{\Lambda,\gamma}Q_{a,\gamma}},
\]

where

\[
\boxed{
R_{\Lambda,\gamma}
=
\frac{(i+o)(j+o)}{2o}
(H_{ij\mid o}-\Lambda)
}
\]

and

\[
H_{ij\mid o}
=
i^2+j^2+o^2+ij-o(i+j).
\]

Near \(i,j,o\approx\kappa=\sqrt{\Lambda}\),

\[
R_{\Lambda,\gamma}=2\kappa^3+O(\kappa^2\delta).
\]

For a connected network,

\[
\boxed{\mathfrak T^{\mathrm{het}}_{c,\Gamma}=2\kappa^3 Q_{a,\Gamma}+\rho_\Gamma}
\]

with

\[
\boxed{
\rho_\Gamma
=
\sum_\gamma
(R_{\Lambda,\gamma}-2\kappa^3)Q_{a,\gamma}.
}
\]

This covariance term is structurally necessary.

---

## 12. Charge-only coercivity — KILLED

The exact rank-three two-triad witness has

\[
Q_{a,1}+Q_{a,2}=0
\]

while

\[
\boxed{\mathfrak T^{\mathrm{het}}_{c,1}+\mathfrak T^{\mathrm{het}}_{c,2}>0}.
\]

Net charge cancellation does not control positive centered drift.

The same example also defeats a static SAG shared-output rescue: it is
already one globally compatible rank-three Fourier field.

---

## 13. Cross-radius signed-helicity ledger — EXACT

For conservative oriented transfers \(\eta_{\gamma,m}\) with
\(\sum_m\eta_{\gamma,m}=0\), and \(f_\lambda(r)=r(r^2-\lambda)\),

\[
\boxed{
T_\gamma
=
f_\lambda(o)Q_\gamma
+
\sum_m f_\lambda(r_m)\eta_{\gamma,m}.
}
\]

Define \(\Pi_\gamma^H(\varrho)=\sum_{r_m>\varrho}\eta_{\gamma,m}\). Then

\[
\boxed{
\sum_m f_\lambda(r_m)\eta_{\gamma,m}
=
\int_0^\infty
(3\varrho^2-\lambda)
\Pi_\gamma^H(\varrho)\,d\varrho.
}
\]

For frozen \(\lambda\), this is the nonlinear derivative of

\[
\boxed{
\Psi_\lambda^\varepsilon(u)
=
\frac12
\sum_{k,s}
\varepsilon s\,|k|^2
(|k|^2-\lambda)
|a_k^s|^2.
}
\]

That is an important surviving exact potential.

---

## 14. Moving-center covariance — EXACT

On epoch \(e\), freeze \(\lambda_e=\kappa_e^2\). Then

\[
\boxed{
\mathfrak T_{c,\Gamma}^{\mathrm{het}}
=
2\kappa_e^3 Q_{a,\Gamma}
+
\rho_{\Gamma,e}^{\mathrm{rad}}
+
\rho_{\Gamma,e}^{\mathrm{mov}}
}
\]

where

\[
\boxed{
\rho_{\Gamma,e}^{\mathrm{rad}}
=
\sum_\gamma
(R_{\lambda_e,\gamma}-2\kappa_e^3)Q_{a,\gamma}
}
\]

and

\[
\boxed{
\rho_{\Gamma,e}^{\mathrm{mov}}
=
-(\Lambda-\lambda_e)\sum_\gamma A_\gamma Q_{a,\gamma}.
}
\]

Define

\[
\boxed{S_\Gamma=\sum_\gamma A_\gamma Q_{a,\gamma}}.
\]

Then

\[
\boxed{\rho_{\Gamma,e}^{\mathrm{mov}}=-(\Lambda-\lambda_e)S_\Gamma}.
\]

---

## 15. Latest derivative identity — EXACT

Because \(\partial_\Lambda R_{\Lambda,\gamma}=-A_\gamma\),
differentiating the heterochiral contribution gives

\[
\boxed{
\dot{\mathfrak T}_{c,\Gamma}^{\mathrm{het}}
=
-\Lambda'S_\Gamma
+
\sum_\gamma R_{\Lambda,\gamma}\dot Q_{a,\gamma}.
}
\]

And since \(\rho^{\mathrm{mov}}=-(\Lambda-\lambda_e)S_\Gamma\),

\[
\boxed{
-\Lambda'S_\Gamma
=
\frac{d}{dt}\rho_{\Gamma,e}^{\mathrm{mov}}
+
(\Lambda-\lambda_e)\dot S_\Gamma.
}
\]

This identifies the residual exactly:

\[
\boxed{(\Lambda-\lambda_e)\dot S_\Gamma}.
\]

Do not pointwise-estimate \(\dot S_\Gamma\); that risks derivative
escalation. It is naturally a variation / Stieltjes problem.

This is the latest algebraic frontier.

---

## 16. Joint Gap–Charge Epoch Budget — OPEN

The required structure is

\[
\boxed{
K_{\theta,n}
\le
-\frac{d}{dt}\mathscr Q_{n,e}
+
g^{\mathrm{rad}}
+
g^{\mathrm{mov}}
+
g^{\mathrm{hom}}
+
g^{\mathrm{cross}}
+
g^{\mathrm{rot/far}}.
}
\]

Dissipation may be spent only once:

\[
\boxed{\sum_\alpha d_{\alpha,n}\le\theta\nu\mathcal D_{s,n}.}
\]

Reset jumps must satisfy a cutoff-uniform ledger.

A bounded charge on each epoch is insufficient.

---

## 17. Reset result — identity sits; increment TRUNCATED

The exact frozen variance identity is

\[
\boxed{W_K=\mathcal D_s+X(\Lambda-K)^2}.
\]

At a chart reset \(K_e\to K_{e+1}\), with the physical state fixed,
the increment \(\Delta W\) was **cut mid-formula** in the source
message. It is **not** completed here.

Do not invent the missing line. Send the rest to reopen §17.

---

## What this ledger does not do

- It does not prove DA-NS-2.
- It does not certify a loop defect.
- It does not restore charge-only coercivity, orientation-only
  payment, or static SAG as a power source.
- It does not splice later numerical S-measurement into the
  frozen endpoint.
- It does not claim Clay Statement B.

**NS not solved.**
