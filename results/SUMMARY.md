# HB Ringdown Experiment 01 — baseline run summary

**Closed.** Full write-up: [`docs/HB-RINGDOWN-EXPERIMENT-01-REPORT.md`](../docs/HB-RINGDOWN-EXPERIMENT-01-REPORT.md)

Frozen settings: `nodes.json` (`observable=frequency_ratio`, `sigma=0.05`), seed 42, `mc=50000`.

## TRAIN (`--split train`)

Events: GW150914, GW170104, GW190521 (14 ratios).

| family | score | p | q_BH | driven_by_one |
|--------|------:|--:|-----:|:-------------:|
| prime_neighbor_ratios | 0.907 | 0.087 | 0.129 | no |
| integer_rational | 0.774 | 0.020 | 0.057 | no |
| random_nodes | 0.726 | 0.103 | 0.129 | no |
| fibonacci_ratios | 0.627 | 0.023 | 0.057 | no |
| golden_ratio | 0.275 | 0.993 | 0.993 | no |

**Verdict:** primary H0 not rejected after BH-FDR at q≤0.05.

## TEST (`--split test`) — held-out, no retuning

Events: GW190412, GW190814, GW200129 (18 ratios).

| family | score | p | q_BH | driven_by_one |
|--------|------:|--:|-----:|:-------------:|
| prime_neighbor_ratios | 0.807 | 0.171 | 0.381 | no |
| integer_rational | 0.696 | 0.015 | 0.076 | no |
| random_nodes | 0.648 | 0.355 | 0.444 | no |
| fibonacci_ratios | 0.479 | 0.229 | 0.381 | no |
| golden_ratio | 0.212 | 0.999 | 0.999 | no |

**Verdict:** held-out TEST also fails to reject H0 after FDR. Prime family does not uniquely outperform controls.

## ALL (exploratory only)

Pooling can produce FDR-significant hits under the weak log-uniform null (prime + integer/rational). That is **not** a successful HB result under the protocol: TRAIN and TEST separately do not survive correction, and most TEST modes are Kerr-fit ratios rather than agnostic measurements.

## Caveats

1. Built-in null is log-uniform, not GR-informed.
2. Several events use Kerr-fit frequencies from remnant `(M, χ)`; only GW190521 includes Capano et al. measured multimode frequencies.
3. Criterion 7 (information beyond Kerr/GR) is not addressed by this baseline.

Machine-readable outputs: `train_mc50000.json`, `test_mc50000.json`, `all_mc50000.json`.
