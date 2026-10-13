"""Figure 2.4, fig:dimerized: the uniform and the dimerized Heisenberg chain.

(a) The uniform chain, every bond the same, no moment on any site.
(b) The dimerized chain: strong bonds J(1+delta) as singlets, weak bonds J(1-delta) as thin rods, and one
    strong bond lit as a triplet (both spins up, an amber glow), the excitation that costs about J(1+delta).
(c) A field h pinning the first spin of each chain and the induced moments <S^z_j> as arrows, length to
    scale: they decay slowly along the uniform chain (back) and within two dimers along the dimerized one
    (front). Exact ground state of L = 12 in the m = 0 sector, h = 0.2 J, delta = 0.5, computed below.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s2 as G                                                     # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'dimerized'
DELTA, H, LC = 0.5, 0.2, 12


def profile(delta):
    L = LC
    states = [s for s in range(2 ** L) if bin(s).count('1') == L // 2]
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    M = np.zeros((n, n))
    for a, s in enumerate(states):
        b = [(s >> (L - 1 - i)) & 1 for i in range(L)]
        M[a, a] += -H * (0.5 - b[0])
        for i in range(L - 1):
            J = 1 + (delta if i % 2 == 0 else -delta)
            M[a, a] += J * (0.25 if b[i] == b[i + 1] else -0.25)
            if b[i] != b[i + 1]:
                M[idx[s ^ (1 << (L - 1 - i)) ^ (1 << (L - 2 - i))], a] += 0.5 * J
    e, v = np.linalg.eigh(M)
    g = v[:, 0] ** 2
    return [sum(g[a] * (0.5 - ((s >> (L - 1 - i)) & 1)) for a, s in enumerate(states)) for i in range(L)]


XA, XB, XC = -8.4, -2.0, 5.5
STEP, L = 0.95, 6
TOP = 0.08


def sites(x0, y, n, step, tag, sphere=True):
    xs = [x0 + (i - (n - 1) / 2) * step for i in range(n)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, y, 0), r=0.26 if step > 0.8 else 0.2)
        if sphere:
            G.spin0(f'{tag}_sp{i}', (x, y, TOP + 0.22), r=0.21)
    return xs


def build():
    F.studio()
    weak = F.mat('weakbond', F.BOND, rough=0.5, spec=0.3)
    # (a) uniform: equal bonds
    xs = sites(XA, 1.2, L, STEP, 'a')
    for i in range(L - 1):
        G.tube(f'a_b{i}', [(xs[i] + 0.2, 1.2, TOP + 0.22), (xs[i + 1] - 0.2, 1.2, TOP + 0.22)], 0.055, weak)
    F.anchor('a', (XA - 2.9, 1.2, 2.4))
    F.anchor('labA', (XA, 0.3, 0))
    # (b) dimerized: singlets on strong bonds, thin weak bonds, one triplet
    xs = sites(XB, 1.2, L, STEP, 'b', sphere=False)
    for i, x in enumerate(xs):
        if i in (2, 3):
            F.arrow(f'b_t{i}', (x, 1.2, TOP + 0.42), (0, 0, 1), length=0.7)
        else:
            G.spin0(f'b_sp{i}', (x, 1.2, TOP + 0.22), r=0.21)
    for i in range(L - 1):
        p0, p1 = (xs[i] + 0.2, 1.2, TOP + 0.3), (xs[i + 1] - 0.2, 1.2, TOP + 0.3)
        if i % 2 == 0 and i != 2:
            G.arc(f'b_sg{i}', p0, p1, 0.3, r=0.07)
        elif i % 2 == 1:
            G.tube(f'b_w{i}', [(xs[i] + 0.2, 1.2, TOP + 0.22), (xs[i + 1] - 0.2, 1.2, TOP + 0.22)], 0.028, weak)
    g = F.glow('glowT', F.ACCENT[1], strength=1.2, alpha=0.30)
    xm = (xs[2] + xs[3]) / 2
    F.obj('b_glow', F.mesh_of('b_glow', [g], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), 1.0, seg=48, rings=24)),
          loc=(xm, 1.2, TOP + 0.42), scale=(0.85, 0.38, 0.5))
    F.anchor('T', (xm, 1.2, TOP + 1.05))
    F.anchor('b', (XB - 2.9, 1.2, 2.4))
    F.anchor('labB', (XB, 0.3, 0))
    # (c) pinned end, uniform chain behind, dimerized in front
    step = 0.6
    for y, d, tag in ((2.2, 0.0, 'cu'), (0.0, DELTA, 'cd')):
        sz = profile(d)
        xs = sites(XC, y, LC, step, tag, sphere=False)
        for i in range(LC - 1):
            if tag == 'cd' and i % 2 == 0:
                G.arc(f'{tag}_sg{i}', (xs[i] + 0.12, y, TOP + 0.05), (xs[i + 1] - 0.12, y, TOP + 0.05), 0.22, r=0.045)
            else:
                F.bond(f'{tag}_b{i}', (xs[i] + 0.2, y, 0.05), (xs[i + 1] - 0.2, y, 0.05),
                       r=0.018 if tag == 'cd' else 0.03)
        for i, x in enumerate(xs):
            ln = 1.25 * abs(sz[i]) / 0.148
            if abs(sz[i]) > 0.02:
                F.arrow(f'{tag}_ar{i}', (x, y, TOP + ln / 2 + 0.02), (0, 0, 1 if sz[i] > 0 else -1), length=ln)
            else:
                G.spin0(f'{tag}_sp{i}', (x, y, TOP + 0.08), r=0.07)
        F.anchor(f'h_{tag}', (xs[0] - 0.3, y, 0.5))
        F.anchor(f'end_{tag}', (xs[-1] + 0.3, y, 0.3))
    F.anchor('c', (XC - 4.2, 2.2, 2.4))
    F.anchor('labC', (XC, -0.9, 0))
    F.camera((-0.45, 1.4, 1.0), elev=30.0, ortho=22.6, aspect=3.6)


F.main(build, NAME)
