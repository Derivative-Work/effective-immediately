# Upload metadata

YouTube metadata for the main video, ready to paste at upload. Written by the agent; the human uploads.

**Before uploading:**
- **Sources review:** done by the human on Nov 24 ([`docs/sources.md`](docs/sources.md)). Any later change to a card means re-rendering the tail.
- **Re-check the news** on the day. The cards and the description are as of November 24, 2026. The House interviews
  (Dec 1–2) are still ahead; the fact card says "scheduled".
- **Make the repository public.** The end card and the description link to
  https://github.com/Derivative-Work/effective-immediately, which is private until then.
- **After upload:** put the video's link into the README ("Watch it on YouTube").
- **Intervention count.** Update the number in the description if more are logged
  (`grep -c '^## ' log/human_interventions.md`; 19 on 2026-11-24).
- **Databento's terms** require "Market data provided by Databento" wherever the data is published: it is in the end
  card and in the description below. Keep both.

---

## Main video (16:9, 1920×1080, 24 fps, 2.39:1 picture)

**File:** `deliverables/effective_immediately_1080p.mp4` (7:43.0). Captions: `deliverables/effective_immediately.en.srt`.
Thumbnail: `deliverables/thumbnails/effective_immediately_thumbnail_A.jpg` (or B or C, below).

### Title

Recommended (75 characters):

```
Out "Effective Immediately," Back in 11 Days: Nvidia's CEO Breakup, as Disco
```

Clickbait-adjacent alternatives, each true to the record:
- `The Board Said "Effective Immediately." It Meant 11 Days. (AI Disco Breakup Song)`
- `Nvidia's Board Broke Up With Its CEO. Then Took Him Back. (AI-Made Disco)`
- `A Breakup Song for Nvidia's 11-Day CEO U-Turn, Made on an Nvidia GPU`
- `"Six Hundred Billion Says You're Good Enough for Me": the Nvidia Breakup Song`
- `We Did Not Intend to Take Him Back: an AI Disco Song About Nvidia's Board`

Avoid "fired": the 8-K and the release say he resigned. Reports said the board was preparing to oust him, so "broke up
with" and "out" stay true without claiming a dismissal.

### Description

```
AI-generated satire. Not investment advice.

On November 12, 2026, Nvidia announced that its co-founder had resigned as CEO, effective immediately. Eleven days later the board reinstated him, unanimously. This is the breakup song, sung by the company: a bass-forward boogie-funk disco number in which the founder is only ever a black leather jacket on a hook, and the board's hands go up on the beat.

WHO HAS A STAKE
The lyrics were written by Claude, and the video made by Claude Code, both from Anthropic. Nvidia is an Anthropic shareholder: it pledged up to $10bn in 2025 and bought about $10bn of shares alongside Anthropic's November 2026 IPO, and Anthropic runs Claude partly on Nvidia GPUs. Music: Suno, backed by Nvidia's venture arm. Stills: FLUX.2 [dev] (Black Forest Labs, Nvidia-backed). Clips: LTX-2.3 (Lightricks; Nvidia optimized its models, no investment found). All of it ran on the creator's Nvidia RTX 5090, as the opening shows. The creator holds no Nvidia shares directly. The plan was audited on Nov 23, 2026 by ChatGPT (OpenAI, in which Nvidia invested $30bn in 2026) and Gemini (Google, an Nvidia customer that builds rival chips and is a major Anthropic shareholder).

Every frame, note and word was made by AI: the song by Suno, the words by Claude, the pictures by FLUX.2, LTX-2.3 and Blender, the edit by Claude Code. A human approved each stage, edited the master, picked the takes and ran the audits. Each of those 19 interventions is logged, along with every prompt and production step:
https://github.com/Derivative-Work/effective-immediately

CHAPTERS
0:00 Intro: the release, and the GPU that made this
0:18 Verse 1: filed the paper
0:33 Pre-chorus: three committees calling
0:49 Chorus: effective immediately
1:24 Verse 2: the quarter
1:47 Post-chorus: we've got this
2:00 Chorus 2
2:34 Bridge: senior levels
3:08 Final chorus
3:34 A Chief Compliance Officer
3:45 We did not intend
3:58 Outro: the plaque, and the credits
4:33 The reinstatement, and what happened
6:32 Who has a stake
7:28 Where it stands

WHAT HAPPENED (as of Nov 24, 2026)
• Nov 12: Nvidia announced its co-founder had resigned as CEO, effective immediately (its 8-K: the board accepted it Nov 11), after reports he had been the target of a foreign intelligence effort, amid company, FBI and congressional inquiries. Investigations, not findings.
• The shares fell as much as 14.3% on Nov 12, recovering much by the close; fell 14% on Nov 20, after Reuters reported the SEC was exploring accounting issues at Nvidia; and rose more than 31% on Nov 23.
• Nov 17: the board created a National Security and Export Control Oversight Committee and said it did not intend to reinstate him; he said he'd be "honored" to return. Nvidia reported Q3 revenue of $115.8bn, up 103%, for a quarter that ended Oct 25.
• Nov 23: the board unanimously reinstated him, citing input from senior levels of the U.S. government it didn't name. Its investigation continues. President Trump told CNBC his intervention was "very important."
• House interviews: Dec 1 (him) and Dec 2 (Nvidia's general counsel).
• The diner shown is generic, not the real one, whose plaque came down Nov 12 and went back within two days. "The Company" is fictional.

SOURCES
Nvidia, Nov 12: https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition
Nvidia, Nov 23: https://nvidianews.nvidia.com/news/nvidia-board-reinstates-jensen-huang-as-president-ceo-and-board-director
Nvidia Q3 FY2027 results: https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx
CNBC, Nov 20: https://www.cnbc.com/2026/11/20/nvidias-7-week-losing-streak-is-longest-since-2008-financial-crisis.html
AP, Nov 23: https://www.bostonglobe.com/2026/11/23/business/nvidia-reinstates-jensen-huang/
NBC News: https://www.nbcnews.com/politics/trump-administration/trump-nvidia-board-reinstates-jensen-huang-rcna610882
Axios: https://axios.com/2026/11/17/nvidia-jensen-huang-congress-testify-dates
Anthropic's IPO prospectus: https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm
Every claim on screen, with its sources: https://github.com/Derivative-Work/effective-immediately/blob/main/docs/sources.md

CREDITS
Words: Claude, the plan audited by ChatGPT and Gemini
Music: Suno v6, edited by a human, post-filtered with music-deslop (M6f 10k); credits music: a Suno v6 instrumental cover
Stills and clips: FLUX.2 [dev] and LTX-2.3 in ComfyUI · Boardroom: Blender
Edit: Claude Code with Opus 5.5 (Remotion)
Market data provided by Databento
Type: Inter, Jost, Courier Prime, VT323, Shrikhand, Liberation Mono (SIL OFL)

Video and assets: CC BY-NC-SA 4.0 · Code: MIT
Satire. Not affiliated with or endorsed by Nvidia or any company named here. Not investment advice.

#AIgenerated #musicvideo #satire
```

The description is under YouTube's 5,000 characters (checked by length). If an edit pushes it over, shorten WHAT HAPPENED
first; every line of it is on the fact card and in `docs/sources.md`.

### Tags

Paste as one comma-separated line:

```
Effective Immediately, Nvidia, Nvidia CEO, Jensen Huang, Nvidia board, CEO reinstated, AI music video, AI generated, AI satire, disco, boogie funk, breakup song, Suno, Claude, Claude Code, FLUX.2, LTX-2.3, Blender, Remotion, Derivative Work
```

### Settings

| Setting | Value |
|---|---|
| Category | Music |
| Audience | Not made for kids |
| Altered or synthetic content | **Yes.** The singing voice is AI-generated, and the scenes are generated or rendered. The terminal in the opening prints "AI-generated satire" in the first 10 seconds. |
| Language / caption language | English / English |
| Captions | Upload `deliverables/effective_immediately.en.srt` as English subtitles (69 cues, the lyrics as sung). The burned-in subtitles carry the same words. |
| License | Standard YouTube License. YouTube's only Creative Commons option is CC BY, which would drop the NC-SA terms; the description states the licence instead. |
| Thumbnail | Option A (below), 1280×720. |
| Chapters | From the description (first at 0:00, each 10 s or longer). |
| End screen | Over the final card, from 7:35 to the end (8 s). Starting earlier would cover the disclosure or the dated cards. |
| Comments | Open. |
| Visibility | Unlisted for a check pass, then public. |

### Thumbnail options

Rendered from `remotion/src/Thumbnail.tsx` (`npx remotion still remotion/src/index.ts Thumb-A …`), 1280×720, in
`deliverables/thumbnails/`. None shows Nvidia's name, logo, green or a face (brief).

| Option | Picture | Text | Notes |
| --- | --- | --- | --- |
| **A (recommended)** | Split: the empty hook (cold) and the jacket back in the diner booth (warm) | NOV 12 · NOV 23 · EFFECTIVE IMMEDIATELY (until further notice) | The whole joke in one frame; reads at phone size. |
| B | The empty hook alone | OUT. EFFECTIVE IMMEDIATELY. · BACK IN 11 DAYS | Starkest; the brief's "empty jacket" idea. |
| C | The empty counselor's chair, the company in silhouette | WE DID NOT INTEND… (TO TAKE HIM BACK) | The brief's other idea; the lyric as the hook. |

### Shorts

The brief asks for a vertical cut of chorus 1 (E08 to E11) with the "Effective immediately" lower third as its title.
It isn't made yet; it can follow the main upload.
