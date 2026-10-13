"""Figure 1.3, fig:scf-loop: the self-consistency loop, and why where it starts matters.

(a) The four steps as four stations on a ring, each showing a chain of four sites in that step:
    the guessed moments as arrows, the mean-field Hamiltonian as sites raised and lowered by the
    onsite field -U m_i sigma / 2 (drawn for spin up), the single-particle levels filled up to N,
    and the new moments; the last arrow, back to the start, is the mixing.
(b) The mean-field energy over the order parameter as a surface with two valleys, the
    ferromagnetic one and the lower antiferromagnetic one, and two starting guesses rolling
    into different valleys.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s1 as G                                                     # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'scf_loop'
XA, XB = -3.3, 3.7
DX, YB = 2.2, 3.4                       # half the spacing of the stations along x, depth of the back row
STEP = 0.5                               # spacing of a station's four sites
FLOW = (0.16, 0.20, 0.30)                # the dark course color, for the flow of the loop


def sites(x0, y, tag, z=None):
    xs = [x0 + (i - 1.5) * STEP for i in range(4)]
    for i, x in enumerate(xs):
        zi = 0 if z is None else z[i]
        F.site(f'{tag}_s{i}', (x, y, zi), r=0.17, h=0.05)
    return xs


def energy(x, y):
    g = lambda a: math.exp(-(x - a) ** 2 / 0.45)
    return 1.45 + 0.14 * x * x + 0.04 * y * y - 0.45 * g(-1.25) - 1.05 * g(1.25)


def roll(x, y, n=400, eta=0.01):
    path = [(x, y)]
    for _ in range(n):
        e = 1e-4
        gx = (energy(x + e, y) - energy(x - e, y)) / (2 * e)
        gy = (energy(x, y + e) - energy(x, y - e)) / (2 * e)
        x, y = x - eta * gx / max(1e-9, math.hypot(gx, gy)) * min(1, 6 * math.hypot(gx, gy)), \
            y - eta * gy / max(1e-9, math.hypot(gx, gy)) * min(1, 6 * math.hypot(gx, gy))
        path.append((x, y))
    return path


def build():
    F.studio()
    # (a) the four stations; 1 back left, 2 back right, 3 front right, 4 front left
    c1, c2, c3, c4 = (XA - DX, YB), (XA + DX, YB), (XA + DX, 0.0), (XA - DX, 0.0)
    guess = [0.55, -0.45, 0.5, -0.4]
    new = [0.85, -0.8, 0.8, -0.85]
    xs = sites(*c1, 's1')
    for i, x in enumerate(xs):
        F.arrow(f's1_a{i}', (x, c1[1], 0.05 + abs(guess[i]) / 2), (0, 0, 1 if guess[i] > 0 else -1),
                length=abs(guess[i]))
    lift = [0.2 - 0.18 * (1 if m > 0 else -1) for m in guess]   # spin up sits lower where m_i > 0
    xs = sites(*c2, 's2', z=[0.25 + d for d in lift])
    for i, x in enumerate(xs):
        G.rod(f's2_st{i}', (x, c2[1], 0), (x, c2[1], 0.25 + lift[i]), r=0.02)
    G.slab('s2_ref', (c2[0], c2[1], 0.45), (4 * STEP + 0.1, 0.02, 0.01), rgb=(0.7, 0.72, 0.76))
    for k in range(8):                     # four spinful sites: eight orbitals, four electrons at half filling
        z = 0.12 + 0.16 * k
        G.slab(f's3_l{k}', (c3[0], c3[1], z), (1.4, 0.14, 0.02), rgb=(0.62, 0.64, 0.69))
        if k < 4:
            F.ball(f's3_e{k}', (c3[0], c3[1], z + 0.07), 0.06)
    xs = sites(*c4, 's4')
    for i, x in enumerate(xs):
        F.arrow(f's4_a{i}', (x, c4[1], 0.05 + abs(new[i]) / 2), (0, 0, 1 if new[i] > 0 else -1),
                length=abs(new[i]))
    # the flow of the loop on the floor
    m = 1.25
    z = 0.03
    G.tube('f12', [(c1[0] + m, YB, z), (c2[0] - m, YB, z)], rgb=FLOW)
    G.tube('f23', [(c2[0] + 1.25, YB - 0.4, z), (c3[0] + 1.25, 0.4, z)], rgb=FLOW)
    G.tube('f34', [(c3[0] - m, 0, z), (c4[0] + m, 0, z)], rgb=FLOW)
    G.tube('f41', [(c4[0] - 1.25, 0.4, z), (c1[0] - 1.25, YB - 0.4, z)], rgb=FLOW)
    F.anchor('st1', (c1[0], c1[1], 1.05))
    F.anchor('st2', (c2[0], c2[1], 0.85))
    F.anchor('st3', (c3[0], c3[1] - 0.45, 0))
    F.anchor('st4', (c4[0], c4[1] - 0.45, 0))
    F.anchor('mix', (c4[0] - 1.35, YB / 2, 0))
    F.anchor('N', (c3[0] + 0.8, 0, 0.12 + 0.16 * 3.5))
    F.anchor('a', (XA - DX - 1.3, YB, 2.4))
    # (b) the mean-field energy over the order parameter
    yo = 1.4
    G.surface('E', energy, -2.6, 2.6, -0.9, 0.9, offset=(XB, yo, 0))
    for tag, start, rgb in (('g1', (-0.15, -1.0), F.ELECTRON), ('g2', (0.25, 1.0), F.ELECTRON)):
        pass
    starts = (('g1', (-0.32, -0.35)), ('g2', (0.6, 0.35)))
    for tag, (x, y) in starts:
        path = roll(x, y)
        end = path[-1]
        path = [p for p in path if math.dist(p, end) > 0.12] + [end]   # stop where the ball settles
        pts = [(XB + px, yo + py, energy(px, py) + 0.16) for px, py in path[::8]] + \
              [(XB + end[0], yo + end[1], energy(*end) + 0.16)]
        F.ball(f'{tag}_b', (XB + x, yo + y, energy(x, y) + 0.17), 0.15)
        G.tube(f'{tag}_t', pts[2:], r=0.03, rgb=FLOW)
        end = path[-1]
        print(tag, 'ends at', end)
        F.anchor(tag, (XB + x, yo + y, energy(x, y) + 0.4))
    # the axes: the energy up the left edge, the order parameter along the floor in front
    G.tube('axE', [(XB - 2.75, yo - 0.9, 0.0), (XB - 2.75, yo - 0.9, 2.6)], r=0.022, rgb=FLOW)
    G.tube('axm', [(XB - 2.75, yo - 1.25, 0.02), (XB + 2.9, yo - 1.25, 0.02)], r=0.022, rgb=FLOW)
    F.anchor('Eax', (XB - 2.75, yo - 0.9, 2.65))
    F.anchor('m', (XB + 2.95, yo - 1.25, 0.02))
    F.anchor('FM', (XB - 1.25, yo - 0.9, energy(-1.25, -0.9) - 0.1))
    F.anchor('AFM', (XB + 1.25, yo - 0.9, energy(1.25, -0.9) - 0.1))
    F.anchor('b', (XB - 2.8, YB, 2.4))
    F.camera((0.75, 1.7, 0.75), elev=30.0, ortho=16.0, aspect=2.9)


F.main(build, NAME)
