"""Local Persian (or any language) transcription with Whisper, no Hugging Face needed.

usage: python3 transcribe.py <audio_or_video> <out_prefix> [--lang fa] [--model turbo|small]

Writes <out_prefix>.json  {"segments":[{"start","end","text"}], "pauses":[{"start","end"}]}
       <out_prefix>.srt
Segments are speech runs between pauses (ffmpeg silencedetect), so their edges are exact
audio boundaries; long runs are split under 28 s for Whisper. Whisper drops "اِ / اَم" and
never reports pauses, so the pause list comes from the audio itself, not from the text.

`npx hyperframes transcribe` fails in this container (its model download hits huggingface.co,
which is blocked). This script fetches the sherpa-onnx Whisper export from GitHub releases:
  turbo (large-v3-turbo, ~560 MB download, best for Persian, ~1.3x real time on CPU)
  small (~360 MB, faster, much weaker Persian)
"""

import argparse
import json
import os
import re
import subprocess
import tarfile
import tempfile
import urllib.request
import wave

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("input")
ap.add_argument("out_prefix")
ap.add_argument("--lang", default="fa")
ap.add_argument("--model", default="turbo", choices=["turbo", "small", "medium", "large-v3"])
ap.add_argument("--noise", default="-38dB", help="silencedetect threshold (raise for noisy rooms)")
ap.add_argument("--min-pause", type=float, default=0.3)
args = ap.parse_args()

subprocess.run(["python3", "-m", "pip", "install", "-q", "sherpa-onnx"], check=False)
import sherpa_onnx  # noqa: E402

CACHE = os.path.expanduser("~/.cache/video-studio/asr")
mdir = os.path.join(CACHE, f"sherpa-onnx-whisper-{args.model}")
if not os.path.isdir(mdir):
    os.makedirs(CACHE, exist_ok=True)
    url = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-{args.model}.tar.bz2"
    tmp = mdir + ".tar.bz2"
    print("downloading", url)
    urllib.request.urlretrieve(url, tmp)
    with tarfile.open(tmp) as t:
        t.extractall(CACHE)
    os.remove(tmp)
    for f in os.listdir(mdir):  # keep only the int8 weights
        if f.endswith(".onnx") and ".int8." not in f:
            os.remove(os.path.join(mdir, f))
p = os.path.join(mdir, args.model + "-")
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=p + "encoder.int8.onnx", decoder=p + "decoder.int8.onnx", tokens=p + "tokens.txt",
    language=args.lang, task="transcribe", num_threads=os.cpu_count() or 4,
)

wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", args.input, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
with wave.open(wav) as w:
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
os.remove(wav)
SR, total = 16000, len(a) / 16000

err = subprocess.run(
    ["ffmpeg", "-i", args.input, "-vn", "-af", f"silencedetect=noise={args.noise}:d={args.min_pause}", "-f", "null", "-"],
    capture_output=True, text=True,
).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)] + [total]
pauses = [{"start": round(s, 3), "end": round(min(e, total), 3)} for s, e in zip(ss, se)]

runs, cur = [], 0.0
for pz in pauses:
    if pz["start"] - cur > 0.12:
        runs.append([cur, pz["start"]])
    cur = pz["end"]
if total - cur > 0.12:
    runs.append([cur, total])
chunks = []
for s, e in runs:  # Whisper window is 30 s
    while e - s > 28:
        chunks.append([s, s + 25])
        s += 25
    chunks.append([s, e])

segs = []
for s, e in chunks:
    st = rec.create_stream()
    st.accept_waveform(SR, a[int(max(0, s - 0.1) * SR): int(min(total, e + 0.1) * SR)])
    rec.decode_stream(st)
    text = st.result.text.strip()
    segs.append({"start": round(s, 3), "end": round(e, 3), "text": text})
    print(f"{s:8.2f} {e:8.2f}  {text}", flush=True)

json.dump({"segments": segs, "pauses": pauses, "duration": round(total, 3)},
          open(args.out_prefix + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def ts(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


with open(args.out_prefix + ".srt", "w", encoding="utf-8") as f:
    for i, sg in enumerate([s for s in segs if s["text"]], 1):
        f.write(f"{i}\n{ts(sg['start'])} --> {ts(sg['end'])}\n{sg['text']}\n\n")
print("wrote", args.out_prefix + ".json", args.out_prefix + ".srt")
