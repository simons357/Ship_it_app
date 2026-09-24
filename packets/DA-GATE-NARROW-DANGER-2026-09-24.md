# DA-GATE — narrow danger parameter

**24 September 2026.** Attack on the proposed middle regime.
This locks a correction. It does **not** make the middle region payable.

**Classical unaugmented 3-D Navier–Stokes stays open.**
DA-NS-2 stays **OPEN**. Scalene (17) stays **OPEN**.
The unsigned assembly (4) stays **OPEN**. That is the real gate.
L1 / BOTH SIGNS stays **OPEN**.

Do **not** alter the RMS/SBP gate, the static-frontier lock, the
Fourier-triangle audit, or the Lemma★ shape lock (separate PRs).
Do **not** promote a triad Taylor remainder \(F_{\rm het}\sim r\)
to an assembled inequality. That step is **FORBIDDEN**.

Machine: [`scripts/da_gate_narrow_danger.py`](../scripts/da_gate_narrow_danger.py).
Lock: [`data/da_gate_narrow_danger_2026-09-24.json`](../data/da_gate_narrow_danger_2026-09-24.json).

---

## Status

| Item | Bucket |
|---|---|
| Centered triad (1) | **EXACT** |
| One-gap factor (2), \(\Delta=\Lambda r\) | **EXACT** |
| Promote \(F_{\rm het}\sim r\) to assembled \(T_c\) | **FORBIDDEN** |
| Unsigned assembly (3) as a close | **FORBIDDEN** — occupancy/counting can return |
| Missing inequality (4) | **OPEN** — the real gate |
| Algebra (5)\(\to\)(6)\(\to\)(7) under the stated narrow-packet substitutions | **EXACT** (algebra only) |
| Local estimate (5) as a proved bound | **NOT RE-PROVED** here |
| Universal threshold \(r\sim\kappa^{-1}\) | **KILLED** |
| Danger parameter \(\mathfrak D\) / \(\eta_{\rm DA}\) | **LOCKED** (definition) |
| \(\mathfrak D\ll 1\) \(\Rightarrow\) middle region payable | **NOT PROVED** |
| L1 fork | **LOCKED** |
| DA-NS-2 | **OPEN** |

---

## What cannot be promoted

A triad Taylor expansion giving \(F_{\rm het}\sim r\) is not an
assembled estimate for \(T_c^+\). Replacing a signed sum by a sum
of absolute values is the same forbidden step as before.

Start from the exact centered triad expression

\[
\mathcal T_{abc}
=
(c-b)I_p+(a-c)I_q+(b-a)I_r.
\tag{1}
\]

Let the occupied squared radii lie in \(|\lambda-\Lambda|\le\Delta\)
with \(\Delta\sim\Lambda r\). Then every radial difference obeys
\(|a-b|,|b-c|,|c-a|\le 2\Delta\), so triad by triad

\[
\boxed{
|\mathcal T_{abc}|
\le
2\Delta
\bigl(|I_p|+|I_q|+|I_r|\bigr).
}
\tag{2}
\]

The one-gap factor is exact:

\[
\boxed{\Delta=\Lambda r.}
\]

That part survives.

After assembly one may write

\[
T_c^+
\le
2\Lambda r
\sum_{\triangle}
\bigl(|I_p|+|I_q|+|I_r|\bigr).
\tag{3}
\]

Unsigned assembly can reintroduce occupancy and counting losses.
So the proposed middle-regime close reduces to the missing inequality

\[
\boxed{
\sum_{\triangle}|I_{\triangle}|
\stackrel{?}{\lesssim}
\alpha_c\chi_\kappa\,\mathcal A(u)
}
\tag{4}
\]

with a scale-correct amplitude \(\mathcal A\) and **no hidden
shell-count factor**. This packet does not invent \(\mathcal A\),
\(\alpha_c\), or \(\chi_\kappa\). Equation (4) is the real gate.
It is **OPEN**.

---

## Comparable-band algebra, not a close

The existing centered local estimate packages the same problem
better than (3):

\[
T_{c,\mathrm{loc}}^+
\lesssim
\alpha_{c,\kappa}\chi_\kappa\,\kappa^{3/2}X D_s^{1/2}.
\tag{5}
\]

This packet does **not** re-prove (5). It uses it as the stated
local envelope and follows the substitutions.

Under the narrow-packet identifications
\(D_s/Y=\kappa^2 r^2\) and \(Y^{1/2}=\kappa X^{1/2}\),

\[
D_s^{1/2}=Y^{1/2}\kappa r,
\]

hence

\[
\boxed{
T_{c,\mathrm{loc}}^+
\lesssim
\alpha_c\chi\,r\,\kappa^{7/2}X^{3/2}.
}
\tag{6}
\]

The one factor of \(r\) is there. Compare to
\(\nu D_s=\nu\kappa^4 r^2 X\):

\[
\boxed{
\frac{T_{c,\mathrm{loc}}^+}{\nu D_s}
\lesssim
\frac{\alpha_c\chi}{\nu}
\frac{X^{1/2}}{\kappa^{1/2}r}.
}
\tag{7}
\]

This is the corrected balance. It is **not** \(1/(\kappa r)\).
The previous schematic dropped the amplitude/concentration factor.
The universal split \(\kappa r\sim 1\) is **KILLED**.

---

## Danger parameter

\[
\boxed{
\mathfrak D
:=
\frac{\alpha_c\chi\,X^{1/2}}{\nu\kappa^{1/2}r}.
}
\tag{8}
\]

Local narrow interaction is automatically viscously payable only
when \(\mathfrak D\ll 1\). That implication is **not** proved as a
close. There is no universal micro-narrow boundary \(r\sim\kappa^{-1}\).
The correct threshold is state-dependent:

\[
\boxed{
r_{\mathrm{crit}}
\sim
\frac{\alpha_c\chi X^{1/2}}{\nu\kappa^{1/2}}.
}
\tag{9}
\]

For a narrow packet near \(\kappa\),
\(\|u\|_{\dot H^{1/2}}^2\approx\kappa E\) and \(X\approx\kappa^2 E\),
so \(X^{1/2}\approx\kappa^{1/2}\|u\|_{\dot H^{1/2}}\) and

\[
\boxed{
\mathfrak D
\approx
\frac{\alpha_c\chi}{\nu r}\|u\|_{\dot H^{1/2}}.
}
\tag{10}
\]

Scale \(\kappa\) disappears. Three independent routes now point at
the critical \(\dot H^{1/2}\) scale: the bump attack, dimensional
CRSPR, and this narrow centered-transfer estimate. That is a
coincidence of scales, not a close.

---

## Regime map

Do not partition by \(r\gtrsim\kappa^{-1/2}\) and
\(\kappa^{-1}<r<\kappa^{-1/2}\). Introduce

\[
\boxed{
\eta(t)
:=
\frac{\alpha_c(t)\chi(t)\|u(t)\|_{\dot H^{1/2}}}{\nu r(t)}.
}
\tag{11}
\]

Approximately: \(\eta\ll 1\) local centered transfer payable;
\(\eta\gtrsim 1\) dangerous narrow state. As \(r\to 0\),
\(\eta\to\infty\) unless \(\alpha_c\to 0\), \(\chi\to 0\), or the
critical amplitude falls. Narrowness by itself makes the first-order
heterochiral competition worse, as \(T_c=O(r)\) against
\(D_s=O(r^2)\) already said.

The ultra-narrow missing mechanism cannot be another power of
variance unless the symmetry-reduced \(L_1\) coefficient vanishes:

\[
\boxed{L_1\neq 0\Rightarrow\text{need dynamic loss of }\alpha_c,\chi,\text{ or persistence};}
\]
\[
\boxed{L_1=0\Rightarrow\text{gain another radial power and recompute}.}
\]

That is why the symmetry-reduced L1 gate stays live.

---

## Solver diagnostic

Use the exact (8) form, not the critical-norm rewrite:

\[
\boxed{
\eta_{\mathrm{DA}}
=
\frac{\alpha_{c,\kappa}\chi_\kappa\sqrt{X}}{\nu\sqrt{\kappa}\,r},
\qquad
\mathcal Q
=
\frac{T_{c,\mathrm{loc}}^+}{\nu D_s}.
}
\]

If the local envelope is sharp, dangerous episodes should relate
\(\eta_{\mathrm{DA}}\) to \(\mathcal Q\). If \(\eta_{\mathrm{DA}}\)
becomes enormous while \(\mathcal Q\) stays tiny, the envelope is
too loose and the missing depletion sits in signed assembly.

This packet names the diagnostic. It does not evaluate it. \(N=64\)
and \(N=96\) data are not in this tree.

---

## Attack verdict

The middle region is **not** proved payable. The threshold
\(r\sim\kappa^{-1}\) is **KILLED**. The object to feed the
Five-Finger map is

\[
\boxed{
\mathfrak D
=
\frac{\alpha_c\chi\sqrt{X}}{\nu\sqrt{\kappa}\,r}.
}
\]

Occupation, if it is ever proved, would only control how long
\(\mathfrak D\gtrsim 1\) can persist. That persistence estimate is
**not** proved here.

**NS not solved.**
