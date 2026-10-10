import unittest
import numpy as np
from gaussian_gate_d import grid, project, nonlinear, diagnostics

class TestG(unittest.TestCase):
    def test_exact_fourier_triad_production(self):
        n,L,c=9,2*np.pi,200
        xyz,ks=grid(n,L)
        x,y,z=xyz
        v=np.stack((np.sin(y)+0.2*np.cos(z),np.sin(z)+0.3*np.cos(x),np.sin(x)+0.4*np.cos(y)))
        vh=project(np.fft.fftn(v,axes=(1,2,3)),*ks[:4])*ks[4]
        d=diagnostics(vh,ks,L,c,.5)
        kx,ky,kz,k2,mask=ks
        # Independent spectral convolution: N_k=-i P_k sum_{p+q=k}(q dot u_p)u_q
        modes=np.fft.fftfreq(n)*n
        coeff=vh/n**3
        coeffs={(int(a),int(b),int(cc)):coeff[:,i,j,k] for i,a in enumerate(modes) for j,b in enumerate(modes) for k,cc in enumerate(modes) if np.linalg.norm(coeff[:,i,j,k])>1e-12}
        prod=0j
        for k,u_k in coeffs.items():
            conv=np.zeros(3,dtype=complex)
            for p,u_p in coeffs.items():
                q=tuple(k[j]-p[j] for j in range(3))
                if q in coeffs:
                    conv+=1j*np.dot(q,u_p)*coeffs[q]
            # Projection unnecessary for pairing with solenoidal u_k
            prod+=np.vdot(u_k,np.dot(k,k)*(-conv))
        prod=(L**3*prod).real
        self.assertAlmostEqual(d['production'],prod,places=9)
        self.assertAlmostEqual(d['G'],prod-d['Y']/c,places=9)
        self.assertIsNone(d['T_sc'])
        self.assertIsNone(d['D'])

if __name__=='__main__':unittest.main()
