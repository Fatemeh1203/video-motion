    <script>
      (function () {
        const B = 0.5; // 120 BPM
        const tl = gsap.timeline({ paused: true });
        const SPRING = "back.out(1.9)";
        let seed = 7;
        const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647); // deterministic

        // ---------- parallax particles (two tiled layers, exact loop)
        function layer(id, tile, count, size, op) {
          const el = document.getElementById(id);
          const pts = [];
          for (let i = 0; i < count; i++) pts.push([rnd() * 1080, rnd() * tile, size[0] + rnd() * (size[1] - size[0]), op[0] + rnd() * (op[1] - op[0]), rnd() < 0.18]);
          for (let k = 0; k < Math.ceil(3840 / tile); k++) {
            pts.forEach(function (p) {
              const d = document.createElement("i");
              d.className = "pt";
              d.style.cssText = "left:" + p[0].toFixed(1) + "px;top:" + (p[1] + k * tile).toFixed(1) + "px;width:" + p[2].toFixed(1) + "px;height:" + p[2].toFixed(1) + "px;opacity:" + p[3].toFixed(2) + (p[4] ? ";background:#ffb547" : "");
              el.appendChild(d);
            });
          }
          tl.fromTo(el, { y: 0 }, { y: -tile, duration: 20, ease: "none" }, 0);
        }
        layer("plx-far", 480, 22, [2, 4], [0.12, 0.3]);
        layer("plx-near", 640, 14, [4, 7], [0.18, 0.4]);

        // ---------- chips: 24 bright tool pills
        const TOOLS = [["ChatGPT", "#10a37f"], ["Claude", "#d97757"], ["Gemini", "#4f8cff"], ["Midjourney", "#7c5cff"], ["Cursor", "#111111"], ["n8n", "#ea4b71"],
          ["Suno", "#f59e0b"], ["Runway", "#6d28d9"], ["Perplexity", "#20808d"], ["NotebookLM", "#84cc16"], ["Gamma", "#a855f7"], ["DeepSeek", "#4d6bfe"],
          ["Copilot", "#0ea5e9"], ["Canva AI", "#06b6d4"], ["Grok", "#111111"], ["Kling", "#22c55e"], ["ElevenLabs", "#111111"], ["Lovable", "#ef4444"],
          ["Napkin", "#f97316"], ["Ideogram", "#0f766e"], ["Pika", "#ec4899"], ["HeyGen", "#6366f1"], ["Leonardo", "#eab308"], ["Mistral", "#fb923c"]];
        const cbox = document.getElementById("chips");
        const chips = TOOLS.map(function (t, i) {
          const el = document.createElement("div");
          el.className = "chip";
          el.setAttribute("data-layout-allow-overlap", "");
          el.setAttribute("data-layout-allow-occlusion", "");
          el.style.setProperty("--c", t[1]);
          el.innerHTML = "<i></i>" + t[0];
          cbox.appendChild(el);
          return el;
        });
        // pile positions inside the text-safe box (x 90-990, y 250-1450)
        const pile = chips.map(function (el, i) {
          const w = el.offsetWidth, h = el.offsetHeight;
          const col = i % 3, row = Math.floor(i / 3);
          const x = 90 + col * 300 + rnd() * Math.max(0, 300 - w * 0.55) - 30 * rnd();
          const y = 250 + row * 140 + rnd() * 60;
          return [Math.min(990 - w, Math.max(90, x)), Math.min(1450 - h, Math.max(250, y)), (rnd() - 0.5) * 24];
        });
        const ENTER = 0.42;
        const spec = chips.map(function (el, i) {
          const w = el.offsetWidth;
          const side = i % 4;
          const p = pile[i];
          const s = side === 0 ? [-w - 60, p[1]] : side === 1 ? [1140, p[1]] : side === 2 ? [p[0], -140] : [p[0], 1980];
          const a = -0.5 + i * 0.065; // staggered arrivals, some already mid-flight at frame 0
          const f = Math.min(1, Math.max(0, -a / ENTER)); // fraction travelled at t = 0
          const f0 = [s[0] + (p[0] - s[0]) * f, s[1] + (p[1] - s[1]) * f];
          el.style.left = "0px";
          el.style.top = "0px";
          return { el: el, p: p, s: s, a: a, f0: f0, visible0: a < 0 };
        });
        spec.forEach(function (c) {
          // 0-1.5: fly in and pile up (spring), slight jostle
          if (c.a < 0) {
            tl.fromTo(c.el, { x: c.f0[0], y: c.f0[1], rotation: c.p[2] * 2, opacity: 1 }, { x: c.p[0], y: c.p[1], rotation: c.p[2], duration: ENTER + c.a, ease: "back.out(1.6)" }, 0);
          } else {
            tl.fromTo(c.el, { x: c.s[0], y: c.s[1], rotation: c.p[2] * 3, opacity: 1 }, { x: c.p[0], y: c.p[1], rotation: c.p[2], duration: ENTER, ease: "back.out(1.6)", immediateRender: true }, c.a);
          }
          tl.to(c.el, { rotation: c.p[2] * -0.6, duration: 0.12, ease: "sine.inOut", yoyo: true, repeat: 1 }, 1.05 + rnd() * 0.15);
          // 1.8-2.15: sucked into the centre
          tl.to(c.el, { x: 540 - c.el.offsetWidth / 2, y: 900, scale: 0.05, rotation: c.p[2] * 8, filter: "blur(6px)", duration: 0.32, ease: "power3.in" }, 1.8 + rnd() * 0.06);
          tl.to(c.el, { opacity: 0, duration: 0.01 }, 2.16);
          // 19.5-20: back to the frame-0 chaos for a seamless loop
          if (c.a < 0) {
            tl.fromTo(c.el, { x: c.s[0], y: c.s[1], scale: 1, opacity: 1, rotation: c.p[2] * 3, filter: "blur(0px)" }, { x: c.f0[0], y: c.f0[1], rotation: c.p[2] * 2, duration: 0.5, ease: "power2.out", immediateRender: false }, 19.5);
          } else {
            tl.set(c.el, { x: c.s[0], y: c.s[1], scale: 1, opacity: 1, rotation: c.p[2] * 3, filter: "blur(0px)" }, 19.5);
          }
        });
        // headline swap + implosion
        tl.fromTo("#t-hook", { scale: 1 }, { scale: 1.04, duration: 1.4, ease: "sine.inOut" }, 0);
        tl.to("#t-hook", { opacity: 0, scale: 0.8, duration: 0.1, ease: "power2.in" }, 1.42);
        tl.fromTo("#t-knot", { opacity: 0, scale: 1.35 }, { opacity: 1, scale: 1, duration: 0.25, ease: SPRING }, 1.5);
        tl.fromTo("#burst", { opacity: 0.9, scale: 0.1 }, { opacity: 0, scale: 2.6, duration: 0.4, ease: "power2.out", immediateRender: false }, 2.15);
        tl.to("#t-knot", { scale: 1.06, duration: 0.6, ease: "sine.in" }, 2.2);
        tl.to("#t-knot", { opacity: 0, scale: 1.4, filter: "blur(10px)", duration: 0.12, ease: "power2.in" }, 2.88);
        tl.to("#s1", { opacity: 0, duration: 0.01 }, 3.0);

        // ---------- 3-4.5 answer: punch 0.85 -> 1.08 -> 1
        tl.fromTo("#s2", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 3.0);
        tl.fromTo("#ans", { scale: 0.85, filter: "blur(8px)" }, { scale: 1.08, filter: "blur(0px)", duration: 0.12, ease: "power3.out" }, 3.0);
        tl.to("#ans", { scale: 1, duration: 0.2, ease: "back.out(2.5)" }, 3.12);
        tl.fromTo("#cname", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.25, ease: SPRING }, 3.5);
        tl.to("#s2", { opacity: 0, scale: 1.15, filter: "blur(10px)", duration: 0.12, ease: "power2.in" }, 4.38);

        // ---------- 4.5-9 tool cuts, one every 1.5 beats
        const CUTS = [["Claude", "#3a2a24"], ["NotebookLM", "#2c3320"], ["Runway", "#2c2444"], ["Gamma", "#1d3338"], ["Midjourney", "#22284a"], ["n8n", "#3c2232"]];
        const nbox = document.getElementById("tool-name");
        tl.fromTo("#s3", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 4.5);
        const dots = gsap.utils.toArray("#dots b");
        CUTS.forEach(function (c, i) {
          const t = 4.5 + i * 0.75;
          const n = document.createElement("div");
          n.className = "tname";
          n.textContent = c[0];
          nbox.appendChild(n);
          const span = document.createElement("span");
          span.textContent = c[0];
          span.style.cssText = "position:absolute;visibility:hidden;white-space:nowrap;font:900 160px Vazirmatn";
          document.body.appendChild(span);
          const w = span.offsetWidth;
          span.remove();
          if (w > 860) n.style.fontSize = Math.floor((160 * 860) / w) + "px"; // keep long names inside x 90-990
          tl.fromTo(n, { opacity: 1, scale: 1.25, filter: "blur(10px)" }, { scale: 1, filter: "blur(0px)", duration: 0.2, ease: SPRING, immediateRender: false }, t);
          if (i < CUTS.length - 1) tl.to(n, { opacity: 0, duration: 0.01 }, t + 0.75);
          // card jumps up and flips like a page, new tone per tool
          tl.fromTo("#card", { y: 140, rotationX: -70, backgroundColor: c[1] }, { y: 0, rotationX: 0, backgroundColor: c[1], duration: 0.28, ease: "back.out(1.5)", immediateRender: i === 0 }, t);
          gsap.utils.toArray("#card .tick i").forEach(function (k, j) {
            tl.fromTo(k, { scale: 0.3 }, { scale: 1, duration: 0.18, ease: "back.out(3)", immediateRender: false }, t + 0.06 + j * 0.06);
          });
          tl.fromTo(dots[i], { backgroundColor: "rgba(245,247,255,0.28)", width: 26 }, { backgroundColor: "#f5f7ff", width: 70, duration: 0.15, immediateRender: false }, t);
          if (i > 0) tl.to(dots[i - 1], { backgroundColor: "rgba(245,247,255,0.28)", width: 26, duration: 0.15 }, t);
        });
        tl.to("#s3", { opacity: 0, x: 120, filter: "blur(10px)", duration: 0.12, ease: "power2.in" }, 8.88);

        // ---------- 9-13 four full-screen features, swipe with motion blur
        tl.fromTo("#s4", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 9.0);
        const bars = gsap.utils.toArray("#fidx b");
        ["#f1", "#f2", "#f3", "#f4"].forEach(function (f, i) {
          const t = 9.0 + i;
          tl.fromTo(f, { opacity: 1, x: -1080, skewX: 8, filter: "blur(14px)" }, { x: 0, skewX: 0, filter: "blur(0px)", duration: 0.24, ease: "power3.out", immediateRender: i === 0 }, t);
          tl.fromTo(f + " .ico", { scale: 0.6, rotation: -8 }, { scale: 1, rotation: 0, duration: 0.3, ease: SPRING }, t + 0.05);
          tl.fromTo(f + " .flabel", { scale: 1.12 }, { scale: 1, duration: 0.25, ease: SPRING }, t + 0.08);
          tl.fromTo(bars[i], { backgroundColor: "rgba(245,247,255,0.25)" }, { backgroundColor: "#f5f7ff", duration: 0.1, immediateRender: false }, t);
          if (i < 3) tl.to(f, { x: 1080, skewX: -8, filter: "blur(14px)", duration: 0.22, ease: "power3.in" }, t + 0.82);
        });
        tl.to("#s4", { opacity: 0, x: 1080, filter: "blur(14px)", duration: 0.2, ease: "power3.in" }, 12.82);

        // ---------- 13-15 not alone
        tl.fromTo("#s5", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 13.0);
        tl.fromTo("#alone", { scale: 0.85, filter: "blur(8px)" }, { scale: 1, filter: "blur(0px)", duration: 0.25, ease: SPRING }, 13.0);
        tl.fromTo("#tg", { opacity: 0, y: 260 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }, 13.3);
        tl.fromTo("#tg-input", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.25, ease: SPRING }, 13.2);
        tl.fromTo("#tg-msg img", { rotation: -20 }, { rotation: 20, duration: 0.18, yoyo: true, repeat: 5, ease: "sine.inOut", transformOrigin: "70% 90%" }, 13.7);
        tl.to("#s5", { opacity: 0, scale: 1.1, filter: "blur(10px)", duration: 0.12, ease: "power2.in" }, 14.88);

        // ---------- 15-19.5 CTA
        tl.fromTo("#s6", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 15.0);
        tl.fromTo("#c1", { scale: 0.8, filter: "blur(8px)" }, { scale: 1, filter: "blur(0px)", duration: 0.25, ease: SPRING }, 15.0);
        tl.fromTo("#kw", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(2.2)" }, 15.25);
        for (let t = 15.75; t < 19.4; t += B) {
          tl.fromTo("#kw", { scale: 1.06, boxShadow: "0 0 80px rgba(255,181,71,0.85), inset 0 0 40px rgba(255,181,71,0.3)" },
            { scale: 1, boxShadow: "0 0 40px rgba(255,181,71,0.45), inset 0 0 30px rgba(255,181,71,0.18)", duration: 0.42, ease: "power2.out", immediateRender: false }, t);
        }
        tl.fromTo("#c3", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: SPRING }, 15.75);
        gsap.utils.toArray("#ctags span").forEach(function (s, i) {
          tl.fromTo(s, { opacity: 0, y: 30, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.25, ease: "back.out(2.2)" }, 16.25 + i * 0.25);
        });
        tl.fromTo("#csign", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.25, ease: SPRING }, 16.75);
        tl.fromTo("#clink", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.28, ease: "back.out(2)" }, 17.0);
        tl.fromTo("#arrow", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.25, ease: SPRING }, 16.0);
        for (let t = 16.5; t < 19.4; t += B) {
          tl.fromTo("#arrow", { y: 0 }, { y: 30, duration: 0.25, ease: "power2.in", yoyo: true, repeat: 1, immediateRender: false }, t);
        }
        tl.to("#s6", { opacity: 0, scale: 0.9, filter: "blur(10px)", duration: 0.12, ease: "power2.in" }, 19.4);

        // ---------- 19.5-20 loop back to the opening chaos
        tl.set("#s1", { opacity: 1 }, 19.5);
        tl.set("#t-knot", { opacity: 0, scale: 1, filter: "blur(0px)" }, 19.5);
        tl.fromTo("#t-hook", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.25, ease: SPRING, immediateRender: false }, 19.62);

        window.__timelines = window.__timelines || {};
        window.__timelines["main"] = tl;
      })();
    </script>
  </body>
</html>
