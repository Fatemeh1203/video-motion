"""Replace /*FONTS*/ in sub-composition <style> blocks with local Vazirmatn @font-face rules."""
import sys

WEIGHTS = (300, 400, 500, 700, 800, 900)
block = "".join(
    f'@font-face {{ font-family: "Vazirmatn"; font-weight: {w}; '
    f'src: url("assets/fonts/vazirmatn-arabic-{w}-normal.woff2") format("woff2"); }}\n'
    for w in WEIGHTS
)
for path in sys.argv[1:]:
    s = open(path, encoding="utf-8").read()
    if "/*FONTS*/" in s:
        open(path, "w", encoding="utf-8").write(s.replace("/*FONTS*/", block))
        print("fonts ->", path)
