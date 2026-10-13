"""Figure 5.2, fig:xxz-pinning: the spinless chain as the XXZ chain, and charge order from a pinning field.

(a) The dictionary on one pair of sites, fermions behind and spins in front: the hop of an electron
    is the flip-flop of an up and a down spin, and V n_i n_{i+1} is V S^z_i S^z_{i+1} up to a field.
(b) The first 24 of the L = 100 sites, pinned with m (n_1 - n_L), m = 0.1t, chi = 20: the densities
    are the DMRG ones of the notebook's get_den. At V = t (back row) the edge oscillation is a few
    percent and decays into the bulk; at V = 40t (front row) the order is locked from edge to edge.
    Both runs start from the ground state with an extra staggered field 5t (-1)^i n_i, which seeds the
    orientation the pinning favors; at V = 40t a run from a random start locks into the opposite
    pattern, 0.199t higher in energy, while the seeded one ends with n_1 = 0.002. At V = t the seeded
    and unseeded runs agree. The numbers come from xxz_pinning_dmrg.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s5 as G                                                     # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'xxz_pinning'
TOP = 0.08
Y_BACK = 2.8
XA, XB = -6.3, 2.75
VT = [0.459, 0.525, 0.48, 0.516, 0.486, 0.512, 0.489, 0.51, 0.491, 0.508, 0.492, 0.507, 0.493, 0.507, 0.494, 0.506, 0.494, 0.506, 0.495, 0.505, 0.495, 0.505, 0.495, 0.505]
V40 = [0.002, 0.997, 0.001, 0.999, 0.001, 0.999, 0.001, 0.999, 0.001, 0.999, 0.001, 0.999, 0.001, 0.999, 0.001, 0.999, 0.001, 0.999, 0.001, 0.999, 0.001, 0.999, 0.001, 0.999]
HMAX = 1.1                             # column height of a full site
STEP = 0.42
Y_ROW = 2.8                            # the two rows of (b) are further apart, the columns are tall


def pair(x0, y, tag):
    xs = [x0 - 0.55, x0 + 0.55]
    for k, x in enumerate(xs):
        F.site(f'{tag}_s{k}', (x, y, 0), r=0.28)
    F.bond(f'{tag}_b', (xs[0] + 0.28, y, 0.05), (xs[1] - 0.28, y, 0.05))
    return xs


def ghost_ball(name, loc, r=0.24):
    g = F.ghost('ghost_e', F.ELECTRON, 0.28)
    return F.obj(name, F.mesh_of(name, [g], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), r)), loc=loc)


def build():
    F.studio()
    # (a) hopping and flip-flop
    xh, xv = XA - 1.25, XA + 1.25
    xs = pair(xh, Y_BACK, 'ah_f')
    F.ball('ah_e', (xs[1], Y_BACK, TOP + 0.28), 0.24)
    ghost_ball('ah_g', (xs[0], Y_BACK, TOP + 0.28))
    G.hop('ah_hop', (xs[1] - 0.05, Y_BACK, TOP + 0.62), (xs[0] + 0.05, Y_BACK, TOP + 0.62), height=0.45)
    F.anchor('tf', (xh, Y_BACK, 1.35))
    xs = pair(xh, 0, 'ah_s')
    F.arrow('ah_dn', (xs[0] - 0.13, 0, TOP + 0.45), (0, 0, -1), length=0.75)
    F.ghost_arrow('ah_g_up', (xs[0] + 0.13, 0, TOP + 0.45), (0, 0, 1), length=0.75, alpha=0.3)
    F.arrow('ah_up', (xs[1], 0, TOP + 0.45), (0, 0, 1), length=0.75)
    G.hop('ah_flip', (xs[1] - 0.05, 0, TOP + 0.9), (xs[0] + 0.05, 0, TOP + 0.9), height=0.3)
    F.anchor('ts', (xh, -0.55, 0))
    # (a) the density-density term
    xs = pair(xv, Y_BACK, 'av_f')
    for k, x in enumerate(xs):
        F.ball(f'av_e{k}', (x, Y_BACK, TOP + 0.28), 0.24)
    g = F.glow('glowV', F.ACCENT[1], strength=1.2, alpha=0.30)
    F.obj('av_glow', F.mesh_of('av_glow', [g], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
          loc=(xv, Y_BACK, TOP + 0.12), scale=(0.9, 0.42, 0.2))
    F.anchor('Vf', (xv, Y_BACK, 1.0))
    xs = pair(xv, 0, 'av_s')
    for k, x in enumerate(xs):
        F.arrow(f'av_up{k}', (x, 0, TOP + 0.45), (0, 0, 1), length=0.75)
    F.anchor('Vs', (xv, -0.55, 0))
    F.anchor('a', (XA - 2.6, Y_ROW, 2.75))
    # (b) the pinned chains, first 24 sites
    x0 = XB - (len(VT) - 1) / 2 * STEP
    for row, (y, dens) in enumerate([(Y_ROW, VT), (0.0, V40)]):
        for k, n in enumerate(dens):
            x = x0 + k * STEP
            F.site(f'b{row}_s{k}', (x, y, 0), r=0.17, h=0.06)
            if n * HMAX > 0.01:
                F.column(f'b{row}_c{k}', (x, y, 0.06), n * HMAX, r=0.14)
        F.anchor(f'row{row}', (x0 - 0.35, y, 0.35))
    F.anchor('edge', (x0, -0.45, 0))
    F.anchor('bulk', (x0 + (len(VT) - 1) * STEP, -0.45, 0))
    F.anchor('b', (XB - 5.3, Y_ROW, 2.75))
    F.camera((-0.25, 1.3, 0.6), elev=30.0, ortho=17.6, aspect=3.4)


F.main(build, NAME)
