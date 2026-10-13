"""Figure 5.3, fig:corr-entropy: the eigenvalues of the correlation matrix as the fillings of cups.

(a) A Slater determinant, the four-site Hubbard chain of the notebook at U = 0 and half filling:
    the eight natural orbitals are either full or empty, nu_k = 1 or 0, and S_corr = 0.
(b) The same chain at U = 6t: nu_k = 0.82, 0.73, 0.27, 0.18, each twice (the two spins), and
    S_corr = 4.22. Exact diagonalization of H = t sum (c^dag_i c_{i+1} + h.c.) + U sum (n_up - 1/2)(n_dn - 1/2),
    the notebook's get_mz at Jz = 0.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 'corr_entropy'
XA, XB = -4.0, 4.0
STEP = 0.86
H = 1.3
NU_A = [1, 1, 1, 1, 0, 0, 0, 0]
NU_B = [0.821, 0.821, 0.728, 0.728, 0.272, 0.272, 0.179, 0.179]


def row(x0, nus, tag):
    xs = [x0 + (k - 3.5) * STEP for k in range(8)]
    for k, (x, n) in enumerate(zip(xs, nus)):
        F.cup(f'{tag}_cup{k}', (x, 0, 0), n, r=0.32, h=H)
        F.anchor(f'{tag}nu{k}', (x, -0.45, 0))
    return xs


def build():
    F.studio()
    row(XA, NU_A, 'a')
    row(XB, NU_B, 'b')
    F.anchor('a', (XA - 3.9, 0, 2.15))
    F.anchor('b', (XB - 3.9, 0, 2.15))
    F.anchor('Sa', (XA + 0.3, 0, 1.75))
    F.anchor('Sb', (XB + 0.3, 0, 1.75))
    F.camera((0.0, 0.0, 0.75), elev=30.0, ortho=16.6, aspect=4.6)


F.main(build, NAME)
