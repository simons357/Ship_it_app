# Unaugmented 3D Navier–Stokes — working packet

**Date.** 10 September 2026  
**Use.** This is the live unaugmented-chain document.  
**Status.** Proof *chain*. Last estimate open. No augmentation, no \(K(t)\), no Q-stack. Only \(\nu\Delta u\).

Estimate audit (writing filter for an axisymmetric-with-swirl shell budget; remainder \(T_{j\leftarrow j}\); KEEP / DISCARD / PARK; not a close): [`ESTIMATE-AUDIT.md`](ESTIMATE-AUDIT.md). Desk: leftover WRITE (6) on the geometric path is **H1 = Lemma I on the ball** (\(A_{\mathrm{bad}}\) a priori). Energy-budget writing of the same leftover class: **Lemma★** (locked as hypothesis; exact form is a scale-invariant trilinear bound on \(\mathcal R_\star\); not proved; K=0 dead; the \(a^4\) missing inequality dead; uniform pre-Young \(C\) dead; ★ \(\Rightarrow\) GR in this packaging, not equivalent; lattice packets including HH→L fan did not kill; samples are evidence only). [`LEMMA-STAR.md`](LEMMA-STAR.md), [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md), [`math/ns_attacks/LEMMA_STAR_CANONICAL.md`](math/ns_attacks/LEMMA_STAR_CANONICAL.md), [`LEMMA-STAR-CORRECTIONS.md`](LEMMA-STAR-CORRECTIONS.md). Original five-lane JSON: [`five-lane-export/COMPUTE.md`](five-lane-export/COMPUTE.md). Attack 9B: [`five-lane-export/ATTACK_9B.md`](five-lane-export/ATTACK_9B.md). Counting lock: [`LEMMA-STAR-9B-COUNTING.md`](LEMMA-STAR-9B-COUNTING.md). Growing cube (named, computed; not a kill): [`LEMMA-STAR-CUBE.md`](LEMMA-STAR-CUBE.md). Analytic review (files absent; \(M_0\) not locked): [`LEMMA-STAR-CUBE-REVIEW.md`](LEMMA-STAR-CUBE-REVIEW.md). Do not merge ★ with H1, and do not merge either with global **H**. Lemma C is an if, not an H. **H2** a priori from energy is also open. **H3** (\(A_{\mathrm{ext}}\)) is a named remainder; a priori from energy is open. \(R_\phi\) is not free. If H1 sits and H2-from-energy does not, the cylinder is still open. Theorem A is a different PDE. DA-NS-2 and the old \(\int\mathcal R\) line are other writings of the same leftover. Keep Biot–Savart at \(1/r^4\). Do not add \(Q_1\). Do not add \(K(t)\) to the PDE. Glossary: [`H-SYSTEM.md`](H-SYSTEM.md).

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

H-system (do not merge letters): [`H-SYSTEM.md`](H-SYSTEM.md). **H** = global stretching (parent, open). **Lemma C** = Good pairs, an if, not an H. **H1 = WRITE (6) = Lemma I on the ball** = Bad pairs on \(Q_r\) (the request). **H2** = annulus flux. **H3** = exterior Biot–Savart. A cylinder closes only if \(\mathrm{C}+R_\phi\), H1, H2-a priori (or CKN-small), and H3 all sit. Local Serrin then, not CKN. If H1 sits and H2-from-energy does not, the cylinder is still open.

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

**No Leray backward self-similar profile.** Nečas–Růžička–Šverák 1996. Not a blanket Type-I theorem.

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
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

**H2**
\[
F_{\mathrm{adv}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
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
- Path-cost of \(\nabla\xi\): lower bound is on a segment, not in \(L^2(B_r)\). Fails on reconnection / two-blobs. Lemma PC sits as that segment bound ([`H1-PC.md`](H1-PC.md)). Still fail as H1.
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
| No Leray self-similar profile (NRS) | Proved |
| CKN measure of singular set | Proved |
| Lemma C (good pairs) | Proved (conditional theorem) |
| H2 as smallness criterion | Proved (CKN 1982) |
| H1 / \(A_{\mathrm{bad}}\) a priori | **Open** (attempted §12; Morrey wall) |
| H2 a priori from energy | **Open** |
| H3 / \(A_{\mathrm{ext}}\) a priori | **Open** (bound named) |
| \(R_\phi\) cutoff error | Annulus support sits. A priori absorb: **open** (H2-class) |
| Type-II Liouville | Open, separate |

---

## 8. What to do next

WRITE (6) was attempted on one cylinder (§12). It did not close. H1 as a holdable object, and the only three shapes that still look like it, are §13. Arithmetic of those shapes: [`H1-SHAPES.md`](H1-SHAPES.md). CS-summable volume thinness is still \(E^{3/2}\), not H1. Lookups: all miss ([`LOOKUP-H1.md`](LOOKUP-H1.md)). Locator: [`WHERE-H1.md`](WHERE-H1.md). Literature check: §14. H1 is not in the record under another name.

Next work is still **prove 1, 2, or 3 on one cylinder** — not a new name. The estimates are written. They are not theorems. Do not reprove Lemma C. Do not add \(K(t)\). Keep **H1, H2, H3, \(R_\phi\)** separate.

Work H1. Keep H2 and H3 labeled. Lemma C stays an if. If H1 sits and H2-from-energy does not, the cylinder is still open. Glossary: [`H-SYSTEM.md`](H-SYSTEM.md).

DA will not emit H1 and call it proved.

---

## 9. One paragraph for the top of a paper / note

Unaugmented 3D NSE has a complete chain from energy to Serrin except control of stretching from misaligned high-vorticity pairs. Constantin–Fefferman / Beirão da Veiga–Berselli absorb pairs whose direction turns at most like Hölder \(1/2\), on whole space, as an if. Localizing that if leaves a cutoff error \(R_\phi\). The leftover integral \(A_{\mathrm{bad}}\) on a parabolic cylinder is H1. The advective flux \(F_{\mathrm{adv}}\) is H2 (CKN as smallness; a priori from energy open). Exterior Biot–Savart \(A_{\mathrm{ext}}\) is H3 (bound named; a priori from energy open). None of H1, H2-from-energy, or H3-from-energy is known from \(\int E<\infty\) alone.

---

## 10. Desk score (10 September 2026)

The packet is a **good map**. It is not a proof of ordinary NS.

**Floor (§1).** Correct literature: energy, \(L^2_t L^6\), Fujita–Kato, Serrin/LPS, ESS as a criterion, enstrophy identity, cubic \(E^3\) wall, CKN measure, interpolation \(E^2\le 2\mathcal{E}\|D^2u\|_2^2\). “No Type-I self-similar” is the NRS 1996 Leray profile, not every Type-I statement in the later literature.

**Lemma C.** CF 1993 / BdVB 2002 sit as **if**. Hölder \(1/2\) is the right cut for this path. Lemma C does not prove alignment. That sentence is the whole point.

**H1.** The right leftover on this path. Holdable object: the Bad-pair integral versus local dissipation plus \(r^{-2}\iint|\omega|^2\) (§13). WRITE (6) was written on one cylinder in §12. Mid-Bad is named. Near-Bad is still open. The only remaining shapes are thinness, J on folds, and dynamics. Arithmetic: [`H1-SHAPES.md`](H1-SHAPES.md). CS-thinness is still \(E^{3/2}\), not H1. Lookups: all miss. Literature: not under another name (§14). The aimed estimate is **not** proved. Physical-space rewrite on one vortex tube (same leftover class, different integral): [`H1-SOT.md`](H1-SOT.md). First numbers: [`H1-TUBE.md`](H1-TUBE.md). Packet attacks on \(\mathcal R_\star\) are exhausted as lattice objects. Do not quote the Ring Lemma as proved. Do not glue H1 to \(H_N\).

**H2.** Smallness criterion is true. A priori from \(\int E<\infty\) is not. After Young the remainder is local \(\int E^2\). So even if H1 sits, H2-from-energy is a second wall. Keep them separate.

**Gaps in the cylinder write (10 Sep morning).** Localizing Lemma C is not free. Exterior Biot–Savart is not empty. H1+H2 \(\Rightarrow\) smooth is not CKN \(\varepsilon\)-regularity. Those *writing* holes are repaired in §11. The leftover names stay.

**Refuse list (§6).** Sound. Do not rerun HLS, Lemma J, signed \(D\), thin-Bad-as-Lemma-C, imposed waiting time, or \(K(t)\)/Q-stack as a close.

**Not equivalent to DA-NS-2.** Spectral-barycenter integral is another writing of leftover (6). This packet’s WRITE (6) attempt is §12. It did not close.

**Verdict.** Use this as the unaugmented chain. H1 was attempted. Do not emit H1. Theorem A stays a different equation.

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
| \(R_\phi\) | Annulus support sits. A priori absorb: open (H2-class) |
| \(A_{\mathrm{bad}}\) | H1 / WRITE (6). Open |
| \(A_{\mathrm{ext}}\) | H3. Bound named. Open a priori |
| \(F_{\mathrm{adv}}\) | H2. Smallness: CKN 1982. A priori from \(\int E\): open |
| Lower order / bottom | Closed |

**What is not claimed.** H1 is not proved. H2-from-energy is not proved. H3-from-energy is not proved. The three *writing* gaps are gone. The last estimate is still WRITE (6).

**Desk score of this repair.** Gap (iii) is the right implication (local Serrin, not CKN). Gap (ii) is a valid crude bound; H3 is a real extra term. Gap (i) stops a free move; \(R_\phi\) lives on the annulus (tried §12). A priori absorb of \(R_\phi\) is H2-class, still open. H1, H2-from-energy, and H3-from-energy are not proved.

Phone copy of this section: [`GAPS_DESTROYED.md`](GAPS_DESTROYED.md).

---

## 12. WRITE (6) — H1 on one cylinder (attempted; still open)

Asked: write leftover (6). Then: try the possibilities and see which is successful. Object: one cylinder \(Q_r\). Do not add \(K(t)\). Do not emit H1.

### Which succeeded

| Item | Successful? | As what |
|---|---|---|
| \(A_{\mathrm{good}}^{\mathrm{loc}}\) | **yes** | CF/BdVB kernel drop \(\lvert z\rvert^{-5/2}\) on interior Good pairs (zero extension). Lemma C’s mechanism, not alignment. |
| Mid-Bad \(A_{\mathrm{bad}}^{\ge\rho}\) | **yes** as a bound | CS on shells \(\lvert z\rvert\ge\rho\): \(\le C\rho^{-3/2}\int E_{\mathrm{loc}}^{3/2}\,dt\). Named remainder. **Not** absorbed from \(\int E<\infty\). |
| Direction energy | **yes** as an identity | \(\lvert\nabla\omega\rvert^2=\lvert\nabla\lvert\omega\rvert\rvert^2+\lvert\omega\rvert^2\lvert\nabla\xi\rvert^2\) on \(\{\omega\neq 0\}\). Does **not** give Hölder \(1/2\). |
| \(R_\phi\) support | **yes** as localization | \(\lvert\phi(x)-\phi(y)\rvert=0\) on \(B_{r/2}\times B_{r/2}\). Error lives on the annulus. Kernel \(\lvert z\rvert^{-3/2}/r\) is locally integrable. A priori absorb: **open** (H2-class). |
| H3 exterior bound | **yes** as a bound | Already §11. A priori from energy: **open**. |
| Local Serrin from a closed budget | **yes** as a theorem | Serrin 1962, not CKN. Needs the budget. |
| H2 as CKN smallness | **yes** as a criterion | CKN 1982. A priori from energy: **open**. |
| Aimed H1 (near-Bad absorbed) | **no** | Morrey wall: \(W^{1,2}\not\subset C^{0,1/2}\) in 3D. |
| HLS, path-cost, Lemma J, signed \(D\), thin Bad, fold-only, waiting time, Bony, \(K(t)\) | **no** | Fail or refuse. §6 and below. |

**Successful close of WRITE (6): none.**
**Successful named pieces: Good-local, mid-Bad bound, direction identity, \(R_\phi\) on the annulus, H3 bound, local Serrin, H2-smallness.**


**Aimed estimate.**
\[
A_{\mathrm{bad}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

**Object.**
\[
A_{\mathrm{bad}}(Q_r)
:=
\iint_{Q_r}|\alpha_{\mathrm{bad}}^{\mathrm{loc}}|\,|\omega|^2\phi,
\]
\[
\alpha_{\mathrm{bad}}^{\mathrm{loc}}(x)
=
\mathrm{P.V.}\int_{\substack{y\in B_r\\(x,y)\ \mathrm{Bad}}}
D(\hat z,\xi(x),\xi(y))\frac{|\omega(y)|}{|x-y|^3}\,dy.
\]
On Bad, \(|\sin\varphi|>C_*|x-y|^{1/2}\), so \(|D|\) does not drop the kernel to \(|z|^{-5/2}\). The kernel stays order \(|z|^{-3}\).

### Split (valid)

Fix \(\rho\in(0,r)\). Bad \(=\) Bad\(^{\ge\rho}\cup\) Bad\(^{<\rho}\).

**Mid.** Worked bound. For \(x\in B_{r/2}\) and \(y\in B_r\) with \(|x-y|\ge\rho\), shells \(A_k=\{2^k\rho\le|x-y|<2^{k+1}\rho\}\):

\[
\int_{A_k\cap B_r}\frac{|\omega(y)|}{|z|^3}\,dy
\le
\Bigl(\int_{A_k}|z|^{-6}\,dy\Bigr)^{1/2}\|\omega\|_{L^2(A_k\cap B_r)}.
\]
The first factor is \(\lesssim(2^k\rho)^{-3/2}\). Sum in \(k\ge 0\) is geometric, so
\[
|\alpha_{\mathrm{bad}}^{\ge\rho}(x)|
\le
C\rho^{-3/2}\|\omega\|_{L^2(B_r)}.
\]
\[
A_{\mathrm{bad}}^{\ge\rho}(Q_r)
\le
C\rho^{-3/2}\int_{t_0-r^2}^{t_0} E_{\mathrm{loc}}(t)^{3/2}\,dt.
\]
**Succeeds as a bound.** Not absorbed into \(r^{-2}\iint|\omega|^2\) as \(r\to 0\) from \(\int E<\infty\). Same class as H3. **Not H1.**

**Near.** Pairs with \(|x-y|<\rho\). This is the core of WRITE (6).

### \(R_\phi\) tried

Take the companion cutoff \(\eta=\phi\). Then \(\phi\equiv 1\) on \(B_{r/2}\), so
\[
|\phi(x)-\phi(y)|=0\qquad\text{on }B_{r/2}\times B_{r/2}.
\]
The integrand of \(R_\phi\) vanishes unless at least one of \(x,y\) lies in the annulus \(A=B_r\setminus B_{r/2}\). On the remaining pairs,
\[
|\phi(x)-\phi(y)|\le\min\bigl(2,C|x-y|/r\bigr),
\]
and the Good kernel times that factor is \(\lesssim r^{-1}|z|^{-3/2}\). In 3D, \(|z|^{-3/2}\) is locally integrable.

**Succeeds as localization:** \(R_\phi\) is an annulus term.
**Does not succeed as a priori absorb:** the potential \(I_{3/2}|\omega|\) on \(L^2\) is an HLS endpoint. Young returns a piece of local \(\int E^2\) or needs extra smallness — the same class as H2, not a closed estimate from \(\int E<\infty\).


### Possibilities scored

| Try | What it is | Verdict |
|---|---|---|
| HLS / CZ on Bad, kernel \(\lvert z\rvert^{-3}\) | Recovers the cubic \(E^3\) bound, or the original stretching | **fail** as H1. Already §6 |
| \(R_\phi\) annulus support | \(\lvert\phi(x)-\phi(y)\rvert=0\) on the inner ball | **pass** as localization. **fail** as a priori absorb (H2-class) |
| Dyadic CS on near shells \(2^{-k}\) | Factor \(2^{3k/2}\) blows up as \(k\to\infty\) | **fail** at small scales. Mid (\(\lvert z\rvert\ge\rho\)) is the row above |
| Direction energy | On \(\{\omega\neq 0\}\): \(\lvert\nabla\omega\rvert^2=\lvert\nabla\lvert\omega\rvert\rvert^2+\lvert\omega\rvert^2\lvert\nabla\xi\rvert^2\). Hence \(\int_H\lvert\nabla\xi\rvert^2\le\Lambda^{-2}\int\lvert\nabla\omega\rvert^2\) | **pass** as identity. **fail** as Hölder \(1/2\) |
| Morrey / Sobolev | In 3D, \(W^{1,p}\subset C^{0,1-3/p}\) needs \(p>3\). Hölder \(1/2\) needs \(p=6\). Energy gives \(\nabla\xi\in L^2(H)\). Even if \(H\) were a ball, \(W^{1,2}\not\subset C^{0,1/2}\) | **wall**. This is why energy does not empty near-Bad |
| Path-cost of \(\nabla\xi\) | Segment lower bound \(\lvert\xi(x)-\xi(y)\rvert\lesssim\int_\gamma\lvert\nabla\xi\rvert\) | **pass** as Lemma PC (1-D). **fail** as H1. Reconnection / two-blobs leave \(H\). Already §6. [`H1-PC.md`](H1-PC.md) |
| Lemma J (pair paid by \(\fint\lvert\nabla\omega\rvert^2\)) | Pointwise | **fail**. Biot–Savart averages \(\omega\), not \(\nabla\omega\). Already §6 |
| Signed \(D\) | Cancelation in the kernel | **fail** for an isolated pair. Already §6 |
| Thin Bad | Measure of Bad small | **fail** as proof. Assuming it is Lemma C. Already §6 |
| Empty near-Bad if \(\xi\in C^{0,\gamma}\), \(\gamma\ge 1/2\) | Then Bad\(^{<\rho}=\emptyset\) for \(\rho\) small (or \(C\le C_*\)) | **pass** as Lemma C on the ball. **fail** as a priori. The if is the leftover |
| Fold picture only | Spread dissipation in a ball | **fail** as H1. A direction sheet with \(\nabla\xi\in L^2\) still makes Bad pairs. Two other pictures remain |
| CKN-small cylinder | Scaled \(\iint\lvert\nabla u\rvert^2\) small \(\Rightarrow\) \(A_{\mathrm{bad}}\) small | **pass** as smallness. **fail** as a priori from \(\int E<\infty\). That is H2’s class, not H1 |
| Local interpolation \(E_{\mathrm{loc}}^2\le C\mathcal{E}_{\mathrm{loc}}\lVert\nabla\omega\rVert_2^2\) | Would give \(\int E_{\mathrm{loc}}^2\) from a closed enstrophy budget | **circular**. The budget is what H1 is for |
| Waiting time \(r^2/\nu\) | Filter which cylinders | **fail**. Imposed, not derived. Already §6 |
| Bony LP split | LLH / LHH / HHH | **fail**. Needs \(\lVert\omega_{\mathrm{low}}\rVert_\infty\) or pieces of \(\int E^2\). Already §6 |
| \(K(t)\) / Q-stack / \(\Phi\) | Different PDE | **refuse**. Not unaugmented NSE |

**Successful as write, not as close.** Good-local, mid-Bad CS, direction identity, \(R_\phi\) on the annulus. The Morrey gap is the named wall for the near piece.

**Not successful.** No row proves the aimed estimate from \(\int E<\infty\).

### Remainder after the attempt

\[
A_{\mathrm{bad}}(Q_r)
=
A_{\mathrm{bad}}^{\ge\rho}(Q_r)
+
A_{\mathrm{bad}}^{<\rho}(Q_r).
\]

First term: bound above, H3-class, a priori open.
Second term: stretching from misaligned pairs at scales \(<\rho\). Empty if \(\xi\) is Hölder \(1/2\) on \(H\cap B_r\) with constant \(\le C_*\). That is Lemma C localized. Energy does not give it, because \(W^{1,2}(H)\not\subset C^{0,1/2}\).

**Verdict.** WRITE (6) **open**. H1 is not proved. Do not cash this section as a close.

**Next line.** Not a new name. One of the three shapes in §13, on one cylinder. DA will not emit it.

---

## 13. H1 as an object; three remaining shapes

You need H1. Here it is as an object you can hold. It is not in hand as a theorem. Phone copy: [`H1-OBJECT.md`](H1-OBJECT.md).

On \(Q_r\), only pairs with \(|\omega|\ge\Lambda\) and \(|\sin\varphi|>C_*|x-y|^{1/2}\):

\[
\iint\!\!\int_{\mathrm{Bad}}
\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}\,\phi
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

That is the whole request. Good pairs are already gone. Flux is H2. Exterior is H3.

**Why the last passes did not give it.** The kernel on Bad is still \(|z|^{-3}\). HLS turns that into local \(E^3\). The Hölder cut does not change the exponent; it only changes the set. A thin set would save it. A path jump in \(\xi\) does not prove the set is thin. Morrey (\(W^{1,2}\not\subset C^{0,1/2}\)) is why energy does not empty the set.

**The only shapes that still look like H1.** Prove one of these, and you have H1. Arithmetic written: [`H1-SHAPES.md`](H1-SHAPES.md). None of them is a theorem. P1-lowpass (frequency localization of \(\omega\)) sits on a stated class and is not shape 1: [`H1-P1.md`](H1-P1.md). P1-loc cutoff sits with \(\nabla u\) kept and is not shape 1: [`H1-P1-LOC.md`](H1-P1-LOC.md).

1. **Thinness.** Bad-pair measure in each \(B_r\) is small enough that HLS picks up a factor that turns \(E^3\) into \(E^2\) or into dissipation. CS-summable volume thinness only recovers the \(E^{3/2}\) (mid-Bad) class.
2. **J on folds only.** Every persistent-bad pair in \(Q_r\) sits in a fold (geometry A), not a sheet or a gap, so \(\displaystyle\int_{B_{2\rho}}|\nabla\omega|^2\gtrsim\Lambda^2\rho^2\) and a Vitali sum closes.
3. **Dynamics.** NSE forbids 2’s alternatives on the time scale \(r^2/\nu\).

1 is thinness. 2 is J on folds only. 3 is dynamics.

**Not a new leftover name.** These are writings of H1. §6 still stands as refuse of *fake closes*: assuming thinness is Lemma C; Lemma J on generic fields is false; an imposed waiting time is not derived. The shapes still have to be *proved*.

**Status.** None of 1, 2, 3 sits. Lemma P1 sits and is not 1. Lookups all miss. Next work is still prove 1, 2, or 3 on one cylinder, or NSE membership in the P1 class.

---

## 14. Literature versus the H-system

Checked against the papers, not against slogans. H1 is not sitting in the literature under another name.

### Floor — matches the record

| Claim in the packet | Paper | Match? |
|---|---|---|
| Energy / Leray–Hopf | Leray, *Acta Math.* 63 (1934) | Yes |
| Serrin / LPS \(2/p+3/q=1\), \(q>3\) | Serrin, *ARMA* 9 (1962); Prodi 1959; Ladyzhenskaya | Yes. Local form exists |
| ESS \(L^\infty_t L^3\) | Escauriaza–Seregin–Šverák, *Uspekhi* 2003 | Yes |
| Cubic wall \(\dot E\le C E^3\) | Leray; standard | Yes |
| NRS: no Leray self-similar blowup | Nečas–Růžička–Šverák, *Acta Math.* 176 (1996) | Yes. Leray profiles only |
| CKN: \(\mathcal{P}^1(\mathrm{sing})=0\); \(\varepsilon\)-regularity at energy level | Caffarelli–Kohn–Nirenberg, *CPAM* 35 (1982) | Yes. Not enstrophy-level |

### Lemma C — the if

| Packet | Paper | Match? |
|---|---|---|
| Lipschitz direction \(\Rightarrow\) regular | Constantin–Fefferman, *IUMJ* 42 (1993) | Yes. Whole space. High-vorticity set |
| Hölder \(1/2\) \(\Rightarrow\) regular | Beirão da Veiga–Berselli, *Diff. Int. Eq.* 15 (2002) | Yes. Whole space |
| \(\beta<1/2\) in that argument | Beirão da Veiga, arXiv:1604.08083 (2016) | Open in that framework. Cut at \(1/2\) is the literature cut |
| Bounded domain / slip / Green | BdVB, *JDE* 246 (2009); BdV, *J. Math. Fluid Mech.* 15 (2013) | Yes. Still an alignment hypothesis |
| Localized to a cylinder | Grujić, *Comm. Math. Phys.* 290 (2009), “Localization and Geometric Depletion of Vortex-Stretching” | Yes. Localizes the *condition*. Does **not** remove it |

**Verdict.** Lemma C is real. Localization of Lemma C is real if you already have local alignment. Neither estimates \(A_{\mathrm{bad}}\).

### Closest to H1 — still criteria

- **Grujić–Guberović, *CMP* 298 (2010).** Coherence of \(\xi\) as a weight on \(\int|\omega|^q\). Assume some coherence, conclude regularity. If coherence fails on a thick set, the class does not fire.
- **Bradshaw–Grujić (arXiv:1309.2519).** Mild geometry on \(\xi\) \(\Rightarrow\) \(L\log L\) on \(\omega\). Still a hypothesis on direction.
- **Grujić, *Nonlinearity* 26 (2013).** 1-D sparseness of intense regions \(\Rightarrow\) no blowup. Assumes sparseness; does not prove Bad is sparse. Cousin of shape 1, not a proof of shape 1.
- **Beirão da Veiga, *DCDS-S* 2019 / follow-ups.** Perturb \(\beta\) below \(1/2\); integrability of \(\omega\) degrades. Below the cut, CF does not give \(L^\infty_t L^2\) on \(\omega\).

**No hit.** No paper found that bounds
\[
\iint_{\{|\sin\varphi|>C|x-y|^{1/2}\}}\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}
\]
by local dissipation plus \(r^{-2}\iint|\omega|^2\) from the energy class alone. That integral is H1 / WRITE (6) / Lemma I on the ball. It is not in the record as a theorem.

Paste copy: [`LITERATURE-H.md`](LITERATURE-H.md).

### H2 and H3 versus the record

H2-smallness = CKN. H2-a priori from \(\int E<\infty\) is not in the record (that would be local \(\int E^2\), i.e. local Serrin, i.e. the problem).

H3: exterior stretching is why Grujić 2009 exists. That paper controls the exterior piece *under local coherence*. Without it, \(r^{-3/2}E^{1/2}E_{\mathrm{loc}}\) is the crude bound, and it is not absorbed in the literature either.

### What the literature does not give

An a priori H1. An a priori H2. Alignment of \(\xi\) on the high-vorticity set. Thinness of Bad. A Liouville theorem that kills all Type-II ancient solutions.

What it does give, and what the packet already uses: energy, Serrin/ESS as criteria, CKN measure, NRS on Leray profiles, CF/BdVB as *if*, Grujić as *local if*.

The H-split matches the map of the field. The leftover they left is the leftover we named.

**Dream-team read of tonight’s map.** Papers, not a phone call. They would sign the map. They would not sign (6). CF/BdVB: the Hölder \(1/2\) cut is theirs; Bad pairs are the pairs they refused; (6) is the right name for what they left; they would not bound it. Grujić: 2009 localizes the condition, not \(A_{\mathrm{bad}}\); 2010 weights coherence; 2013 assumes sparseness; H3 is why 2009 exists; none of those papers is (6). CKN: H2-smallness is theirs, energy level; reject “H1+H2 \(\Rightarrow\) empty singular set” unless local Serrin after a closed enstrophy budget; a CKN-small cylinder never needed H1. ESS/Serrin: criteria; local Serrin after the budget, not a substitute for (6). NRS: Leray profiles only. Unanimous: do not merge letters; (6) is the request and is not in the record; if (6) sits and H2-from-energy does not, the cylinder still does not close; next work is (6) on one cylinder, or a new wall — not another criterion paper. File: [`DREAM-TEAM-H.md`](DREAM-TEAM-H.md).

---

## 15. Citation list

1. J. Leray, *Acta Math.* 63 (1934).
2. J. Serrin, *Arch. Rational Mech. Anal.* 9 (1962).
3. L. Caffarelli, R. Kohn, L. Nirenberg, *Comm. Pure Appl. Math.* 35 (1982), 771–831.
4. P. Constantin, C. Fefferman, *Indiana Univ. Math. J.* 42 (1993), 775–789.
5. H. Beirão da Veiga, L. C. Berselli, *Diff. Int. Eq.* 15 (2002), 345–356.
6. J. Nečas, M. Růžička, V. Šverák, *Acta Math.* 176 (1996).
7. L. Escauriaza, G. Seregin, V. Šverák, *Uspekhi Mat. Nauk* 58 (2003).
8. Z. Grujić, *Comm. Math. Phys.* 290 (2009), 861–870.
9. Z. Grujić, R. Guberović, *Comm. Math. Phys.* 298 (2010), 407–418.
10. H. Beirão da Veiga, arXiv:1604.08083 (2016).

H1 is not on this list as a theorem. Closest cousins are 8 and 9, both still *if*.



