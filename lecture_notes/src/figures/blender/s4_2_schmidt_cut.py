"""Figure 4.2, fig:schmidt-cut: what crosses a cut, from two spins to a matrix product state.

(a) A product state: a cut between two spins with nothing crossing it; the singlet: two spins with
    no moment joined by one strand across the cut.
(b) A matrix product state cut at bond n: every bond is a single rod except the one at the cut,
    opened into its chi_n strands, the values of the index alpha.
(c) What a cut severs: one bond of a chain, a whole line of bonds of a square lattice, and strands
    everywhere for a random state, the volume law.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s4 as G                                                     # noqa: E402

NAME = 'schmidt_cut'
YB = 5.0                               # the back row, (a) and (b)
Z = 1.0                                # height of the tensors
TOP = 0.08


def two_spins(x0, tag, singlet):
    xs = [x0 - 0.65, x0 + 0.65]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, YB, 0))
    if singlet:
        for i, x in enumerate(xs):
            G.pale_spin(f'{tag}_p{i}', (x, YB, TOP + 0.3))
        G.arc(f'{tag}_sing', (xs[0] + 0.2, YB, TOP + 0.35), (xs[1] - 0.2, YB, TOP + 0.35), 0.18, r=0.05)
    else:
        F.arrow(f'{tag}_u', (xs[0], YB, TOP + 0.45), (0, 0, 1), length=0.75)
        F.arrow(f'{tag}_d', (xs[1], YB, TOP + 0.45), (0, 0, -1), length=0.75)
    G.pane(f'{tag}_cut', (x0, YB, 0), w=0.8, h=1.3, turn=30.0)
    return xs


def chain_sites(x0, y, n, step, tag, cut_after, sever=True):
    xs = [x0 + (i - (n - 1) / 2) * step for i in range(n)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, y, 0), r=0.2, h=0.06)
        if i < n - 1:
            if sever and i == cut_after:
                G.strand(f'{tag}_b{i}', [(x + 0.2, y, 0.05), (xs[i + 1] - 0.2, y, 0.05)], r=0.06)
            else:
                F.bond(f'{tag}_b{i}', (x + 0.2, y, 0.04), (xs[i + 1] - 0.2, y, 0.04))
    return xs


def build():
    F.studio()
    # (a) product state and singlet
    two_spins(-7.3, 'ap', singlet=False)
    two_spins(-4.0, 'as', singlet=True)
    F.anchor('a', (-9.05, YB, 2.75))
    F.anchor('prod', (-7.3, YB, 1.45))
    F.anchor('sing', (-4.0, YB, 1.45))
    # (b) a matrix product state cut at bond n
    step, x0, n_cut = 1.25, 2.1, 2
    xs = [x0 + (i - 2.5) * step + (0.35 if i > n_cut else -0.35) for i in range(6)]
    for i, x in enumerate(xs):
        F.tensor(f'b_t{i}', (x, YB, Z), size=(0.56, 0.56, 0.56), radius=0.11, rgb=G.TEAL)
        F.leg(f'b_leg{i}', (x, YB, Z - 0.28), (x, YB, 0.22), r=0.045, rgb=G.LEG)
        if i < 5 and i != n_cut:
            F.leg(f'b_bond{i}', (x + 0.28, YB, Z), (xs[i + 1] - 0.28, YB, Z), r=0.085, rgb=G.LEG)
    xa, xb = xs[n_cut] + 0.28, xs[n_cut + 1] - 0.28
    for k, (dy, dz) in enumerate([(0.0, 0.42), (0.0, 0.14), (0.0, -0.14), (0.0, -0.42)]):
        G.strand(f'b_alpha{k}', [(xa, YB, Z), ((xa + xb) / 2, YB + dy, Z + dz), (xb, YB, Z)], r=0.035)
    xc = (xs[n_cut] + xs[n_cut + 1]) / 2
    G.pane('b_cut', (xc, YB, 0.3), w=1.0, h=1.5, turn=30.0)
    F.anchor('b', (xs[0] - 0.7, YB, 2.75))
    F.anchor('blockA', ((xs[0] + xs[n_cut]) / 2, YB, Z + 0.55))
    F.anchor('blockB', ((xs[n_cut + 1] + xs[-1]) / 2, YB, Z + 0.55))
    F.anchor('chin', (xc, YB, Z + 1.05))
    F.anchor('sn', (xs[n_cut], YB, 0.0))
    F.anchor('sn1', (xs[n_cut + 1], YB, 0.0))
    F.anchor('s1', (xs[0], YB, 0.0))
    F.anchor('sL', (xs[-1], YB, 0.0))
    # (c) a chain, a square lattice and a random state, each cut once
    xs = chain_sites(-6.3, 0, 6, 0.75, 'c1', 2)
    G.pane('c1_cut', ((xs[2] + xs[3]) / 2, 0, 0), w=0.6, h=1.0, turn=30.0)
    F.anchor('c', (-8.75, 0, 1.25))
    F.anchor('cchain', (-6.3, -1.75, 0))
    sp, n = 0.62, 5
    for j in range(n):
        y = (j - (n - 1) / 2) * sp
        chain_sites(-0.2, y, n, sp, f'c2r{j}', 1)
    for i in range(n):
        x = -0.2 + (i - (n - 1) / 2) * sp
        for j in range(n - 1):
            y0, y1 = (j - (n - 1) / 2) * sp, (j + 1 - (n - 1) / 2) * sp
            F.bond(f'c2c{i}_{j}', (x, y0 + 0.2, 0.04), (x, y1 - 0.2, 0.04))
    G.pane('c2_cut', (-0.2 - sp / 2, 0, 0), w=3.3, h=0.55, turn=10.0)
    F.anchor('csquare', (-0.2, -1.75, 0))
    xs = chain_sites(5.3, 0, 6, 0.75, 'c3', 2, sever=False)
    pairs = [(0, 3), (1, 4), (2, 5), (0, 5), (1, 3), (2, 4), (0, 2), (3, 5), (1, 5), (0, 4)]
    for k, (i, j) in enumerate(pairs):
        G.arc(f'c3_arc{k}', (xs[i], 0, 0.1), (xs[j], 0, 0.1), 0.12 + 0.11 * (j - i), r=0.022)
    G.pane('c3_cut', ((xs[2] + xs[3]) / 2, 0, 0), w=0.6, h=1.4, turn=30.0)
    F.anchor('crandom', (5.3, -1.75, 0))
    F.camera((-0.75, 2.3, 0.75), elev=30.0, ortho=17.0, aspect=2.35)


F.main(build, NAME)
