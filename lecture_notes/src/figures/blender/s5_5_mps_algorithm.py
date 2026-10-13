"""Figure 5.5, fig:mps-algorithm: acting with H on a matrix product state, and the DMRG sweep.

(a) The operator (violet) stacked on the state (teal), their physical legs joined; the two bonds
    running in parallel merge into one of dimension chi chi_W (a thick rod), and the singular value
    decomposition on every bond compresses it back to chi (a thin rod).
(b) The sweep: bra, operator and ket, with everything left of site i contracted into the left
    environment and everything right of it into the right one; the ket and bra tensors at i are
    left out, so what is drawn is H_eff(i), with the open legs on which M_i sits. The arc
    above says the step then moves one site over.
Tensors and legs as in fig:tensor-notation.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s5 as G                                                     # noqa: E402

NAME = 'mps_algorithm'
TEAL = F.TENSOR
VIOLET = (0.36, 0.17, 0.85)
LEGC = (0.30, 0.31, 0.36)
ENV = (0.42, 0.46, 0.60)
C = 0.5                                # size of a tensor cube
H = C / 2
STEP = 1.05
LEG = 0.4
ZK = 0.36                              # the lowest chain sits just above the floor, so the shadows stay short


def cube(name, loc, rgb, ghost=False, size=C):
    if ghost:
        g = F.ghost('ghost_tensor', TEAL, 0.22)
        return F.obj(name, F.mesh_of(name, [g], lambda bm: F.bm_rounded_box(bm, F.Vector((0, 0, 0)), (size,) * 3, 0.1)),
                     loc=loc)
    m = F.mat('tensor_s5_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.35, emit=0.0, spec=0.5)
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_rounded_box(bm, F.Vector((0, 0, 0)), (size,) * 3, 0.1)),
                 loc=loc)


def row(tag, xs, z, rgb, up=True, down=True, bond_r=0.06, ghost=()):
    """A chain of tensors; the sites in `ghost` are left out, and the legs that met them end open."""
    for k, x in enumerate(xs):
        if k not in ghost:                          # left out: the legs that met it end open
            cube(f'{tag}{k}', (x, 0, z), rgb)
        if up:
            F.leg(f'{tag}{k}_u', (x, 0, z + H), (x, 0, z + H + LEG), rgb=LEGC)
        if down:
            F.leg(f'{tag}{k}_d', (x, 0, z - H), (x, 0, z - H - LEG), rgb=LEGC)
        if k < len(xs) - 1:
            F.leg(f'{tag}{k}_b', (x + H, 0, z), (xs[k + 1] - H, 0, z), r=bond_r, rgb=LEGC)


def build():
    F.studio()
    # (a) stage 1: the operator on the state
    z0, z1 = ZK, ZK + C + 2 * LEG
    xs = [-8.6 + k * STEP for k in range(3)]
    row('ak', xs, z0, TEAL, up=False, down=False)
    row('aw', xs, z1, VIOLET, up=True, down=False)
    for k, x in enumerate(xs):                      # the joined physical legs
        F.leg(f'aj{k}', (x, 0, z0 + H), (x, 0, z1 - H), rgb=LEGC)
    F.anchor('chiS', (xs[0] - 0.35, 0, z0))
    F.anchor('chiW', (xs[0] - 0.35, 0, z1))
    F.anchor('HPsi', (xs[1], 0, z0 - 0.45))
    G.flow('af1', (xs[2] + 0.55, 0, ZK + 0.35), (xs[2] + 1.45, 0, ZK + 0.35))
    # stage 2: one fat bond of dimension chi chi_W
    zm = ZK
    xs = [-4.7 + k * STEP for k in range(3)]
    row('am', xs, zm, TEAL, up=True, down=False, bond_r=0.13)
    F.anchor('chichiW', ((xs[1] + xs[2]) / 2, 0, zm - 0.3))
    G.flow('af2', (xs[2] + 0.55, 0, ZK + 0.35), (xs[2] + 1.45, 0, ZK + 0.35))
    F.anchor('svd', (xs[2] + 1.0, 0, ZK + 0.5))
    # stage 3: compressed back to chi
    xs = [-0.8 + k * STEP for k in range(3)]
    row('ac', xs, zm, TEAL, up=True, down=False, bond_r=0.05)
    F.anchor('chi', ((xs[1] + xs[2]) / 2, 0, zm - 0.3))
    # (b) the local problem of the sweep: the ket and bra tensors at i are left out, open legs
    zk, zw, zb = ZK, ZK + C + 2 * LEG, ZK + 2 * (C + 2 * LEG)
    n, i = 5, 2
    xs = [3.2 + k * STEP for k in range(n)]
    row('bk', xs, zk, TEAL, up=False, down=False, ghost=(i,))
    row('bw', xs, zw, VIOLET, up=False, down=False)
    row('bb', xs, zb, TEAL, up=False, down=False, ghost=(i,))
    for k, x in enumerate(xs):
        F.leg(f'bj{k}', (x, 0, zk + H), (x, 0, zw - H), rgb=LEGC)
        F.leg(f'bj2{k}', (x, 0, zw + H), (x, 0, zb - H), rgb=LEGC)
    zc, dz = (zk + zb) / 2, zb - zk + C + 0.35
    G.slab('envL', ((xs[0] + xs[1]) / 2, 0, zc), (xs[1] - xs[0] + C + 0.4, 0.9, dz), ENV, alpha=0.16, radius=0.2)
    G.slab('envR', ((xs[3] + xs[4]) / 2, 0, zc), (xs[4] - xs[3] + C + 0.4, 0.9, dz), ENV, alpha=0.16, radius=0.2)
    F.anchor('L', ((xs[0] + xs[1]) / 2, 0, zc - dz / 2 - 0.1))
    F.anchor('R', ((xs[3] + xs[4]) / 2, 0, zc - dz / 2 - 0.1))
    F.anchor('site', (xs[i], 0, zc - dz / 2 - 0.1))
    F.anchor('Mi', (xs[i] + 0.12, 0, zk))
    G.hop('sweep', (xs[i] - 0.1, 0, zb + H + 0.3), (xs[i + 1] + 0.1, 0, zb + H + 0.3), height=0.3)
    F.anchor('sweep', (xs[i + 1] + 0.25, 0, zb + H + 0.3))
    F.anchor('heff', (xs[i], 0, zb + H + 0.95))
    F.anchor('b', (xs[0] - 1.05, 0, zb + H + 1.75))
    F.anchor('a', (-9.6, 0, zb + H + 1.75))
    F.camera((-1.1, 0.0, 1.9), elev=30.0, ortho=18.4, aspect=3.35)


F.main(build, NAME)
