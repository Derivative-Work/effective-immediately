# Decisions

Append-only. Deviations from the brief and choices it leaves open, each with why and who decided.

## 1. 2026-11-23 — OPEN (human): the chosen take does not sing lyrics v2.2

- **Evidence:** Suno created the take at 18:07:45Z. v2.2 was proposed at 18:06:44Z, approved at 18:09 and applied at
  18:13 (planning chat messages 41–43). The take has v2.2's outro and v2.1's wording on the other six changed lines
  (`log/ai_changes.md` 1).
- **Why it matters:** "Signed the paper" and "says you're good enough for me" are lines audit round 1 corrected, on the
  date of the decision and on asserting a motive. E15 and E16 are cued on lines the take doesn't sing, and E21's last tag
  loses its lyric.
- **Options:**
  - A (agent's recommendation): replace those lines in Suno on this take, which keeps the performance and most of the
    timing. At minimum the two audit lines.
  - B: regenerate from v2.2 and pick a new take.
  - C: keep the take as sung, change the brief, shots and captions to match, and put the two audit lines back through
    the audit.
- The timing map waits for this, since it is built on the locked master.

## 2. 2026-11-23 — OPEN (human): the cut-off is not in the audio

The take appears to finish the word: Whisper hears "we did not intend" at about 222.2 s and again at about 226.5 s on the
mix (low confidence on the sung stem). The brief's edit is a cut mid-word on "in—" straight to black, so the candidate is
about 226.9 s, with the outro's first words at 230.0 s. To be set by ear.

## 3. 2026-11-23 — OPEN (human): the outro is not one acoustic voice

The brief ends on a solo acoustic voice. In the take the drums stem stays near chorus level through the outro (−20.4 dB
RMS at 230–236 s against −18.8 dB at 224–230 s), with keyboard and guitar under it, and a band hit at 250–251.5 s. The
stems could thin it, but they don't null against the master (correlation 0.94), so a remix will differ slightly from it.

## 4. 2026-11-23 — For M2 and M6: inconsistencies inside the brief (agent; brief not edited)

- The guardrail says the fact card gives the cause as "reports about his personal relationships"; audit round 1 replaced
  that wording with the reported foreign-intelligence effort.
- `saga.json` has `marketValueDrop` "more than $600bn" where the fact card has "about $600bn ... at the low", and
  `interviews.date` "early December (CNN: Dec 1)" where the cards have Dec 1–2.
- The audit prompt's question 3 still quotes "Six hundred billion says you're good enough for me", the line v2.2 replaced
  (and the line this take sings).
- The fact card's header says "No names beyond Nvidia and the founder", but its seventh line names President Trump (added
  after audit round 1, which the audit log records as fact card only).
- `config/saga.json` is copied verbatim from the brief until these are settled.

## 5. 2026-11-23 — Git and licences left to the human (agent)

Nothing is committed yet, since this session wasn't asked to commit. No licence files are added: the series uses MIT for
code and CC BY-NC-SA 4.0 for media, to be confirmed for this song.

## 6. 2026-11-23 — Prompt style variants (agent)

The brief's shared phrases name "one person in silhouette" and a handheld camera. Used unchanged, they would put a person
in the empty shots and move the locked-off ones. So the person words drop for shots with nobody in them (G06, G07, G10,
G11, G12, S01), and the camera words change per clip. With cold light, a person and the handheld camera, the templates
in `config/stills.json` and `config/clips.json` produce the brief's phrases verbatim. FLUX.2 [dev] takes no negative
prompt, and listing "leather jacket" there could prime one, so its negatives stay as the style's "no ..." words. LTX-2.3
gets the brief's full negative list.

## 7. 2026-11-23 — Generation sizes (agent)

- Clips are 1280×544, the 2.39:1 picture rounded to LTX's multiples of 32, above the brief's 480p floor with no pixels
  lost to the letterbox.
- Keyframes are 1536×656. S01 is 2560×1088 rather than the brief's "twice the target width" (3840 wide), which would
  risk the memory limit, and its push stays under the brief's 5% of frame width per second.

## 8. 2026-11-23 — Two takes first, then more where needed (agent)

The brief asks for four takes each. For speed (human interventions 4), each keyframe gets two seeds first, and seeds 3–4
run only for items where neither take passes review. Picks in `config/picks.json` are provisional until the M3 gate.

## 9. 2026-11-23 — The boardroom's figures are procedural (agent)

The hands and E08's narrator are simple procedural models in near-black, since every performer is a silhouette. The people
kit (476 MB) isn't brought in. Votes run on a placeholder 114 BPM grid until the timing map exists.

## 10. 2026-11-23 — Keyframe revisions after review (agent)

- **G05:** "hugging it like a bouquet" produced a literal bouquet in both takes, which the brief's distance from "Flowers"
  rules out. The prompt now says she holds the rack close, and doesn't mention a bouquet.
- **G06, G10:** the hands wore a man's suit sleeve. They are now her hand, in shadow, in her coat sleeve.
- **G07:** the sleeve came out as blue cloth; the prompt now specifies the leather and a zippered cuff.
- **G09:** seed 1124 has a skyline spire resembling a real landmark. Rejected.
- **G11:** the red and orange booths drift toward the brand colors the brief excludes. Now dark brown vinyl on a cream wall.
- **S01:** the wall read as ruined plaster. It is now generated with an empty hook, and the jacket cutout is composited on
  it, so S01b's clean jacket-shaped outline matches the cutout exactly instead of being inpainted.

## 11. 2026-11-23 — G10 clip rejected for a generated face (agent)

G10 seed 1124 turned into a full, realistic woman's face by its fourth second, and seed 1123 left the phone for her torso.
Both are rejected (guardrail: no faces). The clip prompt is now locked off on the phone with only her hand in frame, run on
seeds 1125 and 1126. The earlier prompt is kept in `shots/prompts/G10_clip_v1.txt`.

## 12. 2026-11-23 — G12 swapped to a held still (agent; for the human to confirm at the M3 gate)

G12 has to hold the framing where G11's push ends, so the plaque stays put and the dissolve to S03 lines up. None of its four
takes does: seeds 1123–1124 start from G11's first frame, and from its last frame seed 1125 dollies out and 1126 keeps
pushing. The brief's fallback, looping G11's last second, would jump because G11 is moving. So G12 is G11's last frame held
locked off, with a seeded flicker of the warm light in Remotion. S03 was generated from that same frame.

## 13. 2026-11-23 — Correction to decisions 7: clips are 1280×512 (agent)

LTX-2.3's template rounds the height to a multiple of 64, so the requested 1280×544 came out 1280×512. The clips are cropped
about 2% at each side to fill the 2.39:1 picture. `config/clips.json` now says 512.

## 14. 2026-11-23 — The phone shots are generated hands with a pinned UI (human note)

E03, E18 and E19 were all code, with a drawn silhouette hand on E03. They now use FLUX.2 [dev] stills of a hand holding a
phone with a blank screen (`hand_phone` s1125, `hand_phone_night` s1125), and the Remotion UI is corner-pinned to the
screen. The plates grew a notch, so the UI covers the whole screen to keep the handset generic. Every word is still
Remotion. E07 stays code: the phones are on a desk and no hand is in the brief's shot.

## 15. 2026-11-23 — The board's arms come from the people kit (human note)

`blender/ep/` and `assets/figures/figures.blend` are copied unchanged from All Systems Operational at 701009f, where the
author published the kit under MIT. The built library is under that project's `LICENSE-media.md`, so its use here is part
of the licence question in decisions 5. Each member is one right arm cut from a kit body, with no face or torso. Hands
now rise from below the frame in a foreground row, as the brief describes, and the overhead keeps a ring.

## 16. 2026-11-23 — Screen tracking follows Ever Present's method, not its code (human note)

The human pointed to Ever Present for screen alignment. That repo stays private and nothing is copied from it. Its log
and `screen_comp.py` were read for the method (edge-fitted quad, registration to one reference frame, zero-lag smoothing,
corner-pin), and `scripts/track_display.py` is new code.

## 17. 2026-11-23 — E22 restaged so the purchase order reads (human note)

The illegible text was not intentional. The camera is closer on a longer lens, the page is a larger placard with only
"PURCHASE ORDER" on it, and the two groups of hands leave the probe clear. The table is now out of frame in this shot.

## 18. 2026-11-23 — Generation 2 is the working audio; one offset covers the human's cut

The human confirmed "took your jacket" and "call comes down" and will make the cut. `audio/working/` holds a stand-in edit:
source to 237.15 s, 0.35 s of silence, then the outro from the lead and guitar stems, from 241.40 s to 258.35 s. All timing
stays in source time, and `config/audio.json` maps it to the edit with one number (`offset_s`, now 3.9). When the locked
master arrives: set `master`, measure `offset_s`, run `scripts/cut_list.py`, re-render. `audio/track/` still holds
generation 1 and is not used.

## 19. 2026-11-23 — Deviations in the first cut to the song (agent, for the M4 gate)

- **E06 follows E07.** This take goes straight from "put it away" into the pre-chorus, so there is no turnaround. E07 keeps
  its line ("Three committees…, FBI on the line") and E06's flashes land on "Ticker falling, center stage".
- **E17's hand inserts are one a bar**, not on every clap. Claps come every second beat, so the brief's version would be
  ring-of-hands for half the chorus.
- **Thin coverage.** The song is 4:14 and the brief's shots run far shorter. Clips play down to 0.55× speed and kept
  alternate takes fill the gaps. The weakest stretches are the 22-second intro (E02), E23 (18 s on one still), E21 (holds
  on the phone's last frame) and chorus 2 (E17). More generations would help there.
- **E11 and E22's screen** now draw the market line in Remotion, pinned to the Blender screen, so real ticker data can drop in.

## 20. 2026-11-23 — New coverage: no repeated takes, nothing time-stretched (human note)

23 new clips (G13–G32, G34, G35, and G05b, a longer take of G05) and one new still (G33), each from its own FLUX.2 keyframe, two seeds each. IDs E01–E25, G01–G12 and S01–S03 are unchanged. `scripts/cut_list.py` now stops with an error if a take is used twice or a slot is longer than its takes. Every clip plays at full speed. Held or locked-off moments that remain: the plaque's booth (G11's last frame with a light flicker), S02, G33 and the code-made phones. E13 uses G04's second take behind the scoreboard. G16 was first dropped for resembling G02 and is back, as a distant approach, because the 22-second intro needed it.

## 21. 2026-11-23 — The board is now visible, in silhouette (human note; departs from the brief)

The brief says "The board: only hands". The human's note was that it was "unclear where the hands are supposed to be coming from", so whole seated people from the kit now sit at the table. They are flat, unlit black, so no face or feature can show; an earlier test with lit bodies showed facial relief and was rejected. Only the hands carry any shading. They are generic MakeHuman figures, never named. The arms-only version is in `archive/m4/boardroom_arms_only/`.

## 22. 2026-11-23 — The song's last section is the credits (human note)

The band returns at 4:18 of the take and plays to 4:36. The jacket in the booth holds through all of it, with the credits (the brief's end card, verbatim) coming in line by line over it. The real Nov 23 screenshot follows on the band's last hit. So the end card now comes before the fact card, which is a change to the brief's order. The fact card and disclosure stay after the music, silent. **Open:** at reading pace they need about 3 minutes, and they currently run about 12 seconds, so they can't be read yet.

## 23. 2026-11-23 — The vote goes one hand per beat (human note)

`config/boardroom.json` `vote: "one_by_one"`. One hand rises on each beat and stays up, round the table in the overhead and along the row elsewhere. When the last is up they hold, drop together on the last beat of a bar and start again. In E08 each member votes on the first beat after she passes; in E11, E22s and E22 the count runs once. E22's lowered hand and push now come after the last hand is up. From directly above a raised hand barely changes, so the overhead keeps resting hands in laps and brings each one out over the bright table. Setting `vote` to `"unison"` and re-rendering restores the previous version; its renders are in `archive/m4/boardroom_unison/`.

## 24. 2026-11-23 — E08's narrator is generated footage (human note)

G36 is her walking on plain white with the camera tracking her (FLUX.2 keyframe s1126, LTX-2.3 s1125, 9 s). `scripts/e08_comp.py` keys her from the white, stabilises her and places her between the room and the Blender "matte" pass, at her height and position behind the table. She remains the narrator: the brief has her as the company and never depicts the interim CEO.

## 25. 2026-11-23 — Subtitle styles for the human to choose (open)

Burned into the letterbox, so they never cover the picture or its on-screen text. `scripts/subs.py` builds them from the timing map and `lyrics/as_sung.txt`. Five candidates in `review/m4_sub_styles.mp4` and `.jpg`: A matched to each scene (filing, closed captions, disco, phone display, brass plaque), B SEC filing typewriter, C TV closed captions, D desk phone display, E boogie-funk lettering. The animatic uses A until the human picks. New fonts (SIL OFL 1.1): Courier Prime, VT323, Shrikhand.

**Wording to confirm by ear**, because subtitles make any mismatch visible. The transcripts differ from v2.2 at: "no, we do not intend" (heard "oh"), "We've got this" (heard "We got this"), "the quarter closed" (heard "close"), and the last line, where no "no" was heard between the two "intend"s (the subtitle omits it).

## 26. 2026-11-23 — Subtitle style A; the vote rule; real market data (human notes)

- **Subtitles:** style A (matched to each scene), and the human confirmed the wording.
- **Vote:** one hand per beat stays only where a shot is on screen long enough for everyone's hand plus a two-beat hold (`scripts/cut_list.py`). That is E08 and the row in chorus 1 (B1). Every other board shot is all up and all down on the beat, and event shots (the drop, the recovery, the vote) go all up on the beat nearest their word.
- **Market lines:** E11, E22 and every visible boardroom screen now show real NVDA prices from Alpaca's consolidated (SIP) feed, as a normalised shape with no ticker. The made-up lines are in `archive/m4/made_up_market_lines/`. Because the axis doesn't start at zero, the prior close is a dashed line and the moves are labelled. The chart labels gain dates and percentages, which is new on-screen text for the M6 fact check.
- **For the fact check (open, human):**
  - The data supports the fact card's −14.3% low and the recovery by the close (−4.3%).
  - The first big fall came at about 5:28 pm ET on **Nov 11**, after hours, the evening before the card's Nov 12 announcement date.
  - The stock also fell 14.0% on **Nov 20** and rose **31.5%** on Nov 23, starting with a jump at about 8:55 am ET. The fact card mentions neither.
  - Alpaca's terms on showing its market data in a published video have not been checked.

## 27. 2026-11-24 — Candlesticks, the price line on the fact card, and the Nov 11 timing (human note)

- **Candlesticks** (`scripts/market_lines.py`, `MarketChart` in `remotion/src/components/Data.tsx`):
  - The drop (E11) uses 30-minute candles from Nov 11 14:00 to the Nov 12 close. Extended-hours candles sit on a faint band, and a dotted line marks the night.
  - The recovery (E22) uses daily candles, Nov 11–23. Both big moves happened outside the session, so a daily candle shows them as gaps: the Nov 23 candle alone is a small cross. Gaps over 5% get a shaded band from the previous close to the open (red down on Nov 12, white up on Nov 23), a standard chart annotation.
  - A candle is red when it closed below the previous close and white otherwise, with no green (brief). New on-screen text: "−14.0% on Nov 20".
  - One stray extended-hours print is left out (Nov 12, 08:22, a 173.30 high in a minute that traded 159.0–159.5).
  - In E22s the Nov 20 candle grows first, then Nov 23 about 1.5 s later. Only B1 and B2 show the baked screen texture, and they were re-rendered. E22b was re-rendered too but turned out not to show the screen (identical output). E08 and E22p don't show it and were not touched. The line versions are in `archive/m4/real_market_lines/` and `archive/m4/boardroom_line_screen/`.
- **Fact card, third line** (`config/cards.json`), added: "They fell 14% on Nov 20, after Reuters reported that the SEC was exploring potential accounting issues at Nvidia (CNBC), and rose more than 31% on Nov 23, the day he was reinstated (AP)." The figures follow the sources' wording; the chart's −14.0% and +31.5% are the same closes to one decimal. The cause is included so the card doesn't imply the founder story alone moved the stock on Nov 20 (CNBC also cites worry about "life after" him). **The brief's own fact card doesn't have this sentence yet and must be updated before the M6 audit**, which pastes the card from the brief. The sources were read by a research subagent, not yet by the M6 check.
- **Correction to decisions 26 on Nov 11:** the after-hours fall began at 4:55 pm ET (174.58 to 168.20 by 4:59 pm), and the largest one-minute drop came at 5:28 pm. The news check found it followed press reports that afternoon: a newspaper report the 4:55 pm start fits, then minutes later a report that the board was preparing to oust him. Neither report's exact time was found; reports at 5:06 and 5:25 pm already cite them. The announcement itself was a release stamped 8:48 am on Nov 12, with the 8-K accepted at 8:52 am, so **the card's "On Nov 12, Nvidia announced" stands**. The Nov 23 jump at 8:55 am matches the reinstatement release (08:55 am). What the Nov 11 reports were about stays off the card (brief guardrail).

## 28. 2026-11-24 — Where the prices come from (open, human)

A research subagent read the price vendors' terms. **Alpaca's terms forbid publicly displaying its data without its "express prior written consent"**, so the charts in this cut can't be released as they stand. Prices themselves are facts, and the exchange rules for historical data are permissive (the UTP Plan allows end-of-day and historic information in print without restriction, and Nasdaq's policy needs no approval for end-of-day data). The vendor's own terms are what bind. No source found clearly allows this use without a paid plan or written confirmation:
- **Databento (US Equities Mini):** says it allows external redistribution with no licence fees; usage-priced, likely covered by its new-user credit. Daily and 1-minute bars from March 2023; pre-market shown, after-hours unconfirmed. Its terms page didn't load, so ask for written confirmation. Needs the human's own account.
- **Alpaca, with written consent:** keeps the data already pulled.
- **Twelve Data (about $149 a month, plus possibly a $2,400 a year add-on):** an on-screen or description credit is required. Massive (formerly Polygon) Business is $2,499 a month.
- Prohibited or unusable: Yahoo Finance, nasdaq.com, EODHD and Alpha Vantage personal tiers, Tiingo without a licence. TradingView allows its own branded chart images in video, not its data. IEX's free historical files aren't downloadable now, and its own trades alone would change the candles.
Swapping the source means re-pulling the bars and re-running `scripts/market_lines.py`, the two textures and B1/B2. Nothing else changes.

**Update, 2026-11-24: Databento's terms.** The human pasted Databento's Terms of Use and User Agreement (both effective Jan 31, 2024) into `~/Downloads/databento-*.md`. They aren't copied here, since the repo's audit log may become public. Reading of the User Agreement:
- §1.5(e): publishing data, "or other information derived from the same", is Redistribution. It's allowed only if (i) the original data providers' terms allow it or they approve in writing, and (ii) it complies with §1.6 or Databento approves in writing.
- §1.6: every Redistribution must credit Databento ("Data Provided by Databento"). Redistributing also lets Databento name the customer as a client, with name and logo, in its marketing. Only an enterprise contract removes either condition.
- §9.3, and the website terms: when the account ends, so does the right to use the data, and downloaded materials are to be destroyed. Databento may also end the account for convenience (§9.2(a)). The account should stay open while the video is up.
- §1.7 (screenshots of Databento's own pages) doesn't apply: the charts are drawn here.
Condition (i) rests on Databento's dataset documentation, which says US Equities Mini allows external redistribution without licence fees. That's documentation, not the contract, so a written answer from Databento support is still the way to close it.

**Update, 2026-11-24: switched to Databento.** The human accepted the terms above and set a $1 cap. US Equities Mini 1-minute bars, Nov 10–23, cost an estimated $0.0046 (`scripts/fetch_databento.py`). Compared with Alpaca's consolidated bars:
- **Matches:** session opens, highs and lows within a few cents. Nov 12's low is the same 148.80. The Nov 11 fall (4:55 and 5:28 pm) and the Nov 23 jump (8:55 am) are both there.
- **Closes differ:** US Equities Mini has no closing auction, so the last trade differs from the official close by up to $0.40 (Nov 20: 125.93 against 125.53). The candles use Databento's trades. Every printed figure and the dashed line use the official closes in `config/official_closes.json`, which the news reports. The four on-screen figures are unchanged. **For M6:** the Nov 11 close (173.73) still needs a named outlet, and the Nov 19 and 20 closes are only printed by lesser outlets.
- **Extended hours:** its after-hours bars stop at 7 pm ET. The drop chart loses Nov 11's flat last hour (about 159–160) and has 34 candles, not 36.
- **Stray print:** Nov 12 opened pre-market with a single trade at 172.12, against 160.43 the evening before and a 161.50 close that minute. It is left out (`scripts/market_lines.py`), or the chart would show a $10 fall at 4 am that didn't happen.
- **Credit:** "Market data provided by Databento." is added to the end card (`config/cards.json`) and belongs in the video description. The brief's end card needs the same line.
- **Repo:** chart data derived from either vendor (`archive/**/market*.json`) is git-ignored, and Alpaca's raw bars stay in `assets/market/` (ignored), no longer used. B1 and B2 renders from Alpaca's candles are in `archive/m4/boardroom_alpaca_candles/`.

## 29. 2026-11-24 — The locked master, the fade at the cut, phones, chairs, and the stale charts (human notes)

- **Master:** measured against generation 2's lead stem to the sample at nine points. It is the take plus 57,442 samples (1.19671 s) up to the cut, and the take minus one bar (2.088771 s) after it. The intro's new riff keeps the intro's length. The cut lands on the old cut point (237.15 s): a reverb throw dies below −60 dB by 238.45 s on the edit, and the take resumes at the old resume point (241.40 s). So the timing map stands. `config/audio.json` carries the two numbers, and every shot before the cut keeps its frames. After the cut everything plays 1.81 s later than in the stand-in (+43 frames; 7137 frames in all).
- **Postfilter:** music-deslop at 68441e2 (clean tree), `m6f_10k`, `--source suno`, strength 1.0, the flags Distillation (Allegedly) used. Same length, no shift, peak −0.8 dBFS, no fallback reported. The video plays the post-filtered master without its 1.197 s lead-in (silence, peak −64.5 dBFS). The scoreboard's pulse comes from the master's own bass stem, since the bass was lifted.
- **Fade to black:** E22 side runs through the throw and fades to black over it (31 frames, easing in). Then 20 frames of black, and the booth on the resume.
- **Stale charts:** the screens baked into E11, E11 close and E22s were rendered before the real-data textures existed, and showed through until the live chart started (1–8 frames). The live chart now covers the screen from each shot's first frame and starts growing on its cue. All board shots are re-rendered with the current textures.
- **Chairs:** box chairs (flat grey slabs) are replaced by modelled mid-back office chairs: a cushioned seat, a curved and tapered back with rounded corners, a gas lift and a five-star base on casters, in dark leather and dark metal. The back keeps the old height (about 1 m), so it hides no more of the sitters. The probe's grey box pedestal outside the glass is now a slim column on a round foot. E08 is re-rendered for the chairs only; its votes and her footage are unchanged.
- **Phones** (`remotion/src/components/Phones.tsx`): every screen has a status bar and content from its first frame.
  - **E03:** a message thread. It has a header, a date stamp, a typing indicator until the filing arrives, and a composer bar.
  - **E18p and E19:** the night phone wakes to a lock screen (wallpaper, date, clock). The message and the missed calls arrive as notifications.
  - **E07:** avatars, ringing pulses, and decline and accept buttons. Accept is white, since the brief bars green.
  - A faint glass sheen and darker edges sit the held screens into their plates. Glyphs are drawn here, with no OS icons.
  - **New on-screen text for M6:** "Thursday, Nov 12 · 8:52 AM" (the 8-K's acceptance time), "Tuesday, November 17" (the day he said he'd be honored), "Board of Directors", "typing…", "Message", "MESSAGE", "PHONE", "now", "Incoming call", "calling…", "Decline", "Accept", and the clocks "8:52", "11:48" and "9:14" (set dressing).

## 30. 2026-11-24 — The bookends: the real screenshots, and the terminal in place of the screen recording (human note)

- **E01, the Nov 12 screenshot (3 s, brief):** cropped to the newsroom header, the headline and the date (`remotion/public/gen/captures/E01_release.png`, from x 94–1270, y 205–770 of the human's capture). The crop leaves out:
  - the browser bar, which shows a profile name;
  - the media contacts, which are real people's names;
  - the release's bullets, which name the interim CEO (brief: never named).
  The right edge cuts the newsroom menu mid-word ("In the N"). Nothing in the picture is altered. Captioned "real screenshot · Nov 12, 2026".
- **E01t (new ID), the terminal, in place of the generation screen recording:**
  - **nvidia-smi:** 7.7 s, before the song. The output is real, captured while the GPU ran a production stage at full load. The boardroom render barely registered (6–26%, Blender not in the process list), so the capture came from a re-run of the music-deslop postfilter on the locked master. That re-run's output matched the master's postfilter byte for byte, so nothing in the video changed. The capture shown (`assets/captures/nvidia_smi/postfilter/nvidia-smi_022618_55.txt`, picked by `scripts/e01_terminal.py`) has the RTX 5090 at 100% load, 572 W of 575 W, 68 °C, with the postfilter's process on it. It is typeset in Liberation Mono (SIL OFL), with trailing spaces trimmed.
  - **The script:** `scripts/effective-immediately` is a real script, run to check its output. It prints "Effective Immediately", "AI-generated satire", "Not investment advice", then "generating" with three dots, and the terminal keeps its pauses. It makes nothing itself, and its comment says so. The song starts as the dots finish.
  - **Privacy:** no prompt user or host is shown, just "$". nvidia-smi truncates the process paths itself, so no home directory appears. Product names (RTX 5090, CUDA) appear only inside this bookend, which the brief allows for real captures.
- **E25, the Nov 23 screenshot:** cropped the same way (the headline names only the founder), now 3 s instead of 1.75 s, captioned "real screenshot · Nov 23, 2026".
- **Order:** E01 screenshot, E01t terminal, the song. Music starts at frame 256 (it was 72), so everything after moves 184 frames later. Board renders are unaffected (their cues are local). The brief's E01 row still describes the screen recording, and needs updating.
- **Repo:** the full-page captures are git-ignored. The nvidia-smi captures (`assets/captures/nvidia_smi/`) are small text files kept as evidence.

## 31. 2026-11-24 — The credits instrumental carries the cards at reading pace (human note; closes decisions 22's open item)

- **Postfilter:** the same music-deslop run as the master (68441e2, `m6f_10k`, `--source suno`, strength 1.0). Same length, peak −3.46 dBFS, no fallback reported.
- **Placement:** the song ends and E25 (the Nov 23 screenshot) holds for 3 s over its ring-out. The instrumental starts with the first fact card and plays to its end.
- **Timing** (`scripts/credits_audio.py`, `scripts/cut_list.py`): each card's length is its share of the 513 words at one even pace, 179 words a minute. Every change lands on one of the track's beats (117.5 bpm). Fact card 1 runs 59.7 s, card 2 44.7 s, card 3 16.4 s, and the disclosure 50.7 s. The dated cards follow (7.2 s, one per bar), then the final card (7.4 s), which lands 6 s before the music stops and holds through it.
- **The ending:** the track plays at full level until 184.7 s and stops within a quarter second, which is how the human supplied it. Not changed.
- **Length:** the video is now 7:54 (11,368 frames): 10.7 s of opening, the song (4:34), and 3:09 of cards.
- **Disclosure:** "Music: Suno" covers the instrumental too. Whether the end card should name the cover separately is left to the human.

## 32. 2026-11-24 — The disclosure filled in, as the conflicted party (human note)

- **Image generation:** Claude Code ran every model (FLUX.2 [dev] for stills and keyframes, LTX-2.3 for clips), so the line stays and now says so. The end card reads "Stills: FLUX.2 [dev]". The placeholder marker no longer flags "[dev]", which is part of the model's name.
- **Makers' ties to Nvidia:** a research subagent read the primary pages (sources in `config/disclosure_sources.json` and `docs/sources.md`).
  - **Anthropic:** Nvidia pledged up to $10bn (Nov 2025). It bought about $10bn of Class N shares in a placement alongside the Nov 2026 IPO (424B4, CNBC). How much of the pledge was paid in, and whether the IPO stake counts toward it, is unconfirmed, so the card states the two facts separately and doesn't add them. **Claude wrote this line about its own maker; it goes to the M6 auditors and the human as a conflicted claim.**
  - **Suno:** Nvidia's venture arm (NVentures) was in its Nov 2025 Series C.
  - **Black Forest Labs:** lists Nvidia among its Series A investors, and Nvidia co-optimized FLUX.2.
  - **Lightricks:** Nvidia published RTX optimizations for LTX-2. No investment found.
  - **OpenAI:** the brief's "intends to invest up to $100bn" is out of date: that 2025 letter was never finalized, and Nvidia instead invested $30bn in OpenAI's 2026 round.
  - **Google:** an Nvidia customer and partner that builds rival chips and is a major Anthropic shareholder.
- **The creator's holdings, from the human's words:** "holds no Nvidia shares directly; a third party manages their retirement savings and, to their knowledge, holds none directly." Broad funds may still hold Nvidia, and the card doesn't say so. That's the human's call.
- **Length:** the disclosure is 132 words (up from 108). The tail's reading pace is now 188 words a minute. Fact card 1 runs 57 s, card 2 43 s, card 3 16 s, the disclosure 56 s.
- **E19's callers** ("Employees, Investors, Partners, Customers"): the brief calls them "the groups his statement named" and cites no source. The screen claims nothing about a statement, so they are listed as set dressing in `docs/sources.md`.

## 33. 2026-11-24 — Release preparation (human note)

- **Fact card:** "[Update with the outcome.]" is removed. The video goes out before the Dec 1–2 interviews, which the card calls scheduled.
- **End card:** following the series (Distillation (Allegedly), Buy It on Margin), the on-screen credits don't name the human. It reads "Direction, take selection, editing and every human intervention: a human, listed in the production log", and "Sources, audits and production log: github.com/Derivative-Work/effective-immediately". The licences name the copyright holder, as the siblings' do.
- **Brief (Claude Doc, rev 105 → 114), edited directly:**
  - the fact card's price sentence, and the interviews placeholder removed;
  - the disclosure and the end card;
  - the opening bookend (E01t), in the shot table and the Bookends section;
  - the human's inputs;
  - a paragraph on the credits music and Databento;
  - the release-day audit prompt's stakes, and its "[image model]" filled in;
  - the new sources, appended to its Sources section.
  `docs/brief.md` is re-mirrored.
- **Publishing files, after the siblings:** `README.md`, `LICENSE` (MIT), `LICENSE-media.md` (CC BY-NC-SA 4.0, with what it doesn't cover: fonts, the ComfyUI template, the people kit, the real captures, Databento's data, the auditors' outputs), `LICENSES/CC-BY-NC-SA-4.0.txt`, and `METADATA.md`. METADATA.md has the title options, description (under 5,000 characters, with chapters, facts, sources, the Databento credit and the licence), tags, settings, three thumbnail options and the pre-upload checklist.
- **Titles:** the alternatives avoid "fired". The 8-K and the release say he resigned, so "out" and "broke up with" stay accurate.
- **Thumbnails** (`remotion/src/Thumbnail.tsx`, `deliverables/thumbnails/`): A, the empty hook and the jacket back in the booth (recommended); B, the empty hook; C, the empty counselor's chair. None has Nvidia's name, logo, green or a face.
- **Final render:**
  - the boardroom at full resolution (`SCALE=1 SAMPLES=32`; half-resolution renders in `archive/m4/boardroom_half_res/`);
  - then Remotion at 1920×1080 with the animatic's shot labels off (`slate: false`), to `deliverables/effective_immediately_1080p.mp4`;
  - captions in `deliverables/effective_immediately.en.srt`.
- **Not made for today:** the brief's vertical Shorts cut of chorus 1. It can follow the main upload.

## 34. 2026-11-24 — The opening becomes a panel over the intro (human note)

- **The song starts on frame 0** (it started at 10.7 s). E01 (the Nov 12 screenshot, 3 s) and then E01t (the terminal, 7.7 s) play in a panel 1,100 px wide on the left, while the intro's footage (E02) plays on the right. The panel slides out over 12 frames as the script's dots finish. This follows Distillation (Allegedly)'s merged D01/D02.
- **Nothing is cut.** Every clip keeps its length. The screenshot and terminal keep theirs. The terminal is set at 19 px to fit the panel.
- **Effects:**
  - The video is 7:43.0 (11,112 frames), and everything after the opening is 256 frames earlier.
  - Board cues are unchanged, since they are local to each shot.
  - Subtitles, chapters, the end screen and the captions file are re-timed (`METADATA.md`, `deliverables/effective_immediately.en.srt`).
- **Framing under the panel (human, same day):** the first version only covered the intro footage, so its subjects sat under the panel (G14's walker at about half the width, G01's walker at the doors). The footage now sits in the 814 px right of the panel, cropped at full scale, not shrunk, around each clip's subject (`OpeningReframe` in `remotion/src/Animatic.tsx`). G14 pans with its walker from 0.50 to 0.31 of the width, G13 holds on the feet at 0.58, and G01 follows the walker from 0.42 to 0.60. The box widens back to the full frame as the panel slides away. This is how Distillation (Allegedly) placed its D02 beside its panel.
- **Thumbnail A (the human's pick; "the jacket is cropped"):** the booth half had started 12% into the plate, cutting the jacket in half, and the title covered its lower half. The booth half now starts at the plate's left edge, so the whole jacket shows (the plate itself ends at its far-left edge, beside the divider). The title runs across the top and the dates sit in the bottom corners, clear of the jacket and the hook.
- **Thumbnail A's text, for phones (human, after upload: "thumbnail text needs to be bigger to be legible on mobile"):**
  - **The problem:** in one line across the top, the title could be no wider than about 100 px a letter-height before it
    ran into the jacket's collar. "(until further notice)" was 32 px and the dates 46 px, about 4–6 px tall in a phone's
    smaller lists.
  - **The halves are now unequal:**
    - The booth half is 450 px wide, just enough for the whole jacket (440 px at the plate's scale).
    - The hook half is 830 px, with bare wall only.
  - **New text layout and sizes:**
    - The title stacks in two lines on the hook's wall at 116 px, with "(until further notice)" under it at 56 px.
    - Each date sits at the top of its half at 84 px in Inter, above the hook and the collar.
  - **The hook's plate:** S01 is scaled to 0.8, a little past cover, and anchored at its foot. This lifts the hook clear of
    the title and makes it bigger.
  - **Check:** downscaled to 360 and 168 px wide, the title and dates read at both sizes, and the subtitle at 360. The
    previous version is in `archive/thumbnails/`.
- **Thumbnail A, the jacket against the seat (human: "the jacket is blending in with the seat it's on. See about increasing
  the contrast between the two for the thumbnail only"):**
  - **The problem:** in the plate, the black leather lies on a dark red-brown booth. Their colours are too close to separate by
    colour alone: the lit leather is as warm as the booth, and in the bottom shadows both are black.
  - **The fix, in the thumbnail only:** `scripts/thumb_jacket.py` writes `S03_thumbA.png`, a copy of the plate that
    only thumbnail A uses. The video's S03 is unchanged.
    - The jacket is masked with SAM 2.1, prompted with a box and points. The model is Meta's, Apache 2.0, downloaded from
      Hugging Face.
    - The booth is brightened and its shadows lifted to a warm brown.
    - The jacket is desaturated to a neutral black, with deeper shadows and brighter highlights, so its sheen stays.
    - The mask's edge was checked at 1:1 and at phone sizes. Where the plate has no visible edge (the jacket's lower left,
      in shadow), the outline is SAM's estimate.
  - **Why a baked file and not CSS:** the same grade done with CSS blend layers in Remotion came out visibly softer in
    Chrome's render.
  - The previous version is in `archive/thumbnails/`.

## 35. 2026-11-24 — Four vertical Shorts (human note; the brief asked for one)

- **The four** (`config/shorts.json`, `remotion/src/Shorts.tsx`, compositions `Short-<id>`), each a stretch of the main edit cut on shot boundaries:
  - **chorus:** the brief's Short, E08 through chorus 1, 43.0 s;
  - **bridge:** the night phones to SENIOR LEVELS, 34.1 s;
  - **reinstated:** the final chorus to the compliance officer sign, 37.0 s;
  - **plaque:** the outro, ending before the credits, 17.8 s.
- **Layout, after Distillation (Allegedly):**
  - the "Effective immediately" lower third as the title (brief), with "AI-generated satire · not investment advice" over it;
  - the main edit's whole picture, uncropped at 950 px wide, so nothing in its framing is lost;
  - the lyrics under it, in each section's subtitle style, scaled to fit (`SubLine`, exported from `Subtitles.tsx`);
  - all of it centred in the platforms' safe zone (y 140–1400, clear of the right-hand buttons).
  The music starts on the first frame, with short fades added at encode.
- **Captions:** `scripts/shorts_srt.py` writes one SRT per Short, timed from its first frame. Fragments under 0.7 s at either edge are left out.
- **Metadata:** each Short's title and description in `METADATA.md`. Every factual line restates the fact card, and the footer carries the conflict of interest and the Databento credit.
