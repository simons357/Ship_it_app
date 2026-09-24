# ATTACK 10 — Localized bump: static uniform \(\mathcal{R}_\star\) is dead

**Date:** 2026-09-24  
**Branch:** `cursor/attack-10-localized-bump-6386`  
**Status:** **★ dead as a static bound.** \(\sup\mathcal{R}_\star=\infty\). A single localized bump shows it.  
**NS not solved.** The algebra of the centered identities stands. The inequality had the wrong scaling.

**Prior non-kills:** Attacks 9A / 9B / 9C were Fourier-shell families. None of them concentrate in physical space, which is the direction that kills ★.  
**9B lane:** closed as a *restricted* near-shell probe (Sept 20 note; \(K_{\alpha,\beta}\le 16/9\)). It cannot produce unbounded \(\mathcal{R}_\star\).

---

## What was claimed

Lemma★ (shape form) asserted a geometry-only constant
\[
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
D_s(v)\,\|v\|_2^2\,Y(v),
\]
equivalently \(\sup_v\mathcal{R}_\star(v)<\infty\), over all smooth mean-zero divergence-free fields on a **fixed** torus, with
\[
\mathcal{R}_\star(v)
=
\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}.
\]

That supremum is infinite.

---

## Why it fails: \(\mathcal{R}_\star\) has units

Give velocity units of \(U\) and length units of \(L\). Then

| Object | Scaling |
|--------|---------|
| \(T_c\) | \(U^3 L^{-2}\) |
| \(D_s\) | \(U^2 L^{-3}\) |
| \(\|v\|_2^2\) | \(U^2 L^3\) |
| \(Y=\|Av\|_2^2\) | \(U^2 L^{-1}\) |
| \(\mathcal{R}_\star=(T_c_+)^2/(D_s\|v\|_2^2 Y)\) | \(L^{-3}\) |

On a torus of fixed size, a divergence-free bump of width \(\ell\) therefore has \(\mathcal{R}_\star\) growing like \(\ell^{-3}\).

The note’s own Young step turns ★ into \(\Lambda'\le 2C_0\nu^{-1}E\Lambda\). That would give global regularity controlled by energy alone, which is supercritical. The missing \(L^{-3}\) is the standard supercriticality barrier showing up as a units mismatch.

---

## The construction

Take a smooth, compactly supported, divergence-free profile \(V\) on \(\mathbb{R}^3\) with \(T_c(V)\ne 0\), and set
\[
v_\ell(x)=V\bigl((x-x_0)/\ell\bigr).
\]
Every moment involved is a local integral:

- \(Av=-\Delta v\).
- The Leray projection \(P\) drops out of \(N\) and \(M\), because it is paired with \(Av\) and \(A^2v\), which are already divergence-free.

Change of variables gives
\[
\boxed{\mathcal{R}_\star(v_\ell)=\ell^{-3}\mathcal{R}_\star(V)}
\]
exactly (on \(\mathbb{R}^3\), and on \(\mathbb{T}^3\) once \(\ell\) is small enough that the support fits without periodic overlap). Replacing \(V\) by \(-V\) reverses \(T_c\) and leaves the denominator unchanged, so any \(V\) with \(T_c\ne 0\) gives a positive-sign kill.

A fully rigorous write-up uses compactly supported \(V\). The scaling identity does not wait on that: it is exact for Schwartz profiles as soon as the tails are negligible on the torus.

**Stream-function realization.** Numerics use \(v=\mathrm{curl}\,\psi\) with \(\psi_\ell(x)=\Psi((x-x_0)/\ell)\). Then \(v_\ell=\ell^{-1}V((x-x_0)/\ell)\). The extra \(\ell^{-1}\) from the curl sends \(T_c\sim\ell^{-5}\), but \(\mathcal{R}_\star\) is amplitude-invariant, so
\[
\mathcal{R}_\star(v_\ell)=\ell^{-3}\mathcal{R}_\star(V)
\]
is unchanged.

---

## Why Fourier dilation hid it

The note’s invariance under Fourier dilation \(v(n\cdot)\) is correct, and it hides the problem. Dilating on the torus is a localization (a factor of \(n^3\)) combined with \(n^3\) periodic copies (a factor of \(n^{-3}\)), and the two cancel.

Attacks 9A, 9B, and 9C all built fields out of Fourier shells, none of which concentrate in physical space. That is exactly the direction that kills ★.

---

## Numerical check

Script: `scripts/ns_attacks/attack10_localized_bump.py`  
Reconstruction: random-quadratic Gaussian stream, \(v=\mathrm{curl}\,\psi\), spectral on \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\), 2/3 dealiasing on \((v\cdot\nabla)v\).

**This branch, \(N=64\), seed \(20260924\):**

| \(\ell\) | \(T_c\) | \(\mathcal{R}_\star\) | \(\mathcal{R}_\star\cdot\ell^3\) | tail \(>N/3\) |
|---:|---:|---:|---:|---:|
| 0.55 | \(9.044\times 10^{1}\) | \(6.556\times 10^{-7}\) | \(1.090755\times 10^{-7}\) | \(2.9\times 10^{-12}\) |
| 0.45 | \(2.467\times 10^{2}\) | \(1.197\times 10^{-6}\) | \(1.090755\times 10^{-7}\) | \(7.6\times 10^{-19}\) |
| 0.38 | \(5.745\times 10^{2}\) | \(1.988\times 10^{-6}\) | \(1.090755\times 10^{-7}\) | \(1.7\times 10^{-26}\) |
| 0.32 | \(1.357\times 10^{3}\) | \(3.329\times 10^{-6}\) | \(1.090755\times 10^{-7}\) | \(1.8\times 10^{-18}\) |

\(\mathcal{R}_\star\cdot\ell^3\) is constant to six digits (relative spread \(1.4\times 10^{-6}\)). \(T_c\sim\ell^{-5}\) as required for the curl realization. Sign flip \(v\mapsto -v\) reverses \(T_c\) and leaves \(D_s,E,Y\) unchanged.

The profile is not optimized. The constant means nothing. The \(\ell^{-3}\) growth is the point.

**Author’s 128³ check (filed with the attack; different polynomial):**

| \(\ell\) | \(T_c\) | \(\mathcal{R}_\star\) | \(\mathcal{R}_\star\cdot\ell^3\) |
|---:|---:|---:|---:|
| 0.60 | 0.400 | \(1.56\times 10^{-4}\) | \(3.364\times 10^{-5}\) |
| 0.45 | 1.688 | \(3.82\times 10^{-4}\) | \(3.4847\times 10^{-5}\) |
| 0.35 | 5.930 | \(8.13\times 10^{-4}\) | \(3.4847\times 10^{-5}\) |
| 0.28 | 18.10 | \(1.59\times 10^{-3}\) | \(3.4847\times 10^{-5}\) |

The small difference at \(\ell=0.60\) is overlap between periodic copies of the bump. From \(\ell=0.45\) down, \(\mathcal{R}_\star\cdot\ell^3\) is constant to five digits. Spectral tail beyond \(N/3\) was below \(10^{-9}\).

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack10_localized_bump.py
PYTHONPATH=scripts python3 scripts/ns_attacks/attack10_localized_bump.py --quick
PYTHONPATH=scripts python3 scripts/ns_attacks/attack10_localized_bump.py \
  --n 64 --out results/attack10_localized_bump.json
```

---

## Other corrections to the note

1. **Kill-table row “\(D_s=0\) and \(T_c>0\)” can never happen.** \(D_s=0\) forces a single shell, and then \(\Lambda=\alpha\) makes every weight \(\lambda_k(\lambda_k-\Lambda)\) vanish, so \(T_c=0\). That row is the same case as the vacuous row below it. Confirmed on the shear eigenfield \(v=(\sin y,0,0)\): \(D_s\sim 10^{-13}\), \(T_c=0\).

2. **The limit formula for 9B holds only for the best choice of \(z\).** The limit of \(\mathcal{R}_\star(w_\alpha+\varepsilon z_\beta)\) is
   \[
   \frac{\beta\,\tau^2}{\alpha^2\|z\|_2^2\|w\|_2^4},
   \qquad
   \tau=-\mathrm{Re}\langle\Pi_\beta B(w,w),z\rangle.
   \]
   It equals \(K_{\alpha,\beta}(w)\) only when \(z\) is chosen along \(\Pi_\beta B(w,w)\) with the right sign; in general it is at most \(K\).

3. **9B is closed by the Sept 20 note.** Its equation (9) gives
   \[
   K_{\alpha,\beta}\le\tfrac34 r^2\bigl(1-r/4\bigr)\le 16/9,
   \]
   with \(2/3\) attained by the shear example. The near-shell lane cannot produce unbounded \(\mathcal{R}_\star\). The older “live kill attempt” entry is outdated.

---

## What still stands / what is dead

**Stands**

- Centered-drift identity \(\Lambda'=(2/X)(T_c-\nu D_s)\).
- Equivalent forms of \(D_s\).
- Two-shell formula.
- Homogeneity laws (amplitude invariance of \(\mathcal{R}_\star\); Fourier-dilation invariance on the torus).

**Dead**

- Using a single universal constant bounding \(\mathcal{R}_\star\) as a static closure.

Any repaired version has to balance the units, which means replacing \(\|v\|_2^2\) with a critical norm (\(\dot H^{1/2}\)-type). The result would be a **conditional-regularity** statement, not an unconditional one.

---

## Frontier

This is the static kill that the later desk already moved past.

| Board | Status |
|-------|--------|
| Static uniform \(\sup\mathcal{R}_\star<\infty\) | **KILLED** (this attack) |
| Restricted near-shell \(K_{\alpha,\beta}\) | Closed as a bound \(\le 16/9\); not a ★ close |
| Dynamic question | Can NS maintain a concentrating bump with coherent positive \(T_c\)? |

A static inequality alone cannot rule that out. **NS not solved.** Clay Statement B remains open.

---

## Kill / survive table (corrected)

| Outcome | Verdict |
|---------|---------|
| Localized bump \(v_\ell\) with \(\mathcal{R}_\star\sim\ell^{-3}\to\infty\) | **★ dead** as a static bound (this attack) |
| \(D_s=0\) (one Fourier shell) | Forces \(T_c=0\) — **vacuous**, not a separate kill row |
| Pure single shell, both sides vanish | vacuous — not a kill |
| AP packet fan (9A) / fixed-gap ensemble (9C) | Did not kill ★ — no physical concentration |
| Exact-shell + closing (9B) | Restricted family; \(K\le 16/9\); **not** a ★ kill |
| Every shape has \(\mathcal{R}_\star\le K\) | **FALSE** — no such finite \(K\) |
| A critical-norm repair of ★ | Conditional regularity, **not** the original lemma |

**NS not solved.**
