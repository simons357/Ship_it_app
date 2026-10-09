# Recommended physical-cutoff convention

9 October 2026.
**Recommended for DA preregistration. Not approved. The matched doubled-box runs are resource-blocked. The frozen \(c=200\), \(s\ge 4\) experiment was not launched. Gate D remains OPEN / BLOCKED.**

Physical wavenumber at an integer cutoff \(N\) on a box of side \(L\) is \(2\pi N/L\). Holding that physical cutoff fixed while the box doubles requires the integer cutoff to double.

| Reference box | Doubled box | Physical cutoff |
| --- | --- | --- |
| \(L\), \(N=128\) | \(2L\), \(N=256\) | Matched: \(2\pi\cdot 128/L\) |
| \(L\), \(N=160\) | \(2L\), \(N=320\) | Matched: \(2\pi\cdot 160/L\) |

\(N=128\) and \(N=160\) stay the reference-box cutoffs. The doubled-box rows are additional matched-resolution comparisons. They do not replace the frozen reference-box runs.

The logger rule \(N<n/3\) then requires \(n>960\) for \(N=320\). The smallest such grid is \(n=961\). The current preflight estimates \(576 n^3\) bytes and uses a 2 GiB ceiling (`fail_closed.preflight`). That estimate is about 476 GiB at \(n=961\), so the run is rejected before any transfer. The same ceiling also rejects the reference grids: \(N=128\) needs \(n>384\) (about 31 GiB at \(n=385\)), and \(N=160\) needs \(n>480\) (about 60 GiB at \(n=481\)). The estimate is not a peak-RSS certificate. It is enough to mark these configurations infeasible in the current implementation.

This states the mathematical comparison. It does not run it. DA approval of the interpretation is still pending, so item 6 stays blocked. After that approval, the remaining priorities are a scalable numerical-error certificate and a feasible domain-convergence protocol. A sign of \(D\) on a frozen coefficient array does not certify the trajectory.

## STATUS

CONVENTION: RECOMMENDED. NOT DA-APPROVED.
REFERENCE LABELS: \(N=128\) AND \(N=160\) ON THE REFERENCE BOX.
MATCHED DOUBLED BOX: \(N=256\) AND \(N=320\). RESOURCE-BLOCKED.
CURRENT 2 GiB PREFLIGHT: REJECTS \(n=385,481,769,961\).
FROZEN \(c=200\), \(s\ge 4\): NOT LAUNCHED.
GATE D: OPEN / BLOCKED.
NS NOT SOLVED.
