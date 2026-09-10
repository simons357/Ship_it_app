# Unaugmented 3D Navier–Stokes — working packet

**Date.** 10 September 2026  
**Use.** This is the live unaugmented-chain document.  
**Status.** Proof *chain*. Last estimate open. No augmentation, no \(K(t)\), no Q-stack. Only \(\nu\Delta u\).

Desk: leftover WRITE (6) on this path is **H1** (\(A_{\mathrm{bad}}\) a priori). **H2** a priori from energy is also open. Lemma C is a criterion, not alignment. Theorem A is a different PDE. DA-NS-2 and the old \(\int\mathcal R\) line are other writings of the same leftover, not this packet’s next write. Keep Biot–Savart at \(1/r^4\). Do not add \(Q_1\).

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

- \(A_{\mathrm{good}}\): Lemma C localized.
- \(A_{\mathrm{low}}\): \(\le C\Lambda\iint|\omega|^2\).
- \(A_{\mathrm{far}}\): empty if \(r<\delta\).
- \(F_{\nu}\): \(\le C\nu r^{-2}\iint_{\mathrm{annulus}}|\omega|^2\).

Left:

\[
\frac\nu2\iint_{Q_r}|\nabla\omega|^2
\le
\text{bottom}
+A_{\mathrm{bad}}(Q_r)
+F_{\mathrm{adv}}(Q_r)
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

---

## 5. Last line — two halves

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

If H1 and H2 hold for all small \(r\), the cylinder is regular at enstrophy level and the singular set is empty.

**H2.** True as a *smallness* criterion (energy-CKN-small cylinder). Not proved as an a priori bound from \(\int E<\infty\). Remainder after Young is local \(\int E^2\).

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
| H2 as smallness criterion | Proved |
| H1 / \(A_{\mathrm{bad}}\) a priori | **Open** |
| H2 a priori from energy | **Open** |
| Type-II Liouville | Open, separate |

---

## 8. What to do next

Work **H1** on a single cylinder \(Q_r\). Do not reprove Lemma C. Do not add \(K(t)\). Keep H1 and H2 separate so a failure is labeled.

Optional sibling (not shorter): \(L^\infty_t L^3\) mass on the bad set; Type-II profile. Only after H1 has a new estimate or a new wall.

DA will not emit H1 and call it proved.

---

## 9. One paragraph for the top of a paper / note

Unaugmented 3D NSE has a complete chain from energy to Serrin except control of stretching from misaligned high-vorticity pairs. Constantin–Fefferman / Beirão da Veiga–Berselli absorb pairs whose direction turns at most like Hölder \(1/2\). The leftover integral \(A_{\mathrm{bad}}\) on a parabolic cylinder, together with the advective enstrophy flux through the annulus, is the last line. Neither term is known to be bounded by local dissipation plus \(r^{-2}\iint|\omega|^2\) from the energy class alone.
