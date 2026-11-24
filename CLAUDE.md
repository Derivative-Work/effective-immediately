# Effective Immediately

A bass-forward boogie-funk disco breakup song about Nvidia's board forcing out its founder-CEO on Nov 12, 2026 and
reinstating him on Nov 23. The narrator is the company, a lone silhouette; the founder is only ever a black leather
jacket. Season 2, the series' picks-and-shovels song. The agent does the production; the human approves at each
milestone gate (M1–M6), picks takes, and supplies what the agent can't reach (Suno, screen recordings, audits in other
labs' apps).

**Start here:** the brief is the Claude Doc https://claude.ai/artifact/LG1VQfvJN9mHpKi5mFXuhv (doc
`9bf617ca-b4cf-4f42-ad49-18eb6ffad325`, one tab, body `087a99f9-3ba0`). Read it with the docs tools, not a web fetch;
`docs/brief.md` is a plain-text mirror (`scripts/mirror_brief.py`). The planning chat is in `docs/planning_chat/`, the
Suno take in `docs/suno/`, the milestone status in `docs/plan.md`. Then read the latest entries of
`log/production_log.md` and `log/human_interventions.md`.

- **Conflict of interest:** Claude wrote the lyrics, and Anthropic is an Nvidia customer named in the results this song
  sings about. Any audit finding Claude rejects goes to the human.
- **Guardrails (brief):** no real faces or people; the jacket is never worn, and any take with it on a person is
  rejected, not fixed. The affairs and the women involved stay out entirely. The interim CEO is never named or depicted.
  "Senior levels" stays anonymous. No Nvidia logo, green, product names or campus outside the real-screenshot bookends;
  no Denny's name, colors or interior. Nothing warm before E22, and nothing from the "not to copy" list.
- **Every word on screen is Remotion**, never generated. Prompt every screen, sign and plaque blank.
- **Logs:** `log/production_log.md` gets one entry per generation, render or analysis step, with the command and output
  paths. Every human action goes in `log/human_interventions.md`, anything the generator changed in `log/ai_changes.md`,
  deviations and open choices in `log/decisions.md`. Stills and clips, kept or rejected, go in `shots/prompts.md`; each
  shot's asset type and swaps in `shots/pipeline.md`. Auditor outputs verbatim in `log/audits/`. Nothing is deleted:
  rejects go to `archive/`.
- **Seeds:** every random process reads its seed from `config/seeds.json`; main video seed 1123.
- **Shot IDs** (E01–E25, G01–G12, S01–S03) never change. Story details that may move are read from `config/saga.json`.
- **Large files** (audio, generated assets, renders) stay out of git; run `scripts/manifest.sh` after adding any. Check
  `df -h ~` before big renders.
- **Sibling projects** in `~/Projects` are reference only: read them for method, never modify them.
  `../buy-it-on-margin` is the pipeline this video reuses (`scripts/comfy_client.py`, `stills.py`, `clips.py`,
  `contact_sheet.py`). Bring nothing across from Ever Present, which stays private.
- **Tools:** Python steps run on this repo's `.venv` (`uv sync`; torch 2.8 cu128, WhisperX 3.8.6; WhisperX needs
  `NLTK_DATA=$PWD/.venv/nltk_data`). Captures use Puppeteer (`npm ci`). Blender 5.2, ComfyUI in `~/ComfyUI` (LTX-2.3,
  FLUX.2 [dev]).

## Video generation: memory plan

The machine has 38 GB of RAM and ComfyUI will fill it: earlier projects saw 32–33 GB held at idle, peaks of 37.4 GB, and
batches stopped for low memory (Buy It on Margin production log 20, All Systems Operational production log 10).

1. **Before a batch:** check `free -h`, `nvidia-smi` and `df -h ~`. Nothing else on the GPU, no Blender, no training run.
2. **Start ComfyUI fresh** for the batch and record its PID.
3. **One process, one job at a time.** Never point a second script at the same ComfyUI queue.
4. **One model at a time.** Call `comfy_client.free()` (`POST /free`, unload models and free memory) between stages, and
   always between FLUX.2 and LTX-2.3, so LTX and Gemma load into empty RAM.
5. **Sample RAM, swap and VRAM every 2 s** to `log/render_logs/`, and log the peak.
6. **Make batches resumable** (skip existing takes), so a stopped batch restarts with the same command.
7. **Afterwards:** free the models and stop the server by its PID. Confirm RAM is back to about 3 GB.
