    <script>
      (function () {
        const B = 0.5; // one beat at 120 BPM
        const tl = gsap.timeline({ paused: true });

        // word spans for word-by-word motion (Persian words stay whole)
        document.querySelectorAll(".split").forEach(function (el) {
          const grad = el.classList.contains("g-words");
          el.innerHTML = el.textContent.trim().split(/\s+/).map(function (w) {
            return '<span class="w' + (grad ? " g" : "") + '">' + w + "</span>";
          }).join(" ");
        });
        function words(sel, t, step, from) {
          gsap.utils.toArray(sel + " .w").forEach(function (w, i) {
            tl.fromTo(w, Object.assign({ opacity: 0, y: 60 }, from || {}), { opacity: 1, y: 0, scale: 1, duration: 0.32, ease: "power4.out" }, t + i * step);
          });
        }
        function flash(t, a) {
          tl.fromTo("#flash", { opacity: a || 0.5 }, { opacity: 0, duration: 0.45, ease: "power2.out", immediateRender: false }, t);
        }

        // ---------- S1 hook (0-4): too many tools ----------
        const TOOLS = [
          ["ChatGPT", "#91ffea", 150, 150], ["Claude", "#ffbf86", 1480, 130], ["Gemini", "#77caff", 820, 90],
          ["Midjourney", "#b39aff", 260, 820], ["Perplexity", "#91ffea", 1380, 850], ["NotebookLM", "#ddf998", 70, 340],
          ["Copilot", "#77caff", 1600, 660], ["Cursor", "#ff94ba", 560, 250], ["n8n", "#ff94ba", 1180, 290],
          ["Suno", "#ffbf86", 700, 900], ["Runway", "#b39aff", 1080, 760], ["DeepSeek", "#77caff", 420, 640],
          ["Canva AI", "#ddf998", 1300, 640], ["Gamma", "#91ffea", 960, 960],
        ];
        const box = document.querySelector("#s1-chips");
        TOOLS.forEach(function (t) {
          const el = document.createElement("div");
          el.className = "chip";
          el.style.setProperty("--c", t[1]);
          el.style.left = t[2] + "px";
          el.style.top = t[3] + "px";
          el.innerHTML = "<i></i><span>" + t[0] + "</span>";
          box.appendChild(el);
        });
        const chips = gsap.utils.toArray("#s1 .chip");
        tl.fromTo("#s1", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0);
        tl.fromTo("#s1-cam", { scale: 1.15 }, { scale: 1.0, duration: 4.3, ease: "sine.out" }, 0);
        tl.fromTo("#s1-a", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 0.15);
        chips.forEach(function (el, i) {
          const at = 0.25 + i * (B / 4);
          tl.fromTo(el, { opacity: 0, scale: 0.3, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, at);
          const cx = 960 - (parseFloat(el.style.left) + 120);
          const cy = 540 - (parseFloat(el.style.top) + 30);
          tl.to(el, { x: cx * 0.18, y: cy * 0.18, duration: 3.3 - i * 0.12, ease: "sine.in" }, at + 0.35);
          tl.to(el, { opacity: 0, scale: 0.5, filter: "blur(10px)", x: cx * 0.6, y: cy * 0.6, duration: 0.35, ease: "power3.in" }, 3.6 + (i % 4) * 0.03);
        });
        tl.to("#s1-a", { opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }, 1.75);
        tl.fromTo("#s1-b", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power4.out" }, 2.0);
        tl.to("#s1-b", { scale: 1.06, duration: 1.3, ease: "sine.in" }, 2.4);
        tl.to("#s1-b", { opacity: 0, scale: 1.6, filter: "blur(12px)", duration: 0.3, ease: "power3.in" }, 3.75);
        tl.to("#s1", { opacity: 0, duration: 0.3 }, 4.0);

        // ---------- S2 (4-8): you don't have to go alone ----------
        flash(4.0, 0.55);
        tl.fromTo("#glow", { opacity: 0 }, { opacity: 1, duration: 0.6 }, 4.0);
        tl.fromTo("#s2", { opacity: 0 }, { opacity: 1, duration: 0.15 }, 4.0);
        tl.fromTo("#s2-cam", { scale: 1.2 }, { scale: 1.02, duration: 4.3, ease: "power2.out" }, 4.0);
        tl.fromTo("#s2-a", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "power4.out" }, 4.0);
        words("#s2-b", 4.5, B, { scale: 0.9 });
        tl.to("#s2-copy", { scale: 1.05, duration: 1.7, ease: "sine.inOut" }, 6.0);
        tl.to("#s2-copy", { opacity: 0, y: -40, duration: 0.3, ease: "power2.in" }, 7.75);
        tl.to("#s2", { opacity: 0, duration: 0.3 }, 8.0);

        // ---------- SL (8-16): practical daily lessons on every AI tool ----------
        flash(8.0, 0.3);
        tl.fromTo("#sl", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 8.0);
        tl.fromTo("#sl-eye", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }, 8.05);
        gsap.utils.toArray("#sl-title .w").forEach(function (w, i) {
          tl.fromTo(w, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, ease: "power4.out" }, 8.25 + i * (B / 2));
        });
        tl.fromTo("#sl-sub", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 10.0);
        tl.fromTo("#sl-card", { opacity: 0, x: -100, scale: 0.94 }, { opacity: 1, x: 0, scale: 1, duration: 0.5, ease: "power4.out" }, 8.5);
        const names = gsap.utils.toArray("#sl .sl-name");
        const gchips = gsap.utils.toArray("#sl .sl-chip");
        gchips.forEach(function (c, i) {
          tl.fromTo(c, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, 8.75 + i * (B / 8));
        });
        names.forEach(function (n, i) {
          const t = 9.0 + i * B; // one tool per beat: every tool gets its lesson
          tl.fromTo(n, { opacity: 0, y: 50, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.2, ease: "power4.out" }, t);
          if (i < names.length - 1) tl.to(n, { opacity: 0, y: -40, duration: 0.15, ease: "power2.in" }, t + B - 0.15);
          tl.fromTo(gchips[i], { color: "rgba(239, 244, 255, 0.55)", borderColor: "rgba(255, 255, 255, 0.14)" },
            { color: "#eff4ff", borderColor: "rgba(137, 255, 240, 0.8)", duration: 0.15, immediateRender: false }, t);
        });
        gsap.utils.toArray("#sl .sl-step").forEach(function (st, i) {
          const t = 10.5 + i * 1.0;
          tl.fromTo(st, { opacity: 0.35 }, { opacity: 1, duration: 0.25 }, t);
          tl.fromTo(st.querySelector("i"), { backgroundColor: "rgba(137,255,240,0)", borderColor: "rgba(255,255,255,0.25)" },
            { backgroundColor: "#89fff0", borderColor: "#89fff0", duration: 0.25, ease: "power2.out" }, t);
          tl.fromTo(st.querySelector("i b"), { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(3)" }, t);
        });
        tl.to(["#sl-card", "#sl-grid", "#sl-copy"], { opacity: 0, filter: "blur(8px)", duration: 0.3, ease: "power2.in" }, 15.75);
        tl.to("#sl", { opacity: 0, duration: 0.3 }, 16.0);

        // ---------- S3 (16-24): you are not alone (music breakdown) ----------
        tl.fromTo("#s3", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 16.0);
        const DOTS = [[1480, 880, 34, "#91ffea"], [1760, 800, 22, "#b39aff"], [1240, 860, 26, "#ffbf86"], [1820, 880, 18, "#77caff"],
          [1000, 140, 20, "#ff94ba"], [1380, 120, 28, "#ddf998"], [1720, 160, 16, "#91ffea"], [900, 920, 22, "#b39aff"]];
        const dbox = document.querySelector("#s3-dots");
        DOTS.forEach(function (d) {
          const el = document.createElement("div");
          el.className = "dot";
          el.style.cssText = "left:" + d[0] + "px;top:" + d[1] + "px;width:" + d[2] + "px;height:" + d[2] + "px;--c:" + d[3];
          dbox.appendChild(el);
        });
        tl.fromTo("#s3-eye", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 16.1);
        words("#s3-a", 16.5, B / 2);
        words("#s3-b", 18.0, B / 2);
        gsap.utils.toArray("#s3 .dot").forEach(function (el, i) {
          tl.fromTo(el, { opacity: 0, scale: 0 }, { opacity: 0.9, scale: 1, duration: 0.4, ease: "back.out(3)" }, 18.0 + i * (B / 4));
          tl.to(el, { y: (i % 2 ? -1 : 1) * 30, duration: 4, ease: "sine.inOut" }, 18.4 + i * 0.05);
        });
        tl.fromTo("#s3-chat", { opacity: 0, y: 60, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, 19.0);
        gsap.utils.toArray("#s3-typing b").forEach(function (el, i) {
          tl.fromTo(el, { y: 0 }, { y: -8, duration: 0.15, ease: "sine.inOut", yoyo: true, repeat: 1 }, 19.3 + i * 0.12);
          tl.fromTo(el, { y: 0 }, { y: -8, duration: 0.15, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false }, 19.62 + i * 0.12);
        });
        tl.to("#s3-typing", { opacity: 0, scale: 0.8, duration: 0.15 }, 19.9);
        tl.fromTo("#s3-msg", { opacity: 0, scale: 0.6, y: 20 }, { opacity: 1, scale: 1, y: 0, duration: 0.45, ease: "back.out(2)" }, 20.0);
        tl.to("#s3-msg", { boxShadow: "0 0 50px rgba(137,255,240,0.35)", duration: 1.0, ease: "sine.inOut", yoyo: true, repeat: 1 }, 20.5);
        // snare roll: tension, then suck into the drop
        tl.to(["#s3-copy", "#s3-chat"], { scale: 0.96, duration: 1.7, ease: "sine.in" }, 22.0);
        tl.to(["#s3-copy", "#s3-chat", "#s3-dots"], { opacity: 0, scale: 1.25, filter: "blur(10px)", duration: 0.3, ease: "power3.in" }, 23.72);
        tl.to("#s3", { opacity: 0, duration: 0.3 }, 24.0);

        // ---------- S4 (24-32, the drop): what you get ----------
        flash(24.0, 0.7);
        tl.fromTo("#s4", { opacity: 0 }, { opacity: 1, duration: 0.12 }, 24.0);
        tl.fromTo("#s4-eye", { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }, 24.1);
        ["#f1", "#f2", "#f3", "#f4"].forEach(function (f, i) {
          const t0 = 24.0 + i * 2.0;
          tl.fromTo(f, { opacity: 0 }, { opacity: 1, duration: 0.12 }, t0);
          tl.fromTo(f + " .f-title", { opacity: 0, x: 120, filter: "blur(8px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.4, ease: "power4.out" }, t0);
          tl.fromTo(f + " .f-sub, " + f + " .badge", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, t0 + B);
          tl.fromTo(f + " .f-vis", { opacity: 0, x: -120, scale: 0.92 }, { opacity: 1, x: 0, scale: 1, duration: 0.45, ease: "power4.out" }, t0 + 0.05);
          if (i < 3) {
            tl.to(f, { opacity: 0, x: -60, filter: "blur(8px)", duration: 0.2, ease: "power2.in" }, t0 + 1.8);
          }
        });
        gsap.utils.toArray("#f1 .doc").forEach(function (d, i) {
          tl.fromTo(d, { rotation: 0, x: 0, y: 40 }, { rotation: (i - 1) * 10, x: (i - 1) * 150, y: Math.abs(i - 1) * 24, duration: 0.5, ease: "back.out(1.6)" }, 24.15 + i * (B / 4));
        });
        gsap.utils.toArray("#days .day").forEach(function (d, i) {
          tl.fromTo(d, { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, 26.05 + i * (B / 6));
        });
        gsap.utils.toArray("#days .day.on").forEach(function (d, i) {
          tl.fromTo(d, { scale: 1 }, { scale: 1.08, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }, 26.75 + i * B);
        });
        tl.fromTo("#sim-video", { scale: 1.15 }, { scale: 1.0, duration: 2.0, ease: "power2.out" }, 28.0);
        tl.fromTo("#f3 .badge", { scale: 1 }, { scale: 1.07, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, 29.0);
        tl.fromTo("#ring-arc", { strokeDashoffset: 1257 }, { strokeDashoffset: 0, duration: 1.5, ease: "power2.inOut" }, 30.1);
        tl.fromTo("#ring-num b", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, 30.2);
        tl.to("#s4", { opacity: 0, scale: 1.04, duration: 0.3, ease: "power2.in" }, 31.75);

        // beat pulse on the background glow: kick on every beat 4-16 and 24-38
        for (let t = 4.0; t < 38.0; t += B) {
          if (t >= 16 && t < 24) continue;
          const strong = t >= 24 && t < 32;
          tl.fromTo("#glow", { scale: strong ? 1.12 : 1.06 }, { scale: 1.0, duration: 0.42, ease: "power2.out", immediateRender: false }, t);
        }

        // ---------- S5 (32-40): invite to the Telegram group ----------
        flash(32.0, 0.45);
        tl.fromTo("#s5", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 32.0);
        tl.fromTo("#s5-cam", { scale: 1.12 }, { scale: 1.0, duration: 8, ease: "sine.out" }, 32.0);
        tl.fromTo("#s5-eye", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, 32.1);
        gsap.utils.toArray("#s5-title .w").forEach(function (w, i) {
          tl.fromTo(w, { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 0.3, ease: "power4.out" }, 32.5 + i * B);
        });
        tl.fromTo("#s5-sub", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 34.0);
        tl.fromTo("#s5-qr", { opacity: 0, scale: 0.5, rotation: -6 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.6)" }, 33.6);
        tl.fromTo("#s5-link", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, 34.5);
        tl.fromTo("#s5-link .plane", { rotation: -40, x: -30 }, { rotation: 0, x: 0, duration: 0.6, ease: "back.out(2.4)" }, 34.6);
        tl.fromTo("#s5-sign", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 35.5);
        tl.fromTo("#s5-sign i", { scaleY: 0 }, { scaleY: 1, duration: 0.45, ease: "expo.out" }, 35.7);
        tl.fromTo(
          "#s5-qr",
          { boxShadow: "0 0 0 3px rgba(137, 255, 240, 0.6), 0 40px 120px rgba(0, 0, 0, 0.6)" },
          { boxShadow: "0 0 0 3px rgba(137, 255, 240, 1), 0 0 140px rgba(137, 255, 240, 0.5)", duration: 1.0, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false },
          35.0,
        );
        tl.to("#glow", { opacity: 0, duration: 1.0 }, 38.5);
        tl.to("#s5", { opacity: 0, duration: 1.0, ease: "power1.inOut" }, 39.0);

        window.__timelines = window.__timelines || {};
        window.__timelines["main"] = tl;
      })();
    </script>