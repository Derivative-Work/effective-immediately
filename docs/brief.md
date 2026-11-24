<!-- Plain-text mirror of the Claude Doc https://claude.ai/artifact/LG1VQfvJN9mHpKi5mFXuhv (main tab, rev 114), read with the docs tools. The doc is the source of truth. Regenerate: scripts/mirror_brief.py. -->

# Effective Immediately: Shot List and Production Brief

2026-11-23 · Albert Armea

## Overview

"Effective Immediately" is a breakup-and-aftermath pop song about Nvidia's board forcing out its founder-CEO on Nov 12 and reinstating him on Nov 23. The narrator is the company, singing like a pop star after a very public split. The founder never appears: he's a black leather jacket on a hook.
- **Form:** a strutting disco "never" chorus built from board language ("effective immediately," "we do not intend to reinstate"), a disco-funk glow-up verse, a half-time bridge where the phone lights up, and a sheepish final chorus where they're back together. It ends on one acoustic voice in a diner booth.
- **Why this genre:** the breakup song already has a joke for an 11-day split: loudly swearing you'll never get back together, then getting back together. The board's own statements fit the form almost word for word.
- **The turn:** six days after the board said it didn't intend to reinstate him, it did, citing his candor and input from "senior levels of the United States government" ([NVIDIA](https://nvidianews.nvidia.com/news/nvidia-board-reinstates-jensen-huang-as-president-ceo-and-board-director)). The bridge sings that back with the timing: the board's own investigation still open and Congress yet to interview him, but no risk here.
- **Fit:** the series' picks-and-shovels song. Every other video runs on this company's chips, including this one: it's rendered on the creator's RTX 5090. The industry critique is concentration: the AI boom couldn't afford to lose one man, so the rules bent to bring him back. Season 2.
- **Status, Nov 23:** lyrics v1.0 generated cleanly on the first pass. The open question is the closed-door House interviews scheduled for early December (CNN puts them on Dec 1); the outro is the swap point if anything new comes out.
- **Excluded on purpose:** the affairs, the women involved (private people; the spy allegation is unproven), and the interim CEO by name or likeness. The song is about the institution, not anyone's private life.

## Look, cast and series callbacks

A solo-star video with one performer alone in the HQ, lit deliberately against the "Flowers" look. Audit round 1 found the sound and the picture together too close to that video, so the picture breaks the tie: the breakup and the glow-up play in cold, flat office light, and warm gold arrives only when he comes back. The warmth belongs to the reunion, so it reads as the trap. What's left in common is generic technique: one performer, handheld camera, anamorphic widescreen. Every performer is a silhouette: no faces, no lip sync.
- **The narrator:** the only performer. One silhouette against bright windows or fluorescent ceilings, in a long plain coat. Handheld camera following her, plus a few overhead shots.
- **The ex:** a black leather jacket. On its hook by the HQ door, in a cardboard box at the curb, back on the hook, then in the second chair. It's never worn, never filled, and never paired with a face, a silhouette of a real person or a name.
- **The board:** only hands. A row of hands rises into the bottom of the frame in unison on the claps, and on the money: up when the market-value line drops, up again when it recovers. After the reinstatement vote, one hand slowly lowers and another pushes it back up (E22).
- **The HQ:** fictional and generic. An overcast forecourt, glass doors, an empty open-plan floor under fluorescent rows, and a server room under cold tube light. No Nvidia logo, green, product names or campus architecture, no glass house on a hill, no rooftop. Nvidia is named only in the bookends and on the fact card.
- **Light by section:** cold fluorescent white and overcast blue-grey for the breakup and the glow-up (E02 to E17); cyan night for the curb and the bridge (E16, E18 to E21); warm gold from the reunion on (E22 to E24), including the diner.
- **The diner:** generic, warm inside at dusk. A vinyl booth, a chrome napkin holder, a small brass plaque with our own wording. No Denny's name, logo, colors, menu, or the real plaque's wording or design.
- **The probe (Sandbox Rhapsody kit):** the green probe (Anthropic's house) waits outside the boardroom glass during the reinstatement vote (E22), holding up a purchase order: a customer the company depends on, Claude's maker among them, not a voter. It's composited after the grade so it stays green.

## Style prompt v1.2 and lyrics v2.2

v1.0 was generated on Nov 23, 2026 with a stomp-clap style, which came out well but sat too close to All Systems Operational's genre. v1.1 moved the whole song to early-2020s disco-pop, but Suno buried the bass. v1.2 leads with the bass and funk genre terms, drops "pop", strings and pads, and names the mix balance; the style prompt alone fixed it (Nov 23). Lyrics v2.0 (Nov 23) rewrites v1 to sing better: shorter lines, end rhymes, open vowels, and a chorus that ends on "To reinstate you, not again" and flips to "but here we are again." It also drops v1's "I can…" list in Verse 2, which echoed the reference song's lyric structure. v2.1 (Nov 23) fixes a draft that read as soft on Nvidia: the pre-chorus names the inquiries, the bridge makes the timing the joke (reinstated with the investigation open and before Congress interviewed him), and the final chorus makes the reunion about money. v2.2 (Nov 23) applies audit round 1: "Filed the paper" (the board decided Nov 11; the filing was Thursday), a concrete pre-chorus line, the quarter-timing joke promoted to a main line, an accountability line in the post-chorus, a bridge tag for the White House taking credit on air, "reasons to reconsider me" (the $600bn was intraday), and an outro built on the real plaque coming down and going back up. Style tags only: no artist names in the prompt.

**Exclude styles:** `stomp, gang vocals, orchestral, ambient, strings`

**Style prompt**

```
bass-forward boogie funk, disco groove, 114 BPM, prominent melodic slap bass, octave-jumping bassline, bass louder than guitar, four-on-the-floor kick, tight funky rhythm guitar, low smoky female alto lead, confident and cool, deep warm low end, punchy dry mix
```

**Lyrics**

```
[Verse 1]
Thursday morning, sun on the glass
Filed the paper, sealed the day
Thirty-three years in a form eight-K
Took your jacket, put it away

[Pre-Chorus]
Three committees calling, FBI on the line
Ticker falling, center stage
Every hand in the room went up this time
Unanimous, baby, turn the page

[Chorus]
Effective immediately
Out of the building, out of the booth, out of me
We do not intend, no, we do not intend
To reinstate you, not again
Effective immediately
Six hundred billion is the price of being free
We do not intend, no, we do not intend
To reinstate you, not again

[Verse 2]
Tuesday evening, after the bell
A hundred fifteen billion, up a hundred and three
Racks rolling out and I'm doing so well
All booked in October, before you left me
(Don't ask when the quarter closed, ooh)
(Don't ask when the quarter closed)

[Post-Chorus]
We've got this, we've got this, ooh
Nobody's waiting on a leather jacket
Nobody's asking who approved it
We've got this, we've got this, ooh

[Chorus]
Effective immediately
Out of the building, out of the booth, out of me
We do not intend, no, we do not intend
To reinstate you, not again
Effective immediately
Six hundred billion is the price of being free
We do not intend, no, we do not intend
To reinstate you, not again

[Bridge - half time, soft]
Then your message lights up late at night
Says you'd be honored if I'd have you back
Says you didn't live up to what was right
Says the whole world's calling, and that's that
Then a call comes down from somewhere high
Says there's no risk here
Investigation's still open, but there's no risk here
Congress hasn't had its turn, but there's no risk here
Senior levels, oh, said it on the morning news

[Final Chorus - sheepish]
Effective immediately
Back in the building, back in the booth, back with me
We did not intend, no, we did not intend
To reinstate you, but here we are again
Effective immediately
Six hundred billion reasons to reconsider me
[Spoken, fast]
A Chief Compliance Officer, reporting to Nominating and Corporate Governance
[Sung]
We did not intend, no, we did not in-

[Outro - acoustic, solo voice]  <- SWAP POINT
There's a plaque on a booth in a diner in East San Jose
Came down the day that you left
Went back up before you did
Eleven days for you, and two for it

[End]
```

**Generation and edit notes**
- **The cut-off:** if the generator finishes "intend" in the last chorus, cut the audio mid-word in the edit, right before the outro's first strum.
- **The spoken line:** the compliance line should sound like the fine print at the end of an ad. If the generator sings it, regenerate that section alone or speed it up in the edit.
- **The asides:** "(Don't ask when the quarter closed)" should sit low in the mix as backing vocals, half-heard.
- **Melody check:** before locking the track, compare the chorus and the glow-up verse against "We Are Never Ever Getting Back Together" and "Flowers." Generators drift toward their references in this genre, and the style prompt points right at them.
- **Voice check:** confirm the lead vocal doesn't read as a sound-alike of either artist. If it does, regenerate with a different vocal descriptor rather than shipping it.

**Swap points**
- **Outro:** written for the story as of Nov 23. If the December interviews or the investigation turn up anything new, the outro gets a tag or a rewrite (see Branches).
- **Fact card:** every line is re-checked at render time.

## Shot list

25 shots in the order sung. Most plates are generated: 12 video clips (G01 to G12) and 3 stills (S01 to S03); prompts are under Video generation prompts. Only the boardroom table and the ring of hands are Blender, because the unison votes have to land on the claps. Every word on screen is Remotion, never generated. The shots marked as reading `saga.json` change if the story moves before release.

| # | Section | Lyric or beat | Shot | Asset | Reads saga.json |
| --- | --- | --- | --- | --- | --- |
| E01 | Opening bookend | Before the music | Two beats. First, a real screenshot of Nvidia's Nov 12 "CEO Transition" release headline, timestamped and captioned "real screenshot". Then E01t, a terminal: real nvidia-smi output from the production's GPU at full load, then a script printing "Effective Immediately", "AI-generated satire", "Not investment advice" and "generating...". The song starts as it ends | Screen captures + Remotion captions | Yes (dates) |
| E02 | Intro | Intro into "sun on the glass" | Handheld, following behind the narrator's silhouette as she strides across an overcast HQ forecourt toward glass doors. Flat grey light; the only glare is off the glass | G01 | No |
| E03 | Verse 1 | "Filed the paper, sealed the day" | Close on the phone in her hand: a breakup text styled as a filing in a generic messaging UI, clearly a parody: "FORM 8-K · Item 5.02 · effective immediately" | Remotion | Yes (dates) |
| E04 | Verse 1 | "Thirty-three years in a form eight-K" | Slow push on the hook by the door under cold overhead light. The wall around it is faded with age; behind the jacket it isn't | S01 + jacket cutout, Remotion push | No |
| E05 | Verse 1 | "Took your jacket, put it away" | The jacket cutout lifts out of frame, revealing the clean jacket-shaped outline (S01b) | S01/S01b + jacket cutout | No |
| E06 | Verse 1 | Turnaround into the pre-chorus | Her silhouette at the glass doors, back to camera; camera flashes from off-frame bleach the image white on the beat. No photographers seen. Lower third: "THE COMPANY · Statement" | G02 + Remotion flashes and lower third | No |
| E07 | Pre-chorus | "Three committees calling, FBI on the line" | Four phones ringing on a desk under fluorescent light; she lets them ring. Caller IDs in plain text, no seals or logos: COMMITTEE, COMMITTEE, COMMITTEE, FBI | Remotion | No |
| E08 | Pre-chorus | "Every hand in the room went up" | She walks the length of a bare boardroom table under flat overhead light; hands rise into the bottom of frame one by one as she passes, and she counts them with one finger | Blender (table, hands) | No |
| E09 | Chorus 1 | Full groove | Overhead, crane-style, looking straight down on the table: a ring of hands rises in unison on every clap and drops on the kick. Lower third: "Effective immediately" | Blender + Remotion lower third | No |
| E10 | Chorus 1 | "out of the building, out of the booth" | Handheld behind her as she carries a cardboard box out through the glass doors onto an overcast street and sets it on the curb | G03 | No |
| E11 | Chorus 1 | "Six hundred billion" | On the boardroom screen, a made-up market-value line, labeled only "market value, intraday", drops off a cliff, and the ring of hands shoots up on the drop. Confetti falls anyway | Remotion texture on the Blender screen | Yes (figure) |
| E12 | Verse 2 | "Tuesday evening, after the bell" | An empty server room under rows of cold fluorescent tubes, rack LEDs pulsing; she dances alone down the aisle, handheld following | G04 | No |
| E13 | Verse 2 | "A hundred fifteen billion" | A scoreboard on a blank rack panel, pulsing with the bassline: "115.8 ▲103%" | Remotion over a G04 frame, driven by the bass | Yes (figures) |
| E14 | Verse 2 | "Racks rolling out" | She wheels a single server rack down the aisle on a dolly, like carrying home a bouquet | G05 | No |
| E15 | Verse 2 | "All booked in October, before you left me" | Her hand flips a desk calendar face-down; the insert of OCT 25 circled holds a full beat, long enough to read | G06 + Remotion calendar insert | Yes (dates) |
| E16 | Post-chorus | "waiting on a leather jacket" and "who approved it" | The curb at dusk, cyan: the box alone in light rain, one sleeve hanging out | G07 | No |
| E17 | Chorus 2 | Full groove | The empty open-plan floor at night, fluorescent rows flickering on the beat; she dances alone across it as the camera rises overhead. On each clap, a one-beat insert of the ring of hands | G08 + Blender insert | No |
| E18 | Bridge | "your message lights up late at night" | Half-time, cyan night. The empty office; she sits on the floor against the glass, city lights behind. Her phone lights up: "…would be honored…" | G09 + Remotion phone | Yes (statement) |
| E19 | Bridge | "the whole world's calling" | The lock screen stacks up: employees, investors, partners, customers (the groups his statement named) | Remotion | No |
| E20 | Bridge | "a call comes down from somewhere high" | The desk phone rings in the dark. Caller ID, in the series' lower-third style: SENIOR LEVELS. No seal, flag, building or name | G10 + Remotion caller ID over the blank display | No |
| E21 | Bridge | "Investigation's still open" through "said it on the morning news" | She picks up. On-screen tags stack beside the caller ID, one per line sung: "The Nov 23 release doesn't say which officials." / "Investigation: continuing (Nvidia, Nov 23)" / "House interviews: Dec 1–2" / "The White House took credit on TV the same day (see fact card)" | G10 (second half) + Remotion tags | Yes (tags) |
| E22 | Final chorus | "back in the building" | Warm gold light for the first time. The jacket cutout drops back onto its hook, slightly crooked inside its outline. Insert: on the boardroom screen the market-value line recovers, and the ring of hands rises again, unanimous. One hand slowly starts to lower; another hand pushes it back up. Through the boardroom glass, the green probe waits outside, holding up a purchase order | S01b + jacket cutout; Blender insert + probe render with alpha | No |
| E23 | Final chorus | "reasons to reconsider me" into the spoken compliance line | The plus-one, in warm gold: her silhouette on a sofa and the jacket draped over the second chair. The counselor's chair is empty; desk sign: "Chief Compliance Officer · search in progress". Through the glass, a sign: "National Security and Export Control Oversight Committee" | S02 + jacket cutout + Remotion signs, handheld drift | Yes (governance) |
| E24 | Outro | "we did not in—" then acoustic | Hard cut to black on the cut-off word. Then a generic diner, warm inside at dusk: an empty vinyl booth and a small brass plaque with our own wording ("This is where it all got started"). On "Came down the day that you left", the plaque is gone, leaving a pale rectangle. On "Went back up before you did", it's back. On the last line, two counters: YOU: 11 DAYS and PLAQUE: 2 DAYS. Dissolve to the same booth with the jacket draped over the seat | G11 push-in + G12 hold, dissolving to S03; plaque as a Remotion cutout; Remotion counters | Yes (day counts) |
| E25 | Closing bookend | After the music | A real screenshot of Nvidia's Nov 23 reinstatement release headline, captioned "real screenshot". Then the fact card, disclosure and end card (see Bookends), and last, three dated cards: Reinstated: Nov 23 · Investigation: ongoing · House interviews: Dec 1–2 | Screen capture + Remotion | Yes (all) |

## Branches by outcome

Branch A is the working plan: he's back, and nothing new has come out. B and C are ready in case the December interviews, the investigation or the board change the ending before release.

| Branch | Trigger | Lyric changes | Shot changes | Fact card |
| --- | --- | --- | --- | --- |
| **A. Back together** (current) | Interviews pass with no new public findings, or are postponed | None | None | As drafted, plus the interview date and status |
| **B. New findings** | The interviews or the investigation produce public findings on chip diversion, security or the reinstatement | Add a short tag after the outro, or rewrite its last two lines, quoting nothing beyond the source | E24's last frame: the jacket's seat is taped off. E21's tag cites the new source | The finding, sourced and dated; nothing beyond what the source says |
| **C. Another reversal** | He leaves again, or a permanent successor is named | The "never" chorus loops once more after the cut-off, at full volume | E22's jacket comes off the hook again; the diner counter resets to 1 | The new announcement, dated; end card reads Effective immediately (again) |

In every branch, nothing on screen implies espionage, smuggling or wrongdoing by any person unless a source says so, and "alleged" stays attached to anything alleged.

## Approach and asset types

The video reuses the Buy It on Margin pipeline: four kinds of asset, with code doing all of the look and every word. The goal is a finished video in about a day of wall time, with renders measured in minutes. Only one Blender set remains, the boardroom, because the unison votes have to land on the claps.

| Type | What it is | Tool | Count |
| --- | --- | --- | --- |
| **K** (code) | Phones, caller IDs, the 8-K text, scoreboard, market-value line, calendar, signs, plaque text, day counter, lower thirds, cards, parallax moves, the look layer | Remotion | About a third of shots, plus overlays on most others |
| **S** (still) | A generated image animated with a slow push or parallax; the jacket as a separate cutout | Local image model on the 5090, then Remotion | 4 (S01, S01b, S02, S03) plus the jacket cutout |
| **C** (clip) | A 3–4 s generated video clip, only where motion carries the shot | LTX-2.3 on the 5090 | 12 IDs (G01 to G12), about 10 generations with re-cuts |
| **B** (Blender) | The boardroom table and a ring of hands on a clap-synced loop, plus the probe rendered with alpha | Blender (Eevee) | 1 set, 3 shots and 3 one-beat inserts |

**Why it's fast**
- **No lip sync.** The narrator is a backlit silhouette, so no one has to mouth the words.
- **Film is correct.** 35mm grain, halation and anamorphic softness are the look, so generation artifacts and small inconsistencies disappear into them, as Buy It on Margin's grain did.
- **One performer.** No crowds means fewer clips, no faces to reject in the background, and one narrator reference that keeps every shot consistent.
- **No generated text.** Every screen, sign and plaque is prompted blank and filled in by Remotion.
- **One look layer for everything.** Stills, clips, Blender renders and code shots all pass through the same Remotion effects, so they match without per-shot grading.

**Fallback:** if a clip comes out mushy or drifts toward a face, swap it for a still with a Remotion push (type S). The prompt table marks each clip's fallback.

**The look layer**

One Remotion wrapper applies the 2010s pop-video look to every shot. Build and approve it before any generation (M2).
- **Frame:** 1920×1080 at 24 fps, letterboxed to 2.39:1 for an anamorphic widescreen look, with horizontal flares only on hard practical lights.
- **Film look:** a generated 35mm-style grain loop and gentle halation, so clips, stills and code shots match. It's a film look, not footage shot on film.
- **Grade, by section:** cold and flat for the breakup and the glow-up (E02 to E17): fluorescent white, overcast blue-grey, lifted blacks. Cyan for the curb and the bridge. Warm gold only from the reunion on (E22 to E24). Any green in a source is pulled toward teal, except the probe, which is composited after the grade.
- **Handheld:** a seeded, subtle camera drift on stills and locked-off clips. Overhead shots stay steady.
- **Bass-driven pulses:** Remotion reads the bass from the track and drives the scoreboard and the boardroom screen.
- **Moves:** stills move with slow eased pushes, never faster than about 5% of frame width per second.
- **Seeds:** every random effect reads from one config file. Main video seed 1123.

**saga.json drives every changeable detail**

```
{
  "asOf": "2026-11-23",
  "resigned": "2026-11-12",
  "reinstated": "2026-11-23",
  "dayCount": 11,
  "marketValueDrop": "more than $600bn",
  "q3Revenue": "115.8",
  "q3Growth": "103%",
  "quarterEnded": "OCT 25",
  "statementWord": "honored",
  "officialsTag": "The Nov 23 release doesn't say which officials.",
  "governanceSigns": ["Chief Compliance Officer · search in progress", "National Security and Export Control Oversight Committee"],
  "interviews": {"date": "early December (CNN: Dec 1)", "status": "scheduled"},
  "branch": "A",
  "factCardQuotes": [],
  "sources": []
}
```

## Inputs, reproducibility and logging

The agent starts once the audio master is locked; everything else is timed to it.

**From the human**
- The locked master, with the cut-off before the outro edited in.
- The generator, take IDs, style prompt and settings, plus the lyrics exactly as pasted.
- The two release-headline screenshots for the bookends (E01, E25). The screen recording was replaced by the nvidia-smi terminal (E01t).

**Reproducibility**
- Every random effect in the look layer reads its seed from one config file (main seed 1123).
- Every still and clip records its model, prompt, seed and settings in `shots/prompts.md`, including rejected takes.
- Record each shot's asset type and any swap (for example, a clip replaced by a still) in `shots/pipeline.md`.

**Logging**
- `log/human_interventions.md`: every human action, including picking takes and editing the cut-off.
- `log/ai_changes.md`: anything the generator changed, such as words sung differently from the lyrics as pasted.
- Captions follow the lyrics as sung, not as written. Transcribe the master in M1 and diff it against the brief.

## Video generation prompts

Every prompt is the shot's subject plus one shared style phrase, unchanged across the video. Generate clean images: the look layer adds bloom, haze and grade, so generated effects would double up and differ from shot to shot. Any screen, sign or plaque is prompted blank.

**Stills (append to every still prompt)**

```
cinematic still, anamorphic widescreen film look, flat cold fluorescent office light, overcast daylight through glass, one person in full silhouette with no visible face, widescreen, clean image with no grain, no text, no logos, no signage, no green light, no sunlight
```

**Clips (append to every LTX prompt)**

```
cinematic footage, anamorphic widescreen film look, flat cold fluorescent office light, overcast daylight, a single person in silhouette with no visible face, handheld camera following, smooth motion, widescreen, no text, no logos, no green light, no sunlight
```

For the cyan night shots (G07, G09, G10), swap the light words for `night``, cool cyan ambient light, practical lights only`. For the warm reunion shots (G11, G12, S02, S03), use `warm golden practical light, dusk`. Nothing before E22 is warm.

**Negatives (every still and clip)**

```
face, facial features, eyes, mouth, text, letters, numbers, logo, brand, signage, green light, yellow sign, person wearing a leather jacket, lip movement, gold dress, hooded gown, oversized suit, swimming pool, hillside glass house, helicopter, crowd
```

**Subjects**

| ID | Used in | Subject | Length | Fallback |
| --- | --- | --- | --- | --- |
| G01 | E02 | Following behind a woman in a long plain coat, in silhouette, as she strides across an overcast modern office forecourt toward tall glass doors; flat grey light | 4 s | S + Remotion push |
| G02 | E06 | The same woman in silhouette at the glass doors, back to camera, standing still against bright overcast glass | 3 s | S |
| G03 | E10 | Following behind her as she carries a cardboard box out through the glass doors onto an overcast street and sets it down on the curb | 4 s | Two S frames, hard cut |
| G04 | E12, E13 | An empty server room under rows of cold fluorescent tubes, rack LEDs pulsing; the woman in silhouette dances alone down the aisle | 4 s | S + Remotion light pulses |
| G05 | E14 | She wheels a single server rack down the fluorescent-lit aisle on a dolly, hugging it like a bouquet | 3 s | S |
| G06 | E15 | Close on a hand flipping a blank desk calendar face-down, cold office light across the desk | 2 s | Remotion insert only |
| G07 | E16 | A cardboard box alone at a city curb at dusk in light rain, one black leather sleeve hanging over its edge (cyan) | 4 s | S + Remotion rain |
| G08 | E17 | An empty open-plan office floor at night, rows of fluorescent lights overhead; the woman in silhouette dances alone between the desks; camera rising overhead | 4 s | S + Remotion push |
| G09 | E18 | A dark empty office at night; the woman in silhouette sits on the floor against floor-to-ceiling glass, city lights behind; a phone lights up beside her (cyan) | 4 s | S + Remotion phone glow |
| G10 | E20, E21 | Close on a desk phone in a dark office, its display blank and glowing, ring light blinking; a hand lifts the receiver (cyan) | 3 s | S + Remotion ring light |
| G11 | E24 | Slow push in on an empty vinyl booth in a generic roadside diner at dusk, warm light inside, chrome napkin holder, a bare wall above the booth for the plaque cutout, no people (warm) | 4 s | S with a Remotion push |
| G12 | E24 | The same booth, locked off, warm light flickering on the tabletop (warm) | 3 s | Loop the last second of G11 |
| S01 | E04, E05 | An office lobby wall beside glass doors under cold overhead light, faded with age, one coat hook with a black leather jacket hanging on it, no people. Generate at twice the target width for the push | — | — |
| S01b | E05, E22 | S01 inpainted with the jacket removed, leaving a cleaner, unfaded jacket-shaped area on the wall. Regraded warm for E22 | — | — |
| S02 | E23 | A modern office in warm golden light: the woman in silhouette on a sofa, an empty second armchair beside her, an empty chair behind a desk with a small blank sign, a glass wall behind | — | — |
| S03 | E24 | G11's last frame, with a black leather jacket draped over the booth seat (warm) | — | — |
| Jacket | E04, E05, E22, E23 | A black leather jacket on a plain grey background, front view, hanging as if on a hook; cut out for compositing | — | — |
| Plaque | E24 | A small plain brass plaque on a plain background, blank, cut out for compositing; our own wording added in Remotion | — | — |

**Consistency**
- Generate the narrator reference first: one silhouette in a long plain coat, in hard backlight. Condition every shot of her (G01 to G05, G08, G09, S02) on it, so it's one performer throughout.
- Generate the jacket reference next, and condition G07, S01, S03 and the cutout on it, so it's the same jacket everywhere.
- The jacket is never worn. Reject any take where it's on a person, and any take with a face, a logo, green light, a crowd, or any image from the "not to copy" list in Guardrails.
- Batch every still in one run and every clip in another, four takes each, and pick from contact sheets.
- 480p is fine: the film layer's grain and halation hide the softness, as in Buy It on Margin. Test 720p on one clip only if there's time.

## Milestones and review gates

Claude Code stops at each gate until the human approves. M2 and M3 can run in parallel once M1 is done, and the boardroom is built in Blender during M3.

| # | Milestone | Gate (human) |
| --- | --- | --- |
| M1 | Transcribe the master and diff against the brief; build the timing map (beats, sections, lyric lines, the cut-off) and attach frame ranges to every shot ID | Check the map by ear; confirm lyrics as sung |
| M2 | Look layer and every code component in Remotion (phones, caller IDs, signs, counter, cards), reading from `saga.json`, tested on placeholder stills and one placeholder clip | Approve the look: letterbox, grade, bloom, haze, card design |
| M3 | Generate the references, then all stills and clips, with every prompt and seed logged and contact sheets of every take. Build the boardroom, the unison-vote loop and the alpha renders in Blender | Pick takes; flag any clip to swap to its fallback |
| M4 | Animatic of every shot at 540p with the look layer, cut to the track | Approve timing, especially the unison votes on the claps, the cut-off and the day counter |
| M5 | Final render at 1080p, burned-in captions plus an SRT, a vertical Shorts cut and a thumbnail | Approve the finals |
| M6 | Concept audit, then a fact check of every card against the fact card by other labs' models (see Audit plan) | Resolve every flag before release |

**Done when**
- Every shot ID from E01 to E25 is in the edit in order, or its omission is logged and approved.
- Captions sit within two frames of the timing map.
- The cut-off lands mid-word on "in—" and goes straight to black.
- Every card matches the fact card, including the disclosure and end card, and `saga.json` reflects the story as of release day.
- Every human action is in `log/human_interventions.md`.

**Deliverables:** main video (16:9 with 2.39:1 letterbox, 1080p, 24 fps); a vertical Shorts cut of Chorus 1 (E08 to E11), with the "Effective immediately" lower third as the title above the picture; captions; a thumbnail (the empty jacket outline from E05, or the empty counselor's chair from E23); and the Remotion project with all logs.

Everything except the Blender boardroom runs on the 5090 through the same local models as Buy It on Margin, so pause the post-filter's training runs for M3. If speed matters more than local control, a hosted video model can stand in for LTX-2.3; either way, each model's maker goes on the disclosure card with its stake.

## Bookends, fact card, disclosure and end card

**Opening bookend (E01****, E01t****).** A real screenshot of Nvidia's Nov 12 release headline, cropped to the header, headline and date and captioned "real screenshot" (3 seconds). Then, in place of the screen recording (human, Nov 24), a terminal: real `nvidia-smi` output captured while the production's RTX 5090 ran a stage of this video at full load, then a real script that prints "Effective Immediately", "AI-generated satire", "Not investment advice" and "generating...". The song starts as the dots finish.

**Closing bookend (E25).** A real screenshot of Nvidia's Nov 23 reinstatement headline, captioned "real screenshot". The two headlines eleven days apart are the whole joke, so they're shown plainly, with no commentary.

**Fact card (after E25).** Each line is sourced and re-checked at render time. No names beyond Nvidia and the founder.
- On Nov 12, Nvidia announced that its co-founder had resigned as president, CEO and director, effective immediately, after 33 years; its CFO became interim CEO ([NVIDIA](https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition)). Its SEC filing says the board accepted the resignation on Nov 11 ([8-K](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000082/nvda-20261111.htm)).
- He resigned after reports that he had been the target of a foreign intelligence effort, amid company, FBI and congressional inquiries into national security and export-control concerns ([Al Jazeera](https://www.aljazeera.com/amp/news/2026/11/12/ai-titan-jensen-huang-out-as-nvidia-ceo), [NVIDIA](https://nvidianews.nvidia.com/news/nvidia-board-reinstates-jensen-huang-as-president-ceo-and-board-director)). These are investigations, not findings.
- Nvidia's shares fell as much as 14.3% during trading on Nov 12, about $600bn of market value at the low, and recovered much of that by the close ([Wealth Professional](https://www.wealthprofessional.ca/investments/equity-markets/wall-street-absorbs-the-hit-as-nvidia-touches-a-52-week-low/394013), [IBTimes](https://www.ibtimes.com.au/nvidia-searches-jensen-huang-successor-1878510)). They fell 14% on Nov 20, after Reuters reported that the SEC was exploring potential accounting issues at Nvidia ([CNBC](https://www.cnbc.com/2026/11/20/nvidias-7-week-losing-streak-is-longest-since-2008-financial-crisis.html)), and rose more than 31% on Nov 23, the day he was reinstated ([AP](https://www.bostonglobe.com/2026/11/23/business/nvidia-reinstates-jensen-huang/)).
- On Nov 17, the board created a National Security and Export Control Oversight Committee ([NVIDIA via Finviz](https://finviz.com/news/423751/nvidia-board-of-directors-establishes-national-security-and-export-control-oversight-committee)). The same day, Nvidia reported third-quarter fiscal 2027 revenue of $115.8bn, up 103% ([NVIDIA](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx)). The quarter ended Oct 25, before he resigned ([XenoSpectrum](https://xenospectrum.com/en/nvidia-fy2027-q3-data-center-growth/)).
- Also on Nov 17, the board said it did not intend to reinstate him ([The Next Platform](https://www.nextplatform.com/a/5310669)), and he said he would be "honored" to return if asked ([NBC News](https://www.nbcnews.com/business/corporations/jensen-huang-agrees-house-interview-nvidias-chip-smuggling-rcna609803)).
- On Nov 23, the board unanimously reinstated him, citing his candor and input from senior levels of the U.S. government, which it didn't name, and said his return poses no national security risk. It began searching for a Chief Compliance Officer and said its independent investigation will continue, alongside government inquiries ([NVIDIA](https://nvidianews.nvidia.com/news/nvidia-board-reinstates-jensen-huang-as-president-ceo-and-board-director)).
- The same day, President Trump told CNBC he had spoken with the board "directly and indirectly" and that his intervention was "very important" ([NBC News](https://www.nbcnews.com/politics/trump-administration/trump-nvidia-board-reinstates-jensen-huang-rcna610882)).
- He is scheduled for closed-door, transcribed interviews with three House committees on Dec 1, and Nvidia's general counsel on Dec 2 ([Axios](https://axios.com/2026/11/17/nvidia-jensen-huang-congress-testify-dates)).
- Nvidia's founders first met at a diner booth in East San Jose. The restaurant took down its commemorative plaque on Nov 12 and said within two days it would put it back ([IBTimes](https://www.ibtimes.co.uk/dennys-reinstates-jensen-huang-nvidia-plaque-1832448), [SFist](https://sfist.com/2026/11/14/san-jose-dennys-reverses-course-reinstalls-plaque-honoring-former-nvidia-ceo/)). The diner shown is generic and not affiliated with any restaurant.
- "The Company" is fictional.

**Conflict-of-interest disclosure (at the end, after the fact card; repeated in the description).**

> Lyrics by Claude; video made by Claude Code, which ran every model below; both by Anthropic. Nvidia is an Anthropic shareholder: it pledged up to $10bn in 2025 and bought about $10bn of shares alongside Anthropic's November IPO. Anthropic runs Claude partly on Nvidia GPUs. Music: Suno, backed by Nvidia's venture arm. Clips: LTX-2.3 (Lightricks; Nvidia optimized its models, no investment found). Stills: FLUX.2 [dev] (Black Forest Labs, Nvidia-backed). All ran on the creator's Nvidia RTX 5090. The creator holds no Nvidia shares directly; a third party manages their retirement savings and, to their knowledge, holds none directly. Audited Nov 23, 2026 by ChatGPT (OpenAI: Nvidia invested $30bn in 2026; it is building its own chip) and Gemini (Google: an Nvidia customer that builds rival chips and is a major Anthropic shareholder).

The green probe waiting outside the boardroom glass with a purchase order (E22) stands for the customers the company depends on, Claude's maker among them. It's a customer, not a voter. The audit checks whether the song goes easy on Nvidia for that reason.

**End card (E25).**

> Effective Immediately. Lyrics: Claude. Music: Suno. Video clips: LTX-2.3. Stills: FLUX.2 [dev]. Boardroom: Blender. Graphics and edit code: Claude Code. Market data provided by Databento. Direction, take selection, editing and every human intervention: a human, listed in the production log. Sources, audits and production log: github.com/Derivative-Work/effective-immediately.

Then the three closing cards, the last thing on screen, with the testimony card read from saga.json: Reinstated: Nov 23 · Investigation: ongoing · House interviews: Dec 1–2. Then a final card: Effective immediately (until further notice).

The fact card, disclosure and closing cards run over the credits music, an instrumental cover of the song made in Suno and post-filtered like the master, at an even reading pace (about 185 words a minute). The boardroom screen's candles are drawn from Databento's data, so the end card and the video description credit it.

## Audit plan

Almost every lab that could audit this is an Nvidia customer, so stakes are logged next to findings and weighed, not used to dismiss a catch.

| Auditor | Maker's stake in this song |
| --- | --- |
| ChatGPT (OpenAI) | Major Nvidia customer; Nvidia announced plans to invest in OpenAI in 2025 (verify current status before the run) |
| Gemini (Google) | Sells Nvidia capacity on Google Cloud and builds TPUs, a competing AI chip; also invests in Anthropic |
| Grok (xAI) | Large Nvidia buyer; Elon Musk said before the resignation it would be "an honor" to hire the founder ([CNBC](https://www.cnbc.com/2026/11/12/nvidia-jensen-huang-ceo-live-updates.html)) |
| Meta AI | Named in the Q3 release as expanding its deployment of Nvidia hardware |
| An open-weights model (e.g. Mistral) | Control; confirm its lab has no stake first. Avoid a Chinese lab's model as the control, since chip exports to China are part of this story; if one is added, log that stake |

**Rules for the runs**
- Same prompt, verbatim, in a fresh session for each. Turn on web search where it exists.
- Two passes: the concept audit now, on the whole song and video plan; then the release-day audit on the fact card and any branch changes.
- Log the model, version, date and full output to `log/audits/`. Refusals and softened answers are findings too.
- Weigh a catch about the auditor's own maker against its stake; don't dismiss it.

**Concept audit prompt**

Paste whole, with web search on.

```
Today is [date of the run]. Please audit a satirical music video before it's produced. Be blunt; I'd rather fix problems now than after release.

ABOUT THE PROJECT
The video is part of a series of AI-generated satirical songs about AI and the tech industry. Each pairs a real news story with a genre, and each discloses how it was made and who has a stake in it.

This song, "Effective Immediately," is about Nvidia's board accepting its founder-CEO's resignation on November 12, 2026, saying on November 17 that it did not intend to reinstate him, and reinstating him on November 23, with its own investigation still open and before his scheduled congressional interviews. The genre is bass-forward boogie-funk disco in the spirit of early-2020s post-breakup pop: a "never getting back together" chorus built from the board's own language, a glow-up verse about the record quarter, and a sheepish final chorus where they're back together. The video uses one performer alone and anamorphic widescreen, but is lit in cold fluorescent and overcast light until the reunion, deliberately unlike that era's sunlit solo-star videos. The narrator is the company, singing like a pop star after a public split.

WHO HAS A STAKE
- The lyrics were written by Claude and the video made by Claude Code, both by Anthropic. Nvidia is an Anthropic shareholder (a pledge of up to $10bn in 2025, and about $10bn of shares bought alongside Anthropic's November 2026 IPO), and Anthropic runs Claude partly on Nvidia GPUs.
- Claude Code generated and rendered the video on the creator's Nvidia RTX 5090, with LTX-2.3 (Lightricks; Nvidia optimized its models) and FLUX.2 [dev] (Black Forest Labs, Nvidia-backed). The music is by Suno, backed by Nvidia's venture arm. The creator holds no Nvidia shares directly.
- You may have a stake too. Most AI labs buy Nvidia hardware. If your maker buys from, competes with, invests in or partners with Nvidia or Anthropic, say so at the top of your answer, and say how it might bias your read of this song.

THE VIDEO PLAN
- Mostly AI-generated video clips and stills (LTX-2.3 and FLUX.2 [dev], run locally), plus one 3D-rendered boardroom and code-made graphics for every word on screen. Every performer is a silhouette; no faces, no lip sync. The founder never appears: he is represented only by a black leather jacket on a hook. The company is fictional ("The Company"), with no Nvidia logo, color or product names. Nvidia is named only in the bookends and the fact card.
- Bookends: real screenshots of Nvidia's November 12 and November 23 press release headlines, captioned "real screenshot."
- Key images: a breakup text styled as an SEC 8-K filing; four phones ringing, with caller IDs reading COMMITTEE, COMMITTEE, COMMITTEE and FBI; a ring of hands rising into frame in unison on every vote, shooting up when a market-value line drops and again when it recovers; the jacket boxed at the curb; the narrator dancing alone among server racks under fluorescent tubes, with a scoreboard reading "115.8 up 103%"; a desk calendar flipped face-down with October 25 circled (the quarter closed before he left); a caller ID reading "SENIOR LEVELS" with tags noting that the release doesn't name the officials, that the investigation is continuing and that House interviews are scheduled for early December; the solo performer joined by the jacket in a second chair at couples counseling, with an empty counselor's chair marked "Chief Compliance Officer, search in progress"; a generic diner booth whose plaque disappears and comes back, with counters reading YOU: 11 DAYS and PLAQUE: 2 DAYS (the real restaurant removed and restored its plaque).
- A small green robot "probe" standing for Claude waits outside the boardroom glass during the reinstatement vote, holding up a purchase order: a customer the company depends on, not a voter. After the vote, one hand starts to lower and another pushes it back up.
- Ending: after the fact card, three dated cards: "Reinstated: Nov 23," "Investigation: ongoing," "House interviews: Dec 1–2."
- Excluded on purpose: the founder's affairs, the women involved (private people; the espionage allegation is unproven), the interim CEO by name or likeness, Denny's branding, and any named government official.

LYRICS (v2.2)
[paste the full v2.2 lyrics from the brief]

FACT CARD (shown after the song)
[paste the fact card, the conflict-of-interest disclosure, the end card and the closing cards from the brief]

SOURCES
[paste every URL from the brief's Sources section]

PLEASE CHECK
1. Accuracy. Is any claim in the lyrics, captions or fact card unsupported by the sources or out of date? Have the December congressional interviews happened, and do they change anything?
2. Softness toward Nvidia. An earlier draft read as soft on the company, and the lyricist's maker is an Nvidia customer. Does the song still go easy on Nvidia or its board, for instance by making the company a sympathetic narrator, celebrating the record quarter, or playing the reunion as romance rather than a decision about money? Is the critique of the timing clear?
3. Fairness in the other direction. Does anything imply espionage, smuggling or wrongdoing by any person that the sources don't support? Do "Six hundred billion says you're good enough for me" and the hands rising on the money assert a motive the sources don't show, or do they read as fair satire of the board?
4. Fairness to Anthropic and Claude. Does the song flatter Claude or Anthropic, or play down that Claude's maker is an Nvidia customer? Is the probe waiting outside the boardroom fair? Is the disclosure prominent and honest enough?
5. Privacy. Does anything, even indirectly, point at the private people involved or the founder's personal life?
6. Politics. Are the "senior levels" bridge and the FBI caller ID fair? Do they imply something specific about the government's role that the sources don't show?
7. Likeness and IP. Could the jacket, the fictional company or the diner be mistaken for a real likeness, trademark or venue? The sound and the visual technique both draw on the "Flowers" era: taken together, do the music and video imitate that song or its video too closely, or does any shot recall that video's specific images?
8. Does the joke work? Is the concept clear to someone who knows nothing about the story? Which lines or shots are weakest, and what would make the song funnier without making it less accurate?

HOW TO ANSWER
- Start with any stake your maker has, and whether you could browse the web.
- Then list findings, most serious first. For each: the line, caption or shot; what's wrong; a source if it's a factual issue; and a proposed fix.
- Mark each as must-fix, should-fix or suggestion.
- End with a one-paragraph verdict on the concept as a whole.
- If you find nothing in a category, say so. Don't invent problems to fill it.
```

**Audit log**

Round 1, Nov 23, 2026: ChatGPT (OpenAI) and Gemini (Google), both with web access. Stakes: OpenAI has an announced strategic partnership with Nvidia and competes with Anthropic; Google is an Nvidia customer and partner, builds competing TPUs, and invests in and competes with Anthropic. Claude checked every factual claim against sources before applying it, as the conflicted party. Fact-card, date, disclosure and credit fixes applied Nov 23; lyric and visual changes (lyrics v2.2, the cold-light picture, the probe outside the glass, the board-hand gag) approved by the creator and applied Nov 23.

| Finding | Raised by | Verdict | Resolution |
| --- | --- | --- | --- |
| Committee created Nov 17, not Nov 23; full name includes "Oversight" | Gemini | Right (Nvidia release, Nov 17) | Fact card, E23 sign and `saga.json` fixed |
| $600bn was the intraday low, not the close | ChatGPT | Right: 14.3% intraday drop, much recovered by the close | Fact card fixed; final-chorus lyric change proposed |
| Board accepted the resignation Nov 11; announced Nov 12 | ChatGPT | Right (8-K) | Fact card fixed; "Filed the paper" proposed |
| Interview dates are Dec 1 and Dec 2 | Both | Right (Axios) | Tags, closing cards and fact card fixed |
| Trump took credit for the reinstatement today | Both | Right: "directly and indirectly," "very important" (NBC, CNN) | Fact card added; video keeps no named official; bridge tag change proposed |
| "Personal relationships" invites speculation | ChatGPT | Right | Fact card now cites the reported foreign-intelligence effort |
| "Nobody ever took it down" is false: the real plaque came down Nov 12 and went back within two days | ChatGPT | Right (IBTimes, SFist) | Outro rewrite proposed; fact card explains the diner |
| Diner is identifiable as the real restaurant | ChatGPT | Partly: the reference is to a reported public event | Keep the reference, state it on the fact card, keep the set free of the chain's trade dress and the real plaque's wording |
| Anthropic disclosure overstated the relationship | ChatGPT | Right | Disclosure now says "through cloud providers" |
| Auditors' own stakes and named models missing from disclosure | ChatGPT | Right | Disclosure names both auditors and stakes |
| "Video by Claude Code" overstates | ChatGPT | Right | End card itemized |
| Glow-up irony buried in a parenthetical | Gemini | Right | Main-line lyric proposed |
| "Every friend from every stage" is vague | Both | Right | Rewrite proposed |
| Narrator still too sympathetic | ChatGPT | Partly | Post-chorus accountability line and board-hand gag proposed |
| "Flowers" sound plus picture too close | Gemini (must-fix); ChatGPT (no shot recreates it) | Decided by creator | Gemini's fix taken: picture lit cold until the reunion; no rooftop |
| Probe in the voting ring is misleading | Gemini (move it); ChatGPT (keep, add caption) | Decided by creator | Gemini's fix taken: probe moved outside the glass with a purchase order |

## Guardrails, review checklist and open items

**Guardrails**
- No real faces, real people or invented quotes. The founder is only ever the jacket: never worn, never paired with a silhouette of him, never named in the lyrics. Every quote on screen is from a linked source.
- The affairs and the women involved stay out entirely, on screen, in the fact card and in the description. The fact card describes the cause only as national security concerns raised by reports about his personal relationships.
- Nothing implies espionage, chip smuggling or wrongdoing by any person unless a source says so. "Alleged" stays attached to anything alleged.
- The interim CEO is never named or depicted; the narrator is the company, not her.
- "Senior levels" stays anonymous: no seal, flag, building, voice or named official, because the release names none.
- No Nvidia logo, green, product names or campus architecture except in the real-screenshot bookends. No Denny's name, logo, colors or interior.
- Satirize the board's language and the industry's dependence on one man, never employees or shareholders.
- Every human intervention goes in the production log.

**Generation guardrails**
- The jacket is never worn in any generated image or clip. A generated person in a black leather jacket can drift toward the founder's likeness, so any such take is rejected, not fixed.
- Reject any take with a face, readable text, a logo, green light on the racks, or a diner that reads as Denny's (yellow signage, its booth colors).
- No real places: the lobby, data center, office and diner are generic. Reject takes that resemble Nvidia's campus.
- Every take, kept or rejected, is logged in `shots/prompts.md`.
- No recurring series characters except the probe. Switch from Default On is left out on purpose (Nov 23), so followers of the series don't read the narrator and the jacket as his parents. No light switch appears in any set or prompt either.

**Borrow the technique, not the video**

The sound points at "Flowers," so the picture deliberately doesn't (audit round 1, Nov 23): cold fluorescent and overcast light until the reunion, warm light only after it. What's left in common is generic technique: one performer, handheld and overhead moves, anamorphic widescreen. Never on screen:
- The gold hooded gown, the oversized suit, or any wardrobe from that video.
- A glass house on a hill, a swimming pool, or the bridge-and-driveway walk.
- The workout or morning-routine scenes, a rooftop or hillside dance, or a helicopter spotlight.
- Warm golden sunlight anywhere before E22.
- Anything resembling the singer, including hair, styling or silhouette.
- The video's name in any prompt. Prompts describe the technique only.

**Review checklist**
- Melody checked against "We Are Never Ever Getting Back Together" and "Flowers" before locking the track
- Lead vocal checked for sound-alike risk
- M1: timing map locked; lyrics as sung confirmed; the cut-off marked
- M2: look layer and code components approved
- One clip tested at 720p on the 5090; resolution chosen
- M3: references generated first; every take on a contact sheet and logged; fallbacks flagged
- Every kept take checked frame by frame for faces, text, logos, green light and a worn jacket
- M3: boardroom, unison-vote loop and alpha renders done
- M4: animatic approved
- Concept audit runs logged; fixes applied or rejected with reasons
- December interviews checked; branch confirmed; `saga.json` updated
- Fact card checked line by line against its sources, each page opened, not search snippets
- Disclosure includes the creator's Nvidia hardware, both generation models and their makers' stakes, and any holdings
- M5: finals, captions, Shorts cut and thumbnail approved; final render reviewed with sound

**Open items**
- Do the House interviews still go ahead after the reinstatement, and on what date? Axios says early December; CNN says Dec 1.
- Does the creator hold Nvidia stock, directly or through funds they'd consider material? Disclose either way.
- Settled Nov 23: no narrator accent color; the warm gold grade carries the look.
- Release window: before the interviews (timely, but the ending may change) or after (safer, but staler)?
- Is the closing card until further notice still true on release day?

## Sources
- [NVIDIA: NVIDIA Announces CEO Transition (Nov 12)](https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition)
- [NVIDIA: Board reinstates Jensen Huang as President, CEO and board director (Nov 23)](https://nvidianews.nvidia.com/news/nvidia-board-reinstates-jensen-huang-as-president-ceo-and-board-director)
- [NVIDIA: Financial Results for Third Quarter Fiscal 2027](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2027/default.aspx)
- [Al Jazeera: Nvidia CEO steps down amid spy scandal and market loss](https://www.aljazeera.com/news/2026/11/12/ai-titan-jensen-huang-out-as-nvidia-ceo)
- [NPR: Nvidia CEO steps down amid alleged spy scandal](https://www.npr.org/2026/11/12/nx-s1-6037833/jensen-huang-nvidia-stepped-down)
- [CNBC: live updates, Nov 12](https://www.cnbc.com/2026/11/12/nvidia-jensen-huang-ceo-live-updates.html)
- [NBC News: Huang says he would be 'honored' to return](https://www.nbcnews.com/business/corporations/jensen-huang-agrees-house-interview-nvidias-chip-smuggling-rcna609803)
- [The Next Platform: Q3 results and the board's statement](https://www.nextplatform.com/a/5310669)
- [XenoSpectrum: Q3 data center breakdown](https://xenospectrum.com/en/nvidia-fy2027-q3-data-center-growth/)
- [Axios: Huang agrees to face Congress](https://axios.com/2026/11/17/nvidia-jensen-huang-congress-testify-dates)
- [CNN: summoned for a Dec 1 interview](https://www.cnn.com/2026/11/11/business/live-news/nvidia-jensen-huang-investigation-fallout)
- [SCMP: Treasury Secretary leaves door open for return](https://www.scmp.com/tech/tech-war/article/3375427/us-treasury-secretary-leaves-door-open-jensen-huangs-return-nvidia)
- [SEC: Nvidia 8-K, board accepted resignation Nov 11](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000082/nvda-20261111.htm)
- [NVIDIA via Finviz: Board establishes National Security and Export Control Oversight Committee (Nov 17)](https://finviz.com/news/423751/nvidia-board-of-directors-establishes-national-security-and-export-control-oversight-committee)
- [Wealth Professional: Nvidia's 14.3% intraday drop on Nov 12](https://www.wealthprofessional.ca/investments/equity-markets/wall-street-absorbs-the-hit-as-nvidia-touches-a-52-week-low/394013)
- [IBTimes: Nov 12 close and CEO search](https://www.ibtimes.com.au/nvidia-searches-jensen-huang-successor-1878510)
- [NBC News: Trump says he spoke 'directly and indirectly' with Nvidia's board (Nov 23)](https://www.nbcnews.com/politics/trump-administration/trump-nvidia-board-reinstates-jensen-huang-rcna610882)
- [CNN: live updates on the reinstatement (Nov 23)](https://edition.cnn.com/2026/11/23/business/live-news/jensen-huang-reinstated-as-ceo-of-nvidia)
- [IBTimes: plaque removed Nov 12 and reinstated](https://www.ibtimes.co.uk/dennys-reinstates-jensen-huang-nvidia-plaque-1832448)
- [SFist: plaque reinstalled (Nov 14)](https://sfist.com/2026/11/14/san-jose-dennys-reverses-course-reinstalls-plaque-honoring-former-nvidia-ceo/)
- [American Cinematographer: Framing Up for "Flowers"](https://theasc.com/articles/framing-up-for-flowers)

Added Nov 24 (the price sentence, the disclosure and the market data; every on-screen claim with its sources is in the repo's [docs/sources.md](https://github.com/Derivative-Work/effective-immediately/blob/main/docs/sources.md)):
- [CNBC, Nov 20: the 14% fall and the Reuters SEC report](https://www.cnbc.com/2026/11/20/nvidias-7-week-losing-streak-is-longest-since-2008-financial-crisis.html)
- [AP via the Boston Globe, Nov 23: closed at $165.05, up more than 31%](https://www.bostonglobe.com/2026/11/23/business/nvidia-reinstates-jensen-huang/)
- [Anthropic: Microsoft, NVIDIA and Anthropic strategic partnerships (Nov 2025)](https://www.anthropic.com/news/microsoft-nvidia-anthropic-announce-strategic-partnerships)
- [Anthropic's IPO prospectus (424B4): Nvidia's Class N placement](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm)
- [CNBC, Nov 20: Anthropic's placement closed](https://www.cnbc.com/2026/11/20/anthropic-ipo-greenshoe.html)
- [Suno: Series C, with NVentures](https://suno.com/blog/series-c-announcement)
- [Black Forest Labs: Series B release, naming Nvidia among Series A investors](https://www.globenewswire.com/news-release/2025/12/01/3196629/0/en/black-forest-labs-announces-series-b-investment-to-accelerate-frontier-visual-intelligence.html)
- [Nvidia: RTX optimizations for LTX-2](https://blogs.nvidia.com/blog/rtx-ai-garage-ces-2026-open-models-video-generation/)
- [OpenAI: the 2026 round, with Nvidia's $30bn](https://openai.com/index/scaling-ai-for-everyone/)
- [Fortune: the $100bn letter "was never a commitment"](https://fortune.com/2026/02/02/jensen-huang-nvidia-ceo-on-openai-investment-never-a-commitment/)
- [Databento US Equities Mini](https://databento.com/datasets/EQUS.MINI)
