"""figlib_s4.py: helpers used only by the Session 4 figures (matrix product states for spin chains).

Kept apart from figlib.py so that the five session builds do not edit one shared file at once.
"""
import math

import bpy
from mathutils import Vector

import figlib as F

TEAL = F.TENSOR                         # the tensor teal shared with session 5
LEG = (0.20, 0.21, 0.24)               # tensor legs, darker than lattice bonds so they read as indices
STRAND = (0.0, 0.42, 0.44)             # an entanglement strand, a shared index or a singlet bond
PALE = (0.72, 0.74, 0.80)              # a spin without a moment (a site of a singlet), no arrow


def strand(name, pts, r=0.03, rgb=STRAND, n=32):
    """A smooth tube through the points `pts` (a quadratic Bezier through three, a polyline else)."""
    pts = [Vector(p) for p in pts]
    if len(pts) == 3:
        p0, c, p1 = pts
        pts = [(1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t ** 2 * p1 for t in (i / n for i in range(n + 1))]
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution = '3D', r, 4
    cu.use_fill_caps = True
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts):
        p.co = (*q, 1.0)
    sp.use_smooth = True
    cu.materials.append(F.mat('strand_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.35,
                              emit=0.1, spec=0.5))
    return F.obj(name, cu)


def arc(name, p0, p1, h, **kw):
    """A strand arching from p0 to p1, its top `h` above the straight line."""
    p0, p1 = Vector(p0), Vector(p1)
    return strand(name, [p0, (p0 + p1) / 2 + Vector((0, 0, 2 * h)), p1], **kw)


def pane(name, loc, w=1.5, h=1.6, turn=35.0, alpha=0.30):
    """A cut as a translucent pane in the session accent, turned about z by `turn` degrees so that
    the front camera sees its face and not its edge."""
    ob = F.cut(name, (loc[0], loc[1], loc[2] + h / 2), size=(0.03, w, h), alpha=alpha)
    ob.rotation_euler = (0, 0, math.radians(turn))
    return ob


def pale_spin(name, loc, r=0.24):
    """A spin with no moment, a sphere without an arrow."""
    return F.ball(name, loc, r, rgb=PALE, emit=0.05)
