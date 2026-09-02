# Harmonic Blueprint Experiment 01 — Closed Report

**Shelved.** Off the live desk (`docs/SHELF.md`). Archive only. Do not retune `nodes.json`.

**Status:** closed  
**Date:** 2026-08-10  
**Branch / PR:** `cursor/hb-ringdown-experiment-d70f`  
**Verdict:** primary null hypothesis **H0 not rejected** on the held-out TEST set.

---

## 1. Question

Do dimensionless relationships among black-hole ringdown modes cluster around predefined spectral node families more strongly than expected from a reference null — and does any such structure reproduce across independent events?

This experiment does **not** assume that Harmonic Blueprint (HB), primes, Fibonacci ratios, or the golden ratio are physically correct. Those enter only as predefined comparison families.

---

## 2. Hypotheses

| ID | Statement | Outcome |
|----|-----------|---------|
| **H0** | Observed dimensionless mode relationships are consistent with the null; no reproducible excess proximity to any predefined family. | **Not rejected** |
| **H1** | Relationships show reproducible clustering beyond the null. | Not supported |
| **Secondary (prime / HB)** | Predefined prime-indexed family outperforms controls out of sample. | **Not supported** |

---

## 3. Frozen analysis choices

Locked in `nodes.json` before held-out TEST evaluation. **Not retuned after viewing TEST.**

| Choice | Frozen value |
|--------|----------------|
| Observable | `frequency_ratio` = ω_R(i)/ω_R(j) (and reciprocal) |
| Tolerance | `sigma = 0.05` |
| Statistic | S(R) = mean_i exp[−d(x_i,R)² / (2σ²)], d = min log-distance to nodes |
| Null | log-uniform Monte Carlo on the observed value range (`mc = 50000`, seed 42) |
| Multiple comparisons | Benjamini–Hochberg FDR on family p-values |
| Stability | leave-one-event-out |
| Decision threshold | family supported only if q ≤ 0.05 and not driven by one event |

### Node families (predefined)

1. `integer_rational` — control  
2. `fibonacci_ratios` — control  
3. `golden_ratio` — control  
4. `prime_neighbor_ratios` — secondary / prime hypothesis  
5. `random_nodes` — random control (drawn once, then frozen for the run)

### Event splits

| Split | Events |
|-------|--------|
| TRAIN | GW150914, GW170104, GW190521 |
| TEST | GW190412, GW190814, GW200129 |

---

## 4. Data

Source table: `data/qnm_events.csv`.

- **GW190521:** Capano et al. (2021) measured (220) and (330) frequencies / damping times.  
- **Other events:** Kerr-fit modes from published remnant (M, χ) via Berti-style formulas (pipeline exercise catalog, not a full measured multimode posterior set).

Dimensionless ratios remove overall mass scale so events can be compared.

---

## 5. Results

Machine-readable outputs: `results/train_mc50000.json`, `results/test_mc50000.json`.  
Numeric tables: `results/SUMMARY.md`.

### TRAIN (exploratory / confirmation of freeze)

14 ratios across 3 events. After BH-FDR at q ≤ 0.05: **no family supported.**

Best raw scores: prime (0.907, q ≈ 0.13), integer/rational (0.774, q ≈ 0.057). Neither clears the corrected threshold with the protocol rule.

### TEST (held-out, decisive under this protocol)

18 ratios across 3 events. **No retuning of nodes or σ.**

| Family | Score | p | q_BH | Driven by one event? |
|--------|------:|--:|-----:|:--------------------:|
| prime_neighbor_ratios | 0.807 | 0.171 | 0.381 | no |
| integer_rational | 0.696 | 0.015 | 0.076 | no |
| random_nodes | 0.648 | 0.355 | 0.444 | no |
| fibonacci_ratios | 0.479 | 0.229 | 0.381 | no |
| golden_ratio | 0.212 | 0.999 | 0.999 | no |

**Held-out decision:** no family meets q ≤ 0.05. Primary **H0 stands**. The prime family does not uniquely beat controls out of sample.

### ALL (not used for the claim)

Pooling TRAIN+TEST can produce FDR hits under the weak log-uniform null. That is exploratory only and does **not** override the held-out null.

---

## 6. Falsification check (against Experiment 01 rules)

| Rule | Assessment |
|------|------------|
| Must outperform randomized null on TEST after FDR | Fail — no family with q ≤ 0.05 |
| Must not require retuning on TEST | Pass — freeze held |
| Must not be driven by one event | LOO stable where checked; moot given FDR fail |
| Control families must not do as well or better | On TEST, integer/rational has smaller raw p than prime but still q > 0.05; prime does not uniquely win |
| Preferred GR-informed null | Not yet implemented — baseline uses log-uniform null only |

Under these rules, **prime-indexed / HB does not pass Experiment 01.**

---

## 7. Interpretation

This does **not** prove or disprove that black holes “are harmonic” in the ordinary QNM sense. It answers a narrower question:

> Under the frozen choices and the built-in log-uniform null, is there reproducible excess clustering of dimensionless ringdown ratios around predefined node families on held-out events?

**Answer: no evidence for that claim in this baseline.**

A positive HB-relevant claim would additionally require a GR-informed null and predictive content beyond Kerr expectations (strong-result criterion 7). That bar was not reached; the held-out FDR test already failed.

---

## 8. What this closes

Experiment 01 is **closed** as a protocol run:

1. Pipeline exists and is reproducible.  
2. Nodes and σ were frozen.  
3. TRAIN and held-out TEST were run at `mc = 50000`.  
4. Result recorded: **H0 not rejected; null result accepted.**  
5. No post-hoc node edits after TEST.

---

## 9. Optional later work (out of scope for this close-out)

Only if a new experiment is opened later:

- Replace Kerr-fit rows with measured multimode posteriors.  
- Implement a GR-informed null (Kerr predictions + mass/spin uncertainty + noise + mode selection).  
- Propagate measurement uncertainties into S(R).  
- Pre-register a new freeze before any new TEST.

Until then, no further action is required on Experiment 01.

---

## 10. Reproduce

```bash
pip install -r requirements.txt
python hb_ringdown_test.py --csv data/qnm_events.csv --nodes nodes.json --mc 50000 --split train
python hb_ringdown_test.py --csv data/qnm_events.csv --nodes nodes.json --mc 50000 --split test
python -m unittest tests/test_hb_ringdown.py
```
