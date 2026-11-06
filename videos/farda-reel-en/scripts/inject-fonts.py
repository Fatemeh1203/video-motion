"""Replace /*FONTS*/ in sub-composition <style> blocks with local Vazirmatn @font-face rules (Arabic + Latin subsets)."""
import sys

WEIGHTS = (300, 400, 500, 700, 800, 900)
AR = "U+0600-06FF, U+0750-077F, U+200C-200E, U+2010-2011, U+204F, U+2E41, U+FB50-FDFF, U+FE70-FEFF"
LA = "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-200B, U+2012-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215"
block = "".join(
    f'@font-face {{ font-family: "Vazirmatn"; font-weight: {w}; '
    f'src: url("assets/fonts/vazirmatn-{sub}-{w}-normal.woff2") format("woff2"); unicode-range: {rng}; }}\n'
    for w in WEIGHTS
    for sub, rng in (("arabic", AR), ("latin", LA))
)
for path in sys.argv[1:]:
    s = open(path, encoding="utf-8").read()
    if "/*FONTS*/" in s:
        open(path, "w", encoding="utf-8").write(s.replace("/*FONTS*/", block))
        print("fonts ->", path)
