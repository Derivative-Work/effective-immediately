# Licence for the video and its assets

Copyright 2026 Albert Armea.

"Effective Immediately" (the video) and its assets are licensed under the
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International licence](https://creativecommons.org/licenses/by-nc-sa/4.0/)
(CC BY-NC-SA 4.0). The full legal code is in [LICENSES/CC-BY-NC-SA-4.0.txt](LICENSES/CC-BY-NC-SA-4.0.txt).

The code is under the MIT licence instead: see [LICENSE](LICENSE).

## What this covers

- The video, with its captions and thumbnail.
- The music: the Suno v6 take and its stems, the human's edited master, the post-filtered master, and the credits
  instrumental (a Suno v6 instrumental cover) before and after its post-filter.
- The stills and clips, and the picks as the edit uses them; the Blender boardroom renders.
- The on-screen text: the fact card, the disclosure, the end card and closing cards, the signs, tags, phone screens and
  every other card or label in `config/`, and the frames the code renders from them.
- The production record, written by the agent: the logs and prompts under `log/` and `shots/`, the timing maps, the
  lyrics files and the documents under `docs/`.
- The planning chat in `docs/planning_chat/`.

## What this doesn't cover

- **Code** (`scripts/`, `remotion/src/`, `blender/`, `config/`, `comfy/api/` and the build files): MIT, see
  [LICENSE](LICENSE). Where a source file holds both code and on-screen text or design, the code is MIT, and the frames
  it renders are CC BY-NC-SA.
- **Remotion**, which renders the video from `remotion/src/`, is not part of this repository. It is used under its own
  [Remotion License](https://www.remotion.dev/license): free for individuals, small companies and non-profits; larger
  companies need a company licence to render this project.
- **The ComfyUI workflow template** (`comfy/api/video_ltx2_3_i2v.api.json`, the API form of ComfyUI's
  `video_ltx2_3_i2v` template): from Comfy Org's `comfyui-workflow-templates` package, MIT, copyright 2023-present
  Comfy Org.
- **The people kit** (`blender/ep/`): copied unchanged from All Systems Operational, by the same author, MIT (its own
  `LICENSE`). The MakeHuman figures it builds aren't in this repository.
- **Fonts** (`remotion/public/fonts/`): Inter, Jost, Courier Prime, VT323, Shrikhand and Liberation Mono, each under the
  SIL Open Font License 1.1, by its authors (the licence file beside each font; sources in `SOURCES.md` there).
- **The real captures.** The two screenshots of Nvidia's newsroom (E01, E25) show Nvidia's pages; they are the human's
  captures, cropped, shown as records and not included here. The `nvidia-smi` output in the opening (E01t,
  `assets/captures/nvidia_smi/`) is a record of NVIDIA's tool running on the production machine.
- **Market data.** The boardroom screen's candles are drawn from Databento's US Equities Mini data ("Market data provided
  by Databento"), under Databento's terms; the data itself isn't in this repository and isn't licensed here.
- **The auditors' outputs** in `log/audits/` (ChatGPT, Gemini) are kept verbatim as a record of the audit. They are
  offered here only as far as each provider's terms allow.
- **The Suno page records** in `docs/suno/` are Suno's metadata for the takes, kept as a record.
- **The news reports, filings and company statements** behind the fact card and disclosure: the cards state facts from
  them, with links in [docs/sources.md](docs/sources.md). They aren't reproduced here.

## Attribution

Credit "Effective Immediately" by Albert Armea, made with Claude Code (Opus 5.5) and Suno v6, licensed CC BY-NC-SA 4.0,
with a link to https://github.com/Derivative-Work/effective-immediately.
