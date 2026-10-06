# SCHEME B spatial attempt — toward (B1)

6 October 2026.
**Proof attempt. First stuck step marked. Not (17).**

Parent: [`SCHEME-B-SHELL-POT-2026-10-06.md`](SCHEME-B-SHELL-POT-2026-10-06.md).
Template: [`DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md`](DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md) (SC)–(SB), (11).

---

## Target

\[
\lvert\mathcal T_{\mathrm{sc}}(u)\rvert
\le
C_\star\,X\sqrt{Y}.
\tag{B1}
\]

---

## Step 1 — signed mixed channels (EXACT bookkeeping)

Partition scalene interactions by ordered donor shells
\((\alpha,\beta)\) with \(\alpha\neq\beta\) and receiver mode
\(k\) on shell \(\gamma\notin\{\alpha,\beta\}\),
\(p+q=k\). Write the assembled mixed channel
(polarization details as in (SC); magnitudes only after
the sum)

\[
j_{\star\leftarrow\alpha\beta}
=\sum_{\substack{p+q=k\\ \lvert p\rvert^2=\alpha,\ \lvert q\rvert^2=\beta\\ \gamma=\lvert k\rvert^2\notin\{\alpha,\beta\}}}
\text{(signed monomial in \(u_p,u_q,u_k\))}.
\]

Then \(\mathcal T_{\mathrm{sc}}\) is a finite linear
combination of these channels with radius-difference
weights from (7) (factors \(\lvert\gamma-\alpha\rvert\),
etc.). No shape index appears.

---

## Step 2 — Plancherel pot for one donor pair (EXACT / STANDARD)

Set \(r_p=\lvert u_p\rvert\) on shell \(\alpha\),
\(s_q=\lvert u_q\rvert\) on shell \(\beta\),
\(L_k=\sum_{p+q=k}r_p s_q\). Regardless of output
shell,

\[
\sum_{k\in\mathbb Z^3}L_k^2
=\Bigl(\sum_p r_p^2\Bigr)\Bigl(\sum_q s_q^2\Bigr)
=e_\alpha e_\beta.
\tag{B-P}
\]

Restricting the sum to scalene receivers
\(\gamma\notin\{\alpha,\beta\}\) only decreases the
left side. After polarization Cauchy–Schwarz as in (SB)
(pair coefficient \(\le r_p s_q\)),

\[
\sum_{\gamma\notin\{\alpha,\beta\}}
\sum_{\lvert k\rvert^2=\gamma}\lvert V_k^{\alpha\beta}\rvert^2
\le
C_{\mathrm{pol}}\,e_\alpha e_\beta
\tag{B-V}
\]

with \(C_{\mathrm{pol}}\) absolute (equal-input case gives
\(3\) in (8); distinct-input spot checks
\(\sum L_k^2/(e_\alpha e_\beta)\le 0.91\) on output
shells). One global CS against receivers then yields

\[
\lvert j_{\star\leftarrow\alpha\beta}\rvert
\le
C_j\sqrt{e_\alpha e_\beta}\,\sqrt{E_{\mathrm{rec}}^{\alpha\beta}},
\tag{B-J}
\]

where \(E_{\mathrm{rec}}^{\alpha\beta}\) is the \(\ell^2\) mass
on scalene receiving modes for that donor pair
(\(\le E\)).

**This step does not charge \(\mathrm{touch}(\alpha)\).**

---

## Step 3 — radius weights into enstrophy (STANDARD shape)

Enstrophy production weights receivers by shell label.
Schematically (constants absorb projection / Im factors)

\[
\lvert\mathcal T_{\mathrm{sc}}\rvert
\le
C_T\sum_{\alpha\neq\beta}
w(\alpha,\beta)\,
\sqrt{e_\alpha e_\beta}\,\sqrt{Y_{\mathrm{rec}}^{\alpha\beta}},
\tag{B-W}
\]

where \(w(\alpha,\beta)\) collects radius-difference
factors from (7) after assembly (prototype:
\(w(\alpha,\beta)\lesssim \sqrt{\alpha}+\sqrt{\beta}\),
or a homogeneous degree-\(1/2\) combo), and
\(Y_{\mathrm{rec}}^{\alpha\beta}\le Y\).

Crude close with \(Y_{\mathrm{rec}}\le Y\):

\[
\lvert\mathcal T_{\mathrm{sc}}\rvert
\le
C_T\sqrt{Y}
\sum_{\alpha\neq\beta}
w(\alpha,\beta)\sqrt{e_\alpha e_\beta}.
\tag{B-W'}
\]

---

## Step 4 — FIRST STUCK STEP (collapse the donor sum)

Need

\[
\sum_{\alpha\neq\beta}
w(\alpha,\beta)\sqrt{e_\alpha e_\beta}
\le
C_w\,X
\quad\text{or}\quad
C_w\sqrt{X\cdot(\text{moment})}.
\tag{B-CS}
\]

**What fails naively.** If \(w\equiv 1\), then
\(\sum_{\alpha\neq\beta}\sqrt{e_\alpha e_\beta}
\le(\#\mathrm{shells})\,E\), and \(\#\mathrm{shells}\)
diverges with the Galerkin cutoff — SCHEME A′ in
disguise (sum on shell **pairs** without weights).

**What worked for repeated radius (11).** The equal-input
weight \(g_{\alpha\beta}=\sqrt{\beta(1-\beta/(4\alpha))}\)
summed on output \(\beta\) produced a factor
\(\sim\alpha^{3/2}\) per input shell, then
\(\sum\alpha^{3/2}e_\alpha\le\sqrt{XY}\).

**What is needed here.** A scalene weight
\(w(\alpha,\beta)\) from the true (7)-assembled
factors such that the bilinear form
\(\sum_{\alpha\neq\beta}w(\alpha,\beta)\sqrt{e_\alpha e_\beta}\)
is dominated by \(X\) (or \(\sqrt{X}\) times a controlled
moment already paid by \(\sqrt{Y}\) outside). Candidate
homogeneous accounting:

\[
w(\alpha,\beta)=\sqrt{\alpha\beta}\,?\quad
\text{then }
\sum_{\alpha,\beta}\sqrt{\alpha e_\alpha}\sqrt{\beta e_\beta}
=\Bigl(\sum\sqrt{\alpha e_\alpha}\Bigr)^2,
\]

and \(\sum\sqrt{\alpha e_\alpha}\) is **not** \(\le\sqrt{X}\)
without an extra divergent factor (Cauchy with
\(\sum 1\)).

Weighted fix to try next:

\[
\sum_{\alpha\neq\beta}
\sqrt{\alpha}\,e_\alpha^{1/2}\sqrt{\beta}\,e_\beta^{1/2}
=
\Bigl(\sum\sqrt{\alpha e_\alpha}\Bigr)^2
-\sum\alpha e_\alpha.
\]

Still need \(\sum\sqrt{\alpha e_\alpha}\le C\sqrt{X}\).
False in general: take \(N\) shells with
\(\alpha e_\alpha=1/N\), then \(X=1\) but
\(\sum\sqrt{\alpha e_\alpha}=\sqrt{N}\).

**Stuck conclusion.** With only the crude factor
\(\sqrt{Y_{\mathrm{rec}}}\le\sqrt{Y}\) pulled out of the
donor sum, (B-CS) **does not close** in \(X\) alone.
The repeated-radius miracle was summing the
\(g\)-weights **inside** one input shell before CS.
Scalene needs an analogous **internal** summation —
e.g. fix receiver shell \(\gamma\) and sum donors with
exact-sphere geometry, or keep
\(\sqrt{Y_{\mathrm{rec}}^{\alpha\beta}}\) correlated with
which shells receive from \((\alpha,\beta)\) so that a
double CS hits \(Y\) and \(X\) without
\(\#\mathrm{shells}\).

---

## Step 5 — repaired attack order after the stuck step

1. **Do not** pull \(\sqrt{Y}\) out uniformly.
2. Write
   \[
   \mathcal T_{\mathrm{sc}}
   =\sum_\gamma
   \sum_{\substack{\alpha<\beta\\ \{\alpha,\beta,\gamma\}\mathrm{\ scalene}}}
   \mathcal T_{\alpha\beta\gamma}
   \]
   and, for each fixed \(\gamma\), assemble all donor
   pairs into one receiver-shell channel (as (SC) does
   for one \(\beta\)). Apply (B-V) per \((\alpha,\beta)\)
   **or** a joint donor assembly on shell \(\gamma\).
3. Bound the \(\gamma\)-channel by
   \(C g_\gamma e_\gamma^{1/2}\Phi_\gamma(\{e_\alpha\})\)
   with \(\Phi_\gamma\) charging each \(e_\alpha\) once
   across \(\gamma\).
4. Sum on \(\gamma\) with weights \(\to\sqrt{Y}\) and
   collapse \(\Phi\) with weighted CS \(\to X\).

This is Lemma B-spatial’s remaining core. Steps 1–3
above are the usable reduction; Step 4 is the blank
inside SCHEME B.

---

## STATUS

(B-P) PLANCHEREL DONOR POT: EXACT.
(B-J) ONE-PAIR CHANNEL BOUND: STANDARD GIVEN (B-V).
(B-W') CRUDE PULL-OUT OF √Y: LEADS TO DIVERGENT SHELL-PAIR SUM — NOT A CLOSE.
(B1) FULL SPATIAL: OPEN — STUCK AT COLLAPSING DONOR SUM WITHOUT #SHELLS.
(B2)/(17): BLOCKED ON (B1).
NS NOT SOLVED.
