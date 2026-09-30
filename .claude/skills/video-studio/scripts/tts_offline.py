"""Offline Persian narration with sherpa-onnx (female voice "haaniye", low quality).

usage: python3 tts_offline.py <lines.tsv> <out_dir> [total_seconds] [voice]

lines.tsv: one line per beat, "start_seconds<TAB>text". Each line is synthesized to
<out_dir>/lNN.wav and sped up slightly (up to MAX_SPEED) so it ends before the next line
starts; lines that still don't fit are reported so the text can be shortened.

voice: vits-mimic3-fa-haaniye_low (female, default) or a male piper voice such as
vits-piper-fa_IR-gyro-medium. Models download from the sherpa-onnx GitHub release
(huggingface.co is blocked in this environment).
"""

import os
import subprocess
import sys
import tarfile
import urllib.request
import wave

import numpy as np

TSV, OUT = sys.argv[1], sys.argv[2]
TOTAL = float(sys.argv[3]) if len(sys.argv) > 3 else None
VOICE = sys.argv[4] if len(sys.argv) > 4 else "vits-mimic3-fa-haaniye_low"
CACHE = os.path.expanduser("~/.cache/video-studio/tts")
MAX_SPEED = 1.3
GAP = 0.15

os.makedirs(CACHE, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "sherpa-onnx"], check=False)
import sherpa_onnx  # noqa: E402

mdir = os.path.join(CACHE, VOICE)
if not os.path.isdir(mdir):
    url = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/{VOICE}.tar.bz2"
    tmp = mdir + ".tar.bz2"
    print("downloading", url)
    urllib.request.urlretrieve(url, tmp)
    with tarfile.open(tmp) as t:
        t.extractall(CACHE)
    os.remove(tmp)
onnx = [f for f in os.listdir(mdir) if f.endswith(".onnx")][0]
tts = sherpa_onnx.OfflineTts(
    sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=os.path.join(mdir, onnx),
                tokens=os.path.join(mdir, "tokens.txt"),
                data_dir=os.path.join(mdir, "espeak-ng-data"),
            ),
            num_threads=4,
        )
    )
)

lines = [l.rstrip("\n").split("\t", 1) for l in open(TSV, encoding="utf-8") if l.strip()]
starts = [float(s) for s, _ in lines]


def synth(text, speed, path):
    a = tts.generate(text.replace("؛", "،"), sid=0, speed=speed)
    s = np.clip(np.array(a.samples, dtype=np.float32), -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(a.sample_rate)
        w.writeframes((s * 32767).astype(np.int16).tobytes())
    return len(s) / a.sample_rate


for i, (st, text) in enumerate(lines):
    nxt = starts[i + 1] if i + 1 < len(starts) else (TOTAL or starts[i] + 30)
    room = nxt - float(st) - GAP
    path = os.path.join(OUT, f"l{i:02d}.wav")
    speed = 1.05
    dur = synth(text, speed, path)
    while dur > room and speed < MAX_SPEED:
        speed = min(MAX_SPEED, round(speed * dur / room + 0.02, 3))
        dur = synth(text, speed, path)
    flag = "OK" if dur <= room else "TOO LONG: shorten the text or move the next start"
    print(f"{i:02d} @{float(st):6.1f}s  {dur:5.2f}s / room {room:5.2f}s  speed {speed}  {flag}")
