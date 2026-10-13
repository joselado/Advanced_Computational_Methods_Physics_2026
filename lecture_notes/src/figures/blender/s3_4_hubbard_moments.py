"""Figure 3.4, fig:hubbard-moments: the mean-field and the exact Hubbard chain at half filling.

(a) Mean-field theory: a finite staggered moment on every site.
(b) The exact ground state of Eq. (hub3), L = 6 and U = 4t, computed in hubbard_corr.py: no moment
    on any site, one sphere per electron and no arrow, and the spin correlation <S_0 . S_j> drawn
    as arcs from the first site, thickness proportional to its size, blue where it is negative and
    orange where it is positive.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s3 as G                                                     # noqa: E402
from hubbard_corr import correlations                                     # noqa: E402

NAME = 'hubbard_moments'
XA, XB = -4.2, 4.0
STEP, L = 1.2, 6
TOP = 0.08
NEG, POS = (0.05, 0.25, 0.85), (0.95, 0.38, 0.04)


def build():
    F.studio()
    # (a) mean field: the staggered moment
    xs = G.chain_sites(XA, 0, L, STEP, 'a', r=0.32)
    for i, x in enumerate(xs):
        F.arrow(f'a_arr{i}', (x, 0, TOP + 0.45), (0, 0, 1 if i % 2 == 0 else -1), length=0.8)
    F.anchor('a', (XA - 3.7, 0, 2.6))
    F.anchor('chainA', (XA, -0.8, 0))
    # (b) exact: no moment, correlations as arcs from site 0
    c, m0 = correlations(L=L, U=4.0)
    xs = G.chain_sites(XB, 0, L, STEP, 'b', r=0.32)
    for i, x in enumerate(xs):
        F.ball(f'b_e{i}', (x, 0, TOP + 0.24), 0.24)
    z0 = TOP + 0.5
    for j in range(1, L):
        tilt = 16.0 * (j - 1)                      # fan the arcs so they leave site 0 apart
        dy = 0.3 * math.sin(math.radians(tilt))
        G.arc(f'b_arc{j}', (xs[0], dy, z0), (xs[j], dy, z0), 0.35 + 0.33 * j, 0.008 + 0.16 * abs(c[j]),
              NEG if c[j] < 0 else POS, tilt=tilt)
    F.anchor('b', (XB - 3.7, 0, 2.6))
    F.anchor('chainB', (XB, -0.8, 0))
    print('m_0 =', m0, 'correlations', c)
    F.camera((0.0, 0.0, 1.0), elev=30.0, ortho=16.5, aspect=3.4)


F.main(build, NAME)
