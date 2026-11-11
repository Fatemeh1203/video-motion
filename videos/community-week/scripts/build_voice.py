"""Rebuild narration and retime the composition from the real clip lengths.

usage: python3 scripts/build_voice.py <voice> <rate>
  e.g. python3 scripts/build_voice.py fa-IR-FaridNeural +10%

Reads voice/lines.txt (one line per scene: hook, Saturday..Friday, CTA), synthesizes each
line with edge-tts, trims silence, then writes voice/lines.tsv, assets/audio/narration.mp3,
a ducked assets/audio/bgm.mp3, and patches index.html: scene starts S, per-scene time scale
KS (a scene's inner animation offsets stretch with its line), total DUR and the audio block.
"""
import json
import os
import re
import subprocess
import sys

VOICE, RATE = sys.argv[1], sys.argv[2]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
lines = [l.strip() for l in open("voice/lines.txt", encoding="utf-8") if l.strip()]
assert len(lines) == 9, "expected 9 lines: hook, 7 days, CTA"


def run(*a):
    subprocess.run(a, check=True, stdin=subprocess.DEVNULL)


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


D = []
for i, text in enumerate(lines):
    mp3, wav = f"voice/l{i:02d}.mp3", f"voice/l{i:02d}.wav"
    run("python3", "scripts/tts_edge.py", VOICE, RATE, text, mp3)
    trim = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    run("ffmpeg", "-nostdin", "-v", "error", "-y", "-i", mp3, "-af", trim, "-ac", "1", "-ar", "24000", wav)
    D.append(dur(wav))

# reference cut (Dilara -5%): line lengths and day-scene lengths the animation offsets were tuned to
OLD_D = [4.054, 5.991, 6.167, 4.675, 4.519, 7.150, 7.159, 4.970, 6.299]
OLD_SCENE = [7.2, 7.4, 5.9, 6.3, 8.4, 8.4, 6.2]

hook_end = round(max(0.6 + D[0] + 0.7, 4.6), 2)
S, KS, starts = [hook_end], [], [0.6]
for k in range(7):
    nd = max(OLD_SCENE[k] * D[k + 1] / OLD_D[k + 1], 0.4 + D[k + 1] + 0.6)
    KS.append(round(nd / OLD_SCENE[k], 3))
    starts.append(round(S[-1] + 0.4, 2))
    S.append(round(S[-1] + nd, 2))
starts.append(round(S[7] + 0.5, 2))
TOTAL = round(S[7] + 0.5 + D[8] + 4.0, 2)

with open("voice/lines.tsv", "w", encoding="utf-8") as f:
    for st, text in zip(starts, lines):
        f.write(f"{st}\t{text}\n")
run("python3", "scripts/mix_narration.py", "voice/lines.tsv", "voice", "voice/narration.wav", str(TOTAL))
run("ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "voice/narration.wav", "-c:a", "libmp3lame", "-b:a", "192k", "assets/audio/narration.mp3")
run("python3", "scripts/make-bgm.py", "voice/bgm-raw.wav", str(TOTAL))
duck = (
    "[0:a]volume=0.55[m];[1:a]asplit[k][x];[m][k]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=500[d];"
    f"[x]anullsink;[d]afade=t=in:d=1.5,afade=t=out:st={TOTAL - 3}:d=3[o]"
)
run("ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "voice/bgm-raw.wav", "-i", "assets/audio/narration.mp3",
    "-filter_complex", duck, "-map", "[o]", "-c:a", "libmp3lame", "-b:a", "192k", "assets/audio/bgm.mp3")
for f in ("voice/narration.wav", "voice/bgm-raw.wav"):
    os.remove(f)

# sound effects follow the scenes
sfx = [("sfx-w0", "whoosh-short", S[0] - 0.1, 0.5, 0.22)]
sfx += [(f"sfx-p{k + 1}", "pop", S[k] + 0.1, 0.5, 0.16) for k in range(7)]
sfx += [("sfx-note", "notification", round(S[5] + 4.4 * KS[5], 2), 1.2, 0.22),
        ("sfx-riser", "riser", S[7] - 1.8, 1.8, 0.18), ("sfx-hit", "impact-bass-1", S[7], 1.5, 0.28)]
audio = [f'      <audio id="narration" src="assets/audio/narration.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="8" data-volume="1"></audio>',
         f'      <audio id="bgm" src="assets/audio/bgm.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="9" data-volume="1"></audio>']
audio += [f'      <audio id="{i}" src="assets/sfx/{n}.mp3" data-start="{round(t, 2)}" data-duration="{d}" data-track-index="{10 + j}" data-volume="{v}"></audio>'
          for j, (i, n, t, d, v) in enumerate(sfx)]

s = open("index.html", encoding="utf-8").read()
s = re.sub(r"<!--AUDIO-->.*?<!--/AUDIO-->", "<!--AUDIO-->\n" + "\n".join(audio) + "\n      <!--/AUDIO-->", s, flags=re.S)
s = re.sub(r"const S = \[.*?\];", "const S = " + json.dumps(S).replace(",", ", ").replace(",  ", ", ") + ";", s)
s = re.sub(r"const KS = \[.*?\];", "const KS = " + json.dumps(KS).replace(",", ", ").replace(",  ", ", ") + ";", s)
s = re.sub(r"const DUR = [0-9.]+;", f"const DUR = {TOTAL};", s)
s = re.sub(r'(id="(?:root|grain|vignette)"[^>]*?data-duration=")[0-9.]+"', rf'\g<1>{TOTAL}"', s)
open("index.html", "w", encoding="utf-8").write(s)

print("lines:", [round(d, 2) for d in D])
print("S:", S, "KS:", KS, "TOTAL:", TOTAL)
