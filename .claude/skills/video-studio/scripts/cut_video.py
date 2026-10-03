"""Cut a recording down to its keep-ranges and render a clean MP4 (the "MP4" edit route).

usage: python3 cut_video.py <source> <keep.json> <out.mp4> [--punch 1.08] [--clean-voice] [--lufs -14]

keep.json: [[start_s, end_s], ...] in source time, in order (from the cut table), or the
           transcribe.py JSON: then every pause longer than --max-pause is shortened to
           --target seconds (never to zero, so speech keeps its rhythm).
- every cut gets a 30 ms audio fade on both sides (no clicks);
- every other segment is punched in (default 108 %, centred) to hide the jump cut;
- --clean-voice: RNNoise (arnndn) + gentle de-ess/EQ/compression, the chain used for
  Fatemeh's narration; the model is fetched from GitHub on first use;
- loudness is normalised to --lufs (-14 for YouTube/Instagram, -16 for narration beds).
The source file is never modified.
"""

import argparse
import json
import os
import subprocess
import urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("source")
ap.add_argument("keep")
ap.add_argument("out")
ap.add_argument("--punch", type=float, default=1.08)
ap.add_argument("--clean-voice", action="store_true")
ap.add_argument("--lufs", type=float, default=-14)
ap.add_argument("--crf", type=int, default=18)
ap.add_argument("--max-pause", type=float, default=0.7)
ap.add_argument("--target", type=float, default=0.3)
args = ap.parse_args()

keep = json.load(open(args.keep, encoding="utf-8"))
if isinstance(keep, dict):  # transcribe.py output -> keep ranges with pauses shortened
    tr, keep, cur = keep, [], 0.0
    for p in tr["pauses"]:
        if p["end"] - p["start"] > args.max_pause:
            keep.append([round(cur, 3), round(p["start"] + args.target / 2, 3)])
            cur = p["end"] - args.target / 2
    keep.append([round(cur, 3), tr["duration"]])
    keep = [k for k in keep if k[1] - k[0] > 0.05]
probe = json.loads(subprocess.run(
    ["ffprobe", "-v", "error", "-show_streams", "-of", "json", args.source], capture_output=True, text=True, check=True).stdout)
v = next(s for s in probe["streams"] if s["codec_type"] == "video")
has_audio = any(s["codec_type"] == "audio" for s in probe["streams"])
W, H = int(v["width"]), int(v["height"])

F = 0.03
parts, labels = [], []
for i, (s, e) in enumerate(keep):
    vf = f"[0:v]trim=start={s}:end={e},setpts=PTS-STARTPTS"
    if args.punch > 1 and i % 2 == 1:
        sw, sh = int(W * args.punch) // 2 * 2, int(H * args.punch) // 2 * 2
        vf += f",scale={sw}:{sh},crop={W}:{H}"
    parts.append(vf + f",setsar=1[v{i}]")
    lab = f"[v{i}]"
    if has_audio:
        d = e - s
        parts.append(f"[0:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d={F},afade=t=out:st={max(0, d - F):.3f}:d={F}[a{i}]")
        lab += f"[a{i}]"
    labels.append(lab)
n = len(keep)
parts.append("".join(labels) + f"concat=n={n}:v=1:a={1 if has_audio else 0}[vc]" + ("[ac]" if has_audio else ""))

achain = []
if has_audio and args.clean_voice:
    rnn = os.path.expanduser("~/.cache/video-studio/rnn/std.rnnn")
    if not os.path.exists(rnn):
        os.makedirs(os.path.dirname(rnn), exist_ok=True)
        urllib.request.urlretrieve("https://raw.githubusercontent.com/richardpl/arnndn-models/master/std.rnnn", rnn)
    achain += [
        "highpass=f=75", f"arnndn=m={rnn}", "afftdn=nr=8:nf=-60:tn=1", "deesser=i=0.35",
        "equalizer=f=220:t=q:w=1:g=-2.5", "equalizer=f=3000:t=q:w=1.2:g=2.5", "highshelf=f=9000:g=1.5",
        "acompressor=threshold=-24dB:ratio=3:attack=6:release=150:makeup=4",
    ]
if has_audio:
    achain.append(f"loudnorm=I={args.lufs}:TP=-1.5:LRA=11")
    parts.append("[ac]" + ",".join(achain) + "[aout]")

cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", args.source, "-filter_complex", ";".join(parts),
       "-map", "[vc]", "-c:v", "libx264", "-crf", str(args.crf), "-preset", "slow", "-pix_fmt", "yuv420p"]
if has_audio:
    cmd += ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
cmd += ["-movflags", "+faststart", args.out]
subprocess.run(cmd, check=True)
kept = sum(e - s for s, e in keep)
print(f"wrote {args.out}: {n} segments, {kept:.2f}s kept")
