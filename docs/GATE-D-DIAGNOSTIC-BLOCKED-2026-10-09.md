# Gate D diagnostic — definitions not on hand

9 October 2026.
**The original definitions are not in the notes on hand. The scaffold audit cannot supply them. \(T_{\mathrm{sc}}\) and the project \(G\) remain undefined for implementation. The reconstruction is not implemented. A crossing detector is not built. Gate D remains open and blocked.**

---

## What is present

Only the use of the symbols.

The 9 October Gate D note sets
\[
D(t)=T_{\mathrm{sc}}(h_{K,N}(t))-\nu Y_N(t)/4,
\qquad
d(t)=D(t)/X_N(t),
\]
with \(X_N\), \(Y_N\) the full-field moments and \(h_{K,N}\) the high-pass field. It does not define the triad sum inside \(T_{\mathrm{sc}}\).

The 7 October Gate B assembly bounds \(\lvert T_{\mathrm{sc}}(h)\rvert\) by the complete-block majorant \(M_H\), and points to `NS_REPEATED_RADII_AND_SCALENE_TARGET_2026-09-20.md`, Section 5, equations (15)–(18), plus the scalar triple-product form in Section 1 of `NS-51-Shape-Extension-2026-10-07.md`. Those two files are not attached.

The 8 October audit defines production
\[
T=\int\omega\cdot S(u)\,\omega
\]
and, as a proposed probe only,
\[
G(s)=T(v)-Y(v)/c.
\]
That \(G\) is explicitly not the project diagnostic, and that \(T\) is not \(T_{\mathrm{sc}}\).

## What is missing

The missing source is the 20 September scalene-target note, equations (15)–(18), together with whatever note defines the project \(G\) used in \(D\). Fourier normalization and triad-counting conventions have to come from those pages. They should not be reconstructed from the majorant, the production integral, or the scaffold’s null fields.

Until those pages are attached, the diagnostic implementation stays blocked. Gate D remains open.

## Seated reconstruction, not adopted

The 20 September originals are not in the repository. `docs/FOURIER-TRIANGLE.md` on `cursor/signed-scalene-next-c3ed` (PR #165) is a reconstruction, not those originals. `NS_LEMMA_19_COUNTEREXAMPLE_2026-09-20.md` and `NS_SCALENE_EVOLUTION_IDENTITY_2026-09-20.md` are not filed.

\(T_{\mathrm{sc}}\) and the project \(G\) remain undefined for implementation.

The seated reconstruction, not adopted as the missing source, is: on the normalized torus, \(B(v,w)=P[(v\cdot\nabla)w]\), shell labels equal squared radii,

\[
\tau_k=-\operatorname{Re}\bigl[\widehat B(k)\cdot\overline{u_k}\bigr],
\qquad
\mathcal T(u)=\sum_k\lvert k\rvert^2\tau_k.
\]

For distinct squared radii \(a<b<c\) and \(p+q+r=0\),

\[
I_p=\sum\operatorname{Im}\bigl[(q\cdot u_p)(u_q\cdot u_r)\bigr],
\]

with \(I_q\), \(I_r\) cyclic, and

\[
\mathcal T_{abc}=(c-b)I_p+(a-c)I_q+(b-a)I_r,
\]

negative triple included, no extra factor of two. \(T_{\mathrm{sc}}(h_{K,N})\) is the sum of those complete triads on \(h_{K,N}=P_{\lvert k\rvert>K}u_N\). The same page gives the integrated positive part

\[
\mathcal S_{K,N}(T)
=\int_0^T
\frac{\bigl[T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4\bigr]_+}{X_N}\,dt,
\]

which is not the episode budget \(B_I\).

That page does not define a diagnostic named \(G\). The episode-balance note defines \(D=T_{\mathrm{sc}}(P_{>K}u)-\nu Y/4\) and \(d=D/X\). The orbit note’s \(G_T\) is a resource constant, not a pointwise diagnostic. The 8 October \(G(s)=T(v)-Y(v)/c\) is a proposed production probe, not either of those.

Until the 20 September scalene-target pages are attached, the reconstruction is not implemented and a crossing detector is not built. Gate D remains open and blocked.

## STATUS

DEFINITIONS OF \(T_{\mathrm{sc}}\) AND THE PROJECT \(G\): NOT ON HAND. UNDEFINED FOR IMPLEMENTATION.
20 SEPTEMBER ORIGINALS: NOT IN THE REPOSITORY.
FOURIER-TRIANGLE ON PR #165: RECONSTRUCTION, NOT ADOPTED AS THE MISSING SOURCE.
RECONSTRUCTION: NOT IMPLEMENTED. CROSSING DETECTOR: NOT BUILT.
DIAGNOSTIC IMPLEMENTATION: BLOCKED.
GATE D: OPEN AND BLOCKED.
\(\mathcal S_{K,N}\) IS NOT THE EPISODE BUDGET \(B_I\).
NS NOT SOLVED.
