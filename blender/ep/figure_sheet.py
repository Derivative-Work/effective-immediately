"""Review sheet for the figure library (blender/make_figures.py): links assets/figures/figures.blend as the set
does, lays every person out in a row per pose, renders front and back (Cycles), so faces, hands, clothes and the
phones can be checked before the look test. Output: <out>_front.png, <out>_back.png.
Usage: blender -b --factory-startup --python blender/figure_sheet.py -- --lib assets/figures/figures.blend --out review/m6/figures
"""
import argparse
import sys

import bpy
from mathutils import Vector

a = argparse.ArgumentParser()
a.add_argument("--lib", default="assets/figures/figures.blend")
a.add_argument("--out", default="review/m6/figures")
a.add_argument("--poses", default="")
a = a.parse_args(sys.argv[sys.argv.index("--") + 1:])
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
with bpy.data.libraries.load(a.lib, link=True) as (src, dst):
    dst.collections = [c for c in src.collections if c.startswith("fig_")]
colls = sorted(dst.collections, key=lambda c: c.name)
people = sorted({c.name.split("_")[1] for c in colls})
poses = a.poses.split(",") if a.poses else list(dict.fromkeys("_".join(c.name.split("_")[2:]) for c in colls))
sc = bpy.context.scene
for c in colls:
    p, pose = c.name.split("_")[1], "_".join(c.name.split("_")[2:])
    if pose not in poses:
        continue
    e = bpy.data.objects.new(c.name, None)
    e.instance_type, e.instance_collection = "COLLECTION", c
    e.location = (people.index(p) * 0.85, 0, -poses.index(pose) * 2.4)
    sc.collection.objects.link(e)
sc.render.engine = "CYCLES"
sc.cycles.samples = 48
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = "OPTIX"
prefs.get_devices()
for d in prefs.devices:
    d.use = True
sc.cycles.device = "GPU"
w = bpy.data.worlds.new("w")
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[1].default_value = 0.5
sc.world = w
W_, H_ = len(people) * 0.85 + 0.6, len(poses) * 2.4
cx, cz = (len(people) - 1) * 0.85 / 2, -(len(poses) - 1) * 2.4 / 2 + 1.0
for k, (loc, e) in enumerate((((cx + 8, -30, cz + 12), 30000), ((cx - 8, 30, cz + 10), 20000))):
    l = bpy.data.lights.new(f"l{k}", "AREA")
    l.energy, l.size = e, 15
    lo = bpy.data.objects.new(f"l{k}", l)
    sc.collection.objects.link(lo)
    lo.location = loc
    lo.rotation_euler = (Vector((cx, 0, cz)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam)
sc.camera = cam
cam.data.type = "ORTHO"
cam.data.ortho_scale = max(W_, H_)
sc.render.resolution_x = 2400 if W_ >= H_ else int(2400 * W_ / H_)
sc.render.resolution_y = int(2400 * H_ / W_) if W_ >= H_ else 2400
for tag, d in (("front", -1), ("back", 1)):
    cam.location = (cx, d * 40, cz)
    cam.rotation_euler = Vector((0, -d, 0)).to_track_quat("-Z", "Z").to_euler()
    sc.render.filepath = f"{a.out}_{tag}.png"
    bpy.ops.render.render(write_still=True)
