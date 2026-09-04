# Angular \(1/r^2\) viscosity vs \(I_{\mathrm{tube}}\)

`python3 scripts/track_b_angular.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B5 was the identity. This write is the domination.

---

## The knob on this write

Same packet class as B4c. Split the dissipation.
Full tube vorticity dissipation

\[
D_{\mathrm{tube}}=\int_{r<\delta}|\nabla\omega|^2\,r\,dr\,dz
\]

already budgets \(|I_{\mathrm{tube}}|\) (B4c). The extra
angular piece from \((\Delta u)_\theta=\Delta u_\theta-u_\theta/r^2\)
is

\[
A_{\mathrm{tube}}=\int_{r<\delta}\Bigl(\frac{u_\theta}{r}\Bigr)^2 r\,dr\,dz.
\]

The Feynman number is

\[
R_{\mathrm{ang}}=\frac{|I_{\mathrm{tube}}|}{A_{\mathrm{tube}}}.
\]

Tesla: turn \(j_*\) up. If \(R_{\mathrm{ang}}\) falls, the
\(1/r^2\) piece is the absorption. If it climbs, it is not.

No \(Q_1\). No \(\varepsilon\). No cancel to \(\Phi\).

---

## What the apparatus does

**B5b, fail** of “angular \(1/r^2\) viscosity dominates
\(I_{\mathrm{tube}}\) at \(\delta\sim 2^{-j_*}\).” On resolved
packets (\(j_*=2,3,4,5\)):

| \(j_*\) | \(R_{\mathrm{ang}}\) | \(R_D\) (B4c) |
|---|---|---|
| 2 | \(5.1\) | \(2.1\times 10^{-2}\) |
| 3 | \(10.0\) | \(1.0\times 10^{-2}\) |
| 4 | \(18.8\) | \(4.9\times 10^{-3}\) |
| 5 | \(28.7\) | \(2.0\times 10^{-3}\) |

\(R_{\mathrm{ang}}\) sits above 1 and climbs. The extra
piece, alone, does not beat the source. Full \(D_{\mathrm{tube}}\)
still does.

**B5c, pass.** Turn \(j_*\) up: \(R_{\mathrm{ang}}\) climbs,
\(R_D\) falls. The two ratios disagree. That is the knob.

**B5d, fail** of “the slow fat swirl that killed B4b also
kills angular domination.” Turn \(\varepsilon\) down:
\(R_{\mathrm{ang}}\) *falls*. The B4b killer is not the
B5b killer. Source slowed; \((u_\theta/r)^2\) did not care.

**B5e, fail** of “therefore cancel to \(\Phi=\Gamma/r^2\).”
B4c already budgets the packet with \(\nabla\omega\). Keep
\(\Gamma\). Keep \(1/r^4\). The extra angular term was not
the absorption.

**B5f, fail** of “the angular piece closes \(X\).”
A failed Poincaré is not continuation. The packet tube
budget is not an a priori either. See
[`TRACK-B-TUBE.md`](TRACK-B-TUBE.md).

**B5g, fail** of “this retunes the PDE.” The equation is
untouched.

---

## They work it

**Ladyzhenskaya.** Same weight, both sides. The
\(1/r^2\) piece is not the same weight as
\(1/r^4\partial_z(\Gamma^2)\) once the packet has a
frequency. You need the derivatives. I told you that is
when the tube is stiff. I still will not give you
\(\varepsilon\). I will not let you cancel to \(\Phi\)
to hide a ratio that climbed.

**Kato.** B4c stands. B5b as domination dies. Tosio is
satisfied: the check could fail. It failed.

**Leray.** You did not ask \(\int X\) for \(L^\infty\).
Good.

**Tesla.** Two knobs, two directions. Packet: \(j_*\) up,
angular loses. Killer: \(\varepsilon\) down, angular looks
better. Do not mix them.

**Feynman.** Missable number: \(R_{\mathrm{ang}}\) versus 1,
and whether it climbs. Both readable. Domination missed.

**Majda.** CONC may still use B4c. Do not replace it with
an angular Poincaré that the packets just killed.

**Beale.** Nobody votes this into global regularity.

**Einstein.** The object stayed named. Classical stress.
Axis weight kept.

**Operator.** B5b is scored. B5f is scored. Tube budget
is not an a priori. Next: packet geometry (B14d).
Do not cancel to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B5 | **pass** | \((\Delta u)_\theta\) identity (already) |
| B5b | **fail** | angular \(1/r^2\) dominates \(I_{\mathrm{tube}}\) on packets |
| B5c | **pass** | \(R_{\mathrm{ang}}\) climbs with \(j_*\); \(R_D\) falls |
| B5d | **fail** | B4b killer kills angular domination |
| B5e | **fail** | therefore cancel to \(\Phi\) |
| B5f | **fail** | angular piece closes \(X\) |
| B5g | **fail** | this retunes the PDE |
| domain B | **open** | packet geometry leftover is B14d |

Tesla’s line: turn \(j_*\) up. Angular loses. Full
dissipation does not.
