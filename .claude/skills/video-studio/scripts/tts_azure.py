"""Persian narration with Azure Speech REST + SSML (default fa-IR-DilaraNeural, female).

usage: AZURE_SPEECH_KEY=... AZURE_SPEECH_REGION=westeurope \
       python3 tts_azure.py <lines.tsv> <out_dir> [total_seconds] [voice]

lines.tsv: "start_seconds<TAB>text". The text may contain inline SSML (e.g.
<break time="300ms"/>, <sub alias="چت‌جی‌پی‌تی">ChatGPT</sub>, <emphasis>…</emphasis>).
Each line becomes <out_dir>/lNN.wav (24 kHz mono); if a line does not fit before the next
start, the prosody rate is raised a little (up to +25%).

Requires the host <region>.tts.speech.microsoft.com to be allowed in the environment's
network settings. Untested here until a key is provided.
"""

import os
import sys
import urllib.request
import wave

TSV, OUT = sys.argv[1], sys.argv[2]
TOTAL = float(sys.argv[3]) if len(sys.argv) > 3 else None
VOICE = sys.argv[4] if len(sys.argv) > 4 else "fa-IR-DilaraNeural"
KEY = os.environ["AZURE_SPEECH_KEY"]
REGION = os.environ["AZURE_SPEECH_REGION"]
URL = f"https://{REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
GAP = 0.15
os.makedirs(OUT, exist_ok=True)

CA = "/root/.ccr/ca-bundle.crt"
ctx = None
if os.path.exists(CA):
    import ssl

    ctx = ssl.create_default_context(cafile=CA)


def synth(text, rate_pct, path):
    ssml = (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="fa-IR">'
        f'<voice name="{VOICE}"><prosody rate="{rate_pct:+d}%">{text}</prosody></voice></speak>'
    )
    req = urllib.request.Request(
        URL,
        data=ssml.encode("utf-8"),
        headers={
            "Ocp-Apim-Subscription-Key": KEY,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "User-Agent": "video-studio",
        },
    )
    with urllib.request.urlopen(req, context=ctx) as r, open(path, "wb") as f:
        f.write(r.read())
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


lines = [l.rstrip("\n").split("\t", 1) for l in open(TSV, encoding="utf-8") if l.strip()]
starts = [float(s) for s, _ in lines]
for i, (st, text) in enumerate(lines):
    nxt = starts[i + 1] if i + 1 < len(starts) else (TOTAL or starts[i] + 30)
    room = nxt - float(st) - GAP
    path = os.path.join(OUT, f"l{i:02d}.wav")
    rate = 0
    dur = synth(text, rate, path)
    while dur > room and rate < 25:
        rate = min(25, rate + max(3, int((dur / room - 1) * 100) + 2))
        dur = synth(text, rate, path)
    flag = "OK" if dur <= room else "TOO LONG: shorten the text or move the next start"
    print(f"{i:02d} @{float(st):6.1f}s  {dur:5.2f}s / room {room:5.2f}s  rate {rate:+d}%  {flag}")
