# Gate A — positive shared-budget all-shape load

7 October 2026.
**UNRESOLVED / DIAGNOSTIC ONLY. Not OPEN, FAILED, or DEAD. Not (17).**

Previous “Outcome B / kill” wording is withdrawn as a program status.
The finite computations stay on the board as diagnostics.

Diagnostic \(\ell^1\) load:
[`GATE-A-KILL-CERTIFICATE-2026-10-07.md`](GATE-A-KILL-CERTIFICATE-2026-10-07.md).

Parents:
[`NS-HANDOFF-2026-10-07.md`](NS-HANDOFF-2026-10-07.md),
[`SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md`](SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md).

Probes:
- `scripts/ns_attacks/rho_formula_and_growth_probe.py`
- `scripts/ns_attacks/analytic_load_lower_bound.py`

Program: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).
Main line: [`GATE-B-THETA.md`](GATE-B-THETA.md).

---

## RESULT — diagnostic, not a verdict

| Item | Status |
|---|---|
| Charging convention F1/F2 | **FROZEN** (smallest-leg / multiplicity-5 stands; 6/4 not reopened) |
| \(\rho_5,\rho_9,\rho_{13}\) at \(c=25\) | **Exact match** (**Rerun here**) |
| General-\(c\) \(\rho\), including \(1/(2c)\) | **Diagnostic algebraic face. Not a source-of-truth lemma.** |
| Four-shell numeric table | Diagnostic only |
| \(L_{z_n}\) growth on \(z_n=2n^2\) | Diagnostic \(\ell^1\) load. **Not a kill.** |
| Coercive reason that \(C_{abc}\) is a paid cost | **Missing.** September 20 (16) is an upper bound. |
| Infinite sequence with proved divergent allocation cost | **Missing.** Do not manufacture one. |
| Straight positive assembly → all shapes | **Unresolved.** Finite 17/32/51 remain valid at stated scope. |
| Next | **Gate B / Dish #3** — global \(\sum f_x^2=E\), then \(\theta\) |

---

## 1. Frozen charging (summary)

| Question | Answer |
|---|---|
| Largest shell only? | **No** |
| Who pays? | Third labels \(b\) + family endpoints \(c_\star\) |
| Low anchor? | Global \(\sqrt{E}\) (Gate B) |
| Multiplicity? | Frozen smallest-leg / **multiplicity-5** convention stands. The 6 / zero-pruned 4 accounting is a separate filed tag and is **not reopened**. |

---

## 2. Filed \(\rho\) at \(c=25\); general-\(c\) not SoT

The October 7 51-shape note defines, at the filed low anchor and
\(c=25\),

\[
\rho_a
=
\frac1{50}
\left(\sum_{b\in B_a}
\frac{C_{a,b}^2}{b^2}\right)^{1/2}
=
\frac1{2c}
\left(\sum_{b\in B_a}
\frac{C_{a,b}^2}{b^2}\right)^{1/2}.
\]

September 20 already has
\(C_{abc}=\sqrt{3\Delta}(\lvert c-b\rvert/\sqrt a+\lvert c-a\rvert/\sqrt b+\lvert b-a\rvert/\sqrt c)\).
That majorant is an **upper** bound.

The same algebraic face with variable \(c\) is used in the probes.
It is **not** a promoted general-\(c\) allocation lemma under the
frozen smallest-leg convention.

Load (diagnostic):
\[
L_z:=\sum_a\rho_a(z)\quad\text{(Convention F2)}.
\]

---

## 3. Diagnostic \(\ell^1\) growth — not a kill

On the subnet
\(u=(k,0,\ell),\ v=(n-k,n,-\ell),\ w=(-n,-n,0)\)
with \(k/n\in[0.3,0.7]\), \(\ell/n\in[0,0.4]\), the \(\ell^1\)
sum \(L_{z_n}\) grows. Construction text:
[`GATE-A-KILL-CERTIFICATE-2026-10-07.md`](GATE-A-KILL-CERTIFICATE-2026-10-07.md).

This does **not** close Gate A:

- \(C_{abc}\) is an upper bound, not a coercive cost.
- General-\(c\) \(1/(2c)\) is not a source-of-truth lemma.
- No filed infinite sequence has a proved divergent *allocation cost*.

Numeric check of the spine (**Rerun here**):

| \(n\) | \(z_n\) | \(N_n\) | \(L_n^\star\) |
|---:|---:|---:|---:|
| 20 | 800 | 68 | 2.28 |
| 40 | 3200 | 227 | 3.85 |
| 80 | 12800 | 794 | 6.75 |
| 160 | 51200 | 2892 | 12.31 |
| 320 | 204800 | 10693 | 22.82 |

Do not extend this table to finish Gate A.

---

## 4. Gate B next

Force \(\sum_x f_x^2=E\). One Cauchy–Schwarz. Extract \(\theta\).
No more 52/70/100 family extensions. No larger-\(c\) chase.

---

## STATUS

GATE A: **UNRESOLVED / DIAGNOSTIC ONLY.**
NOT OPEN. NOT FAILED. NOT DEAD.
\(L_{z_n}\) GROWTH: DIAGNOSTIC \(\ell^1\) LOAD, NOT A KILL.
NEXT: GATE B / DISH #3.
(17) NOT CLAIMED.
NS NOT SOLVED.
