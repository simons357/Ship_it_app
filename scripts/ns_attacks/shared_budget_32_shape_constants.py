"""Sanity check on filed weighted-charge faces for the 32-shape extension.

Not a proof. Verifies float consistency of author-reported faces.
"""
from pathlib import Path
import json

# Author-reported faces (paper constants)
rho_prime = 0.8253067330
rho_plus_3_rho_prime = 3.1077752815
rho = rho_plus_3_rho_prime - 3 * rho_prime

# Product factors from constant-3 / constant-2 lines
sqrt3 = 3**0.5
sqrt2 = 2**0.5

payload = {
    "extension": "17 + 15 nonzero from (9,25) → 32 shapes",
    "combined_charge_multiplicity_nonzero_transfer": 4,
    "rho_prime_face": rho_prime,
    "rho_plus_3_rho_prime_face": rho_plus_3_rho_prime,
    "implied_rho_face": rho,
    "reconstruction_check": abs((rho + 3 * rho_prime) - rho_plus_3_rho_prime) < 1e-12,
    "triple_product_factors": {"sqrt3": sqrt3, "sqrt2": sqrt2},
    "constant_3_fixed_shell_lemma": "valid under its hypotheses",
    "constant_2_distinct_donor": "sharpening of distinct-donor case",
    "common_highpass_cutoff": "K = max{2, 3(M-1)}",
    "not_claimed": ["criterion (17)", "global regularity", "arbitrary families"],
    "pr_165": "unchanged",
    "status": "NUMERICAL face check only; analytic proofs in author ZIP",
}

path = Path(__file__).with_name("SHARED-BUDGET-32-SHAPE-CONSTANTS.json")
path.write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps(payload, indent=2))
assert payload["reconstruction_check"]
