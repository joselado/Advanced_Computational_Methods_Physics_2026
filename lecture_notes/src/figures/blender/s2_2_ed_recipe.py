"""Figure 2.2, fig:ed-recipe: exact diagonalization of the Heisenberg chain of L = 4 in three steps.

(a) The 2^4 = 16 product states as rows of arrows, in the binary order of a code (state 0 at the back).
(b) The Hamiltonian in that basis as a 16x16 grid of bars, height |H_ij|: the diagonal from S^z S^z,
    the off-diagonal from the flip-flop term, most cells empty. Rows in the order of (a), row 0 at the back.
(c) The spectrum, the sixteen eigenvalues as levels at their height, degenerate levels side by side,
    with the many-body gap E1 - E0 marked in amber. Open chain, J = 1, numbers computed below.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s2 as G                                                     # noqa: E402

NAME = 'ed_recipe'
L = 4
DIAG = F.ACCENT[2]                       # S^z S^z
FLIP = (0.30, 0.36, 0.48)                # flip-flop, a neutral slate
EMPTY = (0.86, 0.87, 0.90)


def bits(s):
    return [(s >> (L - 1 - i)) & 1 for i in range(L)]          # 0 = up, 1 = down


def hamiltonian():
    n = 2 ** L
    M = np.zeros((n, n))
    for s in range(n):
        b = bits(s)
        for i in range(L - 1):
            M[s, s] += 0.25 if b[i] == b[i + 1] else -0.25
            if b[i] != b[i + 1]:
                M[s ^ (1 << (L - 1 - i)) ^ (1 << (L - 2 - i)), s] += 0.5
    return M


XA, XB, XC = -6.3, 1.5, 7.3              # panel centers
PITCH_B = 0.42                           # cell of the matrix
Y0 = 0.0                                 # front row of every panel


def build():
    F.studio()
    M = hamiltonian()
    E = np.linalg.eigvalsh(M)
    # (a) the sixteen product states, four columns by four rows, state 0 at the back left
    dx, cx, cy = 0.36, 1.75, 1.75
    for s in range(16):
        r, c = divmod(s, 4)
        x0 = XA + (c - 1.5) * cx
        y = Y0 + (3 - r) * cy
        for i, b in enumerate(bits(s)):
            x = x0 + (i - 1.5) * dx
            F.site(f'a_s{s}_{i}', (x, y, 0), r=0.12, h=0.04)
            F.arrow(f'a_a{s}_{i}', (x, y, 0.04 + 0.25), (0, 0, -1 if b else 1), length=0.46)
    F.anchor('a', (XA - 3.6, Y0 + 15 * PITCH_B, 1.7))
    F.anchor('labA', (XA, Y0 - 0.75, 0))
    # (b) the matrix as bars, row i at the back for i = 0
    h = 0.45
    for i in range(16):
        for j in range(16):
            x = XB + (j - 7.5) * PITCH_B
            y = Y0 + (15 - i) * PITCH_B
            v = M[i, j]
            if abs(v) < 1e-9:
                G.bar(f'b_e{i}_{j}', (x, y, 0), (0.34, 0.34, 0.02), EMPTY, rough=0.7, emit=0.0)
            else:
                G.bar(f'b_v{i}_{j}', (x, y, 0), (0.30, 0.30, h * abs(v)), DIAG if i == j else FLIP)
    F.anchor('b', (XB - 3.9, Y0 + 15 * PITCH_B, 1.7))
    F.anchor('labB', (XB, Y0 - 0.75, 0))
    F.anchor('diag', (XB + 7.5 * PITCH_B + 0.25, Y0, 0.3))
    # (c) the spectrum, degenerate levels side by side
    s, base = 1.55, 0.35
    groups = []
    for e in E:
        if groups and abs(groups[-1][0] - e) < 1e-6:
            groups[-1][1] += 1
        else:
            groups.append([e, 1])
    w = 0.42
    for k, (e, g) in enumerate(groups):
        z = base + s * (e - E[0])
        for m in range(g):
            x = XC + (m - (g - 1) / 2) * (w + 0.06)
            G.bar(f'c_l{k}_{m}', (x, Y0 + 1.2, z), (w, 0.42, 0.05), F.SITE, rough=0.5, emit=0.0).visible_shadow = False
    z0, z1 = base + 0.05, base + s * (E[1] - E[0])
    xg = XC + 1.6
    ztop = base + s * (E[-1] - E[0]) + 0.3
    F.leg('c_axis', (xg, Y0 + 1.2, 0.0), (xg, Y0 + 1.2, ztop), r=0.035).visible_shadow = False
    G.bar('c_gap', (xg, Y0 + 1.2, z0), (0.12, 0.12, z1 - z0), F.ACCENT[1], emit=0.2).visible_shadow = False
    F.anchor('Eaxis', (xg, Y0 + 1.2, ztop))
    F.anchor('E0', (XC - 0.32, Y0 + 1.2, base + 0.03))
    F.anchor('E1', (XC - 0.8, Y0 + 1.2, z1 + 0.03))
    F.anchor('gap', (xg, Y0 + 1.2, (z0 + z1) / 2))
    F.anchor('c', (XC - 2.3, Y0 + 15 * PITCH_B, 1.7))
    F.anchor('labC', (XC, Y0 - 0.75, 0))
    F.camera((0.3, 2.4, 1.2), elev=30.0, ortho=20.4, aspect=2.75)


F.main(build, NAME)
