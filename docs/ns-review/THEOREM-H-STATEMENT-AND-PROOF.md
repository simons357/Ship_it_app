# Theorem H — complete statement, proof, and the \(X\le M\) gap

**Packet item 1 of 3.** If only one document is sent, send this one.  
**Manuscript source:** Zenodo `20518057` mirror, `docs/papers/zenodo-spectral/20518057/98d1b1cc9_NS_UPLOAD_ZENODO.tex` on `origin/cursor/tao-snd-h-panel-a0eb` (older SND framework; superseded as a *claim* by KEEP `10.5281/zenodo.22050976`).  
**Claim-paper overlay:** Zenodo `20405526` (PARK — greened “Theorem H: (SND-C) unconditionally”).  
**Companion audits:** 25 Aug 2026 adversarial verdict ([PR #35](https://github.com/simons357/Ship_it_app/pull/35)); reviewer briefing ([PR #101](https://github.com/simons357/Ship_it_app/pull/101)).

This note extracts the **definitions of [SND] and (SND-C)** and the **statement and proof of Theorem H** as written. Annotations after the extract answer the three questions a specialist asked: where \(X\le M\) enters, whether it can be removed, and what \(c_*\) may depend on.

**This extract is not a claim that Theorem H closes Clay Statement (B).** Statement (B) is unforced global regularity on \(\mathbb{T}^3\) with \(f\equiv 0\). Theorem H as written is a shell-flux bound under an a priori enstrophy ceiling.

---

## 0. What the specialist is being asked to check

1. **[SND]** is a peak-shell occupation hypothesis: \(\inf_t J/X\ge c_*>0\).
2. **(SND-C)** is a different object: a bound on dominant-shell flux \(\Pi_{j_*}\) in a *spread* regime \(\rho\le\rho_0\).
3. **Theorem H** is the manuscript’s proof of (SND-C). Its hypotheses include **\(X\le M\)**.
4. **Theorem G** converts (SND-C) into [SND] with a constant \(c_*\) that still depends on \(M\).
5. The **[SND] \(\Rightarrow\) regularity** arrow (Theorem D) is a separate sketch, not a refereed implication. Equating [SND] with Clay Statement (B) is therefore premature even if the \(X\le M\) gap were closed.

A gap in this chain is a reason to keep the hypotheses honest. It is not a reason to abandon Littlewood–Paley / Bony / Ring research.

---

## 1. Spectral objects (manuscript Definition, § Clay Equivalence)

For \(u\in H^1(\mathbb{T}^3)\) divergence-free:

\[
\begin{aligned}
X_j &= 2^{2j}\|\Delta_j u\|_{L^2}^2 && \text{(shell enstrophy)},\\
X &= \sum_j X_j = \|\nabla u\|_{L^2}^2,\\
J &= \max_j X_j && \text{(dominant shell)},\\
\rho &= J/X\in(0,1] && \text{(concentration ratio)},\\
\mathcal{D} &= \nu\|\Delta u\|_{L^2}^2 = \nu\sum_j 2^{2j}X_j && \text{(enstrophy dissipation)},\\
j_* &= \operatorname{argmax}_j X_j.
\end{aligned}
\]

Shell flux (manuscript Definition):

\[
\Pi_j(t)
=
\langle(u\cdot\nabla)u,\,\Delta_j^2 u\rangle_{L^2}
-
\nu\sum_{k>j}2^{2k}\|\Delta_k\nabla u\|_{L^2}^2.
\]

---

## 2. Definition of [SND]

**Manuscript (`def:SND`).** A Leray–Hopf solution satisfies \([\mathrm{SND}]\) if

\[
\inf_{t\ge 0}\frac{J(t)}{X(t)}\ge c_*>0.
\]

Call this **SND-U** when the intended claim is: the infimum holds for all relevant \(H^1(\mathbb{T}^3)\) data, with \(c_*\) not allowed to depend on an a priori ceiling \(M\) produced by the regularity one is trying to prove.

**Honest status:** hypothesis / open for large data. Small-data Koch–Tataru and bounded-\(H^2\) / short-time sketches in the same paper are the regimes where a positive \(c_*\) is plausible.

---

## 3. Definition of (SND-C)

**Manuscript (`def:SNDC`) — note the constant list.** We say \((\mathrm{SND}\text{-}C)\) holds if there exists

\[
C_*=C_*(\nu,\delta_*,C_S)
\]

such that for every divergence-free \(u\in H^1(\mathbb{T}^3)\) with \(X\ge\delta_*/4\) and \(\rho=J/X\le\rho_0\),

\[
|\Pi_{j_*}|
\le
C_*\Bigl(\nu\cdot 2^{2j_*}\cdot X_{j_*} + X^{1/2}\mathcal{D}^{1/2}\Bigr).
\]

Two mismatches live already at the definition:

| Face | Does the constant see \(M\)? | Is \(X\le M\) a hypothesis? |
| --- | --- | --- |
| `def:SNDC` as written | **No** — only \(\nu,\delta_*,C_S\) | **No** — only \(X\ge\delta_*/4\) and \(\rho\le\rho_0\) |
| Theorem H as written | **Yes** — \(C_*=C_*(\nu,\delta_*,M,\rho_0,C_S)\) | **Yes** — \(X\le M\) is stated |

The claim paper (`20405526`) then greens “Theorem H: (SND-C) unconditionally.” In that file, “unconditionally” means “under the definition’s hypotheses,” not “for all \(H^1\) data.” That substitution is Gap H2 of the 25 August verdict.

---

## 4. Theorem H — statement (complete)

**Manuscript (`thm:H`). Shell-Conditioned Commutator Estimate.**

Let \(u\in H^1(\mathbb{T}^3)\) with \(\operatorname{div}u=0\),

\[
X=\|\nabla u\|_{L^2}^2\ge\delta_*>0,\qquad X\le M,\qquad \rho=J/X\le\rho_0\ll 1.
\]

Let \(j_*=\operatorname{argmax}_j X_j\) and \(\mathcal{D}=\nu\|\Delta u\|_{L^2}^2\). Then there exists

\[
C_*=C_*(\nu,\delta_*,M,\rho_0,C_S)<\infty,
\]

independent of \(j_*\) and \(t\), such that

\[
|\Pi_{j_*}|
\le
C_*\Bigl(\nu\cdot 2^{2j_*} X_{j_*} + X^{1/2}\mathcal{D}^{1/2}\Bigr).
\]

**Where \(X\le M\) enters:** it is an explicit hypothesis of the theorem, and it is an explicit argument of \(C_*\).

---

## 5. Theorem H — proof (complete, as written)

Decompose \(\Pi_{j_*}\) by the Bony paraproduct:

\[
\Pi_{j_*}
=
\langle\Delta_{j_*}[(u\cdot\nabla)u],\,\Delta_{j_*}u\rangle_{L^2}
=:
T+T^*+R,
\]

\[
\begin{aligned}
T
&=
\sum_{k\le j_*-4}
\langle\Delta_{j_*}[(\Delta_k u\cdot\nabla)\Delta_{j_*}u],\,\Delta_{j_*}u\rangle
&&\text{(low\(\times\)high)},\\
T^*
&=
\sum_{k\ge j_*+4}
\langle\Delta_{j_*}[(\Delta_k u\cdot\nabla)u],\,\Delta_{j_*}u\rangle
&&\text{(high\(\times\)low)},\\
R
&=
\sum_{|k-j_*|\le 4}
\langle\Delta_{j_*}[(\Delta_k u\cdot\nabla)\Delta_{j'}u],\,\Delta_{j_*}u\rangle
&&\text{(diagonal)}.
\end{aligned}
\]

### Step 1 — diagonal \(R\)

For \(|k-j_*|\le 4\), Bernstein on \(\mathbb{T}^3\) gives \(\|\Delta_k u\|_{L^\infty}\lesssim 2^{j_*/2}X_{j_*}^{1/2}\), hence

\[
|R|\lesssim 2^{j_*/2}X_{j_*}^{3/2}.
\]

From Theorem F, \(\mathcal{D}\ge\nu\cdot 2^{2j_*}X_{j_*}\), so \(2^{j_*/2}\le(\mathcal{D}/(\nu X_{j_*}))^{1/4}\) and

\[
|R|\lesssim\nu^{-1/4}\mathcal{D}^{1/4}X_{j_*}^{5/4}.
\]

**Young (\(p=q=2\)) with \(X_{j_*}\le M\)** yields

\[
|R|\le C_R\Bigl(\nu\cdot 2^{2j_*}X_{j_*}+X^{1/2}\mathcal{D}^{1/2}\Bigr).
\]

**\(M\)-use:** the Young absorption that returns \(R\) to the target right-hand side uses the ceiling \(X_{j_*}\le M\).

### Step 2 — high\(\times\)low \(T^*\)

Kato–Ponce on \(k\ge j_*+4\):

\[
\|\Delta_{j_*}[(\Delta_k u\cdot\nabla)u]\|_{L^2}
\lesssim
\|\Delta_k u\|_{L^2}\|\nabla u\|_{L^\infty}
+
\|\nabla\Delta_k u\|_{L^2}\|u\|_{L^\infty}.
\]

In the spread regime the manuscript writes \(\|u\|_{L^\infty}\lesssim M^{1/2}\) and \(\|\nabla u\|_{L^\infty}\lesssim C_S\mathcal{D}^{1/2}/\nu^{1/2}\). Each far shell has \(X_k\le\rho_0 X\), so after Cauchy–Schwarz

\[
|T^*|\le C_{T^*}\bigl(X^{1/2}\mathcal{D}^{1/2}\bigr),
\qquad
C_{T^*}=C_{T^*}(\nu,M,\rho_0).
\]

**\(M\)-use:** \(\|u\|_{L^\infty}\lesssim M^{1/2}\) and the listed dependence of \(C_{T^*}\) on \(M\).

### Step 3 — low\(\times\)high \(T\) (called the critical piece)

For \(k\le j_*-4\), Bernstein plus \(X_k\le\rho X\) gives

\[
\|\Delta_k u\|_{L^\infty}\lesssim 2^{k/2}\rho^{1/2}X^{1/2}.
\]

Summing \(k\le j_*-4\) and using \(2^{j_*/2}\le(\mathcal{D}/(\nu X_{j_*}))^{1/4}\):

\[
|T|\lesssim C\nu^{-1/4}\rho^{5/4}X^{5/4}\mathcal{D}^{1/4}.
\]

**Young with \(\rho\le\rho_0\) and \(X\le M\):**

\[
|T|\le C_T\bigl(X^{1/2}\mathcal{D}^{1/2}\bigr),
\qquad
C_T=C_T(\nu,\delta_*,M,\rho_0).
\]

**\(M\)-use:** the last Young step; \(C_T\) depends on \(M\).

The manuscript remarks that \(\rho^{5/4}\to 0\) as \(\rho\to 0\) is “exactly what closes Theorem G.” That vanishing is a spread-regime smallness. It is not a substitute for removing \(M\).

### Step 4 — assembly

\[
|\Pi_{j_*}|\le|R|+|T^*|+|T|
\le
C_*\Bigl(\nu\cdot 2^{2j_*}X_{j_*}+X^{1/2}\mathcal{D}^{1/2}\Bigr),
\]

with \(C_*=C_R+C_{T^*}+C_T\) depending only on \(\nu,\delta_*,M,\rho_0,C_S\), independent of \(j_*\) and \(t\).

---

## 6. What Theorem H is used for — Theorem G and \(c_*\)

**Manuscript (`thm:G`).** Assume \((\mathrm{SND}\text{-}C)\). Then there exists \(c_*>0\) **depending only on \(\nu\), \(\delta_*\), \(M\), and \(C_S\)** such that every Leray–Hopf solution with \(\|\nabla u_0\|_{L^2}^2\ge\delta_*/2\) satisfies \(J(t)/X(t)\ge c_*\) for all \(t\ge 0\).

The proof is a contradiction argument: if \(\rho(t_k)\to 0\) with \(X(t_k)\ge\delta_*/4\), Theorem F (shell-spread Poincaré) makes \(\mathcal{D}(t_k)\to\infty\); (SND-C) bounds \(\Pi_{j_*}\); then \(\dot\rho>0\) in the spread regime, so \(\rho\) cannot keep decreasing.

**\(c_*\) dependence (as written):**

| Location | What \(c_*\) may depend on |
| --- | --- |
| Theorem G (the SND-C \(\Rightarrow\) [SND] arrow) | \(\nu,\delta_*,M,C_S\) — **\(M\) remains** |
| Small-data proposition | \(c_*=c_*(\delta_{\mathrm{KT}},\nu)\) |
| Theorem E (smooth on a finite interval with \(X\le M\)) | \(c_*=c_*(M,\eta,\nu,T)\) |
| Arithmetic slogan \(6/\pi^2=\zeta(2)^{-1}\) | **Not** a fluids threshold. PARK with Triple Lock |

Even if Theorem H were granted exactly as written, Theorem G does **not** produce a universal floor \(c_*(\nu,\delta_*)\) from initial data alone. That is Gap H3 of the 25 August verdict.

The manuscript then states a corollary: “Assuming (SND-C), the Clay problem on \(\mathbb{T}^3\) is resolved.” That corollary is **not** licensed by Theorem H + Theorem G as written, because both still carry \(M\).

---

## 7. The three questions, answered from the text

### 7.1 Where does \(X\le M\) enter?

| Site | Role of \(M\) |
| --- | --- |
| Theorem H hypothesis | \(X\le M\) is assumed |
| \(C_*\) | \(C_*=C_*(\ldots,M,\ldots)\) |
| Proof, Step 1 | Young on \(R\) uses \(X_{j_*}\le M\) |
| Proof, Step 2 | \(\|u\|_{L^\infty}\lesssim M^{1/2}\); \(C_{T^*}(\nu,M,\rho_0)\) |
| Proof, Step 3 | Young on \(T\) uses \(X\le M\); \(C_T(\nu,\delta_*,M,\rho_0)\) |
| Theorem G | \(c_*=c_*(\nu,\delta_*,M,C_S)\) |
| Theorem D(i) sketch | “uniform [SND] with Theorem C gives \(\|u^\varepsilon\|_{H^1}\le M\)” — the regularity arrow re-imports a ceiling from Q1 approximants |
| `def:SNDC` | **Omits** \(M\) — inconsistent with the theorem that is supposed to prove it |

Clay Statement (B) (Fefferman): \(\nu>0\), \(n=3\), \(u_0\) smooth divergence-free periodic, **\(f\equiv 0\)**, global smooth solution. The bound that must come out is an \(H^1\) (in fact smoother) control from data. Feeding \(X\le M\) into the keystone estimate is circular for that statement.

### 7.2 Can the assumption be removed?

**Not by the argument on the page.** Every Young / \(L^\infty\) step that returns \(\Pi_{j_*}\) to the target right-hand side uses a size. Replacing \(M\) by the instantaneous \(X(t)\) makes \(C_*\) grow with enstrophy; the ODE in Theorem G then does not give a uniform \(c_*\).

What would count as removing it:

1. Prove Theorem H with \(C_*=C_*(\nu,\delta_*,\rho_0,C_S)\) **independent of \(M\)**; or
2. Produce \(M=M(\|u_0\|_{H^1},\nu)\) by a bootstrap that does not assume the conclusion; or
3. Restrict to a class where \(M\) is already known (small data, bounded \(H^2\), short time) and **stop claiming large-data B**.

(1) and (2) are open. (3) is the honest publishable core (Ring Lemma + conditional SND on those regimes). That is a reason to **keep** spectral research, not to abandon it.

A separate analytic worry, not required to see the \(M\)-gap: the low Bony piece \(T\) still has to control a sum of many low shells uniformly as \(\rho\to 0\). The manuscript claims \(\rho^{5/4}\) saves this. Whether that bound is uniform on Leray–Hopf solutions (as opposed to smooth fields already bounded in \(H^1\)) is a specialist question *after* \(M\) is faced.

### 7.3 What may \(c_*\) depend on?

From the fluids manuscript, not from arithmetic:

- **If** one only has Theorem G as written: \(c_*=c_*(\nu,\delta_*,M,C_S)\). That is not a data-only constant.
- Small data: \(c_*(\delta_{\mathrm{KT}},\nu)\) is the right shape.
- \(6/\pi^2\) is not this constant.

A referee should refuse any sentence of the form “Theorem H proves SND for all \(H^1\) data with universal \(c_*\).”

---

## 8. Why [SND] is not “equivalent to Clay” on this record

Theorem D of the same manuscript asserts Clay \(\Leftrightarrow\) [SND]. Part (i) is the regularity arrow. Its proof, as written, is a sketch: shellwise Serrin, Q1 Theorem C, Aubin–Lions, “inherits the \(H^1\) bound.” It is not a line-by-line energy-class implication, and it uses \(M\) on approximants.

So there are **two** open arrows, not one:

```text
large-data [SND] without circular M     OPEN
        │
        ▼
clean [SND] ⇒ regularity (no Q1/M smuggling)     OPEN (Theorem D is a sketch)
        │
        ▼
unforced Statement (B) on T³
```

Closing the first without the second does not settle B. Calling [SND] “equivalent to the Clay problem” is premature on this manuscript. The 15 September briefing is corrected to match that.

The Main Conditional Result in the same TeX file is the honest theorem-shaped object: *if* [SND] holds with some \(c_*>0\), then (claim) global regularity on \(\mathbb{T}^3\). Even that “if” still needs a cleaned proof. The same page states the remaining gap as: prove [SND] unconditionally for all \(u_0\in H^1(\mathbb{T}^3)\) without size restriction.

---

## 9. What this gap does *not* mean

- It does **not** mean Littlewood–Paley occupation, Bony flux, or the Ring Lemma should be abandoned.
- It does **not** refute SND as a named extra structural hypothesis, in the same genus as BKM / LPS.
- It does **not** decide unforced Statement (B). A forced finite-time singularity (Clay C/D, with \(f\not\equiv 0\)) is a different official statement; see the 15 September briefing for the 8–11 September public record.

The 25 August adversarial verdict ([PR #35](https://github.com/simons357/Ship_it_app/pull/35)) already isolated this as Gap H1. This extract is the manuscript text that verdict was reading.

---

## 10. One-line lock

**Theorem H proves (SND-C) only under \(X\le M\) and \(\rho\le\rho_0\), with \(C_*\) and the Theorem G constant \(c_*\) both allowed to depend on \(M\). That assumption is not removed by the written Bony–Young argument. Spectral research stays; the large-data close does not.**
