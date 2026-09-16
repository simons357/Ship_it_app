# SND persistence — lower comparison, indexed paraproduct, direct test

**Date:** 16 September 2026  
**Clarification:** [`SND-CLARIFICATION.md`](./SND-CLARIFICATION.md)  
**Do not repair Theorem H.** \(A.2\) retained. \(A.3\) is the wrong Dini side.

**Verdict:** the boxed persistence statement is **false** as written. It already fails on explicit unforced shear solutions (\(F_j=0\)), so the failure is not a missing paraproduct estimate. The paraproduct route with \(A.2\) is separately too crude (\(4^{j_*}\) leftover).

Ordinary NS / Clay B: **not claimed**.

---

## (P) — the statement, verbatim

Fix \(\nu>0\), \(M>0\), \(\rho_*\in(0,1]\). Does there exist \(T=T(M,\nu,\rho_*)>0\) such that every smooth mean-zero divergence-free unforced NS solution on a fixed torus with

\[
X(t)\le M\quad\text{on }[0,T],
\qquad
\rho(0)\ge\rho_*,
\]

satisfies \(\rho(t)\ge\rho_*/2\) on \([0,T]\)?

\(T\) is **not** allowed to depend on \(j_*(0)\), on \(\|\Delta u(0)\|_2\), or on a geometric tail.

---

## A.2 (retained)

Smooth, mean-zero, divergence-free, \(X\le M\):

\[
|F_j|
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{1/2}\mathcal{D}^{1/2},
\]

uniform in \(j\). Hölder \(6,2,3\), Poincaré, \(\mathcal{D}\ge\nu\lambda_1 X\). **STANDARD LEMMA.** Not a persistence theorem.

---

## Exact shells. EXACT

\[
X_j=2^{2j}\|\Delta_j u\|_2^2,
\qquad
F_j=\bigl\langle\Delta_j[(u\cdot\nabla)u],\,\Delta_j u\bigr\rangle,
\qquad
\widetilde D_j=\nu\,2^{2j}\|\nabla\Delta_j u\|_2^2.
\]

\[
\dot X_j=-2\widetilde D_j-2\cdot 4^j F_j.
\]

\(J=\max_j X_j\), \(\rho=J/X\), \(j_*\in\mathrm{argmax}\,X_j\). Frozen partition: \(\widetilde D_j\ge\kappa\nu 4^j X_j\), \(\kappa\in(0,1]\).

---

## Correct Dini side. EXACT

\(J\) is a max of finitely many smooth functions. Envelope:

\[
D_-J(t)\ge\min_{j\in\mathrm{argmax}(t)}\dot X_j(t).
\]

\(X\) is \(C^1\) on \(\{X>0\}\). Quotient, lower Dini:

\[
D_-\rho
\ge
\frac{D_-J}{X}-\rho\frac{D^+X}{X}.
\]

A floor needs this **lower** bound. \(A.3\) bounded \(D^+\rho\) from above. That is a ceiling. **Wrong side.**

From the shell equation,

\[
\dot X_{j_*}
\ge
-2\widetilde D_{j_*}
-2\cdot 4^{j_*}\,|F_{j_*}|.
\]

Positive \(F_{j_*}\) drains the peak. An **upper** bound on \(F_{j_*}\) is the nonlinear ingredient of a lower bound on \(\dot X_{j_*}\).

For \(D^+X\): the enstrophy identity

\[
\tfrac12\dot X=-\mathcal{D}-\langle(u\cdot\nabla)u,\Delta u\rangle
\]

and Hölder give \(\langle(u\cdot\nabla)u,\Delta u\rangle\ge -C X^{3/2}\), hence

\[
\dot X\le -2\mathcal{D}+2C X^{3/2}\le 2C M^{3/2}
\]

under \(X\le M\). That upper bound on \(\dot X\) is the right direction for \(-\rho D^+X/X\) in a lower bound on \(D_-\rho\). It does **not** need Bony. It also does not stop a high peak from dying.

---

## Indexed paraproduct of \(F_j\). EXACT as a split

Fix an overlap integer \(N\ge 2\) (e.g. \(N=2\) or \(N=4\)) and freeze it with the LP partition. Write \(u=\sum_k\Delta_k u\). Then

\[
F_j=F_j^{\mathrm{LH}}+F_j^{\mathrm{HL}}+F_j^{\mathrm{HH}},
\]

\[
\begin{aligned}
F_j^{\mathrm{LH}}
&=
\sum_{k\le j-N}
\bigl\langle
\Delta_j\bigl[(\Delta_k u\cdot\nabla)u\bigr],\,
\Delta_j u
\bigr\rangle,
\\
F_j^{\mathrm{HL}}
&=
\sum_{k\ge j+N}
\bigl\langle
\Delta_j\bigl[(\Delta_k u\cdot\nabla)u\bigr],\,
\Delta_j u
\bigr\rangle,
\\
F_j^{\mathrm{HH}}
&=
\sum_{|k-j|<N}
\bigl\langle
\Delta_j\bigl[(\Delta_k u\cdot\nabla)u\bigr],\,
\Delta_j u
\bigr\rangle.
\end{aligned}
\]

The three ranges of \(k\) **exhaust** \(\mathbb{Z}\). No unquantified \(j'\). The inner \(u\) may still be split as \(S_{j-N}u+\Delta_{\mathrm{near}}u+u_{\mathrm{UV}}\) if a later estimate needs it; any such split must keep the same \(N\).

This is the decomposition Theorem H gestured at and did not index. It is **not** by itself an estimate.

### What a closing estimate would have to do

After multiplying by \(4^{j}\), the drain term is \(4^{j}|F_j|\). Viscosity on the peak is \(\widetilde D_j\gtrsim\nu 4^{j} J\). A useful bound is

\[
4^{j}|F_j|
\le
\theta\nu 4^{j} J
+
R(M,\nu,\rho),
\qquad
\theta<1,
\]

with \(R\) independent of \(j\), or depending on \(j\) more weakly than \(4^{j}\). \(A.2\) gives \(4^{j}|F_j|\le C 4^{j}\sqrt{M/\nu}\,X^{1/2}\mathcal{D}^{1/2}\), which **grows** in \(j\). That is the **paraproduct obstruction** if one tries to close (P) with \(A.2\): the leftover \(4^{j_*}\) is unbounded at fixed \(M\) (enstrophy may sit in an arbitrarily high shell).

Kato–Ponce of the form \(|F_j|\le C\|\nabla u\|_\infty\,2^{-2j}X_j\) absorbs \(4^{j}\) into \(\|\nabla u\|_\infty\), which is BKM, not (P). **Do not insert that to “repair” (P).**

---

## Direct test of (P)

### Family H — high peak, many lower shells, \(F\equiv 0\)

Same shear class as the Theorem H counterexample, **peak at high frequency**.

Fix \(\rho_*\in(0,1)\), integer \(L\ge 3\) with \(1/(L-1)<\rho_*/2\) and \(\rho_*>1/L\), and integer \(K\) larger than the lower-block frequencies. On \(\mathbb{T}^3\),

\[
u(x,y,z,0)
=
\Bigl(
\sqrt{2a}\;2^{-K}\sin(2^K y)
+
\sum_{\ell=1}^{L-1}\sqrt{2b}\;2^{-\ell}\sin(2^\ell y),
\;0,\;0
\Bigr),
\]

with \(a=\rho_* q\), \(b=(1-\rho_*)q/(L-1)\), \(q\le M\). Then \(X(0)=q\), \(X_K(0)=a\), \(X_\ell(0)=b\) for \(\ell=1,\dots,L-1\), \(j_*(0)=K\), \(\rho(0)=\rho_*\), and \((u\cdot\nabla)u=0\).

The unforced NS solution is the heat factor on each mode: \(X_j(t)=X_j(0)\,e^{-2\nu 4^j t}\). So \(X(t)\le q\le M\) for all \(t\ge 0\), and \(F_j\equiv 0\).

The high peak dies on the timescale \(1/(\nu 4^K)\). Choose \(K\) large enough that this happens while the lower block is still essentially frozen (\(2\nu 4^{L-1}t\ll 1\)). Then \(j_*\) has switched and \(\rho\) sits at the **intermediate plateau**

\[
\rho
\simeq
\frac{1}{L-1}
<
\frac{\rho_*}{2}.
\]

As \(t\to\infty\) the lowest shell wins and \(\rho\to 1\). Statement (P) already failed at the dip. For any candidate \(T(M,\nu,\rho_*)>0\), take \(K\) large enough that the dip occurs in \((0,T)\). **(P) fails** for every \(\rho_*\in(0,1)\).

The endpoint \(\rho_*=1\) is a single occupied shell. Heat keeps \(\rho\equiv 1\). Family H does not address that endpoint; do not relabel “\(\rho(0)=1\) stays near 1 for a uniform time” as (P).

Arithmetic check: `python3 scripts/snd_persistence_test.py`.

This family does not use a paraproduct. The persistence statement is false **before** Bony is attempted.

On Family H the correctly oriented floor is explicit: unique peak, \(F\equiv 0\),

\[
D_-\rho
\ge
-2\nu 4^{j_*}\rho-\rho\frac{\dot X}{X}
\sim
-2\nu 4^{j_*}\rho(1-\rho)
\]

when the rest of the mass is at much lower frequency. The floor is the right Dini side and is **unbounded in \(j_*\)** at fixed \((M,\nu,\rho_*)\). That is why no \(T(M,\nu,\rho_*)\) exists.

### Other families (do not confuse with (P))

| Family | Hits (P)? |
| --- | --- |
| Audit high-**tail** shears (low peak + one high shell) | No. High dies first; low \(\rho\) increases. |
| Amplitude \(u=Aw\) | \(\rho\) invariant; \(X\le M\) caps \(A\). Does not by itself kill (P). |
| Equal shells \(v_L\) with \(\rho(0)=1/L<\rho_*\) | Outside the hypothesis \(\rho(0)\ge\rho_*\). |
| \(\rho_*=1\) heat | \(\rho\equiv 1\). Not a Family-H kill. Different statement. |

---

## What would still be a legitimate replacement (not written)

If \(T\) is allowed to depend on \(j_*(0)\) or on \(\mathcal{D}(0)\), or if one assumes a low peak, (P) becomes a different statement. Do not relabel that as (P). A local persistence result that needs \(\|\nabla u\|_\infty\) or a geometric tail is downstream of BKM, not an answer to the boxed question.

---

## Lock

- Theorem H: withdrawn. Do not repair.  
- \(A.2\): retained.  
- \(A.3\): wrong Dini side; not a floor.  
- Indexed LH / HL / HH split: written, \(k\)-ranges exhaust \(\mathbb{Z}\).  
- Closing \(|F_j|\) with \(A.2\): paraproduct obstruction \(4^{j_*}\).  
- Statement (P): **false** for every \(\rho_*\in(0,1)\), Family H.  
- Conditional local SND-persistence under only \((M,\nu,\rho_*)\): **no**.
