# Theorem H — manuscript extract (object under review)

**Packet role:** **archive.** Do not send. The sendable card is [`SND-WHAT-IS-KEPT.md`](./SND-WHAT-IS-KEPT.md). This extract is the withdrawn displayed proof.  
**Manuscript source:** Zenodo `20518057` mirror, `docs/papers/zenodo-spectral/20518057/98d1b1cc9_NS_UPLOAD_ZENODO.tex` on `origin/cursor/tao-snd-h-panel-a0eb` (older SND framework; superseded as a *claim* by KEEP `10.5281/zenodo.22050976`).  
**Claim-paper overlay:** Zenodo `20405526` (PARK).  
**Corrections (binding for packet status):** [`SND-MATH-CORRECTIONS-2026-09-15.md`](./SND-MATH-CORRECTIONS-2026-09-15.md).  
**Panel letter:** [`PANEL-RESPONSE-2026-09-16.md`](./PANEL-RESPONSE-2026-09-16.md).  
**Identities from the boxed equation (not a new Theorem H):** [`SND-REPAIRED-SHELL-BUDGET.md`](./SND-REPAIRED-SHELL-BUDGET.md).

Sections 1–6 below are the **extract**: definitions and the displayed Theorem H statement/proof **as written**. They are the object under review, not a claimed theorem of this packet.

---

## Status after the 15 September mathematical audit

> In the supplied extract, Theorem H is not established even with \(X\le M\). Its proof drops a viscous tail, uses invalid Sobolev embeddings and does not provide a complete Bony decomposition. The displayed absolute-flux estimate fails on smooth fixed-enstrophy shear fields. A valid \(M\)-dependent bound for the nonlinear shell term can be proved separately, but its usefulness for SND propagation remains to be shown. Any SND floor asserted from time zero must respect the initial spectral distribution. Retain the spectral toolkit and rebuild the required estimate from the exact shell evolution.

Earlier packet commentary that Theorem H is “proved under \(X\le M\)” is **withdrawn**. The ceiling dependence was correctly noticed; the displayed absolute-value estimate is nevertheless false on an explicit family that satisfies \(X\le M\) and \(\rho\le\rho_0\). Removing \(M\) from *this same* estimate is not an appropriate open target (amplitude scaling; see corrections §5). A universal floor \(c_*(\nu,\delta_*,M,C_S)\) from time zero is obstructed by equal-shell shear data (corrections §6).

What remains of the three specialist questions, after that audit:

1. **Where \(X\le M\) enters the write-up** — still as in §7.1 (hypothesis and Young / \(L^\infty\) steps). Those steps are moot for the displayed \(|\Pi_{j_*}|\) bound, which already fails at fixed \(M\).
2. **Can \(M\) be removed from the displayed estimate?** — the wrong question for this \(\Pi_j\). Rebuild from the exact shell equation in corrections §8.
3. **What may \(c_*\) depend on?** — no uniform \(c_*(\nu,\delta_*,M,C_S)\) from \(t=0\) for all data. Solution-by-solution [SND] is a different claim from a uniform theorem.

The **[SND] \(\Rightarrow\) regularity** arrow (Theorem D) remains a sketch. Equating [SND] with Clay Statement (B) is premature. Unforced (B) uses smooth periodic data with \(f\equiv 0\), not an \(H^1\) ceiling as the official wording.

---

## 0. What the extract contains

1. **[SND]** as written: \(\inf_t J/X\ge c_*>0\).
2. **(SND-C)** as written: a bound on \(|\Pi_{j_*}|\) in a spread regime.
3. **Theorem H** as written, including the hypothesis \(X\le M\).
4. **Theorem G** as written, with \(c_*\) still listed as depending on \(M\).
5. The identification of \(\Pi_{j_*}\) with a Bony splitting of \(F_{j_*}\) (this identification **drops** the viscous tail \(S_{j_*}\); see corrections §1).

---

## Manuscript extract (object under review)

The definitions and displayed proof below are transcribed as written. They are **not** asserted as correct. Commentary after §6 is packet status, not part of the manuscript.

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

**Honest status (packet, not manuscript):** per-solution hypothesis. A **uniform** floor from \(t=0\) for all data of fixed enstrophy is obstructed (corrections §6). Small-data existence does not supply a universal initial \(\rho\).

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

The claim paper (`20405526`) then greens “Theorem H: (SND-C) unconditionally.” In that file, “unconditionally” means “under the definition’s hypotheses,” not “for all \(H^1\) data.” That substitution is a **definition/claim mismatch** (August verdict Gap H2). The formulas establish an error; they do not establish intent.

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

**Where \(X\le M\) enters the write-up:** it is an explicit hypothesis of the displayed theorem, and an explicit argument of \(C_*\). That does **not** make the estimate true; see the status banner and [`SND-MATH-CORRECTIONS-2026-09-15.md`](./SND-MATH-CORRECTIONS-2026-09-15.md) §2.

The displayed statement is written for \(u\in H^1\). On that class \(\mathcal{D}\) need not be finite. Any finite estimate should be proved first for smooth or \(H^2\) fields.

---

## 5. Theorem H — proof (complete, as written)

Decompose \(\Pi_{j_*}\) by the Bony paraproduct **as the manuscript writes it** (this line identifies \(\Pi_{j_*}\) with \(F_{j_*}\) and drops \(S_{j_*}\); corrections §1). The displayed splitting is not a complete indexed Bony decomposition (unquantified \(j'\); high–low uses the whole \(u\)):

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

In the spread regime the manuscript writes \(\|u\|_{L^\infty}\lesssim M^{1/2}\) and \(\|\nabla u\|_{L^\infty}\lesssim C_S\mathcal{D}^{1/2}/\nu^{1/2}\). **Neither is a general 3D Sobolev bound** (corrections §4). The write-up continues: each far shell has \(X_k\le\rho_0 X\), so after Cauchy–Schwarz

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

Even if the displayed Theorem H were granted, Theorem G does **not** produce a universal floor \(c_*(\nu,\delta_*)\) from initial data alone. Independently, **no** common \(c_*(\nu,\delta_*,M,C_S)\) can hold from \(t=0\) for all data of enstrophy \(q\le M\) (equal-shell shears, corrections §6). Distinguish solution-by-solution [SND] from a uniform theorem.

The manuscript then states a corollary: “Assuming (SND-C), the Clay problem on \(\mathbb{T}^3\) is resolved.” That corollary is **not** licensed: the displayed (SND-C) estimate fails, Theorem G still lists \(M\), and official Statement (B) is unforced smooth data.

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

Clay Statement (B) (Fefferman): \(\nu>0\), \(n=3\), \(u_0\) **smooth** divergence-free periodic, **\(f\equiv 0\)**, global smooth solution. An \(H^1\) theory may be a route to that result; it is not the official initial-data wording. Feeding \(X\le M\) into a keystone estimate would in any case be circular for a large-data regularity claim. The displayed keystone is not established even *with* \(X\le M\).

### 7.2 Can the assumption be removed?

**Not an appropriate open target for this displayed estimate.** The absolute-value bound already fails at fixed \(M\) (high-tail shears). Even after replacing \(\Pi_j\) by \(F_j\), the proposed right-hand side is quadratic in amplitude while \(F_j\) is cubic, so an \(M\)-free version for every spread field fails by rescaling (corrections §5).

What remains valid:

1. The elementary bound \(|F_j|\le C\sqrt{M/(\nu\lambda_1)}\,X^{1/2}\mathcal{D}^{1/2}\) (corrections §3) — different from Theorem H; no propagation theorem.
2. Rebuild from the exact shell equation (corrections §8) and test against the shear family, amplitude rescaling, and equal shells.
3. Keep [SND] as a **solution-by-solution** extra hypothesis, not a uniform floor from \(t=0\).

A finite-time continuation bound may depend on \(\nu\), the domain, and an endpoint \(T\); an all-time \(M=M(\|u_0\|_{H^1})\) is stronger.

### 7.3 What may \(c_*\) depend on?

From the fluids manuscript, not from arithmetic:

- **If** one only reads Theorem G as written: \(c_*=c_*(\nu,\delta_*,M,C_S)\). That is not a data-only constant, and it cannot hold uniformly from \(t=0\) for all data of size \(q\le M\).
- Small-data existence does not supply a universal initial \(\rho\): amplitude scaling leaves \(\rho\) unchanged.
- \(6/\pi^2\) is not this constant.

A referee should refuse any sentence of the form “Theorem H proves SND for all \(H^1\) data with universal \(c_*\).” The estimate is not proved, and the uniform floor is obstructed.

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

## 9. What this does *not* mean

- It does **not** mean Littlewood–Paley occupation or a correctly scoped Ring-type bound should be abandoned. Rebuild from the exact shell equation.
- It does **not** refute [SND] as a named extra structural hypothesis **for a given solution**, in the same genus as BKM / LPS.
- A KEEP label is not verification of the manuscript Ring Lemma. The elementary band-limited bound lives on \(\{|\omega|\ge c\|\omega\|_\infty\}\) and **changes the threshold**.
- It does **not** decide unforced Statement (B). Forced C/D (8–11 Sep) are a different official pair.

The 25 August verdict isolated circular \(M\) as Gap H1. That diagnosis **understated** the defect: the displayed \(|\Pi_{j_*}|\) bound fails even with the ceiling. See the August erratum on that file.

---

## 10. One-line lock

**The displayed Theorem H is not established even with \(X\le M\). Keep the extract as an extract. Keep spectral research; replace the estimate using the exact shell evolution.**
