"""Figure 2.1, fig:neel-pair: the two ends of the XXZ chain.

(a) The Ising end: the two Neel product states, one behind the other, a finite moment on every site.
(b) The Heisenberg end: no moment on any site, spheres joined by singlet bonds, drawn in the two dimer
    coverings, one behind the other, between which the singlets resonate.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s2 as G                                                     # noqa: E402

NAME = 'neel_pair'
XA, XB = -4.7, 4.3
STEP, L = 1.1, 6
Y_BACK = 2.6
TOP = 0.08


def chain(x0, y, tag, bonds=True):
    xs = [x0 + (i - (L - 1) / 2) * STEP for i in range(L)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, y, 0))
        if bonds and i < L - 1:
            F.bond(f'{tag}_b{i}', (x + 0.3, y, 0.05), (xs[i + 1] - 0.3, y, 0.05))
    return xs


def build():
    F.studio()
    # (a) the two Neel states
    for y, s0, tag in ((0.0, 1, 'a0'), (Y_BACK, -1, 'a1')):
        xs = chain(XA, y, tag)
        for i, x in enumerate(xs):
            F.arrow(f'{tag}_arr{i}', (x, y, TOP + 0.5), (0, 0, s0 if i % 2 == 0 else -s0))
    F.anchor('a', (XA - 3.25, Y_BACK, 1.75))
    F.anchor('ketA', (XA + 3.15, 0, 0.5))
    F.anchor('ketB', (XA + 3.15, Y_BACK, 0.5))
    # (b) the Heisenberg end: spheres, singlets on the two dimer coverings
    for y, first, tag in ((0.0, 0, 'b0'), (Y_BACK, 1, 'b1')):
        xs = chain(XB, y, tag, bonds=False)
        for i, x in enumerate(xs):
            G.spin0(f'{tag}_sp{i}', (x, y, TOP + 0.26))
        for i in range(first, L - 1, 2):
            G.arc(f'{tag}_sg{i}', (xs[i] + 0.12, y, TOP + 0.42), (xs[i + 1] - 0.12, y, TOP + 0.42), 0.35)
        if first == 1:                      # the second covering pairs the two ends, as on a ring
            G.arc(f'{tag}_sgends', (xs[-1] - 0.05, y + 0.12, TOP + 0.45), (xs[0] + 0.05, y + 0.12, TOP + 0.45), 1.05)
    F.anchor('b', (XB - 3.25, Y_BACK, 1.75))
    F.anchor('plus', (XB - 3.15, Y_BACK / 2, 0.35))
    F.anchor('chainA', (XA, -0.9, 0))
    F.anchor('chainB', (XB, -0.9, 0))
    F.camera((-0.2, 1.3, 0.55), elev=30.0, ortho=16.4, aspect=3.3)


F.main(build, NAME)
