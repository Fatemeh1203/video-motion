# explainer-panel-reel: not found

Fetch date: 2026-11-11 (curl through the session proxy)

Neither `explainer-panel-reel` nor `cutout-grid-reel` is published on the public skills page at https://aanshai.vercel.app/skills. No skill text was saved.

## What was tried

| URL | HTTP status | Result |
|---|---|---|
| https://aanshai.vercel.app/skills | 200 (text/html, ~1.36 MB) | Next.js page. Each skill is embedded as a prompt that starts "Create a Claude Code skill named ...". 92 skills are listed. The strings `explainer-panel-reel` and `cutout-grid-reel` appear 0 times. |
| https://aanshai.vercel.app/skills/explainer-panel-reel | 404 | Not found page |
| https://aanshai.vercel.app/skills/explainer-panel-reel/SKILL.md | 404 | Not found page |
| https://aanshai.vercel.app/skills/explainer-panel-reel/raw | 404 | Not found page |
| https://aanshai.vercel.app/skills/explainer-panel-reel/download | 404 | Not found page |
| https://aanshai.vercel.app/api/skills/explainer-panel-reel | 404 | Not found page |
| https://aanshai.vercel.app/api/skills | 404 | Not found page |
| https://aanshai.vercel.app/skills/cutout-grid-reel | 404 | Not found page |
| https://aanshai.vercel.app/skills.json | 404 | Not found page |
| https://aanshai.vercel.app/skills/paper-cutout (control: a skill that is listed) | 404 | Per-skill pages don't exist. All skill content is on the /skills page. |
| 9 JS bundles under https://aanshai.vercel.app/_next/static/ (the scripts the /skills page loads) | 200 | Neither name appears. The only API routes they reference are `/api/access`, `/api/create-order` and `/api/verify-payment` (payment/access endpoints). These were not called. |

The bundles reference payment endpoints, so these two skills may be paid or gated content. I did not try to get around any access control.

No license text was seen on the page.

## Skills the site does list (92, names only)

- 3d-explainer
- aarti-video
- anime-doodle-lyrics
- anime-fight
- anime-reel
- baba-pusho
- bairan-style
- beat-transition-edit
- blueprint-explainer
- breaking-news
- breakup-chat-lyrics
- business-short-form-reels
- cinema-scope
- comic-halftone
- comic-rap-video
- comic-reel
- crayon-carousel
- crayon-rain-lyrics
- dark-red-timeline-motion-graphics
- depth-ui-reel
- educational-youtube-editor
- flicker-edit
- glass-stat-card
- glass-to-neon-lyrics
- glow-lyrics
- hindi-lyric-video
- hindi-pastel-reel-edit
- ink-line-lyrics
- instagram-ui-hinglish
- iphone-style-by-aansh
- katha-video
- kids-story
- kinetic-lyrics
- kinetic-talking-head-edit
- latent-comic
- latent-reel
- led-matrix-text
- lyric-video
- madhubani-kahani
- madira-peekar-soo-gaye
- magazine-cover
- match-cut
- maut-ke-bare-mai-sochte-ho
- miniature-painting-lyrics
- minimal-love-lyrics
- minimal-lyrics
- mirzapur-video
- neon-lyrics
- neon-outline
- news-report
- night-city-lyrics
- night-glow-lyrics
- one-take-forest-lyrics
- painted-beat-edit
- paper-cutout
- particle-chart
- particle-text
- party-lyrics
- personal-broll-library
- personal-explainer
- personal-short-form-reels
- phone-chat-lyrics
- pink-spotify-clip-lyrics
- podcast-cartoon
- podcast-comic
- podcast-explainer
- podcast-reel-edit
- price-tag-zoom
- pusho-reel
- ranking-format
- rap-video
- red-kinetic-collage-edit
- red-rap-lyrics
- red-silhouette-lyrics
- red-sun-lyrics
- rgb-glitch-live
- scribble-edit
- shadow-puppet
- shutter-stack
- sketch-doodle-edit
- sketch-music-video
- sketch-to-motion
- split-screen-ldr-lyrics
- spotify-particle-lyrics
- street-interview
- talking-head-edit
- titan-anime
- triptych-timecode
- watercolor-lyrics
- watercolor-map
- woof-woof
- youtube-clips
