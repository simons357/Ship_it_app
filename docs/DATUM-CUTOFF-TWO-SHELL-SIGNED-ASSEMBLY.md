# Datum cutoff and two-shell signed assembly

6 October 2026. Classical mean-zero NSE on the normalized 2π torus.

This write supplies an explicit initial-tail cutoff, an exact complete two-sphere signed assembly, a cutoff-independent spatial bound on its already assembled equal-input channels, and an exact regeneration test. It does not supply the all-high scalene time budget (17). Exact spheres below mean |k|²=a, not thick dyadic annuli.

## 1. Choose K from the datum, before estimating evolution

Let A=-PΔ, B(v,w)=P[(v·∇)w], and

\[
 E=\|u\|_2^2,\quad X=\|A^{1/2}u\|_2^2,\quad
 Y=\|Au\|_2^2.
\]

Fix a homogeneous mean-zero torus Sobolev constant C₀ with
\(\|f\|_3\le C_0\|A^{1/4}f\|_2\).
Let C_S be the source's L3-1 constant and c=1/(8C_S). Define

\[
 \sigma_K(u_0)^2=\sum_{|k|>K}|k|\,|\widehat u_0(k)|^2,
 \qquad
 \boxed{K(u_0,\nu)=\min\{n\in\mathbb N:n\ge1,
 C_0\sigma_n(u_0)\le c\nu/2\}.}
\]

This is finite for each H¹ datum, hence for the smooth data in (17). It uses the actual datum's tail. An explicit, less economical sufficient choice is

\[
 K\ge\max\left\{1,\frac{4C_0^2 X(u_0)}{c^2\nu^2}\right\},
\]

rounded up to an integer, since σ_K²≤X(u₀)/K. No future X occurs. For every Galerkin cutoff N,

\[
 \|P_{>K}P_Nu_0\|_3\le C_0\sigma_K(u_0)\le c\nu/2.
\]

The order of quantifiers is fixed datum and viscosity → fixed K → all N and time horizons. This choice proves only initial-tail smallness, not that this particular K satisfies (17).

For the actual Galerkin evolution, exactly

\[
 h_{K,N}(t)=e^{-\nu tA}P_{>K}P_Nu_0
 -\int_0^t e^{-\nu(t-s)A}P_{>K}P_NB(u_N,u_N)(s)\,ds.
\]

Heat contraction in L³ keeps the first term at most cν/2. Thus any later excess beyond cν is caused by the forced regeneration term. The identity does not bound its accumulated size. In particular, a small or zero tail at t=0 is not a persistence theorem.

The source's L3-4 is used only in its valid direction: a fixed-datum L3-5 bound implies (17), with the controlled additive term. The converse is not established.

## 2. Assemble the whole two-sphere signed transfer first

Suppose at the time being tested

\[
 u=v+w,\qquad Av=av,\quad Aw=bw,\quad 0<a<b,
 \qquad e_a=\|v\|_2^2,\quad e_b=\|w\|_2^2.
\]

Real L² pairings are understood. Define the two already summed signed channels

\[
 j_{b\leftarrow aa}=-\langle B(v,v),w\rangle,
 \qquad j_{a\leftarrow bb}=-\langle B(w,w),v\rangle.
\]

The total kinetic transfer into the b-sphere is

\[
 \boxed{J=j_{b\leftarrow aa}-j_{a\leftarrow bb}.}
\]

Proof: expand \(-\langle B(u,u),w\rangle\). The terms
\(\langle B(v,w),w\rangle\) and \(\langle B(w,w),w\rangle\) vanish. Skew symmetry gives
\(\langle B(w,v),w\rangle=-\langle B(w,w),v\rangle\).
Energy conservation then makes the total a-sphere transfer -J. Consequently the full signed enstrophy transfer is

\[
 \boxed{\mathcal T(u)=(b-a)
 \bigl(j_{b\leftarrow aa}-j_{a\leftarrow bb}\bigr).}
 \tag{TS}
\]

This combines all receivers, ordered input pairs, and negative Fourier modes. It never replaces a phase product by |B̂_k|. In particular the mixed-input donors are included; they are not an additional uncontrolled block.

The centered quantity is also an exact complete sum:

\[
 \boxed{\mathcal T_c=(b-a)(a+b-\Lambda)J,\qquad
 \Lambda=Y/X.}
\]

Writing X=ae_a+be_b gives the more explicit identities

\[
 a+b-\Lambda=\frac{ab(e_a+e_b)}X,
 \qquad
 \mathcal D_s=\frac{ab e_a e_b(b-a)^2}{X}.
\]

Thus the gap is retained before any comparison is formed. These identities concern the centered route; they are not substituted for (17).

For one exact sphere, \(\mathcal T=\mathcal T_c=0\) directly from energy conservation. B(u,u) itself need not vanish and can generate other spheres.

## 3. A spatial bound after signed channel assembly

Here is the exact-sphere estimate in the order demanded by the signed gate. It reproduces the source's scoped sphere-incidence mechanism; it is not a new estimate on all-high scalene triads.

For input radius squared α and output radius squared β, put

\[
 g_{\alpha\beta}=\sqrt{\beta(1-\beta/(4\alpha))}
 \quad(0<\beta<4\alpha).
\]

The equal-input transverse identity gives, in each pair's real unit normal e₂,

\[
 S_{pq}=g_{\alpha\beta}
 (A_{1,p}A_{2,q}+A_{2,p}A_{1,q})e_{2,pq}.
\]

Define the complete complex vector sum at each output

\[
 V_k=\sum_{\substack{p+q=k\\|p|^2=|q|^2=\alpha}}
 (A_{1,p}A_{2,q}+A_{2,p}A_{1,q})e_{2,pq}.
\]

The full signed channel is assembled as

\[
 j_{\beta\leftarrow\alpha\alpha}
 =\frac{g_{\alpha\beta}}2\operatorname{Im}
 \sum_{|k|^2=\beta}V_k\cdot\overline{u_k}.
 \tag{SC}
\]

Only now apply global Cauchy–Schwarz to this summed scalar:

\[
 |j_{\beta\leftarrow\alpha\alpha}|^2
 \le\frac{g_{\alpha\beta}^2}{4}
 e_\beta\sum_{|k|^2=\beta}|V_k|^2.
\]

The factor 1/2 is the ordered symmetrization factor. The quantity |V_k|² is the square of the assembled vector sum, not a sum of separate signed receiver estimates.

For completeness, the following incidence argument bounds this quadratic expression without a fiber-occupancy factor. Set r_p=|u_p| and F=Σr_p²=e_α. Each pair coefficient has magnitude at most r_pr_q, by the two-component polarization Cauchy–Schwarz inequality. Expanding Σ|V_k|², its diagonal p=p′ contributes at most F². For p≠p′, write q=k-p, q′=k-p′. The fourfold product obeys

\[
 r_pr_qr_{p'}r_{q'}\le
 \tfrac12(r_p^2r_{p'}^2+r_q^2r_{q'}^2).
\]

At fixed distinct nonantipodal p,p′, admissible k obey |k|²=β and k·p=k·p′=β/2. Two independent planes intersect a sphere in at most two points. Antipodal p′=-p would require β=0 and is excluded. Interchanging (p,p′) with (q,q′) gives the same bound on the other half. The entire off-diagonal contribution is therefore at most 2F². Hence

\[
 \sum_{|k|^2=\beta}|V_k|^2\le3 e_\alpha^2,
 \qquad
 \boxed{|j_{\beta\leftarrow\alpha\alpha}|
 \le\frac{\sqrt3}{2}g_{\alpha\beta}e_\alpha\sqrt{e_\beta}.}
 \tag{SB}
\]

At β=4α the channel is exactly zero by incompressibility, rather than by a limiting estimate. For β>4α it is absent by the triangle inequality. The zero output is absent for mean-zero velocity.

Combining (TS) with these already assembled channel bounds yields

\[
 |\mathcal T(u)|\le\frac{\sqrt3}{2}(b-a)
 \left[g_{ab}e_a\sqrt{e_b}+g_{ba}e_b\sqrt{e_a}\right],
 \tag{TB}
\]

where g_ab is set to zero for b≥4a. The flat cancellation kills the aa→b channel at b=4a; it does not kill the distinct bb→a channel. Reversing u to -u preserves e_a,e_b and reverses J and T. No sign of J follows from shell placement alone.

This proves a spatial, occupancy-independent two-exact-sphere bound after signed assembly. Its final norm majorant is not proposed as an integrable remainder for (17): it can be positive on a zero-transfer shear. The quantities used for the actual signed test remain J and T themselves, which vanish when B(u,u)=0. No claim is made that this proves the separately normalized Need★ object without its precise normalization, or that it changes that ledger entry. In particular a bound on exact spheres is not a bound on two broad dyadic annuli.

## 4. Exact two-sphere regeneration test

Use the following three positive/selected Fourier modes, with the negative coefficients defined by conjugation:

\[
 \widehat u(1,0,0)=(0,1,1),\quad
 \widehat u(0,1,0)=(1,0,1),\quad
 \widehat u(-1,-1,0)=i(1,-1,1).
\]

All coefficients are divergence-free. The squared radii are 1 and 2. Including both Fourier signs, exact rational arithmetic gives

\[
 E=14,\quad X=20,\quad Y=32,
 \qquad J=4,\quad\mathcal T=4.
\]

Each of the four radius-1 modes has kinetic transfer -1; each of the two radius-2 modes has transfer +2. Their energy sum is zero. The enstrophy sum is -4+8=4. The centered quantities are T_c=28/5 and D_s=24/5.

Initially T_sc(u₀)=0, because only two exact radii occur. But

\[
 \widehat B(u_0,u_0)(2,1,0)
 =\left(\frac15,-\frac25,2\right)\ne0.
\]

Indeed the unprojected symmetrized ordered contribution is (1,0,2); projection perpendicular to (2,1,0) gives the displayed result. This mode is initially absent. Its exact initial NSE derivative is the negative of this vector; the viscous term is zero there initially. The same result holds for a Galerkin cutoff admitting |k|²=5.

Summing every generated mode and every scalene receiver, the exact first variation is

\[
 \boxed{\left.\frac d{dt}\mathcal T_{\rm sc}(u(t))\right|_{t=0}=28.}
\]

The proof is finite algebra: differentiate the complete cubic signed sum, inserting u′(0)=-B(u₀,u₀)-νAu₀ once in each of the three coefficient positions. The viscous insertions vanish in this scalene first variation since their support still has only radii 1 and 2. The supplied code evaluates the finite sum with Gaussian rational numbers and independently recovers its linear coefficient from the exact cubic polynomial. Thus the derivative 28 is independent of viscosity. For the local smooth NSE solution, T_sc(u(t))=28t+O(t²).

K=2 is an admissible initial-tail choice for this datum, for every ν: h₂(0)=0. Nonetheless the radius-5 mode lies above K and is generated immediately. This directly separates initial-tail placement from regeneration.

Important scope: the derivative 28 is the full-field scalene transfer. It is not T_sc(h₂). The newly generated high modes initially have only squared radius 5, and the old radii 1 and 2 are below K. This calculation therefore does not establish a positive all-high episode or a failure of (17). It rules out inferring persistence of a zero tail or a two-sphere support class from initial spectral placement.

## 5. Filters and outcome

The exact checks also cover a multicarrier shear u=(f(y),0,g(y)): every q·u_p is zero, B=0, and both signed transfers are zero, regardless of carrier frequency or occupancy. The datum cutoff removes its initial tail; heat produces no new modes. An exact one-sphere cyclic field has signed T=0 even though B is nonzero. Sign reversal sends the two-sphere example's T=4 to -4.

No time-budget estimate is inferred from (TB). Using its positive mass majorant as the budget would fail the shear filter. The single-sphere signed cancellation also means that high carrier frequency alone incurs no scalene charge. These are filters on a proposed future integrand, not assertions that one-sphere support persists.

The cheap two-sphere test therefore survives as a spatial signed estimate; its support class fails to persist. Neither outcome settles the all-high Gate 2. In particular, failure of some proposed generic two-shell majorant would not by itself refute the specifically scalene criterion (17), whose scalar integrand is zero on every two-exact-sphere snapshot. A failure would have to reach its actual three-distinct-radius signed sum or its dynamical budget.

The next unresolved quantity remains

\[
 \sup_N\int_0^T
 \frac{[\mathcal T_{\rm sc}(P_{>K}u_N)-\nu Y_N/4]_+}{X_N}\,dt,
\]

with the datum-selected K fixed. Initial-tail smallness is written above. The assembly of each two-sphere block is written above. What remains is control of the regenerated all-high three-radius blocks, including their repetition. The Duhamel forcing term is the precise place this task enters; the snapshot norm bound supplies no such estimate.

## Sources and reproducibility

Source normalization checked against PR #153 head ce8b1ee585aa89be77fa41f7a69748cb2a82da5a:

- [FOURIER-TRIANGLE.md](https://github.com/simons357/Ship_it_app/blob/ce8b1ee585aa89be77fa41f7a69748cb2a82da5a/docs/FOURIER-TRIANGLE.md), especially (6), (8)–(9), and (15)–(17).
- [SIGNED-ASSEMBLY-GATE.md](https://github.com/simons357/Ship_it_app/blob/ce8b1ee585aa89be77fa41f7a69748cb2a82da5a/docs/SIGNED-ASSEMBLY-GATE.md).
- [L3-BUDGET-GATES.md](https://github.com/simons357/Ship_it_app/blob/ce8b1ee585aa89be77fa41f7a69748cb2a82da5a/docs/L3-BUDGET-GATES.md). Its wording suggesting equivalence is not adopted; only L3-5 ⇒ (17) is used.

Run `python3 two_shell_regeneration_checks.py` beside `c10_full_local_exact_checks.py`. The latter provides reusable arithmetic definitions only; its earlier checks are not executed by this script. Output: TWO-SHELL-REGENERATION-CHECKS.json. All Fourier computations are exact fractions, not a numerical evolution or a class-estimate certificate. The general spatial claim rests on the proof in sections 2–3.

Vault copies: `scripts/ns_attacks/two_shell_regeneration_checks.py` and
`scripts/ns_attacks/c10_full_local_exact_checks.py`. Run them from that
directory. Committed JSON: `TWO-SHELL-REGENERATION-CHECKS.json`.
