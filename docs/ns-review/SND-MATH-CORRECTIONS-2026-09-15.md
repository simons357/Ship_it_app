# SND reviewer packet — mathematical corrections

**Prepared:** 15 September 2026  
**For:** Jonathan R. Simons and the specialist reviewing the SND packet  
**Status:** packet correction. The manuscript extract of Theorem H remains the **object under review**; this note replaces the packet’s earlier claim that the displayed estimate is proved under \(X\le M\).

**Scope.** Direct audit of the four packet documents as supplied in this conversation. Underlying GitHub and Zenodo files were not re-checked in the audit that produced these calculations, so exact transcription of KEEP manuscripts is not claimed here. The calculations address the **formulas as displayed** in [`THEOREM-H-STATEMENT-AND-PROOF.md`](./THEOREM-H-STATEMENT-AND-PROOF.md).

**Finding.** The packet correctly identified dependence on an a priori enstrophy ceiling. It nevertheless **overstated** the status of the displayed Theorem H. With the displayed definition of \(\Pi_j\), the absolute-value estimate **fails** on smooth shear fields with fixed enstrophy and a fixed spread ratio. Thus “proved under \(X\le M\)” must be replaced. The supplied proof also uses invalid three-dimensional Sobolev embeddings. These are defects **before** any proposed removal of \(M\).

A simpler conditional estimate for the nonlinear term alone is valid; its proof is in §3. It does **not** establish the proposed dominant-shell propagation.

Replacement wording (cover, Theorem H commentary, August addendum):

> In the supplied extract, Theorem H is not established even with \(X\le M\). Its proof drops a viscous tail, uses invalid Sobolev embeddings and does not provide a complete Bony decomposition. The displayed absolute-flux estimate fails on smooth fixed-enstrophy shear fields. A valid \(M\)-dependent bound for the nonlinear shell term can be proved separately, but its usefulness for SND propagation remains to be shown. Any SND floor asserted from time zero must respect the initial spectral distribution. Retain the spectral toolkit and rebuild the required estimate from the exact shell evolution.

---

## 1. The proof changes the quantity being estimated

Introduce distinct names:

\[
F_j=\bigl\langle (u\cdot\nabla)u,\,\Delta_j^2 u\bigr\rangle,\qquad
S_j=\nu\sum_{k>j}2^{2k}\|\Delta_k\nabla u\|_2^2.
\]

The packet defines

\[
\Pi_j=F_j-S_j.
\]

For real self-adjoint Fourier multipliers,

\[
F_j=\bigl\langle\Delta_j[(u\cdot\nabla)u],\,\Delta_j u\bigr\rangle.
\]

The first line of the purported proof identifies \(\Pi_{j_*}\) with this last expression. That **drops \(S_j\)**. A Bony decomposition of \(F_j\) cannot by itself bound \(|F_j-S_j|\).

The sign matters. Because \(S_j\ge 0\), an upper bound on \(F_j\) gives an upper bound on \(\Pi_j\). It does **not** give the displayed **absolute-value** bound.

---

## 2. Explicit counterexample with \(X\le M\)

### Conventions

Work on \((\mathbb{R}/2\pi\mathbb{Z})^3\) with normalized volume, so \(\|\sin(ny)\|_2^2=1/2\). Changing the fixed torus period changes fixed constants, not the divergence below.

Use ordinary smooth Littlewood–Paley multipliers that isolate the dyadic frequencies used here. For completeness, choose a smooth radial cutoff \(\chi\) equal to \(1\) for \(r\le 1/2\) and \(0\) for \(r\ge 1\). Put

\[
\varphi(r)=\chi(r/2)-\chi(r),\qquad
\widehat{\Delta_j u}(k)=\varphi(2^{-j}|k|)\,\widehat u(k).
\]

Then \(\varphi(1)=1\) and \(\varphi(2^\ell)=0\) for every nonzero integer \(\ell\). Each mode of frequency \(2^j\) belongs to exactly its designated block. Include the usual low block for the mean. All fields below have mean zero.

Thus the packet’s enstrophy and dissipation equalities hold **exactly** on this family, even though those equalities require qualification for general fields.

### Field and hypotheses

Fix \(q>0\), \(\nu>0\) and \(0<\rho_0<1\). Choose a fixed integer \(N\) large enough that

\[
\frac{2}{N+2}\le\rho_0.
\]

Set

\[
a=\frac{2q}{N+2},\qquad b=\frac{q}{N+2}.
\]

For an integer \(K>N\), define

\[
u_K(x,y,z)
=
\Bigl(
\sqrt{2a}\,\sin y
+
\sqrt{2b}\sum_{j=1}^{N-1}2^{-j}\sin(2^j y)
+
\sqrt{2b}\,2^{-K}\sin(2^K y),
\ 0,\ 0
\Bigr).
\]

Every field is smooth, periodic, mean zero and divergence free. The velocity points in the \(x\)-direction and depends only on \(y\), so

\[
(u_K\cdot\nabla)u_K=0.
\]

Shell enstrophies:

\[
X_0=a,\qquad X_1=\cdots=X_{N-1}=X_K=b,
\]

with all other shells zero. Consequently

\[
X=a+Nb=q,\qquad J=a,\qquad j_*=0,\qquad
\rho=\frac{2}{N+2}.
\]

All these quantities are independent of \(K\). Taking \(\delta_*=M=q\) satisfies the stated lower and upper enstrophy conditions. If strict inequalities were intended, choose fixed \(\delta_*<q<M\).

### Evaluate both sides

Define

\[
S_K=\nu b\Bigl(\sum_{j=1}^{N-1}4^j+4^K\Bigr).
\]

Then

\[
\mathcal{D}(u_K)=\nu a+S_K,\qquad
\Pi_{j_*}(u_K)=-S_K.
\]

The proposed estimate would require

\[
S_K
\le
C_*\Bigl(\nu a+\sqrt{q(\nu a+S_K)}\Bigr).
\]

But

\[
\frac{S_K}{\nu a+\sqrt{q(\nu a+S_K)}}
\sim
2^K\sqrt{\frac{\nu b}{q}}
\longrightarrow\infty.
\]

Every allowed argument of \(C_*(\nu,\delta_*,M,\rho_0,C_S)\) is fixed. Therefore **no such finite constant exists** for this displayed estimate and these standard fixed blocks.

The construction also persists for the usual overlapping dyadic partitions: separate the mode groups, keep the dominant low group fixed and move a nonzero enstrophy share to arbitrarily high frequency. Fixed overlap constants do not change the quadratic-versus-linear frequency growth.

### Numerical check of the exact formula

With \(\nu=q=M=\delta_*=1\), \(N=20\) and \(\rho_0=0.1\), one has \(J=\rho=1/11\).

| Highest shell \(K\) | Required ratio \(\lvert\Pi_{j_*}\rvert\big/\bigl(\nu\,4^{j_*}J+\sqrt{X\mathcal{D}}\bigr)\) |
| ---: | ---: |
| 24 | \(3.57924234\times 10^{6}\) |
| 28 | \(5.72307770\times 10^{7}\) |
| 32 | \(9.15690113\times 10^{8}\) |

These values were calculated directly from rational shell weights. The asymptotic calculation proves unboundedness; the table only checks the arithmetic.

These are also initial states of **explicit global unforced NS solutions**: multiply each sine coefficient by \(e^{-\nu 4^j t}\). The example is not excluded by asking for genuine NS states. Using fixed \(\delta_*<q<M\) and \(2/(N+2)<\rho_0\), the hypotheses and failure persist for sufficiently small positive times whenever the initial ratio has been chosen beyond a proposed bound.

---

## 3. A correct conditional replacement for the nonlinear term

Let \(u\) be mean-zero, divergence-free and smooth on a fixed torus. Take real self-adjoint dyadic multipliers with uniformly bounded symbols. Define \(X=\|\nabla u\|_2^2\) and \(F_j\) as above.

Hölder with exponents \(6,2,3\) gives

\[
|F_j|
\le
\|u\|_6\,\|\nabla u\|_2\,\|\Delta_j^2 u\|_3
\le
C X^{3/2}.
\]

The last inequality follows from the mean-zero Sobolev/Poincaré inequality and the uniform \(H^1\) multiplier bound. The constant is independent of \(j\). The relevant embeddings are standard (Tao, Sobolev-space notes).

Let \(\lambda_1>0\) be the first nonzero eigenvalue of \(-\Delta\). For \(u\in H^2\),

\[
\mathcal{D}=\nu\|\Delta u\|_2^2\ge\nu\lambda_1 X.
\]

If \(X\le M\), then \(X/\mathcal{D}^{1/2}\le\sqrt{M/(\nu\lambda_1)}\), hence

\[
\boxed{
|F_j|
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,
X^{1/2}\mathcal{D}^{1/2}.
}
\]

This conditional lemma needs **neither** the spread hypothesis **nor** a dominant-shell choice. It extends to the appropriate Sobolev class by approximation.

Legitimate consequences:

\[
\Pi_j
\le
C\sqrt{\frac{M}{\nu\lambda_1}}\,X^{1/2}\mathcal{D}^{1/2},
\]

\[
|\Pi_j|
\le
S_j
+
C\sqrt{\frac{M}{\nu\lambda_1}}\,X^{1/2}\mathcal{D}^{1/2}.
\]

These are **different estimates** from Theorem H. Whether either is useful requires deriving the actual evolution inequality used in Theorem G. They do **not** supply a new propagation theorem.

---

## 4. Invalid embeddings in the supplied proof

Step 2 of the extract asserts

\[
\|u\|_\infty\lesssim M^{1/2},\qquad
\|\nabla u\|_\infty\lesssim \|\Delta u\|_2.
\]

Neither is a general three-dimensional Sobolev inequality. Even after imposing mean zero, \(H^1\) controls \(L^6\), not \(L^\infty\); \(H^2\) does not control the gradient in \(L^\infty\). The stated peak-fraction condition supplies no demonstrated replacement embedding. Without a mean-zero normalization, adding a constant velocity already disproves the first assertion while leaving \(X\) and \(\rho\) unchanged.

A legitimate mean-zero interpolation bound is

\[
\|u\|_\infty
\le
C\|\nabla u\|_2^{1/2}\|\Delta u\|_2^{1/2}
=
C\nu^{-1/4}X^{1/4}\mathcal{D}^{1/4}.
\]

Using this bound would change subsequent powers and must be carried through explicitly. It does **not** repair the missing viscous tail.

(Embeddings and dimensional thresholds: Tao’s Sobolev notes, Exercises 40–41.)

---

## 5. Removing \(M\) also requires an amplitude-scaling check

Even after replacing \(\Pi_j\) by \(F_j\), the proposed right-hand side is **quadratic** in velocity amplitude, while \(F_j\) is **cubic**.

For \(u=Aw\), \(A>0\),

\[
X(Aw)=A^2 X(w),\quad
\mathcal{D}(Aw)=A^2\mathcal{D}(w),\quad
\rho(Aw)=\rho(w),\quad
F_j(Aw)=A^3 F_j(w).
\]

For any admissible spread field with \(F_{j_*}(w)\ne 0\), an amplitude-independent quadratic bound fails as \(A\to\infty\). A lower enstrophy threshold does not stop this rescaling.

Such spread fields can be made explicitly. Start with the two-dimensional stream function, embedded in three dimensions,

\[
\psi=\alpha\cos x+\beta\cos(2y)+\gamma\cos(x+2y),\qquad
w=(\partial_y\psi,-\partial_x\psi,0).
\]

For the low block containing only frequency \((1,0,0)\), direct integration gives \(F_0=\alpha\beta\gamma/2\). Choose \(\alpha=2\) and \(\beta=\gamma\) small. Add sufficiently many modes \(c_m\sin(2^m y)\,e_1\), \(m\ge 3\), with one unit of enstrophy per block. The original low block has enstrophy \(2\) and stays dominant, while its fraction becomes arbitrarily small. These added modes do not alter \(F_0\): their \(y\)-frequencies cannot form the required low-output interaction with the original triad.

Therefore **“remove \(M\) from this same estimate for every spread field” is not an appropriate open target.** A revised estimate needs compatible amplitude powers, another justified restriction, or a dynamical / time-integrated formulation.

---

## 6. A universal SND floor is obstructed at the initial time

For any fixed \(q>0\) and integer \(L\ge 1\), take

\[
v_L(y)
=
\sqrt{\frac{2q}{L}}
\sum_{j=0}^{L-1}2^{-j}\sin(2^j y)\,e_1.
\]

Then

\[
X(0)=q,\qquad X_j(0)=q/L,\qquad \rho(0)=1/L.
\]

These are smooth shear data whose exact unforced NS evolutions are global and satisfy \(X(t)\le q\). The initial peak fraction can nevertheless be arbitrarily small while \(\nu\), \(M=q\), a lower initial-enstrophy threshold and the dyadic convention stay fixed.

Thus no common positive bound \(c_*(\nu,\delta_*,M,C_S)\) can hold from \(t=0\) for every such datum. The same obstruction applies if the infimum excludes \(0\) but includes arbitrarily small positive times, by continuity.

This rules out a **uniform** conclusion with those quantifiers. It does **not** rule out a positive lower bound depending on the particular initial spectrum. The original **solution-by-solution** SND hypothesis must be distinguished from a uniform theorem across all data.

Making a field arbitrarily small in amplitude leaves \(\rho\) unchanged. Consequently small-data existence theory alone cannot supply a universal initial spectral fraction.

An argument showing \(\dot\rho>0\) below a threshold generally produces a barrier involving \(\min\{\rho(0),\text{threshold}\}\). It cannot force an initially smaller ratio above that threshold at time zero.

---

## 7. Additional corrections before specialist circulation

| Packet location | Correction |
| --- | --- |
| August verdict, opening and checklist | \(J/X\ge c_*\) means \(J\ge c_* X\), equivalently \(X\le J/c_*\). The printed \(X\ge c_* J\) is **not** equivalent. For \(0<c_*\le 1\), it already follows trivially from \(J\le X\). The August body is preserved; this erratum is attached. |
| “\(H^1\) is supercritical” / “a derivative short” | Under \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2 t)\), \(\|u_\lambda\|_{\dot H^s}=\lambda^{s-1/2}\|u\|_{\dot H^s}\) in three dimensions. Velocity \(\dot H^{1/2}\) is **critical** and \(H^1\) is **subcritical**. The available **energy** control is supercritical. |
| “Energy class” | Leray–Hopf control is \(L^\infty_t L^2_x\cap L^2_t H^1_x\). It is **not** a uniform-in-time \(H^1\) ceiling. |
| Exact LP equalities for general fields | Usually \(\sum_j 2^{2j}\|\Delta_j u\|_2^2\asymp\|\nabla u\|_2^2\), not equality. Freeze the partition and use equivalence constants, or define exact Fourier-weighted shell energies. |
| Theorem H stated for every \(H^1\) field | \(\mathcal{D}\) need not be finite. Establish any finite estimate for smooth or \(H^2\) fields first, then state exactly what limit or a.e. formulation is intended. |
| Displayed Bony decomposition | As written, \(j'\) is unquantified, low–high neighboring output blocks are not fully specified, and the supposed high–low term uses the whole \(u\). High–high-to-low interactions must be assigned explicitly. This is not a complete indexed decomposition. |
| Ring Lemma in the briefing | A “KEEP” label is **not** verification. An elementary band-limited statement is available (below); it **changes the threshold** and must not silently replace the manuscript set. |
| Requested bound \(M=M(\|u_0\|_{H^1})\) | Include viscosity and fixed-domain dependence. For finite-time continuation, a bound finite on each finite interval, allowed to depend on its endpoint \(T\), can suffice; an all-time constant is stronger. |
| Official Statement (B) | Fefferman states **smooth** periodic divergence-free initial data. An \(H^1\) theory may be a route to that result, but it is not the literal wording of the official initial-data assumption. |
| “Naming fraud” | Replace with **definition/claim mismatch** or **mislabeling**. The formulas establish an error; they do not establish intent. |

LP and Bernstein conventions: Visan lecture notes, Appendix A.2.

**Elementary Ring-type statement (scoped).** For band-limited \(\omega\), on

\[
E_c^\infty=\bigl\{|\omega|\ge c\|\omega\|_\infty\bigr\},
\]

Bernstein and

\[
\nabla\xi=\frac{(I-\xi\otimes\xi)\nabla\omega}{|\omega|},\qquad \xi=\omega/|\omega|,
\]

give \(\|\nabla\xi\|_{L^\infty(E_c^\infty)}\le C\lambda/c\). This changes the threshold relative to the manuscript set \(E_c=\{|\omega|\ge c\|\omega\|_2\}\) and should not silently replace it.

---

## 8. The first equation to write for a repaired program

For smooth unforced NS, fixed \(j\), and \(X_j=2^{2j}\|\Delta_j u\|_2^2\), the exact shell equation is

\[
\boxed{
\frac12\dot X_j
+
\nu\,2^{2j}\|\nabla\Delta_j u\|_2^2
=
-2^{2j} F_j.
}
\]

It follows by applying \(\Delta_j\), testing against \(\Delta_j u\) and multiplying by \(2^{2j}\). Incompressibility removes pressure. This specifies the nonlinear quantity, sign, derivative weight and viscous term **before** any estimate is attempted.

Derive the desired \(J/X\) evolution from this equation, handling switches of the maximizing shell with an appropriate comparison argument. Only then select the estimate that the propagation proof actually needs. Test it against:

1. the high-tail shear family of §2;
2. amplitude rescaling (§5);
3. many equal-enstrophy shells (§6).

This is a concrete way to **retain spectral research** while replacing the failed statement.

---

## 9. Public-status verification

The cited public pages were checked. OpenAI’s 8 September announcement presents a forced finite-time singularity result as Statements C and D. Clay’s 11 September announcement acknowledges the announcement and describes its evaluation process; it is not an award notice.

Fefferman’s official formulation distinguishes unforced periodic Statement B from the breakdown alternatives allowing a smooth force. The forced announcement does not itself prove unforced B. This audit does not examine the announced proof or its Lean formalization.

---

## 10. Packet instructions

- Preserve the original manuscript extract as an extract, clearly marked as the object under review.
- Use the boxed replacement wording on the cover sheet, in Theorem H **commentary** (not inside the extract), and as an addendum to the historical August verdict.
- Do not edit the 25 August body except to attach this erratum and the \(X\ge c_* J\) sign correction.
