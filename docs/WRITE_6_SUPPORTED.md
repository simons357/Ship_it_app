# WRITE (6) — statement plus supporting data

**Status.** The estimate is stated. It is not proved.
**Tag.** H1 = WRITE (6) = Lemma I on the ball.
**Do not merge** with H, Lemma C, H2, or H3.

---

## 0. Law of the letters

- **H** — all stretching on \(\mathbb{R}^3\). Parent. Open. Not this file.
- **Lemma C** — Good pairs. An *if* (CF 1993; BdVB 2002). Not an H. Not this file.
- **H1 = WRITE (6) = Lemma I** — this estimate. Open.
- **H2** — annulus flux. Smallness: CKN 1982. From energy: open. Not this file.
- **H3** — exterior Biot–Savart. Bound named. Not absorbed. Not this file.

If (6) sits and H2-from-energy does not, the cylinder still does not close.

---

## 1. The estimate (not proved)

\[
A_{\mathrm{bad}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

Bad pairs: \(|\omega|\ge\Lambda\) and \(|\sin\varphi|>C_*|x-y|^{1/2}\). Kernel still \(|z|^{-3}\).

Alone: [`WRITE_6.md`](WRITE_6.md). Score: aimed leftover yes; theorem no. Absolute value is sufficient, not necessary. The triple-integral form is a majorant via \(|D|\le C|\sin\varphi|\).

---

## 2. Why this integral is on the right-hand side

Local enstrophy, vorticity form, pressure free. Cutoff \(\phi\equiv 1\) on \(B_{r/2}\), supported in \(B_r\):

\[
\tfrac12\frac{d}{dt}\int|\omega|^2\phi+\nu\int|\nabla\omega|^2\phi
=
\int\alpha|\omega|^2\phi
+\tfrac12\int|\omega|^2(\partial_t\phi+u\cdot\nabla\phi)
+\tfrac\nu2\int|\omega|^2\Delta\phi.
\]

After time-integrating on \(Q_r\), stretching splits into Good (Lemma C, *if*), Bad (this file), low, exterior (H3), plus annulus flux (H2) and cutoff error \(R_\phi\). This identity does **not** bound \(A_{\mathrm{bad}}\).

---

## 3. Data that sits behind the write, and does not prove it

**CF kernel and the \(1/2\) cut.** Constantin–Fefferman 1993 (Lipschitz); Beirão da Veiga–Berselli 2002 (Hölder \(1/2\)). Beirão da Veiga 2016 keeps \(\beta<1/2\) open in that argument. On Good pairs the kernel drops to \(|z|^{-5/2}\) and absorbs. On Bad it does not. Lemma C is an *if*. It is not (6).

**Direction energy (identity).** On \(\{\omega\neq 0\}\):
\[
|\nabla\omega|^2=|\nabla|\omega||^2+|\omega|^2|\nabla\xi|^2.
\]
Hence \(\int_H|\nabla\xi|^2\le\Lambda^{-2}\int|\nabla\omega|^2\). Identity. Does not give Hölder \(1/2\) (Morrey: \(W^{1,2}\not\subset C^{0,1/2}\) in 3D).

**H3 bound (named remainder, not this write).**
\[
A_{\mathrm{ext}}\le C r^{-3/2}\int E^{1/2}E_{\mathrm{loc}}\,dt.
\]
Written. Not absorbed as \(r\to 0\) from \(\int E<\infty\). Grujić CMP 2009 controls exterior stretching under *local coherence*. Without that, this crude bound is what sits.

**HLS / Gagliardo–Nirenberg on Bad.** Kernel \(|z|^{-3}\) recovers local \(E^3\), i.e. the cubic wall. The Hölder cut changes the *set*, not the exponent. A thin set would save it. A path jump in \(\xi\) does not prove the set is thin.

**Mid-Bad Cauchy–Schwarz.** For \(|x-y|\ge\rho\),
\[
A_{\mathrm{bad}}^{\ge\rho}\le C\rho^{-3/2}\int E_{\mathrm{loc}}^{3/2}\,dt.
\]
Succeeds as a bound. Same class as H3. Not absorbed. Near-Bad remains (6).

---

## 4. Literature table — nearest cousins, all *if*

| Paper | What it is | (6)? |
|---|---|---|
| CF 1993; BdVB 2002 | Alignment \(\Rightarrow\) regular | No. Lemma C |
| Grujić, *CMP* 290 (2009) | Localizes the *condition* | No. Local if |
| Grujić–Guberović, *CMP* 298 (2010) | Coherence as a weight on \(\int|\omega|^q\) | No. Need some coherence |
| Grujić, *Nonlinearity* 26 (2013) | 1-D sparseness of intense regions | No. Assumes thin |
| Bradshaw–Grujić, arXiv:1309.2519 | Mild geometry \(\Rightarrow\) \(L\log L\) on \(\omega\) | No. Hypothesis on \(\xi\) |
| BdV, arXiv:1604.08083 (2016) | \(\beta<1/2\) open in the CF argument | No. Cut is \(1/2\) |
| CKN 1982 | Energy \(\varepsilon\)-regularity | No. That is H2-smallness |

No paper is (6). Full pass: [`LITERATURE-H.md`](LITERATURE-H.md).

---

## 5. What would prove it (not written)

1. Thinness: Bad-pair measure small enough that HLS turns \(E^3\) into \(E^2\) or dissipation.
2. J on folds only: persistent Bad pairs sit in a fold, \(\int_{B_{2\rho}}|\nabla\omega|^2\gtrsim\Lambda^2\rho^2\), Vitali closes.
3. Dynamics: NSE forbids 2’s alternatives on the scale \(r^2/\nu\).

Lookups: [`LOOKUP-H1.md`](LOOKUP-H1.md).

---

**Verdict.** WRITE (6) is stated. Supporting identities and the literature table sit. The estimate does not sit. Do not cash this file as a proof.
