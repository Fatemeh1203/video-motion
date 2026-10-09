import re
src = open("/home/user/video-motion/videos/community-teaser/index.html", encoding="utf-8").read()
s = src
def r(a, b, count=1):
    global s
    assert a in s, "MISSING: " + a[:80]
    s = s.replace(a, b, count)

# ---- durations
r('data-duration="32">', 'data-duration="40">')
r('<div id="vignette" class="clip" data-start="0" data-duration="32"', '<div id="vignette" class="clip" data-start="0" data-duration="40"')
r('<div id="grain" class="clip" data-start="0" data-duration="32"', '<div id="grain" class="clip" data-start="0" data-duration="40"')

# ---- CSS: lesson scene + 6 day chips
r("      /* ---------- S3 belonging ---------- */", """      /* ---------- SL daily lessons on every AI tool ---------- */
      #sl-bg { position: absolute; inset: 0; background: radial-gradient(ellipse 70% 70% at 30% 45%, #131c38, #080b15 70%); }
      #sl-copy { position: absolute; right: 150px; top: 230px; width: 940px; text-align: right; }
      #sl-eye { display: inline-flex; align-items: center; gap: 14px; font-size: 38px; font-weight: 500; color: var(--mint); opacity: 0; }
      #sl-eye i { display: block; width: 14px; height: 14px; border-radius: 50%; background: var(--mint); box-shadow: 0 0 16px var(--mint); }
      #sl-title { margin-top: 16px; display: flex; flex-wrap: wrap; gap: 0 26px; font-size: 92px; font-weight: 900; line-height: 1.3; }
      #sl-title .br { flex-basis: 100%; height: 0; }
      #sl-sub { margin-top: 26px; font-size: 44px; font-weight: 500; color: var(--muted); opacity: 0; }
      #sl-sub b { color: var(--fg); font-weight: 800; }
      #sl-card {
        position: absolute; left: 150px; top: 190px; width: 700px;
        padding: 34px 40px 30px; border-radius: 32px;
        border: 2px solid var(--glass-line);
        background: linear-gradient(145deg, rgba(23, 29, 48, 0.95), rgba(9, 14, 26, 0.95));
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.5);
        opacity: 0;
      }
      #sl-card-head { display: flex; justify-content: space-between; align-items: center; font-size: 30px; font-weight: 800; color: var(--muted); }
      #sl-card-head span:last-child { padding: 6px 18px; border-radius: 20px; background: rgba(137, 255, 240, 0.14); color: var(--mint); font-size: 26px; }
      #sl-tool { position: relative; height: 130px; margin-top: 14px; }
      .sl-name { position: absolute; left: 0; right: 0; top: 0; text-align: center; direction: ltr; font-size: 96px; font-weight: 900; line-height: 130px; opacity: 0; }
      .sl-step { display: flex; align-items: center; gap: 18px; margin-top: 16px; font-size: 34px; font-weight: 700; opacity: 0.35; }
      .sl-step i { flex: none; display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 50%; border: 3px solid rgba(255, 255, 255, 0.25); font-style: normal; font-size: 26px; color: #080b15; }
      .sl-step i b { opacity: 0; }
      #sl-grid { position: absolute; left: 150px; top: 690px; width: 720px; display: flex; flex-wrap: wrap; gap: 14px; direction: ltr; }
      .sl-chip { display: flex; align-items: center; gap: 10px; padding: 8px 18px; border-radius: 30px; border: 2px solid rgba(255, 255, 255, 0.14); background: rgba(18, 24, 42, 0.9); font-size: 24px; font-weight: 700; color: rgba(239, 244, 255, 0.55); opacity: 0; }
      .sl-chip i { display: block; width: 10px; height: 10px; border-radius: 50%; background: var(--c); }

      /* ---------- S3 belonging ---------- */""")
r(""".day {
        position: absolute; width: 300px; height: 96px; border-radius: 22px;
        display: flex; align-items: center; justify-content: center; gap: 16px;
        font-size: 40px; font-weight: 800;""", """.day {
        position: absolute; width: 300px; height: 84px; border-radius: 22px;
        display: flex; align-items: center; justify-content: center; gap: 16px;
        font-size: 36px; font-weight: 800;""")

# ---- HTML: insert the lesson scene before S3
TOOLS = [("ChatGPT", "#91ffea"), ("Claude", "#ffbf86"), ("Gemini", "#77caff"), ("Midjourney", "#b39aff"),
         ("Perplexity", "#91ffea"), ("NotebookLM", "#ddf998"), ("Cursor", "#ff94ba"), ("n8n", "#ff94ba"),
         ("Suno", "#ffbf86"), ("Runway", "#b39aff"), ("DeepSeek", "#77caff"), ("Canva AI", "#ddf998"),
         ("Copilot", "#77caff"), ("Gamma", "#91ffea")]
names = "".join(f'<div class="sl-name" style="color: {c}">{n}</div>' for n, c in TOOLS)
chips = "".join(f'<div class="sl-chip" style="--c: {c}"><i></i>{n}</div>' for n, c in TOOLS)
r("      <!-- S3 belonging (her own words) -->", f"""      <!-- SL daily practical lessons on every AI tool -->
      <div id="sl" class="scene">
        <div id="sl-bg"></div>
        <div id="sl-card" class="rtl">
          <div id="sl-card-head"><span>درسنامهٔ امروز</span><span>کاربردی</span></div>
          <div id="sl-tool">{names}</div>
          <div class="sl-step"><i><b>✓</b></i>قدم‌به‌قدم، از صفر</div>
          <div class="sl-step"><i><b>✓</b></i>تمرین روی کار واقعی</div>
          <div class="sl-step"><i><b>✓</b></i>جزوه برای مرور</div>
        </div>
        <div id="sl-grid">{chips}</div>
        <div id="sl-copy" class="rtl">
          <div id="sl-eye"><i></i><span>در گروه کامیونیتی هوش مصنوعی</span></div>
          <div id="sl-title"><span class="w">آموزش</span><span class="w">کاربردیِ</span><i class="br"></i><span class="w g">همهٔ</span><span class="w g">ابزارهای</span><i class="br"></i><span class="w g">هوش</span><span class="w g">مصنوعی</span><span class="w g">دنیا</span></div>
          <div id="sl-sub">هر روز، <b>یک درسنامهٔ تازه</b>؛ قدم‌به‌قدم و با جزوه</div>
        </div>
      </div>

      <!-- S3 belonging (her own words) -->""")

# ---- features: f1 text, f2 odd days (Iranian week: فرد = یکشنبه، سه‌شنبه، پنجشنبه)
r('<div class="f-title">هر روز، <span class="g">یک درس تازه</span></div>\n            <div class="f-sub">با جزوهٔ مخصوص هر درس</div>',
  '<div class="f-title">هر روز،<br /><span class="g">یک درسنامهٔ تازه</span></div>\n            <div class="f-sub">با جزوهٔ مخصوص هر درس، برای مرور</div>')
days_old = re.search(r'<div class="f-vis rtl" id="days">.*?</div>\n          </div>', s, re.S).group(0)
DAYS = [("شنبه", False), ("یکشنبه", True), ("دوشنبه", False), ("سه‌شنبه", True), ("چهارشنبه", False), ("پنجشنبه", True)]
days_new = '<div class="f-vis rtl" id="days">\n' + "".join(
    f'            <div class="day{" on" if on else ""}" style="left: 230px; top: {20 + i * 104}px">{"<i></i>" if on else ""}{d}</div>\n'
    for i, (d, on) in enumerate(DAYS)) + "          </div>"
s = s.replace(days_old, days_new)
r('<div class="f-sub">مهم‌ترین خبرها، کوتاه و خلاصه، با هم</div>', '<div class="f-sub">یکشنبه، سه‌شنبه و پنجشنبه؛ کوتاه و خلاصه</div>')

# ---- video clip timings (+8 s for the scenes after the new one)
r('src="assets/clips/simulators.mp4" data-start="19.7"', 'src="assets/clips/simulators.mp4" data-start="27.7"')
r('src="assets/clips/home-ring-clean.mp4" data-start="24" data-duration="8"', 'src="assets/clips/home-ring-clean.mp4" data-start="32" data-duration="8"')

# ---- CTA: Telegram group link + QR
r('<img src="assets/telegram-qr.svg" alt="" /><span>AI_Community</span>', '<img src="assets/telegram-group-qr.svg" alt="" /><span>Telegram Group</span>')
r('<span>t.me/+Orw2hE3tq3thMzNk</span>', '<span>t.me/+B70Edyob54Q0NWVk</span>')
r('<div id="s5-sub">همین امروز بیا و اولین قدمت را بردار.</div>', '<div id="s5-sub">عضو گروه تلگرام شو و همین امروز اولین قدمت را بردار.</div>')

# ---- audio
r('<audio id="music" src="assets/audio/music.mp3" data-start="0" data-duration="32"', '<audio id="music" src="assets/audio/music.mp3" data-start="0" data-duration="40"')
for a, b in [('id="sfx-pop" src="assets/sfx/notification.mp3" data-start="12.0"', 'id="sfx-pop" src="assets/sfx/notification.mp3" data-start="20.0"'),
             ('data-start="17.85"', 'data-start="25.85"'), ('data-start="19.85"', 'data-start="27.85"'),
             ('data-start="21.85"', 'data-start="29.85"'), ('data-start="25.6" data-duration="1.8"', 'data-start="33.6" data-duration="1.8"')]:
    r(a, b)

# ---- timeline script (rewritten for 40 s)
script = open("/tmp/claude-0/scratchpad/group_timeline.js", encoding="utf-8").read()
i = s.rindex("    <script>")
j = s.rindex("    </script>") + len("    </script>")
s = s[:i] + script + s[j:]
open("/home/user/video-motion/videos/community-group/index.html", "w", encoding="utf-8").write(s)
print("ok", len(s))
