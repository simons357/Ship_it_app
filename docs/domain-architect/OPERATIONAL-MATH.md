# Operational mathematics for Domain Architect v1.0

The concept paper states the architecture. This note states the mathematics
the software actually evaluates. Nothing here is a universal field equation.

## 1. Functional signature

A component `X` is recorded as

```
σ(X) = (r, τ, D, C, U, S, K)
```

- `r` is a role from an open list (selection, interaction, transport,
  feedback, dissipation, forcing, constraint, state transition, measurement,
  plus `state` and `parameter` when those are the honest labels).
- `τ` is a mathematical type (scalar, field, operator, …).
- `D → C` is the interface `X : D → C`.
- `U` is an SI-base dimension 7-tuple, or unknown.
- `S` is a set of named invariants (linearity, passivity, gauge, …).
- `K` is a set of named constraints.

An assignment is never a bare label. It is

```
role + confidence + rationale
```

Ambiguous assignments are retained as competing hypotheses.

## 2. Decomposition of a second-order linear plant

For a monic (or scaled) equation

```
a ẍ + b ẋ + c x = f
```

structural position — not the letter names — yields

| Term | Role | Operator | Parameter |
|---|---|---|---|
| `a ẍ` | state transition (inertia) | second time derivative | `a` |
| `b ẋ` | dissipation | first time derivative | `b` |
| `c x` | interaction (restoring) | multiplication by state | `c` |
| `f` | forcing | identity on the input | — |
| `x` | state | — | — |

This is a hypothesis about function, not a claim that every second-order
equation is a mass–spring–damper.

## 3. Cross-domain translation (mechanical ↔ electrical)

The lumped linear correspondences

```
m ẍ + c ẋ + k x = f
L q̈ + R q̇ + (1/C) q = v
```

share the same second-order linear time-invariant structure. The software
records the explicit map

```
T:  x ↦ q,   ẋ ↦ i,   m ↦ L,   c ↦ R,   k ↦ 1/C,   f ↦ v
```

and then classifies the pair:

- **Preserved:** order, linearity, time-invariance, quadratic energy,
  passivity when all coefficients are positive.
- **Broken:** SI dimensions and physical carriers. In SI, `[M] ≠ [L]` and
  `[force] ≠ [voltage]`, so the pair is not directly compatible.
- **Class:** `TRANSFORMABLE`.
- **Kind:** mathematical correspondence, not physical equivalence.

A candidate substitution must apply `T` before it enters a synthesized
architecture.

## 4. Compatibility

For mechanisms `M_A : X_A → Y_A` and `M_B : X_B → Y_B` the software checks,
in order:

1. interface (`X` and `Y` types),
2. dimensions `[M_A] ? [M_B]`,
3. named invariants (symmetry, conservation, positivity, causality).

The verdict is exactly one of

```
DIRECTLY COMPATIBLE | TRANSFORMABLE | INCOMPATIBLE
```

`TRANSFORMABLE` requires an explicit `T`. Superficial analogy without `T`
is refused.

## 5. Missing-mechanism recovery

Paper §16 asks whether DA can recover a deleted mechanism from a known
model. The first benchmark is the damped oscillator.

True dynamics:

```
ẍ + 2 ζ ω ẋ + ω² x = 0
```

Incomplete model (dissipation removed):

```
ẍ + ω² x = 0
```

The **equation residual** of the incomplete operator on observed trajectories
is

```
R(t) = ẍ_obs(t) + ω² x_obs(t)
```

If the truth contains linear damping, then `R(t) = −2 ζ ω ẋ_obs(t)`. The
software therefore:

1. correlates `R` with `{x, ẋ, 1}` to choose a role class,
2. if `corr(R, ẋ) ≈ −1`, assigns **missing dissipation**,
3. restricts the search to linear damping `γ ẋ`,
4. estimates

```
γ̂ = − ⟨R, ẋ⟩ / ⟨ẋ, ẋ⟩ ,     ζ̂ = γ̂ / (2 ω)
```

A constant residual uncorrelated with `x` and `ẋ` is instead classified as
**missing forcing**, with `Â = mean(R)`.

This is ordinary least squares on a role-restricted operator class. It is
not symbolic regression over arbitrary expressions.

## 6. State, controller, constraints

Continuous evolution is the standard initial-value problem

```
ẋ = F(x, u, t)
```

integrated with fixed-step RK4. A target `x★` produces the error
`e = x★ − x`. The default synthesized controller is saturated PD,

```
u = clip( K_p e − K_d ẋ , u_min, u_max )
```

which is the paper’s loop

```
STATE → MEASURE → COMPARE → CONTROL → TRANSITION → NEW STATE
```

with the constraint set `C` applied before the action is sent to `F`.

## 7. Validation gates

Every candidate architecture is stamped with the highest gate it has passed:

```
MATHEMATICAL → COMPUTATIONAL → EMPIRICAL
```

- Mathematical: types, dimensions, interfaces, named invariants, explicit `T`.
- Computational: simulation, residual recovery, identifiability, surrogate
  optimization under frozen constraints.
- Empirical: reserved for held-out measurements. The software does not
  self-award this gate.

A mathematically coherent synthesis is reported as a **hypothesis**.

## 8. What is deliberately not assumed

Prime indexing, a privileged harmonic basis, a canonical field equation, and
physical equivalence of analog systems are not part of the live mathematics.
They remain in the historical archive.
