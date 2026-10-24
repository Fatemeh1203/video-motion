"""Synthesize a bright, light music bed for a school video (deterministic, royalty-free).

Marimba-like melody + soft piano chords + round bass + shaker and a light kick,
112 BPM, C major (C - Am - F - G). Two bars of chords only, then the full groove;
the last bars thin out so the outro can breathe.

Usage: python3 scripts/make-school-music.py assets/audio/bgm.wav [duration_s]
"""

import sys
import wave

import numpy as np

SR = 44100
BPM = 112
BEAT = 60 / BPM
BAR = BEAT * 4
OUT = sys.argv[1] if len(sys.argv) > 1 else "bgm.wav"
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0
N = int(SR * DUR)
rng = np.random.default_rng(11)
L = np.zeros(N)
R = np.zeros(N)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def place(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    L[i : i + len(sig)] += sig * (1 - pan) * 0.5 * 2 ** 0.5
    R[i : i + len(sig)] += sig * (1 + pan) * 0.5 * 2 ** 0.5


def marimba(midi, dur=0.6):
    t = np.arange(int(SR * dur)) / SR
    f = hz(midi)
    env = np.exp(-t * 9)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)
    return s * env * np.minimum(1, t * 400)


def piano(midis, dur):
    t = np.arange(int(SR * dur)) / SR
    out = np.zeros_like(t)
    for m in midis:
        f = hz(m)
        for k, a in ((1, 1.0), (2, 0.4), (3, 0.18), (4, 0.08)):
            out += a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.6 + k * 0.9))
    return out * np.minimum(1, t * 200) / len(midis)


def bass(midi, dur):
    t = np.arange(int(SR * dur)) / SR
    f = hz(midi)
    s = np.sin(2 * np.pi * f * t) + 0.2 * np.sin(2 * np.pi * f * 2 * t)
    return s * np.exp(-t * 2.5) * np.minimum(1, t * 150)


def kick():
    t = np.arange(int(SR * 0.25)) / SR
    f = 110 * np.exp(-t * 25) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 18)


def shaker():
    n = int(SR * 0.07)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    noise = np.diff(noise, prepend=0)  # tilt toward highs
    return noise * np.exp(-t * 60) * 0.5


# C - Am - F - G (one bar each)
CHORDS = [(60, 64, 67), (57, 60, 64), (53, 57, 60), (55, 59, 62)]
ROOTS = [36, 33, 29, 31]
# marimba line per bar, in eighth notes (None = rest)
MELODY = [
    [72, None, 76, 79, 77, 76, 74, None],
    [72, None, 76, 72, 69, None, 72, None],
    [69, None, 72, 77, 76, 74, 72, None],
    [71, None, 74, 79, 77, None, 74, None],
]

bars = int(DUR / BAR) + 1
for b in range(bars):
    t0 = b * BAR
    c = b % 4
    last = t0 > DUR - 2 * BAR
    place(piano(CHORDS[c], BAR * 1.1), t0, pan=-0.15, gain=0.55)
    if b >= 1:
        for beat in (0, 2.5):
            place(bass(ROOTS[c], BEAT * 1.5), t0 + beat * BEAT, gain=0.5)
    if b >= 2 and not last:
        for i, m in enumerate(MELODY[c]):
            if m is not None:
                place(marimba(m), t0 + i * BEAT / 2, pan=0.25, gain=0.32)
        for beat in (0, 2):
            place(kick(), t0 + beat * BEAT, gain=0.35)
        for i in range(8):
            place(shaker(), t0 + i * BEAT / 2 + 0.01, pan=0.35, gain=0.18 if i % 2 else 0.1)

# gentle room: two short feedback echoes
for d, g in ((0.11, 0.18), (0.23, 0.1)):
    k = int(d * SR)
    L[k:] += R[:-k] * g
    R[k:] += L[:-k] * g

mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.8
pcm = (mix * 32767).astype(np.int16)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"wrote {OUT} ({DUR:.1f}s)")
