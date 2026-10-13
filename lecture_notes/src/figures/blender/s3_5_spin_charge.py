"""Figure 3.5, fig:spin-charge: spin-charge separation in the half-filled Hubbard chain.

(a) Behind, an electron removed from the antiferromagnetic chain; in front, the same chain after
    the hole has hopped three times to the right: an empty site without spin, the holon, and two
    parallel neighbors left where the hole started, the spinon.
(b) The two energy scales at U = 10t as two towers of very different height: an added electron,
    a doublon, costing about U/2 (what S_c of Eq. (dynamical) reaches), and a spin flip costing
    about J = 4t^2/U = 0.4t (what S_s reaches).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s3 as G                                                     # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'spin_charge'
XA, XB = -3.6, 4.7
STEP, L = 0.95, 10
Y_BACK = 3.0
TOP = 0.08
U, T = 10.0, 1.0
SCALE = 0.4                            # tower height per t


def spins(pattern, y, tag):
    """A chain with one arrow per site, 1 up, -1 down, 0 an empty site with a ghost electron."""
    xs = G.chain_sites(XA, y, L, STEP, tag, r=0.3)
    for i, (x, s) in enumerate(zip(xs, pattern)):
        if s == 0:
            F.obj(f'{tag}_hole{i}', F.mesh_of(f'{tag}_hole{i}', [F.ghost('hole', F.ELECTRON, 0.18)],
                                             lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), 0.22)),
                  loc=(x, y, TOP + 0.24))
        else:
            F.arrow(f'{tag}_arr{i}', (x, y, TOP + 0.42), (0, 0, s), length=0.72)
    return xs


def tower(name, x, height, top_fn):
    m = F.mat('tower', F.ACCENT[1], rough=0.5, emit=0.05, spec=0.3)
    F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_rounded_box(bm, Vector((0, 0, 0)), (1.9, 0.4, height), 0.04)),
          loc=(x, 0, height / 2))
    top_fn(x, height)


def build():
    F.studio()
    # (a) the electron removed at site 4, then the hole hops three times to the right
    start = [1 if i % 2 == 0 else -1 for i in range(L)]
    start[4] = 0
    later = list(start)
    for k in range(4, 7):                           # the electron on k + 1 hops onto the hole at k
        later[k], later[k + 1] = later[k + 1], 0
    xb = spins(start, Y_BACK, 'p')
    xf = spins(later, 0, 'q')
    for nm, x, w, m in (('pad_spinon', (xf[3] + xf[4]) / 2, STEP + 0.85, F.ghost('pad_gray', (0.45, 0.47, 0.52), 0.3)),
                        ('pad_holon', xf[7], 0.85, F.ghost('pad', F.ACCENT[3], 0.3))):
        F.obj(nm, F.mesh_of(nm, [m], lambda bm, w=w: F.bm_rounded_box(bm, Vector((0, 0, 0)), (w, 0.85, 0.03), 0.012)),
              loc=(x, 0, 0.015))
    F.anchor('removed', (xb[4], Y_BACK, TOP + 0.9))
    F.anchor('holon', (xf[7], -0.75, 0))
    F.anchor('spinon', ((xf[3] + xf[4]) / 2, -0.75, 0))
    F.anchor('a', (XA - 4.55, Y_BACK, 2.3))
    print('back ', start, '\nfront', later)

    # (b) the two scales as towers: an added electron, a doublon at U/2, and a spin flip at J = 4t^2/U
    def doublon(x, h):
        F.site('dbl_s', (x, 0, h), r=0.3)
        F.arrow('dbl_up', (x - 0.17, 0, h + TOP + 0.42), (0, 0, 1), length=0.72)
        F.arrow('dbl_dn', (x + 0.17, 0, h + TOP + 0.42), (0, 0, -1), length=0.72)

    def flip(x, h):
        for k, xx in enumerate((x - 0.5, x + 0.5)):
            F.site(f'flip_s{k}', (xx, 0, h), r=0.3)
            F.arrow(f'flip_a{k}', (xx, 0, h + TOP + 0.42), (0, 0, 1), length=0.72)
    hU, hJ = SCALE * U / 2, SCALE * 4 * T ** 2 / U
    tower('towerU', XB - 1.5, hU, doublon)
    tower('towerJ', XB + 2.0, hJ, flip)
    F.anchor('U', (XB - 1.5, -0.6, 0))
    F.anchor('J', (XB + 2.0, -0.6, 0))
    F.anchor('b', (XB - 3.3, Y_BACK, 2.3))
    F.camera((0.6, 1.4, 1.2), elev=30.0, ortho=17.6, aspect=2.75)


F.main(build, NAME)
