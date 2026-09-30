# Recording the live site (3D footage)

The public demo (fatemeh1203.github.io) is blocked by the proxy, so run the site locally,
exactly like its `.github/workflows/static-demo.yml`:

```bash
apt-get install -y postgresql && service postgresql start
su postgres -c "psql -c \"ALTER USER postgres PASSWORD 'postgres';\"" && su postgres -c "createdb app"
cd /home/user/project-site-2026   # clone Fatemeh1203/project-site-2026 first (add_repo)
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app AUTH_SECRET=local AUTH_TRUST_HOST=true NEXT_TELEMETRY_DISABLED=1
npm ci
psql "$DATABASE_URL" -c 'CREATE EXTENSION IF NOT EXISTS pg_trgm'
npx prisma db push && npx prisma db seed && npm run db:seed-simulators
psql "$DATABASE_URL" -f scripts/static-demo/demo-content.sql
npx next build && nohup npx next start -p 3100 > /tmp/next.log 2>&1 &
```

Then record (puppeteer-core ships in the npx cache after any `npx hyperframes` run):

```bash
PUP=$(ls -d ~/.npm/_npx/*/node_modules/puppeteer-core | head -1)
node scripts/capture-site.cjs "$PUP" http://localhost:3100 /tmp/clips home-ring about-clean
```

- Clips are listed in `CLIPS` inside the script; `clean: true` hides every DOM layer except
  the WebGL canvas (use for portfolio, agents, resources, community, whose content is seed
  placeholder).
- The script swaps `performance.now`/`requestAnimationFrame` for a virtual clock, so the
  output is a smooth 30 fps whatever the render speed (~1–1.5 s per frame; run 3 workers in
  parallel on 4 cores).
- Re-encode for HyperFrames: `ffmpeg -framerate 30 -i dir/%05d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -g 30 -keyint_min 30 -movflags +faststart clip.mp4`.
- Already-recorded clips live in `videos/fatemeh-intro-v2/assets/clips/`: reuse them unless
  the site changed.
