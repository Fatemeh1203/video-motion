"""Energetic 120 BPM electronic track for the community group video (40 s, royalty-free, synthesized).

usage: python3 make-music.py out.wav

Bar = 2 s. Sections line up with the scenes:
  0-4   intro: pad + filtered arp opening, riser into 4.0
  4-8   kick + bass enter (hit on 4.0)
  8-16  groove + clap (daily lessons on every AI tool)
  16-24 breakdown: no kick, pad + arp (the "you're not alone" lines), snare roll + riser into 24
  24-32 drop: supersaw chords, 16th hats, lead hook
  32-40 outro: hit on 32, hook over pad, drums out at 38, final chord rings to 40
Progression Am - F - C - G (vi-IV-I-V), one chord per bar.
"""

import sys
import wave

import numpy as np
from scipy.signal import butter, lfilter, sosfilt

SR = 44100
DUR = 40.0
BEAT = 0.5
N = int(SR * DUR)
rng = np.random.default_rng(7)
L = np.zeros(N)
R = np.zeros(N)


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def saw(f, n, detune=0.0, phase=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    f = f * (1 + detune)
    k = 1
    while k * f < SR / 2.2 and k <= 40:
        out += np.sin(2 * np.pi * k * f * t + phase * k) / k
        k += 1
    return out * 0.6


def env(n, a=0.005, d=0.1, s=0.7, r=0.05):
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = max(1, min(na, n))
    e[:na] = np.linspace(0, 1, na)
    if na + nd < n:
        e[na:na + nd] = np.linspace(1, s, nd)
    if nr < n:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def lp(x, fc, order=2):
    sos = butter(order, min(fc, SR / 2.1), "low", fs=SR, output="sos")
    return sosfilt(sos, x)


def hp(x, fc, order=2):
    sos = butter(order, fc, "high", fs=SR, output="sos")
    return sosfilt(sos, x)


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))


CHORDS = [[57, 60, 64], [53, 57, 60], [55, 60, 64], [55, 59, 62]]  # Am F C G
ROOTS = [45, 41, 48, 43]

# ---------------- sidechain envelope (kick pump) ----------------
kick_times = [b * BEAT for b in range(8, 76) if not (16 <= b * BEAT < 24)]  # 4-16, 24-38
duck = np.ones(N)
for kt in kick_times:
    i = int(kt * SR)
    n = int(0.32 * SR)
    seg = 1 - 0.65 * np.exp(-np.linspace(0, 5, n))
    duck[i:i + n] = np.minimum(duck[i:i + n], seg[: len(duck[i:i + n])])

# ---------------- pad (whole track) ----------------
pad = np.zeros(N)
for bar in range(20):
    t0 = bar * 2.0
    n = int(2.15 * SR)
    ch = CHORDS[bar % 4]
    s = np.zeros(n)
    for m in ch + [ch[0] + 12]:
        for dt in (-0.006, 0.0, 0.007):
            s += saw(midi(m), n, dt, rng.uniform(0, 6))
    s *= env(n, 0.25, 0.4, 0.8, 0.35)
    i = int(t0 * SR)
    pad[i:i + n] += s[: N - i] if i + n > N else s
cut = np.interp(np.arange(N) / SR, [0, 4, 8, 16, 24, 32, 40], [500, 1800, 2000, 1400, 4200, 2600, 1200])
# time-varying filter: process in 50 ms blocks
blk = int(0.05 * SR)
padf = np.zeros(N)
zi = None
for i in range(0, N, blk):
    b, a = butter(2, cut[i] / (SR / 2))
    if zi is None:
        zi = np.zeros(max(len(a), len(b)) - 1)
    padf[i:i + blk], zi = lfilter(b, a, pad[i:i + blk], zi=zi)
padg = np.interp(np.arange(N) / SR, [0, 2, 16, 22, 24, 24.01, 32, 39, 40], [0.0, 0.10, 0.10, 0.14, 0.12, 0.16, 0.12, 0.12, 0.0])
pad_out = padf * padg * duck
L += pad_out
R += pad_out

# ---------------- arp (16ths) ----------------
for bar in range(20):
    if 24 <= bar * 2 < 32:
        continue  # drop has the lead instead
    ch = CHORDS[bar % 4]
    pattern = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[2] + 12]
    for k in range(16):
        t0 = bar * 2.0 + k * BEAT / 4
        n = int(0.16 * SR)
        f = midi(pattern[k % 8])
        s = (np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR)) * 0.4 + saw(f, n) * 0.6) * env(n, 0.002, 0.09, 0.0, 0.02)
        fc = float(np.interp(t0, [0, 4, 8, 16, 24, 32, 40], [700, 2600, 2600, 1800, 2200, 3000, 1500]))
        g = float(np.interp(t0, [0, 3.8, 4, 8, 16, 23.9, 32, 39, 40], [0.05, 0.11, 0.09, 0.09, 0.11, 0.12, 0.09, 0.07, 0.0]))
        add(lp(s, fc), t0, g, pan=0.35 if k % 2 else -0.35)

# ---------------- kick ----------------
def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 7.5)
    s[:200] += rng.normal(0, 0.4, 200) * np.linspace(1, 0, 200)
    return s


K = kick()
for kt in kick_times:
    g = 0.9
    add(K, kt, g)

# ---------------- bass (offbeat 8ths) ----------------
for bar in [b for b in range(2, 19) if not (8 <= b < 12)]:
    root = ROOTS[bar % 4]
    for beat in range(4):
        t0 = bar * 2.0 + beat * BEAT + BEAT / 2
        if t0 >= 38:
            break
        n = int(0.22 * SR)
        s = lp(saw(midi(root), n) + 0.5 * np.sin(2 * np.pi * midi(root - 12) * np.arange(n) / SR), 900) * env(n, 0.004, 0.12, 0.55, 0.04)
        add(s, t0, 0.42 if 24 <= bar * 2 < 32 else 0.34)

# ---------------- clap / snare ----------------
def clap():
    n = int(0.22 * SR)
    s = rng.normal(0, 1, n)
    s = hp(lp(s, 6000), 900) * np.exp(-np.arange(n) / SR * 22)
    return s


C = clap()
for bar in [b for b in range(4, 19) if not (8 <= b < 12)]:
    for beat in (1, 3):
        t0 = bar * 2.0 + beat * BEAT
        if t0 < 38:
            add(C, t0, 0.30)
# snare roll 14-16
for k in range(16):
    t0 = 22.0 + k * 0.125
    add(C[: int(0.1 * SR)], t0, 0.08 + 0.2 * k / 15)

# ---------------- hats ----------------
def hat(n_s=0.05):
    n = int(n_s * SR)
    return hp(rng.normal(0, 1, n), 7000) * np.exp(-np.arange(n) / SR * 70)


H = hat()
for i in range(int(2.0 / (BEAT / 2)), int(38.0 / (BEAT / 2))):
    t0 = i * BEAT / 2
    off = (i % 2) == 1
    if (t0 < 4 or 16 <= t0 < 22) and not off:
        continue
    if 16 <= t0 < 22:
        add(H, t0, 0.05, pan=-0.2)
    elif 24 <= t0 < 32:
        add(H, t0, 0.10 if off else 0.06, pan=0.2)
    elif off:
        add(H, t0, 0.09, pan=0.2)

# ---------------- risers + hits ----------------
def riser(d):
    n = int(d * SR)
    t = np.arange(n) / SR
    s = rng.normal(0, 1, n)
    out = np.zeros(n)
    for j in range(0, n, 2048):
        fc = 400 + 9000 * (j / n) ** 2
        out[j:j + 2048] = hp(lp(s[j:j + 2048], fc), 200)
    return out * (t / d) ** 2


add(riser(2.0), 2.0, 0.12)
add(riser(2.0), 22.0, 0.14)


def impact():
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 10)) * t) * np.exp(-t * 3) * 0.9
    s += lp(rng.normal(0, 1, n), 2500) * np.exp(-t * 6) * 0.25
    return s


for t0, g in ((4.0, 0.5), (8.0, 0.25), (16.0, 0.3), (24.0, 0.5), (32.0, 0.5)):
    add(impact(), t0, g)

# ---------------- lead hook (drop + outro) ----------------
HOOK = [  # (beat offset in 8ths, midi, length in 8ths) per 2 bars, repeated
    (0, 76, 1), (2, 81, 1), (3, 79, 1), (4, 76, 1), (6, 74, 1), (7, 76, 1),
    (8, 72, 2), (11, 69, 1), (12, 72, 1), (13, 74, 1), (14, 76, 2),
    (16, 79, 1), (18, 76, 1), (20, 74, 1), (21, 72, 1), (22, 74, 1), (23, 76, 1),
    (24, 74, 2), (26, 71, 1), (28, 74, 1), (29, 76, 1), (30, 79, 2),
]
for start, gain in ((24.0, 0.16), (32.0, 0.11)):
    for off, m, ln in HOOK:
        t0 = start + off * BEAT / 2
        if t0 >= 39.5:
            continue
        n = int((ln * BEAT / 2 + 0.12) * SR)
        t = np.arange(n) / SR
        vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t * 4, 0, 1)
        s = np.zeros(n)
        for dt in (-0.005, 0.005):
            ph = 2 * np.pi * np.cumsum(midi(m) * (1 + dt) * vib) / SR
            k = 1
            while k * midi(m) < SR / 2.5 and k <= 25:
                s += np.sin(ph * k) / k
                k += 1
        s = lp(s * 0.4, 3800) * env(n, 0.008, 0.15, 0.7, 0.08)
        add(s, t0, gain, pan=-0.1)
        add(s, t0 + 0.375, gain * 0.35, pan=0.6)  # dotted-8th echo
        add(s, t0 + 0.75, gain * 0.15, pan=-0.6)

# ---------------- reverb (shared) + master ----------------
ir_n = int(1.8 * SR)
ir = rng.normal(0, 1, ir_n) * np.exp(-np.arange(ir_n) / SR * 3.2)
ir = lp(ir, 5000) * 0.02


def conv(x):
    m = len(x) + ir_n
    nfft = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[: len(x)]


wetL, wetR = conv(L), conv(R)
L2, R2 = L + wetL * 0.5, R + wetR * 0.5
fade = np.ones(N)
fo = int(1.2 * SR)
fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
fade[: int(0.05 * SR)] = np.linspace(0, 1, int(0.05 * SR))
mix = np.stack([L2 * fade, R2 * fade], 1)
mix /= np.max(np.abs(mix)) + 1e-9
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix *= 0.89
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("wrote", sys.argv[1])
