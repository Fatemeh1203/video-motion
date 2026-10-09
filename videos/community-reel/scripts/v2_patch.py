"""Reels v2 edits on top of build_reel.py output (run build_reel.py first, then this)."""
s = open("index.html", encoding="utf-8").read()
def r(a, b):
    global s
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b, 1)

# ---------- 1. opening: no black first frame, bigger first line, question at ~1.6 s
r('tl.fromTo("#s1", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0);\n', "")
r("      #s1-a { left: 70px; right: 70px; top: 830px; font-size: 62px; line-height: 1.4; }",
  "      #s1 { opacity: 1; }\n      #s1-a { left: 60px; right: 60px; top: 700px; font-size: 118px; font-weight: 900; line-height: 1.3; text-wrap: balance; text-shadow: 0 6px 40px rgba(8, 11, 21, 0.9); }")
r('tl.fromTo("#s1-a", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 0.15);',
  'tl.fromTo("#s1-a", { scale: 1.06 }, { scale: 1, duration: 1.4, ease: "sine.out" }, 0);')
r("const at = 0.25 + i * (B / 4);", "const at = 0.05 + i * (B / 5);")
r('tl.to("#s1-a", { opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }, 1.75);',
  'tl.to("#s1-a", { opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }, 1.35);')
r('tl.fromTo("#s1-b", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power4.out" }, 2.0);',
  'tl.fromTo("#s1-b", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power4.out" }, 1.6);')
r('tl.to("#s1-b", { scale: 1.06, duration: 1.3, ease: "sine.in" }, 2.4);',
  'tl.to("#s1-b", { scale: 1.06, duration: 1.7, ease: "sine.in" }, 2.0);')

r('["Copilot", "#77caff", 780, 560], ["Cursor", "#ff94ba", 330, 640], ["n8n", "#ff94ba", 700, 680],',
  '["Copilot", "#77caff", 790, 500], ["Cursor", "#ff94ba", 300, 580], ["n8n", "#ff94ba", 720, 600],')

# ---------- 2. features: overlap the hand-offs so no frame shows only the eyebrow
r("""          tl.fromTo(f, { opacity: 0 }, { opacity: 1, duration: 0.12 }, t0);
          tl.fromTo(f + " .f-title", { opacity: 0, x: 120, filter: "blur(8px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.4, ease: "power4.out" }, t0);
          tl.fromTo(f + " .f-sub, " + f + " .badge", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, t0 + B);
          tl.fromTo(f + " .f-vis", { opacity: 0, x: -120, scale: 0.92 }, { opacity: 1, x: 0, scale: 1, duration: 0.45, ease: "power4.out" }, t0 + 0.05);
          if (i < 3) {
            tl.to(f, { opacity: 0, x: -60, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }, t0 + 1.8);
          }""",
"""          const tin = i === 0 ? t0 : t0 - 0.14; // enter while the previous card is still leaving
          tl.fromTo(f, { opacity: 0 }, { opacity: 1, duration: 0.01 }, tin);
          tl.fromTo(f + " .f-title", { opacity: i === 0 ? 0 : 0.4, x: 120, filter: "blur(8px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }, tin);
          tl.fromTo(f + " .f-sub, " + f + " .badge", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, tin + 0.25);
          tl.fromTo(f + " .f-vis", { opacity: i === 0 ? 0 : 0.4, x: -120, scale: 0.92 }, { opacity: 1, x: 0, scale: 1, duration: 0.35, ease: "power4.out" }, tin);
          if (i < 3) {
            tl.to(f, { opacity: 0, x: -60, filter: "blur(8px)", duration: 0.1, ease: "power2.in" }, t0 + 1.8);
          }""")

# ---------- 3. Q&A card: new copy + neon chat icon instead of the 24/7 ring
r("""            <div id="ring-wrap">
              <svg viewBox="0 0 460 460"><circle cx="230" cy="230" r="200" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="22" /><circle id="ring-arc" cx="230" cy="230" r="200" fill="none" stroke="#89fff0" stroke-width="22" stroke-linecap="round" stroke-dasharray="1257" stroke-dashoffset="1257" transform="rotate(-90 230 230)" /></svg>
              <div id="ring-num"><b>۲۴/۷</b><span>کنارت هستم</span></div>
            </div>""",
"""            <div id="chat-icon">
              <svg viewBox="0 0 460 420" width="460" height="420">
                <path id="chat-bubble" d="M90 60 H370 a50 50 0 0 1 50 50 V250 a50 50 0 0 1 -50 50 H210 L130 370 V300 H90 a50 50 0 0 1 -50 -50 V110 a50 50 0 0 1 50 -50 Z" fill="rgba(137,255,240,0.06)" stroke="#89fff0" stroke-width="16" stroke-linejoin="round" stroke-dasharray="1400" stroke-dashoffset="1400" />
                <circle class="chat-dot" cx="160" cy="180" r="22" fill="#89fff0" />
                <circle class="chat-dot" cx="230" cy="180" r="22" fill="#89fff0" />
                <circle class="chat-dot" cx="300" cy="180" r="22" fill="#89fff0" />
              </svg>
            </div>""")
r('<div class="f-title"><span class="g">شبانه‌روز</span> کنارت هستم</div>\n            <div class="f-sub">هر جا گیر کنی، بپرس؛ بی‌جواب نمی‌مانی</div>',
  '<div class="f-title">سؤالت <span class="g">بی‌جواب نمی‌مونه</span></div>\n            <div class="f-sub">هر جا گیر کنی، کنارت هستم</div>')
r("      #ring-wrap { left: 170px; top: 20px; }",
  "      #chat-icon { position: absolute; left: 170px; top: 40px; width: 460px; height: 420px; filter: drop-shadow(0 0 18px rgba(137, 255, 240, 0.55)) drop-shadow(0 0 48px rgba(137, 255, 240, 0.25)); }\n      #chat-icon .chat-dot { opacity: 0; }")
r("""        tl.fromTo("#ring-arc", { strokeDashoffset: 1257 }, { strokeDashoffset: 0, duration: 1.5, ease: "power2.inOut" }, 30.1);
        tl.fromTo("#ring-num b", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, 30.2);""",
"""        tl.fromTo("#chat-bubble", { strokeDashoffset: 1400 }, { strokeDashoffset: 0, duration: 0.9, ease: "power2.inOut" }, 29.95);
        gsap.utils.toArray("#chat-icon .chat-dot").forEach(function (d, i) {
          tl.fromTo(d, { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, 30.5 + i * 0.12);
          tl.fromTo(d, { y: 0 }, { y: -14, duration: 0.2, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false }, 31.0 + i * 0.12);
        });""")

# ---------- 4. final scene: no QR, bigger lower link, scarcity + members-only chips, comment CTA as last line
r('        <div id="s5-qr"><img src="assets/telegram-group-qr.svg" alt="" /><span>Telegram Group</span></div>\n', "")
r("""        <div id="s5-sign" class="rtl"><span>به همراهی</span><i></i><b>دکتر فاطمه شمس</b></div>""",
"""        <div id="s5-tags" class="rtl"><span class="tag">ظرفیت محدود</span><span class="tag">فقط ویژهٔ اعضا</span></div>
        <div id="s5-sign" class="rtl"><span>به همراهی</span><i></i><b>دکتر فاطمه شمس</b></div>
        <div id="s5-comment" class="rtl"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#89fff0" stroke-width="2.2" stroke-linejoin="round"><path d="M4 5h16v11H10l-4 3.5V16H4z" /></svg><span>برای اطلاع از شرایط، کلمهٔ <em>«هوش مصنوعی»</em> را کامنت کن تا شرایط برایت ارسال شود.</span></div>""")
r("      #s5-qr { left: 320px; top: 850px; }\n", """      #s5-link { position: absolute; left: 0; right: 0; top: 610px; width: fit-content; margin: 0 auto; gap: 24px; padding: 24px 46px 24px 26px; font-size: 58px; border-width: 4px; box-shadow: 0 0 60px rgba(137, 255, 240, 0.35); }
      #s5-link .plane { width: 92px; height: 92px; }
      #s5-link .plane svg { width: 50px; height: 50px; }
      #s5-tags { position: absolute; left: 0; right: 0; top: 1030px; display: flex; justify-content: center; gap: 18px; }
      .tag { display: inline-block; padding: 10px 26px; border-radius: 30px; border: 2px solid rgba(137, 255, 240, 0.7); background: rgba(8, 11, 21, 0.85); color: var(--mint); font-size: 34px; font-weight: 800; box-shadow: 0 0 24px rgba(137, 255, 240, 0.2); opacity: 0; }
      #s5-comment { position: absolute; left: 90px; right: 90px; top: 1330px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; font-size: 38px; font-weight: 600; line-height: 1.5; color: var(--fg); text-align: center; opacity: 0; }
      #s5-comment span { text-wrap: balance; }
      #s5-comment em { font-style: normal; font-weight: 900; color: var(--mint); }
      #s5-comment svg { flex: none; }
""")
r("      #s5-sign { left: 0; right: 0; bottom: auto; top: 1430px; width: fit-content; margin: 0 auto; }",
  "      #s5-sign { left: 0; right: 0; bottom: auto; top: 1160px; width: fit-content; margin: 0 auto; }")
r('        tl.fromTo("#s5-qr", { opacity: 0, scale: 0.5, rotation: -6 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.6)" }, 33.6);\n', "")
r("""        tl.fromTo(
          "#s5-qr",
          { boxShadow: "0 0 0 3px rgba(137, 255, 240, 0.6), 0 40px 120px rgba(0, 0, 0, 0.6)" },
          { boxShadow: "0 0 0 3px rgba(137, 255, 240, 1), 0 0 140px rgba(137, 255, 240, 0.5)", duration: 1.0, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false },
          35.0,
        );""",
"""        gsap.utils.toArray("#s5 .tag").forEach(function (t, i) {
          tl.fromTo(t, { opacity: 0, y: 20, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(2.2)" }, 35.0 + i * 0.2);
        });
        tl.fromTo("#s5-link", { boxShadow: "0 0 60px rgba(137, 255, 240, 0.35)" }, { boxShadow: "0 0 110px rgba(137, 255, 240, 0.7)", duration: 1.0, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false }, 35.4);
        tl.fromTo("#s5-comment", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 36.2);""")
r('tl.fromTo("#s5-link", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 34.5);',
  'tl.fromTo("#s5-link", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 34.2);')
r('<audio id="sfx-spark" src="assets/sfx/sparkle.mp3" data-start="33.6"', '<audio id="sfx-spark" src="assets/sfx/sparkle.mp3" data-start="34.2"')
open("index.html", "w", encoding="utf-8").write(s)
print("v2 patched")
