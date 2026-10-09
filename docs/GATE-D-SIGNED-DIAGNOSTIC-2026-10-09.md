# Signed diagnostic — confirmed identities

9 October 2026.
**The signed-transfer record is consistent. The static exponent does not establish the dynamical estimate. Gate D remains OPEN / BLOCKED.**

The static result is closed at exponent \(1/2\) for the specified signed ratio
\[
R(H)=\sup_{h\neq 0}\frac{|T_{\mathrm{sc}}(h)|}{\sqrt{E}\,Y}.
\]
That closure does not establish a dynamical estimate.

## Gate D diagnostics

\[
\begin{aligned}
D(t)&=T_{\mathrm{sc}}(P_{\lvert k\rvert>K}u_N)-\frac{\nu Y_N}{4},\\
d(t)&=\frac{D(t)}{X_N(t)},\\
B_I&=\int_I d(t)\,dt.
\end{aligned}
\]

The positive-part budget is a different integral:
\[
\mathcal S_{K,N}(T)=\int_0^T\bigl(d(t)\bigr)_+\,dt.
\]
On \(X_N>0\), \(\bigl(d\bigr)_+=(D)_+/X_N\), so this is the same positive-part integral already written with denominator \(X_N\) and no extra \(Y_N\). \(B_I\) integrates \(d\), including its negative values. \(\mathcal S_{K,N}\) integrates only the positive part.

## Next engineering task

Port the original 20 September \(\Phi_{abc}\) into the diagnostic evaluator, keeping its signs, its radius ordering, and its Hermitian-conjugate counting. Then test the six-mode identity \(T_{\mathrm{sc}}=4m^3 A^3\), and compare that value with an independently evaluated ordered Fourier convolution.

The Gaussian stepper stays disconnected until those checks pass. `scripts/ns_attacks/gate_d_signed_diagnostic/signed_scalene.py` remains the 7 October reference implementation. It is not a certified substitute for the September definition.

The three September pages are still not in this checkout, so \(\Phi_{abc}\) was not ported in this note. The six-mode identity was not tested. No ordered-convolution comparison was run. No new static theorem and no new smoke test were added. The locked \(G=T-Y/200\) unit test was not rerun.

DA still reviews the implementation, the cutoff geometry, and the periodization protocol before any production run.

## STATUS

SIGNED STATIC RATIO: CLOSED AT EXPONENT \(1/2\). DYNAMICAL ESTIMATE: NOT ESTABLISHED.
DIAGNOSTICS CONFIRMED: \(D\), \(d=D/X_N\), \(B_I=\int_I d\), \(\mathcal S_{K,N}=\int(d)_+\).
\(\Phi_{abc}\): NOT PORTED. SEPTEMBER PAGES NOT IN THIS CHECKOUT.
SIX-MODE WITNESS: NOT TESTED. ORDERED-CONVOLUTION COMPARISON: NOT RUN.
GAUSSIAN STEPPER: NOT CONNECTED.
7 OCTOBER `signed_scalene.py`: REFERENCE ONLY.
\(G\) UNIT TEST: NOT RERUN.
GATE D: OPEN / BLOCKED.
NEXT MILESTONE: A TESTED SIGNED DIAGNOSTIC.
NS NOT SOLVED.
