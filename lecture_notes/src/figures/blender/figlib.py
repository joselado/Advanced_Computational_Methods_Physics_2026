"""figlib.py: the Blender helpers shared by the schematic figures of the lecture notes.

A figure script builds one scene with its panels side by side, marks the points where the TikZ
overlay puts its labels with `anchor(name, co)`, and hands its `build()` to `main(build, name)`.
The render has a transparent background with the shadows on a shadow catcher, so it sits on the
white page; no text is rendered, every label comes from `figures/src/<name>.tex`.

Run with Blender 5.2.2 (the `blender` on the PATH is 2.79):
    DISPLAY=:0 ~/apps/blender-5.2.2-linux-x64/blender -b --factory-startup --python <script> -- still
    DISPLAY=:0 ~/apps/blender-5.2.2-linux-x64/blender -b --factory-startup --python <script> -- final
`still` renders at 50 % with few samples into out/<name>_still.png, `final` at full size into
out/<name>.png; both write out/<name>_anchors.tex, the anchors in units of the image width, and
`anchors` writes only that file.
The shapes and colors are those of the course films (videos/common/scene.py), so that a reader
recognizes the arrows, sites and electrons of the exercise shorts.
"""
import math
import os
import sys

import bpy
import bmesh
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
WIDTH = 2400                                  # final width in px; the height follows the camera

# Colors of the series (linear RGB)
UP_TIP, UP_TAIL = (1.0, 0.62, 0.12), (0.75, 0.04, 0.02)
DOWN_TIP, DOWN_TAIL = (0.25, 0.75, 1.0), (0.03, 0.12, 0.55)
ELECTRON = (0.10, 0.62, 0.95)                 # the films' cyan, a little deeper so it holds on paper
SITE = (0.06, 0.06, 0.09)
BOND = (0.55, 0.56, 0.60)
ACCENT = {1: (1.0, 0.55, 0.12), 2: (0.12, 0.75, 0.30), 3: (0.10, 0.62, 0.95),
          4: (0.05, 0.60, 0.60), 5: (0.55, 0.35, 0.95)}

ANCHORS = {}


# ------------------------------------------------------------------------------------------------
# Materials
# ------------------------------------------------------------------------------------------------
def principled(name, rgb, rough=0.4, emit=0.0, alpha=1.0, spec=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    b = mat.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Specular IOR Level'].default_value = spec
    b.inputs['Emission Color'].default_value = (*rgb, 1)
    b.inputs['Emission Strength'].default_value = emit
    b.inputs['Alpha'].default_value = alpha
    return mat


def gradient_arrow_material(name, tip_rgb, tail_rgb, emit=0.15, rough=0.45, spec=0.4):
    """Arrow colored from tail to tip along its own z axis, as in the films."""
    mat = principled(name, tip_rgb, rough=rough, emit=emit, spec=spec)
    nt = mat.node_tree
    b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value, mr.inputs['From Max'].default_value = -0.5, 0.5
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = (*tail_rgb, 1)
    mix.inputs['B'].default_value = (*tip_rgb, 1)
    nt.links.new(tc.outputs['Object'], sep.inputs[0])
    nt.links.new(sep.outputs['Z'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], mix.inputs['Factor'])
    nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    nt.links.new(mix.outputs['Result'], b.inputs['Emission Color'])
    return mat


def glow(name, rgb, strength=2.0, alpha=0.35):
    """A soft translucent glow, for an energy cost such as U or V."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (*rgb, 1)
    em.inputs['Strength'].default_value = strength
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    lw = nt.nodes.new('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.35
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value, mr.inputs['From Max'].default_value = 0.0, 1.0
    mr.inputs['To Min'].default_value, mr.inputs['To Max'].default_value = alpha, 0.0
    mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lw.outputs['Facing'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])
    return mat


def mat(name, rgb, **kw):
    return bpy.data.materials.get(name) or principled(name, rgb, **kw)


# ------------------------------------------------------------------------------------------------
# Meshes and objects
# ------------------------------------------------------------------------------------------------
def _faces_of(verts):
    return {f for v in verts for f in v.link_faces}


def bm_sphere(bm, center, r, mat_index=0, seg=32, rings=16):
    res = bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r,
                                    matrix=Matrix.Translation(center))
    for f in _faces_of(res['verts']):
        f.material_index, f.smooth = mat_index, True


def bm_cylinder(bm, p0, p1, r0, r1=None, mat_index=0, seg=24, caps=True):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    rot = d.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    res = bmesh.ops.create_cone(bm, cap_ends=caps, cap_tris=False, segments=seg, radius1=r0,
                                radius2=r0 if r1 is None else r1, depth=d.length,
                                matrix=Matrix.Translation((p0 + p1) / 2) @ rot)
    for f in _faces_of(res['verts']):
        f.material_index, f.smooth = mat_index, True
    for f in _faces_of(res['verts']):
        if len(f.verts) > 4:                       # the caps stay flat
            f.smooth = False


def mesh_of(name, mats, build_fn):
    bm = bmesh.new()
    build_fn(bm)
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    return me


def obj(name, data, loc=(0, 0, 0), rot=(0, 0, 0), scale=1.0, coll=None):
    ob = bpy.data.objects.new(name, data)
    (coll or bpy.context.scene.collection).objects.link(ob)
    ob.location, ob.rotation_euler = loc, rot
    ob.scale = (scale, scale, scale) if isinstance(scale, (int, float)) else scale
    return ob


def arrow_mesh(name, m):
    """Unit arrow along +z centered on its origin, the shape of the films."""
    def f(bm):
        bm_cylinder(bm, (0, 0, -0.5), (0, 0, 0.05), 0.045, seg=20)
        bm_cylinder(bm, (0, 0, 0.05), (0, 0, 0.5), 0.185, 0.0, seg=32)
    return mesh_of(name, [m], f)


def spin_arrows():
    if bpy.data.meshes.get('arrow_up') is None:
        arrow_mesh('arrow_up', gradient_arrow_material('arrow_up', UP_TIP, UP_TAIL))
        arrow_mesh('arrow_down', gradient_arrow_material('arrow_down', DOWN_TIP, DOWN_TAIL))
    return bpy.data.meshes['arrow_up'], bpy.data.meshes['arrow_down']


def arrow(name, loc, direction, length=0.8):
    """A spin arrow of the series pointing along `direction` (a vector; up colors if its z >= 0)."""
    up, down = spin_arrows()
    d = Vector(direction).normalized()
    me = up if d.z >= -1e-9 else down
    rot = d.to_track_quat('Z', 'Y').to_euler()
    return obj(name, me, loc=loc, rot=rot, scale=length)


def site(name, loc, r=0.32, h=0.08):
    """A lattice site: a dark disc lying on the floor."""
    m = mat('site', SITE, rough=0.5, spec=0.3)
    return obj(name, mesh_of(name, [m], lambda bm: bm_cylinder(bm, (0, 0, 0), (0, 0, h), r, seg=48)), loc=loc)


def bond(name, p0, p1, r=0.035):
    m = mat('bond', BOND, rough=0.5, spec=0.3)
    return obj(name, mesh_of(name, [m], lambda bm: bm_cylinder(bm, p0, p1, r, seg=16)))


def ball(name, loc, r, rgb=ELECTRON, emit=0.15):
    m = mat('ball_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.3, emit=emit, spec=0.5)
    return obj(name, mesh_of(name, [m], lambda bm: bm_sphere(bm, Vector((0, 0, 0)), r)), loc=loc)


def column(name, loc, height, r=0.24, rgb=ELECTRON):
    m = mat('col_%d_%d_%d' % tuple(int(255 * c) for c in rgb), rgb, rough=0.35, emit=0.1, spec=0.5)
    return obj(name, mesh_of(name, [m], lambda bm: bm_cylinder(bm, (0, 0, 0), (0, 0, height), r, seg=40)),
               loc=loc)


def anchor(name, co):
    """A point that the TikZ overlay can refer to as (name)."""
    ANCHORS[name] = Vector(co)


# ------------------------------------------------------------------------------------------------
# Studio, camera and render
# ------------------------------------------------------------------------------------------------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ANCHORS.clear()


def studio(floor_size=80.0):
    """White world, a large soft key light, a fill, and a shadow catcher floor at z = 0."""
    sc = bpy.context.scene
    w = bpy.data.worlds.new('world')
    w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.92, 0.93, 0.96, 1)
    bg.inputs['Strength'].default_value = 0.55
    sc.world = w
    key = bpy.data.lights.new('key', 'AREA')
    key.energy, key.size, key.shape = 2600.0, 6.0, 'SQUARE'
    k = obj('key', key, loc=(-8.0, -10.0, 14.0))
    k.rotation_euler = (Vector((0, 0, 0)) - k.location).to_track_quat('-Z', 'Y').to_euler()
    fill = bpy.data.lights.new('fill', 'AREA')
    fill.energy, fill.size = 700.0, 18.0
    f = obj('fill', fill, loc=(10.0, -12.0, 6.0))
    f.rotation_euler = (Vector((0, 0, 0)) - f.location).to_track_quat('-Z', 'Y').to_euler()
    m = principled('floor', (1, 1, 1), rough=0.9, spec=0.0)
    fl = obj('floor', mesh_of('floor', [m], lambda bm: bmesh.ops.create_grid(
        bm, x_segments=1, y_segments=1, size=floor_size / 2)))
    fl.is_shadow_catcher = True


def camera(target, elev=32.0, azim=0.0, ortho=12.0, aspect=2.4):
    """Orthographic camera looking at `target` from the front (-y), raised by `elev` degrees."""
    sc = bpy.context.scene
    cam = bpy.data.cameras.new('cam')
    cam.type, cam.ortho_scale = 'ORTHO', ortho
    cam.clip_end = 200.0
    e, a = math.radians(elev), math.radians(azim)
    d = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    c = obj('cam', cam, loc=Vector(target) + 40.0 * d)
    c.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = c
    sc.render.resolution_x = WIDTH
    sc.render.resolution_y = int(round(WIDTH / aspect))
    return c


def setup_render(pct, samples):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.film_transparent = True
    sc.render.resolution_percentage = pct
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'


def write_anchors(path):
    """Anchors as TikZ coordinates in units of the image width, origin at the bottom left."""
    sc = bpy.context.scene
    bpy.context.view_layer.update()            # the camera's matrix_world is stale until this
    ratio = sc.render.resolution_y / sc.render.resolution_x
    with open(path, 'w') as fh:
        fh.write('%% written by figlib.py; x and y in units of the image width\n')
        for name, co in ANCHORS.items():
            p = world_to_camera_view(sc, sc.camera, co)
            fh.write('\\coordinate (%s) at (%.4f\\figw,%.4f\\figw);\n' % (name, p.x, p.y * ratio))


def main(build, name):
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['still']
    mode = argv[0]
    reset()
    build()
    os.makedirs(OUT, exist_ok=True)
    pct, samples, suffix = (50, 48, '_still') if mode == 'still' else (100, 256, '')
    setup_render(pct, samples)
    write_anchors(os.path.join(OUT, name + '_anchors.tex'))
    if mode == 'anchors':
        return
    sc = bpy.context.scene
    sc.render.filepath = os.path.join(OUT, name + suffix + '.png')
    bpy.ops.render.render(write_still=True)
    print('wrote', sc.render.filepath)
