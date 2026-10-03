#!/bin/bash
# Prepare a fresh Claude Code on the web container for video work:
# ffmpeg, the HyperFrames CLI + its headless Chrome, and the Python libs the
# video scripts use (music bed, grain, QR, narration). Idempotent.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  (apt-get install -y ffmpeg >/dev/null 2>&1 || (apt-get update >/dev/null 2>&1 && apt-get install -y ffmpeg >/dev/null 2>&1))
fi

if ! command -v hyperframes >/dev/null 2>&1; then
  npm install -g hyperframes >/dev/null 2>&1
fi
hyperframes browser ensure >/dev/null 2>&1 || true

python3 - <<'PY' 2>/dev/null || pip install -q numpy pillow qrcode >/dev/null 2>&1
import numpy, PIL, qrcode
PY

echo "video tools ready: $(ffmpeg -version | head -1 | cut -d' ' -f1-3), hyperframes $(hyperframes --version 2>/dev/null | tail -1)"
