# Door B — H1 B5: \(L^\infty\) / BKM-style sketch

Dated 10 September 2026. **OPEN. Not a GR close.
Every unjustified arrow is MISSING. This is
not a continuation theorem.**

Plan: [`DOOR-B-H1-ESTIMATE-PLAN.md`](DOOR-B-H1-ESTIMATE-PLAN.md).
SoT: [`H1-SOT.md`](H1-SOT.md).
What would close H1: BKM on one cylinder,
independent of \(\lvert\omega\rvert\).

This file is **not** Track B lemma B5
(angular \(1/r^2\) on a swirl tube). That
identity already sits; domination already
failed. Do not recycle the id.

This file is **not** Step G of the
unaugmented vorticity plan (Gronwall on
global \(X\) from Ring + Hardy + spread).
Ring direction bound is REPAIR.

This file is **not** BKM-from-\(L^2\).

---

## Status locks

- Sketch only. **MISSING** marks stay until
  an estimate replaces them.
- Outside-\(\mathcal{E}\) identity: **blocked**.
  No candidate. Do not fill MISSING-7 by
  invention.
- Lattice closure enumerator still running
  on the ★ lane. Different integral.

---

## Object

One space-time cylinder \(Q\) in which
\(E_c=\{|\omega|\ge c\}\) looks like a tube
of radius \(\rho\), length \(L\), waiting
time \(\tau\). \(\xi=\omega/\lvert\omega\rvert\)
on \(E_c\).

Wanted:

\[
\int_0^\tau
\|(\xi\cdot\nabla u\cdot\xi)_+\|_{L^\infty(\mathrm{tube})}\,dt
\le
C(\rho,L).
\]

If this sits, BKM on that tube does not
see how large \(\lvert\omega\rvert\) is.
That is Lemma★ localized, not weaker.
Then (still not GR): cover, H2, H3,
\(R_\phi\), local Serrin.

---

## Sketch, with MISSING marks

**1. Direction control from \(J\).**
If

\[
J(Q)=\int_Q|\nabla\xi|^2|\omega|\,dx\,dt
\]

stays \(O(1)\), \(\xi\) cannot fold too
hard on the cylinder.

**MISSING-1.** \(J(Q)=O(1)\) independent of
amplitude, or paid by dissipation, from
unaugmented NSE. ABC: \(J\sim A\), not
\(O(1)\). Burgers: \(J=0\) by
\(\xi=\hat e_z\), not from the estimate.
Do not cash Lemma J on generic fields.

**2. Lipschitz \(\Rightarrow\) depletion.**
Constantin–Fefferman: stretching is small
when \(\xi\) is Lipschitz *and* poorly
aligned with extension.

**MISSING-2.** Lipschitz of \(\xi\) on
\(E_c\) does not force \(\cos\alpha_3\to 0\).
Already scored (B14b): direction slowly
varying is not direction aligned. The
ledger Ring Lemma
\(\|\nabla\xi\|_{L^\infty(E_c)}\le C\,2^{j^*}\)
is REPAIR: it assumes the bound it wants.
Do not quote it here as proved.

**MISSING-3.** The rate
\(\|(\xi\cdot\nabla u\cdot\xi)_+\|_\infty\)
independent of \(\lvert\omega\rvert\) on the
tube. ABC: the rate grows like \(A\).
That is a kill of this packaging on ABC,
not of NS.

**3. Thinness, from Biot–Savart.**
If \(\rho/L\to 0\), stretching is along one
direction and

\[
\rho^2\int|\omega|^2
\lesssim
E_{\mathrm{tube}}
\]

is the 1-D budget.

**Lemma P1 (sits).** On the low-pass class
\(\widehat{\omega}(k)=0\) for \(|k|>K\),
\(\int|\omega|^2\le K^2\int|u|^2\). If
\(K\le C/\rho\), the display above holds
with global energy. File: [`H1-P1.md`](H1-P1.md).

**MISSING-4.** NSE membership in that
class. Localized tube energy (cutoff)
now sits, with \(\nabla u\) kept:
[`H1-P1-LOC.md`](H1-P1-LOC.md). Dropping
\(\nabla u\) does not sit. A Gaussian pair
gave a number \(\simeq 1.3\)–\(1.5\); that
is a sample, not the lemma. High-pass at
the same \(\rho\) breaks the \(O(1)\) claim.
Straight-tube self-stretch was \(0\)
(no axial strain). Thinness without
stretching is not H1. Do not cash
“assume thin” (Lemma C). Do not cash
Lemma P1 or P1-loc as WRITE (6).

**4. Waiting, or no viscosity.**
Viscosity eats the tube on
\(\tau\sim\rho^2/\nu\). Shorter \(\tau\)
is inviscid: the same geometric bound as
\(\mathcal R_\star\).

**MISSING-5.** A derived waiting time from
NSE, or a viscosity-free close of the
rate in MISSING-3. Do not impose \(\tau\).
Burgers locks \(\rho^2/\nu=4\) to imposed
strain. That is not MISSING-5 filled.

**5. BKM on the tube.**
If MISSING-1–5 sit, the integral of the
positive stretch rate is \(\le C(\rho,L)\),
and the tube does not blow in finite time
by BKM.

**MISSING-6.** The implication is the
skeleton. The estimates are the hole.
Nothing in 1–4 currently sits, so 5 does
not fire.

**6. From one tube to \(L^\infty\).**
Cover \(E_c\) by cylinders. Control flux
(H2), exterior Biot–Savart (H3), cutoff
error \(R_\phi\). Then local Serrin, not
CKN.

**MISSING-7.** Outside-\(\mathcal{E}\)
identity. Stretching not paid by kinetic
energy. **No candidate.** Blocked. Do not
invent a formula and seat it here. Do not
add \(K(t)\) to the PDE to fake it.

**MISSING-8.** Cover of \(E_c\), H2 from
energy, H3 from energy, absorb \(R_\phi\).
Even if P4 sits, P5 of the plan is still
open. One tube is not GR.

**MISSING-9.** Uniform triadic bound on
\(\mathcal R_\star\). Not this sketch.
Enumerator still running on the ★ lane.
Do not paste a lattice peak in as
\(C(\rho,L)\).

---

## What would fill the sketch

Lemma P1 replaced the *number* in
MISSING-4. P1-loc wrote the cutoff.
Membership is still MISSING-4.
Replace MISSING-1–5 by estimates. Then
MISSING-6 is ordinary BKM on a cylinder.
MISSING-7–8 are still not GR. MISSING-9
is the other lane.

A numerical tube with large \(J\) or short
waiting kills this packaging, not NS.
ABC already did that for MISSING-3.

---

## What this is not

- Not geometric regularity of NS.
- Not Beale–Kato–Majda from \(\int\mathcal{E}<\infty\).
- Not Track B B5 angular domination.
- Not Step G Gronwall on global \(X\).
- Not Lemma★ proved, and not Lemma★
  killed. Localized packaging only.
- Not a close of Door B.

NS not solved.
