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

## 3. One-cycle loss law

If the phase errors obey \(\sum_i c_i\varepsilon_i=\delta\)
and the local objective loss is \(\tfrac12\sum_i w_i\varepsilon_i^2\),
the constrained minimizer is

\[
\varepsilon_i
=
\frac{\delta\,c_i/w_i}
{\sum_j c_j^2/w_j}.
\]

With the TREE objective normalized to \(1\),

\[
\boxed{
1-\text{objective}
\;\sim\;
\frac{\delta^2}
{2\sum_j c_j^2/w_j}.
}
\]

The exact nonlinear stationarity of the cosine objective,

\[
\boxed{w_i\sin\varepsilon_i=\lambda c_i,}
\]

is a one-dimensional solve. It is a prediction → measurement
test for Heavy. It is **not** the big polarization optimizer.

Small-\(\delta\) agreement is required by
`tests.test_one_cycle_loss`. Finite-cycle agreement is not a
decay exponent.

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
| One-cycle loss law (small \(\delta\)) | **accepted** as a test |
| NA-2B assembly / incompatibility | **accepted** as a unit test |
| Scale-rate defect | **OPEN** |
| Derived exponent \(0.15\) | **not accepted** |
| Optimizer \(\rho<1\) as a rate | **not accepted** |
| Gate-C novelty for \(T_M\) | **not accepted** |
| TREE/LOOP from a drawing | **not accepted** |

**NS is not solved.**
