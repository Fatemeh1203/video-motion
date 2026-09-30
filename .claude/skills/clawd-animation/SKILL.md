---
name: clawd-animation
description: Hand-painted 2D character animation with p5.js + p5.brush (the Claude Animation Base kit by John Heibel). Use when the user wants a short cartoon, animated character scene, music-video style painted animation, or anything starring Clawd or a hand-drawn character with boiling linework and watercolour, rendered to MP4 with a headless Chrome renderer. Not for UI/text motion graphics or website promos (use /hyperframes or /remotion-best-practices).
---

# Clawd animation (Claude Animation Base)

This skill bundles the Claude Animation Base starter kit
(https://github.com/JohnHeibel/ClaudeAnimationBase, MIT). Everything lives next to this
file.

## Before drawing anything

1. Read `ANIMATION_GUIDE.md` in this folder completely. It holds the rules (handmade,
   alive, one piece, no text, transitions always), the workflow (storyboard first, build
   shot by shot, check contact sheets) and the full API for Clawd and the engine.
2. Look at the model sheets in `docs/` (`emotions.jpg`, `views.jpg`).

## Start a project

Copy the kit into a new project folder and install it there; never edit this skill folder:

```bash
mkdir -p videos/<name> && cp -r <this skill dir>/{src,docs,render.mjs,gpu_probe.mjs,studio.html,package.json,package-lock.json,ANIMATION_GUIDE.md} videos/<name>/
cd videos/<name> && npm install
```

Write the video in `src/scenes/` (the demo in `src/scenes/demo.js` is the reference),
set length and tempo in `src/config.js`.

## Render

```bash
node render.mjs --clip --out=out/video.mp4            # full MP4
```

In this cloud container there is no GPU: add `--soft-gl` so WebGL renders in software,
and point at the preinstalled Chromium with
`--chrome=/opt/pw-browsers/chromium-1194/chrome-linux/chrome`. p5.brush watercolour fills
are slow without a GPU (seconds per frame); prefer flatter fills for long pieces.
`render.mjs` also writes contact sheets, frame strips, crops and stills for checking your
own work (see `ANIMATION_GUIDE.md`).
