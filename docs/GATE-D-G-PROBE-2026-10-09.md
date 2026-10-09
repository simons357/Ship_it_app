# Gate D production probe \(G\)

9 October 2026.
**Diagnostic-level result. Not a Gaussian turnover result. The frozen experiment has not been launched. Gate D remains OPEN / BLOCKED.**

The probe was implemented in a copy of the existing Gaussian driver. The solver was not replaced.

\[
G(s)=T(v(s))-\frac{Y(v(s))}{200}.
\]

\(T\) here is the production term, not \(T_{\mathrm{sc}}\). An independent Fourier-triad calculation checked that production term against the driver's pseudospectral calculation. The reported result on a small periodic divergence-free Fourier field is **PASS**. The same test confirms that \(T_{\mathrm{sc}}\) and \(D\) remain unimplemented. Total production was not substituted for them.

The patch archive is not in this workspace, so this filing does not recheck the bytes or rerun the test. The reported ZIP SHA-256 is

```
d8fb4df9923ce563cf9ef9dc00787c4d0f8d08e87ef47065e5104bd9e4e2e1bd
```

An indexed-code search for \(T_{\mathrm{sc}}\), scalene, and mixed-length residual returned no matching source. That does not establish that the 20 September original is absent from every branch or archive. The authoritative \(T_{\mathrm{sc}}\) definition remains the principal diagnostic blocker.

Next: DA reviews this patch while that definition is recovered.

## STATUS

\(G\) PRODUCTION PROBE: IMPLEMENTED IN A DRIVER COPY. REPORTED INDEPENDENT TEST PASS.
NOT A TURNOVER RESULT. SOLVER NOT REPLACED. FROZEN EXPERIMENT NOT LAUNCHED.
\(T_{\mathrm{sc}}\) AND \(D\): UNIMPLEMENTED.
AUTHORITATIVE \(T_{\mathrm{sc}}\): STILL THE DIAGNOSTIC BLOCKER.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
