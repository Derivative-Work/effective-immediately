"""Grey-box kit for the sanctuary: flat materials, primitives, merged meshes, cameras.

Trimmed from Read-Only's scenes/blender/lib/gb.py (primitives, materials, cameras), plus merged-mesh helpers for the
congregation (one mesh per figure variant, shared by linked copies). Grey-box means blocking plus light: shapes say
what a thing is, the light rig says how the room feels (brief, M3: "Grey-box sanctuary with a lighting board").
Everything is deterministic: random draws come from numpy generators seeded from config/seeds.json.
"""
import json
import math
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
SEEDS = json.loads((ROOT / "config" / "seeds.json").read_text())
LOOK = json.loads((ROOT / "config" / "look.json").read_text())


def rng(name):
    """A numpy generator for one named random process: main seed plus a fixed offset per name."""
    return np.random.default_rng([SEEDS["main"], sum(ord(c) * (i + 1) for i, c in enumerate(name))])


# ---------------------------------------------------------------- materials

_MATS = {}


def lin(hexstr):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    h = hexstr.lstrip("#")
    return (ch(int(h[0:2], 16)), ch(int(h[2:4], 16)), ch(int(h[4:6], 16)), 1.0)


def mat(name, hexcol, rough=0.8, emit=0.0, metal=0.0, alpha=1.0, transmission=0.0):
    """A flat principled material, cached by name. emit > 0 makes it glow in its own colour."""
    if name in _MATS:
        return _MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(hexcol)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = lin(hexcol)
        b.inputs["Emission Strength"].default_value = emit
    if transmission:
        b.inputs["Transmission Weight"].default_value = transmission
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "BLENDED"
    _MATS[name] = m
    return m


def set_emit(m, hexcol=None, strength=None):
    b = m.node_tree.nodes["Principled BSDF"]
    if hexcol:
        b.inputs["Emission Color"].default_value = lin(hexcol)
    if strength is not None:
        b.inputs["Emission Strength"].default_value = strength


def gradient_mat(name, stops, strength=1.0):
    """An emissive vertical gradient over the object's generated Z (0 bottom .. 1 top): a stand-in for a lyric-slide
    photo until the Remotion and generated textures exist. stops: [(pos, hex), ...]."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = strength
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    els = ramp.color_ramp.elements
    for i, (p, c) in enumerate(stops):
        e = els[i] if i < 2 else els.new(p)
        e.position, e.color = p, lin(c)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    _MATS[name] = m
    return m


def image_mat(name, path, strength=1.0):
    """An emissive image on a plane (the lyric screen or a phone), UV-mapped by plane()."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = strength
    img = nt.nodes.new("ShaderNodeTexImage")
    img.image = bpy.data.images.load(str(path), check_existing=True)
    nt.links.new(img.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    _MATS[name] = m
    return m


# ---------------------------------------------------------------- objects

def collection(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    return c


_COLL = [None]


def into(c):
    """Link new objects into collection c (None: the scene collection)."""
    _COLL[0] = c


def link(o, parent=None):
    (_COLL[0] or bpy.context.scene.collection).objects.link(o)
    if parent:
        o.parent = parent
    return o


def mesh_obj(name, me, loc=(0, 0, 0), rot_z=0.0, parent=None):
    o = link(bpy.data.objects.new(name, me), parent)
    o.location, o.rotation_euler.z = loc, rot_z
    return o


def empty(name, loc=(0, 0, 0), parent=None):
    o = link(bpy.data.objects.new(name, None), parent)
    o.location = loc
    return o


def box(name, center, size, m, parent=None, rot_z=0.0):
    """An axis-aligned box: center (x, y, z) and full size (sx, sy, sz), metres."""
    sx, sy, sz = (s / 2 for s in size)
    v = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
         (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], f)
    me.materials.append(m)
    return mesh_obj(name, me, center, rot_z, parent)


def cyl(name, center, r, h, m, parent=None, n=16, axis="Z", r2=None):
    """A cylinder (or a cone frustum with top radius r2) of height h centred on center."""
    r2 = r if r2 is None else r2
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    v = [(r * math.cos(a), r * math.sin(a), -h / 2) for a in ang] + [(r2 * math.cos(a), r2 * math.sin(a), h / 2) for a in ang]
    f = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], f)
    me.materials.append(m)
    o = mesh_obj(name, me, center, 0.0, parent)
    if axis == "X":
        o.rotation_euler.y = math.pi / 2
    elif axis == "Y":
        o.rotation_euler.x = math.pi / 2
    return o


def plane(name, center, size, m, parent=None, facing="-Y"):
    """A rectangle (width, height) facing the given axis direction, UV-mapped 0..1 so an image reads upright and
    left to right for a viewer in front of it."""
    w, h = size[0] / 2, size[1] / 2
    v = {"-Y": [(-w, 0, -h), (w, 0, -h), (w, 0, h), (-w, 0, h)],
         "+Y": [(w, 0, -h), (-w, 0, -h), (-w, 0, h), (w, 0, h)],
         "+X": [(0, -w, -h), (0, w, -h), (0, w, h), (0, -w, h)],
         "-X": [(0, w, -h), (0, -w, -h), (0, -w, h), (0, w, h)],
         "+Z": [(-w, -h, 0), (w, -h, 0), (w, h, 0), (-w, h, 0)],
         "-Z": [(-w, h, 0), (w, h, 0), (w, -h, 0), (-w, -h, 0)]}[facing]
    me = bpy.data.meshes.new(name)
    me.from_pydata(v, [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new()
    for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[i].uv = c
    me.materials.append(m)
    return mesh_obj(name, me, center, 0.0, parent)


# ---------------------------------------------------------------- merged meshes (figures, seats)

class Builder:
    """Accumulates primitives into one bmesh, each with a material slot index; to_mesh() makes one mesh."""

    def __init__(self, mats):
        self.bm = bmesh.new()
        self.mats = list(mats)

    def _tag(self, geom, mi, M):
        verts = [g for g in geom if isinstance(g, bmesh.types.BMVert)]
        bmesh.ops.transform(self.bm, matrix=M, verts=verts)
        for f in {f for v in verts for f in v.link_faces}:
            f.material_index = mi
            f.smooth = True

    def box(self, center, size, mi=0, rot=(0, 0, 0)):
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        M = Matrix.Translation(center) @ Matrix.LocRotScale(None, Matrix.Rotation(rot[0], 3, "X") @ Matrix.Rotation(rot[1], 3, "Y") @ Matrix.Rotation(rot[2], 3, "Z"), size)
        self._tag(r["verts"], mi, M)

    def ball(self, center, radius, mi=0, scale=(1, 1, 1)):
        r = bmesh.ops.create_uvsphere(self.bm, u_segments=12, v_segments=8, radius=1.0)
        self._tag(r["verts"], mi, Matrix.LocRotScale(center, None, [radius * s for s in scale]))

    def capsule(self, a, b, radius, mi=0, rx=None):
        """A tapered limb from point a to point b (a cone frustum with ball ends)."""
        a, b = Vector(a), Vector(b)
        d = b - a
        r = bmesh.ops.create_cone(self.bm, cap_ends=True, segments=10, radius1=radius, radius2=rx or radius, depth=d.length)
        M = Matrix.Translation((a + b) / 2) @ d.to_track_quat("Z", "Y").to_matrix().to_4x4()
        self._tag(r["verts"], mi, M)
        self.ball(a, radius, mi)
        self.ball(b, rx or radius, mi)

    def to_mesh(self, name):
        me = bpy.data.meshes.new(name)
        self.bm.to_mesh(me)
        self.bm.free()
        for m in self.mats:
            me.materials.append(m)
        return me


# ---------------------------------------------------------------- cameras

def look_rot(loc, target):
    return (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


def camera(name, loc, target, lens=35.0, roll=0.0):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_start, cd.clip_end = 0.05, 200
    o = link(bpy.data.objects.new(name, cd))
    o.location = loc
    o.rotation_euler = look_rot(loc, target)
    o.rotation_euler.rotate_axis("Z", roll)
    return o
