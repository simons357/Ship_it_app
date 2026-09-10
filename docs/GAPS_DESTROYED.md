# Three gaps, written until they stop being gaps

Installed as [`UNAUGMENTED-NS-CHAIN.md`](UNAUGMENTED-NS-CHAIN.md) §11.
WRITE (6) / H1 attempt: same file, §12. Still open.

The leftover names stay. What is destroyed is sloppiness: each gap is now either a cited theorem, an explicit remainder, or a labeled open estimate.

---

## Gap (iii) — destroyed as a citation hole

**Theorem (local Serrin from a closed enstrophy budget).**
Let \(u\) be a suitable weak solution of NSE on \(Q_{2r}\). Suppose

\[
\omega\in L^\infty(t_0-r^2,t_0;L^2(B_r))
\cap
L^2(t_0-r^2,t_0;H^1(B_r)).
\]
Then \(u\in L^4(t_0-r^2,t_0;L^6(B_r))\) up to the usual cutoff / Poincaré corrections on the ball, hence \(u\) is smooth on \(Q_{\theta r}\) for some universal \(\theta\in(0,1)\).

**Citations.** Serrin, *Arch. Rational Mech. Anal.* 9 (1962), local form of the \(L^p_t L^q_x\) criterion. Sobolev on the ball: \(\|u\|_{L^6(B_r)}\lesssim\|\nabla u\|_{L^2(B_r)}+r^{-1}\|u\|_{L^2(B_r)}\). The \(H^1\) bound on \(u\) is the \(L^2\) bound on \(\omega\). Bootstrap from \(L^4_t L^6_x\) to smooth is standard (e.g. the local regularity chapter in Terence Tao’s NS notes, or Lemarié-Rieusset).

**Not cited:** Caffarelli–Kohn–Nirenberg 1982. That theorem is energy-level \(\varepsilon\)-regularity (small scaled \(\iint|\nabla u|^2\)). It is the right citation for H2 as a *smallness* criterion. It is the wrong citation for “H1+H2 ⇒ smooth.”

**What this destroys.** The wave of the hand.
**What it does not destroy.** The need for the budget. If H1, H2-a-priori, and H3 all hold, the hypothesis of the theorem above is met. Those three bounds are still open.

NRS 1996 = no Leray backward self-similar profile. Not a blanket Type-I theorem.

---

## Gap (ii) — destroyed as a missing term; remainder explicit

For \(x\in B_{r/2}\),

\[
\alpha(x)
=
\alpha_{\mathrm{in}}(x)
+
\alpha_{\mathrm{ext}}(x),
\]

\[
\alpha_{\mathrm{ext}}(x)
=
\mathrm{P.V.}\int_{\mathbb{R}^3\setminus B_r}
D(\hat z,\xi(x),\xi(y))\frac{|\omega(y)|}{|x-y|^3}\,dy.
\]

If \(r<\delta\), every pair *inside* \(B_r\times B_r\) has \(|x-y|<\delta\). That kills only the interior far piece. \(\alpha_{\mathrm{ext}}\) remains.

**Bound that is valid.** For \(x\in B_{r/2}\) and \(y\notin B_r\), \(|x-y|\ge r/2\). Cauchy–Schwarz on dyadic shells \(A_k=\{y:2^k r\le|y-x|<2^{k+1}r\}\):

\[
|\alpha_{\mathrm{ext}}(x)|
\le
C\sum_{k\ge 0}
(2^k r)^{-3/2}\|\omega\|_{L^2(A_k)}.
\]

In particular

\[
|\alpha_{\mathrm{ext}}(x)|
\le
C r^{-3/2} E(t)^{1/2}.
\]

Hence

\[
A_{\mathrm{ext}}(Q_r)
:=
\iint_{Q_r}|\alpha_{\mathrm{ext}}|\,|\omega|^2\phi
\le
C r^{-3/2}\int_{t_0-r^2}^{t_0} E(t)^{1/2}\|\omega(t)\|_{L^2(B_r)}^2\,dt.
\]

**What this is.** An explicit H3. Not absorbed into \(r^{-2}\iint|\omega|^2\) as \(r\to 0\) without extra smallness or extra time integrability of \(E^{1/2}E_{\mathrm{loc}}\). Young against that product returns a piece of \(\int E_{\mathrm{loc}}^2\) or needs \(\sup E<\infty\).

**Status.** Gap in the *write* is gone. H3 is a named, scaled remainder. A priori control of H3 from \(\int E<\infty\) is **not** proved.

---

## Gap (i) — destroyed as a free localization; errors listed

Whole-space Lemma C (CF 1993; BdVB 2002 Hölder \(1/2\)) applies to integrals over \(\mathbb{R}^3\times\mathbb{R}^3\). On \(Q_r\) write, for \(x\in\operatorname{supp}\phi\),

\[
\alpha_{\mathrm{in}}(x)
=
\alpha_{\mathrm{good}}^{\mathrm{loc}}(x)
+
\alpha_{\mathrm{bad}}^{\mathrm{loc}}(x)
+
\alpha_{\partial}(x),
\]

where

- \(\alpha_{\mathrm{good}}^{\mathrm{loc}}\): both \(x,y\in B_r\), pair Good. Kernel drop \(|z|^{-5/2}\) applies to *this* double integral. Cutoff \(\phi(x)\) (not \(\phi(y)\)) leaves an error when one integrates \(\alpha|\omega|^2\phi\). That error is of the form
  \[
  R_\phi
  =
  \iint_{\mathrm{Good}\cap(B_r\times B_r)}
  \frac{|\omega(y)|}{|x-y|^{5/2}}|\omega(x)|^2|\phi(x)-\eta(y)|\,dx\,dy
  \]
  for a companion cutoff \(\eta\). This is the same class as \(F_{\mathrm{adv}}\) / \(F_{\nu}\) after Young — annulus + lower order — **or** it is not, and then it is an extra open term. It is not automatic from whole-space CF.

- \(\alpha_{\mathrm{bad}}^{\mathrm{loc}}\): both in \(B_r\), pair Bad. This is H1 / WRITE (6).

- \(\alpha_{\partial}\): \(x\in B_r\), \(y\notin B_r\). This *is* \(\alpha_{\mathrm{ext}}\), already H3.

**Literature that localizes the *hypothesis*, not the leftover.**
Grujić and collaborators: spatiotemporal localization of the Hölder-\(1/2\) direction condition (hybrid geometric-analytic criteria). Beirão da Veiga–Berselli 2009 (Green’s matrices, slip domain); 2013 Lipschitz up to the boundary. Those papers assume a direction condition *in the region of interest*. They do not prove \(A_{\mathrm{bad}}(Q_r)\) is small.

**Status.** “Lemma C on \(Q_r\)” is no longer used as a free move. Good-local + cutoff error is a lemma that must be written with \(R_\phi\) estimated, or cited from a localization paper under the Good-pair hypothesis *inside* \(B_{2r}\). That citation is available for the *aligned* hypothesis. It is not a proof of H1.

---

## Balance after the gaps are written

\[
\nu\iint_{Q_r}|\nabla\omega|^2\phi
\le
\text{bottom data}
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
| \(A_{\mathrm{good}}^{\mathrm{loc}}\) | Whole-space CF/BdVB mechanism, on interior Good pairs only |
| \(R_\phi\) | Cutoff error. Must be estimated or cited. Not free. |
| \(A_{\mathrm{bad}}\) | H1 / WRITE (6). Open |
| \(A_{\mathrm{ext}}\) | H3, bound \(r^{-3/2}\int E^{1/2}E_{\mathrm{loc}}\,dt\). Open a priori |
| \(F_{\mathrm{adv}}\) | H2. Smallness: CKN 1982. A priori from \(\int E\): open |
| Lower order / bottom | Closed |

Implication to smoothness on \(Q_{\theta r}\): Gap (iii) theorem, once the budget is closed.

---

## What is not claimed

H1 is not proved. H2-from-energy is not proved. H3-from-energy is not proved.
The three *writing* gaps are gone. The last estimate is still WRITE (6).
