"""Figure 1.5, fig:neel-vs-spiral: classical antiferromagnetic order with and without frustration.

(a) The square lattice with collinear Neel order, every bond joining an up and a down spin.
(b) One triangle: two spins antiparallel satisfy their bond, and the third spin cannot be
    antiparallel to both, drawn as two ghost arrows; frustration in its smallest form.
(c) The triangular lattice with the 120 degree order, spins in the plane of the page, all three
    sublattices in one neutral color so that none of them reads as up or down.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s1 as G                                                     # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'neel_vs_spiral'
XA, XB, XC = -5.3, -0.75, 4.1
A = 1.08                               # lattice spacing
LEN = 0.64                             # arrow length
H = 0.52                                # height of the arrow centers


def lattice_bonds(pts, tag, nn):
    k = 0
    for i, p in enumerate(pts):
        for j, q in enumerate(pts):
            if j > i and abs(math.dist(p, q) - nn) < 1e-6:
                d = ((q[0] - p[0]) / nn, (q[1] - p[1]) / nn)
                F.bond(f'{tag}_b{k}', (p[0] + 0.17 * d[0], p[1] + 0.17 * d[1], 0.04),
                       (q[0] - 0.17 * d[0], q[1] - 0.17 * d[1], 0.04), r=0.03)
                k += 1


ELEV = 48.0
UPV = Vector((0, math.sin(math.radians(ELEV)), math.cos(math.radians(ELEV))))   # the camera's up vector


def build():
    F.studio()
    # (a) square lattice, Neel order
    pts = [(XA + (i - 1.5) * A, (j - 1.5) * A + 1.4) for i in range(4) for j in range(4)]
    for n, (x, y) in enumerate(pts):
        i, j = n // 4, n % 4
        F.site(f'a_s{n}', (x, y, 0), r=0.17, h=0.05)
        F.arrow(f'a_a{n}', (x, y, H), (0, 0, 1 if (i + j) % 2 == 0 else -1), length=LEN)
    lattice_bonds(pts, 'a', A)
    F.anchor('a', (XA - 2.2, 3.3, 2.0))
    F.anchor('la', (XA, 1.4 - 1.5 * A - 0.4, 0))
    # (b) one triangle
    s = 1.8
    tri = [(XB - s / 2, 0.6), (XB + s / 2, 0.6), (XB, 0.6 + s * math.sqrt(3) / 2)]
    for n, (x, y) in enumerate(tri):
        F.site(f'b_s{n}', (x, y, 0), r=0.2, h=0.05)
    lattice_bonds(tri, 'b', s)
    F.arrow('b_a0', (tri[0][0], tri[0][1], H), (0, 0, 1), length=LEN)
    F.arrow('b_a1', (tri[1][0], tri[1][1], H), (0, 0, -1), length=LEN)
    F.ghost_arrow('b_g0', (tri[2][0] - 0.32, tri[2][1], H), (0, 0, 1), length=LEN, alpha=0.3)
    F.ghost_arrow('b_g1', (tri[2][0] + 0.32, tri[2][1], H), (0, 0, -1), length=LEN, alpha=0.3)
    F.anchor('q', (tri[2][0] + 0.55, tri[2][1], H + 0.35))
    F.anchor('b', (XB - 1.3, 3.3, 2.0))
    F.anchor('lb', (XB, 0.6 - 0.4, 0))
    # (c) triangular lattice, 120 degree order in the xz plane
    pts, sub = [], []
    for j in range(4):
        for i in range(5):
            x = XC + (i - 2) * A + (j % 2) * A / 2 - A / 4
            y = j * A * math.sqrt(3) / 2 + 0.25
            pts.append((x, y))
            sub.append((i + 2 * (j // 2) * 2 + (j % 2) * 2) % 3)   # three sublattices
    # sublattice index from the oblique coordinates: (i - j_shift) mod 3
    sub = []
    for j in range(4):
        for i in range(5):
            u = i - (j - (j % 2)) // 2           # oblique coordinate along the a2 = (1/2, sqrt3/2) row
            sub.append((u + 2 * j) % 3)
    for n, (x, y) in enumerate(pts):
        F.site(f'c_s{n}', (x, y, 0), r=0.17, h=0.05)
        th = math.radians(90 + 120 * sub[n])
        # the spin plane faces the camera, spanned by x and the camera's up vector, and the tail of
        # every arrow sits right above its site
        d = math.cos(th) * Vector((1, 0, 0)) + math.sin(th) * UPV
        tail = Vector((x, y, 0.27))
        G.sz_arrow(f'c_a{n}', tail + d * LEN / 2, d, length=LEN, neutral=True)
    lattice_bonds(pts, 'c', A)
    F.anchor('c', (XC - 2.6, 3.3, 2.0))
    F.anchor('lc', (XC, 0.25 - 0.4, 0))
    F.camera((-0.05, 1.7, 0.5), elev=ELEV, ortho=15.4, aspect=2.7)


F.main(build, NAME)
