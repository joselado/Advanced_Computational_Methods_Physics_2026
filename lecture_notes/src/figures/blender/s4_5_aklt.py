"""Figure 4.5, fig:aklt: the AKLT picture of the spin-1 chain.

(a) One spin-1 as two spin-1/2 (grey spheres) inside one capsule, the projector onto the symmetric (S = 1) states.
(b) Singlet bonds joining the halves of neighboring sites; the outer half of each end site is left
    without a partner.
(c) The same chain with those two unpaired spin-1/2 lit, both pointing down: a small uniform field
    (+Bz Sz, as in the notebook) polarizes both, so each edge region carries -1/2.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s4 as G                                                     # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'aklt'
N, STEP = 4, 1.08                      # spin-1 sites per chain and their spacing
HALF = 0.22                            # offset of each spin-1/2 from the center of its capsule
ZC = 0.42                              # height of the capsules
R = 0.13                               # radius of a spin-1/2
HALF_RGB = (0.30, 0.33, 0.42)          # a spin-1/2 paired in a singlet, no moment of its own


def capsule(name, loc, scale=1.0):
    g = F.ghost('capsule', (0.10, 0.65, 0.65), 0.13)
    me = F.mesh_of(name, [g], lambda bm: F.bm_rounded_box(bm, Vector((0, 0, 0)),
                                                         (0.92 * scale, 0.46 * scale, 0.46 * scale),
                                                         0.21 * scale))
    F.site(name + '_site', (loc[0], loc[1], 0), r=0.3, h=0.05)
    return F.obj(name, me, loc=loc)


def chain(x0, tag, lit):
    xs = [x0 + (i - (N - 1) / 2) * STEP for i in range(N)]
    for i, x in enumerate(xs):
        capsule(f'{tag}_cap{i}', (x, 0, ZC))
        for h, dx in enumerate((-HALF, HALF)):
            end = (i == 0 and h == 0) or (i == N - 1 and h == 1)
            if end and lit:
                F.arrow(f'{tag}_end{i}', (x + dx, 0, ZC), (0, 0, -1), length=0.62)   # along the field, +Bz Sz
            else:
                F.ball(f'{tag}_h{i}_{h}', (x + dx, 0, ZC), R, rgb=HALF_RGB, emit=0.05)
        if i < N - 1:
            G.arc(f'{tag}_sing{i}', (x + HALF + R, 0, ZC), (xs[i + 1] - HALF - R, 0, ZC), 0.12, r=0.045)
    return xs


def build():
    F.studio()
    # (a) one spin-1 as two spin-1/2 in a capsule
    xa, s = -4.9, 1.7
    capsule('a_cap', (xa, 0, ZC * s), scale=s)
    for k, dx in enumerate((-HALF * s, HALF * s)):
        F.ball(f'a_half{k}', (xa + dx, 0, ZC * s), R * s, rgb=HALF_RGB, emit=0.05)
    F.anchor('a', (xa - 1.2, 0, 1.75))
    F.anchor('aS1', (xa, 0, ZC * s + 0.62))
    F.anchor('ahalf', (xa, -0.6, 0))
    # (b) singlet bonds between neighboring halves
    xs = chain(-0.85, 'b', lit=False)
    F.anchor('b', (xs[0] - 0.75, 0, 1.75))
    F.anchor('bsing', ((xs[1] + xs[2]) / 2, 0, ZC + 0.2))
    F.anchor('blbl', (-0.85, -0.6, 0))
    # (c) the two unpaired halves at the ends, the edge moments
    xs = chain(3.75, 'c', lit=True)
    F.anchor('c', (xs[0] - 0.75, 0, 1.75))
    F.anchor('cleft', (xs[0] - HALF, -0.45, 0))
    F.anchor('cright', (xs[-1] + HALF, -0.45, 0))
    F.camera((-0.25, 0.0, 0.6), elev=26.0, ortho=12.9, aspect=4.0)


F.main(build, NAME)
