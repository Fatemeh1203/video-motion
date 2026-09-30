"""Writes index.html: scene hosts, ambient layers, music bed and SFX. Edit SCENES/SFX here."""

AR = "U+0600-06FF, U+0750-077F, U+200C-200E, U+2010-2011, U+204F, U+2E41, U+FB50-FDFF, U+FE70-FEFF"
LA = "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-200B, U+2012-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215"
TOTAL = 120

SCENES = [
    ("s1-hook", 0, 10.0),
    ("s2-intro", 9.4, 9.6),
    ("s3-map", 18.4, 12.6),
    ("s4-portal", 30.4, 10.6),
    ("s5-form", 40.4, 12.6),
    ("s6-telegram", 52.4, 12.6),
    ("s7-share", 64.4, 10.6),
    ("s8-sheet", 74.4, 10.6),
    ("s9-classes", 84.4, 9.8),
    ("s10-report", 93.6, 13.2),
    ("s11-trust", 106.2, 7.2),
    ("s12-cta", 112.8, 7.2),
]

# (file, start, duration, volume)
SFX = [
    ("impact-bass-1", 0.2, 2, 0.2),
    ("pop", 1.2, 0.6, 0.14), ("pop", 1.6, 0.6, 0.14), ("pop", 2.0, 0.6, 0.14),
    ("pop", 2.4, 0.6, 0.14), ("pop", 2.8, 0.6, 0.14), ("pop", 3.2, 0.6, 0.14),
    ("glitch-1", 4.6, 0.8, 0.1),
    ("whoosh", 6.9, 0.57, 0.24),
    ("whoosh-cinematic", 9.2, 2, 0.24),
    ("sparkle", 10.4, 1.8, 0.2),
    ("pop", 13.6, 0.6, 0.16), ("pop", 13.9, 0.6, 0.16), ("pop", 14.2, 0.6, 0.16),
    ("pop", 14.5, 0.6, 0.16), ("pop", 14.8, 0.6, 0.16),
    ("whoosh-cinematic", 18.2, 2, 0.24),
    ("click-soft", 20.6, 0.37, 0.2), ("click-soft", 21.0, 0.37, 0.2), ("click-soft", 21.4, 0.37, 0.2),
    ("riser", 22.0, 6, 0.1),
    ("chime", 28.2, 1.5, 0.2),
    ("whoosh", 30.2, 0.57, 0.24),
    ("pop", 33.2, 0.6, 0.16), ("pop", 33.6, 0.6, 0.16), ("pop", 34.0, 0.6, 0.16),
    ("click-soft", 38.9, 0.37, 0.26),
    ("whoosh", 40.2, 0.57, 0.24),
    ("typing", 42.4, 1.5, 0.16), ("typing", 45.0, 1.5, 0.16), ("typing", 47.6, 1.4, 0.16),
    ("click-soft", 50.5, 0.37, 0.26), ("chime", 50.9, 1.5, 0.18),
    ("whoosh", 52.2, 0.57, 0.24),
    ("notification", 53.6, 1.2, 0.24),
    ("click-soft", 58.7, 0.37, 0.26),
    ("click-soft", 61.7, 0.37, 0.26), ("notification", 62.3, 1.2, 0.22),
    ("whoosh", 64.2, 0.57, 0.24),
    ("click-soft", 66.2, 0.37, 0.16), ("click-soft", 66.8, 0.37, 0.16),
    ("click-soft", 67.4, 0.37, 0.16), ("click-soft", 68.0, 0.37, 0.16),
    ("impact-bass-1", 69.6, 2, 0.16),
    ("whoosh", 74.2, 0.57, 0.24),
    ("pop", 76.4, 0.6, 0.16), ("sparkle", 77.0, 1.8, 0.14),
    ("click-soft", 79.9, 0.37, 0.2), ("pop", 80.8, 0.6, 0.16),
    ("whoosh", 84.2, 0.57, 0.24),
    ("pop", 87.0, 0.6, 0.18), ("glitch-1", 89.4, 0.8, 0.1), ("sparkle", 91.0, 1.8, 0.16),
    ("whoosh-cinematic", 93.4, 2, 0.24),
    ("click-soft", 96.4, 0.37, 0.26), ("notification", 97.4, 1.2, 0.22),
    ("chime", 100.6, 1.5, 0.18),
    ("pop", 102.4, 0.6, 0.16), ("pop", 102.8, 0.6, 0.16), ("pop", 103.2, 0.6, 0.16),
    ("whoosh", 106.0, 0.57, 0.24),
    ("pop", 107.0, 0.6, 0.16), ("pop", 107.4, 0.6, 0.16), ("pop", 107.8, 0.6, 0.16), ("pop", 108.2, 0.6, 0.16),
    ("whoosh-cinematic", 112.6, 2, 0.26),
    ("impact-bass-1", 113.4, 2, 0.2),
    ("sparkle", 115.6, 1.8, 0.2),
]

fonts = "".join(
    f'      @font-face {{ font-family: "Vazirmatn"; font-weight: {w}; src: url("assets/fonts/vazirmatn-{sub}-{w}-normal.woff2") format("woff2"); unicode-range: {rng}; }}\n'
    for w in (300, 400, 500, 700, 800, 900)
    for sub, rng in (("arabic", AR), ("latin", LA))
)

hosts = []
for i, (cid, st, du) in enumerate(SCENES):
    hosts.append(
        f'      <div id="el-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
        f'data-start="{st}" data-duration="{du}" data-track-index="{1 + i % 2}" data-width="1920" data-height="1080"></div>'
    )

sfx = []
for i, (f, st, du, vol) in enumerate(SFX):
    sfx.append(
        f'      <audio id="sfx-{i:02d}" src="assets/sfx/{f}.mp3" data-start="{st}" data-duration="{du}" '
        f'data-track-index="{11 + i % 6}" data-volume="{vol}"></audio>'
    )

html = f"""<!DOCTYPE html>
<html lang="fa">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080">
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
{fonts}
      :root {{
        --sky1: #bcd8fb;
        --sky2: #d6e8fd;
        --sky3: #eaf3fe;
        --sky4: #f6faff;
        --ink: #1f335a;
        --ink2: #34507f;
        --ink3: #4d6795;
        --blue: #3d6fd6;
        --blue-d: #2a54ad;
        --violet: #6f57cf;
        --slate: #5c86a8;
        --gold: #a8650d;
        --gold-bg: #fff1d6;
        --green: #1c7a51;
        --green-bg: #dcf5e8;
        --red: #b3263e;
        --tg: #2aabee;
        --card: linear-gradient(180deg, #ffffff, #f4f8ff);
        --card-line: rgba(61, 111, 214, 0.18);
        --shadow: 0 40px 80px -30px rgba(60, 100, 180, 0.55), inset 0 -8px 20px rgba(150, 185, 240, 0.18);
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: var(--sky2); }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: linear-gradient(180deg, var(--sky1) 0%, var(--sky2) 30%, var(--sky3) 60%, var(--sky4) 100%);
        font-family: "Vazirmatn", sans-serif;
        color: var(--ink);
      }}
      #root > div[data-composition-src] {{ position: absolute; inset: 0; }}
      #grain {{ position: absolute; inset: 0; pointer-events: none; background-image: url("assets/grain.png"); background-size: 256px 256px; opacity: 0.07; mix-blend-mode: multiply; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1920" data-height="1080" data-duration="{TOTAL}">
      <div id="el-ambient" data-composition-id="ambient" data-composition-src="compositions/ambient.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-width="1920" data-height="1080"></div>
{chr(10).join(hosts)}

      <div id="grain" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="6"></div>

      <!-- music bed (scripts/make-bgm.py) -->
      <audio id="bgm" src="assets/audio/bgm.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="10" data-volume="0.55"></audio>

      <!-- sound design (media-use bundled SFX) -->
{chr(10).join(sfx)}
    </div>

    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(html)
print("index.html written:", len(SCENES), "scenes,", len(SFX), "sfx")
