# Math panel closeout — what is done / what is blocked

**Branch:** `cursor/tao-snd-h-panel-a0eb`  
**Date:** 2026-08-15  
**Clay / Statement (B):** not claimed

---

## Done (finished on available sources)

| Item | Where |
| --- | --- |
| Tao-standard SND / H / NS Q&A | `TAO-MATH-PANEL-SND-H.md` |
| ARCHON 10-expert review (Zenodo papers) | `ARCHON-NS-FINAL-REVIEW-PANEL.md` |
| Dominant shell ≠ Q6; what \(c_*\) is | `SPECTRAL-OBJECT-MAP.md` + chat answers |
| Zenodo spectral mirror (14 DOIs) | `docs/papers/zenodo-spectral/` |
| Positive-GCD A/B/C + Route C kills | `07_positive_gcd_paper1_abc.tex`, `route_c_gap_a_verify.py` |
| Phi-cancel optional rewire (T2 for Gronwall; Phi ↛ H) | `PHI-OPTIONAL-REWIRE.md`, `PHI-FREE-SND-CHAIN.md` |
| Prior floor / Bridge\* / keep-cut audit carried forward | `docs/BRIDGE-*.md`, `docs/FLOOR-ATTACK.md`, … |

### Reproduce checks

```bash
python3 -m unittest tests.test_bridge_star_h_n -v
python3 scripts/bridge_floor_verify.py 200
python3 scripts/h_n_bridge_star_check.py 400
```

---

## Locked one-liners

1. **\(c_*\)** = SND floor on dominant-shell fraction \(J/X\) (data-dependent in fluids papers); **not** automatically \(6/\pi^2\).
2. **Dominant shell** \(j^*\) ≠ **Q6** (inverse-GCD damper).
3. **Theorem H** ≠ unconditional SND; it is SND-C under \(X\le M\) (circular for Clay).
4. **Phi \(1/r^4\) cancel** is an identity; did not break H; cut Phi→H glue; use **T2** for spectral Gronwall.
5. **Do not** submit Zenodo as unconditional Statement (B) on the papers we have.

---

## Blocked (cannot finish here)

| Item | Why |
| --- | --- |
| Re-run ARCHON on June 10 merge | `NS_FINAL_MERGED_UNCONDITIONAL.tex` / `NS_PROOF_CHAIN.html` not in repo/Zenodo |
| Prove unconditional SND / non-circular \(M\) | Open math; not available from mirrored sources |

**If those files appear in `docs/papers/`:** re-open ARCHON focusing only on “does Theorem H derive \(M\) from \(\|u_0\|_{H^1}\) alone?”

---

## Recommended stop

This branch is a **finished audit + mirror + rewire package**. Further Clay work needs either (a) the missing merge file, or (b) a new proof that produces \(M\) without assuming it — not more packaging.
