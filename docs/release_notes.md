An AI-made bass-forward boogie-funk disco breakup song about Nvidia's board, which announced on November 12, 2026 that its founder-CEO had resigned "effective immediately", then reinstated him eleven days later. The company sings it. The founder is only ever a black leather jacket on a hook, and the board's hands go up on the beat. Claude Code (Opus 5.5) produced the video with Remotion, Blender, FLUX.2 [dev] and LTX-2.3. Suno V6 made the music, which a human edited in Logic Pro, post-filtered with music-deslop. Claude wrote the words. Every human action is logged in [log/human_interventions.md](https://github.com/Derivative-Work/effective-immediately/blob/main/log/human_interventions.md).

AI-generated satire about real events. Not investment advice. Every claim on screen is listed with its sources in [docs/sources.md](https://github.com/Derivative-Work/effective-immediately/blob/main/docs/sources.md), as of November 24, 2026. Conflict of interest: Claude, made by Anthropic, wrote the lyrics. Nvidia is an Anthropic shareholder, and Anthropic runs Claude partly on Nvidia GPUs. ChatGPT and Gemini audited the plan. See the [README](https://github.com/Derivative-Work/effective-immediately#effective-immediately). Market data provided by Databento.

**Watch:** [the video](https://youtu.be/i5uLYgoSIkk)

## Files

| File | What |
| --- | --- |
| `effective_immediately_1080p.mp4` | The video, 7:43, H.264 1080p, 24 fps, AAC: the YouTube upload file itself |
| `effective_immediately_short_chorus.mp4` | Short 1, 43.0 s: the vote in chorus 1, a hand up on each beat as the market value falls |
| `effective_immediately_short_bridge.mp4` | Short 2, 34.1 s: the bridge, and the desk phone ringing: SENIOR LEVELS |
| `effective_immediately_short_reinstated.mp4` | Short 3, 37.0 s: the final chorus, the jacket back on the hook and the board voting him back |
| `effective_immediately_short_plaque.mp4` | Short 4, 17.8 s: the diner plaque that comes down the day he left and goes back up before he does |
| `effective_immediately.en.srt` | English subtitles for the video: the lyrics as sung, line by line |
| `effective_immediately_short_<name>.en.srt` | English subtitles for each Short, timed from its first frame |
| `effective_immediately_thumbnail.jpg` | The thumbnail: the empty hook on Nov 12, the jacket back in the booth on Nov 23 |
| `effective-immediately.logicx.zip` | The creator's Logic Pro project for the master: the chorus riff copied into the intro, the bass boosted and brightened, a bar taken out after "in—", and the cut with its reverb throw. Its audio is Suno's twelve stems and nothing else, through Logic's own plugins: no loops, samples or software instruments. Space Designer's impulse response ("1.3s Conference Room") is Logic's own and isn't included |
| `inputs-suno.tar` | Suno's audio, none of which can be regenerated: the first generation and its stems as downloaded, the generation used and its stems, and the credits music (a Suno instrumental cover) |
| `inputs-master.tar` | The masters bounced from the Logic project (the first, and the one used, with less crackle) and their twelve stems; the post-filtered masters and credits music |
| `takes.tar` | Every generated still and clip, used or not: the FLUX.2 [dev] stills and the LTX-2.3 clips |
| `SHA256SUMS` | Checksums for every file above |

Every file inside the tars, and every render, frame and superseded take, is listed with its SHA-256 hash in [MANIFEST.sha256](https://github.com/Derivative-Work/effective-immediately/blob/main/MANIFEST.sha256). The [production log](https://github.com/Derivative-Work/effective-immediately/blob/main/log/production_log.md) has the command for each, and [scripts/release.sh](https://github.com/Derivative-Work/effective-immediately/blob/main/scripts/release.sh) builds this release. The audio is in two tars because together it passes GitHub's 2 GiB limit per file.

Not included:
- the creator's screenshots of Nvidia's two releases (the video shows them cropped; the full pages show the creator's browser);
- the market data: Databento's terms don't allow redistributing it ([scripts/fetch_databento.py](https://github.com/Derivative-Work/effective-immediately/blob/main/scripts/fetch_databento.py) fetches it with your own key), and the archived renders drawn from Alpaca's data, which the video doesn't use;
- the post-filter model, private for now;
- the people kit's figure library, rebuilt from [blender/ep/](https://github.com/Derivative-Work/effective-immediately/tree/main/blender/ep) and MakeHuman's CC0 assets;
- renders, frames and animatics, which regenerate from the logged commands;
- the Claude Code session transcript.

## Licences

Video, music and assets: [CC BY-NC-SA 4.0](https://github.com/Derivative-Work/effective-immediately/blob/main/LICENSE-media.md). Code: [MIT](https://github.com/Derivative-Work/effective-immediately/blob/main/LICENSE). Satire; not affiliated with or endorsed by Nvidia or any company named.
