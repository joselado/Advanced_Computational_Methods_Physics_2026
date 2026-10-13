"""Figure 4.1, fig:mps-chain: the coefficients of a chain as one tensor and as a matrix product state.

(a) The d^L coefficients C(s_1, ..., s_L) as one block with L physical legs.
(b) The same state as a train of small tensors M_n^{s_n}, physical legs down, bond legs of dimension
    chi drawn thicker, the two end tensors with a single bond leg.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 'mps_chain'
XA, XB = -4.6, 3.3                     # panel centers
Z = 1.25                               # height of the tensors
STEP = 1.05                            # leg spacing in (a)
TSTEP = 1.45                           # tensor spacing in (b)
GAP = 0.55                             # extra room for the dots between site 3 and site L-1
LABELS = ['1', '2', '3', 'Lm', 'L']
LEG = (0.20, 0.21, 0.24)               # legs darker than the bonds of a lattice, so they read as indices


def xs_of(x0, step):
    raw = [0, 1, 2, 3, 4]
    xs = [r * step + (GAP if r >= 3 else 0.0) for r in raw]
    c = (xs[0] + xs[-1]) / 2
    return [x0 + x - c for x in xs]


def build():
    F.studio()
    # (a) one block, d^L numbers, with one physical leg per site
    xs = xs_of(XA, STEP)
    w = xs[-1] - xs[0] + 0.9
    F.tensor('a_block', (XA, 0, Z), size=(w, 0.75, 0.75), radius=0.14, rgb=F.TENSOR)
    for i, x in enumerate(xs):
        F.leg(f'a_leg{i}', (x, 0, Z - 0.3), (x, 0, 0.2), r=0.05, rgb=LEG)
        F.anchor('as' + LABELS[i], (x, 0, 0.0))
    F.anchor('adots', ((xs[2] + xs[3]) / 2, 0, 0.0))
    F.anchor('C', (XA, 0, Z + 0.55))
    F.anchor('a', (xs[0] - 0.6, 0, Z + 1.35))
    F.anchor('eq', ((xs[-1] + 0.45 + xs_of(XB, TSTEP)[0] - 0.31) / 2, 0, Z))
    # (b) a train of small tensors joined by thick bond legs
    xs = xs_of(XB, TSTEP)
    for i, x in enumerate(xs):
        F.tensor(f'b_t{i}', (x, 0, Z), size=(0.62, 0.62, 0.62), radius=0.12, rgb=F.TENSOR)
        F.leg(f'b_leg{i}', (x, 0, Z - 0.3), (x, 0, 0.2), r=0.05, rgb=LEG)
        F.anchor('bs' + LABELS[i], (x, 0, 0.0))
        F.anchor('M' + LABELS[i], (x, 0, Z + 0.45))
    for i in range(4):
        if i == 2:                     # the bonds run into the dots, cut short
            F.leg('b_bond2l', (xs[2] + 0.3, 0, Z), (xs[2] + 0.62, 0, Z), r=0.10, rgb=LEG)
            F.leg('b_bond2r', (xs[3] - 0.62, 0, Z), (xs[3] - 0.3, 0, Z), r=0.10, rgb=LEG)
            F.anchor('bonddots', ((xs[2] + xs[3]) / 2, 0, Z))
            continue
        F.leg(f'b_bond{i}', (xs[i] + 0.3, 0, Z), (xs[i + 1] - 0.3, 0, Z), r=0.10, rgb=LEG)
        F.anchor(f'chi{i}', ((xs[i] + xs[i + 1]) / 2, 0, Z - 0.2))
    F.anchor('bdots', ((xs[2] + xs[3]) / 2, 0, 0.0))
    F.anchor('chi3', ((xs[3] + xs[4]) / 2, 0, Z - 0.2))
    F.anchor('b', (xs[0] - 0.6, 0, Z + 1.35))
    F.camera((-0.3, 0.0, 0.95), elev=22.0, ortho=15.9, aspect=4.6)


F.main(build, NAME)
