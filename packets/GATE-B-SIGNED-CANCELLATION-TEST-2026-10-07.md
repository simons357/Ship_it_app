# Packet — Gate B signed cancellation test (7 October 2026)

Repo notes:

- [`docs/GATE-B-SIGNED-CANCELLATION-TEST.md`](../docs/GATE-B-SIGNED-CANCELLATION-TEST.md)
- [`docs/GATE-B-SOURCE-ASSEMBLY-AND-CONCENTRATION-TEST.md`](../docs/GATE-B-SOURCE-ASSEMBLY-AND-CONCENTRATION-TEST.md)

Checkers:

```bash
python3 scripts/ns_attacks/nonnegative_qx_assembly.py
python3 scripts/ns_attacks/signed_cancellation_test.py
python3 -m unittest tests.test_nonnegative_qx_assembly tests.test_signed_cancellation -v
```

Not (17). NS not solved.
