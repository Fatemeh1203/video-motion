# Brand and facts

## Person

- Name: فاطمه شمس (Fatemeh Shams). On-screen title: «توسعه‌دهنده و مربی هوش مصنوعی».
  (The site's about page says «طراح شبیه‌سازهای آموزشی و ایجنت‌های هوشمند»; she chose the
  first one for videos.)
- GitHub: Fatemeh1203. Site repo: `Fatemeh1203/project-site-2026`. Community repo:
  `Fatemeh1203/AI_Community_with_Renascist` (README only).

## Telegram AI community (AI_Community)

Confirmed by her; use freely:

- **Telegram group invite (use this for new videos, from 2026-10-09):** `https://t.me/+B70Edyob54Q0NWVk`
  (QR: `assets/telegram-group-qr.svg`, decoded and verified).
- Older channel invite: `https://t.me/+Orw2hE3tq3thMzNk` (QR: `assets/telegram-qr.svg`).
- Core promise to stress: practical training on **all the world's AI tools**, as a **daily lesson
  (درسنامهٔ روزانه)** with a handout for each lesson.
- «جای کسانی است که می‌خواهند متحول شوند».
- **Daily lessons**: practical training on all AI tools, every day, step by step.
- **AI news on odd days (روزهای فرد)** = یکشنبه، سه‌شنبه، پنجشنبه. (Iranian week: زوج = شنبه،
  دوشنبه، چهارشنبه; فرد = یکشنبه، سه‌شنبه، پنجشنبه. She caught this mistake once; never swap them.)
- **A handout (جزوه) for every lesson**, kept in the community to review any time.
- **Free educational simulators, only for community members** (the site has 20: math,
  physics, programming labs).
- **Q&A topic; she is present 24/7** («شبانه‌روز کنارت هستم»).
- Topics (from her Telegram screenshot): ابزار هوش مصنوعی، بانک پرامپت ویژهٔ معلم،
  نمونه‌کارها، ایده، فایل‌ها، پرسش و پاسخ، شبیه‌ساز، General.
- Real sample lesson: «درس ۹»: upload a photo of your purchase invoice and ask for an
  analysis; sample output «تحلیل فروش: بیشترین سهم فروش متعلق به کیف‌های چرمی با ۴۵ درصد
  درآمد کل است». Hashtags: #هوش_مصنوعی #آموزش_کاربردی #آپلود_فایل #تحلیل_داده.

Do not invent lesson titles, member counts or testimonials.

## Site: "THE INTELLIGENCE SPACE" (current theme, dark)

- Hero copy: eyebrow «به جهان من خوش آمدی», title «ایده‌ها، اینجا جان می‌گیرند.»,
  subtitle «مرز میان تخیل و هوش مصنوعی را رد کن. هر دروازه، شروع یک دنیای تازه است.»
- Home: a rotating ring of six 3D portals. Each section has its own interactive 3D world:
  about (crystal), portfolio (floating frames, THE ARCHIVE), agents (node network,
  AGENT DISTRICT), simulators (wave terrain, SIMULATION LAB), resources/files
  (holographic crates, SUPPLY DEPOT), community (particles, COLLECTIVE SPACE); about =
  THE ORIGIN.
- Portfolio/agents/files content in the DB is **seed placeholder**: never show it.

## Palette (from the site's `globals.css`, dark theme)

```css
--bg: #080b15;  --bg-2: #0b1122;  --fg: #eff4ff;  --muted: #b3bdd8;
--mint: #89fff0; --brand-1: #a8ffef; --brand-2: #ae9cff; --navy: #1d2542;
--p1: #91ffea; --p2: #b39aff; --p3: #77caff; --p4: #ffbf86; --p5: #ff94ba; --p6: #ddf998;
--glass: linear-gradient(145deg, rgba(23,29,48,.9), rgba(9,14,26,.9));
--glass-line: rgba(255,255,255,.14);
```

Headline accent = gradient text `linear-gradient(100deg, #ae9cff, #a8ffef 70–80%)` on words,
like the site hero. Portal colours p1–p6 map to: about, portfolio, agents, simulators,
files, community.

(Older warm "dawn" theme, used in video 1: bg #11142a, cream #f2ede4, gold #e5b055, peach
#fdb99b, violet #cf8bf3. Use only if she asks for the old look.)

## Typography

Vazirmatn only (the site's font), local woff2 in `assets/fonts/`. Display 800–900, body
400–500. Video sizes: headline 90–130px, body 34–42px, labels ≥ 22px. Persian digits
(۰–۹) in copy; Latin names (ChatGPT, n8n) stay Latin.

## Past projects in the video-motion repo (reuse, do not rebuild)

- `videos/fatemeh-intro`: v1, dawn theme, 114s.
- `videos/fatemeh-intro-v2`: site relaunch, live 3D footage in `assets/clips/*.mp4`.
- `videos/fatemeh-community`: community story, 120s, narration pipeline in `voice/`,
  scene files `compositions/s1-hook.html` … `s9-cta.html`: the best template to start from.
