"""Posing helpers for the MakeHuman (MPFB) figures on the Mixamo rig (blender/make_figures.py).

Figures are built facing -Y (MPFB's default); the character's left is +X. A pose is a dict of bone -> world
direction for the bone's head-to-tail axis (aim), plus optional twists; directions are in the figure's own frame
(-Y forward, +Z up). aim() solves each bone from the root outward, so a forearm aims correctly whatever the upper
arm did. Fingers curl by a local X rotation.
"""
import math

import bpy
from mathutils import Matrix, Vector

P = "mixamorig:"


def aim(rig, bone, direction):
    pb = rig.pose.bones[P + bone]
    bpy.context.view_layer.update()
    m = pb.matrix.copy()                                   # armature space
    cur = (m.to_3x3() @ Vector((0, 1, 0))).normalized()
    want = Vector(direction).normalized()
    q = cur.rotation_difference(want)
    rot = q.to_matrix().to_4x4()
    head = m.translation.copy()
    new = Matrix.Translation(head) @ rot @ Matrix.Translation(-head) @ m
    pb.matrix = new
    bpy.context.view_layer.update()


def bend(rig, bone, deg, axis="X"):
    pb = rig.pose.bones[P + bone]
    pb.rotation_mode = "XYZ"
    r = list(pb.rotation_euler)
    r["XYZ".index(axis)] += math.radians(deg)
    pb.rotation_euler = r
    bpy.context.view_layer.update()


def reset(rig):
    for pb in rig.pose.bones:
        pb.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()


def curl_fingers(rig, deg=35, thumb=15, sides=("Left", "Right")):
    for side in sides:
        for f in ("Index", "Middle", "Ring", "Pinky"):
            for k in (1, 2, 3):
                bend(rig, f"{side}Hand{f}{k}", deg)
        for k in (2, 3):
            bend(rig, f"{side}HandThumb{k}", thumb)


def arm(rig, side, upper, fore, hand=None):
    s = "Left" if side > 0 else "Right"
    aim(rig, f"{s}Arm", upper)
    aim(rig, f"{s}ForeArm", fore)
    if hand:
        aim(rig, f"{s}Hand", hand)


def mirror(v):
    return (-v[0], v[1], v[2])


# --- poses: each takes the rig and a variation u in [0, 1) ------------------------------------------------------

def pose_stand(rig, u):
    for s in (1, -1):
        arm(rig, s, (s * 0.12, -0.02, -1), (s * 0.04, -0.12 - 0.1 * u, -1))
    aim(rig, "Head", (0, -0.15 + 0.1 * u, 1))


def pose_raised(rig, u):
    w = 0.35 + 0.25 * u                                     # how wide the arms open
    for s in (1, -1):
        arm(rig, s, (s * w, -0.25, 0.9), (s * (w - 0.1), -0.3, 0.95), (s * 0.1, -0.35, 1))
    aim(rig, "Neck", (0, 0.05, 1))
    aim(rig, "Head", (0, 0.25, 1))                          # face lifted toward the stage


def pose_raised_one(rig, u):
    arm(rig, 1, (0.35, -0.3, 0.88), (0.25, -0.35, 0.95), (0.1, -0.35, 1))
    arm(rig, -1, (-0.12, -0.05, -1), (-0.05, -0.2, -1))
    aim(rig, "Head", (0, 0.15, 1))


def pose_phone(rig, u):
    """Phone held at chest height in both hands, head bowed over it."""
    for s in (1, -1):
        arm(rig, s, (s * 0.1, -0.3, -0.95), (-s * 0.55, -0.8, 0.3), (-s * 0.35, -0.9, 0.3))
    aim(rig, "Neck", (0, -0.25, 1))
    aim(rig, "Head", (0, -0.75 - 0.2 * u, 1))


def pose_phone_up(rig, u):
    """One hand high, filming or showing the phone; the other arm down."""
    arm(rig, -1, (-0.25, -0.5, 0.82), (-0.08, -0.55, 0.83), (0, 0.12, 1))   # wrist bent back: the phone upright (M7)
    arm(rig, 1, (0.12, -0.03, -1), (0.05, -0.15, -1))
    aim(rig, "Head", (0, -0.1, 1))


def pose_bowed(rig, u):
    aim(rig, "Spine1", (0, -0.12, 1))
    for s in (1, -1):
        arm(rig, s, (s * 0.15, -0.3, -0.95), (-s * 0.5, -0.85, 0.15))
    aim(rig, "Neck", (0, -0.3, 1))
    aim(rig, "Head", (0, -0.9, 1))


def pose_walk(rig, u):
    """Walking away from the camera in S25a (the figure is turned 180 degrees in the set). Neutral legs and arms:
    the stride itself is the motion loop (_channels "walk")."""
    for s in (1, -1):
        arm(rig, s, (s * 0.12, -0.02, -1), (s * 0.05, -0.12, -1))
    aim(rig, "Head", (0, -0.1, 1))


def pose_seated_phone(rig, u):
    """Seated, phone in the lap, head down (S29). Hips stay at the rig's root; the set lowers the figure."""
    for s, side in ((1, "Left"), (-1, "Right")):
        aim(rig, f"{side}UpLeg", (s * 0.08, -1, -0.05))
        aim(rig, f"{side}Leg", (s * 0.02, -0.1, -1))
        aim(rig, f"{side}Foot", (0, -1, -0.3))
    for s in (1, -1):
        arm(rig, s, (s * 0.08, -0.35, -0.92), (-s * 0.55, -0.82, 0.15), (-s * 0.35, -0.92, 0.15))
    aim(rig, "Neck", (0, -0.35, 1))
    aim(rig, "Head", (0, -1.0, 1))


def pose_seated_play(rig, u):
    """Seated at the piano or the kit (the band): hands forward at keyboard height, head level."""
    for s, side in ((1, "Left"), (-1, "Right")):
        aim(rig, f"{side}UpLeg", (s * 0.1, -1, -0.05))
        aim(rig, f"{side}Leg", (s * 0.02, -0.15, -1))
        aim(rig, f"{side}Foot", (0, -1, -0.3))
    for s in (1, -1):
        arm(rig, s, (s * 0.12, -0.45, -0.88), (s * 0.05, -1, 0.05), (0, -1, -0.2))
    aim(rig, "Head", (0, -0.25, 1))


POSES = {"stand": pose_stand, "raised": pose_raised, "raised_one": pose_raised_one, "phone": pose_phone,
         "phone_up": pose_phone_up, "bowed": pose_bowed, "walk": pose_walk, "seated_phone": pose_seated_phone,
         "seated_play": pose_seated_play}
SEATED = {"seated_phone", "seated_play"}
# Finger curl per pose, (degrees per finger joint, thumb), as (left, right) (human, M6: the hands "look like they're
# trying to awkwardly grasp something. I'd expect fully open, flat hands, especially for the ones waving"). Until then
# every pose had 22/10, about 66 degrees over a finger's three joints. Raised hands are open and flat; hanging hands
# relax with a slight curl; only hands holding a phone or playing keep a grip.
OPEN, RELAXED, GRIP, PLAY = (0.0, 0.0), (6.0, 3.0), (22.0, 10.0), (12.0, 6.0)
HANDS = {"stand": (RELAXED, RELAXED), "raised": (OPEN, OPEN), "raised_one": (OPEN, RELAXED), "phone": (GRIP, GRIP),
         "phone_up": (RELAXED, GRIP), "bowed": (RELAXED, RELAXED), "walk": (RELAXED, RELAXED),
         "seated_phone": (GRIP, GRIP), "seated_play": (PLAY, PLAY)}


def hands(rig, pose):
    for side, (deg, thumb) in zip(("Left", "Right"), HANDS[pose]):
        if deg or thumb:
            curl_fingers(rig, deg, thumb, sides=(side,))


# which hand bones hold the phone, per pose (the phone sits between their tails)
PHONE_HANDS = {"phone": ("LeftHand", "RightHand"), "phone_up": ("RightHand",), "seated_phone": ("LeftHand", "RightHand")}


# --- motion (M6, human: crowd motion): a looping action per person and pose, layered on the pose -------------------
# Every channel is a sine with a whole number of cycles in the loop, so the action repeats seamlessly (F-curve cycles
# modifier). Each person draws their own periods and phases, so the room doesn't sway in step. Rotations are small
# local offsets (degrees) on top of the pose: X bends a Mixamo bone forward/back, Z sideways, Y twists it.
PERIOD = 240                     # frames (10 s at 24 fps): the unit the channels count cycles in
LOOP = 480                       # the keyed loop: two PERIODs (24 beats, 6 bars), so a sway over two bars (1.5
                                 # cycles per PERIOD) still repeats whole within the loop
KNEE = 1.0                       # sign of a knee bend about the Leg bone's X (checked on the motion sheet)
STEP = 4                         # key every 4 frames, Bezier between


BEAT = PERIOD / 12               # the song is 71.8 bpm: a beat is 20.06 frames, so a PERIOD holds 12 beats (3 bars)
                                 # to within 0.7 frame; shots.py lines loop frame 0 up with a downbeat in every shot


def _beat_phase(k, lag):
    """Phase that puts a k-cycle sine's peak lag beats after loop frame 0 (a downbeat)."""
    return math.pi / 2 - 2 * math.pi * k * lag * BEAT / PERIOD


def _on_beat(r):
    """Sway for raised hands, as a worship crowd moves (human, M6: a full sway "once every other bar (the most
    common)"; once a beat "not many do this, but it is present"). Cycles per PERIOD (12 beats):
      45%  k 1.5: a full sway over two bars, a side on each downbeat
      25%  k 3:   over one bar, a side on 1 and on 3
      10%  k 6:   a side on every beat
      20%  their own slower time (k 1, 2 or 2.5, any phase)
    The locked ones sit a little behind the beat by their own amount (mean 0.08 beat, spread 0.12).
    Returns (cycles per PERIOD, phase, locked)."""
    u = float(r.random())
    lag = float(r.normal(0.08, 0.12))
    for cut, k in ((0.45, 1.5), (0.70, 3), (0.80, 6)):
        if u < cut:
            return k, _beat_phase(k, lag), True
    return float(r.choice([1.0, 2.0, 2.5])), float(r.uniform(0, 2 * math.pi)), False


def _channels(pose, r):
    """bone -> list of (axis, amplitude deg, cycles per loop, phase) for this pose; r: the person's numpy rng."""
    ks = int(r.integers(3, 7))                     # body sway: 3..6 cycles per 10 s (3.3 .. 1.7 s)
    ph = float(r.uniform(0, 2 * math.pi))
    sway = float(r.uniform(1.2, 2.6))
    ch = {}
    locked = False
    if pose in ("raised", "raised_one"):             # M6 (human: waving "roughly (but not exactly) follow the beat")
        ks, ph, locked = _on_beat(r)

    def add(b, axis, amp, k, phase):
        ch.setdefault(b, []).append((axis, amp, k, phase))
    standing = pose in ("stand", "raised", "raised_one", "phone", "phone_up", "bowed")
    if standing:
        add("Hips", "Z", 0.6 * sway, ks, ph)                       # weight shift
        add("Spine", "Z", -0.8 * sway, ks, ph)
        add("Spine1", "Z", 0.9 * sway, ks, ph + 0.4)
        add("Spine1", "X", 0.6, 3, float(r.uniform(0, 6.3)))      # breathing
    if pose in ("stand",):
        add("Head", "X", 2.5, int(r.integers(4, 9)), float(r.uniform(0, 6.3)))   # singing, nodding
        add("Head", "Z", 2.0, ks, ph + 0.8)
        for s in ("Left", "Right"):
            add(f"{s}Arm", "X", 2.0, ks, ph + (0 if s == "Left" else math.pi))
    if pose in ("raised", "raised_one"):
        arms = ("Left", "Right") if pose == "raised" else ("Left",)
        a = float(r.uniform(5, 10))
        # arms sway side to side with the body; on the beat, the arm lands on the person's beat (ph) and the forearm
        # trails it a little (a negative offset is later), otherwise the free-time offsets as before
        da, dx, df = (0.0, 2.0, -0.35) if locked else (0.6, 2.0, 1.1)
        for s in arms:
            add(f"{s}Arm", "Z", a, ks, ph + da)
            add(f"{s}Arm", "X", 0.25 * a if locked else 0.4 * a, ks, ph + dx)
            add(f"{s}ForeArm", "Z", 0.6 * a, ks, ph + df)
            add(f"{s}Hand", "X", 8.0, ks * 2, ph)                    # the wrist turns at each end of the sway
        add("Head", "Z", 3.0, ks, ph + 0.9)
        add("Head", "X", 2.0, int(r.integers(4, 9)), float(r.uniform(0, 6.3)))
    if pose in ("phone", "seated_phone"):
        add("Head", "X", 2.0, int(r.integers(2, 5)), float(r.uniform(0, 6.3)))
        add("Head", "Z", 1.5, 1, float(r.uniform(0, 6.3)))
        for s in ("Left", "Right"):                     # in step: both hands hold one phone (M7, human: no clipping)
            add(f"{s}ForeArm", "X", 1.5, 2, ph)
        # scrolling on the outer thumb joints, which glide along the screen (M7: at the base joint the thumb dug in)
        add("RightHandThumb3", "X", 8.0, int(r.integers(14, 24)), float(r.uniform(0, 6.3)))
        add("RightHandThumb2", "X", 6.0, int(r.integers(14, 24)), float(r.uniform(0, 6.3)))
    if pose == "phone_up":
        add("LeftArm", "Z", 2.5, ks, ph + 0.5)                     # holding it up, drifting
        add("LeftForeArm", "X", 2.0, 2, ph + 1.3)
        add("Head", "X", 1.5, 3, float(r.uniform(0, 6.3)))
    if pose == "bowed":
        add("Head", "X", 1.5, 2, float(r.uniform(0, 6.3)))
        add("Neck", "X", 1.0, 3, float(r.uniform(0, 6.3)))
    if pose == "seated_phone":
        add("Spine1", "X", 0.8, 3, float(r.uniform(0, 6.3)))       # breathing
    if pose == "seated_play":
        add("Spine", "Z", 2.0, ks, ph)
        add("Head", "Z", 4.0, ks, ph + 0.5)
        add("Head", "X", 3.0, int(r.integers(6, 10)), float(r.uniform(0, 6.3)))
        for s in ("Left", "Right"):
            add(f"{s}ForeArm", "Z", 4.0, int(r.integers(7, 12)), float(r.uniform(0, 6.3)))   # moving along the keys
            add(f"{s}Hand", "X", 6.0, int(r.integers(20, 40)), float(r.uniform(0, 6.3)))
            for f in ("Index", "Middle", "Ring"):
                add(f"{s}Hand{f}1", "X", 12.0, int(r.integers(30, 60)), float(r.uniform(0, 6.3)))
    if pose == "walk":
        # a walk cycle: 9 strides per loop (1.11 s each, ~1.2 m/s with the set's step length). The base pose is
        # mid-stride; these swing each leg and arm through the cycle around it.
        k, p0 = 9, float(r.uniform(0, 2 * math.pi))
        for s, sgn in (("Left", 1), ("Right", -1)):
            add(f"{s}UpLeg", "X", 22.0 * sgn, k, p0)
            add(f"{s}Leg", "X", KNEE * 18.0, 0, math.pi / 2)                       # held bend: the knee
            add(f"{s}Leg", "X", KNEE * 18.0, k, p0 + (0 if s == "Left" else math.pi) + math.pi / 2)   # only flexes
            add(f"{s}Arm", "X", -10.0 * sgn, k, p0)
        add("Hips", "Y", 4.0, k, p0)
        add("Spine1", "Y", -3.0, k, p0)
        add("Head", "X", 1.0, 2 * k, p0)
    return ch


def animate(rig, pose, r):
    """Key the pose's motion loop on rig (already posed). Returns the action."""
    from mathutils import Euler
    ch = _channels(pose, r)
    rig.animation_data_create()
    act = bpy.data.actions.new(f"{rig.name}_loop")
    rig.animation_data.action = act
    base = {}
    for b in ch:
        pb = rig.pose.bones.get(P + b)
        if pb is None:
            continue
        pb.rotation_mode = "QUATERNION"
        base[b] = pb.rotation_quaternion.copy()
    for f in range(0, LOOP + 1, STEP):
        for b, chans in ch.items():
            if b not in base:
                continue
            e = [0.0, 0.0, 0.0]
            for axis, amp, k, phase in chans:
                e["XYZ".index(axis)] += math.radians(amp) * math.sin(2 * math.pi * k * f / PERIOD + phase)
            pb = rig.pose.bones[P + b]
            pb.rotation_quaternion = base[b] @ Euler(e).to_quaternion()
            pb.keyframe_insert("rotation_quaternion", frame=f + 1)
    for fc in _fcurves(act):
        fc.modifiers.new("CYCLES")
    for b in base:                                   # leave the pose at its base when the action is off
        rig.pose.bones[P + b].rotation_quaternion = base[b]
    return act


def _fcurves(act):
    if hasattr(act, "fcurves") and len(getattr(act, "fcurves", [])):
        return list(act.fcurves)
    out = []                                         # Blender 4.4+ layered actions
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for bag in strip.channelbags:
                out += list(bag.fcurves)
    return out
