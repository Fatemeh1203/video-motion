"""Free Persian TTS through edge-tts (Microsoft Edge read-aloud voices), no account or key.

usage: python3 tts_edge.py <voice> <rate> <text> <out.mp3>
  e.g. python3 tts_edge.py fa-IR-DilaraNeural -5% "سلام" out.mp3 </dev/null

Voices: fa-IR-DilaraNeural (female), fa-IR-FaridNeural (male). Needs `pip install edge-tts`.
edge-tts pins certifi's CA list, which fails behind this container's TLS proxy, so the
proxy CA bundle is swapped in when it exists. In a shell loop, give ffmpeg `-nostdin`
(or this script `</dev/null`) or it eats the next line of the loop's input.
This is an unofficial use of a free Microsoft service and may stop working without notice.
"""
import asyncio
import os
import ssl
import sys

import edge_tts.communicate as c

CA = "/root/.ccr/ca-bundle.crt"
if os.path.exists(CA):
    c._SSL_CTX = ssl.create_default_context(cafile=CA)

voice, rate, text, out = sys.argv[1:5]


async def main():
    await c.Communicate(text, voice, rate=rate, proxy=os.environ.get("HTTPS_PROXY")).save(out)


asyncio.run(main())
