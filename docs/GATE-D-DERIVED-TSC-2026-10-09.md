# Derived working definition of \(T_{\mathrm{sc}}\)

9 October 2026.
**A derivation from the Galerkin equation and the filed distinct-radii cut. Not the 20 September originals. Not an adoption of the PR #165 reconstruction. The project \(G\) does not follow.**

The September pages are still absent. This note does not replace them. It records the definition that the equation forces, so the symbol stops being empty.

---

## Conventions

Normalized torus \((\mathbb R/2\pi\mathbb Z)^3\). Real, mean-zero, divergence-free Galerkin field. Shell label means squared radius.

\[
\partial_t u=-B(u,u)+\nu\Delta u,
\qquad
B(v,w)=P[(v\cdot\nabla)w].
\]

\[
X=\sum_{k\neq 0}\lvert k\rvert^2\lvert u_k\rvert^2,
\qquad
Y=\sum_{k\neq 0}\lvert k\rvert^4\lvert u_k\rvert^2.
\]

The Fourier transform of \((u\cdot\nabla)u\) at \(k=p+q\) contributes the ordered term \(i(q\cdot u_p)u_q\). Because \(k\cdot u_k=0\), the Leray projection drops out of the pairing with \(u_k\).

\[
\tau_k=-\operatorname{Re}\bigl[\widehat B(k)\cdot\overline{u_k}\bigr]
=\sum_{p+q=k}\operatorname{Im}\bigl[(q\cdot u_p)(u_q\cdot\overline{u_k})\bigr].
\]

\[
T(u)=\sum_k\lvert k\rvert^2\tau_k.
\]

Differentiating \(X\) then gives the identity
\[
X'=2T-2\nu Y.
\]
This is the same normalization as the filed sharp-band sentence \(T=-\operatorname{Re}\langle B(h,h),-\Delta h\rangle\). Every ordered pair is counted once. There is no extra factor \(\tfrac12\) and no extra factor \(2\).

## The scalene cut

The filed sharp-band sentence says \(T_{\mathrm{sc}}\) retains precisely the interactions with three distinct squared radii. Apply that cut inside the sum:

\[
T_{\mathrm{sc}}(h)
=\sum_{\substack{p+q=k\\ \lvert p\rvert^2,\,\lvert q\rvert^2,\,\lvert k\rvert^2\ \mathrm{pairwise\ distinct}}}
\lvert k\rvert^2
\operatorname{Im}\bigl[(q\cdot u_p)(u_q\cdot\overline{u_k})\bigr],
\]
where every mode in the sum lies in the support of \(h\). For the Gate D field, \(h_{K,N}=P_{\lvert k\rvert>K}u_N\), so all three radii are strictly above \(K^2\). Modes at or below \(K\) are absent from this sum. They can still appear in a later derivative of \(T_{\mathrm{sc}}\). That derivative is not this definition.

The quantities already used in the 9 October note are then
\[
D=T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4,
\qquad
d=D/X_N,
\]
with \(X_N\) and \(Y_N\) the full-field moments. The episode budget remains \(B_I=\int_I d(t)\,dt\). The integrated positive part \(\mathcal S_{K,N}\) is not \(B_I\).

## Check against a printed triad

On the modes \((2,0,0)\), \((0,3,0)\), \((2,3,0)\) with coefficients \(iA e_2\), \(iA e_3\), \(iA e_3\) and their conjugates, the ordered sum at \(A=1\) has imaginary part \(24\), and \(X=52\). Those are the numbers printed for \(\mathcal T\) and \(X\) on the reconstruction page. The match checks the ordered sum. It does not adopt that page as the missing source.

## What this does not determine

The enstrophy identity does not name a second diagnostic \(G\).

The production probe now implemented in a copy of the Gaussian driver is
\[
G(s)=T(v(s))-Y(v(s))/200
\]
([`GATE-D-G-PROBE-2026-10-09.md`](GATE-D-G-PROBE-2026-10-09.md)).
That \(T\) is production, not \(T_{\mathrm{sc}}\). The orbit note’s \(G_T\) remains a resource constant. \(D\) and \(d\) remain unimplemented.

No crossing detector is built. Gate D remains OPEN / BLOCKED.

## STATUS

\(T_{\mathrm{sc}}\): DERIVED WORKING DEFINITION. NOT THE 20 SEPTEMBER ORIGINAL.
PRODUCTION PROBE \(G(s)=T-Y/200\): IMPLEMENTED IN A DRIVER COPY. NOT \(T_{\mathrm{sc}}\).
\(T_{\mathrm{sc}}\) AND \(D\): UNIMPLEMENTED. AUTHORITATIVE \(T_{\mathrm{sc}}\) STILL THE BLOCKER.
CROSSING DETECTOR: NOT BUILT.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
