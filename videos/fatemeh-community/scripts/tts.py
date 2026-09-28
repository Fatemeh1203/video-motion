"""Persian narration via edge-tts (fa-IR-DilaraNeural, female).

usage: python3 scripts/tts.py <out.mp3> "<text>" [rate e.g. -5%]
The session's outbound proxy re-signs TLS, so edge-tts must trust its CA
bundle instead of certifi's default one.
"""
import asyncio
import os
import sys

import certifi

CA = "/root/.ccr/ca-bundle.crt"
if os.path.exists(CA):
    certifi.where = lambda: CA

import edge_tts  # noqa: E402  (after the certifi override)


async def main(out, text, rate="+0%"):
    await edge_tts.Communicate(text, "fa-IR-DilaraNeural", rate=rate).save(out)


asyncio.run(main(sys.argv[1], sys.argv[2], *(sys.argv[3:4])))
