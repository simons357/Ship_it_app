"""Fail-closed Gate D signed-transfer diagnostic. Not a rigorous FFT error certificate."""
import math
import numpy as np
from validated_vorticity import evaluate_checked

class CancellationFailure(ArithmeticError): pass

def preflight(n,N,limit_bytes=2*1024**3):
    if not isinstance(n,int) or not isinstance(N,int) or n<4 or N<1 or N>=n/3:
        raise ValueError("Require integers n>=4 and 1<=N<n/3")
    required=576*n**3
    if required>limit_bytes:
        raise MemoryError(f"fail_memory_preflight: estimated {required} > ceiling {limit_bytes}")
    return required

def cancellation_report(full,repeated,n,shell_count,*,fft_per_shell=2,base_ffts=3,
                        fft_safety_factor=1.,lost_bit_warning=20):
    """Heuristic epsilon*FFT_count*log2(n**3)*magnitude; NOT a proven forward bound."""
    full,repeated=float(full),float(repeated)
    if not all(map(math.isfinite,(full,repeated))): raise ValueError("Nonfinite transfer")
    val=full-repeated
    magnitude=abs(full)+abs(repeated)
    eps=np.finfo(np.float64).eps
    nfft=base_ffts+fft_per_shell*shell_count
    error=float(eps*fft_safety_factor*nfft*math.log2(n**3)*magnitude+eps*abs(val))
    denom=max(abs(val),eps*magnitude,np.finfo(float).tiny)
    lost_bits=max(0.,math.log2(magnitude/denom)) if magnitude else 0.
    status="fail_cancellation" if abs(val)<=error else ("warn_cancellation" if lost_bits>lost_bit_warning else "pass_heuristic")
    return {"T_sc":val,"T_full":full,"T_rep":repeated,"lost_bits":lost_bits,
            "absolute_error_estimate":error,"status":status,"n_fft_estimate":nfft,
            "rigorous_error_bound":False,"sign_certified":False}

def evaluate_fail_closed(vh,L,K,N,*,limit_bytes=2*1024**3,fail_on_cancellation=True):
    n=vh.shape[1]
    estimated=preflight(n,N,limit_bytes)
    value,details=evaluate_checked(vh,L,K,N,max_work_bytes=limit_bytes)
    report=cancellation_report(details["full"],details["repeated"],n,details["shell_count"])
    report.update(memory_preflight_bytes=estimated,hermitian_residual=details["hermitian_residual"],
                  divergence_residual=details["divergence_residual"])
    if report["status"]=="fail_cancellation" and fail_on_cancellation:
        raise CancellationFailure(f"fail_cancellation: {report}")
    return report
