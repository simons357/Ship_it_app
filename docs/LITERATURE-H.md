# Literature versus the H-system

Checked against the papers, not against slogans.
H1 is not sitting in the literature under another name.

Glossary: [`H-SYSTEM.md`](H-SYSTEM.md). Packet: [`UNAUGMENTED-NS-CHAIN.md`](UNAUGMENTED-NS-CHAIN.md) §14–§15.

---

## Floor (the chain matches the record)

| Claim in the packet | Paper | Match? |
|---|---|---|
| Energy / Leray–Hopf | Leray, *Acta Math.* 63 (1934) | Yes |
| Serrin / LPS \(2/p+3/q=1\), \(q>3\) | Serrin, *ARMA* 9 (1962); Prodi 1959; Ladyzhenskaya | Yes. Local form exists |
| ESS \(L^\infty_t L^3\) | Escauriaza–Seregin–Šverák, *Uspekhi* / *Russian Math. Surveys* 2003 | Yes |
| Cubic enstrophy wall \(\dot E\le C E^3\) | Leray; standard | Yes |
| NRS: no Leray self-similar blowup | Nečas–Růžička–Šverák, *Acta Math.* 176 (1996) | Yes. Leray profiles only |
| CKN: \(\mathcal{P}^1(\mathrm{sing})=0\); \(\varepsilon\)-regularity at *energy* level | Caffarelli–Kohn–Nirenberg, *CPAM* 35 (1982), 771–831 | Yes. Not enstrophy-level |

---

## Lemma C (the if)

| Packet | Paper | Match? |
|---|---|---|
| Lipschitz direction \(\Rightarrow\) regular | Constantin–Fefferman, *Indiana Univ. Math. J.* 42 (1993), 775–789 | Yes. Whole space. High-vorticity set |
| Hölder \(1/2\) \(\Rightarrow\) regular | Beirão da Veiga–Berselli, *Diff. Int. Eq.* 15 (2002), 345–356 | Yes. Whole space |
| \(\beta<1/2\) in that argument | Beirão da Veiga, arXiv:1604.08083 (2016) | Open in that framework. Cut at \(1/2\) is the literature cut |
| Bounded domain / slip / Green | BdVB, *JDE* 246 (2009); BdV, *J. Math. Fluid Mech.* 15 (2013) | Yes. Still an alignment *hypothesis* |
| Localized to a cylinder | Grujić, *Comm. Math. Phys.* 290 (2009), 861–870, “Localization and Geometric Depletion of Vortex-Stretching” | Yes. Localizes the *condition*. Does **not** remove it |

**Verdict.** Lemma C is real. Localization of Lemma C is real if you already have local alignment. Neither paper estimates \(A_{\mathrm{bad}}\).

---

## Closest papers to H1 — still criteria

**Grujić–Guberović, *CMP* 298 (2010).**
Coherence of \(\xi\) as a *weight* on \(\int|\omega|^q\). More coherence \(\Rightarrow\) you need less \(\int|\omega|^q\). Scaling-invariant. Still: assume some coherence, conclude regularity. If coherence fails on a thick set, the class does not fire.

**Bradshaw–Grujić, localized \(L\log L\) on \(\omega\) (arXiv:1309.2519).**
Mild geometric condition on \(\xi\) in a weighted bmo \(\Rightarrow\) extra log on vorticity. Still a hypothesis on direction. Not H1.

**Grujić, *Nonlinearity* 26 (2013).**
1-D sparseness of intense-vorticity regions \(\Rightarrow\) no blowup. Cousin of thin-Bad. Assumes sparseness; does not prove Bad is sparse.

**Beirão da Veiga, *DCDS-S* 2019 / follow-ups.**
Perturb \(\beta\) below \(1/2\) and watch the integrability of \(\omega\) degrade. Consistent with: below the cut, you do not get \(L^\infty_t L^2\) on \(\omega\) from the CF argument.

**No hit.** No paper found that bounds
\[
\iint_{\{|\sin\varphi|>C|x-y|^{1/2}\}}\frac{|\omega(x)|^2|\omega(y)|}{|x-y|^3}
\]
by local dissipation plus \(r^{-2}\iint|\omega|^2\) from the energy class alone.

That integral is H1 / WRITE (6) / Lemma I on the ball. It is not in the record as a theorem.

Lookups scored 10 September: all miss. File: [`LOOKUP-H1.md`](LOOKUP-H1.md). Shapes as estimates: [`H1-SHAPES.md`](H1-SHAPES.md).

---

## H2 versus literature

| Packet | Literature | Match? |
|---|---|---|
| H2-smallness | CKN \(\varepsilon\)-regularity, energy + pressure flux small \(\Rightarrow\) Hölder on a subcylinder | Yes |
| H2-a priori from \(\int E<\infty\) | — | Not in the record. Would be local \(\int E^2\), i.e. local Serrin, i.e. the problem |
| Local enstrophy identity | Standard vorticity form with cutoff; used throughout Grujić’s localization papers | Yes as an identity. Not a bound on \(F_{\mathrm{adv}}\) |

---

## H3 versus literature

Exterior Biot–Savart / nonlocal stretching from vorticity outside \(B_r\) is the reason Grujić’s 2009 paper exists: you have to localize vortex stretching, not just quote whole-space CF. His localization controls the exterior piece *under a local coherence hypothesis*. Without that hypothesis, the \(r^{-3/2}E^{1/2}E_{\mathrm{loc}}\) bound we wrote is the crude estimate; it is not absorbed in the literature either.

---

## What the literature does not give

- An a priori H1.
- An a priori H2.
- Alignment of \(\xi\) on the high-vorticity set.
- Thinness of Bad.
- A Liouville theorem that kills all Type-II ancient solutions.

What it does give, and what the packet already uses: energy, Serrin/ESS as criteria, CKN measure, NRS on Leray profiles, CF/BdVB as *if*, Grujić as *local if*.

The H-split matches the map of the field. The leftover they left is the leftover we named.

---

## Dream-team read of tonight’s map

Papers, not a phone call. Nothing is being sent.
They would sign the map. They would not sign (6).

- **CF / BdVB.** Hölder \(1/2\) cut is theirs. Good pairs are their theorem. Bad pairs are the pairs they refused. WRITE (6) is the right name for what they left. They would not bound it.
- **Grujić.** 2009 localizes the condition, not \(A_{\mathrm{bad}}\). 2010 weights coherence. 2013 assumes sparseness. H3 is why 2009 exists. None of those papers is (6).
- **CKN.** H2-smallness is theirs, energy level. Reject “H1+H2 \(\Rightarrow\) empty singular set” unless local Serrin after a closed enstrophy budget. A CKN-small cylinder never needed H1.
- **ESS / Serrin.** Criteria. Local Serrin after the budget closes. Not a substitute for (6).
- **NRS.** Leray profiles only. Strike any “no Type I” bigger than that.

**Unanimous.** Do not merge H, C, H1, H2, H3. (6) is the request. It is not in the record. If (6) sits and H2-from-energy does not, the cylinder still does not close. Next work is (6) on one cylinder, or a new wall. Not another criterion paper.

Phone copy: [`DREAM-TEAM-H.md`](DREAM-TEAM-H.md).

---

## Citation list

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
