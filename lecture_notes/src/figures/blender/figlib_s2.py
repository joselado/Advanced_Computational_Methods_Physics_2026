"""figlib_s2.py: helpers only the Session 2 figures use, on top of figlib.py."""
import math

import bmesh
import bpy
from mathutils import Vector

import figlib as F

SINGLET = F.ACCENT[2]                     # a singlet bond in the green of Session 2
SPIN0 = (0.62, 0.64, 0.70)                # a site with no moment: a neutral sphere


def tube(name, pts, r, m):
    """A tube through the points `pts`, cylinders with spheres at the joints."""
    def f(bm):
        for p0, p1 in zip(pts[:-1], pts[1:]):
            F.bm_cylinder(bm, p0, p1, r, seg=16, caps=False)
        for p in pts:
            F.bm_sphere(bm, Vector(p), r, seg=16, rings=8)
    return F.obj(name, F.mesh_of(name, [m], f))


def arc(name, p0, p1, height, r=0.06, m=None, n=24):
    """A tube on a parabolic arc from p0 to p1 rising by `height` in z, for a singlet bond."""
    p0, p1 = Vector(p0), Vector(p1)
    m = m or F.mat('singlet', SINGLET, rough=0.35, emit=0.1, spec=0.5)
    pts = [p0.lerp(p1, t) + Vector((0, 0, 4 * height * t * (1 - t))) for t in (i / n for i in range(n + 1))]
    return tube(name, pts, r, m)


def spin0(name, loc, r=0.26):
    """A spin with no moment on its site: a neutral sphere, no arrow."""
    return F.ball(name, loc, r, rgb=SPIN0, emit=0.0)


def bar(name, loc, size, rgb, rough=0.4, emit=0.05):
    """A rectangular bar of full sizes `size` standing on its base at `loc`."""
    m = F.mat('bar_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=rough, emit=emit, spec=0.4)
    c = Vector(loc) + Vector((0, 0, size[2] / 2))
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_rounded_box(bm, Vector((0, 0, 0)), size,
                                                                      min(0.02, min(size) / 4))), loc=c)


def ghost_site(name, loc, r=0.32, h=0.08, alpha=0.25):
    """A lattice site drawn as a ghost, for a state the constraint removes."""
    m = F.ghost('ghost_site_%.2f' % alpha, F.SITE, alpha)
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, h), r, seg=48)), loc=loc)


def arc_arrow(name, p0, p1, height, r=0.045, rgb=None, head=0.16, n=28):
    """A curved arrow on a parabolic arc from p0 to p1, the head at p1, for a hop."""
    p0, p1 = Vector(p0), Vector(p1)
    rgb = rgb or (0.20, 0.22, 0.28)
    m = F.mat('arcarrow_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.4, emit=0.05, spec=0.4)
    pts = [p0.lerp(p1, t) + Vector((0, 0, 4 * height * t * (1 - t))) for t in (i / n for i in range(n + 1))]
    # stop the tube where the head begins
    total, cut = 0.0, len(pts) - 1
    for i in range(len(pts) - 1, 0, -1):
        total += (pts[i] - pts[i - 1]).length
        if total >= 2.2 * head:
            cut = i
            break
    tube(name, pts[:cut + 1], r, m)
    d = (pts[-1] - pts[cut]).normalized()
    base = pts[-1] - d * 2.2 * head
    F.obj(name + '_head', F.mesh_of(name + '_head', [m], lambda bm: F.bm_cylinder(bm, base, pts[-1], head, 0.0,
                                                                                 seg=24)))


def ribbon(name, pts, width, thick, m):
    """A strip of width `width` along y through the points `pts` (x, z) at y = 0, thickness `thick`."""
    def f(bm):
        rows = []
        for (x, z) in pts:
            rows.append([bm.verts.new((x, sy * width / 2, z + sz * thick / 2)) for sy, sz in
                         ((-1, 1), (1, 1), (1, -1), (-1, -1))])
        for a, b in zip(rows[:-1], rows[1:]):
            for k in range(4):
                bm.faces.new((a[k], a[(k + 1) % 4], b[(k + 1) % 4], b[k]))
        bm.faces.new(rows[0][::-1])
        bm.faces.new(rows[-1])
        for fc in bm.faces:
            fc.smooth = True
    return F.obj(name, F.mesh_of(name, [m], f))
