# P2 torus algebra and MIN-CYCLE

**28 September 2026.**
Accepted corrections to the P2 / TREE / LOOP statement.
Not a Navier–Stokes close. Not a Gate-C theorem.
Scale-rate remains **OPEN**.

Code:
`scripts/ns_attacks/torus_p2.py`,
`scripts/ns_attacks/integer_snf.py`,
`scripts/ns_attacks/one_cycle_loss.py`,
`scripts/ns_attacks/na2b_assembly.py`,
`scripts/ns_attacks/min_cycle.py`.

```bash
PYTHONPATH=scripts python3 -m unittest \
  tests.test_torus_p2 \
  tests.test_one_cycle_loss \
  tests.test_min_cycle -v
PYTHONPATH=scripts python3 scripts/run_p2_torus_min_cycle.py
```

Parent NS instantiation (topology is not frustration):
the LOOP-GAUGE packet on `cursor/holonomy-and-capacity-ca8e`
uses the same left-kernel test with incidence matrix \(B\)
in place of \(M\). This page is the algebraic lock; that
page is one NS family.

Unaugmented NS on \(\mathbb{T}^3\) is **not solved**.
DA-NS-2 stays **OPEN**. Unrestricted \(\star\) stays **KILLED**.

---

## Research ladder

\[
\boxed{\text{Torus lemma — standard / proved}}
\]

\[
\boxed{\text{Finite P2 compatibility — exact integer algebra}}
\]

\[
\boxed{\text{One-cycle loss law — directly testable}}
\]

\[
\boxed{\text{MIN-CYCLE — canonical-input gated}}
\]

\[
\boxed{\text{Scale-rate defect — OPEN}}
\]

TREE/LOOP are shorthand only. The definitions are algebraic.
Pictures of triangles are not an acceptance record.

---

## 1. Torus lemma (standard, not Gate-C)

Let \(M\in\mathbb{Z}^{m\times n}\) and

\[
T_M:\mathbb{T}^n\to\mathbb{T}^m,\qquad
\theta\mapsto M\theta,
\]

with \(\mathbb{T}^k=\mathbb{R}^k/2\pi\mathbb{Z}^k\). Then

\[
\boxed{
b\in\operatorname{im}T_M
\iff
c^Tb\equiv 0\pmod{2\pi}
\quad
\forall\,c\in\ker_{\mathbb{Z}}(M^T).
}
\]

Pontryagin duality is the clean proof: the annihilator of
\(\operatorname{im} T_M\) is \(\ker_{\mathbb{Z}} M^T\).
Smith normal form is the computational certificate
(`integer_snf.smith_normal_form`). Cite it. Do not claim
novelty. Do not stamp this as a discovered Gate-C theorem.

---

## 2. TREE / LOOP are cycle rank

\[
\boxed{r_{\mathrm{cyc}}=m-\operatorname{rank} M.}
\]

\[
\boxed{\text{TREE}\iff r_{\mathrm{cyc}}=0.}
\]

A genuine one-cycle closure adds a channel without a new
independent phase degree of freedom and satisfies

\[
\boxed{r_{\mathrm{cyc}}:0\longrightarrow 1.}
\]

Then \(\ker_{\mathbb{Z}} M^T\) has rank one. Its primitive
generator \(c\) is the unique compatibility condition.

Operational control (MIN-CYCLE positive control): start from
a TREE matrix, append an integer combination of existing
rows, and check \(r_{\mathrm{cyc}}:0\to 1\). That is strictly
better than inferring topology from a drawing.

The locked NS parallelogram incidence is the same control:
the first three rows are a TREE; the fourth row equals
\(T_1-T_2+T_3\) over \(\mathbb{Z}\), so

\[
c=(1,-1,1,-1)
\]

is the unique primitive generator.

---

## 3. One-cycle loss law (local law, essentially complete)

Maximize

\[
\rho(\varepsilon)
=
\frac1W\sum_{i=1}^m w_i\cos\varepsilon_i,
\qquad
W=\sum_i w_i,\quad w_i>0,
\]

subject to the single primitive cycle constraint

\[
c^T\varepsilon=\delta,
\qquad
\delta=\operatorname{wrap}_{(-\pi,\pi]}(c^Tb).
\]

Channels with \(c_i=0\) align exactly, so every substantive
sum is over \(\operatorname{supp}c\). Write

\[
S=\sum_i\frac{c_i^2}{w_i},
\qquad
Q=\sum_i\frac{c_i^4}{w_i^3}.
\]

### Exact stationarity

A multiplier \(\lambda\) gives

\[
\mathcal L
=
\sum_i w_i\cos\varepsilon_i
+\lambda(c^T\varepsilon-\delta),
\]

hence

\[
\boxed{w_i\sin\varepsilon_i=\lambda c_i.}
\]

Necessarily

\[
\lvert\lambda\rvert
\le
\min_{c_i\neq 0}\frac{w_i}{\lvert c_i\rvert}.
\]

Each equation has branches

\[
\varepsilon_i
=
n_i\pi+(-1)^{n_i}
\arcsin\!\left(\frac{\lambda c_i}{w_i}\right).
\]

The exact solver **enumerates** admissible short branch
vectors \(n_i\in\{-1,0,1\}\) (here \(n\) and \(n+2\) differ
by \(2\pi\) and are the same torus point), imposes
\(c^T\varepsilon=\delta\), and compares \(\rho\). It does not
accept the first root. Ties keep the alignment branch.
Code: `exact_one_cycle_optimum`.

On the alignment-connected branch \(n\equiv 0\),

\[
\varepsilon_i=\arcsin(\lambda c_i/w_i),
\qquad
\delta
=
S\lambda+\frac Q6\lambda^3+O(\lambda^5).
\]

Series inversion:

\[
\boxed{
\lambda
=
\frac{\delta}{S}
-\frac{Q}{6S^4}\delta^3
+O(\delta^5).
}
\]

### Quadratic and quartic

\[
1-\rho
=
\frac1W\sum_i w_i(1-\cos\varepsilon_i).
\]

\[
\boxed{
1-\rho_{\max}
=
\frac{\delta^2}{2WS}
+O(\delta^4).
}
\]

One order farther, still with no numerical work:

\[
W(1-\rho)
=
\frac S2\lambda^2+\frac Q8\lambda^4+O(\lambda^6),
\]

\[
\boxed{
1-\rho_{\max}
=
\frac{\delta^2}{2WS}
-
\frac{Q}{24WS^4}\delta^4
+O(\delta^6).
}
\]

The quartic term is negative: near perfect alignment the
purely quadratic prediction slightly overestimates the true
loss. Equivalently

\[
\boxed{
\rho_{\max}
=
1-\frac{\delta^2}{2WS}
+\frac{Q\,\delta^4}{24WS^4}
+O(\delta^6).
}
\]

### Two controls

\[
c_i=0
\quad\Rightarrow\quad
\boxed{\varepsilon_i=0}
\]

at the maximizing solution (solver / incidence sanity check).

For small \(\lvert\delta\rvert\),

\[
\boxed{
\varepsilon_i
=
\frac{c_i}{w_i}\frac{\delta}{S}
+O(\delta^3).
}
\]

Channel-by-channel: larger \(\lvert c_i\rvert/w_i\) absorbs
more of the unavoidable mismatch. Not merely a prediction
for the final \(\rho\).

### What Heavy tests

On every genuine one-cycle instance
\(r_{\mathrm{cyc}}=m-\operatorname{rank}_{\mathbb Q}M=1\):

1. extract the primitive integer \(c\), compute \(\delta\);
2. predict \(\varepsilon_i^{(2)}=c_i\delta/(w_i S)\) and
   \(1-\rho^{(2)}=\delta^2/(2WS)\);
3. compare to the exact branch-enumerated optimum;
4. if \(\lvert\delta\rvert\le\pi/2\), also compare
   \(1-\rho^{(4)}=\delta^2/(2WS)-Q\delta^4/(24WS^4)\);
5. if \(\lvert\delta\rvert>\pi/2\), report the exact optimum
   and stamp the expansions
   **OUTSIDE PREREGISTERED SMALL-HOLONOMY REGIME**.

This is a finite-cycle local law. It is **not** a decay
exponent. Scale-rate stays **OPEN**.

---

## 4. NA-2B relabel

\[
\boxed{
\text{NA-2B = exact cancellation / assembly unit test}
}
\]

Not optimizer performance. `na2b_assembly.na2b_unit_report`
assembles an image point \(b=M\theta\) and, when
\(r_{\mathrm{cyc}}\ge 1\), certifies a forbidden target by the
integer kernel. No \(\rho\), no local max.

---

## 5. Finite-size incompatibility is not a rate

\[
\boxed{
\text{finite-size incompatibility}
\;\not\Rightarrow\;
\text{scale-decaying defect}
}
\]

Proving \(\rho(H)<1\) exactly on one finite network does not
produce a decay exponent. A rate needs additional information
about how cycle density/rank, holonomies, weights, and their
correlations behave as the shell or network grows.

Until provenance establishes otherwise,

\[
\boxed{0.15\text{ is a threshold / convention, not a derived exponent.}}
\]

Scale-rate defect stays **OPEN**. MIN-CYCLE does not accept it.

---

## MIN-CYCLE acceptance record

Canonical input: an integer matrix \(M\).

| Item | Status |
|---|---|
| Torus lemma | standard / proved |
| Finite P2 compatibility | exact integer algebra |
| Algebraic TREE→LOOP control \(r_{\mathrm{cyc}}:0\to 1\) | **accepted** |
| Unique primitive \(c\) | **accepted** |
| One-cycle loss law (exact + quadratic + quartic) | **accepted** as a local test |
| Branch-enumerated stationarity | **accepted** |
| Small-holonomy regime \(\lvert\delta\rvert\le\pi/2\) | preregistered |
| NA-2B assembly / incompatibility | **accepted** as a unit test |
| Scale-rate defect | **OPEN** |
| Derived exponent \(0.15\) | **not accepted** |
| Optimizer \(\rho<1\) as a rate | **not accepted** |
| Gate-C novelty for \(T_M\) | **not accepted** |
| TREE/LOOP from a drawing | **not accepted** |

**NS is not solved.**
