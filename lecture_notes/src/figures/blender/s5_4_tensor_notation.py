"""Figure 5.4, fig:tensor-notation: tensors as dots with legs, and the matrix product operator.

(a) A scalar, a vector, a matrix and a rank-three tensor as spheres with one leg per index, and
    the contraction of a matrix with a vector over their shared leg, which leaves one free leg.
(b) The matrix product operator (the old fig:mpo-chain): tensors W_i^{s_i s_i'} with two physical
    legs, up for s_i and down for s_i', joined by bonds of dimension chi_W; the end tensors carry
    one bond leg.
MPO tensors are rounded cubes in the session 5 violet, so that in fig:mps-algorithm they stand
apart from the teal tensors of the state.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 'tensor_notation'
Z = 1.0                                # height of the dots and of the operator chain
R = 0.3                                # radius of a dot
LEG = 0.55                             # length of a free leg
TEAL = F.TENSOR
LEGC = (0.30, 0.31, 0.36)              # legs darker than the bonds of a lattice, so they hold on white
VIOLET = (0.36, 0.17, 0.85)            # the session 5 violet, deeper so the tensors hold on paper


def dot(name, x, legs):
    F.ball(name, (x, 0, Z), R, rgb=TEAL, emit=0.0)
    for k, (dx, dz) in enumerate(legs):
        F.leg(f'{name}_l{k}', (x + dx * R, 0, Z + dz * R), (x + dx * (R + LEG), 0, Z + dz * (R + LEG)), rgb=LEGC)


def build():
    F.studio()
    # (a) dots with legs
    xs = [-8.9, -7.6, -5.8, -3.5]
    dot('scalar', xs[0], [])
    dot('vector', xs[1], [(0, -1)])
    dot('matrix', xs[2], [(-1, 0), (1, 0)])
    dot('rank3', xs[3], [(-1, 0), (1, 0), (0, -1)])
    for k, x in enumerate(xs):
        F.anchor(f'n{k}', (x, 0, Z - R - LEG - 0.15))
    # contraction: a matrix joined to a vector over their shared index
    xm, xv = -1.2, 0.3
    F.ball('cm', (xm, 0, Z), R, rgb=TEAL, emit=0.0)
    F.ball('cv', (xv, 0, Z), R, rgb=TEAL, emit=0.0)
    F.leg('cm_free', (xm - R, 0, Z), (xm - R - LEG, 0, Z), rgb=LEGC)
    F.leg('c_shared', (xm + R, 0, Z), (xv - R, 0, Z), rgb=VIOLET)
    F.anchor('sum', ((xm + xv) / 2, 0, Z - R - LEG - 0.15))
    F.anchor('shared', ((xm + xv) / 2, 0, Z + 0.12))
    F.anchor('a', (-9.3, 0, 2.55))
    # (b) the matrix product operator
    L, step, x0 = 4, 1.85, 2.75
    xs = [x0 + k * step for k in range(L)]
    for k, x in enumerate(xs):
        F.tensor(f'W{k}', (x, 0, Z), size=(0.62, 0.62, 0.62), rgb=VIOLET)
        F.leg(f'W{k}_up', (x, 0, Z + 0.31), (x, 0, Z + 0.31 + LEG), rgb=LEGC)
        F.leg(f'W{k}_dn', (x, 0, Z - 0.31), (x, 0, Z - 0.31 - LEG), rgb=LEGC)
        if k < L - 1:
            F.leg(f'W{k}_b', (x + 0.31, 0, Z), (xs[k + 1] - 0.31, 0, Z), r=0.07, rgb=LEGC)
    F.anchor('Wlbl', (xs[1] - 0.33, 0, Z - 0.12))
    F.anchor('sup', (xs[1], 0, Z + 0.31 + LEG))
    F.anchor('sdn', (xs[1], 0, Z - 0.31 - LEG))
    F.anchor('chiW', ((xs[2] + xs[3]) / 2, 0, Z + 0.12))
    F.anchor('b', (x0 - 1.0, 0, 2.55))
    F.camera((0.0, 0.0, 1.05), elev=30.0, ortho=19.4, aspect=4.5)


F.main(build, NAME)
