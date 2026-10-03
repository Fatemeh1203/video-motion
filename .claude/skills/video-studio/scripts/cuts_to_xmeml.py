"""Write a Final Cut Pro 7 XML (xmeml v4) timeline that Premiere opens with File > Import.

usage: python3 cuts_to_xmeml.py <plan.json> <out.xml>

plan.json:
{
  "name": "My edit",
  "source": "/abs/path/original.mp4",          # linked, never copied
  "keep": [[0.0, 4.2], [5.1, 12.8]],           # source seconds, in order (the cut table)
  "overlays": [{"file": "/abs/anim1.mov", "start": 3.0}],   # timeline seconds, V2 (ProRes 4444 alpha)
  "sfx":      [{"file": "/abs/whoosh.wav", "start": 2.9}],  # timeline seconds, A2
  "markers":  [{"start": 7.5, "name": "B-roll", "comment": "screen recording of the site"}],
  "path_map": ["/home/user/video-motion/", "C:/Users/me/Videos/"]  # optional prefix rewrite
}
Frame rate, size, sample rate and durations are read with ffprobe; every time is converted to
whole frames of the source rate so the sequence never drifts (the classic Premiere desync).
"""

import json
import subprocess
import sys
import urllib.parse
from fractions import Fraction
from xml.sax.saxutils import escape

plan = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]


def probe(path):
    d = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                                  capture_output=True, text=True, check=True).stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    return v, a, float(d["format"]["duration"])


sv, sa, sdur = probe(plan["source"])
fps = Fraction(sv["r_frame_rate"])
ntsc = fps.denominator == 1001
timebase = round(float(fps))
W, H = int(sv["width"]), int(sv["height"])
SR = int(sa["sample_rate"]) if sa else 48000


def fr(sec):
    return int(round(sec * float(fps)))


def url(path):
    a, b = plan.get("path_map", ["", ""]) or ["", ""]
    if a and path.startswith(a):
        path = b + path[len(a):]
    path = path.replace("\\", "/")
    if len(path) > 1 and path[1] == ":":
        path = "/" + path
    return "file://localhost" + urllib.parse.quote(path)


RATE = f"<rate><timebase>{timebase}</timebase><ntsc>{'TRUE' if ntsc else 'FALSE'}</ntsc></rate>"
files_done, uid = set(), [0]


def nid(p):
    uid[0] += 1
    return f"{p}-{uid[0]}"


def file_el(fid, path, dur_f, video=True, audio=True, w=W, h=H):
    if fid in files_done:
        return f'<file id="{fid}"/>'
    files_done.add(fid)
    media = ""
    if video:
        media += f"<video><samplecharacteristics>{RATE}<width>{w}</width><height>{h}</height></samplecharacteristics></video>"
    if audio:
        media += f"<audio><samplecharacteristics><depth>16</depth><samplerate>{SR}</samplerate></samplecharacteristics><channelcount>2</channelcount></audio>"
    name = escape(path.replace("\\", "/").split("/")[-1])
    return (f'<file id="{fid}"><name>{name}</name><pathurl>{escape(url(path))}</pathurl>{RATE}'
            f"<duration>{dur_f}</duration><media>{media}</media></file>")


def clip(path, fid, fdur_f, t_in, t_out, s_in, s_out, kind, video=True, audio=True, w=W, h=H, track=1):
    src = f"<sourcetrack><mediatype>{kind}</mediatype><trackindex>{track}</trackindex></sourcetrack>" if kind == "audio" else ""
    return (f'<clipitem id="{nid("clipitem")}"><name>{escape(path.split("/")[-1])}</name><enabled>TRUE</enabled>'
            f"<duration>{fdur_f}</duration>{RATE}<start>{t_in}</start><end>{t_out}</end><in>{s_in}</in><out>{s_out}</out>"
            f"{file_el(fid, path, fdur_f, video, audio, w, h)}{src}</clipitem>")


# V1 / A1: the kept pieces of the original, back to back
src_f = fr(sdur)
v1, a1, t = [], [], 0
for s, e in plan["keep"]:
    si, so = fr(s), fr(e)
    v1.append(clip(plan["source"], "file-src", src_f, t, t + so - si, si, so, "video", True, bool(sa)))
    if sa:
        a1.append(clip(plan["source"], "file-src", src_f, t, t + so - si, si, so, "audio", True, True))
    t += so - si
seq_f = t

v2 = []
for i, o in enumerate(plan.get("overlays", [])):
    ov, _, od = probe(o["file"])
    d = fr(od)
    st = fr(o["start"])
    v2.append(clip(o["file"], f"file-ov{i}", d, st, st + d, 0, d, "video", True, False, int(ov["width"]), int(ov["height"])))
    seq_f = max(seq_f, st + d)

a2 = []
for i, x in enumerate(plan.get("sfx", [])):
    _, _, xd = probe(x["file"])
    d = fr(xd)
    st = fr(x["start"])
    a2.append(clip(x["file"], f"file-sfx{i}", d, st, st + d, 0, d, "audio", False, True))

markers = "".join(
    f"<marker><name>{escape(m.get('name', 'marker'))}</name><comment>{escape(m.get('comment', ''))}</comment>"
    f"<in>{fr(m['start'])}</in><out>-1</out></marker>" for m in plan.get("markers", []))

xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4">'
    f'<sequence id="sequence-1"><name>{escape(plan.get("name", "AI edit"))}</name><duration>{seq_f}</duration>{RATE}'
    "<timecode>" + RATE + "<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>"
    "<media><video><format><samplecharacteristics>" + RATE +
    f"<width>{W}</width><height>{H}</height><pixelaspectratio>square</pixelaspectratio></samplecharacteristics></format>"
    f"<track>{''.join(v1)}</track><track>{''.join(v2)}</track></video>"
    f"<audio><numOutputChannels>2</numOutputChannels><format><samplecharacteristics><depth>16</depth><samplerate>{SR}</samplerate></samplecharacteristics></format>"
    f"<track>{''.join(a1)}</track><track>{''.join(a2)}</track></audio></media>{markers}</sequence></xmeml>\n"
)
open(OUT, "w", encoding="utf-8").write(xml)
print(f"wrote {OUT}: {len(v1)} cuts, {len(v2)} overlays, {len(a2)} sfx, "
      f"{len(plan.get('markers', []))} markers, {seq_f} frames @ {float(fps):.3f} fps")
