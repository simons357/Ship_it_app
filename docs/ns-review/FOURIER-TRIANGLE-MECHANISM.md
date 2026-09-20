# Fourier-triangle mechanism — reconstruction and first missing implication

**20 September 2026.**  
Reconstruction of the seated triad geometry.  
Do not repair Theorem H. Do not unfreeze exact-shell 9D. Do not restore unrestricted \(\star\).  
Ordinary NS / Clay B: **not claimed**.

Sources (other branches; identities not re-proved here):

- `docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md` on `origin/cursor/exact-shell-9d-audit-a7a2`
- `docs/ATTACK-9D-FULL-SUPPORT-BOUND.md` on `origin/cursor/exact-shell-claimed-lock-cec0`
- `docs/NEED-STAR-HH-L-DUAL.md` on `origin/cursor/exact-shell-9d-audit-a7a2`
- `docs/ns-snd-final-status/CENTERED-DRIFT.md` on `origin/cursor/centered-ns-recovery-b5c1`

Arithmetic for the **EXACT** pair-geometry lines: `python3 scripts/fourier_triangle_identities.py`.

The phrases *equal-length cancellation*, *unequal-length defect*, and *I₃ prime restrictions* are **not** seated names on those branches. They are used here as reconstruction labels. They are not new theorems.

---

## Tag legend

| Tag | Meaning on this page |
| --- | --- |
| **EXACT** | Algebraic identity. Keep. |
| **CLAIMED** | Written derivation on the exact-shell page. Specialist sign pending. Not a time-dependent bound. |
| **NUMERICAL** | Sample / sweep. Consistency only. |
| **ILLUSTRATIVE** | Motion picture of a single triad. Not a sum. Not a flow. |
| **OPEN** | Named missing implication. |
| **DEAD** | Already killed. Do not revive. |
| **NOT SEATED** | Name does not exist as a defined object in the NS attack files. |

---

## 1. Setup. EXACT

Normalized torus \(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\). Mean-zero, divergence-free:

\[
v(x)=\sum_{k\in\mathbb{Z}^3\setminus\{0\}} v_k e^{ik\cdot x},
\qquad
k\cdot v_k=0,
\qquad
v_{-k}=\overline{v_k}.
\]

Stokes operator and Leray projector:

\[
A=-P\Delta,
\qquad
(Av)_k=\lambda_k v_k,
\qquad
\lambda_k=|k|^2,
\qquad
P_k=I-\frac{k\otimes k}{|k|^2}.
\]

Bilinear term:

\[
B(v,v)=P[(v\cdot\nabla)v],
\qquad
\widehat{B}_k
=
i\,P_k\sum_{p+q=k}(q\cdot v_p)v_q.
\]

Because \(p\cdot v_p=0\),

\[
q\cdot v_p=(k-p)\cdot v_p=k\cdot v_p,
\]

so

\[
\widehat{B}_k
=
i\,P_k\sum_{p+q=k}(k\cdot v_p)v_q.
\]

Linear moments:

\[
E=\|v\|_2^2,\quad
X=\|A^{1/2}v\|_2^2,\quad
Y=\|Av\|_2^2,\quad
Z=\|A^{3/2}v\|_2^2,\quad
\Lambda=Y/X.
\]

\[
D_s=Z-\Lambda Y=\|(A-\Lambda)A^{1/2}v\|_2^2=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2\ge 0.
\]

Do not invent a second \(D_s\).

---

## 2. One triangle. EXACT

A Fourier triangle is an ordered lattice triple \((p,q,k)\) with \(p+q=k\) and \(p,q,k\neq 0\).

**Shell placement.** Input eigenvalues \(\lambda_p=|p|^2\), \(\lambda_q=|q|^2\); output \(\lambda_k=|k|^2\). On one input shell, \(|p|^2=|q|^2=\alpha\) and \(|k|^2=\beta\). Then \(\beta\le 4\alpha\), otherwise no pairs and \(\Pi_\beta B=0\). \(\Pi_\beta\) is the exact lattice sphere \(\{|k|^2=\beta\}\), not a dyadic annulus.

**Divergence-free polarizations.** \(v_p\in p^\perp\subset\mathbb{C}^3\). An orthonormal real basis \(e_1,e_2\) of \(p^\perp\) gives

\[
v_p
=
a_p\bigl(\cos\psi\,e^{i\phi_1}e_1+\sin\psi\,e^{i\phi_2}e_2\bigr).
\]

Linear polarization is the slice \(\phi_1=\phi_2\). The seated estimates that use only \(|v_p|\) already include independent complex coefficients. The three angles per mode are **not** a global “9-dimensional configuration space.”

**Leray on the output.** Raw piece \(i(q\cdot v_p)v_q\); then \(P_k\). In-plane components along \(k\) are killed. The residual lives in \(k^\perp\).

---

## 3. Equal-length cancellation. EXACT (geometry); CLAIMED (kernel bound)

Reconstruction name for the seated equal-input-shell geometry.

If \(|p|^2=|q|^2=\alpha\) and \(k=p+q\), \(|k|^2=\beta\), then

\[
k\cdot p=k\cdot q=\frac{\beta}{2},
\qquad
|k_\perp|^2
=
\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr).
\]

Because \(v_p\perp p\),

\[
|k\cdot v_p|
\le
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}\,|v_p|.
\]

**Half-symmetrization.** EXACT as a complex-vector identity for \(p\neq q\): the involution \((p,q)\leftrightarrow(q,p)\) uses no conjugation, and

\[
\sum_{p+q=k}(q\cdot v_p)v_q
=
\frac12\sum_{p+q=k}\bigl[(q\cdot v_p)v_q+(p\cdot v_q)v_p\bigr].
\]

The diagonal \(p=q\) forces \(\beta=4\alpha\), where the geometric factor \(\gamma=\sqrt{\beta(1-\beta/(4\alpha))}\) vanishes.

**In-plane cancel after \(P_k\).** CLAIMED on the exact-shell page: after \(P_k\), the in-plane parts cancel by the real geometry of \(k,p,q\). The residual is \(\zeta e_\perp\) with \(e_\perp\perp k\) real unit and \(\zeta\in\mathbb{C}\). Hermitian Cauchy–Schwarz then gives the pair bound

\[
\bigl|P_k\bigl[(q\cdot v_p)v_q+(p\cdot v_q)v_p\bigr]\bigr|
\le
\gamma\,|v_p|\,|v_q|.
\]

That pair bound is the step that is supposed to remove occupancy on **one input shell**. It is **CLAIMED**, not the time-dependent bound. Independent specialist review of the kernel identity, the Hermitian residual, the factor \(3/4\), and the weighted incidence (factor \(3\)) remains pending.

If that pair bound and the factor-\(3\) count both hold, the one-variable maximum is

\[
K_{\alpha,\beta}(w)\le\frac{16}{9},
\qquad
K_{\alpha,\beta}(w)
=
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4},
\quad Aw=\alpha w.
\]

**CLAIMED. Single input shell. Not a flow invariant. Not unrestricted \(\star\). Not regularity.**

---

## 4. Unequal-length defect. EXACT as a mismatch; not a named lemma

Reconstruction name. The phrase is not on the source branches.

If \(|p|^2\neq|q|^2\), then \(k\cdot p\neq\beta/2\) in general, and

\[
k\cdot p=\frac{|k|^2+|p|^2-|q|^2}{2}.
\]

The two legs are no longer interchangeable. Half-symmetrization is still an algebraic identity of the convolution, but the **in-plane cancel** used on the exact-shell page uses \(k\cdot p=k\cdot q=\beta/2\). That geometric cancellation is **not available** for unequal-length legs.

Two-shell closed form of \(D_s\) still sits (EXACT):

\[
D_s
=
\frac{\alpha\beta(\alpha-\beta)^2\,e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

Gap-cancel in the **signed** quotient also sits (EXACT) on exactly two shells \(\alpha>\beta\):

\[
T_c
=
(\alpha-\beta)\frac{\alpha\beta E}{X}\,T_\alpha
=
-(\alpha-\beta)\frac{\alpha\beta E}{X}\,T_\beta.
\]

The gap \((\alpha-\beta)\) cancels in \(\mathcal{R}_\star\). That is a two-shell identity. It is **not** the equal-length in-plane cancel, and it is **not** a bound.

Unsigned Cauchy–Schwarz on the low output hides occupancy \(s\):

\[
|T_\beta|
\le
\sqrt{\beta}\,E\sqrt{s\,e_\beta}.
\]

That is the operational defect when the equal-length geometry is dropped or the sum is taken absolutely: the count of active keys comes back.

---

## 5. Phase-dependent signed transfer. EXACT

Keep \(\mathrm{Im}\). Never replace by an absolute value if the object is \(T_c\).

\[
T_k(v)
=
-\mathrm{Re}\bigl(\widehat B_k\cdot\overline{v_k}\bigr)
=
\sum_{p+q=k}
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

\[
\sum_k T_k=0,
\qquad
N=\sum_k\lambda_k T_k,
\qquad
M=\sum_k\lambda_k^2 T_k,
\qquad
T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]

Ordered-triad form:

\[
T_c
=
\sum_{p+q=k}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Phases enter only through that imaginary part. Reversing \(v\mapsto -v\) sends \(T_c\mapsto -T_c\). Stretching and anti-stretching are the same geometry with opposite sign.

On two-shell HH→L (high inputs on \(\alpha\), output on \(\beta\)):

\[
\mathcal{S}_\star
=
T_\beta^{\mathrm{HH}\to\mathrm{L}}
=
\sum_{\substack{p+q=k\\|p|^2=|q|^2=\alpha\\|k|^2=\beta}}
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

This is the seated signed dual. It is **not** named \(I_3\).

---

## 6. What is numerical, and what is only a picture

**NUMERICAL (do not cash as \(C_0\)).** Grow-\(s\) maxima, aligned 9B samples, printed ratios \(\approx 0.456\), \(0.641\), \(0.610\). The exact three-shear identity \(K_{1,2}=2/3\) is **EXACT**, not a sweep; it sits strictly under \(16/9\) and is a floor, not a ceiling.

**ILLUSTRATIVE.** A single triad with a chosen phase can be drawn so that \(\mathrm{Im}(\cdots)\) is positive and energy leaves the high shell. That picture is legal. It is not the sum over all \((p,q,k)\), and it is not the Navier–Stokes orbit of that field. Do not promote a drawn triangle to a bound.

---

## 7. Where the geometry is lost

Three successive losses. Only the first is optional.

### 7.1 Sum, drop the sign

The complete object is the signed sum \(T_c\). Replacing \(\mathrm{Im}\) by \(|\cdot|\) is **not** an identity. It returns occupancy \(s\) (unsigned CS). Equal-length in-plane cancel, even if granted per pair, does not survive that replacement: opposite-phase pairs that cancelled are counted as positive.

This is already named on the Need★ page: cheap CS hides \(s\). Same hole as \(K\le 16s\).

### 7.2 Sum, keep the sign, leave one shell

If the field is supported on one input shell, the CLAIMED pair bound plus the factor-\(3\) count would give \(K\le 16/9\). That still does **not** control a general multi-shell field. The growing-layer family \(v_n\) is multi-shell and kills unrestricted \(\sup\mathcal{R}_\star<\infty\) (**DEAD**). Exact-shell \(16/9\) does not contradict \(v_n\) and does not repair \(\star\).

### 7.3 Evolve

EXACT along a classical solution:

\[
\Lambda'=\frac{2}{X}(T_c-\nu D_s).
\]

This is a definition / identity check. It is not a bound on \(T_c\).

Navier–Stokes does not preserve one-shell or two-shell support. A triangle that cancelled at \(t=0\) is not a triangle that stays cancelled. The flow populates other lattice spheres. Instantaneous exact-shell geometry is **not** an invariant of the trajectory (exact-shell specialist Q19). It does not feed BKM or \(\int|Au|_2^2\,dt\) (Q20).

So: per-triangle geometry can sit, and still be insufficient once the interactions are summed over the lattice and evolved in time.

---

## 8. I₃ prime restrictions. NOT SEATED

Repo-wide search of the NS attack files finds **no** object named \(I_3\), \(I_3'\), or “prime restriction” inside the Fourier-triangle identities.

Closest seated or proposed objects, **none of which is \(I_3\)**:

| Object | What it is | Status |
| --- | --- | --- |
| \(\mathcal{S}_\star\) | signed HH→L Im-sum | EXACT as a definition; Need★ bound **OPEN** |
| Incidence \(I\) | Route A continuum closure count | Hyp-ST★ conditional; lattice transfer X1–X4/X6 **MISSING** |
| Factor-\(3\) count | \(\sum_{\|k\|^2=\beta}c_k^2\le 3M^2\) | CLAIMED on one input shell; not Ring / Borromean |
| \(\mathcal{I}_\Lambda\) | proposed CS partner of \(D_s\) on the centered-drift tape | **not defined** as a seated formula on the identity page |
| Q6 / inverse-GCD / primes | arithmetic book | **off this track** |

If “I₃ prime restrictions” means *restrict Fourier support to prime frequencies, or to prime-indexed shells*, that is a **support thinning**. It can only decrease occupancy \(s\). It does not restore in-plane cancel for unequal-length legs, does not keep \(\mathrm{Im}\) from being dropped, and does not keep the flow on one shell.

Therefore, inside this mechanism, prime restrictions **do not imply** the time-dependent bound below. They are not a missing identity that was omitted from §1–§5. They are a different book, or an unnamed extra hypothesis that still leaves the same implication open.

Do not import Ring / Borromean / Q6 as a substitute for the signed sum.

---

## 9. First missing implication to the time-dependent bound

Seated identities already reach the instantaneous budget and the ODE for \(\Lambda\):

\[
\Lambda'=\frac{2}{X}(T_c-\nu D_s).
\]

The **target** (OPEN; centered-drift tape), along a classical solution, is

\[
\boxed{
T_c
\le
\theta\nu D_s
+K(t)X,
\qquad
\theta\in[0,1),\quad
K\in L^1_{\mathrm{loc}}(0,T),
}
\]

with \(K\) controlled by energy-class quantities, **not** by \(\|\nabla u\|_\infty\), \(H^1\) ceilings, or BKM. If that sits, \(\Lambda'\le 2K\) and \(X\le\|u\|_2^2\Lambda\) give the usual Gronwall on \(\log\Lambda\). That last step is standard algebra **after** the estimate.

**First missing implication.**

\[
\bigl\{\text{per-triangle geometry, §§2–5}\bigr\}
\quad\not\Longrightarrow\quad
\bigl\{T_c\le\theta\nu D_s+K(t)X\text{ along the flow}\bigr\}.
\]

Why the arrow fails, in order:

1. The useful cancel is **equal-length** and **signed**. The flow’s \(T_c\) sums every length pair.
2. Absolute-value majorants reintroduce occupancy \(s\).
3. The CLAIMED \(K\le 16/9\) is one input shell, instantaneous, not a trajectory.
4. Unrestricted \(\mathcal{R}_\star\) is **DEAD** on \(v_n\). Need★ cannot repair that box.
5. Need★ itself — \(\lvert\mathcal{S}_\star\rvert\le C(\alpha/\sqrt{\beta})\,e_\alpha\sqrt{e_\beta}\) — is still **OPEN**, and even if seated it is two-shell and instantaneous.
6. Prime / I₃ restrictions, were they imposed, only thin \(s\). They do not write \(K(t)\).

So the first unproved arrow is not “more triangle algebra.” It is the passage from the signed, length-sensitive sum to a **useful** remainder \(K(t)\) that survives evolution. That is the centered-drift estimate. It is independent of C10 and of SND persistence. Filling it with \(\|\nabla u\|_\infty\) is BKM, not this implication.

---

## Lock

- Per-triangle geometry, Leray, polarizations, signed \(T_k\), \(D_s\), \(T_c\), \(\Lambda'\): **EXACT**. Preserve.
- Equal-length in-plane cancel + \(K\le 16/9\): **CLAIMED**, one shell. Frozen. Not a close.
- Unequal-length defect: reconstruction name for the missing cancel when \(|p|\neq|q|\), and for unsigned occupancy.
- \(I_3\) prime restrictions: **NOT SEATED**. Do not invent. Do not use primes as an NS remainder.
- Unrestricted \(\star\): **DEAD**.
- First missing implication: triangle geometry \(\not\Rightarrow\) \(T_c\le\theta\nu D_s+K(t)X\) along the flow.
- NS / Clay B: **OPEN**.
