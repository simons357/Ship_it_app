#!/usr/bin/env python3
"""Read-only verifier for the R2 G3 TSV pair.

Does not write M.tsv, b_exact.tsv, the G3 JSON, or PROVENANCE.json.
"""

from __future__ import annotations

from r2_lock_tsvs import main, verify

__all__ = ["verify", "main"]


if __name__ == "__main__":
    main()
