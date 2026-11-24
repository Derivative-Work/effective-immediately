"""M6 look test: the final-look congregation, band and walkers (decisions 9). Builds a library of varied, clothed,
posed people with MakeHuman's MPFB and saves assets/figures/figures.blend; the set (blender/sanctuary.py, --look
final) links it, so MPFB is not needed at render time.

People: adults only (brief: "Congregation is adults only"), age 25-70, mixed gender, build, height, skin and hair;
clothes from MakeHuman's CC0 system assets (assets/mpfb/assets_pack, sha256 in production log 29), each outfit's
colour shifted per person so a few outfits make a varied crowd. Faces are MakeHuman's generic averages of its
targets, invented and seen only from behind, in silhouette or far away (brief: no identifiable faces).
Every person is kept in every pose of blender/figlib.py as one collection "fig_<person>_<pose>": a copy of the rig in
that pose with the pose's looping motion (figlib.animate; M6, human: crowd motion), and copies of the person's
meshes deformed by it (static baked meshes until M6). Phone poses get a phone parented to the hand (dark body, emissive screen facing the face, material "phone_glow"), and its screen centre is stored on
the collection as "phone" (figure space) for the set's phone lights.
Seeds: config/seeds.json main, through gb.rng-style named streams.
Needs the MPFB extension (assets/mpfb/add-on-mpfb-v2.0.18.zip) installed in Blender, its data folder linked to
assets/mpfb/assets_pack (production log 29).
Usage: blender -b --python blender/make_figures.py -- [--people 24] [--out assets/figures/figures.blend]
"""
import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

import addon_utils
import bpy
import numpy as np
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figlib as F  # noqa: E402

addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
from bl_ext.user_default.mpfb.services.humanservice import HumanService  # noqa: E402
from bl_ext.user_default.mpfb.services.targetservice import TargetService  # noqa: E402

A = Path("assets/mpfb/assets_pack").resolve()
SEED = json.load(open("config/seeds.json"))["main"]

# Church clothes: the sportsuit (crop top), the shorts outfit and the overalls are left out; MakeHuman refits any
# outfit to any body, so the plain shirt-and-jeans outfits dress women too. Five outfits print MakeHuman's logo or
# name: their textures are cleaned copies (scripts/clean_clothes.py; brief: no real logo).
MALE = {"clothes": ["male_casualsuit01", "male_casualsuit02", "male_casualsuit03", "male_casualsuit04",
                    "male_casualsuit05", "male_casualsuit06", "male_elegantsuit01"],
        "hair": ["short01", "short02", "short03", "short04", "afro01", None]}
FEMALE = {"clothes": ["female_casualsuit01", "female_elegantsuit01", "male_casualsuit01", "male_casualsuit03",
                      "male_casualsuit05"],
          "hair": ["bob01", "bob02", "long01", "ponytail01", "braid01", "afro01"]}
SHOES = ["shoes01", "shoes02", "shoes03", "shoes04", "shoes05", "shoes06"]
RACES = ["african", "asian", "caucasian"]


def rng(name):
    return np.random.default_rng(int(hashlib.sha256(f"{SEED}:{name}".encode()).hexdigest()[:8], 16))


def clear():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)


def person_spec(i):
    """M6: a short, slight woman in the skirt outfit with white socks read as a schoolgirl on the motion sheet (brief:
    adults only), so the skirt outfit gets the black ankle boots (shoes03, the only pair without socks), women are
    at least MakeHuman height 0.45 and everyone at least age 0.55 (~32 y)."""
    s = _spec(i)
    if s["clothes"] == "female_elegantsuit01":
        s["shoes"] = "shoes03"
    return s


def _spec(i):
    r = rng(f"person{i}")
    female = i % 2 == 1
    race = RACES[int(r.integers(3))]
    age = float(r.uniform(0.55, 0.85))                     # MakeHuman age: 0.5 = 25 y, 1.0 = 90 y (M6: from ~32 y; see height)
    band = "young" if age < 0.6 else "middleage" if age < 0.75 else "old"
    pool = FEMALE if female else MALE
    return {
        "female": female, "race": race, "age": age,
        "macro": {"gender": 0.0 if female else 1.0, "age": age, "muscle": float(r.uniform(0.35, 0.6)),
                  "weight": float(r.uniform(0.35, 0.8)), "height": float(r.uniform(0.45 if female else 0.35, 0.8)),
                  "proportions": 0.5, "cupsize": 0.5, "firmness": 0.5,
                  "race": {k: (0.9 if k == race else 0.05) for k in RACES}},
        "skin": f"{band}_{race}_{'female' if female else 'male'}",
        "clothes": pool["clothes"][int(r.integers(len(pool["clothes"])))],
        "hair": pool["hair"][int(r.integers(len(pool["hair"])))],
        "shoes": SHOES[int(r.integers(len(SHOES)))],      # replaced below for the skirt outfit
        "eyebrows": f"eyebrow{int(r.integers(1, 13)):03d}",
        "tint": [float(r.uniform(-0.5, 0.5)), float(r.uniform(0.3, 0.85)), float(r.uniform(0.45, 0.95))],  # hue, sat, val: muted, Sunday clothes
        "hair_val": float(r.uniform(0.3, 1.0)) if age < 0.75 else float(r.uniform(0.9, 1.6)),           # grey with age
    }


CLEAN = Path("assets/mpfb/clean").resolve()


def use_clean_texture(obj):
    """Point an outfit's diffuse image at its logo-free copy, where one exists."""
    for slot in obj.material_slots:
        if not slot.material or not slot.material.use_nodes:
            continue
        for n in slot.material.node_tree.nodes:
            if n.type == "TEX_IMAGE" and n.image:
                c = CLEAN / Path(n.image.filepath).name
                if c.exists():
                    n.image = bpy.data.images.load(str(c), check_existing=True)


def tint(obj, hue, sat, val):
    """Shift an asset's diffuse colour: a Hue/Saturation/Value node between its colour source and the shader."""
    for slot in obj.material_slots:
        m = slot.material
        if not m or not m.use_nodes:
            continue
        nt = m.node_tree
        for n in list(nt.nodes):
            if n.type != "BSDF_PRINCIPLED":
                continue
            inp = n.inputs["Base Color"]
            if not inp.is_linked:
                continue
            src = inp.links[0].from_socket
            h = nt.nodes.new("ShaderNodeHueSaturation")
            h.inputs["Hue"].default_value = (0.5 + hue) % 1.0
            h.inputs["Saturation"].default_value = sat
            h.inputs["Value"].default_value = val
            nt.links.new(src, h.inputs["Color"])
            nt.links.new(h.outputs["Color"], inp)


def build_person(spec):
    bm = HumanService.create_human(macro_detail_dict=spec["macro"], scale=0.1)
    rig = HumanService.add_builtin_rig(bm, "mixamo")
    skin = A / "skins" / spec["skin"] / f"{spec['skin']}.mhmat"
    if skin.exists():
        HumanService.set_character_skin(str(skin), bm, skin_type="MAKESKIN")
    add = lambda rel, kind: HumanService.add_mhclo_asset(str(A / rel), bm, asset_type=kind, subdiv_levels=0)
    add(f"eyes/low-poly/low-poly.mhclo", "Eyes")
    add(f"eyebrows/{spec['eyebrows']}/{spec['eyebrows']}.mhclo", "Eyebrows")
    add("eyelashes/eyelashes01/eyelashes01.mhclo", "Eyelashes")
    add(f"clothes/{spec['clothes']}/{spec['clothes']}.mhclo", "Clothes")
    add(f"clothes/{spec['shoes']}/{spec['shoes']}.mhclo", "Clothes")
    if spec["hair"]:
        add(f"hair/{spec['hair']}/{spec['hair']}.mhclo", "Hair")
    for o in [o for o in bpy.data.objects if o.parent in (bm, rig)]:
        if o.type == "MESH" and o.name.endswith(spec["clothes"]):
            use_clean_texture(o)
            tint(o, *spec["tint"])
        if spec["hair"] and o.type == "MESH" and o.name.endswith(spec["hair"]):
            tint(o, 0.0, 1.0 if spec["hair_val"] < 0.9 else 0.25, spec["hair_val"])
    return bm, rig


PHONE_W, PHONE_H, PHONE_T = 0.075, 0.155, 0.008     # phone_mesh
GRIP_ALONG = 0.024   # place_phone: a raised phone's far edge short of the fingers' middle joints
SUPPORT_CLEAR = 0.003   # place_phone: the phone's back above the palm and first finger segments
FREE_CLEAR = 0.006      # place_phone: thumbs clear the phone by this (the scroll glides along it)
WRAP_CLEAR = 0.002      # place_phone: wrapping fingers clear it by this (they hold its edge)
LIFT_MAX = 0.015        # place_phone: the most the phone is lifted off the palm over a finger joint
REACH = 0.06         # place_phone: only what lies within this of the phone's plane can pass through it (not the face)


def phone_mesh():
    """A phone: 7.5 x 15.5 x 0.8 cm dark body, screen inset on its +Z face (emissive 'phone_glow')."""
    if "phone_body" in bpy.data.meshes:
        return bpy.data.meshes["phone_body"]
    me = bpy.data.meshes.new("phone_body")
    w, h, t = 0.075, 0.155, 0.008
    v = [(x * w / 2, y * h / 2, z * t / 2) for z in (-1, 1) for y in (-1, 1) for x in (-1, 1)]
    sw, sh = w / 2 - 0.004, h / 2 - 0.006
    v += [(-sw, -sh, t / 2 + 0.0005), (sw, -sh, t / 2 + 0.0005), (sw, sh, t / 2 + 0.0005), (-sw, sh, t / 2 + 0.0005)]
    f = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5), (8, 9, 10, 11)]
    me.from_pydata(v, [], f)
    body = bpy.data.materials.get("phone_case") or bpy.data.materials.new("phone_case")
    body.use_nodes = True
    body.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.012, 0.012, 0.014, 1)
    body.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.35
    glow = bpy.data.materials.get("phone_glow") or bpy.data.materials.new("phone_glow")
    glow.use_nodes = True
    pr = glow.node_tree.nodes["Principled BSDF"]
    pr.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1)
    pr.inputs["Emission Color"].default_value = (0.78, 0.84, 1.0, 1)
    pr.inputs["Emission Strength"].default_value = 6.0
    me.materials.append(body)
    me.materials.append(glow)
    for i, poly in enumerate(me.polygons):
        poly.material_index = 1 if i == 6 else 0
    return me


def bone_mid(rig, name):
    pb = rig.pose.bones[F.P + name]
    return rig.matrix_world @ ((pb.head + pb.tail) / 2)


def palm_normal(rig, side):
    """The palm's facing (world): which way the curled middle finger bends away from the hand's axis."""
    bpy.context.view_layer.update()
    mw = rig.matrix_world
    h = rig.pose.bones[F.P + f"{side}Hand"]
    d = (mw @ h.tail - mw @ h.head).normalized()
    k, t = mw @ rig.pose.bones[F.P + f"{side}HandMiddle1"].head, mw @ rig.pose.bones[F.P + f"{side}HandMiddle3"].tail
    v = t - k
    return (v - d * v.dot(d)).normalized()


# finger bends for the hands that hold a phone (degrees added to figlib's GRIP, 22° a joint): one hand lays the phone
# on the palm and the fingers' first segments, the middle and end joints wrapping its far long edge onto the screen
# side; two hands cradle it on near-flat fingers, thumbs free over the screen
GRIP_EXTRA = {1: (5.0 - 22, 90.0 - 22, 65.0 - 22), 2: (5.0 - 22, 15.0 - 22, 10.0 - 22)}   # to 5/90/65 and 5/15/10


def grip(rig, pose):
    hands = F.PHONE_HANDS.get(pose, ())
    for h in hands:
        side = h[:-len("Hand")]
        for f in ("Index", "Middle", "Ring", "Pinky"):
            for k, d in zip((1, 2, 3), GRIP_EXTRA[len(hands)]):
                F.bend(rig, f"{side}Hand{f}{k}", d)


def palms_to_eyes(rig, pose):
    """Before the motion loop is keyed (human, M7: "Those hands still don't look like they're holding the phones"):
    roll each phone hand's forearm about its own axis so the palm faces the eyes, the phone can rest on the fingers
    with its screen toward the face. Two passes; the hand follows the forearm."""
    for h in F.PHONE_HANDS.get(pose, ()):
        side = h[:-len("Hand")]
        for _ in range(3):
            bpy.context.view_layer.update()
            mw = rig.matrix_world
            fa = rig.pose.bones[F.P + f"{side}ForeArm"]
            a = (mw @ fa.tail - mw @ fa.head).normalized()
            head = mw @ rig.pose.bones[F.P + "Head"].head
            # held up, filming the stage: the screen faces straight back, level, to the eyes behind it (seen from the
            # booth and the back of the house; aimed down at the eyes it showed only its edge); in the hands: the eyes
            e = Vector((0, 1, 0)) if pose == "phone_up" else head - mw @ rig.pose.bones[F.P + h].tail
            e = (e - a * e.dot(a)).normalized()
            pn = palm_normal(rig, side)
            pn = (pn - a * pn.dot(a)).normalized()
            ang = math.atan2(pn.cross(e).dot(a), pn.dot(e))
            if abs(ang) < math.radians(2):
                break
            m = fa.matrix.copy()                         # armature space; the rig sits at the origin unrotated
            hd = m.translation.copy()
            rot = Matrix.Rotation(ang, 4, rig.matrix_world.inverted().to_3x3() @ a)
            fa.matrix = Matrix.Translation(hd) @ rot @ Matrix.Translation(-hd) @ m


_CHAIN = {}


def chains(o, me):
    """Per evaluated vertex, which part of a hand it moves with: 'support' (palm, the ball of the thumb and the fingers'
    first segments), '<Side>Thumb' (the thumb's last segments), '<Side>Wrap' (a finger's middle or end segment, per finger: '<Side><Finger>Wrap'), or ''
    (not a hand). Cached per mesh data and size."""
    key = (o.data.name, len(me.vertices))
    if key not in _CHAIN:
        names = {g.index: g.name[len(F.P):] for g in o.vertex_groups if g.name.startswith(F.P)}
        lab = np.full(len(me.vertices), "", dtype=object)
        for v in me.vertices:
            gs = [g for g in v.groups if g.group in names]
            if not gs:
                continue
            b = names[max(gs, key=lambda g: g.weight).group]
            side = "Left" if b.startswith("LeftHand") else "Right" if b.startswith("RightHand") else None
            if side is None:
                continue
            # the thumb's base (Thumb1, the ball of the thumb) bears the phone like the palm; its last two segments are free
            lab[v.index] = (f"{side}Thumb" if "Thumb" in b and b[-1] in "234"
                            else f"{side}{b[len(side) + 4:-1]}Wrap" if "Thumb" not in b and b[-1] in "23" else "support")
        _CHAIN[key] = lab
    return _CHAIN[key]


def body_points(meshes):
    """[(world vertex array, chain labels)] for the rendered meshes as they stand (static pose)."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    out = []
    for o in meshes:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        co = np.empty(len(me.vertices) * 3)
        me.vertices.foreach_get("co", co)
        mo = np.array(o.matrix_world)
        out.append((co.reshape(-1, 3) @ mo[:3, :3].T + mo[:3, 3], chains(o, me)))
        ev.to_mesh_clear()
    return out


def phone_frame(rig, hands):
    """The phone's axes (x, y, n: n the screen's facing) and centre, before it is set down on the hand."""
    mw = rig.matrix_world
    sides = [h[:-len("Hand")] for h in hands]
    if len(hands) == 1:
        # held up in one hand, across the palm, as phones are held: the fingers lie along its back and wrap its far
        # long edge; the thumb on the screen side
        pb = rig.pose.bones[F.P + hands[0]]
        w, k = mw @ pb.head, mw @ pb.tail
        x = (k - w).normalized()
        n = palm_normal(rig, sides[0])
        n = (n - x * n.dot(x)).normalized()
        y = n.cross(x).normalized()
        pip = mw @ rig.pose.bones[F.P + f"{sides[0]}HandMiddle2"].head
        return x, y, n, pip - x * (PHONE_W / 2 + GRIP_ALONG)
    # in both hands at the chest: on the plane through both wrists and knuckle lines (least squares), facing the eyes
    pts = [mw @ getattr(rig.pose.bones[F.P + h], e) for h in hands for e in ("head", "tail")]
    l, r = (mw @ rig.pose.bones[F.P + h].tail for h in hands)
    q = np.array([list(p) for p in pts])
    n = Vector(np.linalg.svd(q - q.mean(0))[2][2])
    if n.dot(mw @ rig.pose.bones[F.P + "Head"].head - (l + r) / 2) < 0:
        n = -n
    x = (r - l) - n * (r - l).dot(n)
    x.normalize()
    return x, n.cross(x).normalized(), n, (l + r) / 2


def place_phone(rig, pose, meshes):
    """The phone set into the hands on the static pose (human, M7: "the phones are clipping through everyone's
    wrists"; "look more closely"; "Those hands still don't look like they're holding the phones"). Its back rests on
    the palm and the fingers' first segments (SUPPORT_CLEAR above the highest of them inside its outline); then each
    thumb, and in one hand the wrapping fingers, that would enter the phone is bent the least that clears it
    (FREE_CLEAR, wider than the scrolling thumb's motion). Returns the phone's matrix relative to hands[0]'s pose
    bone, or None. Runs before the motion loop is keyed, so the bends carry into it."""
    hands = F.PHONE_HANDS.get(pose)
    if not hands:
        return None
    sides = [h[:-len("Hand")] for h in hands]
    x, y, n, c = phone_frame(rig, hands)
    B = np.array([list(x), list(y), list(n)])

    def local(pts):
        return (pts - np.array(c)) @ B.T

    def inside(loc, m):
        return (np.abs(loc[:, 0]) < PHONE_W / 2 + m) & (np.abs(loc[:, 1]) < PHONE_H / 2 + m) & (np.abs(loc[:, 2]) < PHONE_T / 2 + m)
    top = -1.0
    for pts, lab in body_points(meshes):
        loc = local(pts)
        sel = (np.abs(loc[:, 0]) < PHONE_W / 2 + SUPPORT_CLEAR) & (np.abs(loc[:, 1]) < PHONE_H / 2 + SUPPORT_CLEAR) & (np.abs(loc[:, 2]) < REACH)
        sel &= np.array([not l.endswith(("Thumb", "Wrap")) for l in lab])   # everything else, sleeves too, stays behind
        if sel.any():
            top = max(top, float(loc[sel, 2].max()))
    c = c + n * (top + PHONE_T / 2 + SUPPORT_CLEAR)

    carriers = {}
    for o, (pts, lab) in zip(meshes, body_points(meshes)):
        for l in set(lab) - {"", "support"}:
            carriers.setdefault(l, []).append(o)

    def hits(chain):
        k = 0
        for pts, lab in body_points(carriers.get(chain, [])):
            k += int(inside(local(pts)[lab == chain], FREE_CLEAR if chain.endswith("Thumb") else WRAP_CLEAR).sum())
        return k
    # a thumb lifts onto the screen at its base joint (Thumb1, two axes); the wrapping fingers at their middle joints
    grid = sorted(((a, b) for a in range(-60, 61, 10) for b in range(-60, 61, 10)), key=lambda t: abs(t[0]) + abs(t[1]))
    free = [(f"{s}Thumb", [[(f"{s}HandThumb1", "X", a), (f"{s}HandThumb1", "Z", b)] for a, b in grid]) for s in sides]
    free += [(f"{s}{f}Wrap", [[(f"{s}Hand{f}{k}", "X", d * w) for k, w in ((2, 1.0), (3, 0.6))]
                               for d in sorted(range(-70, 71, 4), key=abs)])
             for s in sides for f in ("Index", "Middle", "Ring", "Pinky")]
    for _ in range(4):
        stuck = []
        for chain, trials in free:
            if not hits(chain):
                continue
            best = None
            for t in trials:
                for b, ax, d in t:
                    F.bend(rig, b, d, ax)
                if not hits(chain):
                    best = t
                    break
                for b, ax, d in reversed(t):
                    F.bend(rig, b, -d, ax)
            if best is None:
                stuck.append(chain)
            else:
                print(f"PHONE {pose}: {chain} cleared by {[(b, ax, round(d)) for b, ax, d in best]}", flush=True)
        if not stuck:
            break
        # a joint that sits at the phone's back can't bend out of it: lift the phone over it (at most LIFT_MAX) and
        # check every part again
        need = 0.0
        for chain in stuck:
            for pts, lab in body_points(carriers.get(chain, [])):
                loc = local(pts)
                sel = (lab == chain) & inside(loc, WRAP_CLEAR)
                if sel.any():
                    need = max(need, float(loc[sel, 2].max()) + PHONE_T / 2 + WRAP_CLEAR)
        if need > LIFT_MAX:
            print(f"PHONE {pose}: {stuck} can't clear the phone (would need {need:.3f} m)", flush=True)
            break
        c = c + n * need
        print(f"PHONE {pose}: lifted {need:.3f} m over {stuck}", flush=True)
    else:
        print(f"PHONE {pose}: still touching after lifts", flush=True)
    m = Matrix((x, y, n)).transposed().to_4x4()
    m.translation = c
    pb = rig.pose.bones[F.P + hands[0]]
    pm = rig.matrix_world @ pb.matrix @ Matrix.Translation((0, pb.bone.length, 0))   # bone parents sit at the tail
    return pm.inverted() @ m


def attach_phone(rc, pose, coll, rel):
    """The phone on the live rig, parented to the holding hand with the static pose's relation, so it moves with it."""
    hands = F.PHONE_HANDS[pose]
    o = bpy.data.objects.new(f"{coll.name}_phone", phone_mesh())
    coll.objects.link(o)
    o.parent, o.parent_type, o.parent_bone = rc, "BONE", F.P + hands[0]
    o.matrix_parent_inverse = Matrix.Identity(4)
    o.matrix_basis = rel
    bpy.context.view_layer.update()
    mw = o.matrix_world
    return list(mw.translation + (mw.to_3x3() @ Vector((0, 0, 1))).normalized() * 0.005)


def live(rig, objs, coll, pose, i):
    """The person in this pose as a live, animated copy (M6 crowd motion): a copy of the posed rig with the pose's
    motion loop (figlib.animate), and copies of the person's meshes (sharing their mesh data) deformed by it."""
    m = {rig: rig.copy()}
    for o in objs:
        m[o] = o.copy()
    for o, c in m.items():
        coll.objects.link(c)
        if o.parent in m:
            c.parent = m[o.parent]
        for md in c.modifiers:
            if md.type == "ARMATURE" and md.object is rig:
                md.object = m[rig]
    rc = m[rig]
    rc.name = f"{coll.name}_rig"
    F.animate(rc, pose, rng(f"motion{i}{pose}"))
    return rc, [c for o, c in m.items() if o is not rig and c.type == "MESH" and not c.hide_render]


def ground(rc, meshes):
    """The seated rig keeps standing hip height: lift or lower the rig so the feet stand at z = 0."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    z = min((c.matrix_world @ Vector(b)).z for c in meshes for b in c.evaluated_get(dg).bound_box)
    rc.location.z -= z
    bpy.context.view_layer.update()
    return -z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--people", type=int, default=24)
    ap.add_argument("--out", default="assets/figures/figures.blend")
    a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    lib = []
    clear()
    for i in range(a.people):
        spec = person_spec(i)
        before = set(bpy.data.objects)
        bm, rig = build_person(spec)
        mine = [o for o in bpy.data.objects if o not in before]          # this person's body, clothes, hair, eyes
        mine_objs = [o for o in mine if o is not rig]
        rest = {pb.name: pb.matrix_basis.copy() for pb in rig.pose.bones}
        for pose, fn in F.POSES.items():
            for pb in rig.pose.bones:
                pb.matrix_basis = rest[pb.name]
            bpy.context.view_layer.update()
            fn(rig, float(rng(f"pose{i}{pose}").random()))
            F.hands(rig, pose)                                  # per pose: open when raised, a grip only on a phone
            grip(rig, pose)
            palms_to_eyes(rig, pose)
            rel = place_phone(rig, pose, [o for o in mine_objs if o.type == "MESH" and not o.hide_render])
            name = f"fig_{i:02d}_{pose}"
            coll = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(coll)
            rc, live_meshes = live(rig, mine_objs, coll, pose, i)
            dz = ground(rc, live_meshes) if pose in F.SEATED else 0.0
            if pose in F.SEATED:
                coll["seated"] = True
            if rel is not None:
                coll["phone"] = attach_phone(rc, pose, coll, rel)
            coll["person"] = json.dumps(spec)
            lib.append(coll)
            bpy.context.view_layer.layer_collection.children[name].exclude = True    # keep later posing fast
        print(f"person {i}: {spec['skin']}, {spec['clothes']}, hair {spec['hair']}", flush=True)
        # keep only the baked collections; drop the live human before the next one
        for o in mine:
            bpy.data.objects.remove(o)
        keep = set(lib)
        for c in list(bpy.data.collections):
            if c not in keep:
                bpy.data.collections.remove(c)
        for c in lib:
            c.use_fake_user = True
        bpy.ops.outliner.orphans_purge(do_recursive=True)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()), compress=True)
    bpy.ops.file.make_paths_relative()                      # textures stay in assets/mpfb/assets_pack
    bpy.ops.wm.save_mainfile(compress=True)
    print("saved", a.out, len(lib), "collections")


if __name__ == "__main__":
    main()
