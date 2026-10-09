"""Sidecar diagnostic logger. Never modifies Gaussian solver stepper.
Do not use for production. Exact sparse reference only, fail closed otherwise.
"""
from integrated_gate import assess
def diagnostic_record(vh, *, L,K,N,c,s):
    result=assess(vh,L,K,N,nu=1/c)
    return dict(s=float(s), diagnostic_status=result["status"],
                T_sc=result.get("T_sc"),D_sign=result["D_sign"],
                D_exact=result.get("D_normalized_exact"),
                sign_certified_for_stored_coefficients=result["sign_certified_for_stored_coefficients"],
                trajectory_certified=False,crossing_certified=False)
