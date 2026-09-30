// Records the live site's WebGL scenes frame-by-frame at a fixed 30 fps.
//
// performance.now and requestAnimationFrame are replaced with a virtual clock
// that only advances when this script pumps a frame, so every screenshot is
// exactly 1/30 s after the previous one no matter how slowly SwiftShader
// renders. Frames go to <out>/<clip>/00000.png and are encoded with ffmpeg.
//
// usage: node capture-site.cjs <puppeteer-core dir> <base url> <out dir> [clip ...]

const path = require("path");
const fs = require("fs");
const { execFileSync } = require("child_process");

const [, , PUP, BASE, OUT, ...only] = process.argv;
const puppeteer = require(PUP);
const FPS = 30;
const DT = 1000 / FPS;

// pointer path helpers (viewport px)
const orbit = (cx, cy, rx, ry, turns) => (k) => [cx + rx * Math.cos(k * turns * 2 * Math.PI), cy + ry * Math.sin(k * turns * 2 * Math.PI)];
const sweep = (x0, y0, x1, y1) => (k) => [x0 + (x1 - x0) * k, y0 + (y1 - y0) * (0.5 - 0.5 * Math.cos(k * Math.PI))];

// clean: hide every DOM layer except the WebGL canvas (the seed sample
// projects/agents/files are placeholders and must not appear in the video)
const CLIPS = [
  { name: "home-ring", url: "/fa", seconds: 14, pointer: null },
  { name: "home-ring-clean", url: "/fa", seconds: 10, pointer: null, clean: true },
  { name: "about", url: "/fa/about", seconds: 6, pointer: orbit(960, 560, 320, 180, 0.8) },
  { name: "about-clean", url: "/fa/about", seconds: 6, pointer: orbit(960, 560, 320, 180, 0.8), clean: true },
  { name: "portfolio-clean", url: "/fa/portfolio", seconds: 5, pointer: sweep(300, 700, 1620, 500), clean: true },
  { name: "agents-clean", url: "/fa/agents", seconds: 5, pointer: sweep(1600, 820, 320, 640), clean: true },
  { name: "simulators", url: "/fa/simulators", seconds: 6, pointer: sweep(200, 900, 1700, 880) },
  { name: "resources-clean", url: "/fa/resources", seconds: 5, pointer: orbit(960, 700, 520, 200, 0.7), clean: true },
  { name: "community-clean", url: "/fa/community", seconds: 6, pointer: orbit(960, 560, 420, 220, 1.0), clean: true },
];
const CLEAN_CSS = "body * { visibility: hidden !important; } canvas { visibility: visible !important; }";

const VCLOCK = () => {
  const realNow = performance.now.bind(performance);
  let t = realNow();
  let queue = [];
  let id = 0;
  performance.now = () => t;
  window.requestAnimationFrame = (cb) => {
    queue.push({ id: ++id, cb });
    return id;
  };
  window.cancelAnimationFrame = (x) => {
    queue = queue.filter((e) => e.id !== x);
  };
  window.__pump = (n, dt) => {
    for (let i = 0; i < n; i++) {
      t += dt;
      const run = queue;
      queue = [];
      for (const e of run) {
        try {
          e.cb(t);
        } catch (err) {
          console.error("raf", err && err.message);
        }
      }
    }
    return queue.length;
  };
  try {
    localStorage.setItem("theme", "dark");
  } catch (e) {}
};

(async () => {
  const browser = await puppeteer.launch({
    executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    args: ["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--hide-scrollbars"],
  });
  for (const clip of CLIPS) {
    if (only.length && !only.includes(clip.name)) continue;
    const dir = path.join(OUT, clip.name);
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });
    page.on("pageerror", (e) => console.log("PAGEERR", clip.name, e.message));
    await page.evaluateOnNewDocument(VCLOCK);
    await page.goto(BASE + clip.url, { waitUntil: "networkidle0", timeout: 90000 });
    // an interaction starts the scene loader; then warm up in pseudo-real time
    await page.mouse.move(900, 560);
    await page.mouse.move(960, 600);
    for (let i = 0; i < 240; i++) {
      await page.evaluate((dt) => window.__pump(1, dt), DT);
      await new Promise((r) => setTimeout(r, 25));
    }
    if (clip.clean) await page.addStyleTag({ content: CLEAN_CSS });
    const frames = Math.round(clip.seconds * FPS);
    for (let f = 0; f < frames; f++) {
      if (clip.pointer) {
        const [x, y] = clip.pointer(f / frames);
        await page.mouse.move(x, y);
      }
      await page.evaluate((dt) => window.__pump(1, dt), DT);
      await page.screenshot({ path: path.join(dir, String(f).padStart(5, "0") + ".png") });
    }
    await page.close();
    execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(FPS), "-i", path.join(dir, "%05d.png"), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", path.join(OUT, clip.name + ".mp4")]);
    console.log("clip", clip.name, frames, "frames");
  }
  await browser.close();
})();
