"""The board's arms and hands, on real anatomy from the people kit (blender/ep, MIT, from All Systems Operational).

Each member is one right arm cut from a kit figure's body mesh and deformed by that figure's Mixamo rig: never a face or a
torso (brief: "The board: only hands"). The sleeve is the arm's own surface pushed out, with a cuff, so no clothing mesh
or texture comes across. Poses are solved in armature space with the kit's aim(), then keyed as quaternions.

Hands follow the series' rules: flat and open, a bent elbow, the palm's facing coming from the forearm.
"""
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Quaternion, Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "ep"))
import figlib as F  # noqa: E402

FIGS = HERE.parent / "assets" / "figures" / "figures.blend"
P = F.P
CHAIN = ("RightArm", "RightForeArm", "RightHand")
FINGERS = ("Index", "Middle", "Ring", "Pinky")
CUFF_START, SKIN_START = 0.80, 0.87   # along the forearm bone


def _update():
    bpy.context.view_layer.update()


def load_person(idx):
    name = f"fig_{idx:02d}_stand"
    with bpy.data.libraries.load(str(FIGS), link=False) as (_, dst):
        dst.collections = [name]
    c = dst.collections[0]
    rig = next(o for o in c.all_objects if o.type == "ARMATURE")
    body = max((o for o in c.all_objects if o.type == "MESH"), key=lambda o: len(o.data.vertices))
    return rig, body


def arm_mesh(rig, body, name, skin, sleeve, cuff):
    """The right arm alone, from the body mesh's real topology, with materials skin / sleeve / cuff."""
    me = body.data.copy()
    me.name = name
    me.materials.clear()
    for m in (skin, sleeve, cuff):
        me.materials.append(m)
    names = [g.name for g in body.vertex_groups]
    chain = {i for i, n in enumerate(names) if n.startswith((P + "RightArm", P + "RightForeArm", P + "RightHand"))}
    keep = names.index("body")
    fa = rig.data.bones[P + "RightForeArm"]
    head, axis = fa.head_local.copy(), fa.tail_local - fa.head_local
    along = lambda co: (co - head).dot(axis) / axis.length_squared
    bm = bmesh.new()
    bm.from_mesh(me)
    dl = bm.verts.layers.deform.verify()
    bones = {i for i, n in enumerate(names) if n.startswith(P)}
    def on_arm(v):  # the rig's weights aren't normalised, so this is the arm's share of the vertex's total
        total = sum(w for g, w in v[dl].items() if g in bones)
        return keep in v[dl] and total > 0 and sum(w for g, w in v[dl].items() if g in chain) / total >= 0.5
    gone = [v for v in bm.verts if not on_arm(v)]
    bmesh.ops.delete(bm, geom=gone, context="VERTS")
    bm.normal_update()
    moved = []
    for v in bm.verts:
        t = along(v.co)
        if t < CUFF_START:
            moved.append((v, v.normal * 0.011))
        elif t < SKIN_START:
            moved.append((v, v.normal * 0.0135))
    for v, d in moved:
        v.co += d
    for f in bm.faces:
        t = along(f.calc_center_median())
        f.material_index = 1 if t < CUFF_START else 2 if t < SKIN_START else 0
        f.smooth = True
    bm.to_mesh(me)
    bm.free()
    return me


def spawn_rig(rig, name):
    r = rig.copy()
    r.name = name
    r.animation_data_clear()
    bpy.context.scene.collection.objects.link(r)
    for pb in r.pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.matrix_basis = Matrix.Identity(4)
    for f in FINGERS:                        # open and flat, with the small natural curve of a relaxed hand
        for k, deg in ((1, 5), (2, 8), (3, 5)):
            r.pose.bones[f"{P}RightHand{f}{k}"].rotation_quaternion = Matrix.Rotation(math.radians(deg), 4, "Z").to_quaternion()
    return r


def palm_normal(r):
    b = r.pose.bones
    across = b[P + "RightHandIndex1"].head - b[P + "RightHandPinky1"].head
    along = b[P + "RightHandMiddle1"].head - b[P + "RightHand"].head
    return across.cross(along).normalized()


def set_arm(r, upper, fore, hand, palm):
    """Aim the three bones (armature-space directions), then turn the forearm so the palm faces `palm`."""
    for n in CHAIN:
        r.pose.bones[P + n].matrix_basis = Matrix.Identity(4)
    _update()
    F.aim(r, "RightArm", upper)
    F.aim(r, "RightForeArm", fore)
    F.aim(r, "RightHand", hand)
    pb = r.pose.bones[P + "RightForeArm"]
    a = (pb.tail - pb.head).normalized()
    n, want = palm_normal(r), Vector(palm).normalized()
    cur, goal = (n - a * n.dot(a)).normalized(), (want - a * want.dot(a)).normalized()
    ang = math.atan2(a.dot(cur.cross(goal)), cur.dot(goal))
    h = pb.head.copy()
    pb.matrix = Matrix.Translation(h) @ Matrix.Rotation(ang, 4, a) @ Matrix.Translation(-h) @ pb.matrix
    _update()
    F.aim(r, "RightHand", hand)
    return {x: r.pose.bones[P + x].matrix_basis.to_quaternion() for x in CHAIN}


def along(a, b, r):
    """From rotation a toward b by r; r may run past 1, so an arm can overshoot and settle."""
    d = a.rotation_difference(b)
    if d.w < 0:
        d = Quaternion((-d.w, -d.x, -d.y, -d.z))
    axis, angle = d.to_axis_angle()
    return a @ Quaternion(axis, angle * r)


class Member:
    def __init__(self, i, rig_src, me, shoulder, yaw, overhead=False, drop=0.3):
        self.i = i
        self.rig = spawn_rig(rig_src, f"member{i}.rig")
        self.shoulder = Vector(shoulder)
        s = rig_src.data.bones[P + "RightArm"].head_local
        self.rig.rotation_euler = (0, 0, yaw)
        self.rig.location = self.shoulder - Matrix.Rotation(yaw, 3, "Z") @ s
        self.arm = bpy.data.objects.new(f"member{i}.arm", me)
        bpy.context.scene.collection.objects.link(self.arm)
        self.arm.parent = self.rig
        mod = self.arm.modifiers.new("arm", "ARMATURE")
        mod.object = self.rig
        _update()
        v = ((i * 37) % 11) / 10 - 0.5            # a little difference between people, the same every render
        if overhead:  # seen from above: flat on the table, then lifted toward the lens with the whole open hand in view
            fwd = Matrix.Rotation(yaw, 3, "Z") @ Vector((0, -1, 0))
            at = lambda out, z: self.shoulder + fwd * out + Vector((0, 0, z - self.shoulder.z))
            self.down = self.reach(at(0.44, 0.83), (0, 0, -1), hand=(0, -1, -0.02), pole=(-0.9, 0.1, -0.25))
            self.up = self.reach(at(0.40 + 0.02 * v, 1.22 + 0.03 * v), (0, 0, -1), hand=(0, -1, 0.22), pole=(-0.9, 0.1, -0.25))
            return
        self.up = set_arm(self.rig, (-0.26 + 0.07 * v, -0.68, 0.06 + 0.05 * v), (-0.05 + 0.09 * v, -0.2, 0.98),
                          (-0.02 + 0.05 * v, -0.12, 1), (0.05 * v, -1, 0.1))
        # Waiting just under the frame with the elbow bent and the wrist loose, so the raise is a lift of the forearm
        # that the viewer sees all of, and not a whole arm swinging up from far below.
        turn = Matrix.Rotation(yaw, 3, "Z")
        top = self.wrist()
        self.down = self.reach(top + turn @ Vector((0, -0.05, 0)) + Vector((0, 0, -drop)), turn @ Vector((0, -0.5, -0.85)),
                               hand=(0, -0.72, 0.6))

    def pose(self, r):
        for n in CHAIN:
            self.rig.pose.bones[P + n].rotation_quaternion = self.down[n].slerp(self.up[n], r)

    def blend(self, q, w):
        """From the raised pose toward another pose (w = 0 is fully raised), so a move starts with no jump."""
        for n in CHAIN:
            self.rig.pose.bones[P + n].rotation_quaternion = self.up[n].slerp(q[n], w)

    def joints(self, upper, fore, hand):
        """Each joint at its own point between down and up: the shoulder leads, the wrist trails."""
        for n, r in zip(CHAIN, (upper, fore, hand)):
            self.rig.pose.bones[P + n].rotation_quaternion = along(self.down[n], self.up[n], r)

    def fingers(self, curl):
        """0 is open and flat, 1 is the loose curl of a hand at rest."""
        for f in FINGERS:
            for k, (flat, loose) in enumerate(((5, 11), (8, 16), (5, 10)), 1):
                deg = flat + (loose - flat) * curl
                self.rig.pose.bones[f"{P}RightHand{f}{k}"].rotation_quaternion = Quaternion((0, 0, 1), math.radians(deg))

    def sway(self, f, amount):
        """A raised arm is never still: a slow drift at the elbow and wrist, different for each person."""
        p = self.i * 2.399
        t = f / 24
        for n, deg, hz in (("RightForeArm", 1.3, 0.31), ("RightHand", 2.4, 0.47)):
            x = math.radians(deg) * amount * (math.sin(2 * math.pi * hz * t + p) + 0.4 * math.sin(2 * math.pi * hz * 2.3 * t + p * 1.7))
            z = math.radians(deg * 0.7) * amount * math.sin(2 * math.pi * hz * 0.8 * t + p * 0.6)
            pb = self.rig.pose.bones[P + n]
            pb.rotation_quaternion = pb.rotation_quaternion @ Quaternion((1, 0, 0), x) @ Quaternion((0, 0, 1), z)

    def current(self):
        return {n: self.rig.pose.bones[P + n].rotation_quaternion.copy() for n in CHAIN}

    def apply(self, q):
        for n in CHAIN:
            self.rig.pose.bones[P + n].rotation_quaternion = q[n]

    def key(self, frame):
        for n in CHAIN:
            self.rig.pose.bones[P + n].keyframe_insert("rotation_quaternion", frame=frame)
        if frame % 2 == 1:
            for f in FINGERS:
                for k in (1, 2, 3):
                    self.rig.pose.bones[f"{P}RightHand{f}{k}"].keyframe_insert("rotation_quaternion", frame=frame)

    def wrist(self):
        _update()
        return self.rig.matrix_world @ self.rig.pose.bones[P + "RightHand"].head

    def reach(self, target, palm_world, hand=None, pole=(-0.75, 0.15, -0.65)):
        """Two-bone IK: the wrist to a world point, elbow out and down."""
        b = self.rig.data.bones
        l1, l2 = b[P + "RightArm"].length, b[P + "RightForeArm"].length
        rot = self.rig.matrix_world.to_3x3().inverted()
        d = rot @ (Vector(target) - self.shoulder)
        dist = min(d.length, l1 + l2 - 0.005)
        u = d.normalized()
        pole = Vector(pole)
        pole = (pole - u * pole.dot(u)).normalized()
        a = (l1 * l1 - l2 * l2 + dist * dist) / (2 * dist)
        elbow = u * a + pole * math.sqrt(max(l1 * l1 - a * a, 0))
        wrist = u * dist
        fore = wrist - elbow
        return set_arm(self.rig, elbow, fore, hand or (fore.normalized() + Vector((0, 0, 0.5))).normalized(), rot @ Vector(palm_world))


def build(seats, persons, skin, sleeve, cuff, overhead=False, drop=0.3):
    """seats: [(shoulder, yaw)]. Three people's arms in turn, so the hands aren't one hand repeated."""
    kit = []
    for k, idx in enumerate(persons):
        rig, body = load_person(idx)
        kit.append((rig, arm_mesh(rig, body, f"arm_mesh{k}", skin, sleeve, cuff)))
    return [Member(i, *kit[i % len(kit)], sh, yaw, overhead, drop) for i, (sh, yaw) in enumerate(seats)]
