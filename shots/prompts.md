# Prompts and takes

Append-only: every still and clip, kept or rejected. Picks are in `config/picks.json`.

## Stills: FLUX.2 [dev]

Model `flux2_dev_fp8mixed.safetensors`, text encoder `mistral_3_small_flux2_fp4_mixed.safetensors`, VAE `flux2-vae.safetensors`; 28 steps, euler, guidance 4.0; ComfyUI v0.42.1. No negative prompt (FLUX.2 [dev] is guidance-distilled). Prompts verbatim in `shots/prompts/<item>.txt`.

| Item | Seed | Size | Output | Seconds | When |
| --- | --- | --- | --- | --- | --- |
| ref_narrator | 1123 | 1664×1248 | `assets/gen/stills/ref_narrator/ref_narrator_s1123.png` | 76.4 | 2026-11-23T13:50:09-05:00 |
| ref_narrator | 1124 | 1664×1248 | `assets/gen/stills/ref_narrator/ref_narrator_s1124.png` | 49.1 | 2026-11-23T13:50:58-05:00 |
| ref_narrator | 1125 | 1664×1248 | `assets/gen/stills/ref_narrator/ref_narrator_s1125.png` | 49.3 | 2026-11-23T13:51:47-05:00 |
| ref_narrator | 1126 | 1664×1248 | `assets/gen/stills/ref_narrator/ref_narrator_s1126.png` | 51.1 | 2026-11-23T13:52:38-05:00 |
| ref_jacket | 1123 | 1248×1248 | `assets/gen/stills/ref_jacket/ref_jacket_s1123.png` | 45.4 | 2026-11-23T13:53:24-05:00 |
| ref_jacket | 1124 | 1248×1248 | `assets/gen/stills/ref_jacket/ref_jacket_s1124.png` | 35.1 | 2026-11-23T13:53:59-05:00 |
| ref_jacket | 1125 | 1248×1248 | `assets/gen/stills/ref_jacket/ref_jacket_s1125.png` | 36.1 | 2026-11-23T13:54:35-05:00 |
| ref_jacket | 1126 | 1248×1248 | `assets/gen/stills/ref_jacket/ref_jacket_s1126.png` | 35.4 | 2026-11-23T13:55:10-05:00 |
| G01 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G01/G01_s1123.png` | 66.8 | 2026-11-23T13:57:23-05:00 |
| G01 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G01/G01_s1124.png` | 48.1 | 2026-11-23T13:58:11-05:00 |
| G02 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G02/G02_s1123.png` | 50.1 | 2026-11-23T13:59:01-05:00 |
| G02 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G02/G02_s1124.png` | 48.1 | 2026-11-23T13:59:49-05:00 |
| G03 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G03/G03_s1123.png` | 50.1 | 2026-11-23T14:00:39-05:00 |
| G03 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G03/G03_s1124.png` | 48.1 | 2026-11-23T14:01:28-05:00 |
| G04 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G04/G04_s1123.png` | 50.1 | 2026-11-23T14:02:18-05:00 |
| G04 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G04/G04_s1124.png` | 48.1 | 2026-11-23T14:03:06-05:00 |
| G05 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G05/G05_s1123.png` | 52.2 | 2026-11-23T14:03:58-05:00 |
| G05 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G05/G05_s1124.png` | 48.1 | 2026-11-23T14:04:46-05:00 |
| G06 | 1123 | 1536×656 | `assets/gen/stills/G06/G06_s1123.png` | 24.3 | 2026-11-23T14:05:10-05:00 |
| G06 | 1124 | 1536×656 | `assets/gen/stills/G06/G06_s1124.png` | 22.2 | 2026-11-23T14:05:33-05:00 |
| G07 (refs: ref_jacket) | 1123 | 1536×656 | `assets/gen/stills/G07/G07_s1123.png` | 50.1 | 2026-11-23T14:06:23-05:00 |
| G07 (refs: ref_jacket) | 1124 | 1536×656 | `assets/gen/stills/G07/G07_s1124.png` | 48.1 | 2026-11-23T14:07:11-05:00 |
| G08 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G08/G08_s1123.png` | 50.1 | 2026-11-23T14:08:01-05:00 |
| G08 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G08/G08_s1124.png` | 48.1 | 2026-11-23T14:08:49-05:00 |
| G09 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G09/G09_s1123.png` | 49.1 | 2026-11-23T14:09:38-05:00 |
| G09 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G09/G09_s1124.png` | 48.1 | 2026-11-23T14:10:26-05:00 |
| G10 | 1123 | 1536×656 | `assets/gen/stills/G10/G10_s1123.png` | 23.3 | 2026-11-23T14:10:49-05:00 |
| G10 | 1124 | 1536×656 | `assets/gen/stills/G10/G10_s1124.png` | 22.1 | 2026-11-23T14:11:12-05:00 |
| G11 | 1123 | 1536×656 | `assets/gen/stills/G11/G11_s1123.png` | 23.3 | 2026-11-23T14:11:35-05:00 |
| G11 | 1124 | 1536×656 | `assets/gen/stills/G11/G11_s1124.png` | 22.1 | 2026-11-23T14:11:57-05:00 |
| S01 (refs: ref_jacket) | 1123 | 2560×1088 | `assets/gen/stills/S01/S01_s1123.png` | 112.2 | 2026-11-23T14:13:49-05:00 |
| S01 (refs: ref_jacket) | 1124 | 2560×1088 | `assets/gen/stills/S01/S01_s1124.png` | 110.2 | 2026-11-23T14:15:39-05:00 |
| S02 (refs: ref_narrator) | 1123 | 1920×816 | `assets/gen/stills/S02/S02_s1123.png` | 68.1 | 2026-11-23T14:16:47-05:00 |
| S02 (refs: ref_narrator) | 1124 | 1920×816 | `assets/gen/stills/S02/S02_s1124.png` | 67.1 | 2026-11-23T14:17:55-05:00 |
| jacket (refs: ref_jacket) | 1123 | 1024×1280 | `assets/gen/stills/jacket/jacket_s1123.png` | 61.1 | 2026-11-23T14:18:56-05:00 |
| jacket (refs: ref_jacket) | 1124 | 1024×1280 | `assets/gen/stills/jacket/jacket_s1124.png` | 60.1 | 2026-11-23T14:19:56-05:00 |
| plaque | 1123 | 1280×832 | `assets/gen/stills/plaque/plaque_s1123.png` | 25.0 | 2026-11-23T14:20:21-05:00 |
| plaque | 1124 | 1280×832 | `assets/gen/stills/plaque/plaque_s1124.png` | 24.0 | 2026-11-23T14:20:45-05:00 |
| G05_v2 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G05/G05_v2_s1123.png` | 70.3 | 2026-11-23T14:23:37-05:00 |
| G05_v2 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G05/G05_v2_s1124.png` | 48.1 | 2026-11-23T14:24:25-05:00 |
| G06_v2 | 1123 | 1536×656 | `assets/gen/stills/G06/G06_v2_s1123.png` | 25.2 | 2026-11-23T14:24:50-05:00 |
| G06_v2 | 1124 | 1536×656 | `assets/gen/stills/G06/G06_v2_s1124.png` | 22.1 | 2026-11-23T14:25:12-05:00 |
| G07_v2 (refs: ref_jacket) | 1123 | 1536×656 | `assets/gen/stills/G07/G07_v2_s1123.png` | 50.1 | 2026-11-23T14:26:02-05:00 |
| G07_v2 (refs: ref_jacket) | 1124 | 1536×656 | `assets/gen/stills/G07/G07_v2_s1124.png` | 48.1 | 2026-11-23T14:26:50-05:00 |
| G10_v2 | 1123 | 1536×656 | `assets/gen/stills/G10/G10_v2_s1123.png` | 24.2 | 2026-11-23T14:27:15-05:00 |
| G10_v2 | 1124 | 1536×656 | `assets/gen/stills/G10/G10_v2_s1124.png` | 22.1 | 2026-11-23T14:27:37-05:00 |
| G11_v2 | 1123 | 1536×656 | `assets/gen/stills/G11/G11_v2_s1123.png` | 26.4 | 2026-11-23T14:28:03-05:00 |
| G11_v2 | 1124 | 1536×656 | `assets/gen/stills/G11/G11_v2_s1124.png` | 22.1 | 2026-11-23T14:28:25-05:00 |
| S01_v2 | 1123 | 2560×1088 | `assets/gen/stills/S01/S01_v2_s1123.png` | 72.4 | 2026-11-23T14:29:38-05:00 |
| S01_v2 | 1124 | 2560×1088 | `assets/gen/stills/S01/S01_v2_s1124.png` | 72.7 | 2026-11-23T14:30:50-05:00 |

## Clips: LTX-2.3

ComfyUI template `video_ltx2_3_i2v` (`ltx-2.3-22b-dev-fp8` + distilled LoRA 0.5, Gemma 3 12B fp4 encoder, x2 spatial upscaler), prompt enhancer off, the brief's negatives. Prompts verbatim in `shots/prompts/<clip>_clip.txt`.

| Clip | Keyframe | Seed | Output | Seconds | When |
| --- | --- | --- | --- | --- | --- |
| G01 | `assets/gen/stills/G01/G01_s1123.png` | 1123 | `assets/gen/clips/G01/G01_s1123.mp4` | 30.1 | 2026-11-23T14:31:24-05:00 |
| G01 | `assets/gen/stills/G01/G01_s1123.png` | 1124 | `assets/gen/clips/G01/G01_s1124.mp4` | 10.4 | 2026-11-23T14:31:34-05:00 |
| G02 | `assets/gen/stills/G02/G02_r_s1123.png` | 1123 | `assets/gen/clips/G02/G02_s1123.mp4` | 14.0 | 2026-11-23T14:31:48-05:00 |
| G02 | `assets/gen/stills/G02/G02_r_s1123.png` | 1124 | `assets/gen/clips/G02/G02_s1124.mp4` | 7.0 | 2026-11-23T14:31:55-05:00 |
| G03 | `assets/gen/stills/G03/G03_s1123.png` | 1123 | `assets/gen/clips/G03/G03_s1123.mp4` | 15.3 | 2026-11-23T14:32:10-05:00 |
| G03 | `assets/gen/stills/G03/G03_s1123.png` | 1124 | `assets/gen/clips/G03/G03_s1124.mp4` | 11.3 | 2026-11-23T14:32:22-05:00 |
| G04 | `assets/gen/stills/G04/G04_r_s1123.png` | 1123 | `assets/gen/clips/G04/G04_s1123.mp4` | 13.5 | 2026-11-23T14:32:35-05:00 |
| G04 | `assets/gen/stills/G04/G04_r_s1123.png` | 1124 | `assets/gen/clips/G04/G04_s1124.mp4` | 10.2 | 2026-11-23T14:32:45-05:00 |
| G08 | `assets/gen/stills/G08/G08_s1123.png` | 1123 | `assets/gen/clips/G08/G08_s1123.mp4` | 13.4 | 2026-11-23T14:32:59-05:00 |
| G08 | `assets/gen/stills/G08/G08_s1123.png` | 1124 | `assets/gen/clips/G08/G08_s1124.mp4` | 10.3 | 2026-11-23T14:33:09-05:00 |
| G09 | `assets/gen/stills/G09/G09_s1123.png` | 1123 | `assets/gen/clips/G09/G09_s1123.mp4` | 13.2 | 2026-11-23T14:33:22-05:00 |
| G09 | `assets/gen/stills/G09/G09_s1123.png` | 1124 | `assets/gen/clips/G09/G09_s1124.mp4` | 10.0 | 2026-11-23T14:33:32-05:00 |
| G05 | `assets/gen/stills/G05/G05_r_s1123.png` | 1123 | `assets/gen/clips/G05/G05_s1123.mp4` | 26.3 | 2026-11-23T14:35:34-05:00 |
| G05 | `assets/gen/stills/G05/G05_r_s1123.png` | 1124 | `assets/gen/clips/G05/G05_s1124.mp4` | 7.0 | 2026-11-23T14:35:41-05:00 |
| G06 | `assets/gen/stills/G06/G06_v2_s1123.png` | 1123 | `assets/gen/clips/G06/G06_s1123.mp4` | 11.1 | 2026-11-23T14:35:52-05:00 |
| G06 | `assets/gen/stills/G06/G06_v2_s1123.png` | 1124 | `assets/gen/clips/G06/G06_s1124.mp4` | 7.0 | 2026-11-23T14:35:59-05:00 |
| G07 | `assets/gen/stills/G07/G07_v2_s1123.png` | 1123 | `assets/gen/clips/G07/G07_s1123.mp4` | 16.2 | 2026-11-23T14:36:15-05:00 |
| G07 | `assets/gen/stills/G07/G07_v2_s1123.png` | 1124 | `assets/gen/clips/G07/G07_s1124.mp4` | 12.1 | 2026-11-23T14:36:27-05:00 |
| G10 | `assets/gen/stills/G10/G10_r_s1124.png` | 1123 | `assets/gen/clips/G10/G10_s1123.mp4` | 11.5 | 2026-11-23T14:36:39-05:00 |
| G10 | `assets/gen/stills/G10/G10_r_s1124.png` | 1124 | `assets/gen/clips/G10/G10_s1124.mp4` | 7.0 | 2026-11-23T14:36:46-05:00 |
| G11 | `assets/gen/stills/G11/G11_v2_s1123.png` | 1123 | `assets/gen/clips/G11/G11_s1123.mp4` | 13.3 | 2026-11-23T14:36:59-05:00 |
| G11 | `assets/gen/stills/G11/G11_v2_s1123.png` | 1124 | `assets/gen/clips/G11/G11_s1124.mp4` | 10.0 | 2026-11-23T14:37:09-05:00 |
| G12 | `assets/gen/stills/G11/G11_v2_s1123.png` | 1123 | `assets/gen/clips/G12/G12_s1123.mp4` | 11.0 | 2026-11-23T14:37:20-05:00 |
| G12 | `assets/gen/stills/G11/G11_v2_s1123.png` | 1124 | `assets/gen/clips/G12/G12_s1124.mp4` | 7.0 | 2026-11-23T14:37:27-05:00 |
| G10 | `assets/gen/stills/G10/G10_r_s1124.png` | 1125 | `assets/gen/clips/G10/G10_s1125.mp4` | 50.4 | 2026-11-23T14:40:26-05:00 |
| G10 | `assets/gen/stills/G10/G10_r_s1124.png` | 1126 | `assets/gen/clips/G10/G10_s1126.mp4` | 7.1 | 2026-11-23T14:40:33-05:00 |
| S03 (refs: G11_last, ref_jacket) | 1123 | 1600×640 | `assets/gen/stills/S03/S03_s1123.png` | 95.1 | 2026-11-23T14:47:38-05:00 |
| S03 (refs: G11_last, ref_jacket) | 1124 | 1600×640 | `assets/gen/stills/S03/S03_s1124.png` | 78.2 | 2026-11-23T14:48:56-05:00 |
| G12 | `assets/gen/stills/G11_last/G11_last_s1124.png` | 1125 | `assets/gen/clips/G12/G12_s1125.mp4` | 27.1 | 2026-11-23T14:50:52-05:00 |
| G12 | `assets/gen/stills/G11_last/G11_last_s1124.png` | 1126 | `assets/gen/clips/G12/G12_s1126.mp4` | 7.0 | 2026-11-23T14:50:59-05:00 |
| hand_phone | 1123 | 1536×656 | `assets/gen/stills/hand_phone/hand_phone_s1123.png` | 57.1 | 2026-11-23T16:18:13-05:00 |
| hand_phone | 1124 | 1536×656 | `assets/gen/stills/hand_phone/hand_phone_s1124.png` | 24.2 | 2026-11-23T16:18:37-05:00 |
| hand_phone | 1125 | 1536×656 | `assets/gen/stills/hand_phone/hand_phone_s1125.png` | 25.0 | 2026-11-23T16:19:02-05:00 |
| hand_phone | 1126 | 1536×656 | `assets/gen/stills/hand_phone/hand_phone_s1126.png` | 30.4 | 2026-11-23T16:19:32-05:00 |
| hand_phone_night | 1123 | 1536×656 | `assets/gen/stills/hand_phone_night/hand_phone_night_s1123.png` | 28.0 | 2026-11-23T16:20:00-05:00 |
| hand_phone_night | 1124 | 1536×656 | `assets/gen/stills/hand_phone_night/hand_phone_night_s1124.png` | 25.0 | 2026-11-23T16:20:26-05:00 |
| hand_phone_night | 1125 | 1536×656 | `assets/gen/stills/hand_phone_night/hand_phone_night_s1125.png` | 24.4 | 2026-11-23T16:20:50-05:00 |
| hand_phone_night | 1126 | 1536×656 | `assets/gen/stills/hand_phone_night/hand_phone_night_s1126.png` | 24.4 | 2026-11-23T16:21:14-05:00 |
| G13 | 1123 | 1536×656 | `assets/gen/stills/G13/G13_s1123.png` | 38.1 | 2026-11-23T17:41:48-05:00 |
| G13 | 1124 | 1536×656 | `assets/gen/stills/G13/G13_s1124.png` | 22.0 | 2026-11-23T17:42:10-05:00 |
| G14 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G14/G14_s1123.png` | 61.8 | 2026-11-23T17:43:12-05:00 |
| G14 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G14/G14_s1124.png` | 48.1 | 2026-11-23T17:44:00-05:00 |
| G15 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G15/G15_s1123.png` | 49.2 | 2026-11-23T17:44:49-05:00 |
| G15 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G15/G15_s1124.png` | 48.3 | 2026-11-23T17:45:37-05:00 |
| G16 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G16/G16_s1123.png` | 49.1 | 2026-11-23T17:46:26-05:00 |
| G16 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G16/G16_s1124.png` | 48.1 | 2026-11-23T17:47:15-05:00 |
| G17 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G17/G17_s1123.png` | 49.3 | 2026-11-23T17:48:04-05:00 |
| G17 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G17/G17_s1124.png` | 49.1 | 2026-11-23T17:48:53-05:00 |
| G18 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G18/G18_s1123.png` | 49.2 | 2026-11-23T17:49:42-05:00 |
| G18 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G18/G18_s1124.png` | 48.3 | 2026-11-23T17:50:31-05:00 |
| G19 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G19/G19_s1123.png` | 49.2 | 2026-11-23T17:51:20-05:00 |
| G19 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G19/G19_s1124.png` | 49.1 | 2026-11-23T17:52:09-05:00 |
| G20 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G20/G20_s1123.png` | 49.1 | 2026-11-23T17:52:58-05:00 |
| G20 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G20/G20_s1124.png` | 48.4 | 2026-11-23T17:53:46-05:00 |
| G21 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G21/G21_s1123.png` | 49.2 | 2026-11-23T17:54:36-05:00 |
| G21 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G21/G21_s1124.png` | 48.3 | 2026-11-23T17:55:24-05:00 |
| G22 (refs: ref_jacket) | 1123 | 1536×656 | `assets/gen/stills/G22/G22_s1123.png` | 50.1 | 2026-11-23T17:56:14-05:00 |
| G22 (refs: ref_jacket) | 1124 | 1536×656 | `assets/gen/stills/G22/G22_s1124.png` | 49.1 | 2026-11-23T17:57:03-05:00 |
| G23 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G23/G23_s1123.png` | 50.1 | 2026-11-23T17:57:53-05:00 |
| G23 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G23/G23_s1124.png` | 48.3 | 2026-11-23T17:58:41-05:00 |
| G24 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G24/G24_s1123.png` | 49.2 | 2026-11-23T17:59:31-05:00 |
| G24 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G24/G24_s1124.png` | 48.3 | 2026-11-23T18:00:19-05:00 |
| G25 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G25/G25_s1123.png` | 49.2 | 2026-11-23T18:01:08-05:00 |
| G25 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G25/G25_s1124.png` | 48.4 | 2026-11-23T18:01:57-05:00 |
| G26 | 1123 | 1536×656 | `assets/gen/stills/G26/G26_s1123.png` | 24.0 | 2026-11-23T18:02:21-05:00 |
| G26 | 1124 | 1536×656 | `assets/gen/stills/G26/G26_s1124.png` | 23.0 | 2026-11-23T18:02:44-05:00 |
| G27 | 1123 | 1536×656 | `assets/gen/stills/G27/G27_s1123.png` | 24.0 | 2026-11-23T18:03:08-05:00 |
| G27 | 1124 | 1536×656 | `assets/gen/stills/G27/G27_s1124.png` | 23.0 | 2026-11-23T18:03:31-05:00 |
| G28 | 1123 | 1536×656 | `assets/gen/stills/G28/G28_s1123.png` | 24.0 | 2026-11-23T18:03:55-05:00 |
| G28 | 1124 | 1536×656 | `assets/gen/stills/G28/G28_s1124.png` | 23.0 | 2026-11-23T18:04:18-05:00 |
| G29 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G29/G29_s1123.png` | 50.1 | 2026-11-23T18:05:08-05:00 |
| G29 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G29/G29_s1124.png` | 48.3 | 2026-11-23T18:05:56-05:00 |
| G30 | 1123 | 1536×656 | `assets/gen/stills/G30/G30_s1123.png` | 24.0 | 2026-11-23T18:06:20-05:00 |
| G30 | 1124 | 1536×656 | `assets/gen/stills/G30/G30_s1124.png` | 23.0 | 2026-11-23T18:06:43-05:00 |
| G32 (refs: ref_jacket) | 1123 | 1536×656 | `assets/gen/stills/G32/G32_s1123.png` | 50.1 | 2026-11-23T18:07:33-05:00 |
| G32 (refs: ref_jacket) | 1124 | 1536×656 | `assets/gen/stills/G32/G32_s1124.png` | 49.1 | 2026-11-23T18:08:22-05:00 |
| G33 | 1123 | 1536×656 | `assets/gen/stills/G33/G33_s1123.png` | 24.0 | 2026-11-23T18:08:47-05:00 |
| G33 | 1124 | 1536×656 | `assets/gen/stills/G33/G33_s1124.png` | 23.0 | 2026-11-23T18:09:10-05:00 |
| G13 | `assets/gen/stills/G13/G13_s1124.png` | 1123 | `assets/gen/clips/G13/G13_s1123.mp4` | 31.4 | 2026-11-23T18:11:43-05:00 |
| G13 | `assets/gen/stills/G13/G13_s1124.png` | 1124 | `assets/gen/clips/G13/G13_s1124.mp4` | 14.0 | 2026-11-23T18:11:57-05:00 |
| G14 | `assets/gen/stills/G14/G14_s1123.png` | 1123 | `assets/gen/clips/G14/G14_s1123.mp4` | 18.3 | 2026-11-23T18:12:15-05:00 |
| G14 | `assets/gen/stills/G14/G14_s1123.png` | 1124 | `assets/gen/clips/G14/G14_s1124.mp4` | 13.1 | 2026-11-23T18:12:29-05:00 |
| G15 | `assets/gen/stills/G15/G15_s1123.png` | 1123 | `assets/gen/clips/G15/G15_s1123.mp4` | 17.3 | 2026-11-23T18:12:46-05:00 |
| G15 | `assets/gen/stills/G15/G15_s1123.png` | 1124 | `assets/gen/clips/G15/G15_s1124.mp4` | 13.3 | 2026-11-23T18:12:59-05:00 |
| G17 | `assets/gen/stills/G17/G17_s1123.png` | 1123 | `assets/gen/clips/G17/G17_s1123.mp4` | 15.1 | 2026-11-23T18:13:14-05:00 |
| G17 | `assets/gen/stills/G17/G17_s1123.png` | 1124 | `assets/gen/clips/G17/G17_s1124.mp4` | 13.0 | 2026-11-23T18:13:27-05:00 |
| G18 | `assets/gen/stills/G18/G18_s1123.png` | 1123 | `assets/gen/clips/G18/G18_s1123.mp4` | 15.0 | 2026-11-23T18:13:42-05:00 |
| G18 | `assets/gen/stills/G18/G18_s1123.png` | 1124 | `assets/gen/clips/G18/G18_s1124.mp4` | 13.6 | 2026-11-23T18:13:56-05:00 |
| G19 | `assets/gen/stills/G19/G19_s1123.png` | 1123 | `assets/gen/clips/G19/G19_s1123.mp4` | 15.0 | 2026-11-23T18:14:11-05:00 |
| G19 | `assets/gen/stills/G19/G19_s1123.png` | 1124 | `assets/gen/clips/G19/G19_s1124.mp4` | 13.0 | 2026-11-23T18:14:24-05:00 |
| G20 | `assets/gen/stills/G20/G20_s1123.png` | 1123 | `assets/gen/clips/G20/G20_s1123.mp4` | 15.0 | 2026-11-23T18:14:39-05:00 |
| G20 | `assets/gen/stills/G20/G20_s1123.png` | 1124 | `assets/gen/clips/G20/G20_s1124.mp4` | 13.0 | 2026-11-23T18:14:52-05:00 |
| G21 | `assets/gen/stills/G21/G21_s1123.png` | 1123 | `assets/gen/clips/G21/G21_s1123.mp4` | 15.0 | 2026-11-23T18:15:07-05:00 |
| G21 | `assets/gen/stills/G21/G21_s1123.png` | 1124 | `assets/gen/clips/G21/G21_s1124.mp4` | 15.0 | 2026-11-23T18:15:22-05:00 |
| G22 | `assets/gen/stills/G22/G22_s1123.png` | 1123 | `assets/gen/clips/G22/G22_s1123.mp4` | 15.1 | 2026-11-23T18:15:37-05:00 |
| G22 | `assets/gen/stills/G22/G22_s1123.png` | 1124 | `assets/gen/clips/G22/G22_s1124.mp4` | 14.0 | 2026-11-23T18:15:51-05:00 |
| G23 | `assets/gen/stills/G23/G23_s1123.png` | 1123 | `assets/gen/clips/G23/G23_s1123.mp4` | 15.5 | 2026-11-23T18:16:07-05:00 |
| G23 | `assets/gen/stills/G23/G23_s1123.png` | 1124 | `assets/gen/clips/G23/G23_s1124.mp4` | 13.2 | 2026-11-23T18:16:20-05:00 |
| G24 | `assets/gen/stills/G24/G24_s1124.png` | 1123 | `assets/gen/clips/G24/G24_s1123.mp4` | 15.3 | 2026-11-23T18:16:35-05:00 |
| G24 | `assets/gen/stills/G24/G24_s1124.png` | 1124 | `assets/gen/clips/G24/G24_s1124.mp4` | 13.4 | 2026-11-23T18:16:49-05:00 |
| G25 | `assets/gen/stills/G25/G25_s1123.png` | 1123 | `assets/gen/clips/G25/G25_s1123.mp4` | 15.1 | 2026-11-23T18:17:04-05:00 |
| G25 | `assets/gen/stills/G25/G25_s1123.png` | 1124 | `assets/gen/clips/G25/G25_s1124.mp4` | 13.1 | 2026-11-23T18:17:17-05:00 |
| G26 | `assets/gen/stills/G26/G26_s1124.png` | 1123 | `assets/gen/clips/G26/G26_s1123.mp4` | 15.4 | 2026-11-23T18:17:32-05:00 |
| G26 | `assets/gen/stills/G26/G26_s1124.png` | 1124 | `assets/gen/clips/G26/G26_s1124.mp4` | 13.2 | 2026-11-23T18:17:46-05:00 |
| G27 | `assets/gen/stills/G27/G27_s1123.png` | 1123 | `assets/gen/clips/G27/G27_s1123.mp4` | 15.3 | 2026-11-23T18:18:01-05:00 |
| G27 | `assets/gen/stills/G27/G27_s1123.png` | 1124 | `assets/gen/clips/G27/G27_s1124.mp4` | 13.1 | 2026-11-23T18:18:14-05:00 |
| G28 | `assets/gen/stills/G28/G28_s1123.png` | 1123 | `assets/gen/clips/G28/G28_s1123.mp4` | 15.2 | 2026-11-23T18:18:29-05:00 |
| G28 | `assets/gen/stills/G28/G28_s1123.png` | 1124 | `assets/gen/clips/G28/G28_s1124.mp4` | 13.3 | 2026-11-23T18:18:43-05:00 |
| G29 | `assets/gen/stills/G29/G29_s1124.png` | 1123 | `assets/gen/clips/G29/G29_s1123.mp4` | 15.0 | 2026-11-23T18:18:58-05:00 |
| G29 | `assets/gen/stills/G29/G29_s1124.png` | 1124 | `assets/gen/clips/G29/G29_s1124.mp4` | 13.0 | 2026-11-23T18:19:11-05:00 |
| G30 | `assets/gen/stills/G30/G30_s1123.png` | 1123 | `assets/gen/clips/G30/G30_s1123.mp4` | 16.0 | 2026-11-23T18:19:27-05:00 |
| G30 | `assets/gen/stills/G30/G30_s1123.png` | 1124 | `assets/gen/clips/G30/G30_s1124.mp4` | 13.2 | 2026-11-23T18:19:40-05:00 |
| G31 | `assets/gen/stills/S02/S02_r_s1123.png` | 1123 | `assets/gen/clips/G31/G31_s1123.mp4` | 15.3 | 2026-11-23T18:19:55-05:00 |
| G31 | `assets/gen/stills/S02/S02_r_s1123.png` | 1124 | `assets/gen/clips/G31/G31_s1124.mp4` | 13.2 | 2026-11-23T18:20:08-05:00 |
| G32 | `assets/gen/stills/G32/G32_s1123.png` | 1123 | `assets/gen/clips/G32/G32_s1123.mp4` | 15.1 | 2026-11-23T18:20:23-05:00 |
| G32 | `assets/gen/stills/G32/G32_s1123.png` | 1124 | `assets/gen/clips/G32/G32_s1124.mp4` | 13.2 | 2026-11-23T18:20:37-05:00 |
| G34 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G34/G34_s1123.png` | 67.8 | 2026-11-23T18:22:18-05:00 |
| G34 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G34/G34_s1124.png` | 48.4 | 2026-11-23T18:23:06-05:00 |
| G35 | 1123 | 1536×656 | `assets/gen/stills/G35/G35_s1123.png` | 25.0 | 2026-11-23T18:23:31-05:00 |
| G35 | 1124 | 1536×656 | `assets/gen/stills/G35/G35_s1124.png` | 23.0 | 2026-11-23T18:23:54-05:00 |
| G16 | `assets/gen/stills/G16/G16_s1123.png` | 1123 | `assets/gen/clips/G16/G16_s1123.mp4` | 31.7 | 2026-11-23T18:24:29-05:00 |
| G16 | `assets/gen/stills/G16/G16_s1123.png` | 1124 | `assets/gen/clips/G16/G16_s1124.mp4` | 14.0 | 2026-11-23T18:24:43-05:00 |
| G05b | `assets/gen/stills/G05/G05_r_s1123.png` | 1123 | `assets/gen/clips/G05b/G05b_s1123.mp4` | 23.2 | 2026-11-23T18:25:06-05:00 |
| G05b | `assets/gen/stills/G05/G05_r_s1123.png` | 1124 | `assets/gen/clips/G05b/G05b_s1124.mp4` | 18.0 | 2026-11-23T18:25:24-05:00 |
| G34 | `assets/gen/stills/G34/G34_s1124.png` | 1123 | `assets/gen/clips/G34/G34_s1123.mp4` | 30.5 | 2026-11-23T18:26:27-05:00 |
| G34 | `assets/gen/stills/G34/G34_s1124.png` | 1124 | `assets/gen/clips/G34/G34_s1124.mp4` | 14.0 | 2026-11-23T18:26:41-05:00 |
| G35 | `assets/gen/stills/G35/G35_s1123.png` | 1123 | `assets/gen/clips/G35/G35_s1123.mp4` | 17.1 | 2026-11-23T18:26:59-05:00 |
| G35 | `assets/gen/stills/G35/G35_s1123.png` | 1124 | `assets/gen/clips/G35/G35_s1124.mp4` | 13.1 | 2026-11-23T18:27:12-05:00 |
| G36 (refs: ref_narrator) | 1123 | 1536×656 | `assets/gen/stills/G36/G36_s1123.png` | 65.7 | 2026-11-23T19:40:37-05:00 |
| G36 (refs: ref_narrator) | 1124 | 1536×656 | `assets/gen/stills/G36/G36_s1124.png` | 48.1 | 2026-11-23T19:41:25-05:00 |
| G36 (refs: ref_narrator) | 1125 | 1536×656 | `assets/gen/stills/G36/G36_s1125.png` | 48.1 | 2026-11-23T19:42:13-05:00 |
| G36 (refs: ref_narrator) | 1126 | 1536×656 | `assets/gen/stills/G36/G36_s1126.png` | 48.1 | 2026-11-23T19:43:01-05:00 |
| G36 | `assets/gen/stills/G36/G36_s1126.png` | 1123 | `assets/gen/clips/G36/G36_s1123.mp4` | 46.5 | 2026-11-23T19:44:47-05:00 |
| G36 | `assets/gen/stills/G36/G36_s1126.png` | 1124 | `assets/gen/clips/G36/G36_s1124.mp4` | 26.7 | 2026-11-23T19:45:13-05:00 |
| G36 | `assets/gen/stills/G36/G36_s1126.png` | 1125 | `assets/gen/clips/G36/G36_s1125.mp4` | 24.4 | 2026-11-23T19:45:38-05:00 |
