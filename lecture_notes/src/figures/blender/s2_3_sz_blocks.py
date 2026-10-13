"""Figure 2.3, fig:sz-blocks: the conserved S^z_tot of the Heisenberg chain of L = 6.

(a) The 64x64 matrix as a pale plate with one raised block per magnetization sector, to scale
    (1, 6, 15, 20, 15, 6, 1), m = +3 at the back left; each block in the color of its sector.
(b) The lowest level of each sector against the Zeeman field B, E_m(B) = E_m(0) - B m, as lines in the
    same colors on a card: the fan, with the ground-state crossings marked by dark beads.
(c) The magnetization staircase of the ground state, m against B, with the chain standing on each plateau:
    spheres with no moment on m = 0, then arrows whose length is the average moment m/L per site.
Open chain, J = 1, numbers computed below by exact diagonalization.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s2 as G                                                     # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'sz_blocks'
L = 6


def sector_minima():
    n = 2 ** L
    M = np.zeros((n, n))
    for s in range(n):
        b = [(s >> (L - 1 - i)) & 1 for i in range(L)]
        for i in range(L - 1):
            M[s, s] += 0.25 if b[i] == b[i + 1] else -0.25
            if b[i] != b[i + 1]:
                M[s ^ (1 << (L - 1 - i)) ^ (1 << (L - 2 - i)), s] += 0.5
    mz = np.array([L / 2 - bin(s).count('1') for s in range(n)])
    return {m: np.linalg.eigvalsh(M[np.ix_(mz == m, mz == m)])[0] for m in range(-3, 4)}


def mcolor(m):
    """The color of sector m: the up series for m > 0, the down series for m < 0, gray for m = 0."""
    if m == 0:
        return (0.30, 0.31, 0.36)
    t = abs(m) / 3.0
    a, b = (F.UP_TIP, F.UP_TAIL) if m > 0 else (F.DOWN_TIP, F.DOWN_TAIL)
    return tuple(a[k] + (b[k] - a[k]) * (t - 1 / 3) * 1.5 for k in range(3))


XA, XB, XC = -7.0, 1.2, 9.5
BMAX, SB = 2.3, 2.3                       # field range in units of J and its length per J


def build():
    F.studio()
    Em = sector_minima()
    # (a) the blocks
    p = 0.1
    F.obj('a_plate', F.mesh_of('a_plate', [F.mat('plate', (0.86, 0.87, 0.90), rough=0.7, spec=0.2)],
                               lambda bm: F.bm_rounded_box(bm, Vector((0, 0, 0)), (64 * p, 64 * p, 0.03), 0.01)),
          loc=(XA, 32 * p, 0.015))
    k0 = 0
    for m in range(3, -4, -1):
        d = math.comb(L, L // 2 + m)
        cx = XA - 32 * p + (k0 + d / 2) * p
        cy = 64 * p - (k0 + d / 2) * p
        G.bar(f'a_blk{m}', (cx, cy, 0.03), (d * p - 0.02, d * p - 0.02, 0.28), mcolor(m))
        F.anchor(f'dim{m}', (cx - d * p / 2 - 0.06, cy - d * p / 2 + 0.05, 0.03))
        k0 += d
    F.anchor('a', (XA - 3.2, 64 * p, 1.9))
    F.anchor('labA', (XA, -1.2, 0))
    # (b) the fan on a card standing at y = YB
    YB, ZE, SE, E_lo, E_hi = 2.6, 0.3, 0.62, -6.0, 0.6
    F.obj('b_card', F.mesh_of('b_card', [F.mat('card', (0.97, 0.97, 0.98), rough=0.8, spec=0.1)],
                              lambda bm: F.bm_rounded_box(bm, Vector((0, 0, 0)), (BMAX * SB + 1.6, 0.06, 4.6), 0.02)),
          loc=(XB + 0.55, YB + 0.1, 2.3)).visible_shadow = False
    x0 = XB - BMAX * SB / 2

    def zE(E):
        return ZE + (E - E_lo) * SE

    for m in range(-1, 4):
        pts = []
        for B in np.linspace(0, BMAX, 47):
            E = Em[m] - B * m
            if E_lo <= E <= E_hi:
                pts.append((x0 + B * SB, YB, zE(E)))
        if len(pts) > 1:
            G.tube(f'b_line{m}', pts, 0.045, F.mat(f'line{m}', mcolor(m), rough=0.4, emit=0.1, spec=0.4))
        Bend = min(BMAX, (E_hi - Em[m]) / -m) if m < 0 else BMAX
        F.anchor(f'm{m}', (x0 + Bend * SB, YB, zE(Em[m] - Bend * m)))
    F.leg('b_axisE', (x0, YB, zE(E_lo) - 0.1), (x0, YB, zE(E_hi) + 0.1), r=0.025)
    F.leg('b_axisB', (x0, YB, zE(E_lo) - 0.1), (x0 + BMAX * SB + 0.1, YB, zE(E_lo) - 0.1), r=0.025)
    gs = []
    for m in range(0, 3):
        Bc = Em[m + 1] - Em[m]                     # E_m - B m = E_{m+1} - B (m+1)
        gs.append(Bc)
        F.ball(f'b_x{m}', (x0 + Bc * SB, YB - 0.05, zE(Em[m] - Bc * m)), 0.09, rgb=F.SITE, emit=0.0)
    F.anchor('b', (XB - 4.6, YB, 4.6))
    F.anchor('Eb', (x0, YB, zE(E_hi) + 0.1))
    F.anchor('Bb', (x0 + BMAX * SB + 0.1, YB, zE(E_lo) - 0.1))
    F.anchor('labB', (XB, -1.2, 0))
    # (c) the staircase, plateaus between the crossing fields of (b)
    edges = [0.0] + gs + [BMAX]
    xc0 = XC - BMAX * SB / 2
    H, D = 0.62, 3.4
    for m in range(4):
        b0, b1 = edges[m], edges[m + 1]
        w = (b1 - b0) * SB
        G.bar(f'c_step{m}', (xc0 + (b0 + b1) / 2 * SB, 1.2, 0.0), (w - 0.03, D, 0.06 + H * m), (0.80, 0.81, 0.85),
              rough=0.6, emit=0.0)
        top = 0.06 + H * m
        for k in range(L):
            r, c = divmod(k, 3)
            x = xc0 + (b0 + b1) / 2 * SB + (c - 1) * min(0.3, w / 3.4)
            y = 1.2 + (r - 0.5) * 2.2
            if m == 0:
                G.spin0(f'c_sp{m}_{k}', (x, y, top + 0.13), r=0.11)
            else:
                ln = 0.4 * m
                F.arrow(f'c_ar{m}_{k}', (x, y, top + ln / 2 + 0.01), (0, 0, 1), length=ln)
        F.anchor(f'pl{m}', (xc0 + (b0 + b1) / 2 * SB, 1.2 - D / 2, top - 0.04))
    F.anchor('c', (XC - 2.9, YB, 4.6))
    F.anchor('labC', (XC, -1.2, 0))
    F.camera((1.0, 2.0, 1.7), elev=30.0, ortho=24.0, aspect=2.8)


F.main(build, NAME)
