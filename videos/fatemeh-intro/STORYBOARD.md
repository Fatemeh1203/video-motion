---
format: 1920x1080
duration: 114s
message: "فاطمه شمس ابزار و ایجنت هوش مصنوعی می‌سازد، آموزش می‌دهد، و شما را به سایت و کامیونیتی تلگرامش دعوت می‌کند"
arc: Hook → Who → What I build → The site → Your project → Community → Join
audience: Persian-speaking AI learners
mode: autonomous
music: warm dawn ambient, 96 BPM, D major (scripts/make-bgm.py)
---

Design: dark dawn canvas #11142a, cream #f2ede4 text, gold #e5b055 accent,
peach #fdb99b / violet #cf8bf3 / sky #9ccbf0 as the site's card accents.
Vazirmatn 900/700 display, 400/300 body. RTL throughout.

## Frame 1 — Dawn hook
- status: animated
- src: compositions/s1-hook.html
- duration: 10s
- transition_in: cut
- blueprint: kinetic-type-beats (rules: waterfall-entry, ambient-glow-bloom, multi-phase-camera)
- scene: The site's dawn parallax rises; «از ایده تا ابزاری که هر روز کار می‌کند».

## Frame 2 — Who I am
- status: animated
- src: compositions/s2-intro.html
- duration: 12s
- transition_in: crossfade
- blueprint: logo-assemble-lockup (rules: waterfall-entry, spring-pop-entrance, orbit-3d-entry)
- scene: «سلام، من فاطمه شمس هستم» + title + three focus lines, orbiting monogram.

## Frame 3 — What I build
- status: animated
- src: compositions/s3-pillars.html
- duration: 15s
- transition_in: crossfade
- blueprint: grid-card-assemble (rules: spring-pop-entrance, svg-icon-enrichment, sine-wave-loop)
- scene: Three cards — شبیه‌ساز، ایجنت، ابزار وب — then the site tagline.

## Frame 4 — The site
- status: animated
- src: compositions/s4-site.html
- duration: 24s
- transition_in: crossfade
- blueprint: device-surface-showcase → kinetic list → grid-card-assemble (rules: multi-phase-camera, waterfall-entry, spring-pop-entrance)
- scene: Browser mock of the home hero, the full-screen menu, then the feature grid.

## Frame 5 — Your project
- status: animated
- src: compositions/s5-request.html
- duration: 10s
- transition_in: crossfade
- blueprint: prompt-type-submit-generate (rules: discrete-text-sequence, press-release-spring)
- scene: The «ثبت پروژه» form types a challenge and submits.

## Frame 6 — Community
- status: animated
- src: compositions/s6-community.html
- duration: 29s
- transition_in: crossfade
- blueprint: grid-card-assemble → dataviz-countup → kinetic-type-beats (rules: waterfall-entry, stat-bars-and-fills, counting-dynamic-scale, kinetic-beat-slam)
- scene: Telegram topics list, the lesson post with a 45% count-up, then «بپرس. یاد بگیر. بساز.»

## Frame 7 — Join
- status: animated
- src: compositions/s7-cta.html
- duration: 14s
- transition_in: crossfade
- blueprint: logo-assemble-lockup (rules: spring-pop-entrance, ambient-glow-bloom)
- scene: Dawn returns; QR + invite link + name lockup.
