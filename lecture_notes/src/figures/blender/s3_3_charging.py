"""Figure 3.3, fig:charging: the chemical potential as a gate, and the staircase of N against mu.

(a) A ring of eight sites standing on a gate plate, the knob mu, holding N = 4 electrons.
(b) The ground-state N against mu for that ring at V = 4t, computed exactly below: each plateau
    spans the window of Eq. (addwindow), and the widest one, at half filling, is the charge gap.
"""
import itertools
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s3 as G                                                     # noqa: E402

NAME = 'charging'
L, V, T = 8, 4.0, 1.0                  # ring of eight, V = 4t, Eq. (cdw3) with periodic boundaries
TOP = 0.08


def ground_energies():
    """E(N), the lowest eigenvalue of Eq. (cdw3) in each particle-number sector of the ring."""
    E = []
    for N in range(L + 1):
        st = [s for s in range(2 ** L) if bin(s).count('1') == N]
        idx = {s: i for i, s in enumerate(st)}
        H = np.zeros((len(st), len(st)))
        for k, s in enumerate(st):
            for i in range(L):
                j = (i + 1) % L
                ni, nj = (s >> i) & 1, (s >> j) & 1
                H[k, k] += V * (ni - 0.5) * (nj - 0.5)
                if ni != nj:
                    lo, hi = min(i, j), max(i, j)
                    between = s & (((1 << hi) - 1) ^ ((1 << (lo + 1)) - 1))
                    H[idx[s ^ (1 << i) ^ (1 << j)], k] += -T * (-1) ** bin(between).count('1')
        E.append(np.linalg.eigvalsh(H)[0])
    return E


def gate_ring(x0):
    """(a): the ring on its gate plate."""
    F.obj('gate', F.mesh_of('gate', [F.mat('gate', (0.62, 0.65, 0.72), rough=0.35, spec=0.5)],
                            lambda bm: F.bm_rounded_box(bm, F.Vector((0, 0, 0)), (4.9, 4.1, 0.22), 0.08)),
          loc=(x0, 1.2, 0.11))
    R, z = 1.65, 0.22
    pts = [(x0 + R * math.cos(2 * math.pi * k / L + math.pi / 8), 1.2 + R * math.sin(2 * math.pi * k / L + math.pi / 8))
           for k in range(L)]
    for k, (x, y) in enumerate(pts):
        F.site(f'r_s{k}', (x, y, z), r=0.27)
        x2, y2 = pts[(k + 1) % L]
        d = F.Vector((x2 - x, y2 - y, 0)).normalized() * 0.27
        F.bond(f'r_b{k}', (x + d.x, y + d.y, z + 0.05), (x2 - d.x, y2 - d.y, z + 0.05))
        if k % 2 == 0:
            F.ball(f'r_e{k}', (x, y, z + 0.08 + 0.21), 0.21)
    F.anchor('a', (x0 - 2.8, 3.2, 1.6))
    F.anchor('gate', (x0, -1.0, 0.0))
    F.anchor('ringN', (x0, 3.3, 0.6))


def staircase(x0, E):
    """(b): one block per plateau, from mu = E(N) - E(N-1) to E(N+1) - E(N), of height N."""
    mus = [E[N + 1] - E[N] for N in range(L)]
    sx, sz, depth = 0.62, 0.36, 0.5                # world units per t, per electron, block depth
    lo, hi = mus[0] - 2.5, mus[-1] + 1.3
    edges = [lo] + mus + [hi]
    for N in range(1, L + 1):
        a, b = edges[N], edges[N + 1]
        rgb = F.ACCENT[1] if N == L // 2 else F.ACCENT[3]
        m = F.mat('step_%d' % (N == L // 2), rgb, rough=0.45, emit=0.06, spec=0.4)
        F.obj(f'step{N}', F.mesh_of(f'step{N}', [m], lambda bm, a=a, b=b, N=N: F.bm_rounded_box(
            bm, F.Vector((0, 0, 0)), ((b - a) * sx - 0.1, depth, N * sz), 0.03)),
            loc=(x0 + (a + b) / 2 * sx, 0, N * sz / 2))
    F.leg('mu_axis', (x0 + lo * sx, -depth / 2 - 0.05, 0.02), (x0 + hi * sx + 0.4, -depth / 2 - 0.05, 0.02), r=0.025)
    F.leg('N_axis', (x0 + lo * sx, -depth / 2 - 0.05, 0.0), (x0 + lo * sx, -depth / 2 - 0.05, L * sz + 0.5), r=0.025)
    F.anchor('muaxis', (x0 + hi * sx + 0.45, -depth / 2 - 0.05, 0.02))
    F.anchor('Naxis', (x0 + lo * sx, -depth / 2 - 0.05, L * sz + 0.5))
    a, b = mus[3], mus[4]
    F.anchor('gapL', (x0 + a * sx, -depth / 2, 0))
    F.anchor('gapR', (x0 + b * sx, -depth / 2, 0))
    F.anchor('half', (x0 + (a + b) / 2 * sx, 0, 4 * sz + 0.02))
    F.anchor('b', (x0 + lo * sx - 1.5, 3.2, 1.6))
    F.anchor('Nzero', (x0 + (lo + mus[0]) / 2 * sx, 0, 0.0))
    for N in (0, 4, 8):
        F.anchor(f'N{N}', (x0 + lo * sx, -depth / 2 - 0.05, N * sz))
    print('plateau widths in t:', [round(mus[N] - mus[N - 1], 3) for N in range(1, L)])


def build():
    F.studio()
    gate_ring(-5.4)
    staircase(3.2, ground_energies())
    F.camera((0.3, 1.0, 1.0), elev=30.0, ortho=17.8, aspect=3.0)


F.main(build, NAME)
