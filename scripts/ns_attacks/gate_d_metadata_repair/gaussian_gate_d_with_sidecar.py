#!/usr/bin/env python3
"""Preregisterable replacement scaffold for Gate D Gaussian packet.
Not the recovered historical driver. Does not implement T_sc or D.
Classical unforced NSE in nondimensional form on a periodic box.
"""
import argparse, json, hashlib
from signed_bridge import signed_diagnostics
from logger_bridge import diagnostic_record
from mask_policy import make_galerkin_mask, check_highpass
from pathlib import Path
import numpy as np


def gaussian_curl(x,y,z):
    r2=x*x+y*y+z*z
    f=np.exp(-r2/2)
    return np.stack((f*(-y*(x+y*z)+z+x*z*z-x),
                     f*(-z*x*y-1+x*(x+y*z)),
                     f*(z-x*x*z-x+x*y*y)),axis=0)

def grid(n,L):
    xx=(np.arange(n)-n//2)*L/n
    x,y,z=np.meshgrid(xx,xx,xx,indexing='ij')
    k=2*np.pi*np.fft.fftfreq(n,d=L/n)
    kx,ky,kz=np.meshgrid(k,k,k,indexing='ij')
    k2=kx*kx+ky*ky+kz*kz
    mask=(np.abs(np.fft.fftfreq(n)*n)<n/3)
    dealias=mask[:,None,None]&mask[None,:,None]&mask[None,None,:]
    return (x,y,z),(kx,ky,kz,k2,dealias)

def project(vh,kx,ky,kz,k2):
    kk=np.stack((kx,ky,kz))
    dot=np.sum(kk*vh,axis=0)
    safe=np.where(k2==0,1,k2)
    out=vh-kk*dot/safe
    out[:,0,0,0]=0
    return out

def nonlinear(vh,ks):
    kx,ky,kz,k2,mask=ks
    vh=vh*mask
    v=np.fft.ifftn(vh,axes=(1,2,3)).real
    conv=np.zeros_like(v)
    for j,kj in enumerate((kx,ky,kz)):
        dv=np.fft.ifftn(1j*kj[None,...]*vh,axes=(1,2,3)).real
        conv+=v[j]*dv
    return -project(np.fft.fftn(conv,axes=(1,2,3))*mask,kx,ky,kz,k2)

def step(vh,ks,h,c):
    kx,ky,kz,k2,mask=ks
    eh=np.exp(-0.5*h*k2/c)
    ef=eh*eh
    n1=nonlinear(vh,ks)
    n2=nonlinear(eh*(vh+h*n1/2),ks)
    n3=nonlinear(eh*vh+h*n2/2,ks)
    n4=nonlinear(ef*vh+h*eh*n3,ks)
    return project((ef*vh+h*(ef*n1+2*eh*n2+2*eh*n3+n4)/6)*mask,kx,ky,kz,k2)

def diagnostics(vh,ks,L,c,high_fraction, signed_K=None, signed_N=None):
    if signed_K is not None and signed_N is None: raise ValueError("Signed diagnostic requires explicit evolution cutoff N")
    if signed_K is not None: check_highpass(signed_K,signed_N)
    kx,ky,kz,k2,mask=ks
    vol=L**3
    v=np.fft.ifftn(vh,axes=(1,2,3)).real
    norm=np.mean(np.sum(v*v,axis=0))*vol
    x=np.mean(np.sum(k2[None,...]*abs(vh)**2,axis=0))*vol/(vh.shape[1]**6)
    y=np.mean(np.sum(k2[None,...]**2*abs(vh)**2,axis=0))*vol/(vh.shape[1]**6)
    # Above mean has an extra n^-3; use Parseval sum below instead.
    x=vol*np.sum(k2[None,...]*abs(vh)**2).real/vh.shape[1]**6
    y=vol*np.sum(k2[None,...]**2*abs(vh)**2).real/vh.shape[1]**6
    nv=nonlinear(vh,ks)
    production=vol*np.sum(np.conj(vh)*k2[None,...]*nv).real/vh.shape[1]**6
    highcut=high_fraction*np.max(np.sqrt(k2[mask]))
    high=vol*np.sum((np.sum(abs(vh)**2,axis=0))*(np.sqrt(k2)>=highcut)).real/(2*vh.shape[1]**6)
    div=np.max(np.abs(kx*vh[0]+ky*vh[1]+kz*vh[2]))/vh.shape[1]**3
    tsc = None if signed_K is None else signed_diagnostics(vh,ks,L,K_index=signed_K,N_index=signed_N)
    d = None if tsc is None else float(tsc-y/(4*c))
    return dict(energy=norm/2,X=x,Y=y,production=production,G=float(production-y/c),high_shell_energy=high,max_fourier_divergence=float(div),T_sc=tsc,D=d,d_over_X=None if d is None or x==0 else d/x)

def run(args):
    xyz,ks=grid(args.n,args.L)
    if args.signed_N is not None:
        ks=(*ks[:4],make_galerkin_mask(args.n,args.L,args.signed_N))
    if args.signed_K is not None: check_highpass(args.signed_K,args.signed_N)
    if getattr(args,'safe_sidecar',False) and (args.signed_K is None or args.signed_N is None):
        raise ValueError('Safe sidecar requires signed K and N')
    v0=gaussian_curl(*xyz)
    vh=np.fft.fftn(v0,axes=(1,2,3))
    vh=project(vh,*ks[:4])*ks[4]
    steps=int(np.ceil(args.s_end/args.ds))
    h=args.s_end/steps
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    source_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    meta=dict(kind='NEW REPLACEMENT SCAFFOLD; NOT ORIGINAL DRIVER',c=args.c,n=args.n,L=args.L,ds=h,s_end=args.s_end,periodization='sample Gaussian on periodic cube, then project and 2/3 filter',cutoff='spherical integer radius N intersect componentwise 2/3 mask' if args.signed_N is not None else 'componentwise 2/3 mask',physical_kmax=None if args.signed_N is None else 2*np.pi*args.signed_N/args.L,physical_kmax_doubled_box_same_N=None if args.signed_N is None else np.pi*args.signed_N/args.L,T_sc_code_available=args.signed_K is not None,D_code_available=args.signed_K is not None,G_implemented=True,accepted_T_sc_verified=False,accepted_D_verified=False,crossing_certified=False,safe_sidecar_enabled=bool(getattr(args,'safe_sidecar',False)),source_sha256=source_hash)
    with out.open('w') as f:
        f.write(json.dumps(dict(metadata=meta))+'\n')
        for i in range(steps+1):
            if i%args.log_every==0 or i==steps:
                d=diagnostics(vh,ks,args.L,args.c,args.high_fraction, None if getattr(args,'safe_sidecar',False) else args.signed_K, None if getattr(args,'safe_sidecar',False) else args.signed_N)
                if getattr(args,'safe_sidecar',False):
                    d['safe_signed']=diagnostic_record(vh,L=args.L,K=args.signed_K,N=args.signed_N,c=args.c,s=i*h)
                    # Do not expose exploratory signed values as accepted Gate D results.
                    d.pop('T_sc',None)
                    d.pop('D',None)
                    d.pop('d_over_X',None)
                    d['T_sc']=d['safe_signed']['T_sc']
                    d['diagnostic_status']=d['safe_signed']['diagnostic_status']
                    d['D']=None
                    d['d_over_X']=None
                f.write(json.dumps(dict(s=i*h,**d))+'\n');f.flush()
            if i<steps:vh=step(vh,ks,h,args.c)
    print(json.dumps(dict(output=str(out),**meta),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=12)
    p.add_argument('--L',type=float,default=12)
    p.add_argument('--c',type=float,default=200)
    p.add_argument('--s-end',type=float,default=0.02)
    p.add_argument('--ds',type=float,default=0.01)
    p.add_argument('--log-every',type=int,default=1)
    p.add_argument('--high-fraction',type=float,default=0.5)
    p.add_argument('--signed-K',type=int,default=None,help='enable expensive O(M^2) signed diagnostic, integer high-pass K')
    p.add_argument('--signed-N',type=int,default=None,help='integer radial Galerkin N for diagnostic, distinct from n')
    p.add_argument('--safe-sidecar',action='store_true',help='log exact sparse diagnostic or fail-closed unverified status')
    p.add_argument('--output',default='gate_d_scaffold.jsonl')
    run(p.parse_args())
