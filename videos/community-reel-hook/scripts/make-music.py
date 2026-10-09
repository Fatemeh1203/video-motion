"""120 BPM loopable electronic track for the 20 s hook Reel (royalty-free, synthesized).

usage: python3 make-music.py out.wav

Bar = 2 s, beat = 0.5 s. Sections follow the edit:
  0.0-1.5  chaos: full drums, bass, busy 16th arp (hit on 0)
  1.5-3.0  the knot: everything stops; reverse swell + riser sucks into 3.0
  3.0-9.0  answer + tool cuts: groove, claps, pluck stabs on every cut
  9.0-13.0 drop: supersaw chords, lead hook, 16th hats (four features)
  13.0-15.0 breakdown: pad + soft arp only ("you're not alone")
  15.0-19.5 CTA: groove back, hook an octave down, snare roll into 19.5
  19.5-20.0 back to the chaos texture so the Reel loops without a seam (no fade)
Progression Am - F - C - G, one chord per bar.
"""
import sys
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR, DUR, BEAT = 44100, 20.0, 0.5
N = int(SR * DUR)
rng = np.random.default_rng(11)
L = np.zeros(N)
R = np.zeros(N)
CHORDS = [[57, 60, 64], [53, 57, 60], [55, 60, 64], [55, 59, 62]]
ROOTS = [45, 41, 48, 43]


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def saw(f, n, det=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    f *= 1 + det
    k = 1
    while k * f < SR / 2.2 and k <= 40:
        out += np.sin(2 * np.pi * k * f * t + rng.uniform(0, 6) * (k == 1)) / k
        k += 1
    return out * 0.6


def env(n, a=0.005, d=0.1, s=0.7, r=0.05):
    e = np.ones(n) * s
    na, nd, nr = max(1, int(a * SR)), int(d * SR), int(r * SR)
    e[:min(na, n)] = np.linspace(0, 1, min(na, n))
    if na + nd < n:
        e[na:na + nd] = np.linspace(1, s, nd)
    if nr < n:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def lp(x, fc):
    return sosfilt(butter(2, min(fc, SR / 2.1), "low", fs=SR, output="sos"), x)


def hp(x, fc):
    return sosfilt(butter(2, fc, "high", fs=SR, output="sos"), x)


def add(sig, t0, g=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or t0 < 0:
        return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * g * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * g * (1 + min(0, pan))


def on(t, *spans):
    return any(a <= t < b for a, b in spans)


DRUMS = ((0, 1.5), (3.0, 13.0), (15.0, 20.0))
# ---- kick + sidechain
kn = int(0.35 * SR)
kt = np.arange(kn) / SR
KICK = np.sin(2 * np.pi * np.cumsum(45 + 95 * np.exp(-kt * 32)) / SR) * np.exp(-kt * 7.5)
KICK[:200] += rng.normal(0, 0.4, 200) * np.linspace(1, 0, 200)
duck = np.ones(N)
kicks = [b * BEAT for b in range(40) if on(b * BEAT, *DRUMS)]
for t in kicks:
    add(KICK, t, 0.95)
    i = int(t * SR)
    seg = 1 - 0.6 * np.exp(-np.linspace(0, 5, int(0.3 * SR)))
    duck[i:i + len(seg)] = np.minimum(duck[i:i + len(seg)], seg[: len(duck[i:i + len(seg)])])

# ---- pad (whole track) with time-varying cutoff
pad = np.zeros(N)
for bar in range(10):
    n = int(2.15 * SR)
    s = sum(saw(midi(m), n, d) for m in CHORDS[bar % 4] + [CHORDS[bar % 4][0] + 12] for d in (-0.006, 0.0, 0.007))
    s *= env(n, 0.03, 0.3, 0.8, 0.3)
    i = int(bar * 2.0 * SR)
    pad[i:i + n] += s[: N - i]
cut = np.interp(np.arange(N) / SR, [0, 1.5, 3.0, 9.0, 13.0, 15.0, 19.5, 20], [2600, 600, 2200, 4200, 1500, 3000, 3200, 2600])
blk = int(0.02 * SR)
padf = np.zeros(N)
for i in range(0, N, blk):
    padf[i:i + blk] = sosfilt(butter(2, cut[i], "low", fs=SR, output="sos"), pad[max(0, i - 2048):i + blk])[-len(pad[i:i + blk]):]
padg = np.interp(np.arange(N) / SR, [0, 1.5, 2.9, 3.0, 9.0, 13.0, 15.0, 20], [0.11, 0.05, 0.12, 0.12, 0.16, 0.14, 0.12, 0.11])
L += padf * padg * duck
R += padf * padg * duck

# ---- arp 16ths (chaos busy at start/end, soft in breakdown, off in drop)
for i in range(80):
    t = i * BEAT / 2
    if on(t, (1.5, 3.0), (9.0, 13.0)):
        continue
    ch = CHORDS[int(t // 2) % 4]
    pat = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[2] + 12]
    n = int(0.15 * SR)
    f = midi(pat[i % 8])
    s = (np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR)) * 0.4 + saw(f, n) * 0.6) * env(n, 0.002, 0.08, 0.0, 0.02)
    g = 0.12 if on(t, (0, 1.5), (19.5, 20)) else (0.07 if on(t, (13, 15)) else 0.09)
    add(lp(s, 3200 if on(t, (0, 1.5), (19.5, 20)) else 2400), t, g, pan=0.35 if i % 2 else -0.35)

# ---- bass offbeat 8ths
for i in range(40):
    t = i * BEAT + BEAT / 2
    if not on(t, (0, 1.5), (3.0, 13.0), (15.0, 20.0)):
        continue
    root = ROOTS[int(t // 2) % 4]
    n = int(0.22 * SR)
    s = lp(saw(midi(root), n) + 0.5 * np.sin(2 * np.pi * midi(root - 12) * np.arange(n) / SR), 900) * env(n, 0.004, 0.12, 0.55, 0.04)
    add(s, t, 0.42 if on(t, (9, 13)) else 0.36)

# ---- clap + roll
cn = int(0.22 * SR)
CLAP = hp(lp(rng.normal(0, 1, cn), 6000), 900) * np.exp(-np.arange(cn) / SR * 22)
for i in range(40):
    t = i * BEAT
    if i % 2 == 1 and on(t, (0, 1.5), (3.0, 13.0), (15.0, 19.0), (19.5, 20)):
        add(CLAP, t, 0.3)
for k in range(8):
    add(CLAP[: int(0.1 * SR)], 19.0 + k * 0.0625, 0.08 + 0.22 * k / 7)

# ---- hats
hn = int(0.05 * SR)
HAT = hp(rng.normal(0, 1, hn), 7000) * np.exp(-np.arange(hn) / SR * 70)
for i in range(80):
    t = i * BEAT / 2
    if not on(t, *DRUMS):
        continue
    off = i % 2 == 1
    if on(t, (0, 1.5), (9, 13), (19.5, 20)):
        add(HAT, t, 0.1 if off else 0.065, pan=0.2)
    elif off:
        add(HAT, t, 0.09, pan=0.2)

# ---- the knot (1.5-3.0): reverse swell + riser into the 3.0 hit
def riser(d, top=9000):
    n = int(d * SR)
    s = rng.normal(0, 1, n)
    out = np.zeros(n)
    for j in range(0, n, 2048):
        out[j:j + 2048] = hp(lp(s[j:j + 2048], 400 + top * (j / n) ** 2), 200)
    return out * (np.arange(n) / n) ** 2


add(riser(1.45), 1.55, 0.18)
sw = np.zeros(int(1.4 * SR))
for m in CHORDS[0] + [69]:
    sw += saw(midi(m), len(sw))
add(lp(sw, 1800) * (np.linspace(0, 1, len(sw)) ** 3) * 0.12, 1.6)


def impact(g=1.0):
    n = int(1.4 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 10)) * t) * np.exp(-t * 3.2) * 0.9
    return (s + lp(rng.normal(0, 1, n), 2500) * np.exp(-t * 6) * 0.25) * g


for t, g in ((0.0, 0.35), (3.0, 0.55), (9.0, 0.5), (15.0, 0.45)):
    add(impact(), t, g)

# ---- pluck stabs on each tool cut (4.5, 5.25, ... 8.25)
for k in range(6):
    t = 4.5 + k * 0.75
    ch = CHORDS[int(t // 2) % 4]
    n = int(0.3 * SR)
    s = sum(saw(midi(m + 12), n) for m in ch) * env(n, 0.002, 0.18, 0.0, 0.05)
    add(lp(s, 3500), t, 0.07)

# ---- lead hook (drop 9-13, CTA 15-19 an octave down)
HOOK = [(0, 76, 1), (2, 81, 1), (3, 79, 1), (4, 76, 1), (6, 74, 1), (7, 76, 1), (8, 72, 2), (11, 69, 1), (12, 72, 1), (13, 74, 1), (14, 76, 2)]
for start, gain, tr in ((9.0, 0.16, 0), (11.0, 0.16, 0), (15.0, 0.1, -12), (17.0, 0.1, -12)):
    for off, m, ln in HOOK:
        t0 = start + off * BEAT / 2
        n = int((ln * BEAT / 2 + 0.12) * SR)
        tt = np.arange(n) / SR
        f = midi(m + tr) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * tt) * np.clip(tt * 4, 0, 1))
        ph = 2 * np.pi * np.cumsum(f) / SR
        s = sum(np.sin(ph * k) / k for k in range(1, 20))
        s = lp(s * 0.4, 3800) * env(n, 0.008, 0.15, 0.7, 0.08)
        add(s, t0, gain, -0.1)
        add(s, t0 + 0.375, gain * 0.3, 0.6)

# ---- reverb + master (no fade: the Reel loops)
irn = int(1.5 * SR)
ir = lp(rng.normal(0, 1, irn) * np.exp(-np.arange(irn) / SR * 3.4), 5000) * 0.02


def conv(x):
    m = len(x) + irn
    nf = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(ir, nf), nf)[: len(x)]


mix = np.stack([L + conv(L) * 0.45, R + conv(R) * 0.45], 1)
mix[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))[:, None]
mix /= np.max(np.abs(mix)) + 1e-9
mix = np.tanh(mix * 1.4) / np.tanh(1.4) * 0.89
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("wrote", sys.argv[1])
