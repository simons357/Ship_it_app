# Signed episode balance: completed diagnostic and exact cost identity

20 September 2026. Status: PARTIAL. An elementary episode-cost identity is derived below. Full-convolution floating-point trajectories diagnose three finite cutoffs. No cutoff-independent budget bound or global regularity claim is made.

This continues the mixed-length time-budget task. It neither reopens an epsilon-incidence route nor asserts that differentiating transfer alone closes the budget. Internal board labels do not replace proof or specialist review.

## Exact objects

Use the existing unforced periodic Galerkin equation, nu=3/2 in the experiment, and full-solution X=||grad u||_2^2 and Y=||Delta u||_2^2. Fix K and let

\[
D= T_{\rm sc}(P_{>K}u)-\nu Y/4,\qquad d=D/X.
\]

All generated modes and low inputs in the full nonlinear convolution remain present. Let

\[
Q_\Sigma=\sum_{abc}Q_{abc,N},\quad
V=-\nu\sum_{abc}(a+b+c)T_{abc},\quad M=-\nu Y'/4.
\]

The exact identities are

\[
D'=Q_\Sigma+V+M,
\qquad
d'=Q_\Sigma/X+V/X+M/X-DX'/X^2.
\tag{1}
\]

V is a signed contribution, not a universally negative function. The signs reported below are observed on the stated trajectories. Q_Sigma is not R4: R4 weights each block by 1/[nu(a+b+c)]. Neither sum can be substituted for the other.

## An exact first-time-moment identity for episode cost

For an episode (a,b) with D(a)=0, D>0 inside and X>0, define

\[
b_I=\int_a^b D(t)/X(t)\,dt.
\]

Since d(t)=integral_a^t d'(s) ds, ordinary integration gives

\[
\boxed{
 b_I=\int_a^b(b-s)\left[
 \frac{Q_\Sigma}{X}+\frac{V}{X}+\frac{M}{X}-\frac{DX'}{X^2}
 \right](s)\,ds.}
\tag{2}
\]

This holds also for an interval truncated before the downward crossing, provided its left endpoint has D(a)=0 and the interval remains positive. If an episode instead starts at initial time with d(a)>0, add (b-a)d(a). For a complete episode d(b)=0 as well, so the integral of d' is zero, but its first time moment need not be zero. Equivalently, for a complete episode b_I=-integral_a^b(s-a)d'(s) ds.

Proof: substitute d(t)=d(a)+integral_a^t d'(s) ds and interchange integrals on the finite triangle a<=s<=t<=b. All functions are smooth for a nonzero finite Galerkin solution. No sign estimate, approximation or phase hypothesis is used. This is elementary bookkeeping, not a novelty claim.

Equation (2) retains cancellation and expresses the measured budget in terms of the four signed derivative contributions. It is not itself a bound. A bound would have to control the sum of these moments over disjoint episodes uniformly in N. Replacing every term by its absolute value can discard the observed cancellation. Episode endpoints and lengths are solution-dependent; they cannot be assumed uniformly controlled while proving their control.

## Experiment

The fixed initial datum is random_field(3, Random(2026092005)), amplitude 1, identical at all cutoffs. K=1 and nu=3/2. E0=680, X0=1486 and Y0=3490. The original comparison covered physical time [0,1]. This diagnostic reintegrates [0,0.15], which contains the complete detected episode at each of the same squared cutoffs 6,12,20. It does not assert anything new about later times.

The evaluator directly sums the ordered Fourier convolution with the Leray projection. The scalene mask requires all three squared radii >1 and pairwise distinct. All nonlinear inputs remain unrestricted within the Galerkin cutoff.

At each downward crossing, the signed terms in D' are:

| N² | End time | Q_Sigma | V | M=-nu Y'/4 | D' |
|---|---:|---:|---:|---:|---:|
| 6 | 0.0419374823 | +8119.676 | -21339.114 | -4100.331 | -17319.769 |
| 12 | 0.0813154787 | -1070.445 | -43860.301 | +9921.717 | -35009.029 |
| 20 | 0.0921538509 | +14766.510 | -59715.562 | +16486.054 | -28462.997 |

Interpretation:

- At N²=6, quartic feeding is still positive at exit. Block viscosity and a rising threshold outweigh it.
- At N²=12, quartic feeding is slightly negative and block viscosity is negative. Y is falling, so the moving threshold opposes exit.
- At N²=20, both quartic feeding and threshold motion promote D, yet the negative block-viscous term outweighs them.

Thus these exits do not require Q_Sigma to become negative. A universally rising threshold does not explain them either. All three show a negative block-viscous term large enough at the exit to contribute decisively to D'<0. This is a measured balance, not a causal intervention or a proof that viscosity must win on all orbits.

At each crossing D=0, so the normalization contribution -DX'/X² vanishes. It matters inside the episode.

## Integrated normalized contributions

The entries below are the four weighted integrals on the right of (2), not raw time integrals and not bounds on their absolute values.

| N² | Quartic moment | Viscous moment | Threshold moment | Normalization moment | Episode cost |
|---|---:|---:|---:|---:|---:|
| 6 | +0.006269796 | -0.003868633 | -0.001115553 | +0.000052216 | 0.001337826 |
| 12 | +0.166128346 | -0.101043064 | -0.023399325 | +0.005232669 | 0.046918626 |
| 20 | +0.296255879 | -0.195921260 | -0.037661696 | +0.009926974 | 0.072599898 |

The threshold moment is negative over each episode even though its instantaneous contribution is positive at the last two exits. Endpoint signs alone therefore do not describe the integrated balance. Normalization adds to the budget in all three integrated results.

These are signed moments relative to the final time b, so their interpretation is specific to (2). They are not a unique causal allocation of budget among physical mechanisms.

The improved N²=6 cost is 0.00133782564. It differs by about 1.9e-8 from the earlier auxiliary-ODE budget 0.00133784455. That earlier discrepancy lies within its stated 1e-7 episode-budget consistency check. The present smooth quadrature between computed roots is more accurate for this experiment; the earlier table's final digits should not be treated as exact.

## Verification and limits

Baseline DOP853 tolerances are rtol=1e-10, atol=1e-12 and max_step=0.002. The N²=20 run is repeated at rtol=1e-12, atol=1e-14 and max_step=0.001. Smooth Gauss-Legendre quadrature uses both 32 and 64 points on each episode.

Checks compare:

1. The derivative of the scalene polynomial in the full vector-field direction with Q_Sigma+V.
2. Explicit three-slot differentiation with the independent cubic coefficient extraction [8(f(eps)-f(-eps))-(f(2eps)-f(-2eps))]/(12 eps), eps=1e-4. This expression is algebraically exact for a cubic; evaluation here is floating-point.
3. The direct positive-episode integral with the signed first-time-moment identity (2).
4. The time integral of Q_Sigma+V+M with the zero endpoint difference D(b)-D(a).
5. Crossings with the earlier fixed-data experiment and the tighter repeat.

The computation is not interval-certified and cannot exclude arbitrarily short missed episodes. A handful of cutoffs cannot establish a uniform limit. Neither a growing finite budget sequence nor failure of a proposed sufficient estimate would by itself prove singularity.

## What this makes precise next

The observed mechanism to investigate is a time-integrated deficit of nonlinear feeding relative to the full dissipative and threshold balance. A sign claim Q<=0 would be unnecessarily strong and fails at two observed exits. An exit condition such as D'(b)<0 explains a particular crossing but does not establish when or whether one must occur.

A successful continuation theorem must control the sum of (2) over all positive episodes, including any final truncated episode and any initial positive term. It needs an independently bounded resource or functional; substituting d' back from d and calling that a bound would be circular. The signed moments are now explicit diagnostics for a candidate theorem. No uniform bound on them has been proved here.

The next analytic candidate should target their combined effect, preserve full input forcing and account for repetition. R4/X remains an alternative exact bookkeeping device with its own normalization and variation terms; this computation does not bound it or silently replace it.

Reproduce with Python, NumPy and SciPy:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 ns_episode_balance.py
```

The package includes the exact-initial-data helper and the resulting JSON. Repeated-radius, fixed-low and epsilon-route statuses are unchanged. No external messages or public claims were sent.

Completed refinement differences: {"budget_difference": 9.43689570931383e-16, "start_difference": 2.130240428499519e-15, "end_difference": 4.0245584642661925e-16, "max_budget_moment_difference": 1.7319479184152442e-14}. These measure numerical agreement, not certified error bounds.
