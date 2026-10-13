"""Figure 1.2, fig:two-interactions: the Hubbard chain and the spinless chain side by side.

(a) Two electrons of opposite spin sharing a site cost U, and the chain orders magnetically.
(b) Two electrons on neighboring sites cost V, and the chain orders in charge.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'two_interactions'
XA, XB = -3.85, 3.85                     # panel centers
STEP, L = 1.1, 6                       # chain spacing and length
Y_BACK = 2.9                           # the two-site vignettes stand behind the chains
TOP = 0.08                             # height of a site disc


def chain(x0, tag):
    xs = [x0 + (i - (L - 1) / 2) * STEP for i in range(L)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, 0, 0))
        if i < L - 1:
            F.bond(f'{tag}_b{i}', (x + 0.3, 0, 0.05), (xs[i + 1] - 0.3, 0, 0.05))
    return xs


def pair(x0, tag):
    xs = [x0 - 0.75, x0 + 0.75]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, Y_BACK, 0))
    F.bond(f'{tag}_b', (xs[0] + 0.3, Y_BACK, 0.05), (xs[1] - 0.3, Y_BACK, 0.05))
    return xs


def build():
    F.studio()
    # (a) the Hubbard chain: an up and a down electron on one site cost U
    xs = pair(XA, 'a2')
    F.arrow('a2_up', (xs[0] - 0.17, Y_BACK, TOP + 0.5), (0, 0, 1))
    F.arrow('a2_dn', (xs[0] + 0.17, Y_BACK, TOP + 0.5), (0, 0, -1))
    g = F.glow('glowU', F.ACCENT[1], strength=1.2, alpha=0.30)
    F.obj('a2_glow', F.mesh_of('a2_glow', [g], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
          loc=(xs[0], Y_BACK, TOP + 0.5), scale=(0.58, 0.58, 0.58))
    F.anchor('U', (xs[0] + 0.55, Y_BACK, TOP + 1.0))
    xs = chain(XA, 'a')
    for i, x in enumerate(xs):
        F.arrow(f'a_arr{i}', (x, 0, TOP + 0.5), (0, 0, 1 if i % 2 == 0 else -1))
    F.anchor('a', (XA - 3.2, Y_BACK, 1.9))
    F.anchor('chainA', (XA, -0.9, 0))
    # (b) the spinless chain: two electrons on neighboring sites cost V
    xs = pair(XB, 'b2')
    for i, x in enumerate(xs):
        F.ball(f'b2_e{i}', (x, Y_BACK, TOP + 0.3), 0.26)
    gv = F.glow('glowV', F.ACCENT[1], strength=1.2, alpha=0.30)
    F.obj('b2_glow', F.mesh_of('b2_glow', [gv], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
          loc=(XB, Y_BACK, TOP + 0.3), scale=(0.75, 0.32, 0.32))
    F.anchor('V', (XB, Y_BACK, TOP + 0.95))
    xs = chain(XB, 'b')
    for i, x in enumerate(xs):
        F.column(f'b_col{i}', (x, 0, TOP), 0.95 if i % 2 == 0 else 0.12)
    F.anchor('b', (XB - 3.2, Y_BACK, 1.9))
    F.anchor('chainB', (XB, -0.9, 0))
    F.camera((0.0, 1.45, 0.55), elev=30.0, ortho=14.6, aspect=3.1)


F.main(build, NAME)
