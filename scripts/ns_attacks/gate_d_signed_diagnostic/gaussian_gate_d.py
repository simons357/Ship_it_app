#!/usr/bin/env python3
"""Preregisterable replacement scaffold for Gate D Gaussian packet.
Not the recovered historical driver. Does not implement T_sc or D.
Classical unforced NSE in nondimensional form on a periodic box.
"""
import argparse, json, hashlib
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

def diagnostics(vh,ks,L,c,high_fraction):
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
    return dict(energy=norm/2,X=x,Y=y,production=production,G=float(production-y/c),high_shell_energy=high,max_fourier_divergence=float(div),T_sc=None,D=None)

def run(args):
    xyz,ks=grid(args.n,args.L)
    v0=gaussian_curl(*xyz)
    vh=np.fft.fftn(v0,axes=(1,2,3))
    vh=project(vh,*ks[:4])*ks[4]
    steps=int(np.ceil(args.s_end/args.ds))
    h=args.s_end/steps
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    source_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    meta=dict(kind='NEW REPLACEMENT SCAFFOLD; NOT ORIGINAL DRIVER',c=args.c,n=args.n,L=args.L,ds=h,s_end=args.s_end,periodization='sample Gaussian on periodic cube, then project and 2/3 filter',cutoff='componentwise 2/3 mask',T_sc_implemented=False,D_implemented=False,G_implemented=True,source_sha256=source_hash)
    with out.open('w') as f:
        f.write(json.dumps(dict(metadata=meta))+'\n')
        for i in range(steps+1):
            if i%args.log_every==0 or i==steps:
                d=diagnostics(vh,ks,args.L,args.c,args.high_fraction)
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
    p.add_argument('--output',default='gate_d_scaffold.jsonl')
    run(p.parse_args())
