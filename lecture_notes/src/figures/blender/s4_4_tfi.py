"""Figure 4.4, fig:tfi: the transverse-field Ising chain at zero, critical and large field.

(a) B_x = 0: every arrow along z, with the all-down partner standing behind as a ghost; a cut
    through it severs nothing.
(b) B_x near J/2: domains of every size, and the strands across the cut at their thickest.
(c) B_x much larger than J: every arrow along x, again a product state with nothing across the cut.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s4 as G                                                     # noqa: E402

NAME = 'tfi'
L, STEP = 8, 0.62
TOP = 0.06
LEN = 0.62
XS = (-5.6, 0.0, 5.6)                  # panel centers
YG = 2.1                              # the ghost partner of (a) stands behind the chain


def chain(x0, tag):
    xs = [x0 + (i - (L - 1) / 2) * STEP for i in range(L)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, 0, 0), r=0.2, h=TOP)
        if i < L - 1:
            F.bond(f'{tag}_b{i}', (x + 0.2, 0, 0.04), (xs[i + 1] - 0.2, 0, 0.04), r=0.03)
    G.pane(f'{tag}_cut', ((xs[3] + xs[4]) / 2, 0, 0), w=0.5, h=1.25, turn=30.0)
    return xs


def build():
    F.studio()
    # (a) zero field: the ferromagnet along z and its all-down partner
    xs = chain(XS[0], 'a')
    for i, x in enumerate(xs):
        F.arrow(f'a_arr{i}', (x, 0, TOP + LEN / 2), (0, 0, 1), length=LEN)
        gh = F.ghost_arrow(f'a_gh{i}', (x, YG, TOP + LEN / 2), (0, 0, -1), length=LEN, alpha=0.28)
        gh.visible_shadow = False            # a ghost casts no shadow
    F.anchor('ghost', (XS[0], YG, TOP + LEN + 0.15))
    # (b) near the critical field: domains of every size, tilted a little toward x
    xs = chain(XS[1], 'b')
    pattern = [1, 1, -1, 1, 1, 1, -1, -1]
    for i, (x, s) in enumerate(zip(xs, pattern)):
        th = math.radians(28)
        F.arrow(f'b_arr{i}', (x, 0, TOP + LEN / 2), (math.sin(th), 0, s * math.cos(th)), length=LEN)
    for k, (i, j) in enumerate([(3, 4), (2, 4), (3, 5), (2, 5), (1, 5), (2, 6), (1, 6), (0, 7)]):
        dy = 0.15                              # from the back rim of the disk, behind the arrow
        G.arc(f'b_str{k}', (xs[i], dy, TOP), (xs[j], dy, TOP), 0.62 + 0.07 * (j - i), r=0.024)
    # (c) large field: every arrow along x
    xs = chain(XS[2], 'c')
    for i, x in enumerate(xs):
        F.arrow(f'c_arr{i}', (x, 0, TOP + 0.42), (1, 0, 0), length=0.36)
    for k, x0 in enumerate(XS):
        F.anchor('abc'[k], (x0 - (L - 1) / 2 * STEP - 0.45, 0, 2.55))
        F.anchor('lbl' + 'abc'[k], (x0, -0.55, 0))
    F.camera((0.0, 0.35, 0.55), elev=26.0, ortho=16.6, aspect=4.0)


F.main(build, NAME)
