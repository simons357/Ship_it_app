# H1 — three shapes, written as estimates

10 September 2026. Arithmetic and lookups. **Not a proof.
H1 is not proved. NS is not solved.**

Object: [`H1-OBJECT.md`](H1-OBJECT.md).
Lookups: [`LOOKUP-H1.md`](LOOKUP-H1.md).
Tube writing of the same leftover class (different
integral): [`H1-SOT.md`](H1-SOT.md).
Do not merge with H, Lemma C, H2, H3, or Lemma★.

Full write (locked \(\mathcal G\); not a theorem):
[`H1-WRITE.md`](H1-WRITE.md).
These are writings of H1. None of them sits.
Do not cash “assume thin” as 1. Do not cash Lemma J
on generic fields as 2. Do not cash an imposed
waiting time as 3.

---

## 1. Thinness

HLS on the full Bad set recovers local \(E^3\).
The Hölder cut changes the set, not the exponent.
A path jump in \(\xi\) does not prove the set is thin.

**Dyadic number (valid CS, not H1).**
Fix \(x\in B_{r/2}\) and a near scale \(\rho\in(0,r)\).
Shells \(A_k=\{y:2^{-(k+1)}\rho\le|x-y|<2^{-k}\rho\}\).
Let \(\theta_k(x)\) be the volume fraction of
\(A_k\) on which \((x,y)\) is Bad. Cauchy–Schwarz on
the kernel \(|z|^{-3}\) gives a factor
\(\theta_k^{1/2}(2^{-k}\rho)^{-3/2}\). The sum in \(k\)
stays of order \(\rho^{-3/2}\) if, for some \(\delta>0\),
\[
\theta_k(x)\le C\,2^{-(3+\delta)k}
\]
uniformly in \(x\) on \(\operatorname{supp}\phi\). Then
\[
A_{\mathrm{bad}}^{<\rho}(Q_r)
\le
C_\delta\rho^{-3/2}\int_{t_0-r^2}^{t_0} E_{\mathrm{loc}}(t)^{3/2}\,dt.
\]
That is the mid-Bad / H3 class already named in the
packet §12. Young against \(E^{3/2}\) still returns a
cubic remainder or a smallness of \(E_{\mathrm{loc}}\).
**CS-summable volume thinness is not H1.**

**What would be H1.** An exponent drop on the kernel
(\(|z|^{-3}\) to \(|z|^{-3+\varepsilon}\)), or an
operator bound that pays stretching by dissipation
plus \(r^{-2}\iint|\omega|^2\), from \(\int E<\infty\).
Lemma C is the angular version of that drop, on Good
pairs only. 1-D sparseness of intense regions is a
different if (Grujić 2013). Neither is proved for Bad
from energy.

**Lookup 1.** Miss. See [`LOOKUP-H1.md`](LOOKUP-H1.md).

**Not this, and not H1.** Frequency thinness
of a low-pass field is Lemma P1. It sits.
[`H1-P1.md`](H1-P1.md). It does not thin the
Bad set, and it does not drop the kernel.
The cutoff commutator is Lemma P1-loc.
It sits with \(\nabla u\) kept. [`H1-P1-LOC.md`](H1-P1-LOC.md).
Path-cost of one pair is Lemma PC. It sits
as a curve bound. It does not thin the set.
[`H1-PC.md`](H1-PC.md).

---

## 2. J on folds only

A bad pair is one of three pictures: fold (dissipation
spread in a ball), reconnection (thin bridge), two blobs
(gap with \(\omega\approx 0\)). Path-cost of \(\nabla\xi\)
dies on a sheet or a gap as H1. Lemma PC sits as the
1-D bound ([`H1-PC.md`](H1-PC.md)). Lemma J on generic
fields is false.

**Vitali write (sufficient, not proved).**
Assume every near-Bad pair at scale \(\rho\) sits in a
ball \(B\) of radius \(2\rho\) with
\[
\int_B|\nabla\omega|^2\gtrsim\Lambda^2\rho^2.
\]
Vitali: a disjoint subcollection \(\{B_j\}\) with
\[
\sum_j\Lambda^2\rho_j^2
\le
C\int_{B_{4r}}|\nabla\omega|^2.
\]
If also
\[
A_{\mathrm{bad}}^{<\rho}
\le
C\sum_j\Lambda^3\rho_j^3,
\]
then
\[
A_{\mathrm{bad}}^{<\rho}
\le
C\bigl(\sup_j\Lambda\rho_j\bigr)
\iint|\nabla\omega|^2.
\]
If every such scale satisfies \(\Lambda\rho_j\le c\nu\),
the \(\nu/8\) slice sits.

Three hypotheses, none free:

- **F.** Persistent Bad pairs are folds, not sheets or gaps.
- **A.** Stretching is bounded by the Vitali sum of \(\Lambda^3\rho^3\).
- **S.** \(\Lambda\rho\) is small enough to eat.

NSE is not known to give F. A is not the pointwise
Lemma J (already false). S is a restriction on scale
versus threshold, not a bound from \(\int E<\infty\).

**Lookup 2.** Miss.

---

## 3. Dynamics

Shape 2’s alternatives are a sheet and a gap.
Shape 3 is the claim that NSE *forbids* those on the
time scale \(r^2/\nu\), so F holds.

That is not a filter on which cylinders to use.
An imposed waiting time is not derived. Pathwise
enstrophy does not produce \(\int|\nabla\omega|^2\).

**Lookup 3.** Miss.

---

## Lookups (scored)

| # | Question | Hit? |
|---|---|---|
| 1 | Thinness of Bad from \(\int E<\infty\) | **Miss.** Grujić, *Nonlinearity* 26 (2013) assumes 1-D \(\delta\)-sparseness of superlevel sets at the analyticity scale (Theorems 4.1–4.2). Later \(Z_\alpha\) papers (Bradshaw–Farhat–Grujić 2019; Grujić–Xu 2024) still treat sparseness as a class, not a theorem that Bad is thin. |
| 2 | Folds + Vitali, sheets/gaps excluded by NSE | **Miss.** No such estimate. |
| 3 | NSE forbids persistent sheets/gaps on \(r^2/\nu\) | **Miss.** |
| 4 | Grujić *CMP* 290 (2009) absorbs H3 from energy | **Miss (expected).** The paper localizes the Hölder-\(1/2\) coherence *condition* (GrZh06 / Gr09). Exterior stretching is controlled under that local if. Not weaker than Lemma C in a way that eats \(A_{\mathrm{ext}}\) from \(\int E<\infty\). Crude bound stays packet §11. |
| 5 | Exact \(A_{\mathrm{bad}}\) integral from energy | **Miss.** Already scored. Confirmed. |

A hit would have been a theorem. These are still ifs.

---

## Status

Shapes 1–3 are now holdable as estimates.
None is proved. Lemma PC sits as the 1-D
path-cost ([`H1-PC.md`](H1-PC.md)). That is
not shape 2 and not H1. H1 is still the leftover.

Do not: another criterion paper, glue to Lemma★,
add \(K(t)\) to the PDE, cash this file as (6).

If H1 sits and H2-from-energy does not, the cylinder
is still open. Local Serrin then, not CKN.

NS is not solved.
