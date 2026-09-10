# The H-system

Different letters, different integrals. Do not merge them.
This H is stretching on unaugmented NSE. It is not matrix \(H_N\). It is not SND. It is not Theorem A’s Sobolev \(H^1\).

Phone packet: [`UNAUGMENTED-NS-CHAIN.md`](UNAUGMENTED-NS-CHAIN.md). H1 object: [`H1-OBJECT.md`](H1-OBJECT.md). Locator: [`WHERE-H1.md`](WHERE-H1.md). Path-cost (1-D, not H1): [`H1-PC.md`](H1-PC.md). Tube SoT: [`H1-SOT.md`](H1-SOT.md).

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

Physical-space rewrite on one vortex tube (same leftover class, different integral): [`H1-SOT.md`](H1-SOT.md). Estimate package: [`DOOR-B-H1-ESTIMATE-PLAN.md`](DOOR-B-H1-ESTIMATE-PLAN.md) (OPEN, not a GR close). Packet attacks on \(\mathcal R_\star\) are exhausted as lattice objects. H1 opened there. First computation: \(J\) and thinness ([`H1-TUBE.md`](H1-TUBE.md)). Do not merge the integrals. Do not quote the Ring Lemma as proved. Do not glue H1 to \(H_N\). Outside-\(\mathcal{E}\) identity blocked. Enumerator still on the ★ lane.

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
Shapes as estimates, not proved: [`H1-SHAPES.md`](H1-SHAPES.md).
P1 low-pass Biot–Savart (sits; not H1): [`H1-P1.md`](H1-P1.md).
Lookups: all miss ([`LOOKUP-H1.md`](LOOKUP-H1.md)).
Dream-team read (map yes, (6) no): [`DREAM-TEAM-H.md`](DREAM-TEAM-H.md).

**Lemma★ is not an H.** Energy-budget writing of leftover (6) on \(\mathbb{T}^3\). Hypothesis. Exact form: scale-invariant trilinear bound on \(\mathcal R_\star\). Working claim: [`math/ns_attacks/LEMMA_STAR_CANONICAL.md`](math/ns_attacks/LEMMA_STAR_CANONICAL.md), [`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md). Four corrections: [`LEMMA-STAR-CORRECTIONS.md`](LEMMA-STAR-CORRECTIONS.md). The \(a^4\) missing inequality is dead. ★ \(\Rightarrow\) GR in this packaging; not equivalent. Lattice packets scored (isolated triad, AP, adjacent spheres, Freiman-AP subset, HH→L fan \(\mathcal R_\star\sim\beta/\alpha\)): no kill. The \(m^{1/2}\) heuristic has not found a lattice home. Route A incidence: conditional continuum \(I\ll m^{4/3}\Rightarrow C(S)=O(m^{4/3})\); lattice transfer MISSING ([`LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md`](LEMMA-STAR-STRUCTURE-ROUTE-A-INCIDENCE.md)). Other live writing: H1 on one cylinder ([`H1-SOT.md`](H1-SOT.md)). Uniform global triadic bound completely open. K=0 dead. Uniform pre-Young \(C\) dead. Samples are evidence only. Do not merge with H1. File: [`LEMMA-STAR.md`](LEMMA-STAR.md), [`LEMMA-STAR-R.md`](LEMMA-STAR-R.md), [`LEMMA-STAR-E.md`](LEMMA-STAR-E.md), [`LEMMA-STAR-PACKET.md`](LEMMA-STAR-PACKET.md). Original five-lane JSON: [`five-lane-export/COMPUTE.md`](five-lane-export/COMPUTE.md). Attack 9B: [`five-lane-export/ATTACK_9B.md`](five-lane-export/ATTACK_9B.md). Counting: [`LEMMA-STAR-9B-COUNTING.md`](LEMMA-STAR-9B-COUNTING.md).
