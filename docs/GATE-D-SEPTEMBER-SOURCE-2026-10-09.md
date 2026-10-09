# September 20 signed-scalene source — reported recovery

9 October 2026.
**The source-definition blocker is reported removed. The implementation is not certified. Gate D remains OPEN / BLOCKED.**

The originals were not found by GitHub code search. They are reported present in the file library:

- `NS_SCALENE_EVOLUTION_IDENTITY_2026-09-20.md`
- `NS_REPEATED_RADII_AND_SCALENE_TARGET_2026-09-20.md`
- `NS_LEMMA_19_COUNTEREXAMPLE_2026-09-20.md`

Those three files are not in this checkout. A second pass did not open them in the Cursor uploads folder, in Drive title or full-text search, in Gmail, or in the fetched git trees. This note records the reported contents. It does not reproduce the pages, and it does not insert a formula.

## Reported contents

The evolution identity defines the radius-block trilinear form, with \(K^2<a<b<c\le N^2\). Both Hermitian-conjugate triples are counted, with no extra factor of two.

The high-frequency field is \(h=P_{\lvert k\rvert>K}u_N\). Its evolution receives nonlinear forcing from the full Galerkin solution, including lower frequencies.

The source specifies the Fourier normalization, the radius ordering, the signs, the conjugate-triple counting, and the full Galerkin forcing. The 7 October sharp-band theorem is no longer the page from which \(T_{\mathrm{sc}}\) has to be reconstructed.

The lemma-19 counterexample supplies a six-mode witness with \(T_{\mathrm{sc}}=4m^3 A^3\).

## What this does not do

Locating the source does not certify an implementation. The pages were not readable from this environment, so \(\Phi_{abc}\) was not copied into the diagnostic evaluator and was not reconstructed from the 7 October theorem or from `signed_scalene.py`. The six-mode witness has not been checked here. No comparison with an independent ordered Fourier convolution has been run for that witness. The locked \(G=T-Y/200\) unit test was not rerun.

No turnover, regeneration, or cutoff-independent budget is claimed. The frozen experiment has not been launched.

## Remaining work

1. Copy the three September 20 files into this repository.
2. Insert the exact \(\Phi_{abc}\) formula into the diagnostic evaluator.
3. Test it against the six-mode witness \(T_{\mathrm{sc}}=4m^3 A^3\).
4. Compare that value with an independently evaluated ordered Fourier convolution.
5. DA reviews the implementation, the cutoff geometry, and the periodization protocol before any production run.

## STATUS

SOURCE-DEFINITION BLOCKER: REPORTED REMOVED. FILES NOT YET IN THIS CHECKOUT.
IMPLEMENTATION: NOT CERTIFIED.
\(G\) UNIT TEST: NOT RERUN.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
