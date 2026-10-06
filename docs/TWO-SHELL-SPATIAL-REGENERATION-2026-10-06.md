# Two-shell spatial assembly survives; regeneration is the obstruction

6 October 2026.
**Two-shell signed spatial test: survives (no occupancy).
Regenerated all-high scalene in time: still OPEN.
Criterion (17) not proved. NS not solved. Not Clay.**

Desk pointer:
[`TWO-SHELL-SPATIAL-REGENERATION.md`](TWO-SHELL-SPATIAL-REGENERATION.md).
Packet:
[`../packets/Two-Shell-Spatial-Regeneration-2026-10-06.md`](../packets/Two-Shell-Spatial-Regeneration-2026-10-06.md).
Plain-text twin:
[`TWO-SHELL-SPATIAL-REGENERATION-2026-10-06.txt`](TWO-SHELL-SPATIAL-REGENERATION-2026-10-06.txt).

Parents:
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md) (6)–(7), (14)–(17);
[`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md) (Need★ = this gate on two shells);
[`SIGNED-SCALENE-NEXT-ATTACK.md`](SIGNED-SCALENE-NEXT-ATTACK.md);
[`L3-5-Exact-Shear-Obstruction-2026-10-03.md`](L3-5-Exact-Shear-Obstruction-2026-10-03.md).

---

## RESULT

Choose the fixed cutoff from the **initial** high tail,
uniformly in the Galerkin cutoff. On two exact spheres
the complete signed assembly has no occupancy factor:
receiver compensation and flat-triangle cancellation
stay visible. That **spatial** two-shell test survives.

The obstruction is **regeneration**. An exact two-sphere
datum can have zero initial high tail at the chosen \(K\),
yet immediately generate a new squared radius. Full-field
scalene transfer can start at zero and have a nonzero
time derivative. That derivative is a statement about the
**full field**, not the all-high tail.

Two-shell spatial assembly is therefore not the remaining
blank toward (17). Controlling regenerated all-high
scalene transfer over time is.

---

## 1. Datum-sensitive cutoff (Gate 4 recipe)

\[
K
=\min\bigl\{
n\ge 1:
C_0\bigl\|P_{>n}u_0\bigr\|_{\dot H^{1/2}}
\le c\nu/2
\bigr\}.
\]

\(C_0\) is a named embedding / comparison constant
for the high-pass field (not an energy-only universal
bound on the later solution). \(c\) is the seated
viscosity threshold from the L3 / scalene budgets
(\(c=1/(8C_S)\) on the L3 desk). \(K\) may depend on
the fixed smooth datum \(u_0\) and on \(\nu\).

This makes the **initial** high tail small, uniformly
in the Galerkin cutoff \(N\). It does **not** by itself
make \(\|h_{K,N}(t)\|_{\dot H^{1/2}}\) small for
\(t>0\). Frozen-\(K\) control of later high modes is
regeneration, not the choice of \(K\).

Do not replace this by a \(K\) depending only on
\(E_0,\nu\). The shear obstruction already kills that
strengthening for unsigned \(L^3\) budgets; the same
quantifier mistake is forbidden here.

---

## 2. Two exact spheres — complete signed assembly

For two exact spheres \(a<b\), the complete signed
assembly is

\[
\mathcal T
=(b-a)\bigl(j_{b\leftarrow aa}-j_{a\leftarrow bb}\bigr).
\]

Relation to the Fourier-triangle desk. Vault (6) is
one radius-multiset \(\{a,a,b\}\):

\[
\tau_{b\leftarrow aa}
=-\operatorname{Re}\langle B(u_a,u_a),u_b\rangle,
\qquad
\mathcal T_{\{a,a,b\}}=(b-a)\tau_{b\leftarrow aa}.
\]

The formula above is the **pair** of completed
repeated-radius orientations on a two-sphere field,
\(\{a,a,b\}\) together with \(\{b,b,a\}\). Here
\(j_{b\leftarrow aa}\) is that \(\tau_{b\leftarrow aa}\)
current (and cyclically \(j_{a\leftarrow bb}\)).
Receiver compensation is the minus sign between the
two currents; the factor \(b-a\) is the exact
enstrophy-weight difference. Taking absolute values
before the two receiver choices are combined would
discard that cancellation.

**Spatial bound.** The two-shell spatial estimate
survives on this identity: receiver compensation and
flat-triangle cancellation
(\(\beta=4\alpha\Rightarrow k_\perp=0\)) remain
visible, with **no occupancy factor**.

This is Need★’s named class (two shells) at the
level of a signed sum, not an occupancy / CS envelope.
It is **not** yet a bound on all-high scalene
\(\mathcal T_{\mathrm{sc}}(h_{K,N})\) for three
distinct radii, and it is **not** (17).

Unrestricted \(\star\) stays **KILLED** by \(v_n\).
A two-shell write is not a bound on \(v_n\).

---

## 3. Regeneration obstruction (exact two-sphere datum)

An exact two-sphere datum with the cutoff rule above
can return \(K=2\): the initial high tail past squared
radius \(2\) vanishes, so

\[
P_{>2}u_0=0.
\]

The same datum immediately generates squared radius
\(5\) (integer lattice: modes of radii \(1\) and \(2\)
close a triangle onto radius \(5\)).

Its **full-field** scalene transfer satisfies

\[
\mathcal T_{\mathrm{sc}}(0)=0,
\qquad
\mathcal T_{\mathrm{sc}}'(0)=28.
\]

The first identity is geometric: at \(t=0\) there are
only two spheres, so no complete three-distinct-radius
scalene block. The second is the birth of scalene from
the nonlinear derivative — vault block ODE (14),
quartic \(\mathcal Q\) not confined to the displayed
two-sphere support.

That derivative concerns the **full field**, not the
all-high tail \(h_{K,N}\). Do not cash
\(\mathcal T_{\mathrm{sc}}'(0)=28\) as a bound on
\(\mathcal S_{K,N}(T)\), nor as \(\sup_N\) control.

Tag: **EXACT** for this named two-sphere example
(identities + stated initial derivative). Independent
recompute of the constant \(28\) is still appropriate.
Not a numerical ODE fit. Not a blowup example.

---

## 4. What this does and does not kill

| Object | Status |
|---|---|
| Occupancy / early \(\lvert\widehat B\rvert\) as necessary for two-shell signed assembly | **Not forced** — spatial test survives without occupancy |
| Need★ two-shell snapshot, signed, receiver compensation visible | **Survives** as a spatial identity / bound shape |
| Frozen \(K(u_0,\nu)\) from initial \(\dot H^{1/2}\) tail | **Written** (datum-sensitive; uniform in \(N\) at \(t=0\)) |
| Regeneration of new radii from a two-sphere datum with vanishing initial high tail | **Exact example** (\(K=2\to\) radius \(5\)) |
| Control of regenerated **all-high** scalene \(\mathcal T_{\mathrm{sc}}(h_{K,N})\) in time | **OPEN** — missing step toward (17) |
| Criterion (17) | **OPEN** |
| Fixed-datum (L3-5) | **OPEN**, not priority |
| Energy-only universal \(F(E_0,\nu,K,T)\) on \(S^{(3)}\) | **KILLED** (shears, 3 Oct 2026) |
| Global regularity / Clay / RH | **NOT CLAIMED** |

Shear filter still applies: if \(B(u,u)=0\), assembled
transfer vanishes. The two-sphere example is the
opposite obstruction — **nonzero** production of new
radii, not a false-positive unsigned budget.

---

## 5. Consequence for the next attack

Gate 2’s two-shell **spatial** instance is no longer
the thing to keep re-proving. Do not restart occupancy
counting (Attack 8) on two shells.

The remaining write is Gate 3 / all-high time:
control the regenerated scalene tail
\(\mathcal T_{\mathrm{sc}}(h_{K,N}(t))\) for the
**frozen** \(K(u_0,\nu)\) above, uniformly in \(N\),
without assuming the \(H^1\) bound (16) that (17) is
meant to feed. Quartic \(\mathcal Q\) in (14) is the
named forcing.

A replacement remainder that merely renames
\(\mathcal Q\) is not progress. A Duhamel factor
\(1/[\nu(a+b+c)]\) does not by itself bound the
integrated positive budget.

---

## STATUS

TWO-SHELL SPATIAL SIGNED ASSEMBLY: SURVIVES (NO OCCUPANCY).
REGENERATED ALL-HIGH SCALENE IN TIME: OPEN.
CRITERION (17): OPEN.
NS NOT SOLVED.
