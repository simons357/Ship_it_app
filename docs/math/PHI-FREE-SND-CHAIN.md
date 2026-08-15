# Phi-free SND proof graph (experiment)

**Rule:** No edge from Phi-renorm / \(1/r^4\) cancel into this chain.

```text
LP shells X_j, X, J, ρ=J/X
        │
        ▼
   SND: inf J/X ≥ c_* > 0     (or T2’s ρ≤ρ₀ convention — freeze one)
        │
        ├──────────────► T2 flux |Φ_j| ≤ C 2^{-0.8j} X^{1/2} D^{1/2}
        │                      │
        │                      ▼
        │               T2 Gronwall: h' ≤ -α h + β_N
        │               (Gronwall equation for shell fractions)
        │
        ├──────────────► Ring Lemma (band-limited CF on E_c)
        │
        └──────────────► SND-C / Theorem H  [OPEN: remove X≤M circularity]
                              │
                              ▼
                    conditional regularity under SND
```

**Excluded from this graph**

- Phi-renorm / \(\partial_z(\Phi^2)\)
- Hardy \(r^{-4}\) (axisymmetric-only Track B′)
- Phi–Q6 correspondence
- Full-spectrum Bridge \(\lambda_{\min}(Q_N)>-1/2\) (withdrawn)

**Track B (parallel, not upstream of H)**

```text
axisymmetric swirl → (Phi cancel) OR (Hardy) → Q1 convergence / method note
```

## Status of “does removing cancel fix H?”

**No direct fix.** H still needs a non-circular \(M\).  
**Yes hygiene fix:** stops fake transfer of Gronwall-free success from axisymmetric Phi into spectral H.
