# Persian narration

The user cares most about **correct pronunciation and natural tone**. You cannot listen to
audio, so never claim a voice sounds right; ask her to listen and name the line to fix.

## What works in this container

| Route | Status | Quality |
|---|---|---|
| Her own recording | always works | best |
| Azure Speech REST + SSML, `fa-IR-DilaraNeural` (female) / `fa-IR-FaridNeural` (male) | needs her key + region, and `<region>.tts.speech.microsoft.com` allowed in the environment's network settings | very good; controllable |
| edge-tts (`speech.platform.bing.com`) | **fails**: the WebSocket handshake gets 403 through the proxy even when the host is allowed | — |
| HuggingFace models (Piper voices) | blocked (huggingface.co 403) | — |
| sherpa-onnx models from GitHub releases | works (`scripts/tts_offline.py`) | low; female only `vits-mimic3-fa-haaniye_low` (median F0 ≈ 220 Hz); `fa_IR-gyro/amir/ganji/reza_ibrahim` are male |
| HeyGen (`/media-use` default) | needs `heygen auth login`, impossible here | — |
| Kokoro (`/media-use` offline) | no Persian | — |

## Workflow

1. Write the script with `anthropic-skills:human-tone` (Persian section): short sentences,
   one idea per line, first person as Fatemeh. Save `SCRIPT.md` (table: time, scene, text).
2. Make `voice/lines.tsv`: `start_seconds<TAB>text`, one line per on-screen beat; start
   each line when its text appears.
3. Synthesize:
   - Azure: `AZURE_SPEECH_KEY=… AZURE_SPEECH_REGION=… python3 scripts/tts_azure.py voice/lines.tsv voice/`
   - Offline: `python3 scripts/tts_offline.py voice/lines.tsv voice/`
   Both fit each line into the gap before the next start by raising the rate a little
   (cap about 1.3× so it doesn't sound rushed; shorten the text instead).
4. `python3 scripts/mix_narration.py voice/lines.tsv voice/ assets/audio/narration.wav <total_seconds>`:
   places the clips, applies high-pass, presence EQ, compression, a touch of room and
   loudness normalisation to −16 LUFS.
5. Add `<audio id="narration" src="assets/audio/narration.wav" data-start="0" data-duration="<total>" data-volume="1">`,
   lower the music to ~0.4, then carve:
   `npm i -D @hyperframes/core && node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed bgm --voice narration`.

## Pronunciation control

- Azure: SSML `<phoneme>`, `<sub alias="…">`, `<prosody rate pitch>`, `<break time>`,
  `<emphasis>`. Put ezafe explicitly (e.g. «کامیونیتیِ هوش مصنوعی») and use `<sub>` for
  Latin names («چت‌جی‌پی‌تی» for ChatGPT).
- Offline: add the diacritics yourself (ـِ for ezafe, ـَ ـُ where ambiguous), write Latin
  names in Persian letters, avoid «؛» (unknown phoneme), keep sentences short.

## Her own recording

Tell her in simple steps: quiet room, phone close, read each line of `SCRIPT.md` with a
short pause, send the file. Then: `ffmpeg -af "highpass=f=80,afftdn,acompressor,loudnorm=I=-16"`,
cut lines on silences (`silencedetect`), place with `mix_narration.py`, carve the music.
