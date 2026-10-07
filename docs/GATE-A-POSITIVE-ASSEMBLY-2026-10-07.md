# Gate A — positive shared-budget all-shape load

7 October 2026.
**OPEN — charging frozen; general \(\rho\) authorized; kill needs analytic \(L_{z_j}\to\infty\). Not (17).**

Parents:
[`NS-HANDOFF-2026-10-07.md`](NS-HANDOFF-2026-10-07.md),
[`SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md`](SHARED-BUDGET-32-SHAPE-EXTENSION-2026-10-06.md).

Probes:
- `scripts/ns_attacks/rho_formula_and_growth_probe.py` → `RHO-FORMULA-AND-GROWTH-PROBE.json`
- `scripts/ns_attacks/analytic_load_lower_bound.py` → `ANALYTIC-LOAD-LOWER-BOUND.json`

Program order:
[`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

---

## RESULT

| Item | Status |
|---|---|
| Finite-family mechanism (17/32/51) | Real and exact at stated scope — **laboratory**, not the all-shape route |
| Further 52/70/100 family extensions | **PARKED** — do not add |
| Charging convention | **FROZEN** (F1 family / F2 all-shape diagnostic) |
| Explicit \(\rho_a\) at fixed \(c_\star=25\) | Reproduces \(\rho_5,\rho_9,\rho_{13}\) **exactly** (**Rerun here**) |
| General-\(c\) \(\rho\) | **Authorized** (same face, variable output shell) |
| Four-shell numeric table | Diagnostic only — **cannot** stamp the kill |
| Analytic sequence \(L_{z_j}\to\infty\) | **ACTIVE** — subnet spine below; Landau–Ramanujan input |
| Kill certificate (Outcome B) | **OPEN** until the analytic lemma is accepted |
| Next after kill | Gate B — shared-energy correction |

Four numerical shells — even exact ones — do **not** close Gate A.
The remaining job: turn observed growth into an analytic lower-bound
sequence as \(z\to\infty\).

---

## 1. Frozen charging convention

| Question | Frozen answer |
|---|---|
| Largest shell only? | **No.** |
| Largest + middle? | Dissipation charges **third labels \(b\)** + **family endpoints \(c_\star\)** when dilated labels coincide. |
| Low anchor from global energy? | **Yes** — present faces borrow full \(\sqrt{E_0}\) (Gate B). |
| Multiplicity 4 vs 5? | **Never 5.** Literal **6** / zero-pruned **4**. |

### Convention F1 — fixed-anchor family (17/32/51 laboratory)

- Family: ordered anchors \((a_\star,c_\star)\) plus active thirds \(B\).
- \(c_\star\) is the **family output / high-pass endpoint**, not necessarily
  geometric \(\max\{a_\star,b,c_\star\}\) (thirds may exceed \(c_\star\)).
- Dissipation multiplicity (zero-pruned): third-shell \(bn^2=R\);
  witness \(R=216\) has multiplicity **exactly 4**.
- Coefficient:
  \[
  \rho_{a_\star}
  =\frac1{2c_\star}
  \left(\sum_{b\in B}
  \frac{C_{a_\star,b;c_\star}^2}{b^2}\right)^{1/2},
  \quad
  C_{a,b;c}
  =
  \sqrt{3\Delta_{a,b;c}}
  \left(
  \frac{\lvert c-b\rvert}{\sqrt a}
  +\frac{\lvert c-a\rvert}{\sqrt b}
  +\frac{\lvert b-a\rvert}{\sqrt c}
  \right).
  \]

### Convention F2 — largest-shell diagnostic

- Shapes with geometric max \(c\) (\(a<b<c\)).
- \(\rho_a(c)\) by the same formula; load
  \[
  L_z:=\mathcal A(z)=\sum_a\rho_a(z),\qquad
  \mathcal R(z)=L_z/\sqrt{z}.
  \]

Diagnostic table (**Rerun here**; author spine matched):

| \(z\) | \#shapes | \(L_z\) | \(\mathcal R(z)\) |
|---:|---:|---:|---:|
| 25 | 47 | 4.6857 | 0.937 |
| 50 | 226 | 9.8482 | 1.393 |
| 101 | 973 | 20.5423 | 2.044 |
| 401 | 11078 | 68.7256 | 3.432 |

---

## 2. General \(\rho\) beyond fixed \(c=25\)

\[
\boxed{
\rho_a(c)
=
\frac1{2c}
\left(\sum_{b\in B_a(c)}
\frac{C_{a,b;c}^2}{b^2}\right)^{1/2}
}
\]

No special role for the numeral 25.

| Anchor | Target | Computed | Match |
|---|---|---|---|
| 5 | 0.6318550824 | 0.6318550823987904 | **YES** |
| 9 | 0.8253067330 | 0.8253067330268598 | **YES** |
| 13 | 1.0833160571 | 1.0833160571… | **YES** |

\(B_{13}=\{2,4,8,14,18,20,22,26,36,38,40,50,54,56,58,62,68,72,74\}\)
(thirds may exceed \(c_\star\); prior miss was an enumeration cap).

---

## 3. Analytic kill spine (the remaining Gate A job)

**Definition.** \(L_z:=\mathcal A(z)\) under F2.

**Target.** An infinite sequence \(z_j\to\infty\) with \(L_{z_j}\to\infty\).
That is the legitimate Outcome B statement — not a four-point table.

### Subnet construction (**Rerun here**)

Let \(z_n=2n^2\). For integers
\((k,\ell)\) in the rectangle
\[
\frac kn\in[0.3,0.7],\qquad
\frac\ell n\in[0,0.4],
\]
the vectors
\[
u=(k,0,\ell),\quad
v=(n-k,n,-\ell),\quad
w=(-n,-n,0)
\]
realize an active non-collinear triangle on shells
\[
a=k^2+\ell^2,\quad
b=n^2+(n-k)^2+\ell^2,\quad
z_n=2n^2.
\]

**One-term lower bound.** On that rectangle, \(C_{a,b;z_n}/b\ge\kappa n\)
with \(\kappa\ge 1.48\) (**Rerun here**, stable in \(n\)). Hence
\[
L_n^\star
\ge
\sum_a\frac1{2z_n}\max_{b\in B_a^{\mathrm{sub}}}\frac{C}{b}
\ge
\frac{\kappa'}{n}
\cdot
\#\{\,k^2+\ell^2:(k,\ell)\in\mathcal R_n\,\}.
\]

**Number-theoretic input.** The number of distinct sums of two squares
in a \(\Theta(n)\times\Theta(n)\) rectangle is of Landau–Ramanujan type
\(\asymp n^2/\sqrt{\log n}\). Combined with the display above,
\[
L_n^\star\to\infty\qquad(n\to\infty),
\]
and therefore \(L_{z_n}\ge L_n^\star\to\infty\).

**Numeric check of the spine** (`analytic_load_lower_bound.py`):

| \(n\) | \(z_n\) | \#distinct \(a\) | \(L_n^\star\) (max-term LB) | \(L_n^\star/n\) |
|---:|---:|---:|---:|---:|
| 20 | 800 | 68 | 2.28 | 0.114 |
| 40 | 3200 | 227 | 3.85 | 0.096 |
| 80 | 12800 | 794 | 6.75 | 0.084 |
| 160 | 51200 | 2892 | 12.31 | 0.077 |
| 320 | 204800 | 10693 | 22.82 | 0.071 |

(\(L_n^\star/n\) drifts like \(1/\sqrt{\log n}\), consistent with
Landau–Ramanujan; \(L_n^\star\) itself increases.)

**Status of the lemma.** Construction + uniform \(C/b\) lower bound:
**Rerun here**. Distinct-sum cardinality asymptotics: standard
number-theory input — cite/accept to stamp Outcome B.
No further finite-family extensions while this is open.

### What this kills (once lemma accepted)

Straight positive shared-budget summation cannot keep \(L_z\) uniformly
controlled as the high shell runs through \(\{z_n\}\). Finite-family
success (17/32/51) remains real at stated scope and is **not** withdrawn.

---

## 4. After Outcome B — Gate B

Force low-frequency factors to share actual energy
\(\sum_k\lvert u_k\rvert^2=E\). Redo the aggregate. Extract the
**exact missing exponent**. That number alone feeds Gate D.

---

## STATUS

GATE A: **OPEN**.
CHARGING F1/F2: FROZEN.
ρ₅, ρ₉, ρ₁₃: RERUN MATCH; GENERAL-\(c\) AUTHORIZED.
NUMERIC TABLE: DIAGNOSTIC ONLY — NOT THE KILL.
ANALYTIC SPINE: \(z_n=2n^2\) SUBNET WITH \(L_n^\star\to\infty\) (LANDAU–RAMANUJAN INPUT).
NO MORE FINITE FAMILY EXTENSIONS.
(17) NOT CLAIMED.
NS NOT SOLVED.
