# Lemma★ — canonical working statement

**Date:** 10 September 2026  
**Status:** **OPEN.** Working foundation with [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md). **NS is not solved.**

Older proof attempts belong in the **annotated archive**, not in this file. See [`ARCHIVE_OLDER_LEMMA_STAR_PROOF.md`](./ARCHIVE_OLDER_LEMMA_STAR_PROOF.md).

---

## Central target

For nonzero, mean-zero, divergence-free \(v\) on \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\),
\[
A=-P\Delta,\quad
B(v,v)=P[(v\cdot\nabla)v],
\]
\[
E=\|v\|_2^2,\quad
X=\|A^{1/2}v\|_2^2,\quad
Y=\|Av\|_2^2,\quad
Z=\|A^{3/2}v\|_2^2,\quad
\Lambda=Y/X,
\]
\[
D_s=Z-\frac{Y^2}{X}=\|(A-\Lambda)A^{1/2}v\|_2^2,\qquad
T_c=-\bigl\langle B(v,v),\,A(A-\Lambda)v\bigr\rangle.
\]

**Lemma★ (shape form):**
\[
\boxed{
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,
D_s(v)\,
E(v)\,
Y(v)
}
\]
for some finite geometric \(C_{\mathrm{geom}}\), all such \(v\). Equivalently, for \(D_s>0\),
\[
\mathcal R_\star(v)
=\frac{(T_c(v)_+)^2}{D_s(v)\,E(v)\,Y(v)},
\qquad
\sup_v\mathcal R_\star(v)<\infty.
\]

Amplitude reduction (\(u=av\)), spectral identities, and viscosity packaging
\[
T_c(u)\le\theta\nu D_s(u)+C_0(\theta)\,\nu^{-1}E(u)Y(u),
\qquad
C_{\mathrm{geom}}=4\theta\,C_0(\theta),
\]
**agree** with this target. \(C_{\mathrm{geom}}\) depends only on the fixed geometry and normalization — not amplitude, Fourier support, shell count, or viscosity.

If \(D_s=0\), the field is one shell and \(T_c=0\). Not a kill.

Five-lane drill record (Attacks 1–5 only; 9A–9D are later): [`docs/ns-recovery/FIVE-LANE-DISCUSSION-AND-MATH.md`](../../ns-recovery/FIVE-LANE-DISCUSSION-AND-MATH.md).

---

## Four corrections

### 1. The older “missing inequality” is false as a universal estimate

It proposes
\[
|T_c(u)|\le C\|u\|_2\,X(u)^{3/2}.
\]
Under \(u=av\): left side scales as \(a^3\), right side as \(a^4\) (\(\|u\|_2\sim a\), \(X\sim a^2\), \(X^{3/2}\sim a^3\)). If \(T_c(v)\neq 0\), take \(a\to 0\): the claimed bound fails. **Discard this route by algebra.**

(The homogeneous \(C_*\) form \(|T_c|\le C_* X^{3/2}\Lambda\) is a different object: both sides scale as \(a^3\). Pre-Young \(|T_c|\le C\|u\|_2 X\Lambda\) is also degree 3. Neither is proved; the \(\|u\|_2 X^{3/2}\) product is not even a candidate.)

### 2. Implication, not equivalence, with global regularity

**Supported:** Lemma★ \(\Rightarrow\) no finite-time blowup of \(\Lambda\) in this packaging \(\Rightarrow\) global regularity on \(\mathbb T^3\) in this packaging.

**Not supported:** “Lemma★ is equivalent to global regularity.” There is no converse in these files showing that global regularity would force \(\sup\mathcal R_\star<\infty\) over every smooth field.

### 3. Positive part vs \(T_c^2\) on all fields

\[
T_c(-v)=-T_c(v),\qquad D_s(-v)=D_s(v),\quad E(-v)=E(v),\quad Y(-v)=Y(v).
\]
A universal bound on \((T_c_+)^2\) is therefore **equivalent** to a universal bound on \(T_c^2\). A large **negative** \(T_c\) deserves attention: reverse the field and it becomes positive. Testing only \((T_c)_+\) on a sample, without checking \(-v\), can hide a stretching counterexample.

### 4. Older “Section 4” is not a theorem

The older proof attempt’s Section 4 does **not** establish its advertised claim. An opening remainder involving \(\|\nabla u\|_\infty^2 X\) is followed by incomplete estimates and then replaced by a different conditional statement. The label **“proved” cannot apply** to that opening claim. Keep that text as an annotated archive only.

---

## Near-shell precision

\[
\lim_{\varepsilon\to 0}\mathcal R_\star(w+\varepsilon z_\beta)=K_{\alpha,\beta}(w)
\]
holds only for an **appropriately aligned, sign-selected** perturbation \(z_\beta\parallel\Pi_\beta B(w,w)\) (stretch orientation). For arbitrary \(z_\beta\), the limit depends on the projection of \(z_\beta\) against \(B(w,w)\). \(K_{\alpha,\beta}\) tests a **restricted family**, not the full lemma.

---

## Remaining target

Establish a uniform bound on \(\mathcal R_\star\), **or** construct a family on which it **diverges**.

One large **finite** value only **raises** the required \(C_{\mathrm{geom}}\). It does **not** disprove existence of a finite constant.

Fixed-output \(\Theta(m^2)\) 9D is excluded (\(K\le 16s\)). Natural same-shell and AP fans did not kill ★.

**NS not solved.**
