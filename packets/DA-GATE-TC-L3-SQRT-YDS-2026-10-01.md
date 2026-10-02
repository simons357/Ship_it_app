# DA gate — half-spread candidate \(|T_c|\le C\|\nabla u\|_3\sqrt{YD_s}\)

**1 October 2026.** Attack, not a proof.
Unrestricted \(\sup\mathcal R_\star<\infty\) stays **KILLED**.
DA-NS-2 stays **OPEN**. Ordinary NS is not solved.

Page:
[`../docs/ns-recovery/TC-L3-SQRT-YDS.md`](../docs/ns-recovery/TC-L3-SQRT-YDS.md).
Machine: `scripts/da_gate_tc_l3_sqrt_yds.py`.

Does **not** alter the locked SBP / \(\phi/d\) / low-tail / sign /
\(S_{pq}\) / local-★ / 71E / 83 packets. Does **not** stamp
\(r\sim\kappa^{-1/2}\). Localized bump is not on this tree.

---

## Locked as OPEN

\[
\lvert T_c\rvert
\le
C\,\|\nabla u\|_3\sqrt{YD_s}.
\]

\(Y=\|Av\|_2^2\). \(\|\nabla u\|_3\) is physical Haar \(L^3\) of
the Frobenius gradient, recovered from the finite Fourier field
(Parseval \(\|\nabla u\|_2^2=X\) sits). No proxy. No \(C\) stamped.

---

## Why this target

Near-shell \(v_\varepsilon=w+\varepsilon z_\beta\):

\[
D_s\sim\varepsilon^2,\qquad T_c\sim\varepsilon.
\]

So \(T_c/D_s\) blows and \(T_c/\sqrt{D_s}\) stays. Linear-in-\(D_s\)
is exactly obstructed. The square-root scale is the one to attack.
That obstruction **motivates** the candidate and does **not**
establish it.

\(T_c\), \(Y\), \(D_s\), \(\|\nabla u\|_2=\sqrt{X}\) are exact
Fourier arithmetic. Sampled quadrature of \(\|\nabla u\|_3\)
**cannot certify a counterexample**. A kill needs the certified
lower bound (from exact \(\|\nabla u\|_4\) or the Fourier
\(\ell^1\) majorant) to blow. A script run verifies identities.
The uniform inequality and its time budget remain separate
proof obligations.

---

## Small-case attack — three lanes

Exact Fourier arithmetic certifies \(T_c\), \(Y\), \(D_s\), and
\(\|\nabla u\|_2=\sqrt{X}\). Sampled quadrature of
\(\|\nabla u\|_3\) cannot certify a counterexample. The kill
number is the certified lower bound; the “this field does not
kill” number is the certified upper bound
\(\lvert T_c\rvert/(\sqrt{X}\sqrt{YD_s})\).

| Lane | Max cert lower | Max cert upper | Certified kill |
|---|---:|---:|---|
| Nearly single-shell, several triads | \(0.0888\) | \(0.0920\) | no |
| Separated frequencies, varied amps | \(0.00516\) | \(0.00551\) | no |
| Dense coordinated packets | \(0.0484\) | \(0.0533\) | no |

Strongest small-case row: fat closer \((5,6)\). Note triad remains
larger (\(0.166\le\cdot\le 0.175\)). No certified counterexample.
A script run verifies identities. The uniform inequality and its
required time budget remain separate proof obligations.

## On-tree score

| Family | Verdict |
|---|---|
| Near-shell \((5,4)\) | \(T_c/D_s=\Theta(\varepsilon^{-1})\); new ratio \(\approx 0.042\), flat |
| Note triad | largest seated, cert \(0.166\le\cdot\le 0.175\) |
| Fat closer \((5,6)\) | strongest small-case, cert \(0.089\le\cdot\le 0.092\) |
| Clustered aligned triads | cert \(0.048\le\cdot\le 0.053\) |
| Separated, varied amps | cert upper \(\le 0.0055\) |
| Same-helicity box | \(T_c=0\) (Beltrami; not a kill) |
| \(v_n\) \(n=1..8\) | \(\sqrt{\mathcal R_\star}\) grows; new slot **falls**; cert upper \(0.018\to 0.006\) |
| Localized bump | **not on this tree** |

The candidate is **not proved**. The near-shell obstruction
motivates it and does not establish it. Unrestricted ★ stays dead.

**NS not solved.**
