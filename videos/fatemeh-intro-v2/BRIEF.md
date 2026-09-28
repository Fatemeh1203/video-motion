---
workflow: general-video
flow: automation
storyboard: no
message: "سایت فاطمه شمس حالا «فضای هوشمند» است: شش دروازه به شش جهان سه‌بعدی؛ بیا ببین و به کامیونیتی بپیوند"
destination: youtube
aspect: 1920x1080
language: fa
audience: Persian-speaking AI learners, teachers and professionals
length: 112s
angle: site relaunch promo — the new portal home and section worlds, captured live
---

## Intent

Second promo, rebuilt around the site's new look (repo `Fatemeh1203/project-site-2026`,
commits ba53a44 / b7d2a29 / 72b9258): the "intelligence space" theme, the rotating ring of
six portals on the home page, and one interactive 3D world per section. Same constraints as
the first video: Persian (RTL), at most 2 minutes, 16:9, advertising role.

## Assets

- assets/clips/*.mp4 — real footage of the running site (local build, dark theme), recorded
  frame-by-frame at 30 fps with a virtual clock (scripts/capture-site.cjs).
  `*-clean` clips hide all page DOM so only the WebGL world shows (the seed sample
  projects/agents/files are placeholders and must not appear).
- assets/poster-dark-wide.webp — the site's own portal-scene poster.
- assets/telegram-qr.svg — QR for https://t.me/+Orw2hE3tq3thMzNk.

## Customizations

- Palette from the site's globals.css (dark): ground #080b15, mint #89fff0, brand ramp
  #a8ffef / #ae9cff, portal colours --portal-1..6; gradient headline like the site hero.
- Copy from messages/fa.json (home hero) and the portal kickers in (site)/page.tsx.
- Title on screen stays «توسعه‌دهنده و مربی هوش مصنوعی» (the user's choice for video 1).

## Notes

- Never split Persian words into letters; animate word-level.
