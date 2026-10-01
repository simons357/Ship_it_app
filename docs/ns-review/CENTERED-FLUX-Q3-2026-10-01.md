# Centered flux, near-shell obstruction, q=3 target

**Date:** 1 October 2026  
**Source:** ChatGPT Work note (“Centered Flux Progress”) pasted as screenshots.  
**Machine:** [`scripts/ns_attacks/centered_flux_q3.py`](../../scripts/ns_attacks/centered_flux_q3.py)  
**Lock:** Truth only. **★ NOT proved. NS NOT solved. Kill lane LIVE.**

This note independently checks the four bullets in that screenshot. It does
not inherit the ChatGPT runtime, scripts, or raw outputs. Convolution is
exact in \(\mathbb{Q}[i]\). The \(L^3\) gradient is a grid quadrature and
is used only for scaling tests.

Do **not** splice this into Φ-renorm, DA-NS-2, or Clay Statement B.

---

## Verdict table

| Claim from the note | Independent status |
|---|---|
| Centered-flux identity, including the energy-cancellation boundary term | **EXACT** on the locked triad; writings agree in \(\mathbb{Q}\) |
| Zero potential: differentiating recovers the barycenter law, no extra bound | **EXACT** as algebra; \(\sum T_k=0\) does not control \(T_c\) |
| Near-shell: \(T_c\) linear in \(\varepsilon\), \(D_s\) quadratic; no uniform \(T_c\le C\nu D_s\) | **CONFIRMED** at five exact \(\varepsilon\) |
| Proposed \(q=3\) bound: stated *conditional* AM-GM consequence | **EXACT** as an implication |
| Proposed \(q=3\) bound \(\lvert T_c\rvert\le C\|\nabla u\|_3\sqrt{D_s}\) as a universal \(C\) | **KILLED** by amplitude scaling |
| Square-root \(D_s\) is the right leading near-shell order | **CONFIRMED** on this family |
| Lemma★ / \(\sup\mathcal R_\star<\infty\) | **OPEN** |
| Control of \(\int\|\nabla u\|_3^2\,\mathrm{d}t\) | **OPEN**, and a separate task |
| Unaugmented 3-D Navier–Stokes / Clay B | **NOT** solved |

---

## 1. Setup (locked triad)

On \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\),

\[
p=(2,0,0),\; v_p=(0,1,0),\qquad
q=(0,2,0),\; v_q=(0,0,i),\qquad
k=(2,2,0),\; v_k=(0,0,\varepsilon),
\]

plus Hermitian conjugates. Then \(p+q=k\), the main shell is
\(\lambda=4\), the closing shell is \(\lambda=8\), and every triad product
stays in \(\mathbb Q[i]\).

Five parameter values:

\[
\varepsilon\in\Bigl\{\tfrac12,\tfrac14,\tfrac18,\tfrac1{16},\tfrac1{32}\Bigr\}.
\]

Signed transfer (no absolute values):

\[
\widehat B_k=i\,P_k\sum_{p+q=k}(q\cdot v_p)v_q,\qquad
T_k=-\mathrm{Re}\bigl(\widehat B_k\cdot\overline{v_k}\bigr).
\]

\[
N=\sum\lambda_k T_k,\qquad
M=\sum\lambda_k^2 T_k,\qquad
T_c=M-\Lambda N,\qquad
\Lambda=Y/X,\qquad
D_s=Z-\Lambda Y.
\]

---

## 2. Centered-flux identity (EXACT)

Energy cancellation:

\[
\sum_k T_k=0.
\]

The boundary term in the barycenter rewrite is exactly that sum:

\[
N=\sum_k(\lambda_k-\Lambda)T_k+\Lambda\sum_k T_k
=\sum_k(\lambda_k-\Lambda)T_k.
\]

Three writings of the centered flux agree in \(\mathbb Q\):

\[
T_c
=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k
=\sum_k(\lambda_k-\Lambda)^2 T_k+\Lambda N.
\]

\(D_s\) agrees with the variance sum, the double sum, and the two-shell
closed form. On this triad the closed form is exact:

\[
D_s=\frac{256\,\varepsilon^2}{1+\varepsilon^2}.
\]

---

## 3. Zero potential (EXACT; no bound)

The nonlinear contribution to kinetic energy vanishes:

\[
\dot E\big|_{\nu=0}=2\sum_k T_k=0.
\]

That is the zero nonlinear potential for \(E\). Taking the \(\lambda\)-
and \(\lambda^2\)-moments of the same balance recovers the barycenter
ODE and nothing else:

\[
X'=-2\nu Y+2N,\qquad
Y'=-2\nu Z+2M,\qquad
\Lambda'=\frac2X\bigl(T_c-\nu D_s\bigr).
\]

The identity is checked by equating the two writings of \(\Lambda'\) in
\(\mathbb Q\). It supplies **no** estimate of \(T_c\).

---

## 4. Near-shell obstruction (CONFIRMED)

Closed forms, checked against the convolution at all five \(\varepsilon\):

\[
T_c=\frac{64\varepsilon(2+\varepsilon^2)}{1+\varepsilon^2},\qquad
D_s=\frac{256\,\varepsilon^2}{1+\varepsilon^2}.
\]

\[
\frac{\lvert T_c\rvert}{D_s}=\frac{2+\varepsilon^2}{4\varepsilon}\to\infty
\qquad(\varepsilon\to 0),
\qquad
\frac{\lvert T_c\rvert}{\sqrt{D_s}}
=\frac{4(2+\varepsilon^2)}{\sqrt{1+\varepsilon^2}}\to 8.
\]

For every fixed \(\nu>0\) and \(C<\infty\),

\[
T_c\le C\nu D_s
\]

fails on this family. The linear-in-dissipation bound is **KILLED**.

The square-root ratio stays \(O(1)\) and has an exact limit \(8\).

That is why a \(\sqrt{D_s}\) factor is the right *leading* near-shell
order. It is not a proof of a uniform inequality on all fields.

\(\mathcal R_\star=T_c_+^2/(D_s\,E\,Y)\) stays \(O(1)\) here. The family
does **not** kill Lemma★.

---

## 5. The stated \(q=3\) target

Screenshot target:

\[
\lvert T_c\rvert\le C\|\nabla u\|_3\sqrt{D_s}.
\]

### 5.1 Conditional consequence (EXACT as algebra)

AM-GM: \(C\|\nabla u\|_3\sqrt{D_s}\le\nu D_s+C^2\|\nabla u\|_3^2/(4\nu)\).
So **if** the target held,

\[
T_c-\nu D_s\le\frac{C^2}{4\nu}\|\nabla u\|_3^2,
\]

and barycenter drift would be controlled by
\(\int\|\nabla u\|_3^2\,\mathrm{d}t\). That integral is a **separate**
open estimate. The implication is correct. The hypothesis is not a
theorem.

### 5.2 Universal \(C\) is KILLED

On a fixed shape \(v\), \(u=av\) scales as

\[
T_c(av)=a^3 T_c(v),\qquad
\|\nabla(av)\|_3=a\|\nabla v\|_3,\qquad
\sqrt{D_s(av)}=a\sqrt{D_s(v)}.
\]

The stated ratio grows like \(a\). Machine check at amplitudes
\(1,2,4\) on \(\varepsilon=1/8\): the ratio doubles when \(a\) doubles.
No field-independent \(C\) exists.

### 5.3 Homogeneous repairs (OPEN, not claimed)

Two amplitude-homogeneous replacements that still have \(\sqrt{D_s}\)
in the near-shell limit:

\[
\lvert T_c\rvert\le C\|\nabla u\|_3\sqrt{Y\,D_s},
\qquad
\lvert T_c\rvert\le C\|\nabla u\|_3^2\sqrt{D_s}.
\]

The first is invariant on \(u=av\) for this triad (machine). Neither
is proved. Do not promote either to Lemma★. The shape quotient remains

\[
\mathcal R_\star
=\frac{(T_c)_+^2}{D_s\,\|v\|_2^2\,Y}.
\]

---

## 6. What this does *not* do

- Does not prove ★.
- Does not close the kill lane (failure to blow \(\mathcal R_\star\)
  on one triad is not a proof).
- Does not control \(\int\|\nabla u\|_3^2\,\mathrm{d}t\).
- Does not touch Φ-renorm or \(\|u^r/r\|_\infty\).
- Does not solve unaugmented 3-D Navier–Stokes.

---

## 7. How to rerun

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/centered_flux_q3.py \
  --out data/centered_flux_q3_2026-10-01.json
python3 -m unittest tests.test_centered_flux_q3
```

`ns_solved` is false in the JSON.
