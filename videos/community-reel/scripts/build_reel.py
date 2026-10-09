s = open("/home/user/video-motion/videos/community-group/index.html", encoding="utf-8").read()
def r(a, b, n=1):
    global s
    assert s.count(a) >= 1, "MISSING " + a[:70]
    s = s.replace(a, b) if n == 0 else s.replace(a, b, n)
r('<meta name="viewport" content="width=1920, height=1080">', '<meta name="viewport" content="width=1080, height=1920">')
r('data-composition-id="main" data-width="1920" data-height="1080"', 'data-composition-id="main" data-width="1080" data-height="1920"')
# S1 tool chips and S3 dots placed for a tall frame, clear of the centre text band and the Reels UI
r('''          ["ChatGPT", "#91ffea", 150, 150], ["Claude", "#ffbf86", 1480, 130], ["Gemini", "#77caff", 820, 90],
          ["Midjourney", "#b39aff", 260, 820], ["Perplexity", "#91ffea", 1380, 850], ["NotebookLM", "#ddf998", 70, 340],
          ["Copilot", "#77caff", 1600, 660], ["Cursor", "#ff94ba", 560, 250], ["n8n", "#ff94ba", 1180, 290],
          ["Suno", "#ffbf86", 700, 900], ["Runway", "#b39aff", 1080, 760], ["DeepSeek", "#77caff", 420, 640],
          ["Canva AI", "#ddf998", 1300, 640], ["Gamma", "#91ffea", 960, 960],''',
'''          ["ChatGPT", "#91ffea", 90, 300], ["Claude", "#ffbf86", 730, 290], ["Gemini", "#77caff", 420, 410],
          ["Midjourney", "#b39aff", 100, 1160], ["Perplexity", "#91ffea", 580, 1440], ["NotebookLM", "#ddf998", 60, 560],
          ["Copilot", "#77caff", 780, 560], ["Cursor", "#ff94ba", 330, 640], ["n8n", "#ff94ba", 700, 680],
          ["Suno", "#ffbf86", 140, 1420], ["Runway", "#b39aff", 640, 1140], ["DeepSeek", "#77caff", 330, 1280],
          ["Canva AI", "#ddf998", 720, 1290], ["Gamma", "#91ffea", 400, 1540],''')
r("const cx = 960 - (parseFloat(el.style.left) + 120);\n          const cy = 540 - (parseFloat(el.style.top) + 30);",
  "const cx = 540 - (parseFloat(el.style.left) + 120);\n          const cy = 960 - (parseFloat(el.style.top) + 30);")
r('''const DOTS = [[1480, 880, 34, "#91ffea"], [1760, 800, 22, "#b39aff"], [1240, 860, 26, "#ffbf86"], [1820, 880, 18, "#77caff"],
          [1000, 140, 20, "#ff94ba"], [1380, 120, 28, "#ddf998"], [1720, 160, 16, "#91ffea"], [900, 920, 22, "#b39aff"]];''',
'''const DOTS = [[880, 1520, 34, "#91ffea"], [980, 1400, 22, "#b39aff"], [140, 1500, 26, "#ffbf86"], [60, 1380, 18, "#77caff"],
          [120, 230, 20, "#ff94ba"], [900, 240, 28, "#ddf998"], [500, 180, 16, "#91ffea"], [320, 1590, 22, "#b39aff"]];''')
OVR = """
      /* ================= 9:16 Reels layout (overrides) =================
         Safe area: keep copy between y 240 and y 1520, x 60-1020 (Reels UI covers the rest). */
      html, body { width: 1080px; height: 1920px; }
      #root { width: 1080px; height: 1920px; }
      .bgvid { width: 1080px; height: 1920px; }
      #glow { left: 40px; top: 460px; }
      #s1-dim { background: radial-gradient(ellipse 80% 45% at 50% 50%, rgba(8, 11, 21, 0.88), rgba(8, 11, 21, 0.6) 70%, rgba(8, 11, 21, 0.8)); }
      #s1-a { left: 70px; right: 70px; top: 830px; font-size: 62px; line-height: 1.4; }
      #s1-b { left: 50px; right: 50px; top: 760px; font-size: 124px; }
      #s2-dim { background: radial-gradient(ellipse 85% 45% at 50% 50%, rgba(8, 11, 21, 0.82), rgba(8, 11, 21, 0.5) 75%, rgba(8, 11, 21, 0.75)); }
      #s2-copy { left: 60px; right: 60px; top: 700px; }
      #s2-a { font-size: 136px; }
      #s2-b { font-size: 96px; }
      #sl-bg { background: radial-gradient(ellipse 90% 60% at 50% 45%, #131c38, #080b15 70%); }
      #sl-copy { left: 70px; right: 70px; width: auto; top: 250px; text-align: center; }
      #sl-title { justify-content: center; font-size: 84px; }
      #sl-sub { font-size: 40px; margin-top: 18px; }
      #sl-card { left: 120px; top: 790px; width: 840px; }
      #sl-grid { left: 100px; top: 1250px; width: 880px; justify-content: center; }
      #s3-bg { background: radial-gradient(ellipse 90% 60% at 50% 40%, #121a33, #080b15 70%); }
      #s3-copy { left: 70px; right: 70px; width: auto; top: 300px; text-align: center; }
      #s3-eye { font-size: 36px; line-height: 1.55; text-wrap: balance; }
      #sl-sub, .f-sub, #s5-sub { text-wrap: balance; }
      #s3-a, #s3-b { justify-content: center; font-size: 108px; }
      #s3-chat { left: 110px; top: 960px; width: 860px; }
      #s3-msg { font-size: 46px; }
      #s4-bg { background: radial-gradient(ellipse 90% 60% at 50% 55%, #10172e, #080b15 70%); }
      #s4-eye { left: 0; right: 0; top: 250px; justify-content: center; }
      .f-copy { left: 70px; right: 70px; width: auto; top: 330px; text-align: center; }
      #f4 .f-copy { width: auto; }
      .f-title { font-size: 92px; }
      .f-sub { font-size: 40px; }
      .f-vis { left: 140px; top: 720px; width: 800px; height: 640px; }
      .doc { left: 235px; }
      #days .day { left: 250px !important; }
      #sim-win { left: 20px; top: 40px; }
      #ring-wrap { left: 170px; top: 20px; }
      #s5-shade { background: radial-gradient(ellipse 90% 60% at 50% 45%, rgba(8, 11, 21, 0.9), rgba(8, 11, 21, 0.6) 70%, rgba(8, 11, 21, 0.4)); }
      #s5-copy { left: 60px; right: 60px; width: auto; top: 250px; text-align: center; }
      #s5-title { justify-content: center; font-size: 112px; }
      #s5-title .br { flex-basis: 100%; height: 0; }
      #s5-sub { font-size: 38px; }
      #s5-qr { left: 320px; top: 850px; }
      #s5-sign { left: 0; right: 0; bottom: auto; top: 1430px; width: fit-content; margin: 0 auto; }
    </style>"""
i = s.index("    </style>")
s = s[:i] + OVR.lstrip("\n").replace("    </style>", "") + "\n    </style>" + s[i + len("    </style>"):]
open("/home/user/video-motion/videos/community-reel/index.html", "w", encoding="utf-8").write(s)
s = s.replace('<span class="w">کامیونیتی</span><span class="w g">هوش</span>', '<span class="w">کامیونیتی</span><i class="br"></i><span class="w g">هوش</span>')
open("/home/user/video-motion/videos/community-reel/index.html", "w", encoding="utf-8").write(s)
print("ok")
