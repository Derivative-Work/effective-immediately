# Shot pipeline

Each shot's asset type and any swap. Picks are provisional until the M3 gate (`config/picks.json`). Types follow the brief:
K code (Remotion), S still, C clip, B Blender. Lengths and every beat-synced move wait for the timing map.

| Shot | Type | Asset (provisional pick) | Status or swap |
| --- | --- | --- | --- |
| E01 | K + capture | Real screenshot and screen recording | **Needs the human's captures** |
| E02 | C | G01 `G01_s1123` | |
| E03 | S + K | `hand_phone_s1125`, UI pinned to its screen (`FilingPhone`) | Was code only (decisions 14) |
| E04 | S + cutout | S01 `S01_v2_s1123`, jacket `jacket_s1123` | The wall is generated empty and the jacket composited (decisions 10) |
| E05 | S + cutout | The same, jacket lifts off the unfaded patch | |
| E06 | C + K | G02 `G02_s1123` from retouched keyframe, flashes, lower third | Doors open behind her, which the prompt didn't ask for |
| E07 | K | `FourPhones` | |
| E08 | B | Boardroom, procedural narrator silhouette, kit arms | Weakest asset: her figure is simple |
| E09 | B + K | Overhead ring of hands, lower third | Votes on the placeholder grid |
| E10 | C | G03 `G03_s1124` | |
| E11 | B + K | Boardroom, market line, confetti | The line is a still on the screen until M4 |
| E12 | C | G04 `G04_s1123` from retouched keyframe | |
| E13 | S + K | G04 keyframe, scoreboard | Bass pulse is a placeholder |
| E14 | C | G05 `G05_s1124` from retouched v2 keyframe | No bouquet (decisions 10) |
| E15 | C + K | G06 `G06_s1124`, calendar insert | Cued to a lyric the current take doesn't sing (decisions 1) |
| E16 | C | G07 `G07_s1123` | |
| E17 | C + B | G08 `G08_s1123`, one-beat ring insert | |
| E18 | C + S + K | G09 `G09_s1123`, then `hand_phone_night_s1125` with the UI pinned | Phone was code only (decisions 14) |
| E19 | S + K | `hand_phone_night_s1125`, UI pinned to its screen (`LockScreen`) | Was code only (decisions 14) |
| E20 | S + K | G10 keyframe, caller ID on its display | |
| E21 | C + K | G10 `G10_s1125`, tracked caller ID, tags | Two earlier takes rejected, one for a generated face (decisions 11) |
| E22 | S + B + K | Jacket returns; screen insert; vote with the probe composited after the grade | |
| E23 | S + K | S02 `S02_s1123` retouched, signs | |
| E24 | C + S + K | G11 `G11_s1124`; **G12 swapped to its held last frame** (decisions 12); S03 `S03_s1123`; plaque; counters | |
| E25 | K + capture | Real screenshot, fact card, disclosure, end card, closing cards | **Needs the screenshot and the card placeholders filled** |

## Added coverage (decisions 20)

The exact cut is in `remotion/public/gen/timing/cut.json`, built by `scripts/cut_list.py`.

| Where | New assets |
| --- | --- |
| E02 intro | G14, G13, G15, G16 around G01 |
| Chorus 1 | G17, G18, G19; board angles B1, B2 |
| Verse 2, post-chorus | G05b, G20, G21, G22 |
| Chorus 2 | G23, G24, G25, G26, G34, G35; board angle E11c |
| Bridge | G27, G28, G29, G30 |
| Final chorus | G31, G32, G33; board angles E22p, E22o, E22b |
