"""figlib_s1.py: helpers used only by the Session 1 figures (classical magnetism)."""
import math

import bpy
from mathutils import Vector

import figlib as F

SLAB = (0.86, 0.87, 0.90)


def slab(name, center, size, rgb=SLAB, radius=0.03):
    """A thin light plate, for a basis state or a level."""
    m = F.mat('slab_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.6, spec=0.3)
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_rounded_box(bm, Vector((0, 0, 0)), size, radius)),
                 loc=center)


def ghost_ball(name, loc, r, rgb=F.ELECTRON, alpha=0.25):
    m = F.ghost('ghostball_%d_%d_%d_%.2f' % (*(int(255 * c) for c in rgb), alpha), rgb, alpha)
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_sphere(bm, Vector((0, 0, 0)), r)), loc=loc)


def bar(name, loc, size, rgb):
    """A bar of a skyline, standing on the floor at loc with full sizes `size`."""
    m = F.mat('bar_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.4, emit=0.05, spec=0.4)
    c = Vector(loc) + Vector((0, 0, size[2] / 2))
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_rounded_box(bm, Vector((0, 0, 0)), size,
                                                                        min(0.04, size[2] / 2.5))), loc=c)


def rod(name, p0, p1, r=0.03, rgb=F.BOND):
    m = F.mat('rod_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.5, spec=0.3)
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_cylinder(bm, p0, p1, r, seg=16)))


def cone_tip(name, p0, p1, r=0.09, rgb=F.BOND):
    """An arrowhead from p0 to p1."""
    m = F.mat('rod_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.5, spec=0.3)
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_cylinder(bm, p0, p1, r, 0.0, seg=24)))


def arc(name, p0, p1, height, r=0.03, rgb=F.BOND, n=24, frac=1.0, head=True):
    """A curved hop from p0 to p1 bulging up by `height`, drawn up to the fraction `frac`."""
    p0, p1 = Vector(p0), Vector(p1)
    pts = []
    for k in range(n + 1):
        s = frac * k / n
        p = p0.lerp(p1, s) + Vector((0, 0, height * math.sin(math.pi * s)))
        pts.append(p)
    m = F.mat('rod_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.5, spec=0.3)

    def f(bm):
        for a, b in zip(pts[:-2] if head else pts[:-1], pts[1:-1] if head else pts[1:]):
            F.bm_cylinder(bm, a, b, r, seg=12)
            F.bm_sphere(bm, b, r, seg=12, rings=6)
        if head:
            F.bm_cylinder(bm, pts[-2] - (pts[-1] - pts[-2]) * 1.2, pts[-1] + (pts[-1] - pts[-2]) * 1.2, 3 * r, 0.0, seg=24)
    return F.obj(name, F.mesh_of(name, [m], f))


def surface(name, f, x0, x1, y0, y1, n=120, rgb=(0.80, 0.83, 0.90), offset=(0, 0, 0)):
    """A height field z = f(x, y) over a rectangle, smooth shaded, shifted by `offset`."""
    import bmesh
    m = F.mat('surf_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.55, spec=0.35)

    def build(bm):
        nx, ny = n, int(n * (y1 - y0) / (x1 - x0))
        vs = [[bm.verts.new((x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny,
                             f(x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny)))
               for j in range(ny + 1)] for i in range(nx + 1)]
        for i in range(nx):
            for j in range(ny):
                fc = bm.faces.new((vs[i][j], vs[i + 1][j], vs[i + 1][j + 1], vs[i][j + 1]))
                fc.smooth = True
    return F.obj(name, F.mesh_of(name, [m], build), loc=offset)


def tube(name, pts, r=0.03, rgb=F.BOND, head=True):
    """A polyline of points as a tube, with an arrowhead at the end if `head`."""
    pts = [Vector(p) for p in pts]
    if len(pts) == 2:
        pts = [pts[0].lerp(pts[1], k / 8) for k in range(9)]
    m = F.mat('rod_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.5, spec=0.3)

    def f(bm):
        body = pts[:-1] if head else pts
        for a, b in zip(body[:-1], body[1:]):
            F.bm_cylinder(bm, a, b, r, seg=12)
            F.bm_sphere(bm, b, r, seg=12, rings=6)
        if head:
            d = (pts[-1] - pts[-2]).normalized()
            F.bm_cylinder(bm, pts[-1] - 0.28 * d, pts[-1], 3 * r, 0.0, seg=24)
    return F.obj(name, F.mesh_of(name, [m], f))


NEUTRAL_TIP, NEUTRAL_TAIL = (0.42, 0.45, 0.95), (0.08, 0.06, 0.38)


def sz_arrow(name, loc, direction, length=0.8, neutral=False):
    """A spin arrow colored continuously by its z component, mixing the up and down gradients, or
    with one neutral gradient if `neutral`, so that a spin in the plane reads as neither up nor
    down; `loc` is the center of the arrow."""
    d = Vector(direction).normalized()
    w = (d.z + 1) / 2
    mix = lambda a, b: tuple(w * x + (1 - w) * y for x, y in zip(a, b))
    if neutral:
        tip, tail, key = NEUTRAL_TIP, NEUTRAL_TAIL, 'szarrow_neutral_%.3f_%.3f' % (d.x, d.z)
    else:
        tip, tail = mix(F.UP_TIP, F.DOWN_TIP), mix(F.UP_TAIL, F.DOWN_TAIL)
        key = 'szarrow_%.3f' % d.z
    if bpy.data.meshes.get(key) is None:
        F.arrow_mesh(key, F.gradient_arrow_material(key, tip, tail))
    return F.obj(name, bpy.data.meshes[key], loc=loc, rot=d.to_track_quat('Z', 'Y').to_euler(), scale=length)
