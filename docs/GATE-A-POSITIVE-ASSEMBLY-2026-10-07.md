# Gate A — positive shared-budget all-shape load

7 October 2026.
**\(L_{z_n}\) load note only. Not the sharp-band Gate A. Not (17).**

The sharp-band source leaves Gate A diagnostic and unresolved. Do not
carry “Gate A killed” into Gate C.

Kill certificate:
[`GATE-A-KILL-CERTIFICATE-2026-10-07.md`](GATE-A-KILL-CERTIFICATE-2026-10-07.md).

Parents:
[`NS-HANDOFF-2026-10-07.md`](NS-HANDOFF-2026-10-07.md),
[`SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md`](SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md).

Probes:
- `scripts/ns_attacks/rho_formula_and_growth_probe.py`
- `scripts/ns_attacks/analytic_load_lower_bound.py`

Program: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

---

## RESULT — Outcome B

| Item | Status |
|---|---|
| Charging convention F1/F2 | **FROZEN** |
| \(\rho_5,\rho_9,\rho_{13}\) | **Exact match** (**Rerun here**) |
| General-\(c\) \(\rho\) | **Authorized** |
| Four-shell numeric table | Diagnostic only |
| Analytic sequence \(L_{z_n}\to\infty\) | Load lower bound for this subnet — not the sharp-band Gate A |
| Straight positive assembly → all shapes | Not closed by the sharp-band source |
| Next | Gate C uses the sharp-band ratio, not this load |

---

## 1. Frozen charging (summary)

| Question | Answer |
|---|---|
| Largest shell only? | **No** |
| Who pays? | Third labels \(b\) + family endpoints \(c_\star\) |
| Low anchor? | Global \(\sqrt{E_0}\) (Gate B) |
| Multiplicity? | Literal **6** / zero-pruned **4** — never “5” |

---

## 2. Authorized \(\rho\)

\[
\rho_a(c)
=
\frac1{2c}
\left(\sum_{b\in B_a(c)}
\frac{C_{a,b;c}^2}{b^2}\right)^{1/2}
\]

with \(C_{a,b;c}=\sqrt{3\Delta}(\lvert c-b\rvert/\sqrt a+\lvert c-a\rvert/\sqrt b+\lvert b-a\rvert/\sqrt c)\).
Fixed \(c_\star=25\): \(\rho_5,\rho_9,\rho_{13}\) match. Variable \(c\): same face.

Load:
\[
L_z:=\sum_a\rho_a(z)\quad\text{(Convention F2)}.
\]

---

## 3. Load lower bound (not the sharp-band Gate A)

\[
\boxed{
z_n=2n^2,\qquad L_{z_n}\to\infty.
}
\]

Construction: subnet
\(u=(k,0,\ell),\ v=(n-k,n,-\ell),\ w=(-n,-n,0)\)
on \(\mathcal R_n\) with \(k/n\in[3/10,7/10]\), \(\ell/n\in[0,2/5]\).
Uniform \(C/b\ge\kappa n\) (\(\kappa=1.48\); continuum min at corner
\((3/10,0)\), \(\widetilde\Delta=9/100\)). Distinct two-square sums
\(N_n\gg_\varepsilon n^{2-2\varepsilon}\) via \(r_2(m)\ll_\varepsilon m^\varepsilon\). Hence
\[
L_n^\star\ge\frac{\kappa N_n}{4n}\to\infty,\qquad L_{z_n}\ge L_n^\star.
\]

Full proof text: [`GATE-A-KILL-CERTIFICATE-2026-10-07.md`](GATE-A-KILL-CERTIFICATE-2026-10-07.md).

Numeric check of the spine (**Rerun here**):

| \(n\) | \(z_n\) | \(N_n\) | \(L_n^\star\) |
|---:|---:|---:|---:|
| 20 | 800 | 68 | 2.28 |
| 40 | 3200 | 227 | 3.85 |
| 80 | 12800 | 794 | 6.75 |
| 160 | 51200 | 2892 | 12.31 |
| 320 | 204800 | 10693 | 22.82 |

---

## 4. Gate B next

Force \(\sum_k\lvert u_k\rvert^2=E\). Extract the exact missing exponent.
No more 52/70/100 family extensions.

---

## STATUS

SHARP-BAND GATE A: DIAGNOSTIC AND UNRESOLVED.
\(L_{z_n}\to\infty\) IS THIS LOAD ONLY. NOT A PREMISE OF GATE C.
(17) NOT CLAIMED.
NS NOT SOLVED.
