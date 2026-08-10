# Harmonic Blueprint Experiment 01

## Cross-Event Spectral Selection in Black-Hole Ringdown

**Status: closed.** See the report: [`HB-RINGDOWN-EXPERIMENT-01-REPORT.md`](HB-RINGDOWN-EXPERIMENT-01-REPORT.md).

### Purpose

Test whether black-hole ringdown spectra contain reproducible, dimensionless organization beyond a reference null, without assuming in advance that Harmonic Blueprint (HB), prime-indexed structure, Fibonacci structure, or golden-ratio structure is correct.

This experiment deliberately avoids exoplanet and cosmology data.

### Scientific question

After a black-hole merger, the remnant relaxes through quasinormal modes (QNMs). Do dimensionless relationships among ringdown modes cluster around predefined spectral node families more strongly than expected from randomized controls? Does any such structure recur across independent events?

### Hypotheses

- **H0:** Observed dimensionless mode relationships are consistent with the null; no reproducible excess proximity to any predefined family.
- **H1:** Relationships exhibit statistically reproducible clustering around one or more predefined families beyond the null.
- **Secondary HB / prime:** A predefined prime-indexed family outperforms control families out of sample. The prime family must be defined before examining the final test set.

### Immediate workflow

1. Obtain / refresh a ringdown-mode table → `data/qnm_events.csv`
2. Freeze `nodes.json` (do not edit after viewing TEST results)
3. Run exploratory TRAIN analysis if needed, then freeze choices
4. Evaluate once on TEST:

```bash
python hb_ringdown_test.py \
  --csv data/qnm_events.csv \
  --nodes nodes.json \
  --mc 50000 \
  --split test
```

5. Inspect score, empirical p, BH q-value, and leave-one-event-out stability

### Observables

Preferred analysis uses dimensionless quantities:

| Name | Definition |
|------|------------|
| `m_omega` | `M * omega_R` |
| `frequency_ratio` | `omega_R(i) / omega_R(j)` (default) |
| `quality_factor` | `Q = omega_R / (2 omega_I)` |
| `detuning` | `D_ijk = |omega_i + omega_j - omega_k| / omega_k` |

### Statistic

For observation `x` and node family `R`:

```text
d(x,R) = min_r |log(x/r)|
s(x,R) = exp[-d(x,R)^2 / (2 sigma^2)]
S(R)   = (1/N) sum_i s(x_i,R)
```

Higher `S` means closer proximity to that family. `sigma` is frozen in `nodes.json`.

### Null model

Built-in Monte Carlo null: preserve the number of relationships and redraw log-uniform values on the observed global range, then recompute `S(R)`.

This is a starting point. For publication, replace or supplement with a GR-informed null from Kerr QNM predictions, mass/spin uncertainty, detector noise, and mode-selection effects.

### Multiple comparisons

The script reports empirical Monte Carlo p-values and Benjamini–Hochberg FDR q-values. A family is not supported merely because raw `p < 0.05`.

### Train / test

| Split | Events |
|-------|--------|
| TRAIN | GW150914, GW170104, GW190521 |
| TEST  | GW190412, GW190814, GW200129 |

Choices (observable, sigma, nodes, cleaning) must be frozen before the held-out TEST run.

### Falsification

Prime/HB fails this experiment if it does not beat the null, loses significance after FDR, only works after retuning on TEST, disappears under a GR-informed null, is driven by one event, or is matched/beaten by control families.

A null result is acceptable and should be reported.

### Strong-result criteria

1. Family predefined  
2. Significantly exceeds null  
3. Survives FDR  
4. Reproduces on held-out events  
5. Not driven by one merger  
6. Survives uncertainty propagation  
7. Adds predictive information beyond Kerr/GR expectations (hardest)

### Data provenance

`data/qnm_events.csv` mixes:

- Capano et al. (2021) measured GW190521 (220)/(330) frequencies and damping times
- Kerr-fit modes from published remnant `(M, chi)` via Berti-style fitting formulas for additional events

Regenerate Kerr-fit rows with:

```bash
python scripts/build_qnm_table.py
```

### Interpretation

A positive result would **not** prove that “black holes are harmonic” in the trivial QNM sense. It would support the narrower claim that ringdown contains reproducible dimensionless spectral organization not captured by the chosen null. Only if HB/prime uniquely predicts that organization should the result be read as evidence relevant to HB.
