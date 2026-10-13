"""Figure 5.1, fig:jw-string: the Jordan-Wigner dictionary and its string.

(a) The local spaces matched: empty to down and occupied to up (the old fig:jw-local).
(b) The string of c_i^dagger: every site to the left of i carries its parity factor 1 - 2 n_j.
(c) A nearest-neighbor hop, where the range of the string is empty and the string is one.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s5 as G                                                     # noqa: E402

NAME = 'jw_string'
TOP = 0.08
Y_BACK = 2.4
XA, XB, XC = -7.4, -0.5, 5.8
OCC = [1, 0, 1, 1]                     # the sites to the left of i in panel (b); three are occupied


def sites(xs, y, tag):
    for k, x in enumerate(xs):
        F.site(f'{tag}_s{k}', (x, y, 0))
        if k < len(xs) - 1:
            F.bond(f'{tag}_b{k}', (x + 0.3, y, 0.05), (xs[k + 1] - 0.3, y, 0.05))


def ghost_ball(name, loc, r=0.26):
    g = F.ghost('ghost_e', F.ELECTRON, 0.28)
    from mathutils import Vector
    return F.obj(name, F.mesh_of(name, [g], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), r)), loc=loc)


def build():
    F.studio()
    # (a) a fermionic site above, a spin below, matched state by state
    xs = [XA - 0.8, XA + 0.8]
    for k, x in enumerate(xs):
        F.site(f'a_f{k}', (x, Y_BACK, 0))
        F.site(f'a_s{k}', (x, 0, 0))
    F.ball('a_e', (xs[1], Y_BACK, TOP + 0.3), 0.26)
    F.arrow('a_dn', (xs[0], 0, TOP + 0.5), (0, 0, -1))
    F.arrow('a_up', (xs[1], 0, TOP + 0.5), (0, 0, 1))
    F.anchor('a', (XA - 1.7, Y_BACK, 1.2))
    F.anchor('k0', (xs[0] - 0.45, Y_BACK, 0.1))
    F.anchor('k1', (xs[1] + 0.4, Y_BACK, 0.35))
    F.anchor('kdn', (xs[0] - 0.4, 0, 0.5))
    F.anchor('kup', (xs[1] + 0.4, 0, 0.5))
    F.anchor('match0', (xs[0], 1.0, 0.25))
    F.anchor('match1', (xs[1], 1.0, 0.25))
    # (b) the string: parity factors on every site to the left of i
    xs = [XB + (k - 3) * 1.0 for k in range(7)]
    i = 4
    sites(xs, 0, 'b')
    for k, n in enumerate(OCC):
        if n:
            F.ball(f'b_e{k}', (xs[k], 0, TOP + 0.3), 0.26)
        F.anchor(f'p{k}', (xs[k], 0, 1.05))
    F.ball('b_e6', (xs[6], 0, TOP + 0.3), 0.26)
    ghost_ball('b_new', (xs[i], 0, TOP + 0.3))
    G.slab('b_string', ((xs[0] + xs[3]) / 2, 0, 0.03), (xs[3] - xs[0] + 0.95, 0.95, 0.06), F.ACCENT[5], alpha=0.45,
           radius=0.03)
    F.anchor('ci', (xs[i], 0, 1.05))
    F.anchor('ib', (xs[i], -0.5, 0))
    F.anchor('Ki', ((xs[0] + xs[3]) / 2 - 0.35, -0.75, 0))
    F.anchor('b', (XB - 3.7, Y_BACK, 1.2))
    # (c) a nearest-neighbor hop: nothing lies between i and i + 1
    xs = [XC - 1.5, XC - 0.5, XC + 0.5, XC + 1.5]
    sites(xs, 0, 'c')
    F.ball('c_e', (xs[2], 0, TOP + 0.3), 0.26)
    ghost_ball('c_new', (xs[1], 0, TOP + 0.3))
    G.hop('c_hop', (xs[2] - 0.08, 0, TOP + 0.65), (xs[1] + 0.08, 0, TOP + 0.65), height=0.55)
    F.anchor('hopc', ((xs[1] + xs[2]) / 2, 0, 1.45))
    F.anchor('ic', (xs[1], -0.5, 0))
    F.anchor('ic1', (xs[2], -0.5, 0))
    F.anchor('one', ((xs[1] + xs[2]) / 2, -1.75, 0))
    F.anchor('c', (XC - 2.2, Y_BACK, 1.2))
    F.camera((-0.4, 1.0, 0.5), elev=30.0, ortho=17.0, aspect=4.0)


F.main(build, NAME)
