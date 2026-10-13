"""Figure 1.4, fig:superexchange: where J = 4t^2/U comes from, on the half-filled Hubbard dimer.

(a) Parallel spins: the hop is blocked by Pauli exclusion, an arc that stops at a barrier.
(b) Antiparallel spins: the hop goes up to the virtual doubly occupied state, on a level raised
    by U, and comes back down onto the exchanged configuration.
(c) The six two-electron states of the dimer as levels: four with one electron per site at
    zero energy, the low-energy manifold, and two doubly occupied at U.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s1 as G                                                     # noqa: E402

NAME = 'superexchange'
XA, XB, XC = -6.0, -1.7, 4.3
D = 0.42                               # half the distance between the two sites of a dimer
U = 1.5                                # height of the doubly occupied level
AL = 0.5                               # arrow length
FLOW = (0.16, 0.20, 0.30)
RAISED = (1.0, 0.66, 0.32)               # a level raised by U, in a pale tint of the cost amber


def dimer(x0, y, z, spins, tag, plate=True, D=D):
    """Two sites on a plate at height z; spins[i] lists the arrows on site i (+1 up, -1 down)."""
    if plate:
        if z > 0.05:
            G.slab(f'{tag}_ped', (x0, y, z / 2), (2 * D + 0.5, 0.62, z), rgb=RAISED, radius=0.04)
        else:
            G.slab(f'{tag}_pl', (x0, y, 0.015), (2 * D + 0.5, 0.62, 0.03), rgb=G.SLAB)
    top = max(z, 0.03)
    for i, sp in enumerate(spins):
        x = x0 + (2 * i - 1) * D
        F.site(f'{tag}_s{i}', (x, y, top), r=0.17, h=0.04)
        off = [0.0] if len(sp) == 1 else [-0.09, 0.09]
        for k, s in enumerate(sp):
            F.arrow(f'{tag}_a{i}{k}', (x + off[k], y, top + 0.04 + AL / 2), (0, 0, s), length=AL)
    F.bond(f'{tag}_b', (x0 - D + 0.17, y, top + 0.02), (x0 + D - 0.17, y, top + 0.02), r=0.02)


def build():
    F.studio()
    # (a) parallel spins: the hop is blocked
    dimer(XA, 0, 0, [(1,), (1,)], 'a')
    G.arc('a_hop', (XA - D, 0, 0.75), (XA + D - 0.12, 0, 0.75), 0.45, r=0.022, rgb=FLOW, frac=0.62, head=False)
    bar = G.slab('a_bar', (XA + 0.12, 0, 1.05), (0.05, 0.4, 0.5), rgb=FLOW)
    F.anchor('pauli', (XA + 0.25, 0, 1.3))
    F.anchor('E0a', (XA, -0.4, 0))
    F.anchor('a', (XA - 1.2, 0, 2.15))
    # (b) antiparallel spins: up to the virtual state at U and down onto the exchanged one
    xl, xm, xr = XB - 2.0, XB, XB + 2.0
    dimer(xl, 0, 0, [(1,), (-1,)], 'bl')
    dimer(xm, 0, U, [(1, -1), ()], 'bm')
    dimer(xr, 0, 0, [(-1,), (1,)], 'br')
    G.tube('b_up', [(xl + 0.55, 0, 0.75), (xm - 0.75, 0, U + 0.35)], r=0.022, rgb=FLOW)
    G.tube('b_dn', [(xm + 0.75, 0, U + 0.35), (xr - 0.55, 0, 0.75)], r=0.022, rgb=FLOW)
    F.anchor('t1', ((xl + xm) / 2 - 0.15, 0, (U + 1.1) / 2 + 0.2))
    F.anchor('t2', ((xr + xm) / 2 + 0.15, 0, (U + 1.1) / 2 + 0.2))
    F.anchor('Ub', (xm + 0.7, 0, U / 2))
    F.anchor('E0l', (xl, -0.4, 0))
    F.anchor('E0r', (xr, -0.4, 0))
    F.anchor('b', (XB - 3.0, 0, 2.15))
    # (c) the six states of the dimer as levels
    low = [[(1,), (-1,)], [(-1,), (1,)], [(1,), (1,)], [(-1,), (-1,)]]
    for k, sp in enumerate(low):
        dimer(XC + (k - 1.5) * 1.32, -0.4, 0, sp, f'c_l{k}', D=0.33)
    high = [[(1, -1), ()], [(), (1, -1)]]
    for k, sp in enumerate(high):
        dimer(XC + (k - 0.5) * 1.6, 3.0, U, sp, f'c_h{k}', D=0.33)
    F.anchor('E0c', (XC, -0.8, 0))
    F.anchor('Uc', (XC + 1.35, 3.0, U / 2 + 0.3))
    F.anchor('c', (XC - 2.85, 0, 2.15))
    F.camera((-0.2, 0.6, 1.3), elev=20.0, ortho=14.8, aspect=3.35)


F.main(build, NAME)
