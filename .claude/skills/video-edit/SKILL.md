---
name: video-edit
description: Edit Fatemeh's own recorded footage (talking head, lesson, screen recording, Reels) end to end — transcribe Persian locally, remove fillers/long pauses/coughs/repeated takes, storyboard, add motion graphics + captions + SFX with HyperFrames, review frames, and deliver either a finished MP4 or a Premiere-editable package (FCP7 XML + transparent ProRes 4444 overlays + SRT). Use on «این ویدیو رو ادیت کن», «مکث‌ها رو بگیر», «زیرنویس بذار», «برای پریمیر», or /video-edit. For brand-new motion videos without footage use /video-studio.
---

# Video edit (footage in, edited video out)

Five stages, always in this order: **transcribe → clean → storyboard → build → review**.
The two tables in the middle (cut table, storyboard) are where the user directs; show them
when step approval is on. Scripts live in `.claude/skills/video-studio/scripts/`. Talk to her in Persian. Brand, fonts and invite: `/video-studio`
(`references/brand.md`). Engine for graphics: HyperFrames (`/hyperframes` → `/talking-head-recut`
for overlays on a speaker, `/embedded-captions` for captions, `/media-use` for SFX/logos).

## 0. Settings (fill from her message; ask only for what is missing)

```
file:            <absolute path; never modify it, work on copies>
type:            lesson / vertical short / product intro / ...
output:          mp4 | premiere
aspect:          16:9 | 9:16
language:        fa
style:           e.g. minimal & very clean, site palette (navy, teal, violet)
feel:            e.g. calm, trustworthy, energetic
goal:            after watching, the viewer should be able to ...
brand:           palette from brand.md, Vazirmatn, logo/QR from video-studio assets
face zone:       center / right / left  → a no-go area for every graphic
assets folder:   <b-roll, logos, sfx, music>
moments:         when I say «X» → what appears, from where, how
freedom:         only these moments | free but uncluttered
filler words:    خب، عه، اِم، یعنی، ببین
step approval:   on (default for the first videos) | off (with /goal)
```

## 1. Fixed rules

- Only local, free tools: HyperFrames, ffmpeg, local Whisper, files in her folder. Skip any
  feature that needs a paid account (media-use catalog, HeyGen cloud) and use the free fallback.
- Never cover her face. Never change the meaning of a sentence with a cut.
- Ambiguous setting → ask before starting, never guess mid-way.

## 2. Transcribe

`python3 .claude/skills/video-studio/scripts/transcribe.py <file> work/transcript`
(Whisper large-v3-turbo via sherpa-onnx from GitHub; `npx hyperframes transcribe` cannot
download its model here). Output: segments between real pauses + a pause list from
`silencedetect`. Whisper drops «عه» and pauses, so trust the audio gaps, not only the text.
Persian ASR is imperfect: correct English tool names by hand and show her the transcript.

## 3. Clean (cut table)

Find and cut:
- filler words from the settings when said out of hesitation (a «خب» that opens a sentence stays);
- silences > 0.7 s → shorten to ~0.3 s (never to zero);
- coughs, throat clears, sips, sudden noises;
- repeated takes → keep the best one: complete > fluent > correct > energetic; tie → the last.

Cut only between words, 20–40 ms audio fades at each cut, every other jump cut punched in
(100 → 108 %). Output table: `start | end | type | removed text | reason`.
`cut_video.py <file> <keep.json|transcript.json> out.mp4 --clean-voice` applies it
(RNNoise + EQ + compression + loudness, punch-ins, click-free fades).

## 4. Storyboard

Table: `time (final timeline) | sentence | what appears | from where / motion | sfx`.
Defaults: tool/company name → its official logo; key number → big number; command/code →
typed on screen; every element must help understanding. Glass card or dark plate behind any
text over footage. Persian text right-aligned, Vazirmatn, word-by-word animation (never split
letters), inside the safe area.

## 5. Build

- **mp4**: HyperFrames project in `videos/<name>/`, the cleaned clip as the base `<video muted>`
  + its audio as `<audio>`, overlays as sub-compositions, captions via `/embedded-captions`,
  music carved under the voice (`/hyperframes-audio`), final loudness −14 LUFS.
- **premiere**: do not render the full video. Render each graphic alone with
  `npx hyperframes render --format mov` (ProRes 4444 with alpha; test one clip for real
  transparency first), then `cuts_to_xmeml.py plan.json edit.xml` →
  V1/A1 kept pieces linked to the original, V2 overlays, A2 sfx, markers for b-roll she
  must add; SRT timed to the final (post-cut) timeline. Read fps/size/sample rate with
  ffprobe and keep every time in whole frames (frame-rate mismatch is the #1 desync).
  Use `path_map` so paths point at her own folder, and write a README: what to import,
  in which order, how to relink offline media.

## 6. Review before delivery (max 5 rounds)

Snapshot every element entrance/exit and every 5 s (`npx hyperframes snapshot --at ...`), look
at each frame: face uncovered, text readable/complete/correct Persian/right-aligned, nothing
off-frame or overlapping, each animation ≤ 0.2 s from its word. Audio: no filler, cough or long
silence left, no clicks at cuts, music never over the voice. Premiere route: sum of XML pieces
= source − cuts, random spot checks against the cut table, all referenced files exist, overlay
alpha verified. Fix, re-render, re-check. If something still fails after 5 rounds, say exactly what.

## 7. Deliver

MP4 (repo copy crf 19 < 100 MB, preview crf 26 < 30 MB via SendUserFile) or the Premiere
package; the cut table and storyboard; a short Persian report: how much time was cut, what was
added on your own initiative, what is still imperfect. Add any feedback she repeats twice to
this skill.

**Done (for /goal)** when the final file is rendered, every stage-6 check passes for all frames
and audio, and the delivery report is written in the chat.
