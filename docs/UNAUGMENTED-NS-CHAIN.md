# Unaugmented 3D Navier–Stokes — working packet

**Date.** 10 September 2026  
**Use.** This is the live unaugmented-chain document.  
**Status.** Proof *chain*. Last estimate open. No augmentation, no \(K(t)\), no Q-stack. Only \(\nu\Delta u\).

Desk: leftover WRITE (6) on this path is **H1** (\(A_{\mathrm{bad}}\) a priori). **H2** a priori from energy is also open. **H3** (\(A_{\mathrm{ext}}\)) is a named remainder; a priori from energy is open. \(R_\phi\) is not free. Lemma C is a criterion, not alignment. Theorem A is a different PDE. DA-NS-2 and the old \(\int\mathcal R\) line are other writings of the same leftover, not this packet’s next write. Keep Biot–Savart at \(1/r^4\). Do not add \(Q_1\).

Machine write-up: [`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md).  
Barycenter sibling (not this path): [`DA-NS-2.md`](DA-NS-2.md).  
Augmented (other PDE): [`A-CHAIN.md`](A-CHAIN.md).

---

## 0. Equation and notation

\[
\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u,\qquad\nabla\cdot u=0
\]

on \(\mathbb{R}^3\) or \(\mathbb{T}^3\), \(\nu>0\), \(f\equiv 0\), smooth divergence-free finite-energy data.

\[
\mathcal{E}(t)=\tfrac12\|u\|_{L^2}^2,\qquad
E(t)=\|\nabla u\|_{L^2}^2,\qquad
\omega=\nabla\times u,\qquad
\xi=\omega/|\omega|\ \ (\omega\neq 0),
\]

\[
\alpha=\xi\cdot S_{\mathrm{strain}}\xi,\qquad
S_{\mathrm{tot}}=\int\alpha|\omega|^2\,dx,\qquad
\varphi(x,y)=\angle(\omega(x),\omega(y)).
\]

Parabolic cylinder: \(Q_r(x_0,t_0)=B_r(x_0)\times(t_0-r^2,t_0]\).

---

## 1. Proved floor

**Energy (while smooth).**
\[
\frac{d}{dt}\mathcal{E}+\nu E=0
\qquad\Rightarrow\qquad
\int_0^T E(t)\,dt\le\mathcal{E}(0)/\nu.
\]
Leray–Hopf weak solutions: inequality instead of equality. Budget only on the smooth interval.

**Energy class.** \(u\in L^\infty_t L^2\cap L^2_t\dot H^1\).

**Sobolev.** \(\|u\|_{L^6}\lesssim E^{1/2}\), so \(u\in L^2_t L^6\). This is the floor.

**Local existence.** Fujita–Kato: strong solution on a short interval. Question is continuation.

**Serrin / LPS (criterion).** If \(u\in L^p_t L^q_x\) with \(2/p+3/q=1\), \(q>3\), then smooth on \([0,T]\).  
At \(q=6\): need \(L^4_t L^6\). Sobolev is one-sided:
\[
\int E^2\,dt<\infty\quad\Longrightarrow\quad\int\|u\|_{L^6}^4\,dt<\infty.
\]

**ESS (criterion).** \(u\in L^\infty_t L^3\Rightarrow\) regular.

**Enstrophy identity.**
\[
\tfrac12\dot E+\nu\|D^2 u\|_2^2=S_{\mathrm{tot}}.
\]

**Cubic bound.** \(|S_{\mathrm{tot}}|\le C E^3\) after Young. Allows \(E\sim(T_*-t)^{-1/2}\). Does not give \(\int E^2\). The 1934 wall.

**No Type-I self-similar blowup.** Nečas–Růžička–Šverák 1996.

**CKN.** Singular set of a suitable weak solution has parabolic 1-measure zero. Set not proved empty.

**Interpolation used later.**
\[
E^2\le 2\mathcal{E}\,\|D^2 u\|_2^2.
\]
So a bound on \(\int\|D^2 u\|_2^2\) gives \(\int E^2\).

---

## 2. Lemma C — good pairs (theorem)

**CF 1993.** If \(|\sin\varphi(x,y)|\le|x-y|/\rho\) whenever both \(|\omega|\ge\Lambda\), then the solution is strong on \([0,T]\).  
**BdVB 2002.** Hölder \(1/2\) suffices: \(|\sin\varphi|\le C|x-y|^{1/2}\).

Mechanism: strain is a \(|z|^{-3}\) kernel of \(\omega\). Alignment puts \(|\sin\varphi|\) in the numerator and drops the kernel to \(|z|^{-2}\) (Lipschitz) or \(|z|^{-5/2}\) (Hölder \(1/2\)). That is absorbable into \(\nu\|\nabla\omega\|_2^2+CE\).

Cutoff used below: **Hölder \(1/2\)** — weakest alignment that still absorbs, smallest leftover. Lipschitz is the same line with a stricter cut.

Lemma C does not prove alignment. It assumes it.

---

## 3. Partition

High-vorticity set \(H=\{|\omega|\ge\Lambda\}\). Pairs in \(H\times H\) with \(|x-y|<\delta\):

- **Good:** \(|\sin\varphi|\le C_*|x-y|^{1/2}\). Contribution \(A_{\mathrm{good}}\) absorbed by Lemma C.
- **Bad:** \(|\sin\varphi|>C_*|x-y|^{1/2}\). Contribution \(A_{\mathrm{bad}}\). Open.
- **Low vorticity** \(|\omega|<\Lambda\): stretching \(\le C\Lambda E\). Harmless.

A bad pair is one of three pictures: fold (dissipation spread in a ball), reconnection (thin bridge), two blobs (gap with \(\omega\approx 0\)).

---

## 4. Local enstrophy on a cylinder

Cutoff \(\phi\equiv 1\) on \(B_{r/2}\), supported in \(B_r\), \(|\nabla\phi|\lesssim 1/r\). Vorticity form — pressure drops.

\[
\tfrac12\frac{d}{dt}\int|\omega|^2\phi+\nu\int|\nabla\omega|^2\phi
=
\int\alpha|\omega|^2\phi
+\tfrac12\int|\omega|^2(\partial_t\phi+u\cdot\nabla\phi)
+\tfrac\nu2\int|\omega|^2\Delta\phi.
\]

Time-integrate on \(Q_r\):

\[
\nu\iint_{Q_r}|\nabla\omega|^2\phi
\le
\text{bottom data}
+A_{\mathrm{good}}+A_{\mathrm{bad}}+A_{\mathrm{far}}+A_{\mathrm{low}}
+F_{\mathrm{adv}}+F_{\nu}.
\]

Moved with justification:

- \(A_{\mathrm{low}}\): \(\le C\Lambda\iint|\omega|^2\).
- \(F_{\nu}\): \(\le C\nu r^{-2}\iint_{\mathrm{annulus}}|\omega|^2\).

Not free, named in §11:

- \(A_{\mathrm{good}}\): interior Good pairs only. Whole-space Lemma C does not give this for free. Cutoff error \(R_\phi\) remains.
- \(A_{\mathrm{far}}\) inside \(B_r\times B_r\) if \(r<\delta\): empty. Exterior Biot–Savart \(\alpha_{\mathrm{ext}}\) is **not** empty. That is H3.
- Closed budget \(\Rightarrow\) smooth: local Serrin, not CKN. §11 Gap (iii).

Left (names, not a closed estimate):

\[
\nu\iint_{Q_r}|\nabla\omega|^2\phi
\le
\text{bottom}
+A_{\mathrm{good}}^{\mathrm{loc}}+R_\phi
+A_{\mathrm{bad}}(Q_r)
+A_{\mathrm{ext}}(Q_r)
+F_{\mathrm{adv}}
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

---

## 5. Last line — named halves

**H1**
\[
A_{\mathrm{bad}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

**H2**
\[
F_{\mathrm{adv}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2
+C r^{-2}\iint_{Q_r}|\omega|^2,
\]
where \(F_{\mathrm{adv}}=\tfrac12\iint|\omega|^2(\partial_t\phi+u\cdot\nabla\phi)\) lives on the annulus, and the dangerous piece is \(r^{-1}\iint|u||\omega|^2\).

**H3.** Exterior remainder, bound named in §11:
\[
|\alpha_{\mathrm{ext}}(x)|\le C r^{-3/2}E(t)^{1/2},
\qquad
A_{\mathrm{ext}}(Q_r)\le C r^{-3/2}\int_{t_0-r^2}^{t_0} E(t)^{1/2}E_{\mathrm{loc}}(t)\,dt.
\]
A priori from \(\int E<\infty\): open.

If H1, H2-a-priori, H3, and \(R_\phi\) all hold for all small \(r\), the local Serrin hypothesis of §11 Gap (iii) is met, hence smoothness on \(Q_{\theta r}\). Those four bounds are not all known from the energy class.

**H2.** True as a *smallness* criterion (CKN 1982: small scaled \(\iint|\nabla u|^2\)). Not proved as an a priori bound from \(\int E<\infty\). Remainder after Young is local \(\int E^2\). CKN is the wrong citation for “closed enstrophy budget \(\Rightarrow\) smooth.”

**H1.** Open. This is the CF leftover. Equivalent to the remaining problem on this path.

CF stretching kernel (for reference):
\[
\alpha(x)=\mathrm{P.V.}\int D(\hat z,\xi(x),\xi(y))\frac{|\omega(y)|}{|z|^3}\,dy,
\qquad
|D|\le C|\sin\varphi|.
\]
On Bad, \(|\sin\varphi|\) is large, so the kernel is not improved.

---

## 6. Attempts already made (do not repeat as proofs)

- HLS on all pairs: recovers \(\int E^3\). No gain.
- Path-cost of \(\nabla\xi\): lower bound is on a segment, not in \(L^2(B_r)\). Fails on reconnection / two-blobs.
- Lemma J (pointwise pair paid by \(\fint|\nabla\omega|^2\)): false for generic fields; Biot–Savart averages \(\omega\), not \(\nabla\omega\); \(\xi\)-equation has no sign and is degenerate at \(\omega=0\).
- Signed kernel \(D\): no cancelation for an isolated pair (fixed spherical harmonic in \(\hat z\)).
- Thinness of Bad: not known. Assuming it is Lemma C again.
- Persistence for time \(r^2/\nu\): filter on which cylinders to use. Waiting time imposed, not derived. Pathwise enstrophy does not produce \(\int|\nabla\omega|^2\).
- Bony LP split of stretching: LLH needs \(\|\omega_{\mathrm{low}}\|_\infty\) (BKM); LHH remainder \(\|\omega_{\mathrm{low}}\|_\infty^2 E_{\mathrm{high}}\); HHH remainder is pieces of \(\int E^2\).
- Swirl ODE / fading \(K(t)\) / Q-stack: not unaugmented NSE. Out of this packet.

---

## 7. Ledger

| Item | Status |
|---|---|
| Energy, \(\int E<\infty\) | Proved |
| \(L^2_t L^6\) | Proved |
| Serrin / ESS as criteria | Proved |
| \(\int E^2\Rightarrow L^4_t L^6\) | Proved (one-sided) |
| Cubic bound \(\dot E\le CE^3\) | Proved, too weak |
| No Type-I self-similar | Proved |
| CKN measure of singular set | Proved |
| Lemma C (good pairs) | Proved (conditional theorem) |
| H2 as smallness criterion | Proved (CKN 1982) |
| H1 / \(A_{\mathrm{bad}}\) a priori | **Open** |
| H2 a priori from energy | **Open** |
| H3 / \(A_{\mathrm{ext}}\) a priori | **Open** (bound named) |
| \(R_\phi\) cutoff error | Lemma to write or cite; not free |
| Type-II Liouville | Open, separate |

---

## 8. What to do next

Work **H1** on a single cylinder \(Q_r\). Do not reprove Lemma C. Do not add \(K(t)\). Keep **H1, H2, H3, \(R_\phi\)** separate so a failure is labeled.

Optional sibling (not shorter): \(L^\infty_t L^3\) mass on the bad set; Type-II profile. Only after H1 has a new estimate or a new wall.

DA will not emit H1 and call it proved.

---

## 9. One paragraph for the top of a paper / note

Unaugmented 3D NSE has a complete chain from energy to Serrin except control of stretching from misaligned high-vorticity pairs. Constantin–Fefferman / Beirão da Veiga–Berselli absorb pairs whose direction turns at most like Hölder \(1/2\), on whole space, as an if. Localizing that if leaves a cutoff error \(R_\phi\). The leftover integral \(A_{\mathrm{bad}}\) on a parabolic cylinder is H1. The advective flux \(F_{\mathrm{adv}}\) is H2 (CKN as smallness; a priori from energy open). Exterior Biot–Savart \(A_{\mathrm{ext}}\) is H3 (bound named; a priori from energy open). None of H1, H2-from-energy, or H3-from-energy is known from \(\int E<\infty\) alone.

---

## 10. Desk score (10 September 2026)

The packet is a **good map**. It is not a proof of ordinary NS.

**Floor (§1).** Correct literature: energy, \(L^2_t L^6\), Fujita–Kato, Serrin/LPS, ESS as a criterion, enstrophy identity, cubic \(E^3\) wall, CKN measure, interpolation \(E^2\le 2\mathcal{E}\|D^2u\|_2^2\). “No Type-I self-similar” is the NRS 1996 Leray profile, not every Type-I statement in the later literature.

**Lemma C.** CF 1993 / BdVB 2002 sit as **if**. Hölder \(1/2\) is the right cut for this path. Lemma C does not prove alignment. That sentence is the whole point.

**H1.** The right leftover on this path. \(A_{\mathrm{bad}}\) is stretching from misaligned high-vorticity pairs. On Bad the kernel stays \(|z|^{-3}\). An a priori bound of that integral by local dissipation plus \(r^{-2}\iint|\omega|^2\) is WRITE (6) here. Open.

**H2.** Smallness criterion is true. A priori from \(\int E<\infty\) is not. After Young the remainder is local \(\int E^2\). So even if H1 sits, H2-from-energy is a second wall. Keep them separate.

**Gaps in the cylinder write (10 Sep morning).** Localizing Lemma C is not free. Exterior Biot–Savart is not empty. H1+H2 \(\Rightarrow\) smooth is not CKN \(\varepsilon\)-regularity. Those *writing* holes are repaired in §11. The leftover names stay.

**Refuse list (§6).** Sound. Do not rerun HLS, Lemma J, signed \(D\), thin-Bad-as-Lemma-C, imposed waiting time, or \(K(t)\)/Q-stack as a close.

**Not equivalent to DA-NS-2.** Spectral-barycenter integral is another writing of leftover (6). This packet’s next write is H1 on one cylinder.

**Verdict.** Use this as the unaugmented chain. Work H1. Do not emit H1. Theorem A stays a different equation.

---

## 11. Three writing gaps, closed as write

The leftover names stay. What is destroyed is sloppiness: each gap is a cited theorem, an explicit remainder, or a labeled open estimate.

### Gap (iii) — citation

**Theorem (local Serrin from a closed enstrophy budget).**
Let \(u\) be a suitable weak solution of NSE on \(Q_{2r}\). Suppose

\[
\omega\in L^\infty(t_0-r^2,t_0;L^2(B_r))
\cap
L^2(t_0-r^2,t_0;H^1(B_r)).
\]
Then \(u\in L^4(t_0-r^2,t_0;L^6(B_r))\) up to cutoff / Poincaré corrections on the ball, hence \(u\) is smooth on \(Q_{\theta r}\) for some universal \(\theta\in(0,1)\).

**Citations.** Serrin, *Arch. Rational Mech. Anal.* 9 (1962), local \(L^p_t L^q_x\). Sobolev on the ball: \(\|u\|_{L^6(B_r)}\lesssim\|\nabla u\|_{L^2(B_r)}+r^{-1}\|u\|_{L^2(B_r)}\). \(H^1\) on \(u\) is \(L^2\) on \(\omega\). Bootstrap: local regularity chapter, Tao NS notes or Lemarié-Rieusset.

**Not cited for this implication:** Caffarelli–Kohn–Nirenberg 1982. That is energy-level \(\varepsilon\)-regularity (small scaled \(\iint|\nabla u|^2\)). Right citation for H2 as a *smallness* criterion. Wrong citation for “closed enstrophy budget \(\Rightarrow\) smooth.”

If H1, H2-a-priori, and H3 all hold (and \(R_\phi\) is absorbed), the hypothesis above is met. Those bounds are still open.

NRS 1996 = no Leray backward self-similar profile. Not a blanket Type-I theorem.

### Gap (ii) — exterior remainder H3

For \(x\in B_{r/2}\),

\[
\alpha(x)=\alpha_{\mathrm{in}}(x)+\alpha_{\mathrm{ext}}(x),
\]

\[
\alpha_{\mathrm{ext}}(x)
=
\mathrm{P.V.}\int_{\mathbb{R}^3\setminus B_r}
D(\hat z,\xi(x),\xi(y))\frac{|\omega(y)|}{|x-y|^3}\,dy.
\]

If \(r<\delta\), interior far pairs die. \(\alpha_{\mathrm{ext}}\) remains. For \(x\in B_{r/2}\) and \(y\notin B_r\), \(|x-y|\ge r/2\). Dyadic shells \(A_k=\{2^k r\le|y-x|<2^{k+1}r\}\):

\[
|\alpha_{\mathrm{ext}}(x)|
\le
C\sum_{k\ge 0}(2^k r)^{-3/2}\|\omega\|_{L^2(A_k)}
\le
C r^{-3/2} E(t)^{1/2}.
\]

\[
A_{\mathrm{ext}}(Q_r)
:=
\iint_{Q_r}|\alpha_{\mathrm{ext}}|\,|\omega|^2\phi
\le
C r^{-3/2}\int_{t_0-r^2}^{t_0} E(t)^{1/2}\|\omega(t)\|_{L^2(B_r)}^2\,dt.
\]

This is H3. Not absorbed into \(r^{-2}\iint|\omega|^2\) as \(r\to 0\) without extra smallness or extra time integrability. Young returns a piece of \(\int E_{\mathrm{loc}}^2\) or needs \(\sup E<\infty\). A priori from \(\int E<\infty\): **not** proved.

### Gap (i) — no free localization of Lemma C

Whole-space Lemma C is over \(\mathbb{R}^3\times\mathbb{R}^3\). On \(Q_r\), for \(x\in\operatorname{supp}\phi\),

\[
\alpha_{\mathrm{in}}
=
\alpha_{\mathrm{good}}^{\mathrm{loc}}
+
\alpha_{\mathrm{bad}}^{\mathrm{loc}}
+
\alpha_{\partial}.
\]

- \(\alpha_{\mathrm{good}}^{\mathrm{loc}}\): both in \(B_r\), Good. Kernel drop \(|z|^{-5/2}\) on that double integral. Cutoff \(\phi(x)\) (not \(\phi(y)\)) leaves
  \[
  R_\phi
  =
  \iint_{\mathrm{Good}\cap(B_r\times B_r)}
  \frac{|\omega(y)|}{|x-y|^{5/2}}|\omega(x)|^2|\phi(x)-\eta(y)|\,dx\,dy.
  \]
  Same class as \(F_{\mathrm{adv}}/F_{\nu}\) after Young, **or** an extra open term. Not automatic from whole-space CF.
- \(\alpha_{\mathrm{bad}}^{\mathrm{loc}}\): H1 / WRITE (6).
- \(\alpha_{\partial}\): this is \(\alpha_{\mathrm{ext}}\), H3.

Grujić et al. localize the *hypothesis* (Hölder \(1/2\) in a region). BdVB 2009/2013 assume a direction condition in the region of interest. They do not prove \(A_{\mathrm{bad}}(Q_r)\) small.

### Balance

\[
\nu\iint_{Q_r}|\nabla\omega|^2\phi
\le
\text{bottom}
+
A_{\mathrm{good}}^{\mathrm{loc}}+R_\phi
+
A_{\mathrm{bad}}(Q_r)
+
A_{\mathrm{ext}}(Q_r)
+
F_{\mathrm{adv}}
+
C r^{-2}\iint_{Q_r}|\omega|^2.
\]

| Term | Status |
|---|---|
| \(A_{\mathrm{good}}^{\mathrm{loc}}\) | CF/BdVB on interior Good pairs |
| \(R_\phi\) | Cutoff error. Estimate or cite. Not free |
| \(A_{\mathrm{bad}}\) | H1 / WRITE (6). Open |
| \(A_{\mathrm{ext}}\) | H3. Bound named. Open a priori |
| \(F_{\mathrm{adv}}\) | H2. Smallness: CKN 1982. A priori from \(\int E\): open |
| Lower order / bottom | Closed |

**What is not claimed.** H1 is not proved. H2-from-energy is not proved. H3-from-energy is not proved. The three *writing* gaps are gone. The last estimate is still WRITE (6).

**Desk score of this repair.** Gap (iii) is the right implication (local Serrin, not CKN). Gap (ii) is a valid crude bound; H3 is a real extra term. Gap (i) stops a free move; \(R_\phi\) is still a lemma. Writing sloppiness is gone. H1, H2-from-energy, and H3-from-energy are not proved.


