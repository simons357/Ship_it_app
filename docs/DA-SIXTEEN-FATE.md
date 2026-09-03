# Sixteen candidates, general fate, then smaller pieces

`python3 scripts/da_machine.py fate`

Not topological-versus-gauge as the only split. Each of the
16 is a **candidate** for a unification / everything slot.
DA gives it one category, one general fate, then the **same
five questions**, then the next smaller pieces.

The Cosmo export is still missing. This is the reconstructed
16. \(R\) is the 16th (output).

## The more general level (same five questions on each)

| Question | What it decides |
|---|---|
| **kind** | gauge / gravity-gauge / topological / harmonic / teleological |
| **nature** | must this appear in any four-force unifier? |
| **score** | does locking it raise \(R\)? |
| **produce** | is it an input that could write the couplings, or already a target? |
| **next** | the smallest remaining split |

Topological versus gauge is **kind**, one question, not the
whole machine.

## Fate of all 16

| # | Candidate | Kind | Nature | Score | Produce | Next piece |
|---|---|---|---|---|---|---|
| 1 | \(\alpha_{\mathrm{em}}\) | gauge | must-hit | decorative | already a target | coupling vs \(U(1)\) vs scale |
| 2 | \(\alpha_s\) | gauge | must-hit | decorative | already a target | coupling vs \(SU(3)\) vs scale |
| 3 | \(\sin^2\theta_W\) | gauge | must-hit | decorative | already a target | mixing vs the embedding |
| 4 | \(m_W/v\) | gauge | must-hit | decorative | already a target | \(m_W\) vs the vev |
| 5 | Planck | gravity-gauge | must-hit | **moves \(R\)** | leftover target | \(M_{\mathrm{Pl}}\), \(v\), ratio, log, width |
| 6 | vacuum | gravity-gauge (topological **fork**) | must-hit | **moves \(R\)** | leftover target | \(\rho_\Lambda\), fourth root, ratio, fork, width |
| 7 | QCD scale | gauge | must-hit | decorative | leftover target | \(\Lambda_{\mathrm{QCD}}\) vs \(\alpha_s\) |
| 8 | \(\theta_{\mathrm{QCD}}\) | **topological** | leftover | decorative | global, not a producer | angle, target 0, global vs local |
| 9 | \(A\) | harmonic | not a force | decorative | **fail** | mean amplitude |
| 10 | \(f\) | harmonic | not a force | decorative | **fail** | mean frequency |
| 11 | \(\varphi\) | harmonic | not a force | decorative | **fail** | scale knob |
| 12 | \(\delta\) | harmonic | not a force | **moves \(R\)** | **fail** | phase disorder |
| 13 | \(S_c\) | teleological | not a force | **moves \(R\)** | **fail** | coherence scalar |
| 14 | \(\kappa\) | teleological | not a force | decorative | **fail** | attractor |
| 15 | \(\lvert\nabla C\rvert\) | teleological | not a force | near-miss | **fail** | gradient |
| 16 | \(R\) | teleological | **fail** | circular | **fail** | the product; not a theory |

**Produce fails for everyone on this vector.** Gauge and
leftovers are already targets. Oscillators and teleology do
not write the couplings (affine \(F\) holdout already
failed). \(R\) is the output.

## Keep going down

The leftovers that still have pieces:

- **Vacuum / Planck:** \(x\), \(x_\star\), minus, square,
  **width**. Width **fails**: equal \(\sigma\) flattens them
  onto the gauge terms. Must-hit stays.
- **Vacuum kind:** gravity-scale here; topological reading
  is a different book. Fork stays **open**.
- **\(\theta_{\mathrm{QCD}}\):** global vs local **passes**
  (do not glue to \(\alpha_s\)). Score **fails**. Keep/drop
  for the strong-CP problem stays **open**.
- **\(\delta\), \(S_c\):** sit in \(\chi^2_{\mathrm{int}}\).
  They move \(R\). They do not move the four forces.
- **\(R\):** product **passes**. Circular-as-TOE **fails**.

Numbers and the full trees: `results/da_fingers.json`.
How a program can emit “possible” and a finite \(X\):
[`docs/DA-HOW-IT-KNEW.md`](DA-HOW-IT-KNEW.md). Flush of
combinations: [`docs/DA-FLUSH.md`](DA-FLUSH.md).
