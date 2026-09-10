# H1 / P1-loc — cutoff Biot–Savart / energy

10 September 2026. **This estimate sits. It is not H1.
WRITE (6) is not proved. NS is not solved.**

Same leftover class. Not a new name.
Global low-pass cousin: [`H1-P1.md`](H1-P1.md).
Path-cost (1-D): [`H1-PC.md`](H1-PC.md).
Plan: [`DOOR-B-H1-ESTIMATE-PLAN.md`](DOOR-B-H1-ESTIMATE-PLAN.md).
Do not merge with Lemma★, \(H_N\), or Lemma C.

Probe: `python3 scripts/h1_p1_loc.py`

MISSING-4 asked for the cutoff. This is that
commutator. It is not membership, and it is
not thinness without dissipation.

---

## What sits

Let \(u\) be divergence-free. Let \(\eta\in C_c^1\)
equal \(1\) on the ball \(B_\rho\), vanish outside
\(B_{2\rho}\), and satisfy \(|\nabla\eta|\le \pi/(2\rho)\)
(cosine taper). Write \(\omega=\nabla\times u\).

**Lemma P1-loc (cutoff).**

\[
\int_{B_\rho}|\omega|^2
\le
4\int_{B_{2\rho}}|\nabla u|^2
+C\rho^{-2}\int_{B_{2\rho}}|u|^2,
\]

with \(C=3\pi^2/2\) for that taper. On \(\mathbb{T}^3\)
the balls are periodic and \(2\rho<\pi\).

Proof. Product rule: \(\nabla\times(\eta u)=\eta\omega+\nabla\eta\times u\).
Hence \(\eta\omega=\nabla\times(\eta u)-\nabla\eta\times u\), and

\[
\int\eta^2|\omega|^2
\le
2\int|\nabla\times(\eta u)|^2
+2\int|\nabla\eta\times u|^2.
\]

On the torus, \(\int|\nabla(\eta u)|^2=\int|\nabla\times(\eta u)|^2+\int|\mathrm{div}(\eta u)|^2\).
Also \(\mathrm{div}(\eta u)=\nabla\eta\cdot u\) and
\(|\nabla(\eta u)|^2\le 2\eta^2|\nabla u|^2+2|u|^2|\nabla\eta|^2\).
Therefore

\[
\int|\nabla\times(\eta u)|^2
\le
2\int\eta^2|\nabla u|^2
+2\int|u|^2|\nabla\eta|^2.
\]

Put the two displays together and use
\(|\nabla\eta|\le\pi/(2\rho)\) on the annulus,
\(\eta\equiv 1\) on \(B_\rho\).

No NSE. No frequency class. The \(\nabla u\) term stays.

---

## What does not sit

**Drop \(\nabla u\).** The P1 thinness
\(\rho^2\int_{B_\rho}|\omega|^2\lesssim\int_{B_{2\rho}}|u|^2\)
is not this lemma. High-pass at scale \(1/\rho\)
breaks that \(O(1)\) claim. The cutoff does not
remove the class.

**NSE membership.** Leftover fields are not known
to be low-pass on the tube. Unchanged.

**H1 / WRITE (6).** A localized energy identity
is not \(A_{\mathrm{bad}}\) versus
\(\nu/8\iint|\nabla\omega|^2\phi+C r^{-2}\iint|\omega|^2\).
The \(\nabla u\) term is the dissipation we would
need to *pay* stretching. It is not a remainder
we already own from \(\int E<\infty\) at scale
\(\rho\to 0\).

Do not cash P1-loc as P1 thinness. Do not cash
it as PC. Do not invent a version that drops
\(\nabla u\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| H1p1loc_cutoff_sits | **pass** | \(\int_{B_\rho}|\omega|^2\le 4\int_{B_{2\rho}}|\nabla u|^2+C\rho^{-2}\int_{B_{2\rho}}|u|^2\) |
| H1p1loc_drop_gradu | **fail** | high-pass: \(\rho^2\int_{B_\rho}|\omega|^2\big/\int_{B_{2\rho}}|u|^2\) is not \(O(1)\) |
| H1p1loc_is_h1 | **fail** | a cutoff identity is not WRITE (6) |
| H1p1loc_nse_class | **open** | NSE puts Bad on a class that drops \(\nabla u\) |

P1-lowpass still sits globally on \(\lvert k\rvert\le K\).
Membership is still the hole in MISSING-4.

NS not solved.
