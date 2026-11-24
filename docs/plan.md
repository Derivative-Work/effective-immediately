# Production plan

Milestones from the brief (rev 105), with a human gate at the end of each. The memory plan for generation is in
`CLAUDE.md`.

| # | Milestone | Status | Human gate |
| --- | --- | --- | --- |
| M0 | Setup and import: brief mirror, planning chat, Suno record, audio and stems, environments, logs | Done 2026-11-23 | None |
| M1 | Transcribe and diff against the brief; timing map (beats, sections, lyric lines, cut-off) and frame ranges per shot | **Done on generation 2**; the locked master is measured against it to the sample and post-filtered (decisions 29) | Check the map by ear; confirm lyrics as sung |
| M2 | Look layer and every code component in Remotion, reading `config/saga.json` | **First pass done, at the gate** (`review/m2_look_on_plates.jpg`) | Approve the look |
| M3 | References, then all stills and clips (memory plan); the boardroom, vote loop and alpha renders in Blender | **First pass done, at the gate** (`review/m3_reel.mp4`); final boardroom renders wait for the timing map | Pick takes; flag fallbacks |
| M4 | 540p animatic of every shot | **Sixth cut done, at the gate** (`review/m4_animatic_v6.mp4`, decisions 19–28) | Approve timing |
| M5 | 1080p final, captions and SRT, Shorts cut, thumbnail | Not started | Approve the finals |
| M6 | Concept audit, then a fact check of every card by other labs' models | Not started | Resolve every flag |

M2 and M3 can run in parallel once M1 is approved.

## Needed from the human

1. ~~The locked master with the cut~~: in, post-filtered and measured (decisions 29).
2. Approve or change the outro's instrumentation (the stand-in is voice and guitar only; decisions 3).
3. For the bookends: the screen recording of the real generation and the two release-headline screenshots.
4. For the disclosure card: the image model's name and maker if not FLUX.2 [dev], and any Nvidia holdings.
5. The credits instrumental (the human is making it), to carry the fact card and disclosure at reading pace, about 3 minutes (decisions 22).
6. Chart prices now come from Databento (decisions 28). Keep the account open while the video is up, and put "Market data provided by Databento" in the description.
7. The brief's fact card needs the Nov 20 and Nov 23 sentence, and its end card the Databento credit, before the M6 audit (decisions 27, 28).