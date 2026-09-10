# The H-system

Different letters, different integrals. Do not merge them.
This H is stretching on unaugmented NSE. It is not matrix \(H_N\). It is not SND. It is not Theorem A’s Sobolev \(H^1\).

Phone packet: [`UNAUGMENTED-NS-CHAIN.md`](UNAUGMENTED-NS-CHAIN.md). H1 object: [`H1-OBJECT.md`](H1-OBJECT.md).

---

## H (old, global)

All stretching on \(\mathbb{R}^3\), paid by dissipation plus \((\int E)^2\). Parent claim. Open.

Do not cash a cylinder estimate as this parent. Do not cash this parent as H1.

---

## Split on one cylinder \(Q_r\)

**Lemma C — not an H.** Good pairs (direction turns at most like \(\sqrt{|x-y|}\)). Theorem as an *if* (CF 1993 / BdVB 2002). Localization to \(Q_r\) costs a cutoff error \(R_\phi\). Not free.

**H1 = WRITE (6) = Lemma I on the ball.** Same leftover. Not a new name. Bad pairs only, kernel still \(|z|^{-3}\):

\[
A_{\mathrm{bad}}(Q_r)
\le
\frac\nu8\iint_{Q_r}|\nabla\omega|^2\phi
+C r^{-2}\iint_{Q_r}|\omega|^2.
\]

Open. This is the request. HLS gives local \(E^3\). Path-cost of \(\nabla\xi\) dies on a sheet or a gap.

**H2 — flux through the skin,** \(r^{-1}\iint|u||\omega|^2\).
Smallness: proved (CKN 1982). From energy alone: open. Remainder is local \(\int E^2\).

**H3 — exterior Biot–Savart.** \(r<\delta\) does not kill it.

\[
A_{\mathrm{ext}}\le C r^{-3/2}\int E^{1/2}E_{\mathrm{loc}}\,dt.
\]

Written. Not absorbed as \(r\to 0\).

---

## When a cylinder closes

A cylinder closes only if \(\mathrm{C}+R_\phi\), H1, H2-a priori (or CKN-small), and H3 all sit. Local Serrin then gives smoothness on \(Q_{\theta r}\). That is not CKN.

If you get H1 and miss H2-from-energy, you still do not have the cylinder.

Work H1. Keep H2 and H3 labeled. Lemma C stays an if.

The estimate (stated, not proved): [`WRITE_6.md`](WRITE_6.md).
Supporting data: [`WRITE_6_SUPPORTED.md`](WRITE_6_SUPPORTED.md).
Dream-team read (map yes, (6) no): [`DREAM-TEAM-H.md`](DREAM-TEAM-H.md).

**Lemma★ is not an H.** Energy-budget writing of leftover (6) on \(\mathbb{T}^3\). Hypothesis. Exact form: scale-invariant trilinear bound on \(\mathcal R_\star\). Isolated triad: no kill. Same-shell packet: \(\mathcal D_s\) stayed the gap, \(T_c\) did not grow like \(m^{1/2}\); no kill. Remaining packet target: HH→L fan, or H1 on one cylinder. Uniform global triadic bound completely open. K=0 dead. Uniform pre-Young \(C\) dead. Samples are evidence only. Do not merge with H1. File: [`LEMMA-STAR.md`](LEMMA-STAR.md), [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md), [`LEMMA-STAR-E.md`](LEMMA-STAR-E.md), [`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md).
