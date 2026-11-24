# Effective Immediately

**AI-generated satire. Not investment advice.** A bass-forward boogie-funk disco breakup song about Nvidia's board and
its founder-CEO: out "effective immediately" on November 12, 2026, reinstated eleven days later. The narrator is the
company, a lone silhouette that sings the breakup and then takes him back. The founder never appears; he is only ever a
black leather jacket on a hook. The board is a row of silhouettes whose hands go up on the beat.

**Conflict of interest:** the lyrics were written by Claude and the video made by Claude Code, both from Anthropic.
Anthropic runs Claude partly on Nvidia GPUs, and Nvidia is an Anthropic shareholder. The disclosure card at the end
says so, along with every other model maker's ties to Nvidia. To offset it, models from other labs audited the plan,
and every audit finding Claude rejected went to the human.

**Watch it on YouTube:** (link after upload)

This repository is the production record the video's credits point to. Claude Code produced the video. A human approved
each milestone, made the Suno generations and the edited master, picked the takes, ran the audits in the other labs'
apps, supplied the screenshots and reviewed the sources. Each of those interventions is logged.

**The production log and decisions are written by the agent and are a record, not a statement of fact about any
company:** where they discuss a fact, the fact card and its sources are the reference.

## How it was made

| Stage | What | Tools |
| --- | --- | --- |
| Lyrics | Written with Claude in the [planning chat](docs/planning_chat/planning_chat.md); audited by ChatGPT and Gemini ([`log/audits/`](log/audits/)) | Claude, other labs' chat apps |
| Song | One Suno take ([`docs/suno/`](docs/suno/)); the human's edited master (the intro riff, the cut with its reverb throw), post-filtered with a cleanup ("deslop") model so the words stay clear | Suno v6, music-deslop M6f |
| Credits music | An instrumental cover of the song, made by the human in Suno ([`docs/suno/credits/`](docs/suno/credits/)), post-filtered the same way | Suno v6, music-deslop M6f |
| Timing | Lyrics aligned to the vocal stem, beats from the band; the human's master measured against the take to the sample ([`scripts/master_audio.py`](scripts/master_audio.py)) | WhisperX, librosa |
| Stills | Scenes, plates and keyframes | FLUX.2 [dev] in ComfyUI, on an NVIDIA GeForce RTX 5090 |
| Clips | Moving shots from picked keyframes, every clip used once at full speed | LTX-2.3 image-to-video in ComfyUI |
| Boardroom | The board as flat black seated silhouettes, voting on the beat; the screen's candles from real prices | Blender 5.2 (Eevee), MakeHuman figures |
| Graphics and edit | Every word on screen, the phones, the charts, the subtitles and the cut | Remotion 4 |
| Market data | NVDA prices for the boardroom screen; the printed figures use official closes as reported | Databento US Equities Mini |
| Real captures | Nvidia's two releases, and `nvidia-smi` during a production stage | the human's screenshots; `nvidia-smi` |
| Checks | Two plan audits by other labs' models; every on-screen claim listed with its sources; the human's review of the sources | ChatGPT, Gemini; a human |
| Human | Milestone approvals, takes, the Suno generations, the master edit, the audits, the screenshots, every edit note | a human |

## Real captures

Three things in the video are real records, not generated.

- **The Nov 12 release (opening):** a screenshot of Nvidia's newsroom, "NVIDIA Announces CEO Transition", cropped to its
  header, headline and date, captioned "real screenshot".
- **The terminal (opening):** `nvidia-smi`, captured while the production's GPU ran the postfilter on the master at full
  load (an RTX 5090 at 100%, 572 W of 575 W), then [`scripts/effective-immediately`](scripts/effective-immediately), a
  real script that prints the video's three opening lines and "generating…". It makes nothing itself. The capture is in
  [`assets/captures/nvidia_smi/`](assets/captures/nvidia_smi/).
- **The Nov 23 release (after the song):** "NVIDIA Board Reinstates Jensen Huang as President, CEO and Board Director",
  cropped the same way.

## Sources

[`docs/sources.md`](docs/sources.md) lists every factual claim on screen with the pages to check it against: the fact
card line by line, the disclosure card, and everything else (chart figures, signs, tags, phone dates, counters, closing
cards). The fact card and disclosure are in [`config/cards.json`](config/cards.json).

## Where things are

- [`log/production_log.md`](log/production_log.md): every generation, analysis and render, with the command, inputs and
  outputs.
- [`log/human_interventions.md`](log/human_interventions.md): every human action, in the human's words.
- [`log/decisions.md`](log/decisions.md): every deviation from the brief, and why.
- [`log/audits/`](log/audits/): the audits, verbatim.
- [`docs/brief.md`](docs/brief.md): a plain-text mirror of the brief (shot list, look, lyrics, audit plan, fact card,
  guardrails). The video deviates from it where `log/decisions.md` says so.
- [`docs/planning_chat/`](docs/planning_chat/): the planning chat. [`docs/suno/`](docs/suno/): the Suno takes' page
  records.
- [`lyrics/`](lyrics/): the lyrics as sung.
- [`shots/`](shots/): every still and clip prompt with its seed, and each shot's pipeline.
- [`config/`](config/): the audio offsets, cards, story details, boardroom set-ups, picks and every edit setting.
  [`timing/`](timing/): the timing maps, board cues, subtitles and the credits music's beats.
- [`blender/`](blender/): the boardroom. [`remotion/src/`](remotion/src/): the graphics and the edit.
- [`scripts/`](scripts/): one script per step, each documented at the top.
- [`METADATA.md`](METADATA.md): the YouTube title, description, tags, settings and thumbnail, and the checklist before
  upload.

## Reproducing it

Large files (audio, clips, stills, renders, the videos) are not in git; [`MANIFEST.sha256`](MANIFEST.sha256) lists them
with checksums. The steps, in order, with their exact commands, are in the production log.

- Every random process reads its seed from [`config/seeds.json`](config/seeds.json) (main seed 1123). Stills and clips
  with the same seed, weights and ComfyUI version should match on the same GPU (production used an NVIDIA GeForce RTX
  5090, 32 GB); expect small differences elsewhere.
- The songs can't be regenerated: Suno doesn't give the same song twice, and the master was edited by hand. The
  post-filter model is private for now.
- The chart prices come from Databento under its terms and aren't redistributed here; `scripts/fetch_databento.py`
  fetches them with your own key.
- The full-page release screenshots aren't in the repository (they show the human's browser); the crops the video uses
  are listed in the manifest.

## Licences

- **Video and assets:** [CC BY-NC-SA 4.0](LICENSE-media.md). That file lists exactly what it covers and what it doesn't
  (fonts, the ComfyUI template, the people kit, the real captures, the market data, the auditors' outputs).
- **Code:** [MIT](LICENSE). Rendering it needs [Remotion](https://www.remotion.dev), which has its own licence: free
  for individuals, small companies and non-profits.

## Credits

- **Lyrics:** Claude, written in the [planning chat](docs/planning_chat/planning_chat.md); the plan audited by ChatGPT
  (OpenAI) and Gemini (Google) on November 23, 2026.
- **Music:** Suno v6, one take ("Effective Immediately", 043cee54), edited by the human. The credits music is an
  instrumental cover of it, also Suno v6 (70fd236d).
- **Post-filter:** music-deslop (M6f, 10k steps), a cleanup model for AI-generated music that Claude Code built and
  trained from a human-written spec, on Creative Commons audio only. The model is private for now.
- **Video:** Claude Code with Claude Opus 5.5, with stills from FLUX.2 [dev] (Black Forest Labs) and motion from
  LTX-2.3 (Lightricks), each used under its own licence; the boardroom in Blender.
- **Market data:** provided by Databento.
- **People kit:** from All Systems Operational ([`blender/ep/`](blender/ep/)), MIT.
- **Fonts:** [Inter](https://fonts.google.com/specimen/Inter), [Jost](https://fonts.google.com/specimen/Jost),
  [Courier Prime](https://fonts.google.com/specimen/Courier+Prime), [VT323](https://fonts.google.com/specimen/VT323),
  [Shrikhand](https://fonts.google.com/specimen/Shrikhand) and [Liberation Mono](https://github.com/liberationfonts)
  (SIL Open Font License 1.1), in `remotion/public/fonts/`.
