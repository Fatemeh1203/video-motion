# Pitfalls seen in this container (HyperFrames)

| Symptom | Cause | Fix |
|---|---|---|
| Snapshot shows only static layout, no text | GSAP from CDN fails (proxy), `gsap is not defined` | Copy `assets/vendor/gsap.min.js` into the project, `<script src="assets/vendor/gsap.min.js">` |
| Lint `html_dir_attribute_breaks_render` | `<html dir="rtl">` | Remove; set `direction: rtl` on text blocks |
| Lint `invalid_parent_traversal_in_asset_path` | `../assets/...` inside `compositions/` | Use root-relative `assets/...` |
| Lint `font_family_without_font_face` | Sub-composition lacks @font-face | `/*FONTS*/` marker + `python3 scripts/inject-fonts.py compositions/*.html` |
| Broken cursive in animations | Letter-split Persian | Animate words (`<span>` per word), never letters |
| Scene transition is a dip to dark, contrast check fails at seams | Opaque background on sub-comp root | Remove root background; keep it on `#root` in index |
| Render: `VIDEO_SOURCE_UNRENDERABLE`, "sparse keyframes" | MP4 copied mid-encode / long GOP | Re-encode `-g 30 -keyint_min 30 -movflags +faststart`; copy only after ffmpeg exits |
| `git push` rejected | File > 100 MB | Re-encode the repo copy at `-crf 19` |
| SendUserFile refused | File > 30 MB | Send a `-crf 26` preview |
| Text overlaps flagged on fanned cards | Intentional overlap | `data-layout-allow-overlap` on the text elements |
| Decorative ghost text flagged | Intentional | `data-layout-allow-overflow data-layout-allow-occlusion data-layout-allow-overlap` |
| Nested `<video data-start>` warning | Ambiguous start basis | `data-hf-media-start-basis="local"` |
| Chromium phone-home 403s in proxy log | Harmless | Ignore |

Doctor checklist for a fresh container:

```bash
apt-get install -y ffmpeg || (apt-get update && apt-get install -y ffmpeg)
npx hyperframes browser ensure
pip install numpy pillow qrcode   # make-bgm, grain, QR
```

Render speed: about 3 frames/s at 1080p with software GL (~15–20 min for 2 minutes). Run
renders in the background and wait on the log for `EXIT`.
