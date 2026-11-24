"""The board, on real anatomy from the people kit (blender/ep, MIT, from All Systems Operational).

Each member is a whole kit person seated at the table in near-black, so it's clear whose hand is going up (human note:
it was "unclear where the hands are supposed to be coming from"). The camera sees them from behind, from above or against
bright glass, and nothing above the wrists is lit enough to show a feature: no faces. Only the hands carry a little form.
Poses are solved in armature space with the kit's aim(), then keyed as quaternions.

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


def _update():
    bpy.context.view_layer.update()


def load_person(idx):
    name = f"fig_{idx:02d}_stand"
    with bpy.data.libraries.load(str(FIGS), link=False) as (_, dst):
        dst.collections = [name]
    c = dst.collections[0]
    rig = next(o for o in c.all_objects if o.type == "ARMATURE")
    return rig, [o for o in c.all_objects if o.type == "MESH"]


def person_parts(meshes, tag, skin, black):
    """All of a kit person's meshes in near-black, with the hands alone in the slightly lighter material."""
    body = max(meshes, key=lambda o: len(o.data.vertices))
    parts = []
    for n, o in enumerate(meshes):
        me = o.data.copy()
        me.name = f"{tag}.{n}"
        me.materials.clear()
        me.materials.append(black)
        if o is body:
            me.materials.append(skin)
            names = [g.name for g in o.vertex_groups]
            bones = {i for i, x in enumerate(names) if x.startswith(P)}
            hands = {i for i, x in enumerate(names) if x.startswith((P + "RightHand", P + "LeftHand"))}
            bm = bmesh.new()
            bm.from_mesh(me)
            dl = bm.verts.layers.deform.verify()
            def share(v):
                total = sum(w for g, w in v[dl].items() if g in bones)
                return sum(w for g, w in v[dl].items() if g in hands) / total if total else 0.0
            for f in bm.faces:
                f.material_index = 1 if sum(share(v) for v in f.verts) / len(f.verts) > 0.5 else 0
                f.smooth = True
            bm.to_mesh(me)
            bm.free()
        else:
            for p in me.polygons:
                p.material_index = 0
        parts.append((o, me))
    return parts


def seat_pose(r, v, overhead=False):
    """Sitting up at the table, the left forearm resting on it (in the lap from overhead, so only a raised hand shows)."""
    for k, side in ((1, "Left"), (-1, "Right")):
        F.aim(r, f"{side}UpLeg", (k * 0.1, -1, -0.04))
        F.aim(r, f"{side}Leg", (k * 0.03, -0.08, -1))
        F.aim(r, f"{side}Foot", (k * 0.05, -1, -0.25))
    F.aim(r, "Spine", (0, -0.06, 1))
    F.aim(r, "Neck", (0, -0.12, 1))
    F.aim(r, "Head", (0.05 * v, -0.3, 1))
    if overhead:
        F.arm(r, 1, (0.12, -0.15, -0.98), (-0.25, -0.85, -0.46), (-0.15, -0.85, -0.5))
    else:
        F.arm(r, 1, (0.16, -0.46, -0.87), (-0.28, -0.96, 0.02), (-0.18, -0.98, 0.0))


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
    def __init__(self, i, rig_src, parts, seat, yaw, overhead=False, table_z=0.775):
        self.i = i
        self.rig = spawn_rig(rig_src, f"member{i}.rig")
        turn = Matrix.Rotation(yaw, 3, "Z")
        self.rig.rotation_euler = (0, 0, yaw)
        self.rig.location = Vector(seat) - turn @ rig_src.data.bones[P + "Hips"].head_local
        for k, (o, me) in enumerate(parts):
            x = o.copy()
            x.data = me
            x.name = f"member{i}.part{k}"
            x.animation_data_clear()
            bpy.context.scene.collection.objects.link(x)
            x.parent = self.rig
            x.matrix_parent_inverse = Matrix.Identity(4)
            for mod in x.modifiers:
                if mod.type == "ARMATURE":
                    mod.object = self.rig
        _update()
        v = ((i * 37) % 11) / 10 - 0.5            # a little difference between people, the same every render
        seat_pose(self.rig, v, overhead)
        self.shoulder = self.rig.matrix_world @ self.rig.pose.bones[P + "RightArm"].head
        fwd = turn @ Vector((0, -1, 0))
        at = lambda out, z: self.shoulder + fwd * out + Vector((0, 0, z - self.shoulder.z))
        out_pole = (-0.9, 0.1, -0.25)
        if overhead:   # from above, a hand in the lap is out of sight; the vote brings the whole open hand out over the bright table
            self.down = self.reach(at(0.12, table_z - 0.1), (0, 0, -1), hand=(0, -0.8, -0.6), pole=out_pole)
            self.up = self.reach(at(0.46 + 0.02 * v, self.shoulder.z + 0.12 + 0.03 * v), (0, 0, -1), hand=(0, -1, 0.12), pole=out_pole)
        else:          # flat on the table, then beside the head on a bent elbow: upper arm out, forearm upright
            self.down = self.reach(at(0.38, table_z + 0.045), (0, 0, -1), hand=(0, -1, -0.02), pole=out_pole)
            self.up = set_arm(self.rig, (-0.7 + 0.06 * v, -0.46, -0.16 + 0.05 * v), (-0.06 + 0.08 * v, -0.14, 0.99),
                              (-0.02 + 0.05 * v, -0.08, 1), (0.05 * v, -1, 0.1))

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


def build(seats, persons, skin, black, overhead=False, table_z=0.775):
    """seats: [(hips, yaw)]. A few kit people in turn, so the board isn't one person repeated."""
    kit = []
    for k, idx in enumerate(persons):
        rig, meshes = load_person(idx)
        kit.append((rig, person_parts(meshes, f"person{k}", skin, black)))
    return [Member(i, *kit[i % len(kit)], hips, yaw, overhead, table_z) for i, (hips, yaw) in enumerate(seats)]
