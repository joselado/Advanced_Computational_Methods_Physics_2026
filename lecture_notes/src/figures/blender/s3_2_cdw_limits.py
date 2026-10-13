"""Figure 3.2, fig:cdw-limits: the two solvable limits of the spinless chain, Eq. (cdw3).

(a) V = 0: the free metal at half filling, the same density 1/2 on every site, cups half full.
(b) V to infinity: the alternating pattern 1, 0, 1, 0, with its partner shifted by one site
    standing behind it as a ghost, the twofold degeneracy of the charge density wave.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s3 as G                                                     # noqa: E402

NAME = 'cdw_limits'
XA, XB = -4.1, 4.1                     # panel centers
STEP, L = 0.95, 8
H = 1.0                                # height of a full cup, density 1
Y_BACK = 3.3
TOP = 0.08


def build():
    F.studio()
    # (a) V = 0: every cup half full
    ya = Y_BACK / 2                                # mid-depth of the two rows of (b)
    xs = G.chain_sites(XA, ya, L, STEP, 'a', r=0.33)
    for i, x in enumerate(xs):
        F.cup(f'a_cup{i}', (x, ya, TOP), 0.5, r=0.3, h=H)
    F.anchor('a', (XA - 4.2, Y_BACK, 2.3))
    F.anchor('nA', (XA, ya - 0.7, 0))
    # (b) V to infinity: 1, 0, 1, 0 in front, the shifted partner behind as a ghost
    xs = G.chain_sites(XB, 0, L, STEP, 'b', r=0.33)
    for i, x in enumerate(xs):
        F.cup(f'b_cup{i}', (x, 0, TOP), 1.0 if i % 2 == 0 else 0.0, r=0.3, h=H)
    xs = G.chain_sites(XB, Y_BACK, L, STEP, 'g', r=0.33)
    for i, x in enumerate(xs):
        F.cup(f'g_cup{i}', (x, Y_BACK, TOP), 0.0, r=0.3, h=H)
        if i % 2 == 1:
            G.ghost_column(f'g_col{i}', (x, Y_BACK, TOP + 0.03), H - 0.06, r=0.27)
    F.anchor('b', (XB - 4.2, Y_BACK, 2.3))
    F.anchor('front', (XB, -0.7, 0))
    F.anchor('back', (XB, Y_BACK, H + 0.3))
    F.camera((0.0, 1.6, 0.6), elev=30.0, ortho=17.0, aspect=3.0)


F.main(build, NAME)
