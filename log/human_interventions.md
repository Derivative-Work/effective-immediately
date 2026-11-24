# Human interventions

Append-only. Every human action: when, what, and why.

## 1. 2026-11-12 to 2026-11-23 (logged retroactively) — Planning chat and brief

- **What:** The human developed the song and brief with Claude over 44 messages, ran audit round 1 in ChatGPT and Gemini,
  and decided the two contested findings (cold light until the reunion; the probe outside the glass).
- **Evidence:** `docs/planning_chat/` (indices 0–43, 2026-11-12T16:15Z to 2026-11-23T18:13Z; snapshot taken
  2026-11-23T18:33:01Z); the brief at rev 105 (`docs/brief.md`).

## 2. 2026-11-23T18:07:45Z (Suno's created_at; logged retroactively) — Suno take

- **What:** The human generated the song in Suno and chose this take.
- **Take:** clip `cc8528ed-aea9-45cd-a778-6a9e10bb6575`, shared as https://suno.com/s/uIZ5J4Hu7othl3Iq. Model v6
  (`chirp-hawk`), 252 s, task `cover`, `aug_creativity` 1. Style and lyrics as pasted are in `log/prompts/m0_suno.md`.

## 3. 2026-11-23 — Project start

- **What:** "Let's get started with the brief", with the planning chat to archive, the chosen generation, the song in
  `~/Downloads`, and the previous songs as look-but-don't-touch references: "pay attention to the video generation plan,
  otherwise you may run out of memory."
- **Supplied:** `Effective Immediately.wav` and `Effective Immediately Stems.zip`.

## 4. 2026-11-23 — Proceed without the timing map

- **What:** After the M1 lyric diff (decisions 1–3): "I'm trying to get this out as quickly as possible: do what you're
  able to without a timing map (sets, initial generations, etc.) and I'll get you corrected audio later".
- **Effect:** M2 and M3 work starts before the M1 gate. Corrected audio is still to come, so the timing map, beat-synced
  moves and anything cut to the track wait for it.

## 5. 2026-11-23 — Notes on the first-pass reel

- **What:** "Phone screens need a better hand"; "Jacket coming off the hook feels off"; "Boardroom hands feel off -- it may
  be useful to reference the people kit from the other songs"; "'SENIOR LEVELS' is not aligned to the screen -- see how
  Ever Present did it"; "Probe's text at boardroom is not legible -- is this intentional?"; "Also for a later stage: I'll
  give you an Alpaca key to pull the actual stock ticker from the relevant time periods".
- **Effect:** production log 9, decisions 14–17. The Alpaca key hasn't been supplied yet. When it is, it stays out of git.

## 6. 2026-11-23 — A new generation to evaluate

- **What:** "Once you have cycles: the new generation and stems are in ~/Downloads; let me know how that one fares before
  committing to it".
- **Supplied:** `Effective Immediately(1).wav`, `Effective Immediately.mp3` and `Effective Immediately Stems(1).zip`
  (Suno id `043cee54-da40-4974-9006-af3afc9b0ee4`, created 21:31:12Z, 276.4 s).
- **Effect:** imported to `audio/candidates/gen2/` only. `audio/track/` and `audio/stems/` stay as they were until the
  human picks.

## 7. 2026-11-23 — Generation 2 confirmed; notes on the revised reel

- **What:** "It's 'took your jacket' and 'call comes down' as requested." "The hands are better but still feel off. Something about them raising is not quite right (though I do appreciate that it is no longer a straight-arm salute...)" "The plaque coming off the wall and going back are way too sudden, and the shot showing the jacket right after needs to be held for longer." "Regarding the audio: I'll make the cut manually, but make what you can with what you have. I'll do my best to make it so that it's a straight offset at the cut point."
- **Effect:** generation 2 is the working audio. The human will supply the locked master with the cut. Everything after the cut is timed through one offset, so the master only changes that number.

## 8. 2026-11-23 — Notes on the first animatic

- **What:** "Concept reads well, but I'm noticing that there's lots of repeated and time-stretched scenes -- see about reducing these. Also, instead of cutting out at the end, use the remainder of the music as the credits". Then: "also, the board's hands are still not reading right, mostly because it's unclear where the hands are supposed to be coming from".

## 9. 2026-11-23 — Notes on the second animatic

- **What:** "I will make a credits instrumental. For the video: For the boardroom and similar scenes, let's try a version where one hand goes up at a time on the beat. Also for the boardroom, the CEO is still obviously a render. (I guess you were going to get to these in one of the later stages.) This one could use burned in subtitles. Try out some styles, ideally period/set appropriate".
- **Reading:** "the CEO" is taken to be the walking figure in E08, the narrator. The brief has her as the company and never depicts the interim CEO, so she stays that.

## 10. 2026-11-23 — Subtitle style, vote rule, and the market data

- **What:** "Subtitles A. Let's only keep the one hand per beat on the scenes that are actually visible long enough for it to be seen, otherwise use the all down/all up on beat. E08 is great. Alpaca key is in ~/Downloads/price-title.env: it's in the same format Share the Shares title updater expected, and is only attached to a paper trading account".
- **Handling of the key:** read at run time from that file. It isn't copied into this repo, logged or printed, and is only sent to Alpaca's market-data API. Read-only requests; no orders.

## 11. 2026-11-23 — Subtitle wording confirmed

- **What:** "Subtitles are correct." This covers the four spots flagged in decisions 25, so `lyrics/as_sung.txt` and the subtitles stand as they are, including the last line without "no".

## 12. 2026-11-24 — Fact card, candlesticks, and the data source

- **What:** "right it's in ~/Documents/..." (the key's location, used for decisions 26). Then, on the fourth animatic: "Yes, add the jumps to the fact card. They may be even more visible if using a candlesticks representation instead of a line graph. Fair point on #2: where else can you get the data from?"
- **Effect:** the Nov 20 fall and Nov 23 rise go on the fact card; both screen charts become candlesticks (decisions 27). Other price sources and their terms were researched for the human to choose from.

## 13. 2026-11-24 — Databento account and terms

- **What:** "I have a Databento account now, what do you need from me to use its data". Then "I pasted the terms in ~/Downloads/databento-*.md" (Terms of Use and User Agreement, both effective Jan 31, 2024).
- **Effect:** the terms were read and summarised for the human (decisions 28). They are not copied into this repo.

## 14. 2026-11-24 — Databento key; spend cap

- **What:** "API key is present. Go ahead, with the under $1 constraint."
- **Supplied:** the key in `~/Documents/databento.env`. It is read at run time by `scripts/fetch_databento.py` and sent only to hist.databento.com. It is never copied, logged or printed.
- **Effect:** the free cost estimate came to $0.0046 and the pull went ahead (production log 17).

## 15. 2026-11-24 — Notes on the sixth cut; the locked master

- **What:** "All of the phone screens are too plain -- some of the white screens are reading as a compositing error rather than intentional (even though the compositing is perfect once it appears)". "Some of the old placeholder (non-Alpaca, fake data) graphs are still appearing for a frame or two before the new Databento data". "Check for gray box in the rendered scenes -- the chairs in particular are standing out". "New master and stems are in. See ~/Downloads/effective-immediately{-stems,.wav}. Main differences against what you have: there is a slight offset at the beginning for ease of editing on my part, bass is boosted and has more high end, riff from chorus copy/pasted into the intro, cut added with a reverb throw so it reads as intentional. Fade to black at the cut instead of cutting straight to it. There's now only one measure between the "in--" and the following lyrics (not two)." Then: "oh also you will need to run the postfilter against the master".
- **Supplied:** `effective-immediately.wav` (275.76 s, 48 kHz, 32-bit float) and twelve stems (AIFF), copied to `audio/master/` (Downloads untouched).
- **Effect:** decisions 29; production log 18.

## 16. 2026-11-24 — The release screenshots, and a new opening

- **Supplied:** two screenshots of Nvidia's newsroom, pasted into the conversation: the Nov 12 "NVIDIA Announces CEO Transition" release and the Nov 23 "NVIDIA Board Reinstates Jensen Huang as President, CEO and Board Director" release. Copied to `assets/captures/releases/` (git-ignored, decisions 30).
- **What:** "For the bookends. I also want to redo the opening bookend: instead of showing the generation screen, let's demonstrate complicity by showing the output of `nvidia-smi` during a heavy stage (like the render you're running right now), then demonstrate "running" a script that first prints something to the effect of "Effective Immediately" "AI-generated satire" "Not investment advice", then "generating...", then cut to the video".
- **Effect:** decisions 30.

## 17. 2026-11-24 — The credits instrumental

- **What:** "For the credits: see ~/Downloads/effective-immediately-credits.wav. You'll need to run the postfilter on it too. Suno share link: https://suno.com/s/n2YP4Uh76eIDOVJy. It's an instrumental cover, with the previous early 2010's breakup song style prompt from before production began."
- **Supplied:** `effective-immediately-credits.wav` (185.56 s, 48 kHz, 16-bit), copied to `audio/credits/`. The share page is archived in `docs/suno/credits/` (Suno v6 "chirp-hawk", clip `70fd236d-44b4-4ba5-a3b8-104403769489`, instrumental cover, created 2026-11-24 07:27 UTC; style "2010s stomp-clap pop with a disco-funk verse and four-on-the-floor pulse…, 116 BPM").
- **Effect:** decisions 31.

## 18. 2026-11-24 — The disclosure placeholders, the audits, and a source list

- **What:** "I didn't drive any video or image generation -- did you use an image generator? If not, cut the line." "I pasted the contents of the audits in ~/Downloads/effective-immediately-audit-*.md for you to get their disclosures. You can get your own for Claude." "I am not currently directly managing a stock portfolio. A third party is handling my retirement assets, and I do not believe they directly included any NVIDIA in my holdings." "I'd also like links to sources to fact check." "Other than those, is there anything you need from me".
- **Supplied:** the Round 1 audits (ChatGPT, Gemini), saved verbatim in `log/audits/`.
- **Effect:** decisions 32; `docs/sources.md`.

## 19. 2026-11-24 — Push to GitHub; an updated master

- **What:** "In the meantime, I made https://github.com/Derivative-Work/effective-immediately and gave you access. Push what you currently have up". Then: "for the next one: I updated the master in ~/Downloads/effective-immediately.wav. This one has less crackle. It still needs the postfilter though."
- **Effect:** the first commit (`e76c383`) was pushed to `main` on the new private repo. The repo was empty, so there was no branch to start from. The updated master replaced the first one (kept as `audio/master/effective-immediately_master_v1.wav`), was post-filtered, and went into the ninth animatic (production log 19).

## 20. 2026-11-24 — Release today; brief, GitHub, metadata, publishing

- **What:** "I am starting on the sources review now. I plan on releasing today, as soon as I am both satisfied with my review and you are done with the render, so get rid of the "update with...". Yes, update the brief and GitHub. Also make the METADATA.md including clickbait-adjacent title and thumbnail options". Then: "oh and otherwise get GitHub ready for publishing (README, licenses, etc. along the lines of the others)".
- **Effect:** decisions 33.

## 21. 2026-11-24 — The music starts sooner; checks done

- **What:** "My only remaining issue with the animatic is that it takes too long for the music to start. See about shortening this without cutting content (maybe overlaying things? see "Distillation")". Then: "I'm good on fact checks and audits at this point".
- **Effect:** decisions 34. The human's review of the sources is done; no further audit round.

## 22. 2026-11-24 — The framing under the opening panel; thumbnail A; Shorts

- **What:** "How are the overlays done for the intro? I'm concerned that the framing of the video underneath it may be off with this -- double check". Then: "I prefer thumbnail A, but do the same check for it -- the jacket is cropped". Then: "Once that's done also make some shorts cuts".
- **Effect:** decisions 34 (framing under the panel, thumbnail A) and 35 (Shorts).

## 23. 2026-11-24 — The main video uploaded

- **What:** the human uploaded the main video to YouTube and gave its link: "video URL https://youtu.be/i5uLYgoSIkk".
- **Effect:** the link went into the README ("Watch it on YouTube") and the Shorts' shared footer in `METADATA.md`, ready
  for the Shorts' upload. The description's intervention count in `METADATA.md` went from 19 to 23.

## 24. 2026-11-24 — Thumbnail text for phones

- **What:** "thumbnail text needs to be bigger to be legible on mobile".
- **Effect:** decisions 34 (thumbnail A's text, for phones). Thumbnail A re-rendered; the human replaces it on YouTube.

## 25. 2026-11-24 — The jacket against the seat, in the thumbnail

- **What:** "Hm the jacket is blending in with the seat it's on. See about increasing the contrast between the two for the thumbnail only".
- **Effect:** decisions 34 (thumbnail A, the jacket against the seat). Thumbnail A re-rendered from a graded copy of S03; the video is unchanged.

## 26. 2026-11-24 — SAM is already in Share the Shares

- **What:** "SAM is already in share the shares".
- **Effect:** `scripts/thumb_jacket.py` uses Share the Shares' SAM ViT-B checkpoint, read in place, instead of a downloaded SAM 2.1. The download was deleted. Decisions 34; thumbnail A re-rendered, with the same look.

## 27. 2026-11-24 — A glow around the jacket

- **What:** "Use the mask to add a glow around the jacket".
- **Effect:** decisions 34 (thumbnail A, the jacket against the seat). Thumbnail A re-rendered; the video is unchanged.

## 28. 2026-11-24 — The seat in the jacket's mask

- **What:** "Check the segmentation again: it's including part of the chair as the jacket at the bottom left".
- **Effect:** decisions 34 (thumbnail A, the jacket against the seat). The mask's points were corrected and thumbnail A
  re-rendered; the video is unchanged.

## 29. 2026-11-24 — The release, with the Logic project

- **What:** "Also create the release in line with the other songs. The Logic project is in
  ~/Downloads/effective-immediately.logicx.zip -- only in-the-box plugins used, all audio directly from the stems, no
  samples added".
- **Supplied:** `effective-immediately.logicx.zip` (315 MB, sha256 `7b3dda0f…`), copied as it is to `audio/logic/`
  (Downloads untouched).
- **Effect:** the v1.0 GitHub release, built by `scripts/release.sh` (production log 22).
