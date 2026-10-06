# Two-triangle normals: is \(1/\sqrt2\) robust?

6 October 2026.
**Snapshot test only. Not Need★ proved. Not (17). NS not solved.**

Parent desks:
[`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md) (\(\rho_2=1/\sqrt2\) stamped on the smallest sharing pair),
[`DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md`](DATUM-CUTOFF-TWO-SHELL-SIGNED-ASSEMBLY.md),
[`SIGNED-SCALENE-NEXT-ATTACK.md`](SIGNED-SCALENE-NEXT-ATTACK.md).

Checks:
`scripts/ns_attacks/two_triangle_normal_angle_checks.py`
→ `TWO-TRIANGLE-NORMAL-ANGLE-CHECKS.json`.

---

## Question

The signed calculation works on a genuine HH→L sharing pair, and the
\(1/\sqrt2\) improvement can be identified geometrically. Does that
factor survive when the two triangle normals \(e_2,e_2'\) become
nearly parallel?

This is still a **two-triangle snapshot** test. It does not integrate
a time budget and does not prove Need★.

---

## Geometric identity (EXACT)

For two equal-amplitude channel contributions with unit normals at
oriented angle \(\theta\), phases aligned so the channel scalars add,

\[
\rho(\theta)
=\frac{\lvert e_2+e_2'\rvert}{2}
=\sqrt{\frac{1+\cos\theta}{2}}
=\lvert\cos(\theta/2)\rvert.
\]

| Geometry | \(\cos\theta\) | \(\rho\) |
|---|---:|---:|
| Orthogonal | \(0\) | \(1/\sqrt2\) |
| \(60^\circ\) | \(1/2\) | \(\sqrt3/2\) |
| Near parallel | \(\to 1\) | \(\to 1\) |
| Parallel | \(1\) | \(1\) |
| Near antiparallel | \(\to -1\) | \(\to 0\) |

So \(1/\sqrt2\) is exactly the **orthogonal equal-weight** case. It is
not a universal two-triangle constant.

- Near-**parallel** oriented normals: the vector-sum improvement is
  **lost** (\(\rho\to 1\)).
- Near-**antiparallel** oriented normals: for the **fixed phases**
  used in the equal-weight identity, signed assembly can cancel
  **harder** than \(1/\sqrt2\) (\(\rho\to 0\)).
- When **partner phases are optimized**, \(\cos\theta\) is
  replaced by \(\lvert\cos\theta\rvert\) in the attainable
  maximum: either nearly parallel orientation can approach
  full compatibility. Near-antiparallel cancellation is a
  **fixed-phase** statement. That does **not** restore
  \(1/\sqrt2\) as a universal constant.

---

## Lattice HH→L scan (NUMERICAL census of exact geometry)

Equal-input pairs \(\lvert p\rvert^2=\lvert q\rvert^2=\alpha\),
\(\lvert k\rvert^2=\beta\), \(0<\beta<4\alpha\), grouped by shared
output \(k\). For each two distinct legs, record the undirected plane
angle and the oriented-normal \(\rho\).

Scan \(\alpha\le 50\), \(\beta\le 40\): thousands of pairs; many
exact orthogonals with \(\rho=1/\sqrt2\); hundreds with undirected
planes within \(\sim 18^\circ\) (\(\lvert\cos\rvert\ge 0.95\)).

Concrete near-parallel-plane witness:

\[
\alpha=50,\ \beta=2,\ k=(-1,-1,0),
\]

legs \((-1,0,-7)+(0,-1,7)\) and \((-1,0,7)+(0,-1,-7)\):
undirected planes \(\sim 11.5^\circ\) apart
(\(\lvert\cos\rvert\approx 0.980\)), while the **oriented** normals
are nearly antiparallel (\(\cos\approx -0.980\)), giving
\(\rho_{\mathrm{oriented}}\approx 0.101\). Flipping one normal’s
orientation swaps this into the near-parallel \(\rho\to 1\) case.
Orientation is part of the channel bookkeeping; it is not free candy
in a class bound.

---

## Outcome

| Claim | Status |
|---|---|
| Signed HH→L sharing-pair calculation can realize \(1/\sqrt2\) | **Yes**, when \(e_2\perp e_2'\) at equal weight |
| \(1/\sqrt2\) robust under nearly parallel normals | **No** — \(\rho\to 1\) if oriented normals align |
| Near-antiparallel normals worse for the signed sum | **No** — they cancel more |
| Stamp \(\rho_2=1/\sqrt2\) as universal two-triangle depletion | **Unsupported** |
| Signed route / Im / receiver compensation killed | **No** |
| Need★ or (17) | **Still OPEN** |

**Where the improvement came from:** orthogonal geometry of the two
\(e_2\) directions under equal channel weights, after the signed
channels are assembled — not from occupancy counting, and not from a
geometry-independent constant.

**Next:** keep signed assembly; do not advertise \(1/\sqrt2\) as
robust. The time blank remains regenerated all-high three-radius
blocks toward (17).

## Lock

\(\rho=1/\sqrt2\) = orthogonal special case.
Near-parallel oriented normals remove that factor.
Signed assembly not killed.
(17) OPEN. NS not solved.
