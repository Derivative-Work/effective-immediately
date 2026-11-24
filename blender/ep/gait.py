"""M6 S25a (human: "The walking looks very unnatural"): a walk with planted feet, baked into a walker's own rig.

The library's "walk" loop only rocked the legs (a sine at the hip, a held knee) while the figure slid forward at a
constant speed, so the feet skated. Here, per frame, in the armature's space (the figure faces -Y):
- the hips move forward at a steady speed, sway a little toward the stance foot, and sit as high as the legs reach
  (so they dip at double support, as a real walk does);
- each foot is planted for the stance phase (60% of the cycle, directly under the hips at mid-stance) and swings to
  its next footprint with a lift; feet stay flat;
- the legs are solved by two-bone IK (knee forward), the bones set by pose-space matrices computed here, so nothing
  depends on constraints evaluating on instanced rigs;
- the arms swing opposite the legs; spine and head keep the walk pose.
Every frame is keyed (quaternions; Hips also location)."""
import math

import bpy
from mathutils import Matrix, Quaternion, Vector

P = "mixamorig:"


def _base_quats(rig, f=1):
    """Each bone's rotation at frame f of its current action (the walk pose), else its pose value."""
    out = {}
    act = rig.animation_data.action if rig.animation_data else None
    fcs = {}
    if act is not None:
        import final as FL
        for fc in FL._fc_of(act):
            fcs[(fc.data_path, fc.array_index)] = fc
    for pb in rig.pose.bones:
        path = f'pose.bones["{pb.name}"].rotation_quaternion'
        out[pb.name] = Quaternion([fcs[(path, i)].evaluate(f) if (path, i) in fcs else pb.rotation_quaternion[i]
                                   for i in range(4)])
    return out


def bake(rig, n, speed=0.9, cadence=1.8, phase=0.0, lift=0.08, stance=0.6, arm_deg=13.0, fps=24):
    """Key a walk of n frames on rig. cadence = steps per second; phase in [0, 1) offsets the cycle."""
    B = rig.data.bones
    rest = {b.name: b.matrix_local.copy() for b in B}
    T = 2.0 / cadence * fps                                   # frames per cycle (two steps)
    stride = speed * T / fps
    base = _base_quats(rig)
    hips = P + "Hips"
    legs = {}
    for side, off in (("Left", 0.0), ("Right", 0.5)):
        up, lo, ft = P + side + "UpLeg", P + side + "Leg", P + side + "Foot"
        legs[side] = dict(up=up, lo=lo, ft=ft, off=off, L1=B[up].length, L2=B[lo].length,
                          hip_rel=rest[hips].inverted() @ rest[up],            # the hip joint, in the Hips frame
                          ankle0=rest[ft].translation.copy())
        # footprints near the midline (human, M6: "check the gait width"): the rest pose is an A-pose with the ankles
        # at +-0.19-0.20 m, a 0.4 m straddle; a walk lands the feet ~9 cm apart (centres), here 40% of the hip
        # joint's offset (+-4.4-5 cm)
        hx = rest[up].translation.x - rest[hips].translation.x
        legs[side]["ankle0"].x = rest[hips].translation.x + 0.4 * hx
    fwd = Vector((0, -1, 0))
    ad = rig.animation_data or rig.animation_data_create()
    ad.action = bpy.data.actions.new(rig.name + "_gait")
    for pb in rig.pose.bones:
        pb.rotation_mode = "QUATERNION"

    def foot_at(side, t):
        """Ankle position (armature space) for this side at frame t, and whether it is in stance."""
        lg = legs[side]
        ph = (t / T + phase + lg["off"]) % 1.0
        k = math.floor(t / T + phase + lg["off"])                # which cycle this foot is in
        # stance runs ph in [0, stance): planted where the hips are at mid-stance of this cycle
        t_mid = (k - phase - lg["off"] + stance / 2) * T
        a = lg["ankle0"].copy()
        if ph < stance:
            a.y += -speed * t_mid / fps
            return a, True
        s = (ph - stance) / (1 - stance)                          # swing: from this footprint to the next
        s2 = 0.5 - 0.5 * math.cos(math.pi * s)
        y0, y1 = -speed * t_mid / fps, -speed * (t_mid + T) / fps
        a.y += y0 + (y1 - y0) * s2
        a.z += lift * math.sin(math.pi * s)
        return a, False

    feet_y = {}
    for f in range(1, n + 1):
        t = f - 1
        feet = {s: foot_at(s, t) for s in legs}
        hy = -speed * t / fps
        # sway toward the stance foot
        st = [s for s in legs if feet[s][1]]
        sway = 0.0 if len(st) != 1 else (0.022 if st[0] == "Left" else -0.022) * math.copysign(1, legs["Left"]["ankle0"].x)
        # hip height: as high as both legs reach (99%), never above rest
        hz = rest[hips].translation.z
        for s, lg in legs.items():
            hj0 = (rest[hips] @ lg["hip_rel"]).translation
            a = feet[s][0]
            dxy = Vector((hj0.x + sway - a.x, hj0.y + hy - a.y))
            reach = 0.99 * (lg["L1"] + lg["L2"])
            if dxy.length < reach:
                hz = min(hz, a.z + math.sqrt(reach ** 2 - dxy.length ** 2) + (rest[hips].translation.z - hj0.z))
        Mh = Matrix.Translation(Vector((sway, hy, hz - rest[hips].translation.z))) @ rest[hips]
        pbh = rig.pose.bones[hips]
        bh = rest[hips].inverted() @ Mh
        pbh.location, pbh.rotation_quaternion = bh.translation, base[hips] if False else Quaternion()
        pbh.keyframe_insert("location", frame=f)
        pbh.keyframe_insert("rotation_quaternion", frame=f)
        for s, lg in legs.items():
            Hj = (Mh @ lg["hip_rel"]).translation
            A = feet[s][0]
            d = A - Hj
            dl = min(d.length, lg["L1"] + lg["L2"] - 1e-4)
            u = d.normalized()
            a_ = (lg["L1"] ** 2 - lg["L2"] ** 2 + dl ** 2) / (2 * dl)
            h_ = math.sqrt(max(lg["L1"] ** 2 - a_ ** 2, 0.0))
            nrm = (fwd - fwd.dot(u) * u).normalized()
            K = Hj + u * a_ + nrm * h_
            A = Hj + u * dl
            # thigh: rest orientation turned so its Y runs hip -> knee
            def aim(rest_m, head, tail):
                y0 = rest_m.to_3x3().col[1].normalized()
                q = y0.rotation_difference((tail - head).normalized())
                m = (q.to_matrix() @ rest_m.to_3x3()).to_4x4()
                m.translation = head
                return m
            Mu = aim(rest[lg["up"]], Hj, K)
            Ml = aim(rest[lg["lo"]], K, A)
            Mf = rest[lg["ft"]].to_3x3().to_4x4()
            Mf.translation = A
            # basis = (parent_pose @ parent_rest^-1 @ rest)^-1 @ desired
            for name, M, parent_pose, parent in ((lg["up"], Mu, Mh, hips), (lg["lo"], Ml, Mu, lg["up"]), (lg["ft"], Mf, Ml, lg["lo"])):
                bas = (parent_pose @ rest[parent].inverted() @ rest[name]).inverted() @ M
                pb = rig.pose.bones[name]
                pb.rotation_quaternion = bas.to_quaternion()
                pb.keyframe_insert("rotation_quaternion", frame=f)
        for name in ("Spine", "Spine1", "Spine2", "Neck", "Head", "LeftShoulder", "RightShoulder"):
            pb = rig.pose.bones.get(P + name)
            if pb is not None:
                pb.rotation_quaternion = base[pb.name]
                pb.keyframe_insert("rotation_quaternion", frame=f)
        feet_y[f] = {s: feet[s][0].y for s in legs}
    # arms, second pass: the shoulders' pose orientation (constant: only the hips translate) from an evaluation, then
    # the upper arm hangs a little out from the body and the elbow bends a little forward, both swinging opposite the
    # feet (the left arm forward while the right foot leads)
    sc = bpy.context.scene
    sc.frame_set(1)
    rr = rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
    for side, sgn in (("Left", 1), ("Right", -1)):
        arm, fore, sh = P + side + "Arm", P + side + "ForeArm", P + side + "Shoulder"
        if arm not in rig.pose.bones or sh not in rr.pose.bones:
            continue
        Ms = rr.pose.bones[sh].matrix.copy()
        out = 1 if rest[arm].translation.x > rest[hips].translation.x else -1
        for f in range(1, n + 1):
            fy = feet_y[f]
            other = "Right" if side == "Left" else "Left"
            lead = max(-1.0, min(1.0, (fy[side] - fy[other]) / max(stride / 2, 1e-3)))   # > 0: the other foot leads
            th = -math.radians(arm_deg) * lead
            d1 = Vector((out * 0.12, -0.03, -1.0)).normalized()
            d1 = Matrix.Rotation(th, 3, "X") @ d1
            d2 = Matrix.Rotation(-math.radians(14) + 0.6 * th, 3, "X") @ d1
            Pa = Ms @ rest[sh].inverted() @ rest[arm]
            Ma = (d1 and (rest[arm].to_3x3().col[1].normalized().rotation_difference(d1).to_matrix() @ rest[arm].to_3x3())).to_4x4()
            Ma.translation = Pa.translation
            pb = rig.pose.bones[arm]
            pb.rotation_quaternion = (Pa.inverted() @ Ma).to_quaternion()
            pb.keyframe_insert("rotation_quaternion", frame=f)
            Pf = Ma @ rest[arm].inverted() @ rest[fore]
            Mf = (rest[fore].to_3x3().col[1].normalized().rotation_difference(d2).to_matrix() @ rest[fore].to_3x3()).to_4x4()
            Mf.translation = Pf.translation
            pb = rig.pose.bones[fore]
            pb.rotation_quaternion = (Pf.inverted() @ Mf).to_quaternion()
            pb.keyframe_insert("rotation_quaternion", frame=f)
    return stride
