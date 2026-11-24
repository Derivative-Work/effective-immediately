"""M3: the one Blender set (brief): a fictional boardroom, a ring of board members' hands that vote in unison, the
narrator's silhouette walking the table (E08), and the green probe outside the glass with a purchase order (E22).

Everything is procedural and deterministic. Only hands appear: never a board member's face or body. Every word is
Remotion: the wall screen and the purchase order are textures rendered there (renders/m3/tx/). Votes run on a
placeholder 114 BPM grid (config/boardroom.json) until the timing map exists. The probe is modelled after Sandbox
Rhapsody's kit (MIT) and can render alone with alpha (--pass probe), to be composited after the grade.

Usage: blender -b --factory-startup --python blender/boardroom.py -- --shot E09 --out renders/m3/boardroom/E09
         [--stills 1,24,48] [--scale 0.5] [--samples 16] [--pass beauty|probe] [--screen renders/m3/tx/drop.png]
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "config" / "boardroom.json").read_text())
C = CFG["colors"]
HANDS = CFG["hands"]
BEAT = CFG["fps"] * 60 / CFG["bpm_placeholder"]
TABLE_X, TABLE_Y, TABLE_Z = 3.6, 0.85, 0.775  # half length, half width, top surface


# ------------------------------------------------------------------ materials

def lin(h, a=1.0):
    h = h.lstrip("#")
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (*[f(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)], a)


def pbr(name, color, rough=0.6, metal=0.0, alpha=1.0, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "BLENDED"
    return m


def emit(name, color, strength, image=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = lin(color)
    e.inputs["Strength"].default_value = strength
    if image:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(str(image))
        nt.links.new(tex.outputs["Color"], e.inputs["Color"])
    nt.links.new(e.outputs[0], out.inputs["Surface"])
    return m


# ------------------------------------------------------------------ mesh helpers

def finish(name, bm, mats, parent=None, smooth=False):
    if smooth:
        for f in bm.faces:
            f.smooth = True
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    return place(name, me, parent)


def place(name, data, parent=None):
    o = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(o)
    o.parent = parent
    return o


def paint(verts, mi):
    for v in verts:
        for f in v.link_faces:
            f.material_index = mi


def cube(bm, size, loc, mi=0):
    M = Matrix.Translation(loc) @ Matrix.Diagonal((*size, 1))
    paint(bmesh.ops.create_cube(bm, size=1, matrix=M)["verts"], mi)


def blob(bm, loc, scale, mi=0, seg=16):
    M = Matrix.Translation(loc) @ Matrix.Diagonal((*scale, 1))
    paint(bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(6, seg // 2), radius=1, matrix=M)["verts"], mi)


def cone(bm, a, b, ra, rb, mi=0, seg=28):
    a, b = Vector(a), Vector(b)
    d = b - a
    M = Matrix.Translation((a + b) / 2) @ d.to_track_quat("Z", "Y").to_matrix().to_4x4()
    verts = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=ra, radius2=rb, depth=d.length, matrix=M)["verts"]
    paint(verts, mi)
    return list(verts)


def capsule(bm, a, b, ra, rb, mi=0, seg=12):
    a, b = Vector(a), Vector(b)
    d = b - a
    M = Matrix.Translation((a + b) / 2) @ d.to_track_quat("Z", "Y").to_matrix().to_4x4()
    paint(bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=ra, radius2=rb, depth=d.length, matrix=M)["verts"], mi)
    blob(bm, a, (ra, ra, ra), mi, seg)
    blob(bm, b, (rb, rb, rb), mi, seg)


# ------------------------------------------------------------------ the room

def build_room(overhead, screen):
    wall, carpet, ceil = pbr("wall", C["wall"], 0.75), pbr("carpet", C["carpet"], 0.95), pbr("ceiling", C["ceiling"], 0.8)
    bm = bmesh.new()
    cube(bm, (12.2, 12.0, 0.05), (0, 1.8, -0.025), 1)
    cube(bm, (12.2, 0.1, 3.0), (0, -3.65, 1.5))
    cube(bm, (0.1, 7.3, 3.0), (-6.05, 0, 1.5))
    cube(bm, (0.1, 7.3, 3.0), (6.05, 0, 1.5))
    finish("room", bm, [wall, carpet])
    bm = bmesh.new()
    cube(bm, (12.2, 7.3, 0.05), (0, 0, 3.025))
    c = finish("ceiling", bm, [ceil])
    if overhead:
        c.visible_camera = False

    # The glass wall on +Y, with a bright overcast corridor behind it, so everything in the room reads in silhouette.
    glass = pbr("glass", "#e8f0f4", 0.05, 0.0, 0.07)
    bm = bmesh.new()
    cube(bm, (12.1, 0.015, 3.0), (0, 3.6, 1.5))
    finish("glass", bm, [glass])
    bm = bmesh.new()
    for i in range(9):
        cube(bm, (0.06, 0.1, 3.0), (-6 + i * 1.5, 3.6, 1.5))
    cube(bm, (12.1, 0.1, 0.1), (0, 3.6, 0.05))
    cube(bm, (12.1, 0.1, 0.08), (0, 3.6, 2.96))
    finish("mullions", bm, [pbr("mullion", C["mullion"], 0.4, 0.6)])
    sky = emit("sky", C["sky"], CFG["lights"]["sky_strength"])
    bm = bmesh.new()
    cube(bm, (14, 0.05, 4.0), (0, 6.2, 1.8))
    finish("corridor_light", bm, [sky])
    bm = bmesh.new()
    cube(bm, (1.5, 0.5, 0.95), (CFG["probe"]["loc"][0], CFG["probe"]["loc"][1] + 0.08, 0.475))
    finish("console", bm, [pbr("console", C["chair"], 0.5)])

    # Fluorescent panels in rows; soft area lights do the actual lighting.
    panel = emit("panel", C["panel"], CFG["lights"]["panel_strength"])
    bm = bmesh.new()
    for x in (-4.5, -2.25, 0, 2.25, 4.5):
        for y in (-1.9, 0, 1.9):
            cube(bm, (1.25, 0.3, 0.02), (x, y, 2.985))
    p = finish("panels", bm, [panel])
    if overhead:
        p.visible_camera = False
    for x in (-3.6, 0, 3.6):
        L = bpy.data.lights.new(f"area{x}", "AREA")
        L.shape, L.size, L.size_y = "RECTANGLE", 3.2, 5.0
        L.energy = CFG["lights"]["area_power"]
        L.color = lin(CFG["lights"]["area_color"])[:3]
        place(f"area{x}", L).location = (x, 0, 2.9)
        B = bpy.data.lights.new(f"bounce{x}", "AREA")  # the light the floor and table throw back up at the ceiling
        B.shape, B.size, B.size_y = "RECTANGLE", 3.2, 5.0
        B.energy = CFG["lights"]["bounce_power"]
        B.color = lin(CFG["lights"]["area_color"])[:3]
        b = place(f"bounce{x}", B)
        b.location, b.rotation_euler = (x, 0, 1.7), (math.pi, 0, 0)

    # The wall screen at +X; its picture is a Remotion texture.
    bm = bmesh.new()
    cube(bm, (0.05, 3.56, 1.6), (5.98, 0, 1.55))
    finish("screen_bezel", bm, [pbr("bezel", "#0a0b0d", 0.35)])
    me = bpy.data.meshes.new("screen")
    w, h = 1.71, 0.715
    me.from_pydata([(5.95, w, 1.55 - h), (5.95, -w, 1.55 - h), (5.95, -w, 1.55 + h), (5.95, w, 1.55 + h)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new()
    for i, c2 in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
        uv.data[i].uv = c2
    me.materials.append(emit("screen", "#101316", 1.4, screen) if screen else emit("screen", "#101316", 1.0))
    place("screen", me)


def build_table():
    bm = bmesh.new()
    cube(bm, (TABLE_X * 2, TABLE_Y * 2, 0.05), (0, 0, TABLE_Z - 0.025))
    for x in (-2.4, 2.4):
        cube(bm, (0.5, 0.9, TABLE_Z - 0.05), (x, 0, (TABLE_Z - 0.05) / 2), 1)
    t = pbr("table", C["table"], 0.32)
    finish("table", bm, [t, pbr("table_base", C["chair"], 0.5)])


def build_chair(name, loc, yaw, mat):
    bm = bmesh.new()
    cube(bm, (0.52, 0.5, 0.08), (0, 0, 0.48))
    cube(bm, (0.48, 0.06, 0.42), (0, -0.25, 0.74))
    cube(bm, (0.07, 0.07, 0.44), (0, 0, 0.22))
    cube(bm, (0.56, 0.08, 0.04), (0, 0, 0.03))
    cube(bm, (0.08, 0.56, 0.04), (0, 0, 0.03))
    o = finish(name, bm, [mat])
    o.location, o.rotation_euler = loc, (0, 0, yaw)


# ------------------------------------------------------------------ the hands

def hand_mesh(skin, sleeve, cuff):
    """Elbow at the origin, forearm along +Z, palm facing +Y. One mesh, shared by every board member."""
    bm = bmesh.new()
    capsule(bm, (0, 0, 0), (0, 0, 0.38), 0.047, 0.036, 1)
    capsule(bm, (0, 0, 0.375), (0, 0, 0.418), 0.038, 0.037, 2)
    capsule(bm, (0, 0, 0.415), (0, 0, 0.45), 0.031, 0.036, 0, 10)
    blob(bm, (0, 0, 0.482), (0.05, 0.02, 0.06), 0)
    for x, length in ((-0.034, 0.06), (-0.012, 0.074), (0.011, 0.082), (0.033, 0.072)):
        spread = x / 0.034 * 0.11
        p, pitch = Vector((x, 0.0, 0.526)), 0.04
        for s, share in enumerate((0.45, 0.3, 0.25)):
            d = Vector((math.sin(spread) * math.cos(pitch), math.sin(pitch), math.cos(spread) * math.cos(pitch)))
            q = p + d * length * share
            capsule(bm, p, q, 0.0105 - 0.0012 * s, 0.0095 - 0.0012 * s, 0, 8)
            p, pitch = q, pitch + 0.13
    p = Vector((0.044, 0.008, 0.462))
    for d, ln, r in (((0.62, 0.22, 0.75), 0.05, 0.0125), ((0.42, 0.25, 0.87), 0.04, 0.0105)):
        q = p + Vector(d).normalized() * ln
        capsule(bm, p, q, r, r - 0.001, 0, 8)
        p = q
    for f in bm.faces:
        f.smooth = True
    me = bpy.data.meshes.new("hand")
    bm.to_mesh(me)
    bm.free()
    for m in (skin, sleeve, cuff):
        me.materials.append(m)
    return me


def build_hands():
    """Six members a side and one at each end. Returns [{base, pivot, x, near}], near side first, in x order."""
    # Near-black and matte, so they read as silhouettes rather than as models.
    skin, sleeve, cuff = (pbr(n, C[n], 1.0, spec=0.05) for n in ("skin", "sleeve", "cuff"))
    me = hand_mesh(skin, sleeve, cuff)
    bm = bmesh.new()
    capsule(bm, (0, 0, 0), (0, -0.34, -0.32), 0.047, 0.058, 0)
    for f in bm.faces:
        f.smooth = True
    upper = bpy.data.meshes.new("upper_arm")
    bm.to_mesh(upper)
    bm.free()
    upper.materials.append(sleeve)
    chair = pbr("chair", C["chair"], 0.55)
    seats = [(x, -TABLE_Y, 0.0) for x in [-2.9 + i * 1.16 for i in range(6)]]
    seats += [(x, TABLE_Y, math.pi) for x in [-2.9 + i * 1.16 for i in range(6)]]
    seats += [(TABLE_X, 0.0, math.pi / 2), (-TABLE_X, 0.0, -math.pi / 2)]
    out = []
    for i, (x, y, yaw) in enumerate(seats):
        base = place(f"member{i}", None)
        base.location = (x, y, TABLE_Z + 0.04)
        base.rotation_euler = (0, 0, yaw)
        pivot = place(f"member{i}.pivot", None, base)
        place(f"member{i}.forearm", me, pivot)
        place(f"member{i}.upper", upper, base)
        out.append({"base": base, "pivot": pivot, "x": x, "near": y < 0 and abs(y) > 0.1, "home": Vector((x, y, TABLE_Z + 0.04))})
        d = Matrix.Rotation(yaw, 3, "Z") @ Vector((0, -0.62, 0))
        build_chair(f"chair{i}", (x + d.x, y + d.y, 0), yaw, chair)
    return out


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def unison(f):
    """Up on every clap (beats 2 and 4), down on the kick that follows."""
    t = f / BEAT
    beat, frac = int(t), (t - int(t)) * BEAT
    if beat % 2 == 1:
        return ease(frac / HANDS["attack_frames"])
    return 1 - ease(frac / HANDS["release_frames"]) if beat > 0 else 0.0


def key_hands(hands, shot, frames, raised_deg):
    rest, up = math.radians(HANDS["rest_deg"]), math.radians(raised_deg)
    near = [h for h in hands if h["near"]]
    walk = walk_path(frames)
    for f in range(0, frames + 1):
        for k, h in enumerate(hands):
            lean, shift = 0.0, 0.0
            if shot == "E08":  # each hand rises as she draws level with it
                t0 = next((g for g in range(frames + 1) if walk(g) >= h["x"]), frames + 10)
                r = ease((f - t0) / 5)
            elif shot == "E11":  # all at once, on the drop
                r = ease((f - 24) / HANDS["attack_frames"])
            elif shot == "E22s":  # the screen insert: the line recovers and the ring rises again, unanimous
                r = ease((f - 12) / HANDS["attack_frames"])
            elif shot == "E22":  # the reinstatement: unanimous, then the hand that starts to lower gets pushed back up
                r = ease((f - 12) / HANDS["attack_frames"])
                if h is near[3]:
                    r *= 1 - 0.62 * ease((f - 40) / 34) + 0.62 * ease((f - 88) / 8)
                if h is near[4]:
                    reach = ease((f - 66) / 14) * (1 - ease((f - 100) / 12))
                    lean, shift = -0.86 * reach, -0.62 * reach
            else:
                r = unison(f)
            h["pivot"].rotation_euler = (-(rest + (up - rest) * r), lean, 0)
            h["pivot"].keyframe_insert("rotation_euler", frame=f + 1)
            h["base"].location = h["home"] + Vector((shift, 0, 0))
            h["base"].keyframe_insert("location", frame=f + 1)


# ------------------------------------------------------------------ the narrator (a silhouette, E08)

def walk_path(frames):
    return lambda f: -3.5 + 7.0 * f / max(1, frames)


def build_narrator(frames):
    ink = pbr("narrator", C["narrator"], 1.0, spec=0.05)
    root = place("narrator", None)
    bm = bmesh.new()
    cone(bm, (0, 0, 0.4), (0, 0, 1.04), 0.285, 0.172)  # the long coat, flaring to a mid-calf hem
    cone(bm, (0, 0, 1.04), (0, 0, 1.36), 0.172, 0.178)
    blob(bm, (0, 0, 1.365), (0.178, 0.195, 0.085))
    capsule(bm, (0, 0, 1.42), (0, 0, 1.54), 0.05, 0.05, 0)
    blob(bm, (0.018, 0, 1.63), (0.1, 0.09, 0.118))  # head
    blob(bm, (-0.024, 0, 1.652), (0.128, 0.122, 0.13))  # hair
    blob(bm, (-0.05, 0, 1.56), (0.112, 0.116, 0.092))  # the chin-length bob of her reference
    finish("narrator.body", bm, [ink], root, smooth=True)
    limbs = {}
    for side, y in (("l", 0.09), ("r", -0.09)):
        hip = place(f"narrator.hip_{side}", None, root)
        hip.location = (0, y, 0.86)
        bm = bmesh.new()
        capsule(bm, (0, 0, 0), (0, 0, -0.82), 0.065, 0.04, 0)
        capsule(bm, (0.02, 0, -0.84), (0.15, 0, -0.85), 0.04, 0.028, 0)
        finish(f"narrator.leg_{side}", bm, [ink], hip, smooth=True)
        sh = place(f"narrator.shoulder_{side}", None, root)
        sh.location = (0, y * 2.15, 1.39)
        bm = bmesh.new()
        capsule(bm, (0, 0, 0), (0, 0, -0.56), 0.062, 0.042, 0)
        if side == "l":
            capsule(bm, (0, 0, -0.56), (0, 0, -0.68), 0.016, 0.011, 0, 8)  # the finger she counts with
        finish(f"narrator.arm_{side}", bm, [ink], sh, smooth=True)
        limbs[side] = (hip, sh)
    walk = walk_path(frames)
    for f in range(0, frames + 1):
        x = walk(f)
        phase = f / CFG["fps"] * 1.9 * 2 * math.pi
        root.location = (x, 2.1, 0.012 * abs(math.sin(phase)))  # between the far chairs and the bright glass
        root.keyframe_insert("location", frame=f + 1)
        for side, sgn in (("l", 1), ("r", -1)):
            hip, sh = limbs[side]
            hip.rotation_euler = (0, sgn * 0.42 * math.sin(phase), 0)
            hip.keyframe_insert("rotation_euler", frame=f + 1)
            swing = -sgn * 0.3 * math.sin(phase)
            if side == "l":  # counts: the arm comes up and points each time she passes a hand
                swing = -0.98 - 0.13 * math.sin(f / BEAT * 2 * math.pi)
            sh.rotation_euler = (0, swing, 0)
            sh.keyframe_insert("rotation_euler", frame=f + 1)
    return root


# ------------------------------------------------------------------ the probe, outside the glass (E22)

def build_probe(po_tex):
    r = CFG["probe"]["radius"]
    shell, lens = pbr("probe_shell", C["probe"], 0.3, 0.25), pbr("probe_lens", C["lens"], 0.04)
    led = emit("probe_led", C["probe_led"], 1.1)  # any brighter clips to white in the Standard view transform
    root = place("probe", None)
    root.location = CFG["probe"]["loc"]
    bm = bmesh.new()
    blob(bm, (0, 0, 0), (r, r, r), 0, 40)
    blob(bm, (0, -r * 0.8, r * 0.05), (r * 0.4, r * 0.24, r * 0.4), 1, 24)
    blob(bm, (0, -r * 0.1, r * 0.98), (r * 0.14, r * 0.14, r * 0.14), 2, 14)
    blob(bm, (0, -r * 0.98, r * 0.05), (r * 0.2, r * 0.05, r * 0.2), 2, 14)
    for i in range(32):  # the green ring round its lens: what makes it the green probe at this distance
        t = 2 * math.pi * i / 32
        blob(bm, (r * 0.5 * math.cos(t), -r * 0.84, r * 0.05 + r * 0.5 * math.sin(t)), (r * 0.06, r * 0.05, r * 0.06), 2, 8)
    for sx in (-1, 1):  # both arms up, holding the page above its body, so the probe itself stays in view
        capsule(bm, (sx * r * 0.9, -r * 0.1, r * 0.1), (sx * r * 1.36, -r * 0.62, r * 0.72), r * 0.055, r * 0.045, 0, 10)
        capsule(bm, (sx * r * 1.36, -r * 0.62, r * 0.72), (sx * r * 1.0, -r * 0.98, r * 1.42), r * 0.045, r * 0.035, 0, 10)
    body = finish("probe.body", bm, [shell, lens, led], root, smooth=True)
    w, h = r * 1.15, r * 1.53
    me = bpy.data.meshes.new("purchase_order")
    y = -r * 1.0
    cz = r * 2.75
    me.from_pydata([(-w, y, cz - h), (w, y, cz - h), (w, y, cz + h), (-w, y, cz + h)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new()
    for i, c2 in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
        uv.data[i].uv = c2
    me.materials.append(emit("purchase_order", C["paper"], 1.0, po_tex) if po_tex else pbr("paper", C["paper"], 0.8))
    paper = place("probe.paper", me, root)
    return [root, body, paper]


# ------------------------------------------------------------------ render

def setup(a, spec):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.eevee.taa_render_samples = a.samples
    sc.eevee.use_raytracing = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.render.fps = CFG["fps"]
    sc.render.resolution_x, sc.render.resolution_y = (round(v * a.scale) for v in CFG["size"])
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.frame_start, sc.frame_end = 1, spec["frames"]
    w = bpy.data.worlds.new("world")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = lin("#20252a")
    w.node_tree.nodes["Background"].inputs[1].default_value = CFG["lights"]["world"]
    sc.world = w
    cam = bpy.data.cameras.new("cam")
    cam.lens, cam.sensor_width = spec["lens"], 36
    o = place("cam", cam)
    o.location = spec["loc"]
    d = Vector(spec["target"]) - Vector(spec["loc"])
    up = "X" if spec.get("overhead") else "Y"
    o.rotation_euler = d.to_track_quat("-Z", up).to_euler()
    if spec.get("overhead"):  # straight down, with the table's long axis across the frame
        o.rotation_euler = (0, 0, 0)
    if spec.get("track"):  # follows her along the table, part of the way
        walk = walk_path(spec["frames"])
        for f in range(spec["frames"] + 1):
            o.location.x = spec["loc"][0] + spec["track"] * walk(f)
            o.keyframe_insert("location", index=0, frame=f + 1)
    sc.camera = o


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", required=True, choices=list(CFG["shots"]))
    ap.add_argument("--out", required=True)
    ap.add_argument("--stills")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--samples", type=int, default=CFG["samples"])
    ap.add_argument("--pass", dest="layer", default="beauty", choices=["beauty", "probe"])
    ap.add_argument("--screen")
    ap.add_argument("--purchase-order", default="renders/m3/tx/purchase_order.png")
    a = ap.parse_args(argv)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    spec = CFG["shots"][a.shot]
    frames, overhead = spec["frames"], bool(spec.get("overhead"))
    screen = ROOT / a.screen if a.screen else None
    build_room(overhead, screen if screen and screen.exists() else None)
    build_table()
    hands = build_hands()
    key_hands(hands, a.shot, frames, HANDS["overhead_raised_deg"] if overhead else HANDS["raised_deg"])
    if a.shot == "E08":
        build_narrator(frames)
        for h in hands:  # only the near row rises into the bottom of frame; nothing stands between us and her
            if not h["near"]:
                for o in [h["base"], *h["base"].children_recursive]:
                    o.hide_render = True
        for i in range(6):  # the near row's chairs would stand right in front of the lens
            bpy.data.objects[f"chair{i}"].hide_render = True
    po = ROOT / a.purchase_order
    probe_objs = build_probe(po if po.exists() else None) if a.shot == "E22" else []
    setup(a, spec)
    sc = bpy.context.scene
    if a.layer == "probe":
        keep = set(probe_objs) | {sc.camera}
        for o in sc.objects:
            if o not in keep:
                o.hide_render = True
        sc.render.film_transparent = True
        sc.render.image_settings.color_mode = "RGBA"
    else:  # the probe is composited after the grade (brief), so it stays out of the graded plate
        for o in probe_objs:
            o.hide_render = True
    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    if a.stills:
        for f in (int(s) for s in a.stills.split(",")):
            sc.frame_set(f)
            sc.render.filepath = str(out / f"{f:04d}.png")
            bpy.ops.render.render(write_still=True)
    else:
        sc.render.filepath = str(out) + "/"
        bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    main()
