"""Figure 2.5, fig:abrikosov: the Abrikosov fermions and the spinon band.

(a) One site as two fermion slots, up (left) and down (right), with its four states |0>, |up>, |dn>, |up dn>;
    the empty and the doubly occupied are ghosted by the constraint, and the two that remain are the spin-1/2.
(b) One bond: at the back the spin exchange J S_i.S_j on the two sites, in front the same two sites with a
    fermion hopping across the bond, the bond operator chi_ij.
(c) The spinon band eps(k) = -J chi cos k as a ribbon, filled (cyan) up to k_F = +-pi/2, empty (ghost)
    above, with a particle-hole pair at the right Fermi point: a hole just below k_F, a particle just above.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s2 as G                                                     # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'abrikosov'
XA, XB, XC = -6.5, -1.2, 5.0
TOP = 0.08


def state(x, y, up, dn, ghosted, tag):
    """A site with two slots; an occupied slot carries an arrow of its spin."""
    if ghosted:
        G.ghost_site(f'{tag}_s', (x, y, 0), r=0.55, h=0.06)
    else:
        F.site(f'{tag}_s', (x, y, 0), r=0.55, h=0.06)
    for k, (occ, d) in enumerate(((up, 1), (dn, -1))):
        xs = x + (k - 0.5) * 0.5
        pad = F.mat('pad', (0.80, 0.81, 0.85), rough=0.6, spec=0.2) if not ghosted else \
            F.ghost('ghost_pad', (0.80, 0.81, 0.85), 0.25)
        F.obj(f'{tag}_pad{k}', F.mesh_of(f'{tag}_pad{k}', [pad], lambda bm: F.bm_cylinder(
            bm, (0, 0, 0), (0, 0, 0.03), 0.17, seg=32)), loc=(xs, y, 0.06))
        if occ:                             # a fermion: a cyan ball carrying a small arrow, as in (b)
            bz, az = 0.09 + 0.15, 0.09 + 0.3 + 0.2
            if ghosted:
                gm = F.ghost('ghost_e', F.ELECTRON, 0.28)
                F.obj(f'{tag}_e{k}', F.mesh_of(f'{tag}_e{k}', [gm], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), 0.15)),
                      loc=(xs, y, bz))
                F.ghost_arrow(f'{tag}_ar{k}', (xs, y, az), (0, 0, d), length=0.4, alpha=0.28)
            else:
                F.ball(f'{tag}_e{k}', (xs, y, bz), 0.15)
                F.arrow(f'{tag}_ar{k}', (xs, y, az), (0, 0, d), length=0.4)


def build():
    F.studio()
    # (a) the four states of one site, two by two: back row empty and double (ghosts), front row up and down
    dx, yb = 1.55, 2.3
    state(XA - dx / 2, yb, 0, 0, True, 'a0')
    state(XA + dx / 2, yb, 1, 1, True, 'a3')
    state(XA - dx / 2, 0.0, 1, 0, False, 'a1')
    state(XA + dx / 2, 0.0, 0, 1, False, 'a2')
    F.anchor('k0', (XA - dx / 2 - 0.7, yb, 0.1))
    F.anchor('k3', (XA + dx / 2 + 0.7, yb, 0.1))
    F.anchor('k1', (XA - dx / 2 - 0.7, 0.0, 0.1))
    F.anchor('k2', (XA + dx / 2 + 0.7, 0.0, 0.1))
    F.anchor('a', (XA - 2.4, yb, 2.6))
    F.anchor('labA', (XA, -0.9, 0))
    # (b) the same bond twice: spin exchange behind, fermion hopping in front
    xi, xj, yb2 = XB - 0.85, XB + 0.85, 2.7
    for y, tag in ((yb2, 'bs'), (0.0, 'bf')):
        F.site(f'{tag}_i', (xi, y, 0))
        F.site(f'{tag}_j', (xj, y, 0))
        F.bond(f'{tag}_b', (xi + 0.3, y, 0.05), (xj - 0.3, y, 0.05))
    F.arrow('bs_ai', (xi, yb2, TOP + 0.45), (0, 0, 1), length=0.8)
    F.arrow('bs_aj', (xj, yb2, TOP + 0.45), (0, 0, -1), length=0.8)
    G.arc('bs_J', (xi + 0.2, yb2, TOP + 0.95), (xj - 0.2, yb2, TOP + 0.95), 0.25, r=0.05,
          m=F.mat('exch', (0.55, 0.56, 0.60), rough=0.5, spec=0.3))
    F.anchor('J', (XB, yb2, TOP + 1.35))
    for x, d, tag in ((xi, 1, 'i'), (xj, -1, 'j')):
        F.ball(f'bf_e{tag}', (x, 0.0, TOP + 0.2), 0.19)
        F.arrow(f'bf_a{tag}', (x, 0.0, TOP + 0.39 + 0.21), (0, 0, d), length=0.42)
    G.arc_arrow('bf_hop1', (xi + 0.2, 0.0, TOP + 0.6), (xj - 0.15, 0.0, TOP + 0.55), 0.35, r=0.035, head=0.12)
    G.arc_arrow('bf_hop2', (xj - 0.2, -0.5, TOP + 0.35), (xi + 0.2, -0.5, TOP + 0.35), -0.2, r=0.035, head=0.12)
    F.anchor('chi', (xj + 0.45, 0.0, TOP + 0.45))
    F.anchor('b', (XB - 2.0, yb, 2.6))
    F.anchor('labB', (XB, -0.9, 0))
    # (c) the spinon band
    sx, sz, z0, yc = 0.85, 0.85, 1.1, 1.0
    full = F.mat('spinon_full', F.ELECTRON, rough=0.35, emit=0.1, spec=0.5)
    empty = F.ghost('spinon_empty', (0.62, 0.66, 0.74), 0.35)

    def pt(k):
        return (XC + k * sx, z0 - sz * math.cos(k))

    n = 60
    ks = [-math.pi + 2 * math.pi * i / n for i in range(n + 1)]
    for name, lo, hi, m in (('c_l', -math.pi, -math.pi / 2, empty), ('c_f', -math.pi / 2, math.pi / 2, full),
                            ('c_r', math.pi / 2, math.pi, empty)):
        seg = [k for k in ks if lo - 1e-9 <= k <= hi + 1e-9]
        G.ribbon(name, [pt(k) for k in seg], 0.9, 0.08, m).location = (0, yc, 0)
    # the Fermi level and the axes
    F.leg('c_ef', (XC - math.pi * sx - 0.2, yc + 0.5, z0), (XC + math.pi * sx + 0.2, yc + 0.5, z0), r=0.02)
    for kk in (-math.pi / 2, math.pi / 2):            # ticks at the Fermi points
        F.leg(f'c_tick{kk:+.1f}', (XC + kk * sx, yc + 0.5, z0 - 0.12), (XC + kk * sx, yc + 0.5, z0 + 0.12), r=0.022)
    F.leg('c_ax', (XC, yc + 0.5, z0 - sz - 0.35), (XC, yc + 0.5, z0 + sz + 0.4), r=0.025)
    # the particle-hole pair at the right Fermi point
    kh, kp = math.pi / 2 - 0.45, math.pi / 2 + 0.45
    hx, hz = pt(kh)
    px, pz = pt(kp)
    F.ball('c_hole', (hx, yc - 0.1, hz + 0.24), 0.17, rgb=(0.97, 0.97, 0.98), emit=0.0)
    F.ball('c_part', (px, yc - 0.1, pz + 0.24), 0.17)
    G.arc_arrow('c_ph', (hx + 0.05, yc - 0.1, hz + 0.45), (px - 0.05, yc - 0.1, pz + 0.45), 0.35, r=0.035, head=0.12)
    F.anchor('kF', (XC + math.pi / 2 * sx, yc + 0.5, z0))
    F.anchor('mkF', (XC - math.pi / 2 * sx, yc + 0.5, z0))
    F.anchor('eps', (XC, yc + 0.5, z0 + sz + 0.4))
    F.anchor('kend', (XC + math.pi * sx + 0.2, yc + 0.5, z0))
    F.anchor('c', (XC - 3.2, yb, 2.6))
    F.anchor('labC', (XC, -0.9, 0))
    F.camera((-0.3, 1.3, 1.25), elev=30.0, ortho=18.2, aspect=3.5)


F.main(build, NAME)
