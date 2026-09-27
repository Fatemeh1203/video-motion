---
workflow: general-video
flow: automation
storyboard: no
message: "آموزشگاه علمی فردا: یادگیری علمی و کاربردی، با شبیه‌سازها و هوش مصنوعی — از امروز به فردا بیایید"
destination: youtube
aspect: 1920x1080
language: fa
audience: Persian-speaking students, university students, teachers, parents and partner schools
length: 120s
angle: institute promo — hook question → brand reveal → learning promise → offerings → see it (simulation + AI) → flexible schedule → who it's for → CTA
---

## Intent

A Persian (RTL) advertising motion video, two minutes long, for «آموزشگاه علمی فردا»
(https://aifardainstitute.ir/), attractive and audience-friendly.

## Assets

- assets/img/farda-mark-navy.png / farda-mark-white.png — the institute's calligraphic logo
  (repo `Fatemeh1203/Farda-Institute`, `assets/farda-logo.png`), recolored on transparency,
  slogan line cropped off (the slogan is set in type instead).
- Palette taken from the institute's own page CSS (`--sky-1..4`, `--ink`, `--link`, `--dot`) and
  its floating-cloud look; Vazirmatn type (same font the page uses).
- assets/audio/bgm.mp3 — synthesized music bed (scripts/make-bgm.py, 104 BPM, E major).
- assets/sfx/* — bundled media-use SFX.

## Customizations

- Slogan «از امروز به فردا بیایید» and name «آموزشگاه علمی فردا» from the institute page.
- Director credit on the end card: فاطمه شمس.
- On-screen Persian text only (no Persian TTS available offline).

## Notes

- aifardainstitute.ir was blocked by this environment's network policy, so no course list,
  prices, phone numbers or statistics were available. The video makes no numeric or
  price claims; offerings are described at category level (science classes, applied AI,
  smart simulators, personal weekly plan, in-person + online) — confirm/adjust with the owner.
- Never split Persian words into letters (breaks cursive joining); animate word-level.
