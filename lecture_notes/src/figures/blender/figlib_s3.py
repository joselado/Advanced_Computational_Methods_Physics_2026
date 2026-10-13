"""figlib_s3.py: helpers used only by the Session 3 figures, on top of figlib.py."""
import figlib as F


def ghost_column(name, loc, height, r=0.24, rgb=F.ELECTRON, alpha=0.3):
    """A charge column drawn as a translucent ghost, for a partner state of equal energy."""
    m = F.ghost('ghostcol_%.2f' % alpha, rgb, alpha)
    return F.obj(name, F.mesh_of(name, [m], lambda bm: F.bm_cylinder(bm, (0, 0, 0), (0, 0, height), r, seg=40)),
                 loc=loc)


def chain_sites(x0, y, n, step, tag, r=0.3, bonds=True):
    """n sites along x centered on x0 at depth y, with bonds between them; returns their x."""
    xs = [x0 + (i - (n - 1) / 2) * step for i in range(n)]
    for i, x in enumerate(xs):
        F.site(f'{tag}_s{i}', (x, y, 0), r=r)
        if bonds and i < n - 1:
            F.bond(f'{tag}_b{i}', (x + r, y, 0.05), (xs[i + 1] - r, y, 0.05))
    return xs


def arc(name, p0, p1, height, r, rgb, n=40, tilt=0.0):
    """A tube along a half-ellipse from p0 to p1 rising to `height`, in the vertical plane through
    them tilted by `tilt` degrees about the line p0-p1 (positive leans away from the camera)."""
    import math
    from mathutils import Vector
    p0, p1 = Vector(p0), Vector(p1)
    up = Vector((0, math.sin(math.radians(tilt)), math.cos(math.radians(tilt))))
    pts = [p0.lerp(p1, k / n) + up * height * math.sin(math.pi * k / n) for k in range(n + 1)]
    m = F.mat('arc_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.4, emit=0.1, spec=0.4)

    def f(bm):
        for a, b in zip(pts[:-1], pts[1:]):
            F.bm_cylinder(bm, a, b, r, seg=16, caps=False)
        for p in pts[1:-1]:
            F.bm_sphere(bm, p, r, seg=16, rings=8)
    return F.obj(name, F.mesh_of(name, [m], f))
