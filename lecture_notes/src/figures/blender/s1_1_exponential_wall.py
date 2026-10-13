"""Figure 1.1, fig:exponential-wall: why the many-body problem is exponential, at a glance.

(a) One electron on a chain of four sites, at its four possible positions (one drawn, three as
    ghosts): four states, a 4x4 matrix.
(b) The same four sites holding any number of electrons: the sixteen occupation configurations
    stacked as a column of thin slabs, one slab per basis state, grouped by electron number.
(c) The dimension against L from 2 to 10, the single-particle L in front and the many-body 2^L
    behind, on the same linear scale.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s1 as G                                                     # noqa: E402

NAME = 'exponential_wall'
XA, XB, XC = -5.2, -0.6, 4.6
STEP = 0.95


def build():
    F.studio()
    # (a) one electron, four places to be
    xs = [XA + (i - 1.5) * STEP for i in range(4)]
    for i, x in enumerate(xs):
        F.site(f'a_s{i}', (x, 0, 0))
        if i < 3:
            F.bond(f'a_b{i}', (x + 0.3, 0, 0.05), (xs[i + 1] - 0.3, 0, 0.05))
        if i == 1:
            F.ball(f'a_e{i}', (x, 0, 0.36), 0.26)
        else:
            G.ghost_ball(f'a_g{i}', (x, 0, 0.36), 0.26, rgb=(0.62, 0.78, 0.92), alpha=0.11)
    # its Hamiltonian, the 4x4 hopping matrix, standing behind the chain
    tz, ts = 1.2, 0.42
    for i in range(4):
        for j in range(4):
            rgb = (0.30, 0.31, 0.35) if abs(i - j) == 1 else (0.78, 0.79, 0.83)
            t = G.slab(f'a_m{i}{j}', (XA + (j - 1.5) * ts, 1.6, tz + (3 - i) * ts), (0.37, 0.04, 0.37), rgb=rgb)
            t.visible_shadow = False                   # a matrix, not an object: no shadow on the floor
    # the brackets of the matrix
    zb, zt = tz - ts / 2 - 0.04, tz + 3.5 * ts + 0.04
    for sgn in (-1, 1):
        xb = XA + sgn * (2 * ts + 0.06)
        for p0, p1 in (((xb, 1.6, zb), (xb, 1.6, zt)), ((xb, 1.6, zb), (xb - sgn * 0.12, 1.6, zb)),
                       ((xb, 1.6, zt), (xb - sgn * 0.12, 1.6, zt))):
            r = G.rod(f'a_br{sgn}_{p1[0]:.2f}_{p1[2]:.2f}', p0, p1, r=0.018, rgb=(0.16, 0.20, 0.30))
            r.visible_shadow = False
    F.anchor('matA', (XA + 2 * ts + 0.05, 1.6, tz + 1.5 * ts))
    F.anchor('a', (XA - 2.0, 0, 4.6))
    F.anchor('countA', (XA, -0.9, 0))
    # (b) any number of electrons: 2^4 = 16 configurations, one slab each
    confs = sorted(range(16), key=lambda c: (bin(c).count('1'), [-(c >> (3 - k) & 1) for k in range(4)]))
    dz, w, sp, gap = 0.25, 1.75, 0.38, 0.14     # a gap between the groups of equal electron number
    zs = [0.06 + n * dz + gap * bin(c).count('1') for n, c in enumerate(confs)]
    for n, c in enumerate(confs):
        z = zs[n]
        obs = [G.slab(f'b_sl{n}', (XB, 0.15, z), (w, 0.3, 0.03))]
        for k in range(4):
            x = XB + (k - 1.5) * sp
            obs.append(F.site(f'b_s{n}_{k}', (x, -0.05, z + 0.015), r=0.11, h=0.025))
            if c >> (3 - k) & 1:
                obs.append(F.ball(f'b_e{n}_{k}', (x, -0.05, z + 0.12), 0.095))
        if n > 0:                                   # only the base casts a shadow, so none reaches (c)
            for ob in obs:
                ob.visible_shadow = False
    groups = [(0, 0), (1, 4), (5, 10), (11, 14), (15, 15)]
    for N, (lo, hi) in enumerate(groups):
        F.anchor(f'N{N}', (XB + w / 2 + 0.1, 0, (zs[lo] + zs[hi]) / 2 + 0.06))
    F.anchor('b', (XB - 1.6, 0, 4.6))
    F.anchor('countB', (XB, -0.9, 0))
    # (c) the two dimensions against L, on one linear scale
    Ls = list(range(2, 11))
    scale = 4.2 / 2 ** 10
    bx = 0.42
    for j, L in enumerate(Ls):
        x = XC + (j - 4) * 0.5
        G.bar(f'c_mb{L}', (x, 0.55, 0), (bx * 0.9, 0.4, max(2 ** L * scale, 0.03)), F.ELECTRON)
        G.bar(f'c_sp{L}', (x, 0.0, 0), (bx * 0.9, 0.4, max(L * scale, 0.03)), F.BOND)
        if L in (2, 6, 10):
            F.anchor(f'L{L}', (x, -0.35, 0))
    F.anchor('top', (XC + 4 * 0.5 - 0.25, 0.55, 2 ** 10 * scale + 0.05))
    F.anchor('mb', (XC + 1.5 * 0.5, 0.55, 2 ** 9 * scale * 0.95))
    F.anchor('sp', (XC - 4 * 0.5 - 0.3, 0.0, 0.0))
    F.anchor('c', (XC - 2.6, 0, 4.6))
    F.camera((-0.1, 0.3, 2.0), elev=14.0, ortho=14.8, aspect=2.4)


F.main(build, NAME)
