#!/usr/bin/env python3
"""Run the B42 T2-ray coefficient report. NS is not solved."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.t2_starvation_coefficient import main

if __name__ == "__main__":
    main()
