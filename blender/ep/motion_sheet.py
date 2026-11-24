"""M6 crowd motion check: the figure library's people in every pose, at several points of the motion loop, so the
loops' directions (knees, sway, arms) can be checked on stills. Eevee, orthographic.
Usage: blender -b --factory-startup --python blender/motion_sheet.py -- --lib assets/figures/figures.blend \\
       --people 0,1 --frames 1,21,41,61 --view front|side --out review/m6/motion_front.png
"""
import argparse
import math
import sys
from pathlib import Path

import bpy

a = argparse.ArgumentParser()
a.add_argument("--lib", default="assets/figures/figures.blend")
a.add_argument("--people", default="0,1")
a.add_argument("--frames", default="1,21,41,61")
a.add_argument("--view", default="front")
a.add_argument("--out", default="review/m6/motion_front.png")
a = a.parse_args(sys.argv[sys.argv.index("--") + 1:])
people = [int(x) for x in a.people.split(",")]
frames = [int(x) for x in a.frames.split(",")]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
with bpy.data.libraries.load(str(Path(a.lib).resolve()), link=False) as (src, dst):
    dst.collections = [c for c in src.collections if c.startswith("fig_") and int(c.split("_")[1]) in people]
poses = sorted({"_".join(c.name.split("_")[2:]) for c in dst.collections})
for c in dst.collections:
    i, pose = int(c.name.split("_")[1]), "_".join(c.name.split("_")[2:])
    e = bpy.data.objects.new(c.name, None)
    e.instance_type, e.instance_collection = "COLLECTION", c
    e.location = (poses.index(pose) * 1.4, people.index(i) * 3.0, 0)
    if a.view == "side":
        e.rotation_euler = (0, 0, math.pi / 2)
    sc.collection.objects.link(e)
cam = bpy.data.cameras.new("cam")
cam.type, cam.ortho_scale = "ORTHO", 1.4 * len(poses) + 0.4
co = bpy.data.objects.new("cam", cam)
sc.collection.objects.link(co)
cx = (len(poses) - 1) * 1.4 / 2
co.location, co.rotation_euler = (cx, -30, 1.0), (math.pi / 2, 0, 0)
sun = bpy.data.lights.new("sun", "SUN")
sun.energy = 3.0
so = bpy.data.objects.new("sun", sun)
so.rotation_euler = (math.radians(50), 0, math.radians(-30))
sc.collection.objects.link(so)
w = bpy.data.worlds.new("w")
w.color = (0.25, 0.25, 0.27)
sc.world = w
sc.camera = co
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 220 * len(poses), 400
out = []
for row, i in enumerate(people):
    for e in [o for o in sc.objects if o.instance_collection]:
        e.hide_render = int(e.name.split("_")[1]) != i
    for f in frames:
        sc.frame_set(f)
        p = Path(a.out).with_name(f"_ms_{i}_{f}.png")
        sc.render.filepath = str(p.resolve())
        bpy.ops.render.render(write_still=True)
        out.append(p)
print("POSES", poses)
print("TILES", " ".join(str(p) for p in out))
