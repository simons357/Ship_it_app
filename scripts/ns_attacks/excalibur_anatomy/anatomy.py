import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
out=Path('/mnt/data/excalibur_anatomy')
# Exact analytic initial curl field, evaluated with derivatives from sympy.
import sympy as sp
x,y,z=sp.symbols('x y z',real=True)
g=sp.exp(-(x*x+y*y+z*z)/2)
A=sp.Matrix([g*x*y,g*x*z,g*(x+y*z)])
U=sp.Matrix([sp.diff(A[2],y)-sp.diff(A[1],z),sp.diff(A[0],z)-sp.diff(A[2],x),sp.diff(A[1],x)-sp.diff(A[0],y)])
J=U.jacobian([x,y,z]); W=sp.Matrix([sp.diff(U[2],y)-sp.diff(U[1],z),sp.diff(U[0],z)-sp.diff(U[2],x),sp.diff(U[1],x)-sp.diff(U[0],y)])
fun=sp.lambdify((x,y,z),list(U)+list(J)+list(W),'numpy',cse=True)
q=np.linspace(-3,3,101); xx,yy=np.meshgrid(q,q,indexing='xy'); zz=np.zeros_like(xx)
a=[np.asarray(t)+np.zeros_like(xx) for t in fun(xx,yy,zz)]
u=np.stack(a[:3]);j=np.stack(a[3:12]).reshape(3,3,*xx.shape);w=np.stack(a[12:15]);S=(j+np.swapaxes(j,0,1))/2
stretch=np.einsum('i...,ij...,j...->...',w,S,w);enst=np.sum(w*w,axis=0);speed=np.sqrt(np.sum(u*u,axis=0));strain=np.sqrt(np.sum(S*S,axis=(0,1)))
fig,axs=plt.subplots(2,2,figsize=(12,10),layout='constrained')
for ax,data,title,cmap in zip(axs.flat,[speed,enst,stretch,strain],['Velocity magnitude |U|','Vorticity magnitude squared |curl U|²','Vorticity stretching ω·Sω','Strain magnitude |S|'],['viridis','inferno','coolwarm','magma']):
 im=ax.imshow(data,extent=[-3,3,-3,3],origin='lower',cmap=cmap,aspect='equal');ax.set_title(title);ax.set_xlabel('x');ax.set_ylabel('y');fig.colorbar(im,ax=ax,shrink=.8)
fig.suptitle('Exact Gaussian initial field U=curl A, z=0 slice (not time evolution)',fontsize=15)
fig.savefig(out/'gaussian_initial_anatomy.png',dpi=150)
# save arrays for reproducibility
np.savez_compressed(out/'gaussian_z0_slice.npz',x=q,y=q,velocity=u,vorticity=w,stretch=stretch,enstrophy=enst,strain=strain)
(out/'README.md').write_text('Exact analytic Gaussian initial field U=curl(exp(-|x|²/2)*(xy,xz,x+yz)). Slice z=0, x,y from -3 to 3, 101x101. Sympy derivatives, numpy evaluation. Four diagnostic panels. These are initial-data geometry only, NOT a Navier-Stokes trajectory, signed scalene transfer, or blowup evidence. Run python anatomy.py.\n')
print('saved',out/'gaussian_initial_anatomy.png', 'max speed',speed.max(),'max stretch',stretch.max(),'min stretch',stretch.min())
