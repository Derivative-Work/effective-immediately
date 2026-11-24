"""M7 (human, 2026-11-14: "also fix the drums and anything else on stage that's clearly still gray box"): the band's
instruments and stage gear for the final look, modelled procedurally, each fitted to the player who uses it.

The band faces upstage (+Y), backs to the house (sanctuary.band, M6), so every instrument sits on its player's +Y side.
Player positions are sanctuary.band's; hands, hips and feet were measured on the figure library (people 44 and 36,
seated_play; 24, stand) so the keys sit under the pianist's hands, the bench and the drum stool under the hips, the
kick and hi-hat pedals under the drummer's feet, and the guitar on the guitarist. No brands, logos or text anywhere.

The grey-box path (animatic, sanctuary.band without "final") is unchanged.
"""
import math

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

from lib import gb


# ---------------------------------------------------------------- materials

def mats(M):
    return {
        "lacquer": M["piano"],
        "black": gb.mat("prop_black", "#0c0c0e", 0.45),
        "hw": gb.mat("prop_hw", "#1a1a1c", 0.35, metal=0.7),                 # powder-coated hardware
        "chrome": gb.mat("prop_chrome", "#d6d8dc", 0.12, metal=1.0),
        "shell": gb.mat("drum_shell", "#5c1119", 0.15),                      # wine-red lacquer
        "head": gb.mat("drum_head", "#e6e1d4", 0.55),                        # coated heads
        "bronze": gb.mat("cymbal_bronze", "#b48a3e", 0.28, metal=1.0),
        "ivory": gb.mat("keys_white", "#eeeae0", 0.3),
        "ebony": gb.mat("keys_black", "#060606", 0.25),
        "plate": gb.mat("piano_plate", "#8f6f32", 0.4, metal=0.85),
        "felt": gb.mat("piano_felt", "#4a1012", 0.95),
        "paper": gb.mat("sheet_music", "#e8e2d2", 0.9),
        "tolex": gb.mat("tolex", "#121213", 0.75),
        "cloth": gb.mat("grille_cloth", "#2b2824", 0.95),
        "lcd": gb.mat("synth_lcd", "#3f6f9a", 0.4, emit=0.6),
        "body": gb.mat("guitar_body", "#6e2410", 0.12),                      # a dark cherry burst
        "guard": gb.mat("guitar_guard", "#e9e3d6", 0.35),
        "neck": gb.mat("guitar_neck", "#7a5230", 0.45),
        "board": gb.mat("guitar_board", "#24160d", 0.5),
        "strap": gb.mat("guitar_strap", "#1b1512", 0.8),
        "rubber": gb.mat("prop_rubber", "#050505", 0.9),
        "stick": gb.mat("drum_stick", "#c9a676", 0.55),
    }


class Props(gb.Builder):
    """gb.Builder plus the shapes the gear needs: oriented cylinders and open tubes, prisms from 2D outlines."""

    def __init__(self, P):
        self.P = P
        self.keys = list(P)
        super().__init__([P[k] for k in self.keys])

    def mi(self, k):
        return self.keys.index(k)

    def cyl(self, center, r, h, k, axis=(0, 0, 1), r2=None, caps=True, segs=24):
        res = bmesh.ops.create_cone(self.bm, cap_ends=caps, segments=segs, radius1=r, radius2=r if r2 is None else r2, depth=h)
        rot = Vector((0, 0, 1)).rotation_difference(Vector(axis).normalized()).to_matrix().to_4x4()
        self._tag(res["verts"], self.mi(k), Matrix.Translation(center) @ rot)

    def rod(self, a, b, r, k, segs=10):
        a, b = Vector(a), Vector(b)
        self.cyl((a + b) / 2, r, (b - a).length, k, axis=b - a, segs=segs)

    def bx(self, center, size, k, rot=(0, 0, 0)):
        self.box(center, size, self.mi(k), rot)

    def prism(self, outline, depth, k, frame, k_top=None):
        """outline: [(a, b)] in the frame's first two axes; extruded depth along its third; frame = (origin, ax, bx, cx)."""
        o, ax, bx_, cx = (Vector(v) for v in frame)
        bot = [self.bm.verts.new(o + ax * a + bx_ * b) for a, b in outline]
        top = [self.bm.verts.new(o + ax * a + bx_ * b + cx * depth) for a, b in outline]
        fs = [self.bm.faces.new(list(reversed(bot))), self.bm.faces.new(top)]
        n = len(outline)
        for i in range(n):
            fs.append(self.bm.faces.new([bot[i], bot[(i + 1) % n], top[(i + 1) % n], top[i]]))
        for f in fs:
            f.material_index = self.mi(k)
        if k_top:
            fs[1].material_index = self.mi(k_top)
        bmesh.ops.recalc_face_normals(self.bm, faces=fs)

    def tripod(self, x, y, z0, top, r=0.28, k="hw"):
        """A stand: three splayed legs to a collar, a pole up to `top` (stage-relative z)."""
        collar = z0 + 0.28
        for i in range(3):
            a = math.radians(90 + 120 * i)
            self.rod((x + r * math.cos(a), y + r * math.sin(a), z0 + 0.01), (x, y, collar), 0.009, k)
            self.cyl((x + r * math.cos(a), y + r * math.sin(a), z0 + 0.012), 0.014, 0.024, "rubber", segs=8)
        self.rod((x, y, z0), (x, y, top), 0.011, k)
        self.cyl((x, y, collar), 0.02, 0.05, k, segs=12)


def bezier(p0, p1, p2, p3, n=10):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = (np.array(p) for p in (p0, p1, p2, p3))
    return [tuple(v) for v in (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3]


def drum(B, c, r, depth, axis, k_head="head", resonant="head"):
    """A drum: lacquered shell, a head at each end with a chrome hoop, and tension lugs around the shell."""
    ax = Vector(axis).normalized()
    c = Vector(c)
    B.cyl(c, r, depth, "shell", axis=ax, caps=False, segs=32)
    for s, kh in ((1, k_head), (-1, resonant)):
        e = c + ax * (s * depth / 2)
        B.cyl(e, r * 0.995, 0.004, kh, axis=ax, segs=32)
        B.cyl(e - ax * (s * 0.006), r + 0.007, 0.022, "chrome", axis=ax, caps=False, segs=32)
    side = ax.orthogonal().normalized()
    n = 8 if r < 0.25 else 10
    for i in range(n):
        d = Matrix.Rotation(2 * math.pi * i / n, 3, ax) @ side
        p = c + d * (r + 0.012)
        B.rod(p - ax * depth * 0.3, p + ax * depth * 0.3, 0.006, "chrome", segs=6)


def cymbal(B, c, r, tilt_axis=(1, 0, 0), tilt=0.0):
    """A cymbal: a shallow bronze cone with a bell, tilted toward the player."""
    up = Matrix.Rotation(tilt, 3, Vector(tilt_axis)) @ Vector((0, 0, 1))
    c = Vector(c)
    B.cyl(c, r, 0.012, "bronze", axis=up, r2=r * 0.25, segs=36)
    B.cyl(c + up * 0.012, r * 0.22, 0.02, "bronze", axis=up, r2=r * 0.08, segs=20)


# ---------------------------------------------------------------- the instruments

def grand_piano(B, x, ky, y0):
    """A grand piano, keyboard front edge at y = ky, centred on x, facing the player at -Y; the curved bentside on
    the player's right (+X), the lid open on that side on its prop stick."""
    def p(u, v, z):
        return (x + u, ky + v, y0 + z)
    # keyboard: 52 white keys, the black keys in twos and threes, cheeks, key slip, key bed
    W = 1.23
    kw = W / 52
    for i in range(52):
        B.bx(p(-W / 2 + kw * (i + 0.5), 0.075, 0.73), (kw - 0.0012, 0.15, 0.022), "ivory")
    for i in range(51):
        if i % 7 in (2, 6):                 # no black key between E-F and B-C (starting from A0: A B | C ...)
            continue
        B.bx(p(-W / 2 + kw * (i + 1), 0.11, 0.748), (kw * 0.55, 0.095, 0.02), "ebony")
    for s in (-1, 1):
        B.bx(p(s * (W / 2 + 0.035), 0.08, 0.735), (0.07, 0.2, 0.09), "lacquer")
    B.bx(p(0, -0.012, 0.705), (W + 0.14, 0.025, 0.05), "lacquer")              # key slip
    B.bx(p(0, 0.08, 0.675), (W + 0.14, 0.2, 0.05), "lacquer")                  # key bed
    B.bx(p(0, 0.18, 0.79), (W, 0.03, 0.11), "lacquer")                         # fallboard, open
    B.bx(p(0, 0.165, 0.737), (W, 0.01, 0.012), "felt")                         # the red felt strip
    # the case: straight side on the player's left, bentside on the right, rounded tail; plate gold inside
    out = [(-0.74, 0.2), (0.74, 0.2), (0.74, 0.55)]
    out += bezier((0.74, 0.55), (0.74, 1.05), (0.12, 1.1), (0.06, 1.62))[1:]
    out += bezier((0.06, 1.62), (0.02, 1.98), (-0.48, 2.02), (-0.74, 1.96))[1:]
    B.prism(out, 0.33, "lacquer", ((x, ky, y0 + 0.64), (1, 0, 0), (0, 1, 0), (0, 0, 1)), k_top="plate")
    # lid, hinged along the straight side, open 32 degrees, and its prop stick
    th = math.radians(32)
    hinge_u, hz = -0.74, 0.985
    lid = out
    o = Vector((x + hinge_u, ky, y0 + hz))
    au = Vector((math.cos(th), 0, math.sin(th)))
    B.prism([(u - hinge_u, v) for u, v in lid], 0.02, "lacquer", (o, au, (0, 1, 0), (-math.sin(th), 0, math.cos(th))))
    pu, pv = 0.5, 1.0
    tip = o + au * (pu - hinge_u) + Vector((0, pv, 0))
    B.rod(p(0.62, pv, 0.975), tip, 0.008, "lacquer")
    # music desk with a sheet of music
    B.bx(p(0, 0.34, 1.12), (0.78, 0.015, 0.27), "lacquer", rot=(math.radians(-14), 0, 0))
    B.bx(p(0, 0.33, 1.13), (0.46, 0.004, 0.25), "paper", rot=(math.radians(-14), 0, 0))
    # legs, casters, lyre and pedals
    for u, v in ((-0.66, 0.3), (0.66, 0.3), (-0.42, 1.78)):
        B.cyl(p(u, v, 0.33), 0.07, 0.62, "lacquer", r2=0.08, segs=16)
        B.cyl(p(u, v, 0.012), 0.03, 0.024, "chrome", axis=(1, 0, 0), segs=10)
    for s in (-1, 1):
        B.bx(p(s * 0.09, 0.5, 0.37), (0.035, 0.035, 0.55), "lacquer")
    B.bx(p(0, 0.5, 0.06), (0.32, 0.12, 0.05), "lacquer")
    for s in (-1, 0, 1):
        B.bx(p(s * 0.07, 0.42, 0.06), (0.03, 0.12, 0.012), "chrome", rot=(math.radians(-8), 0, 0))


def piano_bench(B, x, y, y0):
    B.bx((x, y, y0 + 0.47), (0.82, 0.34, 0.06), "black")
    B.bx((x, y, y0 + 0.505), (0.78, 0.30, 0.012), "rubber")                    # the padded top
    for sx in (-1, 1):
        for sy in (-1, 1):
            B.bx((x + sx * 0.36, y + sy * 0.13, y0 + 0.22), (0.04, 0.04, 0.44), "lacquer")


def drum_kit(B, x, y, y0, present=True):
    """The kit around a drummer seated at (x, y) facing +Y: stool under the hips (0.66 m), kick pedal under the right
    foot and hi-hat pedal under the left (feet at +/-0.18, 0.54 m ahead), snare between the knees, toms, cymbals."""
    def p(dx, dy, z):
        return (x + dx, y + dy, y0 + z)
    # stool
    B.cyl(p(0, 0, 0.56), 0.18, 0.08, "black", segs=24)
    B.tripod(x, y, y0, y0 + 0.52, r=0.26)
    # kick drum with its pedal and spurs
    kx = 0.14
    drum(B, p(kx, 0.86, 0.29), 0.28, 0.42, (0, -1, 0), resonant="black")
    B.bx(p(0.17, 0.56, 0.02), (0.09, 0.22, 0.02), "hw", rot=(math.radians(8), 0, 0))     # footboard
    B.rod(p(0.17, 0.66, 0.06), p(0.17, 0.66, 0.36), 0.006, "chrome")                      # beater
    B.cyl(p(0.17, 0.65, 0.38), 0.025, 0.05, "head", axis=(0, 1, 0), segs=10)
    for s in (-1, 1):
        B.rod(p(kx + s * 0.27, 0.72, 0.18), p(kx + s * 0.42, 0.62, 0.0), 0.008, "chrome")
    # snare on its stand
    drum(B, p(-0.24, 0.5, 0.64), 0.178, 0.14, Matrix.Rotation(math.radians(-8), 3, "X") @ Vector((0, 0, 1)))
    B.tripod(x - 0.24, y + 0.5, y0, y0 + 0.56, r=0.22)
    # rack tom on the kick, floor tom on three legs
    rt = Vector(p(0.02, 0.78, 0.82))
    drum(B, rt, 0.15, 0.24, Matrix.Rotation(math.radians(-22), 3, "X") @ Vector((0, 0, 1)))
    B.rod(rt + Vector((0, 0.05, -0.12)), p(kx, 0.86, 0.57), 0.01, "chrome")
    ft = Vector(p(0.55, 0.45, 0.48))
    drum(B, ft, 0.2, 0.36, (0, 0, 1))
    for i in range(3):
        a = math.radians(30 + 120 * i)
        B.rod(ft + Vector((0.23 * math.cos(a), 0.23 * math.sin(a), 0.05)), ft + Vector((0.27 * math.cos(a), 0.27 * math.sin(a), -0.48)), 0.007, "chrome")
    # hi-hat: stand, pedal at the left foot, two cymbals
    hx, hy = -0.5, 0.5
    B.tripod(x + hx, y + hy, y0, y0 + 0.92, r=0.24)
    B.bx(p(-0.24, 0.5, 0.02), (0.09, 0.24, 0.02), "hw", rot=(math.radians(8), math.radians(10), 0))
    cymbal(B, p(hx, hy, 0.93), 0.18)
    cymbal(B, p(hx, hy, 0.955), 0.18)
    # sticks in the hands (hands measured at (-/+0.25, 0.50, 0.85) on library person 36), tips over the snare and tom
    # no drummer (band absent: S01, S29, S30): the pair laid side by side across the snare's head instead
    sticks = (((-0.29, 0.44, 0.88), (-0.13, 0.80, 0.74)), ((0.29, 0.44, 0.87), (0.06, 0.80, 0.86))) if present else \
        (((-0.44, 0.47, 0.722), (-0.03, 0.49, 0.722)), ((-0.45, 0.52, 0.718), (-0.04, 0.54, 0.718)))
    for (a0, a1) in sticks:
        B.rod(p(*a0), p(*a1), 0.0075, "stick", segs=8)
    # crash (left) and ride (right) on boom stands, tilted toward the drummer
    for (sx, sy, cx, cy, cz, r, tilt) in ((-0.78, 1.0, -0.55, 0.85, 1.36, 0.23, 14), (0.95, 1.0, 0.78, 0.8, 1.12, 0.27, 10)):
        B.tripod(x + sx, y + sy, y0, y0 + cz - 0.25, r=0.3)
        B.rod(p(sx, sy, cz - 0.25), p(cx, cy, cz - 0.02), 0.009, "hw")
        cymbal(B, p(cx, cy, cz), r, tilt_axis=(1, 0, 0), tilt=math.radians(-tilt))


def amp(B, x, y, y0, w=0.7, d=0.35, h=0.7):
    """A guitar or keys amp facing the house (-Y): tolex box, grille cloth, a control strip with knobs, a handle."""
    B.bx((x, y, y0 + 0.02 + h / 2), (w, d, h), "tolex")
    B.bx((x, y - d / 2 - 0.004, y0 + 0.02 + h * 0.42), (w - 0.06, 0.01, h * 0.72), "cloth")
    B.bx((x, y - d / 2 - 0.004, y0 + 0.02 + h * 0.9), (w - 0.06, 0.01, h * 0.12), "black")
    for i in range(6):
        B.cyl((x - w * 0.32 + i * w * 0.1, y - d / 2 - 0.016, y0 + 0.02 + h * 0.9), 0.012, 0.02, "chrome", axis=(0, 1, 0), segs=10)
    B.bx((x, y, y0 + 0.02 + h + 0.02), (0.18, 0.03, 0.03), "black")
    for sx in (-1, 1):
        for sz in (0, 1):
            for sy in (-1, 1):
                B.bx((x + sx * (w / 2 - 0.02), y + sy * (d / 2 - 0.02), y0 + 0.02 + sz * h), (0.05, 0.05, 0.05), "chrome")
        B.cyl((x + sx * (w / 2 - 0.08), y, y0 + 0.01), 0.025, 0.02, "rubber", segs=8)


def wedge(B, x, y, y0):
    """A floor monitor: a wedge whose sloped grille faces upstage (+Y), up at the performers."""
    out = [(-0.22, 0.0), (0.22, 0.0), (0.22, 0.1), (-0.22, 0.3)]
    B.prism(out, 0.6, "tolex", ((x - 0.3, y, y0), (0, 1, 0), (0, 0, 1), (1, 0, 0)))
    a = math.atan2(0.2, 0.44)
    B.bx((x, y + 0.002, y0 + 0.2 + 0.004), (0.54, 0.44, 0.008), "cloth", rot=(a, 0, 0))


def keyboard(B, x, y, y0, z=0.95):
    """A stage keyboard facing the player at -Y on a two-panel table stand (no T or cross reads from the house)."""
    W, n = 0.86, 36
    B.bx((x, y, y0 + z), (1.02, 0.34, 0.08), "black")
    kw = W / n
    for i in range(n):
        B.bx((x - W / 2 + kw * (i + 0.5), y - 0.1, y0 + z + 0.045), (kw - 0.001, 0.13, 0.016), "ivory")
    for i in range(n - 1):
        if i % 7 in (2, 6):
            continue
        B.bx((x - W / 2 + kw * (i + 1), y - 0.075, y0 + z + 0.058), (kw * 0.55, 0.08, 0.016), "ebony")
    B.bx((x, y + 0.08, y0 + z + 0.045), (0.12, 0.05, 0.006), "lcd")
    for i in range(8):
        B.cyl((x - 0.42 + i * 0.05, y + 0.1, y0 + z + 0.05), 0.009, 0.02, "chrome", segs=8)
    for s in (-1, 1):
        B.bx((x + s * 0.47, y, y0 + z / 2 - 0.02), (0.04, 0.32, z - 0.08), "hw")
    B.bx((x, y + 0.12, y0 + 0.28), (0.94, 0.03, 0.06), "hw")


def mic_stand(B, x, y, y0, aim_y=-1, top=1.45):
    """A vocal mic on a straight stand with a round base, the mic angled down toward the singer at aim_y."""
    B.cyl((x, y, y0 + 0.012), 0.14, 0.024, "hw", segs=24)
    B.rod((x, y, y0), (x, y, y0 + top), 0.011, "hw")
    d = Vector((0, aim_y * 0.9, -0.45)).normalized()
    a = Vector((x, y, y0 + top + 0.01))
    B.rod(a, a + d * 0.17, 0.018, "black")
    B.ball(a + d * 0.2, 0.028, B.mi("hw"))


BRIDGE, SCALE, HEEL = -0.148, 0.648, 0.02     # along the neck's line from the body centre (m)


def guitar(B, x, y, y0, strap=True):
    """An electric guitar on the guitarist standing at (x, y) facing +Y: the body at the belly, neck to the player's
    left (-X) and up; a strap over the left shoulder and across the back (torso measured on library person 24)."""
    fy = y + 0.165 + 0.03                         # the belly is 0.165 m ahead of the spine; the body's back 3 cm off it
    cz = y0 + 1.0
    # body outline: two lobes, the upper horn cut away, in the x-z plane (u along the neck's line, w across)
    t = np.linspace(0, 2 * math.pi, 40, endpoint=False)
    out = []
    for a in t:
        u, w = 0.21 * math.cos(a), 0.16 * math.sin(a)
        w *= 1.0 - 0.18 * math.cos(2 * a) ** 2 * (u > -0.05)           # a waist
        u *= 1.0 + 0.12 * (math.cos(a) < 0)                           # the lower bout larger
        out.append((u, w))
    ang = math.radians(22)                         # the neck rises 22 degrees toward the player's left
    au = Vector((-math.cos(ang), 0, math.sin(ang)))
    aw = Vector((math.sin(ang), 0, math.cos(ang)))
    c = Vector((x + 0.05, fy, cz))
    B.prism(out, 0.045, "body", (c, au, aw, (0, 1, 0)))
    B.prism([(u * 0.6 + 0.03, w * 0.6 - 0.03) for u, w in out], 0.004, "guard", (c + Vector((0, 0.046, 0)), au, aw, (0, 1, 0)))
    # pickups and bridge across the strings (au is the strings' line: a box's x axis turned +ang about Y lies along it)
    for i in range(2):
        B.bx(c + au * (-0.02 - 0.07 * i) + Vector((0, 0.05, 0)), (0.02, 0.008, 0.075), "black", rot=(0, ang, 0))
    B.bx(c + au * BRIDGE + Vector((0, 0.05, 0)), (0.025, 0.01, 0.075), "chrome", rot=(0, ang, 0))
    for i in range(3):
        B.cyl(c + au * (-0.12 - 0.04 * i) + aw * (-0.09) + Vector((0, 0.052, 0)), 0.01, 0.012, "chrome", axis=(0, 1, 0), segs=10)
    # neck (human, 2026-11-15: "the neck is far too narrow, and the headstock is a plain rectangle"): a 648 mm scale
    # from the bridge to the nut; the neck 43 mm wide at the nut, 56 mm at the heel, set into the body; a flat
    # fretboard with 22 frets; a 3+3 headstock flared from the nut, tuner posts on the face, keys out the sides
    fr = (lambda a, b, y: c + au * a + aw * b + Vector((0, y, 0)))
    def frame(y):
        return (c + Vector((0, y, 0)), au, aw, (0, 1, 0))
    nut = BRIDGE + SCALE
    half = (lambda a: 0.028 - 0.0065 * (a - HEEL) / (nut - HEEL))     # half-width along the neck
    neck_out = [(HEEL, -half(HEEL)), (nut, -half(nut)), (nut, half(nut)), (HEEL, half(HEEL))]
    B.prism([(a, b * 0.96) for a, b in neck_out], 0.022, "neck", frame(0.026))                   # the shaft
    B.prism([(a, b * 0.82) for a, b in neck_out], 0.01, "neck", frame(0.016))                    # rounded back
    B.prism(neck_out, 0.006, "board", frame(0.048))                                              # fretboard
    for n in range(1, 23):
        a = nut - SCALE * (1 - 2 ** (-n / 12))
        B.bx(fr(a, 0, 0.0545), (0.0016, 0.0015, 2 * half(a) - 0.002), "chrome", rot=(0, ang, 0))
    B.bx(fr(nut, 0, 0.054), (0.005, 0.004, 2 * half(nut)), "head", rot=(0, ang, 0))             # the nut
    t = np.linspace(0, 1, 9)
    flare = [(nut + 0.06 * u, half(nut) + 0.02 * math.sin(u * math.pi / 2)) for u in t]          # nut to the shoulders
    tip = [(nut + 0.06 + 0.11 * u, 0.0435 + 0.0025 * math.sin(u * math.pi)) for u in t[1:]]       # the long sides
    crown = [(nut + 0.17 + 0.018 * math.sin(u * math.pi), 0.0435 * math.cos(u * math.pi)) for u in t[1:-1]]  # rounded top
    side = flare + tip
    head_out = side + crown + [(a, -b) for a, b in reversed(side)]
    B.prism(head_out, 0.016, "neck", frame(0.03))
    for i in range(3):
        for sgn in (-1, 1):
            a = nut + 0.07 + 0.042 * i
            B.cyl(fr(a, sgn * 0.026, 0.05), 0.004, 0.014, "chrome", axis=(0, 1, 0), segs=8)        # string posts
            B.cyl(fr(a, sgn * 0.044, 0.038), 0.007, 0.012, "chrome", axis=aw, segs=8)              # gear housings
            B.rod(fr(a, sgn * 0.05, 0.038), fr(a, sgn * 0.066, 0.038), 0.002, "chrome", segs=6)
            B.bx(fr(a, sgn * 0.072, 0.038), (0.014, 0.005, 0.012), "chrome", rot=(0, ang, 0))      # keys
    for i in range(6):                                                    # strings, bridge to nut
        b = (i - 2.5) * 0.0085
        B.rod(fr(BRIDGE, b * 1.25, 0.058), fr(nut, b, 0.0575), 0.0006, "chrome", segs=4)
    n0 = c + au * 0.17                                                    # the strap button on the upper horn
    if not strap:
        return
    tail = c + au * (-0.25)
    path = [tail, (x + 0.24, y + 0.06, y0 + 0.97), (x + 0.2, y - 0.15, y0 + 1.05), (x - 0.02, y - 0.15, y0 + 1.3),
            (x - 0.15, y - 0.12, y0 + 1.47), (x - 0.17, y - 0.02, y0 + 1.52), (x - 0.17, y + 0.12, y0 + 1.43), n0 + Vector((0, -0.01, 0.02))]
    for a, b in zip(path, path[1:]):
        B.rod(a, b, 0.012, "strap", segs=6)


GUITAR_C = Vector((0.05, 0.195 + 0.0, 1.0))      # the body centre guitar() puts at (x + 0.05, y + 0.195, y0 + 1.0)
STAND_LEAN = math.radians(12)


def guitar_on_stand(x, y, y0):
    """No guitarist (band absent): the guitar upright on a floor stand, face to the house, leaning back 12 degrees.
    Returns (matrix for the guitar built at the origin, the stand's parts as a function of B)."""
    up = Vector((0, math.sin(STAND_LEAN), math.cos(STAND_LEAN)))        # the neck's line on the stand
    base = Vector((x, y, y0))
    c = base + up * 0.36                                                 # the lower bout clears the cradle
    m = (Matrix.Translation(c) @ Matrix.Rotation(-STAND_LEAN, 4, "X") @ Matrix.Rotation(math.pi, 4, "Z")
         @ Matrix.Rotation(math.radians(68), 4, "Y") @ Matrix.Translation(-GUITAR_C))

    def stand(B):
        back = Vector((0, 0.035, 0))                                     # the frame runs behind the body
        cradle = c - up * 0.27
        yoke = c + up * 0.42 + back
        for s in (-1, 1):                                                # the cradle arms, padded
            B.rod(cradle + Vector((s * 0.12, -0.03, 0)), cradle + Vector((s * 0.12, 0.04, 0)), 0.012, "rubber")
        B.rod(cradle + Vector((-0.12, 0.04, 0)), cradle + Vector((0.12, 0.04, 0)), 0.009, "hw")
        B.rod(cradle + Vector((0, 0.04, 0)), yoke, 0.01, "hw")           # the upright to the neck yoke
        for s in (-1, 1):
            B.rod(yoke + Vector((s * 0.035, 0, 0)), yoke + Vector((s * 0.035, -0.04, 0.02)), 0.007, "rubber")
            B.rod(cradle + Vector((s * 0.12, 0.04, 0)), Vector((x + s * 0.2, y + 0.3, y0)), 0.009, "hw")   # the legs
            B.rod(cradle + Vector((s * 0.12, 0.04, 0)), Vector((x + s * 0.17, y - 0.12, y0)), 0.009, "hw")
    return m, stand


# ---------------------------------------------------------------- placement

def build(M, y0, front, present=True):
    """Everything, merged into one mesh per kind of gear (so the set stays light). present=False (band absent): the
    sticks on the snare and the guitar on a stand, not held by players who aren't there."""
    P = mats(M)
    parts = {}

    def part(name, fn, *args):
        B = Props(P)
        fn(B, *args)
        parts[name] = gb.mesh_obj(name, B.to_mesh(name))

    # piano and bench (pianist at (-5.4, 13.85): hands 0.46 m ahead at 0.77 m, hips at 0.58 m)
    part("grand_piano", grand_piano, -5.4, 14.22, y0)
    part("piano_bench", piano_bench, -5.4, 13.84, y0)
    # drums around the drummer at (0, 17.45)
    part("drum_kit", drum_kit, 0.0, 17.45, y0, present)
    # amps facing the house, wedges at the downstage edge facing the singers
    for i, x in enumerate((-3.0, 3.2, 5.6)):
        part(f"amp{i}", amp, x, 17.6, y0)
    for i, x in enumerate((-4.5, -1.5, 1.5, 4.5)):
        part(f"wedge{i}", wedge, x, front + 0.6, y0)
    # keys before the keyboardist at (4.8, 14.2)
    part("keys", keyboard, 4.8, 14.6, y0)
    # vocal mics upstage of the two singers (at y front + 1.5, facing +Y), the spare stand where it was
    for i, (x, y, aim) in enumerate(((-1.5, front + 1.85, -1), (1.5, front + 1.85, -1), (3.4, front + 1.2, -1))):
        part(f"mic{i}", mic_stand, x, y, y0, aim)
    # guitar on the guitarist at (3.2, 16.8)
    if present:
        part("guitar", guitar, 3.2, 16.8, y0)
    else:
        m, stand = guitar_on_stand(3.7, 17.0, y0)
        part("guitar", guitar, 0.0, 0.0, 0.0, False)
        parts["guitar"].matrix_world = m
        part("guitar_stand", lambda B: stand(B))
    for o in parts.values():                     # smooth curved surfaces, hard box edges
        md = o.modifiers.new("edges", "EDGE_SPLIT")
        md.split_angle = math.radians(35)
    return parts
