---
workflow: general-video
flow: automation
storyboard: no
message: "یک هفته در کامیونیتی هوش مصنوعی: هر روز یک درس، روزهای فرد خبر، جزوه برای هر درس، شبیه‌سازهای ویژهٔ اعضا و پرسش و پاسخ شبانه‌روزی"
destination: instagram-reels
aspect: 1080x1920
language: fa
audience: Persian speakers who want to learn AI tools
length: 56s
angle: a week in the community — a Saturday-to-Friday strip; each day opens one real part of the community, then the Telegram invite
---

## Intent

User asked for «یه انیمیشن خوب برای کامیونیتی» with the free Dilara voice, after hearing
edge-tts samples. Picked the «یک هفته در کامیونیتی» concept and 9:16 for Reels.

## Assets

- Narration: edge-tts `fa-IR-FaridNeural` (male), rate +20%, built by `scripts/build_voice.py` (free, no account). First cut used Dilara −5%; she asked for a male voice, faster, and picked the spelling «فاطِمه شَمس» for her name.
- Music: `scripts/make-bgm.py` ambient bed, side-chain ducked under the narration with ffmpeg.
- SFX: pop / whoosh / notification / riser / impact from the earlier reel.
- `assets/telegram-group-qr.svg` → https://t.me/+B70Edyob54Q0NWVk

## Notes

- Narrator is third person (the voice is not Fatemeh), so the video never says «من فاطمه شمس».
- Facts only from `.claude/skills/video-studio/references/brand.md`: daily lessons, AI news on
  odd days (یکشنبه، سه‌شنبه، پنجشنبه), a handout per lesson, free simulators for members
  (math, physics, programming), Q&A with Fatemeh around the clock, the real lesson-9 sample
  (invoice → «بیشترین سهم فروش: کیف‌های چرمی، ۴۵٪»).
- Days are a storytelling device; only the odd-day news is tied to real weekdays.
