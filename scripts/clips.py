"""M3: LTX-2.3 image-to-video clips from the picked keyframes (adapted from Buy It on Margin's scripts/clips.py).

Graph: ComfyUI's video_ltx2_3_i2v template in API form (comfy/api/, Comfy Org's comfyui-workflow-templates, MIT). Sets
the keyframe (node 269), prompt (320:319, enhancer 320:328 off), negative prompt (320:313, the brief's list), size
(320:312, 320:299), fps (320:300), seconds (320:301) and both noise seeds (320:276, 320:277 = seed + 1). The template's
audio branch runs but its audio is discarded. Outputs assets/gen/clips/<clip>/<clip>_s<seed>.mp4, one row per take in
shots/prompts.md. Existing takes are skipped, so the same command resumes a stopped batch.
Usage: .venv/bin/python -I scripts/clips.py [clip ...] [--seeds 1123,1124]   (inside scripts/comfy_batch.sh)
"""
import argparse
import copy
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import comfy_client as cc  # noqa: E402

CFG = json.load(open("config/clips.json"))
PICKS = json.load(open("config/picks.json"))["stills"]
SEEDS = json.load(open("config/seeds.json"))["m3_clips"]
BASE = json.load(open("comfy/api/video_ltx2_3_i2v.api.json"))
OUT, PROMPTS, LOG = Path("assets/gen/clips"), Path("shots/prompts"), Path("shots/prompts.md")


def prompt_for(spec):
    person = CFG["person"] if spec["person"] else ""
    style = CFG["style_template"].format(light=CFG["lights"][spec["light"]], person=person, camera=spec["camera"])
    return spec["motion"] + ". " + style


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="*")
    ap.add_argument("--seeds")
    a = ap.parse_args()
    clips = a.clips or list(CFG["clips"])
    seeds = [int(s) for s in a.seeds.split(",")] if a.seeds else SEEDS
    if "## Clips: LTX-2.3" not in LOG.read_text():
        with open(LOG, "a") as f:
            f.write("\n## Clips: LTX-2.3\n\nComfyUI template `video_ltx2_3_i2v` (`ltx-2.3-22b-dev-fp8` + distilled LoRA "
                    "0.5, Gemma 3 12B fp4 encoder, x2 spatial upscaler), prompt enhancer off, the brief's negatives. "
                    "Prompts verbatim in `shots/prompts/<clip>_clip.txt`.\n\n"
                    "| Clip | Keyframe | Seed | Output | Seconds | When |\n| --- | --- | --- | --- | --- | --- |\n")
    for clip in clips:
        spec = CFG["clips"][clip]
        kf = spec["keyframe"]
        if kf not in PICKS:
            print(f"{clip}: keyframe {kf} not picked yet, skipping", flush=True)
            continue
        src = Path(f"assets/gen/stills/{kf}/{PICKS[kf]}.png")
        name = cc.upload_image(src)
        prompt = prompt_for(spec)
        (PROMPTS / f"{clip}_clip.txt").write_text(prompt + "\n")
        for seed in seeds:
            dest = OUT / clip / f"{clip}_s{seed}.mp4"
            if dest.exists():
                continue
            g = copy.deepcopy(BASE)
            g["269"]["inputs"]["image"] = name
            g["320:319"]["inputs"]["value"] = prompt
            g["320:328"]["inputs"]["value"] = False
            g["320:313"]["inputs"]["text"] = CFG["negative"]
            g["320:312"]["inputs"]["value"], g["320:299"]["inputs"]["value"] = CFG["size"]
            g["320:300"]["inputs"]["value"] = CFG["fps"]
            g["320:301"]["inputs"]["value"] = spec["seconds"]
            g["320:276"]["inputs"]["noise_seed"] = seed
            g["320:277"]["inputs"]["noise_seed"] = seed + 1
            g["75"]["inputs"]["filename_prefix"] = f"ei/{dest.stem}"
            outputs, secs = cc.run(g)
            vid = next(v for k, vs in outputs["75"].items() if k in ("images", "videos", "gifs") for v in vs)
            cc.download(vid, dest)
            when = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
            with open(LOG, "a") as f:
                f.write(f"| {clip} | `{src}` | {seed} | `{dest}` | {secs:.1f} | {when} |\n")
            print(f"{clip} seed {seed}: {dest} ({secs:.1f} s)", flush=True)


if __name__ == "__main__":
    main()
