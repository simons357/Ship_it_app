# Named orbit R4 hypothesis and a small Fourier-l1 data case

Date: 20 September 2026. Working mathematical derivation; independent specialist review pending. No novelty claim. Scope: classical unforced mean-zero periodic Navier–Stokes, normalized so nonzero Fourier wavevectors have length at least one. No modification of the equation.

## 1. Exact hypotheses

Fix real, mean-zero, divergence-free smooth data u0 on the normalized torus, viscosity nu>0, eta in (0,1), and a finite cutoff K chosen independently of N and time. Let u_N solve the full Galerkin equation with initial data P_N u0. Set X=||grad u_N||_2², Y=||Delta u_N||_2². Use the existing signed all-high scalene correction H and fully differentiated quartic R4; H'=-Tsc+R4. Set F=X+2H and C=T-Tsc. All nonlinear input sums remain full Galerkin sums.

H_R4(T):

sup_N integral_0^T [R4-(1-eta)nu Y]_+/X dt <= G_T(u0,nu,K,eta)<infinity.

The quotient is defined as zero for identically zero trajectories. Equivalently, there are measurable nonnegative g_N with R4 <= (1-eta)nu Y+g_N X and sup_N integral g_N<=G_T. The least choice is precisely the displayed positive quotient. G_T may depend on the full fixed datum, but never on N. The general program asks this for every finite T. No boundedness of X is assumed as an input.

H_F(T): there exists c0>0 independent of N,t such that F_N(t)>=c0 X_N(t) for all t in [0,T], with M0=sup_N F_N(0)<infinity.

## 2. Conditional lemma

Assume H_R4(T), H_F(T), and the retained complement bound |C|<=eta nu Y+f_K X with f_K>=0 and sup_N integral_0^T f_K<=L_K(T). Then

sup_N sup_(0<=t<=T) X_N(t) <= (M0/c0) exp[2(L_K(T)+G_T)/c0].

Proof: F'=2R4+2C-2nu Y <=2(f_K+g_N)X <=2(f_K+g_N)F/c0. Apply the scalar integrating factor and then X<=F/c0. This is a conditional enstrophy estimate, not an estimate of the original positive-part S budget.

For the retained f_K=3 C_K sqrt(E)+3X/(16 eta nu), energy and Poincare give

L_K(T) <= 3 C_K sqrt(E0)(1-exp(-nu T))/nu +3E0/(32 eta nu²).

The weaker T bound for the first term also holds. The retained complement estimates keep their existing review status.

## 3. A nontrivial restricted theorem

Define U0=sum_(k!=0) |uhat0(k)|, using Euclidean magnitude of each complex vector. Suppose U0<=nu/4. Then for every N, every fixed K>=0 and all finite T:

F_N(t)>= (1-2U0/nu) X_N(t)>=X_N(t)/2,

sup_N integral_0^T [R4-(1-eta)nu Y]_+/X dt <= 2U0²/[nu(nu-U0)],

sup_N F_N(0)<= (1+2U0/nu) X0.

Thus both named hypotheses hold on this explicit small-data class, including data with nonzero nonlinear interactions. This is a sufficient smallness condition, not a necessary condition and not progress to arbitrary-amplitude regularity by itself.

## 4. Proof: orbit control in Fourier l1

Along a Galerkin trajectory put

U=sum |uhat(k)|, V=sum |k| |uhat(k)|, W=sum |k|² |uhat(k)|.

All sums are over retained nonzero frequencies. Leray projection has operator norm one. With R=-P_N B(u,u), convolution and |ell+m|<=|ell|+|m| give

||Rhat||_l1 <= U V,

sum |k| |Rhat(k)| <= V²+U W <=2U W,

||Rhat||_l2 <= U sqrt(X).

The middle inequality uses Cauchy–Schwarz V²<=UW. The Galerkin projection only removes terms from these upper bounds. Since |k|>=1, V<=W. The mode-amplitude differential inequality, summed over modes, is valid almost everywhere (or in the integrated absolute-continuous sense):

U'+nu W<=UV<=UW.

Starting with U(0)<=U0<nu, the scalar barrier gives U(t)<=U0. Hence

U'+(nu-U0)W<=0,

integral_0^T U W dt <= U0²/[2(nu-U0)].

The last bound follows by multiplying by U and integrating. These estimates are obtained from the dynamics; no a priori enstrophy bound or regularity criterion is assumed.

## 5. Proof: exact-mask cubic and quartic estimates

Write H in its original ordered Fourier-transfer form. Each retained ordered monomial has coefficient

c/[nu(a+b+c)] times Im[(q dot uhat(p))(uhat(q) dot conjugate(uhat(k)))], k=p+q,

where a=|p|², b=|q|², c=|k|², all three radii are distinct and exceed K². Summing these ordered monomials equals the signed block definition of H. In particular 0<=c/(a+b+c)<=1, and the fixed mask does not generate derivative terms.

The absolute ordered sum is bounded by

|H| <= (1/nu) sum_(p+q=k) |q| |uhat(p)| |uhat(q)| |uhat(k)|
     <= U sqrt(X E)/nu <= U X/nu.

Here discrete Young/Cauchy–Schwarz is applied with the p slot in l1, the q slot in weighted l2 and the k slot in l2; E<=X by the normalization. It follows directly that

(1-2U/nu)X<=F<=(1+2U/nu)X.

For R4, differentiate each of the three slots using the full R. Keep the same exact multiplier and mask. Let R1=sum |k| |Rhat(k)|. For the two terms where R replaces the p or k slot, put the q slot in weighted l1 and the remaining slots in l2. For the term where R replaces the q slot, put that slot in weighted l1. This yields

|R4| <= [2 ||Rhat||_l2 sqrt(E) V + E R1]/nu
      <= [2 U V X+2 U W X]/nu
      <= (4/nu) U W X.

This estimate is NOT a claim that the previously sought unrestricted energy-only majorant holds. Its right side involves the additional Fourier-l1 quantities U,W. They become usable only through the small-data orbit inequality proved above.

Since the viscous threshold is nonnegative,

[R4-(1-eta)nu Y]_+/X <= |R4|/X <=4 U W/nu.

Integrating proves G_T<=2U0²/[nu(nu-U0)] uniformly in N and T. Dropping the threshold here makes the proved small-data estimate stronger; it does not alter the definition of the general target.

The H bound supplies c0=1-2U0/nu and M0<=(1+2U0/nu)X0. This completes the restricted theorem.

## 6. Nonlinearity is not excluded

For example, set p=(2,0,0), q=(0,4,0), k=p+q, and coefficients uhat(p)=i a e2, uhat(q)=uhat(k)=i a e3, with Hermitian negatives. Then U0=6|a|, so |a|<=nu/24 is in the class. The retained ordered transfer is nonzero when a!=0 (T=32a³). Thus the theorem is not confined to R=0 heat/shear solutions. Although this example starts with finite support, the proof retains all modes generated by the full Galerkin equation.

## 7. Precise status and remaining gap

PROVED IN THE WORKING DERIVATION: the conditional lemma and the explicitly small Fourier-l1 data case. Neither proof uses the equal-shell lemma or requires a new complement estimate. These are restricted sufficient estimates, not a novelty claim or independent-review stamp.

OPEN: H_R4 for arbitrary fixed smooth data; a sufficient coercivity propagation mechanism for those large data; the original S budget. When U is not below nu, U'+(nu-U)W<=0 has no useful dissipative sign. Therefore the small-data proof cannot simply be extended by dropping its hypothesis.

The earlier outward-boundary witness is compatible with this theorem: it does not satisfy U0<=nu/4. Single finite N boundedness or finite cutoff experiments would not establish the general uniform-N hypothesis.

Overall general-data attack: PARTIAL. Restricted small-data theorem: PROVED (derivation above; specialist review pending). Enstrophy route is not silently identified with an S proof.
