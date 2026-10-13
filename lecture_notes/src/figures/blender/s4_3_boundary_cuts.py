"""Figure 4.3, fig:boundary-cuts: the same block A on an open chain and on a ring.

(a) The open chain: block A at the left end borders the rest at one point, one cut, one severed bond.
(b) The ring: the same block borders the rest at both of its ends, two cuts, two severed bonds.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402
import figlib_s4 as G                                                     # noqa: E402
from mathutils import Vector                                              # noqa: E402

NAME = 'boundary_cuts'
L, NA = 10, 3                          # sites in the chain and in the block A
TOP = 0.06
R_SPIN = 0.2


def spin_site(tag, p):
    F.site(tag + '_s', p, r=0.26, h=TOP)
    G.pale_spin(tag + '_p', (p[0], p[1], TOP + R_SPIN), r=R_SPIN)


def link(tag, p0, p1, severed):
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0).normalized() * 0.27
    a, b = p0 + d + Vector((0, 0, 0.12)), p1 - d + Vector((0, 0, 0.12))
    if severed:
        G.strand(tag, [a, b], r=0.06)
    else:
        F.bond(tag, a, b, r=0.04)


def block(tag, pts):
    """One translucent teal tray under the sites of block A: a flattened tube through the sites,
    run a little past the end sites so that they sit inside it."""
    pts = [Vector(p) for p in pts]
    head = pts[0] + (pts[0] - pts[1]).normalized() * 0.12
    tail = pts[-1] + (pts[-1] - pts[-2]).normalized() * 0.12
    path = [head] + pts + [tail]
    fine = []
    for p, q in zip(path[:-1], path[1:]):
        fine += [p.lerp(q, k / 8) for k in range(8)]
    fine.append(path[-1])
    ob = G.strand(tag, [(p.x, p.y, 0.0) for p in fine], r=0.33)
    ob.data.materials[0] = F.ghost('blockA', (0.10, 0.65, 0.65), 0.40)
    ob.scale = (1.0, 1.0, 0.09)
    return ob


def build():
    F.studio()
    # (a) the open chain
    step, x0 = 0.85, -3.45
    pts = [(x0 + (i - (L - 1) / 2) * step, 0.0, 0.0) for i in range(L)]
    for i, p in enumerate(pts):
        spin_site(f'a{i}', p)
        if i < L - 1:
            link(f'a_b{i}', p, pts[i + 1], severed=(i == NA - 1))
    block('a_A', pts[:NA])
    xc = (pts[NA - 1][0] + pts[NA][0]) / 2
    G.pane('a_cut', (xc, 0, 0), w=0.6, h=1.15, turn=30.0)
    F.anchor('a', (pts[0][0] - 0.5, 0, 1.5))
    F.anchor('Aa', ((pts[0][0] + pts[NA - 1][0]) / 2, -0.5, 0))
    F.anchor('cuta', (xc, 0, 1.2))
    # (b) the ring, the same number of sites and the same block
    xr, rr = 4.6, 1.65
    ang = [-math.pi / 2 + 2 * math.pi * (i + 0.5 - NA / 2) / L for i in range(L)]
    pts = [(xr + rr * math.cos(t), rr * math.sin(t), 0.0) for t in ang]
    for i, p in enumerate(pts):
        spin_site(f'b{i}', p)
        link(f'b_b{i}', p, pts[(i + 1) % L], severed=(i == NA - 1 or i == L - 1))
    block('b_A', pts[:NA])
    for k, (i, j) in enumerate([(NA - 1, NA), (L - 1, 0)]):
        t = (ang[i] + ang[j] + (2 * math.pi if j < i else 0)) / 2
        rm = rr * math.cos(math.pi / L)        # the midpoint of the severed bond
        p = (xr + rm * math.cos(t), rm * math.sin(t), 0)
        G.pane(f'b_cut{k}', p, w=0.5, h=0.75, turn=math.degrees(t) + 90.0)
        F.anchor(f'cutb{k}', (xr + (rr + 0.45) * math.cos(t), (rr + 0.45) * math.sin(t), 0.0))
    F.anchor('b', (xr - rr - 1.0, 0, 1.5))
    F.anchor('Ab', (xr, -rr - 0.5, 0))
    F.camera((0.15, 0.0, 0.45), elev=30.0, ortho=16.2, aspect=4.4)


F.main(build, NAME)
