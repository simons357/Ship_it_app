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

A later archive, `gate_d_phi_reference_2026-10-09.zip`, is recorded in [`GATE-D-PHI-REFERENCE-2026-10-09.md`](GATE-D-PHI-REFERENCE-2026-10-09.md). Its internal \(+4m^3 A^3\) agreement is not a certification of the Lemma 19 witness. One polarization gives \(-4m^3 A^3\) under \(T=-\operatorname{Re}\langle B,-\Delta h\rangle\), and that negative value is not a pass. The Gaussian stepper is unchanged. The locked \(G=T-Y/200\) unit test was not rerun.

DA still reviews the implementation, the cutoff geometry, and the periodization protocol before any production run.

## STATUS

SIGNED STATIC RATIO: CLOSED AT EXPONENT \(1/2\). DYNAMICAL ESTIMATE: NOT ESTABLISHED.
DIAGNOSTICS CONFIRMED: \(D\), \(d=D/X_N\), \(B_I=\int_I d\), \(\mathcal S_{K,N}=\int(d)_+\).
\(\Phi_{abc}\) REFERENCE: SMALL-FIELD MODULE FILED. SEPTEMBER MARKDOWN PAGE NOT IN THE ZIP.
SIX-MODE WITNESS: NOT CERTIFIED. SIGN GAP UNRESOLVED.
GAUSSIAN STEPPER: UNCHANGED.
7 OCTOBER `signed_scalene.py`: REFERENCE ONLY.
\(G\) UNIT TEST: NOT RERUN.
GATE D: OPEN / BLOCKED.
NEXT MILESTONE: A TESTED SIGNED DIAGNOSTIC.
NS NOT SOLVED.
