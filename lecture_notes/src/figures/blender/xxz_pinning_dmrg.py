"""The densities drawn in figure 5.2 (s5_2_xxz_pinning.py, the lists VT and V40).

The pinned spinless chain of the notebook (L = 100, m = 0.1t, chi = 20) at V = t and V = 40t, seeded
in the orientation the pinning favors; prints the first 24 densities and writes pin2.json.
Run with dmrgpy (it took a few minutes on D22).
"""
import json
from dmrgpy import fermionchain
L = 100
def ham(fc, V, m):
    H = 0
    for i in range(L-1):
        H = H + fc.Cdag[i]*fc.C[i+1]
    H = H + H.get_dagger()
    H = H + m*(fc.N[0] - fc.N[L-1])
    for i in range(L-1):
        H = H + V*(fc.N[i]-0.5)*(fc.N[i+1]-0.5)
    return H
out = {}
for V in (1.0, 40.0):
    fc = fermionchain.Fermionic_Chain(L)
    fc.maxm = 20
    # seed: a staggered field that selects the orientation favored by the pinning (first site empty)
    Hs = ham(fc, V, 0.1) + sum(5.0*(-1)**i*fc.N[i] for i in range(L))
    fc.set_hamiltonian(Hs)
    seed = fc.get_gs(mode="DMRG")
    H = ham(fc, V, 0.1)
    fc.set_hamiltonian(H)
    fc.set_initial_wf_guess(seed)
    wf = fc.get_gs(mode="DMRG")
    E = wf.dot(H*wf).real
    d = [wf.dot(Ni*wf).real for Ni in fc.N]
    # the unseeded run, for comparison
    fc2 = fermionchain.Fermionic_Chain(L); fc2.maxm = 20
    H2 = ham(fc2, V, 0.1); fc2.set_hamiltonian(H2)
    w2 = fc2.get_gs(mode="DMRG"); E2 = w2.dot(H2*w2).real
    out[str(V)] = d
    print(V, 'seeded E=%.6f' % E, 'unseeded E=%.6f' % E2, ' '.join('%.3f' % x for x in d[:24]))
json.dump(out, open('pin2.json', 'w'))
