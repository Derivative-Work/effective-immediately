"""M3: stills with FLUX.2 [dev] via ComfyUI (adapted from Buy It on Margin's scripts/stills.py; same graph).

Prompt = the brief's subject + the shared style built from config/stills.json. Items with "refs" are conditioned on
the picked takes of those items (ReferenceLatent; picks in config/picks.json). Outputs
assets/gen/stills/<item>/<stem>_s<seed>.png, prompts verbatim in shots/prompts/<stem>.txt, one row per take in
shots/prompts.md. Existing takes are skipped, so the same command resumes a stopped batch.
Usage: .venv/bin/python -I scripts/stills.py [item ...] [--stage refs|keyframes|edits] [--seeds 1123,1124]
       (run inside scripts/comfy_batch.sh: one process, one job at a time)
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import comfy_client as cc  # noqa: E402

CFG = json.load(open("config/stills.json"))
PICKS = json.load(open("config/picks.json"))["stills"]
SEEDS = json.load(open("config/seeds.json"))["m3_stills"]
OUT, PROMPTS, LOG = Path("assets/gen/stills"), Path("shots/prompts"), Path("shots/prompts.md")


def prompt_for(spec):
    if spec.get("reference"):
        return spec["subject"] + ", " + CFG["reference_style"]
    person = CFG["person"] if spec.get("person") else ""
    return spec["subject"] + ", " + CFG["style_template"].format(light=CFG["lights"][spec["light"]], person=person)


def graph(prompt, seed, w, h, prefix, refs=()):
    """refs: uploaded image names, each scaled to 1 MP, VAE-encoded and chained through ReferenceLatent."""
    m = CFG["model"]
    g = {
        "12": {"class_type": "UNETLoader", "inputs": {"unet_name": m["unet"], "weight_dtype": "default"}},
        "38": {"class_type": "CLIPLoader", "inputs": {"clip_name": m["clip"], "type": "flux2", "device": "default"}},
        "10": {"class_type": "VAELoader", "inputs": {"vae_name": m["vae"]}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["38", 0]}},
        "26": {"class_type": "FluxGuidance", "inputs": {"conditioning": ["6", 0], "guidance": m["guidance"]}},
        "22": {"class_type": "BasicGuider", "inputs": {"model": ["12", 0], "conditioning": ["26", 0]}},
        "25": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "16": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": m["sampler"]}},
        "48": {"class_type": "Flux2Scheduler", "inputs": {"steps": m["steps"], "width": w, "height": h}},
        "47": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "13": {"class_type": "SamplerCustomAdvanced",
               "inputs": {"noise": ["25", 0], "guider": ["22", 0], "sampler": ["16", 0], "sigmas": ["48", 0],
                          "latent_image": ["47", 0]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["13", 0], "vae": ["10", 0]}},
        "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": prefix}},
    }
    cond = ["26", 0]
    for i, name in enumerate(refs):
        g[f"ref{i}_load"] = {"class_type": "LoadImage", "inputs": {"image": name}}
        g[f"ref{i}_scale"] = {"class_type": "ImageScaleToTotalPixels",
                              "inputs": {"image": [f"ref{i}_load", 0], "upscale_method": "area", "megapixels": 1.0,
                                         "resolution_steps": 1}}
        g[f"ref{i}_enc"] = {"class_type": "VAEEncode", "inputs": {"pixels": [f"ref{i}_scale", 0], "vae": ["10", 0]}}
        g[f"ref{i}"] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": cond, "latent": [f"ref{i}_enc", 0]}}
        cond = [f"ref{i}", 0]
    g["22"]["inputs"]["conditioning"] = cond
    return g


def pick_path(item):
    if item not in PICKS:
        raise SystemExit(f"reference {item} not picked yet (config/picks.json)")
    return OUT / item / f"{PICKS[item]}.png"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items", nargs="*")
    ap.add_argument("--stage")
    ap.add_argument("--seeds")
    a = ap.parse_args()
    items = a.items or [k for k, v in CFG["items"].items() if not a.stage or v["stage"] == a.stage]
    seeds = [int(s) for s in a.seeds.split(",")] if a.seeds else SEEDS
    m = CFG["model"]
    PROMPTS.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text("# Prompts and takes\n\nAppend-only: every still and clip, kept or rejected. Picks are in "
                       "`config/picks.json`.\n")
    if "## Stills: FLUX.2 [dev]" not in LOG.read_text():
        with open(LOG, "a") as f:
            f.write(f"\n## Stills: FLUX.2 [dev]\n\nModel `{m['unet']}`, text encoder `{m['clip']}`, VAE `{m['vae']}`; "
                    f"{m['steps']} steps, {m['sampler']}, guidance {m['guidance']}; ComfyUI v0.42.1. No negative "
                    "prompt (FLUX.2 [dev] is guidance-distilled). Prompts verbatim in `shots/prompts/<item>.txt`.\n\n"
                    "| Item | Seed | Size | Output | Seconds | When |\n| --- | --- | --- | --- | --- | --- |\n")
    for item in items:
        spec = CFG["items"][item]
        prompt = prompt_for(spec)
        stem = item if spec.get("v", 1) == 1 else f"{item}_v{spec['v']}"
        (PROMPTS / f"{stem}.txt").write_text(prompt + "\n")
        w, h = spec["size"]
        refs = [cc.upload_image(pick_path(r)) for r in spec.get("refs", [])]
        for seed in seeds:
            dest = OUT / item / f"{stem}_s{seed}.png"
            if dest.exists():
                continue
            outputs, secs = cc.run(graph(prompt, seed, w, h, f"ei/{stem}_s{seed}", refs))
            cc.download(outputs["9"]["images"][0], dest)
            when = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
            via = f" (refs: {', '.join(spec['refs'])})" if spec.get("refs") else ""
            with open(LOG, "a") as f:
                f.write(f"| {stem}{via} | {seed} | {w}×{h} | `{dest}` | {secs:.1f} | {when} |\n")
            print(f"{item} seed {seed}: {dest} ({secs:.1f} s)", flush=True)


if __name__ == "__main__":
    main()
