"""Synthesize the video's ambient music bed (deterministic, royalty-free).

Warm dawn pad + plucked arpeggio + soft pulse, 96 BPM, D major.
Structure follows the scene plan: pad-only intro, groove from the intro
scene, fuller section under the community scene, pad-only outro.

Usage: python3 scripts/make-bgm.py assets/audio/bgm.wav [duration_s]
"""

import sys
import wave

import numpy as np

SR = 44100
BPM = 96
BEAT = 60 / BPM
BAR = BEAT * 4
OUT = sys.argv[1] if len(sys.argv) > 1 else "bgm.wav"
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 114.0
N = int(SR * DUR)
t_all = np.arange(N) / SR
rng = np.random.default_rng(7)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


# Dmaj9 – Bm7 – Gmaj7 – A(add9), two bars each
PROG = [
    [50, 57, 61, 64, 66],  # D  A  C# E  F#
    [47, 54, 57, 62, 66],  # B  F# A  D  F#
    [43, 50, 54, 59, 62],  # G  D  F# B  D
    [45, 52, 57, 59, 64],  # A  E  A  B  E
]
CHORD_LEN = BAR * 2


def env_section(t):
    """Global intensity curve per scene section (0..1)."""
    return np.interp(
        t,
        [0, 9, 11, 68, 72, 98, 102, DUR - 6, DUR],
        [0.55, 0.7, 0.85, 0.85, 1.0, 1.0, 0.75, 0.6, 0.0],
    )


mix_l = np.zeros(N)
mix_r = np.zeros(N)

# ---- Pad: detuned additive voices with slow swell per chord
n_chords = int(np.ceil(DUR / CHORD_LEN)) + 1
for ci in range(n_chords):
    start = ci * CHORD_LEN
    if start >= DUR:
        break
    chord = PROG[ci % len(PROG)]
    length = CHORD_LEN + 1.2  # overlap tail
    s0 = int(start * SR)
    s1 = min(N, int((start + length) * SR))
    tt = np.arange(s1 - s0) / SR
    a = np.clip(tt / 1.4, 0, 1) * np.clip((length - tt) / 1.4, 0, 1)
    a = a**1.5
    for vi, note in enumerate(chord):
        f = hz(note)
        for det, pan in ((-0.09, 0.3), (0.09, 0.7)):
            ff = f * 2 ** (det / 12)
            ph = rng.uniform(0, 2 * np.pi)
            v = (
                np.sin(2 * np.pi * ff * tt + ph)
                + 0.35 * np.sin(2 * np.pi * 2 * ff * tt + ph)
                + 0.12 * np.sin(2 * np.pi * 3 * ff * tt + ph)
            )
            g = 0.035 * a * (1.0 if vi else 1.3)
            mix_l[s0:s1] += v * g * (1 - pan)
            mix_r[s0:s1] += v * g * pan

# ---- Sub bass: chord root, gentle
for ci in range(n_chords):
    start = ci * CHORD_LEN
    if start >= DUR:
        break
    root = PROG[ci % len(PROG)][0] - 12
    s0 = int(start * SR)
    s1 = min(N, int((start + CHORD_LEN) * SR))
    tt = np.arange(s1 - s0) / SR
    a = np.clip(tt / 0.3, 0, 1) * np.clip((CHORD_LEN - tt) / 0.5, 0, 1)
    v = np.sin(2 * np.pi * hz(root) * tt) * 0.09 * a
    gate = np.interp(start, [0, 10, 11], [0.0, 0.0, 1.0])
    mix_l[s0:s1] += v * gate
    mix_r[s0:s1] += v * gate

# ---- Plucked arpeggio (16th-ish pattern) from 10s
ARP_ORDER = [0, 2, 3, 4, 3, 2, 1, 2]
step = BEAT / 2
n_steps = int(DUR / step)
for si in range(n_steps):
    st = si * step
    if st < 10.0 or st > DUR - 10:
        continue
    chord = PROG[int(st // CHORD_LEN) % len(PROG)]
    note = chord[ARP_ORDER[si % len(ARP_ORDER)]] + 12
    f = hz(note)
    ln = 1.1
    s0 = int(st * SR)
    s1 = min(N, s0 + int(ln * SR))
    tt = np.arange(s1 - s0) / SR
    e = np.exp(-tt * 5.5) * np.clip(tt / 0.004, 0, 1)
    v = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * e
    accent = 1.0 if si % 4 == 0 else 0.7
    g = 0.05 * accent
    pan = 0.35 if si % 2 == 0 else 0.65
    mix_l[s0:s1] += v * g * (1 - pan)
    mix_r[s0:s1] += v * g * pan

# ---- Soft kick on beats 1 & 3, shaker on off-beats, 11s .. DUR-10
n_beats = int(DUR / BEAT)
for bi in range(n_beats):
    st = bi * BEAT
    if st < 11.0 or st > DUR - 10:
        continue
    s0 = int(st * SR)
    if bi % 2 == 0:
        ln = 0.35
        s1 = min(N, s0 + int(ln * SR))
        tt = np.arange(s1 - s0) / SR
        f = 45 + 70 * np.exp(-tt * 30)
        ph = 2 * np.pi * np.cumsum(f) / SR
        v = np.sin(ph) * np.exp(-tt * 9) * 0.22
        mix_l[s0:s1] += v
        mix_r[s0:s1] += v
    # shaker on the "and"
    s0 = int((st + BEAT / 2) * SR)
    ln = 0.08
    s1 = min(N, s0 + int(ln * SR))
    if s0 < N:
        tt = np.arange(s1 - s0) / SR
        noise = rng.standard_normal(s1 - s0)
        noise = np.diff(np.concatenate([[0], noise]))  # crude high-pass
        v = noise * np.exp(-tt * 60) * 0.018
        mix_l[s0:s1] += v * 0.8
        mix_r[s0:s1] += v * 1.2

# ---- Intensity curve
g = env_section(t_all)
mix_l *= g
mix_r *= g

# ---- Reverb: convolve with decaying noise IR (FFT)
ir_len = int(SR * 2.4)
ir_t = np.arange(ir_len) / SR
ir_l = rng.standard_normal(ir_len) * np.exp(-ir_t * 2.6)
ir_r = rng.standard_normal(ir_len) * np.exp(-ir_t * 2.6)
ir_l /= np.sqrt(np.sum(ir_l**2))
ir_r /= np.sqrt(np.sum(ir_r**2))


def conv(x, ir):
    n = len(x) + len(ir) - 1
    nfft = 1 << (n - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)[: len(x)]
    return y


wet_l = conv(mix_l, ir_l)
wet_r = conv(mix_r, ir_r)
out_l = mix_l * 0.75 + wet_l * 0.35
out_r = mix_r * 0.75 + wet_r * 0.35

# ---- Master: fade in/out + soft clip + normalize to about -14 dBFS peak area
fade = np.clip(t_all / 1.5, 0, 1) * np.clip((DUR - t_all) / 4.0, 0, 1)
out_l *= fade
out_r *= fade
peak = max(np.max(np.abs(out_l)), np.max(np.abs(out_r)))
out_l = np.tanh(out_l / peak * 1.2) * 0.8
out_r = np.tanh(out_r / peak * 1.2) * 0.8

pcm = np.stack([out_l, out_r], axis=1)
pcm = (pcm * 32767).astype(np.int16)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"wrote {OUT} ({DUR:.1f}s)")
