"""Figure 3.1, fig:fock-basis: the local Hilbert spaces and the Fock basis of three spinless orbitals.

(a) The local states of one site: two for a spin-1/2, two for a spinless fermion, four for a
    spinful fermion, so a chain of L sites has 2^L, 2^L and 4^L states.
(b) The eight basis states of three spinless orbitals, grouped by particle number, 1 + 3 + 3 + 1.
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 'fock_basis'
TOP = 0.08                             # height of a site disc
R_SITE = 0.30


def local_states():
    """(a): three groups of single sites, each site holding one local state."""
    groups = [('spin', 2), ('spinless', 2), ('spinful', 4)]
    x, step, gap = -8.6, 0.95, 0.9
    for tag, n in groups:
        xs = [x + i * step for i in range(n)]
        for i, xi in enumerate(xs):
            F.site(f'a_{tag}{i}', (xi, 0, 0), r=R_SITE)
        if tag == 'spin':
            F.arrow('a_spin_up', (xs[0], 0, TOP + 0.45), (0, 0, 1), length=0.75)
            F.arrow('a_spin_dn', (xs[1], 0, TOP + 0.45), (0, 0, -1), length=0.75)
        elif tag == 'spinless':
            F.ball('a_spinless_e', (xs[1], 0, TOP + 0.24), 0.22)
        else:
            F.arrow('a_spinful_up', (xs[1], 0, TOP + 0.45), (0, 0, 1), length=0.75)
            F.arrow('a_spinful_dn', (xs[2], 0, TOP + 0.45), (0, 0, -1), length=0.75)
            F.arrow('a_spinful_2up', (xs[3] - 0.17, 0, TOP + 0.45), (0, 0, 1), length=0.75)
            F.arrow('a_spinful_2dn', (xs[3] + 0.17, 0, TOP + 0.45), (0, 0, -1), length=0.75)
        xc = (xs[0] + xs[-1]) / 2
        F.anchor(f'{tag}', (xc, 0, 2.2))
        F.anchor(f'{tag}N', (xc, -0.6, 0))
        x = xs[-1] + step + gap
    F.anchor('a', (-9.1, 2.9, 1.0))


def trimer(x0, y, occ, tag):
    xs = [x0 + (i - 1) * 0.72 for i in range(3)]
    for i, xi in enumerate(xs):
        F.site(f'{tag}_s{i}', (xi, y, 0), r=0.26)
        if occ[i]:
            F.ball(f'{tag}_e{i}', (xi, y, TOP + 0.21), 0.2)
    F.bond(f'{tag}_b0', (xs[0] + 0.26, y, 0.05), (xs[1] - 0.26, y, 0.05), r=0.03)
    F.bond(f'{tag}_b1', (xs[1] + 0.26, y, 0.05), (xs[2] - 0.26, y, 0.05), r=0.03)


def fock_basis():
    """(b): the 2^3 occupation states, one column of trimers per particle number."""
    x0, dx, dy = 2.3, 2.5, 1.45
    for n in range(4):
        states = [s for s in itertools.product((0, 1), repeat=3) if sum(s) == n]
        states.sort(reverse=True)
        xc = x0 + n * dx
        for k, s in enumerate(states):
            trimer(xc, k * dy, s, f'b{n}_{k}')
        F.anchor(f'N{n}', (xc, -0.55, 0))
    F.anchor('b', (x0 - 1.3, 2.9, 1.0))
    F.anchor('count', (x0 + 3 * dx + 0.95, 2 * dy + 1.0, 1.75))


def build():
    F.studio()
    local_states()
    fock_basis()
    F.camera((0.95, 1.3, 0.5), elev=30.0, ortho=20.3, aspect=4.6)


F.main(build, NAME)
