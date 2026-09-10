# Lemma★ / \(\mathcal R_\star\) — exact Fourier formulas (USER lock-in)

**Audience:** Jonathan R. Simons  
**Status:** HYPOTHESIS encoding only — **NS NOT SOLVED** · **No SFE**  
**Companion:** [`LEMMA-STAR-DA-NS-1.md`](./LEMMA-STAR-DA-NS-1.md)  
**Code:** `domain_architect/rstar_quantities.py` · `python3 -m domain_architect --lemma-star`

**USER LOCK-IN:** ★ is a **shape statement**, not a viscosity statement. Under \(u=av\), size optimization cancels \(\nu\). Decisive form is a uniform bound on \(\mathcal R_\star(v)\). Numerics = evidence only. Proof needs a **triadic reason**. HH→L is the dangerous channel. Only the **complete** \(T_c\) decides failure — never a restricted HH→L proxy, and never absolute-value of the triad sum.

---

## Domain / Fourier setup

Normalized torus
\[
\mathbb T^3 = \bigl(\mathbb R / 2\pi\mathbb Z\bigr)^3.
\]

Divergence-free Fourier field
\[
v(x)=\sum_{k\in\mathbb Z^3} v_k\, e^{ik\cdot x},\qquad
k\cdot v_k=0,\qquad
v_{-k}=\overline{v_k}.
\]

Eigenvalues of \(A=-\mathbb P\Delta\):
\[
\lambda_k=|k|^2,\qquad (Av)_k=\lambda_k\, v_k.
\]

Shell energy (mode / shell input to DA):
\[
e_k:=|v_k|^2\qquad\text{or aggregated}\qquad
e_\alpha:=\sum_{|k|^2=\alpha}|v_k|^2.
\]

---

## Linear spectral moments

\[
\|v\|_2^2=\sum_k |v_k|^2,
\qquad
X=\sum_k \lambda_k\,|v_k|^2,
\qquad
Y=\sum_k \lambda_k^2\,|v_k|^2,
\qquad
Z=\sum_k \lambda_k^3\,|v_k|^2,
\qquad
\Lambda=\frac{Y}{X}\quad(X>0).
\]

---

## Spectral spread \(D_s\) — three equivalent forms

**Form 1 (moment difference):**
\[
D_s = Z-\Lambda Y = Z-\frac{Y^2}{X}.
\]

**Form 2 (weighted variance):**
\[
D_s = \sum_k \lambda_k\bigl(\lambda_k-\Lambda\bigr)^2\,|v_k|^2.
\]

**Form 3 (pairwise nonnegativity):**
\[
D_s
=\frac{1}{2X}\sum_{k,\ell}
\lambda_k\,\lambda_\ell\,(\lambda_k-\lambda_\ell)^2\,|v_k|^2\,|v_\ell|^2
\ge 0.
\]

All three agree whenever \(X>0\). If \(X=0\) (trivial field), \(D_s=0\) by convention.

### Two-shell closed form

On shells \(\alpha\neq\beta\) with energies \(e_\alpha,e_\beta\ge 0\):
\[
D_s
=\frac{\alpha\beta\,(\alpha-\beta)^2\, e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]
(Equals Form 1–3 on that two-shell support.)

Pure single shell: \(D_s=0\). Pure single shell with vanishing stretch is **not** a kill (both sides of the shape inequality vanish). Live kill = almost-single-shell that still stretches (\(D_s\to 0\) with \(T_c>0\)).

---

## Nonlinear triad quantities

Projector nonlinearity:
\[
B=\mathbb P\bigl[(v\cdot\nabla)v\bigr].
\]

Mode triad sum (**signed** — **NEVER absolute-value the triad sum**):
\[
T_k
=\sum_{p+q=k}
\operatorname{Im}\Bigl[
(q\cdot v_p)\,(v_q\cdot\overline{v_k})
\Bigr].
\]

Weighted sums:
\[
N=\sum_k \lambda_k\, T_k,
\qquad
M=\sum_k \lambda_k^2\, T_k,
\qquad
T_c=M-\Lambda N=\sum_k \lambda_k\bigl(\lambda_k-\Lambda\bigr)\,T_k.
\]

### Expanded ordered triad (\(p+q=k\))

\[
T_c
=\sum_{k}\sum_{p+q=k}
\lambda_k\bigl(\lambda_k-\Lambda\bigr)\,
\operatorname{Im}\Bigl[
(q\cdot v_p)\,(v_q\cdot\overline{v_k})
\Bigr].
\]

### Expanded ordered triad (\(p+q+r=0\))

Set \(k=-r\) (so \(p+q=k\) iff \(p+q+r=0\)):
\[
T_c
=\sum_{p+q+r=0}
\lambda_r\bigl(\lambda_r-\Lambda\bigr)\,
\operatorname{Im}\Bigl[
(q\cdot v_p)\,(v_q\cdot\overline{v_r})
\Bigr].
\]
(Equivalent reindex of the \(p+q=k\) form; same signed sum.)

**Hard rule:** HH→L-restricted partial sums are **not** complete \(T_c\). Kill / failure decisions use **only complete** \(T_c\).

---

## Shape form and \(\mathcal R_\star\) quotient

Boxed shape inequality (viscosity cancelled):
\[
\boxed{\bigl(T_c(v)_+\bigr)^2
\le 4\theta\, C_0\, D_s(v)\,\|v\|_2^2\, Y(v)}
\]

Decisive ratio (complete \([T_c]_+\) in the numerator):
\[
\mathcal R_\star(v)
=\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\, Y(v)}
\quad\bigl(D_s\|v\|_2^2 Y>0\bigr).
\]

Positive part: \(T_c_+=\max(T_c,0)\). If \(T_c\le 0\), then \(\mathcal R_\star=0\) on the domain where the denominator is positive.

### Kill / status rules (locked)

| Rule | Meaning |
| --- | --- |
| \(\sup_v \mathcal R_\star=\infty\) | no finite \(C_0\) → ★ **dead** |
| \(D_s=0\) and \(T_c>0\) | ★ **dead** on that field |
| Pure single shell, both vanish | **not** a kill |
| Almost-single-shell that stretches | **live kill** |
| Finite small \(\mathcal R_\star\) samples | **≠** uniform bound (evidence only) |

---

## Sign check (viscosity bookkeeping)

Evolution of the spectral scale marker:
\[
\Lambda'=\frac{2}{X}\bigl(T_c-\nu D_s\bigr).
\]
Used as a consistency / sign check on the packaging. Under \(u=av\) size optimization the \(\nu\) dependence cancels in the shape form; this identity is **not** a substitute for a uniform \(\mathcal R_\star\) bound.

---

## What is still open

- Uniform bound \(\sup_v\mathcal R_\star(v)<\infty\) ≡ PRODUCT-BLOCK / Clay weld in this packaging.
- Triadic reason controlling HH→L so stretching cannot outrun spectral spread — **not written**.
- **NS NOT SOLVED.** Numerics ≠ proof. No SFE glue.

---

## Attack 9 cross-link (falsification experiments)

| Attack | Status | Doc |
|--------|--------|-----|
| **9A** AP coherent packet/fan | **Negative for kill** — \(T_c\) rose but \(D_s\) grew faster; \(D_s\|v\|_2^2 Y=O(1)\) in packet size was **FALSE** for that family | [`ATTACK-9-COHERENT-PACKET-FAN.md`](./ATTACK-9-COHERENT-PACKET-FAN.md) |
| **Fixed-gap spheres** | **Negative for kill** — \(D_s\) from **gap** (not width); closures \(O(m)\); \(\mathcal R_\star\) falls \(0.11\to 0.031\) (exact quotient, this family); does **not** track \(m^{1/2}\); **natural same-shell ensemble is not a kill** | [`ATTACK-9-FIXED-GAP-SPHERES.md`](./ATTACK-9-FIXED-GAP-SPHERES.md) |
| **9B** Exact-shell + closing | Structured next family — \(v_\varepsilon=w_\alpha+\varepsilon z_\beta\), \(z_\beta\parallel\Pi_\beta B(w_\alpha,w_\alpha)\); boxed \(K_{\alpha,\beta}\) | [`ATTACK-9B-EXACT-SHELL-CLOSING.md`](./ATTACK-9B-EXACT-SHELL-CLOSING.md) |
| **9C** Designed \(\Theta(m^2)\)-closure | **Remaining packet falsifier** — designed \(\Theta(m^2)\)-closure subset with **locked phases** | [`ATTACK-9-FIXED-GAP-SPHERES.md`](./ATTACK-9-FIXED-GAP-SPHERES.md) |

Caveat: a merely “narrow” packet does **not** automatically keep \(D_s=O(1)\) on the lattice
(\(D_s=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2\)). Next clean tests = 9B \(K_{\alpha,\beta}\) / 9C designed closure — **not** another widening AP packet.

Kill lane remains **LIVE**. Refuse “AP packet closed kill lane.” Refuse “same-shell ensemble kills ★.” Code: `domain_architect/kab_quantity.py`.

**Attestation:** \(0.11\to 0.031\) uses exact \(\mathcal R_\star=(T_c_+)^2/(D_s\|v\|_2^2 Y)\) for this fixed-gap family only.

---

## Runtime

```bash
python3 -m domain_architect --lemma-star
python3 -c "from domain_architect.rstar_quantities import *; help(spectral_moments)"
python3 -m unittest tests.test_rstar_quantities -v
```
