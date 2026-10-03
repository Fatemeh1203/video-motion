---
name: video-studio
description: Fatemeh Shams's one-stop video skill. Use for ANY request from this user to make, edit, voice, re-render or send a video, motion graphic, promo, reel, explainer or animation — especially about her Telegram AI community (AI_Community), her site (project-site-2026, "THE INTELLIGENCE SPACE"), her lessons, handouts or simulators. Picks the right engine (HyperFrames, Remotion or Clawd animation), applies her brand (Persian RTL, Vazirmatn, site palette, QR + Telegram invite), adds Persian narration, and delivers an MP4 under 2 minutes. Triggers on /video-studio and on Persian requests like «ویدیو بساز»، «موشن»، «تیزر»، «ریلز»، «صدا بذار»، «گوینده».
---

# Video Studio (فاطمه شمس)

One entry point for every video this user asks for. It does not replace the engine skills;
it chooses one, loads it, and adds everything that is always true for this user.

Talk to the user in **Persian**, precise and natural (load `anthropic-skills:human-tone`
for any on-screen or narration copy). She prefers short, concrete updates and step-by-step
explanations when she has to do something herself.

## 1. Pick the engine (one per video)

| Request | Engine | Load |
|---|---|---|
| Promo / explainer / community or site video, text-heavy, Persian copy (default) | HyperFrames | `/hyperframes` → it routes to `/general-video`, `/product-launch-video`, `/motion-graphics`, … |
| User says «با Remotion» / wants React code | Remotion | `/remotion-best-practices` (+ `/remotion-motion-graphics` craft rules) |
| Cartoon / character story / hand-painted, no on-screen text | Clawd | `/clawd-animation` |
| Captions on her own talking-head footage | HyperFrames | `/embedded-captions` |
| Graphics over her own interview/podcast footage | HyperFrames | `/talking-head-recut` |

Always follow the chosen engine's own workflow (brief → plan → build → check → render).
New projects go under `videos/<kebab-name>/` in the video-motion repo. For HyperFrames,
right after `hyperframes init`, copy this skill's `assets/fonts`, `assets/vendor` and
`assets/telegram-qr.svg` into the project's `assets/`, and `scripts/*.py` into its
`scripts/`. The closest finished template is `videos/fatemeh-community`.
Domain skills (`/media-use`, `/hyperframes-audio`, `/hyperframes-animation`, …) are pulled
in by that workflow; name them only when a step needs them.

## 2. Defaults (confirmed by the user earlier; do not re-ask)

- Language: Persian, RTL. Length: **≤ 2 minutes** («۲ دقیقه باشد نه بیشتر»). Aspect: 16:9
  unless she names Instagram/Reels (then 9:16).
- Title on screen: «فاطمه شمس» + «توسعه‌دهنده و مربی هوش مصنوعی».
- Every promo ends on the invite: QR (`assets/telegram-qr.svg`) + `t.me/+Orw2hE3tq3thMzNk`.
- Only ask what is genuinely missing (usually: topic/angle, and whether a voice is wanted).

Brand, palette, fonts and community facts: **read `references/brand.md` before designing.**

## 3. Build rules that were learned the hard way (this container)

Read `references/pitfalls.md` before the first render. The critical ones:

- Vendor GSAP locally (`assets/vendor/gsap.min.js`); the CDN is unreachable from headless Chrome and the timeline silently never runs.
- Never put `dir="rtl"` on `<html>` (renders a black video). Put `direction: rtl` on text containers.
- Never split Persian words into letters (breaks joining); animate word by word.
- Embed Vazirmatn with local `@font-face` in every sub-composition (`scripts/inject-fonts.py` replaces a `/*FONTS*/` marker).
- Sub-composition roots transparent (no background) so scene crossfades really cross.
- Install ffmpeg (`apt-get install -y ffmpeg`) and `npx hyperframes browser ensure` in a fresh container.

## 4. Narration (Persian voice)

Pronunciation and tone matter a lot to this user. Read `references/persian-voice.md`. Order of preference:

1. **Her own recording** (best). Script it with `SCRIPT.md`, clean + level it, place each line on its scene.
   Worked example: `videos/fatemeh-community/scripts/recording/` (Whisper-small ONNX from the
   sherpa-onnx GitHub release to find each line, RNNoise `arnndn` + EQ/compressor to remove room
   noise, long pauses trimmed, then the scenes are retimed to her voice instead of speeding her up).
2. **Azure Speech (fa-IR-DilaraNeural, female) via REST + SSML** when she provides a key/region
   and the host `<region>.tts.speech.microsoft.com` is allowed: `scripts/tts_azure.py`.
   SSML gives per-word pronunciation, rate, pitch and pauses.
3. **Offline fallback** `scripts/tts_offline.py` (sherpa-onnx, female voice "haaniye", low
   quality). Tell her honestly it may sound robotic.

Then `scripts/mix_narration.py` builds one timed track from `voice/lines.tsv`, add it as
`<audio id="narration">`, and carve the music under it with `/hyperframes-audio`
(`scripts/carve.mjs --bed bgm --voice narration`). You cannot hear audio: never claim the
pronunciation is correct; ask her to listen and name any line to fix.

## 5. Music and sound

`scripts/make-bgm.py out.wav <seconds>` synthesizes a royalty-free ambient bed (96 BPM).
SFX come from `/media-use`'s bundled library (whoosh, pop, typing, chime, notification,
impact, riser, sparkle).

## 6. Real site footage

To show the live site (3D portal ring and section worlds), follow
`references/site-capture.md`: run project-site-2026 locally, then
`scripts/capture-site.cjs` records WebGL frame-by-frame with a virtual clock. Seed data
(sample projects/agents/files) is placeholder: record those pages in `clean` mode.

## 7. Deliver

1. `npx hyperframes check` must pass (0 errors, contrast AA) and inspect a contact sheet
   of scene midpoints before rendering.
2. Render `--quality delivery`, then encode:
   - repo copy: `-crf 19` (must stay < 100 MB for GitHub),
   - preview to send: `-crf 26`, `aac 160k` (must stay < 30 MB for SendUserFile).
   Wait until ffmpeg has finished before committing or sending.
3. Send the preview with SendUserFile, commit + push project and repo copy, and summarise
   in Persian: what is in each scene, what was inferred, and what she should check.

Never invent facts about her, her community or her site. If a detail is not in
`references/brand.md`, the repos, or her messages, ask or leave it out.
