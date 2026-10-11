# Excalibur deliverable A — inventory, imports, and frozen core hash

**Date:** 11 October 2026.
**Plan:** [`EXCALIBUR-ARCHITECTURE-V1.md`](EXCALIBUR-ARCHITECTURE-V1.md).
**Status:** Inventory only. Not a mathematical approval. Not a production launch.

No source file under `scripts/ns_attacks` was edited. No archive was deleted. No cloud machine was started. The frozen \(c=200\), \(s\ge 4\) trajectory was not run. Research Gate D remains OPEN / BLOCKED.

## 1. Where the code lives

`scripts/ns_attacks` is absent from `origin/main` and from `origin/cursor/foundation-setup-c3ed`.

The locked stepper path is present on one remote branch:

`origin/cursor/shared-budget-32-shape-c3ed`

Commit inspected: `b07148f4d5b55414db31338bfdff1f7bce41c957` (`File the Gaussian packet preregistration as proposed.`).

This inventory was written on `cursor/excalibur-inventory-c3ed`, branched from that commit. Selecting any other branch as the canonical tree would drop the Navier–Stokes attack scripts.

## 2. Frozen core hash

Canonical evolution file:

`scripts/ns_attacks/gate_d_signed_diagnostic/gaussian_gate_d.py`

| Item | Value |
| --- | --- |
| Bytes | 4219 |
| SHA-256 | `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56` |
| Runtime imports | `argparse`, `json`, `hashlib`, `pathlib.Path`, `numpy` |
| Diagnostic import | None. This file does not implement \(T_{\mathrm{sc}}\) or \(D\). |

Function-body SHA-256, taken from the source text of each function:

| Function | SHA-256 |
| --- | --- |
| `gaussian_curl` | `85e89a9072309f1a03936e5b5270f3075e2c4dc5dfdc7b743247bcc746fa847a` |
| `grid` | `545d8b9744ac0e6a2d639331b98f9b1d98d180de824ff634a205ba486dc5e111` |
| `project` | `ab25835aa290508a7677f0ada0b12c10054f3309b2c9136adb870eda08330e15` |
| `nonlinear` | `a79bddaf65b42a674020d09880e3f987a59d5fab59b4ba82b9a9c29b50f66a0f` |
| `step` | `fa53c148769ded9086f403a98bd8179daaca1895178748a7fff5184f3c979ef8` |
| `diagnostics` | `44976ce7cdd56afcde4601003d8e82af76eff679bd2cbdcd560dd46a7607d3ae` |
| `run` | `2aff53e03cf622ee81500e7a2b9da890e7c5079ad90e06ab3b568e06845601eb` |

`grid`, `project`, `nonlinear`, `step`, and `gaussian_curl` are the frozen evolution core. `diagnostics` and `run` are downstream of that core even inside the same file.

## 3. Copies of the Gaussian stepper

Six other `gaussian_gate_d.py` files keep the five evolution bodies and change `diagnostics` and `run`.

| Path | File SHA-256 | Evolution bodies |
| --- | --- | --- |
| `gate_d_adaptive_evaluator/gaussian_gate_d.py` | `3bc81c79b9dfb9a5f8eebc773dfc5764d84bae6352fba8581ee87156dc7cbeb9` | match |
| `gate_d_fft_shell_candidate/gaussian_gate_d.py` | `3bc81c79b9dfb9a5f8eebc773dfc5764d84bae6352fba8581ee87156dc7cbeb9` | match |
| `gate_d_guarded_logger/gaussian_gate_d.py` | `3bc81c79b9dfb9a5f8eebc773dfc5764d84bae6352fba8581ee87156dc7cbeb9` | match |
| `gate_d_metadata_repair/gaussian_gate_d.py` | `3bc81c79b9dfb9a5f8eebc773dfc5764d84bae6352fba8581ee87156dc7cbeb9` | match |
| `gate_d_vorticity_evaluator/gaussian_gate_d.py` | `3bc81c79b9dfb9a5f8eebc773dfc5764d84bae6352fba8581ee87156dc7cbeb9` | match |
| `gate_d_gaussian_scaffold/gaussian_gate_d.py` | `a591e95657eadbe9f1027939ec08f696e5fbba3de67d2cdf1f15060123c15534` | match |

Paths are relative to `scripts/ns_attacks/`.

Both sidecars also match those five bodies:

| Path | File SHA-256 |
| --- | --- |
| `gate_d_guarded_logger/gaussian_gate_d_with_sidecar.py` | `bb92ae5b5ac52a5ca893633b4355c01342dfecd850ed55badf01aec00b58f80e` |
| `gate_d_metadata_repair/gaussian_gate_d_with_sidecar.py` | `adc8c6a491501989fdb2d964be3bfd5fc85ffe0912a6e03ab3404427e3294846` |

The two sidecar file hashes differ. The difference is the run header, not the evolution step. The metadata-repair header no longer claims an accepted \(T_{\mathrm{sc}}\).

## 4. Runtime import map

The guarded candidate entry point is `gate_d_guarded_logger/gaussian_gate_d_with_sidecar.py`. Its local imports are:

- `signed_bridge` → `signed_phi`
- `logger_bridge` → `integrated_gate` → `fail_closed` → `validated_vorticity` → `vorticity_signed`
- `integrated_gate` also imports `exact_sparse_transfer` and `exact_discrete_y`
- `mask_policy`

`adaptive_certified` is not imported by the sidecar. It remains an off-path evaluator. The metadata-repair tree repeats this same import shape.

Two older evolution programs are in the same directory and are not this core:

- `gate_d_adversarial_run.py` imports `verify_signed_gate` and steps a sparse six-box packet. It is not the Gaussian RK4 file.
- `gate_d_full_trajectory.py` imports that adversarial runner.
- `gated_initial.py` has its own `nonlinear` and is a static initial sweep.

Those three stay historical. They are not selected as the canonical engine.

## 5. Archives in the git tree

Identical bytes are listed once, with every path that holds them.

| SHA-256 | Bytes | Paths |
| --- | --- | --- |
| `e05285f2fdfadcf5493bf898eff482edfaceb12dd4d4f154db7a7ca995d3d3eb` | 14553 | `docs/sources/Gate-D-Signed-Packet-Execution.zip`; `handoff/gate-d-signed-packet-2026-10-08/Gate-D-Signed-Packet-Execution.zip`; `packets/Gate-D-Signed-Packet-Execution.zip`; `scripts/ns_attacks/Gate-D-Signed-Packet-Execution.zip` |
| `2d70a1de513e24421982e9eb9f8df5ac2ec50e789a71fda658e510a1087d57cc` | 19678 | `handoff/Gate-D-Review-and-Separate-Gaussian-Extension-2026-10-09.VAULT.zip` |
| `ca01fa9ab93950174ae3ca25a932c8778910e1fc71d075deda559df914f9e020` | 20715 | `packets/gate_d/da_review/gate_d_guarded_logger_fix_2026-10-09.zip`; `scripts/ns_attacks/gate_d_guarded_logger/gate_d_guarded_logger_fix_2026-10-09.zip` |
| `8d07445a462f880bf96126010231c559ef27e968de5c2a13f52c9140c76db8d6` | 20843 | `packets/gate_d/da_review/gate_d_metadata_repair_candidate_2026-10-09.zip`; `scripts/ns_attacks/gate_d_metadata_repair/gate_d_metadata_repair_candidate_2026-10-09.zip` |

The guarded-logger and metadata-repair hashes match the hashes already recorded in the 9 October review.

## 6. Uploads outside the git tree

These files sit in the local upload folder. They are not a second canonical source. Hashes that already appear above are the same bytes.

| SHA-256 | Name | Same as a tree archive |
| --- | --- | --- |
| `ca01fa9ab93950174ae3ca25a932c8778910e1fc71d075deda559df914f9e020` | `gate_d_guarded_logger_fix_2026-10-09_13d7.zip` and `_1831.zip` | yes |
| `8d07445a462f880bf96126010231c559ef27e968de5c2a13f52c9140c76db8d6` | `gate_d_metadata_repair_candidate_2026-10-09_6f0a.zip` | yes |
| `e05285f2fdfadcf5493bf898eff482edfaceb12dd4d4f154db7a7ca995d3d3eb` | three `Gate-D-Signed-Packet-Execution_*.zip` copies | yes |
| `01c5f84b775a96d21c6d2cc40f1d6f53500a071fbff658f13cf87fa90356dfe0` | `gate_d_vorticity_evaluator_2026-10-09_1abc.zip` | no tree copy under that hash |
| `df4b29dde808ae181d3a1ab8bf5e1533eb6429e77bc4c3021de2e70e1481696c` | `gate_d_adaptive_evaluator_2026-10-09_c2c7.zip` | no |
| `555cc89b7bc48425be8942c9071b755ab5d376a7b6283be3c1ec24f9459d65ce` | `gate_d_fft_shell_candidate_2026-10-09_e387.zip` | no |
| `8ac42d9e08f1570613630e688e0294b6df8c8f3e02b5498fdbb21817867d33d4` | `gate_d_gaussian_scaffold_2026-10-09_1e36.zip` | no |
| `bfe47670a892531547dd713173c594ac0048ec2d45e7f3ff54e19afd39ed2f85` | `gate_d_phi_reference_2026-10-09_6964.zip` | no |
| `e0fca0efb942a5be1cdc60159faae4fdfb456754896aca5705369cbe46a81ba9` | `gate_d_signed_reference_2026-10-09_5f4b.zip` | no |
| `30f4d46b0ca2ac914a5a02b3b431d50f02e09c0f4df3ce3ddecf2b8a23de238e` | `Datum-Cutoff-Two-Shell-Signed-Assembly_c95c.zip` | no |

## 7. What this inventory does not decide

The canonical file is the locked Gaussian RK4 stepper above. That choice freezes a hash. It does not certify Lemma 19, the viscosity rational \(1/200\), an enclosure for \(Y\), the \(L\) versus \(2L\) cutoff, or agreement with the \(\mathbb R^3\) Gaussian.

The September 20 markdown pages named by the preregistration are still not in this checkout.

Deliverables B through E are untouched. The proposed `ns_core/` tree was not created.

## STATUS

CANONICAL FILE: `scripts/ns_attacks/gate_d_signed_diagnostic/gaussian_gate_d.py`.
FILE SHA-256: `0da006cdcbfdc437c660159ff1c019eaf3eb9fb19f1baa35178e05142f82dc56`.
EVOLUTION BODIES: UNCHANGED ON EVERY GAUSSIAN COPY CHECKED.
BRANCH HOLDING THAT FILE: `cursor/shared-budget-32-shape-c3ed` ONLY.
`main`: PATH ABSENT.
PRODUCTION \(c=200\), \(s\ge 4\): NOT LAUNCHED.
GATE D: OPEN / BLOCKED.
NO TURNOVER, REGENERATION, SHARED BUDGET, OR REGULARITY.
NS NOT SOLVED.
