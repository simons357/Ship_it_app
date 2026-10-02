# The candidate \(|T_c|\le C\|\nabla u\|_3\sqrt{YD_s}\)

**Date:** 1 October 2026  
**Machine:** [`scripts/ns_attacks/tc_sqrt_yds.py`](../../scripts/ns_attacks/tc_sqrt_yds.py)  
**Lock:** Truth only. **★ NOT proved. NS NOT solved. Kill lane LIVE.**

This note attacks the amplitude-homogeneous repair left open by the
centered-flux / \(q=3\) check. It does not splice into \(\Phi\)-renorm,
DA-NS-2, or Clay Statement B.

---

## Verdict table

| Claim | Status |
|---|---|
| Sitting pairing \(\lvert T_c\rvert\le\|A^{1/2}B\|_2\sqrt{D_s}\) | **EXACT** (Cauchy–Schwarz) |
| Near-shell: \(T_c=\Theta(\varepsilon)\), \(D_s=\Theta(\varepsilon^2)\); no uniform \(T_c\le C\nu D_s\) | **KILLED** (inherited; closed forms) |
| Stated \(q=3\) target \(\lvert T_c\rvert\le C\|\nabla u\|_3\sqrt{D_s}\) | **KILLED** by amplitude (inherited) |
| Square-root in \(D_s\) is the right *leading* near-shell order | **CONFIRMED**; \(\lvert T_c\rvert/\sqrt{D_s}\to 8\) |
| Alternate repair \(\lvert T_c\rvert\le C\|\nabla u\|_3^2\sqrt{D_s}\) | **KILLED** by a localized bump (\(\rho\sim\ell^{-1/2}\)) |
| Candidate \(\lvert T_c\rvert\le C\|\nabla u\|_3\sqrt{Y\,D_s}\) | **OPEN**. Bounded on every family tested; \(\rho_Y\le 0.242\) |
| Crude product close \(\|A^{1/2}B\|_2\le C\|\nabla u\|_3\sqrt{Y}\) | **NOT proved**. \(W^{1,3}\not\hookrightarrow L^\infty\). No numerical kill yet |
| Lemma★ / \(\sup\mathcal R_\star<\infty\) | **OPEN** (already killed as a *static uniform* bound; not repaired here) |
| Control of \(\int\|\nabla u\|_3^2\,\mathrm{d}t\) | **OPEN**, and a separate task |
| Unaugmented 3-D Navier–Stokes / Clay B | **NOT** solved |

---

## 1. Why this candidate

The flux identity and the barycenter law sit:

\[
\Lambda'=\frac2X\bigl(T_c-\nu D_s\bigr).
\]

A linear absorption \(T_c\le C\nu D_s\) is impossible. On the locked
two-shell triad of the \(q=3\) note,

\[
T_c=\frac{64\varepsilon(2+\varepsilon^2)}{1+\varepsilon^2},\qquad
D_s=\frac{256\varepsilon^2}{1+\varepsilon^2},
\]

so \(\lvert T_c\rvert/D_s=(2+\varepsilon^2)/(4\varepsilon)\to\infty\), while

\[
\frac{\lvert T_c\rvert}{\sqrt{D_s}}=\frac{4(2+\varepsilon^2)}{\sqrt{1+\varepsilon^2}}\to 8.
\]

That is the exact obstruction: the leading near-shell order in \(D_s\)
is a square root, not a first power.

The screenshot target \(\lvert T_c\rvert\le C\|\nabla u\|_3\sqrt{D_s}\)
has the right \(D_s\) power and the wrong homogeneity. On \(u=av\),

\[
T_c(av)=a^3 T_c(v),\qquad
\|\nabla(av)\|_3\sqrt{D_s(av)}=a^2\|\nabla v\|_3\sqrt{D_s(v)}.
\]

The ratio grows like \(a\). No field-independent \(C\) exists.

Two amplitude-homogeneous repairs keep \(\sqrt{D_s}\):

\[
\lvert T_c\rvert\le C\|\nabla u\|_3\sqrt{Y\,D_s},
\qquad
\lvert T_c\rvert\le C\|\nabla u\|_3^2\sqrt{D_s}.
\]

Only the first is scaling-critical for a localized bump
\(v_\ell(x)=V(x/\ell)\). With \(T_c\sim U^3\ell^{-2}\),
\(Y\sim U^2\ell^{-1}\), \(D_s\sim U^2\ell^{-3}\), \(\|\nabla u\|_3\sim U\),

| Right-hand side | Scaling | Verdict |
|---|---|---|
| \(\sqrt{D_s\,E\,Y}\) (unrestricted ★) | \(U^3\ell^{-1/2}\) | supercritical; **killed** |
| \(\|\nabla u\|_3\sqrt{D_s}\) (stated \(q=3\)) | \(U^2\ell^{-3/2}\) | wrong in \(U\); **killed** |
| \(\|\nabla u\|_3^2\sqrt{D_s}\) | \(U^3\ell^{-3/2}\) | supercritical; **killed** below |
| \(\|\nabla u\|_3\sqrt{Y\,D_s}\) | \(U^3\ell^{-2}\) | critical; the remaining target |

That is the concrete advance: an exact obstruction, and one remaining
homogeneous square-root candidate that the known static kills do not
remove.

---

## 2. Pairing reduction

Definitions are the locked centered ones on \(\mathbb T^3\),
measure \(\mathrm{d}x/(2\pi)^3\), \(A=-\Delta\) on divergence-free
fields, \(\lambda_k=\lvert k\rvert^2\):

\[
T_c=-\langle B(u,u),A(A-\Lambda)u\rangle,
\qquad
D_s=\|(A-\Lambda)A^{1/2}u\|_2^2.
\]

Cauchy–Schwarz is an identity, not a hope:

\[
\lvert T_c\rvert
\le
\|A^{1/2}B(u,u)\|_2\sqrt{D_s}.
\]

The candidate therefore reduces to a product estimate

\[
\|A^{1/2}P(u\cdot\nabla u)\|_2
\le
C\|\nabla u\|_3\sqrt{Y}
=
C\|\nabla u\|_3\|u\|_{\dot H^2}.
\]

Split \(\nabla(u\otimes u)=\nabla u\otimes\nabla u+u\otimes\nabla^2 u\).

**Easy term.** Gagliardo–Nirenberg plus Sobolev on \(\mathbb T^3\):

\[
\|\nabla u\|_4\le C\|\nabla u\|_3^{1/2}\|\nabla u\|_6^{1/2},
\qquad
\|\nabla u\|_6\le C\|\Delta u\|_2=\sqrt{Y},
\]

so \(\|\nabla u\otimes\nabla u\|_2\le C\|\nabla u\|_3\sqrt{Y}\).

**Hard term.** \(\|u\otimes\nabla^2 u\|_2\le\|u\|_\infty\sqrt{Y}\).
The estimate \(\|u\|_\infty\le C\|\nabla u\|_3\) is false:
\(W^{1,3}(\mathbb T^3)\) does not embed in \(L^\infty\). The pairing
route does **not** close by Hölder–Sobolev. A logarithmically
concentrating sequence can make \(\|u\|_\infty/\|\nabla u\|_3\)
arbitrarily large. That is an obstruction to *this proof*, not yet a
kill of the candidate: \(T_c\) may fail to achieve the pairing.

On every family below, the pairing ratio
\(\|A^{1/2}B\|_2/(\|\nabla u\|_3\sqrt{Y})\) stayed \(\le 1/2\).
That is a sample, not a theorem.

---

## 3. Machine

Convolution for sparse fields is exact in \(\mathbb Q[i]\). The
\(L^3\) gradient is a DFT quadrature and is used only in ratios.
Localized / log probes are spectral. The spectral scheme matches the
exact triad flux to \(10^{-8}\).

### 3.1 Near-shell (locked triad)

As \(\varepsilon\to 0\), \(Y\to 64\) and \(\|\nabla u\|_3\to g_\infty\approx 4.129\), so

\[
\rho_Y
:=\frac{\lvert T_c\rvert}{\|\nabla u\|_3\sqrt{Y\,D_s}}
\to
\frac{8}{8\,g_\infty}
=\frac1{g_\infty}
\approx 0.242.
\]

Observed: \(0.177,0.221,0.237,0.241,0.242\). The square-root candidate
is saturated, not violated. The linear ratio is \(1.125,2.06,4.03,8.02,16.01\).

### 3.2 Amplitude

On \(\varepsilon=1/8\) and \(a\in\{1,2,4\}\), \(\rho_Y\) is invariant
(\(0.23666\) to machine precision). The \(Y\)-less \(q=3\) ratio
doubles when \(a\) doubles.

### 3.3 Growing layer \(v_n\) (the ★ kill)

Locked: \(E_n=4(2n+1)\), \(T_c=3n^5(3n^2+3n+1)\).  
\(\mathcal R_\star\) grows (\(0.0014\to 0.0062\) for \(n=1\dots 5\)).
\(\rho_Y\) **falls** (\(0.0153\to 0.0054\)), consistent with
\(\|\nabla u\|_3\sim n^{5/3}\) against \(T_c/\sqrt{YD_s}\sim n\).
The family that killed unrestricted ★ does **not** kill the candidate.

### 3.4 Localized curl-Gaussian bump

After the torus-scale width \(\ell=0.9\),

\[
\rho_Y(\ell)\in\{0.0439,0.0444,0.0446\}
\quad(\ell=0.65,0.48,0.36),
\]

a plateau, all well below the near-shell limit \(0.242\). The
alternate quotient collapses as predicted:

\[
\rho_{g32}(\ell)\,\sqrt{\ell}
\in\{0.0618,0.0623,0.0624\}.
\]

So \(\lvert T_c\rvert/(\|\nabla u\|_3^2\sqrt{D_s})\sim\ell^{-1/2}\to\infty\).
The second homogeneous repair is **KILLED**. The first is not.

### 3.5 Other probes

| Family | \(\rho_Y\) | Notes |
|---|---|---|
| Separated two-shell, ratio \(2\), frequency \(m=1\dots 4\) | \(0.207\to 0.052\) | falls like \(1/m\) |
| Random \(3\times 3\times 3\) cubelet, 8 seeds | \(\le 0.037\) | no outlier |
| Log envelope \(\times\) triad, \(\delta\downarrow\) | \(0.005\to 0.008\) | slow; not a kill |

---

## 4. Conditional consequence (algebra only)

If the candidate held, AM-GM would give

\[
T_c-\nu D_s
\le
\frac{C^2}{4\nu}\,Y\,\|\nabla u\|_3^2,
\qquad
(\log\Lambda)'
\le
\frac{C^2}{2\nu}\,\|\nabla u\|_3^2.
\]

Barycenter drift would then be controlled by
\(\int\|\nabla u\|_3^2\,\mathrm{d}t\). That integral is **not** an
energy-class bound. The implication is correct. The hypothesis is not
a theorem. Even if the hypothesis were proved, Clay B would remain
open.

---

## 5. What this does *not* do

- Does not prove the candidate.
- Does not restore unrestricted ★.
- Does not close the pairing product estimate.
- Does not control \(\int\|\nabla u\|_3^2\,\mathrm{d}t\).
- Does not touch \(\Phi\)-renorm or \(\|u^r/r\|_\infty\).
- Does not solve unaugmented 3-D Navier–Stokes.

The remaining analytic target is exactly the candidate, or a
structured close of \(\|A^{1/2}B\|_2\le C\|\nabla u\|_3\sqrt{Y}\)
that uses the Leray projector and the pairing alignment, not
\(\|u\|_\infty\).

---

## 6. How to rerun

```bash
PYTHONPATH=. python3 scripts/ns_attacks/tc_sqrt_yds.py \
  --out data/tc_sqrt_yds_2026-10-01.json
python3 -m unittest tests.test_tc_sqrt_yds
```

`ns_solved` is false in the JSON.
