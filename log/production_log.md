# Production log

Append-only. One entry per generation, render or analysis step.

## 1. 2026-11-23 — Project setup and inputs

- **Brief:** read with the docs tools at rev 105, raw read in `docs/brief_reads/main_tab_rev105.json`, mirrored with
  `python3 -I scripts/mirror_brief.py docs/brief_reads/main_tab_rev105.json docs/brief.md "main tab"`.
- **Planning chat:** `node scripts/fetch_share.mjs https://claude.ai/share/52d9cd3a-7d54-4694-ad9f-eebf1c52960f docs/planning_chat/planning_chat`
  → snapshot "In-progress song: Effective Immediately (Jensen Huang resignation and reinstatement)", taken
  2026-11-23T18:33:01Z, 44 messages, indices 0–43, no gaps. `scripts/chat_snapshot_to_md.py` → `planning_chat.md`
  (1,275 lines).
- **Suno take:** `node scripts/fetch_suno.mjs https://suno.com/s/uIZ5J4Hu7othl3Iq docs/suno` (31 JSON responses);
  `python3 -I scripts/suno_clip.py docs/suno cc8528ed-aea9-45cd-a778-6a9e10bb6575` → `docs/suno/clip.json`,
  `docs/suno/lyrics.txt`.
- **Audio,** copied from `~/Downloads` (originals untouched; git-ignored, in the manifest):
  - `audio/track/effective-immediately.wav`: 48 kHz stereo s16, 252.000 s, −15.9 LUFS, LRA 6.0 LU, true peak −3.5 dBFS,
    sha256 `24f93912…`.
  - `audio/source/Effective Immediately Stems.zip`, with its 11 WAV stems extracted to `audio/stems/` (252.000 s each).
    The zip's MP3 copies were not extracted.
- **Environment:** `PUPPETEER_SKIP_DOWNLOAD=1 npm ci` and `uv sync` from Sugar Push's locks (renamed). torch 2.8.0+cu128,
  CUDA available. NLTK data copied from Sugar Push's `.venv`. GPU idle (309 MiB), 238 GB free.

## 2. 2026-11-23 — M1: transcription and lyric diff

- **Commands:** `NLTK_DATA=$PWD/.venv/nltk_data .venv/bin/python -I scripts/transcribe_vocals.py "audio/stems/Effective Immediately (Vocals).wav" timing/whisper_lead.json`,
  the same for Backing Vocals → `timing/whisper_backing.json`. Then `scripts/m1_spot_checks.py` and
  `scripts/m1_outro_checks.py` (no VAD, on the stems and the mix).
- **Result:** the take sings v2.1's wording on six lines and v2.2's outro (`log/ai_changes.md` 1, decisions 1).
- **Stems:** 0 ms lag against the master by onset envelope. Their sum correlates 0.94 with the master (residual −7.9 dB).
- **Ending:** the last band hit decays cleanly, to below −60 dB by 251.8 s, so the file isn't truncated.
- **Not done:** the timing map, which waits on the master (decisions 1–3). No one has checked these results by ear: the
  agent can't listen, and Whisper is unreliable on sung words.
- **Listening file:** `.venv/bin/python -I scripts/m1_check_clips.py` → `review/m1_check_lines.mp3`, index in
  `review/m1_check_lines.md`.

## 3. 2026-11-23 — M3: narrator and jacket references

- **Why:** human interventions 4: proceed without the timing map.
- **Pipeline:** Buy It on Margin's FLUX.2 [dev] and LTX-2.3 graphs (`scripts/stills.py`, `clips.py`, `comfy_client.py`,
  `contact_sheet.py`, adapted). `scripts/comfy_batch.sh` enforces the memory plan in `CLAUDE.md`.
- **Command:** `scripts/comfy_batch.sh m3_refs '.venv/bin/python -I scripts/stills.py --stage refs'`: 8 takes, 35–76 s each.
- **Memory:** lowest available 1.9 GB, peak swap 11.7 GB, peak VRAM 31.3 GB. RAM back to 36 GB available after the stop.
- **Provisional picks:** `ref_narrator_s1126` (clean silhouette; s1123 has a seam down the middle) and `ref_jacket_s1125`
  (the plainest). Sheet: `review/m3_refs.jpg`.

## 4. 2026-11-23 — M2: look layer and code components, first pass

- `remotion/src/`: the look layer (`look/LookLayer.tsx`, parameters in `config/look.json`) and every code component, with
  card text verbatim from the brief in `config/cards.json`. Unfilled placeholders render in red so they can't ship.
- `.venv/bin/python -I scripts/grain_plates.py` → `remotion/public/grain/` (24 plates).
- `node scripts/m2_gallery.mjs` and `scripts/m2_sheet.py` → `review/m2_components.jpg` (21 stills, 15 s).
- **Review of the first sheet, fixed:** grain too heavy on flat areas (0.34 → 0.17), phone text too small, a crude hand on
  E03, a low-contrast plaque, and E11's confetti missing.

## 5. 2026-11-23 — M3: keyframes, first pass and revisions

- **First pass:** `scripts/comfy_batch.sh m3_keyframes '.venv/bin/python -I scripts/stills.py --stage keyframes --seeds 1123,1124'`:
  15 items, 30 takes. Lowest available RAM 1.9 GB, peak swap 11.7 GB, peak VRAM 31.3 GB. Sheet: `review/m3_keyframes.jpg`.
- **Review:** every take viewed; G01–G05, G08, G09 and S02 also enlarged. Six prompts revised to v2 (decisions 10).
- **Provisional picks** (`config/picks.json`): G01 s1123, G02 s1123, G03 s1123, G04 s1123, G08 s1123, G09 s1123, S02 s1123,
  jacket s1123, plaque s1124.
- **Retouches** (`.venv/bin/python -I scripts/retouch.py`, `config/retouch.json`; originals kept, results are `*_r_s*.png`):
  - G02: a green exit sign above the door made a blank neutral panel.
  - G04: 2,382 px of green rack LEDs recoloured pale and cool.
  - S02: the faint facial detail in her profile taken down to solid shadow.
  - A first attempt left a smeared door header, speckled rack frames and a hard box edge at her neck, so its masks were
    tightened and feathered, and the results checked in enlarged before-and-after crops.
- **Batch running:** `scripts/comfy_batch.sh m3_kf2_clips1` with the six v2 keyframes, then clips G01–G04, G08 and G09.

## 6. 2026-11-23 — M3: clips, composites and remaining stills

- **Clips:** `scripts/clips.py` inside `scripts/comfy_batch.sh` (batches `m3_kf2_clips1`, `m3_clips2`, `m3_g10`, `m3_g12`): 12 IDs, 28 takes, 7–50 s each, 1280×512, 24 fps. Lowest available RAM across these batches 1.3 GB, peak swap 12.4 GB, peak VRAM 31.3 GB. Nothing was killed, and the low-memory guard never fired.
- **Provisional clip picks:** G01 s1123, G02 s1123, G03 s1124, G04 s1123, G05 s1124, G06 s1124, G07 s1123, G08 s1123, G09 s1123, G10 s1125, G11 s1124. G12 swapped to a held still (decisions 12). G10 s1124 rejected for a generated face (decisions 11).
- **Guardrail scan:** `.venv/bin/python -I scripts/clip_checks.py` → `review/m3_clip_checks.json`. Haar face detection flagged 68 of the frames it scanned. A sample of 19, brightened, showed rack lights, wet pavement, coat folds and solid-black silhouettes, and no facial features. The other flagged frames weren't individually viewed. Bright green stayed under 0.4% of any frame, in the cyan night shots.
- **Composites:** `scripts/cutouts.py` (jacket, plaque, S01b's unfaded patch). S03 from G11's last frame and the jacket reference (s1123).
- **Sheets:** `review/m3_keyframes.jpg`, `m3_keyframes_v2.jpg`, `m3_clips_a.jpg`, `m3_clips_b.jpg`, `m3_clips_g10.jpg`, `m3_clips_g12.jpg`, `m3_s03.jpg`, `m2_look_on_plates.jpg`.

## 7. 2026-11-23 — M3: the boardroom, first pass

- `blender/boardroom.py`, `config/boardroom.json`, `SCALE=0.5 SAMPLES=24 scripts/m3_boardroom.sh` → `renders/m3/boardroom/` (E08, E09, E11, E17i, E22, E22s at 960×402, about 1 min in all; the probe as one full-size alpha still). Votes are on a placeholder 114 BPM grid.
- **Known weak:** E08's narrator is a simple figure; in E22 the purchase order is too small to read comfortably and the lowering hand is partly hidden by another hand.

## 8. 2026-11-23 — First-pass reel

- `npx remotion render Reel review/m3_reel.mp4 --scale=0.5 --concurrency=8 --crf=21`: every shot E01–E25 and the cards, 960×540, 110.4 s, silent, placeholder lengths, 4 min 37 s to render, 0.8 GB peak. Sampled at every shot and at the probe, plaque gag and dissolve. It has not been watched through in motion.
- **Not done (needs the corrected audio):** the timing map, the animatic, anything on the beat, the Shorts cut and captions. **Still placeholders:** the two real screenshots, the screen recording, and the red card fields.

## 9. 2026-11-23 — First-pass notes: phones, jacket, board, caller ID, probe (human interventions 5)

- **Phones:** `scripts/stills.py hand_phone hand_phone_night` inside `scripts/comfy_batch.sh m3b_hand_phones`: 8 takes, 1536×656, picks s1125 and s1125. Lowest available RAM 1.8 GB, peak swap 12.7 GB, peak VRAM 31.3 GB; nothing killed. Screens fitted with `scripts/track_display.py still … --notch`; UI pinned in `remotion/src/components/Phones.tsx`.
- **Caller ID:** `scripts/track_display.py clip remotion/public/gen/clips/G10.mp4 remotion/public/gen/track/G10_clip.json --ref 40`: 73 frames, corner error against each frame's edges 0.39 px median and 1.0 px at p95 (clip pixels), corner jerk p95 0.29 px. Pinned with `remotion/src/look/pin.ts`.
- **Jacket:** the v1 cutout had a strip missing from the chest and ragged collar edges (`archive/m3/jacket_v1/`). `scripts/cutouts.py` now uses GrabCut plus a darkness limit, and paints out the hanger wire. `scripts/jacket_sim.py` simulates the lift (40 frames) and the return (44 frames, settles crooked) with a shadow that leaves the wall.
- **Board:** `blender/board_arms.py` on the kit in `blender/ep/` (decisions 15), people 5, 12 and 23. Foreground rows in E08, E11, E22 and E22s; a ring with its own flat-to-lifted poses in E09 and E17i. v1 is in `archive/m3/boardroom_v1/`.
- **Probe:** `PurchaseOrder` redrawn as a placard and E22 restaged (decisions 17).
- **Reel:** `npx remotion render remotion/src/index.ts Reel review/m3_reel_v2.mp4 --scale=0.5 --concurrency=8 --crf=21`: silent, placeholder lengths, sampled by frames.

## 10. 2026-11-23 — Generation 2 evaluated, not adopted (human interventions 6)

- **Import:** `audio/candidates/gen2/` (master 276.4 s, 48 kHz stereo, −15.9 LUFS, LRA 5.5, peak −3.5 dBFS; 12 stems, 0 ms lag, their sum correlates 0.94 with the master). `audio/track/` is unchanged (sha256 `24f93912…`).
- **Lyrics:** `scripts/transcribe_vocals.py` → `timing/candidates/gen2_lead.json`; `scripts/lyric_check.py` → `review/gen2_lyric_check.md`. All six lines that gen 1 got wrong now transcribe as v2.2. Ear checks: 0:30 ("your" heard as "the"/"her"), 2:51 ("call" heard as "car").
- **Structure:** the last line finishes "intend" and holds into the outro, with the band playing until 242.0 s, under the outro's first words. The outro is voice and guitar with quiet drums and percussion to about 254 s. The full band returns at 257.96 s and plays 18 s to the end.
- **Listening file:** `scripts/candidate_preview.py` → `review/gen2_check.mp3`, index `review/gen2_check.md`. Its third clip is a rough edit: cut at 237.15 s, outro from the lead and guitar stems, ending at 258.35 s. Not checked by ear.

## 11. 2026-11-23 — M1: timing map on generation 2 (human interventions 7)

- `NLTK_DATA=$PWD/.venv/nltk_data .venv/bin/python scripts/timing_map.py` → `timing/timing_map.json`, `timing/bass_env.json`, from `lyrics/as_sung.txt` (v2.2's wording; the human confirmed the two doubtful words by ear).
- Tempo drifts from about 115.0 to 115.5 bpm, so the grid follows the backbeat rather than one constant tempo: 228 pulses, 12 repaired in the stretch with no drums, 455 beats, 211 claps. Local fit within 16 ms.
- **Not checked by ear:** word and beat alignment. Bar phase (which backbeat is 2 and which is 4) is inferred and doesn't affect the claps.

## 12. 2026-11-23 — Hands, plaque, jacket hold, and the M4 animatic (human interventions 7)

- **Why the hands felt off:** measured frame by frame, each arm crossed the picture in 2–3 frames as one rigid piece, then froze, with every arm identical.
- **Now** (`blender/boardroom.py`, `blender/board_arms.py`): the arm waits just under the frame with the elbow bent and lifts over about 8 frames. Shoulder, elbow, wrist and fingers each start slightly after the last, overshoot a little and settle. People are a frame or two apart, and raised arms keep a slow drift. Arrivals land on the song's claps.
- **Plaque:** `Animatic.tsx`: a corner lets go, it swings on one screw and slips behind the booth (34 frames, on "Came down"); it rises and settles (40 frames, on "Went back up").
- **Jacket in the booth (S03):** a 1.5 s dissolve, then a 6 s hold past the last word.
- **Cut:** `scripts/cut_list.py` → `remotion/public/gen/timing/`, `timing/board_cues.json`. `SCALE=0.5 SAMPLES=24 scripts/m3_boardroom.sh` (7 shots, about 4 min). `npx remotion render remotion/src/index.ts Animatic review/m4_animatic.mp4 --scale=0.5 --concurrency=8 --crf=21 --audio-bitrate=192k`.
- **Checked:** `review/m4_animatic.mp4` is 6905 frames (287.7 s) at 960×540 with audio. Its audio matches the working edit at 0 ms offset at three points. One frame from each of the 44 shots was viewed, plus the plaque's two moves frame by frame. **Not checked:** playback in motion, or sync by ear.

## 13. 2026-11-23 — New coverage, the seated board, music under the credits (human interventions 8)

- **Keyframes and clips:** `scripts/stills.py` and `scripts/clips.py` inside `scripts/comfy_batch.sh` (`m5_keyframes`, `m5_clips`, `m5_extra`, `m5_extra2`): 22 keyframes and 23 new clips (G13–G32, G34, G35, G05b), two seeds each, 5 s (G05b 6 s). Lowest available RAM 1.9 GB, peak swap 12.8 GB, peak VRAM 31.3 GB; nothing killed. Rejected at review: G28 s1123 (a blurred head appears behind the cord), G16's first placement. Picks are in `config/picks.json`.
- **Board:** `blender/board_arms.py` seats whole kit people (5, 12, 23, 31) in flat black at the table; 12 camera setups in `config/boardroom.json`. `SCALE=0.5 SAMPLES=24 scripts/m3_boardroom.sh`.
- **Audio:** the working edit now runs on after the outro into the band's last section, to the end of the take (272.5 s). The offset is unchanged (3.9 s).
- **Cut:** `scripts/cut_list.py`: 51 shots, 7094 frames (4:55.6), 33 takes each used once at full speed. `npx remotion render remotion/src/index.ts Animatic review/m4_animatic_v2.mp4 --scale=0.5 --concurrency=8 --crf=21 --audio-bitrate=192k`, then frames 6187–6603 re-rendered and spliced after moving the credits off the jacket. Sendable copy: `review/m4_animatic_v2_share.mp4`.
- **Checked:** audio matches the working edit at 0 ms at four points; a frame of every take viewed; four takes with heads brightened showed no faces. **Not checked:** playback in motion, sync by ear, or every frame for faces.

## 14. 2026-11-23 — One hand per beat, her footage in E08, subtitle styles (human interventions 9)

- **Narrator:** `scripts/stills.py G36` (batch `m6_walk_kf`, pick s1126) and `scripts/clips.py G36 --seeds 1123,1124,1125` (batch `m6_walk`, 9 s, pick s1125). Lowest available RAM 1.3 GB, peak swap 12.6 GB, peak VRAM 31.3 GB; nothing killed. `scripts/e08_comp.py` composites her into E08.
- **Vote:** `config/boardroom.json` `vote: "one_by_one"`; every board shot with hands re-rendered with `SCALE=0.5 SAMPLES=24 scripts/m3_boardroom.sh`. The overhead (E09, E17i, E22o) is tighter, with resting hands in laps.
- **Subtitles:** `scripts/subs.py` → `remotion/public/gen/timing/subs.json`, `timing/subtitles.srt` (69 cues). `scripts/sub_styles.py` → `review/m4_sub_styles.mp4`, `.jpg`. Fonts added: Courier Prime, VT323, Shrikhand (SIL OFL 1.1, `remotion/public/fonts/SOURCES.md`).
- **Alignment fix:** the aligner had put "Racks" and the first "We've" inside the line before. `scripts/timing_map.py` now takes them from the transcript (92.43 s and 107.54 s). The cut didn't change; frames 2233–2385 and 2586–2717 were re-rendered and spliced.
- **Animatic:** `review/m4_animatic_v3.mp4` (7094 frames, 4:55.6, subtitle style A); sendable copy `review/m4_animatic_v3_share.mp4`.
- **Checked:** audio matches the working edit at 0 ms at four points; sampled frames across the song; subtitle cues for overlaps and late words. **Not checked:** playback in motion, or subtitle and vote sync by ear.

## 15. 2026-11-23 — Vote rule, real market lines, fourth animatic (human interventions 10–11)

- **Market data:** `.venv/bin/python -I scripts/fetch_market.py ~/Documents/price-title.env` (read-only; SIP feed; NVDA 1-minute and daily bars, Nov 10–23) → `assets/market/nvda_bars.json` (git-ignored). `scripts/market_lines.py` → `remotion/public/gen/timing/market.json`. The key was read at run time and is not in this repo.
- **Vote:** `scripts/cut_list.py` sets each shot's vote. One hand per beat: E08 (not re-rendered) and B1. All up, all down on the beat: the rest. `SCALE=0.5 SAMPLES=24 scripts/m3_boardroom.sh E09 B2 E11 E11c E17i E22 E22s E22o E22b`, then B1, B2 and E22b again with the new screen textures.
- **Animatic:** `review/m4_animatic_v4.mp4` (7094 frames, 4:55.6, subtitle style A); sendable copy `review/m4_animatic_v4_share.mp4`.
- **Checked:** audio matches the working edit at 0 ms at four points; charts and vote shots viewed on sampled frames. **Not checked:** playback in motion, or vote sync by ear.

## 16. 2026-11-24 — Candlestick charts, the fact card's price line, fifth animatic (human interventions 12)

- **Charts:** `.venv/bin/python -I scripts/market_lines.py` (same `assets/market/nvda_bars.json`, no new fetch) → `remotion/public/gen/timing/market.json`: 36 half-hour candles (drop), 9 daily candles with two gap bands (recover), one stray print left out. `npx remotion still remotion/src/index.ts TX-screen-drop|TX-screen-recover renders/m3/tx/screen_{drop,recover}.png --frame=60`. `SCALE=0.5 SAMPLES=24 scripts/m3_boardroom.sh B1 B2 E22b` (24, 22, 27 s). Line versions archived (`archive/m4/real_market_lines/`, `archive/m4/boardroom_line_screen/`).
- **Fact card:** `config/cards.json`, third fact (decisions 27); the previous file is `archive/m4/cards_before_price_moves.json`.
- **Research:** two subagents read the news coverage of the moves and the price vendors' terms (decisions 27, 28).
- **Animatic:** `npx remotion render remotion/src/index.ts Animatic review/m4_animatic_v5.mp4 --scale=0.5 --concurrency=8 --crf=21 --audio-bitrate=192k` (862 s), then frames 6646–6717 (fact card 1) re-rendered after the sources came back and spliced. 7094 frames, 4:55.6. Sendable copy `review/m4_animatic_v5_share.mp4` (two-pass, 610 kbps, 26.1 MB).
- **Checked:** audio matches the working edit at 0 ms at 40, 150, 245 and 262 s; the charts viewed at the start, middle and end of E11, E11 close and E22s, and in B2; the fact card page viewed. **Not checked:** playback in motion.

## 17. 2026-11-24 — Databento prices, sixth animatic (human interventions 13–14)

- **Data:** `.venv/bin/python -I scripts/fetch_databento.py probe`, then `fetch` (EQUS.MINI, NVDA, `ohlcv-1m` and `ohlcv-1d`, Nov 10–23; estimate $0.0046 against the $1 cap) → `assets/market/nvda_databento.json` (git-ignored). Official closes for printed figures: `config/official_closes.json`.
- **Charts:** `.venv/bin/python -I scripts/market_lines.py` (Databento; stray Nov 12 04:00 print left out) → `market.json`; both textures re-rendered; `SCALE=0.5 SAMPLES=24 scripts/m3_boardroom.sh B1 B2`. End card gains "Market data provided by Databento."
- **Animatic:** `npx remotion render remotion/src/index.ts Animatic review/m4_animatic_v6.mp4 --scale=0.5 --concurrency=8 --crf=21 --audio-bitrate=192k` (862 s, 7094 frames). Sendable copy `review/m4_animatic_v6_share.mp4` (26.0 MB). v5 (Alpaca's prices) is for internal review only.
- **Checked:** audio matches the working edit at 0 ms at four points; E11, B2, E22s and the credits viewed on sampled frames. **Not checked:** playback in motion.

## 18. 2026-11-24 — Locked master, postfilter, chairs, phones, new opening, credits music (human interventions 15–17)

- **Master:** `audio/master/` (the human's master and stems). Postfilter: `cd ~/Code/music-deslop && uv run python -m postfilter.infer --in <repo>/audio/master/effective-immediately_master.wav --out <repo>/audio/postfilter/effective-immediately_postfilter.wav --ckpt ~/Code/music-deslop-data/release/m6f_10k.safetensors --source suno` (68441e2, clean tree; 27 s, 7.3 GB peak RAM; log `audio/postfilter/infer.log`). `.venv/bin/python -I scripts/master_audio.py` checks the two offsets at nine points and writes `audio/working/effective-immediately_edit.wav` (linked as `remotion/public/gen/audio/working.wav`) and `timing/bass_edit.json`. The stand-in edit stays in `audio/working/`.
- **Cut:** `scripts/cut_list.py` (fade over the throw, the master's bass, the opening, the credits tail) and `scripts/subs.py`. The previous `cut.json`, board cues, subtitles and audio config are in `archive/m4/`.
- **Boardroom:** new chairs and pedestal in `blender/boardroom.py` (old version `archive/m4/boardroom_box_chairs.py`). `SCALE=0.5 SAMPLES=24 scripts/m3_boardroom.sh` (all twelve shots, 499 s). Box-chair renders in `archive/m4/boardroom_box_chairs/`.
- **Phones:** `remotion/src/components/Phones.tsx` (old version `archive/m4/Phones_plain.tsx`), with phone details in `config/saga.json`.
- **Opening:**
  - Captures: `assets/captures/nvidia_smi/` (6 during the boardroom render, too light to use; 58 during a postfilter re-run whose output matched the master's byte for byte).
  - `.venv/bin/python -I scripts/e01_terminal.py` → `remotion/public/gen/captures/terminal.json`.
  - Screenshots cropped with ffmpeg to `remotion/public/gen/captures/E01_release.png` and `E25_release.png`.
  - Font: Liberation Mono (OFL) added.
- **Credits music:** `audio/credits/` (the human's file). Postfilter as above → `audio/postfilter/effective-immediately-credits_postfilter.wav` (18 s; log `infer_credits.log`). `node scripts/fetch_suno.mjs https://suno.com/s/n2YP4Uh76eIDOVJy docs/suno/credits` and `python3 -I scripts/suno_clip.py docs/suno/credits 70fd236d-…` → `docs/suno/credits/clip.json`. `.venv/bin/python -I scripts/credits_audio.py` → `timing/credits_map.json`.
- **Audits:** the human's copies of the Round 1 audits, verbatim, in `log/audits/2026-11-23_round1_{chatgpt,gemini}.md`.
- **Sources:** `.venv/bin/python -I scripts/sources.py` → `docs/sources.md`.
- **Animatic v7:** `npx remotion render … review/m4_animatic_v7.mp4` (7351 frames, before the credits tail). Audio matches the edit at six points, before and after the cut (0.4 ms). The first frames of E11, E11 close and E22s now show the candle chart.

## 19. 2026-11-24 — Disclosure, credits tail, eighth and ninth animatics, updated master (human interventions 18–19)

- **Tail:** `scripts/cut_list.py` with the new disclosure (188 words a minute). `npx remotion render … --frames=5999-11367 --muted` (from the booth, because the end card's credits changed) and `npx remotion render … --codec=wav` (the soundtrack, 796 s). Spliced onto `review/m4_animatic_v7.mp4` at frame 5999 (seam checked frame by frame) → `review/m4_animatic_v8.mp4` (11,368 frames, 7:53.7), sendable copy `…_v8_share.mp4` (two-pass, 380 kbps).
- **Updated master:** the same length and timing as the first (0-sample lag at nine points; 2.6% RMS difference, the crackle). The first is kept as `audio/master/effective-immediately_master_v1.wav`, its postfilter output as `audio/postfilter/effective-immediately_postfilter_v1.wav`. Postfilter as before (68441e2, 25 s, no fallback) → `audio/postfilter/effective-immediately_postfilter.wav`. `scripts/master_audio.py` rebuilt the edit audio (offsets hold).
- **Soundtrack without re-rendering:** `.venv/bin/python -I scripts/soundtrack.py <out.wav>` places the edit audio and the credits music at `musicFrom` and `creditsFrom`, to the sample. Against Remotion's own soundtrack render it matches in level, with the credits exact and the song 16 samples (0.3 ms) earlier, where Remotion had placed it late. Muxed onto v8's picture → `review/m4_animatic_v9.mp4` and `…_v9_share.mp4`. Song and credits both at 0.0 ms against their sources.

## 20. 2026-11-24 — Release: brief, publishing files, opening panel, final render, Shorts (human interventions 20–22)

- **Brief:** Claude Doc edited directly (rev 105 → 114). Mirror re-made by a subagent from a full read (`python3 -I scripts/mirror_brief.py <read> docs/brief.md`). The mirror's header link is fixed to the doc's real URL.
- **Publishing:** `README.md`, `LICENSE`, `LICENSE-media.md`, `LICENSES/CC-BY-NC-SA-4.0.txt` (copied from Distillation (Allegedly), the CC legal code), `METADATA.md`. Thumbnails: `npx remotion still remotion/src/index.ts Thumb-{A,B,C} deliverables/thumbnails/effective_immediately_thumbnail_{A,B,C}.jpg --image-format=jpeg --jpeg-quality=92`.
- **Opening panel:** `scripts/cut_list.py` (music from frame 0, `opening` in `cut.json`), `scripts/subs.py`. `Opening` and `OpeningReframe` are in `remotion/src/Animatic.tsx`. Checked on eight frames across the opening, including mid-slide.
- **Boardroom at full resolution:** `SCALE=1 SAMPLES=32 scripts/m3_boardroom.sh` (12 shots and both probe stills at 1920×804, 912 s). Checked against the approved half-resolution E08 on matching frames.
- **Final render:**
  - `npx remotion render remotion/src/index.ts Animatic … --props='{"slate":false}' --concurrency=8 --crf=16 --audio-bitrate=320k` (3,237 s; 11,112 frames, 1920×1080, 24 fps).
  - A first run was stopped because the panel hid the intro's subjects (human note). A second died when a `pkill` pattern matched its own shell.
  - Soundtrack from `scripts/soundtrack.py`, muxed without re-encoding the picture → `deliverables/effective_immediately_1080p.mp4` (7:43.0, AAC 320 kbps).
  - Song and credits music within 0.1 ms of their sources at nine points. A contact sheet of 16 frames shows no animatic labels.
- **Shorts:** `npx remotion render remotion/src/index.ts Short-<id> …` for chorus, bridge, reinstated and plaque, then 0.15 s and 0.6 s audio fades (video copied) → `deliverables/effective_immediately_short_<id>.mp4`. Captions from `scripts/shorts_srt.py`.

## 21. 2026-11-24 — Upload; thumbnail A re-set for phones, its jacket graded (human interventions 23–28)

- **Link:** the main video's YouTube link went into the README and the Shorts' footer (`8d92d50`).
- **Thumbnail A:** `remotion/src/Thumbnail.tsx` (`Split`) re-laid out for phones (decisions 34).
  - Command: `npx remotion still remotion/src/index.ts Thumb-A deliverables/thumbnails/effective_immediately_thumbnail_A.jpg --image-format=jpeg --jpeg-quality=92`.
  - Checked at 1280, 360 and 168 px wide.
  - The previous version is `archive/thumbnails/effective_immediately_thumbnail_A_v2_small_text.jpg`.
- **Thumbnail A, the jacket graded apart from the seat (human intervention 25):**
  - Command: `.venv/bin/python scripts/thumb_jacket.py`, then the same `npx remotion still … Thumb-A …`.
  - The model, SAM 2.1 (`facebook/sam2.1-hiera-large`), was downloaded to the Hugging Face cache. It gave the mask an IoU
    score of 0.917, and the mask covers 12.1% of the plate.
  - Outputs: `remotion/public/gen/plates/S03_jacket_mask.png` and `S03_thumbA.png`.
  - Checked at 1:1 and at 360 and 168 px wide.
  - The previous version is `archive/thumbnails/effective_immediately_thumbnail_A_v3_jacket_blends.jpg`.
- **Thumbnail A, the mask from Share the Shares' SAM (human intervention 26):**
  - **Model:** `scripts/thumb_jacket.py` now uses Segment Anything ViT-B (`segment-anything==1.0`, added with `uv add`).
    The checkpoint is read in place from `../share-the-shares/models/sam_vit_b_01ec64.pth`, and its sha256 is checked.
  - **Mask:** the scores were 0.962, 0.959 and 0.893, and candidate 1 was kept; candidate 0 spills into the booth's side
    panel. The mask covers 12.2% of the plate and matches the SAM 2.1 mask to an IoU of 0.986.
  - **Re-rendered:** the same `npx remotion still … Thumb-A …`.
  - **Clean-up:** deleted the SAM 2.1 download from the Hugging Face cache (`models--facebook--sam2.1-hiera-large`,
    857 MB).
  - **Previous version:** `archive/thumbnails/effective_immediately_thumbnail_A_v4_sam21_mask.jpg`.
- **Thumbnail A, a glow around the jacket (human intervention 27):**
  - **Script:** `scripts/thumb_jacket.py` gains the glow, a table mask (SAM ViT-B; scores 0.984, 0.987 and 0.980, the
    best kept; 17.1% of the plate), and `--regrade`, which grades from the saved masks without running SAM.
  - **Command:** `.venv/bin/python scripts/thumb_jacket.py`, then the same `npx remotion still … Thumb-A …`.
  - **Checked** at 1:1 and at 360 and 168 px wide.
  - **Previous version:** `archive/thumbnails/effective_immediately_thumbnail_A_v5_no_glow.jpg`.
- **Thumbnail A, the seat out of the jacket's mask (human intervention 28):**
  - **Cause:** one of the jacket's positive points, (60, 600), sat in the black shadow of the seat beside the jacket, so the
    mask took in the seat below the jacket's left side and hem.
  - **Fix:** that point moved onto the lit hem, (230, 595), and four negative points went on the shadowed seat. SAM scored
    0.949, 0.949 and 0.883, and candidate 1 was kept again; candidate 0 still spills into the side panel and seat. The
    mask covers 10.5% of the plate, down from 12.2%.
  - **Also:** a 7 px opening was added before the mask is carried to the frame's bottom edge. Without it, a one-pixel spur
    off the hem was carried down as a dark line through the glow.
  - **Command:** `.venv/bin/python scripts/thumb_jacket.py`, then the same `npx remotion still … Thumb-A …`.
  - **Checked** at 1:1, with the plate's shadows brightened to see the leather's edge, and at 360 and 168 px wide.
  - **Previous version:** `archive/thumbnails/effective_immediately_thumbnail_A_v6_seat_in_mask.jpg`.

## 22. 2026-11-24 — Release v1.0 (human intervention 29)

- **The Logic project** (`audio/logic/effective-immediately.logicx.zip`, as the human supplied it), checked before
  publishing:
  - **Audio:** the saved project and backups 01–06 list only the twelve stems in `Media/Audio Files/`, with no sampler,
    Quick Sampler, Ultrabeat or playback files. The stems are Suno's generation 2 (`audio/candidates/gen2/stems/`),
    sample for sample once decoded (Logic rewrote the file headers).
  - **The earliest backup** (00) also lists two of Logic's sampler instruments (Studio Bass "Classic Bass Pick" and
    "Phasing Guitar Plucks"); they're gone from the next save.
  - **Plugins:** only Logic's own, by name in the project data (Gain, Space Designer, Mastering Assistant, Channel EQ,
    Bass Amp Designer, Distortion, Overdrive), none from third parties. Space Designer loads Logic's factory impulse
    response "1.3s Conference Room", which isn't in the zip.
  - Like All Systems Operational's Logic zip, it holds the macOS resource files and the human's home path in the
    project data.
- **Manifest:** `scripts/manifest.sh` now covers `deliverables/` (the five final videos, which `.gitignore` already
  said were listed) and picked up the Logic zip: 3,964 files. Nothing else had changed.
- **Staged:** `scripts/release.sh` (modelled on All Systems Operational's) hard-links the videos and the Logic zip into
  `release/` and writes three tars, sorted and without the local user:
  - `inputs-suno.tar` (1.10 GB, 17 files): generation 1's take and stems zip, generation 2 and its stems, the credits
    music.
  - `inputs-master.tar` (1.06 GB, 20 files): both masters, their twelve stems, the post-filtered audio and its logs.
    The audio is split in two because together it passes GitHub's 2 GiB limit per file.
  - `takes.tar` (219 MB, 191 files): `assets/gen/`, every FLUX.2 still and LTX-2.3 clip.
  - Every file in the tars is in the manifest, and the 234 manifest lines they and the videos cover still match.
  - `SHA256SUMS` digest `704ca27d…`.
- **Left out:** the archived boardroom renders and animatics (`archive/`; some show charts drawn from Alpaca's or
  Databento's data) and everything else the script's header lists.
- **Notes:** `docs/release_notes.md`, in All Systems Operational's and Share the Shares' form; Databento's credit is in
  them. README links the release; `LICENSE-media.md` covers the Logic project and notes Logic's impulse response.
- **Command:** `scripts/release.sh --create` → `gh release create v1.0 --target main --latest --title "Effective
  Immediately v1.0" --notes-file docs/release_notes.md` with the 16 files.
- **Published:** https://github.com/Derivative-Work/effective-immediately/releases/tag/v1.0 ("Effective Immediately
  v1.0", latest; tag `v1.0` at `579be58`), 16 assets. Staged again for the upload, the tars came out byte-identical, and
  GitHub's digest for each of the 15 files matches `SHA256SUMS`. Log: `log/render_logs/release_v1.0.log`.
