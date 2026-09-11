# What is kept from Φ-renorm?

**Audience:** Jonathan + agents who must not green false glue  
**Purpose:** Field-first card for the swirl \(\Phi\) identity — separate from cosmic essays and from Lemma★.  
**Honesty lock:** ★ **NOT** proved · NS **NOT** solved · kill lane **LIVE** · RH **NOT** proved.  
**Archive (interpretive essay):** [`archives/PHI-RENORM-UNIVERSAL-GEOMETRY-2026-05.md`](./archives/PHI-RENORM-UNIVERSAL-GEOMETRY-2026-05.md)  
**DA inventory:** `docs/domain-architect/01-EQUATION-INVENTORY.md` · **NS-Φ** · conflict **C-GLUE-4**

---

## 1. Start from the field

The objects live in **axisymmetric-with-swirl** Navier–Stokes: a velocity field that does not depend on the azimuthal angle \(\theta\), with a nonzero swirl component \(u_\theta\).

In cylindrical coordinates \((r,\theta,z)\),

\[
u = u_r\,\hat r + u_\theta\,\hat\theta + u_z\,\hat z.
\]

Two natural swirl scalars:

| Symbol | Definition | Kind |
| --- | --- | --- |
| \(\Gamma\) | \(r\,u_\theta\) | **Extensive** — angular-momentum density |
| \(\Phi\) | \(\Gamma/r^2 = u_\theta/r\) | **Intensive** — specific swirl / angular rate |

Near the axis \(r\to 0\), \(u_\theta\) itself must vanish for a smooth axisymmetric field. The intensive quantity \(\Phi\) is the one that can stay finite (\(\Phi|_{r=0}=\partial_r u_\theta|_{r=0}\) in the smooth class). Writing estimates in \(\Gamma\) makes a \(1/r^4\) factor look like a catastrophe; that is often the **wrong variable**, not a cosmic signal.

---

## 2. The identity (algebra, not cosmology)

Whenever \(r\neq 0\) and the fields are smooth enough,

\[
\boxed{
\frac{1}{r^4}\,\partial_z(\Gamma^2)
=
\partial_z(\Phi^2).
}
\]

**Proof sketch:** \(\Gamma = r^2\Phi\), so \(\Gamma^2 = r^4\Phi^2\). Since \(r\) does not depend on \(z\),

\[
\frac{1}{r^4}\partial_z(\Gamma^2)
=
\frac{1}{r^4}\partial_z(r^4\Phi^2)
=
\partial_z(\Phi^2).
\]

That is the whole jewel for the cancel: **algebraic identity**. No Hardy inequality is required to rewrite the term. No CMB map is required either.

**Honest scope:**

- This is about the **axisymmetric-with-swirl** class and the **axis coordinate singularity**.
- \(Q_1\)-augmented Track B notes may use this identity inside an augmented PDE; that is **not** classical unaugmented 3D NS solved.
- Classical global regularity for unaugmented axisymmetric-with-swirl remains **open** in Jonathan’s own Track B dashboards.

---

## 3. KEEP vs PARK

Aligned with Jonathan’s settled inventory (Phi-renorm KEEP; Bridge / Triple Lock / SFE→prize glue PARK).

### KEEP

| Item | Label |
| --- | --- |
| \(\Gamma\to\Phi\) swirl algebra / \(\Phi\)-renorm cancel identity | **Algebraic identity** |
| Intensive \(\Phi\) as the natural near-axis variable | Analytic packaging |
| Möbius–GCD / Q6 structure notes **without** “RH proved” | Separate arithmetic book |
| Unaugmented NS + SND | **Hypothesis** (open) |
| Domain Architect | Honesty / routing — refuses false glue |

### PARK / analogy (hold poetically; do not green as proof)

| Item | Label |
| --- | --- |
| CMB quadrupole / “Axis of Evil” as NS confirmation | Observational **analogy** |
| Saturn hexagon as proof of the same structure | Physical **analogy** |
| Kabbalah / Tree of Life / “cosmic star lattice” as math equivalence | Interpretive table — **not** PDE equivalence |
| “Planck confirms the NS proof” | **False glue** |
| Bridge*, ARCHON RH proved, Triple Lock, SFE→NS/RH, Millennium-from-SFE, unconditional Clay | **PARK** |
| Φ-renorm ⇒ Lemma★ proved ⇒ Clay B | **Refuse collapse** |

Language preference: *algebraic identity* / *hypothesis* / *interpretive analogy* — not “the universe is regular for the same reason” as established fact.

---

## 4. Next to Lemma★ — related, not the same box

| | **Φ-renorm** | **Lemma★ / \(\mathcal{R}_\star\)** |
| --- | --- | --- |
| Setting | Axisymmetric-with-swirl; cylindrical axis | Divergence-free fields on \(\mathbb{T}^3\) |
| Core move | Change variable so the axis term is non-singular | Bound nonlinear transfer using shape / spectral moments |
| Danger object | \(1/r^4\) centrifugal / swirl term in wrong variables | Centered cascade \((T_c)_+\) vs spread \(D_s\) |
| Status | Identity **KEEP**; classical regularity **open** | Packaging **open**; ★ **NOT** proved |

Fundamentals for Lemma★ (field → structures): PR **#65** · `LEMMA-STAR-WHAT-IS-IT.md`.

**Do not glue:** Φ-renorm identity ≠ Lemma★ closed ≠ Clay Statement B.

---

## 5. One-line summary

**Φ-renorm is the wrong-variable story near the swirl axis; Lemma★ is the shape story for nonlinear transfer on the torus.** Keep the algebra. Park the cosmic proof claims. NS is not solved.
