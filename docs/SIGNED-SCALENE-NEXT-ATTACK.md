# Signed scalene — next attack

4 October 2026.
**Return priority to criterion (17).
Energy-only reverse of \(\mathcal S^{(3)}\) stays KILLED.
No fake proof. NS not solved. Not Clay.**

Authoritative full packet:
[`../packets/Signed-Scalene-Next-Attack-2026-10-04.md`](../packets/Signed-Scalene-Next-Attack-2026-10-04.md).

Parents (brought onto this branch from
PR #153 / PR #159 heads; not mixed with
claim-ledger or aerostat packs):

- [`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md)
  — identities; remaining sufficient
  theorem is (17).
- [`L3-BUDGET-GATES.md`](L3-BUDGET-GATES.md)
  — (L3-1)–(L3-5); (L3-5) OPEN,
  equivalent in role to (17), not an
  energy-only universal bound.
- [`L3-5-EXACT-SHEAR-OBSTRUCTION.md`](L3-5-EXACT-SHEAR-OBSTRUCTION.md)
  — energy-only strengthening of (L3-5)
  **FALSIFIED**; shears give \(S\equiv 0\).
- [`TWO-SHELL-SPATIAL-REGENERATION.md`](TWO-SHELL-SPATIAL-REGENERATION.md)
  — desk pointer; full write
  [`DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md`](DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md)
  (two-shell spatial signed assembly
  survives, no occupancy;
  regeneration of all-high scalene is
  the remaining blank).
- [`TWO-TRIANGLE-NORMAL-ANGLE.md`](TWO-TRIANGLE-NORMAL-ANGLE.md)
  — \(\rho_2=1/\sqrt2\) is the orthogonal
  \(e_2\) special case; near-parallel
  oriented normals send \(\rho\to 1\).
- [`ALL-HIGH-T6-K2-DATUM.md`](ALL-HIGH-T6-K2-DATUM.md)
  — all-high local jet on the \(K=2\)
  datum: \((15084/1625)t^6+O(t^7)\).
- [`BLOCK-5825-FIRST-ATTEMPT.md`](BLOCK-5825-FIRST-ATTEMPT.md)
  — one complete regenerated block
  \((5,8,25)\): evolution written;
  intra-block dilation-stable;
  external energy-only absorption
  fails; summing blocks still open.
- [`Q-OTHER-51025.md`](Q-OTHER-51025.md)
  — \(\mathcal Q^{\mathrm{other}}\) split:
  joint \(S_4=\{5,8,10,25\}\) finite.
- [`BLOCK-5825-PARTIAL-BOUNDS.md`](BLOCK-5825-PARTIAL-BOUNDS.md)
  — author correction: fixed-block bounds
  (P1)–(P3) including outside inputs;
  all-shape assembly still OPEN toward (17).
- [`TRUTH-RUN-CAVEATS.md`](TRUTH-RUN-CAVEATS.md)
  — Duhamel STANDARD; \(\int\lvert Q\rvert\) unchecked;
  budget \(\neq\int\lvert T_{5825}\rvert\);
  SCHEME A (sum per shape) FAILED.

## STATUS board

| Object | Status |
|---|---|
| Fourier-triangle geometry (1)–(7), (14), (18) | **PROVED** (EXACT identities; keep hypotheses) |
| Exact-sphere / repeated-radius working bound \(\lvert\mathcal T_{\mathrm{rep}}\rvert\le(\sqrt3/2)X\sqrt Y\) | **CLAIMED / seated** (analytic working estimate; not global closure) |
| Complement control \(\Rightarrow\) conditional \(X\) bound (16) given \(S\) | **PROVED** as conditional algebra on seated inputs |
| Classical (L3-1); one-way (L3-4): \(S\le C_S S^{(3)}+\mathrm{controlled}\) | **PROVED** |
| Fixed-datum (L3-5): \(\sup_N S^{(3)}_{K,N}(T)<\infty\) with \(K=K(u_0,\nu)\) | **OPEN** (not refuted by shears) |
| Criterion (17): \(\sup_N S_{K,N}(T)<\infty\) with \(K=K(u_0,\nu)\) | **OPEN** — **priority target** |
| Two-shell complete signed assembly \(\mathcal T=(b-a)(j_{b\leftarrow aa}-j_{a\leftarrow bb})\) | **Spatial test survives** (no occupancy); full write [`DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md`](DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md) |
| Frozen \(K\) from initial \(\dot H^{1/2}\) tail | **Written** (datum-sensitive; \(t=0\) uniform in \(N\)) |
| Regenerated all-high scalene in time | **Local jet written** on \(K=2\) datum: \(\mathcal T_{\mathrm{sc}}(h_2)=(15084/1625)t^6+O(t^7)\); orders \(\le t^5\) vanish; \(\nu\)-independent — [`ALL-HIGH-T6-K2-DATUM.md`](ALL-HIGH-T6-K2-DATUM.md). Integrated budget / (17) still **OPEN** |
| Universal energy-only \(F(E_0,\nu,K,T)\) on \(S^{(3)}\); reverse \(S^{(3)}\lesssim S+F\) | **KILLED** (exact shear obstruction, 3 Oct 2026) |
| Unrestricted \(\star\); charge-only close; Theorem H as NS close | **KILLED** (prior desks) |
| Global regularity / Clay / RH | **NOT CLAIMED** |

## Criterion (17) — vault statement

From [`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md) §11:

\[
h_{K,N}=P_{\lvert k\rvert>K}u_N,
\quad
\mathcal S_{K,N}(T)
=\int_0^T
\frac{\bigl[\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4\bigr]_+}{X_N}\,dt.
\tag{15}
\]

\[
\forall u_0\in C^\infty_{\mathrm{div}},\
\forall\nu>0,\quad
\exists K=K(u_0,\nu)<\infty:\quad
\forall T<\infty,\quad
\sup_N\mathcal S_{K,N}(T)<\infty.
\tag{17}
\]

\(\mathcal T_{\mathrm{sc}}\) sums complete
triads with three distinct exact radii.
Quantifiers are **datum-sensitive**
(\(K\) and the bound may depend on
\(u_0,\nu,T\)), **not** energy-only
universal in \((E_0,\nu)\).

## Shear rejection test

On the exact parallel-shear family of
[`L3-5-Exact-Shear-Obstruction-2026-10-03.md`](L3-5-Exact-Shear-Obstruction-2026-10-03.md),
every ordered interaction vanishes, so
\(\mathcal T_{\mathrm{sc}}=\mathcal T_{\mathrm{rep}}=\mathcal T=0\)
and \(S_{K,N}(T)=0\), while \(S^{(3)}\)
can be arbitrarily large at fixed
\(E_0,\nu,K,T\). Shears are a rejection
test the **signed** route already passes;
they kill energy-only \(L^3\) strengthenings,
not (17).

## Next gates (attack order)

See the dated packet for full
statements. Short board:

1. Freeze shear rejection (PROVED).
2. Keep seated complement \(\Rightarrow\) (16)
   (PROVED conditional).
3. Signed assembly of all-high scalene
   \(\mathcal T_{\mathrm{sc}}(h)\) — two-shell
   **spatial** instance survives (6 Oct 2026);
   all-high-in-time still OPEN.
4. Regenerative quartic / all-high jet —
   local \(t^6\) onset **written**;
   fixed-pair bounds (P1)–(P3) **claimed**
   (incl. outside inputs; frequency helps).
5. Assemble **all** scalene shapes without
   repeatedly charging the same shell
   energies — SCHEME B (B1) **OPEN**
   ([`SCHEME-B-SHELL-POT.md`](SCHEME-B-SHELL-POT.md));
   A / A′ dead.
6. Integrate to uniform-in-\(N\) budget
   (17) — OPEN (incl. \(\nu Y/4\) threshold);
   bridge (B2) conditional on (B1).
7. Continuation / Galerkin limit after
   uniform \(X\) — standard, not the blank.

## Non-goals

- No energy-only reverse /
  universal \(F(E_0,\nu,K,T)\) on \(S^{(3)}\).
- No RH.
- No Clay / “NS solved” claim.
- No claim-ledger or aerostat packaging
  on this branch.
- No speculative proof essay that
  merely renames the positive remainder.

## Lock

Priority: (17).
Energy-only \(S^{(3)}\) reverse: KILLED.
Two-shell spatial signed assembly:
survives (no occupancy).
All-high local jet on \(K=2\) datum:
\(t^6\) onset written.
Fixed-pair bounds (P1)–(P3): author claimed;
first audit target \(\int\lvert Q\rvert\).
SCHEME A (sum per shape): FAILED.
SCHEME A′ (Young after shape sum): FAILED (probe).
SCHEME B once-per-shell pot: **OPEN — plow**
([`SCHEME-B-SHELL-POT.md`](SCHEME-B-SHELL-POT.md)).
Target (B1): \(\lvert\mathcal T_{\mathrm{sc}}\rvert\le C_\star X\sqrt Y\)
(exact-sphere regrouping; each \(e_a\) once via \(X,Y\)).
“Shell” = exact \(\lvert k\rvert^2\) Fourier set, not a
physical shell or hole in the fluid.
(17) still OPEN.
(L3-5) fixed-datum: OPEN, deprioritized.
Lemma A / sign gate: unaltered (as on
parent desks).
NS not solved.
