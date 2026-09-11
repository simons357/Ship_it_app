# SuperGrok cube family — scored against the lock

11 September 2026. Screenshot dump, then
this book’s evaluator.
**★ OPEN. NS not solved.
Do not start H1. Do not stamp a kill.
Do not rewrite the boxed claim.**

Statement: [`LEMMA-STAR-STATEMENT.md`](LEMMA-STAR-STATEMENT.md).
Identities: [`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Core: [`LEMMA-STAR-CORE.md`](LEMMA-STAR-CORE.md).
Family-check paste (no family):
[`LEMMA-STAR-FAMILY-CHECK.md`](LEMMA-STAR-FAMILY-CHECK.md).

Probe: `python3 scripts/lemma_star_cube_family.py --nmax 3`

Analytic-review score (files absent;
quadratic moments sit; \(M_0\) not locked):
[`LEMMA-STAR-CUBE-REVIEW.md`](LEMMA-STAR-CUBE-REVIEW.md).

The dump named a family. This branch
did not have it. It does now.
Screenshots are not a stamp.

---

## The named field

Integer modes, cube \(|k_j|\le n\):

\[
\widehat{v}_n(k)
=
\frac{k_1(-k_1^2+in k_2)}{n^7}\,(-k_2,k_1,0).
\]

Equivalent profile \(n^{-3}F(k/n)\).
Support grows with \(n\).
This is **not** Fourier dilation \(v(n\cdot)\).
The dilation invariant does not apply.

On paper: mean-zero, \(k\cdot\widehat{v}=0\),
\(v_{-k}=\overline{v_k}\). The lock confirmed
that on \(n=1,\dots,6\).
Admissible \(\neq\) Hadamard well-posedness
of NSE \(\neq\) \(\sup\mathcal R_\star<\infty\).

---

## What SuperGrok stamped

Unrestricted \(\sup\mathcal R_\star<\infty\)
is **false**. Claimed continuum scaling

\[
n^3 E_n=E_0+O(n^{-1}),\quad
Y_n/n=Y_0+O(n^{-1}),\quad
\mathcal D_{s,n}/n^3=D_0+O(n^{-1}),\quad
T_{c,n}/n^2=M_0+O(n^{-1}),
\]

hence \(\mathcal R_\star(v_n)=c_{\mathrm{box}}n^3+O(n^2)\)
with a positive \(c_{\mathrm{box}}\).
Quoted \(n=2\): \(T_c>0\),
\(\mathcal R_\star\approx 8.06\times 10^{-7}\).

They also wrote that the degree-52
Bernstein certificate for every
\(n\ge 2\) was **not** regenerated,
and that the analytic step still
needed review. Then they changed
the working-file status anyway.

Cited files
(`Lemma_Star_Finite_Lattice_Proof.md`,
`lemmma_star_counterexample.pdf`)
are **not** on this branch.
Commit `1b4b633` here is Lemma PC,
not a cube proof. `98eaad4` is not
on this branch. Do not merge the
sibling book.

---

## Locked numbers

Same \(\mathcal D_s\), \(T_c\), \(\mathcal R_\star\)
as the core. Reverse required. \(N=\sum\lambda T_k\).

| \(n\) | modes | \(T_c\) | \(\mathcal R_\star\) | \(\mathcal R_\star/n^3\) | \(n^3 E\) | \(Y/n\) | \(\mathcal D_s/n^3\) | \(T_c/n^2\) |
|---|---|---|---|---|---|---|---|---|
| 1 | 18 | \(0\) | \(0\) | \(0\) | \(54\) | \(370\) | \(34.0\) | \(0\) |
| 2 | 100 | \(4959/32768\) | \(8.062\times 10^{-7}\) | \(1.008\times 10^{-7}\) | \(16.09\) | \(82.7\) | \(10.67\) | \(0.0378\) |
| 3 | 294 | \(0.1370\) | \(2.858\times 10^{-6}\) | \(1.059\times 10^{-7}\) | \(9.43\) | \(41.8\) | \(5.54\) | \(0.0152\) |
| 4 | 648 | \(0.1240\) | \(5.255\times 10^{-6}\) | \(8.211\times 10^{-8}\) | \(6.97\) | \(28.2\) | \(3.72\) | \(0.00775\) |
| 5 | 1210 | \(0.1243\) | \(8.675\times 10^{-6}\) | \(6.940\times 10^{-8}\) | \(5.74\) | \(21.8\) | \(2.85\) | \(0.00497\) |
| 6 | 2028 | \(0.1314\) | \(1.342\times 10^{-5}\) | \(6.212\times 10^{-8}\) | \(5.01\) | \(18.2\) | \(2.35\) | \(0.00365\) |
| 7 | 3150 | \(0.1424\) | \(1.974\times 10^{-5}\) | \(5.754\times 10^{-8}\) | \(4.53\) | \(15.9\) | \(2.04\) | \(0.00291\) |

\(N=0\) on these samples (noise at \(10^{-17}\)
for odd \(n\)).
Two \(\mathcal D_s\) formulas agree.
\(\mathcal R_\star(av)=\mathcal R_\star(v)\).
\(T_c(-v)=-T_c(v)\); the positive sign is \(+v\).

\(n=2\) \(\mathcal R_\star\) matches the dump.
Their \(T_c=49509/32768\) is a digit slip:
the lock is \(4959/32768\).

The old dump fraction equals
\(3.967\times 10^{-10}\).
The review float
\(3.967267736160021\times 10^{-8}\)
is \(M_0^2/(D_0 E_0 Y_0)\) after the
quadratic moments of \(F\) are
corrected. See
[`LEMMA-STAR-CUBE-REVIEW.md`](LEMMA-STAR-CUBE-REVIEW.md).
Discrete \(\mathcal R_\star/n^3\) at
\(n=7\) is still \(5.75\times 10^{-8}\).

---

## Keep

- Check locked \(\mathcal D_s\), \(T_c\),
  \(\mathcal R_\star\) before a kill stamp.
- Growing cube \(\neq\) \(v(n\cdot)\).
- \(A=-P\Delta\) and \(A=-\Delta\) agree
  on divergence-free fields. Already locked.
- Four corrections do not save a genuine
  \(\mathcal R_\star\to\infty\).
- ★ \(\Rightarrow\) GR in this packaging,
  one way. No converse.
- This is not an NSE trajectory, not H1,
  not Cauchy–Schwarz, not a Clay close.
- One large **finite** sample only raises
  \(C_{\mathrm{geom}}\).
- Bernstein for every \(n\ge 2\) was not
  regenerated. Do not claim it.

---

## Correct

**“Unrestricted ★ is false.”**
The lock has finite \(\mathcal R_\star\)
on \(n\le 7\), largest
\(1.97\times 10^{-5}\).
Kill is \(\mathcal R_\star(v_n)\to\infty\).
A short increasing list at \(10^{-6}\)
is a clue, not that limit.
N-shell still sits at \(0.610\).

**Riemann-sum limit already proves
unboundedness.**
\(n^3 E\), \(Y/n\), \(\mathcal D_s/n^3\),
and \(T_c/n^2\) are still falling
through \(n=7\).
\(\mathcal R_\star/n^3\) at \(n=7\) is
\(5.75\times 10^{-8}\).
\(T_c/n^2\) is still \(4.4\times\) the
claimed \(M_0\).
No settled leading term on this branch.

**Change the working-file status line.**
Not on this book. The boxed claim stays
the unrestricted statement. Restricted
replacements — finite-shell support,
NSE trajectories only, or
\(C_{\mathrm{geom}}\) allowed to grow
with \(\Lambda\) / shell width / \(Z/Y\) —
are new lemmas. Write them only after
the operator asks, and only after a
real kill or a real bound.

**Merge the sibling / PDF / zip.**
No. Score here. Compute here.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| LScube_named | **pass** | family is on this branch |
| LScube_lock_first | **pass** | identities before a stamp |
| LScube_div_real | **pass** | setup sits |
| LScube_amp_odd | **pass** | amplitude flat; \(T_c\) odd |
| LScube_screenshot_stamp | **fail** | screenshots are not the lock |
| LScube_bernstein_every_n | **fail** | every-\(n\ge 2\) certificate absent |
| LScube_ns_solved | **fail** | not NSE; not H1 |
| LScube_unrestricted_killed | **fail** | unrestricted ★ is OPEN |

★ stays OPEN. Kill lane stays LIVE.
The cube is the first named family
here whose support grows.
It has not diverged on the lock.

Do not start H1.
Do not stop patching.
Do not glue Q-stack.

NS not solved.
