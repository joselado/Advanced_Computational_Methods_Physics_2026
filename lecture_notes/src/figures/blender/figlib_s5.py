"""figlib_s5.py: helpers used only by the Session 5 figures, on top of figlib.py.

`hop` draws a hop or a flip as an arc with an arrowhead, `flow` a straight arrow that reads as
"becomes" between two stages of a panel, and `slab` a translucent rounded block for a string or
an environment.
"""
import math

import bmesh                                                              # noqa: F401
from mathutils import Vector

import figlib as F

GRAY = (0.30, 0.31, 0.36)


def hop(name, p0, p1, height=0.7, r=0.045, rgb=GRAY, head=0.16, seg=24):
    """An arc from p0 to p1 bulging up by `height`, with an arrowhead at p1."""
    p0, p1 = Vector(p0), Vector(p1)
    lift = Vector((0, 0, height))
    pts = [p0.lerp(p1, s) + lift * math.sin(math.pi * s) for s in (k / seg for k in range(seg + 1))]
    # stop the tube short of p1 and put the cone there
    tip = pts[-1]
    back = pts[-4]
    t = (tip - back).normalized()
    base = tip - 2.2 * head * t
    m = F.mat('hop_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.45, spec=0.3)

    def f(bm):
        kept = [p for p in pts if (p - p0).length < (base - p0).length]
        kept.append(base)
        for a, b in zip(kept[:-1], kept[1:]):
            F.bm_cylinder(bm, a, b, r, seg=12, caps=False)
        for p in kept[1:-1]:
            F.bm_sphere(bm, p, r, seg=12, rings=6)
        F.bm_sphere(bm, kept[0], r, seg=12, rings=6)
        F.bm_cylinder(bm, base, tip, head, 0.0, seg=24)
    return F.obj(name, F.mesh_of(name, [m], f))


def flow(name, p0, p1, r=0.06, head=0.2, rgb=GRAY):
    """A straight arrow from p0 to p1, for 'becomes' between two stages."""
    p0, p1 = Vector(p0), Vector(p1)
    t = (p1 - p0).normalized()
    base = p1 - 2.0 * head * t
    m = F.mat('hop_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.45, spec=0.3)

    def f(bm):
        F.bm_cylinder(bm, p0, base, r, seg=16)
        F.bm_cylinder(bm, base, p1, head, 0.0, seg=24)
    return F.obj(name, F.mesh_of(name, [m], f))


def slab(name, center, size, rgb, alpha=0.25, radius=0.15):
    """A translucent rounded block, for a string of factors or a contracted environment."""
    g = F.ghost('slab_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha), rgb, alpha)
    return F.obj(name, F.mesh_of(name, [g], lambda bm: F.bm_rounded_box(bm, Vector((0, 0, 0)), size, radius)),
                 loc=center)
