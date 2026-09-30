"""Place narration clips on a timeline and polish them into one track.

usage: python3 mix_narration.py <lines.tsv> <clips_dir> <out.wav> <total_seconds>

Reads start times from lines.tsv and clips lNN.wav from clips_dir (any sample rate, mono),
places each at its start, then applies high-pass, presence EQ, gentle compression, a
little room and loudness normalisation to -16 LUFS (stereo 44.1 kHz).
"""

import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

TSV, CLIPS, OUT, TOTAL = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
lines = [l.rstrip("\n").split("\t", 1) for l in open(TSV, encoding="utf-8") if l.strip()]

SR = None
track = None
for i, (st, _) in enumerate(lines):
    p = os.path.join(CLIPS, f"l{i:02d}.wav")
    with wave.open(p) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32767
    if SR is None:
        SR = sr
        track = np.zeros(int(SR * TOTAL), dtype=np.float32)
    if sr != SR:
        a = np.interp(np.linspace(0, len(a), int(len(a) * SR / sr), endpoint=False), np.arange(len(a)), a)
    s = int(float(st) * SR)
    end = min(len(track), s + len(a))
    track[s:end] += a[: end - s]

raw = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
with wave.open(raw, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(track, -1, 1) * 32767).astype(np.int16).tobytes())

chain = (
    "highpass=f=90,lowpass=f=11000,equalizer=f=250:t=q:w=1:g=-2,"
    "equalizer=f=3200:t=q:w=1.2:g=3,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
    "aecho=0.8:0.5:35:0.12,loudnorm=I=-16:TP=-1.5:LRA=9"
)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", chain, "-ar", "44100", "-ac", "2", OUT], check=True)
os.remove(raw)
print("wrote", OUT)
