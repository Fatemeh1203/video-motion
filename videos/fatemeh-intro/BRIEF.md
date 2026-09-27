---
workflow: general-video
flow: automation
storyboard: no
message: "فاطمه شمس ابزار و ایجنت هوش مصنوعی می‌سازد، آموزش می‌دهد، و شما را به سایت و کامیونیتی تلگرامش دعوت می‌کند"
destination: youtube
aspect: 1920x1080
language: fa
audience: Persian-speaking learners, teachers and professionals interested in practical AI
length: 114s
angle: personal brand promo — person → work → site → community → join
---

## Intent

A Persian (RTL) promotional motion video, at most 2 minutes, that introduces
Fatemeh Shams ("توسعه‌دهنده و مربی هوش مصنوعی"), her personal site
(repo `Fatemeh1203/project-site-2026`) and her Telegram AI community
(`AI_Community`, repo `Fatemeh1203/AI_Community_with_Renascist`).
Advertising role; the theme should match her work — the site's own dawn
palette, Vazirmatn type and parallax mountain scene.

## Assets

- assets/scene/*.webp — the site's own dawn parallax layers (public/scene/dawn, night); opening and closing scenes.
- assets/fonts/vazirmatn-* — the site's font (Vazirmatn, from @fontsource/vazirmatn).
- assets/telegram-qr.svg — QR for https://t.me/+Orw2hE3tq3thMzNk (CTA).
- Telegram screenshot (chat) — community topic names and the lesson post (sales-analysis example, hashtags) are taken from it.

## Customizations

- Community invite link on the end card: https://t.me/+Orw2hE3tq3thMzNk
- On-screen Persian text only (no Persian TTS available offline); synthesized ambient music bed (scripts/make-bgm.py) + bundled SFX.

## Notes

- The site's seed data (sample name/projects/agents) is placeholder — do not show those names; describe site sections and features instead.
- Never split Persian words into letters (breaks cursive joining); animate word-level.
